@echo off
echo ========================================
echo  RUN CHROME AS ADMINISTRATOR
echo ========================================
echo.
echo This batch file will:
echo 1. Request Administrator privileges
echo 2. Start Chrome with debugging port
echo 3. Enable full automation
echo.
echo Click YES on the UAC prompt that appears.
echo.
pause

REM Self-elevate if not running as admin
net session >NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Running as admin now
echo [OK] Running with Administrator privileges
echo.

REM Kill Chrome
echo [STEP 1] Stopping Chrome...
taskkill /F /IM chrome.exe >NUL 2>NUL
timeout /t 2 /nobreak >NUL

REM Start Chrome with CDP
echo [STEP 2] Starting Chrome with debugging...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"
timeout /t 3 /nobreak >NUL

REM Test CDP
echo [STEP 3] Testing CDP...
timeout /t 2 /nobreak >NUL
curl -s http://127.0.0.1:9222/json/version > cdp_test.txt
if exist cdp_test.txt (
    echo [SUCCESS] CDP is working!
    type cdp_test.txt
    del cdp_test.txt
    echo.
    echo Chrome is ready for automation.
    echo.
    echo You can now run:
    echo   python x_automation_cdp.py test
) else (
    echo [FAIL] CDP not responding
)

pause
