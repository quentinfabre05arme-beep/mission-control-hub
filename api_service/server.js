// Autonomous Data API — Revenue Stream #3
// Serves market data, technical analysis, sentiment

const http = require('http');
const fs = require('fs').promises;
const path = require('path');

const PORT = process.env.PORT || 3000;
const RATE_LIMIT = 100; // requests per hour per API key

// In-memory rate tracking (reset hourly)
const rateTracker = new Map();

class DataAPIServer {
  constructor() {
    this.cache = new Map();
    this.cacheTTL = 2 * 60 * 1000; // 2 minutes
  }

  async getMarketData(symbol) {
    const cacheKey = `market_${symbol}`;
    if (this.cache.has(cacheKey)) {
      const { data, timestamp } = this.cache.get(cacheKey);
      if (Date.now() - timestamp < this.cacheTTL) return data;
    }
    
    try {
      const data = await fs.readFile(
        path.join(__dirname, '../mission_control/market_data.json'),
        'utf8'
      );
      const parsed = JSON.parse(data);
      const result = parsed[symbol];
      
      if (result) {
        this.cache.set(cacheKey, { data: result, timestamp: Date.now() });
      }
      return result;
    } catch {
      return null;
    }
  }

  checkRateLimit(apiKey) {
    const now = Date.now();
    const hourAgo = now - 60 * 60 * 1000;
    
    if (!rateTracker.has(apiKey)) {
      rateTracker.set(apiKey, []);
    }
    
    const requests = rateTracker.get(apiKey).filter(t => t > hourAgo);
    requests.push(now);
    rateTracker.set(apiKey, requests);
    
    return {
      allowed: requests.length <= RATE_LIMIT,
      remaining: Math.max(0, RATE_LIMIT - requests.length),
      used: requests.length
    };
  }

  async handleRequest(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const apiKey = url.searchParams.get('key') || 'free';
    
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    
    // Rate limit check
    const rateStatus = this.checkRateLimit(apiKey);
    if (!rateStatus.allowed) {
      res.statusCode = 429;
      res.end(JSON.stringify({
        error: 'Rate limit exceeded',
        upgrade: 'Pro tier: 10,000 requests/month',
        pricing: 'https://your-domain.com/pricing'
      }));
      return;
    }
    
    // Route handlers
    if (url.pathname === '/v1/quote') {
      const symbol = url.searchParams.get('symbol')?.toUpperCase();
      if (!symbol) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: 'Symbol required' }));
        return;
      }
      
      const data = await this.getMarketData(symbol);
      if (!data) {
        res.statusCode = 404;
        res.end(JSON.stringify({ error: 'Symbol not found' }));
        return;
      }
      
      res.end(JSON.stringify({
        symbol,
        price: data.price,
        change: data.change,
        source: data.source,
        timestamp: data.timestamp,
        rate_limit: {
          remaining: rateStatus.remaining,
          used: rateStatus.used
        }
      }));
      return;
    }
    
    if (url.pathname === '/v1/symbols') {
      res.end(JSON.stringify({
        symbols: ['BTC', 'ETH', 'MSTR', 'HIMS', 'SOL', 'XRP', 'LINK'],
        note: 'Free tier: 7 symbols. Pro: 100+ symbols'
      }));
      return;
    }
    
    if (url.pathname === '/') {
      res.end(JSON.stringify({
        name: 'Quentinvest Data API',
        version: '1.0.0',
        endpoints: {
          '/v1/quote': 'GET ?symbol=BTC',
          '/v1/symbols': 'List available symbols'
        },
        pricing: {
          free: '100 requests/hour',
          pro: '€29/month - 10,000 requests',
          enterprise: '€299/month - unlimited'
        },
        upgrade: 'Contact: api@quentinvest.com'
      }));
      return;
    }
    
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  }

  start() {
    const server = http.createServer((req, res) => this.handleRequest(req, res));
    server.listen(PORT, () => {
      console.log(`Data API server running on port ${PORT}`);
      console.log(`Free tier: ${RATE_LIMIT} requests/hour`);
      console.log(`Upgrade: http://localhost:${PORT}/`);
    });
    return server;
  }
}

// Start if run directly
if (require.main === module) {
  const api = new DataAPIServer();
  api.start();
}

module.exports = DataAPIServer;
