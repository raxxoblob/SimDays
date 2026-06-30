# Always-on HUD: single decorative top bar (hud_topbar.png), centred near top.
# Holds date/time, money, and the three need bars. Top-left screen corner left free.

screen hud():
    zorder 10
    $ datestr = "%s . Day %d" % (day_name(day), day + 1)
    $ timestr = time_label(hour)

    fixed:
        xalign 0.5
        ypos 8
        xysize (1641, 129)
        add "images/ui/hud_topbar.png"

        add "images/ui/icons/stat_time.png" xpos 180 ypos 36 xysize (56, 56)
        text "[datestr]" xpos 250 ypos 28 size 20 color "#143c6e"
        text "[timestr]" xpos 250 ypos 56 size 30 color "#0a285a" bold True

        add "images/ui/icons/stat_money.png" xpos 620 ypos 36 xysize (56, 56)
        text "$[money]" xpos 686 ypos 46 size 30 color "#8a5a00" bold True

        add "images/ui/icons/stat_hunger.png" xpos 930 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hunger, 100) xpos 980 ypos 62 xysize (112, 16) left_bar Solid("#ef9f27") right_bar Solid("#ffffffa0") thumb Null()
        add "images/ui/icons/stat_hygiene.png" xpos 1108 ypos 42 xysize (44, 44)
        bar value StaticValue(need_hygiene, 100) xpos 1158 ypos 62 xysize (112, 16) left_bar Solid("#1d9e75") right_bar Solid("#ffffffa0") thumb Null()
        add "images/ui/icons/stat_energy.png" xpos 1286 ypos 42 xysize (44, 44)
        bar value StaticValue(need_energy, 100) xpos 1336 ypos 62 xysize (112, 16) left_bar Solid("#97c459") right_bar Solid("#ffffffa0") thumb Null()
