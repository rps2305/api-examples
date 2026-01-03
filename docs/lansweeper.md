# Lansweeper

## Overview
Lansweeper exposes APIs for accessing asset data, reports, and site information. Access is tied to your Lansweeper Cloud or on-prem installation and requires API credentials.

## Python
```python
import requests

base_url = "https://api.lansweeper.com/api/v2"
headers = {"Authorization": "Bearer LANSWEEPER_API_TOKEN"}

resp = requests.get(f"{base_url}/reports", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer LANSWEEPER_API_TOKEN" }
Invoke-RestMethod -Uri "https://api.lansweeper.com/api/v2/reports" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer LANSWEEPER_API_TOKEN" \
  https://api.lansweeper.com/api/v2/reports
```

## Docs
- https://docs.lansweeper.com/docs/api/working-with-reports
- https://docs.lansweeper.com/docs/api/working-with-sites
