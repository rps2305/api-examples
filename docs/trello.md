# Trello

## Overview
Trello's REST API allows you to work with boards, cards, and lists.

## Python
```python
import requests

key = "TRELLO_KEY"
token = "TRELLO_TOKEN"
resp = requests.get(
    "https://api.trello.com/1/members/me",
    params={"key": key, "token": token},
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://api.trello.com/1/members/me?key=TRELLO_KEY&token=TRELLO_TOKEN"
Invoke-RestMethod -Method Get -Uri $uri
```

## curl
```bash
curl "https://api.trello.com/1/members/me?key=TRELLO_KEY&token=TRELLO_TOKEN"
```

## Docs
- https://developer.atlassian.com/cloud/trello/rest/
