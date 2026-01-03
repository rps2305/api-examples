# API Examples

This repository contains concise usage notes and request examples for common APIs, self-hosted services, and protocols. Each item includes Python, PowerShell, and curl guidance plus links to official documentation.

## How to use
1. Open the relevant document in `docs/`.
2. Replace placeholders like `TOKEN`, `API_KEY`, `HOST`, and `PORT` with your values.
3. Use the Python/PowerShell/curl snippets as a starting point.
4. For more public APIs, browse https://free-apis.github.io/#/browse.

## Index

### AI & ML

| Name | Description | Doc |
| --- | --- | --- |
| BFL | Black Forest Labs model APIs. | [docs/bfl.md](docs/bfl.md) |
| Anthropic | Claude model APIs for chat and tool use. | [docs/anthropic.md](docs/anthropic.md) |
| Azure OpenAI | OpenAI-compatible models hosted on Azure. | [docs/azure-openai.md](docs/azure-openai.md) |
| Cohere | Text generation and embeddings APIs. | [docs/cohere.md](docs/cohere.md) |
| Draw Things | On-device AI image generation app and wiki. | [docs/drawthings.md](docs/drawthings.md) |
| Hugging Face Inference API | Hosted inference endpoints for models. | [docs/huggingface.md](docs/huggingface.md) |
| Jina AI Reader | Reader endpoint for fetching cleaned web content. | [docs/jina-ai.md](docs/jina-ai.md) |
| Novita AI | Hosted model inference with OpenAI-compatible APIs. | [docs/novita.md](docs/novita.md) |
| Ollama | Local model runtime with HTTP API. | [docs/ollama.md](docs/ollama.md) |
| OpenAI | AI model APIs for text, vision, and audio. | [docs/openai.md](docs/openai.md) |

### Collaboration & Productivity

| Name | Description | Doc |
| --- | --- | --- |
| BookStack | Self-hosted wiki and knowledge base with REST API. | [docs/bookstack.md](docs/bookstack.md) |
| Asana | Project and task management REST API. | [docs/asana.md](docs/asana.md) |
| Jira Cloud | Issue tracking and project management API. | [docs/jira.md](docs/jira.md) |
| Microsoft Graph | Unified API for Microsoft 365 services. | [docs/ms-graph.md](docs/ms-graph.md) |
| Notion | Workspace API for pages, databases, and blocks. | [docs/notion.md](docs/notion.md) |
| OmniFocus Automation | JavaScript automation API for OmniFocus. | [docs/omnifocus.md](docs/omnifocus.md) |
| Slack | Web API for messaging and workspace automation. | [docs/slack.md](docs/slack.md) |
| Trello | Boards, cards, and lists API. | [docs/trello.md](docs/trello.md) |

### Communications & Messaging

| Name | Description | Doc |
| --- | --- | --- |
| Discord | Chat platform APIs and bot/webhook integrations. | [docs/discord.md](docs/discord.md) |
| Gmail | Google email service with SMTP and Gmail API access. | [docs/gmail.md](docs/gmail.md) |
| ntfy | Lightweight publish/subscribe notification service over HTTP. | [docs/ntfy.md](docs/ntfy.md) |
| Signal (signal-cli REST) | Community REST service for Signal automation. | [docs/signal.md](docs/signal.md) |
| SMTP | Email sending protocol used by mail servers. | [docs/smtp.md](docs/smtp.md) |
| Telegram Bot API | Bot automation API for Telegram. | [docs/telegram-bot.md](docs/telegram-bot.md) |
| Twilio | Messaging and voice REST APIs. | [docs/twilio.md](docs/twilio.md) |

### Data & Databases

| Name | Description | Doc |
| --- | --- | --- |
| Microsoft SQL Server | Relational database system (TDS protocol). | [docs/ms-sql.md](docs/ms-sql.md) |
| MySQL | Relational database system (TCP protocol). | [docs/mysql.md](docs/mysql.md) |
| MongoDB Atlas Data API | HTTPS access to MongoDB collections. | [docs/mongodb-atlas.md](docs/mongodb-atlas.md) |
| PostgreSQL | Relational database system (TCP protocol). | [docs/postgres.md](docs/postgres.md) |
| Redis | In-memory data store (RESP protocol). | [docs/redis.md](docs/redis.md) |
| Elasticsearch | Search and analytics REST API. | [docs/elasticsearch.md](docs/elasticsearch.md) |
| OpenSearch | Open-source search REST API. | [docs/opensearch.md](docs/opensearch.md) |

