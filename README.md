# API Examples

This repository contains concise usage notes and request examples for common APIs, self-hosted services, and protocols. Each item includes Python, PowerShell, and curl guidance plus links to official documentation.

## How to use
1. Open the relevant document in `docs/`.
2. Replace placeholders like `TOKEN`, `API_KEY`, `HOST`, and `PORT` with your values.
3. Use the Python/PowerShell/curl snippets as a starting point.
4. For more public APIs, browse https://free-apis.github.io/#/browse.

## Quality checks
Run the docs validator before opening a PR to catch broken README links, indexing
mismatches, and missing standard doc sections:

```bash
python scripts/validate_docs.py
```

## Index

### AI & ML

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BFL</td>
      <td>Black Forest Labs model APIs.</td>
      <td>Yes</td>
      <td><a href="docs/bfl.md">docs/bfl.md</a></td>
    </tr>
    <tr>
      <td>Anthropic</td>
      <td>Claude model APIs for chat and tool use.</td>
      <td>Yes</td>
      <td><a href="docs/anthropic.md">docs/anthropic.md</a></td>
    </tr>
    <tr>
      <td>Azure OpenAI</td>
      <td>OpenAI-compatible models hosted on Azure.</td>
      <td>Yes</td>
      <td><a href="docs/azure-openai.md">docs/azure-openai.md</a></td>
    </tr>
    <tr>
      <td>Cohere</td>
      <td>Text generation and embeddings APIs.</td>
      <td>Yes</td>
      <td><a href="docs/cohere.md">docs/cohere.md</a></td>
    </tr>
    <tr>
      <td>Draw Things</td>
      <td>On-device AI image generation app and wiki.</td>
      <td>No</td>
      <td><a href="docs/drawthings.md">docs/drawthings.md</a></td>
    </tr>
    <tr>
      <td>Hugging Face Inference API</td>
      <td>Hosted inference endpoints for models.</td>
      <td>Yes</td>
      <td><a href="docs/huggingface.md">docs/huggingface.md</a></td>
    </tr>
    <tr>
      <td>Jina AI Reader</td>
      <td>Reader endpoint for fetching cleaned web content.</td>
      <td>No</td>
      <td><a href="docs/jina-ai.md">docs/jina-ai.md</a></td>
    </tr>
    <tr>
      <td>Novita AI</td>
      <td>Hosted model inference with OpenAI-compatible APIs.</td>
      <td>Yes</td>
      <td><a href="docs/novita.md">docs/novita.md</a></td>
    </tr>
    <tr>
      <td>Ollama</td>
      <td>Local model runtime with HTTP API.</td>
      <td>No</td>
      <td><a href="docs/ollama.md">docs/ollama.md</a></td>
    </tr>
    <tr>
      <td>OpenAI</td>
      <td>AI model APIs for text, vision, and audio.</td>
      <td>Yes</td>
      <td><a href="docs/openai.md">docs/openai.md</a></td>
    </tr>
  </tbody>
</table>

### Collaboration & Productivity

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BookStack</td>
      <td>Self-hosted wiki and knowledge base with REST API.</td>
      <td>Varies</td>
      <td><a href="docs/bookstack.md">docs/bookstack.md</a></td>
    </tr>
    <tr>
      <td>Asana</td>
      <td>Project and task management REST API.</td>
      <td>Yes</td>
      <td><a href="docs/asana.md">docs/asana.md</a></td>
    </tr>
    <tr>
      <td>Jira Cloud</td>
      <td>Issue tracking and project management API.</td>
      <td>Yes</td>
      <td><a href="docs/jira.md">docs/jira.md</a></td>
    </tr>
    <tr>
      <td>Microsoft Graph</td>
      <td>Unified API for Microsoft 365 services.</td>
      <td>Yes</td>
      <td><a href="docs/ms-graph.md">docs/ms-graph.md</a></td>
    </tr>
    <tr>
      <td>Notion</td>
      <td>Workspace API for pages, databases, and blocks.</td>
      <td>Yes</td>
      <td><a href="docs/notion.md">docs/notion.md</a></td>
    </tr>
    <tr>
      <td>OmniFocus Automation</td>
      <td>JavaScript automation API for OmniFocus.</td>
      <td>No</td>
      <td><a href="docs/omnifocus.md">docs/omnifocus.md</a></td>
    </tr>
    <tr>
      <td>Slack</td>
      <td>Web API for messaging and workspace automation.</td>
      <td>Yes</td>
      <td><a href="docs/slack.md">docs/slack.md</a></td>
    </tr>
    <tr>
      <td>Trello</td>
      <td>Boards, cards, and lists API.</td>
      <td>Yes</td>
      <td><a href="docs/trello.md">docs/trello.md</a></td>
    </tr>
  </tbody>
