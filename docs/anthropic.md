# Anthropic

## Overview
Anthropic provides Claude model APIs for chat and tool-augmented generation via a REST interface.

## Python
```python
import requests

api_key = "ANTHROPIC_API_KEY"
headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

payload = {
    "model": "claude-3-5-sonnet-20240620",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello from the API"}],
}

resp = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{
  "x-api-key" = "ANTHROPIC_API_KEY"
  "anthropic-version" = "2023-06-01"
  "content-type" = "application/json"
}
$body = @{
  model = "claude-3-5-sonnet-20240620"
  max_tokens = 256
  messages = @(@{ role = "user"; content = "Hello from the API" })
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "https://api.anthropic.com/v1/messages" -Headers $headers -Body $body
```

## curl
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20240620","max_tokens":256,"messages":[{"role":"user","content":"Hello from the API"}]}'
```

## Docs
- https://docs.anthropic.com/claude/docs
