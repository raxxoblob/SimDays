"""Generate clean rounded 'glass' bars for the activity menu (idle + hover).
Replaces the heavy panel + item PNGs with light, self-contained assets sliced
as Ren'Py Frames. ponytail: fixed 400x96 base; Frame borders keep the corners."""
from PIL import Image, ImageDraw

UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
W, H, R = 400, 96, 30   # base size + corner radius; Frame border must exceed R


def bar(fill, edge=None, accent=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=R, fill=fill,
                        outline=edge, width=2 if edge else 0)
    if accent:  # left accent stripe (rounded), sits inside the left Frame border
        d.rounded_rectangle((10, 18, 20, H - 18), radius=5, fill=accent)
    return img


# idle: deep navy glass; hover: brighter blue glass + cyan accent stripe
bar((14, 28, 54, 205), edge=(120, 160, 220, 40)).save(UI + r"\act_bar_idle.png")
bar((28, 92, 180, 230), edge=(150, 200, 255, 90), accent=(120, 200, 255, 255)).save(UI + r"\act_bar_hover.png")
print("activity bars written:", W, "x", H, "R", R)
