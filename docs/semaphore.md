# Semaphore

## Overview
Ansible Semaphore provides a REST API to manage projects, inventories, and task runs. Authenticate with a bearer token.

## Python
```python
import requests

base_url = "https://semaphore.example.com/api"
headers = {"Authorization": "Bearer SEMAPHORE_TOKEN"}

resp = requests.get(f"{base_url}/user", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer SEMAPHORE_TOKEN" }
Invoke-RestMethod -Uri "https://semaphore.example.com/api/user" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer SEMAPHORE_TOKEN" \
  https://semaphore.example.com/api/user
```

## Docs
- https://github.com/ansible-semaphore/semaphore
- https://github.com/ansible-semaphore/semaphore/blob/develop/api-docs.yml
