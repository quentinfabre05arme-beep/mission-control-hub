# External Dashboard Access Guide
## Access Mission Control from Anywhere (Internet)

---

## Quick Start: Cloudflare Tunnel (RECOMMENDED)

Cloudflare Tunnel provides a **free, secure, permanent URL** for your dashboard.

### Option A: Quick Temporary Tunnel (No signup, instant)

```bash
# Already installed? Just run:
cloudflared tunnel --url http://localhost:8080

# Output will show:
# https://random-words.trycloudflare.com  ← Your public URL
```

**Pros:** Instant, no account needed  
**Cons:** URL changes every time you restart

---

### Option B: Permanent Tunnel (Free account, stable URL)

**Step 1: Install Cloudflared**
```powershell
# Download
Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'C:\Windows\System32\cloudflared.exe'
```

**Step 2: Authenticate**
```bash
cloudflared login
# Opens browser - login to Cloudflare (free account)
```

**Step 3: Create Tunnel**
```bash
cloudflared tunnel create mission-control
# Saves credentials file
```

**Step 4: Configure Route**
```bash
# Replace with your domain or use cloudflare's free subdomain
cloudflared tunnel route dns mission-control dashboard.yourdomain.com
```

**Step 5: Run Tunnel**
```bash
cloudflared tunnel run mission-control
```

**Your dashboard is now at:** `https://dashboard.yourdomain.com`

---

## Alternative: ngrok (Easiest but temporary)

```bash
# Download from https://ngrok.com/download
# Add auth token (free signup required)
ngrok config add-authtoken YOUR_TOKEN

# Expose dashboard
ngrok http 8080

# Output shows:
# Forwarding: https://abc123.ngrok.io → http://localhost:8080
```

**Pros:** Very simple, great for testing  
**Cons:** URL changes on restart, session limits on free tier

---

## Alternative: LocalTunnel (Open Source)

```bash
# Requires Node.js
npm install -g localtunnel

# Expose port 8080
lt --port 8080

# Output shows:
# https://random-name.loca.lt
```

**Pros:** Free, open source, simple  
**Cons:** Less reliable than Cloudflare

---

## Security Considerations

⚠️ **When exposing to internet:**

1. **Add authentication** - Don't leave dashboard public
2. **Use HTTPS** - All services above provide this
3. **Limit access** - Cloudflare can restrict by IP/email
4. **Monitor logs** - Watch for unauthorized access

---

## Recommended Setup for Daily Use

### Method 1: Cloudflare Quick Tunnel (Temporary, testing)
```bash
cloudflared tunnel --url http://localhost:8080
```

### Method 2: Cloudflare Permanent (Production)
Follow steps in Option B above. Get a free domain from:
- https://www.freenom.com (free .tk .ml domains)
- Or use Cloudflare Pages free subdomain

### Method 3: Tailscale (Private mesh network)
For personal use only - no public exposure needed.
```bash
# Install Tailscale
# Connect phone + PC to same Tailscale network
# Access via: http://PC-NAME:8080 (from anywhere)
```

---

## Current Status

| Method | Status | URL |
|--------|--------|-----|
| Local WiFi | ✅ Running | http://192.168.1.69:8080 |
| Cloudflare Quick | ⏳ Not started | Run command below |
| Cloudflare Permanent | ⏳ Not configured | Follow Option B |

**To start external access now:**
```bash
cloudflared tunnel --url http://localhost:8080
```

---

## Auto-Start External Tunnel

Want the tunnel to start automatically? Add to `openclaw_autostart.bat`:

```batch
REM Start Cloudflare tunnel in background
start /min "Cloudflare Tunnel" cloudflared tunnel --url http://localhost:8080
```

**Note:** Quick tunnel URL changes on each restart. For permanent URL, use Option B above.

---

*Last Updated: 2026-07-12*
