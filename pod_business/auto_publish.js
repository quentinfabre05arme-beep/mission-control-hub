// Auto-publish designs to Printify → Etsy

const fs = require('fs');
const path = require('path');

const CONFIG = JSON.parse(fs.readFileSync('config.json', 'utf8'));
const API_BASE = 'https://api.printify.com/v1';

async function publishToPrintify(design) {
  console.log(`Publishing: ${design.title}...`);
  
  try {
    // Step 1: Create product blueprint
    const productData = {
      title: design.title,
      description: `${design.title} — Perfect for ${design.niche} enthusiasts. High-quality ${design.productType} with unique design.`,
      blueprint_id: getBlueprintId(design.productType),
      print_provider_id: getPrintProviderId(design.productType),
      variants: [ { id: getVariantId(design.productType), price: getPrice(design.productType), is_enabled: true } ],
      print_areas: [ { variant_ids: [getVariantId(design.productType)], placeholders: [ { position: 'front', images: [ { id: 'placeholder', name: design.title, x: 0.5, y: 0.5, scale: 1, angle: 0 } ] } ] } ],
      tags: design.tags.split(',').map(t => t.trim()),
      visibility: 'visible'
    };
    
    const createRes = await fetch(`${API_BASE}/shops/${CONFIG.shop_id}/products.json`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CONFIG.printify_api_token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    });
    
    if (!createRes.ok) {
      const error = await createRes.text();
      console.log(`  ❌ Failed: ${error.substring(0, 100)}`);
      return { success: false, error };
    }
    
    const product = await createRes.json();
    console.log(`  ✅ Created: ${product.id}`);
    
    // Step 2: Publish to Etsy (via sales channel)
    const publishRes = await fetch(`${API_BASE}/shops/${CONFIG.shop_id}/products/${product.id}/publish.json`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CONFIG.printify_api_token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ external: { id: 'etsy', handle: CONFIG.etsy_shop_id } })
    });
    
    if (publishRes.ok) {
      console.log(`  ✅ Published to Etsy`);
      return { success: true, productId: product.id };
    } else {
      console.log(`  ⚠️ Created but not published to Etsy`);
      return { success: true, productId: product.id, published: false };
    }
    
  } catch (error) {
    console.log(`  ❌ Error: ${error.message}`);
    return { success: false, error: error.message };
  }
}

function getBlueprintId(type) {
  const blueprints = {
    't-shirt': 5,      // Gildan 5000
    'mug': 252,        // White ceramic mug
    'poster': 202,     // Poster
    'sticker': 358,    // Die-cut sticker
    'phone-case': 421  // iPhone case
  };
  return blueprints[type] || 5;
}

function getPrintProviderId(type) {
  const providers = {
    't-shirt': 1,      // Printify
    'mug': 1,
    'poster': 1,
    'sticker': 1,
    'phone-case': 1
  };
  return providers[type] || 1;
}

function getVariantId(type) {
  const variants = {
    't-shirt': 4018,   // Black / L
    'mug': 8435,       // White / 11oz
    'poster': 6978,    // 18x24
    'sticker': 10466,  // Small
    'phone-case': 11149 // iPhone 13
  };
  return variants[type] || 4018;
}

function getPrice(type) {
  const prices = {
    't-shirt': 2199,   // $21.99
    'mug': 1299,       // $12.99
    'poster': 1899,    // $18.99
    'sticker': 499,    // $4.99
    'phone-case': 1699 // $16.99
  };
  return prices[type] || 2199;
}

async function run() {
  console.log('=== Auto-Publish to Printify ===\n');
  
  const designs = JSON.parse(fs.readFileSync('generated_designs/batch_2026-07-24.json', 'utf8'));
  console.log(`Publishing ${designs.length} designs...\n`);
  
  const results = [];
  for (const design of designs) {
    const result = await publishToPrintify(design);
    results.push({ design: design.title, ...result });
    
    // Rate limiting
    await new Promise(r => setTimeout(r, 1000));
  }
  
  console.log('\n=== Results ===');
  const success = results.filter(r => r.success).length;
  console.log(`✅ Successful: ${success}/${designs.length}`);
  
  // Save results
  fs.writeFileSync('publish_results_2026-07-24.json', JSON.stringify(results, null, 2));
  console.log('\n📁 Results saved: publish_results_2026-07-24.json');
}

run().catch(console.error);
