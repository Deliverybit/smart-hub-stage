"""Phone/tablet must omit index banner cards; desktop still renders them."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _banner_info(page) -> dict:
    return page.evaluate(
        """() => {
          const cards = [...document.querySelectorAll(".scoop-index-card")];
          const visible = cards.filter((el) => {
            const cs = getComputedStyle(el);
            if (cs.display === "none" || cs.visibility === "hidden") return false;
            const r = el.getBoundingClientRect();
            return r.width > 4 && r.height > 4;
          });
          return {
            w: window.innerWidth,
            cardCount: cards.length,
            visibleCount: visible.length,
            hasCompact: !!document.querySelector(".scoop-banner-compact"),
            hasDesktop: !!document.querySelector(".scoop-banner-desktop"),
            title: ((document.querySelector("h1") || {}).textContent || "").replace(/[^\\x20-\\x7E]/g, ""),
          };
        }"""
    )


def _open(browser, url: str, width: int, height: int):
    page = browser.new_page(viewport={"width": width, "height": height})
    page.add_init_script("try { sessionStorage.setItem('scoop-mobile-home-seen', '1'); } catch (e) {}")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    page.wait_for_selector("[data-testid='stCheckbox']", state="attached", timeout=45000)
    page.wait_for_timeout(2500)
    return page


def main() -> int:
    from playwright.sync_api import sync_playwright

    url = os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NYSE_Top_10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        phone = _open(browser, url, 390, 844)
        phone_info = _banner_info(phone)
        tablet = _open(browser, url, 1024, 768)
        tablet_info = _banner_info(tablet)
        desk = _open(browser, url, 1600, 900)
        desk.wait_for_timeout(4000)
        desktop_info = _banner_info(desk)
        browser.close()

    summary = {"phone": phone_info, "tablet": tablet_info, "desktop": desktop_info}
    print(repr(summary), flush=True)
    if phone_info["w"] > 1366 or tablet_info["w"] > 1366:
        raise SystemExit("FAIL phone/tablet viewport was not compact")
    if phone_info["cardCount"] or phone_info["visibleCount"] or phone_info["hasCompact"] or phone_info["hasDesktop"]:
        raise SystemExit(f"FAIL phone still has index cards: {phone_info}")
    if tablet_info["cardCount"] or tablet_info["visibleCount"] or tablet_info["hasCompact"] or tablet_info["hasDesktop"]:
        raise SystemExit(f"FAIL tablet still has index cards: {tablet_info}")
    if desktop_info["w"] < 1367:
        raise SystemExit("FAIL desktop viewport was not wide")
    if desktop_info["visibleCount"] < 3 or not desktop_info["hasDesktop"]:
        raise SystemExit(f"FAIL desktop lost index cards: {desktop_info}")
    print("PASS phone/tablet omit index cards; desktop keeps them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
