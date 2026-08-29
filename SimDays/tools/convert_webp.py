"""Convert heavy PNG assets to WebP and delete the PNGs.
Backgrounds: lossy q88. Sprites: lossless (preserve rembg alpha edges).
UI/icons stay PNG for now (small + still iterated). Game refers to images by
registered NAME, so only images.rpy path strings need updating."""
import os, glob
from PIL import Image

LOC = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations"
ZOE = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\characters\zoe"
SKIP = {"map_marked.png"}   # user working file — leave editable

def convert(path, lossless, quality):
    im = Image.open(path)
    if im.mode == "P":
        im = im.convert("RGBA")
    out = os.path.splitext(path)[0] + ".webp"
    im.save(out, "WEBP", lossless=lossless, quality=quality, method=6)
    before = os.path.getsize(path); after = os.path.getsize(out)
    os.remove(path)
    return before, after

tb = ta = 0
for p in glob.glob(os.path.join(LOC, "*.png")):
    if os.path.basename(p).lower() in SKIP:
        continue
    b, a = convert(p, lossless=False, quality=88); tb += b; ta += a
for p in glob.glob(os.path.join(ZOE, "*.png")):   # top-level sprites only
    b, a = convert(p, lossless=True, quality=100); tb += b; ta += a

print(f"converted. before={tb/1024/1024:.1f}MB  after={ta/1024/1024:.1f}MB  saved={ (tb-ta)/1024/1024:.1f}MB")
