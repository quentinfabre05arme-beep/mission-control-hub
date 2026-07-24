/**
 * ALPHA FUND - EMERGENCY POSITION SELLER
 * Sells specified position to free up cash for new opportunities
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  PORTFOLIO_FILE: path.join(__dirname, 'PAPER_PORTFOLIO.json'),
  TRADE_LOG: path.join(__dirname, 'TRADES_LOG.md'),
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

function sellPosition(ticker) {
  const portfolio = loadPortfolio();
  
  const positionIndex = portfolio.positions.findIndex(p => p.ticker === ticker);
  if (positionIndex === -1) {
    console.log(`❌ Position ${ticker} not found`);
    return null;
  }
  
  const position = portfolio.positions[positionIndex];
  const currentPrice = position.currentPrice || position.entryPrice;
  
  const total = position.shares * currentPrice;
  const commission = total * CONFIG.COMMISSION_RATE;
  const pnl = (currentPrice - position.entryPrice) * position.shares;
  const pnlPct = ((currentPrice / position.entryPrice) - 1) * 100;
  
  // Remove position
  portfolio.positions.splice(positionIndex, 1);
  portfolio.cash += (total - commission);
  
  // Log trade
  const trade = {
    id: `SELL${Date.now()}`,
    timestamp: new Date().toISOString(),
    ticker: position.ticker,
    action: 'SELL',
    shares: position.shares,
    price: currentPrice,
    total: total - commission,
    commission: commission,
    pnl: pnl,
    pnlPct: pnlPct,
    reason: `Manual sell — ${pnlPct.toFixed(1)}% P&L, freeing cash for better opportunities`
  };
  
  portfolio.trades.push(trade);
  
  // Update performance
  portfolio.performance.total_trades++;
  if (pnl > 0) {
    portfolio.performance.winning_trades++;
  } else {
    portfolio.performance.losing_trades++;
  }
  
  // Recalculate win rate
  const closedTrades = portfolio.trades.filter(t => t.action === 'SELL');
  const winners = closedTrades.filter(t => t.pnl > 0).length;
  portfolio.performance.win_rate = closedTrades.length > 0 ? (winners / closedTrades.length) * 100 : 0;
  
  logTrade(trade);
  savePortfolio(portfolio);
  
  console.log(`✅ SOLD ${position.ticker}: ${position.shares} shares @ $${currentPrice.toFixed(2)}`);
  console.log(`   P&L: $${pnl.toFixed(2)} (${pnlPct.toFixed(1)}%)`);
  console.log(`   Cash freed: $${(total - commission).toFixed(2)}`);
  console.log(`   New cash balance: $${portfolio.cash.toFixed(2)}`);
  
  return trade;
}

// Sell the worst performer
const tickerToSell = process.argv[2];
if (!tickerToSell) {
  console.log('Usage: node sell_position.js <TICKER>');
  console.log('Example: node sell_position.js MSTR');
  process.exit(1);
}

sellPosition(tickerToSell);
