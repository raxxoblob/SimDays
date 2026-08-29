"""Split the two 3x3 icon sheets into 18 uniform transparent PNGs.
Each icon is a circular badge (navy ring) on white. We find the circle per cell,
mask everything outside it to transparent, crop square, resize to 400x400."""
import os, numpy as np
from PIL import Image

UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
OUTDIR = os.path.join(UI, "icons")
os.makedirs(OUTDIR, exist_ok=True)
SIZE = 400

SHEETS = {
    "icons1.png": ["lobby_luxury", "office_budget", "office_mid",
                   "office_exec", "shop_clothing", "shop_electronics",
                   "shop_lifestyle", "bar", "restaurant_eleven"],
    "icons2.png": ["office_ext", "apartment_ext", "coffee_shop",
                   "restaurant", "college", "mall",
                   "park", "beach", "garage"],
}

def extract_circle(cell):
    """cell: RGB ndarray. Return RGBA cropped square with outside-circle transparent."""
    h, w, _ = cell.shape
    nonwhite = ~np.all(cell > 238, axis=2)          # ring + content vs white bg
    ys, xs = np.where(nonwhite)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rad = (max(x1 - x0, y1 - y0) / 2) + 2           # include the full ring
    yy, xx = np.ogrid[:h, :w]
    inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= rad ** 2
    rgba = np.dstack([cell, np.where(inside, 255, 0).astype(np.uint8)])
    # crop to the circle's square bounds
    L, T = int(round(cx - rad)), int(round(cy - rad))
    R, Bm = int(round(cx + rad)), int(round(cy + rad))
    L, T = max(L, 0), max(T, 0); R, Bm = min(R, w), min(Bm, h)
    return Image.fromarray(rgba[T:Bm, L:R], "RGBA").resize((SIZE, SIZE), Image.LANCZOS)

for sheet, names in SHEETS.items():
    arr = np.asarray(Image.open(os.path.join(UI, sheet)).convert("RGB"))
    H, W, _ = arr.shape
    ch, cw = H // 3, W // 3
    for r in range(3):
        for c in range(3):
            name = names[r * 3 + c]
            cell = arr[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
            extract_circle(cell).save(os.path.join(OUTDIR, f"icon_{name}.png"))
            print("icon_%s.png" % name)
print("DONE 18 icons ->", OUTDIR)
