# Microsoft Graph

## Overview
Microsoft Graph provides a unified REST API for Microsoft 365 services. Authenticate with OAuth 2.0 and call endpoints under `https://graph.microsoft.com/v1.0`.

## App registration credentials
Store Entra ID app registration values in `.env` (or export them in your shell):

```dotenv
AZURE_TENANT_ID=YOUR_TENANT_ID
AZURE_CLIENT_ID=YOUR_CLIENT_ID
AZURE_CLIENT_SECRET=YOUR_CLIENT_SECRET
```

```powershell
$env:AZURE_TENANT_ID = "YOUR_TENANT_ID"
$env:AZURE_CLIENT_ID = "YOUR_CLIENT_ID"
$env:AZURE_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
```

## OAuth 2.0 client credentials (Python)
```python
import os
import requests

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_resp = requests.post(
    token_url,
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    },
)
token_resp.raise_for_status()
access_token = token_resp.json()["access_token"]
```

## OAuth 2.0 client credentials (PowerShell)
```powershell
$tenantId = $env:AZURE_TENANT_ID
$clientId = $env:AZURE_CLIENT_ID
$clientSecret = $env:AZURE_CLIENT_SECRET

$tokenUri = "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token"
$tokenBody = @{
  client_id     = $clientId
  client_secret = $clientSecret
  scope         = "https://graph.microsoft.com/.default"
  grant_type    = "client_credentials"
}
$tokenResp = Invoke-RestMethod -Method Post -Uri $tokenUri -Body $tokenBody
$accessToken = $tokenResp.access_token
```

## Python
```python
import requests

token = "OAUTH_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

resp = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer OAUTH_ACCESS_TOKEN" }
Invoke-RestMethod -Uri "https://graph.microsoft.com/v1.0/me" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer OAUTH_ACCESS_TOKEN" https://graph.microsoft.com/v1.0/me
```

## Pagination, filtering, limits, and sorting
Microsoft Graph uses server-driven paging. When a response includes `@odata.nextLink`, request that URL to fetch the next page.

```python
import requests

headers = {"Authorization": f"Bearer {access_token}"}
url = (
    "https://graph.microsoft.com/v1.0/users"
    "?$select=id,displayName,mail"
    "&$filter=accountEnabled eq true"
    "&$orderby=displayName"
    "&$top=25"
    "&$count=true"
)

items = []
while url:
    resp = requests.get(url, headers={**headers, "ConsistencyLevel": "eventual"})
    resp.raise_for_status()
    data = resp.json()
    items.extend(data.get("value", []))
    url = data.get("@odata.nextLink")

print(f"Fetched {len(items)} users")
```

```powershell
$headers = @{
  Authorization = "Bearer $accessToken"
  ConsistencyLevel = "eventual"
}
$uri = "https://graph.microsoft.com/v1.0/users?`$select=id,displayName,mail&`$filter=accountEnabled eq true&`$orderby=displayName&`$top=25&`$count=true"
$items = @()

while ($uri) {
  $resp = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers
  $items += $resp.value
  $uri = $resp.'@odata.nextLink'
}

"Fetched $($items.Count) users"
```

## Docs
- https://learn.microsoft.com/graph/overview
- https://learn.microsoft.com/graph/auth/
