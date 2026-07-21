#!/usr/bin/env node
/**
 * Pinterest Web Automation - Auto-create pins for POD designs
 * Uses Puppeteer to control Chrome browser
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.pinterest' });

const CONFIG = {
  email: process.env.PINTEREST_EMAIL,
  password: process.env.PINTEREST_PASSWORD,
  board: process.env.PINTEREST_BOARD || 'Crypto Tees',
  etsyUrl: process.env.ETSY_SHOP_URL || 'https://www.etsy.com/shop/QuentinvestDesigns',
  headless: false, // Set to true for invisible mode after testing
  screenshots: true
};

const LOG_FILE = path.join(__dirname, 'logs', 'pinterest.log');

function log(message) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${message}`;
  console.log(entry);
  if (!fs.existsSync(path.dirname(LOG_FILE))) {
    fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
  }
  fs.appendFileSync(LOG_FILE, entry + '\n');
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function takeScreenshot(page, name) {
  if (!CONFIG.screenshots) return;
  const screenshotPath = path.join(__dirname, 'logs', `screenshot_${name}_${Date.now()}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  log(`📸 Screenshot saved: ${screenshotPath}`);
}

async function loginToPinterest(page) {
  log('🔐 Logging into Pinterest...');
  
  await page.goto('https://www.pinterest.com/login/', { waitUntil: 'networkidle2' });
  await delay(2000);
  
  // Enter email
  await page.waitForSelector('input[id="email"]', { timeout: 10000 });
  await page.type('input[id="email"]', CONFIG.email, { delay: 50 });
  log('✓ Email entered');
  
  // Enter password
  await page.type('input[id="password"]', CONFIG.password, { delay: 50 });
  log('✓ Password entered');
  
  // Click login
  await page.click('button[type="submit"]');
  log('✓ Login button clicked');
  
  // Wait for navigation
  await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 });
  await delay(3000);
  
  // Check if logged in
  const currentUrl = page.url();
  if (currentUrl.includes('pinterest.com') && !currentUrl.includes('/login')) {
    log('✅ Successfully logged into Pinterest!');
    await takeScreenshot(page, 'logged_in');
    return true;
  } else {
    log('❌ Login may have failed. Current URL: ' + currentUrl);
    await takeScreenshot(page, 'login_failed');
    return false;
  }
}

async function createPin(page, design) {
  log(`\n📌 Creating pin for: ${design.name}`);
  
  // Go to pin builder
  await page.goto('https://www.pinterest.com/pin-builder/', { waitUntil: 'networkidle2' });
  await delay(2000);
  
  // Upload image
  log('📤 Uploading image...');
  const fileInput = await page.$('input[type="file"]');
  if (!fileInput) {
    // Try alternative selector
    const altInput = await page.$('input[accept="image/*"]');
    if (altInput) {
      await altInput.uploadFile(design.imagePath);
    } else {
      log('⚠️ Could not find file upload input');
      await takeScreenshot(page, 'upload_failed');
      return false;
    }
  } else {
    await fileInput.uploadFile(design.imagePath);
  }
  
  await delay(3000); // Wait for upload
  log('✓ Image uploaded');
  
  // Add title
  const titleInput = await page.$('textarea[placeholder*="title"], input[placeholder*="title"]');
  if (titleInput) {
    await titleInput.type(design.title, { delay: 30 });
    log('✓ Title added');
  }
  
  // Add description
  const descInput = await page.$('textarea[placeholder*="description"], textarea[placeholder*="about"]');
  if (descInput) {
    await descInput.type(design.description, { delay: 30 });
    log('✓ Description added');
  }
  
  // Add link
  const linkInput = await page.$('input[placeholder*="link"], input[placeholder*="URL"]');
  if (linkInput) {
    await linkInput.type(design.link, { delay: 30 });
    log('✓ Link added');
  }
  
  // Select board
  log('📋 Selecting board...');
  const boardDropdown = await page.$('[data-test-id="board-dropdown"], [data-test-id="select-board"]');
  if (boardDropdown) {
    await boardDropdown.click();
    await delay(1000);
    
    // Try to find board by name
    const boardOption = await page.$(`text=${CONFIG.board}`);
    if (boardOption) {
      await boardOption.click();
      log(`✓ Board selected: ${CONFIG.board}`);
    } else {
      log('⚠️ Could not find board, using default');
    }
  }
  
  // Save pin
  const saveButton = await page.$('[data-test-id="pin-builder-save"], button:has-text("Save")');
  if (saveButton) {
    await saveButton.click();
    log('💾 Saving pin...');
    await delay(3000);
  }
  
  await takeScreenshot(page, `pin_created_${design.name}`);
  log(`✅ Pin created for ${design.name}`);
  return true;
}

async function main() {
  log('╔════════════════════════════════════════════╗');
  log('║     Pinterest Automation - Starting Run     ║');
  log('╚════════════════════════════════════════════╝');
  
  // Validate config
  if (!CONFIG.email || !CONFIG.password) {
    log('❌ Error: Pinterest credentials not found in .env.pinterest');
    process.exit(1);
  }
  
  log(`Board: ${CONFIG.board}`);
  log(`Etsy: ${CONFIG.etsyUrl}`);
  
  // Launch browser
  log('\n🚀 Launching Chrome...');
  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width: 1280, height: 800 }
  });
  
  const page = await browser.newPage();
  
  try {
    // Login
    const loggedIn = await loginToPinterest(page);
    if (!loggedIn) {
      throw new Error('Failed to log into Pinterest');
    }
    
    // Example designs (will be replaced with actual designs)
    const testDesigns = [
      {
        name: 'bitcoin_millionaire',
        imagePath: path.join(__dirname, 'generated', 'design_1_bitcoin_millionaire.png'),
        title: 'Bitcoin Millionaire Tee | Crypto Investor Gift',
        description: `🔥 Bitcoin Millionaire Tee

Perfect for crypto investors, HODLers, and Bitcoin believers.
Premium softstyle unisex fit.

✅ High-quality print
✅ Bitcoin investor gift
✅ Crypto merch
✅ HODL life

🔗 Shop now on Etsy

#bitcoin #crypto #hodl #investor #gift #cryptocurrency #blockchain #millionaire`,
        link: `${CONFIG.etsyUrl}/listing/YOUR_LISTING_ID`
      }
    ];
    
    // Create pins
    for (const design of testDesigns) {
      if (fs.existsSync(design.imagePath)) {
        await createPin(page, design);
      } else {
        log(`⚠️ Image not found: ${design.imagePath}`);
      }
    }
    
    log('\n✅ Pinterest automation completed!');
    
  } catch (error) {
    log(`\n❌ Error: ${error.message}`);
    await takeScreenshot(page, 'error');
  } finally {
    await browser.close();
    log('🛑 Browser closed');
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(err => {
    log(`FATAL ERROR: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { createPin, loginToPinterest };
