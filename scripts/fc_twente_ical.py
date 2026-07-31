#!/usr/bin/env python3
"""Create an iCalendar from FC Twente's public fixture page (no API key)."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from event_sources import EventSourceError, ical_datetime, json_ld_events, load_text

DEFAULT_URL = "https://www.fctwente.nl/teams/eerste-selectie/wedstrijden"


def escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


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
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//api-examples//FC Twente//EN", "CALSCALE:GREGORIAN", "X-WR-CALNAME:FC Twente wedstrijden"]
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//api-examples//FC Twente//EN", "CALSCALE:GREGORIAN"]
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
        lines.extend(["BEGIN:VEVENT", f"UID:{uid}@api-examples", f"DTSTART{ical_datetime(start)}", f"SUMMARY:{escape(name)}"])
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
    return "\r\n".join(lines) + "\r\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="FC Twente fixtures page")
    parser.add_argument("--input", type=Path, help="parse a previously downloaded HTML file")
    parser.add_argument("--output", type=Path, default=Path("fc-twente.ics"))
    args = parser.parse_args()
    try:
        events = json_ld_events(load_text(args.url, args.input))
    except EventSourceError as exc:
        parser.error(str(exc))
    if not events:
        parser.error("no schema.org events found; check the fixtures URL or page format")
    try:
        calendar = make_calendar(events)
    except EventSourceError as exc:
        parser.error(str(exc))
    count = calendar.count("BEGIN:VEVENT")
    if not count:
        parser.error("no usable SportsEvent entries with a name and startDate were found")
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
