"""Split statsicons.png (3x3 glossy circular badges on a DARK bg) into 9
transparent PNGs. Detect each badge by brightness, mask to its circle."""
import os, numpy as np
from PIL import Image

SRC = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui\statsicons.png"
OUT = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui\icons"
os.makedirs(OUT, exist_ok=True)
SIZE = 400

NAMES = [["time", "money", "hunger"],
         ["hygiene", "energy", "mood"],
         ["int", "str", "social"]]

arr = np.asarray(Image.open(SRC).convert("RGB"))
H, W, _ = arr.shape
ch, cw = H // 3, W // 3

def extract(cell):
    h, w, _ = cell.shape
    bright = cell.max(axis=2)
    ys, xs = np.where(bright > 105)            # solid badge pixels
    cx, cy = xs.mean(), ys.mean()              # centroid = badge centre (glow-robust)
    rad = 0.46 * h                             # fixed radius (badges are uniform, ~fills cell height)
    yy, xx = np.ogrid[:h, :w]
    inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= rad ** 2
    rgba = np.dstack([cell, np.where(inside, 255, 0).astype(np.uint8)]).astype(np.uint8)
    full = Image.fromarray(rgba, "RGBA")
    box = (int(round(cx - rad)), int(round(cy - rad)),
           int(round(cx + rad)), int(round(cy + rad)))
    return full.crop(box).resize((SIZE, SIZE), Image.LANCZOS)

for r in range(3):
    for c in range(3):
        cell = arr[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
        name = NAMES[r][c]
        extract(cell).save(os.path.join(OUT, f"stat_{name}.png"))
        print(f"stat_{name}.png")
print("DONE 9 stat icons")
