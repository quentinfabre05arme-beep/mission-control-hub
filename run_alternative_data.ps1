# Alternative Data Fetcher for Alpha Fund
# Run: .\run_alternative_data.ps1

$scriptPath = Join-Path $PSScriptRoot "investment_fund\scripts\fetch_alternative_data.js"

Write-Host "🔄 Fetching Alternative Data for Alpha Fund..." -ForegroundColor Cyan
Write-Host ""

node $scriptPath

Write-Host ""
Write-Host "✅ Alternative data fetch complete" -ForegroundColor Green
