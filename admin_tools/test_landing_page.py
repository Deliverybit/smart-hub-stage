#!/usr/bin/env python3
"""Verify mobile/tablet first-visit landing routing."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import landing_page  # noqa: E402


class _Session(dict):
    def __getattr__(self, name: str):
        return self[name]

    def __setattr__(self, name: str, value) -> None:
        self[name] = value


def _fresh_session() -> _Session:
    landing_page.st.session_state = _Session()
    return landing_page.st.session_state


def _patch_js(responsive: str | None, seen: str | None) -> None:
    calls = iter([responsive, seen])

    def fake_js_eval(*, js_expressions: str, key: str, want_output: bool, height: int):
        _ = js_expressions, key, want_output, height
        return next(calls, None)

    landing_page._js_eval = lambda expression, *, key: fake_js_eval(  # type: ignore[method-assign]
        js_expressions=expression,
        key=key,
        want_output=True,
        height=0,
    )


def test_should_redirect_mobile_first_visit() -> None:
    _patch_js("1", "")
    assert landing_page.should_redirect_to_landing() is True


def test_should_skip_desktop() -> None:
    _patch_js("0", "")
    assert landing_page.should_redirect_to_landing() is False


def test_should_skip_after_seen() -> None:
    _patch_js("1", "1")
    assert landing_page.should_redirect_to_landing() is False


def test_should_wait_for_js() -> None:
    _patch_js(None, None)
    assert landing_page.should_redirect_to_landing() is None


def test_route_home_entry_goes_to_landing() -> None:
    ss = _fresh_session()
    _patch_js("1", "")
    switched: list[str] = []

    def fake_switch(page: str) -> None:
        switched.append(page)

    landing_page.st.switch_page = fake_switch  # type: ignore[method-assign]
    landing_page.route_home_entry()
    assert ss.get(landing_page.ROUTED_KEY) is True
    assert switched == [landing_page.LANDING_PAGE]


def test_route_home_entry_goes_to_nyse_on_desktop() -> None:
    ss = _fresh_session()
    _patch_js("0", "")
    switched: list[str] = []

    def fake_switch(page: str) -> None:
        switched.append(page)

    landing_page.st.switch_page = fake_switch  # type: ignore[method-assign]
    landing_page.route_home_entry()
    assert ss.get(landing_page.ROUTED_KEY) is True
    assert switched == [landing_page.DEFAULT_SCREENER_PAGE]


def main() -> int:
    tests = [
        test_should_redirect_mobile_first_visit,
        test_should_skip_desktop,
        test_should_skip_after_seen,
        test_should_wait_for_js,
        test_route_home_entry_goes_to_landing,
        test_route_home_entry_goes_to_nyse_on_desktop,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} landing page checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
