# Open-Meteo

## Overview
Open-Meteo provides free weather forecast and historical weather APIs. No API key or sign-up is required, making it the simplest choice for weather data. Daily, hourly and current conditions are available per location.

## Python
```python
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.2658,
    "longitude": 6.7931,
    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
    "timezone": "Europe/Amsterdam",
    "forecast_days": 7,
}

resp = requests.get(url, params=params)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://api.open-meteo.com/v1/forecast?latitude=52.2658&longitude=6.7931&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FAmsterdam&forecast_days=7"
Invoke-RestMethod -Method Get -Uri $uri
```

## curl
```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=52.2658&longitude=6.7931&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FAmsterdam&forecast_days=7"
```

## Notes
- Free for non-commercial and low-volume use; check the terms and fair-use policy.
- `weather_code` is a WMO code (0 = clear, 3 = overcast, 61+ = rain, 95+ = thunderstorm).
- Historical data and air-quality/geocoding endpoints are also available.

## Docs
- https://open-meteo.com/
- https://open-meteo.com/en/docs