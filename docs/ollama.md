# Ollama

## Overview
Ollama provides a local HTTP API for running open models. The default server runs at `http://localhost:11434`.

## Python
```python
import requests

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1", "prompt": "Explain what an API is in one sentence."},
)
resp.raise_for_status()
print(resp.json()["response"])
```

## PowerShell
```powershell
$body = @{ model = "llama3.1"; prompt = "Explain what an API is in one sentence." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $body -ContentType "application/json"
```

## curl
```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.1","prompt":"Explain what an API is in one sentence."}'
```

## Docs
- https://github.com/ollama/ollama
- https://github.com/ollama/ollama/blob/main/docs/api.md
