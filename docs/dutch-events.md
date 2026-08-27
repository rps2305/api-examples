# Dutch events and FC Twente calendar

## Overview
The repository includes six ready-to-run Python scripts, all built on the
shared helpers in `scripts/event_sources.py`:

- `scripts/metropool_events.py` reads the public Metropool agenda and emits its
  embedded schema.org events as JSON. Supports `--url` and `--input`.
- `scripts/decactus_events.py` does the same for the De Cactus agenda. Supports
  `--url` and `--input`.
- `scripts/oogst_events.py` scrapes the Broedplaats Oogst agenda and prints its
  events as JSON.
- `scripts/hengelo_events.py` scrapes the Uit in Hengelo agenda and prints its
  events as JSON.
- `scripts/dutch_holidays.py` computes the official Dutch public holidays for
  the current and next year (no network access) and prints them as JSON.
- `scripts/fc_twente_ical.py` reads FC Twente's public fixture page and writes
  every published schema.org event to an iCalendar (`.ics`) file. This needs no
  account or API key and does not filter by competition, so published Eredivisie,
  European, and KNVB Beker matches are retained. Supports `--url`, `--input`,
  and `--output`.

The venue websites do not advertise a stable public API. Their scripts therefore
consume the machine-readable JSON-LD (or, for Oogst and Hengelo, the
server-rendered HTML) already published with each agenda page. Website markup
can change; use `--url` on the scripts that support it if a page moves.
Network and HTTP failures produce a short command-line error instead of a
Python traceback.

The parsers and calendar generator are covered by offline HTML-fixture tests,
so the core behavior can be validated without contacting the source websites.

## Python
No third-party Python packages are needed. From the repository root, run:

```bash
python scripts/metropool_events.py > metropool.json
python scripts/decactus_events.py > decactus.json
python scripts/oogst_events.py > oogst.json
python scripts/hengelo_events.py > hengelo.json
python scripts/dutch_holidays.py > feestdagen.json

python scripts/fc_twente_ical.py --output fc-twente.ics
```

For `metropool_events.py`, `decactus_events.py`, and `fc_twente_ical.py`, pass
`--input downloads/page.html` to parse a page downloaded in a browser instead
of fetching it again. The source website controls how far ahead its page
lists events.

## PowerShell
PowerShell can invoke the same keyless scripts:

```powershell
python scripts/metropool_events.py | Out-File -Encoding utf8 metropool.json
python scripts/decactus_events.py | Out-File -Encoding utf8 decactus.json
python scripts/oogst_events.py | Out-File -Encoding utf8 oogst.json
python scripts/hengelo_events.py | Out-File -Encoding utf8 hengelo.json
python scripts/dutch_holidays.py | Out-File -Encoding utf8 feestdagen.json

python scripts/fc_twente_ical.py --output fc-twente.ics
```

## curl
These requests are useful for inspecting the sources directly. Event extraction
still requires the Python scripts because the agenda response is HTML.

```bash
curl -L https://metropool.nl/agenda/
curl -L https://www.decactus.nl/agenda/
curl -L https://oogst.eu/agenda/
curl -L https://uitinhengelo.nl/agenda
curl -L https://fctwente.nl/wedstrijden/eerste-selectie
```

## Docs
- https://schema.org/Event
- https://metropool.nl/agenda/
- https://www.decactus.nl/agenda/
- https://oogst.eu/agenda/
- https://uitinhengelo.nl/agenda
- https://fctwente.nl/wedstrijden/eerste-selectie
