# Always-visible HUD overlay

screen hud():
    zorder 10
    # top bar background
    frame:
        xfill True
        ysize 58
        xpos 0
        ypos 0
        background "#000000cc"
        hbox:
            xfill True
            spacing 24
            padding (18, 8, 18, 8)
            # Date + time
            vbox:
                yalign 0.5
                text "[day_name(day)], Day [day+1]" style "hud_label"
                text "[time_label(hour)]"           style "hud_value"
            # Money
            vbox:
                yalign 0.5
                text "Money"   style "hud_label"
                text "$ [money]" style "hud_value"
            # Stats
            vbox:
                yalign 0.5
                text "STR [stat_str]  INT [stat_int]  CHR [stat_chr]  APP [stat_app]" style "hud_label"
            # Needs bars
            hbox:
                yalign 0.5
                spacing 10
                vbox:
                    text "Hunger"  style "hud_label"
                    bar value StaticValue(need_hunger, 100) xsize 80 ysize 8 style "hud_bar_need"
                vbox:
                    text "Hygiene" style "hud_label"
                    bar value StaticValue(need_hygiene, 100) xsize 80 ysize 8 style "hud_bar_need"
                vbox:
                    text "Energy"  style "hud_label"
                    bar value StaticValue(need_energy, 100) xsize 80 ysize 8 style "hud_bar_need"

style hud_label:
    size 12
    color "#aaaaaa"

style hud_value:
    size 15
    color "#ffffff"
    bold True

style hud_bar_need:
    ysize 8
    left_bar  Solid("#e8a020")
    right_bar Solid("#444444")
    thumb ""
