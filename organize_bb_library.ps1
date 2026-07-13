# Organize bodybuilding books by author
$oneDrive = $env:OneDrive
$source = Join-Path $oneDrive '02-RESSOURCES\Formations et Bodybuilding\bodybuilding'
$dest = Join-Path $oneDrive '02-RESSOURCES\01-LIBRARY-BODYBUILDING\01-Major-Authors'

$authors = @(
    '3d muscle journey',
    'Bret Contreras',
    'Eric Cressey', 
    'Jeff Nippard',
    'brad schoenfeld',
    'chris beardsley',
    'layne norton',
    'mike israetel',
    'Lyle Mcdonald',
    'charles poliquin',
    'jim stoppani',
    'Mike matthews',
    'Olivier Lafay',
    'christian thibaudeau',
    'Nick Tuminello',
    'Mountain dog'
)

foreach ($author in $authors) {
    $srcPath = Join-Path $source $author
    if (Test-Path $srcPath) {
        Copy-Item $srcPath $dest -Recurse -Force
        Write-Host "Copied: $author"
    }
}

# Move other folders to appropriate categories
$guidesDest = Join-Path $oneDrive '02-RESSOURCES\01-LIBRARY-BODYBUILDING\04-Practical-Guides'
$guides = @('buff dudes', 'Programs examples', 'Bodyweight')
foreach ($guide in $guides) {
    $srcPath = Join-Path $source $guide
    if (Test-Path $srcPath) {
        Copy-Item $srcPath $guidesDest -Recurse -Force
        Write-Host "Copied guide: $guide"
    }
}

# Move science materials
$scienceDest = Join-Path $oneDrive '02-RESSOURCES\01-LIBRARY-BODYBUILDING\02-Science-Research'
$science = @('Body autres auteurs', 'JPS podcast')
foreach ($item in $science) {
    $srcPath = Join-Path $source $item
    if (Test-Path $srcPath) {
        Copy-Item $srcPath $scienceDest -Recurse -Force
        Write-Host "Copied to science: $item"
    }
}

Write-Host "`n✅ Bodybuilding library organized!"
