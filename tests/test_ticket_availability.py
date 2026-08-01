import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from decactus_events import event_from_stager
from metropool_events import scrape_events
from oogst_events import scrape_events as scrape_oogst_events


def metropool_card(name: str, tags: str = "") -> str:
    return f'''<div class="event relative test">
      <span class="event-genre">Pop</span>{tags}
      <a class="remove-underline" href="/agenda/{name.lower()}" data-detail-link="1">
        <h4 class="event-title">{name}</h4>
      </a>
      <span data-event-category3="20-08-2026 / 20:30"></span>
      <a class="btn btn-primary" href="https://tickets.example/{name.lower()}">Tickets</a>
    </div>'''


class TicketAvailabilityTests(unittest.TestCase):
    def test_metropool_uses_only_explicit_sold_out_tag(self) -> None:
        html = metropool_card("Racoon", '<span class="tag">Uitverkocht</span>')
        html += metropool_card("Available", '<span class="tag">Metropool Presents</span>')
        events = scrape_events(html)
        self.assertIs(events[0]["soldOut"], True)
        self.assertNotIn("soldOut", events[1])

    def test_metropool_ignores_sold_out_words_in_event_copy(self) -> None:
        events = scrape_events(metropool_card("Na een uitverkochte tour"))
        self.assertNotIn("soldOut", events[0])

    def test_stager_normalizes_sold_out_boolean(self) -> None:
        item = {
            "eventId": 123,
            "name": "Testconcert ",
            "startsOn": "2026-08-20T18:30:00Z",
            "endsOn": "2026-08-20T21:30:00Z",
            "soldOut": True,
        }
        event = event_from_stager(item)
        self.assertEqual(event["name"], "Testconcert")
        self.assertEqual(event["startDate"], "2026-08-20T16:30:00Z")
        self.assertEqual(event["endDate"], "2026-08-20T19:30:00Z")
        self.assertIs(event["soldOut"], True)

    def test_metropool_uses_the_winter_offset(self) -> None:
        html = metropool_card("Wintershow").replace("20-08-2026", "15-01-2027")
        event = scrape_events(html)[0]
        self.assertEqual(event["startDate"], "2027-01-15T20:30:00+01:00")

    def test_oogst_uses_the_winter_offset(self) -> None:
        html = '''<main><div class="project-card"><p class="tijdstip">
        15 januari 2027 <span class="tijd">20:30</span></p>
        <h3>Wintershow</h3></div></main>'''
        event = scrape_oogst_events(html)[0]
        self.assertEqual(event["startDate"], "2027-01-15T20:30:00+01:00")


if __name__ == "__main__":
    unittest.main()
