# Persoonlijke Twente-agenda

Open `index.html` direct in je browser voor de lokale, statische agenda.

Voor publicatie kopieer je de inhoud van deze map naar `event-calendar.puntuale.nl`. De website en de e-maildigest zijn bewust gescheiden: de website bevat de volledige interactieve agenda; de e-mail is een compacte, inbox-veilige maandselectie met een link naar de website.

## Bronnen en agenda-abonnement

De agenda verzamelt toekomstige openbare items van Metropool, De Cactus, Broedplaats Oogst, de Hengelose evenementenkalender en FC Twente. Iedere kaart heeft een 🗓-knop voor één iCalendar-bestand; `events.ics` bevat alle toekomstige bronnen en kan als agenda-abonnement worden gebruikt. FC Twente-thuiswedstrijden zijn donkerrood gemarkeerd.

Controleer tijden, toegang en tickets altijd bij de oorspronkelijke aanbieder. Zie `disclaimer.html` voor bronlinks en de volledige disclaimer.

## Wekelijkse e-mail

De digest gaat iedere maandag om 07:00 naar `ronald.punt@mac.com` en bevat de komende maand. Gmail gebruikt standaard `smtp.gmail.com` via SSL op poort 465. Het app-wachtwoord staat veilig in je macOS Keychain onder `com.ronald.event-calendar.gmail`; zet het nooit in een bestand of commit. Optioneel: `EVENT_CALENDAR_SMTP_PORT`, `EVENT_CALENDAR_FROM`, en `EVENT_CALENDAR_WEBHOOK_URL`.

Vervang `PERSONAL_CALENDAR_PATH` in `com.ronald.event-calendar.plist` door het absolute pad van deze map. Plaats daarna het bestand in `~/Library/LaunchAgents/` en laad het met `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.ronald.event-calendar.plist`.

## Docker: site, scraper en verzendwebhook

De container serveert de statische agenda op poort 8080. Bij het opstarten wordt de agenda vernieuwd; lukt een externe scraper tijdelijk niet, dan blijft de meegebouwde agenda beschikbaar.

```sh
cd event-calendar
cp .env.example .env
docker compose up --build -d
```

Vul in `.env` een Gmail-appwachtwoord in voor `EVENT_CALENDAR_SMTP_PASSWORD` en een lang, willekeurig geheim voor `EVENT_CALENDAR_WEBHOOK_TOKEN`. Dit bestand staat in `.gitignore` en mag niet worden gecommit.

De beveiligde webhook ververst eerst alle bronnen, bouwt de website en iCalendar-feed opnieuw op, en verstuurt daarna de maanddigest:

```sh
curl -X POST http://localhost:8080/webhook/send \
  -H "Authorization: Bearer JOUW_WEBHOOK_TOKEN"
```

De respons is bijvoorbeeld `{"sent": true, "events": 12}`. Zet de container achter HTTPS (bijvoorbeeld via de reverse proxy voor `event-calendar.puntuale.nl`) voordat je de webhook publiek maakt. De container voert dezelfde vernieuwing en verzending zelfstandig iedere maandag in het uur van 07:00 uit (tijdzone `Europe/Amsterdam`); zet `EVENT_CALENDAR_SCHEDULE_ENABLED=false` om dit uit te schakelen.
