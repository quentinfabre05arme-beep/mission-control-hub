# Debug Chrome CDP connection
Write-Host "=== Chrome CDP Debug ===" -ForegroundColor Cyan

# Check if Chrome is running
$chrome = Get-Process chrome -ErrorAction SilentlyContinue | Select-Object -First 1
if ($chrome) {
    Write-Host "Chrome PID: $($chrome.Id)" -ForegroundColor Green
    
    # Check all ports Chrome is using
    Write-Host "`nChecking Chrome ports..." -ForegroundColor Yellow
    try {
        $connections = Get-NetTCPConnection -OwningProcess $chrome.Id -ErrorAction Stop
        $connections | Where-Object { $_.State -eq 'Listen' } | 
            Select-Object LocalAddress, LocalPort, State | 
            Format-Table -AutoSize
    } catch {
        Write-Host "Could not get port info: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Chrome not running!" -ForegroundColor Red
}

# Test common CDP ports
$ports = @(9222, 9223, 9224, 9229, 9333)
Write-Host "`nTesting CDP ports..." -ForegroundColor Yellow
foreach ($port in $ports) {
    try {
        $test = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
        if ($test.TcpTestSucceeded) {
            Write-Host "Port $port : OPEN" -ForegroundColor Green
            
            # Try to get version
            try {
                $response = Invoke-WebRequest -Uri "http://127.0.0.1:$port/json/version" -UseBasicParsing -TimeoutSec 2
                Write-Host "  -> CDP Version: $($response.Content | ConvertFrom-Json | Select-Object -ExpandProperty Browser)" -ForegroundColor Green
            } catch {
                Write-Host "  -> Not CDP" -ForegroundColor Yellow
            }
        } else {
            Write-Host "Port $port : Closed" -ForegroundColor Gray
        }
    } catch {
        Write-Host "Port $port : Error" -ForegroundColor Gray
    }
}

Write-Host "`n=== End Debug ===" -ForegroundColor Cyan
