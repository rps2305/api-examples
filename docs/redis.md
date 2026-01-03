# Redis

## Overview
Redis is an in-memory data store accessed over TCP using the RESP protocol.

## Python
```python
import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)
client.set("status", "ok")
print(client.get("status"))
```

## PowerShell
```powershell
# Redis is not HTTP-based. Use a Redis client library or redis-cli.
redis-cli -h localhost -p 6379 SET status ok
redis-cli -h localhost -p 6379 GET status
```

## curl
```bash
# Redis is not HTTP-based. Use redis-cli or a Redis client library.
```

## Docs
- https://redis.io/docs/
- https://redis-py.readthedocs.io/
