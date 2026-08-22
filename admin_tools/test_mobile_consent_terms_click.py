#!/usr/bin/env python3
"""Verify mobile consent Terms links use controlled navigation (phone only)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS  # noqa: E402
from legal_consent_logger import MOBILE_CONSENT_VIEW_MAX, inject_mobile_consent_terms_nav_bridge  # noqa: E402
from tooltip_scroll import _PAGE_NAV_LAYOUT_RESYNC_JS, _RESPONSIVE_DOC_HELPER_JS  # noqa: E402


def test_mobile_consent_viewport_max_is_phone_only() -> None:
    assert MOBILE_CONSENT_VIEW_MAX == 743


def test_consent_terms_nav_helpers_in_core_js() -> None:
    js = _RESPONSIVE_DOC_HELPER_JS
    assert "__scoopResolveTermsUrl" in js
    assert "__scoopNavigateMobileTerms" in js


def test_page_nav_intercepts_terms_on_phone() -> None:
    js = _PAGE_NAV_LAYOUT_RESYNC_JS
    assert "__scoopNavigateMobileTerms(link, appWin)" in js
    assert "event.preventDefault()" in js
    assert "PAGE_NAV_BIND_VERSION = 6" in js


def test_mobile_terms_css_overrides_stale_desktop_flags() -> None:
    css = MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS
    assert "[data-scoop-desktop-layout=\"1\"]" in css
    assert "[data-scoop-screener-gated=\"1\"]" in css
    assert "@media (max-width: 743px)" in css


def test_consent_bridge_uses_assign_and_prevent_default() -> None:
    import inspect

    source = inspect.getsource(inject_mobile_consent_terms_nav_bridge)
    assert "preventDefault" in source
    assert "location.assign" in source
    assert "passive: false" in source
    assert "__scoopMobileConsentTermsNavVersion = 2" in source


def main() -> int:
    tests = [
        test_mobile_consent_viewport_max_is_phone_only,
        test_consent_terms_nav_helpers_in_core_js,
        test_page_nav_intercepts_terms_on_phone,
        test_mobile_terms_css_overrides_stale_desktop_flags,
        test_consent_bridge_uses_assign_and_prevent_default,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} mobile consent terms click checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
