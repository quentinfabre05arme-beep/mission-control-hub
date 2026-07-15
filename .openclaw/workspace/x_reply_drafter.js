// x_reply_drafter.js - Generate reply drafts using Grok AI
// Takes discovered posts and creates reply options

const fs = require('fs').promises;
const path = require('path');

// Import grok_analytics if available
let grokAnalytics;
try {
  grokAnalytics = require('./grok_analytics');
} catch {
  console.log('Note: grok_analytics.js not available, using template mode');
}

const CONFIG = {
  queueFile: 'C:\\Users\\quent\\.openclaw\workspace\\data\\x_reply_queue.json',
  voiceProfile: {
    style: 'Thesis-first, data-backed, contrarian when warranted',
    phrases: ['This is the distinction most miss', 'What the data shows', 'The market is pricing in'],
    avoid: ['moon', 'lambo', 'hodl', 'to the moon', 'diamond hands'],
    tone: 'Professional, calm, conviction without hype'
  }
};

async function log(msg) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] ${msg}`);
}

async function loadQueue() {
  const data = await fs.readFile(CONFIG.queueFile, 'utf-8');
  return JSON.parse(data);
}

async function saveQueue(queue) {
  await fs.writeFile(CONFIG.queueFile, JSON.stringify(queue, null, 2));
}

// Generate reply using Grok API
async function generateReplyWithGrok(targetPost, style = 'expand') {
  if (!grokAnalytics || !grokAnalytics.optimizeContent) {
    // Fallback to template mode if Grok not available
    return generateReplyTemplate(targetPost, style);
  }
  
  const prompt = `
Draft a reply to this X post:

Original post by @${targetPost.author}:
"${targetPost.text}"

Engagement: ${targetPost.engagement.likes} likes, ${targetPost.engagement.replies} replies

Reply style: ${style}
- agree = acknowledge and add perspective
- expand = build on their point with data
- challenge = respectful counterpoint with evidence

Your voice: ${CONFIG.voiceProfile.style}
Avoid: ${CONFIG.voiceProfile.avoid.join(', ')}

Requirements:
- Maximum 280 characters
- Single line breaks for readability
- Hook in first line
- Must add value, not just agree
- Professional tone

Draft:`;

  try {
    const result = await grokAnalytics.optimizeContent(prompt);
    return result.optimization || result;
  } catch (err) {
    log(`Grok error: ${err.message}. Using template.`);
    return generateReplyTemplate(targetPost, style);
  }
}

// Template-based reply generation (no Grok needed)
function generateReplyTemplate(targetPost, style) {
  const text = targetPost.text.toLowerCase();
  const author = targetPost.author;
  
  // Reply templates by topic
  const templates = {
    btc: {
      agree: [
        `This is the distinction most miss.\n\n${author} gets it. The thesis is playing out in real-time.`,
        `Exactly.\n\nThe market is slowly waking up to what the data already shows.`,
        `This.\n\nBitcoin isn't just a trade. It's a treasury reserve asset. The transformation is underway.`
      ],
      expand: [
        `This is the distinction most miss.\n\nCapital sits idle. Credit circulates.\n\nBitcoin fixed scarcity. Strategy fixes velocity.\n\nTogether they're rewriting treasury reserves.`,
        `The data backs this.\n\nCompanies holding BTC aren't speculating.\n\nThey're front-running the repricing of money itself.`,
        `${author} gets the big picture.\n\nWhat's missed: the velocity of this transition.\n\nFirst movers get asymmetric returns. Followers get the mean.`
      ],
      challenge: [
        `The framework is right. The timeline is the question.\n\nAdoption is accelerating, but regulatory headwinds remain.\n\nThe thesis holds, but patience required.`,
        `True, but let's not ignore the risks.\n\nConcentration, regulatory, technical.\n\nThe upside is real. So is the volatility.`
      ]
    },
    eth: {
      agree: [
        `The tech thesis is clear.\n\nExecution risk is the only variable. And execution has been strong.`,
        `Exactly. Ethereum is infrastructure for the next financial system.\n\nThe bet isn't on price. It's on adoption curves.`
      ],
      expand: [
        `This is underappreciated.\n\nThe merge reduced issuance. The L2s scale usage.\n\nSupply dynamics are shifting. The market hasn't fully priced this.`,
        `The tech is sound.\n\nWhat's interesting: the institutional pivot to ETH after ETF approval.\n\nWe're watching a liquidity preference shift in real-time.`
      ]
    },
    healthcare: {
      agree: [
        `The GLP-1 transformation is just beginning.\n\nHealthcare is being rewired. Most haven't connected the dots yet.`,
        `Exactly. This isn't a drug cycle. It's a consumer behavior shift.\n\nThe implications for healthcare economics are massive.`
      ],
      expand: [
        `The data is compelling.\n\nBut watch the second-order effects: insurance dynamics, provider incentives, long-term adherence.\n\nThe winners will own the full stack, not just the molecule.`
      ]
    },
    macro: {
      agree: [
        `The macro setup is the story.\n\nLiquidity cycles, fiscal dominance, monetary pivots.\n\nAssets are being repriced against a new baseline.`,
        `This. The Fed doesn't control the narrative anymore.\n\nThe bond market does. And the bond market is voting.`
      ],
      expand: [
        `The signal is in the dispersion.\n\nNot all risk assets will benefit equally.\n\nQuality, cash flows, and duration exposure will separate winners from beta-chasers.`
      ]
    }
  };
  
  // Determine topic
  let topic = 'macro';
  if (text.includes('bitcoin') || text.includes('btc')) topic = 'btc';
  else if (text.includes('ethereum') || text.includes('eth')) topic = 'eth';
  else if (text.includes('glp') || text.includes('healthcare') || text.includes('hims')) topic = 'healthcare';
  
  // Get templates for topic/style
  const topicTemplates = templates[topic] || templates.macro;
  const styleTemplates = topicTemplates[style] || topicTemplates.expand;
  
  // Pick random template
  const reply = styleTemplates[Math.floor(Math.random() * styleTemplates.length)];
  
  return reply;
}

