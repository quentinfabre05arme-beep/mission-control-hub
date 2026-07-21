#!/usr/bin/env node
/**
 * Simple Pinterest Automation - Login and Create Pin
 * Uses fresh Chrome profile with manual login
 */

const puppeteer = require('puppeteer');
const path = require('path');

const EMAIL = 'quentin.fabre05arme@gmail.com';
const PASSWORD = '2025!Narguess!2025';

const DESIGN = {
  imagePath: path.join(__dirname, 'generated', 'design_1_bitcoin_millionaire.png'),
  title: 'Bitcoin Millionaire Tee | Crypto Investor Gift | Premium Crypto Merch',
  description: `🔥 Bitcoin Millionaire Tee 🔥

The perfect gift for crypto investors, Bitcoin believers, and HODLers.

✨ Premium Features:
• Softstyle unisex fit
• High-quality DTG print
• Bitcoin-inspired luxury design
• Gold typography on black

🎁 Great for:
• Bitcoin investors
• Crypto enthusiasts  
• Stock market traders
• Gift for him/her

🚀 Join the crypto revolution in style!

🔗 Shop now: https://www.etsy.com/shop/QuentinvestDesigns

#bitcoin #crypto #hodl #investor #gift #cryptocurrency #blockchain #millionaire #btc #cryptomillionaire #cryptomerch #bitcoinshirt`,
  link: 'https://www.etsy.com/shop/QuentinvestDesigns',
  board: 'Crypto Tees'
};

async function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  console.log('🚀 Starting Pinterest Automation...\n');
  
  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1280,900'],
    defaultViewport: { width: 1280, height: 900 }
  });
  
  const page = await browser.newPage();
  
  try {
    // Login
    console.log('🔐 Navigating to Pinterest login...');
    await page.goto('https://www.pinterest.com/login/', { waitUntil: 'networkidle2', timeout: 60000 });
    await delay(3000);
    
    console.log('📧 Entering email...');
    await page.type('input[id="email"]', EMAIL, { delay: 50 });
    
    console.log('🔑 Entering password...');
    await page.type('input[id="password"]', PASSWORD, { delay: 50 });
    
    console.log('🖱️ Clicking login...');
    await page.click('button[type="submit"]');
    
    console.log('⏳ Waiting for login...');
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {});
    await delay(5000);
    
    const url = page.url();
    console.log(`📍 Current URL: ${url}`);
    
    if (url.includes('login') || url.includes('challenge')) {
      console.log('⚠️  2FA or verification needed! Check browser.');
      console.log('⏳ Waiting 60 seconds for manual verification...');
      await delay(60000);
    }
    
    // Go to pin builder
    console.log('\n📌 Opening Pin Builder...');
    await page.goto('https://www.pinterest.com/pin-builder/', { waitUntil: 'networkidle2', timeout: 60000 });
    await delay(3000);
    
    // Upload image
    console.log('📤 Uploading image...');
    const fileInput = await page.$('input[type="file"]');
    if (!fileInput) {
      console.log('❌ File upload not found');
      return;
    }
    
    await fileInput.uploadFile(DESIGN.imagePath);
    console.log('✓ Image uploaded');
    await delay(5000);
    
    // Fill title
    console.log('📝 Adding title...');
    const titleArea = await page.$('textarea[placeholder*="title"], input[placeholder*="title"]');
    if (titleArea) await titleArea.type(DESIGN.title, { delay: 30 });
    
    // Fill description
    console.log('📝 Adding description...');
    const descArea = await page.$('textarea[placeholder*="description"], textarea[placeholder*="about"]');
    if (descArea) await descArea.type(DESIGN.description, { delay: 10 });
    
    // Fill link
    console.log('🔗 Adding link...');
    const linkInput = await page.$('input[placeholder*="link"], input[placeholder*="destination"]');
    if (linkInput) await linkInput.type(DESIGN.link, { delay: 30 });
    
    await delay(1000);
    
    // Save
    console.log('💾 Saving pin...');
    const saveBtn = await page.$('[data-test-id="pin-builder-save"], button:has-text("Save")');
    if (saveBtn) {
      await saveBtn.click();
      console.log('✓ Save clicked');
    }
    
    await delay(5000);
    console.log('\n✅ PIN CREATED!');
    console.log('🛑 Browser will stay open for 30 seconds...');
    await delay(30000);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
    console.log('🛑 Browser closed');
  }
}

run().catch(console.error);
