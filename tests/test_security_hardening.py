import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "event-calendar"
sys.path.insert(0, str(ROOT))

import build_calendar
import server


class SecurityHardeningTests(unittest.TestCase):
    def test_external_blank_links_isolate_the_opener(self) -> None:
        for path in (ROOT / "index.html", ROOT / "about.html", ROOT / "disclaimer.html", ROOT / "privacy.html"):
            html = path.read_text(encoding="utf-8")
            for fragment in html.split('target="_blank"')[1:]:
                opening_tag = fragment.split(">", 1)[0]
                self.assertIn('rel="noopener noreferrer"', opening_tag, path.name)

    def test_frontend_avoids_html_parsing_sinks(self) -> None:
        for name in ("app.js", "loading-watchdog.js"):
            javascript = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn("innerHTML", javascript)
            self.assertNotIn("insertAdjacentHTML", javascript)
            self.assertNotIn("outerHTML", javascript)
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn(".map(normalizeEvent).filter(Boolean)", app)
        self.assertIn("link.rel = 'noopener noreferrer'", app)

    def test_embedded_scraped_json_cannot_close_its_script_element(self) -> None:
        payload = build_calendar.json_for_script(
            [{"name": "</script><script>alert(1)</script>", "description": "A&B\u2028C"}]
        )
        self.assertNotIn("<", payload)
        self.assertNotIn(">", payload)
        self.assertNotIn("&", payload)
        self.assertNotIn("\u2028", payload)
        self.assertIn("\\u003c/script\\u003e", payload)

    def test_prerendered_scraped_text_is_html_escaped(self) -> None:
        markup = build_calendar.prerender_event(
            {
                "name": "</h3><script>alert(1)</script>",
                "startDate": "2026-08-01T20:00:00+02:00",
                "location": "<img src=x onerror=alert(1)>",
                "source": "metropool",
                "url": "javascript:alert(1)",
            }
        )
        self.assertNotIn("<script>", markup)
        self.assertNotIn("<img", markup)
        self.assertNotIn("javascript:", markup)
        self.assertIn("&lt;script&gt;", markup)

    def test_server_sends_strict_security_headers(self) -> None:
        headers = server.SECURITY_HEADERS
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["Referrer-Policy"], "strict-origin-when-cross-origin")
        self.assertEqual(headers["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertEqual(headers["Strict-Transport-Security"], "max-age=31536000; includeSubDomains")
        self.assertIn("payment=()", headers["Permissions-Policy"])
        policy = headers["Content-Security-Policy"]
        self.assertIn("script-src 'self'", policy)
        self.assertIn("frame-ancestors 'none'", policy)
        self.assertIn("script-src 'self' https://matomo.puntuale.nl", policy)
        self.assertIn("connect-src 'self' https://matomo.puntuale.nl", policy)
        self.assertNotIn("'unsafe-inline'", policy)
        self.assertNotIn("'unsafe-eval'", policy)


if __name__ == "__main__":
    unittest.main()
