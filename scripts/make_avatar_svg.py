#!/usr/bin/env python3
"""portrait.sh panel: assets/avatar.png first types itself out as one-color
ASCII (row-by-row SMIL clip wipe), then cross-fades into the real avatar and
holds. The avatar is embedded as a data URI because GitHub serves README SVGs
through <img>, which blocks external references."""
import base64
import html
import io
import os

from PIL import Image

from fonts import BODY
from theme import ACCENT, FLAX, INK, MUTED, TITLEBAR_H, frame, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "avatar.png")
OUT = os.path.join(HERE, "..", "portrait-ascii.svg")

W, H = 740, 880                    # 370 px wide in the README, same height as info-card.svg
TB, STATUS_H = TITLEBAR_H * 2, 50
D = 640                            # avatar / ascii square
X0 = (W - D) / 2
Y0 = TB + (H - TB - STATUS_H - D) / 2
COLS = 100
CELL_W = D / COLS
CELL_H = CELL_W * 15 / 8
ROWS = int(D / CELL_H)
RAMP = " .`:-=+*cs#%@"
WHITE_FLOOR = 0.88
TYPE_S = 3.2                       # ascii prints in ~3 s
FADE_AT, FADE_S = TYPE_S + 0.4, 1.2


def load():
    im = Image.open(SRC).convert("RGBA")
    flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)
    return flat.convert("RGB")


def ascii_rows(im):
    g = im.convert("L").resize((COLS, ROWS), Image.LANCZOS).load()
    for y in range(ROWS):
        line = ""
        for x in range(COLS):
            v = g[x, y] / 255
            line += " " if v >= WHITE_FLOOR else RAMP[min(len(RAMP) - 1, int((1 - v / WHITE_FLOOR) * len(RAMP)))]
        yield line


def data_uri():
    # WebP keeps the transparent sticker edge (hair breaks out of the disc) at a fraction of PNG size
    buf = io.BytesIO()
    Image.open(SRC).convert("RGBA").resize((D, D), Image.LANCZOS).save(buf, "WEBP", quality=90, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def render():
    im = load()
    dur = TYPE_S / ROWS
    out = [svg_open(W, H), frame(W, H, "Portrait", num="02", pad=28, scale=2, uid="pbg")]
    out.append(f'<g><animate attributeName="opacity" from="1" to="0" begin="{FADE_AT}s" dur="{FADE_S}s" fill="freeze"/>')
    for i, line in enumerate(ascii_rows(im)):
        if not line.strip():
            continue
        y = Y0 + i * CELL_H
        out.append(
            f'<clipPath id="pr{i}"><rect x="{X0}" y="{y:.2f}" height="{CELL_H + 1:.2f}" width="0">'
            f'<animate attributeName="width" from="0" to="{D}" begin="{i * dur:.3f}s" dur="{dur:.3f}s" fill="freeze"/>'
            f'</rect></clipPath><text clip-path="url(#pr{i})" xml:space="preserve" x="{X0}" '
            f'y="{y + CELL_H * 0.78:.2f}" fill="{INK}" font-size="{CELL_H * 0.86:.2f}" textLength="{D}" '
            f'lengthAdjust="spacingAndGlyphs">{html.escape(line)}</text>')
    out.append("</g>")
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{FADE_AT}s" '
               f'dur="{FADE_S}s" fill="freeze"/>'
               f'<image href="{data_uri()}" x="{X0}" y="{Y0}" width="{D}" height="{D}"/>'
               f'<circle cx="{X0 + D / 2}" cy="{Y0 + D / 2}" r="{D / 2 - 2}" fill="none" '
               f'stroke="{FLAX[600]}" stroke-width="4"/></g>')
    sy = H - 18
    out.append(f'<line x1="0" y1="{H - STATUS_H}" x2="{W}" y2="{H - STATUS_H}" stroke="{FLAX[700]}" stroke-opacity="0.7"/>')
    out.append(f'<text x="28" y="{sy}" font-family="{BODY}" font-size="22" fill="{MUTED}">avatar.png · '
               f'<tspan fill="{ACCENT}">Belal Aboseada</tspan> · Damanhur, EG</text>')
    out.append(f'<rect x="{W - 41}" y="{sy - 18}" width="13" height="22" fill="{ACCENT}">'
               f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" '
               f'repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote portrait-ascii.svg ({len(svg):,} bytes)")
