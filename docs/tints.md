# Tints Palette API

## Overview
Tints provides a palette API for generating color swatches from encoded palette identifiers.

## Python
```python
import requests

palette_id = "v1:YnJhbmR8MjUyMkZDfDUwMHxwfDB8MHwwfDEwMHxh"
response = requests.get(f"https://www.tints.dev/palette/{palette_id}", timeout=30)
response.raise_for_status()
print(response.text)
```

## PowerShell
```powershell
$paletteId = "v1:YnJhbmR8MjUyMkZDfDUwMHxwfDB8MHwwfDEwMHxh"
Invoke-RestMethod -Method Get -Uri "https://www.tints.dev/palette/$paletteId"
```

## curl
```bash
curl "https://www.tints.dev/palette/v1:YnJhbmR8MjUyMkZDfDUwMHxwfDB8MHwwfDEwMHxh"
```

## Docs
- https://www.tints.dev/palette/v1:YnJhbmR8MjUyMkZDfDUwMHxwfDB8MHwwfDEwMHxh
