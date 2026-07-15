// x_reply_finder.js - Discover high-engagement posts to reply to
// Runs every 2 hours via cron

const fs = require('fs').promises;
const path = require('path');

const CONFIG = {
  queueFile: 'C:\\Users\\quent\\.openclaw\workspace\\data\\x_reply_queue.json',
  screenshotDir: 'C:\\Users\\quent\\.openclaw\workspace\\data\\screenshots',
  minEngagement: {
    likes: 500,
    replies: 50,
    views: 10000
  },
  maxAgeHours: 6,  // Posts must be within 6 hours
  targetAccounts: [
    { handle: 'saylor', name: 'Michael Saylor', topics: ['BTC', 'MSTR', 'treasury'] },
    { handle: 'VitalikButerin', name: 'Vitalik', topics: ['ETH', 'tech', 'crypto'] },
    { handle: 'hims', name: 'Hims', topics: ['healthcare', 'GLP-1', 'telehealth'] },
    { handle: 'CryptoHayes', name: 'Arthur Hayes', topics: ['BTC', 'macro', 'trading'] },
    { handle: 'RaoulGMI', name: 'Raoul Pal', topics: ['macro', 'crypto', 'finance'] }
  ]
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true }).catch(() => {});
}

async function log(msg) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] ${msg}`);
}

async function loadQueue() {
  try {
    const data = await fs.readFile(CONFIG.queueFile, 'utf-8');
    return JSON.parse(data);
  } catch {
    return {
      discovered: [],
      drafted: [],
      posted: [],
      rejected: [],
      lastScan: null
    };
  }
}

async function saveQueue(queue) {
  await ensureDir(path.dirname(CONFIG.queueFile));
  queue.lastScan = new Date().toISOString();
  await fs.writeFile(CONFIG.queueFile, JSON.stringify(queue, null, 2));
}

// Check if post meets engagement criteria
function meetsCriteria(post) {
  if (!post.engagement) return false;
  
  // Check age
  const postAge = (Date.now() - new Date(post.timestamp).getTime()) / (1000 * 60 * 60);
  if (postAge > CONFIG.maxAgeHours) return false;
  
  // Check engagement
  return (
    (post.engagement.likes >= CONFIG.minEngagement.likes) ||
    (post.engagement.replies >= CONFIG.minEngagement.replies) ||
    (post.engagement.views >= CONFIG.minEngagement.views)
  );
}

// Calculate priority score
function calculatePriority(post) {
  const likes = post.engagement?.likes || 0;
  const replies = post.engagement?.replies || 0;
  const views = post.engagement?.views || 0;
  const age = (Date.now() - new Date(post.timestamp).getTime()) / (1000 * 60 * 60);
  
  // Higher score = more urgent to reply
  // Factor: likes * 1 + replies * 2 + views * 0.001 - age * 10
  const score = (likes * 1) + (replies * 2) + (views * 0.001) - (age * 10);
  
  return Math.round(score);
}

// Extract post data from browser (placeholder - would be automated)
async function scanTargetAccounts() {
  log('Scanning target accounts for high-engagement posts...');
  
  const discovered = [];
  
  // In real implementation, this uses browser automation
  // to visit each target profile and extract recent posts
  
  // For now, return example structure
  for (const account of CONFIG.targetAccounts) {
    log(`Checking @${account.handle}...`);
    // Browser automation would go here
    // discovered.push(...extractedPosts);
  }
  
  return discovered;
}

async function main() {
  log('=== X Reply Finder Starting ===');
  
  const queue = await loadQueue();
  
  // Scan for new posts
  const newPosts = await scanTargetAccounts();
  
  // Filter and add to queue
  let added = 0;
  for (const post of newPosts) {
    // Skip if already in queue
    const exists = queue.discovered.find(p => p.id === post.id);
    if (exists) continue;
    
    // Check criteria
    if (meetsCriteria(post)) {
      post.discoveredAt = new Date().toISOString();
      post.status = 'pending_draft';
      post.priority = calculatePriority(post);
      queue.discovered.push(post);
      added++;
      log(`Added: ${post.author} - ${post.text.substring(0, 50)}... (Priority: ${post.priority})`);
    }
  }
  
  // Sort by priority
  queue.discovered.sort((a, b) => b.priority - a.priority);
  
  await saveQueue(queue);
  log(`Added ${added} new posts to queue`);
  log(`Total pending: ${queue.discovered.length}`);
  log('=== X Reply Finder Complete ===');
  
  return { added, total: queue.discovered.length };
}

// Manual add function (for when you find posts yourself)
async function addPostManually(postData) {
  const queue = await loadQueue();
  
  const post = {
    id: `${postData.author}-${Date.now()}`,
    ...postData,
    discoveredAt: new Date().toISOString(),
    status: 'pending_draft',
    priority: calculatePriority(postData)
  };
  
  queue.discovered.push(post);
  queue.discovered.sort((a, b) => b.priority - a.priority);
  await saveQueue(queue);
  
  return post;
}

module.exports = {
  loadQueue,
  saveQueue,
  scanTargetAccounts,
  addPostManually,
  meetsCriteria,
  calculatePriority
};

// CLI usage
if (require.main === module) {
  main().catch(console.error);
}
