import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from event_sources import json_ld_events
from fc_twente_ical import fold, make_calendar


FIXTURE = Path(__file__).parent / "fixtures" / "events.html"


class CalendarTests(unittest.TestCase):
    def test_calendar_contains_only_sports_events(self) -> None:
        calendar = make_calendar(json_ld_events(FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(calendar.count("BEGIN:VEVENT"), 1)
        self.assertIn("SUMMARY:FC Twente - Ajax", calendar)
        self.assertIn("DTSTART:20260801T180000Z", calendar)
        self.assertIn("DTEND:20260801T194500Z", calendar)
        self.assertNotIn("Testconcert", calendar)

    def test_lines_are_folded_by_utf8_octets(self) -> None:
        lines = fold("DESCRIPTION:" + "é" * 80)
        self.assertGreater(len(lines), 1)
        self.assertTrue(all(len(line.encode("utf-8")) <= 75 for line in lines))
        self.assertTrue(lines[1].startswith(" "))


if __name__ == "__main__":
    unittest.main()
