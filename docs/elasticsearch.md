# Elasticsearch

## Overview
Elasticsearch exposes a JSON REST API for search, analytics, and indexing.

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
- https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html
