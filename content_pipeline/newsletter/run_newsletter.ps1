# Alpha Fund Newsletter Runner
# Usage: .\run_newsletter.ps1 [-Force] [-DryRun]

param(
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$Workspace = "C:\Users\quent\.openclaw\workspace"
$ScriptPath = "$Workspace\content_pipeline\newsletter\weekly_scheduler.js"

Write-Host "📰 Alpha Fund Newsletter Generator" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "🔍 DRY RUN mode" -ForegroundColor Yellow
    node $ScriptPath --dry-run
} elseif ($Force) {
    Write-Host "⚡ FORCE mode" -ForegroundColor Yellow
    node $ScriptPath --force
} else {
    node $ScriptPath
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Done!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed with exit code $LASTEXITCODE" -ForegroundColor Red
}