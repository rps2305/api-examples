# Web-Check

## Overview
Web-Check is a self-hosted uptime/status monitoring dashboard. It aggregates checks for websites and services.

## Python
```python
import requests

base_url = "http://localhost:3000"
resp = requests.get(f"{base_url}/api/health")
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/health"
```

## curl
```bash
curl "http://localhost:3000/api/health"
```

## Docs
- https://github.com/Lissy93/web-check
