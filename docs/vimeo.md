# Vimeo

## Overview
Vimeo provides a REST API for videos, folders, and user accounts.

## Python
```python
import requests

headers = {"Authorization": "Bearer VIMEO_ACCESS_TOKEN"}
resp = requests.get("https://api.vimeo.com/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer VIMEO_ACCESS_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://api.vimeo.com/me" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer VIMEO_ACCESS_TOKEN" https://api.vimeo.com/me
```

## Docs
- https://developer.vimeo.com/api/reference
