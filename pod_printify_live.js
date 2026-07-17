const https = require('https');
const fs = require('fs').promises;
const path = require('path');

// Load from .env file if exists (prioritize .env.local)
// Try multiple paths since script can be run from different directories
const possiblePaths = [
  path.join(process.cwd(), 'pod_business', '.env.local'),
  path.join(process.cwd(), '.env.local'),
  path.join(__dirname, 'pod_business', '.env.local'),
  path.join(__dirname, '.env.local'),
  'C:\\Users\\quent\\.openclaw\\workspace\\pod_business\\.env.local'
];

let envLoaded = false;
for (const envPath of possiblePaths) {
  if (require('fs').existsSync(envPath)) {
    require('dotenv').config({ path: envPath });
    envLoaded = true;
    break;
  }
}

if (!envLoaded) {
  console.error('Warning: No .env file found');
}

const CONFIG = {
  apiKey: process.env.PRINTIFY_API_KEY,
  shopId: process.env.PRINTIFY_SHOP_ID,
  baseUrl: 'api.printify.com',
  dataDir: 'C:\\Users\\quent\\.openclaw\\workspace\\pod_business',
  autoPublish: true,
  dailyQuota: 5
};

// HTTP request helper
function apiRequest(endpoint, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    if (!CONFIG.apiKey) {
      reject(new Error('PRINTIFY_API_KEY not set'));
      return;
    }

    const options = {
      hostname: CONFIG.baseUrl,
      path: `/v1${endpoint}`,
      method: method,
      headers: {
        'Authorization': `Bearer ${CONFIG.apiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': 'Quentinvest-POD-Automation/1.0'
      }
    };

    if (body) {
      const bodyString = JSON.stringify(body);
      options.headers['Content-Length'] = Buffer.byteLength(bodyString);
    }

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(json);
          } else {
            reject(new Error(`API Error ${res.statusCode}: ${json.error || data}`));
          }
        } catch {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function log(msg) {
  const ts = new Date().toISOString();
  const logLine = `[${ts}] [POD] ${msg}\n`;
  console.log(logLine.trim());
  
  // Append to log file
  try {
    await fs.appendFile(path.join(CONFIG.dataDir, 'automation.log'), logLine);
  } catch {}
}

// Get shops
async function getShops() {
  log('Fetching shops...');
  const response = await apiRequest('/shops.json');
  // Handle both {data: [...]} and [...] response formats
  return response.data || (Array.isArray(response) ? response : []) || [];
}

// Upload image
async function uploadImage(imagePath, fileName) {
  log(`Uploading image: ${fileName}`);
  
  // Read file as base64
  const imageBuffer = await fs.readFile(imagePath);
  const base64Image = imageBuffer.toString('base64');
  
  const uploadData = {
    file_name: fileName,
    contents: base64Image
  };
  
  const result = await apiRequest('/uploads.json', 'POST', uploadData);
  log(`Image uploaded: ${result.id}`);
  return result;
}

// Get blueprints
async function getBlueprints() {
  log('Fetching product blueprints...');
  const response = await apiRequest('/catalog/blueprints.json');
  return response.data || [];
}

// Get print providers for a blueprint
async function getPrintProviders(blueprintId) {
  const response = await apiRequest(`/catalog/blueprints/${blueprintId}/print_providers.json`);
  return response.data || [];
}

// Create product
async function createProduct(shopId, productData) {
  log(`Creating product: ${productData.title}`);
  const result = await apiRequest(`/shops/${shopId}/products.json`, 'POST', productData);
  log(`Product created: ${result.id}`);
  return result;
}

// Publish product
async function publishProduct(shopId, productId) {
  log(`Publishing product ${productId}...`);
  await apiRequest(`/shops/${shopId}/products/${productId}/publish.json`, 'POST', {});
  log(`Product published successfully`);
}

// Generate product data
function generateProductData(imageId, design) {
  return {
    title: `${design.text} - Premium Design`,
    description: generateDescription(design),
    blueprint_id: 5, // Unisex Jersey Short Sleeve Tee
    print_provider_id: 99, // Example: Printify
    variants: [
      { id: 60833, price: 2499, is_enabled: true }, // S
      { id: 60834, price: 2499, is_enabled: true }, // M  
      { id: 60835, price: 2499, is_enabled: true }, // L
      { id: 60836, price: 2699, is_enabled: true }, // XL
      { id: 60837, price: 2899, is_enabled: true }  // 2XL
    ],
    print_areas: [{
      variant_ids: [60833, 60834, 60835, 60836, 60837],
      placeholders: [{
        position: 'front',
        images: [{
          id: imageId,
          x: 0.5,
          y: 0.5,
          scale: 1.0,
          angle: 0
        }]
      }]
    }],
    tags: [design.category, 'trending', 'premium']
  };
}

function generateDescription(design) {
  return `Premium ${design.category} design featuring "${design.text}". 

• High-quality DTG printing
• Premium cotton blend
• Data-driven design aesthetic
• Perfect for ${design.category} enthusiasts

Printed on demand with worldwide shipping.`;
}

// Full automation cycle
async function runAutomation() {
  log('=== PRINTIFY FULL AUTOMATION STARTING ===');
  
  // Step 1: Get shops
  const shops = await getShops();
  if (shops.length === 0) {
    throw new Error('No shops found. Create a shop in Printify first.');
  }
  
  const shopId = CONFIG.shopId !== 'auto' ? CONFIG.shopId : shops[0].id;
  log(`Using shop: ${shops[0].title} (ID: ${shopId})`);
  
  // Step 2: Load designs
  const designsDir = path.join(CONFIG.dataDir, 'designs');
  const designFiles = await fs.readdir(designsDir).catch(() => []);
  const svgFiles = designFiles.filter(f => f.endsWith('.svg')).slice(0, CONFIG.dailyQuota);
  
  log(`${svgFiles.length} designs to process`);
  
  // Step 3: Process each design
  const results = [];
  
  for (const svgFile of svgFiles) {
    try {
      const designPath = path.join(designsDir, svgFile);
      
      // Parse design name
      const designName = svgFile.replace('.svg', '').replace(/_/g, ' ').toUpperCase();
      const category = svgFile.includes('crypto') ? 'crypto' : 
                      svgFile.includes('fitness') ? 'fitness' : 'professions';
      
      const design = {
        text: designName,
        category: category
      };
      
      // Upload image
      // Note: Printify accepts various formats, but we'll need to convert SVG first
      // For now, log the intent
      log(`Would upload: ${svgFile}`);
      
      // In production, convert SVG to PNG first, then upload
      results.push({
        design: svgFile,
        status: 'ready_for_upload',
        shopId: shopId
      });
      
    } catch (err) {
      log(`Error processing ${svgFile}: ${err.message}`);
      results.push({ design: svgFile, status: 'error', message: err.message });
    }
  }
  
  // Step 4: Save results
  const summary = {
    timestamp: new Date().toISOString(),
    shopId: shopId,
    designsProcessed: svgFiles.length,
    results: results
  };
  
  await fs.writeFile(
    path.join(CONFIG.dataDir, 'automation_results.json'),
    JSON.stringify(summary, null, 2)
  );
  
  log('=== AUTOMATION COMPLETE ===');
  return summary;
}

// Check status
async function checkStatus() {
  log('Checking Printify status...');
  
  try {
    const shops = await getShops();
    
    if (shops.length > 0) {
      const shop = shops[0];
      log(`✓ Connected to Printify`);
      log(`✓ Shop: ${shop.title} (ID: ${shop.id})`);
      
      // Update shop ID in config
      CONFIG.shopId = shop.id;
      
      return {
        status: 'connected',
        shop: shop,
        message: 'Ready for full automation'
      };
    } else {
      return {
        status: 'no_shops',
        message: 'No shops found. Create a shop in Printify dashboard first.'
      };
    }
    
  } catch (err) {
    return {
      status: 'error',
      message: err.message
    };
  }
}

// Main entry
async function main() {
  const mode = process.argv[2];
  
  switch(mode) {
    case 'status':
      const status = await checkStatus();
      console.log(JSON.stringify(status, null, 2));
      break;
      
    case 'run':
      await runAutomation();
      break;
      
    case 'upload':
      // Test upload
      log('Test upload mode - requires PNG conversion first');
      break;
      
    default:
      console.log(`
Printify Full Automation - ACTIVE

Usage: node pod_printify_live.js [command]

Commands:
  status  - Check API connection and shop status
  run     - Run full automation cycle
  upload  - Test image upload

Environment:
  PRINTIFY_API_KEY: ${CONFIG.apiKey ? '✓ Set' : '✗ Not set'}
  PRINTIFY_SHOP_ID: ${CONFIG.shopId || 'auto-detect'}

Status:
  Run 'status' to verify connection
      `);
  }
}

module.exports = { checkStatus, runAutomation };

if (require.main === module) {
  main().catch(err => {
    console.error('Fatal error:', err.message);
    process.exit(1);
  });
}
