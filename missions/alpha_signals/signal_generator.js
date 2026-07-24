/**
 * ALPHA SIGNALS BOT - Signal Generator
 * Generates BUY/HOLD/SELL signals from composite research scores
 */

const path = require('path');

// Use existing research infrastructure
const RESEARCH_PATH = path.resolve(__dirname, '../../mission_control');

// Load existing modules via require
let enhancedResearch, enhancedMarketService, enhancedTA, enhancedSentiment;

try {
  enhancedResearch = require(path.join(RESEARCH_PATH, 'enhanced_research.js'));
} catch (e) {
  console.warn('Could not load enhanced_research.js:', e.message);
}

// Asset configuration
const ASSETS = {
  BTC: { name: 'Bitcoin', type: 'crypto', priority: 'HIGH' },
  ETH: { name: 'Ethereum', type: 'crypto', priority: 'HIGH' },
  MSTR: { name: 'MicroStrategy', type: 'stock', priority: 'MEDIUM' },
  HIMS: { name: 'Hims & Hers', type: 'stock', priority: 'MEDIUM' },
  COIN: { name: 'Coinbase', type: 'stock', priority: 'MEDIUM' },
  TSLA: { name: 'Tesla', type: 'stock', priority: 'LOW' }
};

// Signal thresholds
const SIGNAL_LEVELS = {
  STRONG_BUY: { threshold: 3, label: 'STRONG BUY', emoji: '🟢🟢🟢', action: 'ACCUMULATE' },
  BUY: { threshold: 2, label: 'BUY', emoji: '🟢🟢', action: 'ENTER' },
  WEAK_BUY: { threshold: 1, label: 'WEAK BUY', emoji: '🟢', action: 'WATCH' },
  HOLD: { threshold: -1, label: 'HOLD', emoji: '⚪', action: 'MONITOR' },
  WEAK_SELL: { threshold: -2, label: 'WEAK SELL', emoji: '🔴', action: 'REDUCE' },
  SELL: { threshold: -3, label: 'SELL', emoji: '🔴🔴', action: 'EXIT' },
  STRONG_SELL: { threshold: -Infinity, label: 'STRONG SELL', emoji: '🔴🔴🔴', action: 'EXIT NOW' }
};

// Generate signal from composite score
function generateSignalFromScore(score, confidence) {
  const absScore = Math.abs(score);
  let signal;
  
  if (score >= 3) signal = SIGNAL_LEVELS.STRONG_BUY;
  else if (score >= 2) signal = SIGNAL_LEVELS.BUY;
  else if (score >= 1) signal = SIGNAL_LEVELS.WEAK_BUY;
  else if (score >= -1) signal = SIGNAL_LEVELS.HOLD;
  else if (score >= -2) signal = SIGNAL_LEVELS.WEAK_SELL;
  else if (score >= -3) signal = SIGNAL_LEVELS.SELL;
  else signal = SIGNAL_LEVELS.STRONG_SELL;
  
  return {
    ...signal,
    score,
    confidence: confidence || 'MEDIUM'
  };
}

// Calculate confidence level from data quality
function calculateConfidence(data) {
  let score = 0;
  const factors = [];
  
  // Price data quality
  if (data.price?.source === 'twelveData' || data.price?.source === 'yahoo') {
    score += 2; factors.push('Live price data');
  } else if (data.price?.source === 'cached') {
    score += 1; factors.push('Cached price data');
  }
  
  // Technical analysis coverage
  if (data.technical?.composite?.confidence === 'HIGH') {
    score += 2; factors.push('Full TA coverage');
  } else if (data.technical?.composite?.confidence === 'MEDIUM') {
    score += 1; factors.push('Partial TA coverage');
  }
  
  // Sentiment data
  if (data.sentiment?.summary?.total > 5) {
    score += 1; factors.push('Multiple sentiment sources');
  }
  
  const confidenceLevel = score >= 5 ? 'HIGH' : score >= 3 ? 'MEDIUM' : 'LOW';
  
  return { level: confidenceLevel, score, factors };
}

