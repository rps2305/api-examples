# VMware vSphere Web Services API

## Overview
The vSphere Web Services API is a SOAP-based interface for managing VMware vCenter and ESXi hosts. Authenticate with a session manager call and then invoke SOAP operations against the SDK endpoint.

## Python
```python
import requests

vcenter = "VCENTER_HOST"
username = "USERNAME"
password = "PASSWORD"

soap_envelope = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vim25="urn:vim25">
  <soapenv:Header/>
  <soapenv:Body>
    <vim25:RetrieveServiceContent>
      <vim25:_this type="ServiceInstance">ServiceInstance</vim25:_this>
    </vim25:RetrieveServiceContent>
  </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(
    f"https://{vcenter}/sdk",
    headers={"Content-Type": "text/xml"},
    data=soap_envelope,
    auth=(username, password),
    verify=False,
    timeout=60,
)
response.raise_for_status()
print(response.text)
```

## PowerShell
```powershell
$soapEnvelope = @"
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vim25="urn:vim25">
  <soapenv:Header/>
  <soapenv:Body>
    <vim25:RetrieveServiceContent>
      <vim25:_this type="ServiceInstance">ServiceInstance</vim25:_this>
    </vim25:RetrieveServiceContent>
  </soapenv:Body>
</soapenv:Envelope>
"@

Invoke-WebRequest -Method Post -Uri "https://VCENTER_HOST/sdk" -ContentType "text/xml" -Body $soapEnvelope -Credential (Get-Credential)
```

## curl
```bash
curl -k https://VCENTER_HOST/sdk \
  -u "USERNAME:PASSWORD" \
  -H "Content-Type: text/xml" \
  -d @- <<'EOF'
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vim25="urn:vim25">
  <soapenv:Header/>
  <soapenv:Body>
    <vim25:RetrieveServiceContent>
      <vim25:_this type="ServiceInstance">ServiceInstance</vim25:_this>
    </vim25:RetrieveServiceContent>
  </soapenv:Body>
</soapenv:Envelope>
EOF
```

## Docs
- https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/
