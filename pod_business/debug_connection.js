const https = require('https');
const fs = require('fs');

const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=***
const token = tokenMatch ? tokenMatch[1].trim() : null;
const shopIdMatch = envContent.match(/PRINTIFY_SHOP_ID=(.+)/);
const shopId = shopIdMatch ? shopIdMatch[1].trim() : null;

console.log('🔍 Deep Debug: Printify Connection\n');
console.log('Token present:', token ? 'Yes (' + token.length + ' chars)' : 'No');
console.log('Shop ID in env:', shopId || 'Not set');

function makeRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, data: json, headers: res.headers });
        } catch (e) {
          resolve({ status: res.statusCode, data: data, headers: res.headers });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => reject(new Error('Timeout')));
    req.end();
  });
}

async function debug() {
  // Test different endpoints
  const endpoints = [
    '/v1/shops.json',
    '/v1/shops.json?limit=100',
    '/v1/catalog/blueprints.json?limit=10',
    '/v1/catalog/print_providers.json',
  ];

  for (const endpoint of endpoints) {
    console.log(`\n📡 Testing: ${endpoint}`);
    try {
      const result = await makeRequest(endpoint);
      console.log(`   Status: ${result.status}`);
      if (result.data.data) {
        console.log(`   Items: ${result.data.data.length}`);
        if (result.data.data.length > 0 && endpoint.includes('shops')) {
          result.data.data.forEach((shop, i) => {
            console.log(`   Shop ${i+1}: ID=${shop.id}, Title="${shop.title}"`);
          });
        }
      } else if (result.data.message) {
        console.log(`   Message: ${result.data.message}`);
      }
    } catch (e) {
      console.log(`   Error: ${e.message}`);
    }
  }

  // If shop ID exists, test specific shop
  if (shopId && shopId !== '28241288') {
    console.log(`\n📡 Testing specific shop: ${shopId}`);
    try {
      const result = await makeRequest(`/v1/shops/${shopId}.json`);
      console.log(`   Status: ${result.status}`);
      if (result.status === 200) {
        console.log('   Shop found:', result.data.title);
      } else {
        console.log('   Response:', result.data);
      }
    } catch (e) {
      console.log(`   Error: ${e.message}`);
    }
  }

  console.log('\n✅ Debug complete');
}

debug();
