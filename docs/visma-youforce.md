# Visma Youforce

## Overview
Visma Youforce provides HR and payroll-related APIs for integrating with Youforce tenant data. Authentication and available endpoints depend on your tenant configuration.

## Python
```python
import requests

base_url = "YOUFORCE_BASE_URL"
access_token = "YOUFORCE_ACCESS_TOKEN"

response = requests.get(
    f"{base_url}/",  # replace with a documented endpoint
    headers={"Authorization": f"Bearer {access_token}"},
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

## PowerShell
```powershell
$baseUrl = "YOUFORCE_BASE_URL"
$headers = @{ Authorization = "Bearer YOUFORCE_ACCESS_TOKEN" }

Invoke-RestMethod -Method Get -Uri "$baseUrl/" -Headers $headers
```

## curl
```bash
curl "$YOUFORCE_BASE_URL/" \
  -H "Authorization: Bearer YOUFORCE_ACCESS_TOKEN"
```

## Docs
- https://developer.visma.com/api/youforce
