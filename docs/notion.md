# Notion

## Overview
Notion offers a REST API to read and write pages, databases, and blocks. Integrations use a bearer token and require explicit sharing of resources.

## Python
```python
import requests

token = "NOTION_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

resp = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json={"page_size": 5},
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{
  Authorization = "Bearer NOTION_TOKEN"
  "Notion-Version" = "2022-06-28"
  "Content-Type" = "application/json"
}
$body = @{ page_size = 5 } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.notion.com/v1/search" -Headers $headers -Body $body
```

## curl
```bash
curl -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size":5}'
```

## Docs
- https://developers.notion.com/reference/intro
- https://developers.notion.com/docs
- https://developers.notion.com/page/examples
