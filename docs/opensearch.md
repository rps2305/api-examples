# OpenSearch

## Overview
OpenSearch provides a REST API compatible with Elasticsearch for search workloads.

## Python
```python
import requests

resp = requests.get("http://localhost:9200/_cluster/health")
resp.raise_for_status()
print(resp.json())
```

## PowerShell
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:9200/_cluster/health"
```

## curl
```bash
curl http://localhost:9200/_cluster/health
```

## Docs
- https://opensearch.org/docs/latest/api-reference/
