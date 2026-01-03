# Google Maps API

## Overview
Google Maps Platform provides APIs for geocoding, places, directions, and map tiles. Most endpoints require an API key and project billing setup.

## Python
```python
import requests

params = {
    "address": "1600 Amphitheatre Parkway, Mountain View, CA",
    "key": "GOOGLE_MAPS_API_KEY",
}
resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=GOOGLE_MAPS_API_KEY"
Invoke-RestMethod -Uri $uri
```

## curl
```bash
curl "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=GOOGLE_MAPS_API_KEY"
```

## Docs
- https://developers.google.com/maps
- https://developers.google.com/maps/documentation/geocoding/overview
