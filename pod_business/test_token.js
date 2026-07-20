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

console.log('🔑 Token found, length:', token.length);
console.log('🧪 Testing Printify API connectivity...\n');

const options = {
  hostname: 'api.printify.com',
  path: '/v1/shops.json',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    'User-Agent': 'PrintifyAPI-Test/1.0'
  }
};

const req = https.request(options, (res) => {
  console.log('📡 Response Status:', res.statusCode);
  
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      try {
        const json = JSON.parse(data);
        console.log('✅ SUCCESS! API connection working');
        console.log('🏪 Shops found:', json.data ? json.data.length : 0);
        if (json.data && json.data[0]) {
          console.log('📌 Shop ID:', json.data[0].id);
          console.log('📌 Shop Name:', json.data[0].title);
        }
        process.exit(0);
      } catch (e) {
        console.log('⚠️ Response:', data.substring(0, 300));
      }
    } else if (res.statusCode === 401) {
      console.log('❌ FAILED: 401 Unauthorized - Token invalid or expired');
      console.log('💡 Action needed: Generate new token from printify.com → Account → API Tokens');
      process.exit(1);
    } else {
      console.log('⚠️ Response:', data.substring(0, 300));
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('❌ Request failed:', e.message);
  process.exit(1);
});

req.setTimeout(10000, () => {
  console.error('❌ Request timeout');
  req.destroy();
  process.exit(1);
});

req.end();
