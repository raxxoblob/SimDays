# Always-on HUD: single decorative top bar (hud_topbar.png), centred near top.
# Holds date/time, money, and the three need bars. Top-left screen corner left free.

screen hud():
    zorder 10
    $ datestr = "%s . Day %d" % (day_name(day), day + 1)
    $ timestr = time_label(hour)

    # Profile / status panel: click "Me" (top-right) or press C.
    key "K_c" action ToggleScreen("profile")
    button:
        xpos 1792 ypos 22
        xysize (104, 52)
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action ToggleScreen("profile")
        text "Me" font "fonts/Quicksand-SemiBold.ttf" size 24 color "#cfe0f5" align (0.5, 0.5)

    fixed:
        xalign 0.5
        ypos 8
        xysize (1641, 129)
        add "images/ui/hud_topbar.png"

        add "images/ui/icons/stat_time.png" xpos 180 ypos 36 xysize (56, 56)
        text "[datestr]" xpos 250 ypos 30 size 19 color "#143c6e" font "fonts/VarelaRound.ttf"
        text "[timestr]" xpos 250 ypos 56 size 28 color "#0a285a" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_money.png" xpos 620 ypos 36 xysize (56, 56)
        text "$[money]" xpos 686 ypos 48 size 28 color "#8a5a00" font "fonts/VarelaRound.ttf"

        add "images/ui/icons/stat_hunger.png" xpos 930 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hunger, 100) xpos 980 ypos 64 xysize (112, 18) left_bar Frame("images/ui/bar_fill_hunger.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        add "images/ui/icons/stat_hygiene.png" xpos 1108 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hygiene, 100) xpos 1158 ypos 64 xysize (112, 18) left_bar Frame("images/ui/bar_fill_hygiene.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
        add "images/ui/icons/stat_energy.png" xpos 1286 ypos 42 xysize (44, 44)
        bar value StaticValue(need_energy, 100) xpos 1336 ypos 64 xysize (112, 18) left_bar Frame("images/ui/bar_fill_energy.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
