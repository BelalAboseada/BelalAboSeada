#!/usr/bin/env python3
"""Links section in the same card language as the other panels: a
"( 04 ) Links" header card plus one small dark card per link (number, olive
icon badge, name, handle, arrow). Every tile is its own SVG so the README can
wrap each in a link. Each comes in a desktop shape (wide) and a mobile shape
(square, bigger type) that the README swaps with <picture media=...>.
Writes links/*.svg. Brand icon paths live in assets/icons/ (Simple Icons)."""
import html
import os
import re

from fonts import BODY, TITLE
from theme import ACCENT, BG, BG2, FLAX, FRAME, MUTED, REDUCED, TEXT, grain, sparkle, css

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "links")
ICONS = os.path.join(ROOT, "assets", "icons")

ASTERISK = "".join(f'<rect x="-2" y="-11" width="4" height="22" rx="2" transform="rotate({a})"/>' for a in (0, 45, 90, 135))
LINKEDIN = ('<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05'
            ' 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5c0-1.2-.02-2.73-1.66-2.73-1.66 0-1.92 1.3-1.92 2.64V21h-4z"/>')

# (file, name, handle, href, icon)  icon: simple-icons slug, or raw 24x24 svg markup
LINKS = [
    ("portfolio", "Portfolio", "belalaboseada.vercel.app", "https://belalaboseada.vercel.app/", "asterisk"),
    ("email", "Email", "belalaboseada@gmail.com", "mailto:belalaboseada@gmail.com", "gmail"),
    ("linkedin", "LinkedIn", "in/belal-hesham", "https://www.linkedin.com/in/belal-hesham", "linkedin"),
    ("cv", "CV", "view · download", "https://drive.google.com/file/d/1Ot_5t6ed1R2TANS3rw6u6mf6C7ct8OCl/view?usp=sharing", "googledrive"),
    ("youtube", "YouTube", "@belalaboseada", "https://www.youtube.com/@belalaboseada", "youtube"),
    ("tiktok", "TikTok", "@belalaboseada", "https://www.tiktok.com/@Belalaboseada", "tiktok"),
    ("instagram", "Instagram", "@belal_aboseada", "https://www.instagram.com/belal_aboseada", "instagram"),
    ("facebook", "Facebook", "Belal Hesham", "https://www.facebook.com/belal.hesham.1848", "facebook"),
]


def icon_markup(icon):
    """24x24 glyph, filled with the paper colour."""
    if icon == "asterisk":
        return f'<g transform="translate(12 12)">{ASTERISK}</g>'
    if icon == "linkedin":
        return LINKEDIN
    with open(os.path.join(ICONS, f"{icon}.svg"), encoding="utf-8") as f:
        return "".join(f'<path d="{d}"/>' for d in re.findall(r'<path d="([^"]+)"', f.read()))


def open_svg(w, h, uid):
    anim = ("@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
            ".r{opacity:0;animation:in .6s cubic-bezier(.2,.8,.2,1) both}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{css("Cabinet", "Switzer")}{anim}{REDUCED}</style>'
            f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/>'
            f'<stop offset="1" stop-color="{BG}"/></linearGradient>{grain(uid + "n")}</defs>')


def card(w, h, uid, r):
    return (f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#{uid})"/>'
            f'<rect width="{w}" height="{h}" rx="{r}" filter="url(#{uid}n)"/>'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{r}" fill="none" stroke="{FRAME}" stroke-width="2"/>')


def arrow(x, y, s):
    return (f'<path d="M{x} {y + s} L{x + s} {y} M{x + s * 0.3} {y} H{x + s} V{y + s * 0.7}" fill="none" stroke="{ACCENT}" '
            f'stroke-width="{s * 0.13:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def badge(cx, cy, r, icon):
    s = r * 1.05 / 24   # 24-unit glyph scaled to ~1.05 r (about half the badge)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FLAX[500]}"/>'
            f'<g transform="translate({cx - 12 * s} {cy - 12 * s}) scale({s})" fill="{FLAX[50]}">{icon_markup(icon)}</g>')


def tile_desktop(i, name, handle, icon):
    w, h, uid = 424, 220, f"d{i}"
    delay = f' class="r" style="animation-delay:{0.1 + i * 0.07:.2f}s"'
    return (open_svg(w, h, uid) + card(w, h, uid, 28) +
            f'<g{delay}>'
            f'<text x="30" y="48" font-family="{BODY}" font-size="20" fill="{FLAX[600]}">{i + 1:02d}</text>'
            + arrow(w - 58, 26, 26) + badge(70, 140, 38, icon) +
            f'<text x="128" y="136" font-family="{TITLE}" font-size="40" fill="{TEXT}">{html.escape(name)}</text>'
            f'<text x="129" y="170" font-family="{BODY}" font-size="20" fill="{MUTED}">{html.escape(handle)}</text>'
            '</g></svg>')


def tile_mobile(i, name, icon):
    w, h, uid = 300, 330, f"m{i}"
    delay = f' class="r" style="animation-delay:{0.1 + i * 0.07:.2f}s"'
    return (open_svg(w, h, uid) + card(w, h, uid, 36) +
            f'<g{delay}>'
            f'<text x="26" y="50" font-family="{BODY}" font-size="24" fill="{FLAX[600]}">{i + 1:02d}</text>'
            + arrow(w - 60, 26, 30) + badge(150, 150, 62, icon) +
            f'<text x="150" y="282" text-anchor="middle" font-family="{TITLE}" font-size="{46 if len(name) < 9 else 40}" '
            f'fill="{TEXT}">{html.escape(name)}</text></g></svg>')


def header(w, h, scale, mobile):
    uid = "hd" + ("m" if mobile else "")
    fs = 17 * scale
    y = h / 2 + fs * 0.36
    right = "" if mobile else (
        f'<text x="{w - 110}" y="{y:.1f}" text-anchor="end" font-family="{BODY}" font-size="{11 * scale}" '
        f'letter-spacing="3" fill="{MUTED}">( WORK ) ROW 1 · ( CREATE ) ROW 2</text>')
    return (open_svg(w, h, uid) + card(w, h, uid, 18 * scale) +
            f'<text x="28" y="{y:.1f}" font-family="{TITLE}" font-size="{fs}" fill="{TEXT}">( 04 )</text>'
            f'<text x="{28 + 64 * scale}" y="{y:.1f}" font-family="{TITLE}" font-size="{fs}" fill="{TEXT}">Links</text>'
            + right + sparkle(w - 28 - 8 * scale, h / 2, 8 * scale, FLAX[500]) + '</svg>')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    files = {"links-header.svg": header(1720, 96, 2, False), "links-header-mobile.svg": header(740, 96, 2, True)}
    for i, (fid, name, handle, _, icon) in enumerate(LINKS):
        files[f"{fid}.svg"] = tile_desktop(i, name, handle, icon)
        files[f"{fid}-m.svg"] = tile_mobile(i, name, icon)
    for fn, svg in files.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"wrote {len(files)} files to links/ ({sum(len(s) for s in files.values()) // 1024} KB)")
