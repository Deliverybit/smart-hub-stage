#!/usr/bin/env python3
"""Highlight Headlines column header on desktop when row headlines are hovered."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS_NEW = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
            color: #ffffff !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }
        @supports (position-anchor: auto) {"""

CSS_OLD = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
            color: #ffffff !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }
        .full-results-wrap .full-results-table:has(tbody .tip-wrap.headlines-tip:hover) thead th.fr-col-headlines,
        .full-results-wrap .full-results-table:has(tbody .tip-wrap.headlines-tip:hover) thead th.fr-col-headlines .tip-wrap,
        .full-results-wrap .full-results-table:has(tbody .tip-wrap.headlines-tip .tip-text:hover) thead th.fr-col-headlines,
        .full-results-wrap .full-results-table:has(tbody .tip-wrap.headlines-tip .tip-text:hover) thead th.fr-col-headlines .tip-wrap {
            color: #93c5fd !important;
        }
        @supports (position-anchor: auto) {"""

PY_NEW = """                if tip:
                    header_cells += f'<th>{_tip(c, tip, f"--frh-{idx_col}")}</th>'"""

PY_OLD = """                if tip:
                    if c == "Headlines":
                        header_cells += f'<th class="fr-col-headlines">{_tip(c, tip, f"--frh-{idx_col}")}</th>'
                    else:
                        header_cells += f'<th>{_tip(c, tip, f"--frh-{idx_col}")}</th>'"""


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        if "--hl-pop-w" not in text:
            continue
        if CSS_OLD not in text:
            raise SystemExit(f"CSS block not found in {path.name}")
        if PY_OLD not in text:
            raise SystemExit(f"Python block not found in {path.name}")
        text = text.replace(CSS_OLD, CSS_NEW).replace(PY_OLD, PY_NEW)
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
