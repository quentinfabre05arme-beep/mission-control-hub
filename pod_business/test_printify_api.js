// Direct Printify API test
const https = require('https');

const API_KEY = process.env.PRINTIFY_API_KEY;
const SHOP_ID = process.env.PRINTIFY_SHOP_ID;

if (!API_KEY) {
  console.log('❌ PRINTIFY_API_KEY not set');
  process.exit(1);
}

console.log('Testing Printify API...');
console.log('Shop ID:', SHOP_ID);
console.log('Token length:', API_KEY.length);
console.log('Token prefix:', API_KEY.substring(0, 50) + '...');

const options = {
  hostname: 'api.printify.com',
  path: '/v1/shops.json',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
};

const req = https.request(options, (res) => {
  console.log('\nResponse Status:', res.statusCode);
  console.log('Response Headers:', JSON.stringify(res.headers, null, 2));
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('\nResponse Body:');
    try {
      const parsed = JSON.parse(data);
      console.log(JSON.stringify(parsed, null, 2));
    } catch (e) {
      console.log(data);
    }
    
    if (res.statusCode === 200) {
      console.log('\n✅ API CONNECTION SUCCESSFUL');
    } else if (res.statusCode === 401) {
      console.log('\n❌ API RETURNED 401 UNAUTHORIZED');
      console.log('The token may be revoked or invalid.');
      console.log('ACTION NEEDED: Generate new token at printify.com/app/account/api');
    }
  });
});

req.on('error', (e) => {
  console.error('Request Error:', e.message);
});

req.end();
