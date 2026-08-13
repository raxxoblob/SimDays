# ═══════════════════════════════════════════════════════════════════
# SCENE TESTER — DEVELOPER ONLY
# ═══════════════════════════════════════════════════════════════════
# Access: F9 / ` / Shift+D → debug menu → "▶  Scene Tester".
# Nothing in normal play reaches this screen: the only entry point is the
# debug menu, and the screen itself no-ops unless config.developer.
#
# HOW IT LAUNCHES A SCENE
# Preset (a plain python function) sets state, then Jump() goes straight
# to the shipping label — the same mechanism debug_summer_festival.rpy
# already uses ("Start festival directly"). No new context: these scenes
# end with `jump map` / `jump cafe_actions`, i.e. they hand control back
# to the normal game loop themselves. Wrapping them in
# renpy.call_in_new_context() would run the whole game inside the nested
# context and never return, so it is deliberately NOT used here.
#
# STATE SAFETY
# - Presets SET state before the scene runs.
# - The scene's own mutations (nora_cover_shift_triggered, time spent,
#   relationship changes, queued messages) PERSIST into the current save.
#   That is intentional — the developer sees exactly what a player sees.
# - To re-run a scene, hit its "Reset" button first.
# - Do NOT test from a production save you care about. Use a dev slot.
#
# SCENE_TEST_REGISTRY is debug data only. No gameplay code reads it.
# Canonical eligibility stays in location_beats.rpy / summer_festival.rpy.
# ═══════════════════════════════════════════════════════════════════

