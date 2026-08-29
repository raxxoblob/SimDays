"""
Normalize UI icons to a 512x512 transparent canvas with consistent occupancy.
Handles both transparent-background and white-background source images.

- icon_*  (location icons):  target 84% occupancy
- act_*   (action icons):    target 88% occupancy
- app_*   (phone app icons): target 88% occupancy

Reads from:  game/images/ui/icons/
Writes to:   game/images/ui/icons/  (in-place, overwrites source)
Also writes: game/images/ui/generated/normalize_report.csv
"""

import csv
from pathlib import Path
from PIL import Image

ICONS_DIR  = Path(__file__).parent.parent / "SimDays" / "SimDays" / "game" / "images" / "ui" / "icons"
REPORT_DIR = Path(__file__).parent.parent / "SimDays" / "SimDays" / "game" / "images" / "ui" / "generated"
CANVAS     = 512
REPORT_CSV = REPORT_DIR / "normalize_report.csv"

OCCUPANCY = {
    "icon_":  0.84,
    "act_":   0.88,
    "app_":   0.88,
}

# Near-white threshold: pixels with R,G,B all above this AND high alpha are background
WHITE_THRESH = 240


def strip_white_background(img: Image.Image) -> Image.Image:
    """Replace near-white opaque pixels with transparent, leaving artwork intact."""
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 200 and r >= WHITE_THRESH and g >= WHITE_THRESH and b >= WHITE_THRESH:
                pixels[x, y] = (255, 255, 255, 0)
    return img


def has_white_background(img: Image.Image) -> bool:
    """Quick check: does this image have significant near-white opaque pixels?"""
    img = img.convert("RGBA")
    sample = list(img.getdata())
    white_count = sum(
        1 for r, g, b, a in sample
        if a > 200 and r >= WHITE_THRESH and g >= WHITE_THRESH and b >= WHITE_THRESH
    )
    return white_count > (len(sample) * 0.01)  # > 1% near-white opaque pixels


def content_bbox(img: Image.Image):
    """Bounding box of non-transparent pixels after white stripping."""
    return img.split()[3].getbbox()


def normalize(src: Path, occupancy: float, canvas: int = CANVAS):
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    had_white = has_white_background(img)
    if had_white:
        img = strip_white_background(img)
    bbox = content_bbox(img)
    if not bbox:
        return Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0)), {
            "file": src.name, "orig_w": w, "orig_h": h,
            "content_w": 0, "content_h": 0, "had_white": had_white,
            "occupancy_px": 0.0, "target_occupancy": occupancy, "status": "blank"
        }
    x0, y0, x1, y1 = bbox
    cw, ch = x1 - x0, y1 - y0
    scale = (occupancy * canvas) / max(cw, ch)
    nw, nh = round(cw * scale), round(ch * scale)
    cropped = img.crop(bbox)
    resized = cropped.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    ox = (canvas - nw) // 2
    oy = (canvas - nh) // 2
    out.paste(resized, (ox, oy), resized)
    actual_occ = max(nw, nh) / canvas
    return out, {
        "file": src.name, "orig_w": w, "orig_h": h,
        "content_w": cw, "content_h": ch, "had_white": had_white,
        "occupancy_px": round(actual_occ, 4), "target_occupancy": occupancy, "status": "ok"
    }


def prefix_occupancy(name: str):
    for prefix, occ in OCCUPANCY.items():
        if name.startswith(prefix):
            return occ
    return None


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(ICONS_DIR.glob("*.png"))
    rows = []
    processed = skipped = white_stripped = 0
    for src in sources:
        occ = prefix_occupancy(src.name)
        if occ is None:
            skipped += 1
            continue
        out_img, row = normalize(src, occ)
        out_img.save(str(src), "PNG")
        rows.append(row)
        processed += 1
        if row["had_white"]:
            white_stripped += 1
        flag = " [white stripped]" if row["had_white"] else ""
        print(f"  {src.name}: {row['content_w']}x{row['content_h']} → {int(row['occupancy_px']*100)}% occ{flag}")

    with open(REPORT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file","orig_w","orig_h","content_w","content_h","had_white","occupancy_px","target_occupancy","status"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. {processed} normalized ({white_stripped} white-stripped), {skipped} skipped.")
    print(f"Report: {REPORT_CSV}")


if __name__ == "__main__":
    main()
