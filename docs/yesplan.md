# Yesplan Integrations

## Overview
Yesplan provides integration endpoints for event management workflows. Available endpoints and base URLs depend on your Yesplan account and tenant configuration.

## Python
```python
import requests

base_url = "https://yesplan.be/en/integrations"
headers = {"Authorization": "Bearer YESPLAN_TOKEN"}

resp = requests.get(f"{base_url}/api", headers=headers)
resp.raise_for_status()
print(resp.text)
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer YESPLAN_TOKEN" }
Invoke-RestMethod -Uri "https://yesplan.be/en/integrations/api" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer YESPLAN_TOKEN" \
  https://yesplan.be/en/integrations/api
```

## Docs
- https://yesplan.be/en/integrations