</table>

### Communications & Messaging

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Discord</td>
      <td>Chat platform APIs and bot/webhook integrations.</td>
      <td>Yes</td>
      <td><a href="docs/discord.md">docs/discord.md</a></td>
    </tr>
    <tr>
      <td>Gmail</td>
      <td>Google email service with SMTP and Gmail API access.</td>
      <td>Yes</td>
      <td><a href="docs/gmail.md">docs/gmail.md</a></td>
    </tr>
    <tr>
      <td>ntfy</td>
      <td>Lightweight publish/subscribe notification service over HTTP.</td>
      <td>Varies</td>
      <td><a href="docs/ntfy.md">docs/ntfy.md</a></td>
    </tr>
    <tr>
      <td>Signal (signal-cli REST)</td>
      <td>Community REST service for Signal automation.</td>
      <td>No</td>
      <td><a href="docs/signal.md">docs/signal.md</a></td>
    </tr>
    <tr>
      <td>SMTP</td>
      <td>Email sending protocol used by mail servers.</td>
      <td>No</td>
      <td><a href="docs/smtp.md">docs/smtp.md</a></td>
    </tr>
    <tr>
      <td>Telegram Bot API</td>
      <td>Bot automation API for Telegram.</td>
      <td>Yes</td>
      <td><a href="docs/telegram-bot.md">docs/telegram-bot.md</a></td>
    </tr>
    <tr>
      <td>Twilio</td>
      <td>Messaging and voice REST APIs.</td>
      <td>Yes</td>
      <td><a href="docs/twilio.md">docs/twilio.md</a></td>
    </tr>
  </tbody>
</table>

### Data & Databases

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Microsoft SQL Server</td>
      <td>Relational database system (TDS protocol).</td>
      <td>No</td>
      <td><a href="docs/ms-sql.md">docs/ms-sql.md</a></td>
    </tr>
    <tr>
      <td>MySQL</td>
      <td>Relational database system (TCP protocol).</td>
      <td>No</td>
      <td><a href="docs/mysql.md">docs/mysql.md</a></td>
    </tr>
    <tr>
      <td>MongoDB Atlas Data API</td>
      <td>HTTPS access to MongoDB collections.</td>
      <td>Yes</td>
      <td><a href="docs/mongodb-atlas.md">docs/mongodb-atlas.md</a></td>
    </tr>
    <tr>
      <td>PostgreSQL</td>
      <td>Relational database system (TCP protocol).</td>
      <td>No</td>
      <td><a href="docs/postgres.md">docs/postgres.md</a></td>
    </tr>
    <tr>
      <td>Redis</td>
      <td>In-memory data store (RESP protocol).</td>
      <td>No</td>
      <td><a href="docs/redis.md">docs/redis.md</a></td>
    </tr>
    <tr>
      <td>Elasticsearch</td>
      <td>Search and analytics REST API.</td>
      <td>Varies</td>
      <td><a href="docs/elasticsearch.md">docs/elasticsearch.md</a></td>
    </tr>
    <tr>
      <td>OpenSearch</td>
      <td>Open-source search REST API.</td>
      <td>Varies</td>
      <td><a href="docs/opensearch.md">docs/opensearch.md</a></td>
    </tr>
  </tbody>
</table>

### Developer Tools & Platforms

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GitHub</td>
      <td>REST and GraphQL APIs for repos and automation.</td>
      <td>Yes</td>
      <td><a href="docs/github.md">docs/github.md</a></td>
    </tr>
    <tr>
      <td>GitLab</td>
      <td>REST APIs for repositories and CI/CD.</td>
      <td>Yes</td>
      <td><a href="docs/gitlab.md">docs/gitlab.md</a></td>
    </tr>
    <tr>
      <td>Bitbucket</td>
      <td>REST APIs for repositories and pull requests.</td>
      <td>Yes</td>
      <td><a href="docs/bitbucket.md">docs/bitbucket.md</a></td>
    </tr>
    <tr>
      <td>CircleCI</td>
      <td>CI/CD pipelines and job APIs.</td>
      <td>Yes</td>
      <td><a href="docs/circleci.md">docs/circleci.md</a></td>
    </tr>
    <tr>
      <td>Jenkins</td>
      <td>Automation server with JSON API.</td>
      <td>Varies</td>
      <td><a href="docs/jenkins.md">docs/jenkins.md</a></td>
    </tr>
    <tr>
      <td>Pentestbook API Enumeration</td>
      <td>Reference guide for enumerating web service APIs.</td>
      <td>No</td>
      <td><a href="docs/pentestbook-apis.md">docs/pentestbook-apis.md</a></td>
    </tr>
    <tr>
      <td>Postman Authentication</td>
      <td>Configure diverse auth flows for Postman requests and collections.</td>
      <td>No</td>
      <td><a href="docs/postman-auth.md">docs/postman-auth.md</a></td>
    </tr>
    <tr>
      <td>REST API</td>
      <td>Generic REST API request patterns and examples.</td>
      <td>No</td>
      <td><a href="docs/rest-api.md">docs/rest-api.md</a></td>
    </tr>
  </tbody>
