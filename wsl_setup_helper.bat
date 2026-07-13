@echo off
REM WSL Setup Helper for Windows
REM Run this after WSL installation completes and PC is restarted

echo ========================================
echo WSL Setup Helper
echo ========================================
echo.

REM Check if WSL is installed
echo Checking WSL status...
wsl --list --verbose >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL not found. Please install WSL first.
    echo Run: wsl --install --distribution Ubuntu
    pause
    exit /b 1
)

echo WSL is installed!
echo.

REM Start Ubuntu
echo Starting Ubuntu for first setup...
echo You will need to create a username and password.
echo.
pause

wsl -d Ubuntu

echo.
echo Ubuntu session closed.
echo.

REM Instructions for next steps
echo ========================================
echo Next Steps:
echo ========================================
echo 1. In Ubuntu, run: bash /mnt/c/Users/quent/.openclaw/workspace/wsl_post_install.sh
echo.
echo 2. After that completes, set the environment variable:
echo    [Environment]::SetEnvironmentVariable("XTF_NITTER", "http://127.0.0.1:8788", "User")
echo.
echo 3. Test with: xtf --search "test" --limit 3
echo.
echo 4. Run the pipeline: python enhanced_research_pipeline.py
echo.

pause
