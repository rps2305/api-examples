# Bitbucket

## Overview
Bitbucket Cloud exposes a REST API for repositories, pull requests, and users.

## Python
```python
import requests

headers = {"Authorization": "Bearer BITBUCKET_TOKEN"}
resp = requests.get("https://api.bitbucket.org/2.0/user", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer BITBUCKET_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://api.bitbucket.org/2.0/user" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer BITBUCKET_TOKEN" https://api.bitbucket.org/2.0/user
```

## Docs
- https://developer.atlassian.com/cloud/bitbucket/rest/
