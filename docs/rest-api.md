# REST API

## Overview
REST APIs use HTTP verbs and JSON payloads to create, read, update, and delete resources. Use Bearer tokens or API keys for authentication, and send `Content-Type: application/json` for JSON bodies.

## Python
```python
import requests

base_url = "https://api.example.com/v1"
headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json",
}

# Create
create_resp = requests.post(
    f"{base_url}/widgets",
    headers=headers,
    json={"name": "Demo widget", "enabled": True},
)
print(create_resp.status_code, create_resp.json())

# Read
list_resp = requests.get(f"{base_url}/widgets", headers=headers)
print(list_resp.status_code, list_resp.json())

# Update
update_resp = requests.patch(
    f"{base_url}/widgets/123",
    headers=headers,
    json={"enabled": False},
)
print(update_resp.status_code, update_resp.json())

# Delete
delete_resp = requests.delete(f"{base_url}/widgets/123", headers=headers)
print(delete_resp.status_code)
```

## PowerShell
```powershell
$baseUrl = "https://api.example.com/v1"
$headers = @{ Authorization = "Bearer TOKEN" }

# Create
Invoke-RestMethod -Uri "$baseUrl/widgets" -Method POST -Headers $headers -ContentType "application/json" -Body '{"name":"Demo widget","enabled":true}'

# Read
Invoke-RestMethod -Uri "$baseUrl/widgets" -Method GET -Headers $headers

# Update
Invoke-RestMethod -Uri "$baseUrl/widgets/123" -Method PATCH -Headers $headers -ContentType "application/json" -Body '{"enabled":false}'

# Delete
Invoke-RestMethod -Uri "$baseUrl/widgets/123" -Method DELETE -Headers $headers
```

## curl
```bash
BASE_URL="https://api.example.com/v1"

# Create
curl -X POST "$BASE_URL/widgets" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo widget","enabled":true}'

# Read
curl -X GET "$BASE_URL/widgets" \
  -H "Authorization: Bearer TOKEN"

# Update
curl -X PATCH "$BASE_URL/widgets/123" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled":false}'

# Delete
curl -X DELETE "$BASE_URL/widgets/123" \
  -H "Authorization: Bearer TOKEN"
```

## Docs
- https://www.rfc-editor.org/rfc/rfc9110
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- https://curl.se/docs/manpage.html
