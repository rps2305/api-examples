import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "event-calendar"
sys.path.insert(0, str(ROOT))

from build_calendar import calendar, deduplicate_events


class CalendarExportTests(unittest.TestCase):
    def test_timed_event_without_end_gets_two_hour_duration(self) -> None:
        exported = calendar([
            {"name": "Avond zonder eindtijd", "startDate": "2026-08-02T20:00:00+02:00"}
        ])
        self.assertIn("DTSTART:20260802T180000Z", exported)
        self.assertIn("DTEND:20260802T200000Z", exported)

    def test_known_end_time_is_preserved(self) -> None:
        exported = calendar([{
            "name": "Avond met eindtijd",
            "startDate": "2026-08-02T20:00:00+02:00",
            "endDate": "2026-08-02T21:30:00+02:00",
        }])
        self.assertIn("DTEND:20260802T193000Z", exported)
        self.assertNotIn("DTEND:20260802T200000Z", exported)

    def test_all_day_event_without_end_remains_all_day(self) -> None:
        exported = calendar([{"name": "Hele dag", "startDate": "2026-08-02"}])
        self.assertIn("DTSTART;VALUE=DATE:20260802", exported)
        self.assertNotIn("DTEND", exported)

    def test_official_sources_win_over_uit_in_hengelo_duplicates(self) -> None:
        events = [
            {"name": "Oogst Live: Nana Adjoa + LUWTEN", "startDate": "2026-08-22T18:00:00Z", "source": "metropool", "location": "Hengelo"},
            {"name": "Oogst live: Nana Adjoua + Luwten", "startDate": "2026-08-22T18:00:00Z", "source": "hengelo"},
            {"name": "Classic Outdoor", "startDate": "2026-08-15", "source": "oogst", "location": "Broedplaats Oogst, Hengelo"},
            {"name": "Classic Outdoor", "startDate": "2026-08-15T17:00:00Z", "source": "hengelo"},
        ]

        kept = deduplicate_events(events)

        self.assertEqual([event["source"] for event in kept], ["metropool", "oogst"])


if __name__ == "__main__":
    unittest.main()
