# The Movie Database (TMDB)

## Overview
TMDB provides movie, TV, and people metadata with a REST API.

## Python
```python
import requests

api_key = "TMDB_API_KEY"
resp = requests.get("https://api.themoviedb.org/3/movie/550", params={"api_key": api_key})
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Method Get -Uri "https://api.themoviedb.org/3/movie/550?api_key=TMDB_API_KEY"
```

## curl
```bash
curl "https://api.themoviedb.org/3/movie/550?api_key=TMDB_API_KEY"
```

## Docs
- https://developer.themoviedb.org/docs
