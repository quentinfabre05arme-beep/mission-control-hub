# Organize Entrepreneurship files to Library
$oneDrive = $env:OneDrive
$source = Join-Path $oneDrive "01-ACTIF\Entrepreneurship"
$dest = Join-Path $oneDrive "02-RESSOURCES\03-LIBRARY-BUSINESS"

# Move subfolders to appropriate categories
$mapping = @{
    "creation" = "01-Entrepreneurship"
    "finances" = "01-Entrepreneurship"
    "montage societe" = "01-Entrepreneurship"
    "marketing" = "02-Marketing"
    "instagram" = "02-Marketing"
    "online trainer academy" = "04-Online-Business"
    "website" = "04-Online-Business"
    "Projet outils" = "04-Online-Business"
}

foreach ($item in $mapping.GetEnumerator()) {
    $srcPath = Join-Path $source $item.Key
    $dstPath = Join-Path $dest $item.Value
    
    if (Test-Path $srcPath) {
        Copy-Item $srcPath $dstPath -Recurse -Force
        Write-Host "Copied: $($item.Key) -> $($item.Value)"
    }
}

Write-Host "`n✅ Entrepreneurship files organized!"
