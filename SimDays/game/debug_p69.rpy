# Phase 69 debug + self-check. Reachable from the debug menu ("Phase 69").
#
# The assertions mirror tests/phase69_selfcheck.py, which is the authoritative
# runnable check. What this screen adds is LIVE state: what you own, what your
# bests are, which first-win keepsakes are still open, and the EV/hour of every
# city challenge computed against your actual skills and preparation.

init python:

    def _p69_selfcheck():
        """Returns (ok, [(status, label, detail)]). Mutates no game state."""
        out, fails = [], []

        def chk(label, cond, detail=""):
            out.append(("PASS" if cond else "FAIL", label, detail))
            if not cond:
                fails.append(label)

        # ── Catalog integrity ───────────────────────────────────────────────
        chk("catalog has 12+ entries", len(POSSESSION_CATALOG) >= 12,
            "%d items" % len(POSSESSION_CATALOG))
        chk("every entry has a category and a name",
            all(d.get("name") and d.get("category") for d in POSSESSION_CATALOG.values()))
        chk("every icon_key resolves in POSSESSION_ICONS",
            all(d.get("icon_key") in POSSESSION_ICONS for d in POSSESSION_CATALOG.values()))
        chk("sellable items carry a value",
            all(d.get("sell_value", 0) > 0 for d in POSSESSION_CATALOG.values()
                if d.get("sellable")))
        chk("keepsakes are not sellable",
            all(not d.get("sellable") for d in POSSESSION_CATALOG.values()
                if d["category"] == "keepsake"))
        chk("every unearned entry tells you how to earn it",
            all(d.get("hint") for d in POSSESSION_CATALOG.values()))
        chk("possession_icon never raises on a missing asset",
            possession_icon("keepsake_trophy") in (None, POSSESSION_ICONS["keepsake_trophy"],
                                                   POSSESSION_ICONS["_fallback"]))

        # ── Every keepsake has at least one grant path ──────────────────────
        _wired = set(CITY_CHALLENGE_KEEPSAKES.values())
        _wired |= set(WORLD_CHALLENGE_KEEPSAKES.values())
        _wired |= set(BAR_FIRST_WIN_KEEPSAKES.values())
        _wired |= {"promotion_certificate", "first_paid_gig_stub", "freelance_client_card",
                   "mechanics_restoration_badge", "festival_wristband",
                   "art_market_vendor_card", "rare_vintage_coin"}
        _orphans = [i for i in POSSESSION_CATALOG if i not in _wired]
        chk("every catalog item is reachable in play", not _orphans, ", ".join(_orphans))
        chk("keepsake targets all exist in the catalog",
            all(k in POSSESSION_CATALOG for k in _wired))

        # ── Wiring is live (the init-20 wrappers actually replaced the names) ─
        _missed = []
        for _fn in ("resolve_city_challenge", "attempt_world_challenge", "promote",
                    "open_mic_resolve", "busking_resolve", "new_artwork",
                    "mech_attempt_repair", "do_catering", "gain_skill_practice",
                    "new_day", "_city_chal_mods", "_city_challenge_lines"):
            _orig = getattr(store, "_p69_orig_" + _fn.lstrip("_"), None)
            if _orig is None or getattr(store, _fn, None) is _orig:
                _missed.append(_fn)
        chk("all 12 wrappers installed", not _missed, ", ".join(_missed) or "ok")
        chk("preparation reaches the shared modifier list",
            (store.need_energy < 70)
            or ("Rested" in [l for l, _v in _city_chal_mods(None)]),
            "energy %d" % store.need_energy)

        # ── Personal-best comparison logic ──────────────────────────────────
        chk("tier order is the Phase 60 order",
            _PB_TIER_ORDER == ["critical_failure", "weak", "success", "great", "critical"])
        chk("rating order runs D..S", _PB_RATING_ORDER == ["D", "C", "B", "A", "S"])
        chk("unknown tier strings are ignored, not crashed on",
            _pb_better("nonsense", "success", "tier") is False)

        # ── Economy: EV/hour of every city challenge, with full preparation ──
        for row in _p69_ev_table():
            chk("EV/h under $40: " + row[0], row[2] < 40.0, "$%.1f/h" % row[2])

        return (not fails), out

    def _p69_ev_table():
        """Expected $/hour for every city challenge at its recommended skill,
        WITH the Phase 69 preparation bonuses applied (worst case for balance).
        Recomputed live so a template change shows up here immediately."""
        rows = []
        tiers = ["critical_failure", "weak", "success", "great", "critical"]
        prep = sum(PREPARATION_BONUSES.values())
        for t in CITY_CHALLENGE_TEMPLATES:
            ch = t["challenge"]
            mods = [("Prepared", 5), ("Preparation", prep)]
            if t["id"] == "art_exhibition":
                mods.append(("Submitted piece", 10))
            dist = calculate_check_chance("ev_" + t["id"], ch["recommended"],
                                          ch["difficulty"], mods,
                                          include_pity=False)["distribution"]
            ev = sum((dist[k] / 100.0) * ch["outcomes"][k].get("money", 0) for k in tiers)
            ev -= ch.get("entry", 0)
            rows.append((t["title"], ev, ev / float(t["duration"])))
        return rows

    # ── Debug actions. Every Function() wrapper returns None. ───────────────
    def _p69_grant(item_id):
        grant_possession(item_id, "debug_day%d" % store.day, force=True)

    def _p69_remove(instance_id):
        store.player_possessions = [p for p in store.player_possessions
                                    if p["id"] != instance_id]
        if store._selected_possession == instance_id:
            store._selected_possession = None

    def _p69_toggle_featured(instance_id):
        p = possession_by_id(instance_id)
        if p:
            feature_possession(instance_id, not p.get("featured"))

    def _p69_reset_first_win(item_id):
        """Remove every instance of a keepsake so its first-win path can be
        re-tested without starting a new save."""
        store.player_possessions = [p for p in store.player_possessions
                                    if p["item_id"] != item_id]

    def _p69_clear_all():
        store.player_possessions = []
        store.player_personal_bests = {}
        store.player_accomplishments = []

    def _p69_grant_all():
        for iid in POSSESSION_CATALOG:
            grant_possession(iid, "debug_all")

    def _p69_schedule_challenge(template_id):
        """Put a city challenge on today's schedule, right now, so the whole
        anticipate -> prepare -> attempt -> keepsake loop can be walked."""
        tmpl = city_event_template(template_id)
        if not tmpl:
            return
        eid = "city_%s_debug%d" % (template_id, store.day)
        if any(e["id"] == eid for e in store.city_event_schedule):
            return
        store.city_event_schedule = list(store.city_event_schedule) + [{
            "id": eid, "template_id": template_id, "title": tmpl["title"],
            "category": tmpl["category"], "location": tmpl["location"],
            "day": store.day, "hour": int(store.hour), "duration": tmpl["duration"],
            "desc": tmpl["desc"], "req": {}, "rewards": tmpl.get("rewards", {}),
            "status": "announced", "saved_to_calendar": True,
            "attended": False, "result": None,
        }]

    def _p69_complete_challenge(template_id, tier):
        """Fast-forward: grant exactly what placing at `tier` would grant,
        without the roll. Does not touch the schedule."""
        record_personal_best("best_city_challenge_finish", tier, "tier")
        if tier in _PLACED_TIERS:
            ks = CITY_CHALLENGE_KEEPSAKES.get(template_id)
            if ks:
                grant_possession(ks, "debug_citychal_" + template_id)
            record_accomplishment("debug_%s_%s" % (template_id, tier),
                                  city_event_template(template_id).get("title", template_id),
                                  "Debug-granted %s." % tier,
                                  city_event_template(template_id).get("category", "general"))

    def _p69_run_sync():
        p69_sync_derived()

    def _p69_first_win_status():
        """[(item_id, name, owned_bool, source_label)] for every first-win keepsake."""
        rows = []
        for tid, ks in sorted(CITY_CHALLENGE_KEEPSAKES.items()):
            rows.append((ks, possession_name(ks), has_possession(ks), "city:" + tid))
        for cid, ks in sorted(WORLD_CHALLENGE_KEEPSAKES.items()):
            rows.append((ks, possession_name(ks), has_possession(ks), "world:" + cid))
        return rows


