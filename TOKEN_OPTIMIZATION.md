# Token Optimization Guide for Ollama Cloud Max

## Current Situation
- Model: ollama-cloud/kimi-k2.5:cloud (switched from k2.6)
- Status: 2.3M tokens used
- Issue: Cron jobs spawning subagents burn tokens rapidly

## Optimizations Implemented

### 1. Model Switching
- Primary: ollama-cloud/kimi-k2.5:cloud (lighter than k2.6)
- Fallback: ollama-cloud/kimi-k2.5:cloud (same, avoids fallback token burn)
- Avoid: k2.6 (heavy), k2.7-code (very heavy)

### 2. Cron Job Optimization
**Before:**
- x-autonomous-poster: agentTurn every 30 min (~50K tokens/run)
- mission-control-improvements: agentTurn every 15 min (~30K tokens/run)

**After:**
- x-autonomous-poster: Windows Task Scheduler (0 tokens)
- mission-control-improvements: Disabled (0 tokens)
- x-post-reminder: systemEvent only (0 tokens)
- x-daily-briefing: Kept agentTurn at 08:00 only (~2K tokens/day)

### 3. Session-Level Optimizations

**Use Fast Mode for simple tasks:**
- File operations
- System checks
- Script execution
- Log reading

**Use Standard Mode for:**
- Content generation
- Complex reasoning
- Multi-step tasks

**Use Reasoning Mode for:**
- Debugging
- Architecture decisions
- Complex problem solving

### 4. Context Management
- Set context limits to 100K tokens max
- Enable aggressive compaction
- Flush memory before heavy operations

### 5. Token-Saving Patterns

**DO:**
- Use systemEvent for reminders
- Use exec for script execution
- Batch file operations
- Use subagents only for parallel tasks

**DON'T:**
- Spawn subagents for simple tasks
- Run agentTurn cron jobs frequently
- Use heavy models for script execution
- Keep long context windows

## Expected Savings
- Before: ~700K tokens/day
- After: ~50K tokens/day
- Savings: ~93% reduction

## Monitoring
- Check /status regularly
- Monitor token usage in logs
- Alert if usage exceeds 100K/day