### Developer Tools & Platforms

| Name | Description | Doc |
| --- | --- | --- |
| GitHub | REST and GraphQL APIs for repos and automation. | [docs/github.md](docs/github.md) |
| GitLab | REST APIs for repositories and CI/CD. | [docs/gitlab.md](docs/gitlab.md) |
| Bitbucket | REST APIs for repositories and pull requests. | [docs/bitbucket.md](docs/bitbucket.md) |
| CircleCI | CI/CD pipelines and job APIs. | [docs/circleci.md](docs/circleci.md) |
| Jenkins | Automation server with JSON API. | [docs/jenkins.md](docs/jenkins.md) |
| Pentestbook API Enumeration | Reference guide for enumerating web service APIs. | [docs/pentestbook-apis.md](docs/pentestbook-apis.md) |
| Postman Authentication | Configure diverse auth flows for Postman requests and collections. | [docs/postman-auth.md](docs/postman-auth.md) |
| REST API | Generic REST API request patterns and examples. | [docs/rest-api.md](docs/rest-api.md) |

### Events & Ticketing

| Name | Description | Doc |
| --- | --- | --- |
| Ticketmaster | Event discovery and listings API. | [docs/ticketmaster.md](docs/ticketmaster.md) |
| Yesplan Integrations | Event management integrations and API endpoints. | [docs/yesplan.md](docs/yesplan.md) |

### Files & Storage

| Name | Description | Doc |
| --- | --- | --- |
| Dropbox | Cloud file storage with REST API. | [docs/dropbox.md](docs/dropbox.md) |
| Google Drive | File storage and metadata API. | [docs/google-drive.md](docs/google-drive.md) |
| Amazon S3 | Object storage with HTTP API. | [docs/amazon-s3.md](docs/amazon-s3.md) |
| Azure Blob Storage | Object storage REST API. | [docs/azure-blob.md](docs/azure-blob.md) |
| MinIO | S3-compatible object storage. | [docs/minio.md](docs/minio.md) |
| SMB | Network file-sharing protocol (Windows/Samba). | [docs/smb.md](docs/smb.md) |
| SFTP | SSH File Transfer Protocol for secure file transfers. | [docs/sftp.md](docs/sftp.md) |
| WebDAV | HTTP extensions for remote file management. | [docs/webdav.md](docs/webdav.md) |

### Infrastructure & DevOps

| Name | Description | Doc |
| --- | --- | --- |
| Cloadpanel.io (CloudPanel) | Web server control panel (API varies by install). | [docs/cloadpanel-io.md](docs/cloadpanel-io.md) |
| DNS | Domain Name System resolution and DNS-over-HTTPS. | [docs/dns.md](docs/dns.md) |
| Docker Engine API | REST API for Docker daemon management. | [docs/docker.md](docs/docker.md) |
| Grafana | Monitoring and visualization HTTP API. | [docs/grafana.md](docs/grafana.md) |
| HashiCorp Vault | Secrets management REST API. | [docs/vault.md](docs/vault.md) |
| Kubernetes API | Cluster management REST API. | [docs/kubernetes.md](docs/kubernetes.md) |
| Pi-hole | DNS sinkhole with stats API. | [docs/pi-hole.md](docs/pi-hole.md) |
| Portainer | Container management UI with REST API. | [docs/portainer.md](docs/portainer.md) |
| Proxmox VE | Virtualization platform with REST API. | [docs/proxmox.md](docs/proxmox.md) |
| Prometheus | Metrics query HTTP API. | [docs/prometheus.md](docs/prometheus.md) |
| Prowlarr | Indexer management API for the *arr* stack. | [docs/prowlarr.md](docs/prowlarr.md) |
| Semaphore | Ansible Semaphore automation API. | [docs/semaphore.md](docs/semaphore.md) |
| Transmission | BitTorrent client with JSON-RPC API. | [docs/transmission.md](docs/transmission.md) |
| Uptime Kuma | Self-hosted monitoring with API endpoints. | [docs/uptime-kuma.md](docs/uptime-kuma.md) |
| VMware vSphere Web Services API | SOAP-based API for vCenter/ESXi management. | [docs/vsphere-web-services.md](docs/vsphere-web-services.md) |
| Web-Check | Self-hosted status and monitoring dashboard. | [docs/web-check.md](docs/web-check.md) |

