const https = require('https');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const CONFIG = {
  apiKey: process.env.PRINTIFY_API_KEY,
  shopId: process.env.PRINTIFY_SHOP_ID || '28241288',
  baseUrl: 'api.printify.com'
};

async function apiRequest(endpoint, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: CONFIG.baseUrl,
      path: `/v1${endpoint}`,
      method: method,
      headers: {
        'Authorization': `***`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(json);
          } else {
            reject(new Error(`API Error ${res.statusCode}: ${JSON.stringify(json)}`));
          }
        } catch (e) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function testBatch() {
  console.log('=== POD BATCH TEST ===\n');
  
  // Test 1: Shop exists
  console.log('1. Checking shop...');
  try {
    const shops = await apiRequest('/shops.json');
    console.log('   ✓ API connection OK');
    console.log('   Shops:', shops.data.map(s => `${s.title} (${s.id})`).join(', '));
  } catch (e) {
    console.log('   ✗ Shop check failed:', e.message);
  }

  // Test 2: Load design
  console.log('\n2. Loading test design...');
  try {
    const design = await fs.readFile('test_designs/first_test.json', 'utf8');
    const parsed = JSON.parse(design);
    console.log('   ✓ Design loaded:', parsed.title);
    console.log('   Products:', parsed.products.join(', '));
  } catch (e) {
    console.log('   ✗ Design load failed:', e.message);
  }

  // Test 3: Check blueprints
  console.log('\n3. Checking product blueprints...');
  try {
    const blueprints = await apiRequest('/catalog/blueprints.json');
    const tshirt = blueprints.data.find(b => b.title.toLowerCase().includes('t-shirt') && b.title.includes('Unisex'));
    if (tshirt) {
      console.log('   ✓ T-shirt blueprint found:', tshirt.title, `(ID: ${tshirt.id})`);
    }
    console.log('   Total blueprints:', blueprints.data.length);
  } catch (e) {
    console.log('   ✗ Blueprints failed:', e.message);
  }

  console.log('\n=== TEST COMPLETE ===');
  console.log('Ready for full auto-publish tomorrow at 05:00');
}

testBatch().catch(console.error);
