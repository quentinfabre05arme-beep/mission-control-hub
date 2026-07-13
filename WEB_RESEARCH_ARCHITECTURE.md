# Web Research Pipeline Architecture

## Overview

Automated daily research and content generation system using web search.
No browser automation required - reliable and maintainable.

## File Structure

```
workspace/
├── web_research_pipeline.py      # Main research engine
├── operations/
│   └── research/
│       └── research_YYYY-MM-DD.json    # Daily research data
├── daily_content/
│   └── YYYY-MM-DD_briefing.txt         # Generated briefings
└── MEMORY.md                    # System documentation
```

## Daily Workflow

### 8:00 AM - Research Phase
1. Trigger: Cron job runs `web_research_pipeline.py`
2. Action: Compile research queries for 3 pillars
3. Output: `research/YYYY-MM-DD.json`

### 8:05 AM - Search Phase
1. Web search for each query
2. Extract key insights
3. Compile findings

### 8:10 AM - Content Generation
1. Generate 3 posts from research
2. Apply content templates
3. Save to `daily_content/`

### 8:15 AM - Delivery
1. Send briefing to user
2. Include copy/paste ready posts
3. Clear instructions for posting

## Content Pillars

### 1. ETH Treasury
**Queries:**
- ETH treasury institutional adoption
- Ethereum corporate treasury
- ETH staking yield treasury
- Bitmine ETH holdings

**Sources:** X, CoinDesk, Cointelegraph, The Block

### 2. HIMS Healthcare
**Queries:**
- HIMS stock news
- Hims Hers Health GLP-1
- Telehealth infrastructure
- GLP-1 market HIMS

**Sources:** X, Bloomberg, CNBC, FierceHealthcare

### 3. AI Agentic Commerce
**Queries:**
- AI agentic commerce
- Autonomous agents McKinsey
- NBIS ZETA PLTR AI
- MCP A2A protocol

**Sources:** X, TechCrunch, VentureBeat, McKinsey

## Automation

### Cron Job (Single)
```
Name: web-research-daily
Schedule: 0 8 * * * (8:00 AM daily)
Action: python web_research_pipeline.py
Output: Telegram message with briefing
```

### Manual Triggers
- `python web_research_pipeline.py` - Run immediately
- `python web_research_pipeline.py --topic eth` - Research specific topic

## Content Templates

### Single Post Template
```
[Thesis statement with hook]

[Data point 1]
[Data point 2]
[Data point 3]

[Conclusion/Call to action]

#hashtag1 #hashtag2 #hashtag3
```

### Thread Template
```
[Tweet 1/5]: Hook thesis

[Tweet 2/5]: Data/context

[Tweet 3/5]: Analysis

[Tweet 4/5]: Implications

[Tweet 5/5]: Conclusion + CTA
```

## Future Enhancements

### Phase 2: Grok Integration
- Browser automation for X-specific data
- Real-time sentiment analysis
- Trend detection

### Phase 3: Advanced Analytics
- Engagement prediction
- Optimal timing
- A/B testing content

## Status

**Current:** Basic structure created, ready for web search integration
**Next:** Implement actual web search API calls
**Target:** Full automation by end of week

---
Last Updated: 2026-07-12
