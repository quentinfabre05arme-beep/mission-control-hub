const fs = require('fs');
const { fetchAllPrices } = require('../scripts/price_fetcher');

async function buyTop3() {
  const prices = await fetchAllPrices();
  console.log('Prices fetched');
  
  let portfolio = { cash: 10000, positions: [], trades: [] };
  try {
    portfolio = JSON.parse(fs.readFileSync('PAPER_PORTFOLIO.json', 'utf8'));
  } catch(e) {}
  
  const opps = [
    { symbol: 'SOL', price: prices.SOL?.price || 76.66, score: 0.51 },
    { symbol: 'ETH', price: prices.ETH?.price || 1902.16, score: 0.35 },
    { symbol: 'BTC', price: prices.BTC?.price || 65080.00, score: 0.30 }
  ];
  
  console.log('\n=== AUTO-BUYING TOP 3 ===');
  
  for (const opp of opps) {
    const allocation = portfolio.cash * 0.15;
    const shares = allocation / opp.price;
    
    portfolio.positions.push({
      symbol: opp.symbol,
      entryPrice: opp.price,
      shares: shares,
      invested: allocation,
      entryDate: new Date().toISOString(),
      score: opp.score
    });
    
    portfolio.cash -= allocation;
    
    portfolio.trades.push({
      type: 'BUY',
      symbol: opp.symbol,
      price: opp.price,
      shares: shares,
      value: allocation,
      date: new Date().toISOString(),
      score: opp.score
    });
    
    console.log(`BUY: ${opp.symbol} @ $${opp.price.toFixed(2)} | Shares: ${shares.toFixed(6)} | Value: $${allocation.toFixed(2)}`);
  }
  
  fs.writeFileSync('PAPER_PORTFOLIO.json', JSON.stringify(portfolio, null, 2));
  console.log('\nPortfolio updated. Cash remaining: $' + portfolio.cash.toFixed(2));
}

buyTop3().catch(console.error);
