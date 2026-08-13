# Phase 65 debug + self-check. Reachable from the debug menu ("Phase 65").
#
# The assertions mirror tests/phase65_selfcheck.py, which is the authoritative
# runnable check. What this screen adds is LIVE state inspection — capabilities,
# NPC interests, mastery, commission board, and the economy EV table computed
# against the player's actual gear and reputation.

init python:

    def _p65_selfcheck():
        """Returns (ok, [(status, label, detail)]). Mutates no game state."""
        out, fails = [], []

        def chk(label, cond, detail=""):
            out.append(("PASS" if cond else "FAIL", label, detail))
            if not cond:
                fails.append(label)

        # ── Capability layer ────────────────────────────────────────────────
        easels = capability_sources("painting")
        chk("more than one item grants 'painting'", len(easels) >= 2,
            ", ".join(easels))
        chk("every painting item also grants 'sketching'",
            all("sketching" in ITEM_CATALOG[i]["capabilities"] for i in easels))
        chk("capability index covers every catalog capability",
            all(c in _CAPABILITY_ITEMS
                for d in ITEM_CATALOG.values() for c in d["capabilities"]))
        # The gear bonus must survive int() — the Phase 64 proper_desk bug.
        _raw = ITEM_CATALOG["basic_easel"]["modifiers"]["art_quality_modifier"]
        chk("easel modifier survives conversion to roll points",
            int(round(_raw * 100)) > 0, "%.2f -> +%d" % (_raw, int(round(_raw * 100))))
        chk("old int(v*10) formula would have been zero", int(_raw * 10) == 0)

        # ── Economy ─────────────────────────────────────────────────────────
        chk("commission failure still pays something",
            min(_COMMISSION_PAY_MULT.values()) > 0)
        chk("market absorption is throttled", ART_MARKET_WEEKLY_SLOTS <= 2,
            "%d pieces/week" % ART_MARKET_WEEKLY_SLOTS)
        chk("saturating the market costs you", _ART_SATURATED_MULT < 0.5)
        chk("commission board is reputation-gated",
            ART_REP_GATES["commission_board"] >= 5)
        chk("gallery is reputation-gated", ART_REP_GATES["gallery_sale"] >= 10)
        for _row in _p65_ev_table():
            chk("EV/h under $40: " + _row[0], _row[2] < 40.0, "$%.1f/h" % _row[2])

        # ── Subjects / progression ──────────────────────────────────────────
        chk("harder subjects are worth more",
            all(ART_SUBJECTS[a]["value"] < ART_SUBJECTS[b]["value"]
                for a, b in (("still_life", "landscape"), ("landscape", "abstract"),
                             ("abstract", "portrait"))))
        chk("portfolio-piece difficulty stays in the 45-70 band",
            all(45 <= art_session_difficulty("portfolio_piece", s, a[0]) <= 70
                for s in ("landscape", "abstract", "portrait") for a in ART_AMBITION))
        chk("mastery is capped", PAINTING_MASTERY_CAP == 100)

        # ── NPC interests ───────────────────────────────────────────────────
        chk("all 9 audited NPCs carry interests", len(NPC_INTERESTS) == 9)
        chk("interest values stay in the audited -1..3 band",
            all(-1 <= v <= 3 for d in NPC_INTERESTS.values() for v in d.values()))

        return (not fails), out

    def _p65_ev_table():
        """Expected $/hour for each painting income path, computed against the
        LIVE gear and reputation so the player's own numbers are visible."""
        rows = []
        tiers = ["critical_failure", "weak", "success", "great", "critical"]

        def _sale_ev(skill, subject, session, channel):
            dist = calculate_check_chance(
                _art_check_id(session, subject), skill,
                art_session_difficulty(session, subject),
                _painting_mods(session, subject))["distribution"]
            hours = ART_SESSIONS[session]["hours"] + (1.0 if channel == "street" else 0.0)
            total = 0.0
            for t in tiers:
                lo, hi = _ART_VALUE_BASE[t]
                mid = (lo + hi) // 2
                scalar = ART_SUBJECTS[subject]["value"]
                val = int(min(500, mid * scalar * max(0.4, 1 + (skill - 3) * 0.15)))
                total += (dist[t] / 100.0) * art_sale_price(
                    {"estimated_value": val}, channel, preview=True)
            total -= art_material_cost(session)
            return total, total / hours

        for lbl, sk, subj, sess, ch in (
                ("Street, still life",   2, "still_life", "still_life", "street"),
                ("Street, portrait",     6, "portrait",   "canvas",     "street"),
                ("Gallery, portrait",    6, "portrait",   "canvas",     "gallery"),
                ("Gallery, portfolio",   8, "portrait",   "portfolio_piece", "gallery")):
            ev, evh = _sale_ev(sk, subj, sess, ch)
            rows.append(("%s (art %d)" % (lbl, sk), ev, evh))

        for t in PAINTING_COMMISSIONS:
            for sk in (4, 6, 8):
                if sk * 5 < t["art_rep_min"]:
                    continue
                dist = calculate_check_chance("comm_" + t["id"], sk, t["difficulty"],
                                              _painting_mods("canvas", t["subject"]))["distribution"]
                ev = sum((dist[k] / 100.0) * t["pay"] * _COMMISSION_PAY_MULT[k] for k in tiers)
                ev -= art_material_cost("canvas")
                rows.append(("Commission %s (art %d)" % (t["id"], sk), ev, ev / t["hours"]))
        return rows

    # ── Debug actions. Every Function() wrapper returns None. ───────────────
    def _p65_grant_artwork(tier):
        new_artwork("painting", "portrait", tier, max(1, skill_val("art")), 1.0)

    def _p65_set_art_rep(v):
        store.art_reputation = max(0, min(100, v))

    def _p65_grant_gear(item_id):
        grant_item(item_id)
        if ITEM_CATALOG[item_id]["slot"]:
            equip_item(item_id)

    def _p65_clear_art_gear():
        hs = dict(store.home_slots)
        hs["studio"] = {}
        store.home_slots = hs

    def _p65_force_commission():
        t = painting_commission_offer() or PAINTING_COMMISSIONS[0]
        if not active_painting_commission():
            accept_painting_commission(t)

    def _p65_trigger_art_event():
        """Schedule a Local Art Exhibition today so the flow can be exercised."""
        tmpl = city_event_template("art_exhibition")
        if not tmpl:
            return
        store.city_event_schedule = list(store.city_event_schedule) + [{
            "id": "art_exhibition_debug_%d" % store.day,
            "template_id": "art_exhibition", "title": tmpl["title"],
            "desc": tmpl["desc"], "location": tmpl["location"],
            "day": store.day, "hour": int(store.hour), "duration": tmpl["duration"],
            "req": tmpl["req"], "rewards": tmpl["rewards"],
            "status": "announced", "attended": False,
        }]

    def _p65_commission_board_state():
        c = active_painting_commission()
        if c:
            return "ACTIVE: %s, due day %d (%d days left)" % (
                c["client"], c["deadline_day"] + 1, c["deadline_day"] - store.day)
        o = painting_commission_offer()
        if o:
            return "OFFER: %s — $%d, %gh" % (o["client"], o["pay"], o["hours"])
        return "no offer (refresh in %d days, needs art_rep %d)" % (
            days_until_commission_refresh(), ART_REP_GATES["commission_board"])


