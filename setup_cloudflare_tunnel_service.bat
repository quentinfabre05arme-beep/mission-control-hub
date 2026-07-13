@echo off
REM Setup Cloudflare Tunnel as Windows Service
REM Run this as Administrator after install_dashboard_service.bat

echo =========================================
echo Cloudflare Tunnel Service Setup
echo =========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Check if cloudflared exists
if not exist "C:\Users\quent\.openclaw\workspace\cloudflared.exe" (
    echo Downloading cloudflared...
    cd /d C:\Users\quent\.openclaw\workspace
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
    echo [OK] cloudflared downloaded
)

REM Install Cloudflare Tunnel service
echo Installing Cloudflare Tunnel service...
cd /d C:\Users\quent\.openclaw\workspace

C:\NSSM\nssm.exe install CloudflareTunnel "C:\Users\quent\.openclaw\workspace\cloudflared.exe"
C:\NSSM\nssm.exe set CloudflareTunnel Application "C:\Users\quent\.openclaw\workspace\cloudflared.exe"
C:\NSSM\nssm.exe set CloudflareTunnel AppParameters "tunnel --url http://localhost:8080"
C:\NSSM\nssm.exe set CloudflareTunnel DisplayName "Cloudflare Dashboard Tunnel"
C:\NSSM\nssm.exe set CloudflareTunnel Description "Cloudflare Tunnel for external dashboard access"
C:\NSSM\nssm.exe set CloudflareTunnel Start SERVICE_AUTO_START

REM Configure auto-restart
C:\NSSM\nssm.exe set CloudflareTunnel AppExit Default Restart
C:\NSSM\nssm.exe set CloudflareTunnel AppRestartDelay 10000

REM Start the service
echo Starting Cloudflare Tunnel...
net start CloudflareTunnel

if %errorlevel% == 0 (
    echo.
    echo =========================================
    echo [OK] Cloudflare Tunnel installed!
    echo =========================================
    echo.
    echo IMPORTANT: Check the tunnel URL by running:
    echo   cloudflared.exe tunnel --url http://localhost:8080
    echo.
    echo Or view the log file:
    echo   C:\Users\quent\.openclaw\workspace\tunnel.log
    echo.
    echo The tunnel URL will change on each restart.
    echo For a permanent URL, create a Cloudflare account at:
    echo   https://dash.cloudflare.com
    echo.
) else (
    echo [ERROR] Failed to start tunnel service
    echo Run manually to see error: cloudflared.exe tunnel --url http://localhost:8080
)

pause
