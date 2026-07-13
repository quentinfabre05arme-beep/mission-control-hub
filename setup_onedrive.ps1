# Create OneDrive Mission Control folder structure
$oneDrive = $env:OneDrive
if (-not $oneDrive) { $oneDrive = $env:OneDriveConsumer }
if (-not $oneDrive) { $oneDrive = "C:\Users\$env:USERNAME\OneDrive" }
if (-not (Test-Path $oneDrive)) { $oneDrive = "C:\Users\$env:USERNAME\OneDrive - Personal" }

if (Test-Path $oneDrive) {
    Write-Host "Found OneDrive at: $oneDrive"
    
    $mcFolder = Join-Path $oneDrive "Mission Control"
    $folders = @(
        "Mission Control",
        "Mission Control\Dashboard",
        "Mission Control\Content", 
        "Mission Control\Scripts",
        "Mission Control\Data",
        "Mission Control\Archive"
    )
    
    foreach ($folder in $folders) {
        $path = Join-Path $oneDrive $folder
        New-Item -ItemType Directory -Force -Path $path | Out-Null
        Write-Host "Created: $folder"
    }
    
    Write-Host "`n✅ Mission Control folder structure created!"
    Write-Host "Location: $mcFolder"
} else {
    Write-Host "❌ OneDrive not found"
}
