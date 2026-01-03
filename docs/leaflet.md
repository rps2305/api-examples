# Leaflet

## Overview
Leaflet is a JavaScript mapping library that pairs with map tile providers and GeoJSON data sources. It does not require API keys itself, but tile providers may.

## Python
```python
import json

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [4.895168, 52.370216]},
            "properties": {"name": "Amsterdam"},
        }
    ],
}

print(json.dumps(geojson, indent=2))
```

## PowerShell
```powershell
$geojson = @{
  type = "FeatureCollection"
  features = @(
    @{
      type = "Feature"
      geometry = @{ type = "Point"; coordinates = @(4.895168, 52.370216) }
      properties = @{ name = "Amsterdam" }
    }
  )
}
$geojson | ConvertTo-Json -Depth 5
```

## curl
```bash
curl https://leafletjs.com
```

## Docs
- https://leafletjs.com
