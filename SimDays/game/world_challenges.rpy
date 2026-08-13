# World challenges — persistent mini-goals the player can see from early in the game.
# Not quests. No quest markers. Just a visible number that changes over time.
# Phase 60D.

default world_challenge_history = {}

init python:

    WORLD_CHALLENGES = {
        "beat_sam_record": {
            "label":       "Beat Sam's lifting record",
            "category":    "gym",
            "skill":       "fit",
            "difficulty":  75,
            "reward_tier": {
                "success":  {"label": "You match her record.", "rep": 2},
                "great":    {"label": "You beat it by a margin.", "rep": 3, "confidence": True},
                "critical": {"label": "New gym record.", "rep": 5, "confidence": True, "journal": True},
            },
            "first_win_npc": "sam",
            "cooldown_days": 3,
        },
        "beat_professor_pool": {
            "label":       "Beat The Professor at pool",
            "category":    "bar_games",
            "skill":       None,
            "mastery_key": "pool",
            "difficulty":  80,
            "reward_tier": {
                "success":  {"label": "You finally beat him.", "money": 110, "journal": True},
                "great":    {"label": "You win cleanly.", "money": 110, "rep": 3, "journal": True},
                "critical": {"label": "He tips his cue to you.", "money": 110, "rep": 5, "journal": True},
            },
            # Phase 63B: 1 -> 4 days. This is the only cash-paying world
            # challenge; at a 1-day cooldown it was the best $/hour in the game.
            "cooldown_days": 4,
        },
        "nail_difficult_song": {
            "label":       "Play the hardest song you know cleanly",
            "category":    "music",
            "skill":       "music",
            "difficulty":  60,
            "reward_tier": {
                "success":  {"label": "You play it through.", "xp": 15},
                "great":    {"label": "Better than ever.", "xp": 20, "music_rep": 2},
                "critical": {"label": "Perfect run.", "xp": 25, "music_rep": 4, "confidence": True},
            },
            "unlock_req":  {"music": 4},
            "cooldown_days": 2,
        },
        "complete_advanced_challenge": {
            "label":       "Solve a self-imposed advanced coding challenge",
            "category":    "programming",
            "skill":       "prog",
            "difficulty":  65,
            "reward_tier": {
                "success":  {"label": "You work through it.", "xp": 12},
                "great":    {"label": "Clean solution.", "xp": 18},
                "critical": {"label": "Elegant.", "xp": 25, "portfolio": "prog_challenge"},
            },
            "unlock_req":  {"prog": 5},
            "cooldown_days": 2,
        },
        "local_race_top3": {
            "label":       "Place top 3 in a local 5km race",
            "category":    "fitness",
            "skill":       "fit",
            "difficulty":  70,
            "reward_tier": {
                "success":  {"label": "You finish in the top 3.", "rep": 3, "journal": True},
                "great":    {"label": "Strong finish.", "rep": 4, "confidence": True},
                "critical": {"label": "Personal best. Top finish.", "rep": 6, "journal": True, "confidence": True},
            },
            "unlock_req":  {"fit": 3},
            "event_only":  True,
            "cooldown_days": 7,
        },
        "complete_hardest_recipe": {
            "label":       "Complete the most difficult recipe you know",
            "category":    "culinary",
            "skill":       "cook",
            "difficulty":  65,
            "reward_tier": {
                "success":  {"label": "It works.", "xp": 12},
                "great":    {"label": "Better than expected.", "xp": 18},
                "critical": {"label": "Restaurant quality.", "xp": 25, "confidence": True, "journal": True},
            },
            "unlock_req":  {"cook": 4},
            "cooldown_days": 2,
        },
        # ── Phase 61 signature aspirational challenges ─────────────────────────
        "signature_dish_master": {
            "label":       "Master a high-difficulty signature dish",
            "category":    "culinary",
            "skill":       "cook",
            "difficulty":  78,
            "reward_tier": {
                "success":  {"label": "You nail it.", "xp": 18},
                "great":    {"label": "Refined and clean.", "xp": 24, "confidence": True},
                "critical": {"label": "A dish worth a restaurant's name.", "xp": 30,
                             "portfolio": "culinary", "journal": True, "confidence": True, "rep": 2},
            },
            "unlock_req":  {"cook": 5},
            "cooldown_days": 3,
        },
        "restore_showpiece": {
            "label":       "Restore a badly damaged showpiece",
            "category":    "mechanics",
            "skill":       "mech",
            "difficulty":  76,
            "reward_tier": {
                "success":  {"label": "It runs again.", "xp": 16},
                "great":    {"label": "Better than it left the factory.", "xp": 22, "rep": 2},
                "critical": {"label": "Museum-grade restoration.", "xp": 28, "rep": 4,
                             "journal": True, "confidence": True},
            },
            "unlock_req":  {"mech": 4},
            "cooldown_days": 3,
        },
        "hard_technical_challenge": {
            "label":       "Complete a high-difficulty technical challenge",
            "category":    "programming",
            "skill":       "prog",
            "difficulty":  78,
            "reward_tier": {
                "success":  {"label": "Solved.", "xp": 18},
                "great":    {"label": "Efficient and clean.", "xp": 24},
                "critical": {"label": "A publishable solution.", "xp": 32,
                             "portfolio": "programming", "journal": True, "confidence": True},
            },
            "unlock_req":  {"prog": 5},
            "cooldown_days": 3,
        },
        # ── Phase 65 ──────────────────────────────────────────────────────────
        # The aspirational version of the gallery exhibition city event: not
        # "enter a show" but "win one". Gated on reputation as well as skill,
        # so it only appears once the player is genuinely part of the scene.
        "first_exhibition_win": {
            "label":       "Win a local art exhibition",
            "category":    "art",
            "skill":       "art",
            "difficulty":  72,
            "reward_tier": {
                "success":  {"label": "You take a place.", "xp": 15, "art_rep": 5, "journal": True},
                "great":    {"label": "Second on the wall, and people ask who you are.",
                             "xp": 20, "art_rep": 8, "portfolio": "art", "journal": True},
                "critical": {"label": "First. Your name on the card by the door.",
                             "xp": 28, "art_rep": 12, "money": 200,
                             "portfolio": "art", "journal": True, "confidence": True},
            },
            "unlock_req":  {"art": 4, "art_rep": 8},
            "hours": 3.0,
            "energy": 20,
            "cooldown_days": 14,
        },
    }

    def world_challenge_chance(challenge_id):
        ch = WORLD_CHALLENGES[challenge_id]
        sk = ch.get("skill")
        sk_val = skill_val(sk) if sk else 0
        mastery_mod = activity_mastery_modifier(ch["mastery_key"]) if ch.get("mastery_key") else 0
        mods = []
        if mastery_mod:                    mods.append(("Mastery",     mastery_mod))
        if has_player_state("confident"):  mods.append(("Confident",   +5))
        if has_player_state("inspired"):   mods.append(("Inspired",    +5))
        if store.need_energy < 30:         mods.append(("Low energy",  -8))
        return calculate_check_chance(challenge_id, sk_val, ch["difficulty"], mods)

    # unlock_req keys that are NOT skills — read straight off the store instead.
    # Phase 65 added the first one (art_rep); keep this table, not an if-chain.
    _WC_NON_SKILL_REQ = {"art_rep": "art_reputation"}

    def world_challenge_visible(challenge_id):
        ch = WORLD_CHALLENGES[challenge_id]
        for key, min_lv in ch.get("unlock_req", {}).items():
            if key in _WC_NON_SKILL_REQ:
                if getattr(store, _WC_NON_SKILL_REQ[key], 0) < min_lv:
                    return False
            elif skill_val(key) < min_lv:
                return False
        return True

    def world_challenge_available(challenge_id):
        if not world_challenge_visible(challenge_id): return False
        ch = WORLD_CHALLENGES[challenge_id]
        if ch.get("event_only"): return False
        last = store.world_challenge_history.get(challenge_id, {}).get("last_day", -99)
        return store.day - last >= ch.get("cooldown_days", 1)

    def attempt_world_challenge(challenge_id):
        """Returns (result_dict, won_bool). Applies all rewards directly."""
        ch = WORLD_CHALLENGES[challenge_id]
        chance_data = world_challenge_chance(challenge_id)
        sk = ch.get("skill")
        sk_val = skill_val(sk) if sk else 0
        mods = [(l, v) for l, v in chance_data["modifier_lines"]
                if l not in ("Skill", "Difficulty", "Prev. experience")]
        result = roll_check(challenge_id, sk_val, ch["difficulty"], mods, stable=False)

        # Phase 63B: attempts were free — no time, no energy, no cost. Combined
        # with beat_professor_pool's flat $110 on a 1-day cooldown that is an
        # unbounded money source the moment the screen gets an entry point.
        spend_time(ch.get("hours", 1.0))
        store.need_energy = max(0, store.need_energy - ch.get("energy", 10))

        d = dict(store.world_challenge_history)
        entry = dict(d.get(challenge_id, {"attempts": 0, "wins": 0, "last_day": -99}))
        entry["attempts"] += 1
        entry["last_day"] = store.day
        won = result["tier"] in ("success", "great", "critical")

        if won:
            entry["wins"] = entry.get("wins", 0) + 1
            if entry["wins"] == 1:
                entry["first_win_day"] = store.day
            # Apply tier rewards
            tier = result["tier"]
            rewards = ch["reward_tier"].get(tier, ch["reward_tier"].get("success", {}))
            if rewards.get("money"):     gain_money(rewards["money"])
            if rewards.get("xp") and sk: gain_skill_practice(sk, rewards["xp"], 1)
            if rewards.get("music_rep"): store.music_reputation = min(100, store.music_reputation + rewards["music_rep"])
            if rewards.get("art_rep"):   gain_art_rep(rewards["art_rep"])
            if rewards.get("rep"):       store.freelance_reputation = min(100, store.freelance_reputation + rewards["rep"])
            if rewards.get("confidence"):add_player_state("confident", "wc_" + challenge_id + "_" + str(store.day))
            # First-win milestone fires exactly once (duplicate-safe unique id).
            if entry["wins"] == 1:
                if rewards.get("portfolio"):
                    record_game_event("wc_%s_firstwin" % challenge_id,
                                      "project", ch["label"], summary=True,
                                      journal=rewards.get("journal", False),
                                      portfolio_domain=rewards["portfolio"],
                                      metadata={"challenge": challenge_id})
                elif rewards.get("journal"):
                    record_game_event("wc_%s_firstwin" % challenge_id,
                                      "career", ch["label"], summary=True, journal=True,
                                      metadata={"challenge": challenge_id})

        else:
            # Phase 63B consolation: a failed attempt cost time and energy and
            # previously returned nothing at all. Award a floor of practice XP.
            if sk:
                _base = ch["reward_tier"].get("success", {}).get("xp", 0)
                gain_skill_practice(sk, max(1, _base // 3), 1)

        d[challenge_id] = entry
        store.world_challenge_history = d
        return result, won


# ── World challenges screen ───────────────────────────────────────────────────

screen world_challenges_scr():
    modal True
    zorder 210
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 660
        ysize 520
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 8
            text "YOUR CHALLENGES" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            null height 4
            viewport:
                xfill True
                ysize 400
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    for _cid, _ch in WORLD_CHALLENGES.items():
                        if world_challenge_visible(_cid):
                            $ _avail = world_challenge_available(_cid)
                            $ _hist  = store.world_challenge_history.get(_cid, {})
                            $ _wch   = world_challenge_chance(_cid)
                            $ _last_day = _hist.get("last_day", -99)
                            $ _cooldown = _ch.get("cooldown_days", 1)
                            $ _days_cd  = max(0, _cooldown - (day - _last_day))
                            frame:
                                xfill True
                                background "#1a2230"
                                padding (14, 10, 14, 10)
                                hbox:
                                    spacing 12
                                    xfill True
                                    vbox:
                                        spacing 3
                                        xsize 360
                                        text _ch["label"] font PROFILE_FONT size 14 color "#cfe0f5"
                                        hbox:
                                            spacing 12
                                            text ("Attempts: %d" % _hist.get("attempts", 0)) font ACT_FONT size 12 color "#7090b0"
                                            if _hist.get("wins", 0) > 0:
                                                text ("Best win: Day %d" % _hist.get("first_win_day", day)) font ACT_FONT size 12 color "#7ccc60"
                                    vbox:
                                        spacing 4
                                        xalign 1.0
                                        text ("%d%% chance" % _wch["success_or_better"]) font PROFILE_FONT size 13 color "#ffd66a" xalign 1.0
                                        if _avail:
                                            button:
                                                action [Function(attempt_world_challenge, _cid), Return(_cid)]
                                                background "#1e3a5f"
                                                padding (12, 6)
                                                text "Attempt" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff" xalign 0.5
                                        else:
                                            if _ch.get("event_only"):
                                                text "(event only)" font ACT_FONT size 12 color "#4a6080" xalign 1.0
                                            else:
                                                text ("Cooldown: %dd" % _days_cd) font ACT_FONT size 12 color "#4a6080" xalign 1.0
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Close" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"
