// pod_design_factory.js - Generate vector designs for POD
const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  outputDir: 'C:\\Users\\quent\\.openclaw\\workspace\\pod_business\\designs'
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true }).catch(() => {});
}

async function log(msg) {
  console.log(`[POD-DESIGN] ${msg}`);
}

function generateSVG(text, category) {
  const colors = {
    crypto: ['#F7931A', '#000000'],
    fitness: ['#E53935', '#212121'],
    professions: ['#1976D2', '#424242']
  };
  const palette = colors[category] || ['#333333', '#666666'];
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${palette[0]}" />
      <stop offset="100%" style="stop-color:${palette[1]}" />
    </linearGradient>
  </defs>
  <rect width="4500" height="5400" fill="url(#bg)" />
  <text x="2250" y="2400" font-family="Arial, sans-serif" font-size="200" 
        fill="white" text-anchor="middle" font-weight="bold">${text.toUpperCase()}</text>
  <text x="2250" y="2700" font-family="Arial, sans-serif" font-size="80" 
        fill="white" text-anchor="middle" opacity="0.8">Premium Design</text>
</svg>`;
}

async function generateDesign(text, category) {
  const designId = `design_${category}_${Date.now()}`;
  const svg = generateSVG(text, category);
  
  await ensureDir(CONFIG.outputDir);
  const filepath = path.join(CONFIG.outputDir, `${designId}.svg`);
  await fs.writeFile(filepath, svg);
  
  return { id: designId, text, category, filepath };
}

async function generateBatch(limit = 5) {
  log('=== Design Factory Starting ===');
  
  const designs = [];
  const concepts = [
    { text: 'BITCOIN TREASURY', category: 'crypto' },
    { text: 'GYM RAT LIFE', category: 'fitness' },
    { text: 'DEVELOPER MODE', category: 'professions' },
    { text: 'HODL STRONG', category: 'crypto' },
    { text: 'CODE \u0026 COFFEE', category: 'professions' }
  ];
  
  for (const concept of concepts.slice(0, limit)) {
    const design = await generateDesign(concept.text, concept.category);
    designs.push(design);
    log(`Created: ${design.id}`);
  }
  
  log(`Generated ${designs.length} designs`);
  return designs;
}

module.exports = { generateBatch };
if (require.main === module) generateBatch().catch(console.error);
