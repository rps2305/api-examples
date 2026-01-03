# Google Drive

## Overview
Google Drive provides an API for file storage, sharing, and metadata. OAuth 2.0 is required for most operations.

## Python
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/drive.metadata.readonly"])
service = build("drive", "v3", credentials=creds)

files = service.files().list(pageSize=5, fields="files(id,name)").execute()
print(files)
```

## PowerShell
```powershell
$token = "OAUTH_ACCESS_TOKEN"
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://www.googleapis.com/drive/v3/files?pageSize=5&fields=files(id,name)" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer OAUTH_ACCESS_TOKEN" \
  "https://www.googleapis.com/drive/v3/files?pageSize=5&fields=files(id,name)"
```

## Docs
- https://developers.google.com/drive/api
- https://developers.google.com/identity/protocols/oauth2
