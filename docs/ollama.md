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

## Python (Vision)
```python
import base64
import requests

with open("image.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.2-vision",
        "messages": [
            {
                "role": "user",
                "content": "Describe the image in one sentence.",
                "images": [image_b64],
            }
        ],
    },
)
resp.raise_for_status()
print(resp.json()["message"]["content"])
```

## Python (Text-to-speech, model-dependent)
```python
import base64
import requests

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "bark", "prompt": "Thanks for trying our API examples.", "stream": False},
)
resp.raise_for_status()

audio_b64 = resp.json()["response"]
with open("speech.wav", "wb") as f:
    f.write(base64.b64decode(audio_b64))
```

## Python (Tool calling)
```python
import requests

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1",
        "messages": [{"role": "user", "content": "What's the weather in Seattle?"}],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather in a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
            }
        ],
    },
)
resp.raise_for_status()
print(resp.json()["message"])
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

## PowerShell (Vision)
```powershell
$imageBytes = [System.IO.File]::ReadAllBytes("image.jpg")
$imageB64 = [Convert]::ToBase64String($imageBytes)
$body = @{
  model = "llama3.2-vision"
  messages = @(
    @{
      role = "user"
      content = "Describe the image in one sentence."
      images = @($imageB64)
    }
  )
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/chat" -Body $body -ContentType "application/json"
```

## PowerShell (Text-to-speech, model-dependent)
```powershell
$body = @{
  model = "bark"
  prompt = "Thanks for trying our API examples."
  stream = $false
} | ConvertTo-Json

$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $body -ContentType "application/json"
[System.IO.File]::WriteAllBytes("speech.wav", [Convert]::FromBase64String($resp.response))
```

## PowerShell (Tool calling)
```powershell
$body = @{
  model = "llama3.1"
  messages = @(
    @{ role = "user"; content = "What's the weather in Seattle?" }
  )
  tools = @(
    @{
      type = "function"
      function = @{
        name = "get_weather"
        description = "Get the current weather in a city."
        parameters = @{
          type = "object"
          properties = @{ city = @{ type = "string" } }
          required = @("city")
        }
      }
    }
  )
} | ConvertTo-Json -Depth 8

Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/chat" -Body $body -ContentType "application/json"
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

## curl (Vision)
```bash
IMAGE_B64=$(base64 < image.jpg)

curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"llama3.2-vision\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"Describe the image in one sentence.\",
        \"images\": [\"$IMAGE_B64\"]
      }
    ]
  }"
```

## curl (Text-to-speech, model-dependent)
```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"bark","prompt":"Thanks for trying our API examples.","stream":false}' \
  | jq -r '.response' | base64 --decode > speech.wav
```

## curl (Tool calling)
```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "What'\''s the weather in Seattle?" }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the current weather in a city.",
          "parameters": {
            "type": "object",
            "properties": { "city": { "type": "string" } },
            "required": ["city"]
          }
        }
      }
    ]
  }'
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
