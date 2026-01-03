# OpenStreetMap (Nominatim)

## Overview
OpenStreetMap provides open map data. The Nominatim service offers geocoding and reverse geocoding endpoints for searching addresses and coordinates.

## Python
```python
import requests

params = {
    "q": "Dam Square, Amsterdam",
    "format": "json",
}
resp = requests.get("https://nominatim.openstreetmap.org/search", params=params)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://nominatim.openstreetmap.org/search?q=Dam+Square,+Amsterdam&format=json"
Invoke-RestMethod -Uri $uri
```

## curl
```bash
curl "https://nominatim.openstreetmap.org/search?q=Dam+Square,+Amsterdam&format=json"
```

## Docs
- https://www.openstreetmap.org
- https://nominatim.org/release-docs/latest/api/Overview/
