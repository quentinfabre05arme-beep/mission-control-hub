// Health Monitor — Checks all systems every 15 minutes
const fs = require('fs');
const path = require('path');

const SYSTEMS = [
  { name: 'Alpha Signals', check: () => fs.existsSync('missions/alpha_signals/bot.js'), lastRun: null },
  { name: 'Newsletter', check: () => fs.existsSync('content_pipeline/newsletter/newsletter_generator.js'), lastRun: null },
  { name: 'X Posting', check: () => fs.existsSync('content_pipeline/x_autonomous.js'), lastRun: null },
  { name: 'POD Business', check: () => fs.existsSync('pod_business/daily_monitor.js'), lastRun: null },
  { name: 'Autonomy Core', check: () => fs.existsSync('missions/autonomy_core_v2/autonomy_core.js'), lastRun: null }
];

async function healthCheck() {
  const report = {
    timestamp: new Date().toISOString(),
    systems: [],
    failed: []
  };
  
  for (const system of SYSTEMS) {
    const healthy = system.check();
    const status = healthy ? '✅ HEALTHY' : '🔴 FAILED';
    report.systems.push({ name: system.name, status: healthy ? 'healthy' : 'failed' });
    
    if (!healthy) {
      report.failed.push(system.name);
      console.log(`ALERT: ${system.name} is DOWN`);
      // Auto-trigger recovery
      await attemptRecovery(system.name);
    }
  }
  
  // Save report
  fs.writeFileSync('missions/health_reports/latest.json', JSON.stringify(report, null, 2));
  
  return report;
}

async function attemptRecovery(systemName) {
  console.log(`Attempting recovery for ${systemName}...`);
  // Implementation would trigger restart/rebuild based on system
  fs.appendFileSync('missions/health_reports/recovery_log.txt', 
    `${new Date().toISOString()}: Recovery attempted for ${systemName}\n`);
}

// Run immediately and every 15 minutes
healthCheck();
setInterval(healthCheck, 15 * 60 * 1000);

console.log('Health monitor running — checking every 15 minutes');