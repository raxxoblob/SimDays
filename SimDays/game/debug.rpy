# Dev/debug menu — press F9 in-game. Cheats to reach any game state for testing:
# money/stats/skills, jump into any career at any rank, set relationship levels,
# talk to anyone, skip time. Plus a character-size viewer to compare sprites.
# Purely a dev tool; nothing here is reachable in normal play.

default _dbg_talk_npc = None

init python:
    _DBG_NPCS = ["nora", "marcus", "caroline", "lena", "natalie", "martha",
                 "elle", "zoe", "sam", "eli", "kai", "rena"]
    _DBG_CAREERS = [("corporate", "Corporate"), ("it", "IT"), ("hospital", "Hospital"),
                    ("culinary", "Culinary"), ("trainer", "Trainer")]

    def _dbg_set_stats(v):
        for _s in ("str", "int", "chr", "app"):
            setattr(store, "stat_" + _s, v)

    def _dbg_set_skills(v):
        for _k in PRO_SKILLS:
            setattr(store, "skill_" + _k, v)
        store.skill_exp = {}

    def _dbg_refill():
        store.need_energy = store.need_hunger = store.need_hygiene = 100

    def _dbg_apply_career(cid, rank):
        c = CAREERS.get(cid)
        if not c:
            return
        rank = max(0, min(rank, len(c["ranks"]) - 1))
        _ac = dict(store.active_careers)
        _ac[cid] = {"rank": rank, "perf": 100}
        store.active_careers = _ac
        _sync_job(cid)
        renpy.notify("%s — rank %d" % (c["name"], rank + 1))

    def _dbg_meet_all():
        for _n in _DBG_NPCS:
            setattr(store, _n + "_met", True)
            mark_npc_encountered(_n)
            if _n not in store.npc_contacts:
                store.npc_contacts = list(store.npc_contacts) + [_n]
        renpy.notify("Met everyone + saved contacts")

    def _dbg_set_rel(nid, v):
        setattr(store, nid + "_met", True)
        mark_npc_encountered(nid)
        setattr(store, NPC_DATA[nid]["aff"], v)
        setattr(store, NPC_DATA[nid]["trust"], min(v, 100))
        renpy.notify("%s — aff/trust %d" % (NPC_DATA[nid]["name"], v))

    config.overlay_screens.append("debug_hotkey")


screen debug_hotkey():
    # Several bindings — F9 is grabbed by macOS, so backtick ` and Shift+D also work.
    key "K_F9"        action ToggleScreen("debug_menu")
    key "K_BACKQUOTE" action ToggleScreen("debug_menu")
    key "shift_K_d"   action ToggleScreen("debug_menu")
    # Guaranteed fallback: a tiny always-on button in the bottom-left corner.
    textbutton "DBG":
        xpos 6 ypos 1048
        action ToggleScreen("debug_menu")
        background "#00000066"
        padding (7, 3, 7, 3)
        text_size 13 text_color "#ffdd44aa" text_hover_color "#ffffff"


