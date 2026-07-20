# Printify → Etsy Publishing Pipeline

## Current Status: API Connected, Token Scope Limited

| Component | Status | Details |
|-----------|--------|---------|
| **API Token** | ✅ Valid | 1301 chars, JWT format |
| **Shop Access** | ✅ Working | /v1/shops.json returns shop |
| **Products API** | 🔴 401 | Token may lack product scope |
| **Catalog API** | 🔴 401 | Token may lack catalog scope |
| **Design Files** | ✅ Ready | 5 SVG files in /designs/ |

## The Issue

The API token authenticates successfully for basic shop info, but returns **401 Unauthorized** for:
- `/v1/catalog/blueprints.json` (need this to create products)
- `/v1/shops/{id}/products.json` (need this to manage products)

## Likely Causes

1. **Token Scope**: The token may have been generated with limited scopes (read-only)
2. **Token Type**: May need a "Merchant API" token vs "Partner API" token
3. **Account Type**: Printify account may need merchant verification

## Solutions

### Option 1: Regenerate Token with Full Permissions (Recommended)

1. Go to https://printify.com/app/dashboard
2. Click your profile → **Account Settings** → **API Tokens**
3. Delete current token
4. Create **NEW token** with these permissions:
   - ✅ Read shops
   - ✅ Read/Write products
   - ✅ Read catalog
   - ✅ Publish products
5. Update `.env` with new token
6. Re-run `node stable_connection.js`

### Option 2: Manual Upload via Dashboard

Since API has scope limitations, use the dashboard:

1. Go to https://printify.com/app/dashboard
2. Click **"Add New Product"**
3. Select **T-Shirt** (or preferred product)
4. Upload your SVG files from `pod_business/designs/`
5. Position design on product
6. Set pricing ($24.99 recommended)
7. Publish to **Etsy** → "Quentinvestdesign"

### Option 3: Hybrid Automation

I can prepare everything, you do the final click:

1. **Me**: Generate product metadata (titles, descriptions, tags, pricing)
2. **Me**: Optimize images for Printify specs
3. **You**: Upload via dashboard (5 min)
4. **Me**: Automate future price updates and inventory sync

## Design Files Ready

```
pod_business/designs/
├── design_crypto_1784049410601.svg     (Bitcoin Treasury)
├── design_crypto_1784049410607.svg     (HODL Strong)
├── design_fitness_1784049410604.svg    (Fitness Motivation)
├── design_professions_1784049410606.svg (Professional Pride)
└── design_professions_1784049410609.svg (Work Hard)
```

## Product Metadata Prepared

| # | Title | Price | Tags |
|---|-------|-------|------|
| 1 | Bitcoin Treasury | $24.99 | bitcoin, btc, crypto, cryptocurrency, blockchain, hodl, treasury |
| 2 | HODL Strong | $24.99 | hodl, bitcoin, crypto, cryptocurrency, strong, investor, blockchain |
| 3 | Fitness Motivation | $24.99 | fitness, gym, workout, motivation, health, training |
| 4 | Professional Pride | $24.99 | profession, career, job, work, professional |
| 5 | Work Hard | $24.99 | work, motivation, professional, career, success |

## Immediate Action Required

**Regenerate the Printify API token with full permissions**, or **use Option 2 (manual upload)**.

The designs are ready. The shop is connected. Just need the right token scope or manual upload.

---

*Generated: July 20, 2026 17:05 CET*
