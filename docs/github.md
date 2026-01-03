# GitHub

## Overview
GitHub exposes a REST API and GraphQL API for repository, issue, and workflow automation. Authenticate with a personal access token or GitHub App.

## Python
```python
import requests

token = "GITHUB_TOKEN"
headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

resp = requests.get("https://api.github.com/user", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer GITHUB_TOKEN"; Accept = "application/vnd.github+json" }
Invoke-RestMethod -Method Get -Uri "https://api.github.com/user" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user
```

## Docs
- https://docs.github.com/en/rest
- https://docs.github.com/en/graphql
