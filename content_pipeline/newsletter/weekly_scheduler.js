/**
 * WEEKLY NEWSLETTER SCHEDULER
 * Schedules newsletter generation from research cycles
 * 
 * Usage: node weekly_scheduler.js [--dry-run] [--force]
 * 
 * This should be called by a cron job or Windows Task Scheduler:
 * - Weekly on Sunday at 08:00 Paris time
 * - Or manually via: node weekly_scheduler.js --force
 */

const fs = require('fs');
const path = require('path');
const { generateNewsletter } = require('./newsletter_generator');

const CONFIG = {
  SCHEDULE_FILE: path.join(__dirname, 'schedule.json'),
  LOG_FILE: path.join(__dirname, 'output', 'generation_log.json')
};

// Check if today is newsletter day (Sunday = 0)
function isNewsletterDay() {
  const now = new Date();
  const parisTime = new Date(now.toLocaleString('en-US', { timeZone: 'Europe/Paris' }));
  return parisTime.getDay() === 0; // Sunday
}

// Check if newsletter already generated this week
function isAlreadyGenerated() {
  try {
    if (!fs.existsSync(CONFIG.SCHEDULE_FILE)) return false;
    const schedule = JSON.parse(fs.readFileSync(CONFIG.SCHEDULE_FILE, 'utf8'));
    const now = new Date();
    const thisWeek = getWeekStart(now);
    return schedule.last_generated === thisWeek;
  } catch (e) {
    return false;
  }
}

// Get week start date (Sunday)
function getWeekStart(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day;
  return new Date(d.setDate(diff)).toISOString().split('T')[0];
}

// Update schedule
function updateSchedule() {
  const schedule = {
    last_generated: getWeekStart(new Date()),
    next_generation: getNextSunday(),
    timezone: 'Europe/Paris'
  };
  fs.writeFileSync(CONFIG.SCHEDULE_FILE, JSON.stringify(schedule, null, 2));
  return schedule;
}

// Get next Sunday
function getNextSunday() {
  const now = new Date();
  const next = new Date(now);
  next.setDate(now.getDate() + (7 - now.getDay()));
  return next.toISOString().split('T')[0];
}

// Log generation
function logGeneration(result, options = {}) {
  const log = {
    timestamp: new Date().toISOString(),
    date: result.date,
    output_path: result.outputPath,
    archive_path: result.archivePath,
    sections: Object.keys(result.sections),
    triggered_by: options.force ? 'manual' : 'scheduled',
    success: true
  };

  let logs = [];
  if (fs.existsSync(CONFIG.LOG_FILE)) {
    logs = JSON.parse(fs.readFileSync(CONFIG.LOG_FILE, 'utf8'));
  }
  logs.push(log);
  fs.writeFileSync(CONFIG.LOG_FILE, JSON.stringify(logs, null, 2));
  return log;
}

// Main scheduler
async function runScheduler(options = {}) {
  console.log('📅 Weekly Newsletter Scheduler\n');
  console.log(`Current time (Paris): ${new Date().toLocaleString('en-US', { timeZone: 'Europe/Paris' })}`);
  console.log(`Newsletter day (Sunday): ${isNewsletterDay() ? 'YES ✅' : 'NO'}`);
  console.log(`Already generated: ${isAlreadyGenerated() ? 'YES ✅' : 'NO'}\n`);

  // Force mode: generate regardless of schedule
  if (options.force) {
    console.log('⚡ Force mode enabled — generating newsletter...\n');
  } else if (!isNewsletterDay()) {
    console.log('⏭️ Not newsletter day. Exiting.');
    console.log('Use --force to generate anyway.');
    return { generated: false, reason: 'not_newsletter_day' };
  } else if (isAlreadyGenerated()) {
    console.log('✅ Newsletter already generated this week. Exiting.');
    console.log('Use --force to regenerate.');
    return { generated: false, reason: 'already_generated' };
  }

  // Dry run: show what would happen
  if (options.dryRun) {
    console.log('🔍 DRY RUN — Would generate newsletter now');
    console.log('   Sections: Highlights, Market Snapshot, Asset Analysis, Alternative Data, Composite Ratings, Key Takeaways');
    console.log('   Output: content_pipeline/newsletter/output/');
    console.log('   Archive: content_pipeline/newsletter/output/archive/');
    return { generated: false, reason: 'dry_run' };
  }

  // Generate newsletter
  try {
    const result = await generateNewsletter();
    const schedule = updateSchedule();
    const log = logGeneration(result, options);

    console.log('\n✅ Newsletter generation complete!');
    console.log(`📄 Output: ${result.outputPath}`);
    console.log(`📁 Archive: ${result.archivePath}`);
    console.log(`📅 Next generation: ${schedule.next_generation}`);

    return {
      generated: true,
      result,
      schedule,
      log
    };
  } catch (e) {
    console.error('❌ Generation failed:', e.message);
    return { generated: false, reason: 'error', error: e.message };
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const force = args.includes('--force');
  const dryRun = args.includes('--dry-run');

  const result = await runScheduler({ force, dryRun });
  
  if (!result.generated) {
    process.exit(0); // Not an error
  }
}

module.exports = { runScheduler, isNewsletterDay, isAlreadyGenerated };

if (require.main === module) main();
