#!/usr/bin/env node
/**
 * Printify → Etsy Full Publisher
 * Publishes all designs to Printify and pushes to Etsy
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load config
const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const TOKEN = tokenMatch ? tokenMatch[1].trim() : null;
const SHOP_ID = 28241288;

if (!TOKEN) {
  console.error('❌ Token not found');
  process.exit(1);
}

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
    req.setTimeout(30000, () => reject(new Error('Timeout')));
    if (postData) req.write(JSON.stringify(postData));
    req.end();
  });
}

async function uploadImage(designId) {
  const pngPath = path.join(__dirname, 'designs', `${designId}.png`);
  if (!fs.existsSync(pngPath)) {
    console.log(`   ❌ PNG not found: ${pngPath}`);
    return null;
  }
  
  const imageBuffer = fs.readFileSync(pngPath);
  const base64Data = imageBuffer.toString('base64');
  
  console.log(`   📤 Uploading ${designId}.png (${(imageBuffer.length/1024).toFixed(1)} KB)...`);
  
  try {
    const uploadData = {
      file_name: `${designId}.png`,
      contents: base64Data
    };
    
    const result = await apiRequest('/v1/uploads/images.json', 'POST', uploadData);
    
    if (result.status === 200 && result.data.id) {
      console.log(`   ✅ Image uploaded: ${result.data.id}`);
      return result.data.id;
    } else {
      console.log(`   ❌ Upload failed:`, JSON.stringify(result.data).substring(0, 200));
      return null;
    }
  } catch (error) {
    console.error(`   ❌ Upload error:`, error.message);
    return null;
  }
}

async function getBlueprints() {
  const result = await apiRequest('/v1/catalog/blueprints.json');
  return result.data || [];
}

async function getPrintProviders(blueprintId) {
  const result = await apiRequest(`/v1/catalog/blueprints/${blueprintId}/print_providers.json`);
  return result.data || [];
}

async function createProduct(design, blueprintId, printProviderId, imageId) {
  const productData = {
    title: design.title,
    description: design.description,
    blueprint_id: blueprintId,
    print_provider_id: printProviderId,
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
            images: [{ id: imageId, x: 0.5, y: 0.5, scale: 1.0, angle: 0 }]
          }
        ]
      }
    ]
  };
  
  try {
    const result = await apiRequest(`/v1/shops/${SHOP_ID}/products.json`, 'POST', productData);
    
    if (result.status === 200 || result.status === 201) {
      console.log(`   ✅ Product created: ${result.data.id}`);
      return result.data;
    } else {
      console.log(`   ❌ Product failed:`, JSON.stringify(result.data).substring(0, 300));
      return null;
    }
  } catch (error) {
    console.error(`   ❌ Error:`, error.message);
    return null;
  }
}

async function publishToEtsy(productId) {
  try {
    const result = await apiRequest(
      `/v1/shops/${SHOP_ID}/products/${productId}/publish.json`,
      'POST',
      {}
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

async function main() {
  console.log('🚀 Printify → Etsy Publisher\n');
  console.log('═══════════════════════════════════════\n');
  
  // Verify connection
  console.log('🔌 Verifying API connection...');
  const shopResult = await apiRequest('/v1/shops.json');
  if (shopResult.status !== 200) {
    console.error('❌ API connection failed');
    process.exit(1);
  }
  console.log('✅ API connected: Quentinvestdesign\n');
  
  // Get catalog
  console.log('📦 Loading catalog...');
  const blueprints = await getBlueprints();
  const tshirt = blueprints.find(b => b.title && b.title.toLowerCase().includes('unisex') && b.title.toLowerCase().includes('t-shirt'));
  
  if (!tshirt) {
    console.error('❌ No suitable t-shirt blueprint found');
    process.exit(1);
  }
  
  console.log(`   🎯 Blueprint: ${tshirt.title} (ID: ${tshirt.id})`);
  
  const providers = await getPrintProviders(tshirt.id);
  if (providers.length === 0) {
    console.error('❌ No print providers found');
    process.exit(1);
  }
  
  console.log(`   ✅ ${providers.length} print providers available\n`);
  
  // Process all designs
  const results = [];
  
  for (const design of DESIGNS) {
    console.log(`\n🎨 Processing: ${design.title}`);
    
    const imageId = await uploadImage(design.id);
    if (!imageId) {
      console.log(`   ⏭️ Skipping (upload failed)`);
      continue;
    }
    
    const product = await createProduct(design, tshirt.id, providers[0].id, imageId);
    if (!product) {
      console.log(`   ⏭️ Skipping (product creation failed)`);
      continue;
    }
    
    // Wait a moment before publishing
    await new Promise(r => setTimeout(r, 500));
    
    const published = await publishToEtsy(product.id);
    results.push({ design, product, published });
    
    // Rate limiting between products
    if (DESIGNS.indexOf(design) < DESIGNS.length - 1) {
      console.log('   ⏳ Rate limiting (2s)...');
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  // Summary
  console.log('\n═══════════════════════════════════════');
  console.log('📊 PUBLISHING COMPLETE');
  console.log('═══════════════════════════════════════');
  console.log(`Total designs: ${DESIGNS.length}`);
  console.log(`Products created: ${results.length}`);
  console.log(`Published to Etsy: ${results.filter(r => r.published).length}`);
  console.log('═══════════════════════════════════════\n');
  
  // List products
  if (results.length > 0) {
    console.log('📦 Products Live:');
    results.forEach((r, i) => {
      console.log(`  ${i+1}. ${r.design.title}`);
      console.log(`     ID: ${r.product.id}`);
      console.log(`     Price: $${r.design.price}`);
      console.log(`     Etsy: ${r.published ? '✅ Published' : '❌ Not published'}`);
    });
    
    // Save results
    const output = {
      timestamp: new Date().toISOString(),
      shopId: SHOP_ID,
      shopName: 'Quentinvestdesign',
      products: results.map(r => ({
        title: r.design.title,
        productId: r.product.id,
        price: r.design.price,
        etsyPublished: r.published,
        url: `https://printify.com/app/product/${r.product.id}`
      }))
    };
    
    fs.writeFileSync('products_live.json', JSON.stringify(output, null, 2));
    console.log('\n✅ Results saved to: products_live.json');
    console.log('\n🎉 BUSINESS IS LIVE!');
    console.log('🔗 Check your Printify dashboard: https://printify.com/app/products');
    console.log('🔗 Etsy shop: https://quentinvestdesigns.etsy.com');
  } else {
    console.log('❌ No products were published. Check errors above.');
  }
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});