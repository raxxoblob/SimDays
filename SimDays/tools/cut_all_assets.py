"""Re-cut every UI asset from the user's transparent sheets.
HUD glass pieces get an opacity boost (self-composite) so they don't see-through.
Icons are circular badges -> crop to square alpha-bbox (transparent corners kept)."""
import numpy as np, os
from PIL import Image, ImageDraw
from scipy import ndimage

UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
ICONS = os.path.join(UI, "icons")
os.makedirs(ICONS, exist_ok=True)

def boost(img, times=2):
    out = img
    for _ in range(times):
        out = Image.alpha_composite(out, img)
    return out

# ── 1) HUD pieces (smooth edges) ──
hud = Image.open(os.path.join(UI, "newhud_transparent_smooth_edges.png")).convert("RGBA")
lbl, n = ndimage.label(np.asarray(hud)[..., 3] > 30)
comps = []
for i in range(1, n + 1):
    ys, xs = np.where(lbl == i)
    if len(xs) < 5000: continue
    comps.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
panel_box = max(comps, key=lambda b: b[3] - b[1])             # tallest
rest = [b for b in comps if b != panel_box]
topbar_box = max(rest, key=lambda b: b[2] - b[0])             # widest
item_box = [b for b in rest if b != topbar_box][0]
boost(hud.crop(topbar_box), 2).save(os.path.join(UI, "hud_topbar.png"))
boost(hud.crop(panel_box), 2).save(os.path.join(UI, "activity_panel.png"))
boost(hud.crop(item_box), 2).save(os.path.join(UI, "activity_item.png"))
print("HUD pieces:", {"topbar": hud.crop(topbar_box).size, "panel": hud.crop(panel_box).size, "item": hud.crop(item_box).size})

# ── Unified circular-badge cutter ─────────────────────────────────────
# Every sheet is a 3x3 grid of same-size circular badges (navy ring). Badges
# can drift within their cell and some have a small decorative tail below, so
# neither the cell centre nor the full bbox is reliable. Instead:
#   * radius  = badge WIDTH / 2   (horizontal extent is clean + consistent)
#   * centre  = horizontal bbox centre, and TOP edge + radius vertically
#               (the top of the circle is always clean; ignores the bottom tail)
#   * ONE shared radius (median) across the whole sheet -> all icons identical
# Then mask to a circle. Works for transparent AND white-background sheets.
def cut_sheet(path, names, prefix, transparent, size=400, inset=3, pad=3):
    im = Image.open(path).convert("RGBA")
    W, H = im.size; ch, cw = H // 3, W // 3
    circle = Image.new("L", (size, size), 0)
    ImageDraw.Draw(circle).ellipse((inset, inset, size - 1 - inset, size - 1 - inset), fill=255)
    flat = [n for row in names for n in row]
    cells, cens, rads = [], [], []
    for r in range(3):
        for c in range(3):
            cell = im.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            a = np.asarray(cell)
            valid = (a[..., 3] > 40) if transparent else (a[..., :3].astype(int) < 238).any(axis=2)
            ys, xs = np.where(valid)
            rad = (xs.max() - xs.min()) / 2.0
            cx = (xs.min() + xs.max()) / 2.0
            cy = ys.min() + rad
            cells.append(cell); cens.append((cx, cy)); rads.append(rad)
    R = int(np.median(rads)) + pad                       # one shared radius = uniform size
    for cell, (cx, cy), name in zip(cells, cens, flat):
        out = cell.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R)))\
                  .resize((size, size), Image.LANCZOS)
        out.putalpha(circle)
        out.save(os.path.join(ICONS, f"{prefix}{name}.png"))
    print(prefix, "done (shared radius %d)" % R)

# stat icons (transparent)
cut_sheet(os.path.join(UI, "transparent_icons.png"),
          [["time", "money", "hunger"], ["hygiene", "energy", "mood"], ["int", "str", "social"]],
          "stat_", transparent=True)
# location icons (transparent)
cut_sheet(os.path.join(UI, "icons1_transparent_smooth.png"),
          [["lobby_luxury", "office_budget", "office_mid"],
           ["office_exec", "shop_clothing", "shop_electronics"],
           ["shop_lifestyle", "bar", "restaurant_eleven"]], "icon_", transparent=True)
cut_sheet(os.path.join(UI, "icons2_transparent_smooth.png"),
          [["office_ext", "apartment_ext", "coffee_shop"],
           ["restaurant", "college", "mall"],
           ["park", "beach", "garage"]], "icon_", transparent=True)
# new icons (white background)
cut_sheet(os.path.join(UI, "new_icons_3.png"),
          [["gym", "hospital", "library"],
           ["house_uptown", "house_suburb", "apartment_block"],
           ["metro", "door_12", "door_14"]], "icon_", transparent=False)
# stat + professional-skill icons (transparent). prefix "" -> exact filenames.
cut_sheet(os.path.join(UI, "new_stats_icons.png"),
          [["stat_app", "stat_work", "skill_med"],
           ["skill_prog", "skill_biz", "skill_cook"],
           ["skill_fit", "skill_mech", "skill_art"]], "", transparent=True)
# new venue icons (transparent). Names are my read of each badge - rename if needed.
cut_sheet(os.path.join(UI, "localisation_icons_new.png"),
          [["hub", "university", "restaurant_eleven"],
           ["clinic", "reception", "nightclub"],
           ["rooftop", "terrace", "elevator"]], "icon_", transparent=True)
print("ALL CUT")
