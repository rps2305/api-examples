# Pi-hole

## Overview
Pi-hole is a network-wide DNS sinkhole. It provides an HTTP API (including a token) for stats and adlist management.

## Python
```python
import requests

base_url = "http://pi.hole"
api_token = "PIHOLE_TOKEN"

resp = requests.get(f"{base_url}/admin/api.php", params={"summaryRaw": 1, "auth": api_token})
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "http://pi.hole"
$token = "PIHOLE_TOKEN"
Invoke-RestMethod -Uri "$baseUrl/admin/api.php?summaryRaw=1&auth=$token"
```

## curl
```bash
curl "http://pi.hole/admin/api.php?summaryRaw=1&auth=PIHOLE_TOKEN"
```

## Docs
- https://docs.pi-hole.net/api/
- https://pi-hole.net/
