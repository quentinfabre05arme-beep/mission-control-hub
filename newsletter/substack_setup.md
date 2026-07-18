# Substack Newsletter Setup Guide

## Account Creation Steps

1. **Go to:** https://substack.com/signup
2. **Email:** Use your preferred email (quentinvest@gmail.com or create new)
3. **Newsletter Name:** "Alpha Fund Daily" or "Quentin's Market Brief"
4. **URL:** alpha-fund.substack.com (check availability)

## Publication Settings

| Setting | Recommendation |
|---------|----------------|
| **Publication Name** | Alpha Fund Daily |
| **Tagline** | Investment research, market signals, and alpha generation |
| **Logo** | Upload from `newsletter/assets/logo.png` |
| **Color Theme** | Dark blue (#1a1d23) to match Mission Control |
| **Paid/Free** | Start free, enable paid later |

## First Post Template

Title: "Welcome to Alpha Fund Daily"

Content ready in `newsletter/content/welcome_post.md`

## Automation Integration

Once account is created:
1. Get Substack API key from Settings → API
2. Update `newsletter/.env` with API key
3. Test automated publish flow

## Next Steps

**Action Required:** Create account manually (requires email verification)

**Timeline:** 5 minutes setup + email verification

**Cost:** Free forever for free newsletters
