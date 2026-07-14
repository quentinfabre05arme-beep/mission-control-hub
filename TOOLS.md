# TOOLS.md - Local Notes

## API Keys

### Serper.dev (Web Search)
- **Key:** `1a32d04a8215dde72b67e554c94409ce580094f3`
- **Free tier:** 2,500 searches/month
- **URL:** https://serper.dev
- **Usage:** Web search for research cycles

### Twelve Data (Technical Analysis)
- **Key:** `07f9ead31a5c426ea238e71895beeaa1`
- **Free tier:** 800 requests/day
- **Usage:** RSI, MACD, SMA, Bollinger Bands for BTC/ETH/MSTR/HIMS
- **Status:** ✅ Active

## Dashboard URLs
- **Production:** https://mission-control-hub-lovat.vercel.app
- **Version:** v7.5 (Jul 14, 2026 05:45) — Dashboard Suite
- **Latest Component:** Main Dashboard v7.5 (Updated Jul 14, 2026 05:45)
- **Status:** 3/8 core dashboards accessible (Main + Risk Management + Desktop). Mobile, Portfolio, Sentiment, Backtest, Social still 404 — routing fix applied in vercel.json
- **Total Research Cycles:** 39 completed

## Notes
- **Jul 14, 2026:** COMPREHENSIVE REVIEW COMPLETED — Stale data updated, versions synced to v7.5 where possible, deployment routing fixed
- Risk Management Dashboard v10.0: DEPLOYED at root level ✅ (different path structure)
- Main Dashboard v7.5: Updated Jul 14, 2026 05:45 — includes market data, content queue, TA, search, competitors
- Market data auto-updates every 60 seconds (BTC: $62,512 | ETH: $1,783 | MSTR: $92.10 | HIMS: $34.38)
- **INVESTMENT TRACKING:** Need to add portfolio position tracking (entry prices, P&L, allocation %)
- **DEPLOYMENT PENDING:** vercel.json updated with explicit build entries for all sub-pages. Need to push to Vercel to apply.
- Current focus: Deploy routing fix + version synchronization + portfolio position tracking
- Model routing: Manual switching preferred (ask before switching to qwen3-coder)

## X Account
- **Handle:** @quentinvest1
- **Followers:** 219 (+7 gained recently)
- **Engagement:** 6.3% (+0.4% improvement)
- **Daily Streak:** 2 days
- **Growth Mission:** 212 → 10,000 followers (2.19% complete, 9,781 to go)

## Active Research Cycles
- Total: 39 completed (as of July 13, 2026 21:02)
- Latest completed: #39 (Automated Backtesting Module v6.4)
- Next planned: #40+ (Live Trading Integration, ML Signal Enhancement)

## Known Issues & Solutions
- **OpenClaw browser evaluate/type:** Space splitting bug — use JavaScript injection workaround
- **Windows Chrome CDP:** Requires manual admin elevation — use Playwright Python for automation
- **PowerShell emoji display:** Can show empty boxes — verify with `Get-ChildItem` file counts
- **Memory index:** Needs rebuild with `openclaw memory index --force` when embedding model changes
- **Vercel Routing:** /mission_control/* paths 404 — need vercel.json rewrite rules update
- **Version Sync:** Dashboard components show different versions (v5.8 to v7.5) — needs standardization

## Dashboard Links Verified 🔍 (Jul 14, 2026 05:45)
| Dashboard | URL | Status | Version |
|-----------|-----|--------|---------|
| Main Redirect | https://mission-control-hub-lovat.vercel.app | ✅ 200 | v7.5 |
| Desktop Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/index.html | ✅ 200 | v7.5 |
| Mobile Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/mobile_dashboard.html | ❌ 404 | v5.8 |
| Portfolio Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/portfolio_tracker.html | ❌ 404 | v6.3 |
| News-Sentiment Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/news_sentiment_tracker.html | ❌ 404 | v6.2 |
| Risk Management | https://mission-control-hub-lovat.vercel.app/mission_control_risk_management.html | ✅ 200 | v10.0 |
| Backtesting Module | https://mission-control-hub-lovat.vercel.app/mission_control/backtesting_module.html | ❌ 404 | v6.4 |
| Social Sentiment Live | https://mission-control-hub-lovat.vercel.app/mission_control/social_sentiment_live.html | ❌ 404 | v6.3 |

**Fix Applied:** vercel.json updated with explicit build entries for all sub-pages. Deploy to Vercel to activate.
