import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from event_sources import EventSourceError, ical_datetime, json_ld_events, load_text, normalize_datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "event-calendar"))
from build_calendar import deduplicate_events, future_events, local_date_key

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

    def test_normalizes_local_summer_and_winter_times_to_utc(self) -> None:
        self.assertEqual(normalize_datetime("2026-08-01T20:30:00"), "2026-08-01T18:30:00Z")
        self.assertEqual(normalize_datetime("2027-01-15T20:30:00"), "2027-01-15T19:30:00Z")
        self.assertEqual(normalize_datetime("2026-08-01"), "2026-08-01")

    def test_can_correct_a_floating_local_time_mislabeled_as_utc(self) -> None:
        self.assertEqual(
            normalize_datetime("2026-08-01T20:30:00Z", floating_local=True),
            "2026-08-01T18:30:00Z",
        )
        self.assertEqual(
            normalize_datetime("2027-01-15T20:30:00Z", floating_local=True),
            "2027-01-15T19:30:00Z",
        )

    def test_local_date_key_handles_events_near_utc_midnight(self) -> None:
        self.assertEqual(local_date_key("2026-07-31T22:30:00Z"), "2026-08-01")
        self.assertEqual(local_date_key("2027-01-15T23:30:00Z"), "2027-01-16")

    def test_rejects_invalid_datetime(self) -> None:
        with self.assertRaisesRegex(EventSourceError, "invalid event date/time"):
            ical_datetime("kick-off later")

    def test_keeps_only_future_events(self) -> None:
        now = datetime(2026, 8, 1, 12, tzinfo=ZoneInfo("Europe/Amsterdam"))
        events = [
            {"name": "Past", "startDate": "2026-08-01T11:00:00+02:00"},
            {"name": "Future", "startDate": "2026-08-01T13:00:00+02:00"},
            {"name": "All day today", "startDate": "2026-08-01"},
            {"name": "Tomorrow", "startDate": "2026-08-02"},
        ]
        self.assertEqual(
            [event["name"] for event in future_events(events, now)],
            ["Future", "All day today", "Tomorrow"],
        )

    def test_deduplicates_same_event_across_sources(self) -> None:
        events = [
            {"name": "Oogst Live!", "startDate": "2026-08-01T20:00:00+02:00", "source": "oogst"},
            {"name": "Oogst Live", "startDate": "2026-08-01T20:00:00+02:00", "source": "hengelo"},
        ]
        self.assertEqual(deduplicate_events(events), events[:1])

    def test_deduplicates_same_named_event_on_same_day_and_location(self) -> None:
        events = [
            {"name": "Clubnacht", "startDate": "2026-08-01T18:00:00Z", "location": "Metropool, Hengelo"},
            {"name": "Clubnacht", "startDate": "2026-08-01T18:30:00Z", "location": "Metropool Hengelo"},
        ]
        self.assertEqual(deduplicate_events(events), events[:1])


if __name__ == "__main__":
    unittest.main()
