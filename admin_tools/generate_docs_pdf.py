"""Render docs HTML guides to PDF via Playwright."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


async def generate_pdf(html_path: Path, pdf_path: Path, *, mermaid_count: int = 0) -> None:
    from playwright.async_api import async_playwright

    if not html_path.is_file():
        raise FileNotFoundError(f"HTML source not found: {html_path}")

    file_url = html_path.as_uri()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 1800})

        await page.goto(file_url, wait_until="networkidle")

        if mermaid_count > 0:
            await page.wait_for_function(
                f"() => document.querySelectorAll('.mermaid svg').length >= {mermaid_count}",
                timeout=60_000,
            )
            await page.wait_for_timeout(1500)
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
            path=str(pdf_path),
            format="Letter",
            print_background=True,
            margin={"top": "0.55in", "right": "0.55in", "bottom": "0.55in", "left": "0.55in"},
            prefer_css_page_size=True,
        )
        await browser.close()

    print(f"Wrote {pdf_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a PDF from a docs HTML file.")
    parser.add_argument(
        "name",
        nargs="?",
        default="staging-checklist",
        choices=["launch-plan", "staging-checklist"],
        help="Which document to render (default: staging-checklist)",
    )
    args = parser.parse_args()

    if args.name == "launch-plan":
        html_path = DOCS / "scoop52-launch-plan.html"
        pdf_path = DOCS / "scoop52-launch-plan.pdf"
        mermaid_count = 3
    else:
        html_path = DOCS / "scoop52-staging-optimization-checklist.html"
        pdf_path = DOCS / "scoop52-staging-optimization-checklist.pdf"
        mermaid_count = 1

    asyncio.run(generate_pdf(html_path, pdf_path, mermaid_count=mermaid_count))


if __name__ == "__main__":
    main()
