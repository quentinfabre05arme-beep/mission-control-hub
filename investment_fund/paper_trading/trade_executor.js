/**
 * ALPHA FUND - PAPER TRADE EXECUTOR v2
 * Real prices, proper scoring, P&L tracking
 */

const fs = require('fs');
const path = require('path');
const { fetchAllPrices } = require('../scripts/price_fetcher');

const CONFIG = {
  PORTFOLIO_FILE: path.join(__dirname, 'PAPER_PORTFOLIO.json'),
  TRADE_LOG: path.join(__dirname, 'TRADES_LOG.md'),
  MAX_POSITIONS: 10,
  COMMISSION_RATE: 0.001, // 0.1%
  MAX_POSITION_PCT: 0.15, // Max 15% per position
  MIN_ASYMMETRY_SCORE: 0.25,
  INITIAL_CAPITAL: 10000
};

function loadPortfolio() {
  if (!fs.existsSync(CONFIG.PORTFOLIO_FILE)) {
    const fresh = {
      portfolio_id: 'alpha-paper-001',
      created_at: new Date().toISOString(),
      initial_capital: CONFIG.INITIAL_CAPITAL,
      current_value: CONFIG.INITIAL_CAPITAL,
      cash: CONFIG.INITIAL_CAPITAL,
      positions: [],
      trades: [],
      performance: {
        total_return: 0,
        total_trades: 0,
        winning_trades: 0,
        losing_trades: 0,
        win_rate: 0,
        avg_winner: 0,
        avg_loser: 0,
        max_drawdown: 0
      }
    };
    fs.writeFileSync(CONFIG.PORTFOLIO_FILE, JSON.stringify(fresh, null, 2));
    return fresh;
  }
  return JSON.parse(fs.readFileSync(CONFIG.PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(CONFIG.PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

function logTrade(trade) {
  const entry = `## Trade ${trade.id} — ${trade.timestamp}

- **Ticker:** ${trade.ticker}
- **Action:** ${trade.action}
- **Shares:** ${trade.shares}
- **Price:** $${trade.price.toFixed(2)}
- **Total:** $${trade.total.toFixed(2)}
- **Commission:** $${trade.commission.toFixed(2)}
- **Reason:** ${trade.reason}
- **Stop Loss:** $${trade.stopLoss?.toFixed(2) || 'N/A'}
- **Take Profit:** $${trade.takeProfit?.toFixed(2) || 'N/A'}

---
`;
  fs.appendFileSync(CONFIG.TRADE_LOG, entry);
}

function calculateAsymmetry(ticker, price, change24h) {
  // Simple asymmetry model: upside potential vs downside risk
  // Higher volatility = higher potential but also higher risk
  const volatility = Math.abs(change24h);
  const trend = change24h;
  
  // Base scores by ticker category (simplified - in production use more sophisticated models)
  const upsidePotential = {
    BTC: 0.30, ETH: 0.35, SOL: 0.50,
    MSTR: 0.45, HIMS: 0.55, NVDA: 0.25,
    TSLA: 0.50, PLTR: 0.55, CRWD: 0.35,
    SNOW: 0.40, COIN: 0.60, LLY: 0.18,
    META: 0.22, AMD: 0.35
  };
  
  const base = upsidePotential[ticker] || 0.25;
  
  // Adjust for recent move (mean reversion vs momentum)
  let score;
  if (trend < -2) {
    // Downtrend - higher upside if oversold
    score = base * 1.4;
  } else if (trend < -5) {
    score = base * 2.0;
  } else if (trend > 5) {
    // Strong uptrend - lower asymmetry (already moved)
    score = base * 0.6;
  } else if (trend > 2) {
    score = base * 0.85;
  } else {
    score = base;
  }
  
  // Volatility boost (more volatile = more potential)
  score *= (1 + volatility / 100);
  
  // Calculate targets
  const targetPrice = price * (1 + score);
  const floorPrice = price * (1 - base * 0.5); // Half the upside as downside
  
  return {
    asymmetryScore: parseFloat(score.toFixed(2)),
    upside: parseFloat((score * 100).toFixed(1)),
    downside: parseFloat((-base * 0.5 * 100).toFixed(1)),
    targetPrice: parseFloat(targetPrice.toFixed(2)),
    floorPrice: parseFloat(floorPrice.toFixed(2)),
    catalyst: `${ticker} - ${trend > 0 ? 'momentum' : 'oversold'} setup (${volatility.toFixed(1)}% move)`,
    confidence: Math.min(95, Math.round(60 + score * 100))
  };
}

async function getOpportunities() {
  const prices = await fetchAllPrices();
  const opportunities = [];
  
  for (const [ticker, data] of Object.entries(prices)) {
    const setup = calculateAsymmetry(ticker, data.price, data.change24h);
    opportunities.push({
      ticker,
      currentPrice: data.price,
      change24h: data.change24h,
      ...setup
    });
  }
  
  // Sort by asymmetry score descending
  opportunities.sort((a, b) => b.asymmetryScore - a.asymmetryScore);
  return opportunities;
}

function executePaperTrade(opportunity) {
  const portfolio = loadPortfolio();
  
  // Check if already holding
  const existing = portfolio.positions.find(p => p.ticker === opportunity.ticker);
  if (existing) {
    console.log(`⚠️ Already holding ${opportunity.ticker}, skipping`);
    return null;
  }
  
  // Check position limit
  if (portfolio.positions.length >= CONFIG.MAX_POSITIONS) {
    console.log(`⚠️ Max positions (${CONFIG.MAX_POSITIONS}) reached`);
    return null;
  }
  
  // Calculate position size (max 15% of portfolio, max $1500 for $10K fund)
  const positionSize = Math.min(
    portfolio.cash * CONFIG.MAX_POSITION_PCT,
    1500
  );
  
  // Support fractional shares for high-priced assets
  const shares = opportunity.currentPrice > 500 
    ? parseFloat((positionSize / opportunity.currentPrice).toFixed(6))
    : Math.floor(positionSize / opportunity.currentPrice);
    
  if (shares < 0.001) {
    console.log(`⚠️ Insufficient funds for ${opportunity.ticker} @ $${opportunity.currentPrice}`);
    return null;
  }
  
  const total = shares * opportunity.currentPrice;
  const commission = total * CONFIG.COMMISSION_RATE;
  
  if (total + commission > portfolio.cash) {
    console.log(`⚠️ Not enough cash for ${opportunity.ticker}`);
    return null;
  }
  
  const trade = {
    id: `T${Date.now()}`,
    timestamp: new Date().toISOString(),
    ticker: opportunity.ticker,
    action: 'BUY',
    shares,
    price: opportunity.currentPrice,
    total,
    commission,
    reason: opportunity.catalyst,
    stopLoss: opportunity.floorPrice,
    takeProfit: opportunity.targetPrice
  };
  
  // Update portfolio
  portfolio.cash -= (total + commission);
  portfolio.positions.push({
    ticker: opportunity.ticker,
    shares: parseFloat(shares.toFixed(6)),
    entryPrice: opportunity.currentPrice,
    currentPrice: opportunity.currentPrice,
    stopLoss: opportunity.floorPrice,
    takeProfit: opportunity.targetPrice,
    entryDate: new Date().toISOString(),
    unrealizedPnl: -commission
  });
  
  portfolio.trades.push(trade);
  portfolio.performance.total_trades++;
  
  savePortfolio(portfolio);
  logTrade(trade);
  
  console.log(`\n✅ PAPER TRADE EXECUTED`);
  console.log(`   ${trade.shares >= 1 ? Math.floor(trade.shares) : trade.shares.toFixed(4)} shares of ${trade.ticker} @ $${trade.price.toFixed(2)}`);
  console.log(`   Total: $${trade.total.toFixed(2)} | Commission: $${trade.commission.toFixed(2)}`);
  console.log(`   Cash remaining: $${portfolio.cash.toFixed(2)}`);
  console.log(`   Target: $${trade.takeProfit.toFixed(2)} | Stop: $${trade.stopLoss.toFixed(2)}`);
  
  return trade;
}

async function updatePrices() {
  const portfolio = loadPortfolio();
  const prices = await fetchAllPrices();
  
  let totalValue = portfolio.cash;
  let maxDrawdown = portfolio.performance.max_drawdown || 0;
  
  for (const position of portfolio.positions) {
    const priceData = prices[position.ticker];
    if (priceData) {
      position.currentPrice = priceData.price;
      position.unrealizedPnl = (position.currentPrice - position.entryPrice) * position.shares;
      position.unrealizedPnlPct = ((position.currentPrice / position.entryPrice) - 1) * 100;
    }
    totalValue += position.currentPrice * position.shares;
  }
  
  portfolio.current_value = totalValue;
  portfolio.performance.total_return = (totalValue / portfolio.initial_capital - 1) * 100;
  
  // Update max drawdown
  const peak = Math.max(portfolio.initial_capital, ...portfolio.trades.map(() => portfolio.current_value));
  const dd = (peak - totalValue) / peak * 100;
  if (dd > maxDrawdown) maxDrawdown = dd;
  portfolio.performance.max_drawdown = maxDrawdown;
  
  savePortfolio(portfolio);
  return portfolio;
}

function showPortfolio() {
  const portfolio = loadPortfolio();
  
  console.log(`\n📊 ALPHA FUND PAPER PORTFOLIO`);
  console.log(`   Initial: $${portfolio.initial_capital.toLocaleString()}`);
  console.log(`   Current: $${portfolio.current_value.toFixed(2)} (${portfolio.performance.total_return >= 0 ? '+' : ''}${portfolio.performance.total_return.toFixed(2)}%)`);
  console.log(`   Cash: $${portfolio.cash.toFixed(2)}`);
  console.log(`   Positions: ${portfolio.positions.length}/${CONFIG.MAX_POSITIONS}`);
  console.log(`   Trades: ${portfolio.performance.total_trades} | Win Rate: ${portfolio.performance.win_rate.toFixed(1)}%`);
  console.log(`   Max Drawdown: ${portfolio.performance.max_drawdown.toFixed(1)}%`);
  
  if (portfolio.positions.length > 0) {
    console.log(`\n   OPEN POSITIONS:`);
    portfolio.positions.forEach(p => {
      const emoji = p.unrealizedPnl >= 0 ? '🟢' : '🔴';
      const pct = ((p.currentPrice / p.entryPrice - 1) * 100).toFixed(1);
      console.log(`   ${emoji} ${p.ticker}: ${p.shares >= 1 ? Math.floor(p.shares) : p.shares.toFixed(4)} shares @ $${p.entryPrice.toFixed(2)} → $${p.currentPrice.toFixed(2)} | P&L: $${p.unrealizedPnl.toFixed(2)} (${pct}%)`);
    });
  }
}

async function autoTrade(topN = 3) {
  console.log('\n🔍 SCANNING FOR OPPORTUNITIES...\n');
  const opportunities = await getOpportunities();
  
  console.log('=== TOP ASYMMETRY SCORES ===');
  opportunities.slice(0, 8).forEach((o, i) => {
    console.log(`${i+1}. ${o.ticker}: Score ${o.asymmetryScore} | $${o.currentPrice.toFixed(2)} (${o.change24h >= 0 ? '+' : ''}${o.change24h.toFixed(1)}%)`);
    console.log(`   Upside: ${o.upside}% | Downside: ${o.downside}% | Conf: ${o.confidence}%`);
  });
  
  const topOpps = opportunities
    .filter(o => o.asymmetryScore >= CONFIG.MIN_ASYMMETRY_SCORE)
    .slice(0, topN);
  
  if (topOpps.length === 0) {
    console.log('\n⚠️ No opportunities meet minimum asymmetry threshold');
    return;
  }
  
  console.log(`\n🎯 AUTO-ENTERING TOP ${topOpps.length} OPPORTUNITIES`);
  for (const opp of topOpps) {
    executePaperTrade(opp);
  }
}

// Run
const mode = process.argv[2] || 'status';

(async () => {
  switch (mode) {
    case 'buy':
      const topN = process.argv[3] === '--auto-top3' ? 3 : 1;
      await autoTrade(topN);
      break;
    case 'buy-top3':
      await autoTrade(3);
      break;
    case 'update':
      await updatePrices();
      showPortfolio();
      break;
    case 'status':
      await updatePrices();
      showPortfolio();
      break;
    case 'scan':
      const opps = await getOpportunities();
      opps.forEach((o, i) => {
        console.log(`${i+1}. ${o.ticker}: ${o.asymmetryScore} | $${o.currentPrice.toFixed(2)} | ${o.catalyst}`);
      });
      break;
    default:
      console.log('Usage: node trade_executor.js [buy|buy-top3|update|status|scan] [--auto-top3]');
  }
})();

module.exports = { executePaperTrade, updatePrices, showPortfolio, getOpportunities };