### Industry & Enterprise

| Name | Description | Doc |
| --- | --- | --- |
| EAL ATS | Applicant tracking system (vendor-provided API). | [docs/eal-ats.md](docs/eal-ats.md) |
| GE Vernova Historian | Historian time-series APIs for industrial data. | [docs/ge-vernova-historian.md](docs/ge-vernova-historian.md) |
| Lansweeper | Asset and reporting APIs. | [docs/lansweeper.md](docs/lansweeper.md) |
| Seeq | Industrial analytics platform and APIs. | [docs/seeq.md](docs/seeq.md) |
| Visma Youforce | HR and payroll APIs for Youforce tenants. | [docs/visma-youforce.md](docs/visma-youforce.md) |

### Maps & Geo

| Name | Description | Doc |
| --- | --- | --- |
| 9292 Travel Advice API | Travel planning API for the Netherlands. | [docs/9292.md](docs/9292.md) |
| Google Maps API | Geocoding, places, and map services. | [docs/google-maps.md](docs/google-maps.md) |
| KNMI | Dutch meteorological data platform APIs. | [docs/knmi.md](docs/knmi.md) |
| Leaflet | JavaScript mapping library for interactive maps. | [docs/leaflet.md](docs/leaflet.md) |
| Mapbox | Mapping, geocoding, and tiles API. | [docs/mapbox.md](docs/mapbox.md) |
| NS APIs | Nederlandse Spoorwegen travel information APIs. | [docs/ns.md](docs/ns.md) |
| OpenWeather | Weather data APIs. | [docs/openweather.md](docs/openweather.md) |
| OpenStreetMap | Open map data with Nominatim geocoding. | [docs/openstreetmap.md](docs/openstreetmap.md) |
| WeatherAPI.com | Weather data APIs. | [docs/weatherapi.md](docs/weatherapi.md) |

### Media & Content

| Name | Description | Doc |
| --- | --- | --- |
| Apple iTunes Search API | Media catalog search API. | [docs/apple-itunes.md](docs/apple-itunes.md) |
| Drupal JSON:API | Standardized JSON:API endpoints for Drupal content. | [docs/drupal-jsonapi.md](docs/drupal-jsonapi.md) |
| Imaginary | HTTP image processing service. | [docs/imaginary.md](docs/imaginary.md) |
| Open Food Facts | Open datasets and APIs for food product data. | [docs/openfoodfacts.md](docs/openfoodfacts.md) |
| Reddit | OAuth2-protected REST APIs for Reddit. | [docs/reddit.md](docs/reddit.md) |
| RSS | XML-based syndication feed format. | [docs/rss.md](docs/rss.md) |
| Spotify | Music streaming Web API. | [docs/spotify.md](docs/spotify.md) |
| Stirling PDF | Self-hosted PDF toolkit with REST API. | [docs/stirling-pdf.md](docs/stirling-pdf.md) |
| Tints Palette API | Palette generation endpoint for Tints. | [docs/tints.md](docs/tints.md) |
| TMDB | Movie, TV, and people metadata API. | [docs/tmdb.md](docs/tmdb.md) |
| Vimeo | Video platform REST API. | [docs/vimeo.md](docs/vimeo.md) |
| YouTube | YouTube Data API for search and channel data. | [docs/youtube.md](docs/youtube.md) |
| YouTubeDL-Material | Self-hosted media downloader UI with REST API. | [docs/youtubedl-material.md](docs/youtubedl-material.md) |

## Not found
Some entries do not have clear public API documentation or are ambiguous. See [docs/NOTFOUND.md](docs/NOTFOUND.md) for details.
