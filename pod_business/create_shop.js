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

function makeRequest(path, method = 'GET', postData = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User-Agent': 'PrintifyAPI-Create/1.0'
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
    
    if (postData) {
      req.write(JSON.stringify(postData));
    }
    
    req.setTimeout(15000, () => reject(new Error('Timeout')));
    req.end();
  });
}

async function main() {
  console.log('🔧 Creating Printify shop via API...\n');
  
  // Try to create a manual shop
  const shopData = {
    title: 'Quentinvestdesign Store',
    sales_channel: 'etsy'
  };
  
  try {
    console.log('📡 Creating shop with data:', JSON.stringify(shopData));
    const result = await makeRequest('/v1/shops.json', 'POST', shopData);
    console.log('\n📡 Response Status:', result.status);
    console.log('📡 Response:', JSON.stringify(result.data, null, 2));
    
    if (result.status === 201 || result.status === 200) {
      console.log('\n✅ Shop created successfully!');
      console.log('Shop ID:', result.data.id);
      console.log('Shop Title:', result.data.title);
    } else {
      console.log('\n⚠️ Shop creation returned status', result.status);
      console.log('This usually means shops must be created via dashboard for Etsy integration.');
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
