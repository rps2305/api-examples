# OpenAI

## Overview
OpenAI provides APIs for text, vision, and audio models. Use API keys to authenticate and call endpoints over HTTPS.

## Python
```python
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a short haiku about APIs.",
)

print(response.output_text)
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{ model = "gpt-4.1-mini"; input = "Write a short haiku about APIs." } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

## curl
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-mini","input":"Write a short haiku about APIs."}'
```

## Docs
- https://platform.openai.com/docs
- https://github.com/openai/openai-python
