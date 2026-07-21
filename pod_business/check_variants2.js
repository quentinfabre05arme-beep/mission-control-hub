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
    console.log('Response structure:');
    console.log('  id:', j.id);
    console.log('  title:', j.title);
    console.log('  variants type:', typeof j.variants);
    console.log('  variants is array:', Array.isArray(j.variants));
    if (j.variants) {
      console.log('  variants length:', j.variants.length);
      console.log('  First variant:', JSON.stringify(j.variants[0], null, 2).substring(0, 400));
    }
  });
}).end();
