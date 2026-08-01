import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "event-calendar"))

from taste_profile import taste_recommendation


class TasteProfileTests(unittest.TestCase):
    def test_recommends_a_favored_artist(self) -> None:
        event = {"@type": "Event", "name": "Radiohead live", "genre": "Rock"}
        self.assertEqual(taste_recommendation(event), "Sluit aan bij je voorkeur voor Radiohead.")

    def test_recommends_a_strong_style_signal(self) -> None:
        event = {"@type": "Event", "name": "Salsa night", "genre": "Latin"}
        self.assertIn("latin", taste_recommendation(event) or "")

    def test_generic_rock_alone_is_not_enough(self) -> None:
        event = {"@type": "Event", "name": "Onbekende band", "genre": "Rock"}
        self.assertIsNone(taste_recommendation(event))

    def test_recommends_new_explicit_artist_preferences(self) -> None:
        for name in ("Antimatter & Sleeping Pulse", "Shantel live", "Ooostblok", "Arrested Development"):
            with self.subTest(name=name):
                self.assertIsNotNone(taste_recommendation({"@type": "Event", "name": name}))

    def test_recommends_balkan_and_specific_old_school_hiphop_styles(self) -> None:
        self.assertIsNotNone(taste_recommendation({"@type": "Event", "name": "Balkan beats night"}))
        self.assertIsNotNone(taste_recommendation({"@type": "Event", "name": "Old school hiphop night"}))

    def test_explicit_dislike_overrides_an_alternative_genre_match(self) -> None:
        event = {"@type": "Event", "name": "Pearl Jam tribute", "genre": "Alternative rock"}
        self.assertIsNone(taste_recommendation(event))

    def test_heavy_festival_crossover_needs_more_than_one_signal(self) -> None:
        self.assertIsNone(taste_recommendation({"@type": "Event", "name": "Unknown", "genre": "Metal"}))
        self.assertIsNotNone(taste_recommendation({"@type": "Event", "name": "Unknown", "genre": "Hardcore punk"}))

    def test_sports_and_holidays_are_never_music_recommendations(self) -> None:
        event = {"@type": "SportsEvent", "name": "Radiohead - FC Twente", "source": "fc-twente"}
        self.assertIsNone(taste_recommendation(event))


if __name__ == "__main__":
    unittest.main()
