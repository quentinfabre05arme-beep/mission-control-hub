const https = require('https');
const fs = require('fs');

const envContent = fs.readFileSync('.env.local', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

console.log('Testing Printify /v1/me endpoint...\n');

const options = {
  hostname: 'api.printify.com',
  path: '/v1/me.json',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'User-Agent': 'PrintifyAPI-Test/1.0'
  }
};

const req = https.request(options, (res) => {
  console.log('Status:', res.statusCode);
  
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      const user = JSON.parse(data);
      console.log('✅ Token works! User:', user.data?.name || user.data?.email);
      console.log('Plan:', user.data?.plan);
    } else {
      console.log('❌ Response:', data);
    }
  });
});

req.on('error', (e) => console.error('Error:', e.message));
req.end();