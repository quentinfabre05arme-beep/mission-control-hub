# OneDrive Reorganization Script v2 - Handles long paths
param([int]$BatchSize = 500)

$SourceDir = "C:\Users\quent\OneDrive\Documents"
$DestRoot = "C:\Users\quent\OneDrive"

# Ensure destination folders exist
$DestDirs = @{
    PDF = "$DestRoot\08-REFERENCE\PDFs"
    Image = "$DestRoot\06-MEDIA\Photos"
    Video = "$DestRoot\06-MEDIA\Videos"
    Word = "$DestRoot\03-DOCUMENTS"
    Code = "$DestRoot\07-DEVELOPMENT\Projects"
    Other = "$DestRoot\04-ARCHIVES\Misc"
}

foreach ($dir in $DestDirs.Values) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force -ErrorAction SilentlyContinue | Out-Null
    }
}

# File type mappings (lowercase)
$TypeMap = @{
    '.pdf' = 'PDF'
    '.jpg' = 'Image'; '.jpeg' = 'Image'; '.png' = 'Image'; '.gif' = 'Image'; '.bmp' = 'Image'
    '.tiff' = 'Image'; '.tif' = 'Image'; '.webp' = 'Image'; '.svg' = 'Image'; '.ico' = 'Image'
    '.raw' = 'Image'; '.cr2' = 'Image'; '.nef' = 'Image'; '.heic' = 'Image'; '.heif' = 'Image'
    '.mp4' = 'Video'; '.mov' = 'Video'; '.avi' = 'Video'; '.mkv' = 'Video'; '.wmv' = 'Video'
    '.flv' = 'Video'; '.webm' = 'Video'; '.m4v' = 'Video'; '.mpg' = 'Video'; '.mpeg' = 'Video'
    '.3gp' = 'Video'; '.ts' = 'Video'; '.m2ts' = 'Video'
    '.doc' = 'Word'; '.docx' = 'Word'; '.odt' = 'Word'; '.rtf' = 'Word'; '.txt' = 'Word'
    '.md' = 'Word'; '.xls' = 'Word'; '.xlsx' = 'Word'; '.xlsb' = 'Word'; '.ods' = 'Word'
    '.ppt' = 'Word'; '.pptx' = 'Word'; '.odp' = 'Word'; '.csv' = 'Word'
}

# Code extensions
$CodeExts = @('.py', '.js', '.ts', '.html', '.htm', '.css', '.scss', '.sass', '.less', '.json', '.xml', 
              '.yaml', '.yml', '.sql', '.sh', '.ps1', '.bat', '.cmd', '.java', '.c', '.cpp', '.h', '.hpp',
              '.cs', '.go', '.rs', '.swift', '.php', '.rb', '.pl', '.lua', '.r', '.m', '.scala', '.kt',
              '.dart', '.vue', '.jsx', '.tsx', '.ipynb', '.dockerfile', '.tf', '.gradle', '.pom', '.sln',
              '.csproj', '.config', '.ini', '.conf', '.cfg', '.env', '.lock', '.mod', '.gitignore',
              '.as2', '.flipchart', '.profile')

$ProgressFile = "C:\Users\quent\.openclaw\workspace\ONEDRIVE_REORG_PROGRESS.json"
$Progress = @{}
if (Test-Path $ProgressFile) {
    $Progress = Get-Content $ProgressFile -Raw | ConvertFrom-Json -AsHashtable
}
if (!$Progress) { $Progress = @{} }

# Get processed files list
$Processed = @{}
if ($Progress.batches) {
    foreach ($b in $Progress.batches) {
        if ($b.files_moved) {
            foreach ($f in $b.files_moved) { $Processed[$f] = $true }
        }
    }
}

$CurrentBatch = $Progress.current_batch
if (!$CurrentBatch) { $CurrentBatch = 0 }
$CurrentBatch++

Write-Host "Scanning for files to organize (Batch $CurrentBatch)..."

# Get files with exclusion filter
$Files = Get-ChildItem -LiteralPath $SourceDir -File -Recurse | Where-Object {
    $p = $_.FullName
    !$Processed.ContainsKey($p) -and
    $p -notlike '*\08-REFERENCE\*' -and
    $p -notlike '*\06-MEDIA\*' -and
    $p -notlike '*\03-DOCUMENTS\*' -and
    $p -notlike '*\07-DEVELOPMENT\*' -and
    $p -notlike '*\00-INBOX\*' -and
    $p -notlike '*\01-ACTIF\*' -and
    $p -notlike '*\02-RESSOURCES\*' -and
    $p -notlike '*\04-ARCHIVES\*' -and
    $p -notlike '*\05-PERSONNEL\*' -and
    $p -notlike '*\99-LOGS\*'
} | Select-Object -First $BatchSize