</table>

### Events & Ticketing

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Ticketmaster</td>
      <td>Event discovery and listings API.</td>
      <td>Yes</td>
      <td><a href="docs/ticketmaster.md">docs/ticketmaster.md</a></td>
    </tr>
    <tr>
      <td>Yesplan Integrations</td>
      <td>Event management integrations and API endpoints.</td>
      <td>Yes</td>
      <td><a href="docs/yesplan.md">docs/yesplan.md</a></td>
    </tr>
  </tbody>
</table>

### Files & Storage

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dropbox</td>
      <td>Cloud file storage with REST API.</td>
      <td>Yes</td>
      <td><a href="docs/dropbox.md">docs/dropbox.md</a></td>
    </tr>
    <tr>
      <td>Google Drive</td>
      <td>File storage and metadata API.</td>
      <td>Yes</td>
      <td><a href="docs/google-drive.md">docs/google-drive.md</a></td>
    </tr>
    <tr>
      <td>Amazon S3</td>
      <td>Object storage with HTTP API.</td>
      <td>Yes</td>
      <td><a href="docs/amazon-s3.md">docs/amazon-s3.md</a></td>
    </tr>
    <tr>
      <td>Azure Blob Storage</td>
      <td>Object storage REST API.</td>
      <td>Yes</td>
      <td><a href="docs/azure-blob.md">docs/azure-blob.md</a></td>
    </tr>
    <tr>
      <td>MinIO</td>
      <td>S3-compatible object storage.</td>
      <td>Yes</td>
      <td><a href="docs/minio.md">docs/minio.md</a></td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>Network file-sharing protocol (Windows/Samba).</td>
      <td>No</td>
      <td><a href="docs/smb.md">docs/smb.md</a></td>
    </tr>
    <tr>
      <td>SFTP</td>
      <td>SSH File Transfer Protocol for secure file transfers.</td>
      <td>No</td>
      <td><a href="docs/sftp.md">docs/sftp.md</a></td>
    </tr>
    <tr>
      <td>WebDAV</td>
      <td>HTTP extensions for remote file management.</td>
      <td>Varies</td>
      <td><a href="docs/webdav.md">docs/webdav.md</a></td>
    </tr>
  </tbody>
</table>

