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
    price: 29.99
  },
  {
    id: 'design_crypto_1784049410607',
    title: 'HODL Strong',
    description: 'Classic crypto mantra for true believers. Bold design for Bitcoin and crypto enthusiasts.',
    tags: ['hodl', 'bitcoin', 'crypto', 'cryptocurrency', 'strong', 'investor', 'blockchain'],
    price: 29.99
  },
  {
    id: 'design_fitness_1784049410604',
    title: 'Fitness Motivation',
    description: 'Premium fitness design for gym enthusiasts and athletes.',
    tags: ['fitness', 'gym', 'workout', 'motivation', 'health', 'training'],
    price: 27.99
  },
  {
    id: 'design_professions_1784049410606',
    title: 'Professional Pride',
    description: 'Celebrate your profession with this premium design.',
    tags: ['profession', 'career', 'job', 'work', 'professional'],
    price: 27.99
  },
  {
    id: 'design_professions_1784049410609',
    title: 'Work Hard',
    description: 'Motivational design for dedicated professionals.',
    tags: ['work', 'motivation', 'professional', 'career', 'success'],
    price: 27.99
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
          // Handle both array and object responses
          if (Array.isArray(json)) {
            resolve({ status: res.statusCode, data: json });
          } else {
            resolve({ status: res.statusCode, data: json.data || json });
          }
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

// Get available blueprints
async function getCatalogInfo() {
  console.log('📦 Fetching catalog info...');
  
  try {
    const blueprintsResult = await apiRequest('/v1/catalog/blueprints.json');
    
    if (blueprintsResult.status === 200 && Array.isArray(blueprintsResult.data)) {
      const blueprints = blueprintsResult.data;
      console.log(`   ✅ ${blueprints.length} blueprints available`);
      
      // Find a good T-shirt blueprint
      const tshirt = blueprints.find(b => 
        b.title && b.title.toLowerCase().includes('unisex') && 
        b.title.toLowerCase().includes('t-shirt')
      );
      
      if (tshirt) {
        console.log(`   🎯 Using: ${tshirt.title} (ID: ${tshirt.id})`);
        
        // Get print providers for this blueprint
        const providersResult = await apiRequest(`/v1/catalog/blueprints/${tshirt.id}/print_providers.json`);
        const providers = providersResult.data || [];
        
        if (providers.length > 0) {
          console.log(`   ✅ ${providers.length} print providers available`);
          return { 
            blueprintId: tshirt.id,
            printProviderId: providers[0].id
          };
        }
      }
    }
    
    return null;
  } catch (error) {
    console.error('   ❌ Error:', error.message);
    return null;
  }
}

// Upload image to Printify
async function uploadImage(designId) {
  const svgPath = path.join(__dirname, 'designs', `${designId}.svg`);
  if (!fs.existsSync(svgPath)) {
    console.log(`   ❌ Design file not found: ${svgPath}`);
    return null;
  }
  
  const svgContent = fs.readFileSync(svgPath);
  
  console.log('   📤 Uploading image...');
  
  try {
    // Upload the image using base64
    const uploadData = {
      file_name: `${designId}.svg`,
      contents: svgContent.toString('base64')
    };
    
    const result = await apiRequest('/v1/uploads/images.json', 'POST', uploadData);
    
    if (result.status === 200 && result.data.id) {
      console.log(`   ✅ Image uploaded: ${result.data.id}`);
      return result.data.id;
    } else {
      console.log(`   ⚠️ Upload response:`, JSON.stringify(result.data).substring(0, 300));
      return null;
    }
  } catch (error) {
    console.error('   ❌ Upload error:', error.message);
    return null;
  }
}

// Create a product
async function createProduct(design, catalog, imageId) {
  console.log(`\n🎨 Creating product: ${design.title}`);
  
  const productData = {
    title: design.title,
    description: design.description,
    blueprint_id: catalog.blueprintId,
    print_provider_id: catalog.printProviderId,
    variants: [
      { id: 408, price: Math.round(design.price * 100), is_enabled: true },
      { id: 409, price: Math.round(design.price * 100), is_enabled: true },
      { id: 410, price: Math.round(design.price * 100), is_enabled: true },
      { id: 411, price: Math.round(design.price * 100), is_enabled: true },
    ],
    print_areas: [
      {
        variant_ids: [408, 409, 410, 411],
        placeholders: [
          {
            position: 'front',
            images: [
              {
                id: imageId,
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
  
  try {
    const result = await apiRequest(`/v1/shops/${SHOP_ID}/products.json`, 'POST', productData);
    
    if (result.status === 200 || result.status === 201) {
      console.log(`   ✅ Product created: ${result.data.id || 'N/A'}`);
      return result.data;
    } else {
      console.log(`   ❌ Failed:`, JSON.stringify(result.data).substring(0, 400));
      return null;
    }
  } catch (error) {
    console.error('   ❌ Error:', error.message);
    return null;
  }
}

// Publish product to Etsy
async function publishToEtsy(productId) {
  console.log('   📤 Publishing to Etsy...');
  
  try {
    const result = await apiRequest(
      `/v1/shops/${SHOP_ID}/products/${productId}/publish.json`,
      'POST',
      { external: { id: productId } }
    );
    
    if (result.status === 200) {
      console.log('   ✅ Published to Etsy');
      return true;
    } else {
      console.log(`   ⚠️ Publish response:`, JSON.stringify(result.data).substring(0, 200));
      return false;
    }
  } catch (error) {
    console.error('   ❌ Publish error:', error.message);
    return false;
  }
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
  
  // Process first design
  console.log('\n📦 Starting product creation...');
  const results = [];
  
  for (const design of DESIGNS.slice(0, 1)) { // Start with 1 design
    const imageId = await uploadImage(design.id);
    if (imageId) {
      const product = await createProduct(design, catalog, imageId);
      if (product) {
        const published = await publishToEtsy(product.id);
        results.push({ design, product, published });
      }
    }
    
    // Rate limiting
    await new Promise(r => setTimeout(r, 1000));
  }
  
  // Summary
  console.log('\n═══════════════════════════════════════');
  console.log('📊 Publishing Summary');
  console.log('═══════════════════════════════════════');
  console.log(`Products created: ${results.length}`);
  console.log(`Published to Etsy: ${results.filter(r => r.published).length}`);
  console.log('═══════════════════════════════════════\n');
  
  // Save results
  const output = {
    timestamp: new Date().toISOString(),
    shopId: SHOP_ID,
    results: results.map(r => ({
      title: r.design.title,
      productId: r.product.id,
      published: r.published
    }))
  };
  
  fs.writeFileSync('publish_results.json', JSON.stringify(output, null, 2));
  console.log('✅ Results saved to: publish_results.json');
  
  if (results.length > 0) {
    console.log('\n🎉 First product published! Check your Printify dashboard.');
  }
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});