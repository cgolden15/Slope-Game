from PIL import Image
import os
from collections import Counter

orig_dir = "extracted/all-assets"
files = [f for f in os.listdir(orig_dir) if f.endswith(".png") and "Texture2D" in f]
for f in sorted(files):
    img = Image.open(os.path.join(orig_dir, f)).convert("RGBA")
    w, h = img.size
    pixels = list(img.getdata())
    opaque = [(r, g, b) for r, g, b, a in pixels if a > 30]
    if opaque:
        top2 = Counter(opaque).most_common(2)
        print("%s  %dx%d  %s" % (f[:42], w, h, top2))
