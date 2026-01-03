# DNS

## Overview
DNS (Domain Name System) resolves names to IP addresses. Use DNS libraries or DNS-over-HTTPS (DoH) endpoints for programmatic queries.

## Python
```python
import dns.resolver

resolver = dns.resolver.Resolver()
answers = resolver.resolve("example.com", "A")
for rdata in answers:
    print(rdata.address)
```

## PowerShell
```powershell
Resolve-DnsName -Name "example.com" -Type A
Resolve-DnsName -Name "example.com" -Type MX
```

## curl
```bash
# DNS-over-HTTPS (Cloudflare)
curl "https://cloudflare-dns.com/dns-query?name=example.com&type=A" \
  -H "accept: application/dns-json"
```

## Docs
- https://www.rfc-editor.org/rfc/rfc1035
- https://dnspython.readthedocs.io/
- https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/
