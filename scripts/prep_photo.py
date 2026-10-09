#!/usr/bin/env python3
"""One-time: crop the studio portrait (already on a white seamless, so no
background removal is needed) to the ASCII art's aspect, boost local contrast,
and save assets/portrait-prepped.png.
Usage: python scripts/prep_photo.py "path/to/Belal new .jpg" """
import os
import sys

from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "portrait-prepped.png")
CROP = (0.225, 0.215, 1.0, 0.715)  # head + crossed arms, as fractions of W/H
ASPECT = 700 / 760                   # art area of avi-ascii.svg (w/h)

img = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert("L")
W, H = img.size
l, t, r, b = CROP[0] * W, CROP[1] * H, CROP[2] * W, CROP[3] * H
h = b - t
w = h * ASPECT
l = max(0, r - w)
img = img.crop((int(l), int(t), int(r), int(b))).resize((700, 760), Image.LANCZOS)
img = ImageOps.autocontrast(img, cutoff=(1, 0))
img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=35, threshold=3))
img.save(OUT)
print(f"wrote {OUT} {img.size}")
