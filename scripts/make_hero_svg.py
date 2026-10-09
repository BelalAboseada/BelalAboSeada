#!/usr/bin/env python3
"""Hero banner in the portfolio's look: paper background with film grain,
the name in Cabinet Grotesk sliding up line by line, the spinning asterisk,
the olive subtitle and the avatar popping in. Writes hero.svg (desktop) and
hero-mobile.svg (stacked). Text is sized from the font's real metrics."""
import base64
import io
import os

from fontTools.ttLib import TTFont
from PIL import Image

from fonts import BODY, DIR, FACES, TITLE
from theme import FLAX, grain, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
AVATAR = os.path.join(ROOT, "assets", "avatar.png")
LINES = ["BELAL", "ABOSEADA"]
SUB = "Software Engineer × Tech Content Creator"
INK = "#45463A"

_font = TTFont(os.path.join(DIR, FACES["Cabinet"][2]))


def width(text, size):
    cmap, hmtx = _font.getBestCmap(), _font["hmtx"]
    upm = _font["head"].unitsPerEm
    return sum(hmtx[cmap[ord(c)]][0] for c in text) * size / upm


def avatar_uri(px):
    buf = io.BytesIO()
    Image.open(AVATAR).convert("RGBA").resize((px, px), Image.LANCZOS).save(buf, "WEBP", quality=90, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def asterisk(cx, cy, r, fill):
    arms = "".join(f'<rect x="{-r * 0.17:.1f}" y="{-r}" width="{r * 0.34:.1f}" height="{2 * r}" rx="{r * 0.17:.1f}" '
                   f'fill="{fill}" transform="rotate({a})"/>' for a in (0, 45, 90, 135))
    return (f'<g transform="translate({cx} {cy})"><g>{arms}'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" '
            f'repeatCount="indefinite"/></g></g>')


def render(w, h, size, x0, line_y, star, sub_xy, sub_fs, av):
    css = ("@keyframes up{from{transform:translateY(" + str(int(size * 1.1)) + "px)}to{transform:none}}"
           ".ln{animation:up 1s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes pop{from{opacity:0;transform:scale(.92)}to{opacity:1;transform:none}}"
           ".av{transform-box:fill-box;transform-origin:center;animation:pop 1s .5s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes fade{from{opacity:0}to{opacity:1}}.fd{animation:fade 1s .9s both}")
    out = [svg_open(w, h, fonts=("Cabinet", "Switzer")), f"<style>{css}</style>",
           f"<defs>{grain('hg', 0.10)}</defs>",
           f'<rect width="{w}" height="{h}" rx="36" fill="{FLAX[50]}"/>',
           f'<rect width="{w}" height="{h}" rx="36" filter="url(#hg)"/>']
    for i, (text, y) in enumerate(zip(LINES, line_y)):
        out.append(f'<clipPath id="hl{i}"><rect x="0" y="{y - size * 0.82:.0f}" width="{w}" height="{size * 0.86:.0f}"/>'
                   f'</clipPath><g clip-path="url(#hl{i})"><text class="ln" style="animation-delay:{0.15 + i * 0.15}s" '
                   f'x="{x0}" y="{y}" font-family="{TITLE}" font-size="{size}" fill="{INK}">{text}</text></g>')
    out.append(asterisk(*star, INK))
    out.append(f'<text class="fd" x="{sub_xy[0]}" y="{sub_xy[1]}" font-family="{BODY}" font-size="{sub_fs}" '
               f'fill="{FLAX[500]}">{SUB}</text>')
    ax, ay, ad = av
    out.append(f'<image class="av" href="{avatar_uri(ad)}" x="{ax}" y="{ay}" width="{ad}" height="{ad}"/>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    # desktop: name left, avatar right
    W, H, x0 = 1720, 620, 70
    av_d = 500
    av_x = W - 70 - av_d
    size = 210
    while width("ABOSEADA", size) > av_x - x0 - 70:   # keep a clear gap before the avatar
        size -= 2
    star_x = x0 + width("BELAL", size) + size * 0.45
    top = (H - (size * 1.74 + 78)) / 2 - 10
    desk = render(W, H, size, x0, [top + size * 0.84, top + size * 1.74], (star_x, top + size * 0.42, size * 0.3),
                  (x0 + 6, top + size * 1.74 + 78), 32, (av_x, (H - av_d) // 2, av_d))
    # mobile: avatar on top, name full width below
    MW, mx = 740, 44
    msize = 200
    while width("ABOSEADA", msize) > MW - 2 * mx:
        msize -= 2
    av_d = 440
    top = 40 + av_d + 30
    MH = int(top + msize * 1.74 + 110)
    mstar_x = mx + width("BELAL", msize) + msize * 0.45
    mob = render(MW, MH, msize, mx, [top + msize * 0.84, top + msize * 1.74],
                 (mstar_x, top + msize * 0.42, msize * 0.3), (mx + 4, top + msize * 1.74 + 64), 27,
                 ((MW - av_d) // 2, 40, av_d))
    for name, svg in [("hero.svg", desk), ("hero-mobile.svg", mob)]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
    print("sizes", size, msize)
