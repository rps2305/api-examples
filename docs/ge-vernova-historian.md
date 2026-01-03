# GE Vernova Historian

## Overview
GE Vernova Historian provides APIs for querying and managing time-series data in the Historian platform. Deployments typically expose REST endpoints for data queries and administration, authenticated via credentials or tokens.

## Python
```python
import requests

base_url = "https://HISTORIAN_HOST"
username = "USERNAME"
password = "PASSWORD"

params = {
    "tagname": "TAG_NAME",
    "start": "*-1h",
    "end": "*",
}

response = requests.get(
    f"{base_url}/api/historian/values",
    params=params,
    auth=(username, password),
    timeout=60,
)
response.raise_for_status()
print(response.json())
```

## PowerShell
```powershell
$uri = "https://HISTORIAN_HOST/api/historian/values?tagname=TAG_NAME&start=*-1h&end=*"
Invoke-RestMethod -Method Get -Uri $uri -Credential (Get-Credential)
```

## curl
```bash
curl -u "USERNAME:PASSWORD" "https://HISTORIAN_HOST/api/historian/values?tagname=TAG_NAME&start=*-1h&end=*"
```

## Docs
- https://www.gevernova.com/software/documentation/historian/version81/c_historian_apis_overview.html
