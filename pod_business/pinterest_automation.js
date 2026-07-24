// Pinterest Automation for POD Traffic
// Auto-pins products to Pinterest boards

const fs = require('fs');

const CONFIG = {
  boards: ['Crypto Merch', 'Investor Gifts', 'AI Apparel', 'Trading Lifestyle'],
  pinsPerDay: 5,
  times: ['09:00', '13:00', '17:00', '20:00', '22:00']
};

function generatePinContent(product) {
  const templates = [
    `🔥 ${product.title} — Perfect for ${product.niche} enthusiasts!`,
    `💎 New ${product.niche} design just dropped!`,
    `🚀 ${product.title} — Limited edition`,
    `⭐ ${product.niche} fans, this one's for you!`,
    `💰 ${product.title} — Shop now!`
  ];
  
  return {
    title: product.title,
    description: templates[Math.floor(Math.random() * templates.length)],
    hashtags: product.tags.split(',').map(t => '#' + t.replace(/-/g, '')).join(' '),
    board: CONFIG.boards[CONFIG.boards.findIndex(b => b.toLowerCase().includes(product.niche)) || 0]
  };
}

function createPinSchedule() {
  const designs = JSON.parse(fs.readFileSync('pod_business/generated_designs/batch_2026-07-24.json', 'utf8'));
  const schedule = [];
  
  for (let i = 0; i < Math.min(CONFIG.pinsPerDay, designs.length); i++) {
    const pin = generatePinContent(designs[i]);
    schedule.push({
      time: CONFIG.times[i],
      ...pin,
      productId: designs[i].id
    });
  }
  
  fs.writeFileSync('pod_business/pinterest_schedule.json', JSON.stringify(schedule, null, 2));
  
  console.log('=== Pinterest Automation Schedule ===');
  console.log(`Pins today: ${schedule.length}`);
  schedule.forEach(s => {
    console.log(`${s.time} — ${s.board}: ${s.title}`);
  });
  console.log('\n📁 Schedule saved: pinterest_schedule.json');
  console.log('⚠️  Note: Manual Pin or Tailwind required for actual posting');
}

createPinSchedule();
