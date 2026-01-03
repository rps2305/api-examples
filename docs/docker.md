# Docker Engine API

## Overview
Docker exposes a REST API for container management. You can access it over a TCP socket or a Unix socket. The Docker SDKs wrap this API.

## Python
```python
import docker

client = docker.from_env()
for container in client.containers.list():
    print(container.name)
```

## PowerShell
```powershell
$socket = "http://localhost:2375"
Invoke-RestMethod -Method Get -Uri "$socket/containers/json"
```

## curl
```bash
curl --unix-socket /var/run/docker.sock http://localhost/containers/json
```

## Docs
- https://docs.docker.com/engine/api/
- https://github.com/docker/docker-py
