"""Convert the originals in IMAGES/ to responsive WebP files in assets/photos/.

Run from the event-calendar directory: `python3 build_photos.py`. It needs
ImageMagick (`magick`). Every photo is written at up to three widths and never
upscaled; photos.json records the generated widths and dimensions so the page
markup can emit srcset/sizes without guessing.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "IMAGES"
TARGET = ROOT / "assets" / "photos"
WIDTHS = (480, 960, 1600)
QUALITY = "76"

# slug, original file, caption (place and date from the file name / EXIF), alt text
PHOTOS = [
    ("simple-minds-amsterdamse-bos", "eerste-grote-concert-simple-minds-amsterdamse-bos.jpeg",
     "Mijn eerste grote concert: Simple Minds in het Amsterdamse Bos, 10 juni 1986",
     "Het podium van Simple Minds met een duif op het backdrop en publiek op de voorgrond"),
    ("sony-stereotoren-den-haag", "sony-stereotoren-kamer-denhaag-1991.jpeg",
     "Mijn kamer in Den Haag met Sony-stereotoren, 1991",
     "Een Sony-stereotoren met draaitafel in een studentenkamer, met een Metropool-poster aan de muur"),
    ("rock-torhout-podium-1998", "rock-torhout-stage-1998.jpeg",
     "Het hoofdpodium van Rock Torhout, 1998",
     "Het grote podium van Rock Torhout met een menigte met rode petjes ervoor"),
    ("rock-torhout-publiek-1998", "inhetpubliek-rock-torhout-1998.jpeg",
     "In het publiek bij Rock Torhout, 1998",
     "Twee festivalgangers met handdoeken om het hoofd zitten in het publiek op het grasveld"),
    ("rolling-stones-arena-1998", "rollingstones-1998-arena-amsterdam.jpeg",
     "The Rolling Stones in de Arena, Amsterdam, 1998",
     "Een enorm stadionpodium met vuur en rook tijdens een concert van The Rolling Stones, de tribunes vol publiek"),
    ("within-temptation-dynamo-1998", "within-temtation-op-dynamo-open-air-1998.jpeg",
     "Within Temptation op Dynamo Open Air, 1998",
     "Zangeres in een zwarte jurk op het podium van Dynamo Open Air, met cameraman naast het podium"),
    ("metropool-wemenstraat", "metropool-wemenstraat.jpeg",
     "Metropool aan de Wemenstraat in Hengelo",
     "Het oude Metropool-gebouw aan de Wemenstraat met bestelbus en auto ervoor"),
    ("festival-tentjes", "altijd-klein-tentje-op-festivals.jpeg",
     "Altijd een klein tentje op festivals",
     "Een veld vol kleine koepeltenten op een festivalcamping"),
    ("tindersticks-dublin-1997", "dublin-ireland-tindersticks-1997.jpeg",
     "Tindersticks in Dublin, Ierland, 1997",
     "Tindersticks op een podium met blauw en wit licht, de band staat in een halve cirkel"),
    ("amy-winehouse-werchter-2007", "rock-werchter-amy-winehouse.jpeg",
     "Amy Winehouse op Rock Werchter, 30 juni 2007",
     "Het podium van Rock Werchter met grote beelden van Amy Winehouse en het publiek ervoor"),
    ("zwarte-cross-hoofdpodium-2016", "zwarte-crosshoofdpodium.jpeg",
     "Het hoofdpodium van Zwarte Cross, 22 juli 2016",
     "Het kleurrijke hoofdpodium van Zwarte Cross met de tekst Say yes to apartheid en publiek ervoor"),
    ("paul-mccartney-werchter-2016", "Rock-werchter-2016-paul-mccartney.jpeg",
     "Paul McCartney op Rock Werchter, 30 juni 2016",
     "Het hoofdpodium van Rock Werchter bij avondlicht met Paul McCartney op de grote schermen"),
    ("metropool-ruskaja-2017", "metropool-enschede-ruskaja.jpeg",
     "Ruskaja in Metropool Enschede, 30 september 2017",
     "Een band op een rood verlicht podium met uitgelaten publiek met opgestoken handen"),
    ("booster-festival-2019", "eenmalig-vrijwilleger-booster-festival-enschede.jpeg",
     "Eenmalig vrijwilliger bij Booster Festival, Enschede, 6 april 2019",
     "Zwart-witportret van een man met bril die een bordje met Poppunt Overijssel vasthoudt"),
    ("muse-ziggodome-2019", "ziggodome-amsterdam-muse.jpeg",
     "Muse in de Ziggodome, Amsterdam, 12 september 2019",
     "Groene laserstralen boven het publiek in de Ziggodome tijdens een concert van Muse"),
    ("cactus-acdc-tribute-2021", "cafe-cactus-hengelo-acdc-tribute-all-female-ukrain.jpeg",
     "AC/DC-tribute door een all-female band uit Oekraïne in Café De Cactus, Hengelo, 16 oktober 2021",
     "Vier vrouwelijke muzikanten in leer op het kleine podium van Café De Cactus onder discoballen"),
    ("cactus-sweethearts-2025", "cafe-cactus-biiter-sweethearts-from-usa.jpeg",
     "Bitter Sweethearts uit de VS in Café De Cactus, Hengelo, 3 april 2025",
     "Een blonde zangeres in een glinsterend jurkje en een band in het gezellige Café De Cactus"),
    ("de-nul-2026", "alternatief-obscuur-maar-ook-geliefd-bij-een-hoop-hengeloers-bar-de-nul-aan-de-beekstraat.jpeg",
     "Alternatief, obscuur, maar ook geliefd bij een hoop Hengeloërs: bar De Nul aan de Beekstraat, maart 2026",
     "De gevel van bar De Nul in Hengelo met graffiti en een blauwe lucht"),
    ("oogst-hengelo-2026", "avond-op-oogst-hengelo.jpeg",
     "Een avond op Oogst in Hengelo, 23 mei 2026",
     "Een avondsfeer op Oogst met lichtsnoeren, een groene toren en bezoekers op het terrein"),
    ("dauwpop-sugababes-2026", "dauwpop-2026-sugababes.jpeg",
     "Sugababes op Dauwpop, 30 mei 2026",
     "Drie zangeressen met een bassist op het podium van Dauwpop, met een telefoon op de voorgrond"),
    ("zwarte-cross-reggaeweide-2026", "zwarecross-reggaeweide.jpeg",
     "De Reggaeweide op Zwarte Cross, 19 juli 2026",
     "Een podium met een regenboogboog in reggaekleuren en publiek met kleurrijke hoeden ervoor"),
]


def convert() -> dict[str, dict[str, object]]:
    TARGET.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict[str, object]] = {}
    for slug, original, caption, alt in PHOTOS:
        source = SOURCE / original
        info = subprocess.run(
            ["magick", "identify", "-auto-orient", "-format", "%w %h", f"{source}[0]"],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        width, height = int(info[0]), int(info[1])
        widths = [w for w in WIDTHS if w < width] + [min(width, WIDTHS[-1])]
        widths = sorted(set(widths))
        for target_width in widths:
            subprocess.run(
                ["magick", str(source), "-auto-orient", "-strip", "-resize", f"{target_width}x>",
                 "-quality", QUALITY, "-define", "webp:method=6", str(TARGET / f"{slug}-{target_width}.webp")],
                check=True,
            )
        manifest[slug] = {
            "caption": caption, "alt": alt, "widths": widths,
            "width": widths[-1], "height": round(height * widths[-1] / width),
        }
    (TARGET / "photos.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = convert()
    print(f"Wrote {sum(len(p['widths']) for p in result.values())} files for {len(result)} photos in {TARGET}")
