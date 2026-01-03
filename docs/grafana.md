# Grafana

## Overview
Grafana's HTTP API manages dashboards, users, and data sources.

## Python
```python
import requests

headers = {"Authorization": "Bearer GRAFANA_API_KEY"}
resp = requests.get("http://localhost:3000/api/health", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer GRAFANA_API_KEY" }
Invoke-RestMethod -Method Get -Uri "http://localhost:3000/api/health" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer GRAFANA_API_KEY" http://localhost:3000/api/health
```

## Docs
- https://grafana.com/docs/grafana/latest/developers/http_api/
