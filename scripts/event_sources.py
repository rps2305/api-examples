#!/usr/bin/env python3
"""Shared helpers for the Dutch event examples (standard library only)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

JSON_LD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


class EventSourceError(RuntimeError):
    """A concise, user-facing error raised when an event source cannot be read."""


def get_json(url: str, headers: dict[str, str] | None = None) -> object:
    request = Request(url, headers={"User-Agent": "api-examples/1.0", **(headers or {})})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def get_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 api-examples/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode(response.headers.get_content_charset() or "utf-8")
    except HTTPError as exc:
        raise EventSourceError(f"{url} returned HTTP {exc.code}") from None
    except URLError as exc:
        raise EventSourceError(f"could not retrieve {url}: {exc.reason}") from None


def load_text(url: str, input_file: Path | None = None) -> str:
    """Read a downloaded page when supplied, otherwise retrieve its URL."""
    if input_file is not None:
        try:
            return input_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise EventSourceError(f"could not read {input_file}: {exc.strerror}") from None
    return get_text(url)


def json_ld_events(html: str) -> list[dict[str, object]]:
    """Return schema.org Event objects embedded in a page, including @graph/list forms."""
    events: list[dict[str, object]] = []

    def visit(value: object) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            kind = value.get("@type")
            kinds = kind if isinstance(kind, list) else [kind]
            if any(isinstance(item, str) and item.endswith("Event") for item in kinds):
                events.append(value)
            for key in ("@graph", "itemListElement"):
                if key in value:
                    visit(value[key])
            if "item" in value:
                visit(value["item"])

    for raw in JSON_LD_RE.findall(html):
        try:
            visit(json.loads(unescape(raw).strip()))
        except json.JSONDecodeError:
            continue
    return events


def print_events(events: list[dict[str, object]]) -> None:
    print(json.dumps(events, ensure_ascii=False, indent=2))


def ical_datetime(value: object) -> str:
    """Convert a schema.org ISO date/time to an iCalendar UTC or all-day value."""
    raw = str(value)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return f";VALUE=DATE:{raw.replace('-', '')}"
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return f":{parsed.strftime('%Y%m%dT%H%M%S')}"
    return f":{parsed.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
