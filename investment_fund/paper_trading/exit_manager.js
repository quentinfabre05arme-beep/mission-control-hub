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

async function checkExits() {
  const prices = await fetchAllPrices();
  const portfolio = loadPortfolio();
  let exited = 0;
  const remaining = [];
  
  for (const pos of portfolio.positions) {
    const price = prices[pos.ticker]?.price;
    if (!price) {
      remaining.push(pos);
      continue;
    }
    
    const pnl = (price - pos.entryPrice) * pos.shares;
    const pnlPct = ((price / pos.entryPrice) - 1) * 100;
    
    // Check stop loss
    if (price <= pos.stopLoss) {
      console.log(`🛑 STOP LOSS: ${pos.ticker} @ $${price.toFixed(2)} (stop: $${pos.stopLoss.toFixed(2)})`);
      const trade = {
        timestamp: new Date().toISOString(),
        ticker: pos.ticker,
        shares: pos.shares,
        price: price,
        pnl: pnl - pos.entryPrice * pos.shares * 0.001, // minus commission
        pnlPct: pnlPct,
        reason: `Stop loss hit at $${price.toFixed(2)}`
      };
      logExit(trade);
      portfolio.cash += (price * pos.shares) - (price * pos.shares * 0.001);
      portfolio.performance.total_trades++;
      if (pnl > 0) portfolio.performance.winning_trades++;
      else portfolio.performance.losing_trades++;
      exited++;
      continue;
    }
    
    // Check take profit
    if (price >= pos.takeProfit) {
      console.log(`🎯 TAKE PROFIT: ${pos.ticker} @ $${price.toFixed(2)} (target: $${pos.takeProfit.toFixed(2)})`);
      const trade = {
        timestamp: new Date().toISOString(),
        ticker: pos.ticker,
        shares: pos.shares,
        price: price,
        pnl: pnl - pos.entryPrice * pos.shares * 0.001,
        pnlPct: pnlPct,
        reason: `Take profit hit at $${price.toFixed(2)}`
      };
      logExit(trade);
      portfolio.cash += (price * pos.shares) - (price * pos.shares * 0.001);
      portfolio.performance.total_trades++;
      portfolio.performance.winning_trades++;
      exited++;
      continue;
    }
    
    remaining.push(pos);
  }
  
  portfolio.positions = remaining;
  portfolio.current_value = portfolio.cash + remaining.reduce((sum, p) => {
    const price = prices[p.ticker]?.price || p.currentPrice;
    return sum + price * p.shares;
  }, 0);
  
  if (exited > 0) {
    portfolio.performance.total_return = ((portfolio.current_value / portfolio.initial_capital) - 1) * 100;
    if (portfolio.performance.total_trades > 0) {
      portfolio.performance.win_rate = (portfolio.performance.winning_trades / portfolio.performance.total_trades) * 100;
    }
    
    // Add daily snapshot
    portfolio.daily_snapshots = portfolio.daily_snapshots || [];
    portfolio.daily_snapshots.push({
      date: new Date().toISOString().split('T')[0],
      value: portfolio.current_value,
      cash: portfolio.cash,
      positions_count: portfolio.positions.length,
      timestamp: new Date().toISOString()
    });
  }
  
  savePortfolio(portfolio);
  return { exited, cash: portfolio.cash, positions: portfolio.positions.length };
}

module.exports = { checkExits };

if (require.main === module) {
  checkExits().then(r => {
    console.log(`Exits: ${r.exited}, Cash: $${r.cash.toFixed(2)}, Positions: ${r.positions}`);
  }).catch(console.error);
}
