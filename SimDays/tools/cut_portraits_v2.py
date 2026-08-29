"""
Auto-detect face/head area per sprite and cut two portrait variants:
  portrait_<npc>_tight.png  — face only, close crop
  portrait_<npc>_bust.png   — head + shoulders, more context

Output: images/characters/templates/my_portraits/
Also saves a side-by-side comparison grid: _comparison.png
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os

CHARS = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\characters"
OUT   = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\characters\templates\my_portraits"
SIZE  = 400
os.makedirs(OUT, exist_ok=True)

NPCS = [
    ("nora",      "nora/nora_cafe_normal.png"),
    ("marcus",    "marcus/marcus_casual_normal.png"),
    ("caroline",  "caroline/caroline_normal.png"),
    ("lena",      "dr_lena/drlena_normal.png"),
    ("natalie",   "natalie/natalie_normal.png"),
    ("martha",    "martha/martha_neutral.png"),
    ("elle",      "elle/elle_sundress_normal.png"),
    ("zoe",       "zoe/zoe_punk_smile.webp"),
    ("sam",       "sam/sam_normal.png"),
    ("eli",       "eli/eli_normal.png"),
    ("kai",       "kai/kai_normal.png"),
]

# circle mask
def make_circle_mask(size):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse((3, 3, size-4, size-4), fill=255)
    return m

CIRCLE = make_circle_mask(SIZE)

def detect_head(im):
    """Return (cx, head_top, neck_y) in image coords."""
    a = np.array(im.convert("RGBA"))
    valid = a[..., 3] > 40

    # scan rows for width to find neck (local width minimum in upper third)
    h, w = valid.shape
    scan_top, scan_bot = 40, h // 3
    row_stats = []
    for y in range(scan_top, scan_bot):
        xs = np.where(valid[y])[0]
        if len(xs) < 10:
            row_stats.append((y, 0, w//2, w//2))
        else:
            row_stats.append((y, len(xs), int(xs.min()), int(xs.max())))

    # head_top = first row with >30 opaque pixels
    head_top = next((y for y,wid,_,_ in row_stats if wid > 30), scan_top)

    # neck = narrowest row between head_top+80 and scan_bot
    neck_candidates = [(y, wid) for y,wid,_,_ in row_stats
                       if y > head_top + 80 and wid > 0]
    if neck_candidates:
        neck_y = min(neck_candidates, key=lambda x: x[1])[0]
    else:
        neck_y = scan_bot

    # horizontal face center: average of left+right edge midpoints in head zone
    face_mids = [(xl+xr)//2 for y,wid,xl,xr in row_stats
                 if head_top <= y <= neck_y and wid > 30]
    cx = int(np.median(face_mids)) if face_mids else w // 2

    return cx, head_top, neck_y


def crop_portrait(im, cx, head_top, neck_y, extra_bottom=0.4, extra_top=0.15):
    """
    Crop a square centered on the face.
    extra_top:    fraction of head height to add above head_top
    extra_bottom: fraction of head height to add below neck_y (shoulders)
    """
    head_h = neck_y - head_top
    top    = int(head_top - head_h * extra_top)
    bot    = int(neck_y   + head_h * extra_bottom)
    half   = (bot - top) // 2
    # force square by using half as the radius
    left   = cx - half
    right  = cx + half
    top    = (top + bot) // 2 - half
    bot    = top + half * 2

    # clamp to image bounds (pad with transparency if needed)
    iw, ih = im.size
    if left < 0 or top < 0 or right > iw or bot > ih:
        padded = Image.new("RGBA", (iw + abs(min(left,0))*2, ih), (0,0,0,0))
        offset = abs(min(left,0))
        padded.paste(im, (offset, 0))
        left += offset; right += offset
        return padded.crop((left, max(top,0), right, min(bot, padded.height)))

    return im.crop((left, top, right, bot))


results = []
for npc_id, rel_path in NPCS:
    src = os.path.join(CHARS, rel_path)
    if not os.path.exists(src):
        print(f"MISSING: {src}")
        results.append((npc_id, None, None))
        continue

    im = Image.open(src).convert("RGBA")
    cx, head_top, neck_y = detect_head(im)
    print(f"{npc_id}: head_top={head_top}  neck_y={neck_y}  cx={cx}  sprite={im.size}")

    # tight: just face, minimal shoulders
    tight_crop = crop_portrait(im, cx, head_top, neck_y, extra_bottom=0.15, extra_top=0.2)
    tight = tight_crop.resize((SIZE, SIZE), Image.LANCZOS)
    tight.putalpha(CIRCLE)
    tight.save(os.path.join(OUT, f"portrait_{npc_id}_tight.png"))

    # bust: more shoulders, more breathing room
    bust_crop = crop_portrait(im, cx, head_top, neck_y, extra_bottom=0.7, extra_top=0.25)
    bust = bust_crop.resize((SIZE, SIZE), Image.LANCZOS)
    bust.putalpha(CIRCLE)
    bust.save(os.path.join(OUT, f"portrait_{npc_id}_bust.png"))

    results.append((npc_id, tight, bust))

# ── comparison grid ────────────────────────────────────────────────────
# columns: name label | tight | bust
# rows: one per NPC
THUMB = 200
PAD = 12
LABEL_W = 120
ROW_H = THUMB + PAD
TOTAL_W = LABEL_W + PAD + THUMB + PAD + THUMB + PAD
TOTAL_H = ROW_H * len(results) + PAD

grid = Image.new("RGBA", (TOTAL_W, TOTAL_H), (30, 32, 45, 255))
draw = ImageDraw.Draw(grid)

for i, (npc_id, tight, bust) in enumerate(results):
    y = PAD + i * ROW_H
    draw.text((PAD, y + THUMB//2 - 8), npc_id, fill=(200, 220, 255, 255))
    if tight:
        t = tight.resize((THUMB, THUMB), Image.LANCZOS)
        grid.paste(t, (LABEL_W + PAD, y), t)
    if bust:
        b = bust.resize((THUMB, THUMB), Image.LANCZOS)
        grid.paste(b, (LABEL_W + PAD*2 + THUMB, y), b)

# header labels
draw.text((LABEL_W + PAD + THUMB//2 - 20, 2), "TIGHT", fill=(255,200,100,255))
draw.text((LABEL_W + PAD*2 + THUMB + THUMB//2 - 16, 2), "BUST", fill=(100,200,255,255))

grid.save(os.path.join(OUT, "_comparison.png"))
print(f"\nSaved to {OUT}")
print("Open _comparison.png to compare tight vs bust variants.")
