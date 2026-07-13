@echo off
echo Creating Cloudflare Tunnel scheduled task...
echo.

REM Delete existing task if exists
schtasks /delete /tn "CloudflareTunnel" /f >>nul 2>&1

REM Create new task with proper settings
schtasks /create /tn "CloudflareTunnel" /tr "C:\Users\quent\.openclaw\workspace\cloudflared.exe tunnel --url http://localhost:8080" /sc onstart /ru SYSTEM /rl HIGHEST /f

echo.
echo Starting task...
schtasks /run /tn "CloudflareTunnel"

echo.
echo Done! The tunnel will auto-start on boot.
pause
