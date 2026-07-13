# Dashboard Services Setup Script
# Run as Administrator

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Dashboard Services Installer" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as administrator'" -ForegroundColor Yellow
    exit 1
}

# Stop any existing Python HTTP servers
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*http.server*"} | Stop-Process -Force

# Create scheduled task for HTTP server
Write-Host "Creating Dashboard HTTP Server scheduled task..." -ForegroundColor Yellow

$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "-m http.server 8080" -WorkingDirectory "C:\Users\quent\.openclaw\workspace"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "DashboardHTTPServer" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Start-ScheduledTask -TaskName "DashboardHTTPServer"

Write-Host "[OK] Dashboard HTTP Server scheduled task created and started" -ForegroundColor Green

# Create scheduled task for Cloudflare tunnel
Write-Host "Creating Cloudflare Tunnel scheduled task..." -ForegroundColor Yellow

$action2 = New-ScheduledTaskAction -Execute "C:\Users\quent\.openclaw\workspace\cloudflared.exe" -Argument "tunnel --url http://localhost:8080" -WorkingDirectory "C:\Users\quent\.openclaw\workspace"
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName "CloudflareDashboardTunnel" -Action $action2 -Trigger $trigger -Settings $settings2 -Principal $principal -Force

Start-ScheduledTask -TaskName "CloudflareDashboardTunnel"

Write-Host "[OK] Cloudflare Tunnel scheduled task created and started" -ForegroundColor Green

# Wait for tunnel to start
Write-Host "Waiting for tunnel to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Get tunnel URL from log (if it exists)
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "[OK] Services installed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard HTTP Server: Running on port 8080" -ForegroundColor Cyan
Write-Host "Cloudflare Tunnel: Running (check Task Manager)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Local URLs:" -ForegroundColor Yellow
Write-Host "  http://localhost:8080" -ForegroundColor White
Write-Host "  http://192.168.1.69:8080" -ForegroundColor White
Write-Host ""
Write-Host "To get the external Cloudflare URL, run:" -ForegroundColor Yellow
Write-Host "  cloudflared.exe tunnel --url http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "Services will auto-start on Windows boot!" -ForegroundColor Green
