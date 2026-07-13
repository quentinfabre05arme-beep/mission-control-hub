@echo off
REM Dashboard HTTP Server Auto-start
REM Runs on boot to make Mission Control accessible from phone

cd /d C:\Users\quent\.openclaw\workspace

REM Check if server is already running
netstat -an | findstr ":8080" >nul
if %errorlevel% == 0 (
    echo Dashboard server already running on port 8080
    exit /b 0
)

REM Start the HTTP server in background
start /min "Dashboard Server" pythonw -m http.server 8080

echo Dashboard server started on http://localhost:8080
echo Access from phone: http://192.168.1.69:8080
