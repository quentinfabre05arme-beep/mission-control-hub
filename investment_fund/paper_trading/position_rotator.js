const fs = require('fs');
const path = require('path');
const { fetchAllPrices } = require('../scripts/price_fetcher');

const PORTFOLIO_FILE = path.join(__dirname, 'PAPER_PORTFOLIO.json');
const TRADE_LOG = path.join(__dirname, 'TRADES_LOG.md');

function loadPortfolio() {
  return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

function logExit(trade) {
  const entry = `## EXIT — ${trade.timestamp}\n- **Ticker:** ${trade.ticker}\n- **Action:** SELL\n- **Shares:** ${trade.shares}\n- **Price:** $${trade.price.toFixed(2)}\n- **P&L:** $${trade.pnl.toFixed(2)} (${trade.pnlPct.toFixed(2)}%)\n- **Reason:** ${trade.reason}\n---\n`;
  fs.appendFileSync(TRADE_LOG, entry);
}

async function rotateWorstPerformers(maxPositions = 10, minHoldDays = 3) {
  const prices = await fetchAllPrices();
  const portfolio = loadPortfolio();
  const now = new Date();
  
  // Sort positions by unrealized P&L % (worst first)
  const ranked = portfolio.positions
    .map(p => {
      const price = prices[p.ticker]?.price || p.currentPrice;
      const pnlPct = ((price / p.entryPrice) - 1) * 100;
      const holdDays = (now - new Date(p.entryDate)) / (1000 * 60 * 60 * 24);
      return { ...p, currentPrice: price, pnlPct, holdDays };
    })
    .sort((a, b) => a.pnlPct - b.pnlPct);
  
  const toExit = [];
  const remaining = [];
  
  // Exit worst performers held for minHoldDays to get back under maxPositions
  let targetSlots = maxPositions;
  for (const pos of ranked) {
    if (portfolio.positions.length - toExit.length > targetSlots && pos.holdDays >= minHoldDays) {
      toExit.push(pos);
    } else {
      remaining.push(pos);
    }
  }
  
  // If still over limit, exit worst regardless of hold time
  if (portfolio.positions.length - toExit.length > targetSlots) {
    for (const pos of ranked) {
      if (!toExit.find(e => e.ticker === pos.ticker) && portfolio.positions.length - toExit.length > targetSlots) {
        toExit.push(pos);
      }
    }
  }
  
  for (const pos of toExit) {
    const price = pos.currentPrice;
    const pnl = (price - pos.entryPrice) * pos.shares;
    const pnlPct = ((price / pos.entryPrice) - 1) * 100;
    const commission = price * pos.shares * 0.001;
    
    console.log(`🔄 ROTATING OUT: ${pos.ticker} @ $${price.toFixed(2)} | P&L: $${pnl.toFixed(2)} (${pnlPct.toFixed(1)}%) | Held: ${pos.holdDays.toFixed(1)} days`);
    
    const trade = {
      timestamp: new Date().toISOString(),
      ticker: pos.ticker,
      shares: pos.shares,
      price: price,
      pnl: pnl - commission,
      pnlPct: pnlPct,
      reason: `Rotation — worst performer after ${pos.holdDays.toFixed(1)} days`
    };
    logExit(trade);
    
    portfolio.cash += (price * pos.shares) - commission;
    portfolio.performance.total_trades++;
    if (pnl > 0) portfolio.performance.winning_trades++;
    else portfolio.performance.losing_trades++;
  }
  
  portfolio.positions = remaining.map(({ pnlPct, holdDays, ...p }) => p);
  portfolio.current_value = portfolio.cash + remaining.reduce((sum, p) => sum + (p.currentPrice * p.shares), 0);
  portfolio.performance.total_return = ((portfolio.current_value / portfolio.initial_capital) - 1) * 100;
  
  if (portfolio.performance.total_trades > 0) {
    portfolio.performance.win_rate = (portfolio.performance.winning_trades / portfolio.performance.total_trades) * 100;
  }
  
  // Update max drawdown
  const peak = Math.max(portfolio.initial_capital, ...portfolio.daily_snapshots.map(s => s.value));
  const dd = peak > 0 ? (peak - portfolio.current_value) / peak * 100 : 0;
  if (dd > (portfolio.performance.max_drawdown || 0)) portfolio.performance.max_drawdown = dd;
  
  portfolio.daily_snapshots = portfolio.daily_snapshots || [];
  portfolio.daily_snapshots.push({
    date: new Date().toISOString().split('T')[0],
    value: portfolio.current_value,
    cash: portfolio.cash,
    positions_count: portfolio.positions.length,
    timestamp: new Date().toISOString()
  });
  
  savePortfolio(portfolio);
  return { exited: toExit.length, cash: portfolio.cash, positions: portfolio.positions.length };
}

module.exports = { rotateWorstPerformers };

if (require.main === module) {
  rotateWorstPerformers(10, 3).then(r => {
    console.log(`Exited: ${r.exited}, Cash: $${r.cash.toFixed(2)}, Positions: ${r.positions}`);
  }).catch(console.error);
}
