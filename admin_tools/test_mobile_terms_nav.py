#!/usr/bin/env python3
"""Mobile-only Terms navigation from screener gating pages."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooltip_scroll import (  # noqa: E402
    _PAGE_NAV_LAYOUT_RESYNC_JS,
    _RESPONSIVE_DOC_HELPER_JS,
    _RESPONSIVE_SIDEBAR_JS,
)


def test_phone_viewport_helper_exists() -> None:
    assert "__scoopIsPhoneViewport" in _RESPONSIVE_DOC_HELPER_JS
    assert "__scoopIsTabletViewport" in _RESPONSIVE_DOC_HELPER_JS
    assert "__scoopIsTermsPage" in _RESPONSIVE_DOC_HELPER_JS
    assert "__scoopViewportWidth() <= 743" in _RESPONSIVE_DOC_HELPER_JS
    assert "w >= 744 && w <= 1366" in _RESPONSIVE_DOC_HELPER_JS


def test_page_nav_marks_mobile_terms_click() -> None:
    js = _PAGE_NAV_LAYOUT_RESYNC_JS
    assert "markMobileTermsNav" in js
    assert "enforceMobileTermsMainView" in js
    assert "scoop-terms-nav-collapse" in js
    assert "holdMobileTermsMainView" in js
    assert "removeAttribute(\"data-scoop-screener-gated\")" in js
    assert "removeAttribute(\"data-scoop-desktop-layout\")" in js
    assert "PAGE_NAV_BIND_VERSION = 6" in js
    assert "preventDefault" in js
    assert "__scoopNavigateMobileTerms" in js
    assert "touchstart" in js
    assert "__scoopIsPhoneViewport()" in js


def test_mobile_consent_terms_main_view_css_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS

    css = MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS
    assert "@media (max-width: 743px)" in css
    assert 'html[data-scoop-terms-active="1"]' in css
    assert "display: block !important" in css


def test_consent_bridge_injects_on_gate() -> None:
    import inspect

    from legal_consent_logger import inject_mobile_consent_terms_nav_bridge

    source = inspect.getsource(inject_mobile_consent_terms_nav_bridge)
    assert "MOBILE_CONSENT_VIEW_MAX" in source
    assert 'aw.__scoopMobileConsentTermsNavVersion = 2' in source
    assert "preventDefault" in source
    assert "location.assign" in source
    assert "removeAttribute(\"data-scoop-desktop-layout\")" in source
    gate_source = inspect.getsource(__import__("legal_consent_logger").render_terms_gate)
    assert "inject_mobile_consent_terms_nav_bridge" in gate_source


def test_sidebar_holds_main_view_on_mobile_terms() -> None:
    js = _RESPONSIVE_SIDEBAR_JS
    assert "holdMainViewForMobileTerms" in js
    assert "scheduleCollapseAfterMobileTermsNav" in js
    assert "shouldHoldMobileTermsMainView" in js
    assert "__scoopIsPhoneViewport()" in js
    assert "TERMS_NAV_COLLAPSE_KEY" in js


def test_tablet_desktop_untouched_by_phone_guard() -> None:
    js = _RESPONSIVE_SIDEBAR_JS
    assert "if (!__scoopIsPhoneViewport())" in js


def test_phone_market_nav_assigns_location() -> None:
    js = _PAGE_NAV_LAYOUT_RESYNC_JS
    assert "PAGE_NAV_BIND_VERSION = 6" in js
    pointer_idx = js.index("handleMobileTermsNavPointer")
    phone_idx = js.index("if (__scoopIsPhoneViewport()) {", pointer_idx)
    assign_idx = js.index("appWin.location.assign(__scoopResolveTermsUrl(link, appWin))", phone_idx)
    assert assign_idx > phone_idx


def test_tablet_market_nav_assigns_location() -> None:
    js = _PAGE_NAV_LAYOUT_RESYNC_JS
    pointer_idx = js.index("handleMobileTermsNavPointer")
    tablet_idx = js.index("if (__scoopIsTabletViewport()) {", pointer_idx)
    assign_idx = js.index("appWin.location.assign(__scoopResolveTermsUrl(link, appWin))", tablet_idx)
    assert assign_idx > tablet_idx


def main() -> int:
    tests = [
        test_phone_viewport_helper_exists,
        test_page_nav_marks_mobile_terms_click,
        test_mobile_consent_terms_main_view_css_scoped,
        test_consent_bridge_injects_on_gate,
        test_sidebar_holds_main_view_on_mobile_terms,
        test_tablet_desktop_untouched_by_phone_guard,
        test_phone_market_nav_assigns_location,
        test_tablet_market_nav_assigns_location,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} mobile terms nav checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
