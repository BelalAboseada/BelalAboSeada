#!/usr/bin/env python3
"""Hand-authored neofetch-style info card (info-card.svg). Rows fade/slide in
on a stagger, then a cursor blinks. STATIC=1 renders the final frame only.
Edit ROWS below when your story changes -- live stats live in the heatmap."""
import html
import os

from theme import ACCENT, FLAX, FRAME, MUTED, TEXT, TITLEBAR_H, frame, svg_open

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "info-card.svg")
STATIC = os.environ.get("STATIC") == "1"
W, H = 980, 880          # same height as portrait-ascii.svg at README widths 490/370
PAD, FS, LH = 36, 22, 48
KEY_W = 160

USER = "belal@aboseada"
ROWS = [
    ("Role", "Software Engineer · Tech Content Creator"),
    ("Host", "Damanhur, Egypt"),
    ("Now", "Shipping a SaaS + freelance web apps"),
    ("Prev", "Madar · MockMate AI coach · Pyutube CLI"),
    ("Front", "TypeScript · Next.js · React · Vue · Tailwind"),
    ("Motion", "GSAP · Lenis · scroll-driven 3D pages"),
    ("Back", "Node.js · Laravel · Supabase · Firebase"),
    ("Content", "Arabic tech videos: gadgets, AI, everyday"),
    ("Uptime", "on GitHub since 2023"),
    ("Web", "belalaboseada.vercel.app"),
    ("Mail", "belalaboseada@gmail.com"),
]
MOTTO = "Developer by day, creator by night."


def anim(i):
    return "" if STATIC else f' class="r" style="animation-delay:{0.35 + i * 0.16:.2f}s"'


def render():
    css = ("@keyframes in{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}"
           ".r{opacity:0;animation:in .5s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
           ".cur{animation:blink 1.1s steps(1) infinite}")
    out = [svg_open(W, H), f"<style>{css}</style>", frame(W, H, "belal@github: ~$ neofetch", pad=28, scale=2)]
    y = TITLEBAR_H * 2 + 58
    out.append(f'<g{anim(0)}><text x="{PAD}" y="{y}" font-size="{FS + 5}" font-weight="700" fill="{FLAX[50]}">'
               f'{USER}</text></g>')
    y += 22
    out.append(f'<g{anim(1)}><text x="{PAD}" y="{y}" font-size="{FS}" fill="{FRAME}">'
               f'{"-" * len(USER)}</text></g>')
    y += LH - 4
    for i, (k, v) in enumerate(ROWS, start=2):
        out.append(f'<g{anim(i)}><text x="{PAD}" y="{y}" font-size="{FS}">'
                   f'<tspan fill="{ACCENT}" font-weight="700">{k}</tspan>'
                   f'<tspan fill="{MUTED}">:</tspan></text>'
                   f'<text x="{PAD + KEY_W}" y="{y}" font-size="{FS}" fill="{TEXT}">{html.escape(v)}</text></g>')
        y += LH
    i += 1
    y += 6
    out.append(f'<g{anim(i)}><text x="{PAD}" y="{y}" font-size="{FS}" font-style="italic" fill="{FLAX[300]}">'
               f'&#8220;{html.escape(MOTTO)}&#8221;</text></g>')
    i += 1
    y += 34
    sw = 54
    swatches = "".join(f'<rect x="{PAD + j * sw}" y="{y}" width="{sw}" height="26" fill="{FLAX[s]}"/>'
                       for j, s in enumerate([950, 800, 700, 600, 500, 400, 300, 200, 100, 50]))
    out.append(f'<g{anim(i)}>{swatches}</g>')
    py = H - 40
    out.append(f'<text x="{PAD}" y="{py}" font-size="{FS}" fill="{MUTED}"><tspan fill="{ACCENT}">belal@github</tspan>'
               f' ~ $ </text>')
    cls = "" if STATIC else ' class="cur"'
    out.append(f'<rect{cls} x="{PAD + 17 * FS * 0.6:.1f}" y="{py - FS + 3}" width="{FS * 0.6:.1f}" height="{FS}" '
               f'fill="{ACCENT}"/>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote info-card.svg ({len(svg):,} bytes)")
