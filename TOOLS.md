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
- **Version:** v7.5 (Jul 14, 2026 07:15) — Dashboard Suite
- **Latest Component:** Main Dashboard v7.5 (Updated Jul 14, 2026 07:15)
- **Status:** 8/8 core dashboards accessible ✅ — All dashboards now live after vercel.json routing fix deployed
- **Total Research Cycles:** 39 completed
- **Latest Review:** Jul 14, 2026 07:15 — Deployment complete, all links verified, market data refreshed

## Notes
- **Jul 14, 2026 07:15:** DEPLOYMENT SUCCESSFUL — vercel.json routing fix deployed to production. All 8 dashboards now accessible. Market data refreshed (BTC: $62,745.89 | ETH: $1,789.88 | MSTR: $92.11 | HIMS: $34.38)
- **Jul 14, 2026 07:00:** CRON REVIEW COMPLETED — Version tags synced to v7.5 across all dashboards, vercel.json modernized (removed deprecated `builds` array), deployment PENDING
- **Jul 14, 2026 06:45:** CRON REVIEW COMPLETED — Market data refreshed (BTC: $62,649 | ETH: $1,785.25), full link audit performed, 5 dashboards still 404 pending Vercel deployment
- **Jul 14, 2026 06:05:** REVIEW COMPLETED — Version tags updated to v7.5 for all dashboards, unified navigation component created
- **Jul 14, 2026:** COMPREHENSIVE REVIEW COMPLETED — Stale data updated, versions synced to v7.5 where possible, deployment routing fixed
- Risk Management Dashboard v10.0: DEPLOYED at root level ✅ (different path structure)
- Main Dashboard v7.5: Updated Jul 14, 2026 05:45 — includes market data, content queue, TA, search, competitors
- Market data auto-updates every 60 seconds (BTC: $62,745.89 | ETH: $1,789.88 | MSTR: $92.11 | HIMS: $34.38) — UPDATED Jul 14, 07:15
- **INVESTMENT TRACKING:** Need to add portfolio position tracking (entry prices, P&L, allocation %)
- **DEPLOYED:** vercel.json routing fix applied. All dashboards accessible.
- Current focus: Portfolio position tracking + next research cycle #40
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
- **Vercel Routing:** ✅ FIXED Jul 14, 07:15 — All /mission_control/* paths now serving correctly
- **Version Sync:** All dashboard nav version tags now synced to v7.5 ✅

## Dashboard Links Verified 🔍 (Jul 14, 2026 07:15)
| Dashboard | URL | Status | Version |
|-----------|-----|--------|---------|
| Main Redirect | https://mission-control-hub-lovat.vercel.app | ✅ 200 | v7.5 |
| Desktop Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/index.html | ✅ 200 | v7.5 |
| Mobile Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/mobile_dashboard.html | ✅ 200 | v7.5 |
| Portfolio Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/portfolio_tracker.html | ✅ 200 | v7.5 |
| News-Sentiment Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/news_sentiment_tracker.html | ✅ 200 | v7.5 |
| Risk Management | https://mission-control-hub-lovat.vercel.app/mission_control_risk_management.html | ✅ 200 | v10.0 |
| Backtesting Module | https://mission-control-hub-lovat.vercel.app/mission_control/backtesting_module.html | ✅ 200 | v7.5 |
| Social Sentiment Live | https://mission-control-hub-lovat.vercel.app/mission_control/social_sentiment_live.html | ✅ 200 | v7.5 |

**Status:** All dashboards deployed and verified ✅

## Dashboard Version Issues Found
- All nav version tags now synced to v7.5 ✅
- `mission_control_portfolio.html`: Was v6.2 → FIXED to v7.5
- `mission_control_market_intelligence.html`: Shows v10.0 — different component (kept as-is)
- `mission_control_hub.html`: No version shown — added to backlog
- Version inconsistency resolved across all active dashboard files
