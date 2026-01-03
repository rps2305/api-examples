# Gmail

## Overview
Gmail can be accessed via the Gmail API (OAuth 2.0) or via SMTP using an app password. The API is recommended for production integrations.

## Python (Gmail API)
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.send"])
service = build("gmail", "v1", credentials=creds)

raw = base64.urlsafe_b64encode(
    b"To: recipient@example.com\r\nSubject: Gmail API test\r\n\r\nHello from Gmail API"
).decode("utf-8")

service.users().messages().send(userId="me", body={"raw": raw}).execute()
```

## PowerShell (SMTP with app password)
```powershell
$cred = New-Object System.Management.Automation.PSCredential(
  "your@gmail.com",
  (ConvertTo-SecureString "app-password" -AsPlainText -Force)
)
Send-MailMessage -SmtpServer "smtp.gmail.com" -Port 587 -UseSsl -Credential $cred \
  -From "your@gmail.com" -To "recipient@example.com" -Subject "SMTP test" -Body "Hello from Gmail"
```

## curl (SMTP with app password)
```bash
curl --url "smtp://smtp.gmail.com:587" \
  --ssl-reqd \
  --mail-from "your@gmail.com" \
  --mail-rcpt "recipient@example.com" \
  --user "your@gmail.com:app-password" \
  -T <(printf "Subject: Gmail SMTP\n\nHello from Gmail\n")
```

## Docs
- https://developers.google.com/gmail/api
- https://support.google.com/accounts/answer/185833
