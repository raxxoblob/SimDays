# Busking and open mic performance resolution.
# Phase 60 (corrected): two-roll system (crowd + performance), Guitar>=1 unlock.
# Skill gates are placeholder only — busking available with own_guitar + Guitar>=1.

default music_reputation = 0   # 0-100; grows via busking/open_mic/paid gigs

init python:

    CROWD_TEXT = {
        "exceptional": "An exceptional crowd gathers around you.",
        "great":       "A good crowd builds. People are stopping to listen.",
        "average":     "The usual mix of passersby.",
        "quiet":       "The park is unusually quiet today.",
        "empty":       "Almost no one around.",
    }

    # Phase 63B: crowd/perf multipliers compressed and their product capped.
    # Previously 0.1..2.0 on both axes, so a high-skill busker stacking
    # skill(+25) + mastery(+20) + guitar(+15) rolled great/critical almost every
    # time and earned x4.0 — busking hit $267/h uncapped, ~4x the best career.
    _CROWD_MULT  = {"empty": 0.15, "quiet": 0.55, "average": 1.0, "great": 1.35, "exceptional": 1.6}
    _PERF_MULT   = {"critical_failure": 0.2, "weak": 0.6, "success": 1.0, "great": 1.35, "critical": 1.6}
    _BUSK_MULT_CAP = 1.9    # ceiling on crowd_mult * perf_mult
    _BUSK_TIP_FLOOR = 3     # consolation: a bad pitch still pays bus fare
    # Reputation gain halves past 50 (same idiom as activity mastery) so rep 100
    # is a mid-game milestone (~3 weeks), not a week-2 formality.
    _PERF_REP    = {"critical_failure": -1,  "weak": 0,  "success": 1,   "great": 2,   "critical": 3}
    BUSK_DAILY_CAP = 3      # sessions per day; busking was previously uncapped

    def _busking_crowd_base(music_rep=0, day_value=None, hour_value=None):
        """Deterministic base before the random roll. Used for both roll and preview."""
        dw   = (day_value  if day_value  is not None else store.day)  % 7
        h    = int(hour_value if hour_value is not None else store.hour)
        base = 50
        if 12 <= h <= 16:    base += 10   # midday
        if dw in (4, 5, 6):  base += 10   # Fri-Sun
        if h < 10 or h > 20: base -= 15   # early/late
        base += min(15, (music_rep // 5) * 3)   # rep bonus, max +15
        base  = daily_condition_effect("busking_crowd", base)
        # Phase 67: a world event or incident in the park pulls a crowd.
        # Never checks event ids — only the modifier key.
        base += location_event_modifier("location_park", "busking_crowd", 0)
        return max(1, min(99, base))

    def _busking_crowd_chance_good(music_rep=0, day_value=None, hour_value=None):
        """P(great-or-better crowd) as integer %. Pure — no side effects."""
        base = _busking_crowd_base(music_rep, day_value, hour_value)
        # final = raw + (base - 50); good = final >= 65; raw ~ U[1,100]
        # P(good) = P(raw >= 115 - base) = max(0, base - 14)
        return max(0, min(100, base - 14))

    def _busking_crowd_roll(music_rep=0, day_value=None, hour_value=None):
        """Actual random crowd roll. Returns (tier_str, crowd_mod_int)."""
        base  = _busking_crowd_base(music_rep, day_value, hour_value)
        raw   = renpy.random.randint(1, 100)
        final = max(1, min(100, raw + (base - 50)))
        if   final >= 85: return ("exceptional", +20)
        elif final >= 65: return ("great",        +10)
        elif final >= 35: return ("average",        0)
        elif final >= 15: return ("quiet",         -10)
        else:             return ("empty",         -20)

    def _busk_followers(perf_tier, crowd_tier):
        if perf_tier in ("critical_failure", "weak"):   return 0
        if crowd_tier in ("empty", "quiet"):            return 0
        tbl = {
            ("success",  "average"):     (0,  2),
            ("success",  "great"):       (1,  4),
            ("success",  "exceptional"): (1,  5),
            ("great",    "average"):     (1,  4),
            ("great",    "great"):       (3,  8),
            ("great",    "exceptional"): (4, 12),
            ("critical", "average"):     (2,  6),
            ("critical", "great"):       (5, 14),
            ("critical", "exceptional"): (8, 20),
        }
        lo, hi = tbl.get((perf_tier, crowd_tier), (0, 0))
        return renpy.random.randint(lo, hi)

    def _busk_expected_tips(music_skill, music_rep):
        """Estimated tip range (average crowd, weak→great performance)."""
        base = music_rep * 0.40 + music_skill * 2.5
        return (max(_BUSK_TIP_FLOOR, int(base * _PERF_MULT["weak"])),
                int(base * _PERF_MULT["great"]))

    def busking_resolve(music_skill, music_rep, energy_pct):
        """Two-roll busking resolution. Returns combined result dict."""
        # Roll 1: crowd
        crowd_tier, _unused_crowd_mod = _busking_crowd_roll(music_rep)

        # Roll 2: performance
        mods = []
        if energy_pct < 30:               mods.append(("Low energy",  -8))
        if energy_pct > 70:               mods.append(("Good energy", +5))
        if has_player_state("inspired"):  mods.append(("Inspired",    +8))
        if has_player_state("confident"): mods.append(("Confident",   +3))
        _mast = activity_mastery_modifier("busking")
        if _mast != 0:                    mods.append(("Experience",  _mast))
        _gtr = equipment_modifier("guitar", "busk_perf")
        _str = strings_modifier()
        if _str != 0:                     mods.append(("Strings",     _str))
        if _gtr != 0:                     mods.append(("Guitar",      _gtr))

        perf_result = roll_check("busking", skill_val=music_skill, difficulty=45,
                                 modifiers=mods, stable=False)
        perf_tier   = perf_result["tier"]

        # Combined outcome
        # Phase 63B: rep coefficient 1.2 -> 0.40, skill 2 -> 2.5. Reputation was
        # the dominant term (120 of ~136 base at rep 100) and rep is self-fed by
        # busking itself, which made the loop a runaway.
        base_tips   = int(music_rep * 0.40 + music_skill * 2.5 + renpy.random.randint(-3, 4))
        _mult       = min(_BUSK_MULT_CAP, _CROWD_MULT[crowd_tier] * _PERF_MULT[perf_tier])
        tips        = max(_BUSK_TIP_FLOOR, int(base_tips * _mult))
        rep_gain    = _PERF_REP[perf_tier]
        if rep_gain > 0 and music_rep > 50:
            rep_gain = max(1, rep_gain // 2)
        followers   = _busk_followers(perf_tier, crowd_tier)

        # Rare outcomes live in rare_outcomes.rpy (init 25 wrapper) and are
        # stable-seeded, so they cannot be re-rolled by reloading. The old
        # unstable 8% "a promoter leaves you their card" line was removed: it
        # promised a contact that never arrived.

        # Activity mastery: win = success-or-better performance
        gain_activity_mastery("busking", won=(perf_tier in ("success", "great", "critical")))

        # Phase 67/68: a strong public set is something the city can hear about,
        # and may generate a venue lead (mail only — never a direct payout).
        if perf_tier in ("great", "critical") and crowd_tier in ("great", "exceptional"):
            publish_player_fact("public_performance", "park_d%d" % store.day)
        maybe_rare_opportunity("busking")

        return {
            "crowd_tier":  crowd_tier,
            "crowd_text":  CROWD_TEXT[crowd_tier],
            "perf_result": perf_result,
            "perf_tier":   perf_tier,
            "tips":        tips,
            "followers":   followers,
            "rep_gain":    rep_gain,
            "xp_base":     18,   # always guaranteed
            "rare":        None, # filled by the rare_outcomes.rpy wrapper
        }

    def open_mic_resolve(music_skill, music_rep, rehearsed, energy_pct,
                          modifiers_extra=None):
        """Full open mic performance result."""
        mods = []
        if rehearsed:                       mods.append(("Rehearsed setlist", +8))
        if energy_pct < 30:                 mods.append(("Low energy",        -7))
        if energy_pct > 70:                 mods.append(("Good energy",       +4))
        if has_player_state("inspired"):    mods.append(("Inspired",          +8))
        if has_player_state("confident"):   mods.append(("Confident",         +5))
        _omg = equipment_modifier("guitar", "busk_perf")
        _ostr = strings_modifier()
        if _ostr != 0:                      mods.append(("Strings",           _ostr))
        _ojkt = dressed_for("music_performance")
        if _ojkt > 0:                       mods.append(("Stage clothes",     _ojkt))
        if _omg != 0:                       mods.append(("Guitar",            _omg))
        if modifiers_extra:                 mods.extend(modifiers_extra)

        result = roll_check("open_mic", skill_val=music_skill, difficulty=55,
                            modifiers=mods, stable=False)
        tier = result["tier"]

        rep_gain  = {"critical_failure": -3, "weak":  0, "success":  5,
                     "great": 10, "critical": 18}[tier]
        followers = {"critical_failure":  0, "weak":  1, "success":  6,
                     "great": 15, "critical": 30}[tier]
        tips      = max(0, {"critical_failure": 0, "weak": 5, "success": 15,
                            "great": 30, "critical": 55}[tier] + renpy.random.randint(-5, 5))

        # See busking_resolve: rare outcomes are layered on in rare_outcomes.rpy.
        # The old 15% "a new opportunity may open" line is gone — venue_invitation
        # / promoter_notice actually open one now.

        return {
            "result":    result,
            "tier":      tier,
            "rep_gain":  rep_gain,
            "followers": followers,
            "tips":      tips,
            "xp_base":   25,   # always guaranteed; larger than busking
            "rare":      None, # filled by the rare_outcomes.rpy wrapper
        }


# ── Screens ────────────────────────────────────────────────────────────────────

screen busking_preview_scr(crowd_chance, perf_great_chance, tips_low, tips_high):
    modal True
    zorder 280
    frame:
        xalign 0.5 yalign 0.4
        xsize 480
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text "BUSKING" font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            null height 6
            hbox:
                spacing 8 xalign 0.5
                text "Good-or-better crowd:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text ("[crowd_chance]%%") font PROFILE_FONT size 14 color "#ffd66a" yalign 0.5
            hbox:
                spacing 8 xalign 0.5
                text "Great-or-better performance:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text ("[perf_great_chance]%%") font PROFILE_FONT size 14 color "#ffd66a" yalign 0.5
            null height 4
            hbox:
                spacing 8 xalign 0.5
                text "Expected tips:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text ("$[tips_low] – $[tips_high]") font PROFILE_FONT size 13 color "#7ccc60" yalign 0.5
            hbox:
                spacing 8 xalign 0.5
                text "Guitar XP:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text "guaranteed" font PROFILE_FONT size 13 color "#5bcafa" yalign 0.5
            null height 4
            text rare_preview_line("busking"):
                font ACT_FONT size 12 color "#ffd66a" xalign 0.5
            null height 8
            hbox:
                spacing 16 xalign 0.5
                button:
                    action Return(True)
                    background "#1e3a5f"
                    padding (20, 8)
                    text "Perform — 1.5h" font PROFILE_FONT size 13 color "#5bcafa" hover_color "#ffffff"
                button:
                    action Return(False)
                    background "#241824"
                    padding (20, 8)
                    text "Cancel" font PROFILE_FONT size 13 color "#9090a0" hover_color "#ffffff"


screen busking_result_scr(perf):
    modal True
    zorder 290
    $ _pt  = perf["perf_tier"]
    $ _ct  = perf["crowd_tier"]
    $ _col = tier_color(_pt)
    frame:
        xalign 0.5 yalign 0.4
        xsize 460
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 8
            text "Busking" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            # Crowd tier row
            hbox:
                spacing 8 xalign 0.5
                text "Crowd:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text _ct.capitalize() font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5
            text perf["crowd_text"] font ACT_FONT size 12 color "#7090b0" xalign 0.5
            null height 4
            # Performance tier
            hbox:
                spacing 8 xalign 0.5
                text "Performance:" font ACT_FONT size 13 color "#7090b0" yalign 0.5
                text tier_label(_pt) font PROFILE_FONT size 20 color _col yalign 0.5
            null height 6
            hbox:
                spacing 10 xalign 0.5
                text "Tips" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                text ("$%d" % perf["tips"]) font PROFILE_FONT size 16 color "#ffd66a" yalign 0.5
            if perf["followers"] > 0:
                hbox:
                    spacing 10 xalign 0.5
                    text "New followers" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                    text ("+%d" % perf["followers"]) font PROFILE_FONT size 14 color "#7ccc60" yalign 0.5
            if perf["rep_gain"] != 0:
                hbox:
                    spacing 10 xalign 0.5
                    text "Reputation" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                    $ _rsign = "+" if perf["rep_gain"] > 0 else ""
                    text ("[_rsign][perf['rep_gain']]") font PROFILE_FONT size 14 color ("#7ccc60" if perf["rep_gain"] > 0 else "#e05050") yalign 0.5
            hbox:
                spacing 10 xalign 0.5
                text "Guitar XP" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                text ("+%d guaranteed" % perf["xp_base"]) font PROFILE_FONT size 14 color "#5bcafa" yalign 0.5
            $ _nm = near_miss_line(perf["perf_result"])
            if _nm:
                text _nm font ACT_FONT size 12 color "#7090b0" xalign 0.5
            if perf.get("rare"):
                use rare_reveal_row(perf["rare"])
            null height 8
            button:
                action Return()
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Continue" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"


screen open_mic_result_scr(perf):
    modal True
    zorder 290
    $ _res  = perf["result"]
    $ _tier = _res["tier"]
    $ _col  = tier_color(_tier)
    frame:
        xalign 0.5 yalign 0.4
        xsize 460
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text "Open Mic" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            null height 4
            text tier_label(_tier) font PROFILE_FONT size 22 color _col xalign 0.5
            null height 6
            hbox:
                spacing 10 xalign 0.5
                text "Tips" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                text ("$%d" % perf["tips"]) font PROFILE_FONT size 16 color "#ffd66a" yalign 0.5
            hbox:
                spacing 10 xalign 0.5
                text "Followers" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                text ("+%d" % perf["followers"]) font PROFILE_FONT size 14 color "#7ccc60" yalign 0.5
            if perf["rep_gain"] != 0:
                hbox:
                    spacing 10 xalign 0.5
                    text "Reputation" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                    $ _rsign = "+" if perf["rep_gain"] > 0 else ""
                    text ("[_rsign][perf['rep_gain']]") font PROFILE_FONT size 14 color ("#7ccc60" if perf["rep_gain"] > 0 else "#e05050") yalign 0.5
            hbox:
                spacing 10 xalign 0.5
                text "Guitar XP" font ACT_FONT size 14 color "#9fb6d6" yalign 0.5
                text ("+%d guaranteed" % perf["xp_base"]) font PROFILE_FONT size 14 color "#5bcafa" yalign 0.5
            $ _nm = near_miss_line(_res)
            if _nm:
                text _nm font ACT_FONT size 12 color "#7090b0" xalign 0.5
            if perf.get("keepsake"):
                text ("Keepsake: " + possession_name(perf["keepsake"])):
                    font ACT_FONT size 13 color "#ffd66a" xalign 0.5
            if perf.get("rare"):
                use rare_reveal_row(perf["rare"])
            null height 8
            button:
                action Return()
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Continue" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"


# ── Labels ─────────────────────────────────────────────────────────────────────

label busking_performance:
    # Phase 63B: busking was uncapped per day — the optimizer ran 8+ sessions a
    # day and out-earned every other path combined. Cap matches bar games (3/day).
    if activity_use_count_today("busking") >= BUSK_DAILY_CAP:
        "You've played the good pitches out for today. Come back tomorrow."
        return
    $ _music_sk   = skill_val("music")
    $ _music_rep  = store.music_reputation
    $ _energy_pct = int(store.need_energy)
    $ _dur = 1.5

    if store.show_check_odds:
        $ _crowd_chance  = _busking_crowd_chance_good(music_rep=_music_rep)
        $ _perf_mods = (
            ([("Low energy",  -8)] if _energy_pct < 30 else []) +
            ([("Good energy", +5)] if _energy_pct > 70 else []) +
            ([("Inspired",    +8)] if has_player_state("inspired")  else []) +
            ([("Confident",   +3)] if has_player_state("confident") else []) +
            ([("Experience",  activity_mastery_modifier("busking"))] if activity_mastery_modifier("busking") != 0 else [])
        )
        $ _perf_ch       = calculate_check_chance("busking", _music_sk, 45, _perf_mods)
        $ _great_chance  = _perf_ch["distribution"].get("great", 0) + _perf_ch["distribution"].get("critical", 0)
        $ _tips_lo, _tips_hi = _busk_expected_tips(_music_sk, _music_rep)
        call screen busking_preview_scr(_crowd_chance, _great_chance, _tips_lo, _tips_hi)
        if not _return:
            return

    $ _perf = busking_resolve(_music_sk, _music_rep, _energy_pct)

    "[_perf['crowd_text']]"

    call screen busking_result_scr(_perf)

    # Apply outcomes
    $ gain_money(_perf["tips"])
    $ gain_skill_practice("music", _perf["xp_base"], _dur)
    $ store.music_reputation = max(0, min(100, store.music_reputation + _perf["rep_gain"]))
    $ mark_activity_used_today("busking")
    $ spend_time(_dur)

    if store._pending_breakthrough:
        $ _bt = store._pending_breakthrough
        $ store._pending_breakthrough = None
        "[SKILL_LABEL_FOR[_bt['skill']]] breakthrough! +[_bt['bonus']] bonus XP."

    if _perf.get("rare"):
        "[_perf['rare']]"

    return


label open_mic_performance:
    $ _music_sk  = skill_val("music")
    $ _music_rep = store.music_reputation
    $ _energy_pct = int(store.need_energy)

    # Content gate: Guitar >= 4 AND music_reputation >= 8
    if _music_sk < 4:
        "You need more guitar practice before taking the open mic stage."
        return
    if _music_rep < 8:
        "You need more local reputation first. Try busking to build your following."
        return

    $ _om_mods = (
        ([("Low energy",  -7)] if _energy_pct < 30 else []) +
        ([("Good energy", +4)] if _energy_pct > 70 else []) +
        ([("Inspired",    +8)] if has_player_state("inspired")  else []) +
        ([("Confident",   +5)] if has_player_state("confident") else [])
    )

    $ _odds_now = calculate_check_chance("open_mic", _music_sk, 55, _om_mods)
    $ _reh_before, _reh_after = preview_preparation_delta("open_mic", _music_sk, 55, _om_mods, "Rehearsed setlist", +8)
    show screen check_distribution_scr(_odds_now, "Open Mic Odds")
    "The venue is filling up.  Success: [_odds_now['success_or_better']]%%  |  Rehearsed: [_reh_after]%%"

    menu:
        "Rehearse your setlist (2h)":
            if too_tired():
                "You're too worn out to rehearse properly."
                hide screen check_distribution_scr
                return
            $ spend_time(2)
            $ store.need_energy = max(0, store.need_energy - 20)
            "You run through your set twice. Fingers know where to go."
            $ _rehearsed = True
        "Take the stage now":
            $ _rehearsed = False

    hide screen check_distribution_scr

    $ _dur = 2.0
    $ _perf = open_mic_resolve(_music_sk, _music_rep, _rehearsed, _energy_pct)

    call screen open_mic_result_scr(_perf)

    $ gain_money(_perf["tips"])
    $ gain_skill_practice("music", _perf["xp_base"], _dur)
    $ store.music_reputation = max(0, min(100, store.music_reputation + _perf["rep_gain"]))
    $ spend_time(_dur)

    if store._pending_breakthrough:
        $ _bt = store._pending_breakthrough
        $ store._pending_breakthrough = None
        "[SKILL_LABEL_FOR[_bt['skill']]] breakthrough! +[_bt['bonus']] bonus XP."

    if _perf.get("rare"):
        "[_perf['rare']]"

    return
