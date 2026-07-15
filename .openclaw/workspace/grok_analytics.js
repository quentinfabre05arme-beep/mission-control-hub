// grok_analytics.js - Grok API integration for X analytics
// Requires xAI API key for Grok

const CONFIG = {
  apiKey: process.env.GROK_API_KEY || process.env.XAI_API_KEY,
  baseUrl: 'https://api.x.ai/v1',
  model: 'grok-3-beta'
};

async function log(msg) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

async function grokRequest(messages, temperature = 0.7) {
  if (!CONFIG.apiKey) {
    throw new Error('GROK_API_KEY not configured');
  }
  
  const response = await fetch(`${CONFIG.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CONFIG.apiKey}`
    },
    body: JSON.stringify({
      model: CONFIG.model,
      messages: messages,
      temperature: temperature,
      max_tokens: 1024
    })
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Grok API error: ${response.status} - ${error}`);
  }
  
  const data = await response.json();
  return data.choices[0].message.content;
}

// Analyze post performance with Grok
async function analyzePostPerformance(post) {
  log(`Analyzing post: ${post.id}`);
  
  const prompt = `
Analyze this X post performance:

Post text: "${post.text}"
Views: ${post.views}
Likes: ${post.likes}
Reposts: ${post.reposts}
Replies: ${post.replies}
Posted: ${post.timestamp}

Provide:
1. Engagement quality (why it performed well/poorly)
2. What worked in the content
3. What could be improved
4. Audience reaction assessment
5. Recommendation for next similar post

Be concise but specific.`;

  const analysis = await grokRequest([
    { role: 'system', content: 'You are an X/Twitter analytics expert specializing in crypto and finance content.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    postId: post.id,
    timestamp: new Date().toISOString(),
    analysis: analysis
  };
}

// Analyze trending topics
async function analyzeTrends(topic) {
  log(`Analyzing trends for: ${topic}`);
  
  const prompt = `
What are the current trends and sentiment around "${topic}" on X/Twitter?

Focus on:
1. Key narratives driving discussion
2. Sentiment (bullish/bearish/neutral)
3. Notable accounts talking about it
4. Emerging sub-topics
5. Opportunity for content creation

Provide actionable insights for someone posting about ${topic}.`;

  const trends = await grokRequest([
    { role: 'system', content: 'You are a social media trend analyst specializing in crypto and finance.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    topic: topic,
    timestamp: new Date().toISOString(),
    trends: trends
  };
}

// Compare to competitor
async function compareToCompetitor(yourPost, competitorPost) {
  log('Comparing posts...');
  
  const prompt = `
Compare these two X posts:

YOUR POST:
"${yourPost.text}"
Engagement: ${yourPost.likes} likes, ${yourPost.reposts} reposts, ${yourPost.views} views

COMPETITOR POST:
"${competitorPost.text}"
Engagement: ${competitorPost.likes} likes, ${competitorPost.reposts} reposts, ${competitorPost.views} views

What can you learn from their approach?
What are they doing differently?
How to improve your content?`;

  const comparison = await grokRequest([
    { role: 'system', content: 'You are a competitive content strategist.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    timestamp: new Date().toISOString(),
    comparison: comparison
  };
}

// Content optimization
async function optimizeContent(draftPost) {
  log('Optimizing content...');
  
  const prompt = `
Optimize this X post for maximum engagement:

Draft: "${draftPost}"

Audience: Finance, crypto, and healthcare investors
Style: Data-driven, thesis-first, no hype

Provide:
1. Improved version with hook
2. Alternative angles (2-3 options)
3. Hashtag recommendations
4. Best time to post this content
5. Thread potential (should this be a thread?)`;

  const optimization = await grokRequest([
    { role: 'system', content: 'You are an X copywriter specializing in high-performing finance content.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    original: draftPost,
    timestamp: new Date().toISOString(),
    optimization: optimization
  };
}

// Sentiment analysis of replies
async function analyzeSentiment(replies) {
  log('Analyzing sentiment...');
  
  const repliesText = replies.map(r => r.text).join('\n---\n');
  
  const prompt = `
Analyze the sentiment of these X replies:

${repliesText}

Provide:
1. Overall sentiment (positive/negative/neutral with %)
2. Common themes in replies
3. Quality of engagement (thoughtful vs shallow)
4. Any concerns or praise patterns
5. How to respond strategically`;

  const sentiment = await grokRequest([
    { role: 'system', content: 'You are a sentiment analysis expert for social media engagement.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    timestamp: new Date().toISOString(),
    sentiment: sentiment
  };
}

// Best time to post calculation
async function calculateBestTime(historicalPosts) {
  log('Calculating optimal posting time...');
  
  const postsData = JSON.stringify(historicalPosts.map(p => ({
    timestamp: p.timestamp,
    engagementRate: p.engagementRate,
    dayOfWeek: new Date(p.timestamp).toLocaleDateString('en-US', { weekday: 'long' }),
    hour: new Date(p.timestamp).getHours()
  })));
  
  const prompt = `
Based on these historical post performances:

${postsData}

Calculate:
1. Best day of week to post
2. Best time of day
3. Worst performing times (avoid)
4. Pattern explanation

Return specific recommendations for next week.`;

  const bestTime = await grokRequest([
    { role: 'system', content: 'You are a social media timing strategist using data analysis.' },
    { role: 'user', content: prompt }
  ]);
  
  return {
    timestamp: new Date().toISOString(),
    recommendation: bestTime
  };
}

module.exports = {
  analyzePostPerformance,
  analyzeTrends,
  compareToCompetitor,
  optimizeContent,
  analyzeSentiment,
  calculateBestTime
};

// CLI usage
if (require.main === module) {
  const command = process.argv[2];
  const arg = process.argv[3];
  
  switch(command) {
    case 'analyze':
      analyzePostPerformance(JSON.parse(arg)).then(console.log).catch(console.error);
      break;
    case 'trends':
      analyzeTrends(arg).then(console.log).catch(console.error);
      break;
    case 'optimize':
      optimizeContent(arg).then(console.log).catch(console.error);
      break;
    default:
      console.log('Usage: node grok_analytics.js [analyze|trends|optimize] [data]');
  }
}
