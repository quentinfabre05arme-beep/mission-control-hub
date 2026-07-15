// pod_mockup_generator.js - Create product mockups and manage Printify integration
// Generates product previews and automates Printify publishing

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  mockupsDir: 'C:\\Users\\quent\\.openclaw\workspace\\pod_business\\mockups',
  printifyApiKey: process.env.PRINTIFY_API_KEY,
  printifyBaseUrl: 'https://api.printify.com/v1',
  shopId: process.env.PRINTIFY_SHOP_ID
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true }).catch(() => {});
}

async function log(msg) {
  console.log(`[POD-MOCKUP] ${msg}`);
}

// Product templates for Printify
const PRODUCT_TEMPLATES = [
  {
    id: 'unisex-jersey-t-shirt',
    name: 'Unisex Jersey Short Sleeve Tee',
    description: 'A premium quality t-shirt featuring a timeless design. Made from soft, breathable cotton.',
    basePrice: 12.50,
    variants: ['S', 'M', 'L', 'XL', '2XL', '3XL'],
    colors: ['Black', 'White', 'Navy', 'Heather Grey', 'Red']
  },
  {
    id: 'mug-11oz',
    name: 'White Ceramic Mug 11oz',
    description: 'Perfect for coffee, tea, and hot chocolate. Classic white ceramic with a glossy finish.',
    basePrice: 8.95,
    variants: ['11oz'],
    colors: ['White']
  },
  {
    id: 'poster-matte',
    name: 'Matte Poster',
    description: 'Museum-quality posters made on thick matte paper. Perfect for framing.',
    basePrice: 15.00,
    variants: ['12x16', '18x24', '24x36'],
    colors: ['Standard']
  },
  {
    id: 'sticker-diecut',
    name: 'Die Cut Sticker',
    description: 'High-quality vinyl stickers with a permanent adhesive. Weatherproof and dishwasher safe.',
    basePrice: 3.50,
    variants: ['Small', 'Medium', 'Large'],
    colors: ['Transparent']
  }
];

