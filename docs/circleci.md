# CircleCI

## Overview
CircleCI provides a REST API for pipelines, jobs, and user identity.

## Python
```python
import requests

headers = {"Circle-Token": "CIRCLECI_TOKEN"}
resp = requests.get("https://circleci.com/api/v2/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ "Circle-Token" = "CIRCLECI_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://circleci.com/api/v2/me" -Headers $headers
```

## curl
```bash
curl -H "Circle-Token: CIRCLECI_TOKEN" https://circleci.com/api/v2/me
```

## Docs
- https://circleci.com/docs/api/v2/
