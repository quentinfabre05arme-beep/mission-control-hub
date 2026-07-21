/**
 * ALPHA FUND - DAILY PRICE UPDATE
 * Updates portfolio with current prices, tracks P&L
 * Run daily at market close or via cron
 */

const fs = require('fs');
const path = require('path');
const { fetchAllPrices } = require('../scripts/price_fetcher');

const PORTFOLIO_FILE = path.join(__dirname, 'PAPER_PORTFOLIO.json');

function loadPortfolio() {
  return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

async function updatePrices() {
  const portfolio = loadPortfolio();
  const prices = await fetchAllPrices();
  const timestamp = new Date().toISOString();
  
  let totalValue = portfolio.cash;
  let unrealizedPnlTotal = 0;
  
  for (const position of portfolio.positions) {
    const priceData = prices[position.ticker];
    if (priceData) {
      position.currentPrice = priceData.price;
      position.unrealizedPnl = (position.currentPrice - position.entryPrice) * position.shares;
      position.unrealizedPnlPct = ((position.currentPrice / position.entryPrice) - 1) * 100;
      unrealizedPnlTotal += position.unrealizedPnl;
    }
    totalValue += position.currentPrice * position.shares;
  }
  
  portfolio.current_value = totalValue;
  portfolio.performance.total_return = (totalValue / portfolio.initial_capital - 1) * 100;
  
  // Max drawdown
  const peak = portfolio.initial_capital; // Simplified
  const dd = (peak - totalValue) / peak * 100;
  if (dd > portfolio.performance.max_drawdown) {
    portfolio.performance.max_drawdown = dd;
  }
  
  // Daily snapshot
  if (!portfolio.daily_snapshots) portfolio.daily_snapshots = [];
  portfolio.daily_snapshots.push({
    date: timestamp.split('T')[0],
    value: totalValue,
    cash: portfolio.cash,
    unrealized_pnl: unrealizedPnlTotal,
    positions_count: portfolio.positions.length
  });
  
  // Keep only last 30 days
  if (portfolio.daily_snapshots.length > 30) {
    portfolio.daily_snapshots = portfolio.daily_snapshots.slice(-30);
  }
  
  savePortfolio(portfolio);
  
  console.log(`📈 Daily Update — ${timestamp}`);
  console.log(`   Portfolio Value: $${totalValue.toFixed(2)}`);
  console.log(`   Total Return: ${portfolio.performance.total_return.toFixed(2)}%`);
  console.log(`   Unrealized P&L: $${unrealizedPnlTotal.toFixed(2)}`);
  console.log(`   Cash: $${portfolio.cash.toFixed(2)}`);
  console.log(`   Positions: ${portfolio.positions.length}`);
  
  return portfolio;
}

updatePrices().catch(e => console.error('Update failed:', e.message));
