const https = require('https');
const fs = require('fs');

const envContent = fs.readFileSync('.env.local', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

if (!token) {
  console.log('❌ No token found');
  process.exit(1);
}

console.log('Testing Printify API with detailed logging...\n');
console.log('Token length:', token.length);
console.log('Token starts with:', token.substring(0, 50));

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
  console.log('\nResponse Status:', res.statusCode);
  console.log('Response Headers:', res.headers);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('\nResponse Body:', data);
  });
});

req.on('error', (e) => {
  console.error('\n❌ Request Error:', e.message);
});

req.end();