/**
 * SVG Design Generator
 * Creates new designs automatically
 */

const fs = require('fs');

const DESIGN_TEMPLATES = [
  {
    id: 'design_crypto_millionaire',
    title: 'Crypto Millionaire',
    text1: 'CRYPTO MILLIONAIRE',
    text2: 'Loading... 99%',
    colors: ['#F7931A', '#FFD700'],
    category: 'crypto'
  },
  {
    id: 'design_gym_beast',
    title: 'Gym Beast Mode',
    text1: 'BEAST MODE',
    text2: 'Activated',
    colors: ['#E53935', '#212121'],
    category: 'fitness'
  },
  {
    id: 'design_startup_life',
    title: 'Startup Life',
    text1: 'STARTUP LIFE',
    text2: 'Coffee → Code → Repeat',
    colors: ['#1976D2', '#424242'],
    category: 'career'
  },
  {
    id: 'design_code_coffee',
    title: 'Code & Coffee',
    text1: 'CODE & COFFEE',
    text2: 'The Perfect Stack',
    colors: ['#6F4E37', '#212121'],
    category: 'tech'
  },
  {
    id: 'design_hustle_grind',
    title: 'Hustle & Grind',
    text1: 'HUSTLE & GRIND',
    text2: 'Success is the only option',
    colors: ['#388E3C', '#1B5E20'],
    category: 'motivation'
  }
];

function generateSVG(template) {
  const [c1, c2] = template.colors;
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="4500" height="5400" viewBox="0 0 4500 5400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${c1}" />
      <stop offset="100%" style="stop-color:${c2}" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="4500" height="5400" fill="url(#bg)" />
  <rect x="100" y="100" width="4300" height="5200" fill="none" stroke="white" stroke-width="20" opacity="0.3" rx="50" />
  <text x="2250" y="2200" font-family="Arial Black, sans-serif" font-size="280" 
        fill="white" text-anchor="middle" font-weight="bold" filter="url(#glow)">${template.text1}</text>
  <text x="2250" y="2700" font-family="Arial, sans-serif" font-size="100" 
        fill="white" text-anchor="middle" opacity="0.9">${template.text2}</text>
  <text x="2250" y="5000" font-family="Arial, sans-serif" font-size="60" 
        fill="white" text-anchor="middle" opacity="0.6">Premium Design</text>
</svg>`;
}

function main() {
  console.log('🎨 Creating New Designs...\n');
  
  DESIGN_TEMPLATES.forEach(template => {
    const svg = generateSVG(template);
    const filename = `${template.id}.svg`;
    fs.writeFileSync(`designs/${filename}`, svg);
    console.log(`✅ Created: ${filename}`);
    console.log(`   Title: ${template.title}`);
    console.log(`   Category: ${template.category}`);
    console.log('');
  });
  
  console.log('🚀 Ready to publish! Run: node publish_working.js');
}

main();
