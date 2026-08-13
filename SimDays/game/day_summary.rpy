# Day summary overlay — non-modal card in the bottom-left corner.
# Auto-collapses after 10 seconds. Shows aggregated activity from the previous day.
# Built by new_day() in data.rpy; read from pending_day_summary.

init python:
    # Human-readable skill labels for day summary (avoids import cycle).
    _SUMMARY_SKILL_LABELS = {
        "prog": "Programming", "med": "Medicine", "biz": "Business",
        "cook": "Cooking", "fit": "Fitness", "mech": "Mechanics",
        "art": "Art", "music": "Music",
    }


screen day_summary_overlay():
    modal False
    zorder 200
    default _day_summary_collapsed = False

    $ _pds = store.pending_day_summary
    if _pds and store.day_summary_visible:
        timer 10.0 action SetScreenVariable("_day_summary_collapsed", True)

        if _day_summary_collapsed:
            # ── Collapsed: small pill button ───────────────────────────
            frame:
                xpos 20 ypos 910
                background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                padding (12, 6, 12, 6)
                button:
                    action SetScreenVariable("_day_summary_collapsed", False)
                    background None
                    text ("Day %d" % (_pds["day"] + 1)):
                        font PROFILE_FONT size 15 color "#5bcafa" hover_color "#ffffff"
        else:
            # ── Expanded: summary card ─────────────────────────────────
            frame:
                xpos 20 ypos 760
                xsize 310
                background "#12161ef8"
                padding (14, 12, 14, 12)
                vbox:
                    spacing 6
                    # Title row
                    hbox:
                        xfill True
                        text ("DAY %d SUMMARY" % (_pds["day"] + 1)):
                            font PROFILE_FONT size 15 color "#5bcafa" yalign 0.5
                        button:
                            action [SetVariable("day_summary_visible", False), Hide("day_summary_overlay")]
                            background None
                            text "✕" font PROFILE_FONT size 14 color "#4a6080" hover_color "#ffffff" align (0.5, 0.5)
                    null height 2
                    # Money earned
                    if _pds.get("money_earned", 0) > 0:
                        hbox:
                            spacing 6
                            text "+" font PROFILE_FONT size 13 color "#7fd06a" yalign 0.5
                            text ("$%d earned" % _pds["money_earned"]) font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                    # Money spent
                    if _pds.get("money_spent", 0) > 0:
                        hbox:
                            spacing 6
                            text "-" font PROFILE_FONT size 13 color "#e86a55" yalign 0.5
                            text ("$%d spent" % _pds["money_spent"]) font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                    # Skills gained
                    for _sk, _xp in (_pds.get("skills") or {}).items():
                        if _xp > 0:
                            $ _sk_lbl = _SUMMARY_SKILL_LABELS.get(_sk, _sk.title())
                            hbox:
                                spacing 6
                                text "▸" font PROFILE_FONT size 12 color "#4db1ff" yalign 0.5
                                text ("%s  +%d XP" % (_sk_lbl, _xp)) font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                    # Notable events
                    for _note in (_pds.get("notable") or []):
                        if _note:
                            hbox:
                                spacing 6
                                text "★" font PROFILE_FONT size 12 color "#ffd66a" yalign 0.5
                                text _note font ACT_FONT size 12 color "#ffd66a" yalign 0.5
                    # Fallback if nothing recorded
                    if (not _pds.get("money_earned") and not _pds.get("money_spent")
                            and not _pds.get("skills") and not _pds.get("notable")):
                        text "Quiet day." font ACT_FONT size 13 color "#4a6080"
                    null height 2
                    button:
                        xalign 1.0
                        action SetScreenVariable("_day_summary_collapsed", True)
                        background None
                        text "Collapse" font ACT_FONT size 11 color "#4a6080" hover_color "#9fb6d6"
