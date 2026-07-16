/**
 * MARKET DATA SERVICE - Multi-Source Resilient Price Fetcher
 * Always returns fresh prices via cascading fallbacks
 * Sources: Twelve Data → CoinGecko → Yahoo Finance → Cached
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const CONFIG = {
  TWELVE_DATA_KEY: '07f9ead31a5c426ea238e71895beeaa1',
  CACHE_FILE: path.join(__dirname, 'market_data.json'),
  MAX_AGE_MINUTES: 5,
  TIMEOUT_MS: 10000
};

// Asset mapping across sources
const ASSETS = {
  BTC: {
    twelvedata: 'BTC/USD',
    coingecko: 'bitcoin',
    yahoo: 'BTC-USD',
    symbol: 'BTC'
  },
  ETH: {
    twelvedata: 'ETH/USD', 
    coingecko: 'ethereum',
    yahoo: 'ETH-USD',
    symbol: 'ETH'
  },
  MSTR: {
    twelvedata: 'MSTR',
    coingecko: null, // No CoinGecko for stocks
    yahoo: 'MSTR',
    symbol: 'MSTR'
  },
  HIMS: {
    twelvedata: 'HIMS',
    coingecko: null,
    yahoo: 'HIMS',
    symbol: 'HIMS'
  }
};

// HTTP request helper
function fetchJSON(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { ...options, timeout: CONFIG.TIMEOUT_MS }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

// Source 1: Twelve Data API - for current price
async function fetchTwelveData(symbol) {
  const url = `https://api.twelvedata.com/price?symbol=${symbol}&apikey=${CONFIG.TWELVE_DATA_KEY}`;
  const data = await fetchJSON(url);
  if (data.price) {
    return {
      price: parseFloat(data.price),
      source: 'twelvedata',
      timestamp: new Date().toISOString()
    };
  }
  throw new Error(`Twelve Data error: ${data.message || 'No price'}`);
}

// Source 1b: Twelve Data quote for extended data including change
async function fetchTwelveDataQuote(symbol) {
  const url = `https://api.twelvedata.com/quote?symbol=${symbol}&apikey=${CONFIG.TWELVE_DATA_KEY}`;
  const data = await fetchJSON(url);
  if (data.close) {
    return {
      price: parseFloat(data.close),
      change_24h: data.percent_change ? parseFloat(data.percent_change) : 0,
      source: 'twelvedata',
      timestamp: new Date().toISOString()
    };
  }
  throw new Error(`Twelve Data quote error: ${data.message || 'No data'}`);
}

// Source 2: CoinGecko (free, no key needed for basic calls)
// Add delay to avoid rate limits
async function fetchCoinGecko(coinId) {
  if (!coinId) throw new Error('No CoinGecko ID for this asset');
  // Add 1 second delay before CoinGecko call to avoid rate limits
  await new Promise(r => setTimeout(r, 1000));
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${coinId}&vs_currencies=usd&include_24hr_change=true`;
  const data = await fetchJSON(url);
  if (data[coinId]) {
    return {
      price: data[coinId].usd,
      change_24h: data[coinId].usd_24h_change || 0,
      source: 'coingecko',
      timestamp: new Date().toISOString()
    };
  }
  throw new Error('CoinGecko: No data');
}

// Source 3: Yahoo Finance (unofficial endpoint)
async function fetchYahoo(symbol) {
  // Using Yahoo Finance query1 endpoint (rate limited but no key needed)
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?interval=1d&range=1d`;
  const data = await fetchJSON(url);
  if (data.chart?.result?.[0]?.meta?.regularMarketPrice) {
    const meta = data.chart.result[0].meta;
    const prevClose = meta.previousClose || meta.regularMarketPrice;
    const current = meta.regularMarketPrice;
    const change = ((current - prevClose) / prevClose) * 100;
    return {
      price: current,
      change_24h: change,
      source: 'yahoo',
      timestamp: new Date().toISOString()
    };
  }
  throw new Error('Yahoo: No price data');
}

// Cascade fetch for a single asset
async function fetchAssetWithFallback(assetKey) {
  const asset = ASSETS[assetKey];
  const errors = [];
  
  // Add staggered delay based on asset index to avoid rate limits
  const assetIndex = Object.keys(ASSETS).indexOf(assetKey);
  await new Promise(r => setTimeout(r, assetIndex * 500));
  
  // Try Twelve Data quote endpoint first (has change %)
  try {
    console.log(`[${assetKey}] Trying Twelve Data quote...`);
    const data = await fetchTwelveDataQuote(asset.twelvedata);
    return { ...data, symbol: assetKey };
  } catch (e) {
    errors.push(`Twelve Data quote: ${e.message}`);
    // If rate limited or failed, try simple price endpoint
    if (!e.message.includes('rate limit') && !e.message.includes('credits')) {
      try {
        console.log(`[${assetKey}] Trying Twelve Data price...`);
        const data = await fetchTwelveData(asset.twelvedata);
        // Get 24h change from CoinGecko for crypto
        if (asset.coingecko) {
          try {
            const cgData = await fetchCoinGecko(asset.coingecko);
            return { ...data, change_24h: cgData.change_24h, symbol: assetKey };
          } catch {
            return { ...data, change_24h: 0, symbol: assetKey };
          }
        }
        return { ...data, change_24h: 0, symbol: assetKey };
      } catch (e2) {
        errors.push(`Twelve Data price: ${e2.message}`);
      }
    }
    console.log(`[${assetKey}] Twelve Data failed, trying fallbacks...`);
  }
  
  // Try CoinGecko for crypto (free tier, no key needed)
  if (asset.coingecko) {
    try {
      console.log(`[${assetKey}] Trying CoinGecko...`);
      const data = await fetchCoinGecko(asset.coingecko);
      return { ...data, symbol: assetKey };
    } catch (e) {
      errors.push(`CoinGecko: ${e.message}`);
    }
  }
  
  // Try Yahoo Finance as last resort
  try {
    console.log(`[${assetKey}] Trying Yahoo Finance...`);
    await new Promise(r => setTimeout(r, 1000));
    const data = await fetchYahoo(asset.yahoo);
    return { ...data, symbol: assetKey };
  } catch (e) {
    errors.push(`Yahoo: ${e.message}`);
  }
  
  // All sources failed - return cached if available
  console.log(`[${assetKey}] All sources failed, using cache...`);
  const cached = loadCache();
  if (cached.assets[assetKey]) {
    return {
      ...cached.assets[assetKey],
      symbol: assetKey,
      source: 'cached',
      stale: true
    };
  }
  
  throw new Error(`All sources failed for ${assetKey}: ${errors.join('; ')}`);
}

// Load cache
function loadCache() {
  try {
    const data = fs.readFileSync(CONFIG.CACHE_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return {
      timestamp: new Date().toISOString(),
      assets: {}
    };
  }
}

// Save cache
function saveCache(data) {
  fs.writeFileSync(CONFIG.CACHE_FILE, JSON.stringify(data, null, 2));
}

// Check if cache is fresh
function isCacheFresh(timestamp) {
  const cacheTime = new Date(timestamp);
  const now = new Date();
  const diffMinutes = (now - cacheTime) / 1000 / 60;
  return diffMinutes < CONFIG.MAX_AGE_MINUTES;
}

// Main fetch all assets
async function fetchAllPrices(forceRefresh = false) {
  const cache = loadCache();
  
  // Return cache if fresh and not forcing
  if (!forceRefresh && isCacheFresh(cache.timestamp)) {
    console.log('Using fresh cache...');
    return { ...cache, fromCache: true };
  }
  
  // Fetch all assets in parallel
  console.log('Fetching fresh prices...');
  const results = await Promise.allSettled([
    fetchAssetWithFallback('BTC'),
    fetchAssetWithFallback('ETH'),
    fetchAssetWithFallback('MSTR'),
    fetchAssetWithFallback('HIMS')
  ]);
  
  const assets = {};
  const failures = [];
  
  results.forEach((result, index) => {
    const symbol = ['BTC', 'ETH', 'MSTR', 'HIMS'][index];
    if (result.status === 'fulfilled') {
      assets[symbol] = {
        price: result.value.price,
        change_24h: result.value.change_24h || 0,
        source: result.value.source,
        signal: calculateSignal(result.value.change_24h || 0)
      };
    } else {
      failures.push(`${symbol}: ${result.reason.message}`);
      // Use cached if available
      if (cache.assets[symbol]) {
        assets[symbol] = { ...cache.assets[symbol], source: 'cached', stale: true };
      }
    }
  });
  
  const output = {
    timestamp: new Date().toISOString(),
    assets,
    _meta: {
      fromCache: false,
      failures: failures.length > 0 ? failures : undefined,
      sources: Object.values(assets).map(a => a.source)
    }
  };
  
  // Save to cache
  saveCache(output);
  
  return output;
}

// Calculate signal based on 24h change
function calculateSignal(change24h) {
  if (change24h > 5) return 'BULLISH';
  if (change24h > 2) return 'BULLISH';
  if (change24h < -5) return 'BEARISH';
  if (change24h < -2) return 'BEARISH';
  return 'NEUTRAL';
}

// CLI interface
async function main() {
  const args = process.argv.slice(2);
  const forceRefresh = args.includes('--refresh') || args.includes('-r');
  const format = args.includes('--json') ? 'json' : 'table';
  
  try {
    const data = await fetchAllPrices(forceRefresh);
    
    if (format === 'json') {
      console.log(JSON.stringify(data, null, 2));
    } else {
      console.log('\n=== MARKET DATA ===');
      console.log(`Last Updated: ${data.timestamp}`);
      console.log(`Status: ${data.fromCache ? 'FROM CACHE' : 'LIVE'}`);
      if (data._meta?.failures) {
        console.log(`⚠️ Failures: ${data._meta.failures.join(', ')}`);
      }
      console.log('');
      console.log('| Asset | Price | 24h Change | Source | Signal |');
      console.log('|-------|-------|------------|--------|--------|');
      
      Object.entries(data.assets).forEach(([symbol, asset]) => {
        const changeStr = asset.change_24h >= 0 ? `+${asset.change_24h.toFixed(2)}%` : `${asset.change_24h.toFixed(2)}%`;
        const stale = asset.stale ? ' (STALE)' : '';
        console.log(`| ${symbol.padEnd(5)} | $${asset.price.toLocaleString()} | ${changeStr.padEnd(10)} | ${asset.source}${stale} | ${asset.signal} |`);
      });
      
      console.log('\nSources used:', [...new Set(data._meta?.sources || [])].join(', '));
    }
  } catch (e) {
    console.error('Fatal error:', e.message);
    process.exit(1);
  }
}

// Export for use as module
module.exports = { fetchAllPrices, fetchAssetWithFallback, loadCache };

// Run if called directly
if (require.main === module) {
  main();
}
