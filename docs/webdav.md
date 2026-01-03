# WebDAV

## Overview
WebDAV extends HTTP to allow remote file management (PROPFIND, PUT, MOVE, DELETE). Many servers support Basic or Digest auth over HTTPS.

## Python
```python
import requests
from requests.auth import HTTPBasicAuth

base_url = "https://webdav.example.com/remote.php/dav/files/USER"

response = requests.request(
    "PROPFIND",
    f"{base_url}/",
    auth=HTTPBasicAuth("USER", "PASSWORD"),
    headers={"Depth": "1"},
)
print(response.status_code)
print(response.text)

with open("upload.txt", "rb") as handle:
    put_resp = requests.put(
        f"{base_url}/upload.txt",
        data=handle,
        auth=HTTPBasicAuth("USER", "PASSWORD"),
    )
print(put_resp.status_code)
```

## PowerShell
```powershell
$baseUrl = "https://webdav.example.com/remote.php/dav/files/USER"
$credential = Get-Credential

Invoke-WebRequest -Uri "$baseUrl/" -Method PROPFIND -Headers @{ Depth = "1" } -Credential $credential

Invoke-WebRequest -Uri "$baseUrl/upload.txt" -Method PUT -InFile "./upload.txt" -Credential $credential
```

## curl
```bash
# List directory contents
curl -u "USER:PASSWORD" \
  -X PROPFIND \
  -H "Depth: 1" \
  "https://webdav.example.com/remote.php/dav/files/USER/"

# Upload a file
curl -u "USER:PASSWORD" \
  -T ./upload.txt \
  "https://webdav.example.com/remote.php/dav/files/USER/upload.txt"
```

## Docs
- https://www.rfc-editor.org/rfc/rfc4918
- https://curl.se/docs/manpage.html
- https://docs.python-requests.org/
