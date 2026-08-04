#!/usr/bin/env python3
"""Insert phone sidebar CSS (≤743px) before the iPad Mini block in all pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import PHONE_SIDEBAR_LAYOUT  # noqa: E402

PHONE_MARKER = "/* ===== Phone mobile (≤743px)"
IPAD_MINI_MARKER = "/* ===== iPad Mini portrait (744px–768px)"

PHONE_BLOCK_RE = re.compile(
    r"/\* ===== Phone mobile \(≤743px\).*?\n    \}",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if PHONE_MARKER in text:
        if not PHONE_BLOCK_RE.search(text):
            raise SystemExit(f"Phone marker found but block missing in {path.name}")
        text = PHONE_BLOCK_RE.sub(PHONE_SIDEBAR_LAYOUT.strip(), text, count=1)
    elif IPAD_MINI_MARKER not in text:
        raise SystemExit(f"No iPad Mini block found in {path.name}")
    else:
        text = text.replace(
            IPAD_MINI_MARKER,
            PHONE_SIDEBAR_LAYOUT.strip() + "\n\n    " + IPAD_MINI_MARKER,
            1,
        )
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
