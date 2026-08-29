"""Unify hand-marked zones: BLUE outlines from map_marked.png + GREEN fills from
parcels_drawn.png. Scale both to 1920x1080 game space, fit the isometric road
angle, snap each to a road-aligned parallelogram, drop blue zones that a green
zone overrides, render in blue (edge + translucent fill), number for labelling."""
import numpy as np, json, math
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

BLUE_SRC  = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_marked.png"
GREEN_SRC = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\parcels_drawn.png"
MAP       = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\locations\map_city.png"
OUT_IMG   = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\images\parcels_final.png"
OUT_JSON  = r"C:\Users\oskar.bazydlo\Documents\LivingTheDream\tools\zones.json"
GW, GH = 1920, 1080

def blobs_from(path, kind):
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    sx, sy = GW / sw, GH / sh
    a = np.asarray(im).astype(np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    if kind == "blue":
        m = (B > 150) & ((B - R) > 60) & ((B - G) > 25)
    else:
        m = (G > 150) & ((G - R) > 90) & ((G - B) > 90)
    lbl, n = ndimage.label(m, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if len(xs) < (250 if kind == "blue" else 2000):
            continue
        bw = xs.max() - xs.min() + 1; bh = ys.max() - ys.min() + 1
        if kind == "blue" and len(xs) / (bw * bh) > 0.15:   # drop filled water
            continue
        P = np.column_stack([xs * sx, ys * sy]).astype(float)
        out.append((P, kind))
    return out

allb = blobs_from(GREEN_SRC, "green") + blobs_from(BLUE_SRC, "blue")

def corners(P, alpha, plo=2, phi=98):
    a1 = np.array([math.cos(alpha), math.sin(alpha)])
    a2 = np.array([math.cos(alpha), -math.sin(alpha)])
    M = np.array([a1, a2]); S = P @ M.T
    su0, sv0 = np.percentile(S, plo, axis=0); su1, sv1 = np.percentile(S, phi, axis=0)
    Minv = np.linalg.inv(M)
    return np.array([Minv @ c for c in [(su0, sv0), (su1, sv0), (su1, sv1), (su0, sv1)]])

def area(poly):
    x, y = poly[:, 0], poly[:, 1]
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2

# global iso angle = min total fitted area
best_alpha = min((math.radians(d) for d in np.arange(8, 82, 1.0)),
                 key=lambda al: sum(area(corners(P, al)) for P, _ in allb))
print("iso angle deg:", round(math.degrees(best_alpha), 1))

zones = []
for P, kind in allb:
    poly = corners(P, best_alpha)
    zones.append({"kind": kind, "centroid": [float(P[:, 0].mean()), float(P[:, 1].mean())],
                  "poly": [[int(round(x)), int(round(y))] for x, y in poly]})

# green overrides blue: drop blue zone whose centroid is near any green centroid
greens = [z for z in zones if z["kind"] == "green"]
final = list(greens)
for z in zones:
    if z["kind"] == "blue":
        c = np.array(z["centroid"])
        if all(np.hypot(*(c - np.array(g["centroid"]))) > 200 for g in greens):
            final.append(z)
final.sort(key=lambda z: (z["centroid"][1] // 150, z["centroid"][0]))
print("final zones:", len(final))

base = Image.open(MAP).convert("RGBA").resize((GW, GH))
ov = Image.new("RGBA", (GW, GH), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
try: font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
except Exception: font = ImageFont.load_default()
BLUE = (90, 170, 255)
for idx, z in enumerate(final, 1):
    d.polygon([tuple(p) for p in z["poly"]], fill=BLUE + (90,), outline=BLUE + (255,), width=5)
    cx, cy = int(z["centroid"][0]), int(z["centroid"][1])
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(0, 0, 0, 225))
    tb = d.textbbox((0, 0), str(idx), font=font)
    d.text((cx - (tb[2]-tb[0])/2, cy - (tb[3]-tb[1])/2 - tb[1]), str(idx), font=font, fill=(255, 255, 255, 255))
    print(f"  #{idx} ({z['kind']}) centroid=({cx},{cy})")

Image.alpha_composite(base, ov).convert("RGB").save(OUT_IMG)
json.dump(final, open(OUT_JSON, "w"), indent=1)
print("saved", OUT_IMG)
