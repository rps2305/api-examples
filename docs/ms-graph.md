# Microsoft Graph

## Overview
Microsoft Graph provides a unified REST API for Microsoft 365 services. Authenticate with OAuth 2.0 and call endpoints under `https://graph.microsoft.com/v1.0`.

## Python
```python
import requests

token = "OAUTH_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

resp = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer OAUTH_ACCESS_TOKEN" }
Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/me" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer OAUTH_ACCESS_TOKEN" https://graph.microsoft.com/v1.0/me
```

## Docs
- https://learn.microsoft.com/graph/overview
- https://learn.microsoft.com/graph/auth/
