@echo off
echo Creating elevated Task Scheduler job for Chrome CDP...
echo.
echo This will request Administrator privileges when the task runs.
echo.

REM Create task with highest privileges
schtasks /create /tn "X-Automation-Elevated" ^
    /tr "C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222" ^
    /sc onlogon ^
    /rl HIGHEST ^
    /f

if %ERRORLEVEL% == 0 (
    echo [SUCCESS] Task created with HIGHEST privileges
    echo.
    echo When you log in, Windows will prompt for admin rights
    echo and Chrome will start with CDP enabled.
    echo.
    echo To run now: schtasks /run /tn "X-Automation-Elevated"
) else (
    echo [FAIL] Could not create elevated task
    echo This requires Administrator privileges
)

pause
