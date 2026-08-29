"""Cut head-and-shoulders portraits from NPC _normal sprites.
Output: images/ui/icons/portrait_<npc>.png  (200x200 px, circle-masked)
Also saves a portrait_preview.png grid so you can eyeball all at once.

Adjust CROP if a portrait clips hair or cuts chin. (left, top, right, bottom)
Default crops the upper ~40% of the 1024x1536 sprite — head + shoulders.
"""
from PIL import Image, ImageDraw
import os

CHARS = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\characters"
OUT   = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\SimDays\SimDays\game\images\ui\icons"
SIZE  = 200
CROP  = (112, 40, 912, 640)   # (left, top, right, bottom) on 1024x1536 sprite

NPCS = [
    ("nora",      "nora/nora_cafe_normal.png"),
    ("marcus",    "marcus/marcus_casual_normal.png"),
    ("caroline",  "caroline/caroline_normal.png"),
    ("lena",      "dr_lena/drlena_normal.png"),
    ("natalie",   "natalie/natalie_normal.png"),
    ("martha",    "martha/martha_neutral.png"),
    ("elle",      "elle/elle_sundress_normal.png"),
    ("zoe",       "zoe/zoe_punk_smile.png"),
    ("sam",       "sam/sam_normal.png"),
    ("eli",       "eli/eli_normal.png"),
    ("kai",       "kai/kai_normal.png"),
]

# circle mask
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).ellipse((2, 2, SIZE - 3, SIZE - 3), fill=255)

portraits = []
for npc_id, rel_path in NPCS:
    src = os.path.join(CHARS, rel_path)
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        portraits.append(None)
        continue
    im = Image.open(src).convert("RGBA")
    cropped = im.crop(CROP).resize((SIZE, SIZE), Image.LANCZOS)
    cropped.putalpha(mask)
    dest = os.path.join(OUT, f"portrait_{npc_id}.png")
    cropped.save(dest)
    print(f"portrait_{npc_id}.png  ({im.size} -> crop {CROP} -> {SIZE}x{SIZE})")
    portraits.append(cropped)

# preview grid (4 cols)
cols = 4
rows = (len(portraits) + cols - 1) // cols
pad = 10
grid = Image.new("RGBA", (cols * (SIZE + pad) + pad, rows * (SIZE + pad) + pad), (30, 30, 40, 255))
for i, (p, (npc_id, _)) in enumerate(zip(portraits, NPCS)):
    if p is None: continue
    x = pad + (i % cols) * (SIZE + pad)
    y = pad + (i // cols) * (SIZE + pad)
    grid.paste(p, (x, y), p)
preview = os.path.join(OUT, "portrait_preview.png")
grid.save(preview)
print(f"\nPreview saved: {preview}")
print("Done. Check portrait_preview.png — adjust CROP at top of script if needed.")
