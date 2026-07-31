# Dutch events and FC Twente calendar

## Overview
The repository includes three ready-to-run Python scripts:

- `scripts/metropool_events.py` reads the public Metropool agenda and emits its
  embedded schema.org events as JSON.
- `scripts/decactus_events.py` does the same for the De Cactus agenda.
- `scripts/fc_twente_ical.py` reads FC Twente's public fixture page and writes
  every published schema.org event to an iCalendar (`.ics`) file. This needs no
  account or API key and does not filter by competition, so published Eredivisie,
  European, and KNVB Beker matches are retained.

The venue websites do not advertise a stable public API. Their scripts therefore
consume the machine-readable JSON-LD already published with each agenda page.
Website markup can change; use `--url` if a page moves. All three commands also
accept `--input PAGE.html`, which is useful for parsing a page downloaded in a
browser or for scheduled processing without another HTTP request. Network and
HTTP failures produce a short command-line error instead of a Python traceback.

## Python
No third-party Python packages are needed. From the repository root, run:

```bash
python scripts/metropool_events.py > metropool.json
python scripts/decactus_events.py > decactus.json

python scripts/fc_twente_ical.py --output fc-twente.ics
```

To process downloaded pages instead, pass (for example)
`--input downloads/metropool.html`. The source website controls how far ahead its
page lists events.

## PowerShell
PowerShell can invoke the same keyless scripts:

```powershell
python scripts/metropool_events.py | Out-File -Encoding utf8 metropool.json
python scripts/decactus_events.py | Out-File -Encoding utf8 decactus.json

python scripts/fc_twente_ical.py --output fc-twente.ics
```

## curl
These requests are useful for inspecting the sources directly. Event extraction
still requires the Python scripts because the agenda response is HTML.

```bash
curl -L https://metropool.nl/agenda/
curl -L https://www.decactus.nl/agenda/
curl -L https://www.fctwente.nl/teams/eerste-selectie/wedstrijden
```

## Docs
- https://schema.org/Event
- https://metropool.nl/agenda/
- https://www.decactus.nl/agenda/
- https://www.fctwente.nl/teams/eerste-selectie/wedstrijden
