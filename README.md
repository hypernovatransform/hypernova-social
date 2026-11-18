# hypernova-social

Public image hosting for Hypernova Transform LinkedIn posts. Buffer fetches post images from the raw links in this repository.

- `YYYY-MM/` - finished post images, named `YYYY-MM-DD-short-title.png` (1080 x 1350).
- `tools/render.py` - turns a design-canvas artboard (`.dc.html`) into a PNG: `python3 tools/render.py <artboard.dc.html> <out.png>`. Needs Python Playwright and Chrome.
- `tools/assets/` - brand logos and the Lexend Deca font (SIL Open Font License, see `OFL.txt`).

Public link pattern: `https://raw.githubusercontent.com/hypernovatransform/hypernova-social/main/<path>`
