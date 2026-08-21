#!/usr/bin/env python3
"""Verify home entry routing (desktop NYSE vs mobile/tablet sidebar)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import landing_page  # noqa: E402


def _patch_js(responsive: str | None) -> None:
    def fake_js_eval(*, js_expressions: str, key: str, want_output: bool, height: int):
        _ = js_expressions, key, want_output, height
        return responsive

    landing_page._js_eval = lambda expression, *, key: fake_js_eval(  # type: ignore[method-assign]
        js_expressions=expression,
        key=key,
        want_output=True,
        height=0,
    )


def test_resolve_home_mobile_tablet() -> None:
    _patch_js("1")
    assert landing_page.resolve_home_entry() == "mobile"


def test_resolve_home_desktop() -> None:
    _patch_js("0")
    assert landing_page.resolve_home_entry() == "desktop"


def test_resolve_home_waits_for_js() -> None:
    _patch_js(None)
    assert landing_page.resolve_home_entry() is None


def main() -> int:
    tests = [
        test_resolve_home_mobile_tablet,
        test_resolve_home_desktop,
        test_resolve_home_waits_for_js,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} home routing checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
