# x_post_simple.ps1 - Free X Posting via Windows Automation
# Requires Chrome to be logged into X already

param(
    [string]$Text = (Get-Content "C:\Users\quent\.openclaw\workspace\x_queue.json" | ConvertFrom-Json).posts | Where-Object { $_.status -eq 'pending' } | Select-Object -First 1 -ExpandProperty text
)

$logFile = "C:\Users\quent\.openclaw\workspace\logs\x_posts.log"
$screenshotDir = "C:\Users\quent\.openclaw\workspace\screenshots"

function Write-Log($message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Write-Output $logEntry
    Add-Content -Path $logFile -Value $logEntry -ErrorAction SilentlyContinue
}

# Ensure directories exist
New-Item -ItemType Directory -Path (Split-Path $logFile) -Force -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Directory -Path $screenshotDir -Force -ErrorAction SilentlyContinue | Out-Null

Write-Log "=== X Simple Poster Starting ==="

if (-not $Text) {
    Write-Log "No pending posts found in queue"
    exit 0
}

Write-Log "Posting text: $Text"

# Check if Chrome is running
$chromeRunning = Get-Process chrome -ErrorAction SilentlyContinue
if (-not $chromeRunning) {
    Write-Log "Starting Chrome..."
    Start-Process "chrome.exe" "https://x.com/home" -WindowStyle Minimized
    Start-Sleep -Seconds 5
}

# Use AutoHotkey-style approach with PowerShell
# This simulates keyboard shortcuts in Chrome

Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        
        [DllImport("user32.dll")]
        public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, int dwExtraInfo);
        
        public const int SW_RESTORE = 9;
        public const byte VK_CONTROL = 0x11;
        public const byte VK_T = 0x54;
        public const byte VK_RETURN = 0x0D;
        public const uint KEYEVENTF_KEYUP = 0x0002;
    }
"@

# Find Chrome window
$chrome = Get-Process chrome | Where-Object { $_.MainWindowTitle -like "*X*" -or $_.MainWindowTitle -like "*Twitter*" } | Select-Object -First 1

if (-not $chrome) {
    Write-Log "Chrome window not found - opening X..."
    Start-Process "chrome.exe" "https://x.com/compose/tweet" -WindowStyle Normal
    Start-Sleep -Seconds 3
    $chrome = Get-Process chrome | Where-Object { $_.MainWindowTitle } | Select-Object -First 1
}

if ($chrome) {
    # Bring Chrome to foreground
    [WinAPI]::ShowWindow($chrome.MainWindowHandle, [WinAPI]::SW_RESTORE)
    [WinAPI]::SetForegroundWindow($chrome.MainWindowHandle)
    Start-Sleep -Milliseconds 500
    
    # Open new tab with compose URL
    [WinAPI]::keybd_event([WinAPI]::VK_CONTROL, 0, 0, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_T, 0, 0, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_T, 0, [WinAPI]::KEYEVENTF_KEYUP, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_CONTROL, 0, [WinAPI]::KEYEVENTF_KEYUP, 0)
    Start-Sleep -Milliseconds 500
    
    # Type compose URL
    [System.Windows.Forms.SendKeys]::SendWait("https://x.com/compose/tweet")
    Start-Sleep -Milliseconds 200
    [WinAPI]::keybd_event([WinAPI]::VK_RETURN, 0, 0, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_RETURN, 0, [WinAPI]::KEYEVENTF_KEYUP, 0)
    Start-Sleep -Seconds 2
    
    # Type the tweet text (simple approach - no special chars)
    [System.Windows.Forms.SendKeys]::SendWait($Text)
    Start-Sleep -Milliseconds 500
    
    # Send Ctrl+Enter to post
    [WinAPI]::keybd_event([WinAPI]::VK_CONTROL, 0, 0, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_RETURN, 0, 0, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_RETURN, 0, [WinAPI]::KEYEVENTF_KEYUP, 0)
    [WinAPI]::keybd_event([WinAPI]::VK_CONTROL, 0, [WinAPI]::KEYEVENTF_KEYUP, 0)
    
    Start-Sleep -Seconds 2
    
    Write-Log "✅ Post sent via keyboard automation"
} else {
    Write-Log "❌ Could not find or start Chrome"
}

Write-Log "=== X Simple Poster Complete ==="
