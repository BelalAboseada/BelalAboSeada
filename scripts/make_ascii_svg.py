#!/usr/bin/env python3
"""Turn assets/portrait-prepped.png into a one-color ASCII portrait SVG that
prints itself row by row (SMIL clip wipe + riding cursor) and then holds.
GitHub runs SVG animations inside <img>, but never JS."""
import html
import os

from PIL import Image

from theme import ACCENT, FLAX, INK, MUTED, TITLEBAR_H, frame, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "portrait-prepped.png")
OUT = os.path.join(HERE, "..", "portrait-ascii.svg")

COLS = 150
ART_W, ART_H = 700, 760
CELL_W = ART_W / COLS
CELL_H = CELL_W * 15 / 8          # monospace glyph ~ 8:15
ROWS = int(ART_H / CELL_H)
RAMP = " .`:-=+*cs#%@"             # light (sparse) -> dark (dense)
WHITE_FLOOR = 0.86                 # brighter than this -> blank (studio backdrop)
GAMMA = 1.3
PAD, STATUS_H, TB = 20, 50, TITLEBAR_H * 2
W, H = ART_W + 2 * PAD, TB + ART_H + STATUS_H + 10
TOTAL_S = 5.5                      # whole portrait prints in ~5.5 s


def rows():
    img = Image.open(SRC).convert("L").resize((COLS, ROWS), Image.LANCZOS)
    px = img.load()
    for y in range(ROWS):
        line = []
        for x in range(COLS):
            v = (px[x, y] / 255) ** GAMMA
            line.append(" " if v >= WHITE_FLOOR else RAMP[min(len(RAMP) - 1, int((1 - v / WHITE_FLOOR) * len(RAMP)))])
        yield "".join(line)


def render():
    lines = list(rows())
    dur = TOTAL_S / ROWS
    out = [svg_open(W, H), frame(W, H, "belal@github: ~$ ./portrait.sh", pad=28, scale=2)]
    top = TB + 6
    for i, line in enumerate(lines):
        y = top + i * CELL_H
        begin = f"{i * dur:.3f}s"
        if line.strip():
            out.append(
                f'<clipPath id="r{i}"><rect x="{PAD}" y="{y:.2f}" height="{CELL_H + 1:.2f}" width="0">'
                f'<animate attributeName="width" from="0" to="{ART_W}" begin="{begin}" dur="{dur:.3f}s" '
                f'fill="freeze"/></rect></clipPath>'
                f'<text clip-path="url(#r{i})" xml:space="preserve" x="{PAD}" y="{y + CELL_H * 0.78:.2f}" '
                f'fill="{INK}" font-size="{CELL_H * 0.86:.2f}" textLength="{ART_W}" '
                f'lengthAdjust="spacingAndGlyphs">{html.escape(line)}</text>')
    # block cursor raster-scanning down, then parking blinking on the status line
    out.append(
        f'<rect width="{CELL_W:.2f}" height="{CELL_H:.2f}" fill="{ACCENT}">'
        f'<animate attributeName="x" values="{PAD};{PAD + ART_W}" dur="{dur:.3f}s" repeatCount="{ROWS}" fill="freeze"/>'
        f'<animate attributeName="y" from="{top}" to="{top + ROWS * CELL_H}" dur="{TOTAL_S}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0" begin="{TOTAL_S}s" fill="freeze"/></rect>')
    sy = H - 22
    out.append(f'<line x1="0" y1="{sy - 36}" x2="{W}" y2="{sy - 36}" stroke="{FLAX[700]}" stroke-opacity="0.7"/>')
    out.append(f'<text x="{PAD}" y="{sy}" font-size="22" fill="{MUTED}">{COLS}x{ROWS} · '
               f'<tspan fill="{ACCENT}">Belal Aboseada</tspan> · Damanhur, EG</text>')
    out.append(f'<rect x="{W - PAD - 13}" y="{sy - 18}" width="13" height="22" fill="{ACCENT}" opacity="0">'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1.1s" '
               f'begin="{TOTAL_S}s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote portrait-ascii.svg {COLS}x{ROWS} ({len(svg):,} bytes)")
