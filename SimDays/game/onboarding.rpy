# onboarding.rpy — Tutorial overlay screen and compat stubs.
# v2 onboarding runs inline in script.rpy:start. Legacy labels kept for save compat.

# ── Styles ──────────────────────────────────────────────────────────────────

style tutorial_btn is default:
    background "#2a4060"
    hover_background "#3a6090"
    insensitive_background "#1a2840"
    padding (18, 10, 18, 10)

style tutorial_btn_text is default:
    color "#cfe0f5"
    hover_color "#ffffff"
    insensitive_color "#4a6080"
    size 17
    font "fonts/Quicksand-SemiBold.ttf"

style tutorial_heading_text is default:
    color "#ffdd44"
    size 22
    bold True
    font "fonts/Quicksand-SemiBold.ttf"

style tutorial_body_text is default:
    color "#cfe0f5"
    size 17
    font "fonts/Quicksand-SemiBold.ttf"

# ── Tutorial overlay screen ──────────────────────────────────────────────────
# area: (x, y, w, h) of the HUD region to highlight, or None for no highlight.
# Returns False on Continue, True on Skip Tutorial.

screen tutorial_overlay(heading, body, area=None):
    modal True
    zorder 100

    fixed:
        xsize 1920
        ysize 1080

        add Solid("#000000b0")

        if area is not None:
            $ _ax, _ay, _aw, _ah = area
            # Yellow border drawn as four thin bars
            add Solid("#ffdd44") xpos (_ax - 3) ypos (_ay - 3) xsize (_aw + 6) ysize 3
            add Solid("#ffdd44") xpos (_ax - 3) ypos (_ay + _ah) xsize (_aw + 6) ysize 3
            add Solid("#ffdd44") xpos (_ax - 3) ypos (_ay - 3) xsize 3 ysize (_ah + 6)
            add Solid("#ffdd44") xpos (_ax + _aw) ypos (_ay - 3) xsize 3 ysize (_ah + 6)

        frame:
            xalign 0.5
            yalign 0.5
            xminimum 640
            xmaximum 880
            background "#12202eee"
            padding (36, 28, 36, 28)
            vbox:
                spacing 20
                text heading style "tutorial_heading_text" xalign 0.5
                text body style "tutorial_body_text" xalign 0.5
                null height 8
                hbox:
                    spacing 20
                    xalign 0.5
                    textbutton "Continue" action Return(False) style "tutorial_btn"
                    textbutton "Skip Tutorial" action Return(True) style "tutorial_btn"


# ── Locked city message ──────────────────────────────────────────────────────

label onboarding_city_locked:
    mc "I should get my things inside first."
    jump location_hallway


# ── Marcus first-day orientation (compat stub) ───────────────────────────────
# v1 onboarding label. v2 onboarding runs inline in script.rpy:start.
# This stub exists solely so old save files that stored a reference to this
# label can resume without an "unknown label" crash. Redirects to hallway.
label marcus_first_day_orientation:
    jump location_hallway
