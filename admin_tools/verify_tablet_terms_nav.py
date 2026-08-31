"""Playwright: tablet Disclaimer & Terms stays in tablet view (not desktop split)."""

from __future__ import annotations

import sys

from playwright.sync_api import sync_playwright

CME = "http://localhost:8501/CME_Top_10"
TABLET = {"width": 1024, "height": 1366}


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=TABLET)
        page.add_init_script(
            """
            sessionStorage.setItem('scoop-theme', 'dark');
            sessionStorage.setItem('scoop-mobile-home-seen', '1');
            sessionStorage.setItem('scoop-responsive-sidebar-ready', '1');
            """
        )
        page.goto(CME, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(8000)

        link = page.locator('a[href*="Terms_of_Service"]').first
        link.wait_for(state="visible", timeout=60000)
        link.click()
        page.wait_for_url("**/Terms_of_Service**", timeout=60000)
        page.wait_for_timeout(5000)

        metrics = page.evaluate(
            """() => {
                const root = document.documentElement;
                const view = document.querySelector('[data-testid="stAppViewContainer"]');
                const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                const back = document.querySelector('.scoop-mobile-back-home');
                const cs = view ? getComputedStyle(view) : null;
                const sRect = sidebar ? sidebar.getBoundingClientRect() : null;
                return {
                    viewport: window.innerWidth,
                    tabNav: root.getAttribute('data-scoop-tab-nav'),
                    desktopLayout: root.getAttribute('data-scoop-desktop-layout'),
                    termsActive: root.getAttribute('data-scoop-terms-active'),
                    viewDisplay: cs ? cs.display : null,
                    viewFlexDir: cs ? cs.flexDirection : null,
                    sidebarExpanded: sidebar ? sidebar.getAttribute('aria-expanded') : null,
                    sidebarVisibleWidth: sRect ? Math.round(sRect.width) : null,
                    sidebarLeft: sRect ? Math.round(sRect.left) : null,
                    hasBackHome: !!back,
                    path: location.pathname,
                };
            }"""
        )
        browser.close()

        print("metrics:", metrics)
        assert metrics["viewport"] == 1024, metrics
        assert "/Terms_of_Service" in metrics["path"], metrics
        assert metrics["termsActive"] == "1", metrics
        assert metrics["tabNav"] == "1", metrics
        assert metrics["desktopLayout"] in (None, ""), metrics
        assert metrics["viewDisplay"] == "block", metrics
        assert metrics["hasBackHome"] is True, metrics
        # Sidebar should be off-canvas / not a desktop split column.
        assert metrics["sidebarLeft"] is None or metrics["sidebarLeft"] < 0 or (
            metrics["sidebarVisibleWidth"] or 0
        ) < 40, metrics
        print("PASS tablet Terms stays in tablet main view")
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
