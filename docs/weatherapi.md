# WeatherAPI.com

## Overview
WeatherAPI.com offers current, forecast, and historical weather endpoints.

## Python
```python
import requests

api_key = "WEATHERAPI_KEY"
resp = requests.get(
    "https://api.weatherapi.com/v1/current.json",
    params={"key": api_key, "q": "London"},
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Method Get -Uri "https://api.weatherapi.com/v1/current.json?key=WEATHERAPI_KEY&q=London"
```

## curl
```bash
curl "https://api.weatherapi.com/v1/current.json?key=WEATHERAPI_KEY&q=London"
```

## Docs
- https://www.weatherapi.com/docs/
