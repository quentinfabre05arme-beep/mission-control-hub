---
name: "heartbeat-v2"
description: "Proactive heartbeat automation with self-triggered research and action loops without manual intervention"
---

# Heartbeat v2

Replaces placeholder heartbeat with actual automated value generation. Self-triggers work based on configurable rules without waiting for human instructions.

## Triggers

- **Scheduled:** Every 30 minutes via cron
- **Event-Driven:** On file changes, API updates, thresholds
- **Opportunity-Based:** When conditions match patterns

## Automation Rules

### Rule 1: Market Opportunity Detection
```
IF (BTC price change > 3% in 1 hour)
AND (sentiment score > 0.7)
THEN generate_analysis_report()
AND queue_social_post()
```

### Rule 2: Content Pipeline Check
```
IF (scheduled_posts < 3 for next 24h)
THEN trigger_content_generation()
AND populate_queue()
```

### Rule 3: Dashboard Health
```
IF (any dashboard returns non-200)
THEN auto_diagnose()
AND attempt_fix()
AND notify_if_unresolved()
```

### Rule 4: Research Cycle Trigger
```
IF (time_since_last_cycle > 6 hours)
AND (high_priority_sources_updated)
THEN start_research_cycle()
```

## Implementation

```javascript
// heartbeat_v2.js
const rules = [
  { name: "market-opportunity", check: checkMarket, action: generateAnalysis },
  { name: "content-pipeline", check: checkQueue, action: generateContent },
  { name: "dashboard-health", check: checkDashboards, action: repairDashboard },
  { name: "research-cycle", check: checkResearch, action: startResearch }
];

async function heartbeat() {
  for (const rule of rules) {
    if (await rule.check()) {
      await rule.action();
    }
  }
}
```

## Configuration

```json
{
  "intervalMinutes": 30,
  "maxActionsPerBeat": 3,
  "silentMode": true,
  "notifyOn": ["error", "opportunity", "completion"]
}
```

## Logging

- Actions taken: `logs/heartbeat/YYYY-MM-DD.log`
- Decisions made: `logs/heartbeat/decisions.log`
- Performance: execution time per rule

## Safety

- Max 3 actions per heartbeat to prevent loops
- All actions logged before execution
- Human approval required for spending/external posts
- Circuit breaker on repeated failures
