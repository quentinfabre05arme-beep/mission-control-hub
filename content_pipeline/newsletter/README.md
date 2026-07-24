# Alpha Fund Newsletter System

## Overview

Automated newsletter generation pulling from research cycles and alternative data. Creates Substack-compatible markdown output.

## Structure

```
content_pipeline/newsletter/
├── templates/
│   ├── newsletter_template.md      # Base template
│   └── substack_compatible.md      # Substack-optimized template
├── output/
│   ├── archive/                     # Historical newsletters
│   └── generation_log.json          # Generation history
├── subscribers/
│   └── subscribers.json             # Subscriber tracking
├── newsletter_generator.js          # Core generator
├── weekly_scheduler.js              # Scheduling automation
└── README.md                        # This file
```

## Quick Commands

```powershell
# Generate newsletter manually
node content_pipeline/newsletter/newsletter_generator.js

# Force generate (ignore schedule)
node content_pipeline/newsletter/weekly_scheduler.js --force

# Dry run (show what would generate)
node content_pipeline/newsletter/weekly_scheduler.js --dry-run

# Add subscriber
node content_pipeline/newsletter/newsletter_generator.js subscribe user@example.com

# List subscribers
node content_pipeline/newsletter/newsletter_generator.js list-subscribers

# Generate for specific date
node content_pipeline/newsletter/newsletter_generator.js --date 2026-07-24
```

## Automation Setup

### Option 1: Windows Task Scheduler (Recommended)

```powershell
# Run weekly on Sunday at 08:00 Paris time
schtasks /create /tn "AlphaFund-Newsletter" `
  /tr "node C:\Users\quent\.openclaw\workspace\content_pipeline\newsletter\weekly_scheduler.js" `
  /sc weekly /d SUN /st 08:00
```

### Option 2: Cron (if available)

```bash
# Sunday at 08:00 Europe/Paris
0 8 * * 0 cd /workspace && node content_pipeline/newsletter/weekly_scheduler.js
```

## Newsletter Sections

Each newsletter includes:

1. **📊 Market Snapshot** — Current prices and 24h changes for all tracked assets
2. **🎯 Weekly Highlights** — Fear & Greed, whale activity, anomalies
3. **🔬 Asset Analysis** — Price action and signals for BTC, ETH, MSTR, HIMS
4. **🚨 Alternative Data** — On-chain metrics, social sentiment, funding rates
5. **📈 Composite Ratings** — Overall bullish/bearish ratings with key factors
6. **🎓 Key Takeaways** — Actionable insights and contrarian opportunities

## Data Sources

| Section | Source | File |
|---------|--------|------|
| Market Prices | `mission_control/market_data.json` | Local cache |
| Alternative Data | `investment_fund/data/alternative/` | Daily JSON |
| Research Cycles | `mission_control/` | Various outputs |

## Substack Publishing

1. Generate newsletter: `node newsletter_generator.js`
2. Open output: `content_pipeline/newsletter/output/newsletter_YYYY-MM-DD.md`
3. Copy content to Substack editor
4. Publish as draft, review, then publish

## Subscriber Management

```json
{
  "subscribers": [
    {
      "email": "user@example.com",
      "subscribed_at": "2026-07-24T15:00:00Z",
      "active": true,
      "metadata": { "source": "website" }
    }
  ],
  "count": 1,
  "settings": {
    "weekly_send_day": "Sunday",
    "weekly_send_time": "08:00",
    "timezone": "Europe/Paris"
  }
}
```

## Template Variables

Available in templates:
- `{{title}}` — Newsletter title
- `{{subtitle}}` — Subtitle
- `{{date}}` — Publication date
- `{{author}}` — Author name
- `{{highlights}}` — Weekly highlights
- `{{market_snapshot}}` — Market data table
- `{{asset_analyses}}` — Individual asset analysis
- `{{alternative_data}}` — On-chain/sentiment data
- `{{composite_ratings}}` — Overall ratings table
- `{{key_takeaways}}` — Summary insights
- `{{disclaimer}}` — Legal disclaimer
- `{{generation_date}}` — Generation timestamp
- `{{cycle_count}}` — Research cycles count

## Status

✅ **Infrastructure complete** — Ready for weekly generation and Substack publishing
