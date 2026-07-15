# XActions Direct API - Post via auth_token
# This uses X/Twitter's internal API endpoints with session authentication

$authToken = "9067dbd3e390766b7eae9e05eb4e931215ea0d33"
$csrfToken = "YOUR_CSRF_TOKEN_HERE"  # Need this too

# X API endpoint for posting
tweetText = "Test post from XActions automation"

# Headers required
$headers = @{
    "authorization" = "Bearer AAAAAAAAAAAAAAAAAAAA..."
    "x-csrf-token" = $csrfToken
    "cookie" = "auth_token=$authToken; ct0=$csrfToken"
    "content-type" = "application/json"
}

# Note: This requires more tokens - csrf_token from cookies too
# Full implementation would need:
# 1. auth_token (you provided)
# 2. csrf_token (from cookies, ct0 value)
# 3. Proper headers with Bearer token

Write-Output "XActions auth_token configured: $authToken"
Write-Output ""
Write-Output "Need csrf_token (ct0 cookie) to complete setup"
