#!/usr/bin/env python3
"""Validate documentation consistency for this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
README = REPO_ROOT / "README.md"
README_LINK_RE = re.compile(r'href="(docs/[^"]+\.md)"')
ALLOWED_UNINDEXED_DOCS = {"docs/NOTFOUND.md"}


def main() -> int:
    errors: list[str] = []

    readme_text = README.read_text(encoding="utf-8")
    readme_links = set(README_LINK_RE.findall(readme_text))
    docs_files = {f"docs/{path.name}" for path in DOCS_DIR.glob("*.md")}

    missing_files = sorted(readme_links - docs_files)
    if missing_files:
        errors.append(
            "README links to docs that do not exist: " + ", ".join(missing_files)
        )

    unindexed_docs = sorted(docs_files - readme_links - ALLOWED_UNINDEXED_DOCS)
    if unindexed_docs:
        errors.append(
            "Docs files not listed in README index: " + ", ".join(unindexed_docs)
        )

    for doc_path in sorted(DOCS_DIR.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        first_non_empty = next((line for line in text.splitlines() if line.strip()), "")
        if not first_non_empty.startswith("# "):
            errors.append(
                f"{doc_path.relative_to(REPO_ROOT)} must start with a level-1 heading"
            )

    if errors:
        print("Validation failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed: README index and docs files are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