// Generate 3 reply options for a post
async function generateReplyOptions(post) {
  log(`Drafting replies for @${post.author}...`);
  
  const styles = ['agree', 'expand', 'challenge'];
  const drafts = [];
  
  for (const style of styles) {
    try {
      const reply = await generateReplyWithGrok(post, style);
      drafts.push({
        style: style,
        text: reply,
        predictedEngagement: style === 'expand' ? 'high' : 'medium',
        why: getWhyExplanation(style)
      });
    } catch (err) {
      log(`Error generating ${style} reply: ${err.message}`);
    }
  }
  
  return drafts;
}

function getWhyExplanation(style) {
  const explanations = {
    agree: 'Builds rapport with author, shows alignment with thought leader',
    expand: 'Adds unique perspective, most likely to get engagement',
    challenge: 'Respectful counterpoint, can spark discussion'
  };
  return explanations[style] || 'Adds value to conversation';
}

async function main() {
  log('=== X Reply Drafter Starting ===');
  
  const queue = await loadQueue();
  let drafted = 0;
  
  // Find posts needing drafts
  const pending = queue.discovered.filter(p => p.status === 'pending_draft');
  log(`${pending.length} posts waiting for drafts`);
  
  for (const post of pending) {
    try {
      const drafts = await generateReplyOptions(post);
      
      if (drafts.length > 0) {
        post.draftReplies = drafts;
        post.status = 'drafted';
        post.draftedAt = new Date().toISOString();
        drafted++;
        
        log(`Drafted ${drafts.length} replies for @${post.author}`);
        
        // Output for user review
        console.log(`\n--- @${post.author} ---`);
        console.log(`Post: ${post.text.substring(0, 80)}...`);
        console.log(`Link: ${post.url}`);
        drafts.forEach((d, i) => {
          console.log(`\n[${i+1}] ${d.style.toUpperCase()} (${d.predictedEngagement}):`);
          console.log(d.text);
          console.log(`Why: ${d.why}`);
        });
        console.log('---\n');
      }
    } catch (err) {
      log(`Error drafting for @${post.author}: ${err.message}`);
    }
  }
  
  await saveQueue(queue);
  log(`Drafted replies for ${drafted} posts`);
  log('=== X Reply Drafter Complete ===');
  
  return { drafted, total: queue.discovered.length };
}

// Manual draft for single post
async function draftReplyForPost(postData) {
  const drafts = await generateReplyOptions(postData);
  return drafts;
}

module.exports = {
  generateReplyOptions,
  draftReplyForPost,
  generateReplyWithGrok
};

// CLI usage
if (require.main === module) {
  main().catch(console.error);
}
