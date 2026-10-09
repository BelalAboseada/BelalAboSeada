#!/usr/bin/env python3
"""Compose the whoami row from the two panels: side by side for desktop
(whoami.svg) and stacked with the larger mobile card for phones
(whoami-mobile.svg). The README picks one with <picture media=...>, because a
two-cell table can't reflow on a narrow screen. Run after make_avatar_svg.py
and make_info_card.py."""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GAP = 20


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        svg = f.read()
    w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    return svg, w, h


def place(svg, x, y):
    # a nested <svg> takes x/y; its own width/height/viewBox keep it 1:1
    return svg.replace("<svg ", f'<svg x="{x}" y="{y}" ', 1)


def compose(parts, w, h):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    return head + "".join(parts) + "</svg>"


if __name__ == "__main__":
    portrait, pw, ph = load("portrait-ascii.svg")
    card, cw, ch = load("info-card.svg")
    mcard, mw, mh = load("info-card-mobile.svg")
    desk = compose([place(portrait, 0, 0), place(card, pw + GAP, 0)], pw + GAP + cw, max(ph, ch))
    mobile = compose([place(portrait, 0, 0), place(mcard, 0, ph + GAP)], max(pw, mw), ph + GAP + mh)
    for name, svg in [("whoami.svg", desk), ("whoami-mobile.svg", mobile)]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
