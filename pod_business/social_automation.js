#!/usr/bin/env node
/**
 * Social Media Automation System
 * Generates and schedules posts for Twitter/X, Instagram, Pinterest, TikTok
 * 
 * USAGE:
 *   node social_automation.js --platform=twitter --product="Bitcoin Treasury"
 *   node social_automation.js --platform=all --schedule=daily
 */

const fs = require('fs');
const path = require('path');

// Load growth content
const GROWTH_CONTENT = JSON.parse(fs.readFileSync('growth_content.json', 'utf8'));

// Social media accounts (to be configured)
const ACCOUNTS = {
  twitter: {
    username: '@quentinvest1',
    apiReady: false,
    note: 'X API requires OAuth setup'
  },
  instagram: {
    username: 'quentinvestdesign',
    apiReady: false,
    note: 'Meta Business API requires verification'
  },
  pinterest: {
    username: 'quentinvestdesign',
    apiReady: false,
    note: 'Pinterest API v5 requires business account'
  },
  tiktok: {
    username: 'quentinvestdesign',
    apiReady: false,
    note: 'TikTok for Business API required'
  }
};

// Best posting times (CET)
const POSTING_SCHEDULE = {
  twitter: ['08:00', '12:00', '17:00', '20:00'],
  instagram: ['09:00', '13:00', '18:00', '21:00'],
  pinterest: ['10:00', '14:00', '19:00'],
  tiktok: ['11:00', '15:00', '20:00', '22:00']
};

// Generate post content
function generatePost(platform, product) {
  const productData = GROWTH_CONTENT.products.find(p => p.title === product);
  if (!productData) return null;

  const posts = {
    twitter: `${productData.socialPosts.twitter}

🔗 https://quentinvestdesigns.etsy.com

${productData.etsyTags.slice(0, 5).map(t => '#' + t.replace(/\s/g, '')).join(' ')}`,

    instagram: `${productData.socialPosts.instagram}

🛒 Shop link in bio!

${productData.etsyTags.slice(0, 10).map(t => '#' + t.replace(/\s/g, '')).join(' ')}`,

    pinterest: `${productData.socialPosts.pinterest}`,

    tiktok: `${productData.videoScript}

🛍️ Link in bio to shop!`
  };

  return posts[platform];
}

// Get today's products to promote
function getTodaysProducts() {
  const dayOfWeek = new Date().getDay();
  const schedule = GROWTH_CONTENT.weeklySchedule;
  const todaySchedule = schedule[dayOfWeek === 0 ? 6 : dayOfWeek - 1]; // Adjust for Monday start
  
  return todaySchedule ? todaySchedule.productsToPromote : [];
}

// Create posting calendar for the week
function generateWeeklyCalendar() {
  const calendar = [];
  const platforms = Object.keys(POSTING_SCHEDULE);
  
  platforms.forEach(platform => {
    POSTING_SCHEDULE[platform].forEach(time => {
      const products = getTodaysProducts();
      products.forEach(product => {
        calendar.push({
          platform,
          time,
          product: product.title,
          content: generatePost(platform, product.title),
          ready: ACCOUNTS[platform].apiReady
        });
      });
    });
  });
  
  return calendar.sort((a, b) => a.time.localeCompare(b.time));
}

// Generate ready-to-post content
function generateReadyToPost() {
  const products = getTodaysProducts();
  const platforms = ['twitter', 'instagram', 'pinterest', 'tiktok'];
  
  const output = {
    date: new Date().toISOString(),
    posts: []
  };
  
  products.forEach(product => {
    platforms.forEach(platform => {
      output.posts.push({
        platform,
        product: product.title,
        content: generatePost(platform, product.title),
        image: `designs/${product.id}.png`,
        link: 'https://quentinvestdesigns.etsy.com'
      });
    });
  });
  
  return output;
}

