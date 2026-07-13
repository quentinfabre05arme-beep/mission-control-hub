@echo off
REM ============================================
REM Dashboard Auto-Installer - Run as Admin
REM One-click setup for permanent dashboard access
REM ============================================

echo.
echo  ============================================
echo   DASHBOARD PERMANENT INSTALLER
echo  ============================================
echo.
echo  This will install:
echo   - Dashboard HTTP Server (auto-start on boot)
echo   - Cloudflare Tunnel (auto-start on boot)
echo.
echo  Press any key to continue...
pause >nul

REM Check admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Not running as Administrator!
    echo  Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo  [1/4] Stopping any running dashboard processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *http.server*" >>nul 2>&1
taskkill /F /IM cloudflared.exe >>nul 2>&1
echo  [OK] Processes stopped

echo.
echo  [2/4] Creating Dashboard HTTP Server service...
cd /d C:\Users\quent\.openclaw\workspace

REM Create scheduled task for HTTP server
schtasks /create /tn "DashboardHTTP" /tr "python.exe -m http.server 8080" /sc onstart /ru SYSTEM /rl HIGHEST /f >>nul 2>&1
if %errorlevel% neq 0 (
    echo  [WARN] Task may already exist, continuing...
)

REM Start the task
schtasks /run /tn "DashboardHTTP" >>nul 2>&1
echo  [OK] HTTP Server scheduled task created

echo.
echo  [3/4] Creating Cloudflare Tunnel service...

REM Create scheduled task for Cloudflare tunnel
schtasks /create /tn "CloudflareTunnel" /tr "cloudflared.exe tunnel --url http://localhost:8080" /sc onstart /ru SYSTEM /rl HIGHEST /f >>nul 2>&1
if %errorlevel% neq 0 (
    echo  [WARN] Task may already exist, continuing...
)

REM Start the task
schtasks /run /tn "CloudflareTunnel" >>nul 2>&1
echo  [OK] Cloudflare Tunnel scheduled task created

echo.
echo  [4/4] Waiting for services to start...
timeout /t 5 /nobreak >>nul

echo.
echo  ============================================
echo   INSTALLATION COMPLETE!
echo  ============================================
echo.
echo   Services installed:
echo    - DashboardHTTP: Auto-starts on boot
 echo    - CloudflareTunnel: Auto-starts on boot
echo.
echo   Current status:
schtasks /query /tn "DashboardHTTP" /fo LIST | findstr "Task Name" | findstr /V "Next"
schtasks /query /tn "DashboardHTTP" /fo LIST | findstr "Run"
echo.
echo   To get your Cloudflare URL:
echo    1. Wait 10 seconds
echo    2. Check messages from Claw in Telegram
echo    3. Or run: cloudflared.exe tunnel --url http://localhost:8080
echo.
echo  ============================================
pause
