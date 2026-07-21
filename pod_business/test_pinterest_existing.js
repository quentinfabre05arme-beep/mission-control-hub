const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Find Chrome user data directory
function getChromeUserDataDir() {
  const platform = os.platform();
  if (platform === 'win32') {
    return path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data');
  } else if (platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support', 'Google', 'Chrome');
  } else {
    return path.join(os.homedir(), '.config', 'google-chrome');
  }
}

async function testWithExistingProfile() {
  console.log('🚀 Testing Pinterest with existing Chrome profile...');
  
  const userDataDir = getChromeUserDataDir();
  console.log(`📍 Chrome profile: ${userDataDir}`);
  
  // Launch with existing profile
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      `--user-data-dir=${userDataDir}`,
      '--profile-directory=Default'
    ],
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    defaultViewport: { width: 1280, height: 800 }
  });
  
  const page = await browser.newPage();
  
  try {
    // Go to Pinterest home - should already be logged in
    console.log('📍 Going to Pinterest...');
    await page.goto('https://www.pinterest.com/', { waitUntil: 'networkidle2', timeout: 60000 });
    
    await new Promise(r => setTimeout(r, 3000));
    
    // Check if logged in
    const currentUrl = page.url();
    console.log(`📍 Current URL: ${currentUrl}`);
    
    // Look for profile indicator
    const profilePic = await page.$('[data-test-id="user-profile-picture"]');
    const userMenu = await page.$('[data-test-id="header-menu-options"]');
    
    if (profilePic || userMenu || currentUrl.includes('/home/')) {
      console.log('✅ ALREADY LOGGED IN!');
      await page.screenshot({ path: 'logs/pinterest_already_logged_in.png' });
      
      // Try to create a pin
      console.log('📌 Testing pin creation...');
      await page.goto('https://www.pinterest.com/pin-builder/', { waitUntil: 'networkidle2' });
      
      await new Promise(r => setTimeout(r, 3000));
      await page.screenshot({ path: 'logs/pinterest_pin_builder.png' });
      console.log('📸 Pin builder screenshot saved');
      
      // Check if pin builder loaded
      const uploadButton = await page.$('input[type="file"]');
      if (uploadButton) {
        console.log('✅ Pin builder ready!');
      } else {
        console.log('⚠️ Pin builder may need manual check');
      }
      
    } else {
      console.log('⚠️ Not logged in automatically');
      console.log('Trying direct login with saved credentials...');
      
      // Try clicking login if present
      const loginBtn = await page.$('[data-test-id="login-button"], a[href*="/login/"]');
      if (loginBtn) {
        await loginBtn.click();
        await new Promise(r => setTimeout(r, 5000));
        
        // Check if auto-filled
        const emailField = await page.$('input[id="email"]');
        if (emailField) {
          const value = await emailField.evaluate(el => el.value);
          if (value) {
            console.log('✅ Email auto-filled');
            
            // Click continue/login
            const continueBtn = await page.$('button[type="submit"]');
            if (continueBtn) {
              await continueBtn.click();
              await new Promise(r => setTimeout(r, 5000));
            }
          }
        }
      }
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'logs/pinterest_error.png' });
  }
  
  console.log('\n⏳ Keeping browser open for 20 seconds...');
  await new Promise(r => setTimeout(r, 20000));
  
  await browser.close();
  console.log('🛑 Browser closed');
}

testWithExistingProfile().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