### Infrastructure & DevOps

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cloadpanel.io (CloudPanel)</td>
      <td>Web server control panel (API varies by install).</td>
      <td>Varies</td>
      <td><a href="docs/cloadpanel-io.md">docs/cloadpanel-io.md</a></td>
    </tr>
    <tr>
      <td>DNS</td>
      <td>Domain Name System resolution and DNS-over-HTTPS.</td>
      <td>No</td>
      <td><a href="docs/dns.md">docs/dns.md</a></td>
    </tr>
    <tr>
      <td>Docker Engine API</td>
      <td>REST API for Docker daemon management.</td>
      <td>No</td>
      <td><a href="docs/docker.md">docs/docker.md</a></td>
    </tr>
    <tr>
      <td>Grafana</td>
      <td>Monitoring and visualization HTTP API.</td>
      <td>Varies</td>
      <td><a href="docs/grafana.md">docs/grafana.md</a></td>
    </tr>
    <tr>
      <td>HashiCorp Vault</td>
      <td>Secrets management REST API.</td>
      <td>Yes</td>
      <td><a href="docs/vault.md">docs/vault.md</a></td>
    </tr>
    <tr>
      <td>Kubernetes API</td>
      <td>Cluster management REST API.</td>
      <td>Yes</td>
      <td><a href="docs/kubernetes.md">docs/kubernetes.md</a></td>
    </tr>
    <tr>
      <td>Pi-hole</td>
      <td>DNS sinkhole with stats API.</td>
      <td>Varies</td>
      <td><a href="docs/pi-hole.md">docs/pi-hole.md</a></td>
    </tr>
    <tr>
      <td>Portainer</td>
      <td>Container management UI with REST API.</td>
      <td>Yes</td>
      <td><a href="docs/portainer.md">docs/portainer.md</a></td>
    </tr>
    <tr>
      <td>Proxmox VE</td>
      <td>Virtualization platform with REST API.</td>
      <td>Yes</td>
      <td><a href="docs/proxmox.md">docs/proxmox.md</a></td>
    </tr>
    <tr>
      <td>Prometheus</td>
      <td>Metrics query HTTP API.</td>
      <td>Varies</td>
      <td><a href="docs/prometheus.md">docs/prometheus.md</a></td>
    </tr>
    <tr>
      <td>Prowlarr</td>
      <td>Indexer management API for the *arr* stack.</td>
      <td>Varies</td>
      <td><a href="docs/prowlarr.md">docs/prowlarr.md</a></td>
    </tr>
    <tr>
      <td>Semaphore</td>
      <td>Ansible Semaphore automation API.</td>
      <td>Varies</td>
      <td><a href="docs/semaphore.md">docs/semaphore.md</a></td>
    </tr>
    <tr>
      <td>Transmission</td>
      <td>BitTorrent client with JSON-RPC API.</td>
      <td>Varies</td>
      <td><a href="docs/transmission.md">docs/transmission.md</a></td>
    </tr>
    <tr>
      <td>Uptime Kuma</td>
      <td>Self-hosted monitoring with API endpoints.</td>
      <td>Varies</td>
      <td><a href="docs/uptime-kuma.md">docs/uptime-kuma.md</a></td>
    </tr>
    <tr>
      <td>VMware vSphere Web Services API</td>
      <td>SOAP-based API for vCenter/ESXi management.</td>
      <td>Yes</td>
      <td><a href="docs/vsphere-web-services.md">docs/vsphere-web-services.md</a></td>
    </tr>
    <tr>
      <td>Web-Check</td>
      <td>Self-hosted status and monitoring dashboard.</td>
      <td>Varies</td>
      <td><a href="docs/web-check.md">docs/web-check.md</a></td>
    </tr>
  </tbody>
</table>

### Industry & Enterprise

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>EAL ATS</td>
      <td>Applicant tracking system (vendor-provided API).</td>
      <td>Varies</td>
      <td><a href="docs/eal-ats.md">docs/eal-ats.md</a></td>
    </tr>
    <tr>
      <td>GE Vernova Historian</td>
      <td>Historian time-series APIs for industrial data.</td>
      <td>Varies</td>
      <td><a href="docs/ge-vernova-historian.md">docs/ge-vernova-historian.md</a></td>
    </tr>
    <tr>
      <td>Lansweeper</td>
      <td>Asset and reporting APIs.</td>
      <td>Yes</td>
      <td><a href="docs/lansweeper.md">docs/lansweeper.md</a></td>
    </tr>
    <tr>
      <td>Seeq</td>
      <td>Industrial analytics platform and APIs.</td>
      <td>Yes</td>
      <td><a href="docs/seeq.md">docs/seeq.md</a></td>
    </tr>
    <tr>
      <td>Visma Youforce</td>
      <td>HR and payroll APIs for Youforce tenants.</td>
      <td>Yes</td>
      <td><a href="docs/visma-youforce.md">docs/visma-youforce.md</a></td>
    </tr>
  </tbody>
</table>

