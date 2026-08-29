"""Generate the white 9-slice shapes HUD V2 tints at runtime (im.matrix.tint).

All output is pure white with only the alpha channel carrying the shape, so
hud_v2.rpy can recolour every panel/bar from the HUD2 constants dict.
Run: python tools/gen_hud2_panels.py
"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "ui", "hud2")
SS = 4  # supersample factor for smooth corners


def _rounded(w, h, r, stroke=None):
    img = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(img)
    box = [0, 0, w * SS - 1, h * SS - 1]
    if stroke:
        d.rounded_rectangle(box, radius=r * SS, outline=255, width=int(stroke * SS))
    else:
        d.rounded_rectangle(box, radius=r * SS, fill=255)
    a = img.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    out.putalpha(a)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    shapes = {
        "panel_r18.png":      _rounded(40, 40, 18),
        "panel_r18_line.png": _rounded(40, 40, 18, stroke=1.5),
        "bar5.png":           _rounded(24, 5, 2),
        "bar8.png":           _rounded(24, 8, 4),
    }
    for name, img in shapes.items():
        p = os.path.join(OUT, name)
        img.save(p)
        print("wrote", os.path.normpath(p), img.size)

    # self-check: corners transparent, centre opaque, edges symmetric
    p = shapes["panel_r18.png"]
    assert p.getpixel((0, 0))[3] < 10, "panel corner should be transparent"
    assert p.getpixel((20, 20))[3] == 255, "panel centre should be opaque"
    b = shapes["bar5.png"]
    assert b.getpixel((12, 2))[3] == 255, "bar centre should be opaque"
    assert b.getpixel((0, 0))[3] < 128, "bar cap corner should be soft"
    ln = shapes["panel_r18_line.png"]
    assert ln.getpixel((20, 20))[3] < 10, "outline centre should be hollow"
    assert ln.getpixel((20, 0))[3] > 200, "outline top edge should be drawn"
    print("self-check OK")


if __name__ == "__main__":
    main()
