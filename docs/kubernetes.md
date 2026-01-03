# Kubernetes API

## Overview
Kubernetes exposes a REST API for cluster resources and workloads.

## Python
```python
import requests

api_server = "https://KUBE_API_SERVER"
token = "KUBE_BEARER_TOKEN"
headers = {"Authorization": f"Bearer {token}"}
resp = requests.get(f"{api_server}/api", headers=headers, verify=False)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$apiServer = "https://KUBE_API_SERVER"
$headers = @{ Authorization = "Bearer KUBE_BEARER_TOKEN" }
Invoke-RestMethod -Method Get -Uri "$apiServer/api" -Headers $headers -SkipCertificateCheck
```

## curl
```bash
curl -k -H "Authorization: Bearer KUBE_BEARER_TOKEN" https://KUBE_API_SERVER/api
```

## Docs
- https://kubernetes.io/docs/reference/using-api/
