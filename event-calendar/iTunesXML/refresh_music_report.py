#!/usr/bin/env python3
"""Refresh Bibliotheek.xml from Music, then rebuild the HTML report.

Usage: python3 refresh_music_report.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.resolve()


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "export_music_library.py"), str(ROOT)], check=True)
    subprocess.run([sys.executable, str(ROOT / "build_music_report.py")], cwd=ROOT, check=True)
    print(ROOT / "music-library-report" / "report.html")


if __name__ == "__main__":
    main()
