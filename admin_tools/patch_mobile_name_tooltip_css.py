#!/usr/bin/env python3
"""Remove legacy below-card company tooltip CSS from screener pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LEGACY_NAME_TIP_BLOCK_RE = re.compile(
    r"\s*html body \.stApp \[data-testid=\"stAppViewContainer\"\] \.stMarkdown "
    r"\.full-results-wrap \.full-results-table tbody td\[data-label=\"Company\"\], "
    r"\.full-results-wrap \.full-results-table tbody td\[data-label=\"Name\"\], "
    r"\.full-results-wrap \.full-results-table tbody td\[data-label=\"Commodity\"\] \{\s*"
    r"position: relative !important;\s*"
    r"\}\s*"
    r"html body \.stApp \[data-testid=\"stAppViewContainer\"\] \.stMarkdown "
    r"\.full-results-wrap \.full-results-table tbody td\[data-label=\"Company\"\] "
    r"\.fr-val \.tip-wrap:not\(\.headlines-tip\).*?"
    r"border-color: transparent transparent #1e1e2f transparent !important;\s*"
    r"\}\s*",
    re.S,
)

LEGACY_NAME_TIP_ACTIVE_RE = re.compile(
    r"\s*\.stMarkdown \.full-results-wrap \.full-results-table tbody tr\.scoop-name-tip-active \{.*?"
    r"\}\s*"
    r"\[data-testid=\"stMarkdownContainer\"\]:has\(tr\.scoop-name-tip-active\) \{.*?"
    r"overflow: visible !important;\s*"
    r"\}\s*",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    text = LEGACY_NAME_TIP_BLOCK_RE.sub("\n", text)
    text = LEGACY_NAME_TIP_ACTIVE_RE.sub("\n", text)
    path.write_text(text, encoding="utf-8")
    removed = original != text
    print(f"{'cleaned' if removed else 'unchanged'} {path.name}")


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
