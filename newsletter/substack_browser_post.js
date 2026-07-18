const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SUBSTACK_URL = process.env.SUBSTACK_URL || 'quentinvest.substack.com';

async function publishToSubstack() {
  console.log('🚀 Starting Substack browser automation...');
  
  // Read post content
  const postPath = path.join(__dirname, 'substack_post_2026-07-18.md');
  const postContent = fs.readFileSync(postPath, 'utf8');
  
  // Extract title (first line)
  const lines = postContent.split('\n');
  const title = lines[0].replace('# ', '').trim();
  const body = lines.slice(2).join('\n'); // Skip title and blank line
  
  console.log(`📰 Title: ${title}`);
  console.log(`📝 Body length: ${body.length} chars`);
  
  // Launch browser
  const browser = await puppeteer.launch({
    headless: false, // Show browser for login
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  
  try {
    // Navigate to Substack publish
    const publishUrl = `https://${SUBSTACK_URL}/publish`;
    console.log(`🔗 Navigating to: ${publishUrl}`);
    await page.goto(publishUrl, { waitUntil: 'networkidle0' });
    
    // Check if already logged in
    const currentUrl = page.url();
    console.log(`📍 Current URL: ${currentUrl}`);
    
    if (currentUrl.includes('login') || currentUrl.includes('signin')) {
      console.log('🔐 Login required. Waiting for manual login...');
      console.log('Please log in to Substack in the browser window.');
      console.log('The script will continue after login (2 minute timeout).');
      
      // Wait for navigation away from login page
      await page.waitForNavigation({ 
        waitUntil: 'networkidle0', 
        timeout: 120000 
      });
    }
    
    console.log('✅ Logged in. Setting up post...');
    
    // Wait for the editor to load
    await page.waitForSelector('[data-testid="editor-title-input"], .title-input, [placeholder="Title"]', { 
      timeout: 10000 
    });
    
    // Enter title
    const titleSelector = '[data-testid="editor-title-input"], .title-input, [placeholder="Title"]';
    await page.click(titleSelector);
    await page.keyboard.type(title);
    console.log('✍️ Title entered');
    
    // Enter body
    const bodySelector = '[data-testid="editor-paragraph"], .ProseMirror, [contenteditable="true"]';
    await page.click(bodySelector);
    
    // Type body content (split into chunks for reliability)
    const chunks = body.match(/[\s\S]{1,500}/g) || [body];
    for (const chunk of chunks) {
      await page.keyboard.type(chunk);
      await new Promise(r => setTimeout(r, 50));
    }
    console.log('✍️ Body entered');
    
    // Wait a moment for content to settle
    await new Promise(r => setTimeout(r, 1000));
    
    console.log('📋 Post ready. Review in browser, then:');
    console.log('  1. Click "Publish" button');
    console.log('  2. Confirm publish');
    console.log('');
    console.log('⏳ Browser will stay open for 60 seconds...');
    
    await new Promise(r => setTimeout(r, 60000));
    
    console.log('✅ Done! Closing browser.');
    await browser.close();
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('Browser staying open for debugging...');
    await new Promise(r => setTimeout(r, 30000));
    await browser.close();
  }
}

publishToSubstack().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
