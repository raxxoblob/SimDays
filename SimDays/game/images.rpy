# Image declarations
# Ren'Py looks for images relative to the game/ folder.
# game/images is a directory junction -> ../../images (the shared asset folder).

# ── Backgrounds ───────────────────────────────────────────────────────
# All location backgrounds are 16:9 (1672x941 or 1920x1080). We wrap each in
# a Transform that forces 1920x1080 (the game resolution) so they fill the
# screen with no borders. Same ratio -> no distortion.
init python:
    def _bg(name, filename=None):
        path = "images/locations/%s.webp" % (filename or name)
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
        "centerstreet_day", "centerstreet_night",
    ]:
        _bg(_n)

    _bg("classroom", "class")   # 'class' is a Python keyword — rename the image
    # apartment stairwell (doors 12 = you, 14 = Marcus) + Marcus's place — all PNGs.
    renpy.image("hallway",           Transform("images/locations/hallway.png",           size=(1920, 1080)))
    renpy.image("marcus_home_day",   Transform("images/locations/marcus_home_day.png",   size=(1920, 1080)))
    renpy.image("marcus_home_night", Transform("images/locations/marcus_home_night.png", size=(1920, 1080)))

    # Intro cinematic frames (pre-rendered POV, full-screen). 1672x941 -> 1920x1080.
    for _i, _f in enumerate(["intro_scene_1", "intro_scene2", "intro_scene3",
                             "intro_scene4", "intro_scene5", "intro_scene6", "intro_scene7"], 1):
        renpy.image("intro%d" % _i, Transform("images/scenes/intro_scene/%s.png" % _f, size=(1920, 1080)))

    # Map: source is 5068x2764 (28MB). Forced to 1920x1080 like the rest.
    # ponytail: ~3% horizontal squeeze (1.834 vs 1.778); imperceptible.
    # Upgrade path: downscale the PNG to 1920x1080 to cut the VRAM load.
    _bg("map_city")

    # Map district zones: idle = dim icon, hover = bright icon + highlight + name
    for _z in ["bogate_domki", "warehouse", "park", "domki", "bloki", "centrum", "szpital", "mall", "plaza"]:
        renpy.image("z_%s_idle" % _z, "images/ui/z_%s_idle.png" % _z)
        renpy.image("z_%s_hi" % _z, "images/ui/z_%s_hi.png" % _z)

# ── Sprite positioning transforms ─────────────────────────────────────
# Sprites are tall portraits (~1086x1448 / 1024x1535). 'fit contain' scales
# each into a box preserving aspect; yalign 1.0 anchors feet to the bottom.
# yoffset 96 pushes the head clear of the topbar HUD (crops a little at the
# shoes, which is fine for standing full-body sprites).
transform sprite_c:
    fit "contain"
    xysize (760, 1040)
    xalign 0.5
    yalign 1.0
    yoffset 96

transform sprite_r:
    fit "contain"
    xysize (760, 1040)
    xalign 0.82
    yalign 1.0
    yoffset 96

transform sprite_l:
    fit "contain"
    xysize (760, 1040)
    xalign 0.18
    yalign 1.0
    yoffset 96

# ── Zoe sprites (plain files; positioned via the transforms above) ─────
image zoe_street_neutral   = "images/characters/zoe/zoe_street_neutral.webp"
image zoe_street_smile     = "images/characters/zoe/zoe_street_smile.webp"
image zoe_street_talk      = "images/characters/zoe/zoe_street_talk.webp"
image zoe_street_surprised = "images/characters/zoe/zoe_street_surprised.webp"
image zoe_street_full      = "images/characters/zoe/zoe_street_full.webp"
image zoe_punk_smile       = "images/characters/zoe/zoe_punk_smile.webp"
image zoe_hoodie_smile     = "images/characters/zoe/zoe_hoodie_smile.webp"
image zoe_coat_smile       = "images/characters/zoe/zoe_coat_smile.webp"

# ── Marcus sprites (transparent PNGs; outfit_expression) ───────────────
image marcus_casual_normal = "images/characters/marcus/marcus_casual_normal.png"
image marcus_casual_talk   = "images/characters/marcus/marcus_casual_talk.png"
image marcus_casual_laugh  = "images/characters/marcus/marcus_casual_laugh.png"
image marcus_bar_normal    = "images/characters/marcus/marcus_bar_normal.png"
image marcus_bar_talk      = "images/characters/marcus/marus_bar_talk.png"
image marcus_bar_laugh     = "images/characters/marcus/marcus_bar_laugh.png"
image marcus_sport_normal  = "images/characters/marcus/marcus_sport_normal.png"
image marcus_sport_laugh   = "images/characters/marcus/marcus_sport_laugh.png"
image marcus_sport_tired   = "images/characters/marcus/marcus_sport_tired.png"
image marcus_sport_worried = "images/characters/marcus/marcus_sport_worried.png"

# ── Martha sprites (transparent PNGs) ──────────────────────────────────
image martha_neutral = "images/characters/martha/martha_neutral.png"
image martha_talk    = "images/characters/martha/martha_talk.png"
image martha_smile   = "images/characters/martha/martha_smile.png"
image martha_cold    = "images/characters/martha/martha_cold.png"
image martha_worried = "images/characters/martha/martha_worried.png"
