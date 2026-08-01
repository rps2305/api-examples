#!/usr/bin/env python3
"""Build a browser-ready event feed from all local event scrapers."""

from __future__ import annotations

import hashlib
import html as html_module
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUTPUT = Path(__file__).with_name("events.json")
ICAL = Path(__file__).with_name("events.ics")
INDEX = Path(__file__).with_name("index.html")
DISCLAIMER = Path(__file__).with_name("disclaimer.html")
sys.path.insert(0, str(SCRIPTS))

from event_sources import load_text, normalize_event_times  # noqa: E402
from fc_twente_ical import DEFAULT_URL as FC_TWENTE_URL  # noqa: E402
from fc_twente_ical import escape, fold, ical_datetime, scrape_matches  # noqa: E402
from taste_profile import taste_recommendation  # noqa: E402


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
        raw_start = str(event["startDate"])
        if len(raw_start) == 10:
            if date.fromisoformat(raw_start) >= now.date():
                result.append(event)
            continue
        start = datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        if start.astimezone(now.tzinfo) >= now:
            result.append(event)
    return result


def deduplicate_events(events: list[dict[str, object]]) -> list[dict[str, object]]:
    """Recognize duplicates by normalized name, start, and—when known—place."""
    seen_exact: set[tuple[str, str]] = set()
    seen_at_place: set[tuple[str, str, str]] = set()
    result: list[dict[str, object]] = []
    for event in events:
        name = re.sub(r"[^a-z0-9]+", " ", str(event["name"]).casefold()).strip()
        start = str(event["startDate"])
        location = re.sub(r"[^a-z0-9]+", " ", str(event.get("location") or "").casefold()).strip()
        exact_identity = name, start
        place_identity = name, local_date_key(start), location
        if exact_identity in seen_exact or (location and place_identity in seen_at_place):
            continue
        seen_exact.add(exact_identity)
        if location:
            seen_at_place.add(place_identity)
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


def json_for_script(value: object) -> str:
    """Serialize JSON without characters that can escape an HTML script data block."""
    return json.dumps(value, ensure_ascii=False).translate(
        {
            ord("<"): "\\u003c",
            ord(">"): "\\u003e",
            ord("&"): "\\u0026",
            0x2028: "\\u2028",
            0x2029: "\\u2029",
        }
    )


WEEKDAYS = ("maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag")
MONTHS = ("januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december")
SOURCE_PRIORITY = {"metropool": 0, "de-cactus": 1, "fc-twente": 2, "oogst": 3}


def safe_external_url(value: object) -> str:
    """Return only absolute HTTP(S) URLs collected from external sources."""
    candidate = str(value or "").strip()
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return ""
    return candidate if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def venue_label(event: dict[str, object]) -> str:
    source = event.get("source")
    if source == "feestdagen":
        return "🇳🇱 Feestdag"
    if source == "fc-twente":
        return "⚽ FC Twente"
    if source == "de-cactus":
        return "🌵 DE CACTUS"
    if source == "oogst":
        return "🌾 Oogst"
    if source == "hengelo":
        return "🏛️ Hengelo"
    location = str(event.get("location") or "").strip()
    return f"🎵 Metropool {location}".strip()


def event_time(event: dict[str, object]) -> str:
    start = str(event["startDate"])
    if event.get("source") == "feestdagen":
        return "Hele dag"
    if len(start) == 10:
        return "Tijd volgt"
    parsed = datetime.fromisoformat(start.replace("Z", "+00:00"))
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(ZoneInfo("Europe/Amsterdam"))
    return f"{parsed.hour:02d}:{parsed.minute:02d}"


def local_date_key(value: object) -> str:
    """Return the calendar date at the event location, not the UTC date."""
    raw = str(value)
    if len(raw) == 10:
        return raw
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
    return parsed.astimezone(ZoneInfo("Europe/Amsterdam")).date().isoformat()


