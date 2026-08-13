# Freelance system — contract work the player can pick up via the computer.
# Uses mail.rpy for notifications. Separate from gigs (which are one-shot phone jobs).

default freelance_reputation    = 0
default freelance_completed     = 0
default freelance_failed        = 0
default freelance_active_project = None
default freelance_offers        = []
default freelance_history       = []
default freelance_pending_payments = []
default freelance_last_refresh_day = -1

init python:

    FREELANCE_TEMPLATES = [
        # skill 1 — entry level; difficulty ≈ min_skill
        {"id": "css_fix_01",    "title": "Fix CSS layout bug",          "client": "Otak Studio",
         "min_skill": 1, "min_rep": 0,  "hours": 2, "days": 3, "pay": 55, "exp":  5, "difficulty": 2},
        {"id": "html_page_01",  "title": "Simple landing page",         "client": "Meridian Foods",
         "min_skill": 1, "min_rep": 0,  "hours": 3, "days": 4, "pay": 70, "exp":  6, "difficulty": 2},
        # skill 2
        {"id": "form_fix_01",   "title": "Form validation bug",         "client": "Bellway Apps",
         "min_skill": 2, "min_rep": 0,  "hours": 3, "days": 3, "pay": 85, "exp":  7, "difficulty": 3},
        {"id": "api_docs_01",   "title": "Write API docs",              "client": "Novus Tech",
         "min_skill": 2, "min_rep": 2,  "hours": 2, "days": 4, "pay": 65, "exp":  6, "difficulty": 3},
        # skill 3
        {"id": "script_01",     "title": "Automation script",           "client": "Crane Logistics",
         "min_skill": 3, "min_rep": 3,  "hours": 4, "days": 4, "pay": 120, "exp": 10, "difficulty": 4},
        {"id": "wp_plugin_01",  "title": "WordPress plugin tweak",      "client": "Hazel Creative",
         "min_skill": 3, "min_rep": 3,  "hours": 4, "days": 5, "pay": 140, "exp": 12, "difficulty": 4},
        # skill 4
        {"id": "rest_api_01",   "title": "Build REST endpoint",         "client": "Pulse Digital",
         "min_skill": 4, "min_rep": 8,  "hours": 5, "days": 5, "pay": 190, "exp": 14, "difficulty": 5},
        {"id": "db_opt_01",     "title": "Database query optimisation", "client": "Vanta Analytics",
         "min_skill": 4, "min_rep": 8,  "hours": 4, "days": 4, "pay": 175, "exp": 12, "difficulty": 5},
        # skill 5
        {"id": "spa_01",        "title": "Single-page app component",   "client": "Solara Labs",
         "min_skill": 5, "min_rep": 14,  "hours": 6, "days": 6, "pay": 260, "exp": 18, "difficulty": 6},
        {"id": "auth_01",       "title": "OAuth integration",           "client": "Keypath Systems",
         "min_skill": 5, "min_rep": 14,  "hours": 5, "days": 5, "pay": 230, "exp": 16, "difficulty": 6},
        # skill 6
        {"id": "mobile_01",     "title": "Mobile app screen",           "client": "Arca Mobile",
         "min_skill": 6, "min_rep": 22, "hours": 7, "days": 6, "pay": 440, "exp": 20, "difficulty": 7},
        {"id": "data_pipe_01",  "title": "Data pipeline",               "client": "Flux Insights",
         "min_skill": 6, "min_rep": 22, "hours": 6, "days": 5, "pay": 400, "exp": 18, "difficulty": 7},
        # skill 7-8
        {"id": "arch_01",       "title": "Architecture refactor",       "client": "Trident Software",
         "min_skill": 7, "min_rep": 32, "hours": 8, "days": 7, "pay": 580, "exp": 25, "difficulty": 7},
        {"id": "perf_01",       "title": "Performance audit and fix",   "client": "Apex Commerce",
         "min_skill": 8, "min_rep": 42, "hours": 8, "days": 6, "pay": 700, "exp": 28, "difficulty": 8},
        # skill 9-10
        {"id": "ml_api_01",     "title": "ML API integration",          "client": "Synapse AI",
         "min_skill": 9, "min_rep": 55, "hours": 10, "days": 7, "pay":  950, "exp": 35, "difficulty": 9},
        {"id": "fullstack_01",  "title": "Full-stack feature",          "client": "Vertex Platform",
         "min_skill": 10, "min_rep": 70, "hours": 12, "days": 8, "pay": 1200, "exp": 45, "difficulty": 10},
    ]

    def freelance_eligible(t):
        """Can the player see this offer?"""
        return (skill_val("prog") >= t["min_skill"]
                and store.freelance_reputation >= t["min_rep"]
                and store.freelance_active_project is None)

    def refresh_freelance_offers():
        """Generate up to 3 offers (+ faster_internet bonus). Called from new_day()."""
        if store.freelance_last_refresh_day >= store.day:
            return
        store.freelance_last_refresh_day = store.day
        eligible = [t for t in FREELANCE_TEMPLATES if freelance_eligible(t)]
        recent_ids = [h["template_id"] for h in store.freelance_history[-3:]]
        eligible = [t for t in eligible if t["id"] not in recent_ids]
        import random as _r
        _rng = _r.Random(store.day * 137 + store.freelance_reputation)
        max_offers = 3 + int(home_upgrade_effect("freelance_offers"))
        picked = _rng.sample(eligible, min(max_offers, len(eligible)))
        store.freelance_offers = [t["id"] for t in picked]

    def _all_freelance_templates():
        """All templates including returning client follow-ups."""
        return list(FREELANCE_TEMPLATES) + list(_RETURNING_CLIENT_TEMPLATES)

    # Phase 60B: pay multipliers by final rating
    _FL_PAY_MULTIPLIERS = {"D": 0.80, "C": 0.92, "B": 1.00, "A": 1.06, "S": 1.15}

    FREELANCE_RARE_EVENTS = [
        {"id": "breakthrough_structure",
         "trigger_tiers": ["great", "critical"], "chance": 0.08,
         "text": "You find a much cleaner way to structure the feature.",
         "effects": {"extra_progress": 1.0, "quality_bonus": 4, "xp_bonus": 8}},
        {"id": "unexpected_bug",
         "trigger_tiers": ["critical_failure", "weak"], "chance": 0.12,
         "text": "A library behaves differently than documented. You need more time.",
         "effects": {"extra_work_required": 1.0, "xp_bonus": 10}},
        {"id": "client_hint",
         "trigger_tiers": ["success", "great", "critical"], "chance": 0.06,
         "text": "The client messages with a clarification that simplifies part of the work.",
         "effects": {"extra_progress": 0.5}},
        {"id": "referral_hint",
         "trigger_tiers": ["great", "critical"], "chance": 0.05,
         "text": "The client mentions another project coming up if this one goes well.",
         "effects": {"referral_flag": True}},
    ]

    def _check_freelance_rare_event(project, tier):
        """Fires at most one rare event per project per session. Mutates project dict in place."""
        fired = project.get("rare_events", [])
        for ev in FREELANCE_RARE_EVENTS:
            if ev["id"] in fired:           continue
            if tier not in ev["trigger_tiers"]: continue
            if renpy.random.random() > ev["chance"]: continue
            eff = ev["effects"]
            if "extra_work_required" in eff:
                project["required_hours"] = project.get("required_hours", 0) + eff["extra_work_required"]
            if "extra_progress" in eff:
                project["worked_hours"] = project.get("worked_hours", 0) + eff["extra_progress"]
            if "quality_bonus" in eff:
                project["quality_bonus"] = project.get("quality_bonus", 0) + eff["quality_bonus"]
            if "referral_flag" in eff:
                project["referral_unlocked"] = True
            project.setdefault("rare_events", []).append(ev["id"])
            return ev
        return None

    def _freelance_xp_multiplier(prog_skill, difficulty):
        """Harder projects give more XP. Easy ones give less."""
        diff = difficulty - prog_skill
        if diff <= -3: return 0.5
        if diff <= 0:  return 1.0
        if diff == 1:  return 1.2
        if diff == 2:  return 1.4
        return 1.6

    def freelance_session_roll(project, hours, approach="normal"):
        """Single work session roll. Returns session result dict. Mutates project dict."""
        prog_skill = skill_val("prog")
        difficulty = project.get("difficulty", 5)
        approach_mods = {
            "careful": [("Careful approach", -8)],
            "normal":  [],
            "push":    [("Pushing hard",     +10)],
        }
        mods = list(approach_mods.get(approach, []))
        if has_player_state("focused"):  mods.append(("Focused",    +8))
        if has_player_state("stressed"): mods.append(("Stressed",   -6))
        if store.need_energy < 30:       mods.append(("Low energy", -8))
        elif store.need_energy > 70:     mods.append(("High energy",+4))
        # Phase 64: was int(eff * 10). desk_efficiency is 0.05, so this computed
        # int(0.5) = 0 and the $260 Proper Desk did literally nothing to a
        # freelance session. round() alone does not fix it either — Python 3
        # banker's rounding makes round(0.5) == 0. Scale so 5% -> +3 roll points,
        # in line with the other session modifiers (Focused +8, High energy +4).
        desk_bonus = int(round(home_upgrade_effect("desk_efficiency") * 60))
        if desk_bonus: mods.append(("Proper desk", desk_bonus))

        result = roll_check(
            "fl_session_" + str(project.get("template_id", "")),
            skill_val=prog_skill,
            difficulty=40 + difficulty * 2,   # diff5=50, diff8=56
            modifiers=mods, stable=False)
        tier = result["tier"]

        progress_mult = {"critical_failure": 0.6, "weak": 0.8,
                         "success": 1.0, "great": 1.25, "critical": 1.5}[tier]
        approach_progress = {"careful": 0.9, "normal": 1.0, "push": 1.25}[approach]
        effective_progress = hours * progress_mult * approach_progress

        xp_mult = {"critical_failure": 1.2, "weak": 1.1,
                   "success": 1.0, "great": 1.1, "critical": 1.25}[tier]
        difficulty_mult = _freelance_xp_multiplier(prog_skill, difficulty)
        # Phase 63B: 8 -> 4 XP/hour. At 8, a freelance-only player hit prog 8 by
        # day 23 (target: day 60-80) and prog 5 by day 11 (target: day 30-45).
        xp = int(hours * 4 * xp_mult * difficulty_mult)

        quality_delta = {"critical_failure": -3, "weak": -1,
                         "success": 0, "great": +2, "critical": +4}[tier]

        narratives = {
            "critical_failure": ["You struggle through an unfamiliar section.",
                                 "The codebase keeps surprising you."],
            "weak":    ["Slower progress than expected.",
                        "A few wrong turns before finding the right approach."],
            "success": ["Steady progress.", "Things are coming together."],
            "great":   ["A productive session.", "The pieces are fitting together well."],
            "critical":["Everything clicks. You're in the zone.", "Clean, fast, effective."],
        }
        narrative = renpy.random.choice(narratives[tier])

        # Apply progress and quality to the project (caller must reassign to store)
        project["worked_hours"]   = project.get("worked_hours", 0) + effective_progress
        project["quality_bonus"]  = project.get("quality_bonus", 0) + max(0, quality_delta)
        project["quality_penalty"]= project.get("quality_penalty", 0) + max(0, -quality_delta)
        project.setdefault("session_log", []).append(tier)
        project.setdefault("approach_history", []).append(approach)

        rare = _check_freelance_rare_event(project, tier)

        return {
            "result":             result,
            "tier":               tier,
            "hours_spent":        hours,
            "effective_progress": effective_progress,
            "xp":                 xp,
            "quality_delta":      quality_delta,
            "narrative":          narrative,
            "rare_event":         rare,
        }

    def project_ready_to_submit(project):
        return project is not None and project.get("worked_hours", 0) >= project.get("required_hours", 999)

    def accept_freelance(template_id, override_pay=None):
        t = next((x for x in _all_freelance_templates() if x["id"] == template_id), None)
        if t is None or store.freelance_active_project is not None:
            return False
        client_id = t.get("client_id") or _client_id_from_name(t.get("client", ""))
        if client_id:
            ensure_client_profile(client_id, t.get("client", ""), "programming")
        # Randomise work_required ±15% rounded to 0.5h
        import random as _r2
        _rng2 = _r2.Random(store.day * 31 + hash(template_id))
        _wh = t["hours"]
        _work_req = round(_rng2.uniform(_wh * 0.85, _wh * 1.25) * 2) / 2
        store.freelance_active_project = {
            "template_id":    template_id,
            "title":          t["title"],
            "client":         t.get("client", ""),
            "client_id":      client_id,
            "domain":         t.get("domain", "programming"),
            "required_skill": t["min_skill"],
            "difficulty":     t.get("difficulty", t["min_skill"]),
            "accepted_day":   store.day,
            "deadline_day":   store.day + t["days"],
            "required_hours": _work_req,
            "worked_hours":   0.0,
            "pay":            override_pay if override_pay else t["pay"],
            "exp":            t["exp"],
            "status":         "active",
            "is_eli":         False,
            "preparation":    {"tested": False, "polished": False, "client_brief_reviewed": False},
            "session_log":    [],
            "quality_bonus":  0,
            "quality_penalty":0,
            "approach_history": [],
            "rare_events":    [],
        }
        store.freelance_offers = []
        return True

    def freelance_work(hours, approach="normal"):
        """Session-based work on the active project. Uses freelance_session_roll."""
        p = store.freelance_active_project
        if p is None or p["status"] != "active":
            return False, None
        p = dict(p)
        session = freelance_session_roll(p, hours, approach)
        store.freelance_active_project = p
        spend_time(hours)
        energy_cost = int(hours * 5 * {"careful": 1.0, "normal": 1.0, "push": 1.25}[approach])
        store.need_energy = max(0, store.need_energy - energy_cost)
        gain_skill_practice("prog", session["xp"], hours)
        return True, session

    def negotiate_freelance_rate(offer, target_pct=1.15):
        """Attempt to negotiate a higher rate. Returns result dict."""
        fl_rep   = getattr(store, "freelance_reputation", 0)
        biz_sk   = skill_val("biz")
        client_id= offer.get("client_id", "")
        trust    = store.client_profiles.get(client_id, {}).get("trust", 0)
        if target_pct <= 1.10: base_chance = 65
        elif target_pct <= 1.20: base_chance = 45
        elif target_pct <= 1.30: base_chance = 28
        else:                    base_chance = 12
        mods = [
            ("Freelance Rep",   min(15, fl_rep // 3)),
            ("Business skill",  min(10, biz_sk * 2)),
            ("Client trust",    min(8,  trust // 8)),
        ]
        result = roll_check("fl_negotiate_" + str(offer.get("id", offer.get("template_id",""))),
                            skill_val=0, difficulty=100 - base_chance,
                            modifiers=mods, stable=False)
        success = result["tier"] in ("success", "great", "critical")
        withdrawn = (result["tier"] == "critical_failure" and target_pct >= 1.30
                     and renpy.random.random() < 0.3)
        responses = {
            True:  ["Fair enough. We can work with that.", "Okay, adjusted."],
            False: ["That's above our budget.", "We can't stretch that far."],
        }
        return {
            "success":   success, "withdrawn": withdrawn,
            "response":  renpy.random.choice(responses[success]),
            "result":    result,
        }

    def request_extension(project):
        """Ask client for +3 days. Returns (success, result_dict)."""
        client_id = project.get("client_id", "")
        trust = store.client_profiles.get(client_id, {}).get("trust", 0)
        days_overdue = max(0, store.day - project.get("deadline_day", store.day))
        base = 50 + trust // 2 - days_overdue * 15
        mods = [("Client trust", min(15, trust // 5))]
        if days_overdue > 0:
            mods.append(("Already overdue", -days_overdue * 10))
        result = roll_check("fl_extension_" + str(project.get("template_id", "")),
                            skill_val=0, difficulty=max(5, 100 - base),
                            modifiers=mods, stable=False)
        success = result["tier"] in ("success", "great", "critical")
        p = dict(store.freelance_active_project or {})
        if success:
            p["deadline_day"] = p.get("deadline_day", store.day) + 3
            store.freelance_active_project = p
        else:
            if client_id:
                prof = dict(store.client_profiles.get(client_id, {}))
                prof["trust"] = max(0, prof.get("trust", 0) - 5)
                d = dict(store.client_profiles)
                d[client_id] = prof
                store.client_profiles = d
        return success, result

    def _freelance_test_review():
        """Mark project as tested; costs 1h and 15 energy. Does NOT submit."""
        p = dict(store.freelance_active_project)
        prep = dict(p.get("preparation", {}))
        prep["tested"] = True
        p["preparation"] = prep
        store.freelance_active_project = p
        spend_time(1)
        store.need_energy = max(0, store.need_energy - 15)

    def freelance_submit():
        p = store.freelance_active_project
        if not project_ready_to_submit(p):
            return False
        p = dict(p)
        p["status"] = "submitted"

        # Phase 60B: evaluate with quality data + rating-based pay multiplier
        result = evaluate_project(p, p.get("preparation", {}))
        _rating_mult = _FL_PAY_MULTIPLIERS.get(result["rating"], 1.0)
        _pay = int(p["pay"] * _rating_mult * freelance_pay_modifier())

        on_time = store.day <= p["deadline_day"]
        early   = store.day < p["deadline_day"] - 1
        rep_gain = result["rep_gain"]
        store.freelance_reputation = min(100, store.freelance_reputation + rep_gain)
        store.freelance_completed  += 1
        tid = p["template_id"]
        # Resolve the template for gate completion.
        _tmpl = next((t for t in _all_freelance_templates() if t["id"] == tid), {})
        _msk  = _tmpl.get("min_skill", 0)
        _hrs  = _tmpl.get("hours", 0)
        # Prog mastery gates
        complete_skill_gate("prog", 3, "fl_complete")
        if _msk >= 4 or _hrs >= 4:
            complete_skill_gate("prog", 5, "fl_intermediate_" + tid)
        if _msk >= 6:
            complete_skill_gate("prog", 7, "fl_hightier_" + tid)
        # Phase 63B deadlock fix: gate 9 previously needed a min_skill>=9 project,
        # but ml_api_01 (the only one) needs prog 9 — which the gate blocks. Prog
        # was hard-capped at 8 (0/300 sim runs ever reached 9). Same for gate 10.
        # Thresholds now sit one tier below the level they unlock.
        if _msk >= 8:
            complete_skill_gate("prog", 9, "fl_major_" + tid)
        if _msk >= 9:
            complete_skill_gate("prog", 10, "fl_capstone_" + tid)

        payment = {
            "template_id": tid,
            "pay": _pay, "exp": p["exp"],
            "pay_day": store.day + 1,
            "title": p["title"], "client": p.get("client", ""),
            "is_eli": p.get("is_eli", False),
            "mail_on_complete": _tmpl.get("mail_on_complete", ""),
        }
        store.freelance_pending_payments = list(store.freelance_pending_payments) + [payment]
        store.freelance_history = list(store.freelance_history) + [
            {"template_id": tid, "day": store.day, "result": "completed",
             "rating": result["rating"], "score": result["score"]}]

        # Update client profile
        client_id = p.get("client_id") or _client_id_from_name(p.get("client", ""))
        if client_id:
            update_client_after_project(client_id, dict(result, pay=_pay))

        # Add to portfolio
        add_project_to_portfolio(p, result)

        # Player state triggers
        if p.get("preparation", {}).get("tested"):
            add_player_state("focused", "tested_proj_" + tid)
        if result["rating"] in ("A", "S"):
            add_player_state("confident", "rating_A_" + tid)

        store.freelance_active_project = None

        # Also record in event logger for day summary (non-portfolio path)
        record_game_event(
            "fl_complete_%s_day%d" % (tid, store.day),
            "project", p["title"],
            summary=True, journal=False, portfolio_domain=None,
            metadata={"client": p.get("client", ""), "pay": _pay,
                      "template_id": tid, "day": store.day, "rating": result["rating"]})

        queue_mail(
            p.get("client", "Client"),
            "Project received: " + p["title"],
            "Thanks for the delivery. Payment will be processed tomorrow.",
            "freelance", store.day, "fl_submit_%s_%d" % (tid, store.day))

        # Store result for the result screen
        store._pending_project_result = {"result": result, "project": dict(p, pay=_pay)}
        return True

    def freelance_abandon():
        p = store.freelance_active_project
        if p is None:
            return
        store.freelance_reputation = max(0, store.freelance_reputation - 3)
        store.freelance_failed += 1
        store.freelance_history = list(store.freelance_history) + [
            {"template_id": p["template_id"], "day": store.day, "result": "abandoned"}]
        store.freelance_active_project = None

    def check_freelance_deadlines():
        """Mark overdue active projects as failed. Called from new_day()."""
        p = store.freelance_active_project
        if p and p["status"] == "active" and store.day > p["deadline_day"]:
            p = dict(p)
            p["status"] = "failed"
            store.freelance_reputation = max(0, store.freelance_reputation - 8)
            store.freelance_failed += 1
            store.freelance_history = list(store.freelance_history) + [
                {"template_id": p["template_id"], "day": store.day, "result": "failed"}]
            # Player state: missed deadline → stressed
            add_player_state("stressed", "missed_dl_" + p["template_id"])
            store.freelance_active_project = None
            queue_mail(p.get("client", "Client"), "Contract cancelled: " + p["title"],
                       "We were unable to wait any longer. The contract has been reassigned.",
                       "freelance", store.day, "fl_fail_%s_%d" % (p["template_id"], store.day))

    def process_freelance_payments():
        """Pay out completed projects. Called from new_day()."""
        due       = [x for x in store.freelance_pending_payments if x["pay_day"] <= store.day]
        remaining = [x for x in store.freelance_pending_payments if x["pay_day"] >  store.day]
        for pmt in due:
            gain_money(pmt["pay"])
            # Phase 63B: halved. This completion bonus is raw gain_skill — it
            # bypasses daily DR, streak and breakthrough entirely, and at high
            # tiers (25-45 XP/project/day) it was the single largest prog XP
            # source, outweighing the throttled session XP.
            gain_skill("prog", max(1, int(pmt["exp"] * 0.5)))
            mail_body = pmt.get("mail_on_complete") or "$%d has been transferred to your account." % pmt["pay"]
            queue_mail(pmt.get("client", "Client"), "Payment sent: " + pmt["title"],
                       mail_body,
                       "freelance", store.day,
                       "fl_pay_%s_%d" % (pmt["template_id"], store.day))
            if pmt.get("is_eli"):
                queue_phone_message("eli", "Nice work on the feature. Pushed to main.",
                                    store.day, "eli_side_project_done")
        store.freelance_pending_payments = remaining


# ── Computer: freelance screen ─────────────────────────────────────────────────
screen computer_freelance_scr():
    modal True
    add "#000000aa"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 580
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (20, 16, 20, 16)
        vbox:
            spacing 10
            text "Freelance" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            null height 2

            if freelance_active_project is not None:
                # ── Active project ────────────────────────────────────────────
                $ _p = freelance_active_project
                frame:
                    xfill True
                    background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                    padding (14, 12, 14, 12)
                    vbox:
                        spacing 6
                        text _p["title"] font PROFILE_FONT size 17 color "#cfe0f5"
                        text ("Client: " + _p["client"]) font ACT_FONT size 14 color "#7a90a8"
                        null height 4
                        # Progress bar
                        $ _prog = min(1.0, _p["worked_hours"] / max(1, _p["required_hours"]))
                        hbox:
                            spacing 10
                            yalign 0.5
                            text "Progress:" font ACT_FONT size 13 color "#8fb0d0" yalign 0.5
                            frame:
                                xsize 320
                                ysize 14
                                background "#1a2a3a"
                                frame:
                                    xsize int(320 * _prog)
                                    ysize 14
                                    background ("#7fd06a" if _prog >= 1.0 else "#5bcafa")
                            text ("%dh / %dh" % (_p["worked_hours"], _p["required_hours"])) font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                        $ _days_left = _p["deadline_day"] - day
                        text ("Deadline: day %d  (%d days left)" % (_p["deadline_day"], _days_left)) font ACT_FONT size 13 color ("#e8a24d" if _days_left <= 1 else "#8fb0d0")
                        text ("Pay on completion: $%d" % _p["pay"]) font ACT_FONT size 14 color "#ffd66a"
                null height 4
                # Pre-work session odds display
                $ _p2 = freelance_active_project
                $ _fl_diff2 = _p2.get("difficulty", 5) if _p2 else 5
                $ _fl_ch2 = calculate_check_chance("fl_session_" + (_p2 or {}).get("template_id",""), skill_val("prog"), 40 + _fl_diff2*2, [("Focused",+8)] if has_player_state("focused") else [])
                hbox:
                    spacing 12
                    xalign 0.5
                    text ("Good session: %d%%  |  Difficulty: %d" % (_fl_ch2["success_or_better"], _fl_diff2)):
                        font ACT_FONT size 12 color "#4a6080" yalign 0.5
                null height 2
                hbox:
                    spacing 10
                    xalign 0.5
                    textbutton "Work carefully (1h)":
                        sensitive (not too_tired())
                        action [Function(freelance_work, 1, "careful"), Return()]
                        text_font ACT_FONT text_size 14 text_color "#cfe0f5" text_hover_color "#ffffff"
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        xpadding 8 ypadding 6
                    textbutton "Work (2h)":
                        sensitive (not too_tired())
                        action [Function(freelance_work, 2, "normal"), Return()]
                        text_font ACT_FONT text_size 14 text_color "#cfe0f5" text_hover_color "#ffffff"
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        xpadding 8 ypadding 6
                    textbutton "Push hard (2h)":
                        sensitive (not worn_out())
                        action [Function(freelance_work, 2, "push"), Return()]
                        text_font ACT_FONT text_size 14 text_color "#e8a24d" text_hover_color "#ffffff"
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        xpadding 8 ypadding 6
                $ _p3 = freelance_active_project
                $ _ready = project_ready_to_submit(_p3)
                $ _days_left3 = (_p3["deadline_day"] - day) if _p3 else 0
                if _ready:
                    $ _fl_mods = (
                        ([("Focused",    +5)] if has_player_state("focused")  else []) +
                        ([("Stressed",   -5)] if has_player_state("stressed") else []) +
                        ([("Low energy", -4)] if need_energy < 30 else [])
                    )
                    $ _fl_chance = calculate_check_chance("freelance_exec_" + (_p3["template_id"] if _p3 else ""), 0, 50, _fl_mods)["success_or_better"]
                    text ("Execution: %d%% chance of no penalty" % _fl_chance):
                        font ACT_FONT size 12 color "#4a8a6a" xalign 0.5
                    hbox:
                        spacing 10
                        xalign 0.5
                        textbutton "Submit":
                            action [Function(_freelance_submit_wrapper), Return()]
                            text_font ACT_FONT text_size 15 text_color "#7fd06a" text_hover_color "#ffffff"
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                            xpadding 10 ypadding 6
                        textbutton "Test and review (1h)":
                            sensitive (not _p3.get("preparation", {}).get("tested") and not too_tired())
                            action Function(_freelance_test_review)
                            text_font ACT_FONT text_size 14 text_color "#5bcafa" text_hover_color "#ffffff"
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                            xpadding 10 ypadding 6
                        if _p3.get("preparation", {}).get("tested"):
                            text "✓ Tested" font ACT_FONT size 13 color "#7fd06a" yalign 0.5
                if not _ready and _days_left3 <= 1 and _p3:
                    # Extension request option when deadline is close
                    $ _ext_ch = calculate_check_chance("fl_extension_" + (_p3.get("template_id","")), 0, 40, [("Client trust", min(15, store.client_profiles.get(_p3.get("client_id",""),{}).get("trust",0)//5))])["success_or_better"]
                    hbox:
                        spacing 10
                        xalign 0.5
                        textbutton ("Request extension (%d%% chance)" % _ext_ch):
                            action [Function(request_extension, _p3), Return()]
                            text_font ACT_FONT text_size 14 text_color "#cc9040" text_hover_color "#ffffff"
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                            xpadding 10 ypadding 6
                hbox:
                    spacing 10
                    xalign 0.5
                    textbutton "Abandon":
                        action [Function(freelance_abandon), Return()]
                        text_font ACT_FONT text_size 15 text_color "#e8a24d" text_hover_color "#ffffff"
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        xpadding 10 ypadding 6
                    textbutton "Close":
                        action Return("close")
                        text_font ACT_FONT text_size 15 text_color "#9fb6d6" text_hover_color "#ffffff"
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        xpadding 10 ypadding 6

            else:
                # ── Offer list ────────────────────────────────────────────────
                $ _offer_tmpl = [t for t in _all_freelance_templates() if t["id"] in freelance_offers]
                if not _offer_tmpl:
                    text "No offers right now. New contracts refresh each day." font ACT_FONT size 14 color "#4a6080" xalign 0.5
                else:
                    viewport:
                        xfill True
                        ysize 400
                        mousewheel True
                        scrollbars "vertical"
                        vbox:
                            spacing 10
                            xfill True
                            for _t in _offer_tmpl:
                                frame:
                                    xfill True
                                    background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                                    padding (14, 10, 14, 10)
                                    vbox:
                                        spacing 4
                                        text _t["title"] font PROFILE_FONT size 15 color "#cfe0f5"
                                        text ("Client: " + _t["client"]) font ACT_FONT size 13 color "#7a90a8"
                                        hbox:
                                            spacing 16
                                            text ("%dh work" % _t["hours"]) font ACT_FONT size 13 color "#8fb0d0"
                                            text ("$%d" % _t["pay"]) font ACT_FONT size 13 color "#ffd66a"
                                            text ("Deadline: %d days" % _t["days"]) font ACT_FONT size 13 color "#8fb0d0"
                                        hbox:
                                            spacing 16
                                            text ("Min skill: Prog %d" % _t["min_skill"]) font ACT_FONT size 12 color ("#7fd06a" if skill_val("prog") >= _t["min_skill"] else "#e8a24d")
                                            text ("Rep req: %d" % _t["min_rep"]) font ACT_FONT size 12 color ("#7fd06a" if freelance_reputation >= _t["min_rep"] else "#e8a24d")
                                        # Negotiation odds
                                        $ _neg_ch = calculate_check_chance("fl_negotiate_" + _t["id"], 0, 55, [("Business", min(10, skill_val("biz")*2))])["success_or_better"]
                                        hbox:
                                            spacing 10
                                            xalign 1.0
                                            textbutton "Accept":
                                                action [Function(accept_freelance, _t["id"]), Return()]
                                                text_font ACT_FONT text_size 14 text_color "#7fd06a" text_hover_color "#ffffff"
                                                background Frame("images/ui/act_bar_idle.png",10,10,10,10)
                                                hover_background Frame("images/ui/act_bar_hover_clean.png",10,10,10,10)
                                                xpadding 8 ypadding 5
                                            textbutton ("Negotiate +15%% (%d%%)" % _neg_ch):
                                                action [Function(_freelance_negotiate_wrapper, _t["id"]), Return()]
                                                text_font ACT_FONT text_size 13 text_color "#cc9040" text_hover_color "#ffffff"
                                                background Frame("images/ui/act_bar_idle.png",10,10,10,10)
                                                hover_background Frame("images/ui/act_bar_hover_clean.png",10,10,10,10)
                                                xpadding 8 ypadding 5
                textbutton "Close" action Return("close") xalign 0.5 text_font ACT_FONT text_size 19 text_color "#9fb6d6" text_hover_color "#ffffff"
                text ("Reputation: %d  |  Completed: %d  |  Failed: %d" % (freelance_reputation, freelance_completed, freelance_failed)) font ACT_FONT size 12 color "#4a6080" xalign 0.5
