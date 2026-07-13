# Organize 03-DOCUMENTS folder
$oneDrive = $env:OneDrive
$source = Join-Path $oneDrive "03-DOCUMENTS"

# Categorize and move files
$files = Get-ChildItem $source -File -ErrorAction SilentlyContinue

$stats = @{
    EPS = 0
    Admin = 0
    Formation = 0
    Other = 0
    Moved = 0
}

foreach ($file in $files) {
    $name = $file.Name.ToLower()
    $destFolder = $null
    
    # Determine category based on filename
    if ($name -match '^(ap|situation|analyse|construire|activite|cycle|domaine|pn|forme|sante|eps|competence|reinvestir|etablir|construire|acrosport|rugby|badminton|musculation|athletisme|gymnastique|dance|natation|escalade|ski|combat|raquet|basket|foot|hand|volley|hockey|lutte|judo|karate|boxe)') {
        if ($name -match '^(ap|situation|analyse|competence|cycle|domaine|pn|forme|sante|acrosport|rugby|badminton)') {
            $destFolder = "01-EPS-Enseignement\01-AP"
        } elseif ($name -match 'cours|chapitre|lecon|module|theme|axe|seance') {
            $destFolder = "01-EPS-Enseignement\02-Cours"
        } elseif ($name -match 'eval|note|bareme|grille|controle|ds|interro|quiz') {
            $destFolder = "01-EPS-Enseignement\03-Evaluations"
        } elseif ($name -match 'sequence|progression|programme|planning') {
            $destFolder = "01-EPS-Enseignement\04-Sequences"
        } else {
            $destFolder = "01-EPS-Enseignement\05-Sports"
        }
        $stats.EPS++
    }
    elseif ($name -match 'violence|adolescent|ethique|securite|prevention|apprentissage|motricite|moteur|pedago|eleve|classe|enseign|prof|education|social|inclusion|handicap|egalite') {
        $destFolder = "01-EPS-Enseignement\06-Pedagogie"
        $stats.EPS++
    }
    elseif ($name -match 'admin|contrat|bulletin|attestation|certif|diplome|stage|convention|fiche|demande|dossier|inscription|inscrit|emplo|stage|economie') {
        $destFolder = "02-Administratif"
        $stats.Admin++
    }
    elseif ($name -match 'formation|certificat|mooc|seminaire|colloque|congres') {
        $destFolder = "03-Formations"
        $stats.Formation++
    }
    
    # Move file if destination determined
    if ($destFolder) {
        $destPath = Join-Path $source $destFolder
        $destFile = Join-Path $destPath $file.Name
        
        try {
            Move-Item $file.FullName $destFile -Force -ErrorAction SilentlyContinue
            $stats.Moved++
            Write-Host "Moved: $($file.Name) -> $destFolder"
        }
        catch {
            Write-Host "Error moving: $($file.Name)"
        }
    } else {
        $stats.Other++
    }
}

Write-Host "`nOrganization Summary:"
Write-Host "EPS documents: $($stats.EPS)"
Write-Host "Administrative: $($stats.Admin)"
Write-Host "Formations: $($stats.Formation)"
Write-Host "Other (not moved): $($stats.Other)"
Write-Host "Total moved: $($stats.Moved) of $($files.Count)"
