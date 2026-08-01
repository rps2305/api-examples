#!/usr/bin/env python3
"""Generate the official Dutch public holidays for the current and next year."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from event_sources import print_events

OFFICIAL_HOLIDAYS_URL = (
    "https://www.rijksoverheid.nl/onderwerpen/arbeidsovereenkomst-en-cao/"
    "vraag-en-antwoord/officiele-feestdagen"
)


def easter_sunday(year: int) -> date:
    """Return Gregorian Easter Sunday using the Meeus/Jones/Butcher algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def holidays_for_year(year: int) -> list[dict[str, object]]:
    """Return each official holiday as an all-day schema.org Event."""
    easter = easter_sunday(year)
    kings_day = date(year, 4, 27)
    if kings_day.weekday() == 6:  # Koningsdag is celebrated a day earlier on Sunday years.
        kings_day -= timedelta(days=1)
    holidays = (
        ("Nieuwjaarsdag", date(year, 1, 1)),
        ("Goede Vrijdag", easter - timedelta(days=2)),
        ("Eerste paasdag", easter),
        ("Tweede paasdag", easter + timedelta(days=1)),
        ("Koningsdag", kings_day),
        ("Bevrijdingsdag", date(year, 5, 5)),
        ("Hemelvaartsdag", easter + timedelta(days=39)),
        ("Eerste pinksterdag", easter + timedelta(days=49)),
        ("Tweede pinksterdag", easter + timedelta(days=50)),
        ("Eerste kerstdag", date(year, 12, 25)),
        ("Tweede kerstdag", date(year, 12, 26)),
    )
    return [
        {
            "@type": "Event",
            "name": name,
            "startDate": holiday.isoformat(),
            "genre": "Nationale feestdag",
            "location": "Nederland",
            "url": OFFICIAL_HOLIDAYS_URL,
        }
        for name, holiday in holidays
    ]


def main() -> None:
    year = datetime.now(ZoneInfo("Europe/Amsterdam")).year
    print_events(holidays_for_year(year) + holidays_for_year(year + 1))


if __name__ == "__main__":
    main()
