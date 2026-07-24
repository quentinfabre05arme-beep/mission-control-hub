const fs = require('fs');
const env = fs.readFileSync('.env', 'utf8');
const lines = env.split('\n');
const tokenLine = lines.find(l => l.startsWith('PRINTIFY_API_KEY'));
const token = tokenLine ? tokenLine.split('=').slice(1).join('=').trim() : '';

console.log('Token length:', token.length);

fetch('https://api.printify.com/v1/shops.json', {
  headers: { 'Authorization': '***' + token }
}).then(r => {
  console.log('Shops API:', r.status);
  if (r.ok) return r.json();
  return r.text().then(t => { throw new Error(r.status + ': ' + t.substring(0, 100)); });
}).then(d => {
  console.log('SUCCESS! Shop:', d.data[0]?.title);
}).catch(e => console.log('Error:', e.message));
