---
name: "cron-optimizer"
description: "Optimize cron jobs quarterly: audit, remove duplicates, reduce token burn, set silent self-healing mode."
---

# Cron Optimizer Skill

## Purpose
Audit and optimize cron jobs to minimize token burn while maintaining system reliability. Remove duplicates, useless jobs, and set smart alerting.

## Trigger
- User mentions "cron", "scheduled tasks", "token usage", "too many messages"
- Quarterly heartbeat (every 90 days)
- System maintenance check finds duplicate or failing jobs

## Anti-Patterns to Kill
| Pattern | Why | Action |
|---------|-----|--------|
| Heartbeat every 15 min with no action | 6ms runtime, does nothing | Delete |
| Self-improvement research outputting v3.0 when system is v7.6 | Stale data, wrong version | Delete |
| Duplicate dashboard review jobs | Same task, different names | Merge into one |
| API check that always reports green | Alert fatigue | Make silent unless broken |
| Job that always fails same way | Broken, not fixing itself | Disable and alert user |

## Optimization Rules
1. **Max 3-4 cron jobs** for routine maintenance
2. **Silent by default** — only alert when something needs user action
3. **Self-healing** — fix what you can without asking
4. **Quarterly review** — audit all jobs, remove dead weight

## Ideal Minimal Setup
| Job | Schedule | Behavior |
|-----|----------|----------|
| Daily briefing | 08:00 daily | Always sends — core value |
| System maintenance | Every 6 hours | Silent self-healing |
| Memory maintenance | Every 2 hours | Silent unless significant |

## Token Burn Calculation
- Estimate: ~400-650K tokens/day with bloated cron
- Target: ~30-50K tokens/day with optimized cron
- Savings: ~350-600K tokens/day (~90% reduction)

## Implementation
```bash
# Audit
cron action=list

# For each job:
# - Check lastRunStatus
# - Check lastDurationMs (if <100ms, probably useless)
# - Check diagnosticSummary for repeated errors
# - Ask: does this provide value to the user?

# Remove useless
cron action=remove jobId=<id>

# Merge duplicates
cron action=update jobId=<id> patch={"enabled":false}

# Make silent
cron action=update jobId=<id> patch={"payload":{"message":"...SILENTLY. Only report if broken..."}}
```
