# setup-chrome-autostart.ps1 - Configure Chrome to auto-start with X
# This ensures Chrome is always running for Task Scheduler automation

$ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $ChromePath)) {
    $ChromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}
if (-not (Test-Path $ChromePath)) {
    $ChromePath = "C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\Application\chrome.exe"
}

if (-not (Test-Path $ChromePath)) {
    Write-Host "❌ Chrome not found. Please install Chrome first." -ForegroundColor Red
    exit 1
}

Write-Host "Found Chrome at: $ChromePath" -ForegroundColor Green

# Create startup shortcut
$StartupFolder = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupFolder "Chrome-X-Autostart.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ChromePath
$Shortcut.Arguments = '--app="https://x.com" --window-size=800,600 --window-position=0,0'
$Shortcut.WorkingDirectory = Split-Path $ChromePath
$Shortcut.IconLocation = $ChromePath
$Shortcut.Save()

Write-Host "✅ Created startup shortcut: $ShortcutPath" -ForegroundColor Green
Write-Host ""
Write-Host "Chrome will now:" -ForegroundColor Cyan
Write-Host "  • Auto-start on Windows boot" -ForegroundColor Gray
Write-Host "  • Open X.com automatically" -ForegroundColor Gray
Write-Host "  • Run in app mode (minimal UI)" -ForegroundColor Gray
Write-Host ""
Write-Host "To test now:" -ForegroundColor Yellow
Write-Host "  1. Restart PC, or" -ForegroundColor Gray
Write-Host "  2. Double-click the shortcut in Startup folder" -ForegroundColor Gray
Write-Host ""
Write-Host "Startup folder location:" -ForegroundColor Yellow
Write-Host "  $StartupFolder" -ForegroundColor Gray
