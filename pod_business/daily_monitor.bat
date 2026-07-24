@echo off
echo ==========================================
echo Printify POD Daily Monitor - %date% %time%
echo ==========================================
cd /d "%~dp0"

node connection_test.js > logs\daily_check_%date:~-4,4%-%date:~-7,2%-%date:~-10,2%.log 2>&1

echo.
echo Daily check complete. Log saved.
echo ==========================================
pause
