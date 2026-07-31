# City map - road-aligned district zones with always-on icon markers.
# Idle: district icon at the zone centre. Hover: blue parallelogram + name.
# Click area = the zone's mask PNG.

# key, jump target, icon file (in images/ui/icons/), centre x, centre y, display name
define MAP_ZONES = [
    ("bogate_domki", "zone_locked_uptown", "house_uptown",   220, 148, "Uptown"),
    ("warehouse",    "location_warehouse", "garage",        1665, 147, "Warehouse District"),
    ("park",         "location_park",      "park",           930, 254, "City Park"),
    ("domki",        "zone_locked_suburbs","house_suburb",   426, 384, "Suburbs"),
    ("bloki",        "location_hallway",   "apartment_ext",  739, 397, "Apartments"),
    ("centrum",      "location_centrum",   "office_ext",    1196, 387, "City Centre"),
    ("szpital",      "location_hospital",  "szpital",        289, 599, "Hospital"),
    ("mall",         "location_mall",      "mall",           964, 552, "Mall"),
    ("plaza",        "location_beach",     "beach",         1061, 929, "Beach"),
    ("nadbrzeze",    "location_nadbrzeze", "nadbrzeze",     1139, 707, "Quayside"),
]

screen city_map():
    tag menu

    # district zones: idle shows a dim icon, hover brightens it + highlights the parcel
    for key, lbl, icon, cx, cy, zname in MAP_ZONES:
        # ponytail: z_nadbrzeze_idle/_hi were baked far more saturated/opaque than
        # sibling zones (idle a≈243 vs ≈140; hi is vivid cyan vs pale blue), so we
        # scale their alpha in-code. Its _hi is ALSO missing the district icon that
        # sibling _hi images bake in, so on hover the icon vanished — composite the
        # idle icon back over the highlight.
        if key == "nadbrzeze":
            $ _z_idle = Transform("images/ui/z_nadbrzeze_idle.png", alpha=0.55)
            $ _z_hi   = Composite((1920, 1080), (0, 0), Transform("images/ui/z_nadbrzeze_hi.png", alpha=0.5), (0, 0), "images/ui/z_nadbrzeze_idle.png")
        else:
            $ _z_idle = "z_%s_idle" % key
            $ _z_hi   = "z_%s_hi" % key
        imagebutton:
            idle  _z_idle
            hover _z_hi
            focus_mask Image("images/ui/z_%s_mask.png" % key)
            action Jump(lbl)
        # zone name label — always visible, centred on the zone
        text zname:
            xpos cx ypos (cy + 52) xanchor 0.5 yanchor 0.0
            size 15 font "fonts/Quicksand-SemiBold.ttf" color "#ffffff"
            outlines [(2, "#000000aa", 0, 0)]



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
    ("hub",         "The Hub",     "location_hub"),
    ("office_exec", "Nexus Tower", "location_office"),
    ("university",  "College",     "location_college"),
    ("gym",         "Gym",         "location_gym"),
    ("library",     "Library",     "location_library"),
    ("bar",         "Bar",         "location_bar"),
    ("nightclub",   "Club",        "location_nightclub"),
    ("garage",      "Car Dealer",  "location_cardealer"),
    ("restaurant_eleven", "Eleven", "location_kitchen"),
]

# Mall shops (own backgrounds + icons). Shown as an icon bar inside the mall.
define MALL_SHOPS = [
    ("shop_clothing",    "Clothing",    "location_shop_clothing"),
    ("shop_electronics", "Electronics", "location_shop_electronics"),
    ("shop_lifestyle",   "Gifts",       "location_shop_gifts"),
]

