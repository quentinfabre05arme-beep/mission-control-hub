# OneDrive Smart Organizer
param(
    [string]$OneDrivePath = "$env:USERPROFILE\OneDrive",
    [string]$LogPath = "$env:USERPROFILE\.openclaw\workspace\logs\onedrive-organizer.log"
)

# Ensure log directory exists
$LogDir = Split-Path -Parent $LogPath
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogPath -Value $LogEntry
    Write-Host $LogEntry
}

function Get-FileCategory {
    param([string]$FileName, [string]$Extension)
    
    $FileNameLower = $FileName.ToLower()
    $Ext = $Extension.ToLower()
    
    # Books and documents
    if ($Ext -in @('.pdf', '.epub', '.mobi', '.azw', '.azw3')) {
        if ($FileNameLower -match '(training|workout|fitness|gym|muscle|strength|bodybuilding|nutrition|diet)') {
            return "Books-Library\01-Bodybuilding-Strength"
        }
        if ($FileNameLower -match '(crypto|bitcoin|ethereum|blockchain|defi|trading|invest)') {
            return "Books-Library\04-Investment-Crypto"
        }
        if ($FileNameLower -match '(business|marketing|sales|entrepreneur|startup)') {
            return "Books-Library\03-Business"
        }
        return "Books-Library\09-Other"
    }
    
    # Teaching documents
    if ($Ext -in @('.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls')) {
        if ($FileNameLower -match '(eps|school|teaching|education|student|class|lesson|pedagog)') {
            return "Teaching-EPS"
        }
        if ($FileNameLower -match '(business|invoice|contract|devis|facture)') {
            return "Business-Work"
        }
        return "Personal-Documents\Documents"
    }
    
    # Code and tech files
    if ($Ext -in @('.js', '.html', '.css', '.json', '.py', '.java', '.cpp', '.cs', '.php', '.rb', '.go', '.ts', '.jsx', '.tsx', '.vue', '.sql')) {
        return "Development-Tech\Code-Projects"
    }
    
    # Media files
    if ($Ext -in @('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mp3', '.wav', '.flac', '.aac', '.ogg')) {
        if ($FileNameLower -match '(screenshot|capture|screen)') {
            return "Media\Screenshots"
        }
        if ($Ext -in @('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')) {
            return "Media\Videos"
        }
        if ($Ext -in @('.mp3', '.wav', '.flac', '.aac', '.ogg')) {
            return "Media\Audio"
        }
        return "Media\Photos"
    }
    
    # Archives
    if ($Ext -in @('.zip', '.rar', '.7z', '.tar', '.gz')) {
        return "Personal-Documents\Archives"
    }
    
    # Default
    return "Home-Life\Misc"
}

function Remove-EmptyFolders {
    param([string]$Path)
    
    $EmptyFolders = Get-ChildItem -Path $Path -Directory -Recurse | Where-Object {
        (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object).Count -eq 0
    }
    
    foreach ($Folder in $EmptyFolders) {
        # Skip top-level folders
        if ($Folder.FullName -eq $OneDrivePath -or $Folder.Parent.FullName -eq $OneDrivePath) {
            continue
        }
        
        try {
            Remove-Item -Path $Folder.FullName -Recurse -Force -ErrorAction SilentlyContinue
            Write-Log "Removed empty folder: $($Folder.FullName)" "INFO"
        } catch {
            Write-Log "Failed to remove folder: $($Folder.FullName)" "WARN"
        }
    }
}

# Main
Write-Log "=== OneDrive Organizer Started ==="

if (!(Test-Path $OneDrivePath)) {
    Write-Log "OneDrive path not found" "ERROR"
    exit 1
}

$FilesToProcess = Get-ChildItem -Path $OneDrivePath -Recurse -File | Where-Object {
    $Parent = $_.DirectoryName
    $IsInOrganized = $false
    $OrganizedFolders = @('Books-Library', 'Teaching-EPS', 'Business-Work', 'Development-Tech', 'Media', 'Personal-Documents', 'Home-Life')
    foreach ($Folder in $OrganizedFolders) {
        if ($Parent -like "*$Folder*") {
            $IsInOrganized = $true
            break
        }
    }
    (-not $IsInOrganized) -and
    (-not $_.Attributes.HasFlag([System.IO.FileAttributes]::Hidden)) -and
    (-not $_.Attributes.HasFlag([System.IO.FileAttributes]::System))
}

Write-Log "Found $($FilesToProcess.Count) files to organize"

$MovedCount = 0
$ErrorCount = 0

foreach ($File in $FilesToProcess) {
    try {
        $Category = Get-FileCategory -FileName $File.Name -Extension $File.Extension
        $TargetPath = Join-Path -Path $OneDrivePath -ChildPath $Category
        
        if (!(Test-Path $TargetPath)) {
            New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
            Write-Log "Created directory: $TargetPath" "INFO"
        }
        
        $TargetFile = Join-Path -Path $TargetPath -ChildPath $File.Name
        
        # Handle duplicates
        if (Test-Path $TargetFile) {
            $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($File.Name)
            $Extension = [System.IO.Path]::GetExtension($File.Name)
            $Counter = 1
            do {
                $NewName = "${BaseName}_${Counter}${Extension}"
                $TargetFile = Join-Path -Path $TargetPath -ChildPath $NewName
                $Counter++
            } while (Test-Path $TargetFile)
        }
        
        Move-Item -Path $File.FullName -Destination $TargetFile -Force
        Write-Log "Moved: $($File.Name) to $Category" "INFO"
        $MovedCount++
    } catch {
        Write-Log "Failed to move: $($File.Name)" "ERROR"
        $ErrorCount++
    }
}

Remove-EmptyFolders -Path $OneDrivePath

Write-Log "=== Complete: $MovedCount moved, $ErrorCount errors ==="