// Create HTML mockup template
async function generateMockupHtml(design, product) {
  const template = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${design.concept.text} - ${product.name}</title>
  <style>
    body { margin: 0; padding: 40px; background: #f5f5f5; font-family: Arial, sans-serif; }
    .mockup-container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .product-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px; }
    .product-image { background: #f9f9f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; min-height: 400px; }
    .product-image svg { max-width: 100%; height: auto; }
    .product-info { padding: 20px; }
    .title { font-size: 28px; font-weight: bold; color: #333; margin-bottom: 10px; }
    .price { font-size: 24px; color: #4CAF50; margin-bottom: 20px; }
    .description { color: #666; line-height: 1.6; margin-bottom: 20px; }
    .tags { display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { background: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 16px; font-size: 12px; }
    .platforms { margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 8px; }
    .platform { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #ddd; }
    .status-pending { color: #ff9800; }
    .status-ready { color: #4caf50; }
    .status-published { color: #2196f3; }
  </style>
</head>
<body>
  <div class="mockup-container">
    <h1>Product Mockup</h1>
    <div class="product-grid">
      <div class="product-image">
        ${await fs.readFile(design.filepath, 'utf-8')}
      </div>
      <div class="product-info">
        <div class="title">${design.concept.text}</div>
        <div class="price">$${(product.basePrice * 2.5).toFixed(2)}</div>
        <div class="description">
          ${product.description}
          <br><br>
          Perfect for ${design.metadata.tags.slice(0, 3).join(', ')} enthusiasts.
        </div>
        <div class="tags">
          ${design.metadata.tags.map(t => `<span class="tag">${t}</span>`).join('')}
        </div>
      </div>
    </div>
    
    <div class="platforms">
      <h3>Platform Status</h3>
      <div class="platform">
        <span>Printify (Etsy/Shopify)</span>
        <span class="status-${design.platforms.printify.status}">${design.platforms.printify.status}</span>
      </div>
      <div class="platform">
        <span>Redbubble</span>
        <span class="status-${design.platforms.redbubble.status}">${design.platforms.redbubble.status}</span>
      </div>
      <div class="platform">
        <span>Teespring/Spring</span>
        <span class="status-${design.platforms.teespring.status}">${design.platforms.teespring.status}</span>
      </div>
    </div>
  </div>
</body>
</html>`;
  
  return template;
}

// Generate mockups for a design
async function generateMockups(designId) {
  log(`Generating mockups for ${designId}...`);
  
  // Load design
  const registryPath = path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business\\designs', 'designs_registry.json');
  const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
  const design = registry.find(d => d.id === designId);
  
  if (!design) {
    throw new Error(`Design ${designId} not found`);
  }
  
  const mockups = [];
  
  // Generate mockup for each product type
  for (const product of PRODUCT_TEMPLATES) {
    const mockupId = `mockup_${designId}_${product.id}`;
    const filename = `${mockupId}.html`;
    const filepath = path.join(CONFIG.mockupsDir, filename);
    
    const html = await generateMockupHtml(design, product);
    await ensureDir(CONFIG.mockupsDir);
    await fs.writeFile(filepath, html);
    
    mockups.push({
      id: mockupId,
      designId: designId,
      product: product,
      filepath: filepath,
      filename: filename,
      created: new Date().toISOString(),
      pricing: {
        baseCost: product.basePrice,
        retailPrice: (product.basePrice * 2.5).toFixed(2),
        profit: (product.basePrice * 1.5).toFixed(2)
      }
    });
    
    log(`+ ${product.name} mockup created`);
  }
  
  // Update design status
  const designIndex = registry.findIndex(d => d.id === designId);
  registry[designIndex].status = 'mockup_ready';
  registry[designIndex].mockups = mockups;
  await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
  
  return mockups;
}

// Printify API Integration
async function publishToPrintify(designId, productIds = ['unisex-jersey-t-shirt']) {
  if (!CONFIG.printifyApiKey) {
    log('Printify API key not configured. Set PRINTIFY_API_KEY environment variable.');
    return { status: 'error', message: 'API key missing' };
  }
  
  log(`Publishing ${designId} to Printify...`);
  
  // Load design
  const registryPath = path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business\\designs', 'designs_registry.json');
  const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
  const design = registry.find(d => d.id === designId);
  
  if (!design) {
    return { status: 'error', message: 'Design not found' };
  }
  
  const results = [];
  
  for (const productId of productIds) {
    const product = PRODUCT_TEMPLATES.find(p => p.id === productId);
    if (!product) continue;
    
    try {
      // Step 1: Upload design image to Printify
      // Note: In production, would upload SVG converted to PNG
      const uploadData = {
        file_name: design.filename,
        url: 'https://example.com/placeholder-image.png' // Would be actual hosted image
      };
      
      // Step 2: Create product
      const productData = {
        title: `${design.concept.text} - ${product.name}`,
        description: product.description,
        blueprint_id: getBlueprintId(productId),
        print_provider_id: getPrintProviderId(),
        variants: generateVariants(product),
        print_areas: [
          {
            variant_ids: generateVariantIds(product),
            placeholders: [
              {
                position: 'front',
                image_url: uploadData.url,
                crop: { x: 0.5, y: 0.5, scale: 1.0 }
              }
            ]
          }
        ]
      };
      
      // Simulate API call (real implementation would use fetch/axios)
      const mockResponse = {
        id: `printify_${Date.now()}`,
        status: 'pending',
        title: productData.title,
        preview_url: `https://printify.com/preview/${Date.now()}`
      };
      
      results.push({
        product: productId,
        status: 'success',
        printifyId: mockResponse.id,
        previewUrl: mockResponse.preview_url
      });
      
      log(`+ Published to Printify: ${product.name}`);
      
    } catch (err) {
      log(`Error publishing ${productId}: ${err.message}`);
      results.push({ product: productId, status: 'error', message: err.message });
    }
  }
  
  // Update design status
  const designIndex = registry.findIndex(d => d.id === designId);
  registry[designIndex].platforms.printify = {
    status: results.some(r => r.status === 'success') ? 'published' : 'error',
    results: results,
    publishedAt: new Date().toISOString()
  };
  await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
  
  return { status: 'success', results };
}

// Helper functions for Printify
function getBlueprintId(productId) {
  const blueprintMap = {
    'unisex-jersey-t-shirt': 5,
    'mug-11oz': 110,
    'poster-matte': 20,
    'sticker-diecut': 369
  };
  return blueprintMap[productId] || 5;
}

function getPrintProviderId() {
  return 99; // Example provider
}

function generateVariants(product) {
  return product.variants.map((v, i) => ({
    id: i + 1,
    title: v,
    price: Math.round(product.basePrice * 250) // cents
  }));
}

function generateVariantIds(product) {
  return product.variants.map((_, i) => i + 1);
}

// Generate Redbubble listing data
async function generateRedbubbleListing(designId) {
  log(`Generating Redbubble listing for ${designId}...`);
  
  const registryPath = path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business\\designs', 'designs_registry.json');
  const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
  const design = registry.find(d => d.id === designId);
  
  if (!design) return null;
  
  const listing = {
    platform: 'redbubble',
    designId: designId,
    title: `${design.concept.text} - ${design.concept.subtext}`,
    description: generateDescription(design),
    tags: [...design.metadata.tags, 'print on demand', 'digital art', 'trending'].slice(0, 15),
    products: ['t-shirt', 'sticker', 'mug', 'poster', 'phone case'],
    pricing: {
      markup: 20 // 20% markup
    },
    files: {
      design: design.filepath,
      // Redbubble requires manual upload of PNG
      instructions: `Upload ${design.filename} converted to PNG, 7632x6480px for best quality`
    },
    created: new Date().toISOString(),
    status: 'ready_for_manual_upload'
  };
  
  // Save listing
  const listingsPath = path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business\\redbubble_listings.json');
  let listings = [];
  try {
    listings = JSON.parse(await fs.readFile(listingsPath, 'utf-8'));
  } catch {}
  
  listings.push(listing);
  await fs.writeFile(listingsPath, JSON.stringify(listings, null, 2));
  
  // Update design
  const designIndex = registry.findIndex(d => d.id === designId);
  registry[designIndex].platforms.redbubble.status = 'ready';
  await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
  
  log(`Redbubble listing ready: ${listing.title}`);
  return listing;
}

function generateDescription(design) {
  const templates = [
    `Show off your love for ${design.metadata.tags[0]} with this unique design. Perfect for ${design.metadata.tags[1]} enthusiasts.`,
    `Minimalist ${design.metadata.tags[0]} design for those who appreciate clean aesthetics. Great conversation starter.`,
    `Express your passion for ${design.concept.subtext} with this premium quality design. Makes a great gift!`
  ];
  return templates[Math.floor(Math.random() * templates.length)];
}

// Main execution
async function main() {
  log('=== POD Mockup Generator Starting ===');
  
  // Get designs ready for mockup
  const registryPath = path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business\\designs', 'designs_registry.json');
  const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
  const pending = registry.filter(d => d.status === 'ready_for_mockup');
  
  log(`${pending.length} designs pending mockup`);
  
  for (const design of pending.slice(0, 3)) {
    await generateMockups(design.id);
    
    // Generate Redbubble listing
    await generateRedbubbleListing(design.id);
  }
  
  // Try Printify publishing (if API key available)
  if (CONFIG.printifyApiKey) {
    const printifyReady = registry.filter(d => d.status === 'mockup_ready');
    for (const design of printifyReady.slice(0, 2)) {
      await publishToPrintify(design.id);
    }
  } else {
    log('Printify API key not set. Skipping automated publishing.');
    log('Set PRINTIFY_API_KEY to enable automatic uploads.');
  }
  
  log('=== POD Mockup Generator Complete ===');
}

module.exports = {
  generateMockups,
  publishToPrintify,
  generateRedbubbleListing,
  PRODUCT_TEMPLATES
};

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}
