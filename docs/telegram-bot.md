# Telegram Bot API

## Overview
Telegram exposes a simple HTTPS Bot API for messaging and bot automation.

## Python
```python
import requests

bot_token = "TELEGRAM_BOT_TOKEN"
resp = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$token = "TELEGRAM_BOT_TOKEN"
Invoke-RestMethod -Method Get -Uri "https://api.telegram.org/bot$token/getMe"
```

## curl
```bash
curl "https://api.telegram.org/botTELEGRAM_BOT_TOKEN/getMe"
```

## Docs
- https://core.telegram.org/bots/api
