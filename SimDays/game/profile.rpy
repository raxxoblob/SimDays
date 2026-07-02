# Profile / status panel - slides in from the right. Skills + current job.
# Opened from the HUD button (or the C key). Matches the glass-bar UI style.

define PROFILE_FONT = "fonts/Quicksand-SemiBold.ttf"

# One skill row: optional icon, label, coloured bar, numeric value.
screen skill_row(icon, label, value, colour):
    hbox:
        spacing 12
        xsize 400
        if icon:
            add icon xysize (40, 40) yalign 0.5
        else:
            null width 40
        text label font PROFILE_FONT size 20 color "#cfe0f5" yalign 0.5 xsize 128
        bar:
            value StaticValue(value, 100)
            xsize 150 ysize 16 yalign 0.5
            left_bar Solid(colour) right_bar Solid("#ffffff28") thumb Null()
        text "[value]" font PROFILE_FONT size 20 color "#ffffff" yalign 0.5 xsize 40 xalign 1.0


screen profile():
    zorder 30
    modal True
    $ pdate = "%s . Day %d . %s" % (day_name(day), day + 1, time_label(hour))

    # click anywhere outside the panel to close
    button:
        xfill True yfill True
        background "#00000099"
        action Hide("profile")

    frame:
        xalign 1.0 yalign 0.5
        xsize 500 yfill True
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (40, 40, 40, 40)

        vbox:
            spacing 20

            # ── header ──
            text "[mc_name]" font PROFILE_FONT size 40 color "#ffffff"
            text "[pdate]" font PROFILE_FONT size 18 color "#9fb6d6"

            null height 6

            # ── skills ──
            text "SKILLS" font PROFILE_FONT size 18 color "#7fa0cc"
            use skill_row("images/ui/icons/stat_str.png",    "Strength",   stat_str, "#e0533c")
            use skill_row("images/ui/icons/stat_int.png",    "Intellect",  stat_int, "#3c82e0")
            use skill_row("images/ui/icons/stat_social.png", "Charisma",   stat_chr, "#e0b23c")
            # ponytail: no stat_app icon yet -> label-only until it's generated.
            use skill_row(None,                              "Appearance", stat_app, "#a05cd0")

            null height 10

            # ── work ──
            text "WORK" font PROFILE_FONT size 18 color "#7fa0cc"
            if job_title:
                text "[job_title]" font PROFILE_FONT size 22 color "#ffffff"
                hbox:
                    spacing 12
                    text "Performance" font PROFILE_FONT size 18 color "#cfe0f5" yalign 0.5 xsize 150
                    bar:
                        value StaticValue(job_performance, 100)
                        xsize 190 ysize 18 yalign 0.5
                        left_bar Solid("#39c07a") right_bar Solid("#ffffff28") thumb Null()
                    text "[job_performance]" font PROFILE_FONT size 18 color "#ffffff" yalign 0.5
                if job_next:
                    text "Next rank: [job_next]" font PROFILE_FONT size 17 color "#9fb6d6"
                if job_schedule:
                    text "Shift: [job_schedule]" font PROFILE_FONT size 17 color "#9fb6d6"
            else:
                text "Unemployed" font PROFILE_FONT size 22 color "#ffffff"
                text "Find work out in the city to start a career." font PROFILE_FONT size 17 color "#9fb6d6"

            null height 20
            textbutton "Close":
                action Hide("profile")
                text_font PROFILE_FONT text_size 20 text_color "#cfe0f5" text_hover_color "#ffffff"
