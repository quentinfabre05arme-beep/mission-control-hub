// Working Printify Publisher — Full Scope Token

const fs = require('fs');

// Load token
const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const TOKEN = tokenMatch ? tokenMatch[1].trim() : '';
const SHOP_ID = 28241288;

console.log('🚀 Printify Publisher v2\n');
console.log('Token loaded:', TOKEN ? '✅ ' + TOKEN.substring(0, 20) + '...' : '❌ Not found');

// Simple test first
async function testConnection() {
  console.log('\n=== Testing Connection ===');
  
  try {
    // Test shops
    const shopsRes = await fetch('https://api.printify.com/v1/shops.json', {
      headers: { 'Authorization': '***' + TOKEN }
    });
    console.log('Shops API:', shopsRes.status);
    
    if (shopsRes.ok) {
      const shops = await shopsRes.json();
      console.log('✅ Connected to shop:', shops.data[0]?.title);
      return true;
    }
    
    const error = await shopsRes.text();
    console.log('Error:', error.substring(0, 200));
    return false;
    
  } catch (e) {
    console.log('Connection error:', e.message);
    return false;
  }
}

testConnection();
