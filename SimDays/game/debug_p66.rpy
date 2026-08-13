# Phase 66 debug — relationship depth. Reachable from the debug menu.
# tests/phase66_selfcheck.py is the authoritative runnable check; this screen is
# LIVE state inspection: all axes, stage, profile, today's saturation, gift
# history, invitation pressure, and the change trace.

default _p66_npc = "nora"

init python:

    def _p66_axes(npc_id):
        return [(a.capitalize(), a, npc_rel(npc_id, a)) for a in REL_AXES]

    def _p66_saturation_line(npc_id):
        per = store._rel_saturation.get(npc_id, {})
        live = ["%s x%d" % (c, v[1]) for c, v in per.items() if v[0] == store.day]
        return ", ".join(live) if live else "nothing yet today"

    def _p66_profile_line(npc_id):
        p = npc_rel_profile(npc_id)
        return "  ".join("%s %.2f" % (k[:4], p[k]) for k in sorted(p))

    def _p66_gift_line(npc_id):
        h = npc_gift_history(npc_id, 5)
        if not h:
            return "no gifts"
        return ", ".join("%s(d%d)" % (g.get("gift_type", "?"), g.get("day", -1)) for g in h)

    def _p66_invite_line(npc_id):
        return "  ".join("%s %.0f%%" % (t, invitation_acceptance_chance(npc_id, t) * 100)
                         for t in ("casual", "home_visit", "professional", "romantic"))

    def _p66_set_axis(npc_id, axis, value):
        set_npc_rel(npc_id, axis, value)
        renpy.notify("%s %s = %d" % (npc_id, axis, npc_rel(npc_id, axis)))

    def _p66_toggle_trace():
        store._rel_trace_enabled = not store._rel_trace_enabled
        renpy.notify("Relationship trace %s" % ("ON" if store._rel_trace_enabled else "OFF"))

    def _p66_clear_trace():
        store._rel_trace = []

    def _p66_test_change(npc_id, category):
        got = apply_relationship_change(npc_id, "debug", category,
                                        affection=3, trust=3, respect=3, familiarity=3)
        renpy.notify("%s via %s -> %s" % (npc_id, category, got or "capped/saturated"))


screen debug_p66_scr():
    modal True
    zorder 210
    add "#000000e0"
    frame:
        xalign 0.5 yalign 0.5
        xsize 900
        ysize 680
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "PHASE 66 — RELATIONSHIP DEPTH" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            null height 2
            hbox:
                spacing 6
                xalign 0.5
                for _n in sorted(NPC_DATA):
                    textbutton NPC_DATA[_n]["name"][:6]:
                        action SetVariable("_p66_npc", _n)
                        text_size 12
                        text_color ("#ffd66a" if _p66_npc == _n else "#7a9ab8")
            null height 4
            viewport:
                xfill True
                ysize 520
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True
                    $ _n = _p66_npc

                    text "%s — stage: %s" % (NPC_DATA[_n]["name"], npc_relationship_stage_label(_n)) font PROFILE_FONT size 15 color "#ffd66a"
                    for _lbl, _ax, _v in _p66_axes(_n):
                        if _ax != "attraction" or npc_is_romance_capable(_n):
                            hbox:
                                spacing 8
                                xfill True
                                text "%-12s %4d" % (_lbl, _v) font ACT_FONT size 12 color "#cfe0f5" yalign 0.5
                                textbutton "0"  action Function(_p66_set_axis, _n, _ax, 0) text_size 11
                                textbutton "25" action Function(_p66_set_axis, _n, _ax, 25) text_size 11
                                textbutton "50" action Function(_p66_set_axis, _n, _ax, 50) text_size 11
                                textbutton "75" action Function(_p66_set_axis, _n, _ax, 75) text_size 11
                                textbutton "100" action Function(_p66_set_axis, _n, _ax, 100) text_size 11

                    null height 6
                    text "PROFILE" font PROFILE_FONT size 13 color "#ffd66a"
                    text _p66_profile_line(_n) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "SATURATION TODAY" font PROFILE_FONT size 13 color "#ffd66a"
                    text _p66_saturation_line(_n) font ACT_FONT size 12 color "#7a9ab8"
                    hbox:
                        spacing 8
                        textbutton "Clear (this NPC)" action Function(clear_rel_saturation, _n) text_size 12
                        textbutton "Clear (all)" action Function(clear_rel_saturation) text_size 12

                    null height 6
                    text "GIFT HISTORY (last 5)" font PROFILE_FONT size 13 color "#ffd66a"
                    text _p66_gift_line(_n) font ACT_FONT size 12 color "#7a9ab8"
                    text "repetition multiplier: %.2f" % _gift_repetition_multiplier(_n) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "INVITATION PRESSURE" font PROFILE_FONT size 13 color "#ffd66a"
                    text _p66_invite_line(_n) font ACT_FONT size 12 color "#7a9ab8"

                    null height 6
                    text "SOURCE CONTRIBUTION TOTALS" font PROFILE_FONT size 13 color "#ffd66a"
                    $ _tot = _rel_source_totals.get(_n, {})
                    if _tot:
                        for _cat in sorted(_tot):
                            text "%-18s %s" % (_cat, _tot[_cat]) font ACT_FONT size 11 color "#7a9ab8"
                    else:
                        text "none recorded" font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "TEST A CHANGE (+3 all axes)" font PROFILE_FONT size 13 color "#ffd66a"
                    hbox:
                        spacing 6
                        box_wrap True
                        for _cat in sorted(RELATIONSHIP_SOURCE_CAPS):
                            textbutton _cat action Function(_p66_test_change, _n, _cat) text_size 11

                    null height 8
                    text "CHANGE TRACE (newest last)" font PROFILE_FONT size 13 color "#ffd66a"
                    hbox:
                        spacing 8
                        textbutton ("Trace log: ON" if _rel_trace_enabled else "Trace log: OFF") action Function(_p66_toggle_trace) text_size 12
                        textbutton "Clear" action Function(_p66_clear_trace) text_size 12
                    for _e in _rel_trace[-15:]:
                        text ("d%d %s %s/%s req=%s got=%s sat=%.2f"
                              % (_e["day"], _e["npc"], _e["cat"], _e["src"],
                                 _e["req"], _e["got"], _e["sat"])) font ACT_FONT size 11 color "#5bcafa"

            null height 4
            textbutton "Close" action [Hide("debug_p66_scr"), Show("debug_menu")] xalign 0.5 text_size 16 text_color "#9fb6d6"
