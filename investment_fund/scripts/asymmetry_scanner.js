/**
 * ASYMMETRY SCANNER — Identifies high-conviction opportunities
 * Runs every 15 minutes, scores on 7-factor model
 * Auto-queues top opportunities for review
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  MIN_ASYMMETRY_SCORE: 3.0,
  TARGET_ASYMMETRY_SCORE: 5.0,
  SCAN_INTERVAL_MINUTES: 15,
  OUTPUT_DIR: path.join(__dirname, '..', 'opportunities'),
  MARKET_DATA_FILE: path.join(__dirname, '..', '..', 'mission_control', 'market_data.json'),
  TICKERS: [
    // Core 12
    'BTC', 'ETH', 'NVDA', 'TSLA', 'MSTR', 'AAPL', 'HIMS', 'COIN', 'SPY', 'QQQ', 'GLD', 'TLT',
    // Phase 1 Expansion (25 names)
    'PLTR', 'CRWD', 'SNOW', 'NET', 'DUOL',  // Growth
    'BRK.B', 'UNH', 'V', 'MA', 'JPM',       // Value
    'ASML', 'TSM', 'BABA', 'TCEHY',          // International
    'SOL', 'LINK', 'AAVE', 'MKR'             // Crypto
  ]
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.OUTPUT_DIR)) {
  fs.mkdirSync(CONFIG.OUTPUT_DIR, { recursive: true });
}

/**
 * Calculate asymmetry score
 * Score = (Upside %) / (Downside %) × Catalyst Probability
 */
function calculateAsymmetry(ticker, currentPrice, fundamentals) {
  const upside = fundamentals.targetPrice / currentPrice - 1;
  const downside = currentPrice / fundamentals.floorPrice - 1;
  const catalystProb = fundamentals.catalystProbability || 0.5;
  
  const asymmetry = (upside / Math.max(downside, 0.05)) * catalystProb;
  
  return {
    ticker,
    currentPrice,
    targetPrice: fundamentals.targetPrice,
    floorPrice: fundamentals.floorPrice,
    upside: upside * 100,
    downside: downside * 100,
    catalystProb,
    asymmetryScore: asymmetry,
    catalyst: fundamentals.catalyst,
    confidence: fundamentals.confidence || 50
  };
}

/**
 * Mock fundamental data (replace with real DCF/NAV models)
 */
function getFundamentals(ticker) {
  // Placeholder: In production, this pulls from DCF engine
  const mockData = {
    'BTC': { targetPrice: 75000, floorPrice: 55000, catalyst: 'Halving supply shock', catalystProbability: 0.7, confidence: 75 },
    'ETH': { targetPrice: 2500, floorPrice: 1600, catalyst: 'ETF approval', catalystProbability: 0.6, confidence: 70 },
    'NVDA': { targetPrice: 280, floorPrice: 170, catalyst: 'AI demand cycle', catalystProbability: 0.8, confidence: 85 },
    'TSLA': { targetPrice: 450, floorPrice: 300, catalyst: 'Robotaxi unveil', catalystProbability: 0.5, confidence: 60 },
    'MSTR': { targetPrice: 130, floorPrice: 75, catalyst: 'BTC treasury appreciation', catalystProbability: 0.65, confidence: 70 },
    'AAPL': { targetPrice: 380, floorPrice: 280, catalyst: 'Apple Intelligence rollout', catalystProbability: 0.6, confidence: 75 },
    'HIMS': { targetPrice: 45, floorPrice: 25, catalyst: 'GLP-1 expansion', catalystProbability: 0.55, confidence: 65 },
    'COIN': { targetPrice: 220, floorPrice: 120, catalyst: 'Institutional crypto adoption', catalystProbability: 0.6, confidence: 70 },
    'PLTR': { targetPrice: 35, floorPrice: 18, catalyst: 'Government AI contracts', catalystProbability: 0.7, confidence: 80 },
    'CRWD': { targetPrice: 380, floorPrice: 240, catalyst: 'Cybersecurity demand', catalystProbability: 0.75, confidence: 85 }
  };
  
  return mockData[ticker] || { 
    targetPrice: 0, 
    floorPrice: 0, 
    catalyst: 'Research needed', 
    catalystProbability: 0.3,
    confidence: 40
  };
}

