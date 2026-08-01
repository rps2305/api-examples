#!/usr/bin/env python3
"""Export the complete Apple Music library to a replaceable XML file.

Usage:
    python3 export_music_library.py [destination-directory]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    destination = (
        Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent).expanduser().resolve()
    )
    if not destination.is_dir():
        raise SystemExit(f"Destination folder does not exist: {destination}")

    output = destination / "Bibliotheek.xml"
    temporary = destination / ".Bibliotheek.new.xml"
    temporary.unlink(missing_ok=True)
    script = """on run argv
set exportFile to POSIX file (item 1 of argv)
tell application "Music"
    activate
    export library playlist 1 as XML to exportFile
end tell
end run"""
    subprocess.run(["osascript", "-e", script, str(temporary)], check=True)

    # Confirm that Music produced a plist/XML library rather than a playlist text export.
    subprocess.run(["plutil", "-lint", str(temporary)], check=True)
    temporary.replace(output)
    print(output)


if __name__ == "__main__":
    main()
