# Bar challenge mini-games: pool, darts, arm wrestling.
# Phase 60: mastery system, stable rolls (anti save-scum), named NPC opponents.
#
# Max payout: Pool Professor ($110) + Darts Friday Champion ($70) + Arm Sam ($90) = $270
# (Friday only for the darts champion; on other days max is ~$235)

default bar_game_cooldowns = {}   # {game_type + "_" + opponent_id: last_day_played}
default bar_first_wins     = []   # [first_win_id, ...]

init python:

    BAR_OPPONENTS = {
        "pool": [
            {"id": "pool_reg_easy",  "label": "Bar Regular",        "difficulty": 35,
             "entry": 10,  "reward": 20,  "first_win": None},
            {"id": "pool_marcus",    "label": "Marcus",              "difficulty": 55,
             "entry": 20,  "reward": 45,  "first_win": "marcus_pool",
             "requires_met": "marcus"},
            {"id": "pool_reg_hard",  "label": "Experienced Regular", "difficulty": 65,
             "entry": 25,  "reward": 55,  "first_win": None},
            {"id": "pool_professor", "label": "The Professor",       "difficulty": 80,
             "entry": 50,  "reward": 110, "first_win": "professor_pool"},
        ],
        "darts": [
            {"id": "darts_reg",      "label": "Regular",             "difficulty": 40,
             "entry": 5,   "reward": 12,  "first_win": None},
            {"id": "darts_kai",      "label": "Kai",                 "difficulty": 60,
             "entry": 15,  "reward": 35,  "first_win": "kai_darts",
             "requires_met": "kai"},
            # Friday only: check in bar_games_scr
            {"id": "darts_champion", "label": "Friday Champion",     "difficulty": 75,
             "entry": 30,  "reward": 70,  "first_win": "darts_champion",
             "days_only": [4]},
        ],
        "arm_wrestling": [
            {"id": "arm_reg_easy",   "label": "Regular",             "difficulty": 30,
             "entry": 10,  "reward": 22,  "first_win": None},
            {"id": "arm_mike",       "label": "Big Mike",            "difficulty": 55,
             "entry": 20,  "reward": 45,  "first_win": "arm_mike"},
            {"id": "arm_sam",        "label": "Sam",                 "difficulty": 70,
             "entry": 40,  "reward": 90,  "first_win": "arm_sam_first",
             "requires_met": "sam"},
        ],
    }

    def bar_challenge_cooldown_ok(game_type, opponent_id, cooldown_days=1):
        key  = game_type + "_" + opponent_id
        last = store.bar_game_cooldowns.get(key, -99)
        return store.day - last >= cooldown_days

    def record_bar_game_result(game_type, opponent_id):
        d = dict(store.bar_game_cooldowns)
        d[game_type + "_" + opponent_id] = store.day
        store.bar_game_cooldowns = d

    def bar_games_today_count():
        return sum(1 for v in store.bar_game_cooldowns.values() if v == store.day)

    def bar_game_chance(game_type, opponent, fit_skill=0):
        """Returns (chance_data_dict, mods_list). No side effects."""
        mastery_mod = activity_mastery_modifier(game_type)
        mods = [("Mastery", mastery_mod)] if mastery_mod else []
        if game_type == "arm_wrestling" and fit_skill:
            mods.append(("Fitness", min(15, int(fit_skill * 2.5))))
        if has_player_state("confident"):
            mods.append(("Confident", +5))
        if store.need_energy < 30:
            mods.append(("Low energy", -8))
        # Phase 67: a busy bar (trivia night, an argument at the pool table)
        # means a bigger audience and sharper opponents. Modifier key only.
        _bar_att = location_event_modifier("location_bar", "bar_attendance", 0)
        if _bar_att:
            mods.append(("Busy bar", -min(8, _bar_att // 4)))
        chance_data = calculate_check_chance(
            game_type + "_" + opponent["id"],
            skill_val=0,
            difficulty=opponent["difficulty"],
            modifiers=mods,
        )
        return chance_data, mods

    def _bar_opp_available(game_type, opp):
        """True if this opponent is visible and challengeable tonight."""
        days_only = opp.get("days_only")
        if days_only and (store.day % 7) not in days_only:
            return False
        req_met = opp.get("requires_met")
        if req_met and not getattr(store, req_met + "_met", False):
            return False
        return True


# ── Screens ────────────────────────────────────────────────────────────────────

screen bar_games_scr():
    modal True
    zorder 210
    $ _games_left = max(0, 3 - bar_games_today_count())
    frame:
        xalign 0.5 yalign 0.4
        xsize 640
        background "#12161ef8"
        padding (24, 20, 24, 24)
        vbox:
            spacing 10
            text "Bar Games" font PROFILE_FONT size 22 color "#ffd66a" xalign 0.5
            $ _glc = "#7ccc60" if _games_left > 0 else "#e05050"
            text ("Games available tonight: %d / 3" % _games_left) font ACT_FONT size 13 color _glc xalign 0.5
            null height 6

            # Pool
            hbox:
                spacing 8
                text "POOL" font PROFILE_FONT size 15 color "#5bcafa" yalign 1.0
                if day % 7 in (4, 5):
                    text "(Tournament weekend)" font ACT_FONT size 12 color "#ffd66a" yalign 1.0
            for _opp in BAR_OPPONENTS["pool"]:
                if _bar_opp_available("pool", _opp):
                    $ _cd_ok  = bar_challenge_cooldown_ok("pool", _opp["id"])
                    $ _can    = _cd_ok and _games_left > 0
                    $ _cd, _  = bar_game_chance("pool", _opp, 0)
                    $ _pct    = _cd["success_or_better"]
                    $ _pcol   = "#7ccc60" if _pct >= 50 else ("#cc9040" if _pct >= 25 else "#e05050")
                    hbox:
                        xfill True yalign 0.5
                        spacing 8
                        text _opp["label"] font ACT_FONT size 13 color "#cfe0f5" xsize 200 yalign 0.5
                        text ("%d%%" % _pct) font PROFILE_FONT size 13 color _pcol xsize 50 yalign 0.5
                        if not _can:
                            text ("cooldown" if not _cd_ok else "limit reached") font ACT_FONT size 12 color "#4a6080" yalign 0.5
                        else:
                            textbutton ("Challenge — $%d" % _opp["entry"]):
                                action Return(("pool", _opp["id"]))
                                background "#1a2a3a"
                                hover_background "#1e3a5f"
                                xpadding 10 ypadding 4
                                text_font ACT_FONT text_size 12 text_color "#5bcafa" text_hover_color "#ffffff"
            null height 4

            # Darts
            hbox:
                spacing 8
                text "DARTS" font PROFILE_FONT size 15 color "#5bcafa" yalign 1.0
                if day % 7 == 4:
                    text "(Champion available tonight)" font ACT_FONT size 12 color "#ffd66a" yalign 1.0
            for _opp in BAR_OPPONENTS["darts"]:
                if _bar_opp_available("darts", _opp):
                    $ _cd_ok  = bar_challenge_cooldown_ok("darts", _opp["id"])
                    $ _can    = _cd_ok and _games_left > 0
                    $ _cd, _  = bar_game_chance("darts", _opp, 0)
                    $ _pct    = _cd["success_or_better"]
                    $ _pcol   = "#7ccc60" if _pct >= 50 else ("#cc9040" if _pct >= 25 else "#e05050")
                    hbox:
                        xfill True yalign 0.5
                        spacing 8
                        text _opp["label"] font ACT_FONT size 13 color "#cfe0f5" xsize 200 yalign 0.5
                        text ("%d%%" % _pct) font PROFILE_FONT size 13 color _pcol xsize 50 yalign 0.5
                        if not _can:
                            text ("cooldown" if not _cd_ok else "limit reached") font ACT_FONT size 12 color "#4a6080" yalign 0.5
                        else:
                            textbutton ("Challenge — $%d" % _opp["entry"]):
                                action Return(("darts", _opp["id"]))
                                background "#1a2a3a"
                                hover_background "#1e3a5f"
                                xpadding 10 ypadding 4
                                text_font ACT_FONT text_size 12 text_color "#5bcafa" text_hover_color "#ffffff"
            null height 4

            # Arm wrestling
            text "ARM WRESTLING" font PROFILE_FONT size 15 color "#5bcafa"
            for _opp in BAR_OPPONENTS["arm_wrestling"]:
                if _bar_opp_available("arm_wrestling", _opp):
                    $ _cd_ok  = bar_challenge_cooldown_ok("arm_wrestling", _opp["id"])
                    $ _can    = _cd_ok and _games_left > 0
                    $ _fit    = skill_val("fit")
                    $ _cd, _  = bar_game_chance("arm_wrestling", _opp, _fit)
                    $ _pct    = _cd["success_or_better"]
                    $ _pcol   = "#7ccc60" if _pct >= 50 else ("#cc9040" if _pct >= 25 else "#e05050")
                    hbox:
                        xfill True yalign 0.5
                        spacing 8
                        text _opp["label"] font ACT_FONT size 13 color "#cfe0f5" xsize 200 yalign 0.5
                        text ("%d%%" % _pct) font PROFILE_FONT size 13 color _pcol xsize 50 yalign 0.5
                        if not _can:
                            text ("cooldown" if not _cd_ok else "limit reached") font ACT_FONT size 12 color "#4a6080" yalign 0.5
                        else:
                            textbutton ("Challenge — $%d" % _opp["entry"]):
                                action Return(("arm_wrestling", _opp["id"]))
                                background "#1a2a3a"
                                hover_background "#1e3a5f"
                                xpadding 10 ypadding 4
                                text_font ACT_FONT text_size 12 text_color "#5bcafa" text_hover_color "#ffffff"
            null height 10
            textbutton "Leave":
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (24, 8)
                text_font PROFILE_FONT text_size 14 text_color "#9fb6d6" text_hover_color "#ffffff"


screen bar_game_confirm_scr(game_type, opp, chance_data, mods):
    modal True
    zorder 220
    $ _game_label = game_type.replace("_", " ").title()
    frame:
        xalign 0.5 yalign 0.4
        xsize 460
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text ("%s vs %s" % (_game_label, opp["label"])):
                font PROFILE_FONT size 18 color "#ffd66a" xalign 0.5
            null height 4
            hbox:
                xalign 0.5
                spacing 20
                vbox:
                    spacing 4
                    text "Entry" font ACT_FONT size 13 color "#7090b0" xalign 0.5
                    text ("$%d" % opp["entry"]) font PROFILE_FONT size 16 color "#e05050" xalign 0.5
                vbox:
                    spacing 4
                    text "Reward" font ACT_FONT size 13 color "#7090b0" xalign 0.5
                    text ("$%d" % opp["reward"]) font PROFILE_FONT size 16 color "#7ccc60" xalign 0.5
            null height 6
            # Win chance + full distribution
            $ _suc = chance_data["success_or_better"]
            text ("Win chance: %d%%" % _suc):
                font PROFILE_FONT size 16 color ("#7ccc60" if _suc >= 50 else ("#cc9040" if _suc >= 30 else "#e05050")) xalign 0.5
            frame:
                background "#0a0e15"
                padding (12, 8)
                xfill True
                vbox:
                    spacing 3
                    for _tid, _pct in [
                        ("critical",         chance_data["distribution"]["critical"]),
                        ("great",            chance_data["distribution"]["great"]),
                        ("success",          chance_data["distribution"]["success"]),
                        ("weak",             chance_data["distribution"]["weak"]),
                        ("critical_failure", chance_data["distribution"]["critical_failure"]),
                    ]:
                        hbox:
                            spacing 8
                            text ("%-14s" % tier_label(_tid)):
                                font ACT_FONT size 12 color tier_color(_tid) yalign 0.5 xsize 130
                            text ("%d%%" % _pct):
                                font ACT_FONT size 12 color "#7090b0" yalign 0.5
            if opp.get("first_win") and opp["first_win"] not in bar_first_wins:
                text "First win recorded in journal." font ACT_FONT size 12 color "#4a6080" xalign 0.5
            null height 8
            hbox:
                spacing 16
                xalign 0.5
                button:
                    action Return("confirm")
                    background "#1e3a5f"
                    hover_background "#2a5080"
                    padding (24, 8)
                    text "Challenge" font PROFILE_FONT size 15 color "#5bcafa" hover_color "#ffffff"
                button:
                    action Return("cancel")
                    background "#1a2030"
                    hover_background "#222835"
                    padding (24, 8)
                    text "Back" font ACT_FONT size 14 color "#7090b0" hover_color "#cfe0f5"


# ── Label ──────────────────────────────────────────────────────────────────────

label bar_game_play(game_type, opponent_id):
    $ _opp = next((o for o in BAR_OPPONENTS[game_type] if o["id"] == opponent_id), None)
    if _opp is None:
        return
    $ _fit      = skill_val("fit") if game_type == "arm_wrestling" else 0
    $ _cd, _mods = bar_game_chance(game_type, _opp, _fit)

    call screen bar_game_confirm_scr(game_type, _opp, _cd, _mods)
    if _return == "cancel":
        return

    # try_spend happens before roll — no checkpoint between spend and roll_check
    if not try_spend(_opp["entry"]):
        "You don't have enough for the entry fee."
        return

    # Stable roll: same attempt number on reload before this point = same result
    $ _attempt = store._check_attempts.get(game_type + "_" + opponent_id, 0) + 1
    $ _result  = roll_check(
        game_type + "_" + opponent_id,
        skill_val=0,
        difficulty=_opp["difficulty"],
        modifiers=_mods,
        attempt_number=_attempt,
        stable=True,
    )
    $ _won = _result["tier"] in ("success", "great", "critical")

    call screen check_result_scr(_result,
        title=(_opp["label"] + " — " + game_type.replace("_", " ").title()))

    if _won:
        "[_opp['label']] concedes. You collect the pot."
        $ gain_money(_opp["reward"])
        $ gain_activity_mastery(game_type, won=True)
        if _opp.get("first_win") and _opp["first_win"] not in store.bar_first_wins:
            $ store.bar_first_wins = list(store.bar_first_wins) + [_opp["first_win"]]
            $ record_game_event(
                "bar_win_" + _opp["first_win"], "social",
                "Defeated " + _opp["label"],
                journal=True,
                metadata={"game": game_type, "opponent": _opp["label"]})
            "Word travels. [_opp['label']] remembers that."
        # Rare social upside on a win (rare_outcomes.rpy). No cash, no mastery.
        $ _bar_rare = bar_game_rare(game_type, opponent_id, _result["tier"])
        if _bar_rare:
            "[_bar_rare]"
    else:
        if _result["tier"] == "critical_failure":
            "You lose badly. [_opp['label']] doesn't say anything, which is almost worse."
        else:
            "You lose. [_opp['label']] offers a nod."
        $ gain_activity_mastery(game_type, won=False)

    $ record_bar_game_result(game_type, opponent_id)
    $ spend_time(0.5)
    return
