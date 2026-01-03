# Dropbox

## Overview
Dropbox provides a REST API for file storage, sharing, and account management. Use a long-lived access token or OAuth 2.0 for user authorization.

## Python
```python
import requests

access_token = "DROPBOX_TOKEN"
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

resp = requests.post(
    "https://api.dropboxapi.com/2/users/get_current_account",
    headers=headers,
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$token = "DROPBOX_TOKEN"
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

Invoke-RestMethod -Method Post -Uri "https://api.dropboxapi.com/2/users/get_current_account" -Headers $headers
```

## curl
```bash
curl -X POST https://api.dropboxapi.com/2/users/get_current_account \
  -H "Authorization: Bearer DROPBOX_TOKEN" \
  -H "Content-Type: application/json"
```

## Docs
- https://www.dropbox.com/developers/documentation/http/documentation
- https://www.dropbox.com/developers/apps
