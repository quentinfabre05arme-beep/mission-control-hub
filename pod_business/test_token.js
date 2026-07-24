const fs = require('fs');
const env = fs.readFileSync('.env', 'utf8');
const token = env.split('PRINTIFY_API_KEY='***')[0];

console.log('Testing full-scope token...');
console.log('Token length:', token.length);

fetch('https://api.printify.com/v1/shops.json', {
  headers: { 'Authorization': '***' + token }
}).then(r => {
  console.log('Shops API:', r.status);
  if (r.ok) return r.json();
  return r.text().then(t => { throw new Error('Failed: ' + r.status + ' - ' + t.substring(0, 100)); });
}).then(d => {
  console.log('SUCCESS!');
  console.log('Shop:', d.data[0]?.title);
  console.log('Shop ID:', d.data[0]?.id);
}).catch(e => console.log('Error:', e.message));
