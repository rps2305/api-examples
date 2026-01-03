# Hugging Face Inference API

## Overview
Hugging Face hosts thousands of models and provides a unified Inference API for text, vision, and audio tasks.

## Python
```python
import requests

token = "HF_API_TOKEN"
model = "distilbert-base-uncased-finetuned-sst-2-english"
headers = {"Authorization": f"Bearer {token}"}

payload = {"inputs": "Hugging Face APIs are handy."}
resp = requests.post(
    f"https://api-inference.huggingface.co/models/{model}",
    json=payload,
    headers=headers,
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer HF_API_TOKEN" }
$body = @{ inputs = "Hugging Face APIs are handy." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english" -Headers $headers -Body $body
```

## curl
```bash
curl -H "Authorization: Bearer HF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs":"Hugging Face APIs are handy."}' \
  https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english
```

## Docs
- https://huggingface.co/docs/api-inference
