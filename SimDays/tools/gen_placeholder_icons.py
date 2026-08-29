"""Generate circular badge placeholders matching the icon style (navy ring,
colored centre, white label) for venues we have no real icon for yet."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui\icons"
os.makedirs(OUT, exist_ok=True)
SIZE = 400
RING = (26, 38, 74)        # navy
try:
    FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 64)
except Exception:
    FONT = ImageFont.load_default()

# key, label, centre colour
PLACE = [
    ("gym",     "GYM",      (180, 70, 70)),
    ("szpital", "HOSPITAL", (70, 130, 160)),
]

for key, label, col in PLACE:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = 6
    d.ellipse([m, m, SIZE - m, SIZE - m], fill=col + (255,), outline=RING + (255,), width=16)
    tb = d.textbbox((0, 0), label, font=FONT)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    d.text(((SIZE - tw) / 2 - tb[0], (SIZE - th) / 2 - tb[1]), label, font=FONT,
           fill=(255, 255, 255, 255))
    img.save(os.path.join(OUT, f"icon_{key}.png"))
    print("icon_%s.png" % key)
print("DONE placeholders")
