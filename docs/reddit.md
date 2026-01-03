# Reddit API

## Overview
Reddit offers OAuth2-protected REST APIs for user, subreddit, and content management. Register an application to obtain client credentials and a user agent string.

## Python
```python
import requests

client_id = "REDDIT_CLIENT_ID"
client_secret = "REDDIT_CLIENT_SECRET"
username = "REDDIT_USERNAME"
password = "REDDIT_PASSWORD"
user_agent = "example-script/0.1 by REDDIT_USERNAME"

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
headers = {"User-Agent": user_agent}

token_response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=auth,
    data={"grant_type": "password", "username": username, "password": password},
    headers=headers,
    timeout=30,
)
token_response.raise_for_status()
access_token = token_response.json()["access_token"]

api_headers = {"Authorization": f"bearer {access_token}", "User-Agent": user_agent}
me = requests.get("https://oauth.reddit.com/api/v1/me", headers=api_headers, timeout=30)
me.raise_for_status()
print(me.json())
```

## PowerShell
```powershell
$clientId = "REDDIT_CLIENT_ID"
$clientSecret = "REDDIT_CLIENT_SECRET"
$username = "REDDIT_USERNAME"
$password = "REDDIT_PASSWORD"
$userAgent = "example-script/0.1 by REDDIT_USERNAME"

$basicAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$clientId:$clientSecret"))
$tokenResponse = Invoke-RestMethod \
  -Method Post \
  -Uri "https://www.reddit.com/api/v1/access_token" \
  -Headers @{ Authorization = "Basic $basicAuth"; "User-Agent" = $userAgent } \
  -Body @{ grant_type = "password"; username = $username; password = $password }

$accessToken = $tokenResponse.access_token
Invoke-RestMethod \
  -Method Get \
  -Uri "https://oauth.reddit.com/api/v1/me" \
  -Headers @{ Authorization = "bearer $accessToken"; "User-Agent" = $userAgent }
```

## curl
```bash
access_token=$(curl -s https://www.reddit.com/api/v1/access_token \
  -u "REDDIT_CLIENT_ID:REDDIT_CLIENT_SECRET" \
  -H "User-Agent: example-script/0.1 by REDDIT_USERNAME" \
  -d "grant_type=password&username=REDDIT_USERNAME&password=REDDIT_PASSWORD" \
  | jq -r '.access_token')

curl https://oauth.reddit.com/api/v1/me \
  -H "Authorization: bearer $access_token" \
  -H "User-Agent: example-script/0.1 by REDDIT_USERNAME"
```

## Docs
- https://www.reddit.com/dev/api/
- https://github.com/reddit-archive/reddit/wiki/OAuth2
