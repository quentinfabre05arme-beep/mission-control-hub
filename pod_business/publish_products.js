#!/usr/bin/env node
/**
 * Printify → Etsy Product Publisher
 * Publishes designs to Printify and pushes to Etsy
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load config - read token directly from env file line
const envLines = fs.readFileSync('.env', 'utf8').split('\n');
let TOKEN = null;
for (const line of envLines) {
  if (line.startsWith('PRINTIFY_API_KEY=')) {
    TOKEN = line.substring('PRINTIFY_API_KEY='.length).trim();
    break;
  }
}
const SHOP_ID = 28241288;

if (!TOKEN) {
  console.error('❌ Token not found');
  process.exit(1);
}

// Design files available
const DESIGNS = [
  {
    id: 'design_crypto_1784049410601',
    title: 'Bitcoin Treasury',
    description: 'Premium Bitcoin-themed design for crypto enthusiasts. Features the iconic Bitcoin orange and black color scheme.',
    tags: ['bitcoin', 'btc', 'crypto', 'cryptocurrency', 'blockchain', 'hodl', 'treasury'],
    price: 24.99
  },
  {
    id: 'design_crypto_1784049410607',
    title: 'HODL Strong',
    description: 'Classic crypto mantra for true believers. Bold design for Bitcoin and crypto enthusiasts.',
    tags: ['hodl', 'bitcoin', 'crypto', 'cryptocurrency', 'strong', 'investor', 'blockchain'],
    price: 24.99
  },
  {
    id: 'design_fitness_1784049410604',
    title: 'Fitness Motivation',
    description: 'Premium fitness design for gym enthusiasts and athletes.',
    tags: ['fitness', 'gym', 'workout', 'motivation', 'health', 'training'],
    price: 24.99
  },
  {
    id: 'design_professions_1784049410606',
    title: 'Professional Pride',
    description: 'Celebrate your profession with this premium design.',
    tags: ['profession', 'career', 'job', 'work', 'professional'],
    price: 24.99
  },
  {
    id: 'design_professions_1784049410609',
    title: 'Work Hard',
    description: 'Motivational design for dedicated professionals.',
    tags: ['work', 'motivation', 'professional', 'career', 'success'],
    price: 24.99
  }
];

// Printify API client
function apiRequest(path, method = 'GET', postData = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json',
        'User-Agent': 'PrintifyPublisher/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ status: res.statusCode, data: json });
        } catch (e) {
          resolve({ status: res.statusCode, data: data.substring(0, 500) });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => reject(new Error('Timeout')));
    
    if (postData) {
      req.write(JSON.stringify(postData));
    }
    
    req.end();
  });
}

// Get available blueprints and print providers
async function getCatalogInfo() {
  console.log('📦 Fetching catalog info...');
  
  try {
    const blueprintsResult = await apiRequest('/v1/catalog/blueprints.json');
    const providersResult = await apiRequest('/v1/catalog/print_providers.json');
    
    if (blueprintsResult.status === 200) {
      const blueprints = blueprintsResult.data.data || [];
      console.log(`   ✅ ${blueprints.length} blueprints available`);
      
      // Find a good T-shirt blueprint
      const tshirt = blueprints.find(b => 
        b.title.toLowerCase().includes('unisex') && 
        b.title.toLowerCase().includes('t-shirt')
      );
      
      if (tshirt) {
        console.log(`   🎯 Using: ${tshirt.title} (ID: ${tshirt.id})`);
        return { blueprintId: tshirt.id };
      }
    }
    
    return null;
  } catch (error) {
    console.error('   ❌ Error:', error.message);
    return null;
  }
}

// Create a product (simplified - uploads image then creates product)
async function createProduct(design, blueprintId) {
  console.log(`\n🎨 Creating product: ${design.title}`);
  
  // Read the SVG file
  const svgPath = path.join(__dirname, 'designs', `${design.id}.svg`);
  if (!fs.existsSync(svgPath)) {
    console.log(`   ❌ Design file not found: ${svgPath}`);
    return null;
  }
  
  // Note: In production, we'd upload the image to Printify first
  // For now, we'll create the product structure
  
  const productData = {
    title: design.title,
    description: design.description,
    blueprint_id: blueprintId,
    print_provider_id: 1, // Will need to be fetched dynamically
    variants: [
      { id: 408, price: Math.round(design.price * 100), is_enabled: true }, // S
      { id: 409, price: Math.round(design.price * 100), is_enabled: true }, // M
      { id: 410, price: Math.round(design.price * 100), is_enabled: true }, // L
      { id: 411, price: Math.round(design.price * 100), is_enabled: true }, // XL
    ],
    print_areas: [
      {
        variant_ids: [408, 409, 410, 411],
        placeholders: [
          {
            position: 'front',
            images: [
              {
                id: 'image_placeholder', // Would be actual uploaded image ID
                x: 0.5,
                y: 0.5,
                scale: 1.0,
                angle: 0
              }
            ]
          }
        ]
      }
    ]
  };
  
  console.log(`   ℹ️  Product data prepared (image upload required)`);
  console.log(`   💰 Price: $${design.price}`);
  console.log(`   🏷️  Tags: ${design.tags.join(', ')}`);
  
  return productData;
}

// Main
async function main() {
  console.log('🚀 Printify Product Publisher\n');
  console.log('═══════════════════════════════════════\n');
  
  // Verify connection
  console.log('🔌 Verifying API connection...');
  const shopResult = await apiRequest('/v1/shops.json');
  if (shopResult.status !== 200) {
    console.error('❌ API connection failed');
    process.exit(1);
  }
  console.log('✅ API connected\n');
  
  // Get catalog info
  const catalog = await getCatalogInfo();
  if (!catalog) {
    console.error('❌ Could not get catalog info');
    process.exit(1);
  }
  
  // Prepare products
  console.log('\n📦 Preparing products...');
  const products = [];
  
  for (const design of DESIGNS) {
    const product = await createProduct(design, catalog.blueprintId);
    if (product) {
      products.push({ design, product });
    }
  }
  
  // Summary
  console.log('\n═══════════════════════════════════════');
  console.log('📊 Publishing Summary');
  console.log('═══════════════════════════════════════');
  console.log(`Products ready: ${products.length}/${DESIGNS.length}`);
  console.log(`Target shop: Quentinvestdesign (${SHOP_ID})`);
  console.log(`Channel: Etsy`);
  console.log('═══════════════════════════════════════\n');
  
  console.log('⚠️  Note: Image upload step required');
  console.log('   Printify API requires images to be uploaded separately');
  console.log('   before products can be created.\n');
  
  console.log('Next steps:');
  console.log('1. Upload images via Printify dashboard or API');
  console.log('2. Create products with image IDs');
  console.log('3. Publish to Etsy\n');
  
  // Export product data
  const output = {
    timestamp: new Date().toISOString(),
    shopId: SHOP_ID,
    products: products.map(p => ({
      title: p.design.title,
      description: p.design.description,
      tags: p.design.tags,
      price: p.design.price,
      designFile: p.design.id + '.svg'
    }))
  };
  
  fs.writeFileSync('products_ready.json', JSON.stringify(output, null, 2));
  console.log('✅ Product data saved to: products_ready.json');
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
