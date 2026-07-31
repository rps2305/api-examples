#!/usr/bin/env python3
# ruff: noqa: E501
"""Email or webhook a personal one-month Twente event digest."""

from __future__ import annotations

import json
import os
import smtplib
import subprocess
from datetime import datetime, timedelta
from email.message import EmailMessage
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

EVENTS = Path(__file__).with_name("events.json")
RECIPIENT = "ronald.punt@mac.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_USERNAME = "ronaldpunt.hengelo@gmail.com"
KEYCHAIN_SERVICE = "com.ronald.event-calendar.gmail"
PUBLIC_SITE_URL = "https://event-calendar.puntuale.nl"

# De e-mailclient ondersteunt geen CSS-variabelen; deze tokens spiegelen de website.
EMAIL_COLORS = {
    "canvas": "#f7f4ed",
    "surface": "#fcfaf5",
    "ink": "#1e293b",
    "inverse": "#f7f4ed",
    "muted": "#625b50",
    "border": "#cfc7b7",
    "accent": "#ff4f1f",
    "accent_warm": "#f9c234",
    "masthead": "#111827",
}
EMAIL_FONT_UI = "Arial, Helvetica, sans-serif"
EMAIL_FONT_DISPLAY = "Arial Narrow, Arial, Helvetica, sans-serif"


def upcoming_events() -> list[dict[str, object]]:
    now = datetime.now().astimezone()
    end = now + timedelta(days=30)
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    return [
        event
        for event in events
        if now <= datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00")).astimezone() < end
    ]


def html_digest(events: list[dict[str, object]]) -> str:
    items = []
    for event in events:
        start = datetime.fromisoformat(str(event["startDate"]).replace("Z", "+00:00")).astimezone()
        links = f'<a href="{escape(str(event["url"]))}">Info</a>' if event.get("url") else ""
        if event.get("ticketUrl") and event["ticketUrl"] != event.get("url"):
            links += f' · <a href="{escape(str(event["ticketUrl"]))}">Tickets</a>'
        meta = " · ".join(str(value) for value in (event.get("genre"), event.get("location")) if value)
        items.append(
            "<tr><td style='padding:14px 0;border-bottom:1px solid "
            f"{EMAIL_COLORS['border']};vertical-align:top'>"
            f"<strong>{escape(start.strftime('%a %d %b, %H:%M'))}</strong><br>"
            f"<span style='font:600 17px {EMAIL_FONT_DISPLAY}'>{escape(str(event['name']))}</span><br>"
            f"<span style='color:{EMAIL_COLORS['muted']}'>{escape(meta)}</span><br>{links}</td></tr>"
        )
    content = "".join(items) or "<tr><td>Geen evenementen in de komende zeven dagen.</td></tr>"
    return f"""<!doctype html><html lang='nl'><body style='margin:0;background:{EMAIL_COLORS['canvas']};color:{EMAIL_COLORS['ink']};font-family:{EMAIL_FONT_UI}'>
<table role='presentation' width='100%' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:24px'>
<table role='presentation' width='600' cellspacing='0' cellpadding='0' style='max-width:600px'><tr><td style='background:{EMAIL_COLORS['masthead']};color:{EMAIL_COLORS['inverse']};padding:28px'>
<p style='margin:0;color:{EMAIL_COLORS['accent_warm']};font:12px {EMAIL_FONT_UI};letter-spacing:1px'>TWENTE · UITAGENDA</p><h1 style='margin:10px 0 0;font:700 36px {EMAIL_FONT_DISPLAY}'>Uit deze week</h1></td></tr>
<tr><td style='background:{EMAIL_COLORS['surface']};padding:26px'><p>Jouw agenda voor de komende maand.</p><table role='presentation' width='100%' cellspacing='0' cellpadding='0'>{content}</table>
<p style='margin:26px 0 0'><a href='{PUBLIC_SITE_URL}' style='display:inline-block;background:{EMAIL_COLORS['accent']};color:{EMAIL_COLORS['inverse']};padding:12px 16px;text-decoration:none'>Bekijk volledige agenda →</a></p></td></tr>
<tr><td style='padding:18px 26px;color:{EMAIL_COLORS['muted']};font:12px {EMAIL_FONT_UI}'>Een idee van <a href='https://www.ronaldpunt.nl' style='color:{EMAIL_COLORS['muted']}'>Ronald Punt</a>. Deze agenda gebruikt webscraping; gebruik op eigen risico.</td></tr>
</table></td></tr></table></body></html>"""


def send_email(content: str) -> None:
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
    message = EmailMessage()
    message["Subject"] = "Uit deze week — Twente"
    message["From"] = os.environ.get("EVENT_CALENDAR_FROM", username)
    message["To"] = RECIPIENT
    message.set_content("Open deze e-mail in een HTML-compatibele client.")
    message.add_alternative(content, subtype="html")
    with smtplib.SMTP_SSL(host, port) as smtp:
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
    content = html_digest(events)
    send_email(content)
    send_webhook(events)
    print(f"Sent {len(events)} upcoming events to {RECIPIENT}")


if __name__ == "__main__":
    main()