init python:
    # Opening hours per venue (open, close). Game clock is 7.0-27.0, so a close
    # value > 24 means "into the small hours" (e.g. bar 17-27 = 5pm-3am).
    # Venues with no night art close before evening (e.g. College).
    VENUE_HOURS = {
        "coffee_shop": (7, 19),
        "hub":         (8, 22),
        "office_exec": (8, 20),
        "university":  (8, 18),   # day art only
        "gym":         (6, 23),
        "library":     (8, 22),
        "bar":         (17, 27),  # evening into the night
        "nightclub":   (21, 27),
        "garage":      (9, 19),
        "restaurant_eleven": (16, 27),   # kitchen runs evenings
        "flea_market": (9, 18),           # Sat-Sun only
        "terrace":     (12, 22),
        "casino":      (20, 28),  # 8pm-4am
        "lombard":     (10, 20),
        "diner":       (20, 28),  # 8pm-4am
    }

    _WEEKDAY_ONLY = {"office_exec", "university"}  # closed Sat-Sun (day%7 >= 5)
    _WEEKEND_ONLY = {"flea_market"}                # closed Mon-Fri (day%7 < 5)

    def venue_open(key):
        wd = store.day % 7   # 0=Mon…4=Fri, 5=Sat, 6=Sun
        if key in _WEEKDAY_ONLY and wd >= 5:
            return False
        if key in _WEEKEND_ONLY and wd < 5:
            return False
        o, c = VENUE_HOURS.get(key, (0, 27))
        return o <= store.hour < c

    def venue_hours_str(key):
        o, c = VENUE_HOURS.get(key, (0, 27))
        return "%02d:00-%02d:00" % (o % 24, c % 24)

screen hallway_hub():
    use hud
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        hbox:
            spacing 40
            # Your Place
            vbox:
                xsize 150
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_door_12.png", size=(120, 120))
                    hover Transform("images/ui/icons/icon_door_12.png", size=(132, 132))
                    action Jump("location_home")
                text "Your Place" xalign 0.5 size 16 color "#ffffff"
            # Marcus's door
            if marcus_met and (not move_in_complete or npc_here("marcus")):
                vbox:
                    xsize 150
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        idle  Transform("images/ui/icons/icon_door_14.png", size=(120, 120))
                        hover Transform("images/ui/icons/icon_door_14.png", size=(132, 132))
                        action Jump("marcus_talk")
                    text "Marcus (14)" xalign 0.5 size 16 color "#ffffff"
            # City Map — locked until player enters their apartment
            $ _city_locked = not move_in_complete
            vbox:
                xsize 150
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_hub.png", size=(120, 120), alpha=(0.5 if _city_locked else 1.0))
                    hover Transform("images/ui/icons/icon_hub.png", size=(132, 132))
                    action Jump("onboarding_city_locked" if _city_locked else "map")
                text ("Go to the City" if _city_locked else "City Map") xalign 0.5 size 16 color ("#888888" if _city_locked else "#ffffff")
                if _city_locked:
                    text "[[Get your things inside first]]" xalign 0.5 size 13 color "#887755"

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
                $ _open = venue_open(icon)
                vbox:
                    xsize 132
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        sensitive _open
                        idle  Transform("images/ui/icons/icon_%s.png" % icon, size=(108, 108), alpha=(1.0 if _open else 0.32))
                        hover Transform("images/ui/icons/icon_%s.png" % icon, size=(120, 120))
                        action Jump(target)
                    if _open:
                        text label xalign 0.5 size 16 color "#ffffff"
                    else:
                        text label xalign 0.5 size 15 color "#7a8aa0"
                        text venue_hours_str(icon) xalign 0.5 size 12 color "#7a8aa0"
            # Phase 50: gallery button — visible while Zoe's plan is active or during post-opening period
            $ _gal_open = (
                (store.npc_invitation_pending is not None
                 and store.npc_invitation_pending.get("invitation_id") == "zoe_exhibition"
                 and store.day <= store.npc_invitation_pending.get("expiry_day", -999))
                or (store.zoe_exhibition_done and store.day <= store.zoe_gallery_until_day)
            )
            if _gal_open:
                vbox:
                    xsize 132
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        idle  Transform("images/ui/icons/icon_hub.png", size=(108, 108))
                        hover Transform("images/ui/icons/icon_hub.png", size=(120, 120))
                        action Jump("location_gallery")
                    text "Gallery" xalign 0.5 size 16 color "#b0d0ff"
            vbox:
                xsize 132
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_hub.png", size=(108, 108))
                    hover Transform("images/ui/icons/icon_hub.png", size=(120, 120))
                    action Jump("map")
                text "City Map" xalign 0.5 size 16 color "#ffffff"

