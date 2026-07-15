/**
 * OpenClaw X Autonomous Poster
 * Posts to @quentinvest1 using browser automation via CDP
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  username: 'quentinvest1',
  cdpPort: 18800,
  logFile: path.join(__dirname, 'logs', 'x_posts.log'),
  sessionFile: path.join(__dirname, 'x_session', 'cookies.json'),
  maxDailyPosts: 3,
  postTimes: ['08:00', '14:00', '19:00'], // Paris time
};

// Ensure log directory exists
const logDir = path.dirname(CONFIG.logFile);
if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

function log(message) {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] ${message}\n`;
  fs.appendFileSync(CONFIG.logFile, line);
  console.log(line.trim());
}

// Content generation (simplified — will be replaced with AI generation)
function generatePost() {
  const templates = [
    "The AI infrastructure build-out is just getting started. We're still in the infrastructure phase — models, compute, data pipelines. The application layer comes next.",
    "BTC at $62K. ETH at $1.78K. The consolidation continues. Patience is the only edge in macro.",
    "GLP-1 drugs aren't just about weight loss. They're about metabolic health, inflammation, and longevity. HIMS at $34 is a bet on healthcare infrastructure.",
    "Every AI agent will need a MCP (Model Context Protocol) layer. Standardization wins. The protocol layer is where value accrues.",
    "Longevity isn't science fiction anymore. It's an engineering problem. The companies solving it will be the next trillion-dollar market cap stories."
  ];
  return templates[Math.floor(Math.random() * templates.length)];
}

// Main posting function using fetch to internal API
async function postToX(text) {
  log(`Attempting to post: "${text.substring(0, 50)}..."`);
  
  try {
    // Try to use OpenClaw's built-in browser or external tool
    // For now, log the intent and queue for posting
    const queueFile = path.join(__dirname, 'x_queue.json');
    let queue = [];
    if (fs.existsSync(queueFile)) {
      queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
    }
    
    queue.push({
      text,
      timestamp: new Date().toISOString(),
      status: 'pending',
      id: Date.now()
    });
    
    fs.writeFileSync(queueFile, JSON.stringify(queue, null, 2));
    log(`Post queued successfully. Queue size: ${queue.length}`);
    return true;
    
  } catch (err) {
    log(`Error queuing post: ${err.message}`);
    return false;
  }
}

// Check if we should post now
function shouldPostNow() {
  const now = new Date();
  const hour = now.getHours().toString().padStart(2, '0');
  const minute = now.getMinutes().toString().padStart(2, '0');
  const timeStr = `${hour}:${minute}`;
  
  // Check if it's within 5 minutes of a post time
  return CONFIG.postTimes.some(t => {
    const [h, m] = t.split(':');
    const targetMin = parseInt(h) * 60 + parseInt(m);
    const currentMin = parseInt(hour) * 60 + parseInt(minute);
    return Math.abs(targetMin - currentMin) <= 5;
  });
}

// Count posts today
function getTodaysPostCount() {
  const queueFile = path.join(__dirname, 'x_queue.json');
  if (!fs.existsSync(queueFile)) return 0;
  
  const queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
  const today = new Date().toDateString();
  return queue.filter(p => new Date(p.timestamp).toDateString() === today).length;
}

// Main loop
async function main() {
  log('=== X Autonomous Poster Started ===');
  
  // DEBUG: Force post regardless of time
  const forcePost = process.argv.includes('--force');
  
  if (!forcePost && !shouldPostNow()) {
    log('Not a scheduled posting time. Use --force to override.');
    return;
  }
  
  const todayCount = getTodaysPostCount();
  if (todayCount >= CONFIG.maxDailyPosts) {
    log(`Daily limit reached (${todayCount}/${CONFIG.maxDailyPosts}). Exiting.`);
    return;
  }
  
  const post = generatePost();
  await postToX(post);
  
  log('=== Done ===');
}

// Run
main().catch(err => {
  log(`Fatal error: ${err.message}`);
  process.exit(1);
});
