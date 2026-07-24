/**
 * ALPHA FUND - POSITION ROTATION SCRIPT
 * Sells losers below threshold, reallocates to best opportunities
 */

const fs = require('fs');
const path = require('path');
const { fetchAllPrices } = require('../scripts/price_fetcher');

const CONFIG = {
  PORTFOLIO_FILE: path.join(__dirname, 'PAPER_PORTFOLIO.json'),
  TRADE_LOG: path.join(__dirname, 'TRADES_LOG.md'),
  ROTATION_THRESHOLD: -0.03, // Sell if down >3%
  MIN_HOLD_DAYS: 1,
  COMMISSION_RATE: 0.001
};

function loadPortfolio() {
  return JSON.parse(fs.readFileSync(CONFIG.PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(CONFIG.PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

function logTrade(trade) {
  const entry = `## EXIT — ${new Date().toISOString()}
- **Ticker:** ${trade.ticker}
- **Action:** SELL
- **Shares:** ${trade.shares}
- **Price:** $${trade.price.toFixed(2)}
- **P&L:** $${trade.pnl.toFixed(2)} (${trade.pnlPct.toFixed(2)}%)
- **Reason:** ${trade.reason}
---
`;
  fs.appendFileSync(CONFIG.TRADE_LOG, entry);
}

function calculateAsymmetry(ticker, price, change24h) {
  const upsidePotential = {
    BTC: 0.30, ETH: 0.35, SOL: 0.50,
    MSTR: 0.45, HIMS: 0.55, NVDA: 0.25,
    TSLA: 0.50, PLTR: 0.55, CRWD: 0.35,
    SNOW: 0.40, COIN: 0.60, LLY: 0.18,
    META: 0.22, AMD: 0.35
  };
  
  const base = upsidePotential[ticker] || 0.25;
  let score;
  
  if (change24h < -5) {
    score = base * 2.0;
  } else if (change24h < -2) {
    score = base * 1.4;
  } else if (change24h > 5) {
    score = base * 0.6;
  } else if (change24h > 2) {
    score = base * 0.85;
  } else {
    score = base;
  }
  
  score *= (1 + Math.abs(change24h) / 100);
  
  return {
    asymmetryScore: parseFloat(score.toFixed(2)),
    upside: parseFloat((score * 100).toFixed(1)),
    downside: parseFloat((-base * 0.5 * 100).toFixed(1)),
    targetPrice: parseFloat((price * (1 + score)).toFixed(2)),
    floorPrice: parseFloat((price * (1 - base * 0.5)).toFixed(2)),
    confidence: Math.min(95, Math.round(60 + score * 100))
  };
}

async function rotatePositions() {
  const portfolio = loadPortfolio();
  const prices = await fetchAllPrices();
  
  console.log('🔄 ROTATION SCAN — Checking for losers to sell...\n');
  
  const heldTickers = new Set(portfolio.positions.map(p => p.ticker));
  let soldCount = 0;
  let freedCash = 0;
  
  // Check each position for rotation
  for (const position of [...portfolio.positions]) {
    const priceData = prices[position.ticker];
    if (!priceData) continue;
    
    position.currentPrice = priceData.price;
    const pnlPct = ((position.currentPrice / position.entryPrice) - 1);
    const holdDays = (Date.now() - new Date(position.entryDate).getTime()) / (1000 * 60 * 60 * 24);
    
    // Sell if down >5% and held for at least MIN_HOLD_DAYS
    if (pnlPct < CONFIG.ROTATION_THRESHOLD && holdDays >= CONFIG.MIN_HOLD_DAYS) {
      const total = position.shares * position.currentPrice;
      const commission = total * CONFIG.COMMISSION_RATE;
      const pnl = (position.currentPrice - position.entryPrice) * position.shares;
      
      // Remove position
      portfolio.positions = portfolio.positions.filter(p => p.ticker !== position.ticker);
      portfolio.cash += (total - commission);
      freedCash += (total - commission);
      
      // Log trade
      const trade = {
        id: `SELL${Date.now()}`,
        timestamp: new Date().toISOString(),
        ticker: position.ticker,
        action: 'SELL',
        shares: position.shares,
        price: position.currentPrice,
        total: total - commission,
        commission: commission,
        pnl: pnl,
        pnlPct: pnlPct * 100,
        reason: `Rotation — down ${(pnlPct * 100).toFixed(1)}% after ${holdDays.toFixed(1)} days`
      };
      
      portfolio.trades.push(trade);
      
      // Update performance
      portfolio.performance.total_trades++;
      if (pnl > 0) {
        portfolio.performance.winning_trades++;
      } else {
        portfolio.performance.losing_trades++;
      }
      
      logTrade(trade);
      
      console.log(`❌ SOLD ${position.ticker}: ${position.shares} shares @ $${position.currentPrice.toFixed(2)}`);
      console.log(`   P&L: $${pnl.toFixed(2)} (${(pnlPct * 100).toFixed(1)}%) | Cash freed: $${(total - commission).toFixed(2)}`);
      
      soldCount++;
    }
  }
  
  if (soldCount === 0) {
    console.log('✅ No positions need rotation (all within -5% threshold)');
  } else {
    console.log(`\n💰 Total cash freed: $${freedCash.toFixed(2)}`);
    console.log(`💵 New cash balance: $${portfolio.cash.toFixed(2)}`);
  }
  
  // Now scan for new opportunities with freed cash
  const opportunities = [];
  for (const [ticker, data] of Object.entries(prices)) {
    if (heldTickers.has(ticker) && soldCount === 0) continue; // Skip held unless we sold something
    const setup = calculateAsymmetry(ticker, data.price, data.change24h);
    opportunities.push({
      ticker,
      currentPrice: data.price,
      ...setup
    });
  }
  
  opportunities.sort((a, b) => b.asymmetryScore - a.asymmetryScore);
  
  console.log('\n📊 TOP OPPORTUNITIES:');
  opportunities.slice(0, 5).forEach((o, i) => {
    const held = heldTickers.has(o.ticker) ? ' [HELD]' : '';
    console.log(`${i+1}. ${o.ticker}: Score ${o.asymmetryScore}${held} | $${o.currentPrice.toFixed(2)}`);
  });
  
  savePortfolio(portfolio);
  
  return { soldCount, freedCash, topOpportunities: opportunities.slice(0, 3) };
}

// Run if called directly
if (require.main === module) {
  rotatePositions().then(result => {
    console.log('\n✅ Rotation complete');
    process.exit(0);
  }).catch(err => {
    console.error('❌ Error:', err);
    process.exit(1);
  });
}

module.exports = { rotatePositions };
