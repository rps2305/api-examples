# Transmission

## Overview
Transmission provides a JSON-RPC API for managing torrents. Authenticate with HTTP basic auth or a session ID.

## Python
```python
import requests

base_url = "http://transmission.example.com:9091/transmission/rpc"

resp = requests.post(base_url, json={"method": "session-get"})
if resp.status_code == 409:
    session_id = resp.headers.get("X-Transmission-Session-Id")
    resp = requests.post(
        base_url,
        headers={"X-Transmission-Session-Id": session_id},
        json={"method": "session-get"},
    )

resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$uri = "http://transmission.example.com:9091/transmission/rpc"
$response = Invoke-WebRequest -Method Post -Uri $uri -Body '{"method":"session-get"}' -ContentType "application/json"
if ($response.StatusCode -eq 409) {
  $sessionId = $response.Headers["X-Transmission-Session-Id"]
  Invoke-RestMethod -Method Post -Uri $uri -Headers @{"X-Transmission-Session-Id"=$sessionId} -Body '{"method":"session-get"}' -ContentType "application/json"
}
```

## curl
```bash
curl -s -X POST "http://transmission.example.com:9091/transmission/rpc" \
  -H "X-Transmission-Session-Id: $(curl -s -D - -o /dev/null http://transmission.example.com:9091/transmission/rpc | awk '/X-Transmission-Session-Id/ {print $2}')" \
  -d '{"method":"session-get"}'
```

## Docs
- https://github.com/transmission/transmission/blob/main/docs/rpc-spec.md
