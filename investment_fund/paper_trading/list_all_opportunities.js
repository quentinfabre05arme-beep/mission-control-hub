const { fetchAllPrices } = require('../scripts/price_fetcher');

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
  if (change24h < -5) score = base * 2.0;
  else if (change24h < -2) score = base * 1.4;
  else if (change24h > 5) score = base * 0.6;
  else if (change24h > 2) score = base * 0.85;
  else score = base;
  
  score *= (1 + Math.abs(change24h) / 100);
  
  return {
    ticker,
    currentPrice: price,
    change24h,
    asymmetryScore: parseFloat(score.toFixed(2)),
    upside: parseFloat((score * 100).toFixed(1)),
    downside: parseFloat((-base * 0.5 * 100).toFixed(1)),
    targetPrice: parseFloat((price * (1 + score)).toFixed(2)),
    floorPrice: parseFloat((price * (1 - base * 0.5)).toFixed(2))
  };
}

(async () => {
  const prices = await fetchAllPrices();
  const held = ['COIN','SOL','CRWD','HIMS','MSTR','PLTR','ETH','BTC','SNOW'];
  
  const opps = Object.entries(prices).map(([ticker, data]) => 
    calculateAsymmetry(ticker, data.price, data.change24h)
  ).sort((a, b) => b.asymmetryScore - a.asymmetryScore);
  
  console.log('=== ALL OPPORTUNITIES ===');
  opps.forEach((o, i) => {
    const status = held.includes(o.ticker) ? ' [HELD]' : '';
    console.log(`${i+1}. ${o.ticker}: Score ${o.asymmetryScore} | $${o.currentPrice.toFixed(2)} (${o.change24h >= 0 ? '+' : ''}${o.change24h.toFixed(1)}%)${status}`);
  });
  
  const available = opps.filter(o => !held.includes(o.ticker));
  console.log('\n=== AVAILABLE (not held) ===');
  available.forEach((o, i) => {
    console.log(`${i+1}. ${o.ticker}: Score ${o.asymmetryScore} | $${o.currentPrice.toFixed(2)} (${o.change24h >= 0 ? '+' : ''}${o.change24h.toFixed(1)}%)`);
  });
})();
