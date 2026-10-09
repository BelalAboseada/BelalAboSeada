#!/usr/bin/env python3
"""About card in the portfolio's services-list style: big Cabinet Grotesk
name, olive subtitle, then numbered rows (01 · LABEL · value) split by
hairlines. Rows fade/slide in on a stagger. STATIC=1 renders the final frame.

Two layouts: desktop (980 wide, sits next to the portrait) and mobile (740
wide, shorter values) for the stacked phone view."""
import html
import os

from fonts import BODY, TITLE, TITLE_MID
from theme import ACCENT, FLAX, MUTED, TEXT, TITLEBAR_H, frame, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.environ.get("STATIC") == "1"

NAME = "BELAL ABOSEADA"
SUB = "Software Engineer × Tech Content Creator"
MOTTO = "Developer by day, creator by night."
ROWS = [
    ("Now", "Shipping a SaaS + freelance web apps"),
    ("Prev", "Madar · MockMate AI coach · Pyutube CLI"),
    ("Front", "TypeScript · Next.js · React · Vue · Tailwind"),
    ("Motion", "GSAP · Lenis · scroll-driven 3D pages"),
    ("Back", "Node.js · Laravel · Supabase · Firebase"),
    ("Content", "Arabic tech videos: gadgets, AI, everyday"),
    ("Base", "Damanhur, Egypt"),
    ("Web", "belalaboseada.vercel.app"),
    ("Mail", "belalaboseada@gmail.com"),
]
MOBILE_ROWS = [
    ("Now", "SaaS + freelance web apps"),
    ("Front", "TS · Next.js · React · Vue"),
    ("Back", "Node · Laravel · Supabase"),
    ("Content", "Arabic tech videos"),
    ("Base", "Damanhur, Egypt"),
    ("Web", "belalaboseada.vercel.app"),
    ("Mail", "belalaboseada@gmail.com"),
]
DESKTOP = dict(w=980, h=880, rows=ROWS, val_x=230)
MOBILE = dict(w=740, h=None, rows=MOBILE_ROWS, val_x=210)
PAD, RH = 36, 52


def render(cfg):
    w, rows, val_x = cfg["w"], cfg["rows"], cfg["val_x"]
    tb = TITLEBAR_H * 2
    h = cfg["h"] or (tb + 186 + RH * len(rows) + 150)
    css = ("@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
           ".r{opacity:0;animation:in .6s cubic-bezier(.2,.8,.2,1) both}")

    def anim(i):
        return "" if STATIC else f' class="r" style="animation-delay:{0.3 + i * 0.12:.2f}s"'

    out = [svg_open(w, h), f"<style>{css}</style>", frame(w, h, "About", num="03", pad=28, scale=2, uid="cbg")]
    y = tb + 80
    out.append(f'<g{anim(0)}><text x="{PAD}" y="{y}" font-family="{TITLE}" font-size="56" fill="{FLAX[50]}" '
               f'letter-spacing="1">{NAME}</text></g>')
    y += 42
    out.append(f'<g{anim(1)}><text x="{PAD}" y="{y}" font-family="{BODY}" font-size="23" fill="{ACCENT}">'
               f'{html.escape(SUB)}</text></g>')
    y += 28
    out.append(f'<line x1="{PAD}" y1="{y}" x2="{w - PAD}" y2="{y}" stroke="{FLAX[700]}" stroke-width="1.5"/>')
    i = 1
    for i, (k, v) in enumerate(rows, start=2):
        base = y + RH - 18
        out.append(
            f'<g{anim(i)}>'
            f'<text x="{PAD}" y="{base}" font-family="{BODY}" font-size="16" fill="{FLAX[600]}">{i - 1:02d}</text>'
            f'<text x="{PAD + 44}" y="{base}" font-family="{BODY}" font-size="17" fill="{MUTED}" '
            f'letter-spacing="2">{k.upper()}</text>'
            f'<text x="{PAD + val_x - 36}" y="{base}" font-family="{TITLE_MID}" font-size="26" fill="{TEXT}">'
            f'{html.escape(v)}</text>'
            f'<line x1="{PAD}" y1="{y + RH}" x2="{w - PAD}" y2="{y + RH}" stroke="{FLAX[800]}" stroke-width="1.5"/>'
            f'</g>')
        y += RH
    y += 54
    out.append(f'<g{anim(i + 1)}><text x="{PAD}" y="{y}" font-family="{BODY}" font-size="22" font-style="italic" '
               f'fill="{FLAX[300]}">&#8220;{html.escape(MOTTO)}&#8221;</text></g>')
    y += 30
    sw = (w - 2 * PAD) / 9
    swatches = "".join(f'<rect x="{PAD + j * sw:.1f}" y="{y}" width="{sw + 0.5:.1f}" height="14" fill="{FLAX[s]}"/>'
                       for j, s in enumerate([800, 700, 600, 500, 400, 300, 200, 100, 50]))
    out.append(f'<g{anim(i + 2)}>{swatches}</g>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    for name, cfg in [("info-card.svg", DESKTOP), ("info-card-mobile.svg", MOBILE)]:
        svg = render(cfg)
        with open(os.path.join(HERE, "..", name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
