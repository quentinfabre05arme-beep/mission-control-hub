// pod_design_factory.js - Generate vector designs for POD
// Creates SVG files optimized for print quality

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  outputDir: 'C:\\Users\\quent\\.openclaw\workspace\\pod_business\\designs',
  templatesDir: 'C:\\Users\\quent\\.openclaw\workspace\\pod_business\\templates',
  printSpecs: {
    dpi: 300,
    tshirt: { width: 4500, height: 5400 }, // 15x18 inches at 300dpi
    mug: { width: 2700, height: 1125 },    // 9x3.75 inches
    poster: { width: 4500, height: 5400 },
    sticker: { width: 1500, height: 1500 }
  }
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true }).catch(() => {});
}

async function log(msg) {
  console.log(`[POD-DESIGN] ${msg}`);
}

// SVG Template Library
const SVG_TEMPLATES = {
  // Minimal text design
  minimalText: (config) => `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${config.colors[0]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:${config.colors[1]};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="4500" height="5400" fill="url(#bg)" />
  <text x="2250" y="2400" font-family="${config.fonts[0]}, sans-serif" font-size="200" 
        fill="white" text-anchor="middle" font-weight="bold">${config.text}</text>
  <text x="2250" y="2700" font-family="${config.fonts[1]}, sans-serif" font-size="100" 
        fill="white" text-anchor="middle">${config.subtext}</text>
</svg>`,

  // Bold typography
  boldText: (config) => `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <rect width="4500" height="5400" fill="${config.colors[1]}" />
  <text x="2250" y="2200" font-family="Impact, sans-serif" font-size="300" 
        fill="${config.colors[0]}" text-anchor="middle" font-weight="bold"
        transform="rotate(-5, 2250, 2200)">${config.text}</text>
  <rect x="1500" y="2400" width="1500" height="15" fill="${config.colors[0]}" />
  <text x="2250" y="2700" font-family="Arial, sans-serif" font-size="80" 
        fill="${config.colors[2]}" text-anchor="middle">${config.subtext}</text>
</svg>`,

  // Code/developer theme
  codeTheme: (config) => `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse">
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#1a1a2e" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="4500" height="5400" fill="#0f0f23" />
  <rect width="4500" height="5400" fill="url(#grid)" />
  <!-- Code brackets -->
  <text x="800" y="2600" font-family="Fira Code, monospace" font-size="200" 
        fill="#4CAF50" text-anchor="middle"></></text>
  <text x="3700" y="2600" font-family="Fira Code, monospace" font-size="200" 
        fill="#4CAF50" text-anchor="middle">/></text>
  <text x="2250" y="2600" font-family="${config.fonts[0]}, monospace" font-size="150" 
        fill="#00ff00" text-anchor="middle" font-weight="bold">${config.text}</text>
  <text x="2250" y="2900" font-family="Fira Code, monospace" font-size="60" 
        fill="#666" text-anchor="middle">// ${config.subtext}</text>
</svg>`,

  // Retro/vintage
  vintageTheme: (config) => `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="distress">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="10"/>
    </filter>
  </defs>
  <rect width="4500" height="5400" fill="#f5f1e8" />
  <circle cx="2250" cy="2000" r="800" fill="none" stroke="${config.colors[0]}" stroke-width="20"/>
  <circle cx="2250" cy="2000" r="750" fill="none" stroke="${config.colors[1]}" stroke-width="10"/>
  <text x="2250" y="1950" font-family="Rye, serif" font-size="180" 
        fill="${config.colors[0]}" text-anchor="middle" font-weight="bold"
        filter="url(#distress)">${config.text}</text>
  <text x="2250" y="2850" font-family="Special Elite, serif" font-size="70" 
        fill="${config.colors[2]}" text-anchor="middle">EST. ${config.subtext}</text>
</svg>`,

  // Abstract geometric
  geometric: (config) => `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <rect width="4500" height="5400" fill="${config.colors[0]}" />
  <!-- Geometric shapes -->
  <polygon points="2250,1200 1200,2800 3300,2800" fill="${config.colors[1]}" opacity="0.8"/>
  <circle cx="1500" cy="3500" r="400" fill="${config.colors[2]}" opacity="0.6"/>
  <rect x="2700" y="3100" width="600" height="600" fill="${config.colors[3]}" opacity="0.7" transform="rotate(45, 3000, 3400)"/>
  <text x="2250" y="4200" font-family="${config.fonts[0]}, sans-serif" font-size="200" 
        fill="white" text-anchor="middle" font-weight="bold">${config.text}</text>
  <text x="2250" y="4500" font-family="${config.fonts[1]}, sans-serif" font-size="80" 
        fill="white" text-anchor="middle" opacity="0.8">${config.subtext}</text>
</svg>`
};

