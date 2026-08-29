"""From tools/zones.json (road-aligned polygons), render per-zone in-game assets:
  images/ui/z_<key>_idle.png - dim district icon at centre (resting state)
  images/ui/z_<key>_hi.png   - blue fill + outline + name + bright icon (hover)
  images/ui/z_<key>_mask.png - solid polygon (click hit-area / focus_mask)
Plus images/zones_labeled.png - all zones + names, for review."""
import json, os
from PIL import Image, ImageDraw, ImageFont

ZONES = json.load(open(r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\tools\zones.json"))
MAP = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_city.webp"
UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
ICONS = os.path.join(UI, "icons")
GW, GH = 1920, 1080
BLUE = (90, 170, 255)
ICON_PX = 112
IDLE_ALPHA = 0.55      # resting icon opacity; full (1.0) on hover
ICON_MIN_Y = 205       # push icons below the topbar HUD (which covers y 8-137)
ICON_OFFSET = {"bogate_domki": (-55, 0)}   # per-zone nudge (dx, dy) for the icon+label

# index (sorted order from build_zones) -> key, display name, district icon file
MAPPING = [
    ("bogate_domki", "Uptown",     "house_uptown"),
    ("warehouse",    "Warehouse",  "garage"),
    ("park",         "Park",       "park"),
    ("domki",        "Suburbs",    "house_suburb"),
    ("bloki",        "Apartments", "apartment_block"),
    ("centrum",      "Downtown",   "office_ext"),
    ("szpital",      "Hospital",   "hospital"),
    ("mall",         "Mall",       "mall"),
    ("plaza",        "Beach",      "beach"),
]
try:
    FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
except Exception:
    FONT = ImageFont.load_default()

def load_icon(name, alpha=1.0):
    ic = Image.open(os.path.join(ICONS, f"icon_{name}.png")).convert("RGBA").resize((ICON_PX, ICON_PX), Image.LANCZOS)
    if alpha < 1.0:
        a = ic.getchannel("A").point(lambda v: int(v * alpha))
        ic.putalpha(a)
    return ic

def paste_icon(img, ic, cx, cy):
    img.alpha_composite(ic, (cx - ICON_PX // 2, cy - ICON_PX // 2))

def draw_label(d, cx, cy, name):
    tb = d.textbbox((0, 0), name, font=FONT)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    ly = cy - (ICON_PX // 2) - 8 - th
    if ly < 150:                       # would sit under the topbar HUD -> drop below
        ly = cy + (ICON_PX // 2) + 8
    lx = cx - tw // 2
    d.rectangle([lx - 9, ly - 7, lx + tw + 9, ly + th + 7], fill=(0, 0, 0, 210))
    d.text((lx, ly - tb[1]), name, font=FONT, fill=(255, 255, 255, 255))

labeled = Image.open(MAP).convert("RGBA").resize((GW, GH))
lov = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
ld = ImageDraw.Draw(lov)

for (key, name, icon), z in zip(MAPPING, ZONES):
    poly = [tuple(p) for p in z["poly"]]
    cx, cy = int(z["centroid"][0]), int(z["centroid"][1])
    _ox, _oy = ICON_OFFSET.get(key, (0, 0))
    ix = cx + _ox
    iy = max(cy, ICON_MIN_Y) + _oy   # clear the topbar HUD, plus any per-zone nudge
    icon_dim = load_icon(icon, IDLE_ALPHA)
    icon_full = load_icon(icon, 1.0)

    # idle: dim icon only
    idle = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    paste_icon(idle, icon_dim, ix, iy)
    idle.save(os.path.join(UI, f"z_{key}_idle.png"))

    # hover: highlight + bright icon + name (polygon stays on the true zone)
    hi = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    ImageDraw.Draw(hi).polygon(poly, fill=BLUE + (95,), outline=BLUE + (255,), width=5)
    paste_icon(hi, icon_full, ix, iy)
    draw_label(ImageDraw.Draw(hi), ix, iy, name)
    hi.save(os.path.join(UI, f"z_{key}_hi.png"))

    # mask
    mk = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    ImageDraw.Draw(mk).polygon(poly, fill=(255, 255, 255, 255))
    mk.save(os.path.join(UI, f"z_{key}_mask.png"))

    # review overlay (bright)
    ld.polygon(poly, fill=BLUE + (80,), outline=BLUE + (255,), width=4)
    paste_icon(lov, icon_full, ix, iy)
    draw_label(ld, ix, iy, name)
    print(f"{key:14s} -> idle / hi / mask")

Image.alpha_composite(labeled, lov).convert("RGB").save(r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\zones_labeled.png")
print("saved zones_labeled.png + assets")
