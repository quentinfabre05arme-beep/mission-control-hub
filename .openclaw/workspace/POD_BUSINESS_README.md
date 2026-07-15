# Autonomous Print-on-Demand Business

A fully automated system for generating and selling print-on-demand products across multiple platforms.

## 🎯 What This System Does

| Phase | Automation Level | What Happens |
|-------|-----------------|--------------|
| **Trend Discovery** | ✅ Fully Auto | Scans trending niches daily |
| **Design Generation** | ✅ Fully Auto | Creates SVG vector designs |
| **Mockup Creation** | ✅ Fully Auto | Generates product previews |
| **Printify Publishing** | ⚠️ Needs API Key | Auto-publishes to Etsy/Shopify |
| **Redbubble/Teespring** | 🔧 Semi-Auto | Pre-optimized listings ready |
| **Sales Tracking** | ✅ Fully Auto | Monitors revenue & profits |
| **Weekly Reports** | ✅ Fully Auto | Reports every Sunday |

## 📁 File Structure

```
pod_business/
├── designs/              # Generated SVG designs
│   └── designs_registry.json
├── mockups/              # Product mockup HTML files
├── reports/              # Weekly earnings reports
├── trends.json           # Active trending niches
├── sales_data.json       # Sales tracking data
└── redbubble_listings.json  # Pre-optimized listings
```

## 🚀 Quick Start

### Step 1: Run First Cycle (Manual)

```bash
# Discover trends + generate designs
node pod_orchestrator.js
```

### Step 2: Check Generated Assets

```bash
# View designs
dir pod_business\designs

# View mockups
start pod_business\mockups\mockup_*.html

# Check Redbubble listings
start pod_business\redbubble_listings.json
```

### Step 3: Configure Printify (Optional)

For fully automated publishing:

1. Create Printify account: https://printify.com
2. Get API key from: https://printify.com/account/api
3. Set environment variable:
   ```bash
   setx PRINTIFY_API_KEY "your_api_key_here"
   setx PRINTIFY_SHOP_ID "your_shop_id"
   ```
4. Enable auto-publish in `pod_orchestrator.js`:
   ```javascript
   autoPublish: true
   ```

### Step 4: Manual Upload to Redbubble/Teespring

1. Open `pod_business\redbubble_listings.json`
2. Each listing includes:
   - Title
   - Description  
   - Tags
   - Pricing
   - File upload instructions
3. Convert SVG to PNG (7632x6480px)
4. Upload manually to platforms

## 📊 Daily Operations

### Automated (Every 24 Hours)
- Trend discovery
- Design generation (5 designs/day)
- Mockup creation
- Sales data collection

### Manual Tasks
- Upload to Redbubble (weekly batch)
- Upload to Teespring (weekly batch)
- Review Printify listings (if using API)
- Approve/pause underperforming designs

## 💰 Revenue Targets

| Metric | Target | Timeline |
|--------|--------|----------|
| Daily Designs | 5 | Week 1+ |
| Active Listings | 100+ | Month 1 |
| First Sale | - | Week 2-4 |
| Monthly Profit | $500+ | Month 3 |
| Monthly Profit | $2000+ | Month 6 |

## 📈 Tracking Performance

### Weekly Reports (Auto-Generated)
- Total sales & revenue
- Profit by platform
- Top-performing designs
- Growth trends
- Actionable recommendations

### View Current Stats
```bash
node pod_orchestrator.js analytics
```

### Simulate Sales (Testing)
```bash
node pod_orchestrator.js sales 20
```

## 🔧 Manual Commands

```bash
# Discover trends only
node pod_orchestrator.js trends

# Generate designs only
node pod_orchestrator.js design

# Create mockups for specific design
node pod_orchestrator.js mockup [design-id]

# Publish to Printify
node pod_orchestrator.js publish [design-id]

# Generate report
node pod_orchestrator.js report

# Show analytics
node pod_orchestrator.js analytics
```

## 🎨 Design Categories

The system tracks and generates designs for:

- **Crypto**: Bitcoin, Ethereum, DeFi themes
- **Fitness**: Gym, workout, motivation
- **Gaming**: Esports, streaming, retro
- **Professions**: Developer, nurse, teacher, etc.
- **Lifestyle**: Minimalist, travel, coffee
- **Humor**: Sarcasm, puns, memes
- **Pets**: Dog, cat, rescue themes
- **Seasonal**: Halloween, Christmas, etc.

## 🔑 Success Factors

1. **Volume**: More designs = more chances to sell
2. **Trend Timing**: Early on trends = less competition
3. **Platform Diversity**: Don't rely on one platform
4. **Regular Uploads**: Consistency matters for algorithms
5. **SEO Keywords**: Titles/tags affect discoverability

## ⚠️ Limitations

- **Redbubble/Teespring**: Manual upload required (no APIs)
- **Design Quality**: AI-generated, may need human curation
- **Trend Accuracy**: Simulated data (replace with real APIs)
- **Printify**: Requires API key for auto-publish

## 🔮 Future Enhancements

- [ ] Integration with Google Trends API
- [ ] Integration with Etsy/EtsyHunt API
- [ ] AI-powered design quality scoring
- [ ] Automatic A/B testing
- [ ] Competitor design analysis
- [ ] Dynamic pricing optimization

## 📞 Support

System status: `node pod_orchestrator.js`
Logs: Check console output
Reports: `pod_business/reports/weekly_report_*.txt`

---

**Last Updated:** July 14, 2026
**Version:** 1.0
**Status:** Operational
