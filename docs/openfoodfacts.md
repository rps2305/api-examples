# Open Food Facts Data

## Overview
Open Food Facts provides open datasets and APIs for food product data. You can download bulk data files or query individual product records by barcode.

## Python
```python
import requests

barcode = "737628064502"
url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

resp = requests.get(url)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$barcode = "737628064502"
Invoke-RestMethod -Uri "https://world.openfoodfacts.org/api/v0/product/$barcode.json"
```

## curl
```bash
curl https://world.openfoodfacts.org/api/v0/product/737628064502.json
```

## Docs
- https://world.openfoodfacts.org/data
- https://world.openfoodfacts.org/data/api
