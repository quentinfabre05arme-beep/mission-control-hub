# OneDrive Organization Script
$oneDrive = $env:OneDrive

# Move loose files to appropriate folders
$geminiFiles = @('gemini_final.png', 'gemini_active.png', 'gemini_conversations.png', 'gemini_current.png', 'gemini_screenshot.png')
foreach ($file in $geminiFiles) {
    $source = Join-Path $oneDrive $file
    $dest = Join-Path $oneDrive '06-MEDIA'
    if (Test-Path $source) {
        Move-Item $source $dest -Force
        Write-Host "Moved: $file -> 06-MEDIA"
    }
}

$resourceFiles = @('TOPICS_CARD.txt', 'REQUESTS_SUMMARY.md')
foreach ($file in $resourceFiles) {
    $source = Join-Path $oneDrive $file
    $dest = Join-Path $oneDrive '02-RESSOURCES'
    if (Test-Path $source) {
        Move-Item $source $dest -Force
        Write-Host "Moved: $file -> 02-RESSOURCES"
    }
}

$devFiles = @('DASHBOARD.html', 'MOBILE_DASHBOARD.md')
foreach ($file in $devFiles) {
    $source = Join-Path $oneDrive $file
    $dest = Join-Path $oneDrive '07-DEVELOPMENT'
    if (Test-Path $source) {
        Move-Item $source $dest -Force
        Write-Host "Moved: $file -> 07-DEVELOPMENT"
    }
}

$logFiles = @('QUICK_STATUS.txt')
foreach ($file in $logFiles) {
    $source = Join-Path $oneDrive $file
    $dest = Join-Path $oneDrive '99-LOGS'
    if (Test-Path $source) {
        Move-Item $source $dest -Force
        Write-Host "Moved: $file -> 99-LOGS"
    }
}

# Move Mission Control to Development folder
$mcSource = Join-Path $oneDrive 'Mission Control'
$mcDest = Join-Path $oneDrive '07-DEVELOPMENT\Mission Control'
if (Test-Path $mcSource) {
    # Copy instead of move to preserve the structure
    Copy-Item $mcSource (Join-Path $oneDrive '07-DEVELOPMENT') -Recurse -Force
    Write-Host "Copied: Mission Control -> 07-DEVELOPMENT"
}

# Move apify-mcp-server to Development
$apifySource = Join-Path $oneDrive 'apify-mcp-server'
$apifyDest = Join-Path $oneDrive '07-DEVELOPMENT\apify-mcp-server'
if (Test-Path $apifySource) {
    Copy-Item $apifySource (Join-Path $oneDrive '07-DEVELOPMENT') -Recurse -Force
    Write-Host "Copied: apify-mcp-server -> 07-DEVELOPMENT"
}

Write-Host "`n✅ OneDrive organized!"
