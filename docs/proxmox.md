# Proxmox VE

## Overview
Proxmox VE exposes a REST API for managing nodes, VMs, storage, and clusters. Authenticate with a ticket or API token.

## Python
```python
import requests

base_url = "https://proxmox.example.com:8006"
api_token = "root@pam!token=API_TOKEN_SECRET"

headers = {"Authorization": f"PVEAPIToken={api_token}"}
resp = requests.get(f"{base_url}/api2/json/nodes", headers=headers, verify=False)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "https://proxmox.example.com:8006"
$headers = @{ Authorization = "PVEAPIToken=root@pam!token=API_TOKEN_SECRET" }
Invoke-RestMethod -Uri "$baseUrl/api2/json/nodes" -Headers $headers -SkipCertificateCheck
```

## curl
```bash
curl -k -H "Authorization: PVEAPIToken=root@pam!token=API_TOKEN_SECRET" \
  https://proxmox.example.com:8006/api2/json/nodes
```

## Docs
- https://pve.proxmox.com/wiki/Proxmox_VE_API
