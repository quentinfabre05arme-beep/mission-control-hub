param([int]$BatchSize = 500, [int]$MaxBatches = 20)

$Source = "C:\Users\quent\OneDrive\Documents"
$ProgressFile = "C:\Users\quent\.openclaw\workspace\ONEDRIVE_REORG_PROGRESS.json"

$Destinations = @{
    PDF = "C:\Users\quent\OneDrive\08-REFERENCE\PDFs"
    Image = "C:\Users\quent\OneDrive\06-MEDIA\Photos"
    Video = "C:\Users\quent\OneDrive\06-MEDIA\Videos"
    Audio = "C:\Users\quent\OneDrive\06-MEDIA\Audio"
    Word = "C:\Users\quent\OneDrive\03-DOCUMENTS"
    Code = "C:\Users\quent\OneDrive\07-DEVELOPMENT\Projects"
    Archive = "C:\Users\quent\OneDrive\04-ARCHIVES\Files"
    Other = "C:\Users\quent\OneDrive\04-ARCHIVES\Misc"
}

foreach ($d in $Destinations.Values) { 
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

$TypeMap = @{
    '.pdf' = 'PDF'
    '.jpg' = 'Image'; '.jpeg' = 'Image'; '.png' = 'Image'; '.gif' = 'Image'; '.bmp' = 'Image'
    '.tiff' = 'Image'; '.tif' = 'Image'; '.webp' = 'Image'; '.svg' = 'Image'; '.ico' = 'Image'
    '.raw' = 'Image'; '.cr2' = 'Image'; '.nef' = 'Image'; '.heic' = 'Image'; '.heif' = 'Image'
    '.mp4' = 'Video'; '.mov' = 'Video'; '.avi' = 'Video'; '.mkv' = 'Video'; '.wmv' = 'Video'
    '.flv' = 'Video'; '.webm' = 'Video'; '.m4v' = 'Video'; '.mpg' = 'Video'; '.mpeg' = 'Video'
    '.3gp' = 'Video'; '.ts' = 'Video'; '.m2ts' = 'Video'
    '.mp3' = 'Audio'; '.wav' = 'Audio'; '.flac' = 'Audio'; '.aac' = 'Audio'; '.ogg' = 'Audio'
    '.wma' = 'Audio'; '.cda' = 'Audio'; '.m4a' = 'Audio'
    '.doc' = 'Word'; '.docx' = 'Word'; '.odt' = 'Word'; '.rtf' = 'Word'; '.txt' = 'Word'
    '.md' = 'Word'; '.xls' = 'Word'; '.xlsx' = 'Word'; '.xlsb' = 'Word'; '.ods' = 'Word'
    '.ppt' = 'Word'; '.pptx' = 'Word'; '.odp' = 'Word'; '.csv' = 'Word'; '.epub' = 'Word'
    '.zip' = 'Archive'; '.rar' = 'Archive'; '.7z' = 'Archive'; '.tar' = 'Archive'; '.gz' = 'Archive'
}

$CodeExts = @('.py','.js','.ts','.html','.htm','.css','.scss','.json','.xml','.yaml','.yml','.sql','.sh','.ps1','.bat','.cmd','.java','.c','.cpp','.h','.cs','.go','.php','.rb','.lua','.r','.scala','.kt','.dart','.vue','.jsx','.tsx','.ipynb','.dockerfile','.tf','.gradle','.pom','.sln','.csproj','.config','.ini','.conf','.env','.lock','.gitignore','.as2','.flipchart','.profile','.ocd')

$batchNum = 1
$totalMoved = 1300  # From previous runs

while ($batchNum -le $MaxBatches) {
    Write-Host "`n=== BATCH $batchNum ==="
    
    $Files = Get-ChildItem -Path $Source -File -Recurse | Where-Object { 
        $p = $_.FullName
        $p -notmatch '\\(08-REFERENCE|06-MEDIA|03-DOCUMENTS|07-DEVELOPMENT|00-INBOX|01-ACTIF|02-RESSOURCES|04-ARCHIVES|05-PERSONNEL|99-LOGS)\\'
    } | Select-Object -First $BatchSize
    
    if ($Files.Count -eq 0) {
        Write-Host "No more files to process!"
        break
    }
    
    Write-Host "Processing $($Files.Count) files..."
    
    $Stats = @{'PDF'=0; 'Image'=0; 'Video'=0; 'Audio'=0; 'Word'=0; 'Code'=0; 'Archive'=0; 'Other'=0; 'Errors'=0}
    $Moved = @()
    $Start = Get-Date
    
    foreach ($f in $Files) {
        try {
            $ext = $f.Extension.ToLower()
            $type = 'Other'
            if ($TypeMap.ContainsKey($ext)) { $type = $TypeMap[$ext] }
            elseif ($CodeExts -contains $ext) { $type = 'Code' }
            
            $dest = $Destinations[$type]
            $Stats[$type]++
            
            # Use parent folder name for organization
            $parent = $f.Directory.Name
            if ($parent -eq 'Documents') { $parent = 'Root' }
            $destPath = Join-Path $dest $parent
            
            # Ensure directory exists
            if (!(Test-Path $destPath)) { 
                New-Item -ItemType Directory -Path $destPath -Force -ErrorAction SilentlyContinue | Out-Null 
            }
            
            # Generate unique filename
            $baseName = $f.BaseName -replace '[^\w\-\.]', '_'
            $target = Join-Path $destPath ($baseName + $ext)
            $counter = 1
            while (Test-Path $target) {
                $target = Join-Path $destPath ($baseName + "_" + $counter + $ext)
                $counter++
            }
            
            # Use robocopy for reliable move
            $srcDir = '"' + $f.DirectoryName + '"'
            $dstDir = '"' + $destPath + '"'
            $fileName = $f.Name
            
            # robocopy /mov moves and deletes source
            $proc = Start-Process -FilePath "robocopy" -ArgumentList "$srcDir $dstDir `"$fileName`" /mov /r:2 /w:1" -WindowStyle Hidden -PassThru -Wait
            
            # Check if file was moved
            if (!(Test-Path $f.FullName)) {
                $Moved += $f.FullName
            } else {
                # Try fallback Move-Item
                try {
                    Move-Item -Path $f.FullName -Destination $target -Force -ErrorAction Stop
                    $Moved += $f.FullName
                } catch {
                    $Stats['Errors']++
                }
            }
        }
        catch {
            $Stats['Errors']++
        }
    }
    
    $Duration = ((Get-Date) - $Start).TotalSeconds
    $totalMoved += $Moved.Count
    
    Write-Host "Moved: $($Moved.Count) files in $([math]::Round($Duration,1))s"
    Write-Host "Total: $totalMoved / 45000"
    
    # Save progress
    $prog = @{}
    if (Test-Path $ProgressFile) { 
        try { $prog = (Get-Content $ProgressFile -Raw | ConvertFrom-Json) } catch {}
    }
    if (!$prog) { $prog = @{} }
    
    $batchEntry = @{
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        batch_number = $batchNum
        files_moved = $Moved.Count
        stats = $Stats
    }
    
    $batches = @()
    if ($prog.batches) { $batches = $prog.batches }
    $batches += $batchEntry
    
    $remaining = 45000 - $totalMoved
    $eta = (Get-Date).AddMinutes($remaining / $BatchSize * ($Duration / 60)).ToString("yyyy-MM-ddTHH:mm:ss")
    
    $prog['current_batch'] = $batchNum
    $prog['total_processed'] = $totalMoved
    $prog['last_update'] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    $prog['status'] = "running"
    $prog['total_target'] = 45000
    $prog['batches'] = $batches
    $prog['estimated_completion'] = $eta
    if (!$prog['started']) { $prog['started'] = "2026-07-10T13:22:00" }
    
    $prog | ConvertTo-Json -Depth 5 | Set-Content $ProgressFile
    
    $batchNum++
}

Write-Host "`n=== PROCESSING COMPLETE ==="
Write-Host "Total files moved: $totalMoved"
