const drafter = require('./x_reply_drafter');

const saylorPost = {
  author: 'saylor',
  text: 'Bitcoin is Digital Capital. Strategy transforms it into Digital Credit.',
  engagement: { likes: 3348, replies: 448, views: 218384 },
  timestamp: '2026-07-14T13:00:00Z',
  url: 'https://x.com/saylor/status/2076996691861905775'
};

async function demo() {
  console.log('=== Reply Drafter Demo ===\n');
  console.log(`Target: @${saylorPost.author}`);
  console.log(`Post: "${saylorPost.text}"`);
  console.log(`Engagement: ${saylorPost.engagement.likes} likes, ${saylorPost.engagement.views} views\n`);
  console.log('Drafting replies...\n');
  
  const drafts = await drafter.draftReplyForPost(saylorPost);
  
  drafts.forEach((d, i) => {
    console.log(`[${i+1}] ${d.style.toUpperCase()} — ${d.predictedEngagement} engagement`);
    console.log(d.text);
    console.log(`Why: ${d.why}\n`);
  });
}

demo().catch(console.error);
