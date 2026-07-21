const fs = require('fs');
const path = require('path');

const opportunitiesDir = path.resolve('investment_fund/opportunities');
if (!fs.existsSync(opportunitiesDir)) fs.mkdirSync(opportunitiesDir, { recursive: true });

const scanFile = fs.readdirSync(opportunitiesDir)
  .filter(f => f.startsWith('scan_'))
  .sort()
  .pop();

if (!scanFile) {
  console.log('No scan file found');
  process.exit(1);
}

const raw = JSON.parse(fs.readFileSync(path.join(opportunitiesDir, scanFile), 'utf8'));
const data = raw.opportunities || raw;
const top3 = data.filter(o => (o.asymmetryScore || o.score) > 2.5).sort((a, b) => (b.asymmetryScore || b.score) - (a.asymmetryScore || a.score)).slice(0, 3);

console.log('TOP 3 QUEUED FOR REVIEW:');
top3.forEach((o, i) => {
  const score = o.asymmetryScore || o.score;
  const upside = typeof o.upside === 'number' ? o.upside.toFixed(1) : o.upside;
  console.log(`${i + 1}. ${o.ticker} | Score: ${score.toFixed(2)} | Upside: ${upside}% | Catalyst: ${o.catalyst}`);
});

const reviewQueue = path.join(opportunitiesDir, 'review_queue.json');
let queue = fs.existsSync(reviewQueue) ? JSON.parse(fs.readFileSync(reviewQueue, 'utf8')) : [];

let added = 0;
top3.forEach(o => {
  if (!queue.find(q => q.ticker === o.ticker)) {
    queue.push({ ...o, queuedAt: new Date().toISOString() });
    added++;
  }
});

fs.writeFileSync(reviewQueue, JSON.stringify(queue, null, 2));
console.log(`\nQueue updated: ${added} new entries. Total in queue: ${queue.length}`);
console.log(`File: ${reviewQueue}`);
