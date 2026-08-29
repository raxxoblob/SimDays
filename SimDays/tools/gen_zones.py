import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
OUTDIR = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
os.makedirs(OUTDIR, exist_ok=True)
try:
    FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30)
except Exception:
    FONT = ImageFont.load_default()

# key, display name, cx, cy, rx, ry, (r,g,b)
ZONES = [
    ("home",    "Home",         320, 450, 150, 80, (126, 200, 255)),
    ("cafe",    "Coffee Shop",  655, 410, 135, 72, (200, 146,  74)),
    ("gym",     "Gym",          540, 600, 120, 64, (255, 107, 107)),
    ("library", "Library",      575, 715, 120, 64, (176, 123, 232)),
    ("bar",     "Bar",         1055, 665, 130, 66, (255,  95, 162)),
    ("office",  "Nexus Tower", 1235, 300, 160, 85, ( 95, 208, 255)),
    ("mall",    "Mall",         925, 490, 150, 78, (255, 210,  74)),
    ("park",    "Park",         865, 150, 150, 72, (107, 208, 107)),
    ("beach",   "Beach",       1210, 930, 200, 75, (255, 217, 138)),
]

def diamond(cx, cy, rx, ry):
    return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]

def make_hover(cx, cy, rx, ry, color, name):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon(diamond(cx, cy, rx, ry), fill=color + (70,), outline=color + (235,), width=4)
    top = (cx, cy - ry)
    pin_cy = top[1] - 46
    r = 20
    d.ellipse([cx - r, pin_cy - r, cx + r, pin_cy + r], fill=color + (255,), outline=(255, 255, 255, 255), width=3)
    d.polygon([(cx - 11, pin_cy + 10), (cx + 11, pin_cy + 10), (cx, top[1] - 4)], fill=color + (255,))
    d.ellipse([cx - 7, pin_cy - 7, cx + 7, pin_cy + 7], fill=(255, 255, 255, 255))
    tb = d.textbbox((0, 0), name, font=FONT)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    lx, ly = cx - tw // 2, pin_cy - r - th - 14
    d.rectangle([lx - 9, ly - 7, lx + tw + 9, ly + th + 7], fill=(0, 0, 0, 205))
    d.text((lx, ly - tb[1]), name, font=FONT, fill=(255, 255, 255, 255))
    return img

def make_mask(cx, cy, rx, ry):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(img).polygon(diamond(cx, cy, rx, ry), fill=(255, 255, 255, 255))
    return img

# shared transparent idle
Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(os.path.join(OUTDIR, "zone_blank.png"))
for key, name, cx, cy, rx, ry, color in ZONES:
    make_hover(cx, cy, rx, ry, color, name).save(os.path.join(OUTDIR, f"zone_{key}_hi.png"))
    make_mask(cx, cy, rx, ry).save(os.path.join(OUTDIR, f"zone_{key}_mask.png"))
    print(key, "done")
print("ALL ZONES DONE")
