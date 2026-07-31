#!/usr/bin/env python3
"""Scrape public events from Hengelo's event overview."""

from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape

from event_sources import load_text

URL = "https://aanmelden.hengelo.nl/evenementen"
MONTHS = {
    "jan": 1,
    "feb": 2,
    "mrt": 3,
    "apr": 4,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "nov": 11,
    "dec": 12,
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def scrape_events(
    html: str, year: int | None = None, month: int | None = None
) -> list[dict[str, object]]:
    now = datetime.now()
    year, month = year or now.year, month or now.month
    events = []
    for block in re.findall(
        r'<div class="eventDayList">(.*?)(?=<div class="eventDayList">'
        r"|</div>\s*</div>\s*<!-- jQuery)",
        html,
        re.S,
    ):
        day = re.search(r'eventDayNumber">(\d+).*?eventMonth">(\w+)', block, re.S)
        if not day or day.group(2).lower() not in MONTHS:
            continue
        event_month = MONTHS[day.group(2).lower()]
        event_year = year + (event_month < month)
        for href, name, location, times in re.findall(
            r'<h3><a href="([^"]+)">(.*?)</a></h3>\s*<p>(.*?)</p>.*?eventTimeBox">(.*?)</span>',
            block,
            re.S,
        ):
            start = f"{event_year}-{event_month:02d}-{int(day.group(1)):02d}"
            time = re.search(r"(\d{1,2}:\d{2})", clean(times))
            if time:
                start += f"T{time.group(1)}:00+02:00"
            events.append(
                {
                    "@type": "Event",
                    "name": clean(name),
                    "startDate": start,
                    "location": clean(location),
                    "genre": "Evenement",
                    "url": "https://aanmelden.hengelo.nl" + href,
                }
            )
    return events


if __name__ == "__main__":
    print(json.dumps(scrape_events(load_text(URL)), ensure_ascii=False))
