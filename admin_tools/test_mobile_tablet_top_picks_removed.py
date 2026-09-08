"""Phone/tablet omit Top Picks; desktop still shows the three pick cards."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _agree(page) -> None:
    loc = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
    if loc.count() == 0:
        return
    loc.locator("label").first.click(force=True, position={"x": 8, "y": 8})
    page.wait_for_timeout(8000)


def _info(page) -> dict:
    return page.evaluate(
        """() => {
          const vis = (el) => {
            if (!el) return false;
            const cs = getComputedStyle(el);
            if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) return false;
            const r = el.getBoundingClientRect();
            return r.width > 4 && r.height > 4;
          };
          const h3 = [...document.querySelectorAll("h3")].find((n) => /Top Picks/i.test(n.textContent || ""));
          const metrics = [...document.querySelectorAll("[data-testid='stMetric']")].filter(vis);
          return {
            w: window.innerWidth,
            topHeading: vis(h3),
            topInDom: !!h3,
            metricCount: metrics.length,
          };
        }"""
    )


def _open(browser, url: str, width: int, height: int):
    page = browser.new_page(viewport={"width": width, "height": height})
    page.add_init_script("try { sessionStorage.setItem('scoop-mobile-home-seen', '1'); } catch (e) {}")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(5000)
    page.wait_for_selector("[data-testid='stCheckbox']", state="attached", timeout=45000)
    _agree(page)
    page.wait_for_selector(".full-results-wrap, [data-testid='stAlert']", timeout=60000)
    page.wait_for_timeout(1500)
    return page


def main() -> int:
    from playwright.sync_api import sync_playwright

    url = os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NYSE_Top_10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        phone = _info(_open(browser, url, 390, 844))
        tablet = _info(_open(browser, url, 1024, 768))
        desktop = _info(_open(browser, url, 1600, 900))
        browser.close()

    print(repr({"phone": phone, "tablet": tablet, "desktop": desktop}), flush=True)
    if phone["w"] > 1366 or tablet["w"] > 1366:
        raise SystemExit("FAIL phone/tablet viewport was not compact")
    if phone["topHeading"] or phone["topInDom"] or phone["metricCount"]:
        raise SystemExit(f"FAIL phone still has Top Picks: {phone}")
    if tablet["topHeading"] or tablet["topInDom"] or tablet["metricCount"]:
        raise SystemExit(f"FAIL tablet still has Top Picks: {tablet}")
    if desktop["w"] < 1367:
        raise SystemExit("FAIL desktop viewport was not wide")
    if not desktop["topHeading"] or desktop["metricCount"] < 1:
        raise SystemExit(f"FAIL desktop lost Top Picks: {desktop}")
    print("PASS phone/tablet omit Top Picks; desktop keeps them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
