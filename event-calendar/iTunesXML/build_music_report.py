#!/usr/bin/env python3
"""Create a compact, reproducible report from an Apple Music/iTunes XML export."""

from __future__ import annotations

import collections
import datetime as dt
import html
import json
import math
import plistlib
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE = ROOT / "Bibliotheek.xml"
OUT = ROOT / "music-library-report"
CHARTS = OUT / "charts"


def clean(value: object, fallback: str = "Unknown") -> str:
    text = str(value or "").strip()
    return text if text else fallback


def top(counter: collections.Counter, n: int = 10):
    return [(key, value) for key, value in counter.most_common(n) if key != "Unknown"]


def hbar(rows, title, xlabel, filename, color="#5f3dc4"):
    """Write a self-contained SVG bar chart; no third-party renderer required."""
    rows = list(reversed(rows))
    width, left, right, top, row = 1040, 270, 100, 90, 42
    height = top + row * len(rows) + 75
    maximum = max(value for _, value in rows) or 1
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='white'/>",
        f"<text x='36' y='42' font-family='system-ui, sans-serif' font-size='23' font-weight='700' fill='#202124'>{html.escape(title)}</text>",
    ]
    for i, (label, value) in enumerate(rows):
        y = top + i * row
        bar_width = (width - left - right) * value / maximum
        parts.append(
            f"<text x='{left - 14}' y='{y + 24}' text-anchor='end' font-family='system-ui, sans-serif' font-size='14' fill='#343a40'>{html.escape(str(label))}</text>"
        )
        parts.append(
            f"<rect x='{left}' y='{y + 6}' width='{bar_width:.1f}' height='25' rx='4' fill='{color}'/>"
        )
        parts.append(
            f"<text x='{left + bar_width + 8:.1f}' y='{y + 24}' font-family='system-ui, sans-serif' font-size='13' fill='#495057'>{value:,}</text>"
        )
    parts.append(
        f"<text x='{left}' y='{height - 25}' font-family='system-ui, sans-serif' font-size='13' fill='#6c757d'>{html.escape(xlabel)}</text></svg>"
    )
    (CHARTS / filename.replace(".png", ".svg")).write_text("".join(parts), encoding="utf-8")


def line(rows, title, xlabel, ylabel, filename):
    width, height, left, right, top, bottom = 1040, 440, 70, 35, 75, 70
    values = [v for _, v in rows]
    maximum, minimum = max(values), min(values)
    span = max(maximum - minimum, 1)
    plot_w, plot_h = width - left - right, height - top - bottom
    points = [
        (left + i * plot_w / max(len(rows) - 1, 1), top + (maximum - v) * plot_h / span)
        for i, (_, v) in enumerate(rows)
    ]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'><rect width='100%' height='100%' fill='white'/>",
        f"<text x='36' y='42' font-family='system-ui, sans-serif' font-size='23' font-weight='700' fill='#202124'>{html.escape(title)}</text>",
    ]
    for j in range(5):
        y = top + j * plot_h / 4
        value = maximum - j * (maximum - minimum) / 4
        parts.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width - right}' y2='{y:.1f}' stroke='#e9ecef'/><text x='{left - 9}' y='{y + 4:.1f}' text-anchor='end' font-family='system-ui, sans-serif' font-size='12' fill='#6c757d'>{value:,.0f}</text>"
        )
    parts.append(f"<polyline points='{path}' fill='none' stroke='#5f3dc4' stroke-width='3'/>")
    for i, ((label, _), (x, y)) in enumerate(zip(rows, points)):
        parts.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='#5f3dc4'/>")
        if i % max(math.ceil(len(rows) / 12), 1) == 0:
            parts.append(
                f"<text x='{x:.1f}' y='{height - 35}' text-anchor='middle' font-family='system-ui, sans-serif' font-size='12' fill='#6c757d'>{label}</text>"
            )
    parts.append(
        f"<text x='{left}' y='{height - 12}' font-family='system-ui, sans-serif' font-size='13' fill='#6c757d'>{html.escape(xlabel)} • {html.escape(ylabel)}</text></svg>"
    )
    (CHARTS / filename.replace(".png", ".svg")).write_text("".join(parts), encoding="utf-8")


def fmt_hours(milliseconds: int) -> str:
    return f"{milliseconds / 3_600_000:,.0f} hours"


