// pod_sales_tracker.js - Monitor sales across platforms and generate reports
// Tracks revenue, calculates profits, and optimizes based on performance

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  dataDir: 'C:\\Users\\quent\\.openclaw\workspace\\pod_business',
  salesFile: 'sales_data.json',
  reportDir: 'reports',
  platforms: ['printify', 'redbubble', 'teespring']
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true }).catch(() => {});
}

async function log(msg) {
  console.log(`[POD-SALES] ${msg}`);
}

// Initialize sales data structure
async function initSalesData() {
  return {
    sales: [],
    designs: {},
    monthlyRevenue: {},
    platformPerformance: {},
    lastUpdate: null
  };
}

async function loadSalesData() {
  try {
    const data = await fs.readFile(path.join(CONFIG.dataDir, CONFIG.salesFile), 'utf-8');
    return JSON.parse(data);
  } catch {
    return await initSalesData();
  }
}

async function saveSalesData(data) {
  await ensureDir(CONFIG.dataDir);
  data.lastUpdate = new Date().toISOString();
  await fs.writeFile(
    path.join(CONFIG.dataDir, CONFIG.salesFile),
    JSON.stringify(data, null, 2)
  );
}

// Record a sale
async function recordSale(sale) {
  const data = await loadSalesData();
  
  const saleRecord = {
    id: `sale_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    timestamp: new Date().toISOString(),
    platform: sale.platform,
    designId: sale.designId,
    product: sale.product,
    quantity: sale.quantity || 1,
    revenue: sale.revenue,
    cost: sale.cost,
    profit: sale.revenue - sale.cost,
    currency: sale.currency || 'USD'
  };
  
  data.sales.push(saleRecord);
  
  // Update design stats
  if (!data.designs[sale.designId]) {
    data.designs[sale.designId] = { sales: 0, revenue: 0, profit: 0 };
  }
  data.designs[sale.designId].sales += saleRecord.quantity;
  data.designs[sale.designId].revenue += saleRecord.revenue;
  data.designs[sale.designId].profit += saleRecord.profit;
  
  // Update platform performance
  if (!data.platformPerformance[sale.platform]) {
    data.platformPerformance[sale.platform] = { sales: 0, revenue: 0, profit: 0 };
  }
  data.platformPerformance[sale.platform].sales += saleRecord.quantity;
  data.platformPerformance[sale.platform].revenue += saleRecord.revenue;
  data.platformPerformance[sale.platform].profit += saleRecord.profit;
  
  await saveSalesData(data);
  log(`Sale recorded: ${sale.designId} on ${sale.platform} (+$${saleRecord.profit.toFixed(2)})`);
  
  return saleRecord;
}

// Generate analytics
async function generateAnalytics(days = 30) {
  const data = await loadSalesData();
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  
  const recentSales = data.sales.filter(s => new Date(s.timestamp) >= cutoff);
  
  // Top performing designs
  const designPerformance = {};
  for (const sale of recentSales) {
    if (!designPerformance[sale.designId]) {
      designPerformance[sale.designId] = { sales: 0, revenue: 0, profit: 0 };
    }
    designPerformance[sale.designId].sales += sale.quantity;
    designPerformance[sale.designId].revenue += sale.revenue;
    designPerformance[sale.designId].profit += sale.profit;
  }
  
  const topDesigns = Object.entries(designPerformance)
    .sort((a, b) => b[1].profit - a[1].profit)
    .slice(0, 10);
  
  // Platform breakdown
  const platformStats = {};
  for (const sale of recentSales) {
    if (!platformStats[sale.platform]) {
      platformStats[sale.platform] = { sales: 0, revenue: 0, profit: 0 };
    }
    platformStats[sale.platform].sales += sale.quantity;
    platformStats[sale.platform].revenue += sale.revenue;
    platformStats[sale.platform].profit += sale.profit;
  }
  
  // Daily trend
  const dailyStats = {};
  for (const sale of recentSales) {
    const day = sale.timestamp.split('T')[0];
    if (!dailyStats[day]) {
      dailyStats[day] = { sales: 0, profit: 0 };
    }
    dailyStats[day].sales += sale.quantity;
    dailyStats[day].profit += sale.profit;
  }
  
  return {
    period: `${days} days`,
    totalSales: recentSales.length,
    totalRevenue: recentSales.reduce((sum, s) => sum + s.revenue, 0),
    totalProfit: recentSales.reduce((sum, s) => sum + s.profit, 0),
    topDesigns: topDesigns,
    platformBreakdown: platformStats,
    dailyTrend: dailyStats,
    generatedAt: new Date().toISOString()
  };
}

// Generate weekly report
async function generateWeeklyReport() {
  log('Generating weekly report...');
  
  const analytics = await generateAnalytics(7);
  const lastWeek = await generateAnalytics(14); // For comparison
  
  const previousWeekSales = lastWeek.totalSales - analytics.totalSales;
  const previousWeekProfit = lastWeek.totalProfit - analytics.totalProfit;
  
  const salesGrowth = previousWeekSales > 0 
    ? ((analytics.totalSales - previousWeekSales) / previousWeekSales * 100).toFixed(1)
    : 0;
  
  const profitGrowth = previousWeekProfit > 0
    ? ((analytics.totalProfit - previousWeekProfit) / previousWeekProfit * 100).toFixed(1)
    : 0;
  
  const report = {
    weekEnding: new Date().toISOString().split('T')[0],
    summary: {
      totalSales: analytics.totalSales,
      totalRevenue: analytics.totalRevenue.toFixed(2),
      totalProfit: analytics.totalProfit.toFixed(2),
      salesGrowth: `${salesGrowth}%`,
      profitGrowth: `${profitGrowth}%`,
      avgProfitPerSale: analytics.totalSales > 0 
        ? (analytics.totalProfit / analytics.totalSales).toFixed(2)
        : 0
    },
    topPerformers: analytics.topDesigns.slice(0, 5).map(([id, stats]) => ({
      designId: id,
      sales: stats.sales,
      revenue: stats.revenue.toFixed(2),
      profit: stats.profit.toFixed(2)
    })),
    platformPerformance: analytics.platformBreakdown,
    recommendations: generateRecommendations(analytics)
  };
  
  // Save report
  await ensureDir(path.join(CONFIG.dataDir, CONFIG.reportDir));
  const reportFile = `weekly_report_${report.weekEnding}.json`;
  await fs.writeFile(
    path.join(CONFIG.dataDir, CONFIG.reportDir, reportFile),
    JSON.stringify(report, null, 2)
  );
  
  // Generate human-readable version
  const textReport = formatWeeklyReport(report);
  await fs.writeFile(
    path.join(CONFIG.dataDir, CONFIG.reportDir, `weekly_report_${report.weekEnding}.txt`),
    textReport
  );
  
  log(`Weekly report saved: ${reportFile}`);
  return report;
}

function generateRecommendations(analytics) {
  const recs = [];
  
  if (analytics.totalSales === 0) {
    recs.push('No sales this week. Consider running promotions or expanding product range.');
  }
  
  if (analytics.topDesigns.length > 0) {
    recs.push(`Double down on "${analytics.topDesigns[0][0]}" - your top performer.`);
    recs.push(`Create variations of top 3 designs to capture more market.`);
  }
  
  const platforms = Object.keys(analytics.platformBreakdown);
  if (platforms.length === 1) {
    recs.push('Only one platform generating sales. Consider expanding to other platforms.');
  }
  
  const avgDailyProfit = analytics.totalProfit / 30;
  if (avgDailyProfit < 5) {
    recs.push('Low daily profit. Focus on higher-margin products or increase prices.');
  }
  
  recs.push('Test 3 new designs this week based on trending niches.');
  recs.push('Optimize listings with better keywords and mockups.');
  
  return recs;
}

function formatWeeklyReport(report) {
  return `
====================================
POD BUSINESS WEEKLY REPORT
Week Ending: ${report.weekEnding}
====================================

📊 SUMMARY
-----------
Total Sales: ${report.summary.totalSales}
Total Revenue: $${report.summary.totalRevenue}
Total Profit: $${report.summary.totalProfit}
Sales Growth: ${report.summary.salesGrowth}
Profit Growth: ${report.summary.profitGrowth}
Avg Profit/Sale: $${report.summary.avgProfitPerSale}

🏆 TOP PERFORMERS
-----------------
${report.topPerformers.map((d, i) => `${i + 1}. ${d.designId}
   Sales: ${d.sales} | Revenue: $${d.revenue} | Profit: $${d.profit}`).join('\n')}

📱 PLATFORM PERFORMANCE
------------------------
${Object.entries(report.platformPerformance).map(([platform, stats]) => `${platform}: ${stats.sales} sales, $${stats.profit.toFixed(2)} profit`).join('\n')}

💡 RECOMMENDATIONS
-----------------
${report.recommendations.map(r => `• ${r}`).join('\n')}

====================================
Generated: ${new Date().toLocaleString()}
====================================
`;
}

// Simulate sales (for testing)
async function simulateSales(count = 10) {
  log(`Simulating ${count} sales...`);
  
  const platforms = ['printify', 'redbubble', 'teespring'];
  const products = ['t-shirt', 'mug', 'sticker', 'poster'];
  
  for (let i = 0; i < count; i++) {
    await recordSale({
      platform: platforms[Math.floor(Math.random() * platforms.length)],
      designId: `design_crypto_${Math.floor(Math.random() * 5) + 1}`,
      product: products[Math.floor(Math.random() * products.length)],
      revenue: 15 + Math.random() * 20,
      cost: 5 + Math.random() * 8
    });
  }
  
  log(`${count} sales simulated`);
}

// Monthly revenue projection
async function generateProjection() {
  const data = await loadSalesData();
  const analytics = await generateAnalytics(30);
  
  const dailyAvg = analytics.totalProfit / 30;
  const monthlyProjection = dailyAvg * 30;
  const yearlyProjection = dailyAvg * 365;
  
  return {
    dailyAverage: dailyAvg.toFixed(2),
    monthlyProjection: monthlyProjection.toFixed(2),
    yearlyProjection: yearlyProjection.toFixed(2),
    breakEven: dailyAvg > 0 ? (100 / dailyAvg).toFixed(0) : 'N/A', // Days to cover $100 costs
    generatedAt: new Date().toISOString()
  };
}

// Main execution
async function main() {
  log('=== POD Sales Tracker ===');
  
  // Ensure data file exists
  const data = await loadSalesData();
  await saveSalesData(data);
  
  // Generate weekly report
  const report = await generateWeeklyReport();
  
  // Generate projection
  const projection = await generateProjection();
  
  log('\n--- Weekly Summary ---');
  log(`Sales: ${report.summary.totalSales}`);
  log(`Revenue: $${report.summary.totalRevenue}`);
  log(`Profit: $${report.summary.totalProfit}`);
  log(`\nProjected Monthly: $${projection.monthlyProjection}`);
  log(`Projected Yearly: $${projection.yearlyProjection}`);
  
  log('\n--- Top Recommendations ---');
  report.recommendations.slice(0, 3).forEach(r => log(`• ${r}`));
  
  log('=== Sales Tracker Complete ===');
}

module.exports = {
  recordSale,
  generateAnalytics,
  generateWeeklyReport,
  generateProjection,
  simulateSales,
  loadSalesData
};

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}