$Total = $Files.Count
Write-Host "Processing $Total files..."

if ($Total -eq 0) {
    Write-Host "No files remaining!"
    exit 0
}

$Stats = @{ PDF = 0; Image = 0; Video = 0; Word = 0; Code = 0; Other = 0; Errors = 0 }
$Moved = @()
$Start = Get-Date

foreach ($File in $Files) {
    try {
        $Ext = $File.Extension.ToLower()
        $Type = $null
        
        if ($TypeMap.ContainsKey($Ext)) {
            $Type = $TypeMap[$Ext]
        } elseif ($CodeExts -contains $Ext) {
            $Type = 'Code'
        } else {
            $Type = 'Other'
        }
        
        $DestFolder = $DestDirs[$Type]
        $Stats[$Type]++
        
        # Create flat structure in destination (preserve folder names but flatten)
        $RelDir = $File.DirectoryName.Substring($SourceDir.Length).TrimStart('\')
        if ($RelDir -and $RelDir.Length -gt 0) {
            # Use first level folder only to avoid deep nesting
            $FirstFolder = $RelDir.Split('\')[0]
            $TargetPath = Join-Path $DestFolder $FirstFolder
        } else {
            $TargetPath = $DestFolder
        }
        
        # Ensure path exists with long path support
        $LongTarget = "\\?\$TargetPath"
        if (!(Test-Path -LiteralPath $TargetPath)) {
            New-Item -ItemType Directory -Path $TargetPath -Force -ErrorAction SilentlyContinue | Out-Null
        }
        
        # Generate unique filename
        $TargetFile = Join-Path $TargetPath $File.Name
        $Counter = 1
        $BaseName = $File.BaseName
        while (Test-Path -LiteralPath $TargetFile) {
            $NewName = "$BaseName`_" + ($Counter++) + $Ext
            $TargetFile = Join-Path $TargetPath $NewName
        }
        
        # Move with robocopy for long path support
        $RoboArgs = @('"' + $File.FullName + '"', '"' + $TargetFile + '"', '/mov', '/r:0', '/w:0')
        $RoboResult = & robocopy (Split-Path $File.FullName -Parent) $TargetPath $File.Name /mov /r:0 /w:0 2>&1
        
        if ($LASTEXITCODE -lt 8) {  # Robocopy success codes are 0-7
            $Moved += $File.FullName
        } else {
            # Fallback to Move-Item
            Move-Item -LiteralPath $File.FullName -Destination $TargetFile -Force -ErrorAction SilentlyContinue
            $Moved += $File.FullName
        }
        
    } catch {
        $Stats.Errors++
    }
}

$Duration = ((Get-Date) - $Start).TotalSeconds

# Update progress
$TotalProc = $Progress.total_processed
if (!$TotalProc) { $TotalProc = 800 }  # From original progress
$TotalProc += $Moved.Count

$Remaining = 45000 - $TotalProc
$BatchesLeft = [math]::Ceiling($Remaining / $BatchSize)
$ETA = (Get-Date).AddSeconds($BatchesLeft * $Duration).ToString("yyyy-MM-ddTHH:mm:ss")

$BatchData = @{
    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    batch_number = $CurrentBatch
    files_moved = $Moved.Count
    stats = $Stats
}

if (!$Progress.batches) { $Progress.batches = @() }
$Progress.batches += $BatchData
$Progress.current_batch = $CurrentBatch
$Progress.total_processed = $TotalProc
$Progress.last_update = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
$Progress.estimated_completion = $ETA
$Progress.status = "running"

$Progress | ConvertTo-Json -Depth 10 | Set-Content $ProgressFile

Write-Host "`n=== BATCH $CurrentBatch COMPLETE ==="
Write-Host "Moved: $($Moved.Count) files"
Write-Host "  PDFs: $($Stats.PDF) | Images: $($Stats.Image) | Videos: $($Stats.Video)"
Write-Host "  Docs: $($Stats.Word) | Code: $($Stats.Code) | Other: $($Stats.Other)"
Write-Host "  Errors: $($Stats.Errors)"
Write-Host "Total: $TotalProc / 45000"
Write-Host "ETA: $ETA"

# Continue if more files exist
$MoreFiles = Get-ChildItem -LiteralPath $SourceDir -File -Recurse | Where-Object {
    $p = $_.FullName
    !$Processed.ContainsKey($p) -and !$Moved.Contains($p) -and
    $p -notlike '*\08-REFERENCE\*' -and
    $p -notlike '*\06-MEDIA\*' -and
    $p -notlike '*\03-DOCUMENTS\*' -and
    $p -notlike '*\07-DEVELOPMENT\*'
} | Select-Object -First 1

if ($MoreFiles) {
    exit 0  # More to process
} else {
    exit 1  # Done
}
