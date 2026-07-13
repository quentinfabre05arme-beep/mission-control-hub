# Manual CDP Activation (Required Due to Windows Security)

Chrome CDP is being blocked by Windows security policies.

## Alternative: Manual DevTools Protocol

### Step 1: Start Chrome with CDP Manually

**Right-click on Desktop → New → Shortcut**

**Location:**
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Name:** Chrome CDP

**Right-click shortcut → Run as Administrator**

### Step 2: Verify CDP is Working

Open Command Prompt and run:
```bash
curl http://127.0.0.1:9222/json/version
```

If you see JSON response, CDP is working.

### Step 3: Run Automation

Once CDP is active:
```bash
python x_automation_cdp.py test
```

---

## If CDP Still Doesn't Work

**Use Semi-Automated Mode (Reliable):**

```bash
post_hims_thread.bat
```

This opens X and provides JavaScript to paste into DevTools console.

---

## Current Status

- ✅ Playwright installed
- ✅ Task Scheduler configured
- ✅ Content library ready
- ⚠️ Chrome CDP blocked by Windows security
- 🔄 Awaiting manual Chrome startup with admin privileges
