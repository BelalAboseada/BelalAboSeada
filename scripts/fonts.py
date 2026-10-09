#!/usr/bin/env python3
"""Website fonts for the SVGs. GitHub serves README SVGs through <img>, which
can't fetch web fonts, so the site's Cabinet Grotesk (titles) and Switzer
(body) are embedded as small woff2 subsets via data-URI @font-face.

`python scripts/fonts.py` rebuilds the subsets from the variable TTFs in
assets/fonts/ (copied from the portfolio, not committed); the subsets are
committed so the daily workflow can render without the originals."""
import base64
import os
import string

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "assets", "fonts")
CHARS = string.printable.strip() + " ×·→“”’–—•"
FACES = {
    # css family: (source ttf, weight instance, subset file)
    "Cabinet": ("CabinetGrotesk-Variable.ttf", 800, "cabinet-800.woff2"),
    "CabinetMid": ("CabinetGrotesk-Variable.ttf", 500, "cabinet-500.woff2"),
    "Switzer": ("Switzer-Variable.ttf", 500, "switzer-500.woff2"),
}
TITLE = "Cabinet, 'Cabinet Grotesk', 'Arial Black', sans-serif"
TITLE_MID = "CabinetMid, 'Cabinet Grotesk', Arial, sans-serif"
BODY = "Switzer, 'Helvetica Neue', Arial, sans-serif"


def build():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    for fam, (src, wght, out) in FACES.items():
        font = instancer.instantiateVariableFont(TTFont(os.path.join(DIR, src)), {"wght": wght})
        opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
        sub = subset.Subsetter(opts); sub.populate(text=CHARS); sub.subset(font)
        font.flavor = "woff2"; font.save(os.path.join(DIR, out))
        print(f"{out}: {os.path.getsize(os.path.join(DIR, out)):,} bytes")


def css(*families):
    """@font-face rules for the given families (default: all)."""
    rules = []
    for fam in families or FACES:
        with open(os.path.join(DIR, FACES[fam][2]), "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        rules.append(f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(rules)


if __name__ == "__main__":
    build()
