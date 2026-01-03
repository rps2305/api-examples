# HashiCorp Vault

## Overview
Vault exposes a REST API for secrets, authentication, and system status.

## Python
```python
import requests

headers = {"X-Vault-Token": "VAULT_TOKEN"}
resp = requests.get("http://localhost:8200/v1/sys/health", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ "X-Vault-Token" = "VAULT_TOKEN" }
Invoke-RestMethod -Method Get -Uri "http://localhost:8200/v1/sys/health" -Headers $headers
```

## curl
```bash
curl -H "X-Vault-Token: VAULT_TOKEN" http://localhost:8200/v1/sys/health
```

## Docs
- https://developer.hashicorp.com/vault/api-docs
