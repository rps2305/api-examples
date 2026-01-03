# Slack

## Overview
Slack provides a Web API for messaging, channels, and workspace automation.

## Python
```python
import requests

headers = {"Authorization": "Bearer SLACK_BOT_TOKEN"}
resp = requests.get("https://slack.com/api/auth.test", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer SLACK_BOT_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://slack.com/api/auth.test" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer SLACK_BOT_TOKEN" https://slack.com/api/auth.test
```

## Docs
- https://api.slack.com/web
