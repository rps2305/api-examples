# BFL

## Overview
BFL (Black Forest Labs) provides model APIs for generating media and other AI outputs. Authenticate with an API key and call the HTTPS endpoints defined in the BFL docs.

## Python
```python
import requests

api_key = "BFL_API_KEY"
base_url = "https://api.bfl.ai"

payload = {
    "prompt": "A futuristic cityscape at sunset.",
}

response = requests.post(
    f"{base_url}/v1/ENDPOINT",
    headers={"Authorization": f"Bearer {api_key}"},
    json=payload,
    timeout=60,
)
response.raise_for_status()
print(response.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer BFL_API_KEY"; "Content-Type" = "application/json" }
$body = @{ prompt = "A futuristic cityscape at sunset." } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.bfl.ai/v1/ENDPOINT" -Headers $headers -Body $body
```

## curl
```bash
curl https://api.bfl.ai/v1/ENDPOINT \
  -H "Authorization: Bearer BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A futuristic cityscape at sunset."}'
```

## Docs
- https://docs.bfl.ai/quick_start/introduction
