# MongoDB Atlas Data API

## Overview
MongoDB Atlas Data API provides HTTPS access to collections without a driver.

## Python
```python
import requests

app_id = "APP_ID"
api_key = "MONGODB_DATA_API_KEY"
headers = {"Content-Type": "application/json", "api-key": api_key}

payload = {
    "dataSource": "Cluster0",
    "database": "sample_mflix",
    "collection": "movies",
    "filter": {"title": "The Matrix"},
}

url = f"https://data.mongodb-api.com/app/{app_id}/endpoint/data/v1/action/findOne"
resp = requests.post(url, json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$appId = "APP_ID"
$headers = @{ "Content-Type" = "application/json"; "api-key" = "MONGODB_DATA_API_KEY" }
$body = @{
  dataSource = "Cluster0"
  database = "sample_mflix"
  collection = "movies"
  filter = @{ title = "The Matrix" }
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "https://data.mongodb-api.com/app/$appId/endpoint/data/v1/action/findOne" -Headers $headers -Body $body
```

## curl
```bash
curl -H "Content-Type: application/json" \
  -H "api-key: MONGODB_DATA_API_KEY" \
  -d '{"dataSource":"Cluster0","database":"sample_mflix","collection":"movies","filter":{"title":"The Matrix"}}' \
  https://data.mongodb-api.com/app/APP_ID/endpoint/data/v1/action/findOne
```

## Docs
- https://www.mongodb.com/docs/atlas/api/data-api/
