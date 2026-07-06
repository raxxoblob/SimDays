# Profile / status panel - right side, tucked UNDER the topbar HUD so it never
# covers it. NON-modal: actions on the left stay clickable while it's open.
# Toggle with the "Me" button (top-right of HUD) or the C key.

define PROFILE_FONT = "fonts/Quicksand-SemiBold.ttf"

# One skill row that fills the panel width: icon + label + bar + value.
screen stat_chip(label, value, fill, icon=None, tip=""):
    button:
        xfill True
        ysize 76
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action NullAction()
        tooltip tip
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


# One specialization row (icon + name + 0-10 bar + value). All are shown so the
# player sees the full set of trades, learned or not.
screen spec_row(key):
    $ _lv = skill_val(key)
    $ _ex = skill_exp.get(key, 0)
    $ _need = skill_exp_needed(_lv)
    $ _maxed = _lv >= 10
    button:
        xfill True
        ysize 52
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action NullAction()
        tooltip ("%s - Lv %d. %s" % (PRO_SKILLS[key][0], _lv, "Maxed out." if _maxed else "%d/%d EXP to Lv %d (higher levels take more)." % (_ex, _need, _lv + 1)))
        padding (14, 7, 16, 7)
        hbox:
            spacing 10
            $ _ic = "images/ui/icons/skill_%s.png" % key
            if renpy.loadable(_ic):
                add _ic xysize (28, 28) yalign 0.5
            else:
                null width 28
            text ("%s  Lv%d" % (PRO_SKILLS[key][0], _lv)) font PROFILE_FONT size 17 color ("#cfe0f5" if _lv > 0 else "#7f8ba0") yalign 0.5 xsize 120
            bar:
                value StaticValue((10 if _maxed else _ex), (10 if _maxed else _need))
                xsize 108 ysize 13 yalign 0.5
                left_bar Frame("images/ui/bar_fill_%s.png" % PRO_SKILLS[key][2], 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
            text ("MAX" if _maxed else "%d/%d" % (_ex, _need)) font PROFILE_FONT size 15 color "#ffffff" yalign 0.5 xalign 1.0


screen profile():
    zorder 30
    # right side, below the topbar (ypos 150); no `modal` -> left menu stays live.

    frame:
        xpos 1490
        ypos 150
        xsize 430
        ysize 868
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (20, 16, 12, 16)

        vbox:
            spacing 8
            # ── fixed header ──
            hbox:
                text "[mc_name]" font PROFILE_FONT size 30 color "#ffffff" yalign 0.5
                textbutton "X":
                    xalign 1.0 yalign 0.5
                    action Hide("profile")
                    text_font PROFILE_FONT text_size 24 text_color "#9fb6d6" text_hover_color "#ffffff"
            $ _st = status_score()
            $ _stl = status_label()
            $ _cap = affection_cap()
            text "Status: [_stl] ([_st]/100)  -  love cap [_cap]" font PROFILE_FONT size 16 color "#e0c060"

            # ── scrollable body ──
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 748
                vbox:
                    xsize 360
                    spacing 8

                    text "CORE STATS" font PROFILE_FONT size 15 color "#7fa0cc"
                    use stat_chip("Strength",   stat_str, "images/ui/bar_fill_str.png", "images/ui/icons/stat_str.png", "Strength - train at the gym. Gates physical jobs.")
                    use stat_chip("Intellect",  stat_int, "images/ui/bar_fill_int.png", "images/ui/icons/stat_int.png", "Intellect - study at the library / work desk jobs. Gates IT, corporate, medicine.")
                    use stat_chip("Charisma",   stat_chr, "images/ui/bar_fill_chr.png", "images/ui/icons/stat_social.png", "Charisma - socialize (bar, club). Helps relationships and people-facing work.")
                    use stat_chip("Appearance", stat_app, "images/ui/bar_fill_app.png", "images/ui/icons/stat_app.png", "Appearance - gym, clothes, grooming. Low hygiene tanks it fast.")

                    null height 4
                    text "SPECIALIZATIONS" font PROFILE_FONT size 15 color "#7fa0cc"
                    for _k in PRO_SKILLS:
                        use spec_row(_k)

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
                                        xsize 180 ysize 16 yalign 0.5
                                        left_bar Frame("images/ui/bar_fill_perf.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                                    text "[job_performance]" font PROFILE_FONT size 16 color "#ffffff" yalign 0.5
                                if job_next:
                                    text "Next: [job_next]" font PROFILE_FONT size 15 color "#9fb6d6"
                            else:
                                text "Unemployed" font PROFILE_FONT size 19 color "#ffffff"
                                text "Find work in the city." font PROFILE_FONT size 15 color "#9fb6d6"

                    null height 4
                    text "ASSETS" font PROFILE_FONT size 15 color "#7fa0cc"
                    $ _tiers = "Home t%d   Car t%d   Wardrobe t%d   Jewelry t%d" % (apartment_tier, car_tier, wardrobe_tier, jewelry_tier)
                    $ _items = ", ".join([n for n, o in [("Computer", own_computer), ("Guitar", own_guitar), ("Better bed", own_bed)] if o]) or "none"
                    frame:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        padding (16, 10, 18, 10)
                        vbox:
                            spacing 4
                            text "[_tiers]" font PROFILE_FONT size 15 color "#cfe0f5"
                            text "Items: [_items]" font PROFILE_FONT size 15 color "#cfe0f5"

            # hover footer: shows the tooltip of whatever stat/skill you point at
            $ _ptt = GetTooltip()
            if _ptt:
                text "[_ptt]" font PROFILE_FONT size 14 color "#e0c060" xsize 386
