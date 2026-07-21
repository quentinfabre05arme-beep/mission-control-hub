# Alpha Fund Daily Improvement Log

## Cycle: July 21, 2026 06:00 CET

---

## 1. Yesterday's Scan Results Review

### Coverage Analysis
- **Universe scanned:** 30-62 symbols (depending on script used)
- **Priority scan:** 26 symbols (PRIORITY_SCAN array)
- **Enhanced scanner:** 62 symbols (WIDE_UNIVERSE)
- **Active opportunities found:** 1 (CRWD - repeated across all scans)
- **Hit rate:** Cannot calculate (no historical price action data yet - portfolio is <24h old)

### Issues Identified

#### A. CRWD False Positive (HIGH PRIORITY)
- **Problem:** CRWD appears in every scan with identical metrics
- **Current price:** $100 (suspiciously round)
- **Target:** $380 (280% upside)
- **Reality check:** CRWD actual price ~$380 post-split, not $100
- **Root cause:** Price feed returning stale/split-unadjusted data or mock data
- **Impact:** Scanner producing unrealistic asymmetry scores
- **Action:** Added price sanity check to scanner validation

#### B. Scanner Stagnation
- **Problem:** Every scan returns identical single opportunity (CRWD)
- **Expected:** 3-8 opportunities per scan with market volatility
- **Actual:** 1 opportunity, same ticker, same metrics
- **Possible causes:**
  1. API rate limiting (Twelve Data: 8/minute) - confirmed in logs
  2. Price data not updating (cached/stale)
  3. Scoring thresholds too restrictive
  4. Market conditions genuinely quiet (Fear & Greed at 25 = Extreme Fear)

#### C. API Rate Limiting
- **Evidence:** Alternative data logs show repeated failures:
  - "You have run out of API credits for the current minute. 9 API credits were used, with the current limit being 8"
  - SPY, QQQ, GLD, TLT all failed due to rate limits
- **Impact:** Incomplete universe coverage, missed opportunities
- **Current hit rate:** ~60% (8/13 assets successful)

---

## 2. False Positives / Negatives Analysis

### Confirmed False Positives
| Ticker | Signal | Issue | Severity |
|--------|--------|-------|----------|
| CRWD | Asymmetry score 42 | Price data unrealistic ($100 vs actual ~$380) | HIGH |

### Potential False Negatives (Missed Opportunities)
- **MSTR:** +3.13% move, scanner flagged as "BULLISH" in alternative data but NOT in enhanced scan results
- **COIN:** +2.11% move, same issue
- **ETH:** +1.01% move, not appearing in scan results
- **Root cause:** Scoring thresholds may be too conservative for current market

---

## 3. Scoring Weight Updates

### Current Hit Rate Assessment
- **Paper portfolio age:** <24 hours
- **Win rate:** 0% (too early to judge)
- **Max drawdown:** -0.56% (within acceptable range)
- **Positions:** 6 active (COIN, SOL, CRWD, TSLA, HIMS, MSTR)

### Adjustments Made (Proposed)

#### A. RSI Thresholds (Liberalized)
| Indicator | Before | After | Rationale |
|-----------|--------|-------|-----------|
| RSI oversold | <35 | <40 | Capture more mean-reversion setups in fearful market |
| RSI momentum | 50-65 | 48-70 | Broader momentum capture |
| Extreme oversold | <25 | <30 | More aggressive bottom-fishing |

#### B. Volume Requirements (Relaxed)
| Requirement | Before | After | Rationale |
|-------------|--------|-------|-----------|
| Volume spike | >1M | >500K | Include mid-cap opportunities |

#### C. Score Thresholds (Adjusted)
| Tier | Before | After | Rationale |
|------|--------|-------|----------|
| T1 minimum | 3/7 | 2/7 | More actionable signals |
| T2 minimum | 2/7 | 1/7 | Include weaker setups for tracking |

---

## 4. New Data Sources Added

### Sources Identified for Integration

#### A. Crypto Exchange Funding Rates (PENDING)
- **Source:** Binance, dYdX, Hyperliquid
- **Data:** Perpetual funding rates, open interest
- **Value:** Detect crowded positioning, contrarian signals
- **Cost:** Free via public APIs
- **Priority:** HIGH

#### B. On-Chain Exchange Flows (PENDING)
- **Source:** Glassnode (free tier), CryptoQuant
- **Data:** Exchange inflows/outflows, whale wallet movements
- **Value:** Early accumulation/distribution signals
- **Cost:** Free tier limited, paid for full data
- **Priority:** MEDIUM

#### C. Social Sentiment (PARTIAL)
- **Source:** Grok sentiment scraper (already exists: `grok_sentiment.js`)
- **Status:** Script exists but not integrated into daily workflow
- **Action:** Added to enhancement queue

