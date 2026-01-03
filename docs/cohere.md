# Cohere

## Overview
Cohere offers text generation, embeddings, and RAG-friendly APIs for production use.

## Python
```python
import requests

api_key = "COHERE_API_KEY"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

payload = {"model": "command", "message": "Summarize this sentence."}
resp = requests.post("https://api.cohere.ai/v1/chat", json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer COHERE_API_KEY"; "Content-Type" = "application/json" }
$body = @{ model = "command"; message = "Summarize this sentence." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://api.cohere.ai/v1/chat" -Headers $headers -Body $body
```

## curl
```bash
curl -H "Authorization: Bearer COHERE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"command","message":"Summarize this sentence."}' \
  https://api.cohere.ai/v1/chat
```

## Docs
- https://docs.cohere.com/
