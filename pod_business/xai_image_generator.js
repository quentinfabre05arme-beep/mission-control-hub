#!/usr/bin/env node
/**
 * xAI Image Generator
 * Uses xAI API to generate POD designs
 * 
 * Usage:
 *   node xai_image_generator.js --design="crypto_millionaire"
 *   node xai_image_generator.js --design="gym_beast"
 *   node xai_image_generator.js --list
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load API key from .env
function loadEnv() {
  const envPath = path.join(__dirname, '.env.local');
  if (fs.existsSync(envPath)) {
    const env = fs.readFileSync(envPath, 'utf8');
    const match = env.match(/XAI_API_KEY=(.+)/);
    return match ? match[1].trim() : null;
  }
  return process.env.XAI_API_KEY;
}

const DESIGNS = {
  crypto_millionaire: {
    title: "Crypto Millionaire",
    prompt: `Create a premium t-shirt design with "CRYPTO MILLIONAIRE" text in elegant, bold typography. 
Style: Luxury, minimal, modern.
Elements: Subtle Bitcoin and Ethereum coin icons as background watermark.
Colors: Black background with gold and white text.
Mood: Premium, wealthy, exclusive.
Layout: Centered text, clean composition.
Format: High quality, print-ready, transparent background preferred.`,
    filename: "design_crypto_millionaire_ai.png"
  },
  gym_beast: {
    title: "Gym Beast Mode",
    prompt: `Create an aggressive fitness t-shirt design with "BEAST MODE ACTIVATED" text.
Style: Bold, blocky typography with distressed/grunge texture.
Elements: Barbell silhouette, muscle fiber patterns.
Colors: Dark red, black, white.
Mood: Powerful, intense, motivational.
Layout: Centered, strong visual impact.
Format: High quality, print-ready.`,
    filename: "design_gym_beast_ai.png"
  },
  startup_life: {
    title: "Startup Life",
    prompt: `Create a tech startup t-shirt design with "STARTUP LIFE" and "COFFEE → CODE → REPEAT" tagline.
Style: Modern sans-serif, clean, professional.
Elements: Subtle laptop, coffee cup, code bracket icons.
Colors: Navy blue, white, light blue accents.
Mood: Professional, tech culture, developer lifestyle.
Layout: Clean hierarchy, balanced composition.
Format: High quality, print-ready.`,
    filename: "design_startup_life_ai.png"
  },
  code_coffee: {
    title: "Code & Coffee",
    prompt: `Create a developer lifestyle t-shirt with "CODE & COFFEE" and "THE PERFECT STACK" text.
Style: Elegant, cozy, programmer aesthetic.
Elements: Coffee cup, code brackets, terminal symbols.
Colors: Warm brown, cream, charcoal gray.
Mood: Comfortable, relatable, developer culture.
Layout: Centered, inviting composition.
Format: High quality, print-ready.`,
    filename: "design_code_coffee_ai.png"
  },
  hustle_grind: {
    title: "Hustle & Grind",
    prompt: `Create an entrepreneurial t-shirt with "HUSTLE & GRIND" and "SUCCESS IS THE ONLY OPTION" text.
Style: Industrial, bold, motivational.
Elements: Subtle upward arrows, mountain peaks, success symbols.
Colors: Green, black, white.
Mood: Driven, ambitious, success-oriented.
Layout: Strong hierarchy, powerful impact.
Format: High quality, print-ready.`,
    filename: "design_hustle_grind_ai.png"
  }
};

async function generateImage(prompt, apiKey, outputPath) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model: "grok-2-image-1212",
      prompt: prompt,
      n: 1,
      size: "1024x1024",  // xAI supports this size
      response_format: "url"
    });

    const options = {
      hostname: 'api.x.ai',
      port: 443,
      path: '/v1/images/generations',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.data && response.data[0]) {
            const imageUrl = response.data[0].url;
            downloadImage(imageUrl, outputPath)
              .then(() => resolve(outputPath))
              .catch(reject);
          } else {
            reject(new Error('No image URL in response: ' + JSON.stringify(response)));
          }
        } catch (e) {
          reject(new Error('Parse error: ' + e.message + '\nData: ' + data));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function downloadImage(url, outputPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath);
    https.get(url, (response) => {
      if (response.statusCode === 302 || response.statusCode === 301) {
        // Follow redirect
        https.get(response.headers.location, (res) => {
          res.pipe(file);
          file.on('finish', () => {
            file.close();
            resolve();
          });
        }).on('error', reject);
      } else {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          resolve();
        });
      }
    }).on('error', reject);
  });
}

// CLI
const args = process.argv.slice(2);
const designArg = args.find(a => a.startsWith('--design='))?.replace('--design=', '');
const listMode = args.includes('--list');
const allMode = args.includes('--all');

if (listMode) {
  console.log('Available designs:\n');
  Object.entries(DESIGNS).forEach(([key, design]) => {
    console.log(`  ${key}: ${design.title}`);
  });
  process.exit(0);
}

const apiKey = loadEnv();
if (!apiKey) {
  console.error('❌ Error: XAI_API_KEY not found');
  console.error('Add to pod_business/.env.local: XAI_API_KEY=your_key_here');
  process.exit(1);
}

if (allMode) {
  console.log('🎨 Generating all 5 designs...\n');
  
  (async () => {
    for (const [key, design] of Object.entries(DESIGNS)) {
      const outputPath = path.join(__dirname, 'designs', design.filename);
      console.log(`Generating: ${design.title}...`);
      try {
        await generateImage(design.prompt, apiKey, outputPath);
        console.log(`  ✅ Saved: ${design.filename}`);
      } catch (e) {
        console.error(`  ❌ Failed: ${e.message}`);
      }
    }
    console.log('\n🚀 Done! Run: node publish_working.js to upload to Printify');
  })();
} else if (designArg && DESIGNS[designArg]) {
  const design = DESIGNS[designArg];
  const outputPath = path.join(__dirname, 'designs', design.filename);
  
  console.log(`🎨 Generating: ${design.title}\n`);
  console.log('Prompt:', design.prompt.substring(0, 100) + '...\n');
  
  generateImage(design.prompt, apiKey, outputPath)
    .then(() => {
      console.log(`✅ Saved: ${outputPath}`);
      console.log('\n🚀 Next: node publish_working.js to upload to Printify');
    })
    .catch(err => {
      console.error('❌ Error:', err.message);
    });
} else {
  console.log('xAI Image Generator\n');
  console.log('Usage:');
  console.log('  node xai_image_generator.js --list');
  console.log('  node xai_image_generator.js --design=crypto_millionaire');
  console.log('  node xai_image_generator.js --all');
  console.log('\nAvailable designs:');
  Object.keys(DESIGNS).forEach(k => console.log(`  - ${k}`));
}
