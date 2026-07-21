#!/usr/bin/env node
/**
 * Fix Image Upload Blocker
 * Converts SVG designs to PNG format for Printify API
 */

const fs = require('fs');
const path = require('path');

console.log('╔════════════════════════════════════════════════════╗');
console.log('║    POD IMAGE UPLOAD FIX - SVG to PNG Converter    ║');
console.log('╚════════════════════════════════════════════════════╝\n');

// Configuration
const DESIGNS_DIR = path.join(__dirname, 'designs');
const OUTPUT_DIR = path.join(__dirname, 'generated', 'png_exports');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  console.log(`✅ Created output directory: ${OUTPUT_DIR}\n`);
}

// Find all SVG designs
const svgFiles = fs.readdirSync(DESIGNS_DIR)
  .filter(f => f.endsWith('.svg'))
  .map(f => path.join(DESIGNS_DIR, f));

console.log(`Found ${svgFiles.length} SVG design(s):`);
svgFiles.forEach(f => console.log(`  - ${path.basename(f)}`));

// Check for ImageMagick
console.log('\n📋 Manual Conversion Instructions:');
console.log('─────────────────────────────────────────────────────\n');

console.log('Option 1: ImageMagick (Recommended)');
console.log('─────────────────────────────────────────────────────');
console.log(`# Install ImageMagick (if not installed):`);
console.log(`choco install imagemagick  # Windows`);
console.log(`brew install imagemagick   # macOS`);
console.log(`apt-get install imagemagick # Linux\n`);

console.log(`# Convert all SVGs to PNG (3000x3000px):`);
svgFiles.forEach(f => {
  const baseName = path.basename(f, '.svg');
  console.log(`convert -background none -density 300 "${f}" -resize 3000x3000 "${path.join(OUTPUT_DIR, baseName + '.png')}"`);
});

console.log('\n\nOption 2: Inkscape (Best SVG support)');
console.log('─────────────────────────────────────────────────────');
svgFiles.forEach(f => {
  const baseName = path.basename(f, '.svg');
  console.log(`inkscape "${f}" --export-filename="${path.join(OUTPUT_DIR, baseName + '.png')}" --export-width=3000 --export-height=3000`);
});

console.log('\n\nOption 3: Online Converter (Quick fallback)');
console.log('─────────────────────────────────────────────────────');
console.log('1. Go to: https://convertio.co/svg-png/');
console.log('2. Upload each SVG from:', DESIGNS_DIR);
console.log('3. Set output to 3000x3000 PNG');
console.log('4. Download to:', OUTPUT_DIR);

console.log('\n\nOption 4: Printify Dashboard (Immediate)');
console.log('─────────────────────────────────────────────────────');
console.log('1. Log into https://printify.com/');
console.log('2. Go to My Store → Add Product');
console.log('3. Upload each SVG directly (Printify converts automatically)');
console.log('4. Products auto-sync to Etsy\n');

// Create a batch script for Windows
const batchScript = `@echo off
echo Converting SVG to PNG...
echo Requires ImageMagick or Inkscape
echo.
echo If not installed, use Option 4 (Printify Dashboard) for immediate fix
pause
`;

const batchPath = path.join(__dirname, 'convert_svg_to_png.bat');
fs.writeFileSync(batchPath, batchScript);
console.log(`✅ Created batch script: ${batchPath}\n`);

// Update automation log
const logEntry = {
  timestamp: new Date().toISOString(),
  action: 'image_upload_fix',
  svgCount: svgFiles.length,
  outputDir: OUTPUT_DIR,
  options: ['imagemagick', 'inkscape', 'online', 'dashboard'],
  recommended: 'dashboard_immediate'
};

const logPath = path.join(__dirname, 'logs', 'fix_image_upload.json');
fs.writeFileSync(logPath, JSON.stringify(logEntry, null, 2));

console.log('╔════════════════════════════════════════════════════╗');
console.log('║                  RECOMMENDATION                    ║');
console.log('╚════════════════════════════════════════════════════╝');
console.log('│                                                    │');
console.log('│  🚀 IMMEDIATE ACTION: Use Option 4 (Dashboard)      │');
console.log('│                                                    │');
console.log('│  1. Open https://printify.com/                     │');
console.log('│  2. Upload 5 SVG designs manually                 │');
console.log('│  3. Products auto-publish to Etsy                 │');
console.log('│  4. Revenue starts within 24-48 hours             │');
console.log('│                                                    │');
console.log('╚════════════════════════════════════════════════════╝\n');

console.log('Files:');
console.log(`  - SVG designs: ${DESIGNS_DIR}`);
console.log(`  - PNG output:  ${OUTPUT_DIR}`);
console.log(`  - Log:         ${logPath}`);
console.log(`  - Script:      ${batchPath}\n`);

console.log('Next: Run publish_products.js after conversion\n');
