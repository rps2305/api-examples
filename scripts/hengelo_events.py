#!/usr/bin/env python3
"""Scrape public events from the Uit in Hengelo agenda."""

from __future__ import annotations

import json
import re
from datetime import date, datetime, time, timedelta
from html import unescape
from html.parser import HTMLParser
from zoneinfo import ZoneInfo

from event_sources import load_text

URL = "https://uitinhengelo.nl/agenda"
TIMEZONE = ZoneInfo("Europe/Amsterdam")
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
    return re.sub(r"\s+", " ", unescape(value)).strip(" ,")


class AgendaParser(HTMLParser):
    """Collect event cards without depending on whitespace or attribute order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.events: list[dict[str, object]] = []
        self._event: dict[str, object] | None = None
        self._depth = 0
        self._detail_depth: int | None = None
        self._detail_parts: list[str] = []
        self._capture: str | None = None
        self._capture_tag: str | None = None
        self._capture_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        classes = set(attributes.get("class", "").split())
        if (
            self._event is None
            and tag == "div"
            and "event" in classes
            and attributes.get("href")
        ):
            self._event = {
                "url": attributes["href"],
                "categories": [],
            }
            self._depth = 1
            return
        if self._event is None:
            return
        if tag == "div":
            self._depth += 1
            if "eventDetail" in classes:
                self._detail_depth = self._depth
                self._detail_parts = []
        if tag == "h5":
            self._start_capture("name", tag)
        elif tag == "span" and "eventCat" in classes:
            self._start_capture("category", tag)
        elif tag == "span" and "date" in classes:
            self._start_capture("date", tag)

    def _start_capture(self, field: str, tag: str) -> None:
        self._capture = field
        self._capture_tag = tag
        self._capture_parts = []

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._capture_parts.append(data)
        if self._detail_depth is not None:
            self._detail_parts.append(f" {data}")

    def handle_endtag(self, tag: str) -> None:
        if self._event is None:
            return
        if self._capture is not None and tag == self._capture_tag:
            value = clean("".join(self._capture_parts))
            if self._capture == "category" and value:
                categories = self._event["categories"]
                assert isinstance(categories, list)
                categories.append(value)
            elif value:
                self._event[self._capture] = value
            self._capture = None
            self._capture_tag = None
            self._capture_parts = []
        if tag != "div":
            return
        if self._detail_depth == self._depth:
            self._event["details"] = clean("".join(self._detail_parts))
            self._detail_depth = None
            self._detail_parts = []
        self._depth -= 1
        if self._depth == 0:
            self.events.append(self._event)
            self._event = None


def dated(day: int, month: int, today: date) -> date:
    year = today.year + ((month, day) < (today.month, today.day))
    return date(year, month, day)


def date_range(value: str, today: date) -> tuple[date, date | None] | None:
    label = clean(value).lower()
    if label == "vandaag":
        return today, None
    if label == "morgen":
        return today + timedelta(days=1), None
    matches = re.findall(r"(\d{1,2})\s+([a-z]{3})", label)
    if not matches:
        return None
    if label.startswith("t/m"):
        start = today
        end_day, end_month = matches[0]
        end = dated(int(end_day), MONTHS[end_month], today)
        return start, end
    start_day, start_month = matches[0]
    if start_month not in MONTHS:
        return None
    start = dated(int(start_day), MONTHS[start_month], today)
    if len(matches) == 1:
        return start, None
    end_day, end_month = matches[-1]
    if end_month not in MONTHS:
        return start, None
    end_year = start.year + (MONTHS[end_month] < start.month)
    return start, date(end_year, MONTHS[end_month], int(end_day))


def local_datetime(day: date, clock: str) -> str:
    hour, minute = (int(part) for part in clock.split(":"))
    return datetime.combine(day, time(hour, minute), TIMEZONE).isoformat()


def scrape_events(html: str, now: datetime | None = None) -> list[dict[str, object]]:
    now = now or datetime.now(TIMEZONE)
    parser = AgendaParser()
    parser.feed(html)
    events: list[dict[str, object]] = []
    for card in parser.events:
        dates = date_range(str(card.get("date", "")), now.date())
        if not dates or not card.get("name"):
            continue
        start_day, end_day = dates
        clocks = re.findall(r"\b\d{1,2}:\d{2}\b", str(card.get("details", "")))
        start = local_datetime(start_day, clocks[0]) if clocks else start_day.isoformat()
        categories = card.get("categories")
        event: dict[str, object] = {
            "@type": "Event",
            "name": str(card["name"]),
            "startDate": start,
            "location": "",
            "genre": ", ".join(categories) if isinstance(categories, list) and categories else "Evenement",
            "url": str(card["url"]),
        }
        if end_day is not None:
            event["endDate"] = (
                local_datetime(end_day, clocks[1]) if len(clocks) > 1 else end_day.isoformat()
            )
        events.append(event)
    return events


if __name__ == "__main__":
    print(json.dumps(scrape_events(load_text(URL)), ensure_ascii=False))
