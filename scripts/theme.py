"""Shared palette + frame helpers. Colors are the Flax Smoke ramp from
belalaboseada.online (global.css) -- one hue family, no reds/blues."""

FLAX = {
    50: "#F4F4F1", 100: "#E8E8DF", 200: "#D2D3C3", 300: "#B6B79F",
    400: "#9B9C7F", 500: "#838566", 600: "#62644C", 700: "#4D4E3D",
    800: "#404133", 900: "#38392E", 950: "#1C1D16",
}

BG = "#16170F"
BG2 = FLAX[950]
FRAME = FLAX[700]
MUTED = FLAX[400]
TEXT = FLAX[100]
ACCENT = FLAX[300]
INK = FLAX[200]

FONT = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
TITLEBAR_H = 30


def frame(w, h, title, pad=20, scale=1, uid="bg"):
    """Window chrome: gradient body, hairline border, three dots, centered title.
    scale=2 for SVGs the README shows at half size, so the chrome matches.
    uid keeps the gradient id unique when panels are nested in one SVG."""
    tb = TITLEBAR_H * scale
    dots = "".join(
        f'<circle cx="{pad + i * 16 * scale}" cy="{tb / 2}" r="{5 * scale}" fill="{c}"/>'
        for i, c in enumerate([FLAX[300], FLAX[500], FLAX[700]])
    )
    return (
        f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient></defs>'
        f'<rect width="{w}" height="{h}" rx="{12 * scale}" fill="url(#{uid})"/>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{12 * scale}" fill="none" '
        f'stroke="{FRAME}" stroke-width="1"/>'
        f'<line x1="0" y1="{tb}" x2="{w}" y2="{tb}" stroke="{FRAME}" stroke-opacity="0.7"/>'
        f'{dots}'
        f'<text x="{w / 2}" y="{tb / 2 + 4 * scale}" fill="{MUTED}" font-size="{12 * scale}" '
        f'text-anchor="middle">{title}</text>'
    )


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}">')
