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

    # ── Phone photo message dev helpers ──────────────────────────────────
    # Force-queue any registered photo message regardless of eligibility.
    # Only for testing — bypasses once-ever and cooldown checks.
    # Do not call from production code.
    def _dst_force_photo_message(npc_id, photo_id):
        """Force-deliver a registered photo initiative message for any NPC.

        Bypasses: asset loadability, once-ever lock, per-NPC photo cooldown.
        Does NOT bypass: NPC being a contact (needed for thread display).
        """
        _pd = _NPC_PHOTO_MESSAGES.get(npc_id, {}).get(photo_id)
        if not _pd:
            renpy.notify("PHOTO ENGINE: no registered entry %s/%s" % (npc_id, photo_id))
            return
        _att = {
            "id":   photo_id,
            "path": _pd["asset"],
            "kind": "photo",
            "alt":  _pd.get("category", "photo"),
        }
        # Temporarily drop from sent set so queue_phone_message allows re-queue.
        _saved = store.npc_photo_messages_sent - {photo_id}
        store.npc_photo_messages_sent = _saved
        queue_phone_message(npc_id, _pd["text"], store.day, photo_id,
                            responses=_pd["responses"], attachment=_att)
        deliver_message_now(photo_id)
        renpy.notify("Queued + delivered: %s/%s%s" % (
            npc_id, photo_id,
            "" if renpy.loadable(_pd["asset"]) else " (ASSET MISSING)",
        ))

    def _dst_force_text_only_message():
        """Queues a plain text message to verify existing text-only path unchanged."""
        queue_phone_message("nora", "[DEV] text-only backward-compat test",
                            store.day, "dev_text_only_test")
        deliver_message_now("dev_text_only_test")
        renpy.notify("Queued text-only test message — check thread renders without attachment")

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

    def _dst_festival_zoe_romance_hook():
        """Sets up the festival with Zoe at dating state so the romance hook
        is visible at the shelter menu (Zoe branch). The hook fires only when
        renpy.has_label('summer_festival_zoe_romance') is True — add a TEST-ONLY
        stub in this file to activate it during local development."""
        _dst_festival_all_met()
        set_romance_state("zoe", "dating", source="debug_preset")
        store.summer_festival_state["blackout_choice"] = "organize"
        renpy.notify("Festival preset: Zoe dating — romance hook visible at shelter (if label exists)")

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
            "presets": {
                "all met": _dst_festival_all_met,
                "zoe romance hook": _dst_festival_zoe_romance_hook,
            },
            "checkpoints": {
                "blackout: technical": "summer_festival_blackout_technical",
                "blackout: organize": "summer_festival_blackout_organize",
                "blackout: stay together": "summer_festival_blackout_group",
                "after blackout (→ shelter)": "summer_festival_post_blackout",
            },
            "reset": _dst_festival_reset,
            "notes": "Checkpoints skip earlier CGs; only the full run sees all 13. "
                     "The blackout choice menu is inline in summer_festival_main, "
                     "so the three branch labels are the earliest jump-in points. "
                     "'zoe romance hook' preset sets Zoe to dating; the hook at the "
                     "shelter Zoe branch activates when renpy.has_label("
                     "'summer_festival_zoe_romance') is True — add a TEST-ONLY stub "
                     "in this file to exercise it locally.",
        },
    }

    # ── Phone / Photos test entries ───────────────────────────────────────────
    # Auto-generated from all director-registered photo entries in
    # _NPC_PHOTO_MESSAGES (populated by register_npc_photo_message() calls in
    # game/director_phone/ content files). Empty when no content is registered.
    # _dst_force_photo_message() bypasses once-ever + cooldown for dev preview.
    # These are Function() calls — they do not jump to a label.
    for _npc_id, _npc_photos in _NPC_PHOTO_MESSAGES.items():
        for _pid, _pdata in _npc_photos.items():
            _entry_key = "%s/%s" % (_npc_id, _pid)
            SCENE_TEST_REGISTRY[_entry_key] = {
                "title":    _entry_key,
                "category": "Phone / Photos",
                "desc":     _pdata["text"],
                "label":    None,   # no label; preset queues directly
                "presets":  {"force send": lambda _n=_npc_id, _p=_pid: _dst_force_photo_message(_n, _p)},
                "checkpoints": None,
                "reset":    None,
                "notes":    ("NPC: %s  Category: %s  Asset: %s%s" % (
                                 _npc_id, _pdata.get("category", "—"), _pdata["asset"],
                                 " ✓" if renpy.loadable(_pdata["asset"]) else " MISSING",
                             )),
            }
    SCENE_TEST_REGISTRY["_phone_text_only_test"] = {
        "title":    "text-only backward-compat",
        "category": "Phone / Photos",
        "desc":     "Verify text-only message path unchanged after attachment schema extension.",
        "label":    None,
        "presets":  {"send": _dst_force_text_only_message},
        "checkpoints": None,
        "reset":    None,
        "notes":    "Queues a dev text message to Nora. Must render without attachment card.",
    }

    SCENE_TEST_CATEGORIES = [
        "Location Beats",
        "Group Hangouts",
        "Major Events",
        "Phone / Photos",
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


# ═══════════════════════════════════════════════════════════════════════════
# SCENE TESTER ENTRIES
# ═══════════════════════════════════════════════════════════════════════════
# Registered into the existing SCENE_TEST_REGISTRY (debug_scene_tester.rpy).
# Presets set state then the tester jumps to the shipping label — same
# contract as every other entry in that file.

init 1 python:

    def _dst_zoe_arc_base():
        store.zoe_met = True
        mark_npc_encountered("zoe")
        if "zoe" not in store.npc_contacts:
            store.npc_contacts = store.npc_contacts + ["zoe"]
        store.last_tier_a_beat_day = -1

    def _dst_zoe_early():
        """Acquaintance: she'll talk about a print, not about herself."""
        _dst_zoe_arc_base()
        store.zoe_affection = 12
        store.zoe_trust     = 8
        set_npc_rel("zoe", "familiarity", 18)
        set_npc_rel("zoe", "respect", 10)
        renpy.notify("Zoe preset: early (aff 12 / trust 8 / fam 18)")

    def _dst_zoe_comfortable():
        """Comfortable: paid work and the bass are on the table."""
        _dst_zoe_arc_base()
        store.zoe_affection = 38
        store.zoe_trust     = 32
        set_npc_rel("zoe", "familiarity", 45)
        set_npc_rel("zoe", "respect", 30)
        store.knows_zoe_art_interest       = True
        store.knows_zoe_paid_creative_work = True
        renpy.notify("Zoe preset: comfortable (aff 38 / trust 32 / fam 45)")

    def _dst_zoe_close():
        """Close: every knowledge fact set, Just Stay in range."""
        _dst_zoe_arc_base()
        store.zoe_affection = 62
        store.zoe_trust     = 60
        set_npc_rel("zoe", "familiarity", 65)
        set_npc_rel("zoe", "respect", 50)
        for _f in ("knows_zoe_art_interest", "knows_zoe_paid_creative_work",
                   "knows_zoe_gallery_goal", "knows_zoe_funding_problem",
                   "knows_zoe_bass_history", "knows_zoe_creative_values"):
            setattr(store, _f, True)
        renpy.notify("Zoe preset: close (aff 62 / trust 60 / fam 65)")

    def _dst_zoe_initiative_ready():
        """Clears every gate the shipping picker checks, so the next new_day
        rolls a Zoe text with the whole arc pool available."""
        _dst_zoe_comfortable()
        store.npc_initiative_last_global_day = -1
        store._p68_contact_day = -1
        _ld = dict(store.npc_initiative_last_day); _ld.pop("zoe", None)
        store.npc_initiative_last_day = _ld
        _clear_initiative_pending("zoe")
        store.npc_last_seen["zoe"] = store.day - 8   # opens the gap-only variants
        renpy.notify("Zoe initiative: cooldowns cleared, 8-day contact gap set")

    _ZOE_ARC_RESET_FLAGS = (
        "zoe_print_done", "zoe_beige_done", "zoe_second_opinion_pending",
        "zoe_second_opinion_done", "zoe_second_opinion_callback_done",
        "zoe_bass_window_done", "zoe_bass_followup_done", "zoe_coffee_pending",
        "zoe_coffee_done", "zoe_not_ready_done", "zoe_noticed_callback_done",
        "zoe_deadline_scene_done", "zoe_deadline_submitted",
        "zoe_deadline_followup_done", "zoe_after_deadline_done",
        "zoe_just_stay_done",
    )

    def _dst_zoe_arc_reset():
        """Clears every beat flag in this file. Knowledge facts are left alone —
        _zoe_sync_knowledge would immediately re-derive them from the topic arcs
        anyway, so clearing them would just lie about what the save knows."""
        for _f in _ZOE_ARC_RESET_FLAGS:
            setattr(store, _f, False)
        store.zoe_second_opinion_choice = None
        store.zoe_second_opinion_day = -1
        store.zoe_deadline_day = -1
        store.zoe_deadline_result = "pending"
        store.last_tier_a_beat_day = -1
        renpy.notify("All Zoe arc beat flags cleared")

    def _dst_zoe_secopin_preset():
        _dst_zoe_comfortable()
        store.knows_zoe_art_interest    = True
        store.zoe_second_opinion_done   = False
        store.zoe_second_opinion_choice = None
        store.zoe_second_opinion_day = -1
        store.zoe_second_opinion_pending = True
        store.last_tier_a_beat_day = -1
        renpy.notify("Second Opinion armed")

    def _dst_zoe_secopin_artist():
        _dst_zoe_secopin_preset()
        store.skill_art = max(store.skill_art, 25)   # opens the technical line
        renpy.notify("Second Opinion armed (art-skilled MC)")

    def _dst_zoe_secopin_reset():
        store.zoe_second_opinion_done = False
        store.zoe_second_opinion_choice = None
        store.zoe_second_opinion_callback_done = False
        store.zoe_noticed_callback_done = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Second Opinion flags cleared")

    def _dst_zoe_coffee_preset():
        _dst_zoe_comfortable()
        store.zoe_coffee_done    = False
        store.zoe_coffee_pending = True
        store.last_tier_a_beat_day = -1
        renpy.notify("Coffee Not Advice armed")

    def _dst_zoe_coffee_funding():
        _dst_zoe_coffee_preset()
        store.knows_zoe_funding_problem = True   # she names the same people
        renpy.notify("Coffee Not Advice armed (funding known)")

    def _dst_zoe_coffee_reset():
        store.zoe_coffee_done = False
        store.zoe_coffee_pending = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Coffee flags cleared")

    def _dst_zoe_bass_first():
        _dst_zoe_comfortable()
        store.knows_zoe_bass_history = False
        store.zoe_bass_window_done   = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Bass: first-telling version")

    def _dst_zoe_bass_callback():
        _dst_zoe_comfortable()
        store.knows_zoe_bass_history = True      # switches to the callback branch
        store.zoe_bass_window_done   = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Bass: callback version (history already known)")

    def _dst_zoe_bass_reset():
        store.zoe_bass_window_done = False
        store.zoe_bass_followup_done = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Bass flags cleared")

    def _dst_zoe_just_stay_preset():
        _dst_zoe_close()
        store.zoe_just_stay_done = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Just Stay armed (platonic)")

    def _dst_zoe_just_stay_romantic():
        _dst_zoe_just_stay_preset()
        set_romance_state("zoe", "interested", source="scene_tester")
        renpy.notify("Just Stay armed (romantic variant)")

    def _dst_zoe_just_stay_reset():
        store.zoe_just_stay_done = False
        store.last_tier_a_beat_day = -1
        renpy.notify("Just Stay flags cleared")

    SCENE_TEST_REGISTRY.update({
        "zoe_states": {
            "title": "Zoe — Relationship States",
            "category": "Relationship Scenes",
            "desc": "Set an early / comfortable / close Zoe, or arm the phone initiative. "
                    "Jumps back to the map — use the presets, not the launch button.",
            "label": "map",
            "presets": {
                "early": _dst_zoe_early,
                "comfortable": _dst_zoe_comfortable,
                "close": _dst_zoe_close,
                "phone initiative ready": _dst_zoe_initiative_ready,
            },
            "checkpoints": None,
            "reset": _dst_zoe_arc_reset,
            "notes": "State-only entry. After 'phone initiative ready', sleep to the "
                     "next day — the picker runs in new_day and shares the one-contact "
                     "budget with every other NPC.",
        },
        "zoe_second_opinion": {
            "title": "Zoe — Second Opinion",
            "category": "Relationship Scenes",
            "desc": "Two layouts, same brief. She wants an answer, not comfort.",
            "label": "zoe_second_opinion_scene",
            "presets": {
                "basic": _dst_zoe_secopin_preset,
                "artist MC": _dst_zoe_secopin_artist,
            },
            "checkpoints": None,
            "reset": _dst_zoe_secopin_reset,
            "notes": "Normally armed by the zoe_msg_second_opinion text, then fires at "
                     "the park or Grounds. Stores zoe_second_opinion_choice, which "
                     "drives The Thing You Noticed and the Talk callback.",
        },
        "zoe_coffee": {
            "title": "Zoe — Coffee, Not Advice",
            "category": "Relationship Scenes",
            "desc": "Bad email. She asked for company, not a plan.",
            "label": "zoe_coffee_not_advice_scene",
            "presets": {
                "basic": _dst_zoe_coffee_preset,
                "funding known": _dst_zoe_coffee_funding,
            },
            "checkpoints": None,
            "reset": _dst_zoe_coffee_reset,
            "notes": "Best Trust comes from saying nothing. The motivational answer "
                     "still gains trust +1 — clumsy, not punished.",
        },
        "zoe_bass": {
            "title": "Zoe — Bass in the Window",
            "category": "Relationship Scenes",
            "desc": "A bass in a shop window. Deliberately unresolved.",
            "label": "zoe_bass_window_scene",
            "presets": {
                "first telling": _dst_zoe_bass_first,
                "callback version": _dst_zoe_bass_callback,
            },
            "checkpoints": None,
            "reset": _dst_zoe_bass_reset,
            "notes": "Hub, Mon-Fri 09-13, fam>=20. Branches on knows_zoe_bass_history, "
                     "which arc_zoe_music_2 also sets.",
        },
        "zoe_just_stay": {
            "title": "Zoe — Just Stay",
            "category": "Relationship Scenes",
            "desc": "She has a reason to be there. The reason is not the reason.",
            "label": "zoe_just_stay_scene",
            "presets": {
                "platonic": _dst_zoe_just_stay_preset,
                "romantic context": _dst_zoe_just_stay_romantic,
            },
            "checkpoints": None,
            "reset": _dst_zoe_just_stay_reset,
            "notes": "Park, fam>=60 and trust>=55. Friendship-capable by default; the "
                     "romantic variant is one extra exchange plus attraction +4.",
        },
    })


# ═══════════════════════════════════════════════════════════════════════════
# ZOE — EARLY ONBOARDING PACK (zoe_onboarding.rpy)
# ═══════════════════════════════════════════════════════════════════════════
# init 2, deliberately: tests/zoe_arc_selfcheck.py execs the single init-1
# block in this file and asserts the depth-pass pack registers exactly five
# entries. Keeping this pack one priority later leaves that contract intact.

label dst_marcus_zoe_callback_launch:
    # Same exception as dst_nora_reopen_launch above: marcus_met_zoe_callback
    # ends with `return` because _check_talk_followup `call`s it, so the tester's
    # plain Jump() has to supply a call frame. Debug only.
    call marcus_met_zoe_callback
    jump map


init 2 python:

    def _dst_zoe_onb_fresh():
        """Wipes Zoe back to never-met, so the beach meeting can run again."""
        store.zoe_met                 = False
        store.zoe_properly_introduced = False
        store.zoe_intro_beach_done    = False
        store.zoe_intro_alt_done      = False
        store.zoe_bootstrap_complete  = False
        store.zoe_bootstrap_start_day = -1
        store.zoe_first_impression    = ""
        store.zoe_first_callback_sent = False
        store.marcus_beach_reminder_sent   = False
        store.marcus_met_zoe_callback_done = False
        store.npc_contacts = [c for c in store.npc_contacts if c != "zoe"]
        store.npc_messages = [m for m in store.npc_messages
                              if m["tag"] not in ("zoe_first_callback",
                                                  "marcus_beach_reminder")]

    def _dst_zoe_intro_beach():
        _dst_zoe_onb_fresh()
        store.marcus_mentioned_zoe = False
        store.hour = 15.0
        renpy.notify("Zoe intro: fresh (Marcus never mentioned her)")

    def _dst_zoe_intro_beach_marcus():
        _dst_zoe_onb_fresh()
        store.marcus_mentioned_zoe = True
        store.hour = 15.0
        renpy.notify("Zoe intro: fresh + Marcus mentioned her")

    def _dst_zoe_intro_alt():
        """Day 4+, Wednesday 14:00 at Grounds — where check_zoe_alt_intro()
        also agrees, so the natural trigger is testable too."""
        _dst_zoe_onb_fresh()
        store.marcus_mentioned_zoe = True
        if store.day < 4:
            store.day = 4
        store.day += (2 - store.day % 7) % 7        # next Wednesday (her café block)
        store.hour = 14.0
        renpy.notify("Zoe alt intro armed: Wed 14:00, day %d" % store.day)

    def _dst_zoe_callback(impression):
        """Runs the SHIPPING tick, so this exercises the real gate rather than
        hand-queueing the message."""
        store.zoe_met                 = True
        store.zoe_properly_introduced = True
        store.zoe_intro_beach_done    = True
        store.zoe_bootstrap_complete  = False
        store.zoe_first_callback_sent = False
        store.zoe_first_impression    = impression
        store.zoe_bootstrap_start_day = store.day - 2   # exactly the delay
        store.npc_messages = [m for m in store.npc_messages
                              if m["tag"] != "zoe_first_callback"]
        if "zoe" not in store.npc_contacts:
            store.npc_contacts = store.npc_contacts + ["zoe"]
        _zoe_bootstrap_tick()
        deliver_due_messages()
        renpy.notify("Zoe first callback delivered (%s) — open the phone"
                     % (impression or "fallback"))

    def _dst_zoe_cb_observant():
        _dst_zoe_callback("observant")

    def _dst_zoe_cb_honest():
        _dst_zoe_callback("honest")

    def _dst_zoe_cb_banter():
        _dst_zoe_callback("banter")

    def _dst_zoe_cb_fallback():
        _dst_zoe_callback("")

    def _dst_zoe_boot_print():
        """Print scene (A) — the cheapest authored beat, hub Mon-Fri 09-13."""
        _dst_zoe_arc_base()
        store.zoe_properly_introduced = True
        store.zoe_intro_beach_done    = True
        store.zoe_bootstrap_complete  = False
        store.zoe_bootstrap_start_day = store.day - 1
        store.zoe_print_done = False
        store.last_tier_a_beat_day = -1
        _dst_beat_set_weekday(0)                     # Monday
        store.hour = 10.0
        renpy.notify("Bootstrap day 2: Print scene ready at the Hub")

    def _dst_zoe_boot_grounds():
        """The one gate the bootstrap window relaxes: Grounds ordinary time at
        fam 15 (ships at 30) on a 3-day cooldown (ships at 6)."""
        _dst_zoe_arc_base()
        store.zoe_properly_introduced = True
        store.zoe_intro_beach_done    = True
        store.zoe_bootstrap_complete  = False
        store.zoe_bootstrap_start_day = store.day - 1
        set_npc_rel("zoe", "familiarity", 15)        # under the shipping fam>=30
        store.last_tier_a_beat_day = -1
        _dst_beat_clear("zoe_wednesday")
        _dst_beat_set_weekday(2)                     # Wednesday, her café block
        store.hour = 14.0
        renpy.notify("Bootstrap boost armed — walk into Grounds (fam 15)")

    def _dst_zoe_marcus_callback():
        store.zoe_met                      = True
        store.zoe_properly_introduced      = True
        store.marcus_met_zoe_callback_done = False
        store.marcus_met                   = True
        renpy.notify("Marcus callback armed (impression: %s)"
                     % (store.zoe_first_impression or "none"))

    def _dst_zoe_onb_reset():
        _dst_zoe_onb_fresh()
        renpy.notify("Zoe onboarding flags cleared (back to never-met)")

    SCENE_TEST_REGISTRY.update({
        "zoe_beach_intro": {
            "title": "Zoe — First Beach Introduction",
            "category": "Relationship Scenes",
            "desc": "The authored first meeting (locations.rpy beach_meet_zoe) plus the "
                    "onboarding tail: Marcus recognition, the open thread, the "
                    "first-impression record and the contact exchange.",
            "label": "zoe_beach_intro",
            "presets": {
                "fresh": _dst_zoe_intro_beach,
                "Marcus mentioned": _dst_zoe_intro_beach_marcus,
            },
            "checkpoints": {
                "approach route": "zoe_beach_approach",
                "watch route": "zoe_beach_watch",
                "onboarding tail": "zoe_beach_intro_tail",
            },
            "reset": _dst_zoe_onb_reset,
            "notes": "Naturally fires as the FIRST branch of location_beach whenever "
                     "not zoe_met and hour < 19 — no day cap. Sets zoe_first_impression, "
                     "adds Zoe to npc_contacts and stamps zoe_bootstrap_start_day.",
        },
        "zoe_alt_intro": {
            "title": "Zoe — First Beach Alt Intro",
            "category": "Relationship Scenes",
            "desc": "Day 4+ fallback for a player who never walked to the beach. "
                    "Shorter; same four facts, same flags.",
            "label": "zoe_alt_intro",
            "presets": {
                "Grounds (Wed 14:00)": _dst_zoe_intro_alt,
            },
            "checkpoints": None,
            "reset": _dst_zoe_onb_reset,
            "notes": "check_zoe_alt_intro() runs at location_cafe and location_hub, "
                     "gated on npc_here() so her real schedule decides the window "
                     "(Hub Mon-Fri 09-13, Grounds Wed 13-18).",
        },
        "zoe_first_callback": {
            "title": "Zoe — First Phone Callback",
            "category": "Relationship Scenes",
            "desc": "Her one scripted text, two days after the intro. Four variants "
                    "keyed to zoe_first_impression. No reply required.",
            "label": "map",
            "presets": {
                "observant": _dst_zoe_cb_observant,
                "honest":    _dst_zoe_cb_honest,
                "banter":    _dst_zoe_cb_banter,
                "no impression (fallback)": _dst_zoe_cb_fallback,
            },
            "checkpoints": None,
            "reset": _dst_zoe_onb_reset,
            "notes": "Preset-only entry — it runs _zoe_bootstrap_tick() and delivers "
                     "immediately, so open the phone rather than using Launch. Queued "
                     "directly, NOT through the initiative picker: that is a 0.25-0.55 "
                     "daily roll on a one-message global budget and cannot honour a "
                     "2-day promise.",
        },
        "zoe_bootstrap_followup": {
            "title": "Zoe — Early Follow-up (Print scene ready)",
            "category": "Relationship Scenes",
            "desc": "The two beats reachable inside the bootstrap window: the Print "
                    "scene (no relationship gate) and Grounds ordinary time (gate relaxed).",
            "label": "zoe_print_scene",
            "presets": {
                "print ready (Hub, Mon 10:00)": _dst_zoe_boot_print,
                "grounds boost (Wed 14:00)": _dst_zoe_boot_grounds,
            },
            "checkpoints": None,
            "reset": _dst_zoe_arc_reset,
            "notes": "The grounds preset is state-only — walk into Grounds instead of "
                     "using Launch. Window is 10 days from zoe_bootstrap_start_day and "
                     "only relaxes zoe_wednesday (fam 30→12, cooldown 6→3).",
        },
        "marcus_zoe_callback": {
            "title": "Marcus — Met Zoe Callback",
            "category": "Relationship Scenes",
            "desc": "Fires once in Marcus's next Talk after you've met Zoe.",
            "label": "dst_marcus_zoe_callback_launch",
            "presets": {
                "armed": _dst_zoe_marcus_callback,
            },
            "checkpoints": None,
            "reset": _dst_zoe_marcus_callback,
            "notes": "Naturally reached through _check_talk_followup('marcus'), which "
                     "sits in front of the generic topic screen. Has two extra lines "
                     "when zoe_first_impression is 'banter' or 'honest'.",
        },
    })


# ═══════════════════════════════════════════════════════════════════
# MARCUS — EVERYDAY FRIENDSHIP (marcus_friendship.rpy / marcus_onboarding.rpy)
# ═══════════════════════════════════════════════════════════════════
# Every entry launches through marcus_friendship_test, which gives the beat a
# call frame (the beats `return` — they are normally `call`ed from
# npc_interact) and a sprite the interaction UI would otherwise own.
init 3 python:

    def _dst_mf_base():
        """Marcus met, on speaking terms, budgets clear, standing in the bar
        during his real shift (npc_schedules.rpy: Mon-Fri 16-24)."""
        store.marcus_met = True
        mark_npc_encountered("marcus")
        store.move_in_complete = True
        if "marcus" not in store.npc_contacts:
            store.npc_contacts = store.npc_contacts + ["marcus"]
        set_npc_rel("marcus", "familiarity", 40)
        set_npc_rel("marcus", "affection", 32)
        set_npc_rel("marcus", "trust", 25)
        store.marcus_beat_last_day = -1
        store.marcus_ctx_talk_last_day = -1
        store.current_loc = "location_bar"
        store.day += (0 - store.day % 7) % 7    # next Monday
        store.hour = 19.0

    def _dst_mf_arm(label_name, beat_id=None):
        store.marcus_test_label = label_name
        store.marcus_beat_last_day = -1
        if beat_id:
            _d = dict(store.tier_a_beat_last_day)
            _d.pop(beat_id, None)
            store.tier_a_beat_last_day = _d

    def _dst_mf_first_week():
        _dst_mf_base()
        store.day = 2
        store.marcus_mc_checkin_done = False
        store.active_careers = {}
        _dst_mf_arm("marcus_first_week_checkin")
        renpy.notify("Marcus: first-week check-in (day 2, unemployed)")

    def _dst_mf_work_none():
        _dst_mf_base()
        store.active_careers = {}
        store.job_id = None
        store.job_title = None
        store.marcus_work_check_last = -1
        _dst_mf_arm("marcus_beat_how_work", "marcus_fr_how_work")
        renpy.notify("Marcus: how's work — unemployed")

    def _dst_mf_work_new():
        _dst_mf_base()
        store.active_careers = {"it": {"rank": 0, "perf": 40}}
        _sync_job("it")
        store.marcus_known_career = None
        store.marcus_known_rank = -1
        store.marcus_work_check_last = -1
        _dst_mf_arm("marcus_beat_how_work", "marcus_fr_how_work")
        renpy.notify("Marcus: how's work — new job (IT rank 0)")

    def _dst_mf_work_established():
        _dst_mf_base()
        store.active_careers = {"it": {"rank": 2, "perf": 60}}
        _sync_job("it")
        store.marcus_known_career = "it"
        store.marcus_known_rank = 2
        store.marcus_heard_job_got = True
        store.marcus_work_check_last = -1
        _dst_mf_arm("marcus_beat_how_work", "marcus_fr_how_work")
        renpy.notify("Marcus: how's work — established (IT rank 2)")

    def _dst_mf_promotion():
        _dst_mf_base()
        store.active_careers = {"it": {"rank": 2, "perf": 60}}
        _sync_job("it")
        store.marcus_known_career = "it"
        store.marcus_known_rank = 1      # told about rank 1; MC is now rank 2
        store.marcus_heard_job_got = True
        store.marcus_heard_promotion = False
        store.marcus_work_check_last = -1
        _dst_mf_arm("marcus_beat_how_work", "marcus_fr_how_work")
        renpy.notify("Marcus: promotion reaction armed")

    def _dst_mf_interview_cb():
        _dst_mf_base()
        store.active_careers = {}
        store.job_id = None
        store.mc_told_marcus_interview = True
        store.marcus_interview_told_day = store.day - 2
        store.marcus_interview_text_sent = False
        store.marcus_known_career = None
        _dst_mf_arm("marcus_ctx_talk")
        renpy.notify("Marcus: interview callback armed (Talk + text on next sleep)")

    def _dst_mf_had_a_day():
        _dst_mf_base()
        _dst_mf_arm("marcus_beat_had_a_day", "marcus_fr_had_a_day")
        renpy.notify("Marcus: had a day")

    def _dst_mf_look_dead():
        _dst_mf_base()
        store.need_energy = 18
        store.wed_marcus_low_energy_count = 3   # the shipping wevent has retired
        _dst_mf_arm("marcus_beat_you_look_dead", "marcus_fr_you_look_dead")
        renpy.notify("Marcus: you look dead (energy 18)")

    def _dst_mf_hangout():
        _dst_mf_base()
        _dst_mf_arm("marcus_beat_five_minutes", "marcus_fr_five_minutes")
        renpy.notify("Marcus: random hangout (five minutes)")

    def _dst_mf_hangout_food():
        _dst_mf_base()
        store.need_hunger = 40
        _dst_mf_arm("marcus_beat_food_run", "marcus_fr_food_run")
        renpy.notify("Marcus: food run")

    def _dst_mf_hangout_court():
        _dst_mf_base()
        store.npc_invitation_pending = None
        store.marcus_court_offer_last_day = -999
        _dst_mf_arm("marcus_beat_court_later", "marcus_fr_court")
        renpy.notify("Marcus: court invite (uses marcus_park_invite route)")

    def _dst_mf_come_with():
        _dst_mf_base()
        _dst_mf_arm("marcus_beat_come_with_me", "marcus_fr_come_with")
        renpy.notify("Marcus: come with me")

    def _dst_mf_random_story():
        _dst_mf_base()
        _dst_mf_arm("marcus_beat_random_story", "marcus_fr_random_story")
        renpy.notify("Marcus: random story (5-variant rotation)")

    def _dst_mf_good_news():
        _dst_mf_base()
        store.active_careers = {"it": {"rank": 1, "perf": 60}}
        _sync_job("it")
        record_game_event("promote_it_r1_day%d" % store.day, "career",
                          "Promoted: " + (store.job_title or "it"),
                          summary=False, journal=True,
                          metadata={"cid": "it", "new_rank": 1})
        publish_player_fact("got_promoted", "it_r1")
        _dst_mf_arm("marcus_beat_good_shift", "marcus_fr_good_shift")
        renpy.notify("Marcus: good-news reaction (career event on record)")

    def _dst_mf_bad_news():
        _dst_mf_base()
        store.active_careers = {"corporate": {"rank": 0, "perf": 20}}
        _sync_job("corporate")
        store.mc_told_marcus_job_trouble = True
        store.marcus_job_trouble_career = "corporate"
        store.marcus_job_trouble_day = store.day - 6
        store.marcus_job_callback_done = False
        store.need_energy = 22
        _dst_mf_arm("marcus_beat_bad_shift", "marcus_fr_bad_shift")
        renpy.notify("Marcus: bad-shift reaction armed")

    def _dst_mf_that_job():
        _dst_mf_bad_news()
        _dst_mf_arm("marcus_beat_that_job_again", "marcus_fr_that_job")
        renpy.notify("Marcus: still hate that place — armed")

    def _dst_mf_nothing_really():
        _dst_mf_base()
        set_npc_rel("marcus", "familiarity", 65)
        set_npc_rel("marcus", "affection", 62)
        set_npc_rel("marcus", "trust", 58)
        _dst_mf_arm("marcus_beat_nothing_really", "marcus_fr_nothing")
        renpy.notify("Marcus: nothing, really (Close)")

    def _dst_mf_need_anything():
        _dst_mf_nothing_really()
        _dst_mf_arm("marcus_beat_need_anything", "marcus_fr_need_any")
        renpy.notify("Marcus: need anything (Close)")

    def _dst_mf_still_alive():
        _dst_mf_base()
        store.day = 3
        store.hour = 19.0
        store.marcus_mc_checkin_done = True    # the check-in already landed
        store.marcus_still_alive_done = False
        store.marcus_lock_joke_active = False
        _dst_mf_arm("marcus_beat_still_alive", "marcus_fr_still_alive")
        renpy.notify("Marcus: Still Alive (day 3, check-in done)")

    def _dst_mf_5am():
        _dst_mf_base()
        store.current_loc = "location_park"
        store.hour = 7.5
        store.marcus_five_am_known = False
        store.marcus_five_am_talk_done = False
        _d = dict(store.topic_arc_done); _d.pop("marcus_sports_1", None)
        store.topic_arc_done = _d
        _dst_mf_arm("marcus_beat_5am", "marcus_fr_5am")
        renpy.notify("Marcus: 5 AM (park, 07:30)")

    def _dst_mf_5am_zoe():
        _dst_mf_5am()
        store.zoe_properly_introduced = True
        renpy.notify("Marcus: 5 AM + the Zoe tag")

    def _dst_mf_job_good_cb():
        _dst_mf_base()
        store.active_careers = {"it": {"rank": 0, "perf": 55}}
        _sync_job("it")
        store.marcus_known_career = "it"
        store.marcus_known_rank = 0
        store.marcus_heard_job_got = True
        store.mc_told_marcus_career_good = True
        store.mc_told_marcus_job_trouble = False
        store.marcus_career_good_day = store.day - 4
        _dst_mf_arm("marcus_beat_job_still_good", "marcus_fr_job_good")
        renpy.notify("Marcus: job-still-good callback (told 4 days ago)")

    def _dst_mf_food_run():
        _dst_mf_base()
        store.need_hunger = 40
        _dst_mf_arm("marcus_beat_food_run", "marcus_fr_food_run")
        renpy.notify("Marcus: food run")

    def _dst_mf_bball():
        _dst_mf_base()
        set_npc_rel("marcus", "familiarity", 55)
        set_npc_rel("marcus", "affection", 48)
        set_npc_rel("marcus", "trust", 40)
        _d = dict(store.topic_arc_done); _d.pop("marcus_sports_2", None)
        store.topic_arc_done = _d
        store.mc_knows_marcus_bball_offer = False
        store.marcus_bball_talk_done = False
        _dst_mf_arm("arc_marcus_sports_2")
        renpy.notify("Marcus: Could've Left (arc_marcus_sports_2 — the canonical one)")

    def _dst_mf_msg_pack():
        """State-only. Opens every gate in the authored message pack at once,
        then sleep — the picker still only sends one, from one NPC, per day."""
        _dst_mf_base()
        set_npc_rel("marcus", "familiarity", 55)
        set_npc_rel("marcus", "affection", 48)
        set_npc_rel("marcus", "trust", 40)
        store.marcus_five_am_known = True
        store.mc_told_marcus_interview = True
        store.marcus_interview_told_day = store.day - 2
        store.marcus_known_career = None
        store.active_careers = {}
        store.job_id = None
        store.npc_invitation_pending = None
        store.marcus_court_offer_last_day = -999
        store.npc_last_seen["marcus"] = store.day - 8   # opens M1 and M7
        _d = dict(store.npc_initiative_last_day); _d["marcus"] = -999
        store.npc_initiative_last_day = _d
        store.npc_initiative_last_global_day = -1
        _clear_initiative_pending("marcus")
        store.npc_messages = [_m for _m in store.npc_messages
                              if not _m["tag"].startswith("marcus_msg_")]
        renpy.notify("Marcus message pack armed (M1-M8 + 'You free?') — sleep")

    def _dst_mf_phone_ready():
        """State-only. Sleep to the next day — the picker runs in new_day and
        shares the one-contact-per-day budget with every other NPC."""
        _dst_mf_base()
        _d = dict(store.npc_initiative_last_day); _d["marcus"] = -999
        store.npc_initiative_last_day = _d
        store.npc_initiative_last_global_day = -1
        _clear_initiative_pending("marcus")
        store.npc_messages = [_m for _m in store.npc_messages
                              if not _m["tag"].startswith("marcus_msg_")]
        renpy.notify("Marcus phone pool armed — sleep one night")

    _MF_TEST_BEAT_IDS = (
        "marcus_fr_good_shift", "marcus_fr_you_look_dead", "marcus_fr_bad_shift",
        "marcus_fr_that_job", "marcus_fr_how_work", "marcus_fr_had_a_day",
        "marcus_fr_random_story", "marcus_fr_five_minutes", "marcus_fr_food_run",
        "marcus_fr_court", "marcus_fr_come_with", "marcus_fr_need_any",
        "marcus_fr_nothing", "marcus_fr_still_alive", "marcus_fr_5am",
        "marcus_fr_job_good")

    def _dst_mf_reset():
        _d = dict(store.tier_a_beat_last_day)
        for _b in _MF_TEST_BEAT_IDS:
            _d.pop(_b, None)
        store.tier_a_beat_last_day = _d
        store.marcus_beat_last_day = -1
        store.marcus_ctx_talk_last_day = -1
        store.marcus_work_check_last = -1
        store.marcus_had_a_day_last = -1
        store.marcus_had_a_day_topic = ""
        renpy.notify("Marcus friendship cooldowns cleared")

    SCENE_TEST_REGISTRY.update({
        "marcus_still_alive": {
            "title": "Marcus — Still Alive",
            "category": "Relationship Scenes",
            "desc": "\"Still alive.\" \"Barely.\" \"Good.\" Day 2-5, costs almost nothing.",
            "label": "marcus_friendship_test",
            "presets": {"day 3": _dst_mf_still_alive},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "One-shot (marcus_still_alive_done). The lock branch sets "
                     "marcus_lock_joke_active, which the mstory_lock random story "
                     "already pays off. \"You said you wake up at five\" is NOT an "
                     "error: arcs.rpy:176 has him up at six and awake since five.",
        },
        "marcus_5am": {
            "title": "Marcus — 5 AM",
            "category": "Relationship Scenes",
            "desc": "Park, before 09:00. Why he's awake, and why it isn't discipline.",
            "label": "marcus_friendship_test",
            "presets": {
                "park 07:30": _dst_mf_5am,
                "+ Zoe known": _dst_mf_5am_zoe,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Closes all three routes to the same fact: it completes "
                     "arc_marcus_sports_1 and sets marcus_five_am_talk_done, and is "
                     "gated on neither having happened. Sets marcus_five_am_known, "
                     "which is the ONLY gate on the \"Been awake since 5.\" text. "
                     "The Zoe tag needs zoe_properly_introduced.",
        },
        "marcus_job_still_good": {
            "title": "Marcus — Job Going Well Callback",
            "category": "Relationship Scenes",
            "desc": "\"Job still good?\" \"You remembered?\" \"I remember things.\"",
            "label": "marcus_friendship_test",
            "presets": {"told 4 days ago": _dst_mf_job_good_cb},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Window is 3-7 days after marcus_career_good_day, same career, "
                     "and no job-trouble flag. Outside that it retires silently "
                     "rather than asking about a claim the state no longer supports.",
        },
        "marcus_job_hate_cb": {
            "title": "Marcus — Job Hate Callback",
            "category": "Relationship Scenes",
            "desc": "\"Still hate that place?\" Asked ONCE per complaint.",
            "label": "marcus_friendship_test",
            "presets": {"complained 6 days ago": _dst_mf_that_job},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "marcus_job_callback_done closes it whatever the answer; only a "
                     "fresh complaint reopens it. Never fires about a job MC has "
                     "since left (marcus_job_trouble_career).",
        },
        "marcus_food_run": {
            "title": "Marcus — Food Run",
            "category": "Relationship Scenes",
            "desc": "\"You eaten?\" \"That's a weird hello.\" Declining costs nothing.",
            "label": "marcus_friendship_test",
            "presets": {"cafe/bar": _dst_mf_food_run},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Only offered at the café or the bar. Accept = 20 min, hunger "
                     "+12, familiarity +2 / affection +1. The \"some guy argued with "
                     "me\" story is deliberately unplaced — do not give it a venue.",
        },
        "marcus_bball_offer": {
            "title": "Marcus — Could've Left",
            "category": "Relationship Scenes",
            "desc": "The semi-pro offer at eighteen. This is arc_marcus_sports_2.",
            "label": "marcus_friendship_test",
            "presets": {"friend, arc unseen": _dst_mf_bball},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "NOT a new scene — arcs.rpy:184 already owns this material "
                     "(offer at eighteen, dad was sick, \"Sometimes.\"). Reached "
                     "through the ordinary Talk grid, topic 'sports'. Completing it "
                     "sets mc_knows_marcus_bball_offer, which now gates the "
                     "\"Ask about the basketball\" contextual option.",
        },
        "marcus_msg_pack": {
            "title": "Marcus — Message Pack",
            "category": "Relationship Scenes",
            "desc": "State-only. Opens every authored text gate, then sleep.",
            "label": "map",
            "presets": {"arm all": _dst_mf_msg_pack},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "M1 alive / M2 food / M3 court in 30 / M4 how'd it go / M5 "
                     "vending machine / M6 tonight / M7 haven't seen you / M8 awake "
                     "since 5 / \"You free?\". M4 cannot fire without a real pending "
                     "interview. The picker still sends at most one NPC per day.",
        },
        "marcus_first_week": {
            "title": "Marcus — First Week Check-in",
            "category": "Relationship Scenes",
            "desc": "Did you survive the first night. Asks about work without lecturing.",
            "label": "marcus_friendship_test",
            "presets": {"day 2, no job": _dst_mf_first_week},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Also reachable as the marcus_msg_first_week text (day 1-4). "
                     "Whichever lands first sets marcus_mc_checkin_done.",
        },
        "marcus_how_work_none": {
            "title": "Marcus — How's Work (unemployed)",
            "category": "Relationship Scenes",
            "desc": "\"Figure out the work situation yet?\" No advice given.",
            "label": "marcus_friendship_test",
            "presets": {"no career": _dst_mf_work_none},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "The interview answer sets mc_told_marcus_interview and arms the "
                     "2-day text callback.",
        },
        "marcus_how_work_new": {
            "title": "Marcus — How's Work (new job)",
            "category": "Relationship Scenes",
            "desc": "Rank 0. Dry observation, no encouragement speech.",
            "label": "marcus_friendship_test",
            "presets": {"IT rank 0": _dst_mf_work_new},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "\"I don't love it\" records WHICH career it was, so the callback "
                     "can never go stale after a job change.",
        },
        "marcus_how_work_est": {
            "title": "Marcus — How's Work (established)",
            "category": "Relationship Scenes",
            "desc": "\"Work still treating you like a human being?\"",
            "label": "marcus_friendship_test",
            "presets": {
                "IT rank 2": _dst_mf_work_established,
                "promotion reaction": _dst_mf_promotion,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "4-day cooldown lives in marcus_work_check_last. The promotion "
                     "branch fires when the real rank exceeds marcus_known_rank.",
        },
        "marcus_interview_cb": {
            "title": "Marcus — Interview Callback",
            "category": "Relationship Scenes",
            "desc": "He remembered. Contextual Talk option plus the phone text.",
            "label": "marcus_friendship_test",
            "presets": {"told 2 days ago": _dst_mf_interview_cb},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Reads the real career state first: if MC took a job since, the "
                     "scene congratulates instead of asking. Text version queues on "
                     "the next new_day.",
        },
        "marcus_had_a_day": {
            "title": "Marcus — Marcus Had a Day",
            "category": "Relationship Scenes",
            "desc": "He leads. Four rotating topics (delivery / cancelled / game / chili).",
            "label": "marcus_friendship_test",
            "presets": {
                "armed": _dst_mf_had_a_day,
                "random story instead": _dst_mf_random_story,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Stores marcus_had_a_day_topic so \"Ask what happened\" appears in "
                     "contextual Talk for the rest of that day. Cooldown 5.",
        },
        "marcus_look_dead": {
            "title": "Marcus — You Look Dead",
            "category": "Relationship Scenes",
            "desc": "\"You look terrible.\" ... \"Respectfully.\" No energy restored.",
            "label": "marcus_friendship_test",
            "presets": {"energy 18": _dst_mf_look_dead},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Gated behind wed_marcus_low_energy_count >= 3 so it never "
                     "duplicates wevent_marcus_low_energy_comment.",
        },
        "marcus_hangout": {
            "title": "Marcus — Random Hangout",
            "category": "Relationship Scenes",
            "desc": "Ordinary time: five minutes, a food run, an errand, or the court.",
            "label": "marcus_friendship_test",
            "presets": {
                "five minutes": _dst_mf_hangout,
                "food run": _dst_mf_hangout_food,
                "come with me": _dst_mf_come_with,
                "court later": _dst_mf_hangout_court,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Court accept writes npc_invitation_pending marcus_park_invite — "
                     "the shipping route resolved by wevent_marcus_park_invite_scene.",
        },
        "marcus_good_news": {
            "title": "Marcus — Good News Reaction",
            "category": "Relationship Scenes",
            "desc": "He noticed you walked in differently. Interested, not sycophantic.",
            "label": "marcus_friendship_test",
            "presets": {
                "promotion on record": _dst_mf_good_news,
                "bad shift instead": _dst_mf_bad_news,
                "still hate that place": _dst_mf_that_job,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Eligibility reads the career journal entry promote() writes and "
                     "the got_promoted public fact — no new tracking added.",
        },
        "marcus_nothing_really": {
            "title": "Marcus — Nothing, Really",
            "category": "Relationship Scenes",
            "desc": "\"No reason.\" \"No reason?\" \"You need a reason now?\"",
            "label": "marcus_friendship_test",
            "presets": {
                "close": _dst_mf_nothing_really,
                "need anything": _dst_mf_need_anything,
            },
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Close/Trusted stage only (npc_relationship_stage).",
        },
        "marcus_phone_setup": {
            "title": "Marcus — Phone Check-in setup",
            "category": "Relationship Scenes",
            "desc": "State-only. Arms the initiative pool, then sleep one night.",
            "label": "map",
            "presets": {"armed": _dst_mf_phone_ready},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "Eight new variants share the ONE unprompted contact per day with "
                     "every other NPC. Marcus cooldown is 3, or 2 for the first 14 "
                     "days. Use the presets, not Launch.",
        },
    })


# ═══════════════════════════════════════════════════════════════════════
# RELATIONSHIP CONTINUITY & PRESENCE (relationship_continuity.rpy)
# ═══════════════════════════════════════════════════════════════════════
# Greetings and farewells are reached by TALKING to the person, not by a
# label — so every greeting entry here is state-only ("label": "map"): set a
# preset, walk to them, press Talk. The micro beats, friction and repairs DO
# have labels, launched through rc_continuity_test, which supplies the call
# frame they need (they `return` — they are normally `call`ed from the
# greeting) and a sprite the interaction UI would otherwise own.
init 4 python:

    def _dst_rc_reset():
        """Clears every anti-repeat gate this pack owns, on both characters."""
        store.rc_marcus_greet_day      = -999
        store.rc_marcus_farewell_day   = -999
        store.rc_zoe_greet_day         = -999
        store.rc_zoe_farewell_day      = -999
        store.rc_zoe_sit_day           = -999
        store.rc_zoe_wed_farewell_done = False
        store.rc_marcus_busy_day       = -999
        store.rc_zoe_busy_day          = -999
        store.rc_micro_last            = {}
        store.rc_micro_fired           = {}
        store.rc_marcus_f1_done        = False
        store.rc_marcus_f2_done        = False
        store.rc_marcus_friction_day   = -999
        store.rc_marcus_repair_done    = True
        store.rc_zoe_f1_done           = False
        store.rc_zoe_f2_done           = False
        store.rc_zoe_friction_day      = -999
        store.rc_zoe_repair_done       = True
        store.marcus_greet_late_done   = False
        store.marcus_greet_late_day    = -999
        renpy.notify("Continuity gates cleared (greetings, micro, friction)")

    def _dst_rc_arm(label_name, npc_id):
        store.rc_test_label = label_name
        store.rc_test_npc   = npc_id

    def _dst_rc_set_life(npc_id, state):
        """Writes the REAL npc_initiative.rpy record (_npc_personal_life), so
        the busy/unavailable gates are exercised through npc_life_state()
        rather than through a debug-only flag."""
        _p = dict(store._npc_personal_life)
        _p[npc_id] = {"state": state, "started_day": store.day,
                      "expires_day": store.day + 3}
        store._npc_personal_life = _p

    # ── Marcus greeting bands ────────────────────────────────────────────
    def _dst_rc_m_band(fam, aff, trust, gap, note):
        _dst_mf_base()
        set_npc_rel("marcus", "familiarity", fam)
        set_npc_rel("marcus", "affection", aff)
        set_npc_rel("marcus", "trust", trust)
        _dst_rc_reset()
        store.marcus_last_seen_day = store.day - gap if gap else store.day
        renpy.notify("Marcus greeting: %s — walk to the bar and Talk" % note)

    def _dst_rc_m_acquaintance():
        # Below every stage threshold: "Hey, neighbor." / "There he is."
        _dst_rc_m_band(22, 18, 10, 0, "acquaintance")

    def _dst_rc_m_friend():
        # friend band, no gap: "You free?"
        _dst_rc_m_band(52, 47, 38, 0, "friend (\"You free?\")")

    def _dst_rc_m_friend_gap():
        # gap >= 5 wins over every stage line: "Haven't seen you in a minute."
        _dst_rc_m_band(52, 47, 38, 7, "friend after 7 days away")

    def _dst_rc_m_close():
        # close band + the one-shot playful variant still unspent.
        _dst_rc_m_band(65, 62, 58, 0, "close (\"You're late.\" one-shot)")

    def _dst_rc_m_busy():
        # In the bar, on shift, and NOT yet a friend.
        _dst_rc_m_band(30, 25, 15, 0, "busy (bar shift, pre-friend)")
        store.current_loc = "location_bar"
        store.hour = 19.0
        renpy.notify("Marcus busy armed: bar, 19:00, acquaintance")

    # ── Zoe greeting bands ───────────────────────────────────────────────
    def _dst_rc_z_band(fam, aff, trust, gap, note):
        _dst_zoe_arc_base()
        store.zoe_affection = aff
        store.zoe_trust     = trust
        set_npc_rel("zoe", "familiarity", fam)
        set_npc_rel("zoe", "affection", aff)
        set_npc_rel("zoe", "trust", trust)
        set_npc_rel("zoe", "respect", 30)
        _dst_rc_reset()
        store.rc_zoe_last_seen_day = store.day - gap if gap else store.day
        renpy.notify("Zoe greeting: %s — find her and Talk" % note)

    def _dst_rc_z_acquaintance():
        _dst_rc_z_band(22, 18, 10, 0, "acquaintance (\"There you are.\")")

    def _dst_rc_z_friend():
        _dst_rc_z_band(52, 47, 38, 0, "friend (\"You have five minutes?\")")

    def _dst_rc_z_friend_gap():
        _dst_rc_z_band(52, 47, 38, 7, "friend after 7 days (\"You alive?\")")

    def _dst_rc_z_close():
        _dst_rc_z_band(65, 62, 58, 0, "close (\"Sit. I need another opinion.\")")

    def _dst_rc_z_busy():
        """Uses the REAL life-state record, not a fabricated flag."""
        _dst_rc_z_band(40, 35, 30, 0, "busy")
        store.rc_zoe_f2_done = True          # so F2 does not pre-empt busy
        _dst_rc_set_life("zoe", "busy_work")
        renpy.notify("Zoe busy armed: life state busy_work")

    def _dst_rc_z_stressed():
        _dst_rc_z_band(40, 35, 30, 0, "stressed (friction F2)")
        _dst_rc_set_life("zoe", "stressed_week")
        renpy.notify("Zoe F2 armed: life state stressed_week — Talk to her")

    # ── Pre-Talk callbacks ───────────────────────────────────────────────
    def _dst_rc_m_pretalk_interview():
        """Marcus opens the interview himself instead of offering a menu."""
        _dst_mf_base()
        _dst_rc_reset()
        store.active_careers = {}
        store.job_id = None
        store.marcus_known_career = None
        store.mc_told_marcus_interview  = True
        store.marcus_interview_told_day = store.day - 2
        store.marcus_mc_checkin_done    = True
        renpy.notify("Marcus pre-talk interview armed — Talk to him")

    def _dst_rc_z_pretalk_submission():
        """Zoe opens the open-call result herself."""
        _dst_rc_z_band(52, 47, 38, 0, "submission callback")
        store.zoe_deadline_submitted     = True
        store.zoe_deadline_followup_done = False
        store.zoe_deadline_day           = store.day - 4
        store.knows_zoe_gallery_goal     = True
        renpy.notify("Zoe pre-talk submission armed — Talk to her")

    # ── Micro beats ──────────────────────────────────────────────────────
    def _dst_rc_m_micro():
        _dst_mf_base()
        _dst_rc_reset()
        _dst_rc_arm("rc_marcus_micro_customer", "marcus")
        renpy.notify("Marcus micro: bad customer (bar)")

    def _dst_rc_m_micro_dumb():
        _dst_mf_base()
        _dst_rc_reset()
        _dst_rc_arm("rc_marcus_micro_dumb", "marcus")
        renpy.notify("Marcus micro: the shop trip")

    def _dst_rc_m_micro_ten():
        _dst_mf_base()
        _dst_rc_reset()
        _dst_rc_arm("rc_marcus_micro_ten_minutes", "marcus")
        renpy.notify("Marcus micro: ten minutes")

    def _dst_rc_m_micro_zoe():
        _dst_mf_base()
        _dst_rc_reset()
        store.zoe_properly_introduced = True
        _dst_rc_arm("rc_marcus_micro_zoe", "marcus")
        renpy.notify("Marcus micro: Zoe was in Saturday")

    def _dst_rc_m_micro_lock():
        _dst_mf_base()
        _dst_rc_reset()
        store.apartment_tier = max(store.apartment_tier, 2)
        store.marcus_lock_joke_active = True
        _dst_rc_arm("rc_marcus_micro_lock", "marcus")
        renpy.notify("Marcus micro: the lock, version 3 (apartment upgraded)")

    def _dst_rc_z_micro():
        _dst_rc_z_band(45, 40, 32, 0, "micro")
        _dst_rc_arm("rc_zoe_micro_sign", "zoe")
        renpy.notify("Zoe micro: sign complaint (3-variant rotation)")

    def _dst_rc_z_micro_obs():
        _dst_rc_z_band(45, 40, 32, 0, "micro")
        store.knows_zoe_art_interest = True
        _dst_rc_arm("rc_zoe_micro_observation", "zoe")
        renpy.notify("Zoe micro: the light on the glass")

    def _dst_rc_z_micro_break():
        _dst_rc_z_band(52, 47, 38, 0, "micro")
        _dst_rc_arm("rc_zoe_micro_break", "zoe")
        renpy.notify("Zoe micro: five-minute break")

    def _dst_rc_z_micro_marcus():
        _dst_rc_z_band(45, 40, 32, 0, "micro")
        store.marcus_met = True
        store.mc_knows_marcus_bball_offer = True
        _dst_rc_arm("rc_zoe_micro_marcus", "zoe")
        renpy.notify("Zoe micro: Marcus and the score")

    # ── Friction + repair ────────────────────────────────────────────────
    def _dst_rc_m_friction():
        _dst_rc_m_band(52, 47, 38, 0, "friction F1")
        _dst_rc_arm("rc_marcus_friction_push", "marcus")
        renpy.notify("Marcus F1 armed (normally after you decline an invite)")

    def _dst_rc_m_friction_comp():
        _dst_rc_m_band(52, 47, 38, 0, "friction F2")
        _d = dict(store.bar_game_cooldowns)
        _d["pool_marcus"] = store.day - 1
        store.bar_game_cooldowns = _d
        _dst_rc_arm("rc_marcus_friction_competitive", "marcus")
        renpy.notify("Marcus F2 armed (pool game yesterday)")

    def _dst_rc_m_repair():
        _dst_rc_m_band(52, 47, 38, 0, "repair")
        store.rc_marcus_f1_done      = True
        store.rc_marcus_friction_day = store.day - 1
        store.rc_marcus_repair_done  = False
        _dst_rc_arm("rc_marcus_repair", "marcus")
        renpy.notify("Marcus repair armed (friction yesterday) — or just Talk")

    def _dst_rc_z_friction():
        _dst_rc_z_band(52, 47, 38, 0, "friction F1")
        store.zoe_second_opinion_done   = True
        store.zoe_second_opinion_choice = "structure"
        store.zoe_second_opinion_day    = store.day - 3
        _dst_rc_arm("rc_zoe_friction_reads_harsh", "zoe")
        renpy.notify("Zoe F1 armed (she gave you two layouts three days ago)")

    def _dst_rc_z_repair():
        _dst_rc_z_band(52, 47, 38, 0, "repair")
        store.rc_zoe_f1_done      = True
        store.rc_zoe_friction_day = store.day - 1
        store.rc_zoe_repair_done  = False
        _dst_rc_arm("rc_zoe_repair", "zoe")
        renpy.notify("Zoe repair armed (friction yesterday) — or just Talk")

    # ── Shared routines ──────────────────────────────────────────────────
    def _dst_rc_z_routine():
        """Threshold met, every picker gate cleared. Sleep one night."""
        _dst_rc_z_band(52, 47, 38, 0, "routine shorthand")
        store.zoe_grounds_count = 2
        store.npc_initiative_last_global_day = -1
        store._p68_contact_day = -1
        _ld = dict(store.npc_initiative_last_day); _ld["zoe"] = -999
        store.npc_initiative_last_day = _ld
        _clear_initiative_pending("zoe")
        renpy.notify("Zoe routine armed: grounds_count 2 — sleep, then check phone")

    def _dst_rc_z_routine_below():
        """Threshold NOT met — proves the shorthand stays locked."""
        _dst_rc_z_routine()
        store.zoe_grounds_count = 1
        renpy.notify("Zoe routine BELOW threshold (count 1) — \"Grounds?\" must not send")

    def _dst_rc_m_routine():
        _dst_mf_base()
        _dst_rc_reset()
        store.marcus_bar_count = 2
        store.npc_initiative_last_global_day = -1
        _ld = dict(store.npc_initiative_last_day); _ld["marcus"] = -999
        store.npc_initiative_last_day = _ld
        _clear_initiative_pending("marcus")
        renpy.notify("Marcus routine armed: bar_count 2 — sleep, then check phone")

    def _dst_rc_m_routine_below():
        _dst_rc_m_routine()
        store.marcus_bar_count = 1
        renpy.notify("Marcus routine BELOW threshold (count 1) — must not send")

    SCENE_TEST_REGISTRY.update({
        "rc_marcus_greetings": {
            "title": "Marcus — Greeting Bands",
            "category": "Relationship Scenes",
            "desc": "Acquaintance / friend / friend-after-absence / close + the "
                    "\"You're late.\" one-shot. State-only: set a preset, then Talk.",
            "label": "map",
            "presets": {
                "acquaintance": _dst_rc_m_acquaintance,
                "friend": _dst_rc_m_friend,
                "friend, 7 days away": _dst_rc_m_friend_gap,
                "close + playful one-shot": _dst_rc_m_close,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "The ladder itself is the shipping one in interact.rpy "
                     "marcus_greet — this pass only bracketed it. Gap wins over stage; "
                     "\"You're late.\" is one-shot (marcus_greet_late_done). A second "
                     "Talk on the same day gets \"Back.\" and nothing else.",
        },
        "rc_marcus_busy": {
            "title": "Marcus — Busy / Unavailable",
            "category": "Relationship Scenes",
            "desc": "\"I'm a bit busy. Later?\" Bar hours, in the bar, pre-friend only.",
            "label": "map",
            "presets": {"bar shift, acquaintance": _dst_rc_m_busy},
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "Reads his REAL schedule (npc_schedules.rpy bar Mon-Fri 16-24, "
                     "Sat-Sun 15-27). Once per day, and never at friend stage or above.",
        },
        "rc_zoe_greetings": {
            "title": "Zoe — Greeting Bands",
            "category": "Relationship Scenes",
            "desc": "Acquaintance / friend / after-absence / close. State-only: set a "
                    "preset, then find her and Talk.",
            "label": "map",
            "presets": {
                "acquaintance": _dst_rc_z_acquaintance,
                "friend": _dst_rc_z_friend,
                "friend, 7 days away": _dst_rc_z_friend_gap,
                "close": _dst_rc_z_close,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "Her greeting is now relationship-STAGE banded (it used to read raw "
                     "affection). Gap >= 5 wins over stage; the close \"Sit.\" variant "
                     "has a 10-day cooldown. Second Talk the same day: \"You again.\"",
        },
        "rc_zoe_busy": {
            "title": "Zoe — Busy / Unavailable",
            "category": "Relationship Scenes",
            "desc": "\"Can't. Deadline.\" \"Another day.\" Plus the stressed-week "
                    "friction that pre-empts it.",
            "label": "map",
            "presets": {
                "busy_work (deadline)": _dst_rc_z_busy,
                "stressed_week (friction F2)": _dst_rc_z_stressed,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "Writes the real npc_personal_lives record, not a bespoke flag. "
                     "Never at close/trusted, once per day. F2 is one-shot and resolves "
                     "inside the same conversation.",
        },
        "rc_pretalk": {
            "title": "Marcus / Zoe — Pre-Talk Initiation",
            "category": "Relationship Scenes",
            "desc": "The character opens the pending thread before the Talk menu "
                    "appears. State-only: arm, then press Talk.",
            "label": "map",
            "presets": {
                "Marcus: unresolved interview": _dst_rc_m_pretalk_interview,
                "Zoe: unresolved submission": _dst_rc_z_pretalk_submission,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "_check_talk_followup is wrapped in FRONT of the existing chain, "
                     "which is what turns a menu item into an opener. No new dialogue: "
                     "each returns the shipping label (marcus_ctx_interview / "
                     "zoe_talk_deadline_followup), and each of those closes its own "
                     "thread on entry so it cannot loop.",
        },
        "rc_marcus_micro": {
            "title": "Marcus — Micro Interactions",
            "category": "Relationship Scenes",
            "desc": "Zero-reward texture: a customer, a pointless errand, ten minutes, "
                    "Zoe asking after you, and the lock joke's third version.",
            "label": "rc_continuity_test",
            "presets": {
                "bad customer (bar)": _dst_rc_m_micro,
                "the shop trip": _dst_rc_m_micro_dumb,
                "ten minutes": _dst_rc_m_micro_ten,
                "Zoe was in Saturday": _dst_rc_m_micro_zoe,
                "the lock, version 3": _dst_rc_m_micro_lock,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "No relationship write, no time cost, no CG. Fires from the "
                     "greeting, at most one per character per 5 days and one per beat "
                     "per 14. The customer one is the BAR equivalent of the gym "
                     "complaint — he is never at the gym.",
        },
        "rc_zoe_micro": {
            "title": "Zoe — Micro Interactions",
            "category": "Relationship Scenes",
            "desc": "Zero-reward texture: a bad sign, the light on the glass, five "
                    "minutes of nothing, and Marcus mentioning the score.",
            "label": "rc_continuity_test",
            "presets": {
                "sign complaint": _dst_rc_z_micro,
                "the light on the glass": _dst_rc_z_micro_obs,
                "five-minute break": _dst_rc_z_micro_break,
                "Marcus and the score": _dst_rc_z_micro_marcus,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "No relationship write, no time cost, no CG. The sign complaint "
                     "rotates three variants through _pick_ambient_variant and is the "
                     "bad-typography motif the intros and zoe_msg_poster set up.",
        },
        "rc_marcus_friction": {
            "title": "Marcus — Friction + Repair",
            "category": "Relationship Scenes",
            "desc": "He pushes once after a decline; he gets odd about a score; he "
                    "walks it back a day or two later.",
            "label": "rc_continuity_test",
            "presets": {
                "F1 push after decline": _dst_rc_m_friction,
                "F2 competitive (pool yesterday)": _dst_rc_m_friction_comp,
                "repair (friction yesterday)": _dst_rc_m_repair,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "Both frictions are one-shot and refuse to run while "
                     "story_scene_active. F1 is reached from the three decline branches "
                     "in marcus_friendship.rpy; F2 needs a real pool_marcus game inside "
                     "2 days. Each friction re-arms the repair, which fires from the "
                     "greeting 1-4 days later and never before.",
        },
        "rc_zoe_friction": {
            "title": "Zoe — Friction + Repair",
            "category": "Relationship Scenes",
            "desc": "She takes a compliment as a verdict; she is curt on a bad day; "
                    "she walks it back.",
            "label": "rc_continuity_test",
            "presets": {
                "F1 reads it harshly": _dst_rc_z_friction,
                "repair (friction yesterday)": _dst_rc_z_repair,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "F1 needs an opinion MC actually gave her (zoe_second_opinion_done, "
                     "2+ days old). F2 lives under the Zoe Busy entry because it is "
                     "driven by the stressed_week life state and resolves in-scene.",
        },
        "rc_routines": {
            "title": "Marcus / Zoe — Routine Shorthand",
            "category": "Relationship Scenes",
            "desc": "\"Grounds?\" and \"Static tonight?\" — texts that only exist once "
                    "the routine has happened twice. State-only: arm, then sleep.",
            "label": "map",
            "presets": {
                "Zoe: threshold met (2)": _dst_rc_z_routine,
                "Zoe: below threshold (1)": _dst_rc_z_routine_below,
                "Marcus: threshold met (2)": _dst_rc_m_routine,
                "Marcus: below threshold (1)": _dst_rc_m_routine_below,
            },
            "checkpoints": None,
            "reset": _dst_rc_reset,
            "notes": "Registered into the SHIPPING initiative picker, so they still "
                     "share the one-unprompted-contact-per-day global budget with every "
                     "other NPC — the below-threshold presets exist to prove the gate, "
                     "not to promise a send on the first night.",
        },
    })


# ═══════════════════════════════════════════════════════════════════════════
# STORY / DIRECTING PASS — ZOE + MARCUS (story_direct_pass.rpy)
# ═══════════════════════════════════════════════════════════════════════════
# Presets set state, then the existing launchers give the dialogue-only labels
# a call frame: marcus_friendship_test for Marcus, rc_continuity_test for Zoe.
# No new tester architecture.
init python:

    def _dst_sd_noop():
        renpy.notify("Nothing to reset — the self-check restores its own state")

    def _dst_sd_beach_marcus():
        """The Marcus route of the first beach meeting. All three impressions
        live in ONE menu inside the scene — pick the matching choice."""
        store.zoe_met = False
        store.zoe_properly_introduced = False
        store.zoe_intro_beach_done = False
        store.zoe_bootstrap_complete = False
        store.zoe_first_callback_sent = False
        store.zoe_bootstrap_start_day = -1
        store.zoe_first_impression = ""
        store.marcus_mentioned_zoe = True          # this is what selects the route
        store.marcus_met = True
        mark_npc_encountered("marcus")
        store.hour = 15.0

    def _dst_sd_beach_curious():
        _dst_sd_beach_marcus()
        renpy.notify("Beach/Marcus route — pick \"Ask to see the sketch.\" (curious)")

    def _dst_sd_beach_observant():
        _dst_sd_beach_marcus()
        renpy.notify("Beach/Marcus route — pick \"Look at the building instead.\" (observant)")

    def _dst_sd_beach_honest():
        _dst_sd_beach_marcus()
        renpy.notify("Beach/Marcus route — pick \"Admit you know nothing about art.\" (honest)")

    def _dst_sd_beach_reset():
        store.zoe_met = False
        store.zoe_properly_introduced = False
        store.zoe_intro_beach_done = False
        store.zoe_first_impression = ""
        store.npc_contacts = [c for c in store.npc_contacts if c != "zoe"]
        renpy.notify("Zoe intro flags cleared (all three routes re-armed)")

    # ── Wednesday, first occurrence ──────────────────────────────────────
    def _dst_sd_wed_first():
        _dst_zoe_comfortable()
        store.zoe_wednesday_first_done = False
        _dst_beat_clear("zoe_wednesday")
        store.current_loc = "location_cafe"
        _dst_beat_set_weekday(2)                   # Wednesday
        store.hour = 15.0
        renpy.notify("Wednesday at Grounds: FIRST occurrence armed")

    def _dst_sd_wed_reset():
        store.zoe_wednesday_first_done = False
        _dst_beat_clear("zoe_wednesday")

    # ── Coffee, Not Advice (rewritten body) ──────────────────────────────
    def _dst_sd_coffee_fiveam():
        _dst_zoe_coffee_preset()
        store.marcus_five_am_known = True          # opens the Marcus branch
        renpy.notify("Coffee Not Advice armed — Marcus five-AM branch")

    def _dst_sd_coffee_nofiveam():
        _dst_zoe_coffee_preset()
        store.marcus_five_am_known = False         # opens the trash-can fallback
        renpy.notify("Coffee Not Advice armed — fallback branch")

    # ── Zoe, small disagreement + repair ─────────────────────────────────
    def _dst_sd_disagree():
        _dst_zoe_comfortable()
        # npc_relationship_stage: "friend" needs fam>=50, aff>=45, trust>=35.
        set_npc_rel("zoe", "familiarity", 55)
        set_npc_rel("zoe", "affection", 50)
        set_npc_rel("zoe", "trust", 40)
        store.zoe_affection = 50
        store.zoe_trust     = 40
        store.zoe_disagreement_done = False
        store.zoe_disagreement_day = -1
        store.zoe_disagreement_repair_done = True
        _dst_beat_clear("zoe_disagreement")
        store.current_loc = "location_cafe"
        _dst_beat_set_weekday(2)
        store.hour = 15.0
        renpy.notify("Zoe disagreement armed (fam 50, cafe Wed) — enter the cafe")

    def _dst_sd_disagree_repair():
        _dst_zoe_comfortable()
        store.zoe_disagreement_done = True
        store.zoe_disagreement_day = store.day - 1
        store.zoe_disagreement_repair_done = False
        store.rc_test_label = "zoe_disagreement_repair"
        store.rc_test_npc = "zoe"
        renpy.notify("Repair armed (disagreement yesterday) — or just Talk to Zoe")

    def _dst_sd_disagree_reset():
        store.zoe_disagreement_done = False
        store.zoe_disagreement_day = -1
        store.zoe_disagreement_repair_done = True
        _dst_beat_clear("zoe_disagreement")
        renpy.notify("Zoe disagreement + repair flags cleared")

    # ── Marcus, bad day (rewritten frame) ────────────────────────────────
    def _dst_sd_badday():
        _dst_mf_base()
        _dst_mf_arm("marcus_beat_had_a_day", "marcus_fr_had_a_day")
        store.marcus_had_a_day_last = -1
        renpy.notify("Marcus bad day armed — topic is picked in-scene; re-run for 'game'")

    # ── Marcus, why I stayed ─────────────────────────────────────────────
    def _dst_sd_why_stayed():
        _dst_mf_base()
        # "friend" needs fam>=50, aff>=45, trust>=35 (npc_relationship_stage).
        set_npc_rel("marcus", "trust", 45)
        set_npc_rel("marcus", "familiarity", 55)
        set_npc_rel("marcus", "affection", 50)
        store.mc_knows_marcus_bball_offer = True
        store.marcus_why_stayed_done = False
        store.marcus_bball_offer_day = store.day - 5
        _d = dict(store.tier_a_beat_last_day)
        _d["marcus_fr_still_alive"] = store.day - 5
        store.tier_a_beat_last_day = _d
        store.marcus_test_label = "marcus_why_stayed_scene"
        renpy.notify("Why I Stayed armed (offer 5 days ago, trust 45) — or just Talk")

    def _dst_sd_why_stayed_too_soon():
        _dst_sd_why_stayed()
        store.marcus_bball_offer_day = store.day   # inside the 3-day cooldown
        renpy.notify("Why I Stayed BLOCKED (offer today) — Talk must NOT open it")

    def _dst_sd_why_stayed_reset():
        store.marcus_why_stayed_done = False
        store.marcus_bball_offer_day = -1
        renpy.notify("Why I Stayed flags cleared")

    # ── Static group scene + the two cross-callbacks ─────────────────────
    def _dst_sd_static_group():
        _dst_beat_meet("marcus", "zoe")
        store.zoe_properly_introduced = True
        # Marcus must read "friend" (fam>=50, aff>=45, trust>=35); Zoe only has
        # to be past the acquaintance band.
        set_npc_rel("marcus", "familiarity", 55)
        set_npc_rel("marcus", "affection", 50)
        set_npc_rel("marcus", "trust", 40)
        set_npc_rel("zoe", "familiarity", 40)
        set_npc_rel("zoe", "affection", 35)
        store.marcus_zoe_static_scene_done = False
        store.marcus_zoe_static_day = -1
        _dst_beat_clear("marcus_zoe_static")
        _dst_beat_set_weekday(5)                   # Saturday
        store.hour = 20.0
        renpy.notify("Static group scene armed (Sat 20:00) — walk into the bar")

    def _dst_sd_static_reset():
        store.marcus_zoe_static_scene_done = False
        store.marcus_zoe_static_day = -1
        store.sd_marcus_static_cb_done = False
        store.sd_zoe_static_cb_done = False
        _dst_beat_clear("marcus_zoe_static")
        renpy.notify("Static group scene + both callbacks cleared")

    def _dst_sd_cb_marcus():
        _dst_mf_base()
        store.marcus_zoe_static_scene_done = True
        store.marcus_zoe_static_day = store.day - 4
        store.sd_marcus_static_cb_done = False
        store.marcus_test_label = "sd_marcus_static_callback"
        renpy.notify("Marcus post-Static callback armed (4 days on) — or just Talk")

    def _dst_sd_cb_zoe():
        _dst_zoe_comfortable()
        store.marcus_zoe_static_scene_done = True
        store.marcus_zoe_static_day = store.day - 4
        store.sd_zoe_static_cb_done = False
        store.rc_test_label = "sd_zoe_static_callback"
        store.rc_test_npc = "zoe"
        renpy.notify("Zoe post-Static callback armed (4 days on) — or just Talk")

    SCENE_TEST_REGISTRY.update({
        "sd_zoe_beach_marcus": {
            "title": "Zoe — First Beach Intro (Marcus route)",
            "category": "Relationship Scenes",
            "desc": "The authored first meeting for a player Marcus already pointed "
                    "at her. Curious / observant / honest are three menu options "
                    "inside the scene — each preset says which one to pick.",
            "label": "zoe_beach_marcus_intro",
            "presets": {
                "curious": _dst_sd_beach_curious,
                "observant": _dst_sd_beach_observant,
                "honest": _dst_sd_beach_honest,
            },
            "checkpoints": None,
            "reset": _dst_sd_beach_reset,
            "notes": "Selected by marcus_mentioned_zoe at the top of beach_meet_zoe. "
                     "The two cold-discovery routes (approach / watch) are unchanged "
                     "and fire when he never named her. Does NOT call "
                     "zoe_beach_intro_tail — the tail's content is in this screenplay.",
        },
        "sd_zoe_wednesday_first": {
            "title": "Zoe — Wednesday at Grounds / First",
            "category": "Relationship Scenes",
            "desc": "\"It's two fifty-six.\" The first ordinary afternoon. Later "
                    "Wednesdays keep the repeatable four-variant version.",
            "label": "zoe_wednesday_grounds_scene",
            "presets": {"first occurrence": _dst_sd_wed_first},
            "checkpoints": {"first-occurrence body": "zoe_wednesday_first_scene"},
            "reset": _dst_sd_wed_reset,
            "notes": "Branches at the top of zoe_wednesday_grounds_scene on "
                     "zoe_wednesday_first_done. Old saves that already ran the "
                     "repeatable beat are migrated past it by _sd_backfill().",
        },
        "sd_zoe_coffee": {
            "title": "Zoe — Coffee Not Advice",
            "category": "Relationship Scenes",
            "desc": "Rewritten body: \"They said no.\" Two endings depending on "
                    "whether MC knows Marcus cannot sleep past five.",
            "label": "zoe_coffee_not_advice_scene",
            "presets": {
                "Marcus five-AM known": _dst_sd_coffee_fiveam,
                "fallback (not known)": _dst_sd_coffee_nofiveam,
            },
            "checkpoints": None,
            "reset": _dst_zoe_coffee_reset,
            "notes": "Trigger unchanged: zoe_coffee_pending, set by the "
                     "zoe_msg_bad_email initiative reply. Sets "
                     "zoe_coffee_callback_pending on the way out.",
        },
        "sd_zoe_disagreement": {
            "title": "Zoe — Small Disagreement",
            "category": "Relationship Scenes",
            "desc": "\"I hate that.\" A real difference of taste at friend stage, "
                    "about the exhibition poster at Grounds.",
            "label": "zoe_small_disagreement",
            "presets": {"comfortable (fam 50)": _dst_sd_disagree},
            "checkpoints": None,
            "reset": _dst_sd_disagree_reset,
            "notes": "Separate from rc_zoe_friction_reads_harsh, which is the "
                     "acquaintance-stage misread and stays. Gated fam >= 45 + friend "
                     "stage + 2 days clear of any heavy Zoe beat.",
        },
        "sd_zoe_disagreement_cb": {
            "title": "Zoe — Disagreement Callback",
            "category": "Relationship Scenes",
            "desc": "\"For the record.\" One-shot repair, 1-3 days after.",
            "label": "rc_continuity_test",
            "presets": {"disagreement yesterday": _dst_sd_disagree_repair},
            "checkpoints": None,
            "reset": _dst_sd_disagree_reset,
            "notes": "Cannot fire before the disagreement: "
                     "zoe_disagreement_repair_done defaults True (nothing owed) and "
                     "only zoe_small_disagreement clears it.",
        },
        "sd_marcus_bad_day": {
            "title": "Marcus — Bad Day",
            "category": "Relationship Scenes",
            "desc": "Rewritten frame: good dumb or bad dumb, premium or basic. The "
                    "four canonical day-topics are unchanged inside it.",
            "label": "marcus_friendship_test",
            "presets": {"armed": _dst_sd_badday},
            "checkpoints": None,
            "reset": _dst_mf_reset,
            "notes": "marcus_had_a_day_topic is still written, because "
                     "marcus_ctx_what_happened reads it back the same day. The 'game' "
                     "topic uses the screenplay's own exchange.",
        },
        "sd_marcus_why_stayed": {
            "title": "Marcus — Why I Stayed",
            "category": "Relationship Scenes",
            "desc": "\"My dad was sick.\" The reveal arc_marcus_sports_2 now defers "
                    "to. Trust +3, and he never brings it up again.",
            "label": "marcus_friendship_test",
            "presets": {
                "eligible": _dst_sd_why_stayed,
                "blocked (offer today)": _dst_sd_why_stayed_too_soon,
            },
            "checkpoints": None,
            "reset": _dst_sd_why_stayed_reset,
            "notes": "Opens itself through _check_talk_followup once "
                     "mc_knows_marcus_bball_offer, trust >= 35, friend stage, and 3+ "
                     "days clear of both the offer and marcus_beat_still_alive. "
                     "Retires the marcus_sports_2 topic arc afterwards.",
        },
        "sd_marcus_zoe_static": {
            "title": "Marcus + Zoe — Static Group Scene",
            "category": "Group Hangouts",
            "desc": "Seven o'clock, the table with the light directly above it, and "
                    "a playlist called 'Locked In'.",
            "label": "marcus_zoe_static_small_group",
            "presets": {"Saturday 20:00, both established": _dst_sd_static_group},
            "checkpoints": None,
            "reset": _dst_sd_static_reset,
            "notes": "One-shot. Sits in front of marcus_zoe_bar_scene at the same "
                     "slot (bar, Sat 19-24); the repeatable one still works after.",
        },
        "sd_cb_marcus_static": {
            "title": "Cross Callback — Marcus after Static",
            "category": "Group Hangouts",
            "desc": "\"Zoe still blaming me for the table?\" One-shot, 3+ days on.",
            "label": "marcus_friendship_test",
            "presets": {"4 days after the group scene": _dst_sd_cb_marcus},
            "checkpoints": None,
            "reset": _dst_sd_static_reset,
            "notes": "Gated on marcus_zoe_static_scene_done. Dispatched by the "
                     "_check_talk_followup wrapper in story_direct_pass.rpy.",
        },
        "sd_cb_zoe_static": {
            "title": "Cross Callback — Zoe after Static",
            "category": "Group Hangouts",
            "desc": "\"Marcus changed his playlist.\" One-shot, 3+ days on.",
            "label": "rc_continuity_test",
            "presets": {"4 days after the group scene": _dst_sd_cb_zoe},
            "checkpoints": None,
            "reset": _dst_sd_static_reset,
            "notes": "Sits IN FRONT of the Zoe chain: zoe_arc's wrapper always "
                     "answers zoe_thread_talk, so a callback placed behind it would "
                     "never be reached.",
        },
        "sd_selfcheck": {
            "title": "Story Pass — Gate Self-Check",
            "category": "Misc",
            "desc": "Asserts the five gates a player could hit backwards. Prints OK "
                    "or the failing rule. Restores every flag it touches.",
            "label": "sd_selfcheck",
            "presets": {"run": _dst_sd_noop},
            "checkpoints": None,
            "reset": _dst_sd_noop,
            "notes": "No dialogue, no time cost. Run it after touching any gate in "
                     "story_direct_pass.rpy.",
        },
    })

    # ── Zoe Romance Milestone presets (M2–M6) ────────────────────────────────

    def _dst_zoe_m2_eligible():
        store.zoe_met = True
        set_romance_state("zoe", "interested", source="tester")
        store.romance_last_choice_day["zoe"] = max(0, store.day - 3)
        store.zoe_affection = 55
        store.zoe_trust = 50
        _nr = dict(store.npc_relationships)
        _nr.setdefault("zoe", {})["familiarity"] = 50
        _nr["zoe"]["_seeded"] = True
        store.npc_relationships = _nr
        store.zoe_first_date_declined_day = -1

    def _dst_zoe_m2_not_ready():
        _dst_zoe_m2_eligible()

    def _dst_zoe_m2_friends():
        _dst_zoe_m2_eligible()

    def _dst_zoe_m2_legacy():
        store.zoe_met = True
        set_romance_state("zoe", "dating", source="tester")
        add_relationship_memory("zoe", "first_kiss_zoe", "First kiss (legacy)")
        store.zoe_first_date_done = True
        store.zoe_dating_day = max(0, store.day - 5)

    def _dst_zoe_m2_reset():
        store.zoe_first_date_done    = False
        store.zoe_first_date_pending = False
        store.zoe_first_date_target  = -1
        store.zoe_dating_day         = -1
        store.zoe_first_date_declined_day = -1

    def _dst_zoe_m2_beach_eligible():
        """M2 beach dating breakpoint — interested state, pre-kiss."""
        store.zoe_met = True
        set_romance_state("zoe", "interested", source="tester")
        store.romance_last_choice_day["zoe"] = max(0, store.day - 3)
        store.zoe_affection = 55
        store.zoe_trust = 50
        _nr = dict(store.npc_relationships)
        _nr.setdefault("zoe", {})["familiarity"] = 50
        _nr["zoe"]["_seeded"] = True
        store.npc_relationships = _nr
        store.zoe_beach_dating_done    = False
        store.zoe_beach_dating_pending = False
        store.zoe_beach_dating_declined_day = -1

    def _dst_zoe_m2_beach_reset():
        store.zoe_beach_dating_done    = False
        store.zoe_beach_dating_pending = False
        store.zoe_beach_dating_declined_day = -1

    def _dst_zoe_m3_eligible():
        set_romance_state("zoe", "dating", source="tester")
        add_relationship_memory("zoe", "first_kiss_zoe", "First kiss")
        store.zoe_first_date_done      = True
        store.zoe_beach_dating_done    = True   # M2 beach must precede M4 home
        store.zoe_dating_day = max(0, store.day - 5)
        store.zoe_affection = 60
        store.zoe_trust = 55
        _nr = dict(store.npc_relationships)
        _nr.setdefault("zoe", {})["familiarity"] = 60
        _nr["zoe"]["_seeded"] = True
        store.npc_relationships = _nr

    def _dst_zoe_m3_reset():
        store.zoe_home_no_reason_done = False
        store.zoe_home_pending        = False
        store.zoe_home_declined_day   = -1

    def _dst_zoe_m4_dating():
        set_romance_state("zoe", "dating", source="tester")
        store.zoe_m4_marcus_done = False

    def _dst_zoe_m4_committed():
        set_romance_state("zoe", "committed", source="tester")
        store.zoe_m4_marcus_done = False

    def _dst_zoe_m4_reset():
        store.zoe_m4_marcus_done = False

    def _dst_zoe_m5_eligible():
        set_romance_state("zoe", "dating", source="tester")
        add_relationship_memory("zoe", "first_kiss_zoe", "First kiss")
        store.zoe_first_date_done       = True
        store.zoe_beach_night_done      = True   # M3 must precede M6 commitment
        store.zoe_home_no_reason_done   = True
        store.zoe_dating_day            = max(0, store.day - 12)
        store.zoe_affection             = 65
        store.zoe_trust                 = 70
        _nr = dict(store.npc_relationships)
        _nr.setdefault("zoe", {})["familiarity"] = 70
        _nr["zoe"]["_seeded"] = True
        store.npc_relationships = _nr
        add_relationship_memory("zoe", "zoe_coffee_not_advice",
                                "Coffee with Zoe about the funding problem")
        store.rc_zoe_f1_done     = True
        store.rc_zoe_repair_done = True
        store.zoe_commitment_declined_day = -1

    def _dst_zoe_m5_not_yet():
        _dst_zoe_m5_eligible()

    def _dst_zoe_m5_reset():
        store.zoe_commitment_done        = False
        store.zoe_commitment_pending     = False
        store.zoe_committed_day          = -1
        store.zoe_commitment_declined_day = -1

    def _dst_zoe_m6_eligible():
        set_romance_state("zoe", "committed", source="tester")
        add_relationship_memory("zoe", "first_kiss_zoe", "First kiss")
        store.zoe_first_date_done     = True
        store.zoe_home_no_reason_done = True
        store.zoe_commitment_done     = True
        store.zoe_committed_day       = max(0, store.day - 12)
        store.zoe_dating_day          = max(0, store.day - 25)
        store.zoe_affection           = 75
        store.zoe_trust               = 75
        _nr = dict(store.npc_relationships)
        _nr.setdefault("zoe", {})["familiarity"] = 75
        _nr["zoe"]["_seeded"] = True
        store.npc_relationships = _nr
        add_relationship_memory("zoe", "zoe_home_no_reason",
                                "The terrible film and no particular reason")

    def _dst_zoe_m6_reset():
        store.zoe_love_spoken     = False
        store.zoe_love_spoken_day = -1
        store.zoe_m6_pending      = False

    SCENE_TEST_REGISTRY.update({
        "zoe_m2_beach_dating": {
            "title": "Zoe M2 — Beach Dating Breakpoint",
            "category": "Relationship Scenes",
            "desc": "Canonical interested → dating scene. Full beach night buildup + director handoff.",
            "label": "zoe_beach_dating_scene",
            "presets": {
                "interested eligible": _dst_zoe_m2_beach_eligible,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m2_beach_reset,
            "notes": "M2 — beach breakpoint. Commitment zoe_beach_dating_1 must be active. "
                     "Director label romantic_subscene_zoe_beach_dating required for resolution.",
        },
        "zoe_m2_first_date_legacy": {
            "title": "Zoe M2 — First Date (Grounds, legacy)",
            "category": "Relationship Scenes",
            "desc": "Old Grounds route — disabled in production. Kept for save compatibility testing.",
            "label": "zoe_first_date_scene",
            "presets": {
                "romantic eligible": _dst_zoe_m2_eligible,
                "legacy (kissed)":   _dst_zoe_m2_legacy,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m2_reset,
            "notes": "Grounds M2 is disabled (_zoe_m2_eligible returns False). "
                     "Use only to verify old save compatibility paths.",
        },
        "zoe_m3_no_reason": {
            "title": "Zoe M3 — No Reason",
            "category": "Relationship Scenes",
            "desc": "First ordinary private evening. Terrible film, no agenda.",
            "label": "zoe_home_no_reason_scene",
            "presets": {
                "dating eligible": _dst_zoe_m3_eligible,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m3_reset,
            "notes": "M3 — home evening. Commitment zoe_home_no_reason_1 must be active.",
        },
        "zoe_m4_public": {
            "title": "Zoe M4 — Marcus Figures It Out",
            "category": "Relationship Scenes",
            "desc": "Group recognition coda appended to the static small group scene.",
            "label": "zoe_m4_marcus_recognition",
            "presets": {
                "dating":    _dst_zoe_m4_dating,
                "committed": _dst_zoe_m4_committed,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m4_reset,
            "notes": "M4 — fires as coda of marcus_zoe_static_small_group once dating/committed.",
        },
        "zoe_m5_commitment": {
            "title": "Zoe M6 — No Qualifiers",
            "category": "Relationship Scenes",
            "desc": "Terrace commitment scene (Riverside Terrace, late evening). Committed or not-yet branch.",
            "label": "zoe_commitment_beach_scene",
            "presets": {
                "eligible":  _dst_zoe_m5_eligible,
                "not yet":   _dst_zoe_m5_not_yet,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m5_reset,
            "notes": "M6 — commitment at location_terrace. Commitment zoe_commitment_beach_1 must be active. Requires zoe_beach_night_done.",
        },
        "zoe_m6_love_spoken": {
            "title": "Zoe M6 — Don't Make It An Event",
            "category": "Relationship Scenes",
            "desc": "First spoken love. Three branches: say it back, kiss, or tease the label.",
            "label": "zoe_love_spoken_scene",
            "presets": {
                "eligible": _dst_zoe_m6_eligible,
            },
            "checkpoints": None,
            "reset": _dst_zoe_m6_reset,
            "notes": "M6 — love spoken. Direct eligibility check; no commitment needed.",
        },
    })
