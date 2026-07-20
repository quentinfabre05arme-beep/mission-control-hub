#!/usr/bin/env node
/**
 * Printify Stable Connection Handler
 * Robust API connection with auto-retry and health checks
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  maxRetries: 3,
  retryDelayMs: 1000,
  timeoutMs: 15000,
  apiHostname: 'api.printify.com'
};

// State
let state = {
  token: null,
  shopId: null,
  connected: false,
  lastError: null,
  healthScore: 0
};

// Logger
const log = {
  info: (msg) => console.log(`ℹ️  ${msg}`),
  success: (msg) => console.log(`✅ ${msg}`),
  warn: (msg) => console.log(`⚠️  ${msg}`),
  error: (msg) => console.log(`❌ ${msg}`),
  debug: (msg) => process.env.DEBUG && console.log(`🔍 ${msg}`)
};

// Load environment
function loadEnv() {
  try {
    const envPath = path.join(__dirname, '.env');
    const envContent = fs.readFileSync(envPath, 'utf8');
    
    const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
    const shopIdMatch = envContent.match(/PRINTIFY_SHOP_ID=(.+)/);
    
    state.token = tokenMatch ? tokenMatch[1].trim() : null;
    state.shopId = shopIdMatch ? shopIdMatch[1].trim() : null;
    
    if (!state.token) {
      throw new Error('PRINTIFY_API_KEY not found in .env');
    }
    
    log.success(`Token loaded (${state.token.length} chars)`);
    return true;
  } catch (error) {
    state.lastError = error.message;
    log.error(`Failed to load env: ${error.message}`);
    return false;
  }
}

// Make HTTP request with retry logic
function request(path, options = {}) {
  const { method = 'GET', postData = null, retries = CONFIG.maxRetries } = options;
  
  return new Promise((resolve, reject) => {
    const attempt = (retryCount) => {
      const reqOptions = {
        hostname: CONFIG.apiHostname,
        path: path,
        method: method,
        headers: {
          'Authorization': `Bearer ${state.token}`,
          'Content-Type': 'application/json',
          'User-Agent': 'PrintifyStable/1.0'
        }
      };
      
      log.debug(`${method} ${path} (attempt ${retryCount + 1}/${retries})`);
      
      const req = https.request(reqOptions, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            resolve({ status: res.statusCode, data: json, headers: res.headers });
          } catch (e) {
            resolve({ status: res.statusCode, data: data.substring(0, 500), headers: res.headers });
          }
        });
      });
      
      req.on('error', (err) => {
        if (retryCount < retries - 1) {
          log.warn(`Request failed, retrying... (${err.message})`);
          setTimeout(() => attempt(retryCount + 1), CONFIG.retryDelayMs * (retryCount + 1));
        } else {
          reject(err);
        }
      });
      
      req.setTimeout(CONFIG.timeoutMs, () => {
        req.destroy();
        if (retryCount < retries - 1) {
          log.warn('Request timeout, retrying...');
          setTimeout(() => attempt(retryCount + 1), CONFIG.retryDelayMs * (retryCount + 1));
        } else {
          reject(new Error('Request timeout after all retries'));
        }
      });
      
      if (postData) {
        req.write(JSON.stringify(postData));
      }
      
      req.end();
    };
    
    attempt(0);
  });
}

// Health check
async function healthCheck() {
  log.info('Running health check...');
  
  const checks = [
    { name: 'API Connectivity', path: '/v1/shops.json' },
    { name: 'Catalog Access', path: '/v1/catalog/blueprints.json' },
    { name: 'Print Providers', path: '/v1/catalog/print_providers.json' }
  ];
  
  let score = 0;
  
  for (const check of checks) {
    try {
      const result = await request(check.path);
      if (result.status === 200) {
        log.success(`${check.name}: OK`);
        score += 33;
      } else {
        log.warn(`${check.name}: HTTP ${result.status}`);
      }
    } catch (error) {
      log.error(`${check.name}: ${error.message}`);
    }
  }
  
  state.healthScore = Math.min(score, 100);
  log.info(`Health Score: ${state.healthScore}%`);
  
  return state.healthScore;
}

// Get shop info
async function getShopInfo() {
  try {
    const result = await request('/v1/shops.json');
    
    // Handle both array and object responses
    let shops = [];
    if (Array.isArray(result.data)) {
      shops = result.data;
    } else if (result.data.data) {
      shops = result.data.data;
    }
    
    if (result.status === 200 && shops.length > 0) {
      log.success(`Found ${shops.length} shop(s)`);
      shops.forEach((shop, i) => {
        log.info(`  Shop ${i+1}: ${shop.title} (ID: ${shop.id}, Channel: ${shop.sales_channel})`);
      });
      
      state.shopId = shops[0].id;
      return true;
    }
    
    log.warn('No shops found');
    return false;
  } catch (error) {
    log.error(`Failed to get shop info: ${error.message}`);
    return false;
  }
}

// Main execution
async function main() {
  console.log('\n🔌 Printify Stable Connection Handler\n');
  console.log('═══════════════════════════════════════\n');
  
  // Load environment
  if (!loadEnv()) {
    process.exit(1);
  }
  
  // Health check
  await healthCheck();
  
  // Get shop info
  const hasShop = await getShopInfo();
  
  // Summary
  console.log('\n═══════════════════════════════════════');
  console.log('📊 Connection Status');
  console.log('═══════════════════════════════════════');
  console.log(`Token:        ${state.token ? '✅ Valid' : '❌ Missing'}`);
  console.log(`API:          ${state.healthScore > 0 ? '✅ Connected' : '❌ Disconnected'}`);
  console.log(`Shop:         ${hasShop ? '✅ Connected' : '❌ Not connected'}`);
  console.log(`Health Score: ${state.healthScore}%`);
  console.log('═══════════════════════════════════════\n');
  
  // Recommendations
  if (!hasShop) {
    log.info('Next steps:');
    log.info('1. Visit https://printify.com/app/dashboard');
    log.info('2. Click "Add New Store" → "Etsy"');
    log.info('3. Connect your Etsy shop "Quentinvestdesign"');
    log.info('4. Re-run this script');
  }
  
  process.exit(hasShop ? 0 : 1);
}

// Run if called directly
if (require.main === module) {
  main().catch(err => {
    log.error(`Unhandled error: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { request, healthCheck, getShopInfo, state };
