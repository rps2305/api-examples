# YouTubeDL-Material

## Overview
YouTubeDL-Material is a self-hosted web UI for downloading media via `yt-dlp`. Its API lets you queue downloads, query jobs, and fetch server status.

## Python
```python
import requests

base_url = "https://youtubedl.example.com"
api_key = "API_KEY"

payload = {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "best",
}

headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json",
}

resp = requests.post(f"{base_url}/api/v2/downloads", json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "https://youtubedl.example.com"
$apiKey = "API_KEY"

$payload = @{
  url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  format = "best"
} | ConvertTo-Json

$headers = @{
  "X-Api-Key" = $apiKey
  "Content-Type" = "application/json"
}

Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v2/downloads" -Headers $headers -Body $payload
```

## curl
```bash
curl -X POST "https://youtubedl.example.com/api/v2/downloads" \
  -H "X-Api-Key: API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "best"
  }'
```

## Docs
- https://youtubedl-material.stoplight.io/docs/youtubedl-material/6c882327a57ed-youtube-dl-material-api-docs-official