// Generate a complete design from concept
async function generateDesign(concept, trend) {
  log(`Generating design for "${concept.text}" (${concept.type})`);
  
  const timestamp = Date.now();
  const designId = `design_${trend.category}_${timestamp}`;
  
  const config = {
    text: concept.text.toUpperCase(),
    subtext: concept.subtext || trend.keyword,
    colors: concept.colors,
    fonts: concept.fonts,
    category: trend.category
  };
  
  // Select template based on concept type
  let svg;
  switch(concept.style) {
    case 'minimal':
      svg = SVG_TEMPLATES.minimalText(config);
      break;
    case 'bold':
      svg = SVG_TEMPLATES.boldText(config);
      break;
    case 'code_font':
      svg = SVG_TEMPLATES.codeTheme(config);
      break;
    case 'vintage':
      svg = SVG_TEMPLATES.vintageTheme(config);
      break;
    default:
      svg = SVG_TEMPLATES.geometric(config);
  }
  
  // Save SVG
  const filename = `${designId}.svg`;
  const filepath = path.join(CONFIG.outputDir, filename);
  
  await ensureDir(CONFIG.outputDir);
  await fs.writeFile(filepath, svg);
  
  const design = {
    id: designId,
    filename: filename,
    filepath: filepath,
    trendId: trend.id,
    concept: concept,
    metadata: {
      created: new Date().toISOString(),
      dimensions: CONFIG.printSpecs.tshirt,
      dpi: CONFIG.printSpecs.dpi,
      formats: ['svg'],
      colors: config.colors,
      tags: [trend.category, trend.keyword, concept.style, concept.type]
    },
    status: 'ready_for_mockup',
    platforms: {
      printify: { status: 'pending', productId: null },
      redbubble: { status: 'pending', listingId: null },
      teespring: { status: 'pending', listingId: null }
    }
  };
  
  log(`Design saved: ${filepath}`);
  return design;
}

// Generate multiple designs from top trends
async function generateBatch(limit = 5) {
  log('=== POD Design Factory Starting ===');
  
  // Load trends
  const trendData = await fs.readFile(
    path.join('C:\\Users\\quent\\.openclaw\workspace\\pod_business', 'trends.json'),
    'utf-8'
  ).catch(() => '{"activeTrends": []}');
  
  const trends = JSON.parse(trendData).activeTrends.slice(0, limit);
  
  if (trends.length === 0) {
    log('No active trends found. Run pod_trend_engine.js first.');
    return [];
  }
  
  const designs = [];
  
  for (const trend of trends) {
    if (!trend.concepts) continue;
    
    // Generate top 2 concepts per trend
    for (const concept of trend.concepts.slice(0, 2)) {
      try {
        const design = await generateDesign(concept, trend);
        designs.push(design);
      } catch (err) {
        log(`Error generating design for "${concept.text}": ${err.message}`);
      }
    }
  }
  
  // Save designs registry
  const registryPath = path.join(CONFIG.outputDir, 'designs_registry.json');
  let registry = [];
  try {
    registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
  } catch {}
  
  registry.push(...designs);
  await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
  
  log(`Generated ${designs.length} designs`);
  log('=== POD Design Factory Complete ===');
  
  return designs;
}

// Get designs ready for mockup generation
async function getDesignsForMockup(limit = 5) {
  const registryPath = path.join(CONFIG.outputDir, 'designs_registry.json');
  try {
    const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
    return registry.filter(d => d.status === 'ready_for_mockup').slice(0, limit);
  } catch {
    return [];
  }
}

// Get designs ready for platform upload
async function getDesignsForUpload(platform, limit = 10) {
  const registryPath = path.join(CONFIG.outputDir, 'designs_registry.json');
  try {
    const registry = JSON.parse(await fs.readFile(registryPath, 'utf-8'));
    return registry.filter(d => 
      d.platforms[platform]?.status === 'pending' && 
      d.status === 'mockup_ready'
    ).slice(0, limit);
  } catch {
    return [];
  }
}

module.exports = {
  generateDesign,
  generateBatch,
  getDesignsForMockup,
  getDesignsForUpload,
  SVG_TEMPLATES
};

// Run if called directly
if (require.main === module) {
  generateBatch().catch(console.error);
}
