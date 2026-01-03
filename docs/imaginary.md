# Imaginary

## Overview
Imaginary is an HTTP image processing service that can resize, crop, and transform images. It exposes a REST API with endpoints like `/resize` and `/crop`.

## Python
```python
import requests

resp = requests.get(
    "http://localhost:9000/resize",
    params={"width": 200, "height": 200},
    data={"url": "https://example.com/image.jpg"},
)
resp.raise_for_status()
with open("thumb.jpg", "wb") as f:
    f.write(resp.content)
```

## PowerShell
```powershell
$body = @{ url = "https://example.com/image.jpg" }
Invoke-WebRequest -Method Get -Uri "http://localhost:9000/resize?width=200&height=200" -Body $body -OutFile "thumb.jpg"
```

## curl
```bash
curl "http://localhost:9000/resize?width=200&height=200" \
  -d "url=https://example.com/image.jpg" \
  -o thumb.jpg
```

## Docs
- https://github.com/h2non/imaginary
