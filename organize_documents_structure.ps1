# OneDrive Full Organization Script
$oneDrive = $env:OneDrive

# Create sub-organizations for DOCUMENTS
$docFolders = @(
    "03-DOCUMENTS\01-EPS-Enseignement",      # Teaching materials
    "03-DOCUMENTS\02-Administratif",        # Admin docs  
    "03-DOCUMENTS\03-Formations",            # Training certificates
    "03-DOCUMENTS\04-Personnel",             # Personal docs
    "03-DOCUMENTS\99-Archives"              # Old docs
)

foreach ($folder in $docFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

# Create EPS subfolders
$epsFolders = @(
    "03-DOCUMENTS\01-EPS-Enseignement\01-AP",
    "03-DOCUMENTS\01-EPS-Enseignement\02-Cours",
 "03-DOCUMENTS\01-EPS-Enseignement\03-Evaluations",
    "03-DOCUMENTS\01-EPS-Enseignement\04-Sequences",
    "03-DOCUMENTS\01-EPS-Enseignement\05-Sports",
    "03-DOCUMENTS\01-EPS-Enseignement\06-Pedagogie"
)

foreach ($folder in $epsFolders) {
    $path = Join-Path $oneDrive $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Write-Host "Created: $folder"
}

Write-Host "`n✅ Document folder structure created!"
