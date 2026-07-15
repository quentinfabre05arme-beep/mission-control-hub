// x_post_browser.js - Free X Posting via Browser (No API)
// Run this after manually logging into X in Chrome

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs').promises;
const path = require('path');

// Add stealth plugin
puppeteer.use(StealthPlugin());

const CONFIG = {
  chromeProfile: 'C:\\Users\\quent\\AppData\\Local\\Google\\Chrome\\User Data',
  queueFile: 'C:\\Users\\quent\\.openclaw\\workspace\\x_queue.json',
  logFile: 'C:\\Users\\quent\\.openclaw\\workspace\\logs\\x_posts.log',
  screenshotDir: 'C:\\Users\\quent\\.openclaw\\workspace\\screenshots'
};

async function log(message) {
  const timestamp = new Date().toISOString();
  const logEntry = `[${timestamp}] ${message}\n`;
  console.log(logEntry.trim());
  await fs.mkdir(path.dirname(CONFIG.logFile), { recursive: true });
  await fs.appendFile(CONFIG.logFile, logEntry).catch(() => {});
}

async function getQueuedPost() {
  try {
    const data = await fs.readFile(CONFIG.queueFile, 'utf8');
    const queue = JSON.parse(data);
    const post = queue.posts.find(p => p.status === 'pending');
    if (post) {
      await log(`Found queued post: ${post.id}`);
      return post;
    }
    return null;
  } catch (err) {
    await log(`Error reading queue: ${err.message}`);
    return null;
  }
}

async function markPosted(postId, url = null) {
  try {
    const data = await fs.readFile(CONFIG.queueFile, 'utf8');
    const queue = JSON.parse(data);
    const post = queue.posts.find(p => p.id === postId);
    if (post) {
      post.status = 'posted';
      post.postedAt = new Date().toISOString();
      if (url) post.url = url;
      await fs.writeFile(CONFIG.queueFile, JSON.stringify(queue, null, 2));
      await log(`Marked post ${postId} as posted${url ? ' with URL: ' + url : ''}`);
    }
  } catch (err) {
    await log(`Error updating queue: ${err.message}`);
  }
}

async function postToX(text) {
  await log('Starting browser automation...');
  
  let browser;
  try {
    // Launch with Chrome profile for session persistence
    browser = await puppeteer.launch({
      headless: false, // Must be visible for human-like behavior
      executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      userDataDir: CONFIG.chromeProfile,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--single-process',
        '--disable-gpu'
      ],
      slowMo: 100 // Slow down for human-like typing
    });

    const page = await browser.newPage();
    
    // Set viewport for consistency
    await page.setViewport({ width: 1280, height: 800 });
    
    // Set user agent
    await page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );
    
    // Navigate to X home
    await log('Navigating to X...');
    await page.goto('https://x.com/home', { waitUntil: 'networkidle2', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    // Check if we're logged in
    const url = page.url();
    if (url.includes('login') || url.includes('i/flow/login')) {
      await log('Not logged in - manual login required');
      await page.screenshot({ path: path.join(CONFIG.screenshotDir, 'login-required.png') });
      await browser.close();
      return { success: false, error: 'LOGIN_REQUIRED' };
    }
    
    await log('Logged in detected - proceeding to post');
    
    // Click compose button
    await log('Clicking compose button...');
    const composeSelectors = [
      '[data-testid="SideNav_NewTweet_Button"]',
      'a[href="/compose/tweet"]',
      '[aria-label*="Compose"]'
    ];
    
    let composeClicked = false;
    for (const selector of composeSelectors) {
      try {
        await page.waitForSelector(selector, { timeout: 5000 });
        await page.click(selector);
        composeClicked = true;
        await log(`Compose button clicked using: ${selector}`);
        break;
      } catch (e) {
        continue;
      }
    }
    
    if (!composeClicked) {
      throw new Error('Could not find compose button');
    }
    
    await page.waitForTimeout(2000);
    
    // Find and fill text input
    await log('Entering text...');
    const textSelectors = [
      '[data-testid="tweetTextarea_0"]',
      'div[role="textbox"][contenteditable="true"]',
      '.public-DraftEditor-content'
    ];
    
    let textEntered = false;
    for (const selector of textSelectors) {
      try {
        const element = await page.waitForSelector(selector, { timeout: 5000 });
        await element.click();
        await page.waitForTimeout(500);
        await element.type(text, { delay: 50 }); // Human-like typing
        textEntered = true;
        await log(`Text entered using: ${selector}`);
        break;
      } catch (e) {
        continue;
      }
    }
    
    if (!textEntered) {
      throw new Error('Could not find text input');
    }
    
    await page.waitForTimeout(1000);
    
    // Click post button
    await log('Clicking post button...');
    const postSelectors = [
      '[data-testid="tweetButton"]',
      '[data-testid="tweetButtonInline"]',
      'button[type="submit"]'
    ];
    
    let postClicked = false;
    for (const selector of postSelectors) {
      try {
        const button = await page.waitForSelector(selector, { timeout: 5000 });
        const isEnabled = await button.evaluate(el => !el.disabled);
        if (isEnabled) {
          await button.click();
          postClicked = true;
          await log(`Post button clicked using: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }
    
    if (!postClicked) {
      throw new Error('Could not find or click post button');
    }
    
    // Wait for post to complete
    await log('Waiting for post to complete...');
    await page.waitForTimeout(5000);
    
    // Check for success indicators
    const successIndicators = [
      '[data-testid="toast"]', // Toast notification
      '.r-1p0dtai', // Success animation
      '[data-testid="cellInnerDiv"]:has-text("' + text.substring(0, 20) + '")'
    ];
    
    let posted = false;
    for (const indicator of successIndicators) {
      try {
        await page.waitForSelector(indicator, { timeout: 5000 });
        posted = true;
        await log(`Success detected via: ${indicator}`);
        break;
      } catch (e) {
        continue;
      }
    }
    
    // Screenshot for verification
    await fs.mkdir(CONFIG.screenshotDir, { recursive: true });
    const screenshotPath = path.join(CONFIG.screenshotDir, `post-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    await log(`Screenshot saved: ${screenshotPath}`);
    
    await browser.close();
    
    return { success: posted, simulated: !posted };
    
  } catch (err) {
    await log(`Error during posting: ${err.message}`);
    if (browser) await browser.close().catch(() => {});
    return { success: false, error: err.message };
  }
}

async function main() {
  await log('=== X Browser Poster Starting ===');
  
  const post = await getQueuedPost();
  if (!post) {
    await log('No pending posts in queue');
    return;
  }
  
  await log(`Posting: "${post.text.substring(0, 50)}..."`);
  const result = await postToX(post.text);
  
  if (result.success) {
    await markPosted(post.id, result.url);
    await log('✅ Post completed successfully');
  } else if (result.error === 'LOGIN_REQUIRED') {
    await log('⚠️ Manual login required - please log into X in Chrome first');
  } else {
    await log(`❌ Post failed: ${result.error}`);
  }
  
  await log('=== X Browser Poster Complete ===');
}

main().catch(async err => {
  await log(`Fatal error: ${err.message}`);
  console.error(err);
  process.exit(1);
});
