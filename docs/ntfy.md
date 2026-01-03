# ntfy

## Overview
`ntfy` is a lightweight pub/sub notification service. You publish messages to a topic via HTTP and subscribers receive them via web, mobile, or other clients.

## Python
```python
import requests

base_url = "https://ntfy.sh"  # or your self-hosted instance

topic = "alerts"
message = "Backup completed"

resp = requests.post(f"{base_url}/{topic}", data=message)
resp.raise_for_status()
```

## PowerShell
```powershell
$baseUrl = "https://ntfy.sh"
$topic = "alerts"
$message = "Backup completed"

Invoke-RestMethod -Method Post -Uri "$baseUrl/$topic" -Body $message
```

## curl
```bash
curl -X POST "https://ntfy.sh/alerts" -d "Backup completed"
```

## Docs
- https://docs.ntfy.sh/
- https://github.com/binwiederhier/ntfy
