"""
Round 2: install the newly-added corrected location icons from
images/ui/fixed_icons/{location_icons_9_safe_crop, location_icons_9_safe_top,
location_icons_column_first_9} into images/ui/icons/, mapped to in-game names
and normalized onto a uniform 512x512 transparent canvas.

Mapping decided by inspecting each image (see contact sheet) and cross-checking
the icon keys actually used by MAP_ZONES / CENTRUM_VENUES / MALL_SHOPS /
NADBRZEZE_VENUES. Sources are already clean circles on transparent backgrounds.
"""

from pathlib import Path
from PIL import Image

ROOT   = Path(__file__).parent.parent / "SimDays" / "SimDays" / "game" / "images" / "ui"
FIXED  = ROOT / "fixed_icons"
ICONS  = ROOT / "icons"
CANVAS = 512
OCC    = 0.99

MAP = [
    # ── location_icons_9_safe_crop ──
    ("location_icons_9_safe_crop/apartment_building.png", ["icon_apartment_ext.png", "icon_apartment_block.png"]),
    ("location_icons_9_safe_crop/boardwalk.png",          ["icon_beach.png"]),
    ("location_icons_9_safe_crop/cafe.png",               ["icon_coffee_shop.png"]),
    ("location_icons_9_safe_crop/city_center.png",        ["icon_office_ext.png"]),
    ("location_icons_9_safe_crop/college.png",            ["icon_college.png"]),
    ("location_icons_9_safe_crop/garage.png",             ["icon_garage.png"]),
    ("location_icons_9_safe_crop/mall.png",               ["icon_mall.png"]),
    ("location_icons_9_safe_crop/park.png",               ["icon_park.png"]),
    ("location_icons_9_safe_crop/restaurant.png",         ["icon_restaurant.png"]),

    # ── location_icons_9_safe_top ──
    ("location_icons_9_safe_top/bar.png",               ["icon_bar.png"]),
    ("location_icons_9_safe_top/budget_office.png",     ["icon_office_budget.png"]),
    ("location_icons_9_safe_top/clothing_store.png",    ["icon_shop_clothing.png"]),
    ("location_icons_9_safe_top/corporate_lobby.png",   ["icon_lobby_luxury.png"]),
    ("location_icons_9_safe_top/electronics_store.png", ["icon_shop_electronics.png"]),
    ("location_icons_9_safe_top/executive_office.png",  ["icon_office_exec.png"]),
    ("location_icons_9_safe_top/gift_store.png",        ["icon_shop_lifestyle.png"]),
    ("location_icons_9_safe_top/open_office.png",       ["icon_office_mid.png"]),

    # ── location_icons_column_first_9 ──
    ("location_icons_column_first_9/campus.png",          ["icon_university.png"]),
    ("location_icons_column_first_9/nightclub.png",       ["icon_nightclub.png"]),
    ("location_icons_column_first_9/reception.png",       ["icon_reception.png"]),
    ("location_icons_column_first_9/restaurant.png",      ["icon_restaurant_eleven.png"]),
    # rooftop terrace lounge — much better "Terrace" venue icon than the old office shot
    ("location_icons_column_first_9/rooftop_evening.png", ["icon_terrace.png", "icon_rooftop.png"]),

    # Skipped (no distinct in-game target / redundant with better matches):
    #   column_first_9/apartment_evening, door_night, office_day, office_lobby
    #   safe_top/restaurant  (icon_restaurant + icon_restaurant_eleven already covered)
]


def normalize(src: Path, canvas: int = CANVAS, occ: float = OCC) -> Image.Image:
    img = Image.open(src).convert("RGBA")
    bbox = img.split()[3].getbbox()
    if not bbox:
        return Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    cropped = img.crop(bbox)
    cw, ch = cropped.size
    scale = (occ * canvas) / max(cw, ch)
    nw, nh = round(cw * scale), round(ch * scale)
    resized = cropped.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    out.paste(resized, ((canvas - nw) // 2, (canvas - nh) // 2), resized)
    return out


def main():
    done = missing = 0
    for rel, targets in MAP:
        src = FIXED / rel
        if not src.exists():
            print(f"  MISSING SOURCE: {rel}")
            missing += 1
            continue
        out = normalize(src)
        for t in targets:
            out.save(str(ICONS / t), "PNG")
            print(f"  {rel}  ->  {t}")
            done += 1
    print(f"\nDone. {done} written, {missing} sources missing.")


if __name__ == "__main__":
    main()