### Maps & Geo

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>9292 Travel Advice API</td>
      <td>Travel planning API for the Netherlands.</td>
      <td>Yes</td>
      <td><a href="docs/9292.md">docs/9292.md</a></td>
    </tr>
    <tr>
      <td>Google Maps API</td>
      <td>Geocoding, places, and map services.</td>
      <td>Yes</td>
      <td><a href="docs/google-maps.md">docs/google-maps.md</a></td>
    </tr>
    <tr>
      <td>KNMI</td>
      <td>Dutch meteorological data platform APIs.</td>
      <td>No</td>
      <td><a href="docs/knmi.md">docs/knmi.md</a></td>
    </tr>
    <tr>
      <td>Leaflet</td>
      <td>JavaScript mapping library for interactive maps.</td>
      <td>No</td>
      <td><a href="docs/leaflet.md">docs/leaflet.md</a></td>
    </tr>
    <tr>
      <td>Mapbox</td>
      <td>Mapping, geocoding, and tiles API.</td>
      <td>Yes</td>
      <td><a href="docs/mapbox.md">docs/mapbox.md</a></td>
    </tr>
    <tr>
      <td>NS APIs</td>
      <td>Nederlandse Spoorwegen travel information APIs.</td>
      <td>Yes</td>
      <td><a href="docs/ns.md">docs/ns.md</a></td>
    </tr>
    <tr>
      <td>OpenWeather</td>
      <td>Weather data APIs.</td>
      <td>Yes</td>
      <td><a href="docs/openweather.md">docs/openweather.md</a></td>
    </tr>
    <tr>
      <td>OpenStreetMap</td>
      <td>Open map data with Nominatim geocoding.</td>
      <td>No</td>
      <td><a href="docs/openstreetmap.md">docs/openstreetmap.md</a></td>
    </tr>
    <tr>
      <td>WeatherAPI.com</td>
      <td>Weather data APIs.</td>
      <td>Yes</td>
      <td><a href="docs/weatherapi.md">docs/weatherapi.md</a></td>
    </tr>
  </tbody>
</table>

### Media & Content

<table style="width: 100%;">
  <colgroup>
    <col style="width: 20%;">
    <col style="width: 55%;">
    <col style="width: 10%;">
    <col style="width: 15%;">
  </colgroup>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>API Key Required</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apple iTunes Search API</td>
      <td>Media catalog search API.</td>
      <td>No</td>
      <td><a href="docs/apple-itunes.md">docs/apple-itunes.md</a></td>
    </tr>
    <tr>
      <td>Drupal JSON:API</td>
      <td>Standardized JSON:API endpoints for Drupal content.</td>
      <td>Varies</td>
      <td><a href="docs/drupal-jsonapi.md">docs/drupal-jsonapi.md</a></td>
    </tr>
    <tr>
      <td>Imaginary</td>
      <td>HTTP image processing service.</td>
      <td>No</td>
      <td><a href="docs/imaginary.md">docs/imaginary.md</a></td>
    </tr>
    <tr>
      <td>Open Food Facts</td>
      <td>Open datasets and APIs for food product data.</td>
      <td>No</td>
      <td><a href="docs/openfoodfacts.md">docs/openfoodfacts.md</a></td>
    </tr>
    <tr>
      <td>Reddit</td>
      <td>OAuth2-protected REST APIs for Reddit.</td>
      <td>Yes</td>
      <td><a href="docs/reddit.md">docs/reddit.md</a></td>
    </tr>
    <tr>
      <td>RSS</td>
      <td>XML-based syndication feed format.</td>
      <td>No</td>
      <td><a href="docs/rss.md">docs/rss.md</a></td>
    </tr>
    <tr>
      <td>Spotify</td>
      <td>Music streaming Web API.</td>
      <td>Yes</td>
      <td><a href="docs/spotify.md">docs/spotify.md</a></td>
    </tr>
    <tr>
      <td>Stirling PDF</td>
      <td>Self-hosted PDF toolkit with REST API.</td>
      <td>Varies</td>
      <td><a href="docs/stirling-pdf.md">docs/stirling-pdf.md</a></td>
    </tr>
    <tr>
      <td>Tints Palette API</td>
      <td>Palette generation endpoint for Tints.</td>
      <td>No</td>
      <td><a href="docs/tints.md">docs/tints.md</a></td>
    </tr>
    <tr>
      <td>TMDB</td>
      <td>Movie, TV, and people metadata API.</td>
      <td>Yes</td>
      <td><a href="docs/tmdb.md">docs/tmdb.md</a></td>
    </tr>
    <tr>
      <td>Vimeo</td>
      <td>Video platform REST API.</td>
      <td>Yes</td>
      <td><a href="docs/vimeo.md">docs/vimeo.md</a></td>
    </tr>
    <tr>
      <td>YouTube</td>
      <td>YouTube Data API for search and channel data.</td>
      <td>Yes</td>
      <td><a href="docs/youtube.md">docs/youtube.md</a></td>
    </tr>
    <tr>
      <td>YouTubeDL-Material</td>
      <td>Self-hosted media downloader UI with REST API.</td>
      <td>Varies</td>
      <td><a href="docs/youtubedl-material.md">docs/youtubedl-material.md</a></td>
    </tr>
  </tbody>
</table>

## Not found
Some entries do not have clear public API documentation or are ambiguous. See [docs/NOTFOUND.md](docs/NOTFOUND.md) for details.
