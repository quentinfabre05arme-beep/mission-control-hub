const https = require('https');
const fs = require('fs');
const path = require('path');

const COINGECKO_API_KEY = process.env.COINGECKO_API_KEY || ''; // Optional for free tier
const CACHE_FILE = path.join(__dirname, '../../data/coingecko_cache.json');
const CACHE_TTL_MS = 2 * 60 * 1000; // 2 minutes

class CoinGeckoProService {
  constructor() {
    this.baseUrl = COINGECKO_API_KEY ? 'pro-api.coingecko.com' : 'api.coingecko.com';
    this.cache = this.loadCache();
  }

  loadCache() {
    try {
      if (fs.existsSync(CACHE_FILE)) {
        return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
      }
    } catch (e) {
      console.error('Cache load error:', e.message);
    }
    return { data: {}, timestamp: 0 };
  }

  saveCache() {
    try {
      fs.mkdirSync(path.dirname(CACHE_FILE), { recursive: true });
      fs.writeFileSync(CACHE_FILE, JSON.stringify(this.cache, null, 2));
    } catch (e) {
      console.error('Cache save error:', e.message);
    }
  }

  isCacheValid(key) {
    const entry = this.cache.data[key];
    if (!entry) return false;
    return Date.now() - entry.timestamp < CACHE_TTL_MS;
  }

  async makeRequest(endpoint) {
    return new Promise((resolve, reject) => {
      const headers = {
        'User-Agent': 'EthereumAuthority/1.0',
        'Accept': 'application/json'
      };
      
      if (COINGECKO_API_KEY) {
        headers['x-cg-pro-api-key'] = COINGECKO_API_KEY;
      }

      const options = {
        hostname: this.baseUrl,
        path: endpoint,
        method: 'GET',
        headers
      };

      const req = https.request(options, (res) => {
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
      req.setTimeout(10000, () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });
      req.end();
    });
  }

  // Get ETH price and market data
  async getEthPrice() {
    const cacheKey = 'ethPrice';
    if (this.isCacheValid(cacheKey)) {
      return this.cache.data[cacheKey].data;
    }

    const data = await this.makeRequest('/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true');
    
    const result = {
      price: data.ethereum.usd,
      change24h: data.ethereum.usd_24h_change,
      marketCap: data.ethereum.usd_market_cap,
      volume24h: data.ethereum.usd_24h_vol,
      timestamp: Date.now()
    };

    this.cache.data[cacheKey] = { data: result, timestamp: Date.now() };
    this.saveCache();
    return result;
  }

  // Get LST prices (stETH, cbETH, rETH)
  async getLstPrices() {
    const cacheKey = 'lstPrices';
    if (this.isCacheValid(cacheKey)) {
      return this.cache.data[cacheKey].data;
    }

    // CoinGecko IDs for LSTs
    const ids = 'staked-ether,coinbase-wrapped-staked-eth,rocket-pool-eth';
    const data = await this.makeRequest(`/api/v3/simple/price?ids=${ids}&vs_currencies=usd&include_24hr_change=true`);
    
    const result = {
      stETH: {
        price: data['staked-ether'].usd,
        change24h: data['staked-ether'].usd_24h_change
      },
      cbETH: {
        price: data['coinbase-wrapped-staked-eth']?.usd || null,
        change24h: data['coinbase-wrapped-staked-eth']?.usd_24h_change || null
      },
      rETH: {
        price: data['rocket-pool-eth']?.usd || null,
        change24h: data['rocket-pool-eth']?.usd_24h_change || null
      },
      timestamp: Date.now()
    };

    this.cache.data[cacheKey] = { data: result, timestamp: Date.now() };
    this.saveCache();
    return result;
  }

  // Get trending coins (for market sentiment)
  async getTrendingCoins() {
    const cacheKey = 'trending';
    if (this.isCacheValid(cacheKey)) {
      return this.cache.data[cacheKey].data;
    }

    const data = await this.makeRequest('/api/v3/search/trending');
    
    const result = {
      coins: data.coins.slice(0, 7).map(c => ({
        name: c.item.name,
        symbol: c.item.symbol,
        rank: c.item.market_cap_rank
      })),
      timestamp: Date.now()
    };

    this.cache.data[cacheKey] = { data: result, timestamp: Date.now() };
    this.saveCache();
    return result;
  }

  // Get global crypto market data
  async getGlobalData() {
    const cacheKey = 'globalData';
    if (this.isCacheValid(cacheKey)) {
      return this.cache.data[cacheKey].data;
    }

    const data = await this.makeRequest('/api/v3/global');
    
    const result = {
      totalMarketCap: data.data.total_market_cap.usd,
      totalVolume: data.data.total_volume.usd,
      ethDominance: data.data.market_cap_percentage.eth,
      btcDominance: data.data.market_cap_percentage.btc,
      timestamp: Date.now()
    };

    this.cache.data[cacheKey] = { data: result, timestamp: Date.now() };
    this.saveCache();
    return result;
  }
}

// CLI execution
if (require.main === module) {
  const service = new CoinGeckoProService();
  
  (async () => {
    try {
      console.log('Fetching CoinGecko data...\n');
      
      const [eth, lst, global] = await Promise.all([
        service.getEthPrice(),
        service.getLstPrices(),
        service.getGlobalData()
      ]);
      
      console.log('=== COINGECKO DATA ===');
      console.log(`ETH Price: $${eth.price.toLocaleString()}`);
      console.log(`24h Change: ${eth.change24h.toFixed(2)}%`);
      console.log(`Market Cap: $${(eth.marketCap / 1e9).toFixed(2)}B`);
      console.log(`24h Volume: $${(eth.volume24h / 1e9).toFixed(2)}B`);
      
      console.log(`\nLST Prices:`);
      console.log(`  stETH: $${lst.stETH.price.toLocaleString()} (${lst.stETH.change24h.toFixed(2)}%)`);
      if (lst.cbETH.price) console.log(`  cbETH: $${lst.cbETH.price.toLocaleString()} (${lst.cbETH.change24h.toFixed(2)}%)`);
      if (lst.rETH.price) console.log(`  rETH: $${lst.rETH.price.toLocaleString()} (${lst.rETH.change24h.toFixed(2)}%)`);
      
      console.log(`\nMarket Dominance:`);
      console.log(`  BTC: ${global.btcDominance.toFixed(1)}%`);
      console.log(`  ETH: ${global.ethDominance.toFixed(1)}%`);
      
    } catch (error) {
      console.error('Error:', error.message);
      console.log('\nNote: CoinGecko free tier has rate limits (10-30 calls/min)');
    }
  })();
}

module.exports = CoinGeckoProService;
