---
name: "x-automation-setup"
description: "Set up autonomous X/Twitter account using free tools: XActions, browser control, and n8n integration."
---

# X Automation Setup Skill

## Purpose
Set up and manage an autonomous X/Twitter account using only free/local tools.

## Prerequisites
- n8n installed (verified: v2.29.9 on this machine)
- Browser control working
- Shell access

## Free Methods (No Paid API)

### Method 1: Native Browser Control (Recommended Start)
- Use OpenClaw's built-in browser tool
- Twitter Web tool for research/drafting/publishing
- Cookie persistence via browser profile
- **Caveat:** X prefers API, higher detection risk — start low volume

### Method 2: XActions Toolkit (Strong Complement)
- GitHub: `nirholas/XActions`
- 100% free, open-source
- Browser scripts + CLI + MCP server
- No X API key needed
- OpenClaw executes via shell

### Method 3: n8n Hybrid Workflow
- OpenClaw triggers n8n webhooks
- n8n handles: research → content gen → formatting → posting
- Agent stays in control of decisions

## Guardrails (Mandatory)
1. **Human approval** for first N posts and sensitive topics
2. **Daily volume limit** — start low, increase with trust
3. **Log everything** — all posts tracked in memory
4. **No unauthorized spending** — free tools only
5. **Compliance** — follow X Automation Rules, avoid spam

## Account Setup Steps
1. Create dedicated X account manually
2. Bio: disclose it's automated, link to main account (@quentinvest1)
3. Enable "Automated" profile label if using API
4. Browser login with cookie persistence
5. Test with drafts first, then enable auto-posting

## Content Strategy
- Align with expertise: AI infrastructure, investing supercycle, HIMS/GLP-1, longevity
- Position as "AI agent perspective" or complementary to @quentinvest1
- Use local Ollama for content generation if available

## Implementation
```
1. Research XActions toolkit (git clone, install dependencies)
2. Test browser login to X (cookie-based)
3. Create n8n workflow: content gen → approval gate → posting
4. Set up heartbeat/cron for autonomous execution
5. Start with daily briefing posts, expand with replies
```

## Risks
- Browser methods: higher detection risk
- API free tier: too limited for meaningful posting
- Need to monitor X rule changes
- Cookie/session may expire — need refresh mechanism
