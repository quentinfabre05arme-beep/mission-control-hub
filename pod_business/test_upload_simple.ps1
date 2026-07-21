$token = (Get-Content .env.local | Select-String "^PRINTIFY_API_KEY=").Line.Replace("PRINTIFY_API_KEY=","")

# Read and encode image
$imagePath = "generated/design_1_bitcoin_millionaire.png"
$imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
$base64Image = [System.Convert]::ToBase64String($imageBytes)

Write-Host "Image size: $($imageBytes.Length) bytes"
Write-Host "Base64 length: $($base64Image.Length) chars"

# Create upload
$body = @{
    file_name = "test_design.png"
    contents = $base64Image
} | ConvertTo-Json

Write-Host "Uploading..."

try {
    $response = Invoke-RestMethod -Uri "https://api.printify.com/v1/uploads/images.json" `
        -Method POST `
        -Headers @{"Authorization"="Bearer $token"; "Content-Type"="application/json"} `
        -Body $body
    
    Write-Host "✅ SUCCESS!"
    Write-Host "Upload ID: $($response.id)"
    Write-Host "File name: $($response.file_name)"
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $errorBody = $reader.ReadToEnd()
        Write-Host "Error details: $errorBody"
    }
}
