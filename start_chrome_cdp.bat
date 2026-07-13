@echo off
echo Killing existing Chrome processes...
taskkill /F /IM chrome.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting Chrome with remote debugging...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"

echo Waiting for Chrome to start...
timeout /t 5 /nobreak >nul

echo Testing CDP connection...
curl -s http://127.0.0.1:9222/json/list >nul
if %errorlevel% == 0 (
    echo [OK] Chrome CDP is running!
) else (
    echo [FAIL] CDP not responding. Check Chrome is running.
)

pause
