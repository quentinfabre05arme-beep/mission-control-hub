# Newsletter Publish Guide — July 21, 2026

## Issue: Manual Login Required

Substack publishing requires authentication. The browser shows "Se connecter" (Sign in) button, meaning the session is not authenticated.

## Steps to Publish

### Option 1: Manual Browser Publishing (Current)

1. Open browser and go to: https://substack.com/@quentinvest1
2. Click "Se connecter" (Sign in)
3. Log in with credentials
4. Click "Créer" (Create)
5. Paste content from: `newsletter/daily_brief_2026-07-21.md`
6. Add title: "Quentinvest Daily Brief — July 21, 2026"
7. Publish

### Option 2: API-Based Publishing (Recommended for Automation)

Substack does not have an official public API for posts. Alternative approaches:

**A. Substack RSS + Email Integration**
- Use Substack's "Import via email" feature
- Send formatted HTML email to post+{publication}@substack.com
- Requires email setup

**B. Substack API (Unofficial)**
- Reverse-engineered API available
- Requires session cookie
- Rate limited

**C. Puppeteer Automation**
- Full browser automation with login
- Requires storing credentials securely
- More reliable but complex

## Content Ready to Publish

**File:** `newsletter/daily_brief_2026-07-21.md`
**Word Count:** 685 words
**Sections:** Market Snapshot, Key Moves, Alpha Fund Signals, On-Chain Data, Macro Notes, Action Items

## Quick Copy/Paste

```
# Quentinvest Daily Brief — July 21, 2026

## Market Snapshot

| Asset | Price | 24h Change | Signal |
|-------|-------|------------|--------|
| BTC | $65,491.82 | +0.36% | ⚪ NEUTRAL |
| ETH | $1,922.99 | +0.96% | ⚪ NEUTRAL |
| MSTR | $97.82 | +3.13% | 🟢 BULLISH |
| COIN | $160.43 | +2.11% | 🟢 BULLISH |
| TSLA | $369.57 | -2.96% | 🔴 BEARISH |
| AAPL | $326.59 | -2.14% | 🔴 BEARISH |
| HIMS | $32.70 | -0.43% | ⚪ NEUTRAL |
| NVDA | $203.28 | +0.23% | ⚪ NEUTRAL |

---

## Key Moves

### 1. MSTR Outperforms (+3.13%)
MicroStrategy continues its Bitcoin proxy rally, up 3.13% while BTC itself is flat. The premium suggests institutional accumulation ahead of potential BTC breakout.

### 2. Crypto Stocks Lead (COIN +2.11%)
Coinbase showing strength alongside MSTR. The crypto exchange stock is benefiting from renewed retail interest and potential regulatory tailwinds.

### 3. Tech Majors Diverge (TSLA -2.96%, AAPL -2.14%)
Tesla and Apple both under pressure. Both are below the Alpha Fund's composite threshold — holding off until sentiment stabilizes.

---

## Alpha Fund Signals

**Composite Signal: SLIGHTLY_BULLISH**

| Asset | Score | Rating |
|-------|-------|--------|
| MSTR | +0.50 | SLIGHTLY_BULLISH |
| COIN | +0.50 | SLIGHTLY_BULLISH |
| BTC | +0.30 | SLIGHTLY_BULLISH |
| ETH | +0.30 | SLIGHTLY_BULLISH |
| HIMS | +0.30 | SLIGHTLY_BULLISH |

**Key Factors:**
- Fear & Greed Index: **25 (EXTREME FEAR)** — contrarian buy signal
- Whale accumulation: 66,700 BTC by large holders
- Mid-tier holders distributing — classic pre-rally setup

---

## Macro Notes

- **Fear & Greed at 25 (Extreme Fear)** — Historically marks local bottoms
- **Crypto correlation:** BTC/ETH flat while crypto stocks rally
- **Tech divergence:** MAG7 showing cracks with TSLA/AAPL down
- **Volatility:** Low across majors — compression often precedes expansion

**The Setup:** Extreme fear + whale accumulation + compression = classic accumulation phase.

---

## Action Items

### For Subscribers (Free)
1. **Watch MSTR** — Leading indicator for BTC sentiment
2. **Monitor Fear & Greed** — If it hits 20, consider DCA entry
3. **Track COIN** — Exchange stocks often lead underlying crypto

### For Pro Subscribers (€29/month)
- Full Alpha Fund position sizing
- Entry/exit price alerts
- Weekly deep-dive reports

---

*Generated autonomously by Claw | July 21, 2026 08:00 CET*

*Disclaimer: This newsletter is for informational purposes only. Not financial advice.*
```

## Recommended Next Steps

1. **For today:** Manual publish via browser (copy content above)
2. **For automation:** Set up email-based publishing or Puppeteer automation with stored credentials
3. **For scale:** Consider migrating to a platform with better API support (Beehiiv, Ghost, Buttondown)

## Files Generated

- `newsletter/daily_brief_2026-07-21.md` — Full newsletter content
- `revenue/reports/newsletter_2026-07-21.json` — Structured report data
- `newsletter/publish_guide_2026-07-21.md` — This guide

## Metrics Logged

```json
{
  "report_id": "newsletter-daily-2026-07-21",
  "date": "2026-07-21",
  "type": "daily_brief",
  "status": "content_ready",
  "assets_covered": 8,
  "word_count": 685,
  "alpha_signal": "SLIGHTLY_BULLISH",
  "fear_greed": 25
}
```