# ── Cheat menu ────────────────────────────────────────────────────────────
screen debug_menu():
    modal True
    zorder 250
    add "#000000d8"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 940
        ysize 940
        background "#12161ef8"
        padding (26, 20, 26, 20)
        vbox:
            spacing 10
            hbox:
                text "DEBUG  (F9)" font PROFILE_FONT size 30 color "#ffdd44" yalign 0.5
                textbutton "✕ Close" action Hide("debug_menu") xalign 1.0 text_size 18 text_color "#9fb6d6"
            null height 4
            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 840
                xfill True
                vbox:
                    spacing 6
                    xsize 860

                    text "RESOURCES" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "+$1,000"  action Function(gain_money, 1000)  text_size 16
                        textbutton "+$10,000" action Function(gain_money, 10000) text_size 16
                        textbutton "Clear loan" action SetVariable("loan", 0) text_size 16
                        textbutton "Refill needs" action Function(_dbg_refill) text_size 16

                    null height 6
                    text "STATS & SKILLS" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "Stats → 60" action Function(_dbg_set_stats, 60) text_size 16
                        textbutton "Stats → 90" action Function(_dbg_set_stats, 90) text_size 16
                        textbutton "Skills → 6" action Function(_dbg_set_skills, 6) text_size 16
                        textbutton "Skills → 10" action Function(_dbg_set_skills, 10) text_size 16

                    null height 6
                    text "CAREER  (applies at chosen rank, performance 100)" font PROFILE_FONT size 16 color "#5bcafa"
                    for _cid, _cname in _DBG_CAREERS:
                        hbox:
                            spacing 6
                            text _cname font ACT_FONT size 15 color "#cfe0f5" xsize 130 yalign 0.5
                            textbutton "Apply"  action Function(_dbg_apply_career, _cid, 0) text_size 15
                            textbutton "Rank 2" action Function(_dbg_apply_career, _cid, 1) text_size 15
                            textbutton "Rank 3" action Function(_dbg_apply_career, _cid, 2) text_size 15
                            textbutton "Rank 4" action Function(_dbg_apply_career, _cid, 3) text_size 15
                    textbutton "Quit job" action Function(quit_job) text_size 15

                    null height 6
                    text "TIME" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "+1h" action Function(spend_time, 1) text_size 16
                        textbutton "+6h" action Function(spend_time, 6) text_size 16
                        textbutton "Next day" action Function(new_day) text_size 16

                    null height 6
                    hbox:
                        text "CHARACTERS" font PROFILE_FONT size 16 color "#5bcafa" yalign 0.5
                        textbutton "  Meet everyone" action Function(_dbg_meet_all) text_size 15 xalign 0.0
                    for _nid in _DBG_NPCS:
                        hbox:
                            spacing 6
                            text NPC_DATA[_nid]["name"] font ACT_FONT size 15 color "#cfe0f5" xsize 110 yalign 0.5
                            textbutton "Meet"  action Function(_dbg_set_rel, _nid, 15) text_size 14
                            textbutton "Rel 40" action Function(_dbg_set_rel, _nid, 40) text_size 14
                            textbutton "Rel 80" action Function(_dbg_set_rel, _nid, 80) text_size 14
                            textbutton "Talk →" action [SetVariable("_dbg_talk_npc", _nid), Hide("debug_menu"), Jump("debug_talk")] text_size 14 text_color "#ffd66a"

                    null height 10
                    textbutton "▶  Character size viewer" action [Hide("debug_menu"), Show("debug_char_viewer")] text_size 18 text_color "#7fd06a"


# ── Talk-to-anyone (from debug) ───────────────────────────────────────────
label debug_talk:
    python:
        _n = store._dbg_talk_npc
        setattr(store, _n + "_met", True)
        mark_npc_encountered(_n)
        if npc_aff(_n) <= 0:
            setattr(store, NPC_DATA[_n]["aff"], 5)   # past the cold-approach gate
    scene black
    show screen hud
    call npc_interact(_dbg_talk_npc)
    jump map


# ── Character-size viewer ─────────────────────────────────────────────────
# All sprites side by side at their real relative display scale (women 0.87,
# men 1.0). Eyeball them, then tell me e.g. "make Nora 10% smaller".
screen debug_char_viewer():
    modal True
    zorder 250
    add "#0d1014fa"
    vbox:
        xpos 30
        ypos 20
        spacing 8
        hbox:
            spacing 20
            text "CHARACTER SIZES — relative (feet-aligned)" font PROFILE_FONT size 24 color "#ffdd44" yalign 0.5
            textbutton "← Back" action [Hide("debug_char_viewer"), Show("debug_menu")] text_size 18 text_color "#9fb6d6"
            textbutton "✕ Close" action Hide("debug_char_viewer") text_size 18 text_color "#9fb6d6"
        viewport:
            scrollbars "horizontal"
            mousewheel True
            draggable True
            xsize 1860
            ysize 900
            hbox:
                spacing 10
                for _nid in _DBG_NPCS:
                    $ _spr = NPC_DATA[_nid]["sprite"]
                    $ _sc  = sprite_display_scale(_nid)
                    vbox:
                        spacing 2
                        # feet-aligned box; height scales with the character's display scale
                        fixed:
                            xysize (230, 820)
                            add Solid("#181c22") xysize (230, 820)
                            add _spr:
                                fit "contain"
                                xysize (230, int(800 * _sc))
                                xalign 0.5
                                yalign 1.0
                        text ("%s  x%.2f" % (NPC_DATA[_nid]["name"], _sc)) font ACT_FONT size 15 color "#cfe0f5" xalign 0.5
