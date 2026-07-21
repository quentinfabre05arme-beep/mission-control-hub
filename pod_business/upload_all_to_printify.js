#!/usr/bin/env node
/**
 * Upload all 5 AI designs to Printify and publish to Etsy
 * Uses Unisex Softstyle T-Shirt blueprint with DTG printing
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  apiKey: process.env.PRINTIFY_API_KEY || require('fs').readFileSync('.env.local', 'utf8').match(/PRINTIFY_API_KEY=(.+)/)?.[1]?.trim(),
  shopId: process.env.PRINTIFY_SHOP_ID || '28241288',
  blueprintId: 5, // Unisex Softstyle T-Shirt
  printProviderId: 26, // Printful or similar high-quality
  position: { 
    // Center chest placement
    area: 'front',
    horizontal: 'center',
    vertical: 'center',
    crop: 'center'
  }
};

const DESIGNS = [
  {
    name: "Bitcoin Millionaire Tee",
    file: "design_1_bitcoin_millionaire.png",
    description: "Premium Bitcoin-themed t-shirt for crypto investors and HODLers. Elegant gold typography on black. Softstyle unisex fit.",
    tags: ["bitcoin", "crypto", "millionaire", "investor", "gift", "hodl"],
    price: 29.99
  },
  {
    name: "HODL Life Tee",
    file: "design_2_hodl_life.png",
    description: "Modern streetwear for crypto traders. Bold white letters on navy. Candlestick chart pattern. HODL lifestyle.",
    tags: ["hodl", "crypto", "trading", "investing", "streetwear"],
    price: 29.99
  },
  {
    name: "ETH Bull Tee",
    file: "design_3_eth_bull.png",
    description: "Ethereum bullish design with silver metallic typography. Tech-forward aesthetic for ETH believers.",
    tags: ["ethereum", "eth", "bull", "crypto", "web3"],
    price: 29.99
  },
  {
    name: "Satoshi Vision Tee",
    file: "design_4_satoshi_vision.png",
    description: "Minimalist Bitcoin founder tribute. Clean white text on matte black. Circuit board pattern. Premium understated style.",
    tags: ["bitcoin", "satoshi", "crypto", "minimalist", "founder"],
    price: 29.99
  },
  {
    name: "DeFi Degen Tee",
    file: "design_5_defi_degen.png",
    description: "Bold DeFi culture design with vibrant purple-pink gradient. For Web3 degens and DeFi enthusiasts.",
    tags: ["defi", "degenerate", "crypto", "web3", "defi"],
    price: 29.99
  }
];

const LOG_FILE = path.join(__dirname, 'logs', 'printify_upload.log');

function log(message) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${message}`;
  console.log(entry);
  if (!fs.existsSync(path.dirname(LOG_FILE))) {
    fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
  }
  fs.appendFileSync(LOG_FILE, entry + '\n');
}

async function uploadImage(imagePath) {
  log(`📤 Uploading image: ${path.basename(imagePath)}`);
  
  try {
    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');
    
    // Create upload via Printify API
    const response = await fetch('https://api.printify.com/v1/uploads/images.json', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        file_name: path.basename(imagePath),
        contents: base64Image
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Upload failed: ${error}`);
    }
    
    const data = await response.json();
    log(`✅ Image uploaded: ${data.id}`);
    return data.id;
  } catch (error) {
    log(`❌ Upload error: ${error.message}`);
    return null;
  }
}

async function createProduct(design, imageId) {
  log(`🛠️ Creating product: ${design.name}`);
  
  try {
    const response = await fetch(`https://api.printify.com/v1/shops/${CONFIG.shopId}/products.json`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: design.name,
        description: design.description,
        blueprint_id: CONFIG.blueprintId,
        print_provider_id: CONFIG.printProviderId,
        variants: [
          { id: 4012, price: design.price * 100 }, // S
          { id: 4013, price: design.price * 100 }, // M  
          { id: 4014, price: design.price * 100 }, // L
          { id: 4015, price: design.price * 100 }, // XL
          { id: 4016, price: design.price * 100 }  // 2XL
        ],
        print_areas: [
          {
            variant_ids: [4012, 4013, 4014, 4015, 4016],
            placeholders: [
              {
                position: CONFIG.position,
                images: [
                  {
                    id: imageId,
                    name: design.file,
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
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Product creation failed: ${error}`);
    }
    
    const data = await response.json();
    log(`✅ Product created: ${data.id}`);
    return data;
  } catch (error) {
    log(`❌ Product error: ${error.message}`);
    return null;
  }
}

async function publishToEtsy(productId) {
  log(`🚀 Publishing to Etsy: ${productId}`);
  
  try {
    const response = await fetch(`https://api.printify.com/v1/shops/${CONFIG.shopId}/products/${productId}/publish.json`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: true,
        description: true,
        images: true,
        variants: true,
        tags: true
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Publish failed: ${error}`);
    }
    
    log(`✅ Published to Etsy`);
    return true;
  } catch (error) {
    log(`❌ Publish error: ${error.message}`);
    return false;
  }
}

async function main() {
  log('╔════════════════════════════════════════════╗');
  log('║   Printify → Etsy Upload - Batch 5 Designs ║');
  log('╚════════════════════════════════════════════╝');
  
  if (!CONFIG.apiKey) {
    log('❌ Printify API key not found');
    process.exit(1);
  }
  
  const results = [];
  
  for (const design of DESIGNS) {
    const imagePath = path.join(__dirname, 'generated', design.file);
    
    if (!fs.existsSync(imagePath)) {
      log(`⚠️ Image not found: ${design.file}`);
      results.push({ design: design.name, status: 'skipped', reason: 'image not found' });
      continue;
    }
    
    log(`\n--- Processing: ${design.name} ---`);
    
    // Step 1: Upload image
    const imageId = await uploadImage(imagePath);
    if (!imageId) {
      results.push({ design: design.name, status: 'failed', step: 'upload' });
      continue;
    }
    
    // Step 2: Create product
    const product = await createProduct(design, imageId);
    if (!product) {
      results.push({ design: design.name, status: 'failed', step: 'product' });
      continue;
    }
    
    // Step 3: Publish to Etsy
    const published = await publishToEtsy(product.id);
    
    results.push({
      design: design.name,
      status: published ? 'success' : 'partial',
      productId: product.id,
      published: published
    });
    
    // Small delay between products
    await new Promise(r => setTimeout(r, 2000));
  }
  
  // Summary
  log('\n╔════════════════════════════════════════════╗');
  log('║              UPLOAD SUMMARY                 ║');
  log('╚════════════════════════════════════════════╝');
  
  const successful = results.filter(r => r.status === 'success').length;
  const partial = results.filter(r => r.status === 'partial').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const skipped = results.filter(r => r.status === 'skipped').length;
  
  log(`Total: ${results.length}`);
  log(`✅ Success: ${successful} | ⚠️ Partial: ${partial} | ❌ Failed: ${failed} | ⏭️ Skipped: ${skipped}`);
  
  results.forEach(r => {
    if (r.status === 'success') {
      log(`✅ ${r.design} → Published (ID: ${r.productId})`);
    } else if (r.status === 'partial') {
      log(`⚠️ ${r.design} → Created but not published`);
    } else if (r.status === 'failed') {
      log(`❌ ${r.design} → Failed at ${r.step}`);
    } else {
      log(`⏭️ ${r.design} → ${r.reason}`);
    }
  });
  
  log('\n📁 Log file: ' + LOG_FILE);
  
  return results;
}

main().catch(err => {
  log(`FATAL ERROR: ${err.message}`);
  process.exit(1);
});
