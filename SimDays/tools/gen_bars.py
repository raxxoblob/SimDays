"""Rounded 'pill' bar assets - light, minimalist, happy style.
A soft light track + a flat bright fill (thin top highlight, no heavy gloss).
Used as Ren'Py Frames (border = radius on left/right so caps survive stretch)."""
from PIL import Image, ImageDraw

UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
W, H, R = 160, 36, 18


def pill(rgb):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=R, fill=rgb + (255,))
    # single soft highlight along the top - keeps it flat & cheerful, not glossy
    d.rounded_rectangle((5, 4, W - 6, H // 2 - 1), radius=R - 5, fill=(255, 255, 255, 70))
    return img


# bright, happy palette
COLORS = {
    "hunger": (255, 176, 58), "hygiene": (47, 210, 166), "energy": (143, 217, 79),
    "thirst": (58, 178, 240),
    "str": (255, 111, 97), "int": (77, 177, 255), "chr": (255, 210, 63),
    "app": (192, 123, 255), "perf": (53, 214, 122),
}
for name, rgb in COLORS.items():
    pill(rgb).save(f"{UI}\\bar_fill_{name}.png")

# light, airy track (reads on both the blue topbar and the dark profile panel)
track = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(track).rounded_rectangle((0, 0, W - 1, H - 1), radius=R, fill=(230, 238, 248, 130))
track.save(f"{UI}\\bar_track.png")
print("bar assets written:", list(COLORS) + ["track"])
