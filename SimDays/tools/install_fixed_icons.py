"""
Install the user's hand-corrected icons from images/ui/fixed_icons/ into
images/ui/icons/, mapping each source to its in-game filename and normalizing
onto a uniform 512x512 transparent canvas (content scaled to fill the canvas).

The sources are already cleanly cropped circles on transparent backgrounds; we
only re-center + rescale so every icon renders at a consistent size in-game.
"""

from pathlib import Path
from PIL import Image

ROOT   = Path(__file__).parent.parent / "SimDays" / "SimDays" / "game" / "images" / "ui"
FIXED  = ROOT / "fixed_icons"
ICONS  = ROOT / "icons"
CANVAS = 512
OCC    = 0.99   # these are full-bleed circles; fill the canvas

# (source relative path, [target filenames in icons/])
MAP = [
    # ── split location icons (the venue circles I kept getting wrong) ──
    ("split_location_icons/split_location_icons/01_lombard.png",  ["icon_lombard.png"]),
    ("split_location_icons/split_location_icons/02_casino.png",   ["icon_casino.png"]),
    ("split_location_icons/split_location_icons/03_marina.png",   ["icon_nadbrzeze.png"]),
    ("split_location_icons/split_location_icons/04_anchor.png",   ["icon_anchor.png"]),
    ("split_location_icons/split_location_icons/05_office.png",   ["icon_terrace.png"]),
    ("split_location_icons/split_location_icons/06_sandbeach.png",["icon_sandbeach.png"]),

    # ── location circle icons ──
    ("location_icons_circles_corrected/apartment_12.png",       ["icon_door_12.png"]),
    ("location_icons_circles_corrected/apartment_14.png",       ["icon_door_14.png"]),
    ("location_icons_circles_corrected/apartment_building.png", ["icon_apartment_ext.png", "icon_apartment_block.png"]),
    ("location_icons_circles_corrected/gym.png",                ["icon_gym.png"]),
    ("location_icons_circles_corrected/hospital.png",           ["icon_hospital.png", "icon_szpital.png"]),
    ("location_icons_circles_corrected/large_house.png",        ["icon_house_uptown.png"]),
    ("location_icons_circles_corrected/library.png",            ["icon_library.png"]),
    ("location_icons_circles_corrected/metro.png",              ["icon_metro.png"]),
    ("location_icons_circles_corrected/suburban_house.png",     ["icon_house_suburb.png"]),

    # ── conversation topic icons (topic_<key>) ──
    ("talk_icons_9_separate/art.png",     ["topic_art.png"]),
    ("talk_icons_9_separate/cinema.png",  ["topic_movies.png"]),
    ("talk_icons_9_separate/dining.png",  ["topic_food.png"]),
    ("talk_icons_9_separate/drinks.png",  ["topic_nightlife.png"]),
    ("talk_icons_9_separate/finance.png", ["topic_ambition.png"]),
    ("talk_icons_9_separate/music.png",   ["topic_music.png"]),
    ("talk_icons_9_separate/sports.png",  ["topic_sports.png"]),
    ("talk_icons_9_separate/travel.png",  ["topic_travel.png"]),
    ("talk_icons_9_separate/work.png",    ["topic_work.png"]),

    # ── skill icons (skill_<key>) + appearance stat ──
    ("career_talk_icons_9_separate/healthcare.png",  ["skill_med.png"]),
    ("career_talk_icons_9_separate/programming.png", ["skill_prog.png"]),
    ("career_talk_icons_9_separate/business.png",    ["skill_biz.png"]),
    ("career_talk_icons_9_separate/culinary.png",    ["skill_cook.png"]),
    ("career_talk_icons_9_separate/fitness.png",     ["skill_fit.png"]),
    ("career_talk_icons_9_separate/mechanics.png",   ["skill_mech.png"]),
    ("career_talk_icons_9_separate/art.png",         ["skill_art.png"]),
    ("career_talk_icons_9_separate/appearance.png",  ["stat_app.png"]),

    # ── status / stat icons ──
    ("status_icons_column_first/time.png",      ["stat_time.png"]),
    ("status_icons_column_first/money.png",     ["stat_money.png"]),
    ("status_icons_column_first/hunger.png",    ["stat_hunger.png"]),
    ("status_icons_column_first/hygiene.png",   ["stat_hygiene.png"]),
    ("status_icons_column_first/energy.png",    ["stat_energy.png"]),
    ("status_icons_column_first/social.png",    ["stat_social.png"]),
    ("status_icons_column_first/education.png", ["stat_int.png"]),
    ("status_icons_column_first/fitness.png",   ["stat_str.png"]),
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