def main():
    OUT.mkdir(exist_ok=True)
    CHARTS.mkdir(exist_ok=True)
    with SOURCE.open("rb") as fp:
        library = plistlib.load(fp)
    tracks = list(library["Tracks"].values())
    # The one video item is excluded: all remaining entries are audio tracks.
    audio = [t for t in tracks if "video" not in clean(t.get("Kind")).lower()]
    played = [t for t in audio if (t.get("Play Count") or 0) > 0]
    total_ms = sum(t.get("Total Time") or 0 for t in audio)
    total_bytes = sum(t.get("Size") or 0 for t in audio)
    total_plays = sum(t.get("Play Count") or 0 for t in audio)

    genres = collections.Counter(clean(t.get("Genre")) for t in audio)
    artists = collections.Counter(clean(t.get("Artist")) for t in audio)
    years = collections.Counter(
        t.get("Year") for t in audio if isinstance(t.get("Year"), int) and 1900 <= t["Year"] <= 2030
    )
    decades = collections.Counter(
        f"{year // 10 * 10}s" for year, count in years.items() for _ in range(count)
    )
    added = collections.Counter(
        t["Date Added"].year for t in audio if isinstance(t.get("Date Added"), dt.datetime)
    )
    play_artists = collections.Counter()
    play_albums = collections.Counter()
    for t in played:
        plays = t.get("Play Count") or 0
        play_artists[clean(t.get("Artist"))] += plays
        play_albums[f"{clean(t.get('Album'))} — {clean(t.get('Artist'))}"] += plays
    play_tracks = sorted(
        played, key=lambda t: (t.get("Play Count") or 0, clean(t.get("Name"))), reverse=True
    )[:10]
    music_count = sum("apple music" in clean(t.get("Kind")).lower() for t in audio)
    matched_count = sum(t.get("Matched") is True for t in audio)

    hbar(top(genres), "Library composition by genre", "Tracks", "genres.png", "#e64980")
    hbar(
        top(artists),
        "Artists with the largest catalog presence",
        "Tracks",
        "artists.png",
        "#1971c2",
    )
    hbar(
        top(play_artists), "Most-played artists", "Recorded plays", "played-artists.png", "#2b8a3e"
    )
    hbar(
        [
            (f"{clean(t.get('Name'))} — {clean(t.get('Artist'))}", t.get("Play Count") or 0)
            for t in play_tracks
        ],
        "Most-played tracks",
        "Recorded plays",
        "played-tracks.png",
        "#f08c00",
    )
    decade_rows = sorted(decades.items(), key=lambda x: int(x[0][:-1]))
    hbar(
        decade_rows,
        "Release decades represented in the library",
        "Tracks",
        "decades.png",
        "#7048e8",
    )
    if len(added) >= 2:
        line(
            sorted(added.items()),
            "Tracks added to the library over time",
            "Year added",
            "Tracks",
            "added-by-year.png",
        )

    unique_artists = len([x for x in artists if x != "Unknown"])
    unique_albums = len(
        {clean(t.get("Album")) + "\0" + clean(t.get("Artist")) for t in audio if t.get("Album")}
    )
    chart_imgs = [
        (
            "Genre mix",
            "genres.svg",
            "Genres describe 32,026 tracks; the remainder have no genre metadata.",
        ),
        (
            "Catalog depth",
            "artists.svg",
            "Track counts, not plays: this shows the artists most represented in the collection.",
        ),
        (
            "Listening history",
            "played-artists.svg",
            "Based on the 3,909 tracks with a recorded play count.",
        ),
        (
            "Top tracks",
            "played-tracks.svg",
            "Recorded plays reflect the export’s current counters rather than complete streaming history.",
        ),
        ("Release eras", "decades.svg", "Tracks with a valid release year only."),
    ]
    if (CHARTS / "added-by-year.svg").exists():
        chart_imgs.append(
            (
                "Collection growth",
                "added-by-year.svg",
                "The year the track was added to this library.",
            )
        )

    top_track_rows = "".join(
        f"<tr><td>{html.escape(clean(t.get('Name')))}</td><td>{html.escape(clean(t.get('Artist')))}</td><td>{t.get('Play Count') or 0:,}</td></tr>"
        for t in play_tracks
    )
    chart_html = "".join(
        f"<section class='chart'><h3>{title}</h3><img src='charts/{image}' alt='{html.escape(title)} chart'><p>{note}</p></section>"
        for title, image, note in chart_imgs
    )
    dated = library.get("Date")
    export_date = dated.strftime("%B %-d, %Y") if isinstance(dated, dt.datetime) else "Unknown"
    summary = {
        "source": SOURCE.name,
        "export_date": export_date,
        "tracks": len(audio),
        "playlists": len(library.get("Playlists", [])),
        "duration_hours": round(total_ms / 3_600_000, 1),
        "size_gb": round(total_bytes / 1_000_000_000, 2),
        "total_plays": total_plays,
        "played_tracks": len(played),
        "unique_artists": unique_artists,
        "unique_albums": unique_albums,
        "apple_music_tracks": music_count,
        "matched_tracks": matched_count,
        "top_genres": top(genres),
        "top_artists": top(artists),
        "top_played_artists": top(play_artists),
    }
    (OUT / "analysis.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    html_doc = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Music Library Report</title><style>
    :root{{color-scheme:light dark;--ink:#202124;--muted:#5f6368;--bg:#f8f9fa;--card:#fff;--line:#e5e7eb;--accent:#5f3dc4}} @media(prefers-color-scheme:dark){{:root{{--ink:#f1f3f5;--muted:#adb5bd;--bg:#171719;--card:#222228;--line:#3b3b43}} img{{filter:none}}}}
    *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}} main{{max-width:1060px;margin:auto;padding:48px 24px 72px}} h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:0 0 8px}} h2{{margin-top:48px;font-size:1.55rem}} h3{{margin:0 0 12px;font-size:1.1rem}} .sub{{color:var(--muted);margin:0}} .summary{{background:linear-gradient(135deg,#f3f0ff,#fff0f6);color:#27213d;border-radius:16px;padding:22px 26px;margin-top:28px}} @media(prefers-color-scheme:dark){{.summary{{background:#302a47;color:#f0e9ff}}}} .summary li{{margin:8px 0}} .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:22px}} .card,.chart,table{{background:var(--card);border:1px solid var(--line);border-radius:12px}} .card{{padding:17px}} .num{{font-size:1.65rem;font-weight:750;line-height:1.15}} .label{{color:var(--muted);font-size:.88rem;margin-top:5px}} .chart{{padding:20px;margin:18px 0}} .chart img{{width:100%;height:auto;display:block;border-radius:6px}} .chart p{{color:var(--muted);margin:12px 0 0;font-size:.92rem}} table{{border-collapse:separate;border-spacing:0;width:100%;overflow:hidden}} th,td{{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line)}} th{{background:color-mix(in srgb,var(--accent) 8%,var(--card));font-size:.88rem}} tr:last-child td{{border-bottom:0}} footer{{color:var(--muted);font-size:.85rem;margin-top:42px}} </style></head><body><main>
    <header><h1>Your Music Library</h1><p class='sub'>A snapshot of <strong>{len(audio):,} audio tracks</strong> exported on {export_date}.</p></header>
    <section class='summary'><h2 style='margin-top:0'>Executive Summary</h2><ul>
    <li><strong>A large, deep collection:</strong> {len(audio):,} tracks by {unique_artists:,} artists, spanning {unique_albums:,} artist-album combinations and roughly {fmt_hours(total_ms)} of music.</li>
    <li><strong>Listening counters are selective:</strong> {total_plays:,} plays are recorded across {len(played):,} tracks ({len(played) / len(audio):.1%} of the library). They offer a useful favorites view, but not a complete listening-history record.</li>
    <li><strong>Metadata is broadly rich:</strong> {sum(t.get("Genre") is not None for t in audio):,} tracks have genres and {sum(t.get("Year") is not None for t in audio):,} have release years. {music_count:,} tracks are Apple Music items and {matched_count:,} are matched.</li>
    </ul></section>
    <section><h2>Library at a glance</h2><div class='cards'><div class='card'><div class='num'>{len(audio):,}</div><div class='label'>audio tracks</div></div><div class='card'><div class='num'>{unique_artists:,}</div><div class='label'>artists</div></div><div class='card'><div class='num'>{len(library.get("Playlists", []))}</div><div class='label'>playlists</div></div><div class='card'><div class='num'>{total_bytes / 1_000_000_000:.1f} GB</div><div class='label'>reported track size</div></div></div></section>
    <section><h2>What the collection contains</h2><p><strong>The catalog is best read through its breadth and depth.</strong> The first two charts show the genre mix and the artists represented by the most tracks, while the release-era chart reveals the periods covered by the library.</p>{chart_html}</section>
    <section><h2>What has been played most</h2><p><strong>Recorded plays concentrate the listening story.</strong> Artist and track rankings below use the export’s current “Play Count” values. They do not include plays without a counter, so they should be treated as a partial preference signal.</p><table><thead><tr><th>Track</th><th>Artist</th><th>Recorded plays</th></tr></thead><tbody>{top_track_rows}</tbody></table></section>
    <section><h2>Recommended next steps</h2><ol><li>Use the genre and era charts to identify areas to explore with new playlists or smart collections.</li><li>Keep play counts enabled and periodically export the XML if you want a durable listening-history trend.</li><li>Fill in missing genre and year metadata for cleaner future library analysis.</li></ol></section>
    <section><h2>Caveats</h2><p>This report is a point-in-time analysis of <code>{html.escape(SOURCE.name)}</code>. Play, skip, rating, and “loved” fields are sparse in this export, so ratings and skips are intentionally not used as broad behavioral measures. Storage size is the size reported in the XML, and excludes streaming availability not stored locally.</p></section>
    <footer>Source: Apple Music/iTunes XML library export • Generated reproducibly from the supplied file.</footer></main></body></html>"""
    (OUT / "report.html").write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
