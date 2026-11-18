"""Render a canvas .dc.html artboard to a PNG for social posting.

Usage: python3 render.py <artboard.dc.html> <out.png>
Strips the x-dc wrapper, swaps blob URLs for local asset files, embeds Lexend Deca.
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BLOBS = {
    "/_blob/896b1181365aa22a17f09a4ffe959d8e": ASSETS / "logo_white.png",
    "/_blob/45c442bfdee6dd422ebb380a161294c9": ASSETS / "logo_plum.png",
    "/_blob/7d2f438edf4120b6b8b56667b3b61f9b": ASSETS / "mark_plum.png",
    "/_blob/8e6d1f545aee9f0489a375dbe4993949": ASSETS / "mark_white.png",
}


def build_html(src: str) -> str:
    body = re.search(r"<x-dc>(.*)</x-dc>", src, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
    for blob, path in BLOBS.items():
        body = body.replace(blob, path.as_uri())
    font = (ASSETS / "LexendDeca.ttf").as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'Lexend Deca'; src: url('{font}') format('truetype'); font-weight: 100 900; }}
body {{ margin: 0; }}
</style></head><body>{body}</body></html>"""


def main(src_path: str, out_path: str) -> None:
    html = build_html(Path(src_path).read_text())
    tmp = Path("/tmp/_render.html")
    tmp.write_text(html)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.goto(tmp.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        page.screenshot(path=out_path, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
