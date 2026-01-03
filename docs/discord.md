# Discord

## Overview
Discord provides a REST API and webhooks for bots and integrations. Use a bot token for authenticated API calls.

## Python
```python
import requests

token = "DISCORD_BOT_TOKEN"
channel_id = "1234567890"

resp = requests.post(
    f"https://discord.com/api/v10/channels/{channel_id}/messages",
    headers={"Authorization": f"Bot {token}"},
    json={"content": "Hello from Python"},
)
resp.raise_for_status()
```

## PowerShell
```powershell
$token = "DISCORD_BOT_TOKEN"
$channelId = "1234567890"
$headers = @{ Authorization = "Bot $token" }
$body = @{ content = "Hello from PowerShell" } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://discord.com/api/v10/channels/$channelId/messages" -Headers $headers -Body $body
```

## curl
```bash
curl -X POST "https://discord.com/api/v10/channels/1234567890/messages" \
  -H "Authorization: Bot DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello from curl"}'
```

## Docs
- https://discord.com/developers/docs/intro
- https://discord.com/developers/docs/resources/channel#create-message
