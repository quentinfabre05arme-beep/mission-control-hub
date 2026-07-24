/**
 * NEWSLETTER GENERATOR
 * Pulls research cycle content into newsletter format
 * Creates Substack-compatible markdown output
 * 
 * Usage: node newsletter_generator.js [--output-dir path] [--date YYYY-MM-DD]
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  RESEARCH_DIR: path.join(__dirname, '..', '..', 'mission_control'),
  ALT_DATA_DIR: path.join(__dirname, '..', '..', 'investment_fund', 'data', 'alternative'),
  TEMPLATE_DIR: path.join(__dirname, 'templates'),
  OUTPUT_DIR: path.join(__dirname, 'output'),
  SUBSCRIBERS_FILE: path.join(__dirname, 'subscribers', 'subscribers.json'),
  ARCHIVE_DIR: path.join(__dirname, 'output', 'archive')
};

// Ensure directories exist
[CONFIG.OUTPUT_DIR, CONFIG.ARCHIVE_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Load JSON safely
function loadJson(filePath) {
  try {
    if (!fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    console.warn(`⚠️ Could not load ${filePath}: ${e.message}`);
    return null;
  }
}

// Load latest alternative data report
function loadLatestAlternativeData() {
  try {
    const files = fs.readdirSync(CONFIG.ALT_DATA_DIR)
      .filter(f => f.endsWith('.json'))
      .sort()
      .reverse();
    
    if (files.length === 0) return null;
    return loadJson(path.join(CONFIG.ALT_DATA_DIR, files[0]));
  } catch (e) {
    return null;
  }
}

// Load market data
function loadMarketData() {
  return loadJson(path.join(CONFIG.RESEARCH_DIR, 'market_data.json'));
}

// Load latest research for an asset
function loadLatestResearch(symbol) {
  // Try to find research output files
  const researchDir = CONFIG.RESEARCH_DIR;
  const possibleFiles = [
    path.join(researchDir, `${symbol.toLowerCase()}_research.json`),
    path.join(researchDir, 'output', `${symbol.toLowerCase()}_research.json`),
  ];
  
  for (const file of possibleFiles) {
    const data = loadJson(file);
    if (data) return data;
  }
  return null;
}

// Generate market snapshot section
function generateMarketSnapshot(marketData) {
  if (!marketData || !marketData.assets) {
    return '> Market data temporarily unavailable. Check dashboard for latest prices.';
  }

  let md = '| Asset | Price | 24h Change | Signal |\n';
  md += '|-------|-------|------------|--------|\n';
  
  Object.entries(marketData.assets).forEach(([symbol, asset]) => {
    const change = asset.change_24h >= 0 ? '+' : '';
    const emoji = asset.change_24h > 5 ? '🚀' : asset.change_24h > 2 ? '📈' : asset.change_24h < -5 ? '🔻' : asset.change_24h < -2 ? '📉' : '➡️';
    md += `| **${symbol}** | $${asset.price?.toLocaleString() || 'N/A'} | ${emoji} ${change}${asset.change_24h?.toFixed(2) || 'N/A'}% | ${asset.signal || 'N/A'} |\n`;
  });

  md += `\n*Last updated: ${marketData.timestamp || 'N/A'}*`;
  return md;
}

// Generate highlights from alternative data
function generateHighlights(altData) {
  if (!altData) return '> No alternative data available this week.';

  let md = '';
  
  // Fear & Greed highlight
  if (altData.sentiment?.fear_greed) {
    const fg = altData.sentiment.fear_greed;
    md += `### 📊 Fear & Greed Index: ${fg.value} (${fg.classification})\n\n`;
    md += `Market sentiment is **${fg.classification.toLowerCase()}** ${fg.trend === 'IMPROVING' ? 'and improving ↗️' : 'and declining ↘️'}. `;
    md += `Previous reading: ${fg.previous_value}.\n\n`;
  }

  // Whale signals
  if (altData.on_chain?.whale_activity) {
    const wa = altData.on_chain.whale_activity;
    md += `### 🐋 Whale Activity: ${wa.signal}\n\n`;
    md += `On-chain analysis suggests **${wa.signal.toLowerCase()}** patterns `;
    md += `with ${(wa.confidence * 100).toFixed(0)}% confidence.\n\n`;
  }

  // Anomalies
  if (altData.anomalies?.flags?.length > 0) {
    md += `### 🚨 Anomalies Detected (${altData.anomalies.count})\n\n`;
    altData.anomalies.flags.slice(0, 3).forEach(flag => {
      const emoji = flag.severity === 'HIGH' ? '🔴' : flag.severity === 'MEDIUM' ? '🟡' : '⚪';
      md += `- ${emoji} **[${flag.asset}]** ${flag.type}: ${flag.description}\n`;
    });
    md += '\n';
  }

  return md || '> Highlights coming soon.';
}

// Generate alternative data section
function generateAlternativeData(altData) {
  if (!altData) return '> Alternative data temporarily unavailable.';

  let md = '';

  // On-chain metrics
  if (altData.on_chain?.mempool) {
    const mp = altData.on_chain.mempool;
    md += `### ⛓️ On-Chain Metrics\n\n`;
    md += `- **Mempool Size:** ${mp.mempool_size?.toLocaleString() || 'N/A'} transactions\n`;
    md += `- **Network Congestion:** ${mp.network_congestion || 'N/A'}\n`;
    md += `\n`;
  }

  // Social sentiment
  if (altData.sentiment?.social_sentiment) {
    const ss = altData.sentiment.social_sentiment;
    md += `### 📱 Social Sentiment\n\n`;
    md += `- **Overall:** ${ss.overall_sentiment}\n`;
    md += `- **Bullish:** ${ss.bullish_pct}% | **Bearish:** ${ss.bearish_pct}% | **Neutral:** ${ss.neutral_pct}%\n`;
    if (ss.sources?.length > 0) {
      md += `- **Top topics:** ${ss.sources.slice(0, 3).join(', ')}\n`;
    }
    md += `\n`;
  }

  // Funding rates
  if (altData.order_flow?.funding_rates) {
    const fr = altData.order_flow.funding_rates;
    md += `### 💰 Funding Rate Estimates\n\n`;
    if (fr.BTC) md += `- **BTC:** ${(fr.BTC.estimated_rate * 100).toFixed(2)}% | ${fr.BTC.sentiment}\n`;
    if (fr.ETH) md += `- **ETH:** ${(fr.ETH.estimated_rate * 100).toFixed(2)}% | ${fr.ETH.sentiment}\n`;
    md += `\n`;
  }

  return md || '> No alternative data to report.';
}

// Generate composite ratings
function generateCompositeRatings(altData) {
  if (!altData?.composite_scores) return '> Ratings temporarily unavailable.';

  let md = '| Asset | Rating | Score | Key Factor |\n';
  md += '|-------|--------|-------|------------|\n';

  Object.entries(altData.composite_scores).forEach(([symbol, data]) => {
    const emoji = data.rating.includes('BULLISH') ? '🟢' : data.rating.includes('BEARISH') ? '🔴' : '⚪';
    const factor = data.factors?.[0] || 'N/A';
    md += `| **${symbol}** | ${emoji} ${data.rating} | ${data.score} | ${factor} |\n`;
  });

  return md;
}

// Generate key takeaways
function generateKeyTakeaways(altData, marketData) {
  let md = '';
  
  if (altData?.composite_scores) {
    const bullishAssets = Object.entries(altData.composite_scores)
      .filter(([_, d]) => d.rating.includes('BULLISH'));
    const bearishAssets = Object.entries(altData.composite_scores)
      .filter(([_, d]) => d.rating.includes('BEARISH'));

    if (bullishAssets.length > 0) {
      md += `### ✅ Bullish Signals\n\n`;
      bullishAssets.forEach(([symbol, data]) => {
        md += `- **${symbol}:** ${data.factors?.[0] || 'Positive momentum'}\n`;
      });
      md += '\n';
    }

    if (bearishAssets.length > 0) {
      md += `### ⚠️ Caution Signals\n\n`;
      bearishAssets.forEach(([symbol, data]) => {
        md += `- **${symbol}:** ${data.factors?.[0] || 'Negative pressure'}\n`;
      });
      md += '\n';
    }
  }

  if (altData?.sentiment?.fear_greed) {
    const fg = altData.sentiment.fear_greed;
    if (fg.value < 25) {
      md += `### 💡 Contrarian Opportunity\n\n`;
      md += `Fear & Greed at ${fg.value} suggests extreme fear. Historically, this is when the best long-term entries appear.\n\n`;
    }
  }

  if (!md) {
    md = '> Market is in a consolidation phase. No strong directional signals this week. Patience is key.';
  }

  return md;
}

// Generate asset analyses
function generateAssetAnalyses(marketData) {
  if (!marketData?.assets) return '> Asset analysis temporarily unavailable.';

  let md = '';
  Object.entries(marketData.assets).forEach(([symbol, asset]) => {
    const change = asset.change_24h >= 0 ? '+' : '';
    const trend = asset.change_24h > 3 ? 'strongly bullish' : asset.change_24h > 0 ? 'bullish' : asset.change_24h < -3 ? 'strongly bearish' : asset.change_24h < 0 ? 'bearish' : 'neutral';
    
    md += `### ${symbol} — $${asset.price?.toLocaleString() || 'N/A'} (${change}${asset.change_24h?.toFixed(2) || 'N/A'}%)\n\n`;
    md += `Price action is **${trend}** in the short term. `;
    md += `Signal: *${asset.signal || 'N/A'}*.\n\n`;
  });

  return md;
}

// Main newsletter generation
async function generateNewsletter(options = {}) {
  const date = options.date || new Date().toISOString().split('T')[0];
  const outputDir = options.outputDir || CONFIG.OUTPUT_DIR;
  
  console.log('📰 Generating newsletter...\n');

  // Load data
  const altData = loadLatestAlternativeData();
  const marketData = loadMarketData();
  
  // Generate sections
  const sections = {
    title: `Alpha Fund Weekly — ${date}`,
    subtitle: 'Independent Crypto & Equity Research',
    date: date,
    author: 'Alpha Fund Research',
    tags: 'crypto,research,analysis,BTC,ETH,MSTR,HIMS',
    banner: '> 📰 *Weekly insights from systematic research and alternative data*',
    highlights: generateHighlights(altData),
    market_snapshot: generateMarketSnapshot(marketData),
    asset_analyses: generateAssetAnalyses(marketData),
    alternative_data: generateAlternativeData(altData),
    composite_ratings: generateCompositeRatings(altData),
    key_takeaways: generateKeyTakeaways(altData, marketData),
    disclaimer: '*Disclaimer: This newsletter is for informational purposes only. Not financial advice. Do your own research.*',
    generation_date: new Date().toLocaleString('en-US', { timeZone: 'Europe/Paris' }),
    cycle_count: '50+',
    canonical_url: 'https://mission-control-hub-lovat.vercel.app'
  };

  // Load template
  const templatePath = path.join(CONFIG.TEMPLATE_DIR, 'substack_compatible.md');
  let template = fs.readFileSync(templatePath, 'utf8');

  // Replace placeholders
  Object.entries(sections).forEach(([key, value]) => {
    const regex = new RegExp(`{{${key}}}`, 'g');
    template = template.replace(regex, value);
  });

  // Save newsletter
  const outputPath = path.join(outputDir, `newsletter_${date}.md`);
  fs.writeFileSync(outputPath, template);

  // Also save to archive
  const archivePath = path.join(CONFIG.ARCHIVE_DIR, `newsletter_${date}.md`);
  fs.writeFileSync(archivePath, template);

  console.log(`✅ Newsletter generated: ${outputPath}`);
  console.log(`📁 Archived: ${archivePath}`);

  return {
    outputPath,
    archivePath,
    sections,
    date
  };
}

// Load subscriber list
function loadSubscribers() {
  return loadJson(CONFIG.SUBSCRIBERS_FILE) || { subscribers: [], count: 0 };
}

// Add subscriber
function addSubscriber(email, metadata = {}) {
  const subscribers = loadSubscribers();
  
  // Check if already exists
  if (subscribers.subscribers.some(s => s.email === email)) {
    return { success: false, message: 'Already subscribed' };
  }

  subscribers.subscribers.push({
    email,
    subscribed_at: new Date().toISOString(),
    active: true,
    metadata
  });
  subscribers.count = subscribers.subscribers.length;
  subscribers.last_updated = new Date().toISOString();

  fs.writeFileSync(CONFIG.SUBSCRIBERS_FILE, JSON.stringify(subscribers, null, 2));
  return { success: true, message: 'Subscribed successfully', total: subscribers.count };
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'subscribe' && args[1]) {
    const result = addSubscriber(args[1], { source: 'cli' });
    console.log(result.message);
    if (result.success) console.log(`Total subscribers: ${result.total}`);
    return;
  }

  if (command === 'list-subscribers') {
    const subs = loadSubscribers();
    console.log(`📧 ${subs.count} subscriber(s):\n`);
    subs.subscribers.forEach((s, i) => {
      console.log(`${i + 1}. ${s.email} (${s.active ? '✅' : '❌'}) — ${s.subscribed_at}`);
    });
    return;
  }

  // Default: generate newsletter
  const date = args.find(a => a.startsWith('--date'))?.split('=')[1];
  const outputDir = args.find(a => a.startsWith('--output-dir'))?.split('=')[1];
  
  try {
    const result = await generateNewsletter({ date, outputDir });
    console.log('\n📰 Newsletter ready for Substack!');
    console.log(`📄 File: ${result.outputPath}`);
    console.log(`\n📋 Sections included:`);
    Object.keys(result.sections).forEach(key => {
      if (!key.startsWith('_')) console.log(`   ✓ ${key}`);
    });
  } catch (e) {
    console.error('❌ Error:', e.message);
    process.exit(1);
  }
}

module.exports = { generateNewsletter, addSubscriber, loadSubscribers };

if (require.main === module) main();
