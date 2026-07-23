cd C:\Users\quent\.openclaw\workspace
git add mission_control/index.html mission_control/market_data.json
$commitMessage = "Cycle #193: Market data refreshed, timestamps updated ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
git commit -m $commitMessage
git push
