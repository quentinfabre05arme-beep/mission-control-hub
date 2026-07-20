# Printify API Connection Guide

## Current Status (July 20, 2026)

| Component | Status |
|-----------|--------|
| API Token | ✅ Valid (1301 chars, JWT format) |
| API Connectivity | ✅ Working (200 on /v1/shops.json) |
| Shops | ❌ 0 found |
| Product Catalog | ❌ 0 blueprints visible |
| Etsy Connection | ❌ Not established |

## The Issue

Your Printify account has a valid API token, but:
1. No shops are connected to the account
2. The Etsy shop "Quentinvestdesign" exists but is NOT linked to Printify
3. Product catalog returns empty (likely because no shop = no context)

## Solution Options

### Option 1: Manual Dashboard Setup (Recommended)

1. Go to https://printify.com/app/dashboard
2. Click "Add New Store" or "Connect Store"
3. Select "Etsy"
4. Authorize Printify to access your Etsy shop "Quentinvestdesign"
5. Once connected, the shop ID will be visible
6. Re-run `node check_shops.js` to verify

### Option 2: API-First Shop Creation

```bash
cd pod_business
node create_shop.js
```

**Note:** Printify API typically requires manual OAuth for Etsy integration. The programmatic shop creation may not work for Etsy-connected shops.

## Verification After Setup

Once the shop is connected:

```bash
cd pod_business
node check_shops.js
```

Expected output:
```
📡 Step 2: Fetching shops...
   Status: 200
   Shops found: 1
   
   Shop 1:
   - ID: 28241288 (or new ID)
   - Title: Quentinvestdesign
   - Sales Channel: etsy
```

## Stable API Connection Script

After shop is connected, use `stable_connection.js` for all API operations:

```bash
cd pod_business
node stable_connection.js
```

This script:
- Validates token
- Fetches shop ID automatically
- Tests all API endpoints
- Reports health status

## GitHub Token for Git

The Git push is working with the token in the remote URL. However, this token is exposed. To secure it:

1. Generate new fine-grained token at https://github.com/settings/tokens
2. Update remote: `git remote set-url origin https://NEW_TOKEN@github.com/quentinfabre05arme-beep/mission-control-hub.git`
3. Or use SSH: `git remote set-url origin git@github.com:quentinfabre05arme-beep/mission-control-hub.git`

## Next Steps

1. **You:** Connect Etsy shop via Printify dashboard (5 minutes)
2. **Me:** Verify connection and start publishing designs
3. **Timeline:** First products live within 1 hour of connection

## Emergency Fallback

If Etsy connection fails:
- Create a manual Printify shop (no external platform)
- Publish products to Printify catalog
- Manually sync to Etsy later
- Revenue delay: 1-2 days

---

*Generated: July 20, 2026 16:45 CET*
