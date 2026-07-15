"""Render docs/scoop52-launch-plan.html to a PDF via Playwright."""

from __future__ import annotations

import asyncio
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parent.parent / "docs" / "scoop52-launch-plan.html"
PDF_PATH = Path(__file__).resolve().parent.parent / "docs" / "scoop52-launch-plan.pdf"


async def generate_pdf() -> None:
    from playwright.async_api import async_playwright

    if not HTML_PATH.is_file():
        raise FileNotFoundError(f"HTML source not found: {HTML_PATH}")

    file_url = HTML_PATH.as_uri()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 1800})

        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_function(
            "() => document.querySelectorAll('.mermaid svg').length >= 3",
            timeout=60_000,
        )
        await page.wait_for_timeout(1500)

        # Scale each diagram SVG to fill its landscape page in the PDF export.
        await page.evaluate(
            """() => {
              document.querySelectorAll('.diagram-page.landscape .mermaid svg').forEach((svg) => {
                svg.removeAttribute('height');
                svg.style.width = '100%';
                svg.style.height = 'auto';
                svg.style.maxHeight = '7.4in';
                svg.style.display = 'block';
                svg.style.margin = '0 auto';
              });
            }"""
        )
        await page.wait_for_timeout(500)

        await page.emulate_media(media="print")
        await page.pdf(
            path=str(PDF_PATH),
            format="Letter",
            print_background=True,
            margin={"top": "0.55in", "right": "0.55in", "bottom": "0.55in", "left": "0.55in"},
            prefer_css_page_size=True,
        )
        await browser.close()

    print(f"Wrote {PDF_PATH}")


def main() -> None:
    asyncio.run(generate_pdf())


if __name__ == "__main__":
    main()
