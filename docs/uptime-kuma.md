# Uptime Kuma

## Overview
Uptime Kuma is a self-hosted monitoring service. It exposes a REST-like API via its WebSocket API and HTTP endpoints for status pages and metrics.

## Python (status page JSON)
```python
import requests

status_url = "https://status.example.com/api/status-page/my-page"
resp = requests.get(status_url)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Uri "https://status.example.com/api/status-page/my-page"
```

## curl
```bash
curl "https://status.example.com/api/status-page/my-page"
```

## Docs
- https://github.com/louislam/uptime-kuma
