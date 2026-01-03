# Postman Authentication

## Overview
Postman supports multiple authentication types on each request or collection. Set auth in the **Authorization** tab, and use environment variables (for example `{{API_TOKEN}}`) so you can switch between environments.

## Common setup tips
- Use **Collection** auth if multiple requests share the same credentials.
- Store secrets in **Environments** or **Vault** (Postman app) instead of hard-coding values.
- Use the **Headers** tab to confirm generated headers (for example `Authorization`).

## Authentication types

### No Auth
Use for public endpoints or when auth is handled elsewhere (for example via IP allowlist).

### Basic Auth
1. Select **Basic Auth**.
2. Enter **Username** and **Password**.
3. Postman adds the `Authorization: Basic ...` header.

### Bearer Token
1. Select **Bearer Token**.
2. Paste the token or reference `{{API_TOKEN}}`.
3. Postman adds `Authorization: Bearer <token>`.

### API Key
1. Select **API Key**.
2. Choose where to add the key (**Header** or **Query Params**).
3. Enter the key name (for example `X-API-Key`) and value (`{{API_KEY}}`).

### OAuth 2.0
1. Select **OAuth 2.0**.
2. Click **Get New Access Token**.
3. Provide the auth URL, token URL, client ID/secret, scopes, and callback URL.
4. Click **Request Token**, then **Use Token** to attach it to the request.

### OAuth 1.0
1. Select **OAuth 1.0**.
2. Enter consumer key/secret, token, and token secret.
3. Choose signature method and add the OAuth parameters to the header.

### Digest Auth
1. Select **Digest Auth**.
2. Enter username and password.
3. Postman will handle the challenge/response flow.

### NTLM
1. Select **NTLM**.
2. Provide username, password, domain, and workstation.
3. Postman will generate the NTLM authentication headers.

## Example environment variables
Create an environment with variables like:
- `API_BASE_URL`: `https://api.example.com/v1`
- `API_TOKEN`: `TOKEN`
- `API_KEY`: `KEY`

Then reference them in requests: `{{API_BASE_URL}}/widgets` or `{{API_TOKEN}}`.

## Docs
- https://learning.postman.com/docs/sending-requests/authorization/authorization-types/
- https://learning.postman.com/docs/sending-requests/variables/variables/
