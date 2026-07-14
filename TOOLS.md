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
- **Version:** v7.6 (Jul 14, 2026 10:15) — Dashboard Suite
- **Latest Component:** Main Dashboard v7.6 (Updated Jul 14, 2026 10:15)
- **Status:** 8/8 core dashboards accessible ✅ — All dashboards verified 200 OK
- **Total Research Cycles:** 45 completed (Review #45 just finished)
- **Latest Review:** Jul 14, 2026 10:15 — Stale data fixes, version sync, mobile nav bug fix, cycle count 45, timestamps synced. All 8 links verified 200 OK.
- **Previous Review:** Jul 14, 2026 10:03 — v7.6 version bump across all dashboards, cycle count updated 43→44, timestamp synced to 10:03, Research Cycles Log updated (#44), Active Tasks refreshed. All 8 links verified 200 OK.

## Notes
- **Jul 14, 2026 10:15:** REVIEW #45 COMPLETED — Fixed 12 issues: stale metadata (cycle count 44→45, timestamps synced 10:03→10:15), title tag version mismatch (v7.5→v7.6), mobile nav bug fixed (duplicate Risk Management entries removed), mobile version synced (v7.5→v7.6), all cycle references updated. All 8 links verified 200 OK. Git commit ready, push pending.
- **Jul 14, 2026 10:03:** REVIEW #44 COMPLETED — v7.6 version bump across all 8 dashboards, cycle count updated 43→44, timestamps synced to 10:03, Research Cycles Log updated (#44 Dashboard Review v7.6), Active Tasks refreshed. All links verified 200 OK.
- **Jul 14, 2026 09:30:** REVIEW #43 COMPLETED — Data consistency audit: cycle counts synced (#43 across all sections), weekly goal fixed (1/10 ✅), post template prices updated to match market_data.json, deployment timestamp refreshed, gateway uptime adjusted. All 8 links verified 200 OK.
- **Jul 14, 2026 09:15:** REVIEW #43 COMPLETED — Full market data refresh (BTC: $62,490 | ETH: $1,779.85), portfolio tracker repriced, TA signals updated, timestamps synced, hero stats refreshed, deployment meta updated. All 8 links verified 200 OK.
- **Jul 14, 2026 09:00:** REVIEW #42 COMPLETED — Fixed stale version references in index.html: Settings cycles 26→41, version 9.6→7.5, updated deployment timestamp, research cycle #39→#41, backtesting v6.4→v7.5, activity v5.4→v7.5. Removed outdated deployment routing active issues. All 8 dashboard links verified 200 OK.
- **Jul 14, 2026 08:16:** REVIEW #40 COMPLETED — Fixed broken HTML tag in index.html (Recurring>/span → Recurring</span>), verified all 8 dashboard URLs return 200 OK, deployment healthy
- **Jul 14, 2026 08:05:** CRON REVIEW COMPLETED — Stale timestamps updated across all 6 active dashboards, chart labels shifted to Jul 8-14, nav consistency improved, mobile drawer expanded
- **Jul 14, 2026 08:00:** REVIEW COMPLETED — Fixed stale engagement drop alerts (mobile + desktop), updated market data (BTC: $62,638 | ETH: $1,784.79 | MSTR: $92.10 | HIMS: $34.38), updated TA signals, added "Today's Activity" disclaimer, deployed to production
- **Jul 14, 2026 07:15:** DEPLOYMENT SUCCESSFUL — vercel.json routing fix deployed to production. All 8 dashboards now accessible. Market data refreshed (BTC: $62,745.89 | ETH: $1,789.88 | MSTR: $92.11 | HIMS: $34.38)
- **Jul 14, 2026 07:00:** CRON REVIEW COMPLETED — Version tags synced to v7.5 across all dashboards, vercel.json modernized (removed deprecated `builds` array), deployment PENDING
- **Jul 14, 2026 06:45:** CRON REVIEW COMPLETED — Market data refreshed (BTC: $62,649 | ETH: $1,785.25), full link audit performed, 5 dashboards still 404 pending Vercel deployment
- **Jul 14, 2026 06:05:** REVIEW COMPLETED — Version tags updated to v7.5 for all dashboards, unified navigation component created
- **Jul 14, 2026:** COMPREHENSIVE REVIEW COMPLETED — Stale data updated, versions synced to v7.5 where possible, deployment routing fixed
- Risk Management Dashboard v10.0: DEPLOYED at root level ✅ (different path structure)
- Main Dashboard v7.5: Updated Jul 14, 2026 05:45 — includes market data, content queue, TA, search, competitors
- Market data auto-updates every 60 seconds (BTC: $62,490 | ETH: $1,779.85 | MSTR: $92.11 | HIMS: $34.38) — UPDATED Jul 14, 09:15
- **INVESTMENT TRACKING:** Portfolio position tracking with entry prices and P&L now visible in portfolio_tracker.html
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

## Dashboard Links Verified 🔍 (Jul 14, 2026 09:00)
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
**Response Times:** Avg ~200ms — Good performance
**Deployment:** https://mission-control-hub-lovat.vercel.app (aliased)

## Issues Found in 09:00 Review — ALL FIXED ✅
1. ✅ **Stale version references in Settings** — Cycles Done 26→41, Latest Version 9.6→7.5, hero cards updated
2. ✅ **Outdated component versions** — NL Command v9.6→v7.5, Backtesting v6.4→v7.5, Activity v5.4→v7.5
3. ✅ **Research cycle numbering** — #39 (Current) → #41 (Current) across both instances
4. ✅ **Deployment timestamp** — meta tag updated from 07:15→09:00
5. ✅ **My Tasks timestamp** — Updated label refreshed to 09:00
6. ✅ **Active Issues cleanup** — Removed resolved deployment routing issues from task descriptions

## Issues Found in 08:45 Review — ALL FIXED ✅
1. ✅ **Stale TA prices in index.html** — BTC TA price updated ($62,745.89 → $62,617.78), ETH TA price updated ($1,789.88 → $1,784.77), market-update template refreshed
2. ✅ **Stale portfolio prices in portfolio_tracker.html** — All 4 assets repriced: BTC ($62,007.66 → $62,617.78), ETH ($1,767.39 → $1,784.77), MSTR ($91.65 → $92.11), HIMS ($33.99 → $34.38). Total portfolio value recalculated: $46,891.42 → $46,898.37. All derived values (P&L, position values) updated accordingly.
3. ✅ **News-Sentiment dates** — All news timestamps showing "hours ago" relative to Jul 14, 2026 08:05 — still current, no action needed

## Issues Found in 08:00 Review — ALL FIXED ✅
1. ✅ **Stale engagement drop alert** — Removed from mobile_dashboard.html and index.html. Now shows "Engagement Normal" with current 6.3% rate
2. ✅ **Hardcoded TA values** — Updated BTC price ($62,192→$62,638), ETH price ($1,774→$1,784.79), MSTR ($91.87→$92.10), HIMS ($34.28→$34.38), signal descriptions refreshed
3. ✅ **Today's Activity sidebar** — Added "⏱️ Simulated" badge and disclaimer: "Static demo values — Wire to X API for live data"

## Previous Issues Found in 07:45 Review
1. **Hardcoded TA values** in `index.html` — BTC shows $62,192 (old) vs actual $62,745. Need to wire to market_data.json or update manually. → FIXED in 08:00 review
2. **Stale engagement drop alert** — The "🔴 -45% Engagement Drop" investigation card is still visible. Engagement is now 6.3% (above avg). Should archive/remove. → FIXED in 08:00 review
3. **Today's Activity sidebar** — Posts/Impressions/Engagements are static hardcoded values. Add disclaimer or wire to API. → FIXED in 08:00 review

## Dashboard Version Issues Found
- All nav version tags now synced to v7.5 ✅
- `mission_control_portfolio.html`: Was v6.2 → FIXED to v7.5
- `mission_control_market_intelligence.html`: Shows v10.0 — different component (kept as-is)
- `mission_control_hub.html`: No version shown — added to backlog
- Version inconsistency resolved across all active dashboard files