def prerender_event(event: dict[str, object]) -> str:
    """Render scraped fields as escaped text so initial HTML is safe and crawlable."""
    source = str(event.get("source") or "hengelo")
    source_class = source if source in {"metropool", "de-cactus", "fc-twente", "oogst", "hengelo", "feestdagen"} else "hengelo"
    classes = f"event {source_class}{' fc-home' if event.get('isHome') is True else ''}"
    name = html_module.escape(str(event.get("name") or "Onbekend evenement"))
    location_raw = str(event.get("location") or "").strip()
    genre_raw = str(event.get("genre") or "").strip()
    if source == "feestdagen":
        kind = "🇳🇱 Nationale feestdag"
    elif source == "fc-twente":
        kind = "⚽ Voetbal"
    else:
        kind = f"🎵 {genre_raw}" if genre_raw else "🎤 Live"
    meta = kind + (f" · 📍 {location_raw}" if location_raw else "")
    badges = ""
    if event.get("recommended") is True or event.get("soldOut") is True:
        parts: list[str] = []
        if event.get("recommended") is True:
            reason = html_module.escape(str(event.get("tasteReason") or "Past bij Ronalds muzieksmaak"), quote=True)
            parts.append(f'<span class="taste-badge" title="{reason}">★ Voor jou</span>')
        if event.get("soldOut") is True:
            parts.append('<span class="sold-out-badge">Uitverkocht</span>')
        badges = f'<p class="event-badges">{"".join(parts)}</p>'
    info_url = safe_external_url(event.get("url"))
    ticket_url = safe_external_url(event.get("ticketUrl"))
    links: list[str] = []
    if info_url:
        label = "Wedstrijd" if source == "fc-twente" else "Rijksoverheid" if source == "feestdagen" else "Info"
        links.append(f'<a href="{html_module.escape(info_url, quote=True)}" target="_blank" rel="noopener noreferrer">{label} ↗</a>')
    if ticket_url and ticket_url != info_url:
        links.append(f'<a class="tickets" href="{html_module.escape(ticket_url, quote=True)}" target="_blank" rel="noopener noreferrer">Tickets ↗</a>')
    serialized_event = {**event, "url": info_url, "ticketUrl": ticket_url}
    event_json = html_module.escape(json.dumps(serialized_event, ensure_ascii=False, separators=(",", ":")), quote=True)
    aria_name = html_module.escape(str(event.get("name") or "dit evenement"), quote=True)
    links.append(f'<button class="event-calendar-button" type="button" data-event-calendar="{event_json}" aria-label="Voeg {aria_name} toe aan agenda" title="Voeg toe aan agenda">🗓</button>')
    return (
        f'<article class="{classes}"><p class="event-time">{html_module.escape(event_time(event))}</p>'
        f'<p class="venue">{html_module.escape(venue_label(event))}</p>{badges}<h3>{name}</h3>'
        f'<p class="meta">{html_module.escape(meta)}</p><p class="event-links">{"".join(links)}</p></article>'
    )


def prerender_agenda(events: list[dict[str, object]]) -> str:
    """Build the complete semantic agenda used before JavaScript enhancement."""
    groups: dict[str, list[dict[str, object]]] = {}
    for event in events:
        groups.setdefault(local_date_key(event["startDate"]), []).append(event)
    sections: list[str] = []
    for day_key, items in groups.items():
        current = date.fromisoformat(day_key)
        label = f"{WEEKDAYS[current.weekday()]} {current.day} {MONTHS[current.month - 1]}"
        items.sort(key=lambda event: (SOURCE_PRIORITY.get(str(event.get("source")), 10), str(event["startDate"]), str(event.get("name", "")).casefold()))
        count = len(items)
        sections.append(
            f'<section class="day"><div class="day-heading"><h2><time datetime="{day_key}">{label}</time></h2>'
            f'<span>{count} {"plan" if count == 1 else "plannen"}</span></div>'
            f'<div class="day-events">{"".join(prerender_event(event) for event in items)}</div></section>'
        )
    return "".join(sections) or '<p class="empty">Er staan momenteel geen plannen in de agenda.</p>'


def event_item_list(events: list[dict[str, object]]) -> dict[str, object]:
    """Describe the listing with Schema.org without claiming single-event rich results."""
    listed = [event for event in events if event.get("source") != "feestdagen" and "besloten" not in str(event.get("name", "")).casefold()]
    elements: list[dict[str, object]] = []
    for position, event in enumerate(listed, 1):
        item: dict[str, object] = {
            "@type": "SportsEvent" if event.get("source") == "fc-twente" else "Event",
            "@id": f"https://event-calendar.puntuale.nl/#event-{hashlib.sha256(f'{event.get("name")}-{event.get("startDate")}'.encode()).hexdigest()[:16]}",
            "name": str(event.get("name") or "Onbekend evenement"),
            "startDate": str(event["startDate"]),
            "eventStatus": "https://schema.org/EventScheduled",
        }
        url = safe_external_url(event.get("url"))
        ticket_url = safe_external_url(event.get("ticketUrl"))
        if url:
            item["url"] = url
        location = str(event.get("location") or "").strip()
        if event.get("source") == "fc-twente" and event.get("isHome") is True:
            location = "De Grolsch Veste, Enschede"
        if location:
            item["location"] = {"@type": "Place", "name": location}
        genre = str(event.get("genre") or "").strip()
        if genre:
            item["description"] = genre
        if ticket_url:
            item["offers"] = {
                "@type": "Offer",
                "url": ticket_url,
                "availability": "https://schema.org/SoldOut" if event.get("soldOut") is True else "https://schema.org/InStock",
            }
        elements.append({"@type": "ListItem", "position": position, "item": item})
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Uitagenda Twente: Concerten & FC Twente",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }


def replace_between(document: str, start_marker: str, end_marker: str, content: str) -> str:
    start = document.index(start_marker) + len(start_marker)
    end = document.index(end_marker, start)
    return document[:start] + content + document[end:]


def agenda_summary(events: list[dict[str, object]], processed_at: datetime) -> str:
    """Return the current day and rolling seven-day counts for the hero."""
    today = processed_at.astimezone(ZoneInfo("Europe/Amsterdam")).date()
    week_end = today + timedelta(days=7)
    dates = [date.fromisoformat(local_date_key(event["startDate"])) for event in events]
    today_count = sum(event_date == today for event_date in dates)
    week_count = sum(today <= event_date < week_end for event_date in dates)
    noun = "evenement" if today_count == 1 else "evenementen"
    return (
        '<p id="agenda-summary" class="agenda-summary" '
        'title="Deze week betekent de komende zeven dagen" aria-live="polite">'
        f"Vandaag {today_count} {noun}, deze week {week_count}.</p>"
    )


def refresh_label(processed_at: datetime) -> str:
    """Format a successful processing timestamp in Dutch local time."""
    local = processed_at.astimezone(ZoneInfo("Europe/Amsterdam"))
    return (
        f"{WEEKDAYS[local.weekday()]} {local.day} {MONTHS[local.month - 1]} "
        f"{local.year} om {local:%H:%M}"
    )


def update_index(events: list[dict[str, object]], processed_at: datetime) -> None:
    """Embed data, structured data and prerendered HTML in one deterministic build step."""
    index = INDEX.read_text(encoding="utf-8")
    script_start = index.index('<script id="event-data" type="application/json">')
    script_end = index.index("</script>", script_start) + len("</script>")
    embedded = f'<script id="event-data" type="application/json">{json_for_script(events)}</script>'
    index = index[:script_start] + embedded + index[script_end:]
    schema = f'<script id="event-schema" type="application/ld+json">{json_for_script(event_item_list(events))}</script>'
    index = replace_between(index, "<!-- EVENT_SCHEMA_START -->", "<!-- EVENT_SCHEMA_END -->", schema)
    index = replace_between(index, "<!-- EVENT_LIST_START -->", "<!-- EVENT_LIST_END -->", prerender_agenda(events))
    index = replace_between(index, "<!-- HERO_SUMMARY_START -->", "<!-- HERO_SUMMARY_END -->", agenda_summary(events, processed_at))
    INDEX.write_text(index, encoding="utf-8")


def update_disclaimer(processed_at: datetime) -> None:
    """Publish the timestamp of the most recent all-source success."""
    document = DISCLAIMER.read_text(encoding="utf-8")
    label = html_module.escape(refresh_label(processed_at))
    homepage_status = f'<span class="refresh-status">Laatste succesvolle verwerking: {label}.</span>'
    disclaimer_status = f'<span class="refresh-status">Laatste succesvolle verwerking van alle bronnen: {label}.</span>'
    document = replace_between(document, "<!-- DISCLAIMER_REFRESH_START -->", "<!-- DISCLAIMER_REFRESH_END -->", disclaimer_status)
    DISCLAIMER.write_text(document, encoding="utf-8")

    index = INDEX.read_text(encoding="utf-8")
    index = replace_between(index, "<!-- LAST_REFRESH_START -->", "<!-- LAST_REFRESH_END -->", homepage_status)
    INDEX.write_text(index, encoding="utf-8")


def main() -> None:
    sources = (
        ("decactus_events.py", "de-cactus"),
        ("metropool_events.py", "metropool"),
        ("oogst_events.py", "oogst"),
        ("hengelo_events.py", "hengelo"),
        ("dutch_holidays.py", "feestdagen"),
    )
    events: list[dict[str, object]] = []
    for event in scrape_matches(load_text(FC_TWENTE_URL)):
        event["source"] = "fc-twente"
        normalize_event_times(event)
        events.append(event)
    for script, source in sources:
        for event in run(script):
            event["source"] = source
            normalize_event_times(event)
            events.append(event)
    events = deduplicate_events(future_events(events))
    for event in events:
        reason = taste_recommendation(event)
        if reason:
            event["recommended"] = True
            event["tasteReason"] = reason
    events.sort(key=lambda event: str(event["startDate"]))
    OUTPUT.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    ICAL.write_text(calendar(events), encoding="utf-8", newline="")
    processed_at = datetime.now(ZoneInfo("Europe/Amsterdam"))
    update_index(events, processed_at)
    update_disclaimer(processed_at)
    print(f"Wrote {len(events)} events and prerendered them in {INDEX}")


if __name__ == "__main__":
    main()
