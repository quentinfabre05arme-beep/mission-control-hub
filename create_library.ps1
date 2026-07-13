# OneDrive Library Organization Script
$oneDrive = $env:OneDrive
$resources = Join-Path $oneDrive "02-RESSOURCES"

# Create library structure
$libraryFolders = @(
    "02-RESSOURCES\📚 BIBLIOTHEQUE",  # Main library folder
    "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\02-Nutrition & Sante",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\03-Entrepreneuriat & Business",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\04-Investissement & Finance",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\05-Developpement Personnel",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\06-Technologie & IA",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\07-Langues & Education",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\08-Coaching & Formation",
 "02-RESSOURCES\📚 BIBLIOTHEQUE\99-Archives"
)

foreach ($folder in $libraryFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

# Create subcategories for Bodybuilding
$bbFolders = @(
    "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation\A-Autheurs Majeurs",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation\B-Science de la Musculation",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation\C-Programmes & Routines",
    "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation\D-Guides Pratiques",
 "02-RESSOURCES\📚 BIBLIOTHEQUE\01-Bodybuilding & Musculation\E-Podcasts & Audio"
)

foreach ($folder in $bbFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

Write-Host "`n✅ Library structure created!"
