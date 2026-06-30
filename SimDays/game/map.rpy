# City map — road-aligned district zones with always-on icon markers.
# Idle: district icon at the zone centre. Hover: blue parallelogram + name.
# Click area = the zone's mask PNG.

# key, jump target, icon file (in images/ui/icons/), centre x, centre y
define MAP_ZONES = [
    ("bogate_domki", "location_home",      "apartment_ext",  220, 148),
    ("warehouse",    "location_warehouse", "garage",        1665, 147),
    ("park",         "location_park",      "park",           930, 254),
    ("domki",        "location_home",      "apartment_ext",  426, 384),
    ("bloki",        "location_home",      "apartment_ext",  739, 397),
    ("centrum",      "location_centrum",   "office_ext",    1196, 387),
    ("szpital",      "location_hospital",  "szpital",        289, 599),
    ("mall",         "location_mall",      "mall",           964, 552),
    ("plaza",        "location_beach",     "beach",         1061, 929),
]

screen city_map():
    tag menu

    # district zones: idle shows a dim icon, hover brightens it + highlights the parcel
    for key, lbl, icon, cx, cy in MAP_ZONES:
        imagebutton:
            idle ("z_%s_idle" % key)
            hover ("z_%s_hi" % key)
            focus_mask Image("images/ui/z_%s_mask.png" % key)
            action Jump(lbl)

    textbutton "Sleep / End Day":
        action Jump("action_sleep")
        style "pin_sleep"
        xpos 30
        ypos 1008


style pin_sleep is button:
    background "#000000c0"
    hover_background "#222222e0"
    padding (12, 6, 12, 6)

style pin_sleep_text is button_text:
    size 16
    idle_color "#88aaff"
    hover_color "#aaccff"


# ── Centrum hub: bottom bar of venue icons ────────────────────────────
# icon file (images/ui/icons/), label, jump target
define CENTRUM_VENUES = [
    ("coffee_shop", "Coffee Shop", "location_cafe"),
    ("office_exec", "Nexus Tower", "location_office"),
    ("gym",         "Gym",         "location_gym"),
    ("college",     "Library",     "location_library"),
    ("bar",         "Bar",         "location_bar"),
]

screen centrum_hub():
    use hud

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        hbox:
            spacing 26
            for icon, label, target in CENTRUM_VENUES:
                vbox:
                    xsize 132
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        idle  Transform("images/ui/icons/icon_%s.png" % icon, size=(108, 108))
                        hover Transform("images/ui/icons/icon_%s.png" % icon, size=(120, 120))
                        action Jump(target)
                    text label xalign 0.5 size 16 color "#ffffff"

    textbutton "Back to City Map":
        action Jump("map")
        style "pin_sleep"
        xpos 30
        ypos 1008
