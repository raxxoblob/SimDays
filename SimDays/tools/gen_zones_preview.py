"""Render ALL zones onto the map in one image, uniform blue — a reference
sheet for designing custom icons. Zone coords mirror gen_zones.py."""
from PIL import Image, ImageDraw, ImageFont

MAP = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_city.png"
OUT = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\map_zones_preview.png"
W, H = 1920, 1080
BLUE = (80, 160, 255)

# key, name, cx, cy, rx, ry  (same as gen_zones.py)
ZONES = [
    ("home",    "Home",         320, 450, 150, 80),
    ("cafe",    "Coffee Shop",  655, 410, 135, 72),
    ("gym",     "Gym",          540, 600, 120, 64),
    ("library", "Library",      575, 715, 120, 64),
    ("bar",     "Bar",         1055, 665, 130, 66),
    ("office",  "Nexus Tower", 1235, 300, 160, 85),
    ("mall",    "Mall",         925, 490, 150, 78),
    ("park",    "Park",         865, 150, 150, 72),
    ("beach",   "Beach",       1210, 930, 200, 75),
]

base = Image.open(MAP).convert("RGBA").resize((W, H))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
try:
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30)
except Exception:
    font = ImageFont.load_default()

def diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]

for key, name, cx, cy, rx, ry in ZONES:
    d.polygon(diamond(cx, cy, rx, ry), fill=BLUE + (70,), outline=BLUE + (235,), width=4)
    top = (cx, cy - ry)
    pin_cy = top[1] - 46
    r = 20
    d.ellipse([cx - r, pin_cy - r, cx + r, pin_cy + r], fill=BLUE + (255,), outline=(255, 255, 255, 255), width=3)
    d.polygon([(cx - 11, pin_cy + 10), (cx + 11, pin_cy + 10), (cx, top[1] - 4)], fill=BLUE + (255,))
    d.ellipse([cx - 7, pin_cy - 7, cx + 7, pin_cy + 7], fill=(255, 255, 255, 255))
    tb = d.textbbox((0, 0), name, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    lx, ly = cx - tw // 2, pin_cy - r - th - 14
    d.rectangle([lx - 9, ly - 7, lx + tw + 9, ly + th + 7], fill=(0, 0, 0, 205))
    d.text((lx, ly - tb[1]), name, font=font, fill=(255, 255, 255, 255))

Image.alpha_composite(base, ov).convert("RGB").save(OUT)
print("saved", OUT)