init python:

    # ── Nora — cover the shift ────────────────────────────────────────────
    def _dst_nora_basic():
        """Minimum state for nora_cover_shift_scene, plus a day/hour where
        check_nora_cover_scene() also agrees (Saturday 16:00) so the natural
        trigger can be exercised too."""
        store.nora_met = True
        mark_npc_encountered("nora")
        store.nora_life_state = "cafe"
        store.nora_school_revealed = False
        store.nora_cover_shift_triggered = False
        store.covered_nora_shift = False
        store.nora_cover_thanks_said = False
        set_npc_rel("nora", "familiarity", 25)      # below both 35 and 40 gates
        store.day += (5 - store.day % 7) % 7        # next Saturday (her late shift)
        store.hour = 16.0
        renpy.notify("Nora preset: basic (fam 25)")

    def _dst_nora_school_known():
        _dst_nora_basic()
        store.nora_school_revealed = True
        renpy.notify("Nora preset: school revealed")

    def _dst_nora_comfortable():
        _dst_nora_basic()
        set_npc_rel("nora", "familiarity", 45)      # opens fam>=40 + fam>=35 lines
        renpy.notify("Nora preset: comfortable (fam 45)")

    def _dst_nora_reset():
        store.nora_cover_shift_triggered = False
        store.covered_nora_shift = False
        store.nora_cover_thanks_said = False
        store.npc_messages = [m for m in store.npc_messages
                              if m["tag"] != "nora_cover_shift_thanks"]
        renpy.notify("Nora cover-shift flags cleared")

    # ── Contextual Tier A beats (location_beats_tier_a.rpy) ───────────────
    # Presets only set the state the SCENE reads (plus a day/hour where the
    # real check function also agrees, so the natural trigger is testable).
    # They never re-implement eligibility.
    def _dst_beat_meet(*npc_ids):
        for _n in npc_ids:
            setattr(store, _n + "_met", True)
            mark_npc_encountered(_n)

    def _dst_beat_set_weekday(target_dow):
        store.day += (target_dow - store.day % 7) % 7

    def _dst_beat_clear(beat_id):
        """Clears the global budget plus this beat's cooldown / pity / roll."""
        store.last_tier_a_beat_day = -1
        for _attr in ("tier_a_beat_last_day", "tier_a_beat_miss_count",
                      "tier_a_beat_roll_cache"):
            _d = dict(getattr(store, _attr))
            _d.pop(beat_id, None)
            setattr(store, _attr, _d)
        renpy.notify("Beat '%s' cooldown/pity/roll cleared" % beat_id)

    # Beat 1 — Zoe, beach run-in (location_sandbeach, Sat 12-18)
    def _dst_zoe_outdoor_basic():
        _dst_beat_meet("zoe")
        _dst_beat_clear("zoe_outdoor")
        set_npc_rel("zoe", "familiarity", 20)       # below the fam>=30 gate
        _dst_beat_set_weekday(5)
        store.hour = 14.0
        renpy.notify("Zoe beach preset: basic (fam 20)")

    def _dst_zoe_outdoor_comfortable():
        _dst_zoe_outdoor_basic()
        set_npc_rel("zoe", "familiarity", 40)       # opens the comfortable variant
        renpy.notify("Zoe beach preset: comfortable (fam 40)")

    def _dst_zoe_outdoor_festival():
        _dst_zoe_outdoor_comfortable()
        store.summer_festival_state["attended"] = True
        renpy.notify("Zoe beach preset: + festival callback line")

    def _dst_zoe_outdoor_reset():
        _dst_beat_clear("zoe_outdoor")

    # Beat 2 — Zoe, walk with me (location_park, Thu 14-18)
    def _dst_zoe_walk_basic():
        _dst_beat_meet("zoe")
        _dst_beat_clear("zoe_walk")
        set_npc_rel("zoe", "familiarity", 20)
        store.skill_art = 0                         # below the art>=2 line
        _dst_beat_set_weekday(3)
        store.hour = 15.0
        renpy.notify("Zoe walk preset: basic")

    def _dst_zoe_walk_artist():
        _dst_zoe_walk_basic()
        set_npc_rel("zoe", "familiarity", 40)
        store.skill_art = 3                         # opens the art line
        renpy.notify("Zoe walk preset: artist MC (art 3, fam 40)")

    def _dst_zoe_walk_reset():
        _dst_beat_clear("zoe_walk")

    # Beat 3 — Eli, quick favour (location_library, Mon 12-18)
    def _dst_eli_favor_basic():
        _dst_beat_meet("eli")
        _dst_beat_clear("eli_favor")
        set_npc_rel("eli", "familiarity", 40)       # satisfies the fam>=35 alt
        store.skill_prog = 0
        _dst_beat_set_weekday(0)
        store.hour = 14.0
        renpy.notify("Eli favour preset: basic (non-programmer branch)")

    def _dst_eli_favor_programmer():
        _dst_eli_favor_basic()
        store.skill_prog = 4                        # switches to the code branch
        renpy.notify("Eli favour preset: programmer MC (prog 4)")

    def _dst_eli_favor_festival():
        _dst_eli_favor_basic()
        set_npc_rel("eli", "familiarity", 10)       # alt requirement via festival
        store.summer_festival_state["attended"] = True
        renpy.notify("Eli favour preset: qualifies via festival, low fam")

    def _dst_eli_favor_reset():
        _dst_beat_clear("eli_favor")

    # Beat 4 — Eli, after your shift (location_hub, Mon 09-12, IT career)
    def _dst_eli_after_shift_basic():
        _dst_beat_meet("eli")
        _dst_beat_clear("eli_after_shift")
        if "it" not in store.active_careers:
            _ac = dict(store.active_careers)
            _ac["it"] = {"rank": 1, "perf": 0}
            store.active_careers = _ac
        _dst_beat_set_weekday(0)
        store.hour = 10.0
        renpy.notify("Eli after-shift preset: basic (IT career active)")

    def _dst_eli_after_shift_comfortable():
        _dst_eli_after_shift_basic()
        set_npc_rel("eli", "familiarity", 45)
        renpy.notify("Eli after-shift preset: comfortable (fam 45)")

    def _dst_eli_after_shift_reset():
        _dst_beat_clear("eli_after_shift")

    # Beat 5 — Marcus, pace the last loop (location_park, Mon 07-11)
    def _dst_marcus_park_basic():
        _dst_beat_meet("marcus")
        _dst_beat_clear("marcus_park_favor")
        store.skill_fit = 0                         # below the fit>=3 line
        _dst_beat_set_weekday(0)
        store.hour = 8.0
        renpy.notify("Marcus run preset: basic")

    def _dst_marcus_park_fit():
        _dst_marcus_park_basic()
        store.skill_fit = 4                         # opens the competence line
        renpy.notify("Marcus run preset: fit MC (fit 4)")

    def _dst_marcus_park_reset():
        _dst_beat_clear("marcus_park_favor")

    # Beat 6 — Marcus, one game (location_bar, evening)
    def _dst_marcus_game_basic():
        _dst_beat_meet("marcus")
        _dst_beat_clear("marcus_one_game")
        store.bar_first_wins = [w for w in store.bar_first_wins
                                if w != "marcus_pool"]
        store.bar_game_cooldowns = {}
        _dst_beat_set_weekday(0)
        store.hour = 19.0
        renpy.notify("Marcus game preset: basic (no rivalry history)")

    def _dst_marcus_game_rivalry():
        _dst_marcus_game_basic()
        store.bar_first_wins = list(store.bar_first_wins) + ["marcus_pool"]
        renpy.notify("Marcus game preset: MC has beaten him at pool before")

    def _dst_marcus_game_reset():
        _dst_beat_clear("marcus_one_game")
        store.bar_game_cooldowns = {}

    # Beat 7 — Nora, you look exhausted (location_cafe, low energy)
    def _dst_nora_exhausted_basic():
        _dst_beat_meet("nora")
        _dst_beat_clear("nora_exhausted")
        store.nora_life_state = "cafe"
        store.need_energy = 15                      # below BEAT_LOW_ENERGY (30)
        _dst_beat_set_weekday(5)
        store.hour = 12.0
        renpy.notify("Nora exhausted preset: basic (energy 15)")

    def _dst_nora_exhausted_comfortable():
        _dst_nora_exhausted_basic()
        set_npc_rel("nora", "familiarity", 45)
        renpy.notify("Nora exhausted preset: comfortable (fam 45)")

    def _dst_nora_exhausted_reset():
        _dst_beat_clear("nora_exhausted")

    # Beat 8 — Nora, walking out together (location_cafe, weekend 17-18)
    def _dst_nora_walk_out_basic():
        _dst_beat_meet("nora")
        _dst_beat_clear("nora_walk_out")
        store.nora_life_state = "cafe"
        set_npc_rel("nora", "familiarity", 35)      # above the fam>=30 gate
        # The stronger closing scene must be off the table or this beat is
        # obsolete by design — see _nora_closing_still_possible().
        store.nora_closing_done = True
        _dst_beat_set_weekday(5)
        store.hour = 17.5
        renpy.notify("Nora walk-out preset: basic (closing scene already done)")

    def _dst_nora_walk_out_comfortable():
        _dst_nora_walk_out_basic()
        set_npc_rel("nora", "familiarity", 50)      # +3% chance tier
        renpy.notify("Nora walk-out preset: comfortable (fam 50)")

    def _dst_nora_walk_out_reset():
        _dst_beat_clear("nora_walk_out")

    # ── Nora after-hours café scenes (locations.rpy) ──────────────────────
    # hour is set inside the 19:00-21:00 exemption window so the REAL entry
    # path (label location_cafe) reaches these, not just the direct jump.
    def _dst_nora_closing_basic():
        _dst_beat_meet("nora")
        store.nora_life_state = "cafe"
        store.nora_closing_done = False
        store.nora_affection = 40                   # exactly the gate
        store.nora_trust = 30
        store.hour = 19.5
        renpy.notify("Nora closing preset: basic (aff 40)")

    def _dst_nora_closing_comfortable():
        _dst_nora_closing_basic()
        store.nora_affection = 55                   # opens the aff>=50 choices
        store.nora_trust = 45
        renpy.notify("Nora closing preset: comfortable (aff 55)")

    def _dst_nora_closing_reset():
        store.nora_closing_done = False
        store.nora_reopen_done = False
        store.nora_rent_done = False
        renpy.notify("Nora closing/reopen flags cleared")

    def _dst_nora_reopen_basic():
        _dst_beat_meet("nora")
        store.nora_life_state = "cafe"
        store.nora_closing_done = True              # reopen is post-closing only
        store.nora_reopen_done = False
        store.major_scene_last_day = -1
        set_romance_state("nora", "friends", source="scene_tester")
        # ROMANCE_PROFILES["nora"]: aff 45 / trust 40 / momentum 30
        store.nora_affection = 45
        store.nora_trust = 40
        add_romance_momentum("nora", 30 - get_romance_momentum("nora"))
        store.hour = 19.5
        renpy.notify("Nora reopen preset: basic (friends, momentum 30)")

    def _dst_nora_reopen_comfortable():
        _dst_nora_reopen_basic()
        store.nora_affection = 55                   # opens the aff50/trust45 line
        store.nora_trust = 50
        renpy.notify("Nora reopen preset: comfortable (aff 55 / trust 50)")

    def _dst_nora_reopen_reset():
        store.nora_reopen_done = False
        store.major_scene_last_day = -1
        renpy.notify("Nora reopen flag cleared")

    # Beat 9 — Marcus + Zoe, already here (location_bar, Sat 19-24)
    def _dst_marcus_zoe_basic():
        _dst_beat_meet("marcus", "zoe")
        _dst_beat_clear("marcus_zoe_bar")
        _dst_beat_set_weekday(5)
        store.hour = 20.0
        renpy.notify("Marcus+Zoe preset: basic (Sat 20:00 bar)")

    def _dst_marcus_zoe_comfortable():
        _dst_marcus_zoe_basic()
        set_npc_rel("marcus", "familiarity", 45)
        set_npc_rel("zoe", "familiarity", 45)
        renpy.notify("Marcus+Zoe preset: comfortable with both")

    def _dst_marcus_zoe_reset():
        _dst_beat_clear("marcus_zoe_bar")

    # Beat 10 — Zoe + Nora, cross-thread (location_cafe, Wed 13-15)
    def _dst_cross_zoe_nora_basic():
        _dst_beat_meet("zoe", "nora")
        _dst_beat_clear("cross_zoe_nora")
        store.nora_life_state = "cafe"
        _dst_beat_set_weekday(2)
        store.hour = 14.0
        renpy.notify("Zoe+Nora preset: basic (Wed 14:00 café)")

    def _dst_cross_zoe_nora_comfortable():
        _dst_cross_zoe_nora_basic()
        set_npc_rel("nora", "familiarity", 45)
        set_npc_rel("zoe", "familiarity", 45)
        renpy.notify("Zoe+Nora preset: comfortable with both")

    def _dst_cross_zoe_nora_reset():
        _dst_beat_clear("cross_zoe_nora")

    # ── Summer festival ───────────────────────────────────────────────────
    def _dst_festival_all_met():
        for _n in SF_NPCS:
            setattr(store, _n + "_met", True)
            mark_npc_encountered(_n)
        _debug_festival_reset()                     # debug_summer_festival.rpy
        store.summer_festival_state["scheduled_day"] = store.day
        store.summer_festival_state["eligible"] = True
        store.summer_festival_state["discovered"] = True
        store.hour = 20.0
        renpy.notify("Festival preset: all four met, on tonight")

    def _dst_festival_reset():
        # Indirection on purpose: _debug_festival_reset lives in
        # debug_summer_festival.rpy, whose init python runs after this file's.
        _debug_festival_reset()

    # ── Registry ──────────────────────────────────────────────────────────
    # "label"       — shipping label to jump to.
    # "presets"     — name → callable that sets state first.
    # "checkpoints" — name → shipping sub-label, to skip earlier CGs.
    # "reset"       — callable that clears the scene's own flags.
    SCENE_TEST_REGISTRY = {
        "nora_cover_shift": {
            "title": "Nora — Cover the Shift",
            "category": "Location Beats",
            "desc": "Contextual Café beat. Nora asks MC to cover her shift.",
            "label": "nora_cover_shift_scene",
            "presets": {
                "basic": _dst_nora_basic,
                "school known": _dst_nora_school_known,
                "comfortable": _dst_nora_comfortable,
            },
            "checkpoints": {
                "accept": "nora_cover_accept",
                "decline": "nora_cover_decline",
            },
            "reset": _dst_nora_reset,
            "notes": "Accept → time runs to 19:00, trust +4. Decline → no penalty.",
        },
        # ── Contextual Tier A pack 1 ──────────────────────────────────────
        "zoe_outdoor": {
            "title": "Zoe — Beach Run-In",
            "category": "Location Beats",
            "desc": "Weekend beach. You walk into Zoe losing an argument with a colour.",
            "label": "zoe_outdoor_scene",
            "presets": {
                "basic": _dst_zoe_outdoor_basic,
                "comfortable": _dst_zoe_outdoor_comfortable,
                "festival attended": _dst_zoe_outdoor_festival,
            },
            "checkpoints": None,
            "reset": _dst_zoe_outdoor_reset,
            "notes": "Sandbeach, Sat/Sun 12-18. Stay = 30 min; familiarity only "
                     "rewarded at fam>=30. Cooldown 5 days.",
        },
        "zoe_walk": {
            "title": "Zoe — Walk With Me?",
            "category": "Location Beats",
            "desc": "Park. Zoe wants to walk the long way and not be alone with her opinions.",
            "label": "zoe_walk_scene",
            "presets": {
                "basic": _dst_zoe_walk_basic,
                "artist MC": _dst_zoe_walk_artist,
            },
            "checkpoints": None,
            "reset": _dst_zoe_walk_reset,
            "notes": "Park, Thu/Fri 14-18. Walk = 30 min, familiarity +2. "
                     "Decline is free. Cooldown 4 days.",
        },
        "eli_favor": {
            "title": "Eli — Quick Favour",
            "category": "Location Beats",
            "desc": "Library. Eli borrows a brain for ninety seconds.",
            "label": "eli_favor_scene",
            "presets": {
                "basic": _dst_eli_favor_basic,
                "programmer MC": _dst_eli_favor_programmer,
                "festival attended": _dst_eli_favor_festival,
            },
            "checkpoints": None,
            "reset": _dst_eli_favor_reset,
            "notes": "Library, Mon-Fri 12-18 / Sat 10-16. Trust or Respect, "
                     "never cash. Cooldown 6 days.",
        },
        "eli_after_shift": {
            "title": "Eli — After Your Shift?",
            "category": "Location Beats",
            "desc": "The Hub. Your colleague asks whether the day just ends.",
            "label": "eli_after_shift_scene",
            "presets": {
                "basic": _dst_eli_after_shift_basic,
                "comfortable": _dst_eli_after_shift_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_eli_after_shift_reset,
            "notes": "Hub, Mon-Fri 09-12, requires the IT career. Agreeing creates "
                     "NO commitment — social acknowledgement only. Cooldown 7 days.",
        },
        "marcus_park_favor": {
            "title": "Marcus — Pace The Last Loop",
            "category": "Location Beats",
            "desc": "Morning park. Marcus needs a witness or he'll cut the run short.",
            "label": "marcus_park_favor_scene",
            "presets": {
                "basic": _dst_marcus_park_basic,
                "fit MC": _dst_marcus_park_fit,
            },
            "checkpoints": None,
            "reset": _dst_marcus_park_reset,
            "notes": "Park, Mon-Fri 07-11 (Marcus has NO gym schedule — the spec's "
                     "gym spot became his real morning run). Help = 20 min.",
        },
        "marcus_one_game": {
            "title": "Marcus — One Game",
            "category": "Location Beats",
            "desc": "Bar, evening. Marcus racks the balls. Resolves through bar_game_play.",
            "label": "marcus_one_game_scene",
            "presets": {
                "basic": _dst_marcus_game_basic,
                "rivalry": _dst_marcus_game_rivalry,
            },
            "checkpoints": None,
            "reset": _dst_marcus_game_reset,
            "notes": "Bar from 18:00. Accept hands off to bar_game_play('pool', "
                     "'pool_marcus') — real entry fee, real stable roll.",
        },
        "nora_exhausted": {
            "title": "Nora — You Look Exhausted",
            "category": "Location Beats",
            "desc": "Café. Nora notices the state of you. She does not fix it.",
            "label": "nora_exhausted_scene",
            "presets": {
                "basic": _dst_nora_exhausted_basic,
                "comfortable": _dst_nora_exhausted_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_nora_exhausted_reset,
            "notes": "Only eligible below energy 30. No energy restored by design. "
                     "Cooldown 4 days.",
        },
        "nora_walk_out": {
            "title": "Nora — Walking Out Together",
            "category": "Location Beats",
            "desc": "Café, end of her weekend shift. The weak version of closing time.",
            "label": "nora_walk_out_scene",
            "presets": {
                "basic": _dst_nora_walk_out_basic,
                "comfortable": _dst_nora_walk_out_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_nora_walk_out_reset,
            "notes": "Weekend 17-18 (she is never at the café 18-19). Stands down "
                     "permanently while nora_closing_scene is still possible.",
        },
        "marcus_zoe_bar": {
            "title": "Marcus + Zoe — Already Here",
            "category": "Location Beats",
            "desc": "Saturday bar. They finish the argument before they notice you.",
            "label": "marcus_zoe_bar_scene",
            "presets": {
                "basic": _dst_marcus_zoe_basic,
                "comfortable": _dst_marcus_zoe_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_marcus_zoe_reset,
            "notes": "Bar, Sat 19-24 — the only evening slot Marcus shares with a "
                     "met-able NPC. Marcus and Eli never share a location at all.",
        },
        "cross_zoe_nora": {
            "title": "Zoe + Nora — Cross-Thread",
            "category": "Location Beats",
            "desc": "Wednesday café. Two regulars mid-conversation when you walk in.",
            "label": "cross_zoe_nora_scene",
            "presets": {
                "basic": _dst_cross_zoe_nora_basic,
                "comfortable": _dst_cross_zoe_nora_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_cross_zoe_nora_reset,
            "notes": "Café, Wed 13-15 — the only window with Nora on shift and Zoe "
                     "browsing. Cooldown 10 days.",
        },
        # ── Nora after-hours café ─────────────────────────────────────────
        "nora_closing": {
            "title": "Nora — Closing Scene",
            "category": "Relationship Scenes",
            "desc": "Locked-up café after 19:00. The last cup, and why she never left.",
            "label": "nora_closing_scene",
            "presets": {
                "basic": _dst_nora_closing_basic,
                "comfortable": _dst_nora_closing_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_nora_closing_reset,
            "notes": "Reached through label location_cafe's 19:00-21:00 after-hours "
                     "exemption (aff>=40, not done), or a shift ending past 19:00. "
                     "Sets nora_closing_done and the romance direction.",
        },
        "nora_romance_reopen": {
            "title": "Nora — Romance Reopen",
            "category": "Relationship Scenes",
            "desc": "Post-closing. She asks what 'next week' was supposed to mean.",
            "label": "dst_nora_reopen_launch",
            "presets": {
                "basic": _dst_nora_reopen_basic,
                "comfortable": _dst_nora_reopen_comfortable,
            },
            "checkpoints": None,
            "reset": _dst_nora_reopen_reset,
            "notes": "Same 19:00-21:00 exemption, one rung below the closing scene. "
                     "Needs closing done, state friends/unopened, and momentum 30 "
                     "(ROMANCE_PROFILES). Ends with `return` — the tester's Jump() "
                     "lands back in the main loop.",
        },
        "summer_festival": {
            "title": "Downtown Summer Festival",
            "category": "Major Events",
            "desc": "Full 13-CG evening event. Marcus / Eli / Zoe / Nora.",
            "label": "summer_festival_main",
            "presets": {"all met": _dst_festival_all_met},
            "checkpoints": {
                "blackout: technical": "summer_festival_blackout_technical",
                "blackout: organize": "summer_festival_blackout_organize",
                "blackout: stay together": "summer_festival_blackout_group",
                "after blackout": "summer_festival_post_blackout",
            },
            "reset": _dst_festival_reset,
            "notes": "Checkpoints skip earlier CGs; only the full run sees all 13. "
                     "The blackout choice menu is inline in summer_festival_main, "
                     "so the three branch labels are the earliest jump-in points.",
        },
    }

    SCENE_TEST_CATEGORIES = [
        "Location Beats",
        "Group Hangouts",
        "Major Events",
        "Relationship Scenes",
        "Career / Professional",
        "Misc",
    ]

    def _dst_entries(category):
        return sorted([(k, v) for k, v in SCENE_TEST_REGISTRY.items()
                       if v["category"] == category])


screen debug_scene_tester():
    # modal/zorder are screen properties and must stay at the top level.
    modal True
    zorder 210
    if not config.developer:
        # Belt-and-braces: in a release build the screen closes itself, so even
        # a stray Show() cannot leave the player stuck behind a modal overlay.
        timer 0.01 action Hide("debug_scene_tester")
    else:
        add "#000000e0"
        frame:
            xalign 0.5 yalign 0.5
            xsize 900
            ysize 700
            background "#12161ef8"
            padding (22, 18, 22, 18)
            vbox:
                spacing 6
                text "SCENE TESTER" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
                text "presets set state, then jump to the shipping label — changes persist, use Reset to re-run" font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                null height 4
                viewport:
                    xfill True
                    ysize 570
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        xsize 830
                        for _cat in SCENE_TEST_CATEGORIES:
                            $ _rows = _dst_entries(_cat)
                            if _rows:
                                text _cat font PROFILE_FONT size 13 color "#5bcafa"
                                for _id, _e in _rows:
                                    frame:
                                        xfill True
                                        background "#ffffff0a"
                                        padding (12, 8, 12, 8)
                                        vbox:
                                            spacing 4
                                            xfill True
                                            text _e["title"] font PROFILE_FONT size 15 color "#f0ece4"
                                            text _e["desc"] font ACT_FONT size 12 color "#7a9ab8"
                                            if _e.get("notes"):
                                                text _e["notes"] font ACT_FONT size 11 color "#5a7090"
                                            hbox:
                                                spacing 8
                                                text "preset:" font ACT_FONT size 12 color "#4a6080" yalign 0.5
                                                for _pn, _pf in sorted(_e["presets"].items()):
                                                    textbutton _pn action Function(_pf) text_size 13 text_color "#7abf7a"
                                                textbutton "Reset" action Function(_e["reset"]) text_size 13 text_color "#e05533"
                                            hbox:
                                                spacing 8
                                                textbutton "▶ Launch" action [Hide("debug_scene_tester"), Jump(_e["label"])] text_size 14 text_color "#ffd66a"
                                                if _e.get("checkpoints"):
                                                    text "jump to:" font ACT_FONT size 12 color "#4a6080" yalign 0.5
                                                    for _cn, _cl in sorted(_e["checkpoints"].items()):
                                                        textbutton _cn action [Hide("debug_scene_tester"), Jump(_cl)] text_size 13 text_color "#a890d0"
                        null height 6
                        text "Tools" font PROFILE_FONT size 13 color "#5bcafa"
                        textbutton "▶  Speaker animation test (react_* transforms)":
                            action [Hide("debug_scene_tester"), Jump("dev_speaker_anim_test")]
                            text_size 14 text_color "#7fd06a"
                null height 4
                textbutton "Close" action [Hide("debug_scene_tester"), Show("debug_menu")] xalign 0.5 text_size 16 text_color "#9fb6d6"


# ── Speaker animation test ────────────────────────────────────────────────
# The six react_* transforms in images.rpy, previewed on Nora's café sprites.
label dev_speaker_anim_test:
    $ set_hud("hidden")
    $ story_scene_active = True
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal as focus_nora at sprite_r
    "Speaker animation test — pick a transform to preview it."

label dev_speaker_anim_menu:
    menu:
        "react_bounce":
            show nora_cafe_laugh as focus_nora at sprite_r, react_bounce
            "bounce"
        "react_shake":
            show nora_cafe_angry as focus_nora at sprite_r, react_shake
            "shake"
        "react_step_back":
            show nora_cafe_normal as focus_nora at sprite_r, react_step_back
            "step back"
        "react_lean_in":
            show nora_cafe_talk as focus_nora at sprite_r, react_lean_in
            "lean in"
        "react_nod":
            show nora_cafe_talk as focus_nora at sprite_r, react_nod
            "nod"
        "react_sigh":
            show nora_cafe_sad as focus_nora at sprite_r, react_sigh
            "sigh"
        "Done":
            $ story_scene_active = False
            $ set_hud("full")
            jump map
    jump dev_speaker_anim_menu


# ─── HOW TO REGISTER A NEW SCENE ─────────────────────────────────
# 1. Add a preset function in the init python block above:
#        def _dst_yourscene_basic():
#            store.relevant_flag = True
#            store.hour = 16.0
#            renpy.notify("...")
#    It sets the state the scene READS. It does not re-implement the
#    scene's eligibility check — that lives with the scene.
#
# 2. Add a registry entry:
#        "your_scene_id": {
#            "title": "NPC — Scene Name",
#            "category": "Location Beats",   # must be in SCENE_TEST_CATEGORIES
#            "desc": "One sentence.",
#            "label": "your_actual_scene_label",   # shipping label, no wrapper
#            "presets": {"basic": _dst_yourscene_basic},
#            "checkpoints": {"branch": "your_scene_branch_label"},  # or omit
#            "reset": _dst_yourscene_reset,
#            "notes": "Optional dev notes.",
#        },
#
# 3. Nothing else. The scene keeps its own exit (jump map / jump
#    <location>_actions), so no wrapper label and no dev-mode flag.
#
# tests/location_beats_selfcheck.py section G checks every label and
# preset in the registry actually exists — it will fail if you typo one.
# ─────────────────────────────────────────────────────────────────

# ── Exception to the "no wrapper label" rule above ─────────────────────────
# scene_nora_romance_reopen ends with `return` (it is `call`ed from
# cafe_actions / location_cafe), and the tester launches with a plain Jump().
# Without a call frame that `return` would drop out of the script, so this
# debug-only wrapper supplies one. Do not use it from gameplay code.
label dst_nora_reopen_launch:
    call scene_nora_romance_reopen
    jump map
