# Stirling PDF

## Overview
Stirling-PDF is a self-hosted PDF toolkit with a REST API to merge, split, and convert PDFs. Endpoints typically live under `/api/v1`.

## Python
```python
import requests

base_url = "http://localhost:8080/api/v1"

with open("input.pdf", "rb") as f:
    resp = requests.post(
        f"{base_url}/general/merge",
        files={"fileInput": f},
    )
resp.raise_for_status()
with open("merged.pdf", "wb") as out:
    out.write(resp.content)
```

## PowerShell
```powershell
$baseUrl = "http://localhost:8080/api/v1"
Invoke-WebRequest -Uri "$baseUrl/general/merge" -Method Post -InFile "input.pdf" -OutFile "merged.pdf"
```

## curl
```bash
curl -X POST "http://localhost:8080/api/v1/general/merge" \
  -F "fileInput=@input.pdf" \
  -o merged.pdf
```

## Docs
- https://github.com/Stirling-Tools/Stirling-PDF