define NADBRZEZE_VENUES = [
    # (venue_key for venue_open/hours, icon filename, label, jump target)
    ("bar",     "anchor",     "The Anchor",     "location_anchor"),
    ("terrace", "terrace",    "Terrace",         "location_terrace"),
    ("casino",  "casino",     "Casino",          "location_casino"),
    ("lombard", "lombard",    "Lombard",         "location_lombard"),
    ("diner",   "restaurant", "Late-Night Diner", "location_diner"),
]

screen nadbrzeze_hub():
    use hud
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        hbox:
            spacing 26
            for vkey, icon, label, target in NADBRZEZE_VENUES:
                $ _open = venue_open(vkey)
                vbox:
                    xsize 132
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        sensitive _open
                        idle  Transform("images/ui/icons/icon_%s.png" % icon, size=(108, 108), alpha=(1.0 if _open else 0.32))
                        hover Transform("images/ui/icons/icon_%s.png" % icon, size=(120, 120))
                        action Jump(target)
                    if _open:
                        text label xalign 0.5 size 16 color "#ffffff"
                    else:
                        text label xalign 0.5 size 15 color "#7a8aa0"
                        text venue_hours_str(vkey) xalign 0.5 size 12 color "#7a8aa0"
            if (day % 7) >= 5:
                $ _fmopen = (9 <= hour < 18)
                vbox:
                    xsize 132
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        sensitive _fmopen
                        idle  Transform("images/ui/icons/icon_mall.png", size=(108, 108), alpha=(1.0 if _fmopen else 0.32))
                        hover Transform("images/ui/icons/icon_mall.png", size=(120, 120))
                        action Jump("location_flea_market")
                    if _fmopen:
                        text "Flea Market" xalign 0.5 size 16 color "#ffffff"
                    else:
                        text "Flea Market" xalign 0.5 size 15 color "#7a8aa0"
                        text "09:00-18:00" xalign 0.5 size 12 color "#7a8aa0"
            vbox:
                xsize 132
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_hub.png", size=(108, 108))
                    hover Transform("images/ui/icons/icon_hub.png", size=(120, 120))
                    action Jump("map")
                text "City Map" xalign 0.5 size 16 color "#ffffff"


screen beach_hub():
    use hud
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        hbox:
            spacing 40
            vbox:
                xsize 150
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_sandbeach.png", size=(120, 120))
                    hover Transform("images/ui/icons/icon_sandbeach.png", size=(132, 132))
                    action Jump("location_sandbeach")
                text "Sandbeach" xalign 0.5 size 16 color "#ffffff"
            vbox:
                xsize 150
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_hub.png", size=(120, 120))
                    hover Transform("images/ui/icons/icon_hub.png", size=(132, 132))
                    action Jump("map")
                text "City Map" xalign 0.5 size 16 color "#ffffff"

# Inside the mall: pick a shop (each has its own interior).
screen mall_hub():
    use hud

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        hbox:
            spacing 40
            for icon, label, target in MALL_SHOPS:
                vbox:
                    xsize 150
                    spacing 4
                    imagebutton:
                        xalign 0.5
                        idle  Transform("images/ui/icons/icon_%s.png" % icon, size=(112, 112))
                        hover Transform("images/ui/icons/icon_%s.png" % icon, size=(124, 124))
                        action Jump(target)
                    text label xalign 0.5 size 16 color "#ffffff"
            vbox:
                xsize 150
                spacing 4
                imagebutton:
                    xalign 0.5
                    idle  Transform("images/ui/icons/icon_hub.png", size=(112, 112))
                    hover Transform("images/ui/icons/icon_hub.png", size=(124, 124))
                    action Jump("map")
                text "City Map" xalign 0.5 size 16 color "#ffffff"
