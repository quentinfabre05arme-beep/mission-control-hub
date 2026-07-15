# Research Cycle Schedule — 3x Daily

## Schedule

| Cycle | Time | Focus | Trigger |
|-------|------|-------|---------|
| **Morning** | 08:00 | Overnight market moves, daily briefing | Cron + systemEvent |
| **Midday** | 14:00 | Live market updates, trend confirmation | Cron + systemEvent |
| **Evening** | 19:00 | Day wrap-up, next-day setup | Cron + systemEvent |

## Research Cycle #52 Workflow

Each cycle:
1. **Fresh data fetch** — CoinGecko + Twelve Data (on-demand)
2. **Market analysis** — BTC/ETH/MSTR/HIMS trends
3. **News scan** — Serper.dev for relevant headlines
4. **Grok X sentiment** — Search + analyze X posts for market sentiment
5. **Grok news analysis** — Deep analysis of key news via Grok API
6. **Synthesis** — Key insights + actionable signals
7. **Dashboard update** — If new insights warrant refresh
8. **Memory log** — Append to daily file

## Next Cycle

**Research Cycle #52** — Today 14:00 (in ~15 minutes)
- Status: ⏳ Queued
- Focus: Midday market pulse
- Auto-start: Yes

## Token Budget Per Cycle

- Data fetch: ~500 tokens
- Market analysis: ~2,000 tokens
- News scan (Serper): ~500 tokens
- Grok X sentiment: ~1,500 tokens
- Grok news analysis: ~1,500 tokens
- Synthesis: ~2,000 tokens
- Dashboard update: ~500 tokens (if needed)
- **Total:** ~6,500 tokens per cycle
- **Daily:** ~19,500 tokens (well under 50K limit)

## Automation

Cron jobs created:
- `research-morning` — 08:00 daily
- `research-midday` — 14:00 daily
- `research-evening` — 19:00 daily

All use `systemEvent` for zero-token triggers, then spawn agentTurn for actual research.
