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
