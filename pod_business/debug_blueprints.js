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
        'User-Agent': 'PrintifyDebug/1.0'
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
  console.log('Debugging blueprint response structure...\n');
  
  const result = await apiRequest('/v1/catalog/blueprints.json');
  
  console.log('Status:', result.status);
  console.log('Data type:', typeof result.data);
  console.log('Data keys:', Object.keys(result.data));
  
  if (result.data.data) {
    console.log('result.data.data type:', typeof result.data.data);
    console.log('result.data.data is array:', Array.isArray(result.data.data));
    console.log('result.data.data length:', result.data.data.length);
    
    if (result.data.data.length > 0) {
      console.log('\nFirst item:', JSON.stringify(result.data.data[0], null, 2).substring(0, 300));
    }
  }
}

main();