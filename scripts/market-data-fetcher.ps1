# Market Data Fetcher for Twelve Data API
# Uses quote endpoint to get multiple data points in single call
# Rate limit: 8 API calls/minute on free tier

param(
    [string]$ApiKey = "07f9ead31a5c426ea238e71895beeaa1",
    [string]$OutputPath = "$env:USERPROFILE\.openclaw\workspace\mission_control\market_data.json"
)

# Use quote endpoint - gets price, change, volume in one call
$Symbols = @("BTC/USD", "ETH/USD", "MSTR", "HIMS")
$Results = @{}
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "=== Fetching Market Data ===" -ForegroundColor Cyan
Write-Host "Time: $Timestamp" -ForegroundColor Gray

foreach ($Symbol in $Symbols) {
    Write-Host "`nFetching $Symbol..." -ForegroundColor Yellow
    
    try {
        # Quote endpoint returns: close (current price), change, percent_change, volume, etc.
        $QuoteData = Invoke-RestMethod -Uri "https://api.twelvedata.com/quote?symbol=$Symbol&apikey=$ApiKey" -TimeoutSec 15
        
        if ($QuoteData.status -eq "error") {
            throw $QuoteData.message
        }
        
        $Results[$Symbol] = @{
            price = $QuoteData.close  # close = current price
            open = $QuoteData.open
            high = $QuoteData.high
            low = $QuoteData.low
            change = $QuoteData.change
            percent_change = $QuoteData.percent_change
            volume = $QuoteData.volume
            is_market_open = $QuoteData.is_market_open
            timestamp = $Timestamp
            status = "success"
        }
        
        Write-Host "  Price: $($QuoteData.close)" -ForegroundColor Green
        Write-Host "  Change: $($QuoteData.change) ($($QuoteData.percent_change)%)" -ForegroundColor Cyan
        Write-Host "  Volume: $($QuoteData.volume)" -ForegroundColor Magenta
        
    } catch {
        $Results[$Symbol] = @{
            error = $_.Exception.Message
            timestamp = $Timestamp
            status = "error"
        }
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Wait 8 seconds between symbols (7.5 seconds = 8 calls/minute limit)
    if ($Symbol -ne $Symbols[-1]) {
        Write-Host "  Waiting 8 seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds 8
    }
}

# Save to JSON
$JsonData = @{
    timestamp = $Timestamp
    assets = $Results
} | ConvertTo-Json -Depth 3

$JsonData | Out-File -FilePath $OutputPath -Encoding UTF8

Write-Host "`n=== Data Saved ===" -ForegroundColor Green
Write-Host "File: $OutputPath" -ForegroundColor Gray
