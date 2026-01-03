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

## Structured outputs (JSON schema)
```python
import requests

schema = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "task": {"type": "string"},
                    "due_date": {"type": "string"},
                },
                "required": ["owner", "task", "due_date"],
            },
        }
    },
    "required": ["items"],
}

prompt = (
    "Return JSON only that matches this schema:\n"
    f"{schema}\n"
    "Text: Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday."
)

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1", "prompt": prompt, "format": "json"},
)
resp.raise_for_status()
print(resp.json()["response"])
```

## PowerShell
```powershell
$body = @{ model = "llama3.1"; prompt = "Explain what an API is in one sentence." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $body -ContentType "application/json"
```

## PowerShell (Structured outputs)
```powershell
$schema = @{
  type = "object"
  properties = @{
    items = @{
      type = "array"
      items = @{
        type = "object"
        properties = @{
          owner = @{ type = "string" }
          task = @{ type = "string" }
          due_date = @{ type = "string" }
        }
        required = @("owner", "task", "due_date")
      }
    }
  }
  required = @("items")
} | ConvertTo-Json -Depth 10

$prompt = @"
Return JSON only that matches this schema:
$schema
Text: Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday.
"@

$body = @{ model = "llama3.1"; prompt = $prompt; format = "json" } | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $body -ContentType "application/json"
```

## curl
```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.1","prompt":"Explain what an API is in one sentence."}'
```

## curl (Structured outputs)
```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "format": "json",
    "prompt": "Return JSON only that matches this schema: {\"type\":\"object\",\"properties\":{\"items\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"owner\":{\"type\":\"string\"},\"task\":{\"type\":\"string\"},\"due_date\":{\"type\":\"string\"}},\"required\":[\"owner\",\"task\",\"due_date\"]}}},\"required\":[\"items\"]}. Text: Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday."
  }'
```

## Practical examples
```python
import requests

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": "Summarize this incident in 3 bullets: The API latency spiked at 14:02...",
    },
)
resp.raise_for_status()
print(resp.json()["response"])
```

```powershell
$body = @{
  model = "llama3.1"
  prompt = "Rewrite this support reply to be concise and friendly: We have received your ticket and will respond in 3-5 business days."
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $body -ContentType "application/json"
```

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.1","prompt":"Classify this message as billing, technical, or sales: My card failed on checkout."}'
```

## Docs
- https://github.com/ollama/ollama
- https://github.com/ollama/ollama/blob/main/docs/api.md
