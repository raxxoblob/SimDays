default _challenge_prepped = -1   # day the player bought event-prep supplies

# Phase 61 — City skill challenges.
# EXTENDS the existing city-event system (city_events.rpy) — no new generator.
# We append challenge templates to CITY_EVENT_TEMPLATES (so the existing weekly
# generator schedules them) and add a "challenge" spec the attend flow resolves
# with the Phase 60 roll engine. Attendance stays one-shot (the event's attended
# flag), location+time gated exactly like every other city event.
#
# init priority 1 so this runs AFTER city_events.rpy's default-priority init
# (CITY_EVENT_TEMPLATES must already exist).

init 1 python:

    # tier -> outcome. Rewards favour XP / reputation / portfolio; cash is modest.
    def _chal_outcomes(base_xp, rep_hi, cash_hi, portfolio_domain=None):
        return {
            "critical_failure": {"label": "No placement",   "xp": max(1, base_xp // 3)},
            "weak":             {"label": "Honourable mention", "xp": max(1, base_xp // 2)},
            "success":          {"label": "Third place",    "xp": base_xp, "rep": max(1, rep_hi // 3), "money": cash_hi // 3},
            "great":            {"label": "Second place",   "xp": int(base_xp * 1.2), "rep": max(1, rep_hi // 2), "money": cash_hi // 2},
            "critical":         {"label": "First place",    "xp": int(base_xp * 1.5), "rep": rep_hi, "money": cash_hi,
                                 "portfolio": portfolio_domain, "journal": True, "confidence": True},
        }

    CITY_CHALLENGE_TEMPLATES = [
        {"id": "cook_off", "title": "Local Cook-Off", "category": "culinary",
         "location": "location_park", "duration": 3, "hour": 12,
         "desc": "Amateur cooks compete at the park food fair.",
         "req": {}, "rewards": {}, "days": [5, 6],
         "challenge": {"skill": "cook", "recommended": 6, "difficulty": 62, "entry": 10,
                       "outcomes": _chal_outcomes(16, 4, 60, "culinary")}},
        {"id": "trivia_night", "title": "Pub Trivia Night", "category": "skill",
         "location": "location_bar", "duration": 2, "hour": 20,
         "desc": "Teams battle over general knowledge at Static.",
         "req": {}, "rewards": {}, "days": [2, 3],
         "challenge": {"skill": "biz", "recommended": 4, "difficulty": 55, "entry": 5,
                       "outcomes": _chal_outcomes(10, 3, 45)}},
        {"id": "fitness_challenge", "title": "Amateur Fitness Challenge", "category": "fitness",
         "location": "location_gym", "duration": 3, "hour": 10,
         "desc": "A timed circuit throwdown at Iron Gate.",
         "req": {}, "rewards": {}, "days": [5, 6],
         "challenge": {"skill": "fit", "recommended": 5, "difficulty": 60, "entry": 0,
                       "outcomes": _chal_outcomes(14, 4, 50)}},
        {"id": "art_challenge", "title": "Live Art Challenge", "category": "art",
         "location": "location_park", "duration": 3, "hour": 13,
         "desc": "Artists work to a theme, judged on the spot.",
         "req": {}, "rewards": {}, "days": [5, 6],
         "challenge": {"skill": "art", "recommended": 5, "difficulty": 60, "entry": 0,
                       "outcomes": _chal_outcomes(14, 3, 45, "art")}},
        {"id": "coding_workshop", "title": "Public Coding Challenge", "category": "skill",
         "location": "location_library", "duration": 2, "hour": 14,
         "desc": "A timed algorithm contest at the library.",
         "req": {}, "rewards": {}, "days": [1, 2, 3],
         "challenge": {"skill": "prog", "recommended": 5, "difficulty": 62, "entry": 0,
                       "outcomes": _chal_outcomes(14, 3, 40, "programming")}},
        {"id": "repair_workshop", "title": "Repair Café Contest", "category": "skill",
         "location": "location_library", "duration": 2, "hour": 11,
         "desc": "Volunteers race to fix donated gear the fastest.",
         "req": {}, "rewards": {}, "days": [4, 5],
         "challenge": {"skill": "mech", "recommended": 5, "difficulty": 60, "entry": 0,
                       "outcomes": _chal_outcomes(14, 3, 45)}},
        {"id": "music_showcase", "title": "Open Music Showcase", "category": "music",
         "location": "location_bar", "duration": 3, "hour": 20,
         "desc": "A judged performance slot at Static.",
         "req": {}, "rewards": {}, "days": [4, 5],
         "challenge": {"skill": "music", "recommended": 5, "difficulty": 60, "entry": 0,
                       "outcomes": _chal_outcomes(15, 4, 55)}},
        # Phase 65. Distinct from the existing "Live Art Challenge": that one is
        # made on the spot, this one judges a piece you painted at home and
        # entered in advance. Cash is deliberately modest — reputation and the
        # portfolio entry are the real prize.
        {"id": "art_exhibition", "title": "Local Art Exhibition", "category": "art",
         "location": "location_gallery", "duration": 3, "hour": 18,
         "desc": "A judged show of local work at the gallery.",
         "req": {"art_reputation": 8, "submitted_artwork": 1},
         "rewards": {}, "days": [4, 5, 6],
         "challenge": {"skill": "art", "recommended": 6, "difficulty": 64, "entry": 0,
                       "min_skill": 3, "cooldown_days": 14,
                       "outcomes": {
                           "critical_failure": {"label": "No placement",       "xp": 40,  "art_rep": 1},
                           "weak":             {"label": "Honourable mention", "xp": 60, "art_rep": 3},
                           "success":          {"label": "Third place",        "xp": 75, "art_rep": 5,  "money": 60,  "portfolio": "art"},
                           "great":            {"label": "Second place",       "xp": 90, "art_rep": 8,  "money": 120, "portfolio": "art"},
                           "critical":         {"label": "First place",        "xp": 125, "art_rep": 12, "money": 200, "portfolio": "art",
                                                "journal": True, "confidence": True},
                       }}},
        {"id": "networking_pitch", "title": "Pitch & Network Evening", "category": "career",
         "location": "location_bar", "duration": 2, "hour": 19,
         "desc": "A 3-minute pitch competition for locals.",
         "req": {"stat_chr": 15}, "rewards": {}, "days": [2, 3, 4],
         "challenge": {"skill": "biz", "recommended": 6, "difficulty": 64, "entry": 0,
                       "outcomes": _chal_outcomes(14, 5, 50)}},
    ]

    # Merge into the existing pool (idempotent across reloads/inits).
    _existing_ct_ids = {t["id"] for t in CITY_EVENT_TEMPLATES}
    for _ct in CITY_CHALLENGE_TEMPLATES:
        if _ct["id"] not in _existing_ct_ids:
            CITY_EVENT_TEMPLATES.append(_ct)

    def city_event_template(template_id):
        return next((t for t in CITY_EVENT_TEMPLATES if t["id"] == template_id), {})

    # Phase 62 §10: optional event-prep consumable. Buying supplies before a
    # challenge is never required — it is a modest, visible bonus you may skip.
    EVENT_PREP_COST = 25

    def challenge_prep_active():
        return store._challenge_prepped == store.day

    def buy_event_prep():
        if challenge_prep_active():
            return False
        if not try_spend(EVENT_PREP_COST, "discretionary"):
            return False
        store._challenge_prepped = store.day
        return True

    def _buy_event_prep_wrapper():
        """Function() wrapper — returns None."""
        buy_event_prep()

    def _city_chal_mods(event=None):
        """ONE modifier list shared by the odds preview and the resolution, so
        the number shown to the player is the number that gets rolled."""
        mods = []
        if has_player_state("focused"):   mods.append(("Focused", +3))
        if has_player_state("confident"): mods.append(("Confident", +5))
        if store.need_energy < 25:        mods.append(("Low energy", -5))
        if challenge_prep_active():       mods.append(("Prepared", +5))
        # Phase 65: at an exhibition the judges look at the piece you entered,
        # not at you. Its quality is the single biggest factor in placing.
        if event is not None and event.get("template_id") == "art_exhibition":
            sub = exhibition_submission_bonus(event["id"])
            if sub:
                mods.append(sub)
        return mods

    def city_challenge_spec(event):
        return city_event_template(event.get("template_id", "")).get("challenge")

    def city_challenge_chance(event):
        ch = city_challenge_spec(event)
        sk = ch["skill"]
        mods = _city_chal_mods(event)
        return calculate_check_chance("citychal_" + event["id"], skill_val(sk),
                                      ch["difficulty"], mods)

    def resolve_city_challenge(event_id):
        """Charge entry, roll, apply tiered rewards, mark attended. Returns dict."""
        evts = list(store.city_event_schedule)
        idx = next((i for i, e in enumerate(evts)
                    if e["id"] == event_id and not e.get("attended")), None)
        if idx is None:
            return None
        e = dict(evts[idx])
        ch = city_challenge_spec(e)
        sk = ch["skill"]
        mods = _city_chal_mods(e)
        result = roll_check("citychal_" + event_id, skill_val(sk), ch["difficulty"],
                            mods, stable=False)
        tier = result["tier"]
        outcome = ch["outcomes"][tier]

        # apply rewards
        if outcome.get("xp"):
            gain_skill_practice(sk, outcome["xp"], 1)
        if outcome.get("rep"):
            store.freelance_reputation = min(100, store.freelance_reputation + outcome["rep"])
        if outcome.get("art_rep"):
            gain_art_rep(outcome["art_rep"])
        # The entered piece comes back with a result attached. Placing puts it
        # in the portfolio; either way it is released for sale/gift again.
        _sub = submitted_artwork_for(event_id)
        if _sub is not None:
            update_artwork(_sub["id"], submitted_to=None,
                           exhibited_as=outcome["label"],
                           in_portfolio=(_sub["in_portfolio"] or bool(outcome.get("portfolio"))))
        if outcome.get("money"):
            gain_money(outcome["money"])
        if outcome.get("confidence"):
            add_player_state("confident", "chal_%s_day%d" % (event_id, store.day))
        if outcome.get("portfolio"):
            record_game_event("chal_%s_day%d" % (event_id, store.day), "project",
                "%s — %s" % (e["title"], outcome["label"]), summary=True,
                journal=outcome.get("journal", False), portfolio_domain=outcome["portfolio"],
                metadata={"challenge": event_id, "tier": tier})
        elif outcome.get("journal"):
            record_game_event("chal_%s_day%d" % (event_id, store.day), "event",
                "%s — %s" % (e["title"], outcome["label"]), summary=True, journal=True,
                metadata={"challenge": event_id, "tier": tier})
        else:
            record_game_event("chal_%s_day%d" % (event_id, store.day), "event",
                "%s — %s" % (e["title"], outcome["label"]), summary=True, journal=False,
                metadata={"challenge": event_id, "tier": tier})

        # Phase 68: a public result is something the city can hear about.
        # Placing spreads by word of mouth (Respect only); a poor showing may
        # generate encouragement content instead.
        if tier in ("critical", "great"):
            publish_player_fact("won_city_challenge", event_id)
        elif tier in ("weak", "critical_failure"):
            trigger_failure_content("city_challenge_failed")

        e["attended"] = True
        e["status"] = "completed"
        e["result"] = tier
        evts[idx] = e
        store.city_event_schedule = evts
        return {"result": result, "tier": tier, "outcome": outcome,
                "title": e["title"], "skill": sk}

    # Override the flat-event wrapper so challenge events route to the roll flow.
    # (Redefined here at init priority 1 -> replaces city_events.rpy's version.)
    def _attend_city_event_wrapper(event_id):
        """Function() wrapper — returns None. Challenges run in a new context."""
        e = next((ev for ev in store.city_event_schedule if ev["id"] == event_id), None)
        if e is not None and city_challenge_spec(e):
            renpy.call_in_new_context("city_challenge_ctx", event_id)
        else:
            attend_city_event(event_id)


label city_challenge_ctx(event_id):
    $ _ce = next((ev for ev in store.city_event_schedule if ev["id"] == event_id), None)
    if _ce is None or _ce.get("attended"):
        return
    $ _cspec = city_challenge_spec(_ce)
    call screen city_challenge_confirm_scr(event_id)
    if not _return:
        return
    # entry fee
    if _cspec.get("entry", 0) > 0:
        if not try_spend(_cspec["entry"], "discretionary"):
            "You can't cover the entry fee."
            return
    $ _cres = resolve_city_challenge(event_id)
    $ spend_time(_ce["duration"])
    $ need_energy = max(0, need_energy - 15)
    if _cres is not None:
        call screen check_result_scr(_cres["result"], title=(_cres["title"] + " — " + _cres["outcome"]["label"]), xtra_lines=_city_challenge_lines(_cres))
    return

init python:
    def _city_challenge_lines(cres):
        o = cres["outcome"]
        sklabel = PRO_SKILLS.get(cres.get("skill", ""), ("Skill",))[0]
        lines = []
        if o.get("xp"):     lines.append("+%d %s XP" % (o["xp"], sklabel))
        if o.get("rep"):    lines.append("+%d reputation" % o["rep"])
        if o.get("art_rep"):lines.append("+%d art reputation" % o["art_rep"])
        if o.get("money"): lines.append("+$%d prize" % o["money"])
        if not lines:      lines.append("Good experience.")
        return lines


# ── Challenge confirm / odds screen ─────────────────────────────────────────────
screen city_challenge_confirm_scr(event_id):
    modal True
    zorder 220
    add "#000000cc"
    $ _e = next((ev for ev in city_event_schedule if ev["id"] == event_id), None)
    frame:
        xalign 0.5 yalign 0.5
        xsize 560
        background "#12161ef8"
        padding (24, 20, 24, 22)
        if _e is None:
            vbox:
                spacing 10
                text "This event has ended." font ACT_FONT size 14 color "#cfe0f5"
                textbutton "Close" action Return(False) text_font ACT_FONT text_size 13 text_color "#5bcafa"
        else:
            $ _ch = city_challenge_spec(_e)
            $ _cc = city_challenge_chance(_e)
            $ _sklabel = PRO_SKILLS.get(_ch["skill"], (_ch["skill"],))[0]
            vbox:
                spacing 8
                text _e["title"] font PROFILE_FONT size 18 color "#cfe0f5" xalign 0.5
                text _e["desc"] font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                null height 4
                hbox:
                    xalign 0.5
                    spacing 16
                    text ("Your %s: %d" % (_sklabel, skill_val(_ch["skill"]))) font ACT_FONT size 13 color "#9fb6d6"
                    text ("Recommended: %d" % _ch["recommended"]) font ACT_FONT size 13 color "#7a9ab8"
                if _ch.get("entry", 0) > 0:
                    text ("Entry fee: $%d" % _ch["entry"]) font ACT_FONT size 12 color "#ffd66a" xalign 0.5
                text ("Time: %dh  ·  Energy: -15" % _e["duration"]) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                null height 4
                text "Chance to place:" font ACT_FONT size 13 color "#9fb6d6" xalign 0.5
                for _tid in ("critical","great","success","weak","critical_failure"):
                    hbox:
                        xalign 0.5
                        spacing 10
                        text ("%-16s" % _ch["outcomes"][_tid]["label"]) font ACT_FONT size 12 color tier_color(_tid) xsize 170
                        text ("%d%%" % _cc["distribution"][_tid]) font PROFILE_FONT size 12 color "#ffd66a"
                null height 4
                if challenge_prep_active():
                    text "Prepared — supplies bought today. +5 to the roll." font ACT_FONT size 12 color "#7fd06a" xalign 0.5
                else:
                    textbutton ("Buy supplies and print-outs ($%d) — optional, +5" % EVENT_PREP_COST):
                        action [Function(_buy_event_prep_wrapper), renpy.restart_interaction]
                        sensitive (money >= EVENT_PREP_COST)
                        xalign 0.5
                        background "#1a2a3a"
                        hover_background "#1e3a5f"
                        xpadding 12 ypadding 5
                        text_font ACT_FONT text_size 12
                        text_color ("#ffd66a" if money >= EVENT_PREP_COST else "#4a6080")
                        text_hover_color "#ffffff"
                null height 6
                hbox:
                    xalign 0.5
                    spacing 12
                    button action Return(True) background "#1e3a5f" padding (18, 8):
                        text "Compete" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"
                    button action Return(False) background "#1a2a3a" padding (18, 8):
                        text "Not now" font ACT_FONT size 14 color "#9fb6d6" hover_color "#ffffff"
