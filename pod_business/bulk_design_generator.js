// Bulk Design Generator for POD Scaling
// Generates 100+ products from templates

const fs = require('fs');
const path = require('path');

const CONFIG = {
  currentProducts: 35,
  targetProducts: 100,
  niches: ['crypto', 'investing', 'AI', 'trading', 'bitcoin'],
  productTypes: ['t-shirt', 'mug', 'poster', 'sticker', 'phone-case'],
  designsPerDay: 10
};

const TEMPLATES = {
  crypto: [
    { title: 'Bitcoin to the Moon {{YEAR}}', tags: 'bitcoin,crypto,btc,moon,hodl' },
    { title: 'Ethereum Investor {{YEAR}}', tags: 'ethereum,eth,crypto,investor,defi' },
    { title: 'Crypto Trader Life', tags: 'crypto,trader,bitcoin,ethereum,blockchain' },
    { title: 'HODL Gang', tags: 'hodl,bitcoin,crypto,btc,diamond-hands' },
    { title: 'Crypto Millionaire Loading', tags: 'crypto,millionaire,bitcoin,rich,wealth' }
  ],
  investing: [
    { title: 'Buy the Dip', tags: 'stocks,investing,buy-dip,trading,finance' },
    { title: 'Long Term Investor', tags: 'investor,long-term,stocks,portfolio,wealth' },
    { title: 'Dividend King', tags: 'dividend,stocks,passive-income,investing,money' },
    { title: 'Stock Market Bull', tags: 'bull-market,stocks,trading,investor,finance' }
  ],
  AI: [
    { title: 'Powered by AI', tags: 'ai,artificial-intelligence,tech,future,robot' },
    { title: 'AI Will Not Replace You', tags: 'ai,jobs,technology,future,work' },
    { title: 'ChatGPT My Therapist', tags: 'chatgpt,ai,funny,tech,meme' }
  ],
  trading: [
    { title: 'Day Trader Life', tags: 'day-trader,trading,stocks,crypto,forex' },
    { title: 'Technical Analysis Expert', tags: 'technical-analysis,charts,trading,crypto,stocks' }
  ],
  bitcoin: [
    { title: '21 Million Club', tags: 'bitcoin,21-million,btc,crypto,scarcity' },
    { title: 'Satoshi Nakamoto Fan', tags: 'satoshi,bitcoin,crypto,btc,founder' }
  ]
};

function generateDesigns(count) {
  const designs = [];
  const year = new Date().getFullYear();
  
  for (let i = 0; i < count; i++) {
    const niche = CONFIG.niches[i % CONFIG.niches.length];
    const template = TEMPLATES[niche][i % TEMPLATES[niche].length];
    const productType = CONFIG.productTypes[i % CONFIG.productTypes.length];
    
    designs.push({
      id: `design_${CONFIG.currentProducts + i + 1}`,
      title: template.title.replace('{{YEAR}}', year),
      tags: template.tags,
      niche: niche,
      productType: productType,
      status: 'ready_to_publish',
      createdAt: new Date().toISOString()
    });
  }
  
  return designs;
}

function saveDesigns(designs) {
  const outputDir = 'pod_business/generated_designs';
  fs.mkdirSync(outputDir, { recursive: true });
  
  const batchFile = path.join(outputDir, `batch_${new Date().toISOString().split('T')[0]}.json`);
  fs.writeFileSync(batchFile, JSON.stringify(designs, null, 2));
  
  // Also save as CSV for Printify import
  const csvHeader = 'id,title,tags,niche,productType,status\n';
  const csvRows = designs.map(d => `${d.id},"${d.title}","${d.tags}",${d.niche},${d.productType},${d.status}`).join('\n');
  const csvFile = path.join(outputDir, `batch_${new Date().toISOString().split('T')[0]}.csv`);
  fs.writeFileSync(csvFile, csvHeader + csvRows);
  
  return { batchFile, csvFile, count: designs.length };
}

function generateDailyBatch() {
  console.log('=== POD Bulk Design Generator ===');
  console.log(`Current: ${CONFIG.currentProducts} products`);
  console.log(`Target: ${CONFIG.targetProducts} products`);
  console.log(`Remaining: ${CONFIG.targetProducts - CONFIG.currentProducts}`);
  console.log(`Generating ${CONFIG.designsPerDay} designs for today...\n`);
  
  const designs = generateDesigns(CONFIG.designsPerDay);
  const saved = saveDesigns(designs);
  
  console.log('✅ Designs generated:', saved.count);
  console.log('📁 JSON:', saved.batchFile);
  console.log('📁 CSV (Printify-ready):', saved.csvFile);
  console.log('\nNext steps:');
  console.log('1. Review designs in generated_designs/');
  console.log('2. Upload to Printify');
  console.log('3. Publish to Etsy');
  console.log(`4. Progress: ${CONFIG.currentProducts + CONFIG.designsPerDay}/${CONFIG.targetProducts}`);
  
  // Update metrics
  const metricsPath = 'pod_business/scaling_metrics.json';
  let metrics = { current: CONFIG.currentProducts, target: CONFIG.targetProducts, dailyGenerated: 0 };
  try {
    metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
  } catch {}
  metrics.dailyGenerated = (metrics.dailyGenerated || 0) + CONFIG.designsPerDay;
  metrics.current += CONFIG.designsPerDay;
  fs.writeFileSync(metricsPath, JSON.stringify(metrics, null, 2));
}

generateDailyBatch();
