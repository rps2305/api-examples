# RSS

## Overview
RSS (Really Simple Syndication) is an XML-based format for publishing feeds. Consumers fetch the feed URL and parse items.

## Python
```python
import feedparser

feed = feedparser.parse("https://example.com/feed.xml")
for entry in feed.entries[:5]:
    print(entry.title)
```

## PowerShell
```powershell
[xml]$feed = Invoke-WebRequest -Uri "https://example.com/feed.xml"
$feed.rss.channel.item | Select-Object -First 5 -Property title, link
```

## curl
```bash
curl "https://example.com/feed.xml"
```

## Docs
- https://www.rssboard.org/rss-specification
- https://pythonhosted.org/feedparser/
