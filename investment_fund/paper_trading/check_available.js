const { getOpportunities } = require('./trade_executor');

(async () => {
  const opps = await getOpportunities();
  const held = ['COIN','SOL','CRWD','HIMS','MSTR','PLTR','ETH','BTC','SNOW'];
  const available = opps.filter(o => !held.includes(o.ticker));
  console.log('Available opportunities (not held):');
  available.slice(0, 10).forEach((o, i) => {
    console.log(`${i+1}. ${o.ticker}: Score ${o.asymmetryScore} | $${o.currentPrice.toFixed(2)} (${o.change24h >= 0 ? '+' : ''}${o.change24h.toFixed(1)}%)`);
  });
})();
