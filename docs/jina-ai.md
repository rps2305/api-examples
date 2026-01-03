# Jina AI Reader (r.jina.ai)

## Overview
Jina AI provides a lightweight reader endpoint that fetches and cleans web pages for easier consumption. Prefix any URL with `https://r.jina.ai/http://` or `https://r.jina.ai/https://` to retrieve a readable text response.

## Python
```python
import requests

url = "https://r.jina.ai/https://example.com"
resp = requests.get(url)
resp.raise_for_status()
print(resp.text)
```

## PowerShell
```powershell
Invoke-RestMethod -Uri "https://r.jina.ai/https://example.com"
```

## curl
```bash
curl https://r.jina.ai/https://example.com
```

## Docs
- https://r.jina.ai
