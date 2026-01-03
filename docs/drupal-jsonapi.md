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

## Pagination
```python
import requests

base_url = "https://example.com/jsonapi"
limit = 10
offset = 0
items = []

while True:
    resp = requests.get(
        f"{base_url}/node/article",
        params={"page[limit]": limit, "page[offset]": offset},
    )
    resp.raise_for_status()
    data = resp.json()
    items.extend(data.get("data", []))
    if len(data.get("data", [])) < limit:
        break
    offset += limit

print(f"Fetched {len(items)} articles")
```

## PowerShell
```powershell
$baseUrl = "https://example.com/jsonapi"
Invoke-RestMethod -Method Get -Uri "$baseUrl/node/article"
```

## PowerShell (pagination)
```powershell
$baseUrl = "https://example.com/jsonapi"
$limit = 10
$offset = 0
$items = @()

while ($true) {
  $uri = "$baseUrl/node/article?page[limit]=$limit&page[offset]=$offset"
  $resp = Invoke-RestMethod -Method Get -Uri $uri
  $items += $resp.data
  if ($resp.data.Count -lt $limit) { break }
  $offset += $limit
}

"Fetched $($items.Count) articles"
```

## curl
```bash
curl "https://example.com/jsonapi/node/article"
```

## curl (pagination)
```bash
curl "https://example.com/jsonapi/node/article?page[limit]=10&page[offset]=0"
```

## Docs
- https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module
- https://jsonapi.org/
