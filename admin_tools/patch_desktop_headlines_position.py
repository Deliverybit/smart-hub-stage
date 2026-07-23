#!/usr/bin/env python3
"""Position desktop headlines popup beside the quantity count in the table."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: block !important;
            position: fixed !important;
            left: auto !important;
            right: max(0.75rem, env(safe-area-inset-right, 0px)) !important;
            top: max(0.75rem, env(safe-area-inset-top, 0px)) !important;
            bottom: auto !important;
            transform: none !important;
            /* Same top-down panel every row so scroll position does not move it */
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-pop-w) !important;
            min-width: var(--hl-pop-w) !important;
            max-width: var(--hl-pop-w) !important;
            height: var(--hl-pop-h) !important;
            min-height: var(--hl-pop-h) !important;
            max-height: var(--hl-pop-h) !important;"""

NEW = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: block !important;
            position: absolute !important;
            left: auto !important;
            right: 0 !important;
            top: auto !important;
            bottom: calc(100% + 10px) !important;
            transform: none !important;
            /* Popup sits just above the Headlines count in the row */
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-pop-w) !important;
            min-width: var(--hl-pop-w) !important;
            max-width: var(--hl-pop-w) !important;
            height: auto !important;
            min-height: 0 !important;
            max-height: var(--hl-pop-h) !important;"""

OLD_SUPPORTS = """        @supports (position-anchor: auto) {
            .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
                left: auto !important;
                right: max(0.75rem, env(safe-area-inset-right, 0px)) !important;
                top: max(0.75rem, env(safe-area-inset-top, 0px)) !important;
                transform: none !important;
            }
        }"""

NEW_SUPPORTS = """        @supports (position-anchor: auto) {
            .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
                left: anchor(right) !important;
                top: anchor(top) !important;
                right: auto !important;
                bottom: auto !important;
                transform: translate(0, calc(-100% - 10px)) !important;
            }
        }"""


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        if OLD not in text:
            raise SystemExit(f"Expected headlines popup block not found in {path.name}")
        text = text.replace(OLD, NEW, 1)
        if OLD_SUPPORTS in text:
            text = text.replace(OLD_SUPPORTS, NEW_SUPPORTS, 1)
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
