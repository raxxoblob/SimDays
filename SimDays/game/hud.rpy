# Always-on HUD: generated blue panel + live values (date/time, money, needs).
# Stat badge icons come from images/ui/icons/stat_*.png. Panel = hud_panel.png.

screen hud():
    zorder 10
    $ datestr = "%s . Day %d" % (day_name(day), day + 1)
    $ timestr = time_label(hour)

    add "images/ui/hud_panel.png" xpos 24 ypos 18

    # date + time
    add "images/ui/icons/stat_time.png" xpos 40 ypos 32 xysize (46, 46)
    text "[datestr]" xpos 96 ypos 34 size 19 color "#c8deff"
    text "[timestr]" xpos 96 ypos 58 size 28 color "#ffffff" bold True

    # money
    add "images/ui/icons/stat_money.png" xpos 344 ypos 32 xysize (46, 46)
    text "$[money]" xpos 398 ypos 42 size 28 color "#ffdc78" bold True

    # needs
    add "images/ui/icons/stat_hunger.png" xpos 40 ypos 118 xysize (34, 34)
    bar value StaticValue(need_hunger, 100) xpos 80 ypos 123 xysize (108, 14) left_bar Solid("#ef9f27") right_bar Solid("#00000066") thumb Null()

    add "images/ui/icons/stat_hygiene.png" xpos 222 ypos 118 xysize (34, 34)
    bar value StaticValue(need_hygiene, 100) xpos 262 ypos 123 xysize (108, 14) left_bar Solid("#1d9e75") right_bar Solid("#00000066") thumb Null()

    add "images/ui/icons/stat_energy.png" xpos 404 ypos 118 xysize (34, 34)
    bar value StaticValue(need_energy, 100) xpos 444 ypos 123 xysize (108, 14) left_bar Solid("#97c459") right_bar Solid("#00000066") thumb Null()
