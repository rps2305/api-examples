# SMTP

## Overview
SMTP (Simple Mail Transfer Protocol) is the standard protocol for sending email. Most languages provide libraries to connect to an SMTP server with authentication and TLS.

## Python
```python
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "sender@example.com"
msg["To"] = "recipient@example.com"
msg["Subject"] = "SMTP test"
msg.set_content("Hello from SMTP")

with smtplib.SMTP("smtp.example.com", 587) as server:
    server.starttls()
    server.login("smtp-user", "smtp-password")
    server.send_message(msg)
```

## PowerShell
```powershell
Send-MailMessage \
  -SmtpServer "smtp.example.com" \
  -Port 587 \
  -UseSsl \
  -Credential (Get-Credential) \
  -From "sender@example.com" \
  -To "recipient@example.com" \
  -Subject "SMTP test" \
  -Body "Hello from SMTP"
```

## curl
```bash
curl --url "smtp://smtp.example.com:587" \
  --ssl-reqd \
  --mail-from "sender@example.com" \
  --mail-rcpt "recipient@example.com" \
  --user "smtp-user:smtp-password" \
  -T <(printf "Subject: SMTP test\n\nHello from SMTP\n")
```

## Docs
- https://www.rfc-editor.org/rfc/rfc5321
- https://curl.se/docs/manpage.html