screen debug_p65_scr():
    modal True
    zorder 210
    add "#000000e0"
    $ _p65_ok, _p65_rows = _p65_selfcheck()
    frame:
        xalign 0.5 yalign 0.5
        xsize 860
        ysize 660
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "PHASE 65 — CAPABILITIES + PAINTING" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text ("ALL PASS" if _p65_ok else "FAILURES PRESENT") font PROFILE_FONT size 15 xalign 0.5 color ("#7fd06a" if _p65_ok else "#e05050")
            null height 4
            viewport:
                xfill True
                ysize 500
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True

                    # ── assertions ────────────────────────────────────────
                    for _st, _lbl, _dt in _p65_rows:
                        hbox:
                            spacing 8
                            xfill True
                            text _st font PROFILE_FONT size 12 color ("#7fd06a" if _st == "PASS" else "#e05050") yalign 0.5
                            text _lbl font ACT_FONT size 12 color "#cfe0f5" yalign 0.5
                            text _dt font ACT_FONT size 11 color "#7a9ab8" yalign 0.5 xalign 1.0

                    # ── live capability state ─────────────────────────────
                    null height 8
                    text "LIVE CAPABILITIES" font PROFILE_FONT size 13 color "#ffd66a"
                    $ _caps = home_capabilities()
                    text (", ".join(_caps) if _caps else "none active") font ACT_FONT size 12 color "#5bcafa"
                    text ("art station: %s   ·   gear bonus +%d   ·   supplies: %s"
                          % (equipped_in("studio", "art_station") or "empty",
                             art_gear_bonus(), has_art_supplies())) font ACT_FONT size 12 color "#7a9ab8"

                    # ── progression state ─────────────────────────────────
                    null height 8
                    text "ART STATE" font PROFILE_FONT size 13 color "#ffd66a"
                    text ("Art Lv %d   ·   reputation %d/100   ·   %d artworks   ·   %d commissions done"
                          % (skill_val("art"), art_reputation, len(player_artworks),
                             painting_commissions_done)) font ACT_FONT size 12 color "#7a9ab8"
                    text ("displayed %d   ·   portfolio %d   ·   sold %d   ·   gifted %d"
                          % (len(filtered_artworks("displayed")), len(filtered_artworks("portfolio")),
                             len(filtered_artworks("sold")), len(filtered_artworks("gifted")))) font ACT_FONT size 12 color "#7a9ab8"
                    text ("market slots used this week: %d / %d"
                          % (art_sales_this_week("gallery"), ART_MARKET_WEEKLY_SLOTS)) font ACT_FONT size 12 color "#7a9ab8"
                    text ("commission board: " + _p65_commission_board_state()) font ACT_FONT size 12 color "#7a9ab8"

                    # ── mastery ───────────────────────────────────────────
                    null height 8
                    text "SUBJECT MASTERY" font PROFILE_FONT size 13 color "#ffd66a"
                    for _sj in ART_SUBJECTS:
                        hbox:
                            spacing 8
                            xfill True
                            text ART_SUBJECTS[_sj]["name"] font ACT_FONT size 12 color "#cfe0f5"
                            text ("%d pts  ->  +%d roll   (difficulty %d, value x%.2f)"
                                  % (painting_mastery_points(_sj), painting_mastery_mod(_sj),
                                     ART_SUBJECTS[_sj]["difficulty"], ART_SUBJECTS[_sj]["value"])) font ACT_FONT size 11 color "#7a9ab8" xalign 1.0

                    # ── artwork inventory ─────────────────────────────────
                    null height 8
                    text "ARTWORKS" font PROFILE_FONT size 13 color "#ffd66a"
                    if not player_artworks:
                        text "none" font ACT_FONT size 12 color "#4a6080"
                    for _a in list(reversed(player_artworks))[:12]:
                        hbox:
                            spacing 8
                            xfill True
                            text ("%s  %s" % (_a["id"], _a["subject"])) font ACT_FONT size 11 color "#cfe0f5"
                            text ("%s  $%d  %s%s%s%s%s"
                                  % (art_quality_label(_a["quality"]), _a["estimated_value"],
                                     "wall " if _a["displayed"] else "",
                                     "folio " if _a["in_portfolio"] else "",
                                     "sold " if _a["sold"] else "",
                                     ("gift:" + str(_a["gifted_to"]) + " ") if _a["gifted_to"] else "",
                                     "entered" if _a["submitted_to"] else "")) font ACT_FONT size 11 color "#7a9ab8" xalign 1.0

                    # ── NPC interests ─────────────────────────────────────
                    null height 8
                    text "NPC INTERESTS  (art / music / fit / prog / cook / mech)" font PROFILE_FONT size 13 color "#ffd66a"
                    for _n in NPC_INTERESTS:
                        hbox:
                            spacing 8
                            xfill True
                            text NPC_DATA.get(_n, {}).get("name", _n) font ACT_FONT size 12 color ("#c08ae0" if npc_interest(_n, "art") >= 2 else "#cfe0f5")
                            text ("%2d  %2d  %2d  %2d  %2d  %2d"
                                  % (npc_interest(_n, "art"), npc_interest(_n, "music"),
                                     npc_interest(_n, "fitness"), npc_interest(_n, "programming"),
                                     npc_interest(_n, "cooking"), npc_interest(_n, "mechanics"))) font ACT_FONT size 11 color "#7a9ab8" xalign 1.0

                    # ── EV table ──────────────────────────────────────────
                    null height 8
                    text "ECONOMY — EV PER PATH (live gear and reputation)" font PROFILE_FONT size 13 color "#ffd66a"
                    for _lbl, _ev, _evh in _p65_ev_table():
                        hbox:
                            spacing 8
                            xfill True
                            text _lbl font ACT_FONT size 11 color "#cfe0f5"
                            text ("$%.0f/session   $%.1f/h" % (_ev, _evh)) font ACT_FONT size 11 color ("#e05050" if _evh >= 40 else "#7fd06a") xalign 1.0

            # ── actions ───────────────────────────────────────────────────
            null height 4
            hbox:
                spacing 6
                xalign 0.5
                for _q in ("weak", "success", "great", "critical"):
                    textbutton ("+" + art_quality_label(_q)) action Function(_p65_grant_artwork, _q) text_font ACT_FONT text_size 12 text_color "#7fd06a"
            hbox:
                spacing 6
                xalign 0.5
                textbutton "Basic easel" action Function(_p65_grant_gear, "basic_easel") text_font ACT_FONT text_size 12 text_color "#5bcafa"
                textbutton "Studio easel" action Function(_p65_grant_gear, "studio_easel") text_font ACT_FONT text_size 12 text_color "#5bcafa"
                textbutton "Supplies" action Function(_p65_grant_gear, "art_supply_kit") text_font ACT_FONT text_size 12 text_color "#5bcafa"
                textbutton "Sketchbook" action Function(_p65_grant_gear, "sketchbook") text_font ACT_FONT text_size 12 text_color "#5bcafa"
                textbutton "Clear station" action Function(_p65_clear_art_gear) text_font ACT_FONT text_size 12 text_color "#cc9040"
            hbox:
                spacing 6
                xalign 0.5
                for _r in (0, 5, 8, 10, 25, 60):
                    textbutton ("rep %d" % _r) action Function(_p65_set_art_rep, _r) text_font ACT_FONT text_size 12 text_color "#c08ae0"
                textbutton "Force commission" action Function(_p65_force_commission) text_font ACT_FONT text_size 12 text_color "#ffd66a"
                textbutton "Schedule exhibition" action Function(_p65_trigger_art_event) text_font ACT_FONT text_size 12 text_color "#ffd66a"
            null height 4
            textbutton "Back" action [Hide("debug_p65_scr"), Show("debug_menu")] xalign 0.5 text_font ACT_FONT text_size 18 text_color "#9fb6d6" text_hover_color "#ffffff"
