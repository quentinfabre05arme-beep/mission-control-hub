# Setup-TaskScheduler.ps1 - Configure Windows Task Scheduler for X automation
# Run this once to set up scheduled posting

$TaskName = "OpenClaw-X-Autonomous-Poster"
$ScriptPath = "C:\Users\quent\.openclaw\workspace\x_automation_service.ps1"

# Create log directory
New-Item -ItemType Directory -Force -Path "C:\Users\quent\.openclaw\workspace\logs" | Out-Null

# Create the task action
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`""

# Create triggers for 08:00, 14:00, 19:00 daily
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "14:00"
$Trigger3 = New-ScheduledTaskTrigger -Daily -At "19:00"

# Create task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2, $Trigger3) -Settings $Settings -Force

Write-Host "✅ Task Scheduler configured successfully!" -ForegroundColor Green
Write-Host "Task: $TaskName" -ForegroundColor Cyan
Write-Host "Schedule: 08:00, 14:00, 19:00 daily" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify:" -ForegroundColor Yellow
Write-Host "  schtasks /query /tn $TaskName /fo list"
Write-Host ""
Write-Host "To run now:" -ForegroundColor Yellow
Write-Host "  schtasks /run /tn $TaskName"
Write-Host ""
Write-Host "To remove:" -ForegroundColor Yellow
Write-Host "  schtasks /delete /tn $TaskName /f"
