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

## Python (Vision)
```python
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Describe the image in one sentence."},
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg",
                },
            ],
        }
    ],
)

print(response.output_text)
```

## Python (Text-to-speech)
```python
import requests

headers = {"Authorization": "Bearer OPENAI_API_KEY"}
payload = {
    "model": "gpt-4o-mini-tts",
    "voice": "alloy",
    "input": "Thanks for trying our API examples.",
}

resp = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=payload)
resp.raise_for_status()
with open("speech.mp3", "wb") as f:
    f.write(resp.content)
```

## Python (Tool calling)
```python
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4.1-mini",
    input="What's the weather in Seattle?",
    tools=[
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
    tool_choice="auto",
)

print(response.output)
```

## Structured outputs (JSON schema)
```python
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4.1-mini",
    input="From the text, extract action items with owner and due date: "
    "Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday.",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "action_items",
            "strict": True,
            "schema": {
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
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["items"],
                "additionalProperties": False,
            },
        },
    },
)

print(response.output_text)
```

## PowerShell
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{ model = "gpt-4.1-mini"; input = "Write a short haiku about APIs." } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

## PowerShell (Vision)
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{
  model = "gpt-4.1-mini"
  input = @(
    @{
      role = "user"
      content = @(
        @{ type = "input_text"; text = "Describe the image in one sentence." }
        @{ type = "input_image"; image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg" }
      )
    }
  )
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

## PowerShell (Text-to-speech)
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY" }
$body = @{
  model = "gpt-4o-mini-tts"
  voice = "alloy"
  input = "Thanks for trying our API examples."
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/audio/speech" -Headers $headers -Body $body -ContentType "application/json" -OutFile "speech.mp3"
```

## PowerShell (Tool calling)
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{
  model = "gpt-4.1-mini"
  input = "What's the weather in Seattle?"
  tools = @(
    @{
      type = "function"
      function = @{
        name = "get_weather"
        description = "Get the current weather in a city."
        parameters = @{
          type = "object"
          properties = @{
            city = @{ type = "string" }
          }
          required = @("city")
        }
      }
    }
  )
  tool_choice = "auto"
} | ConvertTo-Json -Depth 8

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

## PowerShell (Structured outputs)
```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{
  model = "gpt-4.1-mini"
  input = "Extract action items: Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday."
  response_format = @{
    type = "json_schema"
    json_schema = @{
      name = "action_items"
      strict = $true
      schema = @{
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
              additionalProperties = $false
            }
          }
        }
        required = @("items")
        additionalProperties = $false
      }
    }
  }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

## curl
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-mini","input":"Write a short haiku about APIs."}'
```

## curl (Vision)
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1-mini",
    "input": [
      {
        "role": "user",
        "content": [
          { "type": "input_text", "text": "Describe the image in one sentence." },
          { "type": "input_image", "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg" }
        ]
      }
    ]
  }'
```

## curl (Text-to-speech)
```bash
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini-tts","voice":"alloy","input":"Thanks for trying our API examples."}' \
  --output speech.mp3
```

## curl (Tool calling)
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1-mini",
    "input": "What'\''s the weather in Seattle?",
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
    ],
    "tool_choice": "auto"
  }'
```

## curl (Structured outputs)
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1-mini",
    "input": "Extract action items: Jon will draft the rollout plan by Friday. Priya will update the FAQ by Monday.",
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "action_items",
        "strict": true,
        "schema": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "owner": { "type": "string" },
                  "task": { "type": "string" },
                  "due_date": { "type": "string" }
                },
                "required": ["owner", "task", "due_date"],
                "additionalProperties": false
              }
            }
          },
          "required": ["items"],
          "additionalProperties": false
        }
      }
    }
  }'
```

## Practical examples
```python
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=(
        "Rewrite this support reply to be concise and friendly:\n"
        "We have received your ticket and will respond in 3-5 business days."
    ),
)

print(response.output_text)
```

```powershell
$headers = @{ Authorization = "Bearer OPENAI_API_KEY"; "Content-Type" = "application/json" }
$body = @{
  model = "gpt-4.1-mini"
  input = "Summarize this incident report in 3 bullet points: The service degraded at 14:02..."
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://api.openai.com/v1/responses" -Headers $headers -Body $body
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-mini","input":"Classify this message as billing, technical, or sales: My card failed on checkout."}'
```

## Docs
- https://platform.openai.com/docs
- https://github.com/openai/openai-python
