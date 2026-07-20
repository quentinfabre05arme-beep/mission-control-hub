/**
 * PAPER TRADE EXECUTOR
 * Simulates trades without real money
 * Tracks P&L, validates strategy before going live
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  PORTFOLIO_FILE: path.join(__dirname, 'PAPER_PORTFOLIO.json'),
  TRADE_LOG: path.join(__dirname, 'TRADES_LOG.md'),
  MAX_POSITIONS: 10,
  COMMISSION_RATE: 0.001 // 0.1%
};

function loadPortfolio() {
  return JSON.parse(fs.readFileSync(CONFIG.PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(CONFIG.PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

function logTrade(trade) {
  const entry = `
## Trade ${trade.id} — ${trade.timestamp}

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

function executePaperTrade(opportunity) {
  const portfolio = loadPortfolio();
  
  // Check if already have position
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
  
  // Calculate position size
  const positionSize = Math.min(
    portfolio.cash * 0.10, // Max 10% per position
    1000 // Max $1K per trade for paper testing
  );
  
  const shares = Math.floor(positionSize / opportunity.currentPrice);
  if (shares < 1) {
    console.log(`⚠️ Insufficient funds for ${opportunity.ticker}`);
    return null;
  }
  
  const total = shares * opportunity.currentPrice;
  const commission = total * CONFIG.COMMISSION_RATE;
  
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
    shares,
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
  console.log(`   ${trade.shares} shares of ${trade.ticker} @ $${trade.price.toFixed(2)}`);
  console.log(`   Total: $${trade.total.toFixed(2)} | Cash remaining: $${portfolio.cash.toFixed(2)}`);
  
  return trade;
}

function updatePrices() {
  const portfolio = loadPortfolio();
  let totalValue = portfolio.cash;
  
  for (const position of portfolio.positions) {
    // Mock price update (in production, fetch real prices)
    const change = (Math.random() - 0.5) * 0.02; // ±1%
    position.currentPrice *= (1 + change);
    position.unrealizedPnl = (position.currentPrice - position.entryPrice) * position.shares;
    totalValue += position.currentPrice * position.shares;
  }
  
  portfolio.current_value = totalValue;
  portfolio.performance.total_return = (totalValue / portfolio.initial_capital - 1) * 100;
  
  savePortfolio(portfolio);
  return portfolio;
}

function showPortfolio() {
  const portfolio = loadPortfolio();
  
  console.log(`\n📊 PAPER PORTFOLIO`);
  console.log(`   Initial: $${portfolio.initial_capital.toLocaleString()}`);
  console.log(`   Current: $${portfolio.current_value.toFixed(2)} (${portfolio.performance.total_return.toFixed(2)}%)`);
  console.log(`   Cash: $${portfolio.cash.toFixed(2)}`);
  console.log(`   Positions: ${portfolio.positions.length}/${CONFIG.MAX_POSITIONS}`);
  
  if (portfolio.positions.length > 0) {
    console.log(`\n   OPEN POSITIONS:`);
    portfolio.positions.forEach(p => {
      const emoji = p.unrealizedPnl >= 0 ? '🟢' : '🔴';
      console.log(`   ${emoji} ${p.ticker}: ${p.shares} shares @ $${p.entryPrice.toFixed(2)} → $${p.currentPrice.toFixed(2)} | P&L: $${p.unrealizedPnl.toFixed(2)}`);
    });
  }
}

// Auto-execute if opportunities exist
function autoTrade() {
  const oppDir = path.join(__dirname, '..', 'opportunities');
  const files = fs.readdirSync(oppDir)
    .filter(f => f.startsWith('scan_'))
    .sort()
    .slice(-1);
  
  if (files.length === 0) return;
  
  const data = JSON.parse(fs.readFileSync(path.join(oppDir, files[0]), 'utf8'));
  const topOpps = data.opportunities
    .filter(o => o.asymmetryScore >= 5.0)
    .slice(0, 3);
  
  for (const opp of topOpps) {
    executePaperTrade(opp);
  }
}

// Run
const mode = process.argv[2] || 'status';

switch (mode) {
  case 'buy':
    autoTrade();
    break;
  case 'update':
    updatePrices();
    showPortfolio();
    break;
  case 'status':
    showPortfolio();
    break;
  default:
    console.log('Usage: node trade_executor.js [buy|update|status]');
}

module.exports = { executePaperTrade, updatePrices, showPortfolio };
