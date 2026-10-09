#!/usr/bin/env python3
"""Hand-authored neofetch-style info card. Rows fade/slide in on a stagger,
then a cursor blinks. STATIC=1 renders the final frame only.

Two layouts: the desktop card (980 wide, sits next to the portrait) and a
mobile card (740 wide, bigger type, shorter lines) for the stacked phone view.
Edit ROWS / MOBILE_ROWS when your story changes -- live stats live in the heatmap."""
import html
import os

from theme import ACCENT, FLAX, FRAME, MUTED, TEXT, frame, svg_open

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.environ.get("STATIC") == "1"

USER = "belal@aboseada"
MOTTO = "Developer by day, creator by night."
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
MOBILE_ROWS = [
    ("Role", "Software Engineer"),
    ("Also", "Tech Content Creator"),
    ("Host", "Damanhur, Egypt"),
    ("Now", "SaaS + freelance web apps"),
    ("Front", "TS · Next.js · React · Vue"),
    ("Back", "Node · Laravel · Supabase"),
    ("Content", "Arabic tech videos"),
    ("Web", "belalaboseada.vercel.app"),
    ("Mail", "belalaboseada@gmail.com"),
]
# desktop: same height as the portrait panel; mobile height follows its rows
DESKTOP = dict(w=980, h=880, pad=36, fs=22, lh=48, key_w=160, rows=ROWS)
MOBILE = dict(w=740, h=None, pad=34, fs=28, lh=56, key_w=170, rows=MOBILE_ROWS)


def render(cfg):
    w, pad, fs, lh, key_w, rows = cfg["w"], cfg["pad"], cfg["fs"], cfg["lh"], cfg["key_w"], cfg["rows"]
    h = cfg["h"] or (60 + 58 + 22 + lh * len(rows) + 6 + 34 + 26 + 150)
    css = ("@keyframes in{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}"
           ".r{opacity:0;animation:in .5s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
           ".cur{animation:blink 1.1s steps(1) infinite}")

    def anim(i):
        return "" if STATIC else f' class="r" style="animation-delay:{0.35 + i * 0.16:.2f}s"'

    out = [svg_open(w, h), f"<style>{css}</style>",
           frame(w, h, "belal@github: ~$ neofetch", pad=28, scale=2, uid="cbg")]
    y = 60 + 58
    out.append(f'<g{anim(0)}><text x="{pad}" y="{y}" font-size="{fs + 5}" font-weight="700" '
               f'fill="{FLAX[50]}">{USER}</text></g>')
    y += 22
    out.append(f'<g{anim(1)}><text x="{pad}" y="{y}" font-size="{fs}" fill="{FRAME}">{"-" * len(USER)}</text></g>')
    y += lh - 4
    i = 1
    for i, (k, v) in enumerate(rows, start=2):
        out.append(f'<g{anim(i)}><text x="{pad}" y="{y}" font-size="{fs}">'
                   f'<tspan fill="{ACCENT}" font-weight="700">{k}</tspan><tspan fill="{MUTED}">:</tspan></text>'
                   f'<text x="{pad + key_w}" y="{y}" font-size="{fs}" fill="{TEXT}">{html.escape(v)}</text></g>')
        y += lh
    y += 6
    out.append(f'<g{anim(i + 1)}><text x="{pad}" y="{y}" font-size="{fs}" font-style="italic" '
               f'fill="{FLAX[300]}">&#8220;{html.escape(MOTTO)}&#8221;</text></g>')
    y += 34
    sw = (w - 2 * pad) / 12
    swatches = "".join(f'<rect x="{pad + j * sw:.1f}" y="{y}" width="{sw:.1f}" height="26" fill="{FLAX[s]}"/>'
                       for j, s in enumerate([950, 800, 700, 600, 500, 400, 300, 200, 100, 50]))
    out.append(f'<g{anim(i + 2)}>{swatches}</g>')
    py = h - 40
    out.append(f'<text x="{pad}" y="{py}" font-size="{fs}" fill="{MUTED}"><tspan fill="{ACCENT}">'
               f'belal@github</tspan> ~ $ </text>')
    cls = "" if STATIC else ' class="cur"'
    out.append(f'<rect{cls} x="{pad + 17 * fs * 0.6:.1f}" y="{py - fs + 3}" width="{fs * 0.6:.1f}" '
               f'height="{fs}" fill="{ACCENT}"/>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    for name, cfg in [("info-card.svg", DESKTOP), ("info-card-mobile.svg", MOBILE)]:
        svg = render(cfg)
        with open(os.path.join(HERE, "..", name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name} ({len(svg):,} bytes)")
