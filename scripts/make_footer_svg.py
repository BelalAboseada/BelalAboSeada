#!/usr/bin/env python3
"""Closing banner in the portfolio's contact style: dark grainy card, big
Cabinet Grotesk call to action ending in " /", email + site in Switzer, a
spinning sparkle. The README wraps it in a mailto link.
Writes footer.svg (desktop) and footer-mobile.svg."""
import os

from fonts import BODY, TITLE
from make_hero_svg import width
from theme import BG, BG2, FLAX, grain, sparkle, svg_open

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LINES = ["LET'S WORK", "TOGETHER /"]
CONTACT = "belalaboseada@gmail.com  →"
SITE = "belalaboseada.vercel.app"


def render(w, size, pad, fs):
    h = int(pad + 60 + size * 1.84 + fs * 3.4 + pad + fs * 1.4)
    css = ("@keyframes up{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}"
           ".u{animation:up .9s cubic-bezier(.2,.8,.2,1) both}")
    out = [svg_open(w, h, fonts=("Cabinet", "Switzer")), f"<style>{css}</style>",
           f'<defs><linearGradient id="fb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/>'
           f'<stop offset="1" stop-color="{BG}"/></linearGradient>{grain("fg")}</defs>',
           f'<rect width="{w}" height="{h}" rx="36" fill="url(#fb)"/>',
           f'<rect width="{w}" height="{h}" rx="36" filter="url(#fg)"/>',
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="36" fill="none" stroke="{FLAX[900]}" stroke-width="2"/>',
           f'<text x="{pad}" y="{pad + 30}" font-family="{BODY}" font-size="{fs * 0.8:.0f}" fill="{FLAX[400]}" '
           f'letter-spacing="3">( CONTACT )</text>',
           sparkle(w - pad - 18, pad + 22, 18, FLAX[500])]
    y = pad + 60 + size * 0.86
    for i, line in enumerate(LINES):
        out.append(f'<text class="u" style="animation-delay:{0.1 + i * 0.15:.2f}s" x="{pad}" y="{y:.0f}" '
                   f'font-family="{TITLE}" font-size="{size}" fill="{FLAX[100]}">{line}</text>')
        y += size * 0.92
    y += fs * 1.2
    out.append(f'<line x1="{pad}" y1="{y - fs * 1.4:.0f}" x2="{w - pad}" y2="{y - fs * 1.4:.0f}" '
               f'stroke="{FLAX[700]}" stroke-width="1.5"/>')
    out.append(f'<text class="u" style="animation-delay:.5s" x="{pad}" y="{y + 6:.0f}" font-family="{BODY}" '
               f'font-size="{fs}" fill="{FLAX[200]}">{CONTACT}</text>')
    out.append(f'<text class="u" style="animation-delay:.6s" x="{w - pad}" y="{y + 6:.0f}" font-family="{BODY}" '
               f'font-size="{fs * 0.8:.0f}" fill="{FLAX[500]}" text-anchor="end">{SITE}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    size = 150
    while width("LET'S WORK", size) > 1200:
        size -= 2
    msize = 120
    while width("LET'S WORK", msize) > 740 - 2 * 44:
        msize -= 2
    for name, svg in [("footer.svg", render(1720, size, 70, 34)), ("footer-mobile.svg", render(740, msize, 44, 26))]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