screen debug_p69_scr():
    modal True
    zorder 210
    add "#000000e0"
    $ _p69_ok, _p69_rows = _p69_selfcheck()
    frame:
        xalign 0.5 yalign 0.5
        xsize 900
        ysize 680
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "PHASE 69 — POSSESSIONS / BESTS / ANTICIPATION" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text ("ALL PASS" if _p69_ok else "FAILURES PRESENT") font PROFILE_FONT size 15 xalign 0.5 color ("#7fd06a" if _p69_ok else "#e05050")
            null height 4
            viewport:
                xfill True
                ysize 520
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True

                    for _st, _lbl, _dt in _p69_rows:
                        hbox:
                            spacing 8
                            xfill True
                            text _st font PROFILE_FONT size 12 color ("#7fd06a" if _st == "PASS" else "#e05050") yalign 0.5
                            text _lbl font ACT_FONT size 12 color "#cfe0f5" yalign 0.5
                            text _dt font ACT_FONT size 11 color "#7a9ab8" yalign 0.5 xalign 1.0

                    # ── Economy ────────────────────────────────────────────
                    null height 8
                    text "CITY CHALLENGE EV (recommended skill, fully prepared)" font PROFILE_FONT size 13 color "#ffd66a"
                    for _t, _ev, _evh in _p69_ev_table():
                        hbox:
                            xfill True
                            text _t font ACT_FONT size 12 color "#cfe0f5"
                            text ("$%.0f  ·  $%.1f/h" % (_ev, _evh)) font ACT_FONT size 12 color ("#7fd06a" if _evh < 40 else "#e05050") xalign 1.0

                    # ── Preparation ────────────────────────────────────────
                    null height 8
                    text "PREPARATION (live)" font PROFILE_FONT size 13 color "#ffd66a"
                    text ("energy %d  ·  rested bonus %s" % (need_energy, "ACTIVE" if need_energy >= 70 else "inactive")):
                        font ACT_FONT size 12 color "#cfe0f5"
                    text ("practised recently: %s" % (", ".join(sorted(k for k in _p69_last_practice
                                                                       if prep_practiced_recently(k))) or "nothing")):
                        font ACT_FONT size 12 color "#cfe0f5"

                    # ── Possessions ────────────────────────────────────────
                    null height 8
                    text ("POSSESSIONS (%d)" % len(player_possessions)) font PROFILE_FONT size 13 color "#ffd66a"
                    if not player_possessions:
                        text "none" font ACT_FONT size 12 color "#7a9ab8"
                    for _p in player_possessions:
                        hbox:
                            spacing 6
                            xfill True
                            text ("[%s] %s (day %d)" % (_p["category"], possession_name(_p["item_id"]), _p["acquired_day"] + 1)):
                                font ACT_FONT size 12 color "#cfe0f5"
                            textbutton ("unfeature" if _p.get("featured") else "feature"):
                                action Function(_p69_toggle_featured, _p["id"])
                                background None padding (6, 0)
                                text_font ACT_FONT text_size 11 text_color "#5bcafa"
                            textbutton "remove":
                                action Function(_p69_remove, _p["id"])
                                background None padding (6, 0)
                                text_font ACT_FONT text_size 11 text_color "#e05050"

                    # ── First-win status ───────────────────────────────────
                    null height 8
                    text "FIRST-WIN KEEPSAKES" font PROFILE_FONT size 13 color "#ffd66a"
                    for _ks, _name, _owned, _src in _p69_first_win_status():
                        hbox:
                            spacing 6
                            xfill True
                            text ("%s  ·  %s" % (_name, _src)) font ACT_FONT size 12 color ("#7fd06a" if _owned else "#7a9ab8")
                            if _owned:
                                textbutton "reset":
                                    action Function(_p69_reset_first_win, _ks)
                                    background None padding (6, 0)
                                    text_font ACT_FONT text_size 11 text_color "#e05050"
                            else:
                                textbutton "grant":
                                    action Function(_p69_grant, _ks)
                                    background None padding (6, 0)
                                    text_font ACT_FONT text_size 11 text_color "#5bcafa"

                    # ── Bests / accomplishments ────────────────────────────
                    null height 8
                    text "PERSONAL BESTS" font PROFILE_FONT size 13 color "#ffd66a"
                    if not player_personal_bests:
                        text "none" font ACT_FONT size 12 color "#7a9ab8"
                    for _k in sorted(player_personal_bests):
                        text ("%s = %s" % (_k, player_personal_bests[_k])) font ACT_FONT size 12 color "#cfe0f5"
                    null height 6
                    text ("ACCOMPLISHMENTS (%d)" % len(player_accomplishments)) font PROFILE_FONT size 13 color "#ffd66a"
                    for _a in player_accomplishments:
                        text ("[%s] %s — day %d" % (_a["category"], _a["title"], _a["day"] + 1)) font ACT_FONT size 12 color "#cfe0f5"

                    # ── Schedule a challenge today ─────────────────────────
                    null height 8
                    text "SCHEDULE A CHALLENGE TODAY" font PROFILE_FONT size 13 color "#ffd66a"
                    for _ct in CITY_CHALLENGE_TEMPLATES:
                        hbox:
                            spacing 6
                            xfill True
                            text _ct["title"] font ACT_FONT size 12 color "#cfe0f5"
                            textbutton "schedule":
                                action Function(_p69_schedule_challenge, _ct["id"])
                                background None padding (6, 0)
                                text_font ACT_FONT text_size 11 text_color "#5bcafa"
                            textbutton "win it":
                                action Function(_p69_complete_challenge, _ct["id"], "critical")
                                background None padding (6, 0)
                                text_font ACT_FONT text_size 11 text_color "#ffd66a"

            null height 6
            hbox:
                spacing 10
                xalign 0.5
                textbutton "Grant all" action Function(_p69_grant_all) text_font ACT_FONT text_size 13 text_color "#5bcafa" background "#1a2a3a" padding (12, 5)
                textbutton "Clear all" action Function(_p69_clear_all) text_font ACT_FONT text_size 13 text_color "#e05050" background "#1a2a3a" padding (12, 5)
                textbutton "Run derived sync" action Function(_p69_run_sync) text_font ACT_FONT text_size 13 text_color "#7fd06a" background "#1a2a3a" padding (12, 5)
                textbutton "Open app" action [Hide("debug_p69_scr"), Show("phone_possessions_scr")] text_font ACT_FONT text_size 13 text_color "#9fb6d6" background "#1a2a3a" padding (12, 5)
                textbutton "Back" action [Hide("debug_p69_scr"), Show("debug_menu")] text_font ACT_FONT text_size 13 text_color "#9fb6d6" background "#1a2a3a" padding (12, 5)
