# OneDrive Reorganization Script
# Moves files from Documents to organized folders by type
# NO DELETION - only moves files

param(
    [int]$BatchSize = 500
)

$SourceDir = "C:\Users\quent\OneDrive\Documents"
$DestDirs = @{
    PDF = "C:\Users\quent\OneDrive\08-REFERENCE\PDFs"
    Image = "C:\Users\quent\OneDrive\06-MEDIA\Photos"
    Video = "C:\Users\quent\OneDrive\06-MEDIA\Videos"
    Word = "C:\Users\quent\OneDrive\03-DOCUMENTS"
    Code = "C:\Users\quent\OneDrive\07-DEVELOPMENT\Projects"
    Other = "C:\Users\quent\OneDrive\04-ARCHIVES\Misc"
}

# File extension mappings
$FileTypes = @{
    PDF = @('.pdf')
    Image = @('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico', '.raw', '.cr2', '.nef', '.heic', '.heif')
    Video = @('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.m2ts')
    Word = @('.doc', '.docx', '.odt', '.rtf', '.txt', '.md', '.xls', '.xlsx', '.xlsb', '.ods', '.ppt', '.pptx', '.odp', '.csv')
    Code = @('.py', '.js', '.ts', '.html', '.htm', '.css', '.scss', '.sass', '.less', '.json', '.xml', '.yaml', '.yml', 
             '.sql', '.sh', '.ps1', '.bat', '.cmd', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.swift',
             '.php', '.rb', '.pl', '.lua', '.r', '.m', '.scala', '.kt', '.kts', '.dart', '.flutter', '.vue', '.jsx', '.tsx',
             '.ipynb', '.rmd', '.dockerfile', '.tf', '.hcl', '.gradle', '.pom', '.iml', '.sln', '.csproj', '.vbproj',
             '.vcxproj', '.props', '.targets', '.pubxml', '.config', '.ini', '.conf', '.cfg', '.env', '.lock', '.sum',
             '.mod', '.gitignore', '.editorconfig', '.eslint', '.prettierrc', '.babelrc', '.webpack', '.vite', '.rollup',
             '.postcssrc', '.tailwind', '.astro', '.svelte', '.solid', '.qwik', '.nuxt', '.next', '.express', '.fastify',
             '.nest', '.prisma', '.graphql', '.gql', '.proto', '.thrift', '.avro', '.parquet', '.orc', '.arrow',
             '.wasm', '.wat', '.wgsl', '.hlsl', '.glsl', '.metal', '.cl', '.cu', '.cuh', '.hip', '.sycl',
             '.zig', '.odin', '.gleam', '.elm', '.purescript', '.idris', '.agda', '.coq', '.lean', '.isabelle',
             '.tla', '.promela', '.spin', '.z3', '.smt2', '.sat', '.cnf', '.dimacs', '.as2', '.flipchart', '.profile')
}

# Create destination directories if they don't exist
foreach ($dir in $DestDirs.Values) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Load progress
$ProgressFile = "C:\Users\quent\.openclaw\workspace\ONEDRIVE_REORG_PROGRESS.json"
$Progress = @{}
if (Test-Path $ProgressFile) {
    $Progress = Get-Content $ProgressFile | ConvertFrom-Json
}

# Get already processed files
$ProcessedFiles = @{}
if ($Progress.batches) {
    foreach ($batch in $Progress.batches) {
        if ($batch.files_processed) {
            foreach ($file in $batch.files_processed) {
                $ProcessedFiles[$file] = $true
            }
        }
    }
}

Write-Host "Loading files from Documents..."

# Get files excluding already organized folders
$ExcludePaths = @(
    '\08-REFERENCE\',
    '\06-MEDIA\',
    '\03-DOCUMENTS\',
    '\07-DEVELOPMENT\',
    '\00-INBOX\',
    '\01-ACTIF\',
    '\02-RESSOURCES\',
    '\04-ARCHIVES\',
    '\05-PERSONNEL\',
    '\99-LOGS\'
)

$AllFiles = Get-ChildItem -Path $SourceDir -File -Recurse | Where-Object {
    $fullPath = $_.FullName
    $shouldInclude = $true
    foreach ($exclude in $ExcludePaths) {
        if ($fullPath -like "*$exclude*") {
            $shouldInclude = $false
            break
        }
    }
    $shouldInclude -and !$ProcessedFiles.ContainsKey($fullPath)
}

