# Prowlarr

## Overview
Prowlarr provides an API for managing indexers and querying status. It uses an API key header for authentication.

## Python
```python
import requests

base_url = "http://prowlarr.example.com:9696/api/v1"
headers = {"X-Api-Key": "PROWLARR_API_KEY"}

resp = requests.get(f"{base_url}/system/status", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ "X-Api-Key" = "PROWLARR_API_KEY" }
Invoke-RestMethod -Uri "http://prowlarr.example.com:9696/api/v1/system/status" -Headers $headers
```

## curl
```bash
curl -H "X-Api-Key: PROWLARR_API_KEY" \
  http://prowlarr.example.com:9696/api/v1/system/status
```

## Docs
- https://wiki.servarr.com/prowlarr
- https://github.com/Prowlarr/Prowlarr
