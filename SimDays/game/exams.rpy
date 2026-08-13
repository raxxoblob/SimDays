# Certification exams. Phase 60D.
# Accessible from phone portfolio screen and library/college study area.
# Failing is cheap (pity accrues); passing gives freelance rep boost and job access.

default certifications_earned = []
default exam_attempts          = {}

init python:

    EXAM_DEFS = {
        "prog_cert_1": {
            "label":       "Junior Programming Certificate",
            "skill":       "prog",
            "min_skill":   3,
            "difficulty":  50,
            "cost":        85,
            "prep_bonus":  10,
            "prereq":      None,
            "reward":      {"freelance_rep": 5},
            "description": "Recognized by local employers. Opens entry-level IT roles.",
        },
        "prog_cert_2": {
            "label":       "Mid-level Programming Certificate",
            "skill":       "prog",
            "min_skill":   5,
            "difficulty":  58,
            "cost":        150,
            "prep_bonus":  12,
            "prereq":      "prog_cert_1",
            "reward":      {"freelance_rep": 8},
        },
        "biz_cert_1": {
            "label":       "Business Fundamentals Certificate",
            "skill":       "biz",
            "min_skill":   3,
            "difficulty":  48,
            "cost":        75,
            "prep_bonus":  10,
            "prereq":      None,
            "reward":      {},
        },
        "med_cert_1": {
            "label":       "First Aid and Basic Clinical Certificate",
            "skill":       "med",
            "min_skill":   2,
            "difficulty":  45,
            "cost":        95,
            "prep_bonus":  12,
            "prereq":      None,
            "reward":      {},
        },
    }

    def exam_eligible(exam_id):
        ex = EXAM_DEFS[exam_id]
        if exam_id in store.certifications_earned: return False
        if ex.get("prereq") and ex["prereq"] not in store.certifications_earned: return False
        return skill_val(ex["skill"]) >= ex["min_skill"]

    def exam_chance(exam_id):
        ex = EXAM_DEFS[exam_id]
        sk_val   = skill_val(ex["skill"])
        attempts = store.exam_attempts.get(exam_id, 0)
        mods = []
        if attempts > 0:
            mods.append(("Exam experience", min(15, attempts * 5)))
        if getattr(store, "exam_prepped_" + exam_id, False):
            mods.append(("Recent prep",     ex["prep_bonus"]))
        if store.need_energy < 30:         mods.append(("Tired",    -8))
        if has_player_state("focused"):    mods.append(("Focused",  +5))
        return calculate_check_chance(exam_id, sk_val, ex["difficulty"], mods)

    def attempt_exam(exam_id):
        """Returns (result_dict, passed_bool, error_str|None)."""
        ex = EXAM_DEFS[exam_id]
        if not exam_eligible(exam_id):
            return None, False, "Not eligible for this exam."
        if not try_spend(ex["cost"]):
            return None, False, "Not enough money ($%d required)." % ex["cost"]
        chance_data = exam_chance(exam_id)
        sk_val = skill_val(ex["skill"])
        mods   = [(l, v) for l, v in chance_data["modifier_lines"]
                  if l not in ("Skill", "Difficulty", "Prev. experience")]
        result = roll_check(exam_id, sk_val, ex["difficulty"], mods, stable=False)
        # Increment attempt counter
        d = dict(store.exam_attempts)
        d[exam_id] = d.get(exam_id, 0) + 1
        store.exam_attempts = d
        # Reset prep flag
        setattr(store, "exam_prepped_" + exam_id, False)
        passed = result["tier"] in ("success", "great", "critical")
        if passed and exam_id not in store.certifications_earned:
            store.certifications_earned = list(store.certifications_earned) + [exam_id]
            for k, v in ex["reward"].items():
                if k == "freelance_rep":
                    store.freelance_reputation = min(100, getattr(store, "freelance_reputation", 0) + v)
            record_game_event("cert_%s_day%d" % (exam_id, store.day),
                              "achievement", ex["label"], summary=True, journal=True)
        return result, passed, None

    def set_exam_prepared(exam_id):
        """Mark as prepped (call after study session). Costs are handled by caller."""
        setattr(store, "exam_prepped_" + exam_id, True)

    # ── NPC help requests ─────────────────────────────────────────────────────
    NPC_HELP_REQUESTS = {
        "eli_computer_issue": {
            "npc": "eli", "skill": "prog", "difficulty": 45,
            "text": "Eli's IDE is having a weird issue. She's been staring at it for twenty minutes.",
            "on_success_memory": ("eli_help_comp",      "You helped me fix that IDE issue."),
            "on_fail_memory":    ("eli_help_comp_fail", "You tried to help with my computer thing."),
            "on_success_rel":    ("trust", 4),
            "on_fail_rel":       ("trust", 1),
        },
        "marcus_sound_issue": {
            "npc": "marcus", "skill": "mech", "difficulty": 40,
            "text": "The speaker at Static is cutting out. Marcus is eyeing it suspiciously.",
            "on_success_memory": ("marcus_help_sound",      "You sorted out that speaker issue."),
            "on_fail_memory":    ("marcus_help_sound_fail", "You had a look at the speaker thing."),
            "on_success_rel":    ("affection", 3),
            "on_fail_rel":       ("affection", 1),
        },
        "nora_schedule_help": {
            "npc": "nora", "skill": "biz", "difficulty": 38,
            "text": "Nora is trying to figure out a shift schedule. It's gotten complicated.",
            "on_success_memory": ("nora_help_schedule",      "You helped me work out that shift nightmare."),
            "on_fail_memory":    ("nora_help_schedule_fail", "You tried to help with the schedule."),
            "on_success_rel":    ("trust", 4),
            "on_fail_rel":       ("trust", 1),
        },
        "zoe_computer_setup": {
            "npc": "zoe", "skill": "prog", "difficulty": 35,
            "text": "Zoe's laptop is being difficult. She doesn't know where to start.",
            "on_success_memory": ("zoe_help_laptop",      "You fixed my laptop. I owe you."),
            "on_fail_memory":    ("zoe_help_laptop_fail", "You tried to fix my laptop."),
            "on_success_rel":    ("affection", 3),
            "on_fail_rel":       ("affection", 1),
        },
    }

    def npc_help_available(req_id):
        """True if relevant NPC is met, player has skill>=2, no cooldown."""
        req = NPC_HELP_REQUESTS[req_id]
        npc = req["npc"]
        met_flag = npc + "_met"
        if not getattr(store, met_flag, False): return False
        if skill_val(req["skill"]) < 2: return False
        last = store.world_challenge_history.get("npc_help_" + req_id, {}).get("last_day", -99)
        return store.day - last >= 1  # once per day

    def attempt_npc_help(req_id):
        """Rolls the check (qualitative display). Returns (result, won, req)."""
        req    = NPC_HELP_REQUESTS[req_id]
        sk     = req["skill"]
        sk_val = skill_val(sk)
        result = roll_check("npc_help_" + req_id, sk_val, req["difficulty"], stable=False)
        won    = result["tier"] in ("success", "great", "critical")
        # Record cooldown reuse of world_challenge_history
        d = dict(store.world_challenge_history)
        d["npc_help_" + req_id] = {"last_day": store.day}
        store.world_challenge_history = d
        # Apply relationship effects (guaranteed regardless of outcome — trying always counts)
        npc   = req["npc"]
        rel_k, rel_v = req["on_success_rel"] if won else req["on_fail_rel"]
        if rel_k == "trust":
            _aff_attr = npc + "_trust"
        else:
            _aff_attr = npc + "_affection"
        if hasattr(store, _aff_attr):
            setattr(store, _aff_attr,
                    min(100, getattr(store, _aff_attr, 0) + rel_v))
        # Skill XP (struggle = learned)
        gain_skill(sk, 3 if won else 5)
        return result, won, req


