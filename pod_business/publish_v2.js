const https = require('https');
const fs = require('fs');
const path = require('path');

const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const TOKEN = tokenMatch ? tokenMatch[1].trim() : null;
const SHOP_ID = 28241288;

function apiRequest(path, method = 'GET', postData = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json',
        'User-Agent': 'PrintifyPublisher/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, data: json });
        } catch (e) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => reject(new Error('Timeout')));
    if (postData) req.write(JSON.stringify(postData));
    req.end();
  });
}

async function main() {
  console.log('Testing blueprint structure...\n');
  
  const result = await apiRequest('/v1/catalog/blueprints.json');
  console.log('Status:', result.status);
  console.log('Data type:', typeof result.data);
  console.log('Is Array:', Array.isArray(result.data));
  
  if (result.data.data) {
    console.log('Has data.data:', true);
    console.log('data.data length:', result.data.data.length);
    console.log('First item:', JSON.stringify(result.data.data[0], null, 2).substring(0, 300));
  } else if (Array.isArray(result.data)) {
    console.log('Data is array, length:', result.data.length);
    console.log('First item:', JSON.stringify(result.data[0], null, 2).substring(0, 300));
  }
}

main();
