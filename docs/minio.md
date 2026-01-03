# MinIO

## Overview
MinIO is an S3-compatible object storage server.

## Python
```python
import boto3

client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="MINIO_ACCESS_KEY",
    aws_secret_access_key="MINIO_SECRET_KEY",
)
print(client.list_buckets())
```

## PowerShell
```powershell
# MinIO is S3-compatible. Use AWS Tools or the mc CLI for management.
mc alias set local http://localhost:9000 MINIO_ACCESS_KEY MINIO_SECRET_KEY
mc ls local
```

## curl
```bash
# Use a presigned URL or an S3-compatible client for authenticated requests.
```

## Docs
- https://min.io/docs/minio/linux/developers/minio-api-reference.html
