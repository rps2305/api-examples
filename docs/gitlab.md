# GitLab

## Overview
GitLab provides REST APIs for repositories, CI/CD, and project management.

## Python
```python
import requests

headers = {"Authorization": "Bearer GITLAB_TOKEN"}
resp = requests.get("https://gitlab.com/api/v4/user", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer GITLAB_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://gitlab.com/api/v4/user" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer GITLAB_TOKEN" https://gitlab.com/api/v4/user
```

## Docs
- https://docs.gitlab.com/ee/api/
