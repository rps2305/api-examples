#!/usr/bin/env python3
"""Serve the static agenda and expose an authenticated delivery webhook."""

from __future__ import annotations

import hmac
import ipaddress
import json
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from datetime import datetime
from email.headerregistry import Address
from email.errors import HeaderParseError
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import build_calendar
import personal_digest

CALENDAR_DIR = Path(__file__).resolve().parent
SEND_PATH = "/webhook/send"
SUGGESTION_PATH = "/api/suggestions"
SUGGESTION_TOKEN_PATH = "/api/suggestions/token"
BUILD_LOCK = threading.Lock()
SCHEDULE_TIMEZONE = ZoneInfo("Europe/Amsterdam")
FORM_SECRET = secrets.token_bytes(32)
FORM_TOKEN_MAX_AGE = 2 * 60 * 60
FORM_TOKEN_MIN_AGE = 3
MAX_REQUEST_SIZE = 8_192
RATE_LIMIT_WINDOW = 60 * 60
RATE_LIMIT_COUNT = 3
RATE_LIMIT_COOLDOWN = 60
CALENDAR_REFRESH_INTERVAL = 6 * 60 * 60
RATE_LOCK = threading.Lock()
RATE_HISTORY: dict[str, deque[float]] = defaultdict(deque)
USED_TOKENS: dict[str, float] = {}
SUGGESTION_CATEGORIES = {"Evenement", "Correctie", "Website", "Anders"}
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; "
        "form-action 'self'; script-src 'self' https://matomo.puntuale.nl; script-src-attr 'none'; style-src 'self'; "
        "style-src-attr 'none'; img-src 'self' data: https://matomo.puntuale.nl; font-src 'self'; "
        "connect-src 'self' https://matomo.puntuale.nl; "
        "manifest-src 'self'; worker-src 'self'; frame-src 'none'; upgrade-insecure-requests"
    ),
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}


def authorized(header: str | None) -> bool:
    """Return whether an Authorization bearer token matches the configured secret."""
    token = os.environ.get("EVENT_CALENDAR_WEBHOOK_TOKEN")
    if not token or not header or not header.startswith("Bearer "):
        return False
    return hmac.compare_digest(header.removeprefix("Bearer "), token)


def build_and_send() -> int:
    """Refresh all sources, then send the current two-month digest once."""
    with BUILD_LOCK:
        build_calendar.main()
        events = personal_digest.upcoming_events()
        logo_cid = personal_digest.make_msgid()[1:-1]
        personal_digest.send_email(personal_digest.html_digest(events, logo_cid), logo_cid)
    return len(events)


def create_form_token(now: float | None = None) -> str:
    """Create a short-lived signed token without storing browser state."""
    issued = int(now if now is not None else time.time())
    payload = f"{issued}.{secrets.token_urlsafe(18)}"
    signature = hmac.digest(FORM_SECRET, payload.encode(), "sha256").hex()
    return f"{payload}.{signature}"


def valid_form_token(token: object, now: float | None = None) -> bool:
    """Accept an unused, correctly signed token only after a human-sized delay."""
    if not isinstance(token, str) or len(token) > 160:
        return False
    try:
        issued_text, nonce, supplied = token.split(".", 2)
        issued = int(issued_text)
    except (TypeError, ValueError):
        return False
    payload = f"{issued}.{nonce}"
    expected = hmac.digest(FORM_SECRET, payload.encode(), "sha256").hex()
    current = now if now is not None else time.time()
    age = current - issued
    if not hmac.compare_digest(supplied, expected):
        return False
    if age < FORM_TOKEN_MIN_AGE or age > FORM_TOKEN_MAX_AGE:
        return False
    with RATE_LOCK:
        expired = [used for used, used_at in USED_TOKENS.items() if current - used_at > FORM_TOKEN_MAX_AGE]
        for used in expired:
            USED_TOKENS.pop(used, None)
        if token in USED_TOKENS:
            return False
        USED_TOKENS[token] = current
    return True


