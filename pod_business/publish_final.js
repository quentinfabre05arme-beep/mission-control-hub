const https = require('https');
const fs = require('fs');
const path = require('path');

const envContent = fs.readFileSync('.env', 'utf8');
const tokenMatch = envContent.match(/PRINTIFY_API_KEY=(.+)/);
const TOKEN = tokenMatch ? tokenMatch[1].trim() : null;
const SHOP_ID = 28241288;

const DESIGNS = [
  { id: 'design_crypto_1784049410601', title: 'Bitcoin Treasury', price: 29.99 },
  { id: 'design_crypto_1784049410607', title: 'HODL Strong', price: 29.99 },
  { id: 'design_fitness_1784049410604', title: 'Fitness Motivation', price: 27.99 },
  { id: 'design_professions_1784049410606', title: 'Professional Pride', price: 27.99 },
  { id: 'design_professions_1784049410609', title: 'Work Hard', price: 27.99 }
];

function apiRequest(path, method = 'GET', postData = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.printify.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => reject(new Error('Timeout')));
    if (postData) req.write(JSON.stringify(postData));
    req.end();
  });
}

async function main() {
  console.log('🚀 Printify → Etsy Publisher\n');
  
  // Get blueprints
  const bpResult = await apiRequest('/v1/catalog/blueprints.json');
  const blueprints = Array.isArray(bpResult.data) ? bpResult.data : [];
  const tshirt = blueprints.find(b => 
    b.title && b.title.toLowerCase().includes('unisex') && 
    b.title.toLowerCase().includes('t-shirt')
  );
  
  if (!tshirt) {
    console.error('❌ No t-shirt found');
    process.exit(1);
  }
  
  console.log(`🎯 Blueprint: ${tshirt.title} (ID: ${tshirt.id})`);
  
  // Get print providers
  const ppResult = await apiRequest(`/v1/catalog/blueprints/${tshirt.id}/print_providers.json`);
  const printProviders = ppResult.data || [];
  
  if (printProviders.length === 0) {
    console.error('❌ No print providers');
    process.exit(1);
  }
  
  const provider = printProviders[0];
  console.log(`🏭 Provider: ${provider.title} (ID: ${provider.id})`);
  
  // Get variants
  const varResult = await apiRequest(`/v1/catalog/blueprints/${tshirt.id}/print_providers/${provider.id}/variants.json`);
  const allVariants = varResult.data?.variants || [];
  
  // Filter for Black color and standard sizes (S, M, L, XL)
  const blackVariants = allVariants.filter(v => 
    v.options?.color?.toLowerCase() === 'black' && 
    ['S', 'M', 'L', 'XL'].includes(v.options?.size)
  );
  
  console.log(`📐 Variants: ${blackVariants.length} (Black, S-XL)\n`);
  
  if (blackVariants.length === 0) {
    console.error('❌ No suitable variants found');
    process.exit(1);
  }
  
  const results = [];
  
  for (const design of DESIGNS) {
    console.log(`🎨 ${design.title}`);
    
    // Upload image
    const pngPath = path.join(__dirname, 'designs', `${design.id}.png`);
    const imageBuffer = fs.readFileSync(pngPath);
    
    console.log(`   📤 Uploading...`);
    const uploadResult = await apiRequest('/v1/uploads/images.json', 'POST', {
      file_name: `${design.id}.png`,
      contents: imageBuffer.toString('base64')
    });
    
    if (uploadResult.status !== 200 || !uploadResult.data.id) {
      console.log(`   ❌ Upload failed`);
      continue;
    }
    
    const imageId = uploadResult.data.id;
    console.log(`   ✅ Image: ${imageId.substring(0, 16)}...`);
    
    // Create product
    const productData = {
      title: design.title,
      description: `${design.title} — Premium quality design printed on soft, comfortable fabric.`,
      blueprint_id: tshirt.id,
      print_provider_id: provider.id,
      variants: blackVariants.map(v => ({
        id: v.id,
        price: Math.round(design.price * 100),
        is_enabled: true
      })),
      print_areas: [
        {
          variant_ids: blackVariants.map(v => v.id),
          placeholders: [{
            position: 'front',
            images: [{ id: imageId, x: 0.5, y: 0.5, scale: 1.0, angle: 0 }]
          }]
        }
      ]
    };
    
    const createResult = await apiRequest(`/v1/shops/${SHOP_ID}/products.json`, 'POST', productData);
    
    if (createResult.status === 200 || createResult.status === 201) {
      const product = createResult.data;
      console.log(`   ✅ Product: ${product.id}`);
      
      // Publish to Etsy
      const pubResult = await apiRequest(`/v1/shops/${SHOP_ID}/products/${product.id}/publish.json`, 'POST', {});
      const published = pubResult.status === 200;
      console.log(`   ${published ? '✅' : '⚠️'} Etsy: ${published ? 'Published' : 'Manual publish needed'}`);
      
      results.push({ title: design.title, id: product.id, price: design.price, published });
    } else {
      console.log(`   ❌ Failed:`, JSON.stringify(createResult.data).substring(0, 250));
    }
    
    console.log('');
    await new Promise(r => setTimeout(r, 1500));
  }
  
  console.log('═══════════════════════════════════════');
  console.log('📊 PUBLISHING COMPLETE');
  console.log('═══════════════════════════════════════');
  console.log(`Products: ${results.length}/${DESIGNS.length}`);
  console.log(`Etsy Live: ${results.filter(r => r.published).length}`);
  
  if (results.length > 0) {
    console.log('\n📦 Products:');
    results.forEach((r, i) => console.log(`  ${i+1}. ${r.title} — $${r.price} ${r.published ? '✅' : '⏳'}`));
    
    fs.writeFileSync('products_live.json', JSON.stringify({ 
      timestamp: new Date().toISOString(), 
      products: results 
    }, null, 2));
    
    console.log('\n🎉 BUSINESS IS LIVE!');
    console.log('🔗 https://printify.com/app/products');
    console.log('🔗 https://quentinvestdesigns.etsy.com');
  }
}

main().catch(e => console.error('❌', e.message));
