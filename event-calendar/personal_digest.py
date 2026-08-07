#!/usr/bin/env python3
# ruff: noqa: E501
"""Email or webhook a personal one-month Twente event digest."""

from __future__ import annotations

import json
import os
import smtplib
import subprocess
from datetime import datetime, timedelta
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

EVENTS = Path(__file__).with_name("events.json")
RECIPIENT = "ronald.punt@mac.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_USERNAME = "ronaldpunt.hengelo@gmail.com"
KEYCHAIN_SERVICE = "com.ronald.event-calendar.gmail"
PUBLIC_SITE_URL = "https://event-calendar.puntuale.nl"
LOCAL_TIMEZONE = ZoneInfo("Europe/Amsterdam")

# De e-mailclient ondersteunt geen CSS-variabelen; deze tokens spiegelen de website.
EMAIL_COLORS = {
    "canvas": "#f7f4ed",
    "surface": "#fcfaf5",
    "ink": "#1e293b",
    "inverse": "#f7f4ed",
    "muted": "#625b50",
    "border": "#cfc7b7",
    "accent": "#b93212",
    "accent_warm": "#f9c234",
    "masthead": "#111827",
}
VENUE_COLORS = {
    "metropool": ("#48206e", "#ffd600"),
    "de-cactus": ("#81d742", "#111827"),
    "fc-twente": ("#910d13", "#f7f4ed"),
    "oogst": ("#202020", "#f7f4ed"),
    "hengelo": ("#3154a1", "#f7f4ed"),
    "feestdagen": ("#f58220", "#111827"),
}
EMAIL_FONT_UI = "Arial, Helvetica, sans-serif"
EMAIL_FONT_DISPLAY = "Arial Narrow, Arial, Helvetica, sans-serif"
LOGO = Path(__file__).with_name("assets") / "icon-192.png"
MONTH_NAMES = ("januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december")
WEEKDAY_ABBREVIATIONS = ("ma", "di", "wo", "do", "vr", "za", "zo")


def upcoming_events() -> list[dict[str, object]]:
    now = datetime.now(LOCAL_TIMEZONE)
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = (first_of_month + timedelta(days=62)).replace(day=1)
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    return [
        event
        for event in events
        if now <= datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00")).astimezone(LOCAL_TIMEZONE) < end
    ]


def month_title(value: datetime) -> str:
    return f"{MONTH_NAMES[value.month - 1].capitalize()} {value.year}"


def html_digest(events: list[dict[str, object]], logo_cid: str) -> str:
    groups: dict[tuple[int, int], list[dict[str, object]]] = {}
    for event in events:
        start = datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00")).astimezone(LOCAL_TIMEZONE)
        groups.setdefault((start.year, start.month), []).append(event)
    sections = []
    for _, month_events in sorted(groups.items()):
        items = []
        first_start = datetime.fromisoformat(str(month_events[0]["startDate"]).replace("Z", "+00:00")).astimezone(LOCAL_TIMEZONE)
        for event in month_events:
            start = datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00")).astimezone(LOCAL_TIMEZONE)
            background, foreground = VENUE_COLORS.get(str(event.get("source")), (EMAIL_COLORS["surface"], EMAIL_COLORS["ink"]))
            source = str(event.get("source") or "")
            venue = {"metropool": "Metropool", "de-cactus": "De Cactus", "fc-twente": "FC Twente", "oogst": "Oogst", "hengelo": "Uit in Hengelo", "feestdagen": "Feestdag"}.get(source, "Uitagenda")
            links = f'<a href="{escape(str(event["url"]), quote=True)}" style="color:{foreground}">Info</a>' if event.get("url") else ""
            if event.get("ticketUrl") and (event["ticketUrl"] != event.get("url") or source == "de-cactus"):
                separator = " &nbsp;·&nbsp; " if links else ""
                links += f'{separator}<a href="{escape(str(event["ticketUrl"]), quote=True)}" style="color:{foreground};font-weight:bold">Tickets</a>'
            meta = " · ".join(str(value) for value in (venue, event.get("genre"), event.get("location")) if value)
            availability = "<br><strong>Uitverkocht</strong>" if event.get("soldOut") is True else ""
            items.append(
                f"<tr><td style='padding:0 0 12px'><table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='background:{background};color:{foreground}'><tr>"
                f"<td style='width:72px;padding:16px 10px 16px 16px;vertical-align:top;font:700 16px {EMAIL_FONT_DISPLAY}'>{escape(start.strftime('%d'))}<br><span style='font:12px {EMAIL_FONT_UI}'>{WEEKDAY_ABBREVIATIONS[start.weekday()].upper()}</span></td>"
                f"<td style='padding:16px 16px 16px 0;vertical-align:top'><strong style='font:600 18px {EMAIL_FONT_DISPLAY}'>{escape(str(event['name']))}</strong><br><span style='font:13px {EMAIL_FONT_UI}'>{escape(meta)}</span><br><span style='font:13px {EMAIL_FONT_UI}'>{escape(start.strftime('%H:%M'))} uur &nbsp; {links}</span>{availability}</td></tr></table></td></tr>"
            )
        sections.append(f"<tr><td style='padding:28px 0 10px;font:700 24px {EMAIL_FONT_DISPLAY};text-transform:uppercase'>{month_title(first_start)}</td></tr>{''.join(items)}")
    content = "".join(sections) or "<tr><td>Geen evenementen in de komende twee maanden.</td></tr>"
    return f"""<!doctype html><html lang='nl'><body style='margin:0;background:{EMAIL_COLORS['canvas']};color:{EMAIL_COLORS['ink']};font-family:{EMAIL_FONT_UI}'>
<table role='presentation' width='100%' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:24px'>
<table role='presentation' width='600' cellspacing='0' cellpadding='0' style='max-width:600px'><tr><td style='background:{EMAIL_COLORS['masthead']};color:{EMAIL_COLORS['inverse']};padding:24px'>
<img src='cid:{logo_cid}' width='56' height='56' alt='Uit Vandaag' style='display:block;margin:0 0 18px' /><p style='margin:0;color:{EMAIL_COLORS['accent_warm']};font:12px {EMAIL_FONT_UI};letter-spacing:1px'>TWENTE · UITAGENDA</p><h1 style='margin:10px 0 0;font:700 36px {EMAIL_FONT_DISPLAY}'>Dit staat er op de planning</h1></td></tr>
<tr><td style='background:{EMAIL_COLORS['surface']};padding:26px'><p style='margin:0'>Jouw culturele agenda voor deze en volgende maand.</p><table role='presentation' width='100%' cellspacing='0' cellpadding='0'>{content}</table>
<p style='margin:26px 0 0'><a href='{PUBLIC_SITE_URL}' style='display:inline-block;background:{EMAIL_COLORS['accent']};color:{EMAIL_COLORS['inverse']};padding:12px 16px;text-decoration:none'>Bekijk volledige agenda →</a></p></td></tr>
<tr><td style='padding:18px 26px;color:{EMAIL_COLORS['muted']};font:12px {EMAIL_FONT_UI}'>Een idee van <a href='https://www.ronaldpunt.nl' style='color:{EMAIL_COLORS['muted']}'>Ronald Punt</a>. Deze agenda gebruikt webscraping; gebruik op eigen risico.</td></tr>
</table></td></tr></table></body></html>"""


