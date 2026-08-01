#!/usr/bin/env python3
"""Get events from the De Cactus agenda page."""

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

from event_sources import EventSourceError, json_ld_events, load_text, normalize_datetime, print_events

DEFAULT_URL = "https://www.decactus.nl/"
STAGER_BASE_URL = "https://decactus.stager.co"
STAGER_SHOP_ID = 2290


def event_from_stager(item: dict[str, object]) -> dict[str, object]:
    """Normalize a Stager shop event, including its explicit availability status."""
    event_id = item["eventId"]
    return {
        "@type": "Event",
        "name": str(item["name"]).strip(),
        # Stager serializes these venue wall-clock fields with a Z suffix.
        # Attach the venue timezone before converting them to a real UTC instant.
        "startDate": normalize_datetime(item["startsOn"], floating_local=True),
        "endDate": normalize_datetime(item["endsOn"], floating_local=True),
        "location": "De Cactus, Hengelo",
        "url": f"{STAGER_BASE_URL}/shop/default/events/{event_id}",
        "ticketUrl": f"{STAGER_BASE_URL}/shop/default/events/{event_id}",
        "soldOut": item.get("soldOut") is True,
    }


def stager_events() -> list[dict[str, object]]:
    """Get every event from the Stager shop embedded on De Cactus' agenda."""
    session_request = Request(
        f"{STAGER_BASE_URL}/shop/v1/session/new",
        data=json.dumps({"shopId": STAGER_SHOP_ID, "locale": "NL"}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(session_request, timeout=30) as response:
        token = json.load(response)["accessToken"]["jwt"]

    events: list[dict[str, object]] = []
    offset = 0
    while True:
        request = Request(
            f"{STAGER_BASE_URL}/shop/v1/events?offset={offset}&limit=10",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urlopen(request, timeout=30) as response:
            page = json.load(response)
        if not page:
            return events
        for item in page:
            events.append(event_from_stager(item))
        offset += len(page)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="De Cactus agenda URL")
    parser.add_argument("--input", type=Path, help="parse a previously downloaded HTML file")
    args = parser.parse_args()
    try:
        events = json_ld_events(load_text(args.url, args.input)) if args.input else stager_events()
    except EventSourceError as exc:
        parser.error(str(exc))
    if not events:
        parser.error("no schema.org events found; check the agenda URL or page format")
    print_events(events)


if __name__ == "__main__":
    main()
