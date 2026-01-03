# SFTP

## Overview
SFTP (SSH File Transfer Protocol) provides file transfers over SSH. Most clients authenticate with username/password or SSH keys.

## Python
```python
import paramiko

transport = paramiko.Transport(("sftp.example.com", 22))
transport.connect(username="USER", password="PASSWORD")

sftp = paramiko.SFTPClient.from_transport(transport)
for entry in sftp.listdir_attr("/remote/path"):
    print(entry.filename)

sftp.get("/remote/path/report.csv", "./report.csv")
sftp.put("./upload.csv", "/remote/path/upload.csv")

sftp.close()
transport.close()
```

## PowerShell
```powershell
# Uses OpenSSH client (Windows 10+/macOS/Linux)
sftp USER@sftp.example.com <<'SFTP'
ls /remote/path
get /remote/path/report.csv
put ./upload.csv /remote/path/upload.csv
bye
SFTP
```

## curl
```bash
# List a directory
curl --user "USER:PASSWORD" "sftp://sftp.example.com/remote/path/"

# Download a file
curl --user "USER:PASSWORD" \
  --output report.csv \
  "sftp://sftp.example.com/remote/path/report.csv"

# Upload a file
curl --user "USER:PASSWORD" \
  -T ./upload.csv \
  "sftp://sftp.example.com/remote/path/upload.csv"
```

## Docs
- https://man.openbsd.org/sftp
- https://docs.paramiko.org/
- https://curl.se/docs/manpage.html
