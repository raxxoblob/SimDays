# Image declarations
# Ren'Py looks for images relative to the game/ folder.
# game/images is a directory junction -> ../../images (the shared asset folder).

# ── Backgrounds ───────────────────────────────────────────────────────
# All location backgrounds are 16:9 (1672x941 or 1920x1080). We wrap each in
# a Transform that forces 1920x1080 (the game resolution) so they fill the
# screen with no borders. Same ratio -> no distortion.
init python:
    def _bg(name, filename=None):
        path = "images/locations/%s.png" % (filename or name)
        renpy.image(name, Transform(path, size=(1920, 1080)))

    for _n in [
        "cheaphouse_day", "cheaphouse_night",
        "goodhomeday", "goodhomenight", "richhomeday", "richhomenight",
        "cafeday", "cafenight", "bar", "restaurantday", "restaurantnight",
        "gymdaypeople", "gymdaynopeople",
        "libraryday", "librarynight",
        "mallday", "mallnight", "clothesshop", "electronicsshop", "giftshop",
        "parkday", "parknight", "beachday", "beachnight",
        "goodoffice1", "mediumoffice1", "pooroffice1", "officelobby1",
        "warehouse", "carworkshop", "hospital1", "schoolhall",
    ]:
        _bg(_n)

    _bg("classroom", "class")   # 'class' is a Python keyword — rename the image

    # Map: source is 5068x2764 (28MB). Forced to 1920x1080 like the rest.
    # ponytail: ~3% horizontal squeeze (1.834 vs 1.778); imperceptible.
    # Upgrade path: downscale the PNG to 1920x1080 to cut the VRAM load.
    _bg("map_city")

# ── Sprite positioning transforms ─────────────────────────────────────
# Sprites are tall portraits (~1086x1448 / 1024x1535). 'fit contain' scales
# each into a box preserving aspect; yalign 1.0 anchors feet to the bottom.
transform sprite_c:
    fit "contain"
    xysize (760, 1040)
    xalign 0.5
    yalign 1.0

transform sprite_r:
    fit "contain"
    xysize (760, 1040)
    xalign 0.82
    yalign 1.0

transform sprite_l:
    fit "contain"
    xysize (760, 1040)
    xalign 0.18
    yalign 1.0

# ── Zoe sprites (plain files; positioned via the transforms above) ─────
image zoe_street_neutral   = "images/characters/zoe/zoe_street_neutral.png"
image zoe_street_smile     = "images/characters/zoe/zoe_street_smile.png"
image zoe_street_talk      = "images/characters/zoe/zoe_street_talk.png"
image zoe_street_surprised = "images/characters/zoe/zoe_street_surprised.png"
image zoe_street_full      = "images/characters/zoe/zoe_street_full.png"
image zoe_punk_smile       = "images/characters/zoe/zoe_punk_smile.png"
image zoe_hoodie_smile     = "images/characters/zoe/zoe_hoodie_smile.png"
image zoe_coat_smile       = "images/characters/zoe/zoe_coat_smile.png"
