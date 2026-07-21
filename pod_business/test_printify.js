const axios = require('axios');
const fs = require('fs');

// Read token from .env.local
const envContent = fs.readFileSync('.env.local', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

if (!token) {
  console.log('❌ No token found in .env.local');
  process.exit(1);
}

console.log('Testing Printify API...');
console.log('Token prefix:', token.substring(0, 20) + '...');

axios.get('https://api.printify.com/v1/shops.json', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  timeout: 10000
})
.then(response => {
  console.log('✅ Token works!');
  console.log('Shop count:', response.data.data.length);
  console.log('Shops:', response.data.data.map(s => s.title).join(', '));
})
.catch(error => {
  if (error.response) {
    console.log('❌ Token failed:');
    console.log('  Status:', error.response.status);
    console.log('  Status Text:', error.response.statusText);
    console.log('  Message:', error.response.data?.message || 'No message');
    
    if (error.response.status === 401) {
      console.log('\n⚠️  Token is invalid or expired. You need to regenerate it.');
      console.log('\nFix steps:');
      console.log('1. Go to https://printify.com/');
      console.log('2. Log into your account');
      console.log('3. Go to Account → API Access');
      console.log('4. Click "Generate New Token"');
      console.log('5. Copy the new token');
      console.log('6. Update pod_business/.env.local with the new token');
    }
  } else {
    console.log('❌ Error:', error.message);
  }
});