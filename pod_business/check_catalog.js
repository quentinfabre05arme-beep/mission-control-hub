const https = require('https');
const fs = require('fs');

const envLines = fs.readFileSync('.env', 'utf8').split('\n');
let TOKEN = null;
for (const line of envLines) {
  if (line.startsWith('PRINTIFY_API_KEY=')) {
    TOKEN = line.substring('PRINTIFY_API_KEY='.length).trim();
    break;
  }
}

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'User-Agent': 'PrintifyCheck/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('Checking Printify Catalog API...\n');
  
  // Try different endpoints
  const endpoints = [
    '/v1/catalog/blueprints.json',
    '/v1/catalog/print_providers.json',
    '/v1/shops/28241288/products.json'
  ];
  
  for (const endpoint of endpoints) {
    console.log(`Testing: ${endpoint}`);
    try {
      const result = await apiRequest(endpoint);
      console.log(`  Status: ${result.status}`);
      if (result.status === 200) {
        const data = result.data.data || result.data;
        console.log(`  Items: ${Array.isArray(data) ? data.length : 'N/A'}`);
        if (Array.isArray(data) && data.length > 0) {
          console.log(`  Sample: ${data[0].title || data[0].name || 'N/A'}`);
        }
      } else {
        console.log(`  Error: ${JSON.stringify(result.data).substring(0, 200)}`);
      }
    } catch (e) {
      console.log(`  Error: ${e.message}`);
    }
    console.log('');
  }
}

main();