#!/usr/bin/env python3
"""Create an iCalendar by scraping FC Twente's public fixture page (no API key)."""

from __future__ import annotations

import argparse
import hashlib
import re
from html import unescape
from pathlib import Path

from event_sources import EventSourceError, ical_datetime, json_ld_events, load_text

DEFAULT_URL = "https://fctwente.nl/wedstrijden/eerste-selectie"

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


def scrape_matches(html: str) -> list[dict[str, object]]:
    """Extract date, time, and teams from FC Twente's rendered match cards."""
    matches: list[dict[str, object]] = []
    cards = re.findall(
        r'<div class="bg-white grid grid-cols-3.*?'
        r'(?=<div class="bg-white grid grid-cols-3|<aside data-drawer)',
        html,
        re.DOTALL,
    )
    for card in cards:
        date = re.search(r'<div class="text-lg font-serif">\s*(\d{1,2}) (\w+) (\d{4})', card)
        time = re.search(
            r"(?:donderdag|vrijdag|zaterdag|zondag|maandag|dinsdag|woensdag)\s+(\d{1,2}:\d{2})",
            card,
        )
        teams = re.findall(r'alt="Logo ([^"]+)"', card)
        if not date or len(teams) != 2 or date.group(2) not in MONTHS:
            continue
        start = f"{date.group(3)}-{MONTHS[date.group(2)]}-{int(date.group(1)):02d}"
        if time:
            start += f"T{time.group(1)}:00+02:00"
        teams = ["FC Twente" if team == "Eerste Selectie" else unescape(team) for team in teams]
        matches.append(
            {
                "@type": "SportsEvent",
                "name": f"{teams[0]} - {teams[1]}",
                "startDate": start,
                "genre": "Voetbal",
                # The FC Twente fixture card lists the away team first.
                "isHome": teams[1] == "FC Twente",
            }
        )
    return matches


def escape(value: object) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold(line: str) -> list[str]:
    """Fold an iCalendar content line at the RFC 5545 75-octet boundary."""
    result: list[str] = []
    prefix = ""
    while len((prefix + line).encode("utf-8")) > 75:
        size = 75 - len(prefix.encode("utf-8"))
        cut = 0
        for index in range(1, len(line) + 1):
            if len(line[:index].encode("utf-8")) > size:
                break
            cut = index
        result.append(prefix + line[:cut])
        line, prefix = line[cut:], " "
    result.append(prefix + line)
    return result


def text(value: object, key: str = "name") -> str:
    if isinstance(value, dict):
        return str(value.get(key, ""))
    return str(value or "")


def make_calendar(events: list[dict[str, object]]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//api-examples//FC Twente//EN",
        "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:FC Twente wedstrijden",
    ]
    for event in events:
        kinds = event.get("@type")
        kinds = kinds if isinstance(kinds, list) else [kinds]
        if "SportsEvent" not in kinds:
            continue
        name = text(event.get("name"))
        start = event.get("startDate")
        if not name or not start:
            continue
        identity = str(event.get("url") or f"{name}-{start}")
        uid = hashlib.sha256(identity.encode()).hexdigest()[:24]
        location = text(event.get("location"))
        description = text(event.get("description"))
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}@api-examples",
                f"DTSTART{ical_datetime(start)}",
                f"SUMMARY:{escape(name)}",
            ]
        )
        if event.get("endDate"):
            lines.append(f"DTEND{ical_datetime(event['endDate'])}")
        if location:
            lines.append(f"LOCATION:{escape(location)}")
        if description:
            lines.append(f"DESCRIPTION:{escape(description)}")
        if event.get("url"):
            lines.append(f"URL:{event['url']}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(part for line in lines for part in fold(line)) + "\r\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="FC Twente fixtures page")
    parser.add_argument("--input", type=Path, help="parse a previously downloaded HTML file")
    parser.add_argument("--output", type=Path, default=Path("fc-twente.ics"))
    args = parser.parse_args()
    try:
        html = load_text(args.url, args.input)
    except EventSourceError as exc:
        parser.error(str(exc))
    events = scrape_matches(html) or json_ld_events(html)
    if not events:
        parser.error("no fixtures found; check the fixtures URL or page format")
    calendar = make_calendar(events)
    count = calendar.count("BEGIN:VEVENT")
    if not count:
        parser.error("events were found, but none contained a name and startDate")
    try:
        args.output.write_text(calendar, encoding="utf-8", newline="")
    except OSError as exc:
        parser.error(f"could not write {args.output}: {exc.strerror}")
    print(f"Wrote {count} fixtures to {args.output}")


if __name__ == "__main__":
    main()
