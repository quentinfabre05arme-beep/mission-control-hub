/**
 * SVG to PNG Converter using Node.js only (no external dependencies)
 * Uses sharp library for conversion
 */

const fs = require('fs');
const path = require('path');

// Check if sharp is available
try {
  const sharp = require('sharp');
  
  async function convertSVG(svgFile) {
    const inputPath = path.join(__dirname, 'designs', svgFile);
    const outputPath = path.join(__dirname, 'designs', svgFile.replace('.svg', '.png'));
    
    console.log(`Converting ${svgFile}...`);
    
    await sharp(inputPath)
      .resize(3000, 3600, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
      .png()
      .toFile(outputPath);
    
    console.log(`  ✅ Created: ${path.basename(outputPath)}`);
    return outputPath;
  }
  
  async function main() {
    const designsDir = path.join(__dirname, 'designs');
    const files = fs.readdirSync(designsDir).filter(f => f.endsWith('.svg'));
    
    console.log(`Found ${files.length} SVG files to convert\n`);
    
    for (const file of files) {
      await convertSVG(file);
    }
    
    console.log('\n✅ All conversions complete!');
  }
  
  main().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
  
} catch (e) {
  console.log('sharp not installed. Installing...');
  const { exec } = require('child_process');
  exec('npm install sharp', { cwd: __dirname }, (error, stdout, stderr) => {
    if (error) {
      console.error('Failed to install sharp:', error);
      process.exit(1);
    }
    console.log('sharp installed. Please run this script again.');
  });
}
