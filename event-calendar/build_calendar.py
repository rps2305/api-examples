#!/usr/bin/env python3
"""Build a browser-ready event feed from all local event scrapers."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUTPUT = Path(__file__).with_name("events.json")
ICAL = Path(__file__).with_name("events.ics")
INDEX = Path(__file__).with_name("index.html")
sys.path.insert(0, str(SCRIPTS))

from event_sources import load_text  # noqa: E402
from fc_twente_ical import DEFAULT_URL as FC_TWENTE_URL  # noqa: E402
from fc_twente_ical import escape, fold, ical_datetime, scrape_matches  # noqa: E402


def run(script: str) -> list[dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)], capture_output=True, check=True, text=True
    )
    return json.loads(result.stdout)


def future_events(
    events: list[dict[str, object]], now: datetime | None = None
) -> list[dict[str, object]]:
    """Keep only events that have not started yet, interpreted in Dutch local time."""
    now = now or datetime.now(ZoneInfo("Europe/Amsterdam"))
    result: list[dict[str, object]] = []
    for event in events:
        start = datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        if start.astimezone(now.tzinfo) >= now:
            result.append(event)
    return result


def calendar(events: list[dict[str, object]]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Uit Vandaag Twente//NL",
        "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:Uit Vandaag — Twente",
    ]
    for event in events:
        name, start = str(event["name"]), event["startDate"]
        uid = hashlib.sha256(f"{name}-{start}".encode()).hexdigest()[:24]
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}@event-calendar.puntuale.nl",
                f"DTSTART{ical_datetime(start)}",
                f"SUMMARY:{escape(name)}",
            ]
        )
        if event.get("location"):
            lines.append(f"LOCATION:{escape(event['location'])}")
        if event.get("url"):
            lines.append(f"URL:{event['url']}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(item for line in lines for item in fold(line)) + "\r\n"


def main() -> None:
    sources = (
        ("decactus_events.py", "de-cactus"),
        ("metropool_events.py", "metropool"),
        ("oogst_events.py", "oogst"),
        ("hengelo_events.py", "hengelo"),
    )
    events: list[dict[str, object]] = []
    for event in scrape_matches(load_text(FC_TWENTE_URL)):
        event["source"] = "fc-twente"
        events.append(event)
    for script, source in sources:
        for event in run(script):
            event["source"] = source
            events.append(event)
    events = future_events(events)
    events.sort(key=lambda event: str(event["startDate"]))
    # Prevent scraped text from terminating the embedded JSON script element.
    payload = json.dumps(events, ensure_ascii=False).replace("</", "<\\/")
    OUTPUT.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    ICAL.write_text(calendar(events), encoding="utf-8", newline="")
    index = INDEX.read_text(encoding="utf-8")
    start = index.index('<script id="event-data" type="application/json">')
    end = index.index("</script>", start) + len("</script>")
    embedded = f'<script id="event-data" type="application/json">{payload}</script>'
    INDEX.write_text(index[:start] + embedded + index[end:], encoding="utf-8")
    print(f"Wrote {len(events)} events to {OUTPUT} and embedded them in {INDEX}")


if __name__ == "__main__":
    main()
