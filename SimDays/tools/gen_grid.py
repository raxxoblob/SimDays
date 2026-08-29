"""Overlay a labelled coordinate grid on the map (in 1920x1080 game space)
so the user can reference cells or draw zone shapes accurately."""
from PIL import Image, ImageDraw, ImageFont
import string

MAP = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_city.png"
OUT = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\map_grid.png"
W, H = 1920, 1080
STEP = 96  # px per cell

img = Image.open(MAP).convert("RGBA").resize((W, H))
d = ImageDraw.Draw(img, "RGBA")
try:
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
except Exception:
    font = ImageFont.load_default()

cols = string.ascii_uppercase  # A, B, C ...
# vertical lines + column letters
for i, x in enumerate(range(0, W + 1, STEP)):
    d.line([(x, 0), (x, H)], fill=(255, 255, 255, 90), width=1)
    if x < W:
        d.text((x + 3, 2), cols[i], font=font, fill=(255, 255, 0, 255))
# horizontal lines + row numbers
for j, y in enumerate(range(0, H + 1, STEP)):
    d.line([(0, y), (W, y)], fill=(255, 255, 255, 90), width=1)
    if y < H:
        d.text((3, y + 2), str(j + 1), font=font, fill=(255, 255, 0, 255))

img.convert("RGB").save(OUT)
print("saved", OUT)
