import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "event-calendar"
sys.path.insert(0, str(ROOT))

from build_calendar import calendar


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


if __name__ == "__main__":
    unittest.main()
