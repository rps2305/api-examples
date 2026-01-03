# YouTube Data API

## Overview
The YouTube Data API lets you search videos, manage channels, and upload content. It requires OAuth 2.0 for most operations.

## Python
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.readonly"])
service = build("youtube", "v3", credentials=creds)

request = service.search().list(part="snippet", q="API tutorials", maxResults=5)
response = request.execute()
print(response)
```

## PowerShell
```powershell
$token = "OAUTH_ACCESS_TOKEN"
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://www.googleapis.com/youtube/v3/search?part=snippet&q=API%20tutorials&maxResults=5" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer OAUTH_ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/search?part=snippet&q=API%20tutorials&maxResults=5"
```

## Docs
- https://developers.google.com/youtube/v3
- https://developers.google.com/identity/protocols/oauth2
