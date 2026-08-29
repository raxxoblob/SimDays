"""Two separate rounded blue HUD panels + a mock on the map.
Panel A (time + money) centred top. Panel B (needs) top-right. All English."""
import os
from PIL import Image, ImageDraw, ImageFont

UI = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\ui"
ICONS = os.path.join(UI, "icons")
MAP = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_city.webp"

def font(sz, bold=True):
    p = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    try: return ImageFont.truetype(p, sz)
    except Exception: return ImageFont.load_default()

def panel(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=(28, 64, 120, 210),
                        outline=(120, 180, 255, 255), width=3)
    d.rounded_rectangle([5, 4, w - 6, h // 2], radius=h // 3, fill=(255, 255, 255, 22))
    return im

def icon(name, size):
    return Image.open(os.path.join(ICONS, f"stat_{name}.png")).convert("RGBA").resize((size, size), Image.LANCZOS)

AW, AH = 470, 84
BW, BH = 486, 84

# Panel A: time + money
pa = panel(AW, AH)
pa.save(os.path.join(UI, "hud_panel_a.png"))
# Panel B: needs
pb = panel(BW, BH)
pb.save(os.path.join(UI, "hud_panel_b.png"))

def mock_a():
    im = pa.copy(); d = ImageDraw.Draw(im)
    im.alpha_composite(icon("time", 50), (12, 17))
    d.text((70, 16), "Mon . Day 1", font=font(17), fill=(200, 222, 255, 255))
    d.text((70, 40), "8:00 AM", font=font(25), fill=(255, 255, 255, 255))
    im.alpha_composite(icon("money", 50), (270, 17))
    d.text((328, 26), "$500", font=font(27), fill=(255, 220, 120, 255))
    return im

def mock_b():
    im = pb.copy(); d = ImageDraw.Draw(im)
    needs = [("hunger", 0.65, (239, 159, 39)), ("hygiene", 0.80, (29, 158, 117)), ("energy", 0.90, (151, 196, 89))]
    x = 14
    for nm, frac, col in needs:
        im.alpha_composite(icon(nm, 40), (x, 22))
        bx, by, bw, bh = x + 46, 35, 92, 14
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=7, fill=(0, 0, 0, 90))
        d.rounded_rectangle([bx, by, bx + max(bh, int(bw * frac)), by + bh], radius=7, fill=col + (255,))
        x += 158
    return im

base = Image.open(MAP).convert("RGBA").resize((1920, 1080))
ma, mb = mock_a(), mock_b()
base.alpha_composite(ma, ((1920 - AW) // 2, 14))
base.alpha_composite(mb, (1920 - BW - 24, 14))
base.convert("RGB").save(r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\hud_mock.png")
print("saved hud_panel_a/b.png + hud_mock.png")
