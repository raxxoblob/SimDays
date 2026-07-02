# Profile / status panel - right side, tucked UNDER the topbar HUD so it never
# covers it. NON-modal: actions on the left stay clickable while it's open.
# Toggle with the "Me" button (top-right of HUD) or the C key.

define PROFILE_FONT = "fonts/Quicksand-SemiBold.ttf"

# One skill row that fills the panel width: icon + label + bar + value.
screen stat_chip(label, value, fill, icon=None):
    frame:
        xfill True
        ysize 76
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (16, 10, 18, 10)
        hbox:
            spacing 12
            if icon:
                add icon xysize (34, 34) yalign 0.5
            else:
                null width 34
            text label font PROFILE_FONT size 19 color "#cfe0f5" yalign 0.5 xsize 104
            bar:
                value StaticValue(value, 100)
                xsize 148 ysize 16 yalign 0.5
                left_bar Frame(fill, 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
            text "[value]" font PROFILE_FONT size 19 color "#ffffff" yalign 0.5 xalign 1.0


screen profile():
    zorder 30
    # right side, below the topbar (ypos 150); no `modal` -> left menu stays live.

    frame:
        xpos 1498
        ypos 150
        xsize 402
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 20)

        vbox:
            spacing 12

            hbox:
                text "[mc_name]" font PROFILE_FONT size 30 color "#ffffff" yalign 0.5
                textbutton "X":
                    xalign 1.0 yalign 0.5
                    action Hide("profile")
                    text_font PROFILE_FONT text_size 24 text_color "#9fb6d6" text_hover_color "#ffffff"

            text "SKILLS" font PROFILE_FONT size 15 color "#7fa0cc"
            use stat_chip("Strength",   stat_str, "images/ui/bar_fill_str.png", "images/ui/icons/stat_str.png")
            use stat_chip("Intellect",  stat_int, "images/ui/bar_fill_int.png", "images/ui/icons/stat_int.png")
            use stat_chip("Charisma",   stat_chr, "images/ui/bar_fill_chr.png", "images/ui/icons/stat_social.png")
            use stat_chip("Appearance", stat_app, "images/ui/bar_fill_app.png")  # no icon yet

            null height 4
            text "WORK" font PROFILE_FONT size 15 color "#7fa0cc"
            frame:
                xfill True
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                padding (16, 12, 18, 12)
                vbox:
                    spacing 8
                    if job_title:
                        text "[job_title]" font PROFILE_FONT size 19 color "#ffffff"
                        hbox:
                            spacing 10
                            text "Perf" font PROFILE_FONT size 16 color "#cfe0f5" yalign 0.5
                            bar:
                                value StaticValue(job_performance, 100)
                                xsize 200 ysize 16 yalign 0.5
                                left_bar Frame("images/ui/bar_fill_perf.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                            text "[job_performance]" font PROFILE_FONT size 16 color "#ffffff" yalign 0.5
                        if job_next:
                            text "Next: [job_next]" font PROFILE_FONT size 15 color "#9fb6d6"
                    else:
                        text "Unemployed" font PROFILE_FONT size 19 color "#ffffff"
                        text "Find work in the city." font PROFILE_FONT size 15 color "#9fb6d6"
