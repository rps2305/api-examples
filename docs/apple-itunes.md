# Apple iTunes Search API

## Overview
Apple provides the iTunes Search API for querying media metadata (apps, music, movies, podcasts) without authentication. This is commonly used for catalog lookup and preview metadata.

## Python
```python
import requests

params = {"term": "Daft Punk", "media": "music", "limit": 5}
resp = requests.get("https://itunes.apple.com/search", params=params)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "https://itunes.apple.com/search?term=Daft+Punk&media=music&limit=5"
Invoke-RestMethod -Uri $uri
```

## curl
```bash
curl "https://itunes.apple.com/search?term=Daft+Punk&media=music&limit=5"
```

## Docs
- https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html
