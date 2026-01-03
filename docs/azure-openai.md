# Azure OpenAI

## Overview
Azure OpenAI exposes OpenAI-compatible models hosted inside Azure subscriptions.

## Python
```python
import requests

resource = "AZURE_RESOURCE"
deployment = "DEPLOYMENT_NAME"
api_key = "AZURE_OPENAI_KEY"
api_version = "2024-02-15-preview"

headers = {"api-key": api_key, "Content-Type": "application/json"}

payload = {
    "messages": [{"role": "user", "content": "Hello from Azure OpenAI"}],
    "max_tokens": 128,
}

url = (
    f"https://{resource}.openai.azure.com/openai/deployments/"
    f"{deployment}/chat/completions?api-version={api_version}"
)
resp = requests.post(url, json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$resource = "AZURE_RESOURCE"
$deployment = "DEPLOYMENT_NAME"
$apiVersion = "2024-02-15-preview"
$headers = @{ "api-key" = "AZURE_OPENAI_KEY"; "Content-Type" = "application/json" }
$body = @{
  messages = @(@{ role = "user"; content = "Hello from Azure OpenAI" })
  max_tokens = 128
} | ConvertTo-Json -Depth 5
$uri = "https://$resource.openai.azure.com/openai/deployments/$deployment/chat/completions?api-version=$apiVersion"
Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body
```

## curl
```bash
curl -H "api-key: AZURE_OPENAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello from Azure OpenAI"}],"max_tokens":128}' \
  "https://AZURE_RESOURCE.openai.azure.com/openai/deployments/DEPLOYMENT_NAME/chat/completions?api-version=2024-02-15-preview"
```

## Docs
- https://learn.microsoft.com/azure/ai-services/openai/
