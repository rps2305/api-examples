import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from event_sources import EventSourceError, ical_datetime, json_ld_events, load_text

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "event-calendar"))
from build_calendar import future_events

FIXTURE = Path(__file__).parent / "fixtures" / "events.html"


class EventSourcesTests(unittest.TestCase):
    def test_extracts_graph_and_ignores_invalid_block(self) -> None:
        events = json_ld_events(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual([event["name"] for event in events], ["Testconcert", "FC Twente - Ajax"])

    def test_extracts_list_items(self) -> None:
        html = (
            '<script type="application/ld+json">'
            '{"itemListElement":[{"item":{"@type":"Event","name":"One"}}]}'
            "</script>"
        )
        self.assertEqual(json_ld_events(html)[0]["name"], "One")

    def test_loads_local_input(self) -> None:
        self.assertIn("FC Twente", load_text("unused", FIXTURE))

    def test_formats_datetime(self) -> None:
        self.assertEqual(ical_datetime("2026-08-01"), ";VALUE=DATE:20260801")
        self.assertEqual(ical_datetime("2026-08-01T20:00:00+02:00"), ":20260801T180000Z")

    def test_rejects_invalid_datetime(self) -> None:
        with self.assertRaisesRegex(EventSourceError, "invalid event date/time"):
            ical_datetime("kick-off later")

    def test_keeps_only_future_events(self) -> None:
        now = datetime(2026, 8, 1, 12, tzinfo=ZoneInfo("Europe/Amsterdam"))
        events = [
            {"name": "Past", "startDate": "2026-08-01T11:00:00+02:00"},
            {"name": "Future", "startDate": "2026-08-01T13:00:00+02:00"},
            {"name": "Tomorrow", "startDate": "2026-08-02"},
        ]
        self.assertEqual(
            [event["name"] for event in future_events(events, now)], ["Future", "Tomorrow"]
        )


if __name__ == "__main__":
    unittest.main()
