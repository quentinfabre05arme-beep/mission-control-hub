# Mission Control Vercel Auto-Deploy Script
# Usage: ./deploy-vercel.ps1
# This script ensures the latest dashboard is always deployed

Write-Host "🚀 Mission Control Vercel Deployer" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check if we're in the right directory
$workspace = "$env:USERPROFILE\.openclaw\workspace"
Set-Location $workspace

# Get current dashboard version from index.html
$versionTag = Select-String -Path "$workspace\mission_control\index.html" -Pattern 'version-tag' | Select-Object -First 1
if ($versionTag) {
    $version = [regex]::Match($versionTag, 'v\d+\.\d+').Value
    Write-Host "📦 Detected version: $version" -ForegroundColor Green
} else {
    Write-Host "⚠️ Could not detect version, continuing anyway..." -ForegroundColor Yellow
}

# Ensure vercel.json points to latest
Write-Host "🔧 Updating Vercel config..." -ForegroundColor Cyan
$vercelConfig = @'
{
  "version": 2,
  "builds": [
    {
      "src": "mission_control/index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/mission_control/(.*)",
      "dest": "/mission_control/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/mission_control/index.html"
    }
  ]
}
'@
$vercelConfig | Out-File -FilePath "$workspace\vercel.json" -Encoding UTF8

# Deploy to Vercel
Write-Host "📤 Deploying to Vercel..." -ForegroundColor Cyan
try {
    $output = vercel --prod 2>&1
    Write-Host $output -ForegroundColor Gray
    
    # Extract URL from output
    $url = [regex]::Match($output, 'https://[\w-]+\.vercel\.app').Value
    if ($url) {
        Write-Host "✅ SUCCESS!" -ForegroundColor Green
        Write-Host "🌐 Live URL: $url" -ForegroundColor Green
        
        # Save URL to file for reference
        $url | Out-File -FilePath "$workspace\.vercel\latest-url.txt" -Encoding UTF8
    } else {
        Write-Host "⚠️ Deployed but couldn't extract URL from output" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
    Write-Host "Make sure Vercel CLI is installed: npm i -g vercel" -ForegroundColor Yellow
}

Write-Host "Done!" -ForegroundColor Cyan
