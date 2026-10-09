#!/usr/bin/env python3
"""Append ?v=<content hash> to the README's local SVG links (src and srcset)
so browsers fetch a fresh copy as soon as an image changes. GitHub lets
browsers cache README images for ~5 minutes otherwise.
Run after regenerating any SVG; the daily heatmap is left unstamped."""
import hashlib
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKIP = {"contrib-heatmap.svg", "contrib-heatmap-mobile.svg"}


def stamp(match):
    attr, name = match.group(1), match.group(2)
    if name in SKIP:
        return f'{attr}="./{name}"'
    with open(os.path.join(ROOT, name), "rb") as f:
        v = hashlib.sha1(f.read()).hexdigest()[:8]
    return f'{attr}="./{name}?v={v}"'


if __name__ == "__main__":
    p = os.path.join(ROOT, "README.md")
    with open(p, encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r'(src|srcset)="\./([\w.-]+\.svg)(?:\?v=\w+)?"', stamp, s)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("\n".join(l.strip() for l in s.splitlines() if ".svg" in l and ("src=" in l or "srcset=" in l)))
