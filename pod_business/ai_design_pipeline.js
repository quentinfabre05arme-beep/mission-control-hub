#!/usr/bin/env node
/**
 * AI Design Pipeline - Generates designs via oo + OpenAI, uploads to Printify
 * Budget: $10 (~1000 gpt-image-1 images at ~$0.01 each)
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Design prompts optimized for t-shirts
const DESIGNS = [
  {
    name: "Bitcoin Millionaire",
    prompt: "Premium minimalist t-shirt design: 'BITCOIN MILLIONAIRE' in elegant gold serif typography on solid black background. Subtle Bitcoin logo as geometric watermark. Luxury, high-end fashion aesthetic. Clean centered composition, print-ready.",
    tags: ["bitcoin", "crypto", "millionaire", "luxury"]
  },
  {
    name: "HODL Life",
    prompt: "Modern streetwear t-shirt design: 'HODL LIFE' in bold white block letters on navy blue background. Subtle candlestick chart pattern as texture. Clean, minimalist, urban style. Centered composition.",
    tags: ["hodl", "crypto", "trading", "investing"]
  },
  {
    name: "Ethereum Bull",
    prompt: "Premium t-shirt design: 'ETH BULL' in futuristic silver metallic typography on dark charcoal background. Subtle Ethereum diamond logo pattern. Tech-forward, modern aesthetic. High contrast, print-ready.",
    tags: ["ethereum", "eth", "bull", "crypto"]
  },
  {
    name: "Satoshi Vision",
    prompt: "Minimalist t-shirt design: 'SATOSHI VISION' in clean white sans-serif font on matte black background. Very subtle circuit board pattern texture. Premium understated style. Centered, balanced composition.",
    tags: ["bitcoin", "satoshi", "crypto", "minimalist"]
  },
  {
    name: "DeFi Degenerate",
    prompt: "Bold streetwear t-shirt design: 'DEFI DEGEN' in vibrant gradient purple-to-pink typography on black background. Abstract DeFi protocol icons as faint geometric pattern. Crypto-native aesthetic. Centered.",
    tags: ["defi", "degenerate", "crypto", "web3"]
  }
];

const OUTPUT_DIR = path.join(__dirname, 'generated');
const LOG_FILE = path.join(__dirname, 'logs', 'ai_pipeline.log');

// Ensure directories exist
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
if (!fs.existsSync(path.dirname(LOG_FILE))) fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });

function log(message) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${message}`;
  console.log(entry);
  fs.appendFileSync(LOG_FILE, entry + '\n');
}

function runCommand(cmd, options = {}) {
  try {
    const result = execSync(cmd, { 
      encoding: 'utf8', 
      timeout: 120000,
      ...options 
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message, output: error.stdout || '' };
  }
}

async function generateDesign(design, index) {
  log(`\n=== Generating Design ${index + 1}/${DESIGNS.length}: ${design.name} ===`);
  
  const promptFile = path.join(OUTPUT_DIR, `prompt_${index}.json`);
  const outputFile = path.join(OUTPUT_DIR, `design_${index}_output.json`);
  
  // Write prompt file
  const promptData = {
    prompt: design.prompt,
    model: "gpt-image-1"
  };
  fs.writeFileSync(promptFile, JSON.stringify(promptData, null, 2));
  log(`Prompt file created: ${promptFile}`);
  
  // Run oo connector (using cmd /c for Windows)
  const cmd = `oo connector run openai --action create_image --data "@${promptFile}" --json`;
  log(`Running: ${cmd}`);
  
  const result = runCommand(cmd);
  
  if (!result.success) {
    log(`❌ Generation failed: ${result.error}`);
    return { success: false, design: design.name, error: result.error };
  }
  
  // Save output
  fs.writeFileSync(outputFile, result.output);
  log(`✅ Output saved: ${outputFile}`);
  
  // Parse and extract image
  try {
    const data = JSON.parse(result.output);
    if (data.data && data.data[0] && data.data[0].b64_json) {
      const imagePath = path.join(OUTPUT_DIR, `design_${index}_${design.name.replace(/\s+/g, '_').toLowerCase()}.png`);
      fs.writeFileSync(imagePath, Buffer.from(data.data[0].b64_json, 'base64'));
      log(`✅ Image saved: ${imagePath}`);
      
      // Create metadata
      const metaPath = path.join(OUTPUT_DIR, `design_${index}_meta.json`);
      fs.writeFileSync(metaPath, JSON.stringify({
        name: design.name,
        prompt: design.prompt,
        tags: design.tags,
        generated: new Date().toISOString(),
        imageFile: path.basename(imagePath)
      }, null, 2));
      
      return { success: true, design: design.name, imagePath, metaPath };
    }
  } catch (e) {
    log(`⚠️ Could not extract image: ${e.message}`);
  }
  
  return { success: true, design: design.name, outputFile };
}

async function main() {
  log('╔════════════════════════════════════════════╗');
  log('║     AI DESIGN PIPELINE - Starting Run     ║');
  log('╚════════════════════════════════════════════╝');
  log(`Budget: $10 OpenAI API (~1000 images)`);
  log(`Designs to generate: ${DESIGNS.length}`);
  log(`Estimated cost: ~$0.05 (${DESIGNS.length} × $0.01)`);
  log('');
  
  const results = [];
  
  for (let i = 0; i < DESIGNS.length; i++) {
    const result = await generateDesign(DESIGNS[i], i);
    results.push(result);
    
    // Small delay between generations
    if (i < DESIGNS.length - 1) {
      log('Waiting 2s before next generation...');
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  // Summary
  log('\n╔════════════════════════════════════════════╗');
  log('║              GENERATION SUMMARY              ║');
  log('╚════════════════════════════════════════════╝');
  
  const successful = results.filter(r => r.success).length;
  const failed = results.length - successful;
  
  log(`Total: ${results.length} | ✅ Success: ${successful} | ❌ Failed: ${failed}`);
  
  results.forEach((r, i) => {
    if (r.success && r.imagePath) {
      log(`${i + 1}. ✅ ${r.design} → ${path.basename(r.imagePath)}`);
    } else if (r.success) {
      log(`${i + 1}. ⚠️ ${r.design} → Output saved but no image extracted`);
    } else {
      log(`${i + 1}. ❌ ${r.design} → ${r.error}`);
    }
  });
  
  log(`\n📁 Output directory: ${OUTPUT_DIR}`);
  log(`📝 Log file: ${LOG_FILE}`);
  
  // Next steps
  log('\n═══════════════════════════════════════════════');
  log('NEXT STEPS:');
  log('1. Review generated images in: pod_business/generated/');
  log('2. Run: node upload_to_printify.js');
  log('3. Run: node publish_to_etsy.js');
  log('═══════════════════════════════════════════════');
}

main().catch(err => {
  log(`FATAL ERROR: ${err.message}`);
  process.exit(1);
});
