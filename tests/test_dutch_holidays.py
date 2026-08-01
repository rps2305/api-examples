import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from dutch_holidays import easter_sunday, holidays_for_year


class DutchHolidaysTests(unittest.TestCase):
    def test_matches_rijksoverheid_dates_for_2026(self) -> None:
        holidays = {event["name"]: event["startDate"] for event in holidays_for_year(2026)}
        self.assertEqual(easter_sunday(2026).isoformat(), "2026-04-05")
        self.assertEqual(holidays["Goede Vrijdag"], "2026-04-03")
        self.assertEqual(holidays["Koningsdag"], "2026-04-27")
        self.assertEqual(holidays["Hemelvaartsdag"], "2026-05-14")
        self.assertEqual(holidays["Tweede pinksterdag"], "2026-05-25")

    def test_matches_rijksoverheid_dates_for_2027(self) -> None:
        holidays = {event["name"]: event["startDate"] for event in holidays_for_year(2027)}
        self.assertEqual(easter_sunday(2027).isoformat(), "2027-03-28")
        self.assertEqual(holidays["Goede Vrijdag"], "2027-03-26")
        self.assertEqual(holidays["Hemelvaartsdag"], "2027-05-06")
        self.assertEqual(holidays["Eerste pinksterdag"], "2027-05-16")

    def test_moves_kings_day_when_april_27_is_sunday(self) -> None:
        holidays = {event["name"]: event["startDate"] for event in holidays_for_year(2014)}
        self.assertEqual(holidays["Koningsdag"], "2014-04-26")


if __name__ == "__main__":
    unittest.main()
