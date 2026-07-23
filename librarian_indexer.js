const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Load existing index
let index;
try {
    index = JSON.parse(fs.readFileSync('content_index.json', 'utf8'));
} catch (e) {
    index = {
        metadata: { version: '1.0', created: new Date().toISOString(), last_updated: new Date().toISOString(), total_files_indexed: 0, batch_number: 0 },
        files: [],
        topics: { investment: [], pod_business: [], mission_control: [], development: [], data_analysis: [], configuration: [], social_media: [], automation: [], security: [], system_maintenance: [], personal: [], uncategorized: [] },
        statistics: { by_extension: {}, by_topic: {}, total_size_bytes: 0, failed_reads: 0, skipped_binaries: 0, encoding_fallbacks: { utf8: 0, utf16: 0, ascii: 0, unreadable: 0 } }
    };
}

// Load scanned files
const scannedFiles = JSON.parse(fs.readFileSync('librarian_files.json', 'utf8'));
const existingPaths = new Set(index.files.map(f => f.path));

// Topic detection keywords
const TOPIC_KEYWORDS = {
    investment: ['investment', 'portfolio', 'trading', 'market', 'fund', 'alpha', 'stock', 'crypto', 'btc', 'eth', 'mstr', 'hims', 'price'],
    mission_control: ['mission', 'dashboard', 'control', 'review', 'cycle', 'monitor', 'status', 'deployment', 'vercel'],
    development: ['code', 'script', 'function', 'class', 'api', 'module', 'pipeline', 'python', 'javascript', 'nodejs'],
    data_analysis: ['analysis', 'data', 'metrics', 'analytics', 'chart', 'graph', 'json', 'csv', 'report'],
    automation: ['automation', 'cron', 'scheduler', 'workflow', 'bot', 'daemon', 'autonomous'],
    social_media: ['twitter', 'x_post', 'social', 'post', 'content', 'engagement', 'impression', 'follower'],
    configuration: ['config', 'settings', 'setup', 'env', '.env', 'json', 'yaml'],
    security: ['security', 'auth', 'password', 'encrypt', 'key', 'token', 'secret'],
    system_maintenance: ['maintenance', 'cleanup', 'backup', 'sync', 'update', 'upgrade'],
    personal: ['USER.md', 'personal', 'private', 'notes']
};

function detectTopics(content, filename) {
    const topics = [];
    const lowerContent = content.toLowerCase();
    const lowerFile = filename.toLowerCase();
    
    for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
        if (keywords.some(k => lowerContent.includes(k) || lowerFile.includes(k))) {
            topics.push(topic);
        }
    }
    
    return topics.length > 0 ? topics : ['uncategorized'];
}

function extractKeyPhrases(content) {
    // Simple word frequency
    const words = content.toLowerCase()
        .replace(/[^\w\s]/g, ' ')
        .split(/\s+/)
        .filter(w => w.length > 3 && !['this', 'that', 'with', 'from', 'have', 'been', 'were', 'they', 'their', 'there'].includes(w));
    
    const freq = {};
    words.forEach(w => freq[w] = (freq[w] || 0) + 1);
    
    return Object.entries(freq)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([word]) => word);
}

function computeHash(content) {
    return crypto.createHash('md5').update(content).digest('hex').substring(0, 16);
}

function readFileWithFallback(filePath) {
    const attempts = ['utf8', 'utf16le', 'ascii'];
    for (const encoding of attempts) {
        try {
            const content = fs.readFileSync(filePath, { encoding });
            return { content, encoding };
        } catch (e) {}
    }
    return null;
}

// Find new files
const newFiles = scannedFiles.filter(f => !existingPaths.has(f.path)).slice(0, 50);
const indexed = [];
const failed = [];

console.log(`Found ${newFiles.length} new files to index`);

for (const file of newFiles) {
    const result = readFileWithFallback(file.path);
    
    if (result) {
        const content = result.content;
        const summary = content.replace(/\s+/g, ' ').substring(0, 200).trim();
        const keyPhrases = extractKeyPhrases(content);
        const topics = detectTopics(content, file.path);
        const hash = computeHash(content);
        
        const entry = {
            path: file.path,
            size: file.size,
            mtime: file.mtime,
            summary,
            key_phrases: keyPhrases,
            topics,
            hash,
            indexed: new Date().toISOString(),
            encoding: result.encoding
        };
        
        index.files.push(entry);
        indexed.push(entry);
        
        // Update statistics
        index.statistics.by_extension[file.ext] = (index.statistics.by_extension[file.ext] || 0) + 1;
        index.statistics.total_size_bytes += file.size;
        index.statistics.encoding_fallbacks[result.encoding === 'utf8' ? 'utf8' : result.encoding === 'utf16le' ? 'utf16' : 'ascii']++;
        
        for (const topic of topics) {
            index.statistics.by_topic[topic] = (index.statistics.by_topic[topic] || 0) + 1;
            if (!index.topics[topic]) index.topics[topic] = [];
            if (!index.topics[topic].includes(file.path)) {
                index.topics[topic].push(file.path);
            }
        }
        
        console.log(`✓ Indexed: ${file.path}`);
    } else {
        index.statistics.failed_reads++;
        index.statistics.encoding_fallbacks.unreadable++;
        failed.push(file.path);
        console.log(`✗ Failed: ${file.path}`);
    }
}

// Update metadata
index.metadata.last_updated = new Date().toISOString();
index.metadata.total_files_indexed = index.files.length;
index.metadata.batch_number = (index.metadata.batch_number || 0) + 1;
index.metadata.last_batch_size = indexed.length;

// Save index
fs.writeFileSync('content_index.json', JSON.stringify(index, null, 2));

// Log results
console.log(`\n=== Indexing Complete ===`);
console.log(`Total indexed: ${index.files.length}`);
console.log(`New this batch: ${indexed.length}`);
console.log(`Failed: ${failed.length}`);
console.log(`Failed files: ${failed.join(', ')}`);
