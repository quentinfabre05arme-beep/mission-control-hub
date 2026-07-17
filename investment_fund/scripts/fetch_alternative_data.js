#!/usr/bin/env node
/**
 * ALPHA FUND - Alternative Data Fetcher
 * Fetches early signals not visible in price data
 * 
 * Usage: node fetch_alternative_data.js [--all] [--asset BTC] [--json]
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  SERPER_KEY: '1a32d04a8215dde72b67e554c94409ce580094f3',
  DATA_DIR: path.join(__dirname, '..', 'data', 'alternative'),
  MARKET_DATA_FILE: path.join(__dirname, '..', '..', 'mission_control', 'market_data.json'),
  CACHE_MINUTES: 60
};

// Ensure directory exists
if (!fs.existsSync(CONFIG.DATA_DIR)) {
  fs.mkdirSync(CONFIG.DATA_DIR, { recursive: true });
}

// Fetch Fear & Greed Index
async function fetchFearGreedIndex() {
  return new Promise((resolve) => {
    const req = https.get('https://api.alternative.me/fng/?limit=1', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({
            value: parseInt(parsed.data[0].value),
            classification: parsed.data[0].value_classification.toUpperCase(),
            timestamp: new Date(parsed.data[0].timestamp * 1000).toISOString()
          });
        } catch (e) {
          resolve(null);
        }
      });
    });
    req.on('error', () => resolve(null));
    req.setTimeout(5000, () => { req.destroy(); resolve(null); });
  });
}

// Load market data
function loadMarketData() {
  try {
    const data = fs.readFileSync(CONFIG.MARKET_DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return null;
  }
}

// Search for whale/on-chain news
async function fetchWhaleNews() {
  return new Promise((resolve) => {
    const postData = JSON.stringify({
      q: 'bitcoin whale exchange inflows outflows accumulation',
      num: 10,
      tbs: 'qdr:d'
    });

    const req = https.request({
      hostname: 'google.serper.dev',
      path: '/news',
      method: 'POST',
      headers: {
        'X-API-KEY': CONFIG.SERPER_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.news?.slice(0, 5) || []);
        } catch (e) {
          resolve([]);
        }
      });
    });
    req.on('error', () => resolve([]));
    req.setTimeout(8000, () => { req.destroy(); resolve([]); });
    req.write(postData);
    req.end();
  });
}

// Analyze whale news for accumulation signals
function analyzeWhaleSignals(news) {
  const accumulationWords = ['accumulating', 'holding', 'not selling', 'decline in inflows', 'outflow', 'leaving exchanges'];
  const distributionWords = ['selling', 'dumping', 'inflow', 'deposit', 'exchange inflows'];
  
  let accumulationScore = 0;
  let distributionScore = 0;
  const relevantHeadlines = [];

  news.forEach(item => {
    const text = `${item.title} ${item.snippet || ''}`.toLowerCase();
    
    accumulationWords.forEach(word => {
      if (text.includes(word)) {
        accumulationScore++;
        relevantHeadlines.push({ sentiment: 'accumulation', title: item.title });
      }
    });
    
    distributionWords.forEach(word => {
      if (text.includes(word)) {
        distributionScore++;
        relevantHeadlines.push({ sentiment: 'distribution', title: item.title });
      }
    });
  });

  const netScore = accumulationScore - distributionScore;
  return {
    signal: netScore > 1 ? 'ACCUMULATION' : netScore < -1 ? 'DISTRIBUTION' : 'NEUTRAL',
    score: netScore,
    confidence: Math.min((accumulationScore + distributionScore) / 5, 1),
    headlines: relevantHeadlines.slice(0, 5)
  };
}

// Detect anomalies
function detectAnomalies(marketData, fearGreed, whaleSignals) {
  const flags = [];
  
  if (!marketData) return flags;

  // Fear & Greed recovery
  if (fearGreed && fearGreed.value > 25 && fearGreed.value < 35) {
    flags.push({
      asset: 'MARKET',
      type: 'SENTIMENT_RECOVERY',
      severity: 'MEDIUM',
      description: `Fear & Greed at ${fearGreed.value} - recovering from extreme fear`,
      signal: 'CONTRARIAN_BUY'
    });
  }

  // Whale accumulation
  if (whaleSignals.signal === 'ACCUMULATION' && whaleSignals.confidence > 0.5) {
    flags.push({
      asset: 'BTC',
      type: 'WHALE_ACCUMULATION',
      severity: 'HIGH',
      description: 'On-chain data suggests whale accumulation',
      signal: 'BULLISH_EARLY'
    });
  }

  // Price divergences
  Object.entries(marketData.assets || {}).forEach(([symbol, asset]) => {
    if (asset.change_24h < -2 && (asset.signal === 'BEARISH' || asset.signal === 'STRONG_BEARISH')) {
      flags.push({
        asset: symbol,
        type: 'PRICE_DIVERGENCE',
        severity: 'LOW',
        description: `${symbol} down ${asset.change_24h.toFixed(2)}% vs neutral market`,
        signal: 'MONITOR'
      });
    }
  });

  return flags;
}

// Generate composite scores
function generateCompositeScores(marketData, fearGreed, whaleSignals) {
  const scores = {};
  
  if (!marketData) return scores;

  Object.keys(marketData.assets || {}).forEach(symbol => {
    let score = 0;
    const factors = [];

    // Price momentum
    const asset = marketData.assets[symbol];
    if (asset.change_24h > 1) { score += 0.2; factors.push('Positive 24h momentum'); }
    if (asset.change_24h < -1) { score -= 0.2; factors.push('Negative 24h momentum'); }

    // Fear & Greed impact
    if (fearGreed) {
      if (fearGreed.value < 30) {
        score += 0.3;
        factors.push('Extreme fear = contrarian buy opportunity');
      }
    }

    // Whale signals (BTC only)
    if (symbol === 'BTC' && whaleSignals.signal === 'ACCUMULATION') {
      score += 0.4;
      factors.push('Whale accumulation detected');
    }

    scores[symbol] = {
      score: score.toFixed(2),
      rating: score > 0.5 ? 'BULLISH' : score > 0.2 ? 'SLIGHTLY_BULLISH' : score > -0.2 ? 'NEUTRAL' : score > -0.5 ? 'SLIGHTLY_BEARISH' : 'BEARISH',
      factors
    };
  });

  return scores;
}

// Main fetch function
async function fetchAlternativeData() {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timestamp = now.toISOString();
  
  console.log('🔄 Fetching alternative data for Alpha Fund...\n');

  // Fetch all data in parallel
  const [marketData, fearGreed, whaleNews] = await Promise.all([
    Promise.resolve(loadMarketData()),
    fetchFearGreedIndex(),
    fetchWhaleNews()
  ]);

  const whaleSignals = analyzeWhaleSignals(whaleNews);
  const anomalies = detectAnomalies(marketData, fearGreed, whaleSignals);
  const composites = generateCompositeScores(marketData, fearGreed, whaleSignals);

  const report = {
    metadata: {
      fetch_timestamp: timestamp,
      local_time: now.toLocaleString('fr-FR', { timeZone: 'Europe/Paris' }),
      cycle_id: `alternative-data-${dateStr}`,
      data_sources: ['alternative.me', 'serper.dev', 'market_data.json']
    },
    market_snapshot: marketData,
    sentiment: {
      fear_greed: fearGreed,
      whale_signals: whaleSignals
    },
    on_chain: {
      whale_activity: whaleSignals,
      exchange_flows: { status: 'PENDING_IMPLEMENTATION' }
    },
    anomalies: {
      flags: anomalies,
      count: anomalies.length,
      summary: `${anomalies.length} anomaly(s) detected`
    },
    composite_scores: composites,
    research_flags: anomalies.map(a => ({
      priority: a.severity === 'HIGH' ? 'HIGH' : 'MEDIUM',
      asset: a.asset,
      task: `Investigate ${a.type}: ${a.description}`,
      signal: a.signal
    }))
  };

  // Save to file
  const outputPath = path.join(CONFIG.DATA_DIR, `${dateStr}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));

  return { report, outputPath };
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const asJson = args.includes('--json');

  try {
    const { report, outputPath } = await fetchAlternativeData();

    if (asJson) {
      console.log(JSON.stringify(report, null, 2));
    } else {
      console.log('\n╔════════════════════════════════════════════════╗');
      console.log('║     ALPHA FUND - ALTERNATIVE DATA REPORT       ║');
      console.log('╚════════════════════════════════════════════════╝');
      console.log(`\n📅 ${report.metadata.local_time}`);
      
      if (report.sentiment.fear_greed) {
        const fg = report.sentiment.fear_greed;
        const emoji = fg.value < 30 ? '💀' : fg.value < 50 ? '😰' : '😊';
        console.log(`\n📊 FEAR & GREED: ${fg.value} ${fg.classification} ${emoji}`);
      }

      console.log(`\n🐋 WHALE SIGNALS: ${report.sentiment.whale_signals.signal}`);
      console.log(`   Confidence: ${(report.sentiment.whale_signals.confidence * 100).toFixed(0)}%`);
      
      console.log(`\n🚨 ANOMALIES DETECTED: ${report.anomalies.count}`);
      report.anomalies.flags.forEach(flag => {
        const sev = flag.severity === 'HIGH' ? '🔴' : flag.severity === 'MEDIUM' ? '🟡' : '⚪';
        console.log(`   ${sev} [${flag.asset}] ${flag.type}: ${flag.signal}`);
      });

      console.log('\n📈 COMPOSITE SCORES:');
      Object.entries(report.composite_scores).forEach(([symbol, data]) => {
        const emoji = data.rating.includes('BULLISH') ? '🟢' : data.rating.includes('BEARISH') ? '🔴' : '⚪';
        console.log(`   ${emoji} ${symbol}: ${data.rating} (score: ${data.score})`);
      });

      console.log(`\n💾 Saved to: ${outputPath}`);
    }
  } catch (e) {
    console.error('❌ Error:', e.message);
    process.exit(1);
  }
}

module.exports = { fetchAlternativeData };

if (require.main === module) main();