# ── Exams screen ──────────────────────────────────────────────────────────────

screen exams_scr():
    modal True
    zorder 210
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 620
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 8
            text "CERTIFICATIONS" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            null height 4
            viewport:
                xfill True
                ysize 360
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    for _eid, _ex in EXAM_DEFS.items():
                        $ _earned = _eid in store.certifications_earned
                        $ _elig   = exam_eligible(_eid)
                        $ _echance = exam_chance(_eid)
                        frame:
                            xfill True
                            background ("#1a3a1a" if _earned else "#1a2230")
                            padding (14, 10, 14, 10)
                            vbox:
                                spacing 4
                                hbox:
                                    spacing 8
                                    text ("✓ " if _earned else "") font PROFILE_FONT size 13 color "#7ccc60" yalign 0.5
                                    text _ex["label"] font PROFILE_FONT size 14 color ("#7ccc60" if _earned else "#cfe0f5") yalign 0.5
                                hbox:
                                    spacing 16
                                    text ("Skill req: %d" % _ex["min_skill"]) font ACT_FONT size 12 color ("#7fd06a" if skill_val(_ex["skill"]) >= _ex["min_skill"] else "#e8a24d")
                                    text ("Fee: $%d" % _ex["cost"]) font ACT_FONT size 12 color "#8fb0d0"
                                    if not _earned:
                                        text ("Pass chance: %d%%" % _echance["success_or_better"]) font ACT_FONT size 12 color "#ffd66a"
                                if _ex.get("description"):
                                    text _ex["description"] font ACT_FONT size 12 color "#4a6080"
                                if not _earned and _elig:
                                    $ _attempts_count = store.exam_attempts.get(_eid, 0)
                                    if _attempts_count > 0:
                                        text ("Previous attempts: %d (+%d%% bonus)" % (_attempts_count, min(15, _attempts_count*5))) font ACT_FONT size 12 color "#4a8a6a"
                                    button:
                                        action [Function(attempt_exam, _eid), Return(_eid)]
                                        background "#1e3a5f"
                                        padding (12, 6)
                                        xalign 1.0
                                        text ("Sit exam ($%d)" % _ex["cost"]) font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Close" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"
