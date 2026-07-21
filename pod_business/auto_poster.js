/**
 * Auto Poster — Creates daily social content
 * Outputs ready-to-post content for Twitter/X, Instagram, Pinterest
 */

const fs = require('fs');

const content = JSON.parse(fs.readFileSync('growth_content.json', 'utf8'));

function getDayOfWeek() {
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date().getDay()];
}

function getTodaysFocus() {
  const schedule = content.weeklySchedule;
  const today = getDayOfWeek();
  return schedule.find(s => s.day === today);
}

function generateTodaysPost() {
  const focus = getTodaysFocus();
  const products = focus.productsToPromote;
  
  console.log(`📅 TODAY (${getDayOfWeek()}): ${focus.focus}\n`);
  
  products.forEach(p => {
    const productData = content.products.find(cp => cp.title === p.title);
    if (!productData) return;
    
    console.log(`🎨 ${p.title}`);
    console.log('─'.repeat(50));
    console.log('\n🐦 TWITTER/X:');
    console.log(productData.socialPosts.twitter);
    console.log('\n📸 INSTAGRAM:');
    console.log(productData.socialPosts.instagram);
    console.log('\n📌 PINTEREST:');
    console.log(productData.socialPosts.pinterest);
    console.log('\n🎬 TIKTOK SCRIPT:');
    console.log(productData.videoScript);
    console.log('\n');
  });
  
  console.log('✅ Copy and post to your social accounts!');
}

// Weekly summary
function generateWeeklyReport() {
  const metrics = JSON.parse(fs.readFileSync('etsy_metrics.json', 'utf8'));
  
  console.log('\n📊 WEEKLY SUMMARY');
  console.log('─'.repeat(50));
  console.log(`Shop: Quentinvestdesign`);
  console.log(`Products: ${metrics.metrics.products}`);
  console.log(`Views: ${metrics.metrics.views}`);
  console.log(`Sales: ${metrics.metrics.sales}`);
  console.log(`Revenue: $${metrics.metrics.revenue}`);
  console.log(`Action: ${metrics.action}`);
  console.log('─'.repeat(50));
}

// Main
const command = process.argv[2];

if (command === 'weekly') {
  generateWeeklyReport();
} else {
  generateTodaysPost();
}
