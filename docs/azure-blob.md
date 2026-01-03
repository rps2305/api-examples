# Azure Blob Storage

## Overview
Azure Blob Storage offers REST endpoints for containers and blobs.

## Python
```python
import requests

account = "ACCOUNT_NAME"
container = "CONTAINER"
sas_token = "SAS_TOKEN"
url = f"https://{account}.blob.core.windows.net/{container}?restype=container&comp=list&{sas_token}"
resp = requests.get(url)
resp.raise_for_status()
print(resp.text)
```

## PowerShell
```powershell
$account = "ACCOUNT_NAME"
$container = "CONTAINER"
$sas = "SAS_TOKEN"
$uri = "https://$account.blob.core.windows.net/$container?restype=container&comp=list&$sas"
Invoke-RestMethod -Method Get -Uri $uri
```

## curl
```bash
curl "https://ACCOUNT_NAME.blob.core.windows.net/CONTAINER?restype=container&comp=list&SAS_TOKEN"
```

## Docs
- https://learn.microsoft.com/rest/api/storageservices/
