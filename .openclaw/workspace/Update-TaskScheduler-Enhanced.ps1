# Update-TaskScheduler-Enhanced.ps1 - Update to enhanced script

$TaskName = "OpenClaw-X-Autonomous-Poster"
$ScriptPath = "C:\Users\quent\.openclaw\workspace\x_post_enhanced.ps1"

# Remove old task
schtasks /delete /tn $TaskName /f 2>$null

# Create new task with enhanced script
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`" -FromQueue"

# Triggers: 08:00, 14:00, 19:00 daily
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "14:00"
$Trigger3 = New-ScheduledTaskTrigger -Daily -At "19:00"

# Settings: Run only if logged on, wake to run, don't stop
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun

# Principal: Current user
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Register
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2, $Trigger3) -Settings $Settings -Principal $Principal -Force

Write-Host "✅ Enhanced task scheduler configured!" -ForegroundColor Green
Write-Host "Script: $ScriptPath" -ForegroundColor Cyan
Write-Host "Schedule: 08:00, 14:00, 19:00" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test:" -ForegroundColor Yellow
Write-Host "  cd C:\Users\quent\.openclaw\workspace" -ForegroundColor Gray
Write-Host "  .\x_post_enhanced.ps1 -Text 'Test message'" -ForegroundColor Gray
