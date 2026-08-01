import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "event-calendar"))

import server


class SuggestionFormTests(unittest.TestCase):
    def setUp(self) -> None:
        server.RATE_HISTORY.clear()
        server.USED_TOKENS.clear()

    def test_signed_form_token_expires_and_cannot_be_reused(self) -> None:
        token = server.create_form_token(now=1_000)
        self.assertFalse(server.valid_form_token(token, now=1_001))
        self.assertTrue(server.valid_form_token(token, now=1_010))
        self.assertFalse(server.valid_form_token(token, now=1_011))
        self.assertFalse(server.valid_form_token(server.create_form_token(now=1_000), now=10_000))

    def test_validates_and_normalizes_suggestion(self) -> None:
        result = server.validate_suggestion(
            {
                "name": "  Ada  ",
                "email": "ada@example.com",
                "category": "Website",
                "message": "  Dit is een geldige suggestie voor de website.  ",
                "website": "",
            }
        )
        self.assertEqual(result, ("Ada", "ada@example.com", "Website", "Dit is een geldige suggestie voor de website.", ""))

    def test_rejects_header_injection_and_short_messages(self) -> None:
        with self.assertRaises(ValueError):
            server.valid_email("attacker@example.com\nBcc: victim@example.com")
        with self.assertRaises(ValueError):
            server.validate_suggestion(
                {"name": "", "email": "", "category": "Anders", "message": "Te kort", "website": ""}
            )

    def test_rate_limit_enforces_cooldown_and_hourly_cap(self) -> None:
        self.assertTrue(server.within_rate_limit("203.0.113.10", now=100))
        self.assertFalse(server.within_rate_limit("203.0.113.10", now=120))
        self.assertTrue(server.within_rate_limit("203.0.113.10", now=161))
        self.assertTrue(server.within_rate_limit("203.0.113.10", now=222))
        self.assertFalse(server.within_rate_limit("203.0.113.10", now=283))
        self.assertTrue(server.within_rate_limit("203.0.113.10", now=3_701))


if __name__ == "__main__":
    unittest.main()
