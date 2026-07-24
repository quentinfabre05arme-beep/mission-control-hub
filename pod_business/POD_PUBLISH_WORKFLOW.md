# POD Publish Workflow — Printify → Etsy

**Status:** API Connected ✅ | **Blocker:** Need design images

---

## Current State

| Component | Status |
|-----------|--------|
| Printify API | ✅ Connected (Shop: Quentinvestdesign) |
| 10 Designs | ✅ Generated (titles/tags ready) |
| Product Images | ❌ Required — see options below |
| Auto-publish Script | ✅ Ready |

---

## Quick Options for Product Images

### Option 1: Canva Automation (Recommended)
1. Create designs in Canva using templates
2. Export as PNG with transparent background
3. Upload to Printify via API

### Option 2: Manual Upload (Today)
1. Go to [printify.com](https://printify.com)
2. Products → Create Product
3. Use titles from `generated_designs/batch_2026-07-24.json`
4. Tags: copy from JSON file
5. Publish to Etsy

### Option 3: Placeholder → Replace Later
1. Use simple text-based designs
2. Publish quickly
3. Replace with real designs later

---

## Manual Upload Quick Reference

**10 Titles Ready:**
1. Bitcoin to the Moon 2026
2. Long Term Investor
3. ChatGPT My Therapist
4. Technical Analysis Expert
5. 21 Million Club
6. Ethereum Investor 2026
7. Buy the Dip
8. Powered by AI
9. Day Trader Life
10. Satoshi Nakamoto Fan

**Tags by Niche:**
- Crypto: bitcoin,crypto,btc,moon,hodl
- Investing: investor,long-term,stocks,portfolio,wealth
- AI: ai,artificial-intelligence,tech,future,robot
- Trading: day-trader,trading,stocks,crypto,forex
- Bitcoin: satoshi,bitcoin,crypto,btc,founder

---

## Auto-publish Script

When images are ready, run:
```powershell
cd pod_business
node auto_publish.js
```

**What it does:**
- Creates 10 products in Printify
- Publishes to Etsy automatically
- Logs results to `publish_results_YYYY-MM-DD.json`

---

## Timeline

| Action | Time | Result |
|--------|------|--------|
| Create 10 designs in Canva | 2 hours | 10 PNG files |
| Upload via API | 10 min | 10 products live |
| Total | 2 hours 10 min | €1,500-15K/mo potential unlocked |

---

## Alternative: Use Existing Designs

If you have existing designs:
1. Rename them to match the titles in `batch_2026-07-24.json`
2. Place in `pod_business/design_images/`
3. Run `node auto_publish.js`

---

**Next Step:** Create 10 designs in Canva → Upload → Auto-publish
