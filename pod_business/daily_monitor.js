const https = require('https');
const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const ENV_PATH = path.join(SCRIPT_DIR, '.env.local');

if (!fs.existsSync(ENV_PATH)) {
  console.error('❌ .env.local not found');
  process.exit(1);
}

const envLines = fs.readFileSync(ENV_PATH, 'utf8').split('\n');
let TOKEN = null;
for (const line of envLines) {
  if (line.startsWith('PRINTIFY_API_KEY=')) {
    TOKEN = line.substring('PRINTIFY_API_KEY='.length).trim();
    break;
  }
}

const SHOP_ID = 28241288;

function apiRequest(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: method,
      headers: {
        'Authorization': 'Bearer ' + TOKEN,
        'Content-Type': 'application/json',
        'User-Agent': 'Quentinvest-POD/2.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch(e) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });

    req.on('error', err => reject(err));
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function main() {
  console.log('📊 Printify Daily Monitor - ' + new Date().toISOString());
  console.log('');

  try {
    // Check shops
    const shops = await apiRequest('/v1/shops.json');
    if (shops.status !== 200) {
      console.error('❌ API connection failed:', shops.status);
      process.exit(1);
    }
    console.log('✅ API: Connected');
    console.log('🏪 Shop:', shops.data[0]?.title, '(ID:', shops.data[0]?.id + ')');

    // Check products
    const products = await apiRequest(`/v1/shops/${SHOP_ID}/products.json`);
    const productList = products.data?.data || [];
    console.log('📦 Products:', productList.length);
    
    let published = 0;
    let draft = 0;
    productList.forEach(p => {
      if (p.visible === true) published++;
      else draft++;
    });
    
    console.log('   ✅ Published:', published);
    console.log('   ❌ Draft:', draft);

    // Check orders
    const orders = await apiRequest(`/v1/shops/${SHOP_ID}/orders.json`);
    const orderList = orders.data?.data || [];
    console.log('🛒 Orders:', orderList.length);
    
    if (orderList.length > 0) {
      orderList.slice(0, 3).forEach(o => {
        console.log('   - Order', o.id, '|', o.status, '| $' + (o.total_price/100).toFixed(2));
      });
    }

    // Save report
    const report = {
      timestamp: new Date().toISOString(),
      shop: shops.data[0]?.title,
      products: {
        total: productList.length,
        published: published,
        draft: draft
      },
      orders: {
        total: orderList.length,
        recent: orderList.slice(0, 3).map(o => ({
          id: o.id,
          status: o.status,
          total: o.total_price
        }))
      }
    };

    const reportPath = path.join(SCRIPT_DIR, 'memory', 'daily_report_' + new Date().toISOString().split('T')[0] + '.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log('');
    console.log('📝 Report saved to:', reportPath);
    console.log('');
    console.log('✅ Daily monitor complete!');

  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

main();
