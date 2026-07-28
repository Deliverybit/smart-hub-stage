#!/usr/bin/env python3
"""Insert iPad 14 Pro Max-only sidebar CSS after the desktop block in all pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import IPAD_14_PRO_MAX_LAYOUT  # noqa: E402

MARKER = "/* ===== iPad 14 Pro Max only"

INSERT_AFTER_DESKTOP_RE = re.compile(
    r"(\s*/\* ===== TABLET \(769px–1366px\).*?\n    \})",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        block_re = re.compile(
            r"/\* ===== iPad 14 Pro Max only — full slide-in retract ===== \*/\s*"
            r"@media \(min-width: 1028px\).*?\n    \}\s*"
            r"@media \(min-width: 1370px\).*?\n    \}",
            re.S,
        )
        if not block_re.search(text):
            raise SystemExit(f"iPad 14 Pro Max marker found but block missing in {path.name}")
        text = block_re.sub(IPAD_14_PRO_MAX_LAYOUT.strip(), text, count=1)
    else:
        # Prefer inserting after desktop (1367px) block; fall back after tablet block.
        desktop_re = re.compile(
            r"/\* ===== TABLET \(769px–1366px\).*?\n    \}\s*"
            r"(?:/\* ===== Surface Duo only.*?\n    \}\s*)?"
            r"@media \(min-width: 1367px\) \{.*?\n    \}",
            re.S,
        )
        match = desktop_re.search(text)
        if not match:
            match = INSERT_AFTER_DESKTOP_RE.search(text)
        if not match:
            raise SystemExit(f"No desktop/tablet block found in {path.name}")
        insert_at = match.end()
        text = text[:insert_at] + "\n" + IPAD_14_PRO_MAX_LAYOUT + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for rel in [
        "app.py",
        "pages/7_Terms_of_Service.py",
        *[f"pages/{p.name}" for p in sorted((ROOT / "pages").glob("*_Top_10.py"))],
    ]:
        path = ROOT / rel
        patch_file(path)
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
