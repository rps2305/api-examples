# Prometheus

## Overview
Prometheus provides an HTTP API for querying metrics and labels.

## Python
```python
import requests

resp = requests.get("http://localhost:9090/api/v1/query", params={"query": "up"})
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:9090/api/v1/query?query=up"
```

## curl
```bash
curl "http://localhost:9090/api/v1/query?query=up"
```

## Docs
- https://prometheus.io/docs/prometheus/latest/querying/api/