def within_rate_limit(client: str, now: float | None = None) -> bool:
    """Reserve one submission slot for a client address."""
    current = now if now is not None else time.time()
    with RATE_LOCK:
        history = RATE_HISTORY[client]
        while history and current - history[0] > RATE_LIMIT_WINDOW:
            history.popleft()
        if history and current - history[-1] < RATE_LIMIT_COOLDOWN:
            return False
        if len(history) >= RATE_LIMIT_COUNT:
            return False
        history.append(current)
    return True


def valid_email(value: object) -> str:
    """Return a normalized optional address or raise ValueError."""
    if value in (None, ""):
        return ""
    if not isinstance(value, str) or len(value) > 254 or "\r" in value or "\n" in value:
        raise ValueError("invalid email")
    try:
        parsed = Address(addr_spec=value.strip())
    except (HeaderParseError, ValueError):
        raise ValueError("invalid email") from None
    if not parsed.username or "." not in parsed.domain:
        raise ValueError("invalid email")
    return parsed.addr_spec


def validate_suggestion(data: object) -> tuple[str, str, str, str, str]:
    """Validate and normalize the public form's bounded fields."""
    if not isinstance(data, dict):
        raise ValueError("invalid payload")
    website = data.get("website", "")
    if not isinstance(website, str):
        raise ValueError("invalid payload")
    name = data.get("name", "")
    message = data.get("message", "")
    category = data.get("category", "")
    if not isinstance(name, str) or len(name.strip()) > 80:
        raise ValueError("invalid name")
    if not isinstance(message, str) or not 20 <= len(message.strip()) <= 2_000:
        raise ValueError("invalid message")
    if category not in SUGGESTION_CATEGORIES:
        raise ValueError("invalid category")
    email = valid_email(data.get("email", ""))
    return name.strip(), email, category, message.strip(), website.strip()


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


def calendar_refresh_loop() -> None:
    """Refresh all agenda sources every six hours, preserving the last good build on failure."""
    while True:
        time.sleep(CALENDAR_REFRESH_INTERVAL)
        try:
            with BUILD_LOCK:
                build_calendar.main()
            print("Agenda automatisch ververst.")
        except Exception as exc:
            print(f"Automatisch verversen mislukt; laatste goede agenda blijft staan: {exc}")


