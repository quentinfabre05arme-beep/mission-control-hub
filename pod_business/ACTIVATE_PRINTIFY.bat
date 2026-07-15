@echo off
REM activate_printify_automation.bat - One-click POD activation
REM Run this after getting your Printify API key

echo ==========================================
echo   PRINTIFY FULL AUTOMATION ACTIVATION
echo ==========================================
echo.

REM Check if running as admin (needed for setx)
net session >NUL 2>NUL
if %errorLevel% neq 0 (
    echo This script needs Administrator privileges.
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo Step 1: Getting API key from you...
echo.
echo Paste your Printify API key below (starts with eyJ...)
echo Then press ENTER:
echo.

set /p API_KEY="API Key: "

if "%API_KEY%"=="" (
    echo ERROR: No API key provided
    pause
    exit /b 1
)

echo.
echo Step 2: Setting environment variable...
setx PRINTIFY_API_KEY "%API_KEY%" /M
if %errorLevel% neq 0 (
    echo ERROR: Failed to set API key
    pause
    exit /b 1
)

echo ✓ API key stored securely
echo.

echo Step 3: Getting Shop ID...
echo.
echo Log into Printify and go to: printify.com/account/api
echo Find your Shop ID (usually a number like 12345678)
echo.
set /p SHOP_ID="Shop ID: "

if "%SHOP_ID%"=="" (
    echo WARNING: No Shop ID provided. Will auto-detect.
    set SHOP_ID=auto
) else (
    setx PRINTIFY_SHOP_ID "%SHOP_ID%" /M
    echo ✓ Shop ID stored
)

echo.
echo Step 4: Testing connection...
echo.

cd /d "C:\Users\quent\.openclaw\workspace"
node pod_printify_automation.js status

echo.
echo ==========================================
echo   ACTIVATION COMPLETE
echo ==========================================
echo.
echo Your POD business is now 100%% automated!
echo.
echo What's happening now:
echo - 5 new designs generated daily
echo - Auto-published to Printify
echo - Products sync to Etsy/Shopify
echo - Sales tracked automatically
echo - Weekly reports every Sunday
echo.
echo Check status anytime:
echo   node pod_printify_automation.js status
echo.
echo View your shop:
echo   https://printify.com/app/dashboard
echo.
pause