def send_email(content: str, logo_cid: str) -> None:
    message = EmailMessage()
    message["Subject"] = "Uit Vandaag: jouw Twentse agenda"
    sender_address = os.environ.get("EVENT_CALENDAR_FROM", os.environ.get("EVENT_CALENDAR_SMTP_USERNAME", SMTP_USERNAME))
    message["From"] = Address("Uit Vandaag – Twente", addr_spec=sender_address)
    message["To"] = RECIPIENT
    message.set_content("Open deze e-mail in een HTML-compatibele client.")
    message.add_alternative(content, subtype="html")
    html_part = message.get_payload()[-1]
    if LOGO.exists():
        html_part.add_related(LOGO.read_bytes(), maintype="image", subtype="png", cid=f"<{logo_cid}>")
    send_message(message)


def send_suggestion(name: str, email: str, category: str, suggestion: str) -> None:
    """Deliver a validated website suggestion without exposing the recipient publicly."""
    message = EmailMessage()
    message["Subject"] = f"Uit Vandaag — nieuwe suggestie ({category})"
    message["From"] = os.environ.get("EVENT_CALENDAR_FROM", os.environ.get("EVENT_CALENDAR_SMTP_USERNAME", SMTP_USERNAME))
    message["To"] = RECIPIENT
    if email:
        message["Reply-To"] = email
    sender = name or "Anonieme bezoeker"
    reply_address = email or "Niet opgegeven"
    message.set_content(
        f"Naam: {sender}\nE-mail: {reply_address}\nCategorie: {category}\n\n{suggestion}\n"
    )
    send_message(message)


def send_message(message: EmailMessage) -> None:
    """Send one prepared message through the configured authenticated SMTP account."""
    password = os.environ.get("EVENT_CALENDAR_SMTP_PASSWORD")
    if password is None:
        if os.name != "posix" or not Path("/usr/bin/security").exists():
            raise RuntimeError("EVENT_CALENDAR_SMTP_PASSWORD is required outside macOS")
        password = subprocess.check_output(
            ["security", "find-generic-password", "-a", SMTP_USERNAME, "-s", KEYCHAIN_SERVICE, "-w"],
            text=True,
        ).strip()
    host = os.environ.get("EVENT_CALENDAR_SMTP_HOST", SMTP_HOST)
    username = os.environ.get("EVENT_CALENDAR_SMTP_USERNAME", SMTP_USERNAME)
    port = int(os.environ.get("EVENT_CALENDAR_SMTP_PORT", "465"))
    with smtplib.SMTP_SSL(host, port, timeout=20) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)


def send_webhook(events: list[dict[str, object]]) -> None:
    url = os.environ.get("EVENT_CALENDAR_WEBHOOK_URL")
    if not url:
        return
    body = json.dumps({"recipient": RECIPIENT, "events": events}).encode()
    request = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=30):
        pass


def main() -> None:
    events = upcoming_events()
    logo_cid = make_msgid()[1:-1]
    content = html_digest(events, logo_cid)
    send_email(content, logo_cid)
    send_webhook(events)
    print(f"Sent {len(events)} upcoming events to {RECIPIENT}")


if __name__ == "__main__":
    main()