// Build signal from research data
async function buildSignal(symbol, researchData) {
  const asset = ASSETS[symbol];
  const composite = researchData?.composite;
  
  if (!composite) {
    return {
      symbol,
      name: asset?.name || symbol,
      signal: 'UNKNOWN',
      emoji: '❓',
      score: 0,
      confidence: 'LOW',
      action: 'NO DATA',
      reason: 'Insufficient research data',
      timestamp: new Date().toISOString()
    };
  }
  
  const confidence = calculateConfidence(researchData.data);
  const signal = generateSignalFromScore(composite.score, confidence.level);
  
  // Build reason from factors
  const reasons = [];
  if (composite.factors) {
    composite.factors.forEach(f => reasons.push(f));
  }
  
  // Add price context
  const price = researchData.data?.price;
  if (price) {
    const change = price.change_24h;
    const changeEmoji = change > 0 ? '📈' : '📉';
    reasons.push(`24h: ${change > 0 ? '+' : ''}${change.toFixed(2)}% ${changeEmoji}`);
  }
  
  return {
    symbol,
    name: asset?.name || symbol,
    signal: signal.label,
    emoji: signal.emoji,
    score: composite.score,
    rawScore: composite.rawScore,
    confidence: confidence.level,
    confidenceScore: confidence.score,
    confidenceFactors: confidence.factors,
    action: signal.action,
    urgency: composite.urgency,
    price: price?.price,
    change24h: price?.change_24h,
    reasons,
    timestamp: new Date().toISOString()
  };
}

// Generate signals for all assets
async function generateAllSignals(options = {}) {
  const symbols = options.symbols || Object.keys(ASSETS);
  const signals = [];
  
  console.log('\n═══════════════════════════════════════════════════════');
  console.log('   ALPHA SIGNALS BOT - Generating Signals');
  console.log('═══════════════════════════════════════════════════════\n');
  
  for (const symbol of symbols) {
    try {
      let researchData = null;
      
      if (enhancedResearch?.enhancedResearch) {
        researchData = await enhancedResearch.enhancedResearch(symbol);
      } else {
        // Fallback: try to load from cached market data
        researchData = await loadCachedData(symbol);
      }
      
      const signal = await buildSignal(symbol, researchData);
      signals.push(signal);
      
      console.log(`✅ ${symbol}: ${signal.signal} (${signal.confidence} confidence)`);
      
      // Rate limit protection
      if (!options.skipDelay) {
        await new Promise(r => setTimeout(r, 500));
      }
    } catch (e) {
      console.error(`❌ ${symbol}: ${e.message}`);
      signals.push({
        symbol,
        name: ASSETS[symbol]?.name || symbol,
        signal: 'ERROR',
        emoji: '⚠️',
        score: 0,
        confidence: 'LOW',
        action: 'RETRY',
        reason: e.message,
        timestamp: new Date().toISOString()
      });
    }
  }
  
  return signals;
}

// Fallback: load from cached market data
async function loadCachedData(symbol) {
  const fs = require('fs');
  const cachePath = path.join(RESEARCH_PATH, 'market_data.json');
  
  try {
    const data = JSON.parse(fs.readFileSync(cachePath, 'utf8'));
    const asset = data.assets?.[symbol];
    
    if (!asset) return null;
    
    // Build minimal composite
    const change = asset.change_24h || 0;
    let score = 0;
    if (change > 10) score = 3;
    else if (change > 5) score = 2;
    else if (change > 2) score = 1;
    else if (change < -10) score = -3;
    else if (change < -5) score = -2;
    else if (change < -2) score = -1;
    
    return {
      composite: {
        score,
        rawScore: score.toFixed(2),
        rating: score >= 3 ? 'STRONG_BUY' : score >= 2 ? 'BUY' : score >= 1 ? 'WEAK_BUY' : 
                score <= -3 ? 'STRONG_SELL' : score <= -2 ? 'SELL' : score <= -1 ? 'WEAK_SELL' : 'HOLD',
        confidence: 'MEDIUM',
        urgency: score >= 2 ? 'TODAY' : score <= -2 ? 'TODAY' : 'NONE',
        factors: [`Price change: ${change.toFixed(2)}%`]
      },
      data: {
        price: asset
      }
    };
  } catch (e) {
    return null;
  }
}

// Export for use by other modules
module.exports = {
  generateAllSignals,
  buildSignal,
  generateSignalFromScore,
  calculateConfidence,
  ASSETS,
  SIGNAL_LEVELS
};

// CLI
async function main() {
  const args = process.argv.slice(2);
  const symbols = args.filter(a => !a.startsWith('--'));
  const format = args.includes('--json') ? 'json' : 'text';
  
  const signals = await generateAllSignals({ 
    symbols: symbols.length > 0 ? symbols : Object.keys(ASSETS)
  });
  
  if (format === 'json') {
    console.log(JSON.stringify(signals, null, 2));
  } else {
    signals.forEach(s => {
      console.log(`\n${s.emoji} ${s.symbol} - ${s.signal}`);
      console.log(`   Score: ${s.score} | Confidence: ${s.confidence}`);
      console.log(`   Action: ${s.action}`);
      if (s.price) console.log(`   Price: $${s.price.toLocaleString()}`);
      if (s.reasons) s.reasons.forEach(r => console.log(`   • ${r}`));
    });
  }
}

if (require.main === module) main();
