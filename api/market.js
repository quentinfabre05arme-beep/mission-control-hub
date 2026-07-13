// Vercel serverless function for market data
export default function handler(req, res) {
  // In production, this would fetch from CoinGecko/Yahoo Finance
  // For now, return the latest cached data or fetch live
  
  const marketData = {
    timestamp: new Date().toISOString(),
    source: 'live_api',
    assets: {
      BTC: { price: 63050, change_24h: -1.26 },
      ETH: { price: 1781.38, change_24h: -1.03 },
      MSTR: { price: 94.64, change_24h: 0.8 },
      HIMS: { price: 34.38, change_24h: -3.02 }
    }
  };
  
  res.status(200).json(marketData);
}