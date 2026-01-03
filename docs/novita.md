# Novita AI

## Overview
Novita AI provides hosted model inference with OpenAI-compatible APIs for chat and embeddings.

## Python
```python
import requests

api_key = "API_KEY"
base_url = "https://api.novita.ai/v1"

payload = {
    "model": "meta-llama/llama-3.1-8b-instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the latest deployment status."},
    ],
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

resp = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$apiKey = "API_KEY"
$baseUrl = "https://api.novita.ai/v1"

$payload = @{
  model = "meta-llama/llama-3.1-8b-instruct"
  messages = @(
    @{ role = "system"; content = "You are a helpful assistant." },
    @{ role = "user"; content = "Summarize the latest deployment status." }
  )
} | ConvertTo-Json -Depth 6

$headers = @{
  Authorization = "Bearer $apiKey"
  "Content-Type" = "application/json"
}

Invoke-RestMethod -Method Post -Uri "$baseUrl/chat/completions" -Headers $headers -Body $payload
```

## curl
```bash
curl -X POST "https://api.novita.ai/v1/chat/completions" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/llama-3.1-8b-instruct",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Summarize the latest deployment status."}
    ]
  }'
```

## Docs
- https://novita.ai/
- https://novita.ai/docs
