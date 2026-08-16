#!/usr/bin/env python3
"""Patch screener pages so mobile/tablet name tooltips stay on-screen."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import (  # noqa: E402
    NAME_VALUE_TOOLTIP_PAGE_MARKER,
    NAME_VALUE_TOOLTIP_PAGE_SNIPPET,
)

ANCHOR = """
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }"""

OLD_SNIPPET_BLOCK_RE = re.compile(
    r"/\* Name/Company/Commodity: tooltip below value \(avoids top-of-card clip\)\. \*/"
    r".*?"
    r"\.stMarkdown \.full-results-wrap:has\(tr\.scoop-name-tip-active\) \{\s*"
    r"overflow: visible !important;\s*"
    r"\}\s*",
    re.S,
)

SNIPPET_BLOCK_RE = re.compile(
    r"/\* Name/Company/Commodity: tooltip below value .*?\*/"
    r".*?"
    r"\.stMarkdown \.full-results-wrap:has\(tr\.scoop-name-tip-active\) \{\s*"
    r"overflow: visible !important;\s*"
    r"\}\s*",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = OLD_SNIPPET_BLOCK_RE.sub("", text)
    count = text.count(NAME_VALUE_TOOLTIP_PAGE_MARKER)
    if count > 3:
        text = SNIPPET_BLOCK_RE.sub("", text)
        count = 0
    if count == 3:
        path.write_text(text, encoding="utf-8")
        print(f"cleaned {path.name}")
        return
    if count > 0:
        path.write_text(text, encoding="utf-8")
        print(f"partial {path.name} ({count} blocks)")
        return
    if ANCHOR not in text:
        raise SystemExit(f"Anchor block not found in {path.name}")
    patched = text.replace(ANCHOR, ANCHOR + NAME_VALUE_TOOLTIP_PAGE_SNIPPET, text.count(ANCHOR))
    path.write_text(patched, encoding="utf-8")
    print(f"patched {path.name}")


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
