const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generateChart() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Set viewport
  await page.setViewport({ width: 800, height: 400 });
  
  // Load HTML file
  const htmlPath = path.join(__dirname, 'chart_14pm.html');
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });
  
  // Wait for fonts to load
  await new Promise(r => setTimeout(r, 1000));
  
  // Take screenshot
  await page.screenshot({
    path: path.join(__dirname, 'chart_14pm.png'),
    fullPage: false,
    clip: { x: 0, y: 0, width: 800, height: 400 }
  });
  
  console.log('✅ Chart saved as: chart_14pm.png');
  
  await browser.close();
}

generateChart().catch(console.error);
