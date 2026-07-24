# OneDrive Online-Only Script
$oneDrivePath = "$env:OneDrive"
Write-Host "=== OneDrive Online-Only Configuration ===" -ForegroundColor Green
Write-Host "OneDrive path: $oneDrivePath"

# Get initial size
$sizeBefore = (Get-ChildItem $oneDrivePath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
Write-Host "Current local size: $([math]::Round($sizeBefore/1GB,2)) GB"
Write-Host ""

# Method: Clear local content by removing files from local storage
# Files remain in cloud and download on demand
$files = Get-ChildItem $oneDrivePath -Recurse -File | Where-Object { $_.Length -gt 1MB }
$totalFiles = $files.Count
$processed = 0
$skipped = 0

Write-Host "Processing $totalFiles files to set online-only..." -ForegroundColor Cyan

foreach ($file in $files) {
    try {
        # Use attrib to make file online-only (cloud-only)
        # +U = Unpinned (cloud-only), -P = Not pinned
        $result = & attrib -p +u "$($file.FullName)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            $processed++
        } else {
            $skipped++
        }
    }
    catch {
        $skipped++
    }
    
    # Progress every 1000 files
    if ($processed % 1000 -eq 0) {
        Write-Host "Processed $processed files..."
    }
}

Write-Host ""
Write-Host "Complete!" -ForegroundColor Green
Write-Host "Files set to online-only: $processed"
Write-Host "Files skipped: $skipped"

# Final size check
$sizeAfter = (Get-ChildItem $oneDrivePath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$freed = $sizeBefore - $sizeAfter
Write-Host ""
Write-Host "Final local size: $([math]::Round($sizeAfter/1GB,2)) GB"
Write-Host "Space freed: $([math]::Round($freed/1GB,2)) GB" -ForegroundColor Cyan