# Profile / status panel - right side, tucked UNDER the topbar HUD so it never
# covers it. NON-modal: actions on the left stay clickable while it's open.
# Toggle with the "Me" button (top-right of HUD) or the C key.

define PROFILE_FONT = "fonts/Quicksand-SemiBold.ttf"

# Fixed column widths so every bar in the panel starts at the same x:
#   row padding-left 14 + icon 36 + 12 + label 140 + 12  ->  bar x = 214.
# Row budget: panel 520 - padding 32 - scrollbar ~22 = 466 content, minus 28 row
# padding = 438; 36+140+160+60 + 3*12 spacing = 432. 6px slack.
define PROFILE_W     = 520
define PROFILE_ICON  = 36
define PROFILE_LABEL = 140
define PROFILE_BAR   = 160
define PROFILE_VAL   = 60

# One skill row that fills the panel width: icon + label (xfill) + bar + value.
# Label uses xfill True so the bar is always pinned to the right edge regardless
# of label length — no more "Programming" wrapping under the bar.
screen stat_chip(label, value, fill, icon=None, tip=""):
    button:
        xfill True
        ysize 68
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action NullAction()
        tooltip tip
        padding (12, 8, 12, 8)
        hbox:
            xfill True
            spacing 10
            yalign 0.5
            if icon:
                add icon xysize (28, 28) yalign 0.5
            else:
                null width 28
            text label font PROFILE_FONT size 17 color "#cfe0f5" yalign 0.5 xfill True
            bar:
                value StaticValue(value, 100)
                xsize 148 ysize 14 yalign 0.5
                left_bar Frame(fill, 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
            text "[value]" font PROFILE_FONT size 17 color "#ffffff" yalign 0.5 xsize 48 textalign 1.0


# One specialization row (icon + name + 0-10 bar + level). All are shown so the
# player sees the full set of trades, learned or not.
# Skill name is xfill so bar is always right-aligned; level replaces xp fraction
# (xp is still readable in the tooltip).
screen spec_row(key):
    $ _lv = skill_val(key)
    $ _ex = skill_exp.get(key, 0)
    $ _need = skill_exp_needed(_lv)
    $ _maxed = _lv >= 100
    button:
        xfill True
        ysize 50
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        action NullAction()
        tooltip ("%s — Lv %d. %s" % (PRO_SKILLS[key][0], _lv, "Maxed." if _maxed else "%d/%d XP to next." % (_ex, _need)))
        padding (12, 6, 12, 6)
        hbox:
            xfill True
            spacing 10
            yalign 0.5
            $ _ic = "images/ui/icons/skill_%s.png" % key
            if renpy.loadable(_ic):
                add _ic xysize (26, 26) yalign 0.5
            else:
                null width 26
            text PRO_SKILLS[key][0] font PROFILE_FONT size 16 color ("#cfe0f5" if _lv > 0 else "#7f8ba0") yalign 0.5 xfill True
            bar:
                value StaticValue((10 if _maxed else _ex), (10 if _maxed else _need))
                xsize 130 ysize 12 yalign 0.5
                left_bar Frame("images/ui/bar_fill_%s.png" % PRO_SKILLS[key][2], 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
            text ("MAX" if _maxed else "Lv%d" % _lv) font PROFILE_FONT size 15 color "#ffffff" yalign 0.5 xsize 44 textalign 1.0


screen profile():
    zorder 30
    # right side, below the topbar; no `modal` -> left menu stays live.

    frame:
        xpos 1920 - PROFILE_W
        ypos 200
        xsize PROFILE_W
        ysize 818
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
                    xsize 466
                    spacing 8

                    text "CORE STATS" font PROFILE_FONT size 16 color "#7fa0cc"
                    use stat_chip("Strength",   stat_str, "images/ui/bar_fill_str.png", "images/ui/icons/stat_str.png", "Strength - train at the gym. Gates physical jobs.")
                    use stat_chip("Intellect",  stat_int, "images/ui/bar_fill_int.png", "images/ui/icons/stat_int.png", "Intellect - study at the library / work desk jobs. Gates IT, corporate, medicine.")
                    use stat_chip("Charisma",   stat_chr, "images/ui/bar_fill_chr.png", "images/ui/icons/stat_social.png", "Charisma - socialize (bar, club). Helps relationships and people-facing work.")
                    $ _app_eff  = eff_app()
                    $ _app_base = stat_app
                    $ _app_eq   = equipped_appearance_bonus()
                    $ _app_tmp  = temporary_appearance_bonus()
                    $ _app_tip  = app_breakdown_tooltip()
                    $ _app_sub  = ("Base %d" % _app_base) + ("  •  Style +%d" % _app_eq if _app_eq else "") + ("  •  +%d temp" % _app_tmp if _app_tmp else "")
                    button:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        action NullAction()
                        tooltip _app_tip
                        padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            hbox:
                                xfill True
                                spacing 10
                                yalign 0.5
                                add "images/ui/icons/stat_app.png" xysize (28, 28) yalign 0.5
                                text "Appearance" font PROFILE_FONT size 17 color "#cfe0f5" yalign 0.5 xfill True
                                bar:
                                    value StaticValue(_app_eff, 100)
                                    xsize 148 ysize 14 yalign 0.5
                                    left_bar Frame("images/ui/bar_fill_app.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                                text "[_app_eff]" font PROFILE_FONT size 17 color "#ffffff" yalign 0.5 xsize 48 textalign 1.0
                            text "[_app_sub]" font PROFILE_FONT size 12 color "#7a9ab8" xpos 38

                    null height 4
                    text "SPECIALIZATIONS" font PROFILE_FONT size 16 color "#7fa0cc"
                    for _k in PRO_SKILLS:
                        use spec_row(_k)

                    null height 4
                    text "WORK" font PROFILE_FONT size 16 color "#7fa0cc"
                    if active_careers:
                        for _cid, _cdata in active_careers.items():
                            $ _c_rank = _cdata.get("rank", 0)
                            $ _c_perf = _cdata.get("perf", 0)
                            $ _c_info = CAREERS.get(_cid, {})
                            $ _c_ranks = _c_info.get("ranks", [])
                            $ _c_r    = _c_ranks[_c_rank] if _c_rank < len(_c_ranks) else {}
                            $ _c_short = _c_info.get("name", _cid).split(" - ")[0]
                            $ _c_title = _c_r.get("title", "?") + " - " + _c_short
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (16, 10, 18, 10)
                                vbox:
                                    spacing 6
                                    text _c_title font PROFILE_FONT size 18 color "#ffffff"
                                    hbox:
                                        spacing 10
                                        text "Perf" font PROFILE_FONT size 16 color "#cfe0f5" yalign 0.5
                                        bar:
                                            value StaticValue(_c_perf, 100)
                                            xsize PROFILE_BAR ysize 14 yalign 0.5
                                            left_bar Frame("images/ui/bar_fill_perf.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                                        text ("%d" % _c_perf) font PROFILE_FONT size 16 color "#ffffff" yalign 0.5
                                    $ _cp = career_arc_progress(_cid)
                                    if _cp[1] > 0:
                                        text ("Arc: %d/%d" % _cp) font PROFILE_FONT size 14 color "#5a7090"
                                    $ _next_ridx = _c_rank + 1
                                    if _next_ridx < len(_c_ranks):
                                        $ _nr     = _c_ranks[_next_ridx]
                                        $ _nr_req = _nr.get("req", {})
                                        text ("Next: " + _nr["title"]) font PROFILE_FONT size 15 color "#9fb6d6"
                                        for _rk in _nr_req:
                                            $ _rv = _nr_req[_rk]
                                            if _rk.startswith("stat_"):
                                                $ _sname = _rk[5:].upper()
                                                $ _sval  = store.stat_app if _rk == "stat_app" else getattr(store, _rk, 0)
                                                $ _sok   = _sval >= _rv
                                                text ("%s %d  %s" % (_sname, _rv, "✓" if _sok else "(%d/%d)" % (_sval, _rv))) font PROFILE_FONT size 14 color ("#5bcafa" if _sok else "#c06060")
                                            elif _rk.startswith("skill_"):
                                                $ _skname = _rk[6:].capitalize()
                                                $ _skval  = getattr(store, _rk, 0)
                                                $ _skok   = _skval >= _rv
                                                text ("%s Lv%d  %s" % (_skname, _rv, "✓" if _skok else "(%d/%d)" % (_skval, _rv))) font PROFILE_FONT size 14 color ("#5bcafa" if _skok else "#c06060")
                                            elif _rk == "degree":
                                                $ _dok = _rv in degrees
                                                text ("Degree: " + _rv.replace("_", " ").title() + ("  ✓" if _dok else "  ✗")) font PROFILE_FONT size 14 color ("#5bcafa" if _dok else "#c06060")
                                        text ("Performance %d/100  %s" % (_c_perf, "✓" if _c_perf >= 100 else "")) font PROFILE_FONT size 14 color ("#5bcafa" if _c_perf >= 100 else "#c06060")
                    else:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                            padding (16, 12, 18, 12)
                            vbox:
                                spacing 4
                                text "Unemployed" font PROFILE_FONT size 20 color "#ffffff"
                                text "Find work in the city." font PROFILE_FONT size 16 color "#9fb6d6"

                    null height 4
                    text "ASSETS" font PROFILE_FONT size 16 color "#7fa0cc"
                    $ _tiers = "Home t%d   Car t%d   Wardrobe t%d   Jewelry t%d" % (apartment_tier, car_tier, wardrobe_tier, jewelry_tier)
                    $ _cdl = cosmetic_days_left()
                    $ _cosmetic_str = ("Polished Look: %d day%s" % (_cdl, "s" if _cdl != 1 else "")) if _cdl > 0 else ""
                    $ _items = ", ".join([n for n, o in [("Computer", own_computer), ("Guitar", own_guitar), ("Better bed", own_bed), ("Prog kit", own_programming_kit), ("Coffee machine", own_coffee_machine), ("Kitchen set", own_kitchen_set)] if o]) or "none"
                    frame:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        padding (16, 10, 18, 10)
                        vbox:
                            spacing 4
                            text "[_tiers]" font PROFILE_FONT size 16 color "#cfe0f5"
                            text "Items: [_items]" font PROFILE_FONT size 16 color "#cfe0f5"
                            if _cosmetic_str:
                                text "[_cosmetic_str]" font PROFILE_FONT size 14 color "#c07bff"

            # hover footer: shows the tooltip of whatever stat/skill you point at
            $ _ptt = GetTooltip()
            if _ptt:
                text "[_ptt]" font PROFILE_FONT size 15 color "#e0c060" xsize 466
