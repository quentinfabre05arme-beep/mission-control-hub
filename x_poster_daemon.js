const fs = require('fs');
const path = require('path');

// Read queue
const queueFile = path.join(__dirname, 'x_queue.json');
const logFile = path.join(__dirname, 'logs', 'x_posts.log');

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(logFile, line);
  console.log(line.trim());
}

// Read pending posts
function getPendingPosts() {
  if (!fs.existsSync(queueFile)) return [];
  const queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
  return queue.filter(p => p.status === 'pending');
}

// Mark post as posted
function markPosted(postId) {
  const queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
  const post = queue.find(p => p.id === postId);
  if (post) {
    post.status = 'posted';
    post.postedAt = new Date().toISOString();
    fs.writeFileSync(queueFile, JSON.stringify(queue, null, 2));
    log(`Post ${postId} marked as posted`);
  }
}

// Main: attempt to post via browser automation
async function postViaBrowser(text) {
  log(`Attempting browser post: "${text.substring(0, 50)}..."`);
  
  // For now, we log the attempt. The actual browser automation
  // will be added once we have a reliable CDP connection.
  // This is a placeholder for the real implementation.
  
  log('Browser automation placeholder — CDP connection needed');
  return false;
}

async function main() {
  log('=== X Poster Daemon Started ===');
  
  const pending = getPendingPosts();
  log(`Found ${pending.length} pending posts`);
  
  for (const post of pending.slice(0, 1)) { // Post one at a time
    const success = await postViaBrowser(post.text);
    if (success) {
      markPosted(post.id);
    } else {
      log(`Failed to post ${post.id}, will retry later`);
    }
  }
  
  log('=== Done ===');
}

main().catch(err => {
  log(`Error: ${err.message}`);
  process.exit(1);
});