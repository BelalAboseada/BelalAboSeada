#!/usr/bin/env python3
"""Render data/contributions.json as a 53x7 contribution heatmap SVG in the
Flax Smoke palette: rounded cells that cascade in diagonally once and freeze,
a Less->More legend, and a stats footer.

Writes contrib-heatmap.svg (full year) and contrib-heatmap-mobile.svg (last
MOBILE_WEEKS weeks, stats stacked) so the graph stays legible on a phone."""
import datetime
import json
import os

from fonts import BODY, TITLE
from theme import ACCENT, FLAX, FRAME, MUTED, TEXT, TITLEBAR_H, frame, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "..", "data", "contributions.json")
ROOT = os.path.join(HERE, "..")

# GitHub's own data-level (0-4, quartiles of *your* activity) -> flax ramp
PALETTE = ["#2B2C23", FLAX[700], FLAX[500], FLAX[300], FLAX[50]]
CELL, GAP = 12, 3
STEP = CELL + GAP
PAD, LABEL_W, MONTH_H = 22, 30, 22
MOBILE_WEEKS = 22


def columns(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    col = [None] * ((first.weekday() + 1) % 7)  # Sunday-first rows
    cols = []
    for d in days:
        col.append(d)
        if len(col) == 7:
            cols.append(col)
            col = []
    if col:
        cols.append(col + [None] * (7 - len(col)))
    return cols


def render(data, mobile=False):
    cols = columns(data["days"])
    if mobile:
        cols = cols[-MOBILE_WEEKS:]
    fs = 15 if mobile else 13
    foot_h = 160 if mobile else 96
    w = PAD + LABEL_W + len(cols) * STEP + PAD
    top = TITLEBAR_H + MONTH_H
    h = top + 7 * STEP + foot_h
    left = PAD + LABEL_W
    css = ("@keyframes pop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}"
           ".c{opacity:0;animation:pop .45s cubic-bezier(.2,.8,.2,1) both}")
    out = [svg_open(w, h), f"<style>{css}</style>",
           frame(w, h, "Activity", num="01"), f'<g font-family="{BODY}">']

    seen = set()
    for ci, col in enumerate(cols):
        d = next((c for c in col if c), None)
        date = datetime.date.fromisoformat(d["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and ci < len(cols) - 2:
            seen.add((date.year, date.month))
            out.append(f'<text x="{left + ci * STEP}" y="{TITLEBAR_H + 15}" fill="{MUTED}" '
                       f'font-size="10">{date.strftime("%b")}</text>')
    for ri, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        out.append(f'<text x="{PAD}" y="{top + ri * STEP + 9.5}" fill="{MUTED}" font-size="9">{name}</text>')

    for ci, col in enumerate(cols):
        for ri, d in enumerate(col):
            if not d:
                continue
            delay = ci * 0.018 + ri * 0.045
            s = "" if d["count"] == 1 else "s"
            out.append(f'<rect class="c" x="{left + ci * STEP}" y="{top + ri * STEP}" width="{CELL}" '
                       f'height="{CELL}" rx="2.5" fill="{PALETTE[d["level"]]}" '
                       f'style="animation-delay:{delay:.3f}s"><title>{d["date"]}: '
                       f'{d["count"]} contribution{s}</title></rect>')

    ly = top + 7 * STEP + 6
    lx = w - PAD - len(PALETTE) * STEP - 34
    out.append(f'<text x="{lx - 6}" y="{ly + 10}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    for i, c in enumerate(PALETTE):
        out.append(f'<rect x="{lx + i * STEP}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>')
    out.append(f'<text x="{lx + len(PALETTE) * STEP + 4}" y="{ly + 10}" fill="{MUTED}" font-size="10">More</text>')

    sep = ly + CELL + 14
    out.append(f'<line x1="0" y1="{sep}" x2="{w}" y2="{sep}" stroke="{FRAME}" stroke-opacity="0.6"/>')
    best, rng = data["best_day"], data["range"]
    stats = [("active days", data["active_days"]), ("longest streak", f'{data["longest_streak"]}d')]
    if data["current_streak"]:
        stats.insert(0, ("current streak", f'{data["current_streak"]}d'))
    spans = f'<tspan fill="{MUTED}">  &#183;  </tspan>'.join(
        f'<tspan fill="{MUTED}">{k} </tspan><tspan fill="{ACCENT}" font-family="{TITLE}">{v}</tspan>'
        for k, v in (stats[:2] if mobile else stats))
    total = (f'<tspan font-family="{TITLE}">{data["total_contributions"]:,}</tspan>'
             f'<tspan fill="{MUTED}"> contributions in the last year</tspan>')
    best_s = (f'best day <tspan fill="{FLAX[50]}" font-family="{TITLE}">{best["count"]}</tspan> on {best["date"]}')
    rng_s = f'{rng["start"]} &#8594; {rng["end"]}'
    if mobile:
        lines = [(total, TEXT), (spans, None), (best_s, MUTED), (rng_s, MUTED)]
        for k, (body, fill) in enumerate(lines):
            f_attr = f' fill="{fill}"' if fill else ""
            out.append(f'<text x="{PAD}" y="{sep + 28 + k * 28}" font-size="{fs}"{f_attr}>{body}</text>')
    else:
        y1, y2 = sep + 26, sep + 50
        out.append(f'<text x="{PAD}" y="{y1}" font-size="{fs}" fill="{TEXT}">{total}</text>')
        out.append(f'<text x="{w - PAD}" y="{y1}" font-size="12" fill="{MUTED}" text-anchor="end">{rng_s}</text>')
        out.append(f'<text x="{PAD}" y="{y2}" font-size="{fs}">{spans}</text>')
        out.append(f'<text x="{w - PAD}" y="{y2}" font-size="12" fill="{MUTED}" text-anchor="end">{best_s}</text>')
    out.append("</g></svg>")
    return "".join(out)


if __name__ == "__main__":
    with open(IN, encoding="utf-8") as f:
        data = json.load(f)
    for name, mobile in [("contrib-heatmap.svg", False), ("contrib-heatmap-mobile.svg", True)]:
        svg = render(data, mobile)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
