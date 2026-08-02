import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "event-calendar"


class PwaAssetsTests(unittest.TestCase):
    def test_manifest_has_installable_icons_and_scope(self) -> None:
        manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(manifest["scope"], "/")
        self.assertEqual(manifest["start_url"], "/")
        purposes = {icon.get("purpose") for icon in manifest["icons"]}
        self.assertIn("any", purposes)
        self.assertIn("maskable", purposes)

    def test_service_worker_precache_versions_match_html(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        worker = (ROOT / "sw.js").read_text(encoding="utf-8")
        for asset in ("styles.css", "app.js", "theme.js", "loading-watchdog.js"):
            versioned = re.search(rf'{asset}\?v=[0-9-]+', index)
            self.assertIsNotNone(versioned)
            self.assertIn(f"/{versioned.group()}", worker)

    def test_offline_shell_contains_current_generated_files(self) -> None:
        worker = (ROOT / "sw.js").read_text(encoding="utf-8")
        for asset in ("/", "/about.html", "/privacy.html", "/events.json", "/events.ics", "/site.webmanifest"):
            self.assertIn(f"'{asset}'", worker)

    def test_homepage_has_semantic_agenda_heading_structure(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("<h1>Uitagenda Twente:", index)
        self.assertIn("const title = element('h2')", app)
        self.assertIn("dateNode.dateTime = date", app)
        self.assertIn("element('span', 'day-year', date.slice(0, 4))", app)
        self.assertIn('class="day-year">', index)
        self.assertIn("element('h3', '', event.name)", app)

    def test_homepage_images_have_alternative_text(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        images = re.findall(r"<img\b[^>]*>", index)
        self.assertTrue(images)
        self.assertTrue(all(re.search(r'\balt="[^"]*"', image) for image in images))
        self.assertIn('alt="Uit Vandaag Twente-logo"', index)

    def test_homepage_explains_the_calendar_and_search_examples(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="footer-about-title">Over deze agenda</h2>', index)
        self.assertIn("Ronald Punt</a> bouwt en beheert", index)
        self.assertIn('placeholder="Zoek op Metropool, rock of FC Twente"', index)
        self.assertIn('id="agenda-summary"', index)
        self.assertIn('id="scope-title">Persoonlijk gekozen, niet compleet.', index)
        self.assertIn("Hengelo, Almelo en Enschede", index)
        self.assertIn("iedere zes uur", index)
        self.assertIn("genormaliseerde naam, aanvang", index)

    def test_disclaimer_uses_branded_source_marks(self) -> None:
        disclaimer = (ROOT / "disclaimer.html").read_text(encoding="utf-8")
        self.assertIn('assets/logo-oogst.svg', disclaimer)
        self.assertIn('assets/logo-uit-in-hengelo.svg', disclaimer)
        self.assertIn("Laatste succesvolle verwerking van alle bronnen", disclaimer)

    def test_hero_summary_is_calculated_from_current_event_data(self) -> None:
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("function updateAgendaSummary(events)", app)
        self.assertIn("dateKeyAfter(today, 7)", app)
        self.assertIn("updateAgendaSummary(events)", app)
        self.assertIn("hasPrerenderedAgenda && visibleLimit === PAGE_SIZE", app)
        self.assertIn("requestIdleCallback(refreshSummary", app)

    def test_matomo_is_consent_first_and_available_on_every_page(self) -> None:
        analytics = (ROOT / "analytics-consent.js").read_text(encoding="utf-8")
        for command in ("requireConsent", "setConsentGiven", "trackPageView", "enableLinkTracking"):
            self.assertIn(command, analytics)
        self.assertIn("https://matomo.puntuale.nl/", analytics)
        self.assertIn("MATOMO_SITE_ID = '15'", analytics)
        self.assertIn("readChoice() !== 'granted'", analytics)
        self.assertIn("requestIdleCallback", analytics)
        self.assertIn("deleteMatomoCookies", analytics)
        self.assertIn("event-calendar/analytics-consent.js", (ROOT / "Dockerfile").read_text(encoding="utf-8"))
        for name in ("index.html", "about.html", "disclaimer.html", "privacy.html"):
            page = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('analytics-consent.js?v=20260802-2', page)
            self.assertIn('data-privacy-settings', page)
        self.assertIn("document.body.prepend(notice)", analytics)

    def test_disclaimer_explains_matomo_and_cookie_durations(self) -> None:
        disclaimer = (ROOT / "disclaimer.html").read_text(encoding="utf-8")
        self.assertIn('id="privacy"', disclaimer)
        self.assertIn("Zonder toestemming", disclaimer)
        self.assertIn("13 maanden", disclaimer)
        self.assertIn("30 minuten", disclaimer)
        self.assertIn("6 maanden", disclaimer)

    def test_page_titles_and_about_description_are_locally_specific(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        self.assertIn("<title>Uitagenda Twente – Concerten, evenementen en FC Twente</title>", index)
        self.assertIn("<title>Ronalds muzieksmaak en concerttips – Uitagenda Twente</title>", about)
        self.assertIn("de persoonlijke basis voor concerttips en aanbevelingen in Uitagenda Twente", about)

    def test_bam_is_announced_and_volunteer_context_is_clear(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        disclaimer = (ROOT / "disclaimer.html").read_text(encoding="utf-8")
        self.assertIn("BAM! Festival</a> worden later toegevoegd", index)
        self.assertIn("al jarenlang vrijwilliger bij Metropool, BAM! Festival en Oogst", about)
        self.assertIn("al jarenlang vrijwilliger bij Metropool, BAM! Festival en Oogst", disclaimer)
        self.assertIn("Deze agenda maak ik op persoonlijke titel", about)
        self.assertIn("de website is geen officiële publicatie", disclaimer)

    def test_social_sharing_metadata_is_complete(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('property="og:title" content="Uitagenda Twente: Concerten &amp; FC Twente"', index)
        self.assertIn('property="og:description" content="Eén agenda voor wedstrijden van FC Twente', index)
        self.assertIn('property="og:image:secure_url"', index)
        self.assertIn('property="og:image:alt"', index)
        self.assertIn('name="twitter:card" content="summary"', index)
        self.assertIn('name="twitter:title" content="Uitagenda Twente: Concerten &amp; FC Twente"', index)

    def test_agenda_is_prerendered_with_schema_item_list(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        events = json.loads((ROOT / "events.json").read_text(encoding="utf-8"))
        schema_match = re.search(r'<script id="event-schema" type="application/ld\+json">(.*?)</script>', index)
        self.assertIsNotNone(schema_match)
        schema = json.loads(schema_match.group(1))
        self.assertEqual(schema["@type"], "ItemList")
        self.assertGreater(schema["numberOfItems"], 0)
        prerendered = index.split("<!-- EVENT_LIST_START -->", 1)[1].split("<!-- EVENT_LIST_END -->", 1)[0]
        self.assertEqual(prerendered.count('<article class="event '), min(60, len(events)))
        self.assertIn("<h3>", prerendered)
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("hasPrerenderedAgenda", app)
        self.assertIn("const PAGE_SIZE = 60", app)
        self.assertIn("matching.slice(0, visibleLimit)", app)
        self.assertIn("data-load-more", index)

    def test_browser_times_are_fixed_to_the_venue_timezone(self) -> None:
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("timeZone: 'Europe/Amsterdam'", app)
        self.assertIn("Object.groupBy(shown, eventDateKey)", app)
        self.assertIn("new Date(event.startDate).toISOString()", app)

    def test_individual_calendar_export_uses_known_or_default_end_time(self) -> None:
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("const DEFAULT_EVENT_DURATION_MINUTES = 120", app)
        self.assertIn("endDate,", app)
        self.assertIn("if (!endDate && event.startDate.length !== 10)", app)
        self.assertIn("lines.push(`DTEND${icalDateValue(endDate)}`)", app)

    def test_back_to_top_is_accessible_and_available_on_every_page(self) -> None:
        script = (ROOT / "back-to-top.js").read_text(encoding="utf-8")
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("Math.max(window.scrollY, document.documentElement.scrollTop)", script)
        self.assertIn("window.addEventListener('pageshow', updateVisibility)", script)
        self.assertIn("window.visualViewport?.addEventListener('resize', updateVisibility)", script)
        self.assertIn("prefers-reduced-motion: reduce", script)
        self.assertIn("heading.focus({ preventScroll: true })", script)
        self.assertIn(".back-to-top[hidden]", styles)
        self.assertIn("calc(var(--space-3) + env(safe-area-inset-top, 0px))", styles)
        self.assertIn("calc(var(--space-4) + env(safe-area-inset-bottom, 0px))", styles)
        for name in ("index.html", "about.html", "disclaimer.html", "privacy.html"):
            page = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('data-back-to-top hidden aria-label="Terug naar boven"', page)
            self.assertIn('back-to-top.js?v=20260802-2', page)

    def test_suggestion_privacy_copy_and_page_are_complete(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
        self.assertIn('class="form-privacy form-wide"', index)
        self.assertIn("Naam en e-mailadres zijn optioneel", index)
        self.assertIn("Categorie en suggestie zijn verplicht", index)
        self.assertEqual(index.count('class="required-label">Verplicht'), 2)
        self.assertIn('href="privacy.html">Lees meer over privacy</a>', index)
        self.assertIn("De website slaat je naam, e-mailadres en suggestie niet op in een database", privacy)
        self.assertIn("Ronald Punt is verantwoordelijk voor deze verwerking", privacy)
        self.assertIn("een afzonderlijk verzoek om verwijdering niet nodig", privacy)
        self.assertIn("event-calendar/privacy.html", (ROOT / "Dockerfile").read_text(encoding="utf-8"))
        self.assertIn("/privacy.html", (ROOT / "sw.js").read_text(encoding="utf-8"))

    def test_homepage_footer_links_to_de_twee_wezen_weesjes(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://www.detweewezen.nl/weesjes"', index)
        self.assertIn("Weesjes bij De Twee Wezen ↗", index)

    def test_agenda_has_no_javascript_and_loading_failure_fallbacks(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        watchdog = (ROOT / "loading-watchdog.js").read_text(encoding="utf-8")
        self.assertIn("<noscript>", index)
        self.assertIn('class="no-js-fallback"', index)
        self.assertIn('data-state="loading"', index)
        self.assertIn('loading-watchdog.js?v=', index)
        self.assertIn('#status[data-state="loading"]', watchdog)
        self.assertIn("}, 8000);", watchdog)
        self.assertIn("status.dataset.state = 'ready'", app)
        self.assertIn("status.dataset.state = 'error'", app)

    def test_venue_marquee_stops_for_reduced_motion(self) -> None:
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        reduced_motion = styles.split("@media (prefers-reduced-motion: reduce)", 1)[1]
        self.assertIn(".venue-track { animation: none; transform: none; will-change: auto; }", reduced_motion)
        self.assertIn(".venue-window { overflow-x: auto; scroll-snap-type: x mandatory; }", reduced_motion)
        self.assertIn(".venue-card:nth-child(n + 6) { display: none; }", reduced_motion)

    def test_contrast_touch_targets_and_theme_controls_are_consistent(self) -> None:
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        theme = (ROOT / "theme.js").read_text(encoding="utf-8")
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(".editorial-scope a { color: var(--color-link-on-dark)", styles)
        self.assertIn("background: var(--color-masthead);", styles)
        self.assertIn("min-inline-size: 44px", styles)
        self.assertIn("overflow-wrap: anywhere", styles)
        self.assertIn('sizes="(max-width: 700px) 78vw, (max-width: 1409px) 44vw, 620px"', index)
        self.assertIn('class="skip-link" href="#agenda-controls"', index)
        self.assertIn('id="agenda-controls" class="controls" tabindex="-1"', index)
        self.assertIn("function setupToggle()", theme)
        for name in ("index.html", "about.html", "disclaimer.html", "privacy.html"):
            page = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('id="theme-toggle"', page)
            self.assertIn('theme.js?v=20260802-3', page)

    def test_sold_out_events_render_a_visual_badge(self) -> None:
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("if (event.soldOut)", app)
        self.assertIn("element('span', 'sold-out-badge', 'Uitverkocht')", app)
        self.assertIn(".sold-out-badge", styles)

    def test_music_taste_page_and_recommendation_filter_are_present(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('data-recommended-filter', index)
        self.assertIn('href="about.html">Ronalds muzieksmaak</a>', index)
        self.assertIn("Mijn muzieksmaak", about)
        self.assertIn("Balkanbeats en old-school hiphop", about)
        self.assertIn("24 bezoeken aan Lowlands", about)
        self.assertIn("Pearl Jam niet, Nirvana nadrukkelijk wel", about)
        self.assertIn("if (event.recommended)", app)


if __name__ == "__main__":
    unittest.main()
