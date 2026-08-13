# Central skill-check and RNG resolution engine.
# Phase 60: roll_check(), probability engine, daily conditions, career incidents,
#           learning breakthrough, activity mastery, bar-game helpers.

init python:

    # ── Tier metadata ──────────────────────────────────────────────────────────
    CHECK_TIER_DATA = {
        "critical_failure": {"label": "Critical Failure", "color": "#e05050"},
        "weak":             {"label": "Weak Result",      "color": "#cc9040"},
        "success":          {"label": "Success",          "color": "#7ccc60"},
        "great":            {"label": "Great Success",    "color": "#5bcafa"},
        "critical":         {"label": "Critical Success", "color": "#ffd66a"},
    }

    def tier_label(tier):
        return CHECK_TIER_DATA[tier]["label"]

    def tier_color(tier):
        return CHECK_TIER_DATA[tier]["color"]

    # ── Core roll ──────────────────────────────────────────────────────────────
    def roll_check(check_id, skill_val=0, difficulty=50,
                   modifiers=None, attempt_number=1, stable=False):
        """
        Returns result dict: raw_roll, final, tier, modifiers, breakdown.
        stable=True: deterministic for (check_id + day + attempt_number).
        Pity: +5 per failed attempt (max +20), reset on non-failure.
        """
        import random as _r
        if stable:
            seed = store.day * 100003 + attempt_number * 997 + _det_hash(check_id) % 50000
            rng = _r.Random(seed)
            raw = rng.randint(1, 100)
        else:
            raw = renpy.random.randint(1, 100)

        mods = list(modifiers or [])
        skill_bonus = min(25, int(skill_val * 2.5))
        if skill_bonus != 0:
            mods.append(("Skill", skill_bonus))
        diff_offset = 50 - difficulty
        if diff_offset != 0:
            mods.append(("Difficulty", diff_offset))
        pity = min(20, store._check_pity.get(check_id, 0))
        if pity > 0:
            mods.append(("Prev. experience", pity))

        total_mod = sum(v for _, v in mods)
        final = max(1, min(100, raw + total_mod))

        if   final >= 95: tier = "critical"
        elif final >= 75: tier = "great"
        elif final >= 40: tier = "success"
        elif final >= 11: tier = "weak"
        else:             tier = "critical_failure"

        # Pity update
        pity_dict = dict(store._check_pity)
        if tier in ("critical_failure", "weak"):
            pity_dict[check_id] = min(20, pity_dict.get(check_id, 0) + 5)
        else:
            pity_dict[check_id] = 0
        store._check_pity = pity_dict

        # Attempt counter
        attempt_dict = dict(store._check_attempts)
        attempt_dict[check_id] = attempt_dict.get(check_id, 0) + 1
        store._check_attempts = attempt_dict

        lines = ["Roll: %d" % raw]
        for lbl, val in mods:
            lines.append("%-20s %+d" % (lbl + ":", val))
        lines.append("-" * 24)
        lines.append("Final: %d" % final)
        breakdown = "\n".join(lines)

        return {
            "raw_roll":  raw,
            "final":     final,
            "tier":      tier,
            "modifiers": mods,
            "breakdown": breakdown,
        }

    # ── Probability engine (NO side effects) ──────────────────────────────────
    def calculate_check_chance(check_id, skill_val=0, difficulty=50,
                                modifiers=None, include_pity=True):
        """
        Returns probability distribution WITHOUT consuming a roll or updating pity.
        Uses identical modifier logic to roll_check().
        """
        mods = list(modifiers or [])
        skill_bonus = min(25, int(skill_val * 2.5))
        diff_offset = 50 - difficulty
        pity = min(20, store._check_pity.get(check_id, 0)) if include_pity else 0
        total_mod = skill_bonus + diff_offset + pity + sum(v for _, v in mods)

        def p_at_least(threshold):
            eff = threshold - total_mod
            if eff <= 1:   return 100
            if eff > 100:  return 0
            return 100 - eff + 1

        p_critical  = p_at_least(95)
        p_great     = p_at_least(75) - p_critical
        p_success   = p_at_least(40) - p_at_least(75)
        p_weak      = p_at_least(11) - p_at_least(40)
        p_crit_fail = 100 - p_at_least(11)

        mod_lines = []
        if skill_bonus: mod_lines.append(("Skill",            skill_bonus))
        if diff_offset: mod_lines.append(("Difficulty",       diff_offset))
        if pity:        mod_lines.append(("Prev. experience", pity))
        for lbl, val in mods:
            mod_lines.append((lbl, val))

        return {
            "success_or_better": p_at_least(40),
            "distribution": {
                "critical_failure": p_crit_fail,
                "weak":             p_weak,
                "success":          p_success,
                "great":            p_great,
                "critical":         p_critical,
            },
            "effective_modifier": total_mod,
            "modifier_lines":     mod_lines,
        }

    def describe_check_modifiers(modifier_lines):
        lines = []
        for label, val in modifier_lines:
            sign = "+" if val >= 0 else ""
            lines.append("%-22s %s%d%%" % (label + ":", sign, val))
        return "\n".join(lines)

    def preview_preparation_delta(check_id, skill_val, difficulty, current_mods,
                                   new_mod_label, new_mod_value):
        """Returns (before_chance, after_chance) for 'success or better'. No side effects."""
        before = calculate_check_chance(check_id, skill_val, difficulty,
                                        current_mods)["success_or_better"]
        after  = calculate_check_chance(check_id, skill_val, difficulty,
                                        current_mods + [(new_mod_label, new_mod_value)])["success_or_better"]
        return before, after

    # Legacy wrapper (delegates to calculate_check_chance).
    def estimate_success_chance(check_id, skill_val=0, difficulty=50, modifiers=None):
        return calculate_check_chance(check_id, skill_val, difficulty, modifiers)["success_or_better"]

    # ── Daily conditions ───────────────────────────────────────────────────────
    DAILY_CONDITIONS = [
        {"id": "beautiful_weather",  "weight": 15,
         "text": "Beautiful weather.",
         "effects": {"busking_crowd": 10, "park_attendance": 10}},
        {"id": "heavy_rain",         "weight": 10,
         "text": "Heavy rain.",
         "effects": {"busking_crowd": -15, "cafe_crowd": 10, "indoor_crowd": 5}},
        {"id": "friday_night_energy","days": [4], "weight": 20,
         "text": "Friday energy in the air.",
         "effects": {"bar_crowd": 15, "nightclub_crowd": 15}},
        {"id": "quiet_day",          "weight": 20,
         "text": "",
         "effects": {}},
        {"id": "local_event",        "weight": 10,
         "text": "Something is happening across town.",
         "effects": {"park_attendance": 5, "busking_crowd": 5}},
        {"id": "monday_drag",        "days": [0], "weight": 15,
         "text": "Monday. Everyone moves a little slower.",
         "effects": {"bar_crowd": -10}},
    ]

    def _generate_daily_condition(day_value=None):
        import random as _r
        d  = day_value if day_value is not None else store.day
        dw = d % 7
        rng = _r.Random(d * 31337 + 7)
        eligible  = [c for c in DAILY_CONDITIONS if dw in c.get("days", range(7))]
        total_w   = sum(c["weight"] for c in eligible)
        roll      = rng.random() * total_w
        cumulative = 0
        for c in eligible:
            cumulative += c["weight"]
            if roll < cumulative:
                return c
        return eligible[-1]

    def daily_condition():
        if store._daily_condition_day != store.day:
            store._daily_condition     = _generate_daily_condition()
            store._daily_condition_day = store.day
        return store._daily_condition

    def daily_condition_effect(effect_key, base=0):
        return base + daily_condition().get("effects", {}).get(effect_key, 0)

    # ── Career incident templates ──────────────────────────────────────────────
    CAREER_INCIDENT_TEMPLATES = {
        "it": [
            {"id": "it_prod_issue",   "min_rank": 0,
             "text": "A production issue hits shortly after you arrive.",
             "check_skill": "prog", "difficulty": 55,
             "choices": [
                 ("Take charge",    {"skill": "prog", "on_success_perf": 3, "on_fail_perf": 0, "on_success_xp": 12}),
                 ("Help the team",  {"skill": "prog", "on_success_perf": 2, "on_fail_perf": 1, "on_success_xp": 8}),
                 ("Stay out of it", {"perf_delta": 0, "xp_delta": 0}),
             ]},
            {"id": "it_code_review", "min_rank": 1,
             "text": "Your code is up for review in today's stand-up.",
             "check_skill": "prog", "difficulty": 60,
             "choices": [
                 ("Present confidently", {"skill": "prog", "on_success_perf": 4, "on_fail_perf": -1, "on_success_xp": 10}),
                 ("Keep it brief",       {"skill": "prog", "on_success_perf": 2, "on_fail_perf":  0, "on_success_xp":  6}),
             ]},
        ],
        "corporate": [
            {"id": "corp_client_surprise", "min_rank": 0,
             "text": "An unexpected client visit. Everyone's scrambling to look prepared.",
             "check_skill": "biz", "difficulty": 55,
             "choices": [
                 ("Step up",  {"skill": "biz", "on_success_perf": 3, "on_fail_perf": 0, "on_success_xp": 10}),
                 ("Blend in", {"perf_delta": 0, "xp_delta": 3}),
             ]},
        ],
        "hospital": [
            {"id": "hosp_emergency", "min_rank": 0,
             "text": "A difficult case arrives. The team is stretched thin.",
             "check_skill": "med", "difficulty": 60,
             "choices": [
                 ("Assist directly",     {"skill": "med", "on_success_perf": 4, "on_fail_perf": 0, "on_success_xp": 15}),
                 ("Support from behind", {"skill": "med", "on_success_perf": 1, "on_fail_perf": 1, "on_success_xp":  8}),
             ]},
        ],
        "culinary": [
            {"id": "cul_inspection_surprise", "min_rank": 0,
             "text": "An unannounced inspection. Every station is under scrutiny.",
             "check_skill": "cook", "difficulty": 58,
             "choices": [
                 ("Handle it professionally", {"skill": "cook", "on_success_perf": 4, "on_fail_perf": -1, "on_success_xp": 12}),
                 ("Focus on your station",    {"skill": "cook", "on_success_perf": 2, "on_fail_perf":  0, "on_success_xp":  7}),
             ]},
        ],
        "trainer": [
            {"id": "tr_client_pain", "min_rank": 0,
             "text": "A client reports pain mid-session. How you respond matters.",
             "check_skill": "fit", "difficulty": 55,
             "choices": [
                 ("Adapt the session",      {"skill": "fit", "on_success_perf": 3, "on_fail_perf": 0, "on_success_xp": 10}),
                 ("Stop early, rest them",  {"perf_delta": 1, "xp_delta": 5}),
             ]},
        ],
    }

    _INC_SKILL_MAP = {
        "it": "prog", "corporate": "biz", "hospital": "med",
        "culinary": "cook", "trainer": "fit",
    }

    def _career_incident_check(career_id, rank):
        """20% chance of a notable shift event. Returns incident dict or None."""
        if renpy.random.random() > 0.20:
            return None
        templates = CAREER_INCIDENT_TEMPLATES.get(career_id, [])
        if not templates:
            return None
        eligible = [t for t in templates if rank >= t.get("min_rank", 0)]
        if not eligible:
            return None
        return renpy.random.choice(eligible)

    # ── Learning breakthrough ──────────────────────────────────────────────────
    def _check_learning_breakthrough(skill_key, base_xp):
        """5-8% chance of breakthrough, increasing with consecutive sessions without one.
        Returns bonus XP (0 if no breakthrough). Sets store._pending_breakthrough when triggered."""
        sessions_since = store._breakthrough_sessions.get(skill_key, 0)
        chance = 0.05 + min(0.03, sessions_since * 0.003)
        if renpy.random.random() > chance:
            d = dict(store._breakthrough_sessions)
            d[skill_key] = d.get(skill_key, 0) + 1
            store._breakthrough_sessions = d
            return 0
        d = dict(store._breakthrough_sessions)
        d[skill_key] = 0
        store._breakthrough_sessions = d
        bonus = int(base_xp * 0.4)
        store._pending_breakthrough = {"skill": skill_key, "bonus": bonus}
        renpy.notify("%s breakthrough! +%d bonus XP." % (
            PRO_SKILLS.get(skill_key, (skill_key.title(), "", ""))[0], bonus))
        return bonus

    # Skill key → display label (init after careers.rpy which defines PRO_SKILLS).
    SKILL_LABEL_FOR = {k: v[0] for k, v in PRO_SKILLS.items()}

    # ── Career perf helper ─────────────────────────────────────────────────────
    def adjust_career_perf(cid, delta):
        """Apply a signed performance delta to an active career."""
        if delta == 0:
            return
        cur = career_perf(cid)
        set_career_perf(cid, cur + delta)

    # ── Activity mastery ───────────────────────────────────────────────────────
    _ACTIVITY_MASTERY_CAP = {
        "pool": 100, "darts": 100, "arm_wrestling": 100, "busking": 100,
    }
    _ACTIVITY_MASTERY_GAIN = {
        "pool":          {"win": 4, "loss": 1},
        "darts":         {"win": 3, "loss": 1},
        "arm_wrestling": {"win": 5, "loss": 2},
        "busking":       {"win": 3, "loss": 1},   # win = success-or-better performance
    }

    def gain_activity_mastery(activity_id, won=False):
        d = dict(store.activity_mastery)
        current  = d.get(activity_id, 0)
        cap      = _ACTIVITY_MASTERY_CAP.get(activity_id, 100)
        gain_tbl = _ACTIVITY_MASTERY_GAIN.get(activity_id, {"win": 3, "loss": 1})
        gain     = gain_tbl["win" if won else "loss"]
        if current > 50:
            gain = max(1, gain // 2)  # ponytail: diminishing returns; upgrade: separate cap at 75
        d[activity_id] = min(cap, current + gain)
        store.activity_mastery = d
        if won:
            w = dict(store.activity_mastery_wins)
            w[activity_id] = w.get(activity_id, 0) + 1
            store.activity_mastery_wins = w

    def activity_mastery_modifier(activity_id):
        """0-100 mastery → 0-20 bonus to roll final. Linear."""
        mastery = store.activity_mastery.get(activity_id, 0)
        return int(mastery * 0.20)

    # ── Freelance execution roll ───────────────────────────────────────────────
    def _freelance_execution_roll(project, base_score):
        """Adds variable result on top of deterministic base score.
        stable=True: same project+day produces same result."""
        check_id = "freelance_exec_" + str(project.get("template_id", ""))
        mods = []
        if has_player_state("focused"):  mods.append(("Focused",    +5))
        if has_player_state("stressed"): mods.append(("Stressed",   -5))
        if store.need_energy < 30:       mods.append(("Low energy", -4))
        result = roll_check(check_id, skill_val=0, difficulty=50,
                            modifiers=mods, stable=True)
        tier_delta = {
            "critical_failure": -10,
            "weak":              -5,
            "success":            0,
            "great":             +7,
            "critical":         +12,
        }[result["tier"]]
        adj_score = max(0, min(100, base_score + tier_delta))
        return adj_score, result

    # ── Social / qualitative chance display ───────────────────────────────────
    def qualitative_chance_label(success_pct):
        """For relational/emotional checks where exact % breaks immersion."""
        if success_pct >= 80: return "Very likely"
        if success_pct >= 60: return "Likely"
        if success_pct >= 40: return "Fair chance"
        if success_pct >= 20: return "Unlikely"
        return "Risky"

    def qualitative_chance_color(success_pct):
        if success_pct >= 60: return "#7ccc60"
        if success_pct >= 40: return "#cc9040"
        return "#e05050"


# ── Screens ────────────────────────────────────────────────────────────────────

screen check_result_scr(result, title="", details="", xtra_lines=None):
    modal True
    zorder 300
    $ _tier = result["tier"]
    $ _col  = tier_color(_tier)
    frame:
        xalign 0.5 yalign 0.4
        xsize 440
        background "#12161ef8"
        padding (24, 20, 24, 20)
        vbox:
            spacing 10
            if title:
                text title:
                    font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            null height 4
            text tier_label(_tier):
                font PROFILE_FONT size 22 color _col xalign 0.5
            # Near-miss readout. Real numbers only — near_miss_line() reads the
            # roll's actual post-modifier score against the real tier floor and
            # returns "" when the next tier was not within 5.
            $ _nm = near_miss_line(result)
            if _nm:
                text _nm:
                    font ACT_FONT size 12 color "#7090b0" xalign 0.5
            null height 6
            default _show_breakdown = False
            if _show_breakdown:
                frame:
                    background "#0a0e15"
                    padding (10, 8)
                    text result["breakdown"]:
                        font ACT_FONT size 12 color "#7090b0"
            button:
                action ToggleLocalVariable("_show_breakdown")
                background None
                xalign 0.5
                text ("Hide details" if _show_breakdown else "Show roll details"):
                    font ACT_FONT size 12 color "#4a6080" hover_color "#9fb6d6"
            if details:
                null height 4
                text details:
                    font ACT_FONT size 14 color "#cfe0f5" xalign 0.5
            if xtra_lines:
                null height 4
                for _xl in xtra_lines:
                    text _xl:
                        font ACT_FONT size 13 color "#cfe0f5" xalign 0.5
            null height 8
            button:
                action Return()
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Continue":
                    font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"


screen check_distribution_scr(chance_data, title=""):
    # non-modal floating display for showing full tier breakdown alongside menus
    modal False
    zorder 200
    frame:
        xalign 0.04 yalign 0.72
        xsize 240
        background "#0a0e15d8"
        padding (14, 10, 14, 10)
        vbox:
            spacing 3
            if title:
                text title:
                    font PROFILE_FONT size 12 color "#9fb6d6"
                null height 4
            for _tid, _pct in [
                ("critical",         chance_data["distribution"]["critical"]),
                ("great",            chance_data["distribution"]["great"]),
                ("success",          chance_data["distribution"]["success"]),
                ("weak",             chance_data["distribution"]["weak"]),
                ("critical_failure", chance_data["distribution"]["critical_failure"]),
            ]:
                hbox:
                    spacing 6
                    text ("%-15s" % tier_label(_tid)):
                        font ACT_FONT size 11 color tier_color(_tid) yalign 0.5 xsize 150
                    text ("%d%%" % _pct):
                        font ACT_FONT size 11 color "#7090b0" yalign 0.5


screen career_incident_choice_scr(incident):
    modal True
    zorder 250
    frame:
        xalign 0.5 yalign 0.38
        xsize 520
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 14
            text incident["text"]:
                font ACT_FONT size 15 color "#cfe0f5" xalign 0.5
            null height 4
            for _idx, (_lbl, _opt) in enumerate(incident["choices"]):
                button:
                    action Return(_idx)
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (16, 10)
                    text _lbl:
                        font ACT_FONT size 14 color "#9fb6d6" hover_color "#ffffff"


# ── Career incident handler ────────────────────────────────────────────────────
label career_incident_handler:
    # Expects store._inc_incident = incident dict, store._inc_cid = career id.
    "[store._inc_incident['text']]"
    call screen career_incident_choice_scr(store._inc_incident)
    # career_incident_choice_scr contract: an int index into ["choices"].
    # bool is a subclass of int, so a stray True/False would silently index
    # choice 1/0 instead of crashing — reject anything that isn't a real,
    # in-range int and fall back to the first (always-safe) choice.
    $ _ci_idx = _return
    if isinstance(_ci_idx, bool) or not isinstance(_ci_idx, int) or not (0 <= _ci_idx < len(store._inc_incident["choices"])):
        $ _ci_idx = 0
    $ _ci_choice_label, _ci_opt = store._inc_incident["choices"][_ci_idx]
    if "skill" in _ci_opt:
        $ _ci_res = roll_check(
            "incident_%s_%d" % (store._inc_cid, store.day),
            skill_val=skill_val(_ci_opt["skill"]),
            difficulty=store._inc_incident.get("difficulty", 55),
            stable=False)
        call screen check_result_scr(_ci_res, title="Shift Incident")
        if _ci_res["tier"] in ("success", "great", "critical"):
            $ _ci_pd = _ci_opt.get("on_success_perf", 0)
            $ _ci_xp = _ci_opt.get("on_success_xp", 0)
        else:
            $ _ci_pd = _ci_opt.get("on_fail_perf", 0)
            $ _ci_xp = 0
    else:
        $ _ci_pd = _ci_opt.get("perf_delta", 0)
        $ _ci_xp = _ci_opt.get("xp_delta", 0)
    if _ci_pd != 0:
        $ adjust_career_perf(store._inc_cid, _ci_pd)
    if _ci_xp > 0:
        $ gain_skill(_INC_SKILL_MAP.get(store._inc_cid, "biz"), _ci_xp)
    $ store._inc_incident = None
    $ store._inc_cid = None
    return


# ── Promotion status screen (Phase 60C erratum) ───────────────────────────────

screen career_promotion_status_scr(career_id, promo_result, breakdown):
    # Shows at end of shift. promo_result = dict from do_promotion_roll().
    modal True
    zorder 260
    $ _success = promo_result.get("success", False)
    $ _col = "#7ccc60" if _success else "#8fb0d0"
    frame:
        xalign 0.5 yalign 0.45
        xsize 500
        background "#12161ef8"
        padding (24, 18, 24, 20)
        vbox:
            spacing 8
            text ("PROMOTION OFFERED" if _success else "PROMOTION STATUS"):
                font PROFILE_FONT size 16 color _col xalign 0.5
            null height 4
            for _lbl, _pct in breakdown:
                hbox:
                    spacing 6
                    xfill True
                    text _lbl font ACT_FONT size 13 color "#9fb6d6" xsize 300
                    text ("+%d%%" % _pct) font PROFILE_FONT size 13 color "#ffd66a" xalign 1.0
            null height 4
            $ _total = sum(v for _, v in breakdown)
            hbox:
                spacing 6
                xfill True
                text "Promotion chance this shift" font PROFILE_FONT size 13 color "#cfe0f5" xsize 300
                text ("%d%%" % _total) font PROFILE_FONT size 14 color _col xalign 1.0
            null height 4
            text ("[Roll: %d vs %d]" % (promo_result.get("roll",0), promo_result.get("threshold",0))):
                font ACT_FONT size 12 color "#7090b0" xalign 0.5
            if _success:
                if promo_result.get("opportunity_only"):
                    text "Your manager wants to speak with you. Watch for the notification.":
                        font ACT_FONT size 13 color "#ffd66a" xalign 0.5
                else:
                    text "Congratulations. Promotion incoming.":
                        font PROFILE_FONT size 14 color "#7ccc60" xalign 0.5
            else:
                text "Next shift: additional consideration applied.":
                    font ACT_FONT size 12 color "#4a6080" xalign 0.5
            null height 8
            button:
                action Return()
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Continue" font PROFILE_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Promotion requirements screen (when not yet eligible) ────────────────────

screen career_promotion_requirements_scr(career_id):
    modal True
    zorder 260
    $ _status = promotion_requirements_status(career_id)
    $ _all_met = all(met for _, met, _ in _status)
    frame:
        xalign 0.5 yalign 0.45
        xsize 480
        background "#12161ef8"
        padding (24, 18, 24, 20)
        vbox:
            spacing 8
            text "PROMOTION STATUS" font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            null height 4
            for _lbl, _met, _detail in _status:
                hbox:
                    spacing 8
                    xfill True
                    text ("✓" if _met else "☐") font PROFILE_FONT size 14 color ("#7ccc60" if _met else "#8fb0d0") yalign 0.5 xsize 20
                    text _lbl font ACT_FONT size 13 color ("#7ccc60" if _met else "#cfe0f5") yalign 0.5 xsize 280
                    text ("(%s)" % _detail) font ACT_FONT size 12 color "#4a6080" xalign 1.0 yalign 0.5
            null height 8
            button:
                action Return()
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Continue" font PROFILE_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Career promotion interview (opportunity_only path) ────────────────────────

label career_promotion_interview:
    $ _ppo = store.pending_promotion_opportunity
    if _ppo is None:
        return
    $ _ppo_cid = _ppo["career_id"]
    # Expired?
    if store.day > _ppo.get("expires_day", store.day):
        "The window passed. Your manager moved on."
        # Pity +2 for missing the window
        $ _ac = dict(store.active_careers)
        $ _c  = dict(_ac.get(_ppo_cid, {}))
        $ _c["promotion_pity"] = _c.get("promotion_pity", 0) + 2
        $ _ac[_ppo_cid] = _c
        $ store.active_careers = _ac
        $ store.pending_promotion_opportunity = None
        return
    "Your manager sits across from you. This is the conversation you've been building toward."
    "They outline the new responsibilities, the adjustment in title and pay."
    menu:
        "Accept.":
            $ promote(_ppo_cid)
            "You accept. New role, new floor."
            $ store.pending_promotion_opportunity = None
        "Ask for a day to think it over.":
            $ _ppo_ext = dict(_ppo)
            $ _ppo_ext["expires_day"] = store.day + 1
            $ store.pending_promotion_opportunity = _ppo_ext
            "Your manager nods. \"Tomorrow, then.\""
    return
