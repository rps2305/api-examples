# SMB

## Overview
SMB (Server Message Block) is a network file-sharing protocol used by Windows and Samba. Use SMB libraries to access shares programmatically.

## Python
```python
from smb.SMBConnection import SMBConnection

conn = SMBConnection("username", "password", "client", "server", use_ntlm_v2=True)
conn.connect("server", 445)

files = conn.listPath("share", "/")
for f in files:
    print(f.filename)
```

## PowerShell
```powershell
New-PSDrive -Name Z -PSProvider FileSystem -Root "\\server\share" -Credential (Get-Credential)
Get-ChildItem Z:\
```

## curl
```bash
# curl does not speak SMB. Use smbclient or an SMB library.
```

## Docs
- https://www.samba.org/samba/docs/
- https://pysmb.readthedocs.io/
