#!/usr/bin/env python3
"""Insert Asus Zenbook Fold-only layout CSS after the iPad 14 Pro Max block."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import (  # noqa: E402
    ASUS_ZENBOOK_FOLD_SCREENER_LAYOUT,
    ASUS_ZENBOOK_FOLD_SEARCH_LAYOUT,
    ASUS_ZENBOOK_FOLD_TERMS_LAYOUT,
)

MARKER = "/* ===== Asus Zenbook Fold only"

IPAD_14_BLOCK_RE = re.compile(
    r"/\* ===== iPad 14 Pro Max only — full slide-in retract ===== \*/\s*"
    r"@media \(min-width: 1028px\).*?\n    \}\s*"
    r"@media \(min-width: 1370px\).*?\n    \}",
    re.S,
)


ZENBOOK_BLOCK_RE = re.compile(
    r"/\* ===== Asus Zenbook Fold only — (?:iPad Mini-style overlay \(folded\)|folded tablet layout) ===== \*/\s*"
    r"@media \(min-width: 849px\).*?"
    r"/\* ===== Asus Zenbook Fold only — (?:iPad Mini-style overlay \(unfolded\)|unfolded tablet layout) ===== \*/\s*"
    r"@media \(min-width: 1700px\).*?\n    \}",
    re.S,
)


def patch_file(path: Path, layout: str) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        if not ZENBOOK_BLOCK_RE.search(text):
            raise SystemExit(f"Zenbook marker found but block missing in {path.name}")
        text = ZENBOOK_BLOCK_RE.sub(layout.strip(), text, count=1)
    else:
        match = IPAD_14_BLOCK_RE.search(text)
        if not match:
            raise SystemExit(f"No iPad 14 Pro Max block found in {path.name}")
        insert_at = match.end()
        text = text[:insert_at] + "\n" + layout + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for rel, layout in [
        ("app.py", ASUS_ZENBOOK_FOLD_SEARCH_LAYOUT),
        ("pages/7_Terms_of_Service.py", ASUS_ZENBOOK_FOLD_TERMS_LAYOUT),
        *[(f"pages/{p.name}", ASUS_ZENBOOK_FOLD_SCREENER_LAYOUT) for p in sorted((ROOT / "pages").glob("*_Top_10.py"))],
    ]:
        patch_file(ROOT / rel, layout)
        print(f"patched {Path(rel).name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
