# File Mover Script - Batch processing for OneDrive reorganization
$Source = "C:\Users\quent\OneDrive\Documents"
$BatchSize = 500
$Destinations = @{
    PDF = "C:\Users\quent\OneDrive\08-REFERENCE\PDFs"
    Image = "C:\Users\quent\OneDrive\06-MEDIA\Photos"
    Video = "C:\Users\quent\OneDrive\06-MEDIA\Videos"
    Audio = "C:\Users\quent\OneDrive\06-MEDIA\Audio"
    Word = "C:\Users\quent\OneDrive\03-DOCUMENTS"
    Code = "C:\Users\quent\OneDrive\07-DEVELOPMENT\Projects"
    Archive = "C:\Users\quent\OneDrive\04-ARCHIVES\Files"
}

# Create dest folders
foreach ($d in $Destinations.Values) { 
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# Extension mappings
$PDF = @('.pdf')
$Image = @('.jpg','.jpeg','.png','.gif','.bmp','.tiff','.tif','.webp','.svg','.ico','.raw','.cr2','.nef','.heic')
$Video = @('.mp4','.mov','.avi','.mkv','.wmv','.flv','.webm','.m4v','.mpg','.mpeg','.3gp')
$Audio = @('.mp3','.wav','.flac','.aac','.ogg','.wma','.cda','.m4a')
$Word = @('.doc','.docx','.odt','.rtf','.txt','.md','.xls','.xlsx','.xlsb','.ods','.ppt','.pptx','.odp','.csv','.epub')
$Code = @('.py','.js','.ts','.html','.htm','.css','.scss','.json','.xml','.yaml','.yml','.sql','.sh','.ps1','.bat','.cmd','.java','.c','.cpp','.h','.cs','.go','.php','.rb','.lua','.r','.scala','.kt','.dart','.vue','.jsx','.tsx','.ipynb','.dockerfile','.tf','.gradle','.pom','.sln','.csproj','.config','.ini','.conf','.env','.lock','.gitignore','.as2','.flipchart','.profile','.ocd')
$Archive = @('.zip','.rar','.7z','.tar','.gz','.bz2')

$Stats = @{'PDF'=0; 'Image'=0; 'Video'=0; 'Audio'=0; 'Word'=0; 'Code'=0; 'Archive'=0; 'Other'=0; 'Errors'=0}
$Moved = @()

Write-Host "Getting file list..."
$Files = Get-ChildItem -Path $Source -File -Recurse | Where-Object { 
    $p = $_.FullName
    $p -notmatch '\\(08-REFERENCE|06-MEDIA|03-DOCUMENTS|07-DEVELOPMENT|00-INBOX|01-ACTIF|02-RESSOURCES|04-ARCHIVES|05-PERSONNEL|99-LOGS)\\'
} | Select-Object -First $BatchSize

Write-Host "Processing $($Files.Count) files..."

foreach ($f in $Files) {
    try {
        $ext = $f.Extension.ToLower()
        $type = 'Other'
        if ($PDF -contains $ext) { $type = 'PDF' }
        elseif ($Image -contains $ext) { $type = 'Image' }
        elseif ($Video -contains $ext) { $type = 'Video' }
        elseif ($Audio -contains $ext) { $type = 'Audio' }
        elseif ($Word -contains $ext) { $type = 'Word' }
        elseif ($Code -contains $ext) { $type = 'Code' }
        elseif ($Archive -contains $ext) { $type = 'Archive' }
        
        $dest = $Destinations[$type]
        $Stats[$type]++
        
        # Create subfolder based on parent folder name
        $parent = $f.Directory.Name
        if ($parent -eq 'Documents') { $parent = 'Root' }
        $destPath = Join-Path $dest $parent
        
        if (!(Test-Path $destPath)) { 
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null 
        }
        
        # Handle duplicates
        $target = Join-Path $destPath $f.Name
        $counter = 1
        while (Test-Path $target) {
            $newName = $f.BaseName + "_" + $counter + $ext
            $target = Join-Path $destPath $newName
            $counter++
        }
        
        Move-Item -Path $f.FullName -Destination $target -Force
        $Moved += $f.FullName
    }
    catch {
        $Stats['Errors']++
    }
}

Write-Host "`n=== BATCH RESULTS ==="
Write-Host "Moved: $($Moved.Count) files"
$Stats.Keys | Sort-Object | ForEach-Object { 
    if ($Stats[$_] -gt 0) { Write-Host "  $_`: $($Stats[$_])" }
}

# Update progress file
$progFile = "C:\Users\quent\.openclaw\workspace\ONEDRIVE_REORG_PROGRESS.json"
$prog = @{}
if (Test-Path $progFile) { 
    $content = Get-Content $progFile -Raw
    if ($content) { try { $prog = ($content | ConvertFrom-Json) } catch {} }
}

$cb = 0
if ($prog.current_batch) { $cb = $prog.current_batch }
$cb = $cb + 1

$currentTotal = 800
if ($prog.total_processed) { $currentTotal = $prog.total_processed }
$currentTotal = $currentTotal + $Moved.Count

$batchEntry = @{
    batch_number = $cb
    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    files_processed = $Moved.Count
    stats = $Stats
}

$existingBatches = @()
if ($prog.batches) { $existingBatches = $prog.batches }
$existingBatches += $batchEntry

$prog['current_batch'] = $cb
$prog['total_processed'] = $currentTotal
$prog['last_update'] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
$prog['status'] = "running"
if (!$prog['started']) { $prog['started'] = "2026-07-10T13:22:00" }
$prog['total_target'] = 45000
$prog['batches'] = $existingBatches

$remaining = 45000 - $currentTotal
$minutesLeft = [math]::Ceiling($remaining / $BatchSize * 0.5)
$eta = (Get-Date).AddMinutes($minutesLeft).ToString("yyyy-MM-ddTHH:mm:ss")
$prog['estimated_completion'] = $eta

$prog | ConvertTo-Json -Depth 5 | Set-Content $progFile

Write-Host "Total processed: $currentTotal / 45000"
Write-Host "ETA: $eta"

if (($Files.Count - $Moved.Count) -gt 0) { exit 0 } else { exit 1 }
