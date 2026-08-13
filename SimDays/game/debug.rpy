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

    def _dbg_skill_balance_report():
        lines = []
        for key in PRO_SKILLS:
            lvl  = skill_val(key)
            xp   = store.skill_exp.get(key, 0)
            need = skill_exp_needed(lvl)
            gated_info = ""
            if lvl < 10:
                next_gated = next((l for l in sorted(_GATED_LEVELS) if l > lvl), None)
                if next_gated:
                    done = skill_gate_completed(key, next_gated)
                    gated_info = "  gate@%d:%s" % (next_gated, "OPEN" if done else "LOCKED")
            lines.append("%s Lv%d  %d/%d XP%s" % (key.upper(), lvl, xp, need, gated_info))
        lines.append("---")
        for cid in store.active_careers:
            c = _migrate_career_entry(store.active_careers[cid])
            promote_ok = can_promote(cid)
            req = _RANK_SHIFT_REQ[c["rank"]] if c["rank"] < len(_RANK_SHIFT_REQ) else 20
            lines.append("%s r%d perf%d shifts%d/%d %s" % (
                cid, c["rank"], c["perf"], c["rank_shifts"], req,
                "PROMOTE-READY" if promote_ok else ""))
        renpy.notify("  |  ".join(lines))

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
        _ac[cid] = {"rank": rank, "perf": 100, "rank_shifts": 99, "total_shifts": 99, "joined_day": store.day, "last_shift_day": -1}
        store.active_careers = _ac
        _sync_job(cid)
        renpy.notify("%s — rank %d" % (c["name"], rank + 1))

    def _dbg_add_money(amount):
        gain_money(amount)   # gain_money returns True; wrapper swallows it so Function() doesn't end the interaction

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

    def _dbg_expire_states():
        store.player_states = []
        renpy.notify("Player states cleared")

    def _dbg_gen_city_events():
        generate_city_events_for_week(store.day // 7)
        renpy.notify("City events generated for week %d" % (store.day // 7))

    def _dbg_add_test_invitation():
        inv = {
            "id": "dbg_marcus_01_%d" % store.day,
            "template_id": "marcus_static_01",
            "npc_id": "marcus",
            "location": "location_bar",
            "day": store.day,
            "start_hour": 21,
            "end_hour": 23,
            "title": "Marcus: Grab a drink at the bar",
            "status": "pending",
        }
        store.active_npc_invitations = list(store.active_npc_invitations) + [inv]
        renpy.notify("Test invitation added")

    def _dbg_show_clients():
        count = len(store.client_profiles)
        names = ", ".join(store.client_profiles.keys()) if count else "none"
        renpy.notify("Client profiles (%d): %s" % (count, names))

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
                        textbutton "+$1,000"  action Function(_dbg_add_money, 1000)  text_size 16
                        textbutton "+$10,000" action Function(_dbg_add_money, 10000) text_size 16
                        textbutton "Clear loan" action SetVariable("loan", 0) text_size 16
                        textbutton "Refill needs" action Function(_dbg_refill) text_size 16

                    null height 6
                    text "COMPUTER OS" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "Open Desktop" action [Hide("debug_menu"), Function(renpy.call_in_new_context, "computer_desktop_session")] text_size 16
                        textbutton "Badge counts" action Function(debug_print_badges) text_size 16
                        text ("visual tier %d" % computer_visual_tier()) font ACT_FONT size 15 color "#8ea4bc" yalign 0.5

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

                    null height 6
                    text "SKILL BALANCE" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "Skill/Gate report" action Function(_dbg_skill_balance_report) text_size 16 text_color "#ffd66a"
                        textbutton "Clear gates" action [SetVariable("skill_gates_completed", {}), Notify("Gates cleared")] text_size 16
                        textbutton "Clear courses" action [SetVariable("completed_courses", []), Notify("Courses cleared")] text_size 16
                        textbutton "Reset DR" action [SetVariable("daily_activity_load", {}), Notify("Daily DR reset")] text_size 16

                    null height 4
                    textbutton "▶  Balance report" action [Hide("debug_menu"), Show("debug_balance_scr")] text_size 18 text_color "#ffd66a"

                    null height 10
                    text "PHASE 57-59 SYSTEMS" font PROFILE_FONT size 16 color "#5bcafa"
                    hbox:
                        spacing 8
                        textbutton "Focused state" action Function(_add_player_state_wrapper, "focused", "debug") text_size 15
                        textbutton "Stressed state" action Function(_add_player_state_wrapper, "stressed", "debug") text_size 15
                        textbutton "Expire states" action Function(_dbg_expire_states) text_size 15
                    hbox:
                        spacing 8
                        textbutton "Gen city events" action Function(_dbg_gen_city_events) text_size 15
                        textbutton "Test invitation" action Function(_dbg_add_test_invitation) text_size 15
                        textbutton "Client profiles" action Function(_dbg_show_clients) text_size 15
                        textbutton "Unlock gallery" action Function(unlock_location, "future_gallery", "debug") text_size 15

                    null height 10
                    textbutton "▶  Scene Tester (launch authored scenes)" action [Hide("debug_menu"), Show("debug_scene_tester")] text_size 18 text_color "#ffd66a"

                    null height 10
                    textbutton "▶  NPC Schedules" action [Hide("debug_menu"), Show("debug_schedule_scr")] text_size 18 text_color "#7fd06a"

                    null height 10
                    textbutton "▶  Character size viewer" action [Hide("debug_menu"), Show("debug_char_viewer")] text_size 18 text_color "#7fd06a"

                    null height 10
                    textbutton "▶  Phase 61 (cooking / mechanics / market)" action [Hide("debug_menu"), Show("debug_p61_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 62 (home / items / wardrobe)" action [Hide("debug_menu"), Show("debug_p62_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 64 self-check (balance assertions)" action [Hide("debug_menu"), Show("debug_p64_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 65 (capabilities / painting)" action [Hide("debug_menu"), Show("debug_p65_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 69 (possessions / bests)" action [Hide("debug_menu"), Show("debug_p69_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 66 (relationship depth)" action [Hide("debug_menu"), Show("debug_p66_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 67 (world pulse / ambient)" action [Hide("debug_menu"), Show("debug_p67_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Phase 68 (NPC initiative / lives)" action [Hide("debug_menu"), Show("debug_p68_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Rare outcomes (variance / cooldowns)" action [Hide("debug_menu"), Show("debug_rare_scr")] text_size 18 text_color "#7fd06a"
                    textbutton "▶  Downtown Summer Festival" action [Hide("debug_menu"), Show("debug_sf_scr")] text_size 18 text_color "#7fd06a"


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
# Shares the tuning data with in-game presentation: same sprite_display_scale /
# sprite_display_y_offset, and the same image names (so image-level crops like
# SPRITE_CROP_LEFT come along). It cannot reuse the sprite_crop transform itself —
# that one places sprites at absolute screen coords (xpos 1176, 660x900 box), which
# would land outside these 230x820 thumbnail cells.
# ponytail: yfix is applied here in thumbnail pixels, not game pixels (the cell is
# ~1/4 scale), so a y-offset looks ~4x stronger here than in game. Fine for judging
# relative sizes, don't tune offsets by eye from this screen.
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
                    $ _yfix = sprite_display_y_offset(_nid)
                    vbox:
                        spacing 2
                        fixed:
                            xysize (230, 820)
                            add Solid("#181c22") xysize (230, 820)
                            add _spr:
                                fit "contain"
                                xysize (230, 800)
                                zoom _sc
                                xalign 0.5
                                yalign 1.0
                                yoffset _yfix
                        text ("%s  x%.2f" % (NPC_DATA[_nid]["name"], _sc)) font ACT_FONT size 15 color "#cfe0f5" xalign 0.5
