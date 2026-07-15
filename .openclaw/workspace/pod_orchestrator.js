// pod_orchestrator.js - Main controller for autonomous POD business
// Coordinates trend discovery, design generation, publishing, and sales tracking

const path = require('path');

// Import modules
const trendEngine = require('./pod_trend_engine');
const designFactory = require('./pod_design_factory');
const mockupGenerator = require('./pod_mockup_generator');
const salesTracker = require('./pod_sales_tracker');

const CONFIG = {
  dailyDesignQuota: 5,      // Designs to generate per day
  weeklyReportDay: 0,        // Sunday (0-6)
  autoPublish: false,       // Set to true when Printify API is configured
  logFile: 'pod_business.log'
};

async function log(msg) {
  const ts = new Date().toISOString();
  const logLine = `[${ts}] [POD-ORCH] ${msg}`;
  console.log(logLine);
  // Would append to log file in production
}

// Phase 1: Discover trends
async function phase1_discoverTrends() {
  log('=== Phase 1: Trend Discovery ===');
  try {
    const result = await trendEngine.main();
    log(`Discovered ${result.trendsFound} new trends`);
    log(`${result.totalActive} active trends ready`);
    return result;
  } catch (err) {
    log(`Trend discovery failed: ${err.message}`);
    return null;
  }
}

// Phase 2: Generate designs
async function phase2_generateDesigns() {
  log('=== Phase 2: Design Generation ===');
  try {
    const designs = await designFactory.generateBatch(CONFIG.dailyDesignQuota);
    log(`Generated ${designs.length} new designs`);
    
    // Log each design
    designs.forEach(d => {
      log(`  ✓ ${d.id}: "${d.concept.text}"`);
    });
    
    return designs;
  } catch (err) {
    log(`Design generation failed: ${err.message}`);
    return [];
  }
}

// Phase 3: Create mockups and listings
async function phase3_createMockups(designs) {
  log('=== Phase 3: Mockup \u0026 Listing Generation ===');
  const results = [];
  
  for (const design of designs) {
    try {
      // Generate product mockups
      const mockups = await mockupGenerator.generateMockups(design.id);
      log(`  ✓ ${design.id}: ${mockups.length} mockups created`);
      
      // Generate Redbubble listing
      const listing = await mockupGenerator.generateRedbubbleListing(design.id);
      log(`  ✓ Redbubble listing ready: ${listing.title}`);
      
      results.push({ designId: design.id, mockups, listing });
      
    } catch (err) {
      log(`  ✗ ${design.id}: ${err.message}`);
    }
  }
  
  return results;
}

// Phase 4: Auto-publish (Printify only)
async function phase4_autoPublish(designs) {
  if (!CONFIG.autoPublish) {
    log('=== Phase 4: Auto-Publish (SKIPPED) ===');
    log('Set autoPublish=true when Printify API key is configured');
    return [];
  }
  
  log('=== Phase 4: Auto-Publish to Printify ===');
  const results = [];
  
  for (const design of designs) {
    try {
      const result = await mockupGenerator.publishToPrintify(design.id);
      if (result.status === 'success') {
        log(`  ✓ Published ${design.id} to Printify`);
        results.push({ designId: design.id, status: 'published' });
      } else {
        log(`  ✗ Failed to publish ${design.id}: ${result.message}`);
      }
    } catch (err) {
      log(`  ✗ Error publishing ${design.id}: ${err.message}`);
    }
  }
  
  return results;
}

// Phase 5: Generate report (if Sunday)
async function phase5_weeklyReport() {
  const today = new Date().getDay();
  if (today !== CONFIG.weeklyReportDay) {
    return null;
  }
  
  log('=== Phase 5: Weekly Report ===');
  try {
    const report = await salesTracker.generateWeeklyReport();
    const projection = await salesTracker.generateProjection();
    
    log(`\n--- Weekly Summary ---`);
    log(`Sales: ${report.summary.totalSales}`);
    log(`Revenue: $${report.summary.totalRevenue}`);
    log(`Profit: $${report.summary.totalProfit}`);
    log(`\nMonthly Projection: $${projection.monthlyProjection}`);
    log(`Yearly Projection: $${projection.yearlyProjection}`);
    
    return { report, projection };
  } catch (err) {
    log(`Report generation failed: ${err.message}`);
    return null;
  }
}

// Full daily cycle
async function runDailyCycle() {
  log('\n==============================================');
  log('  AUTONOMOUS POD BUSINESS - DAILY CYCLE');
  log('==============================================\n');
  
  const startTime = Date.now();
  
  // Phase 1: Trends
  const trends = await phase1_discoverTrends();
  
  // Phase 2: Designs
  const designs = await phase2_generateDesigns();
  
  // Phase 3: Mockups
  const mockups = await phase3_createMockups(designs);
  
  // Phase 4: Publishing
  const published = await phase4_autoPublish(designs);
  
  // Phase 5: Reporting (Sunday only)
  const report = await phase5_weeklyReport();
  
  // Summary
  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  log('\n==============================================');
  log('  DAILY CYCLE COMPLETE');
  log(`  Duration: ${duration}s`);
  log(`  Trends: ${trends?.trendsFound || 0} new`);
  log(`  Designs: ${designs.length} generated`);
  log(`  Mockups: ${mockups.length} created`);
  log(`  Published: ${published.length} to Printify`);
  log(`  Report: ${report ? 'Generated' : 'Skipped (not Sunday)'}`);
  log('==============================================\n');
  
  return {
    trends,
    designs,
    mockups,
    published,
    report,
    duration
  };
}

// Manual operations
async function manual_operations() {
  const command = process.argv[2];
  
  switch(command) {
    case 'trends':
      await trendEngine.main();
      break;
      
    case 'design':
      await designFactory.generateBatch();
      break;
      
    case 'mockup':
      const designId = process.argv[3];
      if (designId) {
        await mockupGenerator.generateMockups(designId);
      } else {
        console.log('Usage: node pod_orchestrator.js mockup [designId]');
      }
      break;
      
    case 'publish':
      const pubDesignId = process.argv[3];
      if (pubDesignId) {
        await mockupGenerator.publishToPrintify(pubDesignId);
      } else {
        console.log('Usage: node pod_orchestrator.js publish [designId]');
      }
      break;
      
    case 'report':
      await salesTracker.generateWeeklyReport();
      break;
      
    case 'sales':
      const count = parseInt(process.argv[3]) || 10;
      await salesTracker.simulateSales(count);
      break;
      
    case 'analytics':
      const analytics = await salesTracker.generateAnalytics(30);
      console.log(JSON.stringify(analytics, null, 2));
      break;
      
    default:
      console.log(`
POD Business Orchestrator

Usage: node pod_orchestrator.js [command]

Commands:
  trends      - Discover trending niches
  design      - Generate designs from trends
  mockup [id] - Create mockups for design
  publish [id]- Publish to Printify
  report      - Generate weekly report
  sales [n]   - Simulate n sales (testing)
  analytics   - Show analytics dashboard
  (no command)- Run full daily cycle
`);
  }
}

// Main entry
if (require.main === module) {
  if (process.argv.length > 2) {
    // Manual operation mode
    manual_operations().catch(console.error);
  } else {
    // Full autonomous cycle
    runDailyCycle().catch(console.error);
  }
}

module.exports = {
  runDailyCycle,
  phase1_discoverTrends,
  phase2_generateDesigns,
  phase3_createMockups,
  phase4_autoPublish,
  phase5_weeklyReport
};
