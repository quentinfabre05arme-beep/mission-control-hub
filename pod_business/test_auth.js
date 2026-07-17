const https = require('https');
require('dotenv').config({ path: '.env.local' });

const token = process.env.PRINTIFY_API_KEY;
const shopId = process.env.PRINTIFY_SHOP_ID;

console.log('Token present:', !!token);
console.log('Token length:', token ? token.length : 0);
console.log('Shop ID:', shopId);

const options = {
  hostname: 'api.printify.com',
  path: '/v1/shops.json',
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'User-Agent': 'Quentinvest-POD/1.0'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    try {
      const json = JSON.parse(data);
      console.log('Response:', JSON.stringify(json, null, 2));
    } catch (e) {
      console.log('Raw:', data);
    }
  });
});

req.on('error', err => console.log('Error:', err.message));
req.end();
