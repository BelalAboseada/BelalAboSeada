"""Shared palette, fonts and card chrome, matching belalaboseada.vercel.app:
Flax Smoke ramp (global.css), Cabinet Grotesk titles, Switzer body, film
grain, "( 01 )" section numbering and the 4-point sparkle."""
from fonts import BODY, TITLE, TITLE_MID, css

FLAX = {
    50: "#F4F4F1", 100: "#E8E8DF", 200: "#D2D3C3", 300: "#B6B79F",
    400: "#9B9C7F", 500: "#838566", 600: "#62644C", 700: "#4D4E3D",
    800: "#404133", 900: "#38392E", 950: "#1C1D16",
}

BG = "#16170F"
BG2 = FLAX[950]
FRAME = FLAX[900]
MUTED = FLAX[400]
TEXT = FLAX[100]
ACCENT = FLAX[300]
INK = FLAX[200]

FONT = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
TITLEBAR_H = 44

# 4-point sparkle from the site's services list, unit radius 10
SPARKLE = ("M0,-10C1.6,-1.6 1.6,-1.6 10,0C1.6,1.6 1.6,1.6 0,10"
           "C-1.6,1.6 -1.6,1.6 -10,0C-1.6,-1.6 -1.6,-1.6 0,-10Z")


def grain(uid, alpha=0.07):
    """Film-grain filter; apply to a full-size rect drawn over the background."""
    return (f'<filter id="{uid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>'
            f'<feColorMatrix type="saturate" values="0"/>'
            f'<feComponentTransfer><feFuncA type="table" tableValues="0 {alpha}"/></feComponentTransfer>'
            f'</filter>')


def sparkle(x, y, r, fill, spin=True):
    anim = (f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" '
            f'dur="14s" repeatCount="indefinite" additive="sum"/>') if spin else ""
    return (f'<g transform="translate({x} {y})"><g transform="scale({r / 10})">'
            f'<path d="{SPARKLE}" fill="{fill}">{anim}</path></g></g>')


def frame(w, h, title, num="01", pad=20, scale=1, uid="bg"):
    """Dark grainy card with the site's section header: ( 01 )  Title  ✦.
    scale=2 for SVGs the README shows at half size, so the chrome matches.
    uid keeps ids unique when panels are nested in one SVG."""
    tb = TITLEBAR_H * scale
    fs = 17 * scale
    base = tb / 2 + fs * 0.36
    return (
        f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient>{grain(uid + "n")}</defs>'
        f'<rect width="{w}" height="{h}" rx="{18 * scale}" fill="url(#{uid})"/>'
        f'<rect width="{w}" height="{h}" rx="{18 * scale}" filter="url(#{uid}n)"/>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{18 * scale}" fill="none" '
        f'stroke="{FRAME}" stroke-width="{scale}"/>'
        f'<line x1="{pad}" y1="{tb}" x2="{w - pad}" y2="{tb}" stroke="{FLAX[700]}" stroke-opacity="0.8" '
        f'stroke-width="{scale * 0.75}"/>'
        f'<text x="{pad}" y="{base:.1f}" font-family="{TITLE}" font-size="{fs}" fill="{TEXT}">( {num} )</text>'
        f'<text x="{pad + 64 * scale}" y="{base:.1f}" font-family="{TITLE}" font-size="{fs}" fill="{TEXT}">'
        f'{title}</text>'
        + sparkle(w - pad - 8 * scale, tb / 2, 8 * scale, FLAX[500])
    )


def svg_open(w, h, fonts=("Cabinet", "CabinetMid", "Switzer")):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}"><style>{css(*fonts)}</style>')
