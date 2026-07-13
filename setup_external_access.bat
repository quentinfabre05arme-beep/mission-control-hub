@echo off
REM Setup External Dashboard Access via Cloudflare Tunnel
REM This allows access from anywhere, not just same WiFi

echo ======================================
echo Dashboard External Access Setup
echo ======================================
echo.
echo Option 1: Cloudflare Tunnel (RECOMMENDED - Free, Stable)
echo Option 2: ngrok (Quick but URL changes)
echo Option 3: LocalTunnel (Simple, free)
echo.

REM Check if cloudflared is installed
where cloudflared >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Cloudflared found
    goto :cloudflare_setup
) else (
    echo [INFO] Cloudflared not found. Installing...
    goto :install_cloudflare
)

:install_cloudflare
REM Download and install cloudflared
echo Downloading Cloudflare Tunnel...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'C:\Windows\System32\cloudflared.exe'"
if %errorlevel% == 0 (
    echo [OK] Cloudflared installed
) else (
    echo [ERROR] Failed to install Cloudflared
    echo Try manual install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
    pause
    exit /b 1
)

:cloudflare_setup
echo.
echo ======================================
echo Cloudflare Tunnel Quick Setup
echo ======================================
echo.
echo To create a permanent tunnel:
echo 1. Sign up at https://dash.cloudflare.com (free)
echo 2. Install cloudflared: cloudflared.exe login
echo 3. Create tunnel: cloudflared tunnel create dashboard
echo 4. Route traffic: cloudflared tunnel route dns dashboard your-domain.com
echo 5. Run: cloudflared tunnel run dashboard
echo.
echo For QUICK temporary access (no account needed):
echo   cloudflared tunnel --url http://localhost:8080

REM Offer quick tunnel option
echo.
set /p choice="Start quick tunnel now? (y/n): "
if /i "%choice%"=="y" (
    echo Starting Cloudflare quick tunnel...
    echo Your dashboard will be available at a public URL
    echo.
    cloudflared tunnel --url http://localhost:8080
) else (
    echo.
    echo Manual setup instructions saved to EXTERNAL_ACCESS_GUIDE.md
)

echo.
echo ======================================
echo Setup Complete
echo ======================================
pause
