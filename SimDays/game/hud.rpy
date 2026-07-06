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

    key "K_p" action Call("open_phone")
    button:
        xpos 1792 ypos 980
        xysize (104, 52)
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action Call("open_phone")
        text "Phone" font "fonts/Quicksand-SemiBold.ttf" size 22 color "#cfe0f5" align (0.5, 0.5)

    fixed:
        xalign 0.5
        ypos 8
        xysize (1641, 129)
        add "images/ui/hud_topbar.png"

        add "images/ui/icons/stat_time.png" xpos 22 ypos 36 xysize (56, 56)
        text "[datestr]" xpos 88 ypos 30 size 19 color "#143c6e" font "fonts/VarelaRound.ttf"
        text "[timestr]" xpos 88 ypos 56 size 28 color "#0a285a" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_money.png" xpos 370 ypos 36 xysize (56, 56)
        text "$[money]" xpos 434 ypos 48 size 28 color "#8a5a00" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_hunger.png" xpos 740 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hunger, 100) xpos 792 ypos 56 xysize (84, 16) left_bar Frame("images/ui/bar_fill_chr.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_hunger]" xpos 882 ypos 50 size 20 color "#143c6e" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_hygiene.png" xpos 940 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hygiene, 100) xpos 992 ypos 56 xysize (84, 16) left_bar Frame("images/ui/bar_fill_hygiene.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_hygiene]" xpos 1082 ypos 50 size 20 color "#143c6e" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_energy.png" xpos 1140 ypos 42 xysize (44, 44)
        bar value StaticValue(need_energy, 100) xpos 1192 ypos 56 xysize (84, 16) left_bar Frame("images/ui/bar_fill_energy.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        text "[need_energy]" xpos 1282 ypos 50 size 20 color "#143c6e" font "fonts/VarelaRound.ttf"

        button:
            xpos 736 ypos 38 xysize (176, 52)
            action NullAction()
            tooltip "Hunger - eat at home or order from your phone."
        button:
            xpos 936 ypos 38 xysize (176, 52)
            action NullAction()
            tooltip "Hygiene - shower at home. Low: Appearance drops."
        button:
            xpos 1136 ypos 38 xysize (184, 52)
            action NullAction()
            tooltip "Energy - sleep to refill. Below 20 you can't do demanding activities."

    $ _tt = GetTooltip()
    if _tt:
        text "[_tt]":
            xalign 0.5 ypos 146 size 17 color "#ffffff"
            font "fonts/Quicksand-SemiBold.ttf"
            outlines [(2, "#000000cc", 0, 0)]
