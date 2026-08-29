"""
Extract icons from newest_sandbay_icons.png (1536x1024, 3x2 grid of 512x512 cells).
Strips the gray background, normalizes each to 512x512 transparent canvas at 84% occupancy,
and saves to images/ui/icons/ overwriting existing files.

Grid layout (visually identified):
  Row 0: lombard  | casino   | nadbrzeze
  Row 1: anchor   | terrace  | sandbeach
"""

from pathlib import Path
from PIL import Image
import numpy as np

ROOT     = Path(__file__).parent.parent / "SimDays" / "SimDays" / "game"
SRC      = ROOT / "images" / "ui" / "newest_sandbay_icons.png"
ICONS    = ROOT / "images" / "ui" / "icons"
CANVAS   = 512
OCCUPANCY = 0.84

GRID = [
    # (col, row, output_filename)
    (0, 0, "icon_lombard.png"),
    (1, 0, "icon_casino.png"),
    (2, 0, "icon_nadbrzeze.png"),
    (0, 1, "icon_anchor.png"),
    (1, 1, "icon_terrace.png"),
    (2, 1, "icon_sandbeach.png"),
]


def apply_circle_mask(img: Image.Image) -> Image.Image:
    """Apply a soft circular mask: finds the largest circle that fits, with
    feathered edges to avoid hard jaggies."""
    img = img.convert("RGBA")
    w, h = img.size
    # The icon circle is centered and nearly fills the cell;
    # detect actual content radius by flood-filling from corners to find bg extent.
    arr = np.array(img, dtype=np.float32)
    corners = [arr[:20, :20], arr[:20, -20:], arr[-20:, :20], arr[-20:, -20:]]
    bg_pixels = np.concatenate([c.reshape(-1, 4) for c in corners], axis=0)
    bg_color = bg_pixels[:, :3].mean(axis=0)

    # Build distance-from-center alpha mask for a circle
    cx, cy = w / 2, h / 2
    # Measure radius: find the average radius where bg starts (search from center outward)
    # Simpler: use 90% of min(w,h)/2 as the circle radius to safely exclude bg
    r = min(w, h) / 2 * 0.97  # 97% — tight but leaves the border ring intact
    feather = 4.0

    ys, xs = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    alpha_mask = np.clip((r - dist) / feather, 0.0, 1.0)

    result = arr.copy()
    result[:, :, 3] = result[:, :, 3] * alpha_mask
    return Image.fromarray(result.astype(np.uint8), "RGBA")


def normalize(img: Image.Image, occupancy: float = OCCUPANCY, canvas: int = CANVAS) -> Image.Image:
    bbox = img.split()[3].getbbox()
    if not bbox:
        return Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
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
    return out


def main():
    sheet = Image.open(SRC).convert("RGBA")
    sw, sh = sheet.size
    cell_w = sw // 3  # 512
    cell_h = sh // 2  # 512
    print(f"Sheet: {sw}x{sh}, cell: {cell_w}x{cell_h}")

    for col, row, fname in GRID:
        x0 = col * cell_w
        y0 = row * cell_h
        cell = sheet.crop((x0, y0, x0 + cell_w, y0 + cell_h))

        stripped = apply_circle_mask(cell)
        normalized = normalize(stripped)

        out_path = ICONS / fname
        normalized.save(str(out_path), "PNG")
        bbox = stripped.split()[3].getbbox()
        cw = (bbox[2] - bbox[0]) if bbox else 0
        ch = (bbox[3] - bbox[1]) if bbox else 0
        print(f"  {fname}: cell ({col},{row}), content {cw}x{ch} → {out_path.name}")

    print("\nDone.")


if __name__ == "__main__":
    main()
