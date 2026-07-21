const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const PORTFOLIO_FILE = path.join(__dirname, 'portfolio.json');

function loadPortfolio() {
  if (!fs.existsSync(PORTFOLIO_FILE)) {
    return {
      cash: 10000,
      positions: [],
      trades: [],
      created_at: new Date().toISOString()
    };
  }
  return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
}

function savePortfolio(p) {
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(p, null, 2));
}

function getPrices() {
  const priceFile = path.join(DATA_DIR, 'market_data.json');
  if (!fs.existsSync(priceFile)) {
    console.error('No price data found');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(priceFile, 'utf8'));
}

function getAsymmetryData() {
  const asymFile = path.join(DATA_DIR, 'asymmetry_scores.json');
  if (!fs.existsSync(asymFile)) {
    console.error('No asymmetry data found');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(asymFile, 'utf8'));
}

function main() {
  const portfolio = loadPortfolio();
  const prices = getPrices();
  const asymmetry = getAsymmetryData();

  // Build scored list
  const scored = [];
  for (const [sym, score] of Object.entries(asymmetry.scores || {})) {
    const priceData = prices[sym];
    if (!priceData || !priceData.price) continue;
    scored.push({
      symbol: sym,
      score: score,
      price: priceData.price,
      change24h: priceData.change24h || 0
    });
  }

  scored.sort((a, b) => b.score - a.score);
  console.log('=== TOP ASYMMETRY ===');
  scored.slice(0, 5).forEach((s, i) => {
    console.log(`${i + 1}. ${s.symbol}: Score ${s.score.toFixed(2)} | $${s.price.toFixed(2)} (${s.change24h > 0 ? '+' : ''}${s.change24h.toFixed(1)}%)`);
  });

  // Buy top 3 not already held
  const heldSymbols = new Set(portfolio.positions.map(p => p.symbol));
  const toBuy = scored.filter(s => !heldSymbols.has(s.symbol)).slice(0, 3);

  if (toBuy.length === 0) {
    console.log('No new opportunities — top 3 already held');
    return;
  }

  const allocPerTrade = portfolio.cash / toBuy.length;

  for (const opp of toBuy) {
    const qty = Math.floor(allocPerTrade / opp.price);
    if (qty < 1) {
      console.log(`SKIP ${opp.symbol}: Insufficient cash (${portfolio.cash.toFixed(2)})`);
      continue;
    }

    const cost = qty * opp.price;
    portfolio.positions.push({
      symbol: opp.symbol,
      entryPrice: opp.price,
      currentPrice: opp.price,
      quantity: qty,
      entryDate: new Date().toISOString().split('T')[0],
      status: 'open'
    });
    portfolio.cash -= cost;
    portfolio.trades.push({
      symbol: opp.symbol,
      type: 'buy',
      price: opp.price,
      quantity: qty,
      date: new Date().toISOString().split('T')[0],
      reason: `Auto-enter: asymmetry score ${opp.score.toFixed(2)}`
    });
    console.log(`BUY ${opp.symbol}: ${qty} shares @ $${opp.price.toFixed(2)} = $${cost.toFixed(2)}`);
  }

  savePortfolio(portfolio);
  console.log(`Cash remaining: $${portfolio.cash.toFixed(2)}`);
}

main();
