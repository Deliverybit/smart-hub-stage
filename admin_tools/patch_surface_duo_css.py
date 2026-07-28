#!/usr/bin/env python3
"""Insert Surface Duo-only sidebar CSS after the tablet block in all pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import SURFACE_DUO_LAYOUT  # noqa: E402

MARKER = "/* ===== Surface Duo only"

INSERT_AFTER_TABLET_RE = re.compile(
    r"(\s*/\* ===== TABLET \(769px–1366px\).*?\n    \})",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        block_re = re.compile(
            r"/\* ===== Surface Duo only — full slide-in, mobile-style arrows ===== \*/\s*"
            r"@media \(width: 540px\).*?\n    \}",
            re.S,
        )
        if not block_re.search(text):
            raise SystemExit(f"Surface Duo marker found but block missing in {path.name}")
        text = block_re.sub(SURFACE_DUO_LAYOUT.strip(), text, count=1)
    else:
        match = INSERT_AFTER_TABLET_RE.search(text)
        if not match:
            raise SystemExit(f"No tablet block found in {path.name}")
        insert_at = match.end()
        text = text[:insert_at] + "\n" + SURFACE_DUO_LAYOUT + text[insert_at:]
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
