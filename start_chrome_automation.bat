@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo  CHROME AUTOMATION STARTUP
echo ========================================

:CHECK_CHROME
REM Check if Chrome already has CDP
curl -s http://127.0.0.1:9222/json/version >NUL 2>NUL
if %ERRORLEVEL% == 0 (
    echo [OK] Chrome CDP already running
    goto VERIFY
)

REM Kill existing Chrome
echo [STEP 1] Stopping Chrome...
taskkill /F /IM chrome.exe >NUL 2>NUL
timeout /t 3 /nobreak >NUL

REM Start Chrome with CDP
echo [STEP 2] Starting Chrome with debugging...
start "ChromeCDP" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"

REM Wait for startup
echo [STEP 3] Waiting for Chrome to initialize...
timeout /t 5 /nobreak >NUL

:VERIFY
echo [STEP 4] Verifying CDP connection...
set RETRIES=0
:RETRY
curl -s http://127.0.0.1:9222/json/version > cdp_response.txt 2>NUL
if %ERRORLEVEL% == 0 (
    echo [SUCCESS] Chrome CDP is running on port 9222
    type cdp_response.txt
    del cdp_response.txt 2>NUL
    goto DONE
) else (
    set /a RETRIES+=1
    if !RETRIES! lss 5 (
        echo [RETRY] Attempt !RETRIES!/5...
        timeout /t 2 /nobreak >NUL
        goto RETRY
    ) else (
        echo [FAIL] Could not establish CDP connection
        echo [TROUBLESHOOT] Check if Chrome actually started
        del cdp_response.txt 2>NUL
        pause
        exit /b 1
    )
)

:DONE
echo.
echo ========================================
echo Chrome is ready for automation!
echo CDP URL: http://127.0.0.1:9222
echo ========================================
pause
