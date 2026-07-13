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
- **Mobile:** Auto-redirects from main URL
- **Version:** v6.4 (Jul 13, 2026 21:15) — Dashboard Suite
- **Latest Component:** Automated Backtesting Module v6.4 (Cycle #39)
- **Status:** 6/7 dashboards deployed. Backtesting Module 404 — fix in progress (vercel.json routes updated)
- **Total Research Cycles:** 39 completed

## Notes
- Risk Management Dashboard v10.0: DEPLOYED and accessible ✅
- Market Signals v9.8, Portfolio v9.9, NL Interface v9.6, Portfolio Tracker v6.0 all online
- Dashboard improvements made Jul 13, 2026 20:15 (added Research Cycles + Market Snapshot sidebar cards)
- Automated Backtesting Module v6.4 deployed Jul 13, 2026 21:02 — tracks sentiment divergence signal performance
- **Jul 13, 2026 21:15:** Fixed vercel.json routes config — added static builds + rewrite rules for /mission_control/* paths
- Current focus: Signal validation + automated backtesting + portfolio optimization
- Model routing: Manual switching preferred (ask before switching to qwen3-coder)

## X Account
- **Handle:** @quentinvest1
- **Followers:** 219
- **Engagement:** 6.3%

## Active Research Cycles
- Total: 39 completed (as of July 13, 2026 21:02)
- Latest completed: #39 (Automated Backtesting Module v6.4)
- Next planned: #40+ (Live Trading Integration, ML Signal Enhancement)

## Known Issues & Solutions
- **OpenClaw browser evaluate/type:** Space splitting bug — use JavaScript injection workaround
- **Windows Chrome CDP:** Requires manual admin elevation — use Playwright Python for automation
- **PowerShell emoji display:** Can show empty boxes — verify with `Get-ChildItem` file counts
- **Memory index:** Needs rebuild with `openclaw memory index --force` when embedding model changes

## Dashboard Links Verified ✅ (Jul 13, 2026 21:02)
| Dashboard | URL | Status |
|-----------|-----|--------|
| Main Redirect | https://mission-control-hub-lovat.vercel.app | ✅ 200 |
| Desktop Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/index.html | ✅ 200 |
| Mobile Dashboard | https://mission-control-hub-lovat.vercel.app/mission_control/mobile_dashboard.html | ✅ 200 |
| Portfolio Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/portfolio_tracker.html | ✅ 200 |
| News-Sentiment Tracker | https://mission-control-hub-lovat.vercel.app/mission_control/news_sentiment_tracker.html | ✅ 200 |
| Risk Management | https://mission-control-hub-lovat.vercel.app/mission_control_risk_management.html | ✅ 200 |
| Backtesting Module | https://mission-control-hub-lovat.vercel.app/mission_control/backtesting_module.html | ❌ 404 — fix deployed |
