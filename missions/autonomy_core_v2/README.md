# Autonomy Core v2.0 - System Architecture

## Overview
Enhanced Autonomy Core v2.0 is a self-improving, revenue-aware, opportunity-scanning, decision-making system with self-healing error recovery. All decisions are logged to MEMORY.md.

## System Components

### 1. Self-Improvement Loop (`self_improvement_loop.js`)
**Purpose:** Continuous self-improvement using the 5-step Detect → Analyze → Solve → Verify → Document pattern.

**Key Features:**
- Detect phase: Checks prerequisites and recent errors
- Analyze phase: Pattern matching for known issues
- Solve phase: Executes with adapted strategy
- Verify phase: Confirms success criteria
- Document phase: Logs to MEMORY.md and daily files
- Exponential backoff between attempts
- Configurable max attempts (default: 5)

**Usage:**
```javascript
const loop = new SelfImprovementLoop();
await loop.execute('Task description', async (context) => {
  // Action to execute
  return result;
});
```

### 2. Revenue Tracker (`revenue_tracker.js`)
**Purpose:** Tracks all revenue streams, costs, and profitability.

**Categories:**
- **Investments:** Crypto trading, stock trading, dividends
- **Business:** Consulting, products, services
- **Passive:** Ads, affiliates, subscriptions

**Key Features:**
- Daily and monthly aggregation
- Profit margin calculation
- Revenue stream health monitoring
- Automatic MEMORY.md logging

**Usage:**
```javascript
const tracker = new RevenueTracker();
tracker.recordRevenue('investments', 'crypto_trading', 150.50, { asset: 'BTC' });
tracker.recordCost('infrastructure', 'apis', 25.00);
console.log(tracker.generateReport());
```

### 3. Opportunity Scanner (`opportunity_scanner.js`)
**Purpose:** Scans for investment and business opportunities.

**Categories:**
- **Crypto:** Dip buying, volume spikes
- **Stocks:** Sector momentum, fundamentals
- **Business:** Online opportunities, arbitrage, emerging sectors

**Scoring Algorithm:**
```
Composite = ROI*0.30 + Risk*0.25 + Effort*0.20 + Timing*0.15 + Alignment*0.10
Grades: A (>0.7), B (>0.5), C (>0.3), D (<0.3)
```

**Usage:**
```javascript
const scanner = new OpportunityScanner();
const results = await scanner.fullScan({ crypto: { BTC: { change_24h: -12 } } });
```

### 4. Auto-Pilot Decision Matrix (`decision_matrix.js`)
**Purpose:** Makes autonomous decisions based on weighted scoring.

**Decision Thresholds:**
- **AUTO_APPROVE (≥0.75):** No human review needed
- **CONDITIONAL_APPROVE (≥0.50):** Proceed with logging
- **REVIEW_REQUIRED (≥0.30):** Human review recommended
- **AUTO_REJECT (<0.20):** Auto-reject

**Criteria Weights:**
- ROI: 25%
- Risk: 20%
- Urgency: 20%
- Effort: 15%
- Alignment: 10%
- Confidence: 10%

**Usage:**
```javascript
const matrix = new DecisionMatrix();
const decision = matrix.evaluate({
  type: 'crypto_trade',
  roi: 25,
  risk: 4,
  urgency: 7,
  effort: 2,
  confidence: 0.8
});
```

### 5. Self-Healing Error Recovery (`error_recovery.js`)
**Purpose:** 5-attempt minimum recovery with progressive strategies.

**Error Categories:**
- Network (ECONNREFUSED, timeout)
- Rate Limit (429, throttled)
- Auth (401, 403)
- Data (parse errors)
- Unknown (fallback)

**Recovery Strategies per Category (5 minimum):**
1. Simple retry with delay
2. Exponential backoff
3. Alternative approach/endpoint
4. Circuit breaker pattern
5. Fallback/cached data

**Usage:**
```javascript
const recovery = new ErrorRecovery();
const result = await recovery.recover(error, async (context) => {
  return await operation(context);
}, context);
```

### 6. Integration Hub (`autonomy_core.js`)
**Purpose:** Main entry point connecting all subsystems.

**Cycle Phases:**
1. Self-Improvement Check
2. Revenue Tracking
3. Opportunity Scan
4. Decision Evaluation
5. Error Recovery Check

## File Structure
```
missions/autonomy_core_v2/
├── autonomy_core.js           # Integration hub (main entry)
├── self_improvement_loop.js   # Self-improvement engine
├── revenue_tracker.js         # Revenue/cost tracking
├── opportunity_scanner.js     # Opportunity detection
├── decision_matrix.js          # Auto-pilot decisions
├── error_recovery.js           # Self-healing recovery
├── logs/                       # Runtime logs
│   ├── cycles.log
│   ├── decisions.log
│   ├── self_improvement.log
│   ├── recovery.log
│   └── executions.log
└── data/                       # Persistent data
    ├── revenue.json
    ├── decisions.json
    └── error_patterns.json
```

## Integration with MEMORY.md
All decisions are automatically logged to MEMORY.md with:
- Timestamp
- Decision type and scores
- Rationale
- Outcome

## Quick Start
```bash
# Initialize
cd missions/autonomy_core_v2
node autonomy_core.js

# Run a full cycle
node -e "const Core = require('./autonomy_core'); const c = new Core(); c.initialize().then(() => c.runCycle())"

# Test individual components
node self_improvement_loop.js
node revenue_tracker.js
node opportunity_scanner.js
node decision_matrix.js
node error_recovery.js
```

## Architecture Diagram
```
┌─────────────────────────────────────┐
│        Autonomy Core v2.0           │
│        (Integration Hub)            │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┬──────────┐
    │          │          │          │
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Self-  │ │Revenue │ │Decision│ │ Error  │
│Improve-│ │Tracker │ │ Matrix │ │Recovery│
│ ment   │ │        │ │        │ │        │
└────────┘ └────────┘ └────────┘ └────────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
               │
               ▼
        ┌────────────┐
        │ Opportunity│
        │  Scanner   │
        └────────────┘
               │
               ▼
          MEMORY.md
```

## Status
✅ All 6 components created and operational
✅ All decisions log to MEMORY.md
✅ 5-attempt minimum error recovery
✅ Revenue tracking with multi-category support
✅ Opportunity scanning with composite scoring
✅ Decision matrix with approval thresholds
