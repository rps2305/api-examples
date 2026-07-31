import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from event_sources import json_ld_events
from fc_twente_ical import fold, make_calendar, scrape_matches

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

    def test_match_cards_do_not_invent_a_venue(self) -> None:
        html = """
        <div class="bg-white grid grid-cols-3">
          <div class="text-lg font-serif">14 augustus 2026</div>
          zaterdag 20:00
          <img alt="Logo Eerste Selectie"><img alt="Logo NEC">
        <aside data-drawer>
        """
        matches = scrape_matches(html)
        self.assertEqual(matches[0]["name"], "FC Twente - NEC")
        self.assertNotIn("location", matches[0])

    def test_marks_fc_twente_as_home_only_when_listed_second(self) -> None:
        html = (
            '<div class="bg-white grid grid-cols-3"><div class="text-lg font-serif">'
            '14 augustus 2026</div> zaterdag 20:00 <img alt="Logo NEC">'
            '<img alt="Logo Eerste Selectie">'
            '<div class="bg-white grid grid-cols-3"><div class="text-lg font-serif">'
            '21 augustus 2026</div> zaterdag 20:00 <img alt="Logo Eerste Selectie">'
            '<img alt="Logo NEC"><aside data-drawer>'
        )
        matches = scrape_matches(html)
        self.assertTrue(matches[0]["isHome"])
        self.assertFalse(matches[1]["isHome"])


if __name__ == "__main__":
    unittest.main()
