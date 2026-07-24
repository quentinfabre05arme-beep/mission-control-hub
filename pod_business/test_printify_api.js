// Test Printify API connection with new token

const fs = require('fs');

const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));

async function testPrintifyAPI() {
  console.log('=== Testing Printify API ===');
  console.log('Token length:', config.printify_api_token?.length || 0);
  console.log('Shop ID:', config.shop_id);
  
  try {
    const response = await fetch('https://api.printify.com/v1/shops.json', {
      headers: {
        'Authorization': `Bearer ${config.printify_api_token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ API Connection SUCCESSFUL');
      console.log('Shops:', JSON.stringify(data.data, null, 2).substring(0, 500));
      return true;
    } else {
      console.log('❌ API Error:', response.status, response.statusText);
      const error = await response.text();
      console.log('Error details:', error.substring(0, 200));
      return false;
    }
  } catch (error) {
    console.log('❌ Connection failed:', error.message);
    return false;
  }
}

testPrintifyAPI();
