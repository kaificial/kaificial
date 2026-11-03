#!/usr/bin/env python3
"""Builds fight-light.svg and fight-dark.svg the 31 second looping animation for the github README.

Everything is SMIL animation: no JavaScript, no CSS, no web fonts, so GitHub shows it as is.

    pip install pillow
    python3 make_fight.py

The story is in story/ (one file per act), and the reusable animation pieces are in engine/.
"""
from pathlib import Path

from story import build
from story.render import render

OUT_DIR = Path(__file__).resolve().parent


def main():
    times = build()
    for theme in ("light", "dark"):
        svg = render(theme, times)
        path = OUT_DIR / f"fight-{theme}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"{path.name}  {len(svg.encode()) / 1024:.0f} KB")
    print(f"beam {times.beam:.2f}  boom {times.boom:.2f}  back on the page {times.landed:.2f}")


if __name__ == "__main__":
    main()
