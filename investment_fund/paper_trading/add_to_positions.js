const { fetchAllPrices } = require('../scripts/price_fetcher');
const fs = require('fs');
const path = require('path');

const PORTFOLIO_FILE = path.join(__dirname, 'PAPER_PORTFOLIO.json');

function loadPortfolio() {
  return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(portfolio) {
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(portfolio, null, 2));
}

async function addToPosition(ticker, additionalValue) {
  const prices = await fetchAllPrices();
  const price = prices[ticker]?.price;
  if (!price) {
    console.log(`❌ No price for ${ticker}`);
    return;
  }
  
  const portfolio = loadPortfolio();
  const pos = portfolio.positions.find(p => p.ticker === ticker);
  if (!pos) {
    console.log(`❌ No position in ${ticker}`);
    return;
  }
  
  const commission = additionalValue * 0.001;
  const totalCost = additionalValue + commission;
  
  if (portfolio.cash < totalCost) {
    console.log(`❌ Not enough cash. Need $${totalCost.toFixed(2)}, have $${portfolio.cash.toFixed(2)}`);
    return;
  }
  
  const additionalShares = ticker === 'BTC' || ticker === 'ETH' 
    ? parseFloat((additionalValue / price).toFixed(6))
    : Math.floor(additionalValue / price);
    
  pos.shares = parseFloat((pos.shares + additionalShares).toFixed(6));
  // Weighted average entry
  const oldValue = (pos.entryPrice * (pos.shares - additionalShares));
  const newValue = price * additionalShares;
  pos.entryPrice = (oldValue + newValue) / pos.shares;
  pos.currentPrice = price;
  
  portfolio.cash -= totalCost;
  
  portfolio.trades.push({
    id: `T${Date.now()}`,
    timestamp: new Date().toISOString(),
    ticker,
    action: 'BUY_ADD',
    shares: additionalShares,
    price,
    total: additionalValue,
    commission,
    reason: `Adding to ${ticker} position — high asymmetry`
  });
  
  savePortfolio(portfolio);
  console.log(`✅ Added ${additionalShares} ${ticker} @ $${price.toFixed(2)} | Total cost: $${totalCost.toFixed(2)}`);
}

(async () => {
  // Add to SOL (highest asymmetry 0.72) and ETH (0.5)
  const portfolio = loadPortfolio();
  const cashPerAdd = Math.min(1000, portfolio.cash / 3);
  
  if (portfolio.cash >= cashPerAdd + 10) {
    await addToPosition('SOL', cashPerAdd);
  }
  
  const portfolio2 = loadPortfolio();
  if (portfolio2.cash >= cashPerAdd + 10) {
    await addToPosition('ETH', cashPerAdd);
  }
  
  const portfolio3 = loadPortfolio();
  if (portfolio3.cash >= cashPerAdd + 10) {
    await addToPosition('BTC', cashPerAdd);
  }
})();
