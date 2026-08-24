"""Playwright check: 12px gaps between mobile/tablet home market nav buttons."""

from __future__ import annotations

import sys

URL = "http://localhost:8501/"
EXPECTED_GAP_PX = 12
GAP_TOLERANCE_PX = 2
MOBILE_VIEWPORT = {"width": 390, "height": 844}
TABLET_VIEWPORT = {"width": 768, "height": 1024}


def _market_button_containers(page):
    return page.locator(
        '[data-testid="stMainBlockContainer"] '
        '[data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"])'
    )


def _measure_market_button_gaps(page) -> list[float]:
    page.wait_for_selector(
        '[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"])',
        timeout=60000,
    )
    page.wait_for_timeout(5000)
    containers = _market_button_containers(page)
    count = containers.count()
    if count < 2:
        raise AssertionError(f"Expected at least 2 market nav button containers, found {count}")

    gaps: list[float] = []
    for index in range(count - 1):
        first = containers.nth(index)
        second = containers.nth(index + 1)
        first_box = first.bounding_box()
        second_box = second.bounding_box()
        if not first_box or not second_box:
            raise AssertionError(f"Could not measure bounding box for button pair {index}")
        gap = second_box["y"] - (first_box["y"] + first_box["height"])
        gaps.append(round(gap, 1))
    return gaps


def _assert_gaps(label: str, gaps: list[float]) -> None:
    low = EXPECTED_GAP_PX - GAP_TOLERANCE_PX
    high = EXPECTED_GAP_PX + GAP_TOLERANCE_PX
    for index, gap in enumerate(gaps):
        if not (low <= gap <= high):
            raise AssertionError(
                f"{label}: gap after button {index + 1} is {gap}px (expected {EXPECTED_GAP_PX}px ±{GAP_TOLERANCE_PX})"
            )
    print(f"PASS {label}: gaps={gaps}")


def verify_home_nav_spacing() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for label, viewport in (("mobile_390", MOBILE_VIEWPORT), ("tablet_768", TABLET_VIEWPORT)):
            page = browser.new_page(viewport=viewport)
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            gaps = _measure_market_button_gaps(page)
            _assert_gaps(label, gaps)
            page.close()
        browser.close()


def verify_home_side_padding() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for label, viewport in (("mobile_390", {"width": 390, "height": 844}), ("tablet_768", {"width": 768, "height": 1024})):
            page = browser.new_page(viewport=viewport)
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('[data-testid="stMainBlockContainer"]', timeout=60000)
            page.wait_for_timeout(3000)
            metrics = page.evaluate(
                """() => {
                    const main = document.querySelector('[data-testid="stMainBlockContainer"]');
                    const style = getComputedStyle(main);
                    const logo = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stImage"]), [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stImage"])');
                    const logoRect = logo ? logo.getBoundingClientRect() : null;
                    const terms = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms"])');
                    const termsRect = terms ? terms.getBoundingClientRect() : null;
                    return {
                        paddingLeft: style.paddingLeft,
                        paddingRight: style.paddingRight,
                        logoLeft: logoRect ? Math.round(logoRect.left) : null,
                        logoWidth: logoRect ? Math.round(logoRect.width) : null,
                        termsRight: termsRect ? Math.round(termsRect.right) : null,
                        viewport: window.innerWidth,
                    };
                }"""
            )
            assert metrics["paddingLeft"] == "20px", f"{label} padding-left={metrics['paddingLeft']}"
            assert metrics["paddingRight"] == "20px", f"{label} padding-right={metrics['paddingRight']}"
            assert metrics["logoLeft"] == 20, f"{label} logo left={metrics['logoLeft']}"
            expected_content_width = metrics["viewport"] - 40
            assert abs(metrics["logoWidth"] - expected_content_width) <= 2, (
                f"{label} logo width={metrics['logoWidth']} expected ~{expected_content_width}"
            )
            assert abs(metrics["termsRight"] - (metrics["viewport"] - 20)) <= 2, (
                f"{label} terms right={metrics['termsRight']} expected ~{metrics['viewport'] - 20}"
            )
            print(f"PASS {label} padding: {metrics}")
            page.close()
        browser.close()


def verify_description_nav_gap() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".scoop-home-landing", timeout=60000)
        page.wait_for_timeout(3000)
        gap = page.evaluate(
            """() => {
                const desc = document.querySelector('.scoop-home-landing');
                const nyse = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="NYSE"])');
                if (!desc || !nyse) return null;
                const d = desc.getBoundingClientRect();
                const n = nyse.getBoundingClientRect();
                return Math.round(n.top - d.bottom);
            }"""
        )
        browser.close()
    assert gap is not None, "Could not locate description and NYSE button"
    assert gap >= 10, f"Description/NYSE gap is {gap}px (expected at least 10px)"


def main() -> int:
    try:
        verify_home_nav_spacing()
        verify_home_side_padding()
        verify_description_nav_gap()
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("Home market nav spacing and 20px side padding verified at mobile and tablet widths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
