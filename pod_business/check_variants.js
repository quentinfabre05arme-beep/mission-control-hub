const https = require('https');
const fs = require('fs');

const env = fs.readFileSync('.env', 'utf8');
const token = env.match(/PRINTIFY_API_KEY=(.+)/)[1].trim();

const opts = {
  hostname: 'api.printify.com',
  path: '/v1/catalog/blueprints/145/print_providers/30/variants.json',
  method: 'GET',
  headers: { 'Authorization': `Bearer ${token}` }
};

https.request(opts, res => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const j = JSON.parse(d);
    console.log('Type:', typeof j);
    console.log('Keys:', Object.keys(j));
    if (j.data) {
      console.log('data.length:', j.data.length);
      console.log('Sample:', JSON.stringify(j.data[0], null, 2).substring(0, 300));
    }
  });
}).end();
