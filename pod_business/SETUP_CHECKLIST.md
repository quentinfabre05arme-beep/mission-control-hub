# POD Setup Checklist
## Complete these steps to activate your POD business

---

## STEP 1: Create Accounts (15 minutes)

### Redbubble
1. Go to: https://www.redbubble.com/sell/signup
2. Email: [your email]
3. Shop Name: **Quentinvest Designs**
4. Password: [secure password]
5. Verify email
6. Complete profile with info from SHOP_SETUP_PACKAGE.md

### Spring (Teespring)
1. Go to: https://spring.com/signup
2. Use same email as Redbubble
3. Connect PayPal for payouts
4. Shop Name: **Quentinvest Designs**

### Printify (Optional - for full automation)
1. Go to: https://printify.com/
2. Create account
3. Connect to Etsy (if you have one) or Shopify
4. Get API key from: https://printify.com/account/api

---

## STEP 2: Prepare Designs (5 minutes)

### Convert SVG to PNG
Open PowerShell and run:

```powershell
cd C:\Users\quent\.openclaw\workspace\pod_business\designs

# Using ImageMagick (if installed)
Get-ChildItem *.svg | ForEach-Object { 
    magick convert $_.FullName -resize 7632x6480 ($_.BaseName + ".png")
}

# OR manual: Use https://cloudconvert.com/svg-to-png
```

**Required specs:**
- Format: PNG
- Size: 7632 x 6480 pixels (for t-shirts)
- DPI: 300
- Background: Transparent

---

## STEP 3: Upload to Redbubble (20 minutes)

### Design 1: BITCOIN TREASURY
1. Click "Add New Work"
2. Upload: `design_crypto_1784049410601.png`
3. Title: "Bitcoin Treasury Strategy - Crypto Investor T-Shirt"
4. Tags: bitcoin, treasury, strategy, crypto, btc, satoshi, digital gold, investment, hodl, blockchain
5. Description: "Show your conviction in Bitcoin as a treasury reserve asset. For investors who see the big picture."
6. Enable products: T-shirt, Classic T-shirt, Pullover Hoodie, Mug, Sticker, Poster
7. Set markup: 20%
8. Save

### Designs 2-5
Repeat for:
- `design_fitness_1784049410604.png` → "Gym Rat Life"
- `design_professions_1784049410606.png` → "Developer Mode"  
- `design_crypto_1784049410607.png` → "HODL Strong"
- `design_professions_1784049410609.png` → "Code & Coffee"

See SHOP_SETUP_PACKAGE.md for full details on each.

---

## STEP 4: Upload to Spring (15 minutes)

1. Go to https://spring.com/dashboard
2. Click "Create"
3. Upload same 5 PNG files
4. Use same titles/tags as Redbubble
5. Set prices (Spring auto-suggests)
6. Publish listings

---

## STEP 5: Configure Automation

Once accounts are set up, tell me:
1. Are accounts created? (Yes/No)
2. Do you want Printify integration? (Yes/No)
3. Share API keys if using Printify

Then I'll activate:
- Daily design generation
- Auto-mockup creation  
- Performance tracking
- Weekly earnings reports

---

## YOUR DASHBOARD

Track everything at:
- **Redbubble:** https://www.redbubble.com/portfolio
- **Spring:** https://spring.com/dashboard
- **Your Reports:** `C:\Users\quent\.openclaw\workspace\pod_business\reports\`

---

## NEXT 30 DAYS

| Day | Action |
|-----|--------|
| 1 | Upload first 5 designs |
| 2-7 | System generates 5 more designs/day |
| 7 | Upload batch 2 (35 designs total) |
| 14 | First sales likely |
| 30 | ~150 designs live, weekly reports active |

---

## SUPPORT

**Full guide:** `SHOP_SETUP_PACKAGE.md`
**Design files:** `pod_business\designs\`
**Automation status:** Run `node pod_orchestrator.js`

---

**Time to complete:** ~1 hour
**Ongoing time:** 0 (fully automated after setup)

**Ready? Start with Step 1 now.**
