"""Cut the three new icon sheets + wire phone_frame."""
import numpy as np, os
from PIL import Image, ImageDraw

UI    = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\SimDays\SimDays\game\images\ui"
ICONS = os.path.join(UI, "icons")
os.makedirs(ICONS, exist_ok=True)


def cut_sheet(filename, names, prefix, rows, cols, circle=True, size=400, inset=3, pad=3):
    """Generic grid cutter. names is a flat list in row-major order."""
    im = Image.open(os.path.join(UI, filename)).convert("RGBA")
    W, H = im.size
    cw, ch = W // cols, H // rows

    # circle mask (shared across all cells so icons are uniform)
    mask = Image.new("L", (size, size), 0)
    if circle:
        ImageDraw.Draw(mask).ellipse(
            (inset, inset, size - 1 - inset, size - 1 - inset), fill=255)
    else:
        mask = None

    cells, cens, rads = [], [], []
    for r in range(rows):
        for c in range(cols):
            cell = im.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            a = np.asarray(cell)
            valid = a[..., 3] > 40
            ys, xs = np.where(valid)
            if len(xs) == 0:
                cells.append(None); cens.append((cw // 2, ch // 2)); rads.append(min(cw, ch) // 3)
                continue
            rad = (xs.max() - xs.min()) / 2.0
            cx  = (xs.min() + xs.max()) / 2.0
            cy  = ys.min() + rad           # top of circle + radius = centre
            cells.append(cell); cens.append((cx, cy)); rads.append(rad)

    R = int(np.median([r for r in rads if r > 0])) + pad

    for cell, (cx, cy), name in zip(cells, cens, names):
        if cell is None:
            print(f"  SKIP {name} (empty cell)")
            continue
        cropped = cell.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R)))
        out = cropped.resize((size, size), Image.LANCZOS)
        if mask:
            out.putalpha(mask)
        dest = os.path.join(ICONS if not prefix.startswith("phone") else UI, f"{prefix}{name}.png")
        out.save(dest)

    print(f"{filename} -> {rows}x{cols}, R={R}, cut {len(names)} icons")


# ── talk_icons.png (3x3) → topic_* ───────────────────────────────────────────
cut_sheet("talk_icons.png",
    ["music", "sports", "art",
     "food",  "ambition", "travel",
     "movies","nightlife","work"],
    prefix="topic_", rows=3, cols=3, circle=True)

# ── act_icons.png (2x2) → act_* ──────────────────────────────────────────────
cut_sheet("act_icons.png",
    ["talk",   "gift",
     "invite", "leave"],
    prefix="act_", rows=2, cols=2, circle=True)

# ── telephone_icons.png (3x3, 1536x1024) → app_* ─────────────────────────────
# These are rounded-square tiles; skip circle mask so corners stay rounded.
cut_sheet("telephone_icons.png",
    ["messages", "contacts", "map",
     "jobs",     "bank",     "stocks",
     "groceries","tips",     "settings"],
    prefix="app_", rows=3, cols=3, circle=False)

print("ALL DONE")
