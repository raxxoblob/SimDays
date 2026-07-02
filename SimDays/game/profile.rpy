# Profile / status strip - a horizontal, scrollable bar under the HUD.
# NON-modal: it floats on top but you can still click activities behind it.
# Toggle with the "Me" button (top-right of HUD) or the C key.

define PROFILE_FONT = "fonts/Quicksand-SemiBold.ttf"

# One compact stat chip: icon + label on top, bar + value below.
screen stat_chip(label, value, fill, icon=None):
    frame:
        xysize (238, 100)
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (18, 12, 18, 12)
        vbox:
            spacing 8
            hbox:
                spacing 8
                if icon:
                    add icon xysize (30, 30) yalign 0.5
                text label font PROFILE_FONT size 18 color "#cfe0f5" yalign 0.5
            hbox:
                spacing 8
                bar:
                    value StaticValue(value, 100)
                    xysize (150, 18) yalign 0.5
                    left_bar Frame(fill, 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
                text "[value]" font PROFILE_FONT size 18 color "#ffffff" yalign 0.5


screen profile():
    zorder 30
    # NOTE: no `modal True` - actions behind the strip stay clickable.

    frame:
        xalign 0.5
        ypos 150
        xsize 1560
        ysize 128
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 14, 14, 14)

        hbox:
            spacing 12

            viewport id "profstrip":
                xsize 1430
                mousewheel "horizontal"
                draggable True
                scrollbars "horizontal"
                hbox:
                    spacing 14
                    use stat_chip("Strength",   stat_str, "images/ui/bar_fill_str.png", "images/ui/icons/stat_str.png")
                    use stat_chip("Intellect",  stat_int, "images/ui/bar_fill_int.png", "images/ui/icons/stat_int.png")
                    use stat_chip("Charisma",   stat_chr, "images/ui/bar_fill_chr.png", "images/ui/icons/stat_social.png")
                    use stat_chip("Appearance", stat_app, "images/ui/bar_fill_app.png")  # no icon yet

                    # Job chip (wider). Shows Performance, or "Unemployed".
                    frame:
                        xysize (360, 100)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        padding (18, 12, 18, 12)
                        vbox:
                            spacing 8
                            if job_title:
                                text "[job_title]" font PROFILE_FONT size 18 color "#ffffff"
                                hbox:
                                    spacing 8
                                    text "Perf" font PROFILE_FONT size 16 color "#cfe0f5" yalign 0.5
                                    bar:
                                        value StaticValue(job_performance, 100)
                                        xysize (210, 18) yalign 0.5
                                        left_bar Frame("images/ui/bar_fill_perf.png", 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()
                                    text "[job_performance]" font PROFILE_FONT size 16 color "#ffffff" yalign 0.5
                                if job_next:
                                    text "Next: [job_next]" font PROFILE_FONT size 15 color "#9fb6d6"
                            else:
                                text "Unemployed" font PROFILE_FONT size 20 color "#ffffff"
                                text "Find work in the city." font PROFILE_FONT size 15 color "#9fb6d6"

            # close button (X) pinned right
            textbutton "X":
                yalign 0.0
                action Hide("profile")
                text_font PROFILE_FONT text_size 26 text_color "#9fb6d6" text_hover_color "#ffffff"
