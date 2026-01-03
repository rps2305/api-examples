# Signal (signal-cli REST)

## Overview
Signal does not provide an official public HTTP API. Many self-hosted setups expose the community `signal-cli` REST service for automation.

## Python
```python
import requests

base_url = "http://HOST:PORT"
resp = requests.get(f"{base_url}/v1/about")
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$baseUrl = "http://HOST:PORT"
Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/about"
```

## curl
```bash
curl http://HOST:PORT/v1/about
```

## Docs
- https://github.com/AsamK/signal-cli
