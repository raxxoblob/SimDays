# world_events.rpy — Central World Event Director
#
# One data-driven system replaces scattered random checks in location labels.
# Location labels call wed_poll_ambient / wed_poll_personal once; this file
# owns all eligibility logic, cooldown tracking, and callback scheduling.
#
# Integration points in locations.rpy:
#   After BG/HUD + sprite setup, before the activity menu:
#       $ _wed_amb = wed_poll_ambient("location_bar")
#       if _wed_amb: call expression _wed_amb
#       $ _wed_per = wed_poll_personal("location_bar")
#       if _wed_per: call expression _wed_per
#
# Adding a new event: add an entry to WED_REGISTRY, write a label named
# "wevent_<id>", add the location to the location label's WED hook call.
# The label must call wed_fire("event_id") when the scene actually runs.

init python:

    # ── Event registry ────────────────────────────────────────────────────
    # Fields:
    #   type:           "ambient" | "personal"
    #   label:          Ren'Py label to call
    #   locations:      list of location_* strings where this can fire
    #   min_day:        earliest day this can fire
    #   once:           if True, fires at most once per save
    #   priority:       higher = checked before lower (personal events only)
    #   cooldown:       days before this can fire again (0 = use once flag)
    #   weight:         0.0–1.0 probability this pre-rolls on an eligible day
    #   conflict_npc:   blocked if any active commitment exists for this NPC

    WED_REGISTRY = {
        # -- Personal events ------------------------------------------------
        "marcus_loan": {
            "type":         "personal",
            "label":        "wevent_marcus_loan",
            "locations":    ["location_bar", "location_park"],
            "min_day":      10,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": "marcus",
        },
        "sam_off_routine": {
            "type":         "personal",
            "label":        "wevent_sam_off_routine",
            "locations":    ["location_cafe", "location_gym"],
            "min_day":      7,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
        },
        "marcus_first_shift_checkin": {
            "type":         "personal",
            "label":        "wevent_marcus_first_shift_checkin",
            "locations":    ["location_hallway"],
            "min_day":      1,
            "once":         True,
            "priority":     3,
            "cooldown":     0,
            "conflict_npc": "marcus",
        },
        "marcus_low_energy_comment": {
            "type":         "personal",
            "label":        "wevent_marcus_low_energy_comment",
            "locations":    ["location_hallway"],
            "min_day":      3,
            "once":         False,
            "priority":     1,
            "cooldown":     5,
            "conflict_npc": "marcus",
        },
        "marcus_first_steps_followup": {
            "type":         "personal",
            "label":        "wevent_marcus_first_steps_followup",
            "locations":    ["location_hallway"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": "marcus",
        },
        "marcus_new_car_comment": {
            "type":         "personal",
            "label":        "wevent_marcus_new_car_comment",
            "locations":    ["location_hallway"],
            "min_day":      1,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": "marcus",
            "condition":    lambda: store.car_tier > 0,
        },
        # -- Sam gym events -------------------------------------------------
        "gym_sam_last_rep": {
            "type":         "personal",
            "label":        "wevent_gym_sam_last_rep",
            "locations":    ["location_gym"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.sam_met and npc_here("sam"),
        },
        "gym_sam_bad_advice": {
            "type":         "personal",
            "label":        "wevent_gym_sam_bad_advice",
            "locations":    ["location_gym"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.sam_met and npc_here("sam"),
        },
        "gym_sam_water_break": {
            "type":         "personal",
            "label":        "wevent_gym_sam_water_break",
            "locations":    ["location_gym"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.sam_met and npc_here("sam") and store.need_energy <= 40,
        },
        # -- Zoe public events ----------------------------------------------
        "zoe_sketching_stranger": {
            "type":         "personal",
            "label":        "wevent_zoe_sketching_stranger",
            "locations":    ["location_park"],
            "min_day":      3,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.zoe_met and npc_here("zoe"),
        },
        "zoe_wrong_colour": {
            "type":         "personal",
            "label":        "wevent_zoe_wrong_colour",
            "locations":    ["location_park"],
            "min_day":      3,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.zoe_met and npc_here("zoe"),
        },
        "zoe_lost_pencil": {
            "type":         "personal",
            "label":        "wevent_zoe_lost_pencil",
            "locations":    ["location_park"],
            "min_day":      3,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.zoe_met and npc_here("zoe"),
        },
        # -- Ambient events -------------------------------------------------
        "rain_in_park": {
            "type":         "ambient",
            "label":        "wevent_rain_in_park",
            "locations":    ["location_park"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     4,
            "weight":       0.28,
        },
        "bar_quiz_night": {
            "type":         "ambient",
            "label":        "wevent_bar_quiz_night",
            "locations":    ["location_bar"],
            "min_day":      5,
            "once":         False,
            "priority":     1,
            "cooldown":     6,
            "weight":       0.35,
        },
        # -- Phase 12: one-time NPC crossover events --------------------------
        "crossover_marcus_nora_coffee": {
            "type":         "personal",
            "label":        "wevent_crossover_marcus_nora_coffee",
            "locations":    ["location_cafe"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.marcus_met and store.nora_met and npc_here("marcus") and npc_here("nora"),
        },
        "crossover_sam_zoe_park": {
            "type":         "personal",
            "label":        "wevent_crossover_sam_zoe_park",
            "locations":    ["location_park"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.sam_met and store.zoe_met and npc_here("sam") and npc_here("zoe"),
        },
        "crossover_martha_caroline_static": {
            "type":         "personal",
            "label":        "wevent_crossover_martha_caroline_static",
            "locations":    ["location_bar"],
            "min_day":      5,
            "once":         True,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: store.martha_met and store.caroline_met and npc_here("martha") and npc_here("caroline"),
        },
        # -- Phase 11: repeatable location ambients ---------------------------
        "static_texture": {
            "type":         "ambient",
            "label":        "wevent_static_texture",
            "locations":    ["location_bar"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        "mall_texture": {
            "type":         "ambient",
            "label":        "wevent_mall_texture",
            "locations":    ["location_mall"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        "beach_texture": {
            "type":         "ambient",
            "label":        "wevent_beach_texture",
            "locations":    ["location_beach"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        # -- Phase 10: repeatable public micro-scenes -------------------------
        "marcus_hallway_texture": {
            "type":         "personal",
            "label":        "wevent_marcus_hallway_texture",
            "locations":    ["location_hallway"],
            "min_day":      3,
            "once":         False,
            "priority":     1,
            "cooldown":     3,
            "conflict_npc": "marcus",
            "condition":    lambda: store.marcus_met and npc_here("marcus") and store.move_in_complete,
        },
        "zoe_park_texture": {
            "type":         "personal",
            "label":        "wevent_zoe_park_texture",
            "locations":    ["location_park"],
            "min_day":      3,
            "once":         False,
            "priority":     1,
            "cooldown":     3,
            "conflict_npc": None,
            "condition":    lambda: store.zoe_met and npc_here("zoe"),
        },
        "nora_cafe_texture": {
            "type":         "personal",
            "label":        "wevent_nora_cafe_texture",
            "locations":    ["location_cafe"],
            "min_day":      3,
            "once":         False,
            "priority":     1,
            "cooldown":     3,
            "conflict_npc": None,
            "condition":    lambda: store.nora_met and npc_here("nora") and store.active_work_shift != "cafe",
        },
        # -- Phase 13: repeatable NPC crossover follow-ups --------------------
        "crossover_marcus_nora_repeat": {
            "type":         "ambient",
            "label":        "wevent_crossover_marcus_nora_repeat",
            "locations":    ["location_cafe"],
            "min_day":      5,
            "once":         False,
            "priority":     1,
            "cooldown":     5,
            "weight":       0.35,
            "condition":    lambda: (
                store.marcus_met and store.nora_met
                and "crossover_marcus_nora_coffee" in store.wed_resolved
                and store.wed_event_last_day.get("crossover_marcus_nora_coffee") != store.day
                and store.major_scene_last_day != store.day
            ),
        },
        "crossover_sam_zoe_repeat": {
            "type":         "ambient",
            "label":        "wevent_crossover_sam_zoe_repeat",
            "locations":    ["location_park"],
            "min_day":      5,
            "once":         False,
            "priority":     1,
            "cooldown":     5,
            "weight":       0.35,
            "condition":    lambda: (
                store.sam_met and store.zoe_met
                and "crossover_sam_zoe_park" in store.wed_resolved
                and store.wed_event_last_day.get("crossover_sam_zoe_park") != store.day
                and store.major_scene_last_day != store.day
            ),
        },
        "crossover_martha_caroline_repeat": {
            "type":         "ambient",
            "label":        "wevent_crossover_martha_caroline_repeat",
            "locations":    ["location_bar"],
            "min_day":      5,
            "once":         False,
            "priority":     1,
            "cooldown":     5,
            "weight":       0.35,
            "condition":    lambda: (
                store.martha_met and store.caroline_met
                and "crossover_martha_caroline_static" in store.wed_resolved
                and store.wed_event_last_day.get("crossover_martha_caroline_static") != store.day
                and store.major_scene_last_day != store.day
            ),
        },
        # -- Phase 15: public area ambients -----------------------------------
        # eleven_public_texture omitted: project has no guest-facing Eleven
        # location separate from location_kitchen (kitchen work POV).
        "nexus_public_texture": {
            "type":         "ambient",
            "label":        "wevent_nexus_public_texture",
            "locations":    ["location_office"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        "hospital_public_texture": {
            "type":         "ambient",
            "label":        "wevent_hospital_public_texture",
            "locations":    ["location_hospital"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        # -- Phase 16: library, college and downtown ambients -----------------
        "library_texture": {
            "type":         "ambient",
            "label":        "wevent_library_texture",
            "locations":    ["location_library"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        "college_texture": {
            "type":         "ambient",
            "label":        "wevent_college_texture",
            "locations":    ["location_college"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        "downtown_texture": {
            "type":         "ambient",
            "label":        "wevent_downtown_texture",
            "locations":    ["location_centrum"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
        # -- Phase 31: NPC invitation scenes ------------------------------------
        "marcus_park_invite_scene": {
            "type":         "personal",
            "label":        "wevent_marcus_park_invite_scene",
            "locations":    ["location_park"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "marcus_park_invite"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.marcus_met
                and npc_here("marcus")
            ),
        },
        "nora_grounds_invite_scene": {
            "type":         "personal",
            "label":        "wevent_nora_grounds_invite_scene",
            "locations":    ["location_cafe"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "nora_grounds_invite"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.nora_met
                and npc_here("nora")
                and store.active_work_shift != "cafe"
            ),
        },
        "zoe_park_invite_scene": {
            "type":         "personal",
            "label":        "wevent_zoe_park_invite_scene",
            "locations":    ["location_park"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "zoe_park_invite"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.zoe_met
                and npc_here("zoe")
            ),
        },
        "eli_library_invite_scene": {
            "type":         "personal",
            "label":        "wevent_eli_library_invite_scene",
            "locations":    ["location_library"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "eli_library_invite"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.eli_met
                and npc_here("eli")
            ),
        },
        # ── Phase 37: NPC-initiated date scenes ──────────────────────────────
        "nora_static_date_scene": {
            "type":         "personal",
            "label":        "wevent_nora_static_date_scene",
            "locations":    ["location_bar"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "nora_static_date"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.nora_met
                and npc_here("nora")
                and _date_route_eligible("nora")
            ),
        },
        "zoe_beach_date_scene": {
            "type":         "personal",
            "label":        "wevent_zoe_beach_date_scene",
            "locations":    ["location_sandbeach"],
            "min_day":      1,
            "once":         False,
            "priority":     2,
            "cooldown":     0,
            "conflict_npc": None,
            "condition":    lambda: (
                store.npc_invitation_pending is not None
                and store.npc_invitation_pending.get("invitation_id") == "zoe_beach_date"
                and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
                and store.zoe_met
                and npc_here("zoe")
                and _date_route_eligible("zoe")
            ),
        },
        # -- Phase 17: garage ambient (bank and airport lounge blocked —
        #    backgrounds exist but no reusable public location label) ----------
        "garage_texture": {
            "type":         "ambient",
            "label":        "wevent_garage_texture",
            "locations":    ["location_cardealer"],
            "min_day":      1,
            "once":         False,
            "priority":     1,
            "cooldown":     2,
            "weight":       0.35,
        },
    }

    # ── Phase 44: engagement gate ─────────────────────────────────────────
    # npc_talkable() doesn't prove MC has actually met a world NPC.
    # This helper distinguishes a real encounter from a stranger passing by.
    def _phase44_engaged(npc_id):
        if npc_id == "marcus":   return bool(getattr(store, "marcus_met",   False))
        if npc_id == "nora":     return npc_aff("nora") > 0
        if npc_id == "elle":     return (npc_aff("elle") > 0
                                         or bool(getattr(store, "elle_pier_done", False)))
        if npc_id == "sam":      return (npc_aff("sam") > 0
                                         or bool(getattr(store, "sam_met",   False)))
        if npc_id == "kai":      return (npc_aff("kai") > 0
                                         or bool(getattr(store, "kai_met",   False)))
        if npc_id == "lena":     return bool(getattr(store, "lena_met",      False))
        if npc_id == "caroline": return bool(getattr(store, "caroline_met",  False))
        return False

    # ── Phase 44 WED entries (appended here; WED_REGISTRY closed above) ────
    WED_REGISTRY["crossover_nora_elle_grounds"] = {
        "type":         "personal",
        "label":        "wevent_crossover_nora_elle_grounds",
        "locations":    ["location_cafe"],
        "min_day":      7,
        "once":         True,
        "priority":     2,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            _phase44_engaged("nora") and _phase44_engaged("elle")
            and npc_talkable("nora") and npc_talkable("elle")
        ),
    }
    WED_REGISTRY["crossover_lena_marcus_bar"] = {
        "type":         "personal",
        "label":        "wevent_crossover_lena_marcus_bar",
        "locations":    ["location_bar"],
        "min_day":      7,
        "once":         True,
        "priority":     2,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            _phase44_engaged("lena") and _phase44_engaged("marcus")
            and npc_talkable("lena") and npc_talkable("marcus")
        ),
    }
    WED_REGISTRY["crossover_sam_kai_gym"] = {
        "type":         "personal",
        "label":        "wevent_crossover_sam_kai_gym",
        "locations":    ["location_gym"],
        "min_day":      7,
        "once":         True,
        "priority":     2,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            _phase44_engaged("sam") and _phase44_engaged("kai")
            and npc_talkable("sam") and npc_talkable("kai")
        ),
    }
    WED_REGISTRY["crossover_caroline_marcus_thursday"] = {
        "type":         "personal",
        "label":        "wevent_crossover_caroline_marcus_thursday",
        "locations":    ["location_bar"],
        "min_day":      7,
        "once":         True,
        "priority":     2,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            _phase44_engaged("caroline") and _phase44_engaged("marcus")
            and npc_talkable("caroline") and npc_talkable("marcus")
        ),
    }

    # ── Phase 49: home social life — NPC invitation visits ────────────────
    # Phase 50: Zoe exhibition opening — once-only, fires at location_gallery
    WED_REGISTRY["zoe_exhibition_opening"] = {
        "type":         "personal",
        "label":        "zoe_exhibition_opening",
        "locations":    ["location_gallery"],
        "min_day":      0,
        "once":         True,
        "priority":     20,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            store.npc_invitation_pending is not None
            and store.npc_invitation_pending.get("invitation_id") == "zoe_exhibition"
            and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
            and not store.zoe_exhibition_done
        ),
    }

    WED_REGISTRY["home_visit_nora_coffee"] = {
        "type":         "personal",
        "label":        "home_visit_nora_coffee",
        "locations":    ["location_home"],
        "min_day":      0,
        "once":         False,
        "priority":     15,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            store.npc_invitation_pending is not None
            and store.npc_invitation_pending.get("invitation_id") == "nora_home_coffee"
            and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
            and not store.nora_home_coffee_done
        ),
    }
    WED_REGISTRY["home_visit_eli_dinner"] = {
        "type":         "personal",
        "label":        "home_visit_eli_dinner",
        "locations":    ["location_home"],
        "min_day":      0,
        "once":         False,
        "priority":     15,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            store.npc_invitation_pending is not None
            and store.npc_invitation_pending.get("invitation_id") == "eli_home_dinner"
            and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
            and not store.eli_home_dinner_done
        ),
    }
    WED_REGISTRY["home_visit_zoe_guitar"] = {
        "type":         "personal",
        "label":        "home_visit_zoe_guitar",
        "locations":    ["location_home"],
        "min_day":      0,
        "once":         False,
        "priority":     15,
        "cooldown":     0,
        "conflict_npc": None,
        "condition":    lambda: (
            store.npc_invitation_pending is not None
            and store.npc_invitation_pending.get("invitation_id") == "zoe_home_guitar"
            and store.day <= store.npc_invitation_pending.get("expiry_day", -999)
            and not store.zoe_home_guitar_done
        ),
    }

    # ── Core query functions ──────────────────────────────────────────────

    def wed_on_cooldown(event_id):
        e   = WED_REGISTRY.get(event_id)
        cd  = e["cooldown"] if e else 0
        if cd <= 0:
            return False
        last = store.wed_event_last_day.get(event_id, -999)
        return (store.day - last) < cd

    def _wed_personal_eligible(event_id, location):
        e = WED_REGISTRY.get(event_id)
        if not e or e["type"] != "personal":
            return False
        if location not in e["locations"]:
            return False
        if store.day < e["min_day"]:
            return False
        if e["once"] and event_id in store.wed_resolved:
            return False
        if wed_on_cooldown(event_id):
            return False
        if store.major_scene_last_day == store.day:
            return False
        cond = e.get("condition")
        if cond is not None and not cond():
            return False
        # Blocked if there is an active (not completed/cancelled) commitment for the NPC today
        npc = e.get("conflict_npc")
        if npc:
            if any(c.get("npc_id") == npc
                   and not c.get("completed") and not c.get("cancelled")
                   and c.get("day") == store.day
                   for c in store.player_commitments):
                return False
        return True

    def wed_personal_eligible(event_id, location):
        """Public wrapper — used by tests and by wed_poll_personal."""
        return _wed_personal_eligible(event_id, location)

    def wed_poll_personal(location):
        """Return one eligible personal event label for this location, or None.
        At most one personal event fires per day across all locations.
        Narrative conditions (trust, etc.) are checked inside the label itself.
        """
        if store.wed_personal_fired_day == store.day:
            return None
        candidates = [
            (e["priority"], eid)
            for eid, e in WED_REGISTRY.items()
            if _wed_personal_eligible(eid, location)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda x: -x[0])
        top_p = candidates[0][0]
        top   = [eid for p, eid in candidates if p == top_p]
        return WED_REGISTRY[renpy.random.choice(top)]["label"]

    def wed_poll_ambient(location):
        """Return pre-rolled ambient event label for this location today, or None.
        Only fires once per location entry (tracked in wed_ambient_fired).
        """
        if store.wed_ambient_fired.get(location):
            return None
        eid = store.wed_ambient_today.get(location)
        if not eid:
            return None
        return WED_REGISTRY.get(eid, {}).get("label")

    # ── Pre-roll: called from new_day() ──────────────────────────────────

    def _wed_roll_ambient_for(location):
        """Probabilistically pick one ambient event for this location today."""
        candidates = []
        for eid, e in WED_REGISTRY.items():
            if e["type"] != "ambient":
                continue
            if location not in e["locations"]:
                continue
            if store.day < e["min_day"]:
                continue
            if e["once"] and eid in store.wed_resolved:
                continue
            if wed_on_cooldown(eid):
                continue
            cond = e.get("condition")
            if cond is not None and not cond():
                continue
            candidates.append(eid)
        if not candidates:
            return None
        renpy.random.shuffle(candidates)
        for eid in candidates:
            w = WED_REGISTRY[eid].get("weight", 0.5)
            if renpy.random.random() < w:
                return eid
        return None

    def _wed_ambient_locations():
        locs = set()
        for e in WED_REGISTRY.values():
            if e["type"] == "ambient":
                for loc in e["locations"]:
                    locs.add(loc)
        return locs

    def wed_preroll_day():
        """Pre-roll ambient events for today. Called by new_day().
        Uses renpy.random so all rolls are rollback-safe.
        Resets per-day tracking.
        """
        store.wed_personal_fired_day = -1
        store.wed_ambient_fired = {}
        result = {}
        for loc in _wed_ambient_locations():
            result[loc] = _wed_roll_ambient_for(loc)
        store.wed_ambient_today = result
        # Promote due callbacks to ready queue
        remaining = []
        ready     = list(store.wed_ready_callbacks)
        for cb in store.wed_callbacks:
            if store.day >= cb["fires_day"]:
                ready.append(cb)
            else:
                remaining.append(cb)
        store.wed_callbacks       = remaining
        store.wed_ready_callbacks = ready

    # ── Fire + schedule ───────────────────────────────────────────────────

    def wed_fire(event_id):
        """Mark event as fired. Call this at the START of an event label
        (after narrative eligibility is confirmed) — not before.
        """
        e = WED_REGISTRY.get(event_id)
        if e is None:
            return   # unknown id: safe no-op
        store.wed_event_last_day = dict(store.wed_event_last_day)
        store.wed_event_last_day[event_id] = store.day
        if e["once"] and event_id not in store.wed_resolved:
            store.wed_resolved = list(store.wed_resolved) + [event_id]
        if e["type"] == "personal":
            store.wed_personal_fired_day = store.day
        else:
            store.wed_ambient_fired = dict(store.wed_ambient_fired)
            for loc in e["locations"]:
                store.wed_ambient_fired[loc] = True

    def wed_schedule_callback(label, fires_day):
        """Queue a callback label to fire on or after fires_day at next location visit."""
        store.wed_callbacks = list(store.wed_callbacks) + [
            {"label": label, "fires_day": fires_day}
        ]

    def wed_pop_callback():
        """Return the label of one ready callback, or None. Removes it from the queue."""
        if not store.wed_ready_callbacks:
            return None
        cb = store.wed_ready_callbacks[0]
        store.wed_ready_callbacks = store.wed_ready_callbacks[1:]
        return cb["label"]

    # ── Marcus home helpers ───────────────────────────────────────────────

    def marcus_is_home():
        """True during Marcus's unscheduled afternoon window.
        He is at park 6-10am and bar 17pm+, so home 10am-5pm.
        Day parity check: on days where day%3==0 he's running errands (~33% absence).
        """
        h = store.hour
        if not (10 <= h < 17):
            return False
        return (store.day % 3) != 0

    def marcus_home_bg():
        return "marcus_home_night" if (store.hour >= 20 or store.hour < 6) else "marcus_home_day"

    def _pick_ambient_variant(cid, variants):
        """Same soft-variety rules as _pick_texture_variant but uses ambient_texture_* stores."""
        last  = store.ambient_texture_last_variant.get(cid)
        days_outer = store.ambient_texture_variant_days
        days  = days_outer.get(cid, {})
        today = store.day
        candidates = [v for v in variants if v != last] or list(variants)
        fresh = [v for v in candidates if today - days.get(v, -999) > 3]
        chosen = (renpy.random.choice(fresh) if fresh
                  else min(candidates, key=lambda v: days.get(v, -999)))
        lv = dict(store.ambient_texture_last_variant); lv[cid] = chosen
        store.ambient_texture_last_variant = lv
        dout = dict(days_outer); din = dict(dout.get(cid, {})); din[chosen] = today
        dout[cid] = din; store.ambient_texture_variant_days = dout
        return chosen


# ── Personal event: Marcus loan ───────────────────────────────────────────

label wevent_marcus_loan:
    # Narrative eligibility check — structural eligibility was confirmed by the WED poll.
    if not marcus_met or marcus_trust < 20 or wed_marcus_loan_state != "none":
        return
    $ wed_fire("marcus_loan")
    $ wed_marcus_loan_state = "offered"
    show marcus_casual_normal as focus_marcus at sprite_r
    m "Hey. I hate to ask — do you have $120 until payday? I can square up by Friday."
    "He's not looking at you when he says it."
    $ _can_full    = (money >= 120 and loan == 0)
    $ _can_partial = (money >= 40  and loan == 0)
    $ _mc_is_low   = (money < 80   or  loan > 0)
    menu:
        "Sure." if _can_full:
            if try_spend(120):
                m "I owe you. For real."
                $ _apply_aff("marcus", 2)
                $ _apply_trust("marcus", 3)
                $ wed_marcus_loan_state = "pending_repay"
                $ wed_marcus_loan_callback_day = day + renpy.random.randint(7, 14)
                $ add_relationship_memory("marcus", "marcus_loan_given", "Lent Marcus money")
        "I can do forty." if _can_partial:
            if try_spend(40):
                m "Forty helps. Appreciate it."
                $ _apply_aff("marcus", 1)
                $ _apply_trust("marcus", 2)
                $ wed_marcus_loan_state = "pending_practical"
                $ wed_marcus_loan_callback_day = day + renpy.random.randint(3, 7)
                $ add_relationship_memory("marcus", "marcus_loan_partial", "Helped Marcus with $40")
        "I'm stretched myself right now." if _mc_is_low:
            m "Yeah, I figured. Had to ask though."
            "He doesn't press it."
            $ _apply_trust("marcus", 2)
            $ wed_marcus_loan_state = "resolved_low_money"
            $ add_relationship_memory("marcus", "marcus_loan_broke", "Both stretched at the same time")
        "I'd rather not lend money." if not _mc_is_low:
            m "Fair enough."
            # ponytail: no trust penalty — respectful refusal is a legitimate position
            $ wed_marcus_loan_state = "resolved_refused"
            $ wed_marcus_loan_callback_day = day + renpy.random.randint(5, 10)
            $ add_relationship_memory("marcus", "marcus_loan_refused", "Turned down Marcus's loan request")
        "Not really my problem.":
            m "Right."
            "He goes quiet."
            $ npc_anger = {**npc_anger, "marcus": npc_anger.get("marcus", 0) + 2}
            $ wed_marcus_loan_state = "resolved_dismissed"
            $ add_relationship_memory("marcus", "marcus_loan_dismissed", "Dismissed Marcus's request")
    return


# ── Personal event: Sam off routine ──────────────────────────────────────

label wevent_sam_off_routine:
    # Narrative eligibility — structural eligibility confirmed by WED.
    if not sam_met or sam_trust < 15 or sam_off_routine_done:
        return
    # Don't fire at gym during her normal gym hours (10-14 Mon-Fri) — it's not "off routine" then
    if current_loc == "location_gym" and 10 <= hour < 14 and day % 7 not in [5, 6]:
        return
    $ wed_fire("sam_off_routine")
    $ sam_off_routine_done = True
    if current_loc == "location_cafe":
        scene expression cafe_bg()
    else:
        scene gymdaypeople
    show screen hud
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    "Sam is here. Wrong day, wrong time. Her coffee is half-finished and she's staring at it."
    menu:
        "\"Thought you were a park person.\"":
            sam "I am. I missed it this morning."
            "You wait."
            sam "Alarm. Just... couldn't."
            $ _apply_trust("sam", 2)
        "\"You alright?\"":
            sam "Fine. I just — yes."
            "She straightens up."
            sam "The routine's the thing, right? One miss and you notice how much of it was holding you together."
            $ _apply_trust("sam", 3)
            $ _apply_aff("sam", 1)
        "\"Coffee's decent here.\"":
            sam "Yeah."
            "She looks at her cup."
            sam "Came in for something else and stayed. It's fine."
            $ _apply_aff("sam", 1)
    hide focus_sam
    $ add_relationship_memory("sam", "sam_off_routine", "Saw Sam off her schedule")
    return


# ── Ambient event: Metro delay ────────────────────────────────────────────

label wevent_metro_delay:
    $ wed_fire("metro_delay")
    $ _metro_delay_time = renpy.random.choice([0.5, 1.0, 0.5])
    "The board reads DELAYED. Signal failure somewhere on the line."
    menu:
        "Wait it out.":
            $ spend_time(_metro_delay_time)
            "Twenty minutes before it clears."
        "Find another way ($6).":
            if try_spend(6):
                "You grab a cab. More expensive; at least it moves."
            else:
                $ spend_time(_metro_delay_time)
                "Not enough for a cab. You wait anyway."
    return


# ── Ambient event: Rain in park ───────────────────────────────────────────

label wevent_rain_in_park:
    $ wed_fire("rain_in_park")
    $ _npc_vis = location_sprites()
    if len(_npc_vis) > 0:
        "The sky closes in fast. Rain in minutes — you can feel it."
        menu:
            "Find cover (stay).":
                scene parkday
                show screen hud
                "You duck under the park shelter. Rain hammers down, then passes."
                $ spend_time(0.5)
            "Head out before it hits.":
                jump map
    else:
        "Rain starts without warning. The park empties fast."
        menu:
            "Stay — you don't mind rain.":
                scene parkday
                show screen hud
                "Soaked but weirdly awake. Five minutes of proper rain."
                $ spend_time(0.5)
                $ need_energy = min(100, need_energy + 5)
            "Leave.":
                jump map
    return


# ── Ambient event: Bar quiz night ─────────────────────────────────────────

label wevent_bar_quiz_night:
    $ wed_fire("bar_quiz_night")
    scene bar
    show screen hud
    "Boards are up. A handwritten sign: QUIZ NIGHT — TEAMS OF 2-4 — ENTRY $5."
    menu:
        "Join a team ($5, 2h).":
            if try_spend(5):
                $ spend_time(2)
                if stat_int >= 30:
                    $ gain_stat("chr", 8)
                    "You're useful. Your table wins the literature round by being the only team that had read the book."
                elif stat_chr >= 30:
                    $ gain_stat("chr", 10)
                    "You're not sure of the answers, but you're confident enough about them. Your table comes second. Close enough."
                else:
                    $ gain_stat("int", 4)
                    "You don't know the answers but you listen well. A few things stick."
            else:
                "Not enough for the entry. You watch from the bar instead."
        "Skip it.":
            "You settle into the background noise."
    return


# ── Callbacks: Marcus loan ────────────────────────────────────────────────

label wevcb_marcus_loan_repay:
    show marcus_casual_normal as focus_marcus at sprite_r
    m "Hey. The $120 — here."
    "He hands it back without ceremony."
    m "Appreciate it. Seriously."
    $ gain_money(120)
    $ _apply_trust("marcus", 2)
    $ wed_marcus_loan_state = "resolved_repaid"
    hide focus_marcus
    return

label wevcb_marcus_loan_partial:
    show marcus_casual_normal as focus_marcus at sprite_r
    m "I said I'd sort something out. You free Saturday morning?"
    menu:
        "Sure, what time?":
            m "Eight. Court at the park. I'll buy coffee after."
            $ _apply_trust("marcus", 2)
            $ _apply_aff("marcus", 2)
            $ wed_marcus_loan_state = "resolved_repaid"
        "Can't this week.":
            m "Some other time, then."
            $ wed_marcus_loan_state = "resolved_repaid"
    hide focus_marcus
    return

label wevcb_marcus_loan_solved:
    show marcus_casual_normal as focus_marcus at sprite_r
    m "Sorted it out, by the way. Just so you know."
    "He doesn't make it into a thing."
    $ _apply_trust("marcus", 1)
    $ wed_marcus_loan_state = "resolved_solved"
    hide focus_marcus
    return


# ── Marcus home: location ─────────────────────────────────────────────────

label location_marcus_home:
    $ current_loc = "location_marcus_home"
    $ activity_exit_jump = "map"
    $ activity_exit_name = "City Map"

    if marcus_home_state == "locked":
        "You don't have Marcus's address yet."
        jump map

    if not marcus_is_home():
        scene expression marcus_home_bg()
        show screen hud
        "You knock. No answer. He must be out."
        jump map

    scene expression marcus_home_bg()
    show screen hud
    show marcus_casual_normal as focus_marcus at sprite_r

    # Loan callback fires here when ready
    if wed_marcus_loan_callback_ready and wed_marcus_loan_state in ("pending_repay", "pending_practical"):
        $ wed_marcus_loan_callback_ready = False
        if wed_marcus_loan_state == "pending_repay":
            call wevcb_marcus_loan_repay
        else:
            call wevcb_marcus_loan_partial
        jump location_marcus_home

    # "Resolved — mentioned it" callback also fires here or at other locations
    if wed_marcus_loan_callback_ready and wed_marcus_loan_state == "pending_solved":
        $ wed_marcus_loan_callback_ready = False
        call wevcb_marcus_loan_solved
        jump location_marcus_home

    $ _chili_ok   = (marcus_home_state in ("invited_once", "welcome") and marcus_chili_last_day != day)
    $ _game_ok    = (hour >= 17 and hour < 23)

    menu (screen="activity"):
        "Talk.":
            call npc_interact("marcus")
            jump location_marcus_home

        "That smells good." if _chili_ok:
            call marcus_home_chili
            jump location_marcus_home

        "Watch the game." if _game_ok:
            call marcus_home_game
            jump location_marcus_home

        "Head out.":
            if marcus_home_state == "invited_once":
                $ marcus_home_state = "welcome"
            jump map


label marcus_home_chili:
    "He spoons some into a bowl without being asked."
    m "Simple. Kidney beans, cheap cuts, chipotle. Takes all day but it doesn't need you."
    $ need_hunger = min(100, need_hunger + 45)
    $ _apply_aff("marcus", 1)
    $ marcus_chili_last_day = day
    if marcus_home_state == "invited_once":
        $ marcus_home_state = "welcome"
    return

label marcus_home_game:
    show marcus_casual_normal as focus_marcus at sprite_r
    "The volume is low. He explains the score without being asked."
    $ spend_time(1.5)
    $ need_energy = min(100, need_energy + 8)
    if marcus_home_state == "invited_once":
        $ marcus_home_state = "welcome"
    menu:
        "Ask about the team.":
            m "Same three problems, different season. They fixed the rebounding and broke the shooting."
            $ _apply_aff("marcus", 1)
        "Just watch.":
            "You don't say much. That's fine."
    return


# ── Personal event: Marcus first-shift check-in ───────────────────────────

label wevent_marcus_first_shift_checkin:
    if not marcus_met or sum(shifts_worked.values()) < 1:
        return
    $ wed_fire("marcus_first_shift_checkin")
    show screen hud
    show marcus_casual_normal as focus_marcus at sprite_r
    m "You're back."
    "Not a question."
    menu:
        "\"Barely.\"":
            $ marcus_first_shift_choice = "barely"
            m "That part doesn't change."
            $ _apply_trust("marcus", 1)
        "\"I could get used to it.\"":
            $ marcus_first_shift_choice = "used_to_it"
            m "Good."
    hide focus_marcus
    return


# ── Personal event: Marcus low-energy comment (max 3, 5-day cooldown) ─────

label wevent_marcus_low_energy_comment:
    if not marcus_met or need_energy > 30 or wed_marcus_low_energy_count >= 3:
        return
    $ wed_fire("marcus_low_energy_comment")
    $ wed_marcus_low_energy_count += 1
    show screen hud
    show marcus_casual_normal as focus_marcus at sprite_r
    m "You know your apartment has a bed, right?"
    mc "I've seen it."
    m "Try using it before it becomes decorative."
    mc "I'm fine."
    m "That sentence usually means the opposite."
    hide focus_marcus
    return


# ── Personal event: Marcus First Steps follow-up (once) ───────────────────

label wevent_marcus_first_steps_followup:
    if not marcus_met or not first_steps_completed:
        return
    $ wed_fire("marcus_first_steps_followup")
    show screen hud
    show marcus_casual_normal as focus_marcus at sprite_r
    m "Looks like you found your feet."
    mc "Mostly."
    m "Mostly is how everyone walks around here."
    mc "You make this city sound reassuring."
    m "That wasn't the goal."
    hide focus_marcus
    $ add_relationship_memory("marcus", "marcus_found_your_feet", "Marcus noticed I was settling in")
    return


# ── Personal event: Marcus new car comment (once) ─────────────────────────

label wevent_marcus_new_car_comment:
    if not marcus_met or not move_in_complete or car_tier <= 0:
        return
    $ wed_fire("marcus_new_car_comment")
    show screen hud
    show marcus_casual_normal as focus_marcus at sprite_r
    m "That yours?"
    mc "Depends. Do you approve?"
    m "It starts?"
    mc "Usually."
    m "Then it's already doing better than half the cars on this street."
    hide focus_marcus
    return


# ── Phase 5: Sam gym events ───────────────────────────────────────────────

label wevent_gym_sam_last_rep:
    if not sam_met:
        return
    $ wed_fire("gym_sam_last_rep")
    scene gymdaypeople
    show screen hud
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    sam "One more."
    mc "That was the last one."
    sam "That was the last one you planned."
    mc "Important distinction."
    sam "Usually is."
    menu:
        "Do one more.":
            "You reset your grip."
            $ _apply_trust("sam", 1)
            sam "Clean rep. Don't rush it."
            hide focus_sam
            $ gain_skill("fit", 2)
        "Stop with good form.":
            mc "I'm stopping before the form goes."
            sam "Good."
            sam "Knowing when to stop counts too."
            hide focus_sam
    return


label wevent_gym_sam_bad_advice:
    if not sam_met:
        return
    $ wed_fire("gym_sam_bad_advice")
    scene gymdaypeople
    show screen hud
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    "A man near the mirrors gives an increasingly complicated explanation of how to avoid warming up."
    mc "Is any of that true?"
    sam "Some of the words are real."
    mc "Should we say something?"
    sam "He'll discover stretching tomorrow."
    hide focus_sam
    return


label wevent_gym_sam_water_break:
    if not sam_met or need_energy > 40:
        return
    $ wed_fire("gym_sam_water_break")
    scene gymdaypeople
    show screen hud
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    sam "Water."
    mc "I'm fine."
    sam "That wasn't a question."
    mc "You always this encouraging?"
    sam "Only when people start negotiating with dehydration."
    hide focus_sam
    return


# ── Phase 5: Zoe public events ────────────────────────────────────────────

label wevent_zoe_sketching_stranger:
    if not zoe_met:
        return
    $ wed_fire("zoe_sketching_stranger")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Don't turn around."
    mc "That's usually when people turn around."
    z "I'm drawing the man behind you."
    mc "Why?"
    z "He has been pretending to read the same page for ten minutes."
    mc "Maybe it's a difficult page."
    z "It's the drinks menu."
    hide focus_zoe
    return


label wevent_zoe_wrong_colour:
    if not zoe_met:
        return
    $ wed_fire("zoe_wrong_colour")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_r
    z "That wall is the wrong colour."
    mc "It's grey."
    z "Exactly."
    mc "What should it be?"
    z "Still grey."
    mc "Helpful."
    z "A different grey."
    hide focus_zoe
    return


label wevent_zoe_lost_pencil:
    if not zoe_met:
        return
    $ wed_fire("zoe_lost_pencil")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    $ _wev_relbar_open("zoe")
    show screen npc_relbar("zoe")
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Have you seen a pencil?"
    mc "What kind?"
    z "The kind that was here."
    mc "Very specific."
    "You point toward the pencil tucked behind her ear."
    $ _apply_trust("zoe", 1)
    z "I was checking whether you were paying attention."
    mc "Of course."
    z "You weren't."
    hide focus_zoe
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ add_relationship_memory("zoe", "zoe_pencil_attention", "Zoe tested whether I was paying attention")
    return


# ── Phase 10: Marcus hallway micro-scenes ────────────────────────────────────

label wevent_marcus_hallway_texture:
    if not marcus_met or not npc_here("marcus") or not move_in_complete:
        return
    $ wed_fire("marcus_hallway_texture")
    show screen hud
    $ _v = _pick_ambient_variant("marcus_hallway", ["laundry", "wrong_mail", "takeout"])
    call expression "wevent_marcus_hallway_tex_" + _v
    return

label wevent_marcus_hallway_tex_laundry:
    show marcus_casual_normal as focus_marcus at sprite_r
    "Marcus steps into the hallway carrying a laundry basket."
    m "Machine on the left eats coins."
    mc "The other one?"
    m "Eats socks."
    mc "Good building."
    m "Strong character."
    hide focus_marcus
    return

label wevent_marcus_hallway_tex_wrong_mail:
    show marcus_casual_normal as focus_marcus at sprite_r
    m "You get anything addressed to apartment sixteen?"
    mc "There is no apartment sixteen."
    m "That explains the delivery rate."
    "He checks the envelope again."
    m "Still not mine."
    hide focus_marcus
    return

label wevent_marcus_hallway_tex_takeout:
    show marcus_casual_normal as focus_marcus at sprite_r
    "Marcus balances a paper bag against his hip while unlocking his door."
    mc "Dinner?"
    m "Technically."
    mc "What makes it technical?"
    m "The restaurant included a fork."
    hide focus_marcus
    return


# ── Phase 10: Zoe park micro-scenes ──────────────────────────────────────────

label wevent_zoe_park_texture:
    if not zoe_met or not npc_here("zoe"):
        return
    $ wed_fire("zoe_park_texture")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    $ _v = _pick_ambient_variant("zoe_park", ["cloud", "bench", "page"])
    call expression "wevent_zoe_park_tex_" + _v
    return

label wevent_zoe_park_tex_cloud:
    show zoe_street_neutral as focus_zoe at sprite_r
    z "That cloud looks artificial."
    mc "Artificial?"
    z "Too symmetrical."
    mc "Should we report it?"
    z "I already drew evidence."
    hide focus_zoe
    return

label wevent_zoe_park_tex_bench:
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Someone moved this bench."
    mc "How can you tell?"
    z "The view is worse."
    mc "Maybe the view moved."
    z "That would be more interesting."
    hide focus_zoe
    return

label wevent_zoe_park_tex_page:
    show zoe_street_neutral as focus_zoe at sprite_r
    "The wind catches one page of Zoe's sketchbook."
    "You stop it with your foot before it crosses the path."
    z "Thanks."
    mc "Do I get to see it?"
    z "That wasn't part of the rescue agreement."
    hide focus_zoe
    return


# ── Phase 10: Nora café micro-scenes (customer visit) ────────────────────────

label wevent_nora_cafe_texture:
    if not nora_met or not npc_here("nora") or active_work_shift == "cafe":
        return
    $ wed_fire("nora_cafe_texture")
    scene expression cafe_bg()
    show screen hud
    $ _v = _pick_ambient_variant("nora_cafe", ["name", "pastry", "table"])
    call expression "wevent_nora_cafe_tex_" + _v
    return

label wevent_nora_cafe_tex_name:
    show nora_cafe_normal as focus_nora at sprite_r
    n "They spelled your name wrong."
    mc "It's four letters."
    n "That probably made them confident."
    hide focus_nora
    return

label wevent_nora_cafe_tex_pastry:
    show nora_cafe_normal as focus_nora at sprite_r
    "Nora looks at the last pastry in the display."
    mc "Are you going to take it?"
    n "I'm waiting to see whether you're polite."
    mc "And if I am?"
    n "Then I take it."
    hide focus_nora
    return

label wevent_nora_cafe_tex_table:
    show nora_cafe_normal as focus_nora at sprite_r
    n "That table has been reserved for twenty minutes."
    mc "Nobody's there."
    n "Exactly."
    mc "Reserved by who?"
    n "A laptop charger."
    hide focus_nora
    return


# ── Phase 11: Static (bar) ambient micro-scenes ───────────────────────────────

label wevent_static_texture:
    $ wed_fire("static_texture")
    $ _v = _pick_ambient_variant("static", ["wrong_drink", "card_reader", "same_song", "reserved_stool"])
    call expression "wevent_static_tex_" + _v
    return

label wevent_static_tex_wrong_drink:
    scene bar
    show screen hud
    "A drink remains on the counter long after its name is called."
    "Someone at the far end of the bar raises a hand."
    "Patron" "That might be mine."
    "Bartender" "It stopped being yours ten minutes ago."
    return

label wevent_static_tex_card_reader:
    scene bar
    show screen hud
    "The card reader displays a tip screen and refuses to move on."
    "Patron" "Did it go through?"
    "Bartender" "It developed boundaries."
    "The screen finally resets."
    return

label wevent_static_tex_same_song:
    scene bar
    show screen hud
    "The same song begins for the third time tonight."
    "Patron" "Again?"
    "A voice near the jukebox answers without looking over."
    "Patron" "It gets better."
    "It does not."
    return

label wevent_static_tex_reserved_stool:
    scene bar
    show screen hud
    "An empty stool has a jacket hanging over it."
    "Nobody returns for several minutes."
    "Patron" "Is someone sitting there?"
    "Bartender" "Spiritually."
    return


# ── Phase 11: Mall ambient micro-scenes ───────────────────────────────────────

label wevent_mall_texture:
    $ wed_fire("mall_texture")
    $ _v = _pick_ambient_variant("mall", ["stopped_escalator", "lost_item", "sample_queue", "wrong_store"])
    call expression "wevent_mall_tex_" + _v
    return

label wevent_mall_tex_stopped_escalator:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    "The escalator stops halfway between floors."
    "Everyone standing on it pauses."
    "Then, reluctantly, they begin using it as stairs."
    return

label wevent_mall_tex_lost_item:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    "Announcement" "A set of keys has been handed to customer service."
    "A second announcement follows immediately."
    "Announcement" "The owner has already collected them."
    return

label wevent_mall_tex_sample_queue:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    "A small queue forms around a tray of free samples."
    "The person handing them out begins cutting each piece in half."
    "The queue continues growing."
    return

label wevent_mall_tex_wrong_store:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    "Customer" "Do you sell phone chargers?"
    "Employee" "This is a shoe store."
    "Customer" "So no?"
    "Employee" "Not intentionally."
    return


# ── Phase 11: Beach ambient micro-scenes ──────────────────────────────────────

label wevent_beach_texture:
    $ wed_fire("beach_texture")
    $ _v = _pick_ambient_variant("beach", ["gull_food", "wind_towel", "cold_water", "sand_shoes"])
    call expression "wevent_beach_tex_" + _v
    return

label wevent_beach_tex_gull_food:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    "A gull lands beside an unattended paper tray."
    "The owner notices one second too late."
    "Beachgoer" "Hey."
    "The gull leaves with no visible remorse."
    return

label wevent_beach_tex_wind_towel:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    "A gust lifts one corner of a beach towel."
    "Then the rest of it."
    "Two people chase it toward the boardwalk."
    return

label wevent_beach_tex_cold_water:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    "A person runs into the water."
    "They stop after three steps."
    "Beachgoer" "It's fine."
    "Nobody follows."
    return

label wevent_beach_tex_sand_shoes:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    "Someone empties sand from one shoe."
    "Then from the other."
    "They put both shoes back on and immediately stop walking."
    return


# ── Phase 12: Marcus and Nora crossover ──────────────────────────────────────

label wevent_crossover_marcus_nora_coffee:
    if not marcus_met or not nora_met:
        return
    $ wed_fire("crossover_marcus_nora_coffee")
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal as focus_nora at sprite_r
    show marcus_casual_normal as focus_marcus at sprite_l
    "Marcus studies the menu above the counter."
    m "When did coffee start needing this many adjectives?"
    n "Around the same time customers started asking for personality."
    m "Can I get one without either?"
    n "Black coffee."
    m "Perfect."
    n "You say that now."
    mc "Do you two know each other?"
    n "He asks that every time."
    m "And she never answers."
    hide focus_nora
    hide focus_marcus
    $ add_relationship_memory("marcus", "marcus_met_nora_at_grounds", "I ran into Marcus and Nora at Grounds")
    return


# ── Phase 12: Sam and Zoe crossover ──────────────────────────────────────────

label wevent_crossover_sam_zoe_park:
    if not sam_met or not zoe_met:
        return
    $ wed_fire("crossover_sam_zoe_park")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_crop(sprite_display_scale("zoe"), _SPRITE_XP_R, sprite_display_y_offset("zoe"))
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_L, sprite_display_y_offset("sam"))
    "Zoe watches Sam repeat the same movement near the court."
    z "Do that again."
    sam "The shot?"
    z "The part before it."
    sam "That narrows it down."
    "Sam repeats the motion more slowly."
    z "Better."
    sam "For the drawing?"
    z "For your balance."
    sam "You could have led with that."
    z "Then you would have changed it."
    hide focus_zoe
    hide focus_sam
    $ add_relationship_memory("sam", "sam_met_zoe_in_park", "Sam and Zoe crossed paths in the park")
    $ add_relationship_memory("zoe", "zoe_met_sam_in_park", "Zoe studied Sam's movement in the park")
    return


# ── Phase 12: Martha and Caroline crossover ───────────────────────────────────

label wevent_crossover_martha_caroline_static:
    if not martha_met or not caroline_met:
        return
    $ wed_fire("crossover_martha_caroline_static")
    scene bar
    show screen hud
    show martha_neutral as focus_martha at sprite_r
    show caroline_normal as focus_caroline at sprite_l
    "Martha and Caroline stand near the quieter end of the bar."
    caro "You changed the order of the presentation."
    ma "I improved the order of the presentation."
    caro "Without mentioning it."
    ma "You noticed."
    caro "That isn't the point."
    ma "It usually is."
    "Both of them look toward MC."
    mc "Should I come back later?"
    caro "Probably."
    ma "You're already here."
    hide focus_martha
    hide focus_caroline
    $ add_relationship_memory("martha", "martha_seen_with_caroline_static", "I saw Martha and Caroline talking at Static")
    $ add_relationship_memory("caroline", "caroline_seen_with_martha_static", "I saw Caroline and Martha talking at Static")
    return


# ── Phase 13: Marcus and Nora crossover repeats ───────────────────────────────

label wevent_crossover_marcus_nora_repeat:
    if not marcus_met or not nora_met or not npc_here("marcus") or not npc_here("nora"):
        return
    $ wed_fire("crossover_marcus_nora_repeat")
    scene expression cafe_bg()
    show screen hud
    $ _v = _pick_ambient_variant("cross_marcus_nora", ["order_again", "wrong_name", "recommendation"])
    call expression "wevent_cross_mn_" + _v
    return

label wevent_cross_mn_order_again:
    show nora_cafe_normal as focus_nora at sprite_r
    show marcus_casual_normal as focus_marcus at sprite_l
    n "Black coffee."
    m "I didn't say anything yet."
    n "You were going to."
    m "I was building to it."
    n "The journey doesn't change the destination."
    hide focus_nora
    hide focus_marcus
    return

label wevent_cross_mn_wrong_name:
    show nora_cafe_normal as focus_nora at sprite_r
    show marcus_casual_normal as focus_marcus at sprite_l
    n "Marco?"
    m "Close."
    n "It's on the cup."
    m "In your handwriting."
    n "Which makes you Marco."
    hide focus_nora
    hide focus_marcus
    return

label wevent_cross_mn_recommendation:
    show nora_cafe_normal as focus_nora at sprite_r
    show marcus_casual_normal as focus_marcus at sprite_l
    m "What's good today?"
    n "Everything."
    m "What's better than usual?"
    n "That would require a baseline."
    m "I come here every week."
    n "And your opinion so far?"
    m "I'm still forming it."
    hide focus_nora
    hide focus_marcus
    return


# ── Phase 13: Sam and Zoe crossover repeats ───────────────────────────────────

label wevent_crossover_sam_zoe_repeat:
    if not sam_met or not zoe_met or not npc_here("sam") or not npc_here("zoe"):
        return
    $ wed_fire("crossover_sam_zoe_repeat")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    $ _v = _pick_ambient_variant("cross_sam_zoe", ["shadow", "pace", "stop"])
    call expression "wevent_cross_sz_" + _v
    return

label wevent_cross_sz_shadow:
    show zoe_street_neutral as focus_zoe at sprite_crop(sprite_display_scale("zoe"), _SPRITE_XP_R, sprite_display_y_offset("zoe"))
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_L, sprite_display_y_offset("sam"))
    "Zoe is looking at the ground rather than her sketchbook."
    sam "Are you drawing shadows?"
    z "I'm drawing what the light avoids."
    sam "That's the same thing."
    z "It isn't."
    "Sam considers this."
    sam "Show me the difference."
    hide focus_zoe
    hide focus_sam
    return

label wevent_cross_sz_pace:
    show zoe_street_neutral as focus_zoe at sprite_crop(sprite_display_scale("zoe"), _SPRITE_XP_R, sprite_display_y_offset("zoe"))
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_L, sprite_display_y_offset("sam"))
    sam "I'm running a different loop today."
    z "I know."
    sam "You've been here forty minutes."
    z "You changed your pace near the third bench."
    sam "Did it look worse?"
    z "It looked like something."
    hide focus_zoe
    hide focus_sam
    return

label wevent_cross_sz_stop:
    show zoe_street_neutral as focus_zoe at sprite_crop(sprite_display_scale("zoe"), _SPRITE_XP_R, sprite_display_y_offset("zoe"))
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_L, sprite_display_y_offset("sam"))
    "Sam stops beside the bench where Zoe is sitting."
    sam "You're always here."
    z "So are you."
    sam "I'm moving."
    z "I'm working."
    sam "Is watching people work?"
    z "Watching people is the work."
    hide focus_zoe
    hide focus_sam
    return


# ── Phase 13: Martha and Caroline crossover repeats ───────────────────────────

label wevent_crossover_martha_caroline_repeat:
    if not martha_met or not caroline_met or not npc_here("martha") or not npc_here("caroline"):
        return
    $ wed_fire("crossover_martha_caroline_repeat")
    scene bar
    show screen hud
    $ _v = _pick_ambient_variant("cross_martha_caroline", ["deadline", "credit", "seat"])
    call expression "wevent_cross_mc_" + _v
    return

label wevent_cross_mc_deadline:
    show martha_neutral as focus_martha at sprite_r
    show caroline_normal as focus_caroline at sprite_l
    caro "The deadline moved."
    ma "By how much?"
    caro "Three days earlier."
    ma "That was a delivery date, not a deadline."
    caro "The client stopped seeing the distinction."
    ma "Then we should help them see it."
    caro "That ship has sailed."
    ma "Find it."
    hide focus_martha
    hide focus_caroline
    return

label wevent_cross_mc_credit:
    show martha_neutral as focus_martha at sprite_r
    show caroline_normal as focus_caroline at sprite_l
    ma "You attributed the forecast model to Hendricks."
    caro "He ran the model."
    ma "You built it."
    caro "There's a difference?"
    ma "There's a large difference."
    caro "I'll note it next time."
    "Martha does not look satisfied with that answer."
    hide focus_martha
    hide focus_caroline
    return

label wevent_cross_mc_seat:
    show martha_neutral as focus_martha at sprite_r
    show caroline_normal as focus_caroline at sprite_l
    "Caroline is already at the bar when Martha arrives."
    ma "You're in my seat."
    caro "There are no assigned seats."
    ma "There are preferred ones."
    caro "I prefer this one."
    "Martha sits one stool over without comment."
    "This is also, apparently, fine."
    hide focus_martha
    hide focus_caroline
    return


# ── Phase 15: Eleven public ambient micro-scenes ─────────────────────────────

label wevent_eleven_public_texture:
    $ wed_fire("eleven_public_texture")
    scene kitchen
    show screen hud
    $ _v = _pick_ambient_variant("eleven_public", ["waiting_table", "dropped_fork", "dessert_question"])
    call expression "wevent_eleven_pub_" + _v
    return

label wevent_eleven_pub_waiting_table:
    "A server checks the same empty table for the third time."
    "Server" "They said they were parking."
    "Host" "Twenty minutes ago."
    "Server" "Large car."
    return

label wevent_eleven_pub_dropped_fork:
    "A fork hits the floor near the centre of the dining room."
    "Several people glance toward the sound."
    "The person who dropped it continues eating as though nothing happened."
    return

label wevent_eleven_pub_dessert_question:
    "Guest" "Is the dessert meant to be shared?"
    "Server" "It can be."
    "Guest" "Is it large enough to be shared?"
    "Server" "That depends on the relationship."
    return


# ── Phase 15: Nexus public ambient micro-scenes ───────────────────────────────

label wevent_nexus_public_texture:
    $ wed_fire("nexus_public_texture")
    scene goodoffice1
    show screen hud
    $ _v = _pick_ambient_variant("nexus_public", ["badge_retry", "elevator_hold", "courier_floor"])
    call expression "wevent_nexus_pub_" + _v
    return

label wevent_nexus_pub_badge_retry:
    "Someone taps their access badge against the reader."
    "The light turns red."
    "They try the same movement again, more slowly."
    "The light remains unconvinced."
    return

label wevent_nexus_pub_elevator_hold:
    "Employee" "Can you hold that?"
    "The elevator doors begin closing."
    "Someone inside presses a button."
    "The doors close faster."
    "Employee" "Helpful."
    return

label wevent_nexus_pub_courier_floor:
    "Courier" "Which floor is accounts?"
    "Receptionist" "Seven."
    "Courier" "And legal?"
    "Receptionist" "Also seven."
    "Courier" "That feels deliberate."
    return


# ── Phase 15: Hospital public ambient micro-scenes ────────────────────────────

label wevent_hospital_public_texture:
    $ wed_fire("hospital_public_texture")
    scene expression ("hospital_night" if (hour >= 20 or hour < 6) else "hospital1")
    show screen hud
    $ _v = _pick_ambient_variant("hospital_public", ["queue_number", "wrong_floor", "vending_machine"])
    call expression "wevent_hospital_pub_" + _v
    return

label wevent_hospital_pub_queue_number:
    "The display changes from forty-one to forty-three."
    "A person holding ticket forty-two looks up."
    "Visitor" "Did I miss it?"
    "Receptionist" "No."
    "Visitor" "Then did the machine?"
    "Receptionist" "Possibly."
    return

label wevent_hospital_pub_wrong_floor:
    "Visitor" "Is imaging on this floor?"
    "Staff" "One floor up."
    "Visitor" "The sign says this floor."
    "Staff" "The sign is waiting to be replaced."
    "Visitor" "For how long?"
    "Staff" "Long enough to become inaccurate."
    return

label wevent_hospital_pub_vending_machine:
    "A packet stops halfway down the vending machine."
    "The buyer presses the selection button again."
    "A second packet joins the first."
    "Visitor" "Progress."
    return


# ── Phase 16: Library ambient micro-scenes ────────────────────────────────────

label wevent_library_texture:
    $ wed_fire("library_texture")
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    $ _v = _pick_ambient_variant("library_public", ["reserved_seat", "printer_paper", "return_cart"])
    call expression "wevent_library_pub_" + _v
    return

label wevent_library_pub_reserved_seat:
    "An empty chair has a notebook resting on it."
    "Nobody returns for several minutes."
    "Visitor" "Is someone using this seat?"
    "Student" "The notebook is."
    return

label wevent_library_pub_printer_paper:
    "The printer stops after producing one page."
    "Student" "It says it's out of paper."
    "Librarian" "It said that before you printed."
    "Student" "So it knew?"
    "Librarian" "It suspected."
    return

label wevent_library_pub_return_cart:
    "A book cart squeaks with every turn of its front wheel."
    "The librarian pushes it more slowly."
    "The squeak becomes longer."
    return


# ── Phase 16: College ambient micro-scenes ────────────────────────────────────

label wevent_college_texture:
    $ wed_fire("college_texture")
    scene college_day
    show screen hud
    $ _v = _pick_ambient_variant("college_public", ["room_change", "group_project", "vending_choice"])
    call expression "wevent_college_pub_" + _v
    return

label wevent_college_pub_room_change:
    "A paper sign has been taped over the room number."
    "Student" "It says the class moved."
    "Student" "Where?"
    "The bottom half of the sign is missing."
    return

label wevent_college_pub_group_project:
    "Student" "I finished my section."
    "Student" "Which section was yours?"
    "Student" "The introduction."
    "Student" "We already had an introduction."
    "Student" "Now we have two."
    return

label wevent_college_pub_vending_choice:
    "Someone studies the vending machine for several minutes."
    "Student" "Everything on the bottom row is sold out."
    "Student" "Then choose from the top."
    "Student" "That isn't how decisions work."
    return


# ── Phase 16: Downtown ambient micro-scenes ───────────────────────────────────

label wevent_downtown_texture:
    $ wed_fire("downtown_texture")
    scene expression ("centerstreet_night" if (hour >= 20 or hour < 6) else "centerstreet_day")
    show screen hud
    $ _v = _pick_ambient_variant("downtown_public", ["crosswalk", "delivery", "parking_meter"])
    call expression "wevent_downtown_pub_" + _v
    return

label wevent_downtown_pub_crosswalk:
    "The crossing signal begins counting down from five."
    "Someone at the curb considers running."
    "They take one step forward."
    "The signal reaches zero."
    "They step back."
    return

label wevent_downtown_pub_delivery:
    "A delivery cart blocks half of a doorway."
    "Courier" "I'll be thirty seconds."
    "Employee" "You said that two minutes ago."
    "Courier" "Then I'm nearly finished."
    return

label wevent_downtown_pub_parking_meter:
    "A driver presses the parking meter button repeatedly."
    "The screen remains blank."
    "Driver" "Is it free?"
    "Passerby" "The parking or the machine?"
    "Driver" "Whichever answer is better."
    return


# ── Phase 17: Garage (car dealer) ambient micro-scenes ───────────────────────
# Bank and airport lounge are blocked: backgrounds exist in images.rpy but
# neither has a reusable public location label or map entry point.

label wevent_garage_texture:
    $ wed_fire("garage_texture")
    scene cardealer_day
    show screen hud
    $ _v = _pick_ambient_variant("garage_public", ["hood_latch", "tire_pressure", "waiting_chair"])
    call expression "wevent_garage_pub_" + _v
    return

label wevent_garage_pub_hood_latch:
    "A mechanic lifts the hood on a car parked near the entrance."
    "It does not latch the first time."
    "Mechanic" "Stand back."
    "The second attempt catches."
    "Mechanic" "Good."
    return

label wevent_garage_pub_tire_pressure:
    "Customer" "The light came on this morning."
    "Mechanic" "Which one?"
    "Customer" "The one that looks like a flat tyre."
    "Mechanic" "They all look like a flat tyre."
    "Customer" "The other one, then."
    return

label wevent_garage_pub_waiting_chair:
    "Three chairs against the wall."
    "Two people sitting in the ones on the ends."
    "The chair in the middle stays empty."
    "Nobody says anything about it."
    return


# ── Phase 31: Marcus park invitation scene ────────────────────────────────────

label wevent_marcus_park_invite_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "marcus_park_invite"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("marcus")):
        return
    $ wed_fire("marcus_park_invite_scene")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    show marcus_park_neutral as focus_marcus at sprite_r
    "Marcus is leaning against the fence near the court."
    m "You actually came."
    mc "You invited me."
    m "People say things."
    mc "Good system."
    m "Works most of the time."
    "He rolls a basketball beneath one foot, then looks toward the open court."
    m "You playing, or supervising?"
    menu:
        "Play for a while.":
            mc "I'll play."
            m "That sounded dangerously confident."
            "You spend a while trading easy shots and arguing about which ones count."
        "Stay and talk.":
            mc "I'm supervising."
            m "Knew I hired the right person."
            "You stay near the court and talk while Marcus takes occasional shots."
    hide focus_marcus
    $ spend_time(1)
    $ _fu_d = dict(store.npc_invitation_followup_pending); _fu_d["marcus"] = {"invitation_id": "marcus_park_invite", "completed_day": day}; store.npc_invitation_followup_pending = _fu_d
    $ store.npc_invitation_pending = None
    return


# ── Phase 31: Nora grounds invitation scene ───────────────────────────────────

label wevent_zoe_park_invite_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "zoe_park_invite"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("zoe")):
        return
    $ wed_fire("zoe_park_invite_scene")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_r
    "Zoe is sitting near the path with her sketchbook open across her knees."
    z "You came."
    mc "You asked for a second opinion."
    z "I asked whether you were available."
    mc "That sounded like an invitation."
    z "Apparently it worked."
    "She turns the sketchbook enough for you to see two versions of the same scene."
    z "Which one?"
    menu:
        "The first one.":
            mc "The first."
            z "Why?"
            mc "It feels less finished."
            z "That was not the expected advantage."
        "The second one.":
            mc "The second."
            z "Why?"
            mc "You look less annoyed by it."
            z "That might be a flaw."
        "Neither yet.":
            mc "Neither. Not yet."
            z "That is irritatingly close to what I thought."
    hide focus_zoe
    $ spend_time(0.5)
    $ _fu_d = dict(store.npc_invitation_followup_pending); _fu_d["zoe"] = {"invitation_id": "zoe_park_invite", "completed_day": day}; store.npc_invitation_followup_pending = _fu_d
    $ store.npc_invitation_pending = None
    return


# ── Phase 33: Eli library invitation scene ────────────────────────────────────

label wevent_eli_library_invite_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "eli_library_invite"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("eli")):
        return
    $ wed_fire("eli_library_invite_scene")
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    show eli_normal as focus_eli at sprite_r
    "Eli is sitting at the end of a long table with two cables running toward the wall."
    eli "The second outlet still works."
    mc "You sound surprised."
    eli "I allowed for changing conditions."
    "You sit across from her while she shifts a stack of books out of the way."
    eli "Are you actually working?"
    menu:
        "For a while.":
            mc "For a while."
            eli "Good. Quietly."
            "You work beside each other with only the occasional turn of a page or tap of a key."
        "After a short break.":
            mc "After a short break."
            eli "That is how long breaks become long breaks."
            mc "You invited me."
            eli "I invited you to the table."
    hide focus_eli
    $ spend_time(1)
    $ _fu_d = dict(store.npc_invitation_followup_pending); _fu_d["eli"] = {"invitation_id": "eli_library_invite", "completed_day": day}; store.npc_invitation_followup_pending = _fu_d
    $ store.npc_invitation_pending = None
    return


# ── Phase 31: Nora grounds invitation scene ───────────────────────────────────

label wevent_nora_grounds_invite_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "nora_grounds_invite"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("nora")
            or store.active_work_shift == "cafe"):
        return
    $ wed_fire("nora_grounds_invite_scene")
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal as focus_nora at sprite_r
    "Nora sets a small cup on the counter in front of you."
    n "Before you ask, it isn't on the menu."
    mc "Comforting."
    n "That depends on the answer."
    "You take a careful sip."
    n "Well?"
    menu:
        "It's good.":
            mc "It's good."
            n "Too quick. Try again."
            mc "It is still good."
            n "Better."
        "It needs something.":
            mc "It needs something."
            n "Specific."
            mc "You invited an unbiased opinion, not a useful one."
            n "That was my mistake."
        "I don't know what it is.":
            mc "I don't know what it is."
            n "That is technically information."
            mc "Useful?"
            n "Not remotely."
    hide focus_nora
    $ spend_time(0.5)
    $ _fu_d = dict(store.npc_invitation_followup_pending); _fu_d["nora"] = {"invitation_id": "nora_grounds_invite", "completed_day": day}; store.npc_invitation_followup_pending = _fu_d
    $ store.npc_invitation_pending = None
    return


# ── Phase 37: Nora Static bar date scene ─────────────────────────────────────

label wevent_nora_static_date_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "nora_static_date"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("nora")
            or not _date_route_eligible("nora")):
        return
    $ wed_fire("nora_static_date_scene")
    scene bar
    show screen hud
    $ _wev_relbar_open("nora")
    show screen npc_relbar("nora")
    show nora_casual_normal as focus_nora at sprite_r
    "Nora is at the far end of the bar with a glass in front of her that isn't water."
    n "You came."
    mc "You asked."
    n "I noted that you were at the bar. You could have been anyone."
    mc "Anyone who comes when you text them."
    n "Apparently."
    "She pushes a second glass across the bar without asking."
    menu:
        "What is it?":
            mc "What is it?"
            n "Something I've been thinking about."
            mc "The drink, not the occasion."
            n "Those are the same answer."
        "Thank you.":
            mc "Thank you."
            n "You haven't tasted it yet."
            mc "Pre-emptive."
            n "Optimistic."
        "We're not calling this a date.":
            mc "We're not calling this a date."
            n "That is an interesting thing to say unprompted."
            mc "I just wanted to be clear."
            n "Then we both know what it is."
    hide focus_nora
    $ spend_time(1.5)
    $ fs_record_social("nora", "date")
    $ record_social_attention("nora", "date")
    $ _apply_aff("nora", 3)
    $ _apply_trust("nora", 1)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ store.npc_invitation_pending = None
    return


# ── Phase 37: Zoe beach date scene ───────────────────────────────────────────

label wevent_zoe_beach_date_scene:
    if (store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "zoe_beach_date"
            or store.day > store.npc_invitation_pending.get("expiry_day", -999)
            or not npc_here("zoe")
            or not _date_route_eligible("zoe")):
        return
    $ wed_fire("zoe_beach_date_scene")
    scene expression ("sandbeach_night" if hour >= 19 else "sandbeach_day")
    show screen hud
    $ _wev_relbar_open("zoe")
    show screen npc_relbar("zoe")
    show zoe_street_neutral as focus_zoe at sprite_r
    "Zoe is at the edge of the sand with her shoes off and a sketchbook closed beside her."
    z "You actually came."
    mc "You said I should be here."
    z "I say a lot of things."
    mc "This one worked."
    "She doesn't answer. The water is dark and the light is going."
    z "Sit down."
    mc "Is that an invitation or an instruction?"
    z "Yes."
    menu:
        "You're not drawing.":
            mc "You're not drawing."
            z "Not right now."
            mc "What changed?"
            z "The view got more interesting."
        "Nice out here.":
            mc "It's nice out here."
            z "I know."
            mc "You could have mentioned that in the text."
            z "I did."
        "What are we doing?":
            mc "What are we doing?"
            z "Sitting. Watching the water."
            mc "That's it?"
            z "That's enough."
    hide focus_zoe
    $ spend_time(1.5)
    $ fs_record_social("zoe", "date")
    $ record_social_attention("zoe", "date")
    $ _apply_aff("zoe", 3)
    $ _apply_trust("zoe", 1)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ store.npc_invitation_pending = None
    return


# ── Phase 44: NPC crossover scenes (Wave 2) ───────────────────────────────────

label wevent_crossover_nora_elle_grounds:
    $ wed_fire("crossover_nora_elle_grounds")
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal as focus_nora at sprite_r
    show elle_sundress_normal as focus_elle at sprite_l
    "Elle is already at the counter when Nora sets something down in front of her — without being asked."
    n "Oat, extra shot, no foam."
    el "I didn't order yet."
    n "I know."
    "Elle looks at the cup."
    el "The place near the harbour did it differently."
    n "Better?"
    el "Different."
    n "That's a diplomatic answer."
    el "It was a smaller cup."
    n "Was it the cup or the view?"
    "Elle pauses just long enough."
    el "The view."
    n "Thought so."
    mc "How long have you two—"
    el "She remembers orders."
    n "She asks questions."
    "They both seem to find this satisfactory."
    hide focus_nora
    hide focus_elle
    $ add_relationship_memory("nora", "nora_met_elle_at_grounds", "Nora and Elle have a routine at Grounds")
    $ add_relationship_memory("elle", "elle_met_nora_at_grounds", "Nora already knows Elle's order")
    return


label wevent_crossover_lena_marcus_bar:
    $ wed_fire("crossover_lena_marcus_bar")
    scene bar
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    show marcus_bar_normal as focus_marcus at sprite_l
    "Lena is at the corner of the bar — the seat nearest the exit."
    "Marcus sits down one stool over, closer to the centre."
    m "The end one has a draft."
    lena "I noticed."
    m "And you took it anyway."
    lena "Old habit."
    "He slides his stool slightly, making room on the quieter side without explaining why."
    "Lena looks at him."
    lena "You didn't explain that."
    m "You didn't ask."
    "She moves to the better seat without comment."
    lena "You're more observant than you let on."
    m "Bar etiquette. Different thing."
    lena "Is it?"
    "He orders without answering."
    hide focus_lena
    hide focus_marcus
    $ add_relationship_memory("lena", "lena_met_marcus_at_static", "Marcus noticed Lena's seat preference before she said anything")
    $ add_relationship_memory("marcus", "marcus_met_lena_at_static", "Lena noted Marcus was more observant than expected")
    return


label wevent_crossover_sam_kai_gym:
    $ wed_fire("crossover_sam_kai_gym")
    scene gymdaypeople
    show screen hud
    show sam_normal as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    show kai_gym_normal as focus_kai at sprite_crop(sprite_display_scale("kai"), _SPRITE_XP_L, sprite_display_y_offset("kai"))
    "Sam is checking her phone between sets. Kai walks over."
    kai "You skipped the cool-down again."
    sam "I had time for one more set."
    kai "Recovery is in the plan. You wrote it."
    sam "I wrote it for a reason."
    kai "And then you scheduled it out."
    "She looks up."
    sam "I've seen your Saturday sessions. You add sets when you're feeling good."
    kai "I'm adjusting to what's there. That's different."
    sam "The programme also says ten minutes at the end."
    "Sam puts the phone down."
    sam "You don't actually rest between sets."
    kai "I move differently between sets. That's rest."
    "Neither of them asks MC."
    hide focus_sam
    hide focus_kai
    $ add_relationship_memory("sam", "sam_met_kai_gym_debate", "Sam and Kai disagree about what recovery means")
    $ add_relationship_memory("kai", "kai_met_sam_gym_debate", "Sam caught Kai's own inconsistency back at him")
    return


label wevent_crossover_caroline_marcus_thursday:
    $ wed_fire("crossover_caroline_marcus_thursday")
    scene bar
    show screen hud
    show caroline_normal as focus_caroline at sprite_r
    show marcus_bar_normal as focus_marcus at sprite_l
    "Marcus is already at the bar when Caroline arrives on Thursday."
    m "You're consistent."
    caro "It's Thursday."
    m "That explains it."
    "She sits two stools away and waits for the bartender."
    m "Quick HR question."
    caro "I'm off the clock."
    m "I wasn't asking for professional advice."
    caro "What were you asking?"
    m "Whether it's legal to ban someone from the dartboard for being too good."
    "She looks at the board. Then at him."
    caro "That's not HR. That's a house rule."
    m "So yes, then."
    caro "I didn't say yes."
    hide focus_caroline
    hide focus_marcus
    $ add_relationship_memory("marcus", "marcus_met_caroline_thursday", "Marcus and Caroline have their own Thursday routine")
    $ add_relationship_memory("caroline", "caroline_met_marcus_thursday", "Marcus does not ask for HR advice at the bar")
    return


# ── Phase 44: crossover Talk callbacks ───────────────────────────────────────

label talk_followup_crossover_nora_elle_nora:
    $ _do_talk_accounting("nora")
    n "Your friend came in again."
    mc "Which friend?"
    n "The one who can't just say the coffee was good."
    "She wipes down the counter."
    n "She's fine. Just precise about what she'll admit."
    $ crossover_nora_elle_callback_nora_done = True
    return


label talk_followup_crossover_nora_elle_elle:
    $ _do_talk_accounting("elle")
    el "Your barista knows my order."
    mc "Nora."
    el "She didn't ask."
    mc "She doesn't need to."
    el "I'm not sure how I feel about that."
    mc "You keep going back."
    el "That's not an answer."
    $ crossover_nora_elle_callback_elle_done = True
    return


label talk_followup_crossover_lena_marcus_lena:
    $ _do_talk_accounting("lena")
    lena "Your neighbour is observant."
    mc "Marcus?"
    lena "He noticed I was sitting in a draft. He didn't say anything — he just moved."
    mc "He's like that."
    lena "Most people aren't."
    $ crossover_lena_marcus_callback_lena_done = True
    return


label talk_followup_crossover_lena_marcus_marcus:
    $ _do_talk_accounting("marcus")
    m "The doctor from the hospital. She drinks alone at the end of the bar."
    mc "Lena."
    m "She doesn't look like someone who needs company. She looks like someone who's earned the quiet."
    mc "That's a generous read."
    m "I just moved a stool."
    $ crossover_lena_marcus_callback_marcus_done = True
    return


label talk_followup_crossover_sam_kai_sam:
    $ _do_talk_accounting("sam")
    sam "Kai doesn't follow his own programme."
    mc "Did you expect him to?"
    sam "I thought I was the one with the structure problem."
    mc "You're both structured. Differently."
    sam "His way isn't a structure. It's a performance."
    "She doesn't say it with contempt."
    $ crossover_sam_kai_callback_sam_done = True
    return


label talk_followup_crossover_sam_kai_kai:
    $ _do_talk_accounting("kai")
    kai "Sam tracks everything."
    mc "She's methodical."
    kai "She tracks rest days like they're debts."
    mc "Maybe they are for her."
    kai "Maybe. But the plan is supposed to serve you, not the other way around."
    "He says it lightly. He means it."
    $ crossover_sam_kai_callback_kai_done = True
    return


label talk_followup_crossover_caroline_marcus_caroline:
    $ _do_talk_accounting("caroline")
    caro "Your neighbour asked about dartboard rules last Thursday."
    mc "Was it an HR question?"
    caro "He said it wasn't."
    mc "Was it?"
    caro "No. But he framed it like one."
    "She seems to find this mildly interesting."
    $ crossover_caroline_marcus_callback_caroline_done = True
    return


label talk_followup_crossover_caroline_marcus_marcus:
    $ _do_talk_accounting("marcus")
    m "The woman from the Thursday crowd — she's HR."
    mc "Caroline."
    m "She told me she was off the clock. Which means she was counting the seconds."
    mc "You could have just asked her."
    m "I wasn't asking for HR advice."
    mc "What were you asking?"
    m "Whether she had a sense of humour."
    mc "Does she?"
    m "She left without confirming it."
    $ crossover_caroline_marcus_callback_marcus_done = True
    return
