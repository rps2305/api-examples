#!/usr/bin/env python3
"""Serve the static agenda and expose an authenticated delivery webhook."""

from __future__ import annotations

import hmac
import json
import os
import threading
import time
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import build_calendar
import personal_digest

CALENDAR_DIR = Path(__file__).resolve().parent
SEND_PATH = "/webhook/send"
BUILD_LOCK = threading.Lock()
SCHEDULE_TIMEZONE = ZoneInfo("Europe/Amsterdam")


def authorized(header: str | None) -> bool:
    """Return whether an Authorization bearer token matches the configured secret."""
    token = os.environ.get("EVENT_CALENDAR_WEBHOOK_TOKEN")
    if not token or not header or not header.startswith("Bearer "):
        return False
    return hmac.compare_digest(header.removeprefix("Bearer "), token)


def build_and_send() -> int:
    """Refresh all sources, then send the current seven-day digest once."""
    with BUILD_LOCK:
        build_calendar.main()
        events = personal_digest.upcoming_events()
        personal_digest.send_email(personal_digest.html_digest(events))
    return len(events)


def weekly_digest_loop() -> None:
    """Send once per ISO week when it is Monday in the configured 07:00 hour."""
    sent_week: tuple[int, int] | None = None
    while True:
        now = datetime.now(SCHEDULE_TIMEZONE)
        year, week, _ = now.isocalendar()
        if now.weekday() == 0 and now.hour == 7 and sent_week != (year, week):
            try:
                count = build_and_send()
                print(f"Wekelijkse digest verstuurd met {count} evenementen.")
                sent_week = (year, week)
            except Exception as exc:
                print(f"Wekelijkse digest mislukt: {exc}")
        time.sleep(30)


class CalendarHandler(SimpleHTTPRequestHandler):
    """Static files plus a single token-protected POST endpoint."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(CALENDAR_DIR), **kwargs)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != SEND_PATH:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not authorized(self.headers.get("Authorization")):
            self.send_error(HTTPStatus.UNAUTHORIZED)
            return
        try:
            count = build_and_send()
        except Exception:  # Do not expose SMTP or scraper details to webhook callers.
            self.log_error("Could not build and send the digest")
            self.send_error(HTTPStatus.BAD_GATEWAY, "De digest kon niet worden verstuurd.")
            return
        body = json.dumps({"sent": True, "events": count}).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    try:
        build_calendar.main()
    except Exception as exc:
        # Preserve the previously baked event feed when an upstream site is unavailable.
        print(f"Initial agenda update failed: {exc}")
    if os.environ.get("EVENT_CALENDAR_SCHEDULE_ENABLED", "true").lower() == "true":
        threading.Thread(target=weekly_digest_loop, name="weekly-digest", daemon=True).start()
    server = ThreadingHTTPServer(("0.0.0.0", port), CalendarHandler)
    print(f"Agenda beschikbaar op http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
