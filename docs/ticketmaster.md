# Ticketmaster

## Overview
Ticketmaster provides APIs for events, venues, and attractions, including a Discovery API for public event searches. Access requires an API key.

## Python
```python
import requests

params = {
    "apikey": "TICKETMASTER_API_KEY",
    "keyword": "concert",
    "countryCode": "NL",
}
resp = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=TICKETMASTER_API_KEY&keyword=concert&countryCode=NL"
Invoke-RestMethod -Uri $uri
```

## curl
```bash
curl "https://app.ticketmaster.com/discovery/v2/events.json?apikey=TICKETMASTER_API_KEY&keyword=concert&countryCode=NL"
```

## Docs
- https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
