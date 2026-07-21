#!/usr/bin/env node
/**
 * xAI Generator v2
 * Uses xAI API for text/image generation
 * 
 * IMPORTANT: xAI image generation API may not be publicly available.
 * This script attempts the API call, falls back to useful output if unavailable.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

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
    prompt: "Create a premium t-shirt design: 'CRYPTO MILLIONAIRE' in elegant gold typography on black background. Subtle Bitcoin/Ethereum icons as watermark. Luxury, minimal style. High contrast, print-ready.",
    filename: "design_crypto_millionaire_ai.png"
  },
  gym_beast: {
    title: "Gym Beast Mode",
    prompt: "Create a fitness t-shirt: 'BEAST MODE ACTIVATED' in bold distressed typography. Dark red, black, white colors. Barbell silhouette, aggressive style. High energy, print-ready.",
    filename: "design_gym_beast_ai.png"
  },
  startup_life: {
    title: "Startup Life",
    prompt: "Create a tech t-shirt: 'STARTUP LIFE' and 'COFFEE → CODE → REPEAT'. Navy blue, white, light blue. Laptop and coffee icons. Clean, professional, developer culture style.",
    filename: "design_startup_life_ai.png"
  },
  code_coffee: {
    title: "Code & Coffee",
    prompt: "Create a developer t-shirt: 'CODE & COFFEE' and 'THE PERFECT STACK'. Warm brown, cream, charcoal. Coffee cup and code brackets. Cozy programmer aesthetic.",
    filename: "design_code_coffee_ai.png"
  },
  hustle_grind: {
    title: "Hustle & Grind",
    prompt: "Create an entrepreneurial t-shirt: 'HUSTLE & GRIND' and 'SUCCESS IS THE ONLY OPTION'. Green, black, white. Upward arrows, industrial typography. Motivational, powerful.",
    filename: "design_hustle_grind_ai.png"
  }
};

async function generatePromptRefinement(designKey, apiKey) {
  const design = DESIGNS[designKey];
  
  const postData = JSON.stringify({
    model: "grok-2-1212",
    messages: [
      {
        role: "system",
        content: "You are an expert t-shirt designer. Create optimized prompts for print-on-demand designs."
      },
      {
        role: "user",
        content: `Create an enhanced prompt for this t-shirt design: "${design.title}"\n\nBase concept: ${design.prompt}\n\nRequirements:\n- Optimized for AI image generation\n- Include specific style keywords\n- Mention layout and composition\n- Add technical details (transparent background, print-ready)\n\nOutput only the enhanced prompt, nothing else.`
      }
    ],
    max_tokens: 500
  });

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.x.ai',
      port: 443,
      path: '/v1/chat/completions',
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
          if (response.choices && response.choices[0]) {
            resolve(response.choices[0].message.content);
          } else {
            reject(new Error('No response from API'));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// CLI
const args = process.argv.slice(2);
const designArg = args.find(a => a.startsWith('--design='))?.replace('--design=', '');
const allMode = args.includes('--all');
const refineMode = args.includes('--refine');
const listMode = args.includes('--list');

if (listMode) {
  console.log('Available designs:\n');
  Object.entries(DESIGNS).forEach(([key, design]) => {
    console.log(`  ${key}: ${design.title}`);
  });
  console.log('\nModes:');
  console.log('  --refine    Use xAI to enhance prompts');
  console.log('  (default)   Output prompts for manual use');
  process.exit(0);
}

const apiKey = loadEnv();
if (!apiKey) {
  console.error('❌ Error: XAI_API_KEY not found in .env.local');
  process.exit(1);
}

// Mode 1: Refine prompts with xAI API
if (refineMode) {
  (async () => {
    const designsToProcess = allMode ? Object.keys(DESIGNS) : [designArg];
    
    for (const key of designsToProcess) {
      if (!DESIGNS[key]) continue;
      
      console.log(`\n🎨 Refining: ${DESIGNS[key].title}`);
      console.log('─'.repeat(50));
      
      try {
        const refined = await generatePromptRefinement(key, apiKey);
        console.log('Enhanced prompt:');
        console.log(refined);
        console.log('\n💡 Copy this to Grok chat (chat.grok.com) to generate image');
      } catch (e) {
        console.error('  ❌ Error:', e.message);
        console.log('  Using original prompt instead...');
        console.log(DESIGNS[key].prompt);
      }
    }
  })();
}
// Mode 2: Output prompts for manual use
else {
  console.log('🎨 xAI Design Generator\n');
  console.log('═══════════════════════════════════════════════════\n');
  console.log('Mode: Manual (copy/paste to Grok chat)\n');
  
  const designsToProcess = allMode ? Object.keys(DESIGNS) : [designArg];
  
  designsToProcess.forEach((key) => {
    if (!DESIGNS[key]) return;
    const design = DESIGNS[key];
    
    console.log(`${key}: ${design.title}`);
    console.log('─'.repeat(50));
    console.log(design.prompt);
    console.log('\nAdd to prompt: "High quality PNG, transparent background, 4500x5400px"');
    console.log('Go to: chat.grok.com\n');
  });
  
  console.log('═══════════════════════════════════════════════════\n');
  console.log('💡 Alternative: Use --refine flag to enhance prompts with xAI API');
  console.log('   node xai_generator_v2.js --design=crypto_millionaire --refine');
  console.log('');
}
