# OpenWeather

## Overview
OpenWeather provides weather data APIs for current conditions and forecasts.

## Python
```python
import requests

api_key = "OPENWEATHER_KEY"
resp = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": "London", "appid": api_key},
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Method Get -Uri "https://api.openweathermap.org/data/2.5/weather?q=London&appid=OPENWEATHER_KEY"
```

## curl
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=OPENWEATHER_KEY"
```

## Docs
- https://openweathermap.org/api
