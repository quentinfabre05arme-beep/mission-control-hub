const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const email = 'quentin.fabre05arme@gmail.com';
const password = '2025!Narguess!2025';

async function testLogin() {
  console.log('🚀 Testing Pinterest login...');
  
  const browser = await puppeteer.launch({
    headless: false, // Visible for testing
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width: 1280, height: 800 }
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('📍 Going to Pinterest login...');
    await page.goto('https://www.pinterest.com/login/', { waitUntil: 'networkidle2', timeout: 60000 });
    
    await new Promise(r => setTimeout(r, 3000));
    
    // Take screenshot of login page
    await page.screenshot({ path: 'logs/pinterest_login_page.png' });
    console.log('📸 Login page screenshot saved');
    
    // Find email field
    const emailSelectors = ['input[id="email"]', 'input[name="id"]', 'input[type="email"]'];
    let emailField = null;
    
    for (const selector of emailSelectors) {
      emailField = await page.$(selector);
      if (emailField) {
        console.log(`✓ Found email field: ${selector}`);
        break;
      }
    }
    
    if (!emailField) {
      console.log('❌ Could not find email field');
      await page.screenshot({ path: 'logs/pinterest_error.png' });
      await browser.close();
      return;
    }
    
    // Enter email
    await emailField.type(email, { delay: 50 });
    console.log('✓ Email entered');
    
    // Find password field
    const passwordSelectors = ['input[id="password"]', 'input[name="password"]', 'input[type="password"]'];
    let passwordField = null;
    
    for (const selector of passwordSelectors) {
      passwordField = await page.$(selector);
      if (passwordField) {
        console.log(`✓ Found password field: ${selector}`);
        break;
      }
    }
    
    if (!passwordField) {
      console.log('❌ Could not find password field');
      await browser.close();
      return;
    }
    
    // Enter password
    await passwordField.type(password, { delay: 50 });
    console.log('✓ Password entered');
    
    // Find and click login button
    const loginButtonSelectors = ['button[type="submit"]', 'button:has-text("Log in")', '[data-test-id="login-button"]'];
    let loginButton = null;
    
    for (const selector of loginButtonSelectors) {
      try {
        loginButton = await page.$(selector);
        if (loginButton) {
          console.log(`✓ Found login button: ${selector}`);
          break;
        }
      } catch (e) {}
    }
    
    if (loginButton) {
      await loginButton.click();
      console.log('✓ Login button clicked');
    } else {
      console.log('❌ Could not find login button');
    }
    
    // Wait for navigation
    console.log('⏳ Waiting for login...');
    await new Promise(r => setTimeout(r, 10000));
    
    // Check current URL
    const currentUrl = page.url();
    console.log(`📍 Current URL: ${currentUrl}`);
    
    if (currentUrl.includes('pinterest.com') && !currentUrl.includes('/login')) {
      console.log('✅ LOGIN SUCCESSFUL!');
      await page.screenshot({ path: 'logs/pinterest_logged_in.png' });
      
      // Save cookies for future sessions
      const cookies = await page.cookies();
      fs.writeFileSync('logs/pinterest_cookies.json', JSON.stringify(cookies, null, 2));
      console.log('🍪 Cookies saved for future sessions');
    } else {
      console.log('⚠️ Login may have failed or 2FA required');
      await page.screenshot({ path: 'logs/pinterest_login_result.png' });
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'logs/pinterest_error.png' });
  }
  
  console.log('\n⏳ Keeping browser open for 30 seconds so you can see the result...');
  await new Promise(r => setTimeout(r, 30000));
  
  await browser.close();
  console.log('🛑 Browser closed');
}

testLogin().catch(console.error);
