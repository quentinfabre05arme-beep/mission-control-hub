# Mission Control Dashboard - Phone Access Guide

## Quick Access

Your dashboard is now **always accessible** from your phone when your PC is on and connected to WiFi.

### URLs (Bookmark these on your phone)

| Dashboard | URL | Purpose |
|-----------|-----|---------|
| **Main Dashboard** | `http://192.168.1.69:8080/mission_control_dashboard.html` | Operations overview |
| **Predictive v3.0** | `http://192.168.1.69:8080/mission_control_predictive.html` | AI content scoring |
| **Analytics** | `http://192.168.1.69:8080/mission_control_analytics.html` | Charts & metrics |

### How It Works

- HTTP server runs automatically on Windows startup
- Serves files from your OpenClaw workspace
- Accessible from any device on your home WiFi
- Updates in real-time as files change

### Phone Setup

1. **Connect to same WiFi** as your PC
2. **Open browser** and go to any dashboard URL above
3. **Bookmark** for quick access
4. **Add to home screen** (optional) for app-like experience

### Features on Phone

- ✅ Responsive design (adapts to screen size)
- ✅ Touch-optimized (48px button targets)
- ✅ Real-time data updates
- ✅ Dark mode optimized
- ✅ Works offline if page loaded (static content)

### Troubleshooting

**Can't connect?**
- Check PC is on and connected to WiFi
- Verify phone is on same WiFi network
- Try http://192.168.1.69:8080/ (root page shows file list)

**Server not running?**
- Check if port 8080 is blocked by firewall
- Manually run: `python -m http.server 8080` in workspace folder

**IP changed?**
- Your PC's IP may change after reboot
- Check current IP: Run `ipconfig` in Command Prompt
- Update bookmarks with new IP

### Auto-Start Configuration

The server starts automatically via:
- Registry entry: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Script: `openclaw_autostart.bat`
- Runs on every Windows boot

### Security Note

- Dashboard is only accessible on your local network
- Not exposed to the internet
- Safe to use on home WiFi

---

**Last Updated:** 2026-07-12  
**Server Status:** ✅ Running on port 8080
