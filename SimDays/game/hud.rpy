# Always-on HUD: single decorative top bar (hud_topbar.png), centred near top.
# Holds date/time, money, and the three need bars. Top-left screen corner left free.

screen hud():
    zorder 10
    $ datestr = "%s . Day %d" % (day_name(day), day + 1)
    $ timestr = time_label(hour)

    key "K_c" action ToggleScreen("profile")
    button:
        xpos 1792 ypos 22
        xysize (104, 52)
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action ToggleScreen("profile")
        text "Me" font "fonts/Quicksand-SemiBold.ttf" size 24 color "#cfe0f5" align (0.5, 0.5)

    # phone peek — hidden when phone is fully open to avoid overlap
    key "K_p" action Show("phone_home")
    if renpy.get_screen("phone_home") is None:
        imagebutton:
            xpos 1460 ypos 986
            idle  Transform("images/ui/phone.png", crop=(0, 0, 1024, 215), size=(460, 94))
            hover Transform("images/ui/phone.png", crop=(0, 0, 1024, 215), size=(470, 97))
            action Show("phone_home")

    fixed:
        xalign 0.5
        ypos 8
        xysize (1641, 129)
        add "images/ui/hud_topbar.png"

        add "images/ui/icons/stat_time.png" xpos 100 ypos 34 xysize (58, 58)
        text "[datestr]" xpos 168 ypos 28 size 19 color "#143c6e" font "fonts/VarelaRound.ttf"
        text "[timestr]" xpos 168 ypos 54 size 30 color "#0a285a" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_money.png" xpos 380 ypos 34 xysize (58, 58)
        text "$[money]" xpos 448 ypos 48 size 30 color "#8a5a00" font "fonts/VarelaRound.ttf"

        # ── Needs: icon + label + bar + value ─────────────────────────────
        add "images/ui/icons/stat_hunger.png" xpos 680 ypos 44 xysize (50, 50)
        text "HUNGER" xpos 740 ypos 38 size 13 color "#3a6090" font "fonts/VarelaRound.ttf"
        bar value StaticValue(need_hunger, 100) xpos 740 ypos 62 xysize (150, 22) left_bar Frame("images/ui/bar_fill_chr.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_hunger]" xpos 900 ypos 60 size 22 color "#143c6e" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_hygiene.png" xpos 1000 ypos 44 xysize (50, 50)
        text "HYGIENE" xpos 1060 ypos 38 size 13 color "#3a6090" font "fonts/VarelaRound.ttf"
        bar value StaticValue(need_hygiene, 100) xpos 1060 ypos 62 xysize (150, 22) left_bar Frame("images/ui/bar_fill_hygiene.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_hygiene]" xpos 1220 ypos 60 size 22 color "#143c6e" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_energy.png" xpos 1320 ypos 44 xysize (50, 50)
        text "ENERGY" xpos 1380 ypos 38 size 13 color "#3a6090" font "fonts/VarelaRound.ttf"
        bar value StaticValue(need_energy, 100) xpos 1380 ypos 62 xysize (150, 22) left_bar Frame("images/ui/bar_fill_energy.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_energy]" xpos 1540 ypos 60 size 22 color "#143c6e" font "fonts/VarelaRound.ttf"

        button:
            xpos 676 ypos 28 xysize (264, 72)
            action NullAction()
            tooltip "Hunger - eat at home or order from your phone."
        button:
            xpos 996 ypos 28 xysize (264, 72)
            action NullAction()
            tooltip "Hygiene - shower at home. Low: Appearance drops."
        button:
            xpos 1316 ypos 28 xysize (270, 72)
            action NullAction()
            tooltip "Energy - sleep to refill. Below 20 you can't do demanding activities."

    $ _tt = GetTooltip()
    if _tt:
        text "[_tt]":
            xalign 0.5 ypos 146 size 17 color "#ffffff"
            font "fonts/Quicksand-SemiBold.ttf"
            outlines [(2, "#000000cc", 0, 0)]

