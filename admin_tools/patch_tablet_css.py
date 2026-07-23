#!/usr/bin/env python3
"""Tablet-only CSS (769px-1366px) using mobile card layout on screeners."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import (  # noqa: E402
    TABLET_SCREENER_MOBILE_LAYOUT,
    TABLET_SEARCH_MOBILE_LAYOUT,
    TABLET_SIDEBAR,
    TABLET_TERMS_MOBILE_LAYOUT,
)

TABLET_SCREENER = f"""
    /* ===== TABLET (769px–1366px) — mobile card layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {{
{TABLET_SIDEBAR}
{TABLET_SCREENER_MOBILE_LAYOUT}
    }}
"""

TABLET_SEARCH = f"""
    /* ===== TABLET (769px–1366px) — mobile card layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {{
{TABLET_SIDEBAR}
{TABLET_SEARCH_MOBILE_LAYOUT}
    }}
"""

TABLET_TERMS = f"""
    /* ===== TABLET (769px–1366px) — mobile-style layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {{
{TABLET_SIDEBAR}
{TABLET_TERMS_MOBILE_LAYOUT}
    }}
"""

TABLET_BLOCK_RE = re.compile(
    r"/\* ===== TABLET.*? ===== \*/\s*@media \(min-width: 769px\) and \(max-width: \d+px\) \{.*?\n    \}",
    re.S,
)


def patch_file(path: Path, tablet_css: str) -> None:
    text = path.read_text(encoding="utf-8")
    if not TABLET_BLOCK_RE.search(text):
        raise SystemExit(f"No tablet block found in {path.name}")
    text = TABLET_BLOCK_RE.sub(tablet_css.strip(), text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_file(ROOT / "app.py", TABLET_SEARCH)
    print("patched app.py")
    patch_file(ROOT / "pages" / "7_Terms_of_Service.py", TABLET_TERMS)
    print("patched 7_Terms_of_Service.py")
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path, TABLET_SCREENER)
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
