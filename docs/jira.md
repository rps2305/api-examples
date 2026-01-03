# Jira Cloud

## Overview
Jira Cloud's REST API supports issues, projects, and workflows with Atlassian auth.

## Python
```python
import base64
import requests

email = "you@example.com"
api_token = "JIRA_API_TOKEN"
auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()
headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}
resp = requests.get("https://your-domain.atlassian.net/rest/api/3/myself", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$email = "you@example.com"
$token = "JIRA_API_TOKEN"
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$email`:$token"))
$headers = @{ Authorization = "Basic $auth"; Accept = "application/json" }
Invoke-RestMethod -Method Get -Uri "https://your-domain.atlassian.net/rest/api/3/myself" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Basic BASE64_EMAIL_TOKEN" \
  -H "Accept: application/json" \
  https://your-domain.atlassian.net/rest/api/3/myself
```

## Docs
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/
