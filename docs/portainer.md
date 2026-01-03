# Portainer

## Overview
Portainer exposes a REST API for managing Docker environments, stacks, and users. Authenticate using JWT obtained from `/auth`.

## Python
```python
import requests

base_url = "https://portainer.example.com/api"

auth_resp = requests.post(
    f"{base_url}/auth",
    json={"Username": "admin", "Password": "password"},
    verify=False,
)
auth_resp.raise_for_status()

jwt = auth_resp.json()["jwt"]
headers = {"Authorization": f"Bearer {jwt}"}

resp = requests.get(f"{base_url}/endpoints", headers=headers, verify=False)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "https://portainer.example.com/api"
$authBody = @{ Username = "admin"; Password = "password" } | ConvertTo-Json
$auth = Invoke-RestMethod -Method Post -Uri "$baseUrl/auth" -Body $authBody -ContentType "application/json" -SkipCertificateCheck
$headers = @{ Authorization = "Bearer $($auth.jwt)" }
Invoke-RestMethod -Uri "$baseUrl/endpoints" -Headers $headers -SkipCertificateCheck
```

## curl
```bash
token=$(curl -sk -X POST https://portainer.example.com/api/auth \
  -H "Content-Type: application/json" \
  -d '{"Username":"admin","Password":"password"}' | jq -r .jwt)

curl -sk -H "Authorization: Bearer $token" https://portainer.example.com/api/endpoints
```

## Docs
- https://documentation.portainer.io/api/docs/
