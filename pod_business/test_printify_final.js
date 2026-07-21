const https = require('https');
const fs = require('fs');

const envContent = fs.readFileSync('.env.local', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

console.log('Testing Printify API...\n');

const options = {
  hostname: 'api.printify.com',
  path: '/v1/shops.json',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'User-Agent': 'PrintifyAPI-Test/1.0',
    'Accept': 'application/json'
  }
};

const req = https.request(options, (res) => {
  console.log('Status:', res.statusCode);
  
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      const shops = JSON.parse(data);
      console.log('✅ SUCCESS! Token works!');
      console.log('Shop count:', shops.data?.length || 'N/A');
      console.log('Shops:', shops.data?.map(s => s.title).join(', ') || shops);
    } else {
      console.log('❌ Failed:', data);
    }
  });
});

req.on('error', (e) => console.error('Error:', e.message));
req.end();