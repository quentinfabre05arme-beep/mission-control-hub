@echo off
REM OpenClaw Auto-Start Script
REM Runs when Windows starts

echo Starting OpenClaw Gateway and Dashboard Server...
cd /d "C:\Users\quent\.openclaw\workspace"

REM Start OpenClaw Gateway in background
start /min "OpenClaw Gateway" cmd /c "openclaw gateway start && echo OpenClaw started successfully || echo Failed to start OpenClaw"

REM Start Dashboard HTTP Server for phone access (wait 5 sec for OpenClaw to start)
timeout /t 5 /nobreak >nul
start /min "Dashboard Server" cmd /c "python -m http.server 8080"

echo OpenClaw and Dashboard server startup initiated.
echo Dashboard accessible at: http://192.168.1.69:8080
