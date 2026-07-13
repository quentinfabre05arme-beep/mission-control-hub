@echo off
echo ========================================
echo  IMPORTANT: Run this file as Administrator!
echo ========================================
echo.
echo Right-click this file and select:
echo   "Run as administrator"
echo.
echo Then click YES when Windows asks.
echo.
pause

REM Kill Chrome first
echo Stopping Chrome...
taskkill /F /IM chrome.exe >NUL 2>NUL
timeout /t 2 >NUL

REM Start Chrome with debugging
echo Starting Chrome with remote debugging on port 9222...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
timeout /t 3 >NUL

echo.
echo Chrome should now be running with debugging enabled.
echo.
pause
