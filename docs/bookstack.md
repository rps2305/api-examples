# BookStack

## Overview
BookStack is a self-hosted wiki and knowledge base. Its REST API lets you list and manage books, chapters, pages, and shelves.

## Python
```python
import requests

base_url = "https://demo.bookstackapp.com"
api_token = "TOKEN_ID:TOKEN_SECRET"

headers = {
    "Authorization": f"Token {api_token}",
    "Accept": "application/json",
}

resp = requests.get(f"{base_url}/api/books", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "https://demo.bookstackapp.com"
$apiToken = "TOKEN_ID:TOKEN_SECRET"

$headers = @{
  Authorization = "Token $apiToken"
  Accept = "application/json"
}

Invoke-RestMethod -Method Get -Uri "$baseUrl/api/books" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Token TOKEN_ID:TOKEN_SECRET" \
  -H "Accept: application/json" \
  "https://demo.bookstackapp.com/api/books"
```

## Docs
- https://demo.bookstackapp.com/api/docs
- https://www.bookstackapp.com/docs/admin/api/
