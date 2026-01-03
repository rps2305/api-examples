# Twilio

## Overview
Twilio provides REST APIs for SMS, voice calls, and messaging channels.

## Python
```python
import requests

account_sid = "TWILIO_ACCOUNT_SID"
auth_token = "TWILIO_AUTH_TOKEN"
resp = requests.get(
    f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json",
    auth=(account_sid, auth_token),
)
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$pair = "TWILIO_ACCOUNT_SID:TWILIO_AUTH_TOKEN"
$encoded = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{ Authorization = "Basic $encoded" }
$uri = "https://api.twilio.com/2010-04-01/Accounts/TWILIO_ACCOUNT_SID.json"
Invoke-RestMethod -Method Get -Uri $uri -Headers $headers
```

## curl
```bash
curl -u TWILIO_ACCOUNT_SID:TWILIO_AUTH_TOKEN \
  https://api.twilio.com/2010-04-01/Accounts/TWILIO_ACCOUNT_SID.json
```

## Docs
- https://www.twilio.com/docs/usage/api
