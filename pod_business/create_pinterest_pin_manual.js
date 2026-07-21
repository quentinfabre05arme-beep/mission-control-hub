#!/usr/bin/env node
/**
 * Manual Pinterest Pin Creator
 * Run this when Chrome is CLOSED (not running)
 * It will use your existing Chrome profile where Pinterest is already logged in
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const DESIGN = {
  name: 'Bitcoin Millionaire',
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

function getChromePaths() {
  return {
    userDataDir: path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data'),
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  };
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function createPin() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║   Pinterest Pin Creator - Manual Mode      ║');
  console.log('╚════════════════════════════════════════════╝');
  console.log('');
  console.log('⚠️  IMPORTANT: Make sure Chrome is CLOSED before running!');
  console.log('');
  
  const { userDataDir, executablePath } = getChromePaths();
  
  console.log('🚀 Launching Chrome with your profile...');
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false, // Visible so you can see what's happening
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        `--user-data-dir=${userDataDir}`,
        '--profile-directory=Default'
      ],
      executablePath: executablePath,
      defaultViewport: { width: 1280, height: 900 }
    });
  } catch (err) {
    if (err.message.includes('already running')) {
      console.log('');
      console.log('❌ ERROR: Chrome is already running!');
      console.log('');
      console.log('To fix this:');
      console.log('1. Close all Chrome windows');
      console.log('2. Check Task Manager for "chrome.exe" processes');
      console.log('3. Kill all Chrome processes');
      console.log('4. Run this script again');
      console.log('');
      console.log('Or use the alternative:');
      console.log('- Open Pinterest manually in Chrome');
      console.log('- Go to https://www.pinterest.com/pin-builder/');
      console.log('- Upload the image manually');
      return;
    }
    throw err;
  }
  
  const page = await browser.newPage();
  
  try {
    // Step 1: Go to Pinterest
    console.log('📍 Opening Pinterest...');
    await page.goto('https://www.pinterest.com/', { waitUntil: 'networkidle2', timeout: 60000 });
    await delay(3000);
    
    const currentUrl = page.url();
    console.log(`📍 Current page: ${currentUrl}`);
    
    // Step 2: Go to Pin Builder
    console.log('📌 Opening Pin Builder...');
    await page.goto('https://www.pinterest.com/pin-builder/', { waitUntil: 'networkidle2', timeout: 60000 });
    await delay(3000);
    
    await page.screenshot({ path: 'logs/pin_builder_start.png' });
    
    // Step 3: Upload image
    console.log('📤 Uploading image...');
    const fileInput = await page.$('input[type="file"]');
    
    if (!fileInput) {
      console.log('⚠️  Could not find file upload. Taking screenshot...');
      await page.screenshot({ path: 'logs/pin_builder_no_upload.png' });
      console.log('❌ Stopping - check screenshot');
      return;
    }
    
    await fileInput.uploadFile(DESIGN.imagePath);
    console.log('✓ Image selected');
    
    await delay(5000); // Wait for upload
    await page.screenshot({ path: 'logs/pin_builder_uploaded.png' });
    
    // Step 4: Add title
    console.log('📝 Adding title...');
    const titleSelectors = [
      'textarea[placeholder*="title"]',
      'input[placeholder*="title"]',
      '[data-test-id="pin-title-input"]'
    ];
    
    for (const selector of titleSelectors) {
      const titleField = await page.$(selector);
      if (titleField) {
        await titleField.type(DESIGN.title, { delay: 30 });
        console.log('✓ Title added');
        break;
      }
    }
    
    // Step 5: Add description
    console.log('📝 Adding description...');
    const descSelectors = [
      'textarea[placeholder*="description"]',
      'textarea[placeholder*="about"]',
      '[data-test-id="pin-description-input"]'
    ];
    
    for (const selector of descSelectors) {
      const descField = await page.$(selector);
      if (descField) {
        await descField.type(DESIGN.description, { delay: 10 });
        console.log('✓ Description added');
        break;
      }
    }
    
    // Step 6: Add link
    console.log('🔗 Adding Etsy link...');
    const linkSelectors = [
      'input[placeholder*="link"]',
      'input[placeholder*="URL"]',
      '[data-test-id="pin-link-input"]'
    ];
    
    for (const selector of linkSelectors) {
      const linkField = await page.$(selector);
      if (linkField) {
        await linkField.type(DESIGN.link, { delay: 30 });
        console.log('✓ Link added');
        break;
      }
    }
    
    await delay(1000);
    await page.screenshot({ path: 'logs/pin_builder_filled.png' });
    
    // Step 7: Select board
    console.log('📋 Selecting board...');
    const boardDropdown = await page.$('[data-test-id="board-dropdown"], [data-test-id="select-board"]');
    
    if (boardDropdown) {
      await boardDropdown.click();
      await delay(1000);
      
      // Try to find and click the board
      const boardOption = await page.$(`text=${DESIGN.board}`);
      if (boardOption) {
        await boardOption.click();
        console.log(`✓ Board selected: ${DESIGN.board}`);
      } else {
        console.log('⚠️  Board not found, using default');
        await page.keyboard.press('Escape');
      }
    }
    
    // Step 8: Save pin
    console.log('💾 Saving pin...');
    const saveSelectors = [
      '[data-test-id="pin-builder-save"]',
      'button:has-text("Save")',
      'button:has-text("Publish")'
    ];
    
    for (const selector of saveSelectors) {
      const saveBtn = await page.$(selector);
      if (saveBtn) {
        await saveBtn.click();
        console.log('✓ Save button clicked');
        break;
      }
    }
    
    await delay(5000);
    await page.screenshot({ path: 'logs/pin_builder_saved.png' });
    
    console.log('');
    console.log('✅ PIN CREATION COMPLETE!');
    console.log('');
    console.log('Check:');
    console.log('- logs/pin_builder_saved.png for final result');
    console.log('- Your Pinterest board: Crypto Tees');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'logs/pin_builder_error.png' });
  }
  
  console.log('');
  console.log('⏳ Keeping browser open for 30 seconds...');
  console.log('Press Ctrl+C to close early');
  await delay(30000);
  
  await browser.close();
  console.log('🛑 Browser closed');
}

// Check if image exists
if (!fs.existsSync(DESIGN.imagePath)) {
  console.log(`❌ Image not found: ${DESIGN.imagePath}`);
  console.log('Generate the design first!');
  process.exit(1);
}

console.log(`✓ Image found: ${DESIGN.imagePath}`);
console.log('');
console.log('This will create a Pinterest pin with:');
console.log(`  Title: ${DESIGN.title.substring(0, 50)}...`);
console.log(`  Board: ${DESIGN.board}`);
console.log(`  Link: ${DESIGN.link}`);
console.log('');

createPin().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
