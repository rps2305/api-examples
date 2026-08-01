"""Explainable music-taste matching for agenda events."""

from __future__ import annotations

import re
import unicodedata


# Strong signals from the supplied Music/iTunes library and the user's stated
# Torhout/Werchter affinity. Labels are kept human-readable for the UI reason.
FAVORED_ARTISTS = (
    "The Beatles",
    "Maite Hontelé",
    "Manu Chao",
    "Nick Cave",
    "Florence + The Machine",
    "Buena Vista Social Club",
    "Lana Del Rey",
    "David Bowie",
    "Bruce Springsteen",
    "Radiohead",
    "Pixies",
    "R.E.M.",
    "The Cure",
    "Foo Fighters",
    "New Order",
    "Massive Attack",
    "The Prodigy",
    "The Chemical Brothers",
    "Depeche Mode",
    "Tool",
    "Muse",
    "Oasis",
    "Metallica",
    "Rammstein",
    "Arctic Monkeys",
    "Editors",
    "U2",
    "The Rolling Stones",
    "Tori Amos",
    "Pink Floyd",
    "Simple Minds",
    "Cocteau Twins",
    "Nirvana",
    "Doe Maar",
    "Celia Cruz",
    "Fratsen",
    "Red Hot Chili Peppers",
    "Antimatter",
    "Shantel",
    "Ooostblok",
    "Arrested Development",
    "Public Enemy",
    "Body Count",
    "Bodycount",
    "De La Soul",
    "Delinquent Habits",
)

# Explicit negative preferences always win over broad genre or festival matches.
EXCLUDED_ARTISTS = ("Pearl Jam",)

STYLE_SIGNALS = (
    ("alternative", 3, "alternative rock"),
    ("new wave", 3, "new wave"),
    ("post punk", 3, "postpunk"),
    ("latin", 3, "latin"),
    ("salsa", 3, "latin"),
    ("cumbia", 3, "latin"),
    ("tropical", 3, "tropische muziek"),
    ("reggae", 3, "reggae"),
    ("balkan", 3, "Balkanbeats"),
    ("latin hip hop", 4, "Latin hiphop"),
    ("old school hip hop", 4, "old-school hiphop"),
    ("old school hiphop", 4, "old-school hiphop"),
    ("rap metal", 3, "rapmetal"),
    ("world", 3, "wereldmuziek"),
    ("indie", 2, "indie"),
    ("electronic", 2, "elektronische muziek"),
    ("singer songwriter", 2, "singer-songwriter"),
    ("old school", 2, "old school"),
    ("hip hop", 1, "hiphop"),
    ("hiphop", 1, "hiphop"),
    ("ska", 2, "ska"),
    ("hardcore", 2, "hardcore"),
    ("punk", 2, "punk"),
    ("industrial", 2, "industrial"),
    ("hard rock", 2, "hardrock"),
    ("rock", 1, "rock"),
    ("metal", 1, "metal"),
    ("blues", 1, "blues"),
)


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    return f" {normalize(phrase)} " in f" {text} "


def taste_recommendation(event: dict[str, object]) -> str | None:
    """Return a concise recommendation reason only for a confident music match."""
    if event.get("source") in {"fc-twente", "feestdagen"} or str(event.get("@type")) == "SportsEvent":
        return None

    title = normalize(event.get("name"))
    context = normalize(f"{event.get('name', '')} {event.get('genre', '')}")
    if any(contains_phrase(title, artist) for artist in EXCLUDED_ARTISTS):
        return None
    for artist in FAVORED_ARTISTS:
        if contains_phrase(title, artist):
            punctuation = "" if artist.endswith(".") else "."
            return f"Sluit aan bij je voorkeur voor {artist}{punctuation}"

    score = 0
    labels: list[str] = []
    for phrase, weight, label in STYLE_SIGNALS:
        if contains_phrase(context, phrase):
            score += weight
            if label not in labels:
                labels.append(label)
    if score < 3:
        return None
    joined = " en ".join(labels[:2])
    return f"Past bij je smaak voor {joined}."
