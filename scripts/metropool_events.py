#!/usr/bin/env python3
"""Get events from the Metropool agenda page."""

import argparse
import re
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

from event_sources import EventSourceError, get_text, json_ld_events, load_text, print_events

DEFAULT_URL = "https://metropool.nl/agenda/"
PARTIAL_URL = (
    "https://metropool.nl/mvc/event/partial?pNumber={page}"
    "&keyword=&genre=&tag=&type=&StartDate=&EndDate=&locatie=&label=&newAnnounced=False"
)


def clean(value: str) -> str:
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", value)).split())


def scrape_events(html: str) -> list[dict[str, object]]:
    """Extract the agenda cards rendered in Metropool's server-side HTML."""
    events: list[dict[str, object]] = []
    starts = list(re.finditer(r'<div class="event relative ', html))
    for index, match in enumerate(starts):
        card = html[match.start() : starts[index + 1].start() if index + 1 < len(starts) else None]
        name = re.search(r'<h4 class="event-title[^>]*">(.*?)</h4>', card, re.DOTALL)
        date_time = re.search(r'data-event-category3="(\d{2}-\d{2}-\d{4}) / (\d{2}:\d{2})"', card)
        genre = re.search(r'<span class="event-genre">(.*?)</span>', card, re.DOTALL)
        location = re.search(r'<p class="event-location">(.*?)</p>', card, re.DOTALL)
        link = re.search(r'<a class="remove-underline" href="([^"]+)" data-detail-link=', card)
        ticket = re.search(r'<a class="btn btn-primary[^>]* href="([^"]+)"', card)
        if not name or not date_time:
            continue
        date = date_time.group(1)
        start = f"{date[6:]}-{date[3:5]}-{date[:2]}T{date_time.group(2)}:00+02:00"
        event: dict[str, object] = {
            "@type": "Event",
            "name": clean(name.group(1)),
            "startDate": start,
        }
        if location:
            event["location"] = clean(location.group(1))
        if genre:
            event["genre"] = clean(genre.group(1))
        if link:
            event["url"] = f"https://metropool.nl{link.group(1)}"
        if ticket:
            event["ticketUrl"] = urljoin(DEFAULT_URL, unescape(ticket.group(1)))
        events.append(event)
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Metropool agenda URL")
    parser.add_argument("--input", type=Path, help="parse a previously downloaded HTML file")
    args = parser.parse_args()
    try:
        html = load_text(args.url, args.input)
    except EventSourceError as exc:
        parser.error(str(exc))
    events = scrape_events(html) or json_ld_events(html)
    if args.input is None and args.url == DEFAULT_URL:
        page = 2
        while True:
            page_events = scrape_events(get_text(PARTIAL_URL.format(page=page)))
            if not page_events:
                break
            events.extend(page_events)
            page += 1
    if not events:
        parser.error("no events found; check the agenda URL or page format")
    print_events(events)


if __name__ == "__main__":
    main()
