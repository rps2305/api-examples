# Drupal JSON:API

## Overview
Drupal's JSON:API module exposes content entities over a standardized JSON:API interface. You can query, create, update, and delete content using HTTP requests.

## Python
```python
import requests

base_url = "https://example.com/jsonapi"
resp = requests.get(f"{base_url}/node/article")
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "https://example.com/jsonapi"
Invoke-RestMethod -Method Get -Uri "$baseUrl/node/article"
```

## curl
```bash
curl "https://example.com/jsonapi/node/article"
```

## Docs
- https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module
- https://jsonapi.org/
