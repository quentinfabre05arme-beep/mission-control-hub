const { chromium } = require('playwright');

async function postToX(text) {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  const page = context.pages()[0];
  
  // Navigate to compose
  await page.goto('https://twitter.com/compose/post');
  await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
  
  // Type the post
  await page.fill('[data-testid="tweetTextarea_0"]', text);
  
  // Click Post button
  await page.click('[data-testid="tweetButton"]');
  
  // Wait for confirmation
  await page.waitForTimeout(3000);
  
  await browser.close();
  console.log('Posted:', text);
}

const text = process.argv[2] || 'Testing autonomous posting from OpenClaw AI agent. #AI #Autonomy';
postToX(text).catch(console.error);