/**
 * Run scan across all tickers
 */
async function runScan() {
  console.log(`\n🔍 Asymmetry Scan — ${new Date().toISOString()}`);
  console.log('=' .repeat(60));
  
  // Load market data
  let marketData = {};
  try {
    const raw = fs.readFileSync(CONFIG.MARKET_DATA_FILE, 'utf8');
    marketData = JSON.parse(raw).assets || {};
  } catch (e) {
    console.log('⚠️ Could not load market data, using placeholders');
  }
  
  const opportunities = [];
  
  for (const ticker of CONFIG.TICKERS) {
    const currentPrice = marketData[ticker]?.price || 100;
    const fundamentals = getFundamentals(ticker);
    
    if (fundamentals.targetPrice === 0) continue;
    
    const score = calculateAsymmetry(ticker, currentPrice, fundamentals);
    
    if (score.asymmetryScore >= CONFIG.MIN_ASYMMETRY_SCORE) {
      opportunities.push(score);
    }
  }
  
  // Sort by asymmetry score
  opportunities.sort((a, b) => b.asymmetryScore - a.asymmetryScore);
  
  // Display results
  console.log(`\n🎯 HIGH-CONVICTION OPPORTUNITIES (Score ≥ ${CONFIG.MIN_ASYMMETRY_SCORE}):\n`);
  console.log('| Ticker | Price   | Target  | Upside | Downside | Score | Catalyst                |');
  console.log('|--------|---------|---------|--------|----------|-------|-------------------------|');
  
  for (const opp of opportunities.slice(0, 10)) {
    const emoji = opp.asymmetryScore >= CONFIG.TARGET_ASYMMETRY_SCORE ? '🌟' : '✓';
    console.log(
      `| ${opp.ticker.padEnd(6)} | $${opp.currentPrice.toFixed(2).padEnd(6)} | $${opp.targetPrice.toFixed(2).padEnd(6)} | ` +
      `${opp.upside.toFixed(1)}%`.padEnd(6) + ` | ${opp.downside.toFixed(1)}%`.padEnd(8) + 
      ` | ${opp.asymmetryScore.toFixed(1)}`.padEnd(5) + ` | ${opp.catalyst.slice(0, 23).padEnd(23)} | ${emoji}`
    );
  }
  
  // Save top opportunities
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const outputFile = path.join(CONFIG.OUTPUT_DIR, `scan_${timestamp}.json`);
  
  fs.writeFileSync(outputFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    opportunities: opportunities.slice(0, 20),
    metadata: {
      totalScanned: CONFIG.TICKERS.length,
      highConviction: opportunities.filter(o => o.asymmetryScore >= CONFIG.TARGET_ASYMMETRY_SCORE).length,
      mediumConviction: opportunities.filter(o => o.asymmetryScore >= CONFIG.MIN_ASYMMETRY_SCORE && o.asymmetryScore < CONFIG.TARGET_ASYMMETRY_SCORE).length
    }
  }, null, 2));
  
  console.log(`\n💾 Saved ${opportunities.length} opportunities to: ${outputFile}`);
  
  // Queue top 3 for immediate review
  const top3 = opportunities.filter(o => o.asymmetryScore >= CONFIG.TARGET_ASYMMETRY_SCORE).slice(0, 3);
  if (top3.length > 0) {
    console.log(`\n🚨 QUEUE FOR REVIEW (${top3.length} opportunities):`);
    for (const opp of top3) {
      console.log(`   ${opp.ticker}: ${opp.asymmetryScore.toFixed(1)}x asymmetry — ${opp.catalyst}`);
    }
  }
  
  return opportunities;
}

// Run if called directly
if (require.main === module) {
  runScan().catch(console.error);
}

module.exports = { runScan, calculateAsymmetry };
