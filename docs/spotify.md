# Spotify

## Overview
Spotify's Web API provides access to users, playlists, and playback data.

## Python
```python
import requests

headers = {"Authorization": "Bearer SPOTIFY_ACCESS_TOKEN"}
resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer SPOTIFY_ACCESS_TOKEN" }
Invoke-RestMethod -Method Get -Uri "https://api.spotify.com/v1/me" -Headers $headers
```

## curl
```bash
curl -H "Authorization: Bearer SPOTIFY_ACCESS_TOKEN" https://api.spotify.com/v1/me
```

## Docs
- https://developer.spotify.com/documentation/web-api
