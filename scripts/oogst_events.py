#!/usr/bin/env python3
"""Scrape public upcoming events from Broedplaats Oogst."""

from __future__ import annotations

import json
import re
from html import unescape

from event_sources import load_text

URL = "https://oogst.eu/agenda/"
MONTHS = {
    "januari": "01",
    "februari": "02",
    "maart": "03",
    "april": "04",
    "mei": "05",
    "juni": "06",
    "juli": "07",
    "augustus": "08",
    "september": "09",
    "oktober": "10",
    "november": "11",
    "december": "12",
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def scrape_events(html: str) -> list[dict[str, object]]:
    events = []
    for card in re.findall(
        r'<div class="project-card">(.*?)(?=<div class="project-card"|</main>)', html, re.S
    ):
        date = re.search(
            r'<p class="tijdstip">\s*(\d{1,2})\s+(\w+)\s+(\d{4})'
            r'(?:\s*<span class="tijd">(\d{1,2}:\d{2}))?',
            card,
        )
        name = re.search(r"<h3>(.*?)</h3>", card, re.S)
        if not date or not name or date.group(2).lower() not in MONTHS:
            continue
        start = f"{date.group(3)}-{MONTHS[date.group(2).lower()]}-{int(date.group(1)):02d}"
        if date.group(4):
            start += f"T{date.group(4)}:00+02:00"
        genre = ", ".join(
            clean(value) for value in re.findall(r"<span[^>]*>(.*?)</span>", card, re.S)
        )
        events.append(
            {
                "@type": "Event",
                "name": clean(name.group(1)),
                "startDate": start,
                "location": "Broedplaats Oogst, Hengelo",
                "genre": genre,
                "url": URL,
            }
        )
    return events


if __name__ == "__main__":
    print(json.dumps(scrape_events(load_text(URL)), ensure_ascii=False))
