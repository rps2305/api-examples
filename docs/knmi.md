# KNMI

## Overview
The KNMI provides weather and climate datasets accessible via scripts and APIs. Access methods vary by dataset and typically use HTTP downloads or APIs with authentication keys.

## Python
```python
import requests

url = "https://api.dataplatform.knmi.nl/open-data/v1/datasets"
headers = {"Authorization": "Bearer KNMI_TOKEN"}

resp = requests.get(url, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer KNMI_TOKEN" }
Invoke-RestMethod -Uri "https://api.dataplatform.knmi.nl/open-data/v1/datasets" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer KNMI_TOKEN" \
  https://api.dataplatform.knmi.nl/open-data/v1/datasets
```

## Docs
- https://www.knmi.nl/kennis-en-datacentrum/achtergrond/data-ophalen-vanuit-een-script
- https://developer.dataplatform.knmi.nl/
