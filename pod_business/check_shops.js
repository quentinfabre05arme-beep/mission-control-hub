const https = require('https');
const fs = require('fs');

// Load token from .env
const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

if (!token) {
  console.error('❌ Token not found in .env');
  process.exit(1);
}

console.log('🔍 Checking Printify shops and connections...\n');
console.log('Token length:', token.length);
console.log('Token starts with:', token.substring(0, 20) + '...');

function makeRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User-Agent': 'PrintifyAPI-Check/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, data: json });
        } catch (e) {
          resolve({ status: res.statusCode, data: data.substring(0, 500) });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => reject(new Error('Timeout')));
    req.end();
  });
}

async function main() {
  try {
    // Step 1: Get user info
    console.log('\n📡 Step 1: Fetching user info...');
    const userResult = await makeRequest('/v1/users/me.json');
    console.log('   Status:', userResult.status);
    if (userResult.status === 200) {
      console.log('   User ID:', userResult.data.id);
      console.log('   Name:', userResult.data.name);
    }

    // Step 2: Get shops
    console.log('\n📡 Step 2: Fetching shops...');
    const shopsResult = await makeRequest('/v1/shops.json');
    console.log('   Status:', shopsResult.status);
    
    if (shopsResult.status === 200) {
      const shops = shopsResult.data.data || [];
      console.log('   Shops found:', shops.length);
      
      if (shops.length === 0) {
        console.log('\n⚠️ No shops connected to this account.');
        console.log('💡 Solutions:');
        console.log('   1. Create a shop in Printify dashboard');
        console.log('   2. Connect Etsy/Shopify/WooCommerce to Printify');
        console.log('   3. Use API to create a shop');
      } else {
        shops.forEach((shop, i) => {
          console.log(`\n   Shop ${i+1}:`);
          console.log(`   - ID: ${shop.id}`);
          console.log(`   - Title: ${shop.title}`);
          console.log(`   - Sales Channel: ${shop.sales_channel || 'N/A'}`);
        });
      }
    }

    // Step 3: Check blueprints
    console.log('\n📡 Step 3: Checking product catalog...');
    const blueprintsResult = await makeRequest('/v1/catalog/blueprints.json');
    console.log('   Status:', blueprintsResult.status);
    if (blueprintsResult.status === 200) {
      const blueprints = blueprintsResult.data.data || [];
      console.log('   Blueprints available:', blueprints.length);
    }

    // Step 4: Check print providers
    console.log('\n📡 Step 4: Checking print providers...');
    const providersResult = await makeRequest('/v1/catalog/print_providers.json');
    console.log('   Status:', providersResult.status);
    if (providersResult.status === 200) {
      const providers = providersResult.data.data || [];
      console.log('   Print providers:', providers.length);
    }

    console.log('\n✅ API check complete');
    console.log('\n📋 Next Steps:');
    console.log('   1. Go to https://printify.com/app/dashboard');
    console.log('   2. Click "Add New Store"');
    console.log('   3. Connect your Etsy shop "Quentinvestdesign"');
    console.log('   4. Once connected, re-run this check');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