class CalendarHandler(SimpleHTTPRequestHandler):
    """Static files plus a single token-protected POST endpoint."""

    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webp": "image/webp",
        ".woff2": "font/woff2",
        ".ics": "text/calendar; charset=utf-8",
    }

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(CALENDAR_DIR), **kwargs)

    def end_headers(self) -> None:
        """Cache fingerprinted static resources while keeping generated pages fresh."""
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)
        request = urlparse(self.path)
        if request.path == "/events.ics":
            self.send_header("Content-Disposition", 'attachment; filename="uit-vandaag-twente.ics"')
        etag = self.static_etag(request.path)
        if etag:
            self.send_header("ETag", etag)
        if request.path.startswith("/assets/") or request.query:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif request.path == "/events.ics":
            self.send_header("Cache-Control", "public, max-age=300, must-revalidate")
        elif request.path.endswith((".html", "/")) or request.path == "/":
            self.send_header("Cache-Control", "public, max-age=300, stale-while-revalidate=3600")
        else:
            self.send_header("Cache-Control", "public, max-age=300, stale-while-revalidate=3600")
        super().end_headers()

    def static_etag(self, request_path: str) -> str | None:
        """Make static file validators stable until their contents change."""
        path = Path(self.translate_path(request_path))
        if path.is_dir():
            path /= "index.html"
        try:
            stat = path.stat()
        except OSError:
            return None
        return f'"{stat.st_mtime_ns:x}-{stat.st_size:x}"' if path.is_file() else None

    def static_not_modified(self) -> bool:
        """Honor an ETag validator before SimpleHTTPRequestHandler writes a body."""
        etag = self.static_etag(urlparse(self.path).path)
        return bool(etag and self.headers.get("If-None-Match") == etag)

    def send_header(self, keyword: str, value: str) -> None:
        """Declare UTF-8 for HTML documents, including custom error pages."""
        if keyword.lower() == "content-type" and value.lower().startswith("text/html") and "charset=" not in value.lower():
            value = f"{value}; charset=utf-8"
        super().send_header(keyword, value)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        """Return a helpful, branded page for missing public URLs."""
        if code != HTTPStatus.NOT_FOUND:
            super().send_error(code, message, explain)
            return
        body = """<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagina niet gevonden – Uit Vandaag Twente</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="/styles.css"></head><body><a class="skip-link" href="#main-content">Ga naar inhoud</a>
<header class="legal-header"><div><p class="eyebrow">FOUT 404</p><h1>Deze pagina bestaat niet.</h1></div>
<div class="legal-actions"><a href="/">← Terug naar de agenda</a></div></header>
<main id="main-content" class="legal-main" tabindex="-1"><h2>Even terug naar de agenda</h2>
<p>De link is mogelijk verouderd of verkeerd overgenomen. In de agenda vind je alle actuele plannen, filters en bronnen.</p>
<p><a class="taste-cta" href="/">Bekijk de agenda →</a></p></main></body></html>"""
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def json_response(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path == SUGGESTION_TOKEN_PATH:
            self.json_response(HTTPStatus.OK, {"token": create_form_token()})
            return
        if self.static_not_modified():
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.end_headers()
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        if self.static_not_modified():
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.end_headers()
            return
        super().do_HEAD()

    def client_identifier(self) -> str:
        """Use proxy forwarding only when the direct peer is local and trusted."""
        peer = ipaddress.ip_address(self.client_address[0])
        # Nginx overwrites X-Real-IP, while X-Forwarded-For can contain client input.
        forwarded = self.headers.get("X-Real-IP", "").strip()
        if peer.is_loopback and forwarded:
            try:
                return str(ipaddress.ip_address(forwarded))
            except ValueError:
                pass
        return str(peer)

    def handle_suggestion(self) -> None:
        expected_origin = os.environ.get("EVENT_CALENDAR_PUBLIC_ORIGIN", "https://event-calendar.puntuale.nl")
        if self.headers.get("Origin") != expected_origin:
            self.json_response(HTTPStatus.FORBIDDEN, {"error": "Ongeldige aanvraag."})
            return
        if self.headers.get_content_type() != "application/json":
            self.json_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ongeldig formulier."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_REQUEST_SIZE:
            self.json_response(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Ongeldig formulier."})
            return
        try:
            data = json.loads(self.rfile.read(length))
            name, email, category, message, website = validate_suggestion(data)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.json_response(HTTPStatus.BAD_REQUEST, {"error": "Controleer de ingevulde velden."})
            return
        # Bots commonly fill fields hidden from people. Return success without sending.
        if website:
            self.json_response(HTTPStatus.ACCEPTED, {"sent": True})
            return
        if not valid_form_token(data.get("token")):
            self.json_response(HTTPStatus.BAD_REQUEST, {"error": "Ververs de pagina en probeer opnieuw."})
            return
        if not within_rate_limit(self.client_identifier()):
            self.json_response(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Probeer het later opnieuw."})
            return
        try:
            personal_digest.send_suggestion(name, email, category, message)
        except Exception:
            self.log_error("Could not send a website suggestion")
            self.json_response(HTTPStatus.BAD_GATEWAY, {"error": "Versturen lukt nu niet. Probeer het later opnieuw."})
            return
        self.json_response(HTTPStatus.CREATED, {"sent": True})

    def do_POST(self) -> None:  # noqa: N802
        request_path = urlparse(self.path).path
        if request_path == SUGGESTION_PATH:
            self.handle_suggestion()
            return
        if request_path != SEND_PATH:
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
        threading.Thread(target=calendar_refresh_loop, name="calendar-refresh", daemon=True).start()
    server = ThreadingHTTPServer(("0.0.0.0", port), CalendarHandler)
    print(f"Agenda beschikbaar op http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
