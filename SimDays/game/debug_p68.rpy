# Phase 68 debug — NPC initiative, personal lives, follow-ups, facts, identity.
# tests/phase68_selfcheck.py is the authoritative runnable check.

default _p68_npc = "nora"

init python:

    def _p68_force_initiative():
        store._initiative_evaluated_day = -1
        store.npc_initiative_last_global_day = -1
        store._p68_contact_day = -1
        evaluate_npc_initiatives(store.day)
        renpy.notify("Initiative pass forced")

    def _p68_set_life(npc_id, state):
        life = dict(store._npc_personal_life)
        if state is None:
            life.pop(npc_id, None)
        else:
            lo, hi = NPC_PERSONAL_LIFE_STATES[state]["duration_range"]
            life[npc_id] = {"state": state, "started_day": store.day,
                            "expires_day": store.day + hi}
        store._npc_personal_life = life
        renpy.notify("%s -> %s" % (npc_id, state or "normal"))

    def _p68_enqueue_test_followup(npc_id):
        fid = enqueue_followup(npc_id, "comment", "debug_%d" % store.day,
                               "generic_comment", delay_min=0, delay_max=3, priority=9)
        renpy.notify("Queued %s" % (fid or "nothing (duplicate)"))

    def _p68_clear_cooldowns():
        store._npc_initiative_cooldowns = {}
        store._npc_cancel_last_day = {}
        store._failure_content_last = {}
        store._followup_last_day = -1
        store._initiative_evaluated_day = -1
        store.npc_initiative_last_global_day = -1
        store._p68_contact_day = -1
        renpy.notify("Phase 68 cooldowns cleared")

    def _p68_publish(fact_type):
        publish_player_fact(fact_type, "debug%d" % store.day)
        renpy.notify("Published %s (propagates tomorrow)" % fact_type)

    def _p68_propagate_now():
        for fid, f in list(store.public_player_facts.items()):
            if not f.get("done"):
                facts = dict(store.public_player_facts)
                facts[fid] = dict(f, day=f["day"] - 5)
                store.public_player_facts = facts
        propagate_public_facts(store.day)
        renpy.notify("Facts propagated")

    def _p68_identity_line(key):
        rule = PLAYER_IDENTITY_RULES[key]
        try:
            met = bool(rule["condition"]())
        except Exception:
            met = False
        return "%-14s %-4s %s" % (key, "ON" if store._player_identity_flags.get(key) else "off",
                                  "condition met" if met else "condition not met")


screen debug_p68_scr():
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
            text "PHASE 68 — NPC INITIATIVE & PERSONAL LIVES" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text ("daily contact budget: %s" %
                  ("SPENT" if _initiative_budget_spent() else "available")) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            null height 4
            viewport:
                xfill True
                ysize 540
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True

                    text "PERSONAL LIFE STATES" font PROFILE_FONT size 13 color "#ffd66a"
                    for _n in sorted(NPC_PERSONAL_LIFE_WEIGHTS):
                        $ _pl = npc_personal_life(_n)
                        hbox:
                            spacing 8
                            xfill True
                            text ("%-10s %-18s %s" % (
                                    NPC_DATA[_n]["name"],
                                    _pl["state"] if _pl else "-",
                                    ("expires d%d" % _pl["expires_day"]) if _pl else "")) font ACT_FONT size 11 color ("#5bcafa" if _pl else "#7a9ab8") yalign 0.5
                            textbutton "clear" action Function(_p68_set_life, _n, None) text_size 10
                            for _st in ("busy_work", "stressed_week", "social_week", "creative_project"):
                                textbutton _st[:6] action Function(_p68_set_life, _n, _st) text_size 10

                    null height 6
                    text "INITIATIVE COOLDOWNS" font PROFILE_FONT size 13 color "#ffd66a"
                    for _n in sorted(NPC_PERSONAL_LIFE_WEIGHTS):
                        $ _lastc = _npc_initiative_cooldowns.get(_n, -999)
                        $ _lastx = npc_initiative_last_day.get(_n, -999)
                        text ("%-10s p68 last d%s   ·   legacy last d%s   ·   init mult %.1f"
                              % (_n, _lastc if _lastc > -900 else "-",
                                 _lastx if _lastx > -900 else "-",
                                 npc_initiative_modifier(_n))) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "FOLLOW-UP QUEUE" font PROFILE_FONT size 13 color "#ffd66a"
                    if _followup_queue:
                        for _f in _followup_queue:
                            text ("%-22s %-9s p%d  d%d-%d  %s"
                                  % (_f["npc_id"] + "/" + _f["trigger_source"],
                                     _f["type"], _f["priority"],
                                     _f["eligible_from_day"], _f["eligible_until_day"],
                                     "DONE" if _f["completed"] else "pending")) font ACT_FONT size 11 color ("#7a9ab8" if _f["completed"] else "#8fe0a0")
                    else:
                        text "empty" font ACT_FONT size 11 color "#7a9ab8"
                    text ("last delivery: day %s" % (_followup_last_day if _followup_last_day >= 0 else "never")) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "PUBLIC FACTS" font PROFILE_FONT size 13 color "#ffd66a"
                    if public_player_facts:
                        for _fid in sorted(public_player_facts):
                            $ _pf = public_player_facts[_fid]
                            text ("%-34s d%d  %s  -> %s"
                                  % (_fid, _pf["day"],
                                     "propagated" if _pf.get("done") else "pending",
                                     ", ".join(_pf["propagated_to"]) or "nobody")) font ACT_FONT size 11 color "#7a9ab8"
                    else:
                        text "none" font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "PLAYER IDENTITY" font PROFILE_FONT size 13 color "#ffd66a"
                    for _k in sorted(PLAYER_IDENTITY_RULES):
                        text _p68_identity_line(_k) font ACT_FONT size 11 color ("#8fe0a0" if _player_identity_flags.get(_k) else "#7a9ab8")
                    text ("nights active: %d   ·   kept commitments: %d   ·   missed: %d"
                          % (_nights_active, _kept_commitments(), _missed_commitments())) font ACT_FONT size 11 color "#7a9ab8"

                    null height 8
                    text "ACTIONS" font PROFILE_FONT size 13 color "#ffd66a"
                    hbox:
                        spacing 8
                        box_wrap True
                        textbutton "Force initiative pass" action Function(_p68_force_initiative) text_size 12
                        textbutton "Clear all cooldowns" action Function(_p68_clear_cooldowns) text_size 12
                        textbutton "Propagate facts now" action Function(_p68_propagate_now) text_size 12
                        textbutton "Update identity" action Function(update_player_identity, day) text_size 12
                    hbox:
                        spacing 8
                        box_wrap True
                        for _ft in sorted(PUBLIC_FACT_TEMPLATES):
                            textbutton "publish " + _ft action Function(_p68_publish, _ft) text_size 11
                    hbox:
                        spacing 8
                        box_wrap True
                        for _tr in sorted(FAILURE_CONTENT):
                            textbutton "fail " + _tr action Function(trigger_failure_content, _tr) text_size 11
                    hbox:
                        spacing 8
                        box_wrap True
                        for _n in sorted(NPC_PERSONAL_LIFE_WEIGHTS):
                            textbutton "fu " + _n action Function(_p68_enqueue_test_followup, _n) text_size 11

            null height 4
            textbutton "Close" action [Hide("debug_p68_scr"), Show("debug_menu")] xalign 0.5 text_size 16 text_color "#9fb6d6"
