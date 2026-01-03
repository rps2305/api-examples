# Amazon S3

## Overview
Amazon S3 is object storage with an HTTP API and SDKs like boto3.

## Python
```python
import boto3

client = boto3.client(
    "s3",
    aws_access_key_id="AWS_ACCESS_KEY_ID",
    aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
    region_name="us-east-1",
)
response = client.list_buckets()
print(response.get("Buckets", []))
```

## PowerShell
```powershell
# Requires AWS Tools for PowerShell
Get-S3Bucket -AccessKey "AWS_ACCESS_KEY_ID" -SecretKey "AWS_SECRET_ACCESS_KEY" -Region "us-east-1"
```

## curl
```bash
# Use a presigned URL for simple curl access
curl "https://YOUR_BUCKET.s3.amazonaws.com/OBJECT_KEY?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=..."
```

## Docs
- https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
