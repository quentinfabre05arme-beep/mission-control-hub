# Token Monitor for Ollama Cloud
# Tracks daily token usage and alerts if approaching limits

$LOG_FILE = "C:\Users\quent\.openclaw\workspace\logs\token_usage.log"
$DAILY_LIMIT = 50000  # Target: 50K tokens/day
$WARNING_THRESHOLD = 0.8  # Alert at 80%

function Get-TodayTokenUsage {
    # Get today's date
    $today = (Get-Date).ToString("yyyy-MM-dd")
    
    # Read log file if exists
    if (Test-Path $LOG_FILE) {
        $entries = Get-Content $LOG_FILE | Where-Object { $_.StartsWith($today) }
        if ($entries) {
            $total = 0
            foreach ($entry in $entries) {
                if ($entry -match "Tokens:\s*(\d+)") {
                    $total += [int]$matches[1]
                }
            }
            return $total
        }
    }
    return 0
}

function Log-TokenUsage {
    param([int]$tokens)
    
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $entry = "$timestamp | Tokens: $tokens | Session: $($env:COMPUTERNAME)"
    
    # Ensure log directory exists
    $logDir = Split-Path $LOG_FILE -Parent
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    Add-Content -Path $LOG_FILE -Value $entry
}

function Check-TokenLimit {
    $used = Get-TodayTokenUsage
    $percentage = ($used / $DAILY_LIMIT) * 100
    
    if ($percentage -ge ($WARNING_THRESHOLD * 100)) {
        Write-Output "WARNING: Token usage at $([math]::Round($percentage, 1))% of daily limit ($used / $DAILY_LIMIT)"
        
        if ($percentage -ge 100) {
            Write-Output "CRITICAL: Daily token limit exceeded!"
            # Could send notification here
        }
    } else {
        Write-Output "Token usage OK: $used / $DAILY_LIMIT ($([math]::Round($percentage, 1))%)"
    }
}

# Main execution
if ($MyInvocation.InvocationName -ne '.') {
    Check-TokenLimit
}