$TotalRemaining = $AllFiles.Count
Write-Host "Found $TotalRemaining files to process"

if ($TotalRemaining -eq 0) {
    Write-Host "No files remaining to process!"
    exit 0
}

# Process in batches
$Batch = $AllFiles | Select-Object -First $BatchSize
$currentBatch = 0
if ($Progress.current_batch) { $currentBatch = $Progress.current_batch }
$BatchNumber = $currentBatch + 1

$Stats = @{
    PDF = 0
    Image = 0
    Video = 0
    Word = 0
    Code = 0
    Other = 0
    Errors = 0
}

$ProcessedInBatch = @()
$StartTime = Get-Date

Write-Host "Processing batch $BatchNumber ($($Batch.Count) files)..."

foreach ($file in $Batch) {
    try {
        $ext = $file.Extension.ToLower()
        $targetFolder = $null
        
        # Determine target folder
        foreach ($type in $FileTypes.Keys) {
            if ($FileTypes[$type] -contains $ext) {
                $targetFolder = $DestDirs[$type]
                $Stats[$type]++
                break
            }
        }
        
        if (!$targetFolder) {
            $targetFolder = $DestDirs.Other
            $Stats.Other++
        }
        
        # Create subdirectory structure in destination
        $relativePath = $file.DirectoryName.Substring($SourceDir.Length).TrimStart('\')
        $targetDir = if ($relativePath) { Join-Path $targetFolder $relativePath } else { $targetFolder }
        
        if (!(Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        
        $targetPath = Join-Path $targetDir $file.Name
        
        # Handle duplicate names
        $counter = 1
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        while (Test-Path $targetPath) {
            $newName = "$baseName`_$counter$ext"
            $targetPath = Join-Path $targetDir $newName
            $counter++
        }
        
        # Move file
        Move-Item -Path $file.FullName -Destination $targetPath -Force
        $ProcessedInBatch += $file.FullName
        
    } catch {
        $Stats.Errors++
        Write-Warning "Error moving $($file.FullName): $_"
    }
}

$EndTime = Get-Date
$Duration = ($EndTime - $StartTime).TotalSeconds

# Update progress
$totalProcessedVal = 0
if ($Progress.total_processed) { $totalProcessedVal = $Progress.total_processed }
$totalProcessedVal = $totalProcessedVal + $ProcessedInBatch.Count

$startDate = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
if ($Progress.started) { $startDate = $Progress.started }

# Calculate ETA
$filesRemaining = 45000 - $totalProcessedVal
$batchesRemaining = [math]::Ceiling($filesRemaining / $BatchSize)
$eta = (Get-Date).AddSeconds($batchesRemaining * $Duration)
$etaStr = $eta.ToString("yyyy-MM-ddTHH:mm:ss")

$ProgressData = @{
    started = $startDate
    status = "running"
    current_batch = $BatchNumber
    total_processed = $totalProcessedVal
    total_target = 45000
    last_update = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    batch_stats = $Stats
    batch_duration_seconds = [math]::Round($Duration, 2)
    estimated_completion = $etaStr
    batches = @()
}

# Update batch tracking
if ($Progress.batches) {
    $ProgressData.batches = $Progress.batches
}

$batchEntry = @{
    batch_number = $BatchNumber
    files_processed = $ProcessedInBatch.Count
    stats = $Stats
    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
}

$ProgressData.batches += $batchEntry

# Save progress
$ProgressData | ConvertTo-Json -Depth 10 | Set-Content $ProgressFile

# Summary
Write-Host "`n=== BATCH $BatchNumber COMPLETE ==="
Write-Host "Files processed: $($ProcessedInBatch.Count)"
Write-Host "  PDFs: $($Stats.PDF)"
Write-Host "  Images: $($Stats.Image)"
Write-Host "  Videos: $($Stats.Video)"
Write-Host "  Documents: $($Stats.Word)"
Write-Host "  Code files: $($Stats.Code)"
Write-Host "  Other: $($Stats.Other)"
Write-Host "  Errors: $($Stats.Errors)"
Write-Host "Duration: $([math]::Round($Duration, 2)) seconds"
Write-Host "Total processed: $totalProcessedVal / 45000"
Write-Host "ETA: $etaStr"

# Return exit code based on if more files remain
if ($TotalRemaining -gt $BatchSize) {
    exit 0
} else {
    exit 1
}