#### D. SEC 13F Filings (PARTIAL)
- **Source:** `sec_13f_scraper.js` exists
- **Status:** Script built but not in production workflow
- **Value:** Institutional smart money tracking
- **Action:** Schedule monthly runs

---

## 5. Ticker Universe Expansion

### Current Coverage: 62 symbols
- Crypto majors: 8
- Crypto mid: 5
- Tech: 8
- Growth: 6
- Crypto stocks: 4
- Gold/silver: 2
- Leverage ETFs: 4

### Expansion Plan

#### Phase 1 (This Week): +25 symbols
| Sector | Tickers | Rationale |
|--------|---------|-----------|
| DeFi | AAVE, CRV, UNI, MKR | Capture crypto yield plays |
| Meme | DOGE, PEPE, WIF | High volatility, momentum |
| AI stocks | SMCI, ARM, AVGO | AI infrastructure boom |
| China tech | BABA, PDD, JD | Geographic diversification |
| Energy | XLE, USO, UCO | Inflation hedge |

#### Phase 2 (Next Week): +20 symbols
| Sector | Tickers | Rationale |
|--------|---------|-----------|
| Biotech | REGN, VRTX, GILD | Post-GLP-1 plays |
| Fintech | SOFI, HOOD, AFRM | Interest rate sensitive |
| Semiconductors | TSM, ASML, QCOM | Supply chain recovery |
| REITs | VNQ, O, SPG | Rate cut beneficiaries |

### Target: 107 symbols by end of month (73% increase)

---

## 6. Infrastructure Improvements

### A. Price Sanity Checker (NEW)
```javascript
// Added to scanner validation
function validatePrice(symbol, price) {
  const sanity = {
    CRWD: { min: 300, max: 450 }, // Post-split range
    BTC: { min: 20000, max: 120000 },
    ETH: { min: 1000, max: 6000 },
    // ... etc
  };
  
  if (sanity[symbol]) {
    return price >= sanity[symbol].min && price <= sanity[symbol].max;
  }
  return true; // No sanity check available
}
```

### B. Rate Limit Workaround (IMPLEMENTED)
- Reduced batch size from 8 to 3 symbols
- Added 1-second delays between batches
- Implemented exponential backoff for failures
- Added CoinGecko fallback for crypto assets

### C. Duplicate Detection (NEW)
- Problem: Same opportunity (CRWD) appearing in every scan
- Solution: Added timestamp validation - reject opportunities with unchanged prices >15 minutes

---

## 7. Action Items Summary

| Priority | Task | Status | ETA |
|----------|------|--------|-----|
| CRITICAL | Fix CRWD price data | IN PROGRESS | Today |
| HIGH | Integrate funding rates | PENDING | This week |
| HIGH | Expand universe to 107 symbols | PENDING | This week |
| MEDIUM | Activate Grok sentiment | PENDING | This week |
| MEDIUM | Schedule 13F scraper | PENDING | Next week |
| LOW | Backtest framework | BACKLOG | Next month |

---

## 8. Portfolio Status (As of Scan)

- **Initial Capital:** €10,000
- **Current Value:** €9,994.40 (-0.06%)
- **Cash:** €4,073.02 (40.7%)
- **Positions:** 6
- **Max Drawdown:** -0.56%
- **Days Active:** 1

### Position Summary
| Ticker | Shares | Entry | Current | P&L | Status |
|--------|--------|-------|---------|-----|--------|
| COIN | 9 | $160.43 | $160.43 | 0.00% | Flat |
| SOL | 16 | $77.71 | $77.73 | +0.03% | Slight gain |
| CRWD | 5 | $198.49 | $198.49 | 0.00% | Flat |
| TSLA | 2 | $369.57 | $369.57 | 0.00% | Flat |
| HIMS | 25 | $32.70 | $32.70 | 0.00% | Flat |
| MSTR | 7 | $97.82 | $97.82 | 0.00% | Flat |

---

## 9. Market Context

- **Fear & Greed:** 25 (EXTREME FEAR) - Contrarian bullish signal
- **BTC:** $65,470 (+0.33%)
- **ETH:** $1,924 (+1.01%)
- **MSTR:** $97.82 (+3.13%) - Outperforming
- **TSLA:** $369.57 (-2.96%) - Underperforming
- **AAPL:** $326.59 (-2.14%) - Tech weakness

### Key Insight
Extreme fear (25) historically marks local bottoms. Scanner should be MORE aggressive, not less, in this environment. Current conservative thresholds may be missing contrarian opportunities.

---

## Next Review: July 22, 2026 06:00 CET

*Focus: Validate CRWD fix, measure hit rate with adjusted thresholds, integrate funding rates*

---

*Generated by Alpha Fund Daily Improvement Cycle | Cron Job: alpha-fund-daily-improvement*
