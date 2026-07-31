#!/usr/bin/env python3
"""Get events published on the De Cactus agenda as schema.org JSON."""

import argparse
from pathlib import Path

from event_sources import EventSourceError, json_ld_events, load_text, print_events

DEFAULT_URL = "https://www.decactus.nl/agenda/"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="De Cactus agenda URL")
    parser.add_argument("--input", type=Path, help="parse a previously downloaded HTML file")
    args = parser.parse_args()
    try:
        events = json_ld_events(load_text(args.url, args.input))
    except EventSourceError as exc:
        parser.error(str(exc))
    if not events:
        parser.error("no schema.org events found; check the agenda URL or page format")
    print_events(events)


if __name__ == "__main__":
    main()