// Main functions
function showStatus() {
  console.log('📱 Social Media Automation Status\n');
  console.log('═══════════════════════════════════════════════════\n');
  
  Object.entries(ACCOUNTS).forEach(([platform, account]) => {
    const status = account.apiReady ? '✅ Ready' : '⚠️ Needs Setup';
    console.log(`${platform.toUpperCase()}`);
    console.log(`  Username: ${account.username}`);
    console.log(`  Status: ${status}`);
    console.log(`  Note: ${account.note}`);
    console.log('');
  });
  
  console.log('═══════════════════════════════════════════════════\n');
  console.log('💡 To enable automatic posting, you need to:');
  console.log('   1. Create business accounts on each platform');
  console.log('   2. Apply for API access');
  console.log('   3. Provide credentials (stored securely)');
  console.log('');
  console.log('🔄 Until then: Copy/paste the generated content manually\n');
}

function showTodaysPosts() {
  const posts = generateReadyToPost();
  
  console.log('📅 Today\'s Social Media Content\n');
  console.log(`Generated: ${new Date(posts.date).toLocaleString('en-US', { timeZone: 'Europe/Paris' })}\n`);
  console.log('═══════════════════════════════════════════════════\n');
  
  posts.posts.forEach((post, i) => {
    console.log(`${i + 1}. ${post.platform.toUpperCase()} — ${post.product}`);
    console.log('─'.repeat(50));
    console.log(post.content);
    console.log(`\n🖼️ Image: ${post.image}`);
    console.log(`🔗 Link: ${post.link}`);
    console.log('\n');
  });
  
  // Save to file
  fs.writeFileSync('todays_posts.json', JSON.stringify(posts, null, 2));
  console.log('✅ Saved to: todays_posts.json\n');
}

function showWeeklyCalendar() {
  const calendar = generateWeeklyCalendar();
  
  console.log('📆 Weekly Posting Calendar\n');
  console.log('═══════════════════════════════════════════════════\n');
  
  const groupedByDay = {};
  calendar.forEach(item => {
    const day = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    if (!groupedByDay[day]) groupedByDay[day] = [];
    groupedByDay[day].push(item);
  });
  
  Object.entries(groupedByDay).forEach(([day, posts]) => {
    console.log(`\n${day.toUpperCase()}`);
    console.log('─'.repeat(50));
    posts.forEach(post => {
      console.log(`  ${post.time} — ${post.platform} — ${post.product}`);
    });
  });
  
  console.log('\n');
}

function setupAccount(platform) {
  const setupUrls = {
    twitter: 'https://developer.twitter.com/en/portal/dashboard',
    instagram: 'https://developers.facebook.com/apps/',
    pinterest: 'https://developers.pinterest.com/apps/',
    tiktok: 'https://developers.tiktok.com/'
  };
  
  console.log(`\n🛠️ Setup ${platform.toUpperCase()} API Access\n`);
  console.log('─────────────────────────────────────────────────');
  console.log(`1. Go to: ${setupUrls[platform]}`);
  console.log('2. Create a new app/project');
  console.log('3. Get API keys/credentials');
  console.log('4. Run: node social_automation.js --configure');
  console.log('─────────────────────────────────────────────────\n');
}

// CLI
const args = process.argv.slice(2);
const command = args[0] || 'status';

switch (command) {
  case '--status':
  case 'status':
    showStatus();
    break;
    
  case '--today':
  case 'today':
    showTodaysPosts();
    break;
    
  case '--week':
  case 'week':
    showWeeklyCalendar();
    break;
    
  case '--setup':
    const platform = args[1]?.replace('--platform=', '');
    if (platform) {
      setupAccount(platform);
    } else {
      console.log('Usage: node social_automation.js --setup --platform=twitter');
    }
    break;
    
  default:
    console.log('Social Media Automation\n');
    console.log('Commands:');
    console.log('  node social_automation.js status     Show account status');
    console.log('  node social_automation.js today        Generate today\'s posts');
    console.log('  node social_automation.js week         Show weekly calendar');
    console.log('  node social_automation.js --setup --platform=NAME  Setup guide');
    console.log('');
    showStatus();
}
