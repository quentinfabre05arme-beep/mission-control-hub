@echo off
REM Install Dashboard HTTP Server as Windows Service
REM Run this as Administrator (Right-click -> Run as administrator)

echo =========================================
echo Dashboard Service Installer
echo =========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Download NSSM if not exists
if not exist "C:\NSSM\nssm.exe" (
    echo Downloading NSSM...
    mkdir C:\NSSM 2>nul
    powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'C:\NSSM\nssm.zip'"
    powershell -Command "Expand-Archive -Path 'C:\NSSM\nssm.zip' -DestinationPath 'C:\NSSM' -Force"
    copy "C:\NSSM\nssm-2.24\win64\nssm.exe" "C:\NSSM\nssm.exe" >nul
    echo [OK] NSSM installed
)

REM Install HTTP Server service
echo Installing Dashboard HTTP Server service...
C:\NSSM\nssm.exe install DashboardHTTP "C:\Users\quent\AppData\Local\Programs\Python\Python313\python.exe"
C:\NSSM\nssm.exe set DashboardHTTP Application "C:\Users\quent\AppData\Local\Programs\Python\Python313\python.exe"
C:\NSSM\nssm.exe set DashboardHTTP AppParameters "-m http.server 8080 --directory C:\Users\quent\.openclaw\workspace"
C:\NSSM\nssm.exe set DashboardHTTP DisplayName "Dashboard HTTP Server"
C:\NSSM\nssm.exe set DashboardHTTP Description "Mission Control Dashboard HTTP Server"
C:\NSSM\nssm.exe set DashboardHTTP Start SERVICE_AUTO_START

REM Configure auto-restart
echo Configuring auto-restart...
C:\NSSM\nssm.exe set DashboardHTTP AppExit Default Restart
C:\NSSM\nssm.exe set DashboardHTTP AppRestartDelay 10000

REM Start the service
echo Starting service...
net start DashboardHTTP

if %errorlevel% == 0 (
    echo.
    echo =========================================
    echo [OK] Dashboard HTTP Server installed!
    echo =========================================
    echo.
    echo Service: DashboardHTTP
    echo Port: 8080
    echo Status: Running
    echo.
    echo Local URL: http://localhost:8080
    echo Local IP: http://192.168.1.69:8080
    echo.
    echo Next: Run setup_cloudflare_tunnel.bat for external access
    echo.
) else (
    echo [ERROR] Failed to start service
    echo Check Event Viewer for details
)

pause
