# Asana

## Overview
Asana provides a REST API for tasks, projects, and teams.

## Python
```python
import requests

headers = {"Authorization": "Bearer ASANA_TOKEN"}
resp = requests.get("https://app.asana.com/api/1.0/users/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer ASANA_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://app.asana.com/api/1.0/users/me" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer ASANA_TOKEN" https://app.asana.com/api/1.0/users/me
```

## Docs
- https://developers.asana.com/docs
