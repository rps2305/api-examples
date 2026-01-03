# Notion

## Overview
Notion offers a REST API to read and write pages, databases, and blocks. Integrations use a bearer token and require explicit sharing of resources.

## Python
```python
import requests

token = "NOTION_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

resp = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json={"page_size": 5},
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{
  Authorization = "Bearer NOTION_TOKEN"
  "Notion-Version" = "2022-06-28"
  "Content-Type" = "application/json"
}
$body = @{ page_size = 5 } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.notion.com/v1/search" -Headers $headers -Body $body
```

## Adding large text blocks
Notion limits each `rich_text` item to 2000 characters and allows up to 100 blocks per request.
Chunk large text and append it to a page or block in batches.

```python
import math
import requests

token = "NOTION_TOKEN"
parent_block_id = "PARENT_BLOCK_ID"
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def chunk_text(text, size=2000):
    return [text[i : i + size] for i in range(0, len(text), size)]

long_text = "..."  # very large string
chunks = chunk_text(long_text)

blocks = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": chunk}}],
        },
    }
    for chunk in chunks
]

for i in range(0, len(blocks), 100):
    resp = requests.patch(
        f"https://api.notion.com/v1/blocks/{parent_block_id}/children",
        headers=headers,
        json={"children": blocks[i : i + 100]},
    )
    resp.raise_for_status()
```

```powershell
$headers = @{
  Authorization = "Bearer NOTION_TOKEN"
  "Notion-Version" = "2022-06-28"
  "Content-Type" = "application/json"
}
$parentBlockId = "PARENT_BLOCK_ID"
$longText = "..." # very large string

$chunks = @()
for ($i = 0; $i -lt $longText.Length; $i += 2000) {
  $chunks += $longText.Substring($i, [Math]::Min(2000, $longText.Length - $i))
}

$blocks = $chunks | ForEach-Object {
  @{
    object = "block"
    type   = "paragraph"
    paragraph = @{
      rich_text = @(@{
        type = "text"
        text = @{ content = $_ }
      })
    }
  }
}

for ($i = 0; $i -lt $blocks.Count; $i += 100) {
  $batch = $blocks[$i..([Math]::Min($i + 99, $blocks.Count - 1))]
  $body = @{ children = $batch } | ConvertTo-Json -Depth 6
  Invoke-RestMethod -Method Patch -Uri "https://api.notion.com/v1/blocks/$parentBlockId/children" -Headers $headers -Body $body
}
```

## Pagination
```python
import requests

token = "NOTION_TOKEN"
database_id = "DATABASE_ID"
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

has_more = True
start_cursor = None
items = []

while has_more:
    payload = {"page_size": 50}
    if start_cursor:
        payload["start_cursor"] = start_cursor
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=headers,
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    items.extend(data["results"])
    has_more = data["has_more"]
    start_cursor = data.get("next_cursor")

print(f"Fetched {len(items)} records")
```

## curl
```bash
curl -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size":5}'
```

## Docs
- https://developers.notion.com/reference/intro
- https://developers.notion.com/docs
- https://developers.notion.com/page/examples
