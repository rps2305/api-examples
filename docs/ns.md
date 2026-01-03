# NS APIs

## Overview
NS (Nederlandse Spoorwegen) offers APIs for travel information, disruptions, and stations. Access requires an API key via the NS API portal.

## Python
```python
import requests

headers = {"Ocp-Apim-Subscription-Key": "NS_API_KEY"}
resp = requests.get("https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ "Ocp-Apim-Subscription-Key" = "NS_API_KEY" }
Invoke-RestMethod -Uri "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations" -Headers $headers
```

## curl
```bash
curl -H "Ocp-Apim-Subscription-Key: NS_API_KEY" \
  https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations
```

## Docs
- https://apiportal.ns.nl/
- https://www.ns.nl/reisinformatie/ns-api
