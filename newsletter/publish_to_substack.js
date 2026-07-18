const puppeteer = require('puppeteer');
const fs = require('fs');

const SUBSTACK_URL = process.env.SUBSTACK_URL || 'YOUR_SUBSTACK.substack.com';

async function publishPost() {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  // Read the post content
  const postContent = fs.readFileSync('substack_post_2026-07-18.md', 'utf8');
  
  // Navigate to Substack publish page
  await page.goto(`https://${SUBSTACK_URL}/publish`);
  
  console.log('Please log in to Substack manually.');
  console.log('The post content is ready in substack_post_2026-07-18.md');
  console.log('After login, paste the content and publish.');
  
  // Keep browser open for manual login
}

publishPost().catch(console.error);
