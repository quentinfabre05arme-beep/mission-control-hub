@echo off
echo ========================================
echo  FORCE CHROME CDP STARTUP
echo ========================================
echo.

REM Kill all Chrome
echo [STEP 1] Killing Chrome processes...
taskkill /F /IM chrome.exe 2>NUL
if %ERRORLEVEL% == 0 (
    echo [OK] Chrome killed
) else (
    echo [INFO] Chrome not running
)
timeout /t 2 /nobreak >NUL

REM Clear Chrome lock files (sometimes prevents restart)
echo [STEP 2] Clearing lock files...
rd /S /Q "%LOCALAPPDATA%\Google\Chrome\User Data\ShaderCache" 2>NUL
del /F /Q "%LOCALAPPDATA%\Google\Chrome\User Data\*lockfile*" 2>NUL

REM Start Chrome with CDP using START command
echo [STEP 3] Starting Chrome with CDP...
echo Command: chrome.exe --remote-debugging-port=9222
echo.

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
    --remote-debugging-port=9222 ^
    --no-first-run ^
    --no-default-browser-check ^
    --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"

echo [OK] Chrome started
echo.
timeout /t 5 /nobreak >NUL

REM Test connection
echo [STEP 4] Testing CDP connection...
curl -s http://127.0.0.1:9222/json/version > cdp_test.txt 2>NUL

if exist cdp_test.txt (
    for /f "tokens=*" %%a in (cdp_test.txt) do (
        echo [OK] CDP Response: %%a
    )
    del cdp_test.txt
    echo.
    echo ========================================
    echo [SUCCESS] CDP is working!
    echo Port: 9222
    echo URL: http://127.0.0.1:9222
    echo ========================================
) else (
    echo [FAIL] CDP not responding
    echo.
    echo ========================================
    echo [TROUBLESHOOTING]
    echo 1. Check Chrome actually started
    echo 2. Try running Chrome as Administrator
    echo 3. Check Windows Firewall
    echo ========================================
)

pause
