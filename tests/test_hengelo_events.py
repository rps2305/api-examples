import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from hengelo_events import scrape_events


class HengeloEventsTests(unittest.TestCase):
    def test_extracts_cards_dates_categories_and_times(self) -> None:
        html = """
        <div class="event" transition href="https://uitinhengelo.nl/evenementen/test">
          <div class="eventContentHolder">
            <span class="eventCat">Muziek, </span><span class="eventCat">Kunst &amp; Cultuur</span>
            <h5>Test &amp; concert</h5><span class="date">01 aug t/m 02 aug</span>
            <div class="eventDetail"><span>Gratis</span><br><span>10:00 - 17:00 uur</span></div>
          </div>
        </div>
        """
        events = scrape_events(
            html, datetime(2026, 7, 31, 12, tzinfo=ZoneInfo("Europe/Amsterdam"))
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["name"], "Test & concert")
        self.assertEqual(events[0]["genre"], "Muziek, Kunst & Cultuur")
        self.assertEqual(events[0]["startDate"], "2026-08-01T10:00:00+02:00")
        self.assertEqual(events[0]["endDate"], "2026-08-02T17:00:00+02:00")

    def test_rolls_dates_after_new_year_and_handles_today_range(self) -> None:
        html = """
        <div class="event" transition href="https://uitinhengelo.nl/evenementen/winter">
          <div class="eventContentHolder"><h5>Winterevent</h5><span class="date">15 jan</span>
            <div class="eventDetail"><span>20:00 - 23:00 uur</span></div></div>
        </div>
        <div class="event" transition href="https://uitinhengelo.nl/evenementen/summer">
          <div class="eventContentHolder"><h5>Zomerevent</h5><span class="date">t/m 07 aug</span></div>
        </div>
        """
        events = scrape_events(
            html, datetime(2026, 7, 31, 12, tzinfo=ZoneInfo("Europe/Amsterdam"))
        )
        self.assertEqual(events[0]["startDate"], "2027-01-15T20:00:00+01:00")
        self.assertEqual(events[1]["startDate"], "2026-07-31")
        self.assertEqual(events[1]["endDate"], "2026-08-07")


if __name__ == "__main__":
    unittest.main()
