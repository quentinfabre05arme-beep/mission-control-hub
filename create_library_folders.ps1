# OneDrive Library Organization Script
$oneDrive = $env:OneDrive
$resources = Join-Path $oneDrive "02-RESSOURCES"

# Create library structure
$libraryFolders = @(
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING",
    "02-RESSOURCES\02-LIBRARY-NUTRITION-HEALTH",
    "02-RESSOURCES\03-LIBRARY-BUSINESS",
    "02-RESSOURCES\04-LIBRARY-INVESTMENT",
    "02-RESSOURCES\05-LIBRARY-PERSONAL-DEVELOPMENT",
    "02-RESSOURCES\06-LIBRARY-TECH-AI",
    "02-RESSOURCES\07-LIBRARY-LANGUAGES",
    "02-RESSOURCES\08-LIBRARY-COACHING",
    "02-RESSOURCES\09-LIBRARY-ARCHIVES"
)

foreach ($folder in $libraryFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

# Create subcategories for Bodybuilding
$bbFolders = @(
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING\01-Major-Authors",
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING\02-Science-Research",
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING\03-Programs-Routines",
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING\04-Practical-Guides",
    "02-RESSOURCES\01-LIBRARY-BODYBUILDING\05-Podcasts-Audio"
)

foreach ($folder in $bbFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

# Create Business subfolders
$bizFolders = @(
    "02-RESSOURCES\03-LIBRARY-BUSINESS\01-Entrepreneurship",
    "02-RESSOURCES\03-LIBRARY-BUSINESS\02-Marketing",
    "02-RESSOURCES\03-LIBRARY-BUSINESS\03-Sales",
    "02-RESSOURCES\03-LIBRARY-BUSINESS\04-Online-Business"
)

foreach ($folder in $bizFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

# Create Investment subfolders
$invFolders = @(
    "02-RESSOURCES\04-LIBRARY-INVESTMENT\01-Crypto",
    "02-RESSOURCES\04-LIBRARY-INVESTMENT\02-Stocks-ETF",
    "02-RESSOURCES\04-LIBRARY-INVESTMENT\03-Real-Estate",
    "02-RESSOURCES\04-LIBRARY-INVESTMENT\04-Macro-Economics"
)

foreach ($folder in $invFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

Write-Host "`nLibrary structure created!"
