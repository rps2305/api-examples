# Mapbox

## Overview
Mapbox offers geocoding, directions, and map tile APIs.

## Python
```python
import requests

access_token = "MAPBOX_ACCESS_TOKEN"
query = "Seattle"
url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
resp = requests.get(url, params={"access_token": access_token})
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$token = "MAPBOX_ACCESS_TOKEN"
Invoke-RestMethod -Method Get -Uri "https://api.mapbox.com/geocoding/v5/mapbox.places/Seattle.json?access_token=$token"
```

## curl
```bash
curl "https://api.mapbox.com/geocoding/v5/mapbox.places/Seattle.json?access_token=MAPBOX_ACCESS_TOKEN"
```

## Docs
- https://docs.mapbox.com/api/
