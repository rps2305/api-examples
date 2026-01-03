# Jenkins

## Overview
Jenkins exposes a JSON API for jobs, builds, and queue management.

## Python
```python
import requests

user = "JENKINS_USER"
api_token = "JENKINS_API_TOKEN"
resp = requests.get("http://localhost:8080/api/json", auth=(user, api_token))
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
$pair = "JENKINS_USER:JENKINS_API_TOKEN"
$encoded = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{ Authorization = "Basic $encoded" }
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/api/json" -Headers $headers
```

## curl
```bash
curl -u JENKINS_USER:JENKINS_API_TOKEN http://localhost:8080/api/json
```

## Docs
- https://www.jenkins.io/doc/book/using/remote-access-api/
