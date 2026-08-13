# Portfolio + Journal phone screens.
# portfolio_scr: shows completed projects, performances, milestones.
# journal_scr: chronological log of journal entries.

init python:
    _PORTFOLIO_DOMAINS = [
        ("programming", "Programming"),
        ("music",       "Music"),
    ]

    _JOURNAL_CATEGORY_PREFIX = {
        "career":  "[Career]",
        "project": "[Project]",
        "story":   "[Story]",
        "journal": "[Journal]",
        "money":   "[Finance]",
    }

    def _journal_prefix(category):
        return _JOURNAL_CATEGORY_PREFIX.get(category, "[" + category.title() + "]")


screen portfolio_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Portfolio" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 610
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 10
                    xfill True
                    # ── Programming domain ───────────────────────────────
                    $ _prog_entries = [e for e in player_portfolio.values() if e["domain"] == "programming"]
                    if _prog_entries:
                        text "Programming" font PROFILE_FONT size 14 color "#4db1ff"
                        $ _total_pay = sum(e["metadata"].get("pay", 0) for e in _prog_entries)
                        text ("%d projects  ·  $%d total" % (len(_prog_entries), _total_pay)) font ACT_FONT size 12 color "#7a9ab8"
                        null height 2
                        for _pe in sorted(_prog_entries, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 8, 10, 8)
                                vbox:
                                    spacing 2
                                    text _pe["title"] font PROFILE_FONT size 13 color "#cfe0f5"
                                    hbox:
                                        spacing 10
                                        text ("Day %d" % (_pe["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                                        if _pe["metadata"].get("client"):
                                            text _pe["metadata"]["client"] font ACT_FONT size 11 color "#4a6080"
                                        if _pe["metadata"].get("pay", 0) > 0:
                                            text ("$%d" % _pe["metadata"]["pay"]) font ACT_FONT size 11 color "#ffd66a"
                    # ── Music domain ─────────────────────────────────────
                    $ _music_entries = [e for e in player_portfolio.values() if e["domain"] == "music"]
                    if _music_entries:
                        null height 4
                        text "Music" font PROFILE_FONT size 14 color "#ff7fb0"
                        for _me in sorted(_music_entries, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 8, 10, 8)
                                vbox:
                                    spacing 2
                                    text _me["title"] font PROFILE_FONT size 13 color "#cfe0f5"
                                    text ("Day %d" % (_me["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                    # ── Art domain (Phase 65) ────────────────────────────
                    # Read-only by design: every action on a piece lives in the
                    # My Artworks screen, so there is one place to change one.
                    $ _art_entries = [a for a in player_artworks if a["in_portfolio"]]
                    if _art_entries:
                        null height 4
                        text "Art" font PROFILE_FONT size 14 color "#c08ae0"
                        $ _art_value = sum(a["estimated_value"] for a in _art_entries)
                        text ("%d pieces  ·  $%d appraised  ·  reputation %d" % (len(_art_entries), _art_value, art_reputation)) font ACT_FONT size 12 color "#7a9ab8"
                        null height 2
                        for _ae in sorted(_art_entries, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 8, 10, 8)
                                vbox:
                                    spacing 2
                                    hbox:
                                        spacing 8
                                        text _ae["subject"] font PROFILE_FONT size 13 color "#cfe0f5"
                                        text art_quality_label(_ae["quality"]) font ACT_FONT size 11 color tier_color(_ae["quality"]) yalign 0.5
                                    hbox:
                                        spacing 10
                                        text ("Day %d" % (_ae["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                                        text ("$%d" % _ae["estimated_value"]) font ACT_FONT size 11 color "#ffd66a"
                                        if _ae.get("client"):
                                            text _ae["client"] font ACT_FONT size 11 color "#4a6080"
                                        if _ae.get("exhibited_as"):
                                            text _ae["exhibited_as"] font ACT_FONT size 11 color "#c08ae0"
                    # ── Other domains (culinary / mechanics / art) — Phase 61 ─
                    $ _other_entries = [e for e in player_portfolio.values() if e["domain"] not in ("programming", "music")]
                    if _other_entries:
                        null height 4
                        text "Craft & Skill" font PROFILE_FONT size 14 color "#ff9f4d"
                        for _oe in sorted(_other_entries, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 8, 10, 8)
                                vbox:
                                    spacing 2
                                    text _oe["title"] font PROFILE_FONT size 13 color "#cfe0f5"
                                    hbox:
                                        spacing 10
                                        text ("Day %d" % (_oe["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                                        text _oe["domain"].title() font ACT_FONT size 11 color "#ff9f4d"
                    # ── Career milestones from journal ────────────────────
                    $ _career_entries = [e for e in player_journal if e["category"] == "career"]
                    if _career_entries:
                        null height 4
                        text "Career Milestones" font PROFILE_FONT size 14 color "#ffd66a"
                        for _ce in sorted(_career_entries, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 8, 10, 8)
                                hbox:
                                    spacing 8
                                    text "★" font PROFILE_FONT size 12 color "#ffd66a" yalign 0.5
                                    vbox:
                                        text _ce["title"] font PROFILE_FONT size 13 color "#ffd66a"
                                        text ("Day %d" % (_ce["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                    # ── Empty state ──────────────────────────────────────
                    if not player_portfolio and not _career_entries:
                        null height 20
                        text "Nothing here yet." font ACT_FONT size 15 color "#4a6080" xalign 0.5
                        text "Complete projects and reach career milestones to build your portfolio." font ACT_FONT size 12 color "#3a4a5a" xalign 0.5
            null height 6
            hbox:
                spacing 10
                xalign 0.5
                textbutton "Journal" action [Hide("portfolio_scr"), Show("journal_scr")] text_font ACT_FONT text_size 16 text_color "#5bcafa" text_hover_color "#ffffff"
                textbutton "Back" action [Hide("portfolio_scr"), Show("phone_home")] text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen journal_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Journal" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 610
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    $ _jentries = list(reversed(player_journal))
                    if not _jentries:
                        null height 20
                        text "Nothing recorded yet." font ACT_FONT size 15 color "#4a6080" xalign 0.5
                    for _je in _jentries:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 8, 10, 8)
                            hbox:
                                spacing 8
                                yalign 0.5
                                $ _jpfx = _journal_prefix(_je["category"])
                                text _jpfx font PROFILE_FONT size 11 color "#5bcafa" yalign 0.5 xsize 74
                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text _je["title"] font ACT_FONT size 13 color "#cfe0f5"
                                    text ("Day %d" % (_je["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("journal_scr"), Show("portfolio_scr")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
