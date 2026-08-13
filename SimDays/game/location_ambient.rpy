# Location ambient system (Section 24C-D, 24F-I).
# Ambient moments, NPC crossovers, opening hours, time flavor, visit tracking,
# reactive conversation topics.

init python:

    # ── 24C — Ambient location moments ───────────────────────────────────────
    LOCATION_AMBIENT_TEMPLATES = {
        "location_cafe": [
            {"id": "cafe_busy_morning",  "hours": range(7,  10), "days": range(7), "text": "The morning rush is in full swing. Every table occupied.", "cooldown": 2},
            {"id": "cafe_nora_customer", "hours": range(10, 16), "days": range(5), "text": "Nora is dealing patiently with a customer who can't decide.", "req_met": "nora", "cooldown": 3},
            {"id": "cafe_laptop_crowd",  "hours": range(13, 17), "days": range(7), "text": "The afternoon crowd is all laptops and headphones.", "cooldown": 2},
            {"id": "cafe_event_flyer",   "hours": range(8,  20), "days": range(7), "text": "A flyer on the board advertises a local Open Mic this Friday.", "cooldown": 7},
        ],
        "location_park": [
            {"id": "park_runners",    "hours": range(6,  10), "days": range(7), "text": "A group of runners passes, breathing hard.", "cooldown": 2},
            {"id": "park_musician",   "hours": range(12, 17), "days": [4,5,6],  "text": "Someone is playing guitar near the fountain. A few people stopped to listen.", "cooldown": 3},
            {"id": "park_zoe_sketch", "hours": range(14, 18), "days": [3, 4],   "text": "Zoe is sitting on the grass with her sketchbook open.", "req_met": "zoe", "cooldown": 4},
        ],
        "location_bar": [
            {"id": "bar_prep_early",    "hours": range(17, 19), "days": range(7), "text": "The bar staff are setting up. Still quiet.", "cooldown": 2},
            {"id": "bar_marcus_regular","hours": range(19, 23), "days": range(7), "text": "Marcus is chatting with a regular at the far end of the bar.", "req_met": "marcus", "cooldown": 3},
            {"id": "bar_celebration",   "hours": range(20, 24), "days": [4,5,6], "text": "A small group in the corner is celebrating something. Laughter and clinking glasses.", "cooldown": 5},
        ],
        "location_library": [
            {"id": "lib_study_group", "hours": range(10, 16), "days": range(5), "text": "A study group has claimed the big table and spread papers everywhere.", "cooldown": 2},
            {"id": "lib_eli_working", "hours": range(12, 18), "days": range(7), "text": "Eli is in the corner, headphones on, completely absorbed in something.", "req_met": "eli", "cooldown": 3},
        ],
        "location_gym": [
            {"id": "gym_maintenance", "hours": range(8,  10), "days": [0,2,4], "text": "Staff are wiping down equipment. The gym is only half-open.", "cooldown": 3},
            {"id": "gym_kai_client",  "hours": range(10, 14), "days": [5,6],   "text": "Kai is running through a training session with someone.", "req_met": "kai", "cooldown": 4},
        ],
        "location_hospital": [
            {"id": "hosp_shift_change", "hours": range(15, 17), "days": range(5), "text": "Shift change. Nurses and doctors pass in and out quickly.", "cooldown": 2},
            {"id": "hosp_waiting",      "hours": range(9,  12), "days": range(7), "text": "The waiting area is full. A child is drawing on a pamphlet.", "cooldown": 2},
        ],
        "location_warehouse": [
            {"id": "wh_delay", "hours": range(9,  13), "days": [1, 3], "text": "A delivery truck is blocking the side entrance.", "req_met": "natalie", "cooldown": 4},
            {"id": "wh_break", "hours": range(12, 14), "days": range(6), "text": "Workers on break outside, coffee cups in hand.", "cooldown": 2},
        ],
    }

    def check_location_ambient(location_id):
        if store.location_ambient_today.get(location_id): return None
        h   = int(store.hour)
        dw  = store.day % 7
        candidates = [
            t for t in LOCATION_AMBIENT_TEMPLATES.get(location_id, [])
            if h in t.get("hours", range(24))
            and (not t.get("days") or dw in t["days"])
            and (not t.get("req_met") or getattr(store, t["req_met"] + "_met", False))
            and (store.day - store.location_ambient_history.get(t["id"], -99)) >= t.get("cooldown", 2)
        ]
        if not candidates: return None
        import random as _r
        rng = _r.Random(store.day * 200 + h + _det_hash(location_id) % 500)
        if rng.random() > 0.4: return None
        return rng.choice(candidates)

    def record_location_ambient(template_id, location_id):
        d = dict(store.location_ambient_history)
        d[template_id] = store.day
        store.location_ambient_history = d
        d2 = dict(store.location_ambient_today)
        d2[location_id] = True
        store.location_ambient_today = d2

    # ── 24D — NPC crossover moments ───────────────────────────────────────────
    NPC_CROSSOVER_TEMPLATES = [
        # hours/days narrowed to match both NPCs' resolved schedules (Phase 59A fix)
        {"id": "marcus_sam_park",       "npcs": ["marcus","sam"],     "location": "location_park",    "hours": range(7,  9),  "days": [1, 3],
         "text": "Marcus and Sam are finishing a run together, stretching near the path.",
         "choices": [("Join the cool-down", {"marcus":1,"sam":1}, 0.5), ("Wave and keep going", {}, 0)], "cooldown": 5},
        # Both are at café Tue 15-17 after schedule reordering fix (Phase 59A).
        {"id": "marcus_nora_tue_cafe",  "npcs": ["marcus","nora"],    "location": "location_cafe",    "hours": [15, 16],      "days": [1],
         "text": "Marcus stops in for his Tuesday coffee. He and Nora are mid-argument about something on his phone.",
         "choices": [("Interrupt with curiosity", {"marcus":1,"nora":1}, 0.5), ("Find a table", {}, 0)], "cooldown": 7},
        # Zoe is never at the library; moved to location_hub where both attend Mon-Fri 9-12.
        {"id": "zoe_eli_hub",           "npcs": ["zoe","eli"],        "location": "location_hub",     "hours": range(9,  12), "days": range(5),
         "text": "Zoe has colonised a corner table and is sketching. Eli is two seats away, laptop open.",
         "choices": [("Pull up a chair", {"zoe":1,"eli":1}, 1), ("Leave them to it", {}, 0)], "cooldown": 6},
        # Sam gym ends 13 on Sat; Kai gym 9-14 WKD. Valid overlap: Sat 9-12 only.
        {"id": "kai_sam_gym_wkd",       "npcs": ["kai","sam"],        "location": "location_gym",     "hours": range(9,  13), "days": [5],
         "text": "Sam is spotting Kai on the bench press, calling out form corrections.",
         "choices": [("Work in with them", {"kai":1,"sam":1}, 1), ("Train elsewhere", {}, 0)], "cooldown": 5},
        # Nora works until 15 on Wed; only h=14 has both at café. One valid hour.
        {"id": "nora_zoe_cafe_wed",     "npcs": ["nora","zoe"],       "location": "location_cafe",    "hours": [14],          "days": [2],
         "text": "Zoe is sketching at a table while Nora refills her coffee.",
         "choices": [("Join them briefly", {"nora":1,"zoe":1}, 0.5), ("Leave them to it", {}, 0)], "cooldown": 6},
        {"id": "martha_caroline_lunch", "npcs": ["martha","caroline"],"location": "location_office",  "hours": range(12, 14), "days": range(5),
         "text": "Martha and Caroline are eating lunch at their desks. The conversation sounds professional but slightly strained.",
         "choices": [("Say hello to both", {"martha":1,"caroline":1}, 0.5), ("Focus on your work", {}, 0)], "cooldown": 7},
    ]

    def check_crossover(location_id):
        h  = int(store.hour)
        dw = store.day % 7
        for tmpl in NPC_CROSSOVER_TEMPLATES:
            if tmpl["location"] != location_id: continue
            if h not in tmpl["hours"]: continue
            if dw not in tmpl["days"]: continue
            last = store._crossover_history.get(tmpl["id"], -99)
            if store.day - last < tmpl.get("cooldown", 5): continue
            if not all(getattr(store, n + "_met", False) for n in tmpl["npcs"]): continue
            states = [resolve_npc_state(n) for n in tmpl["npcs"]]
            if not all(s["location_id"] == location_id and s["public"] for s in states): continue
            import random as _r
            if _r.Random(store.day * 77 + h).random() > 0.35: continue
            return tmpl
        return None

    def record_crossover(template_id):
        d = dict(store._crossover_history)
        d[template_id] = store.day
        store._crossover_history = d

    def _apply_crossover_rel_gain(rel_dict):
        """Apply affection gains from a crossover choice dict {npc_id: amount}."""
        for npc_id, amount in rel_dict.items():
            if amount <= 0: continue
            d = NPC_DATA.get(npc_id, {})
            aff_var = d.get("aff")
            if aff_var:
                setattr(store, aff_var, min(100, getattr(store, aff_var, 0) + amount))

    # ── 24E — Weekly city rhythm ──────────────────────────────────────────────
    CITY_DAY_PROFILES = {
        0: {"name": "Monday",    "vibe": "working week starts", "bar_busy": 0.4},
        1: {"name": "Tuesday",   "vibe": "midweek",             "bar_busy": 0.5},
        2: {"name": "Wednesday", "vibe": "midweek shift",       "bar_busy": 0.5},
        3: {"name": "Thursday",  "vibe": "almost Friday",       "bar_busy": 0.7},
        4: {"name": "Friday",    "vibe": "weekend starts",      "bar_busy": 1.0},
        5: {"name": "Saturday",  "vibe": "full weekend",        "bar_busy": 0.9},
        6: {"name": "Sunday",    "vibe": "quiet close",         "bar_busy": 0.4},
    }

    def city_day_profile(day_value=None):
        return CITY_DAY_PROFILES[(day_value if day_value is not None else store.day) % 7]

    def city_flavor_text(day_value=None, hour_value=None):
        dw = (day_value if day_value is not None else store.day) % 7
        h  = int(hour_value if hour_value is not None else store.hour)
        if dw == 4 and h >= 17: return "The city feels looser than usual. Friday energy."
        if dw == 6 and h < 12:  return "Sunday morning. Half the city is still asleep."
        if dw == 0 and h < 10:  return "Monday. Everyone looks like they need another coffee."
        return ""

    # ── 24F — Time-of-day location flavor ────────────────────────────────────
    LOCATION_TIME_FLAVOR = {
        "location_cafe": {
            "morning":    "The coffee machine hasn't stopped since opening.",
            "afternoon":  "Quieter now — mostly students with laptops.",
            "evening":    "The last few customers linger over cold cups.",
            "late_night": "Closed.",
        },
        "location_park": {
            "morning":    "Runners, dog walkers, cool air.",
            "afternoon":  "Families and people eating lunch on the grass.",
            "evening":    "The light is low. A few people still around.",
            "late_night": "Empty and quiet.",
        },
        "location_bar": {
            "morning":    "Chairs still up. No one here yet.",
            "afternoon":  "Staff prep. A few early drinkers.",
            "evening":    "The bar is filling up.",
            "late_night": "Loud, warm, full.",
        },
        "location_gym": {
            "morning":    "Early crowd, focused and efficient.",
            "afternoon":  "Post-lunch energy slump in the air.",
            "evening":    "After-work rush. All the good machines are taken.",
            "late_night": "Closed.",
        },
        "location_library": {
            "morning":    "Quiet opening. Only the serious regulars this early.",
            "afternoon":  "Study hours. Full and focused.",
            "evening":    "Winding down. A few people finishing up.",
            "late_night": "Closed.",
        },
    }

    def _time_of_day(hour_value=None):
        h = int(hour_value if hour_value is not None else store.hour)
        if h < 12: return "morning"
        if h < 17: return "afternoon"
        if h < 22: return "evening"
        return "late_night"

    def location_time_flavor(location_id, hour_value=None):
        tod = _time_of_day(hour_value)
        return LOCATION_TIME_FLAVOR.get(location_id, {}).get(tod, "")

    # ── 24G — Location opening hours ─────────────────────────────────────────
    LOCATION_OPENING_HOURS = {
        "location_cafe":     {"days": range(7), "open": 7,  "close": 22},
        "location_library":  {"days": range(6), "open": 9,  "close": 21},
        "location_gym":      {"days": range(7), "open": 6,  "close": 22},
        "location_bar":      {"days": range(7), "open": 16, "close": 27},
        "location_hospital": {"days": range(7), "open": 0,  "close": 27},
        "location_office":   {"days": range(5), "open": 8,  "close": 20},
        "location_warehouse":{"days": range(6), "open": 6,  "close": 18},
        "location_park":     {"days": range(7), "open": 0,  "close": 27},
        "location_hub":      {"days": range(6), "open": 8,  "close": 22},
        "location_kitchen":  {"days": range(6), "open": 10, "close": 23},
    }

    def is_location_open(location_id, day_value=None, hour_value=None):
        dw = (day_value if day_value is not None else store.day) % 7
        h  = float(hour_value if hour_value is not None else store.hour)
        info = LOCATION_OPENING_HOURS.get(location_id)
        if not info: return True
        return dw in info["days"] and info["open"] <= h < info["close"]

    def location_closed_reason(location_id):
        dw   = store.day % 7
        info = LOCATION_OPENING_HOURS.get(location_id)
        if not info: return ""
        if dw not in info["days"]: return "Closed today."
        h = store.hour
        if h < info["open"]:   return "Opens at %d:00." % info["open"]
        if h >= info["close"]: return "Closed for the night."
        return ""

    # ── 24H — Reactive conversation topics ───────────────────────────────────
    NPC_REACTIVE_TOPICS = {
        "nora": [
            {"id": "nora_prog_project", "check": lambda: store.freelance_completed >= 1,
             "line": "I heard you finished a programming project. That's actually impressive."},
            {"id": "nora_exhaustion",   "check": lambda: store.need_energy < 25,
             "line": "You look exhausted. Are you sleeping?"},
            {"id": "nora_promotion",    "check": lambda: store.active_careers.get("it", {}).get("rank", 0) >= 1,
             "line": "Someone mentioned you got promoted. Congrats, seriously."},
        ],
        "marcus": [
            {"id": "marcus_freelance",  "check": lambda: store.freelance_completed >= 1,
             "line": "Heard you got paid for that project. Nice."},
            {"id": "marcus_stressed",   "check": lambda: has_player_state("stressed"),
             "line": "You seem like you've had a rough week. Anything going on?"},
            {"id": "marcus_confident",  "check": lambda: has_player_state("confident"),
             "line": "Something went well for you lately. I can tell."},
        ],
        "zoe": [
            {"id": "zoe_performance",   "check": lambda: bool(store.player_portfolio.get("busk_complete_01")),
             "line": "So the park thing was real. I didn't think you'd actually do it."},
            {"id": "zoe_inspired",      "check": lambda: has_player_state("inspired"),
             "line": "You've got that look. Something clicked for you recently?"},
            {"id": "zoe_prog_5",        "check": lambda: skill_val("prog") >= 5,
             "line": "You're getting seriously into programming. I can tell from the bags under your eyes."},
        ],
        "eli": [
            {"id": "eli_prog_progress", "check": lambda: skill_val("prog") >= 3,
             "line": "Your code on that side project was cleaner than I expected. Keep at it."},
            {"id": "eli_freelance_early","check": lambda: store.freelance_completed >= 3,
             "line": "Three projects already. You're moving faster than most people do."},
        ],
        "lena": [
            {"id": "lena_exhaustion",   "check": lambda: store.need_energy < 20,
             "line": "Professionally speaking — you look like you need sleep more than anything else."},
            {"id": "lena_hospital",     "check": lambda: "hospital" in store.active_careers,
             "line": "I've noticed you around the hospital more. How are you finding it?"},
        ],
        "sam": [
            {"id": "sam_fitness_level", "check": lambda: skill_val("fit") >= 3,
             "line": "You've been putting in the work. It shows."},
            {"id": "sam_energy_low",    "check": lambda: store.need_energy < 30,
             "line": "Seriously, are you recovering properly between sessions?"},
        ],
    }

    def select_reactive_topic(npc_id):
        topics = NPC_REACTIVE_TOPICS.get(npc_id, [])
        available = []
        for t in topics:
            try:
                if not t["check"](): continue
            except Exception:
                continue
            last_used = max(
                (h.get("day", -99) for h in store.npc_encounter_history
                 if h.get("template_id") == "reactive_" + t["id"]),
                default=-99
            )
            if store.day - last_used < 5: continue
            available.append(t)
        if not available: return None
        import random as _r
        return _r.Random(store.day * 43 + _det_hash(npc_id) % 100).choice(available)

    def record_reactive_topic_used(npc_id, topic_id):
        store.npc_encounter_history = list(store.npc_encounter_history) + [{
            "npc_id": npc_id, "template_id": "reactive_" + topic_id,
            "day": store.day, "location_id": "",
        }]

    # ── 24I — Location first-visit tracking ──────────────────────────────────
    def record_location_visit(location_id):
        d = dict(store.location_visit_history)
        entry = dict(d.get(location_id, {"first_day": store.day, "last_day": -1, "count": 0}))
        is_first = entry["count"] == 0
        entry["last_day"] = store.day
        entry["count"] += 1
        d[location_id] = entry
        store.location_visit_history = d
        return is_first

    def location_visit_count(location_id):
        return store.location_visit_history.get(location_id, {}).get("count", 0)

    def location_long_absence(location_id, threshold_days=14):
        last = store.location_visit_history.get(location_id, {}).get("last_day", -1)
        return last >= 0 and store.day - last >= threshold_days

    # ── 24J — Living-world location-entry pipeline ────────────────────────────
    # Per-location config: which pipeline stages are active.
    LOCATION_LIVING_WORLD_RULES = {
        # Fully active
        "location_cafe":      {"invitations": True, "crossovers": True,  "ambient": True},
        "location_bar":       {"invitations": True, "crossovers": True,  "ambient": True},
        "location_park":      {"invitations": True, "crossovers": True,  "ambient": True},
        "location_gym":       {"invitations": True, "crossovers": True,  "ambient": True},
        "location_library":   {"invitations": True, "crossovers": True,  "ambient": True},
        "location_office":    {"invitations": True, "crossovers": True,  "ambient": True},
        "location_hub":       {"invitations": True, "crossovers": True,  "ambient": True},
        "location_hospital":  {"invitations": True, "crossovers": False, "ambient": True},
        "location_warehouse": {"invitations": True, "crossovers": False, "ambient": True},
        # Invitations only (no ambient/crossover content yet)
        "location_nightclub": {"invitations": True, "crossovers": False, "ambient": False},
        "location_diner":     {"invitations": True, "crossovers": False, "ambient": False},
        "location_sandbeach": {"invitations": True, "crossovers": False, "ambient": False},
        "location_college":   {"invitations": True, "crossovers": False, "ambient": False},
        # Excluded: routing hubs, shops, scripted-only
        # location_mall, location_centrum, location_cardealer, location_kitchen, etc.
    }

    def _lw_rules(location_id):
        return LOCATION_LIVING_WORLD_RULES.get(
            location_id, {"invitations": False, "crossovers": False, "ambient": False}
        )


    # Per-visit token: tracks which locations have already had living-world content
    # processed this visit. Reset on location change (not on menu refresh).
    # Format: {location_id: visit_token} where visit_token = day * 10000 + int(hour * 100)

    def _visit_token(location_id):
        return store.day * 10000 + int(store.hour * 100)

    def living_world_content_processed_for_visit(location_id):
        token = store._lw_visit_tokens.get(location_id, -1)
        return token == _visit_token(location_id)

    def mark_living_world_processed(location_id):
        d = dict(store._lw_visit_tokens)
        d[location_id] = _visit_token(location_id)
        store._lw_visit_tokens = d

    def can_process_living_world_content(location_id):
        if living_world_content_processed_for_visit(location_id):
            return False
        # Don't fire during active story commitments
        if getattr(store, "story_scene_active", False):
            return False
        return True

    def active_invitation_at_location(location_id, day_value=None, hour_value=None):
        """Returns the first accepted invitation active right now at this location, or None."""
        d = day_value if day_value is not None else store.day
        h = float(hour_value if hour_value is not None else store.hour)
        for inv in getattr(store, "active_npc_invitations", []):
            if inv.get("status") != "accepted": continue
            if inv.get("location") != location_id: continue
            if inv.get("proposed_day") != d: continue
            start = float(inv.get("start_hour", 0))
            end   = float(inv.get("end_hour", 0))
            if start <= h < end:
                return inv
        return None

    def process_location_entry(location_id):
        """
        Call this once at location entry, after story-scene checks.
        Returns ("invitation", inv), ("crossover", template), ("ambient", template), or None.
        Marks the visit so re-entry of the same screen doesn't retrigger.
        Per-location stage gating via LOCATION_LIVING_WORLD_RULES.
        """
        if not can_process_living_world_content(location_id):
            return None
        mark_living_world_processed(location_id)
        # Phase 67: location familiarity. Counted once per location per day,
        # regardless of how many times the screen is re-entered.
        record_location_visit(location_id)
        # Phase 68: "night owl" identity. One count per night, public places only.
        record_night_activity()
        rules = _lw_rules(location_id)
        # 1. Active invitation takes priority over everything
        if rules["invitations"]:
            inv = active_invitation_at_location(location_id)
            if inv:
                return ("invitation", inv)
        # ── Phase 67 ─────────────────────────────────────────────────────
        # These only READ world_pulse_data, which was generated at day start.
        # Nothing here generates events; see world_pulse.rpy.
        # 2. A major world event you have not yet walked into today.
        evt = active_world_event_at(location_id)
        if evt and not event_discovered(evt["id"]):
            return ("world_event", evt)
        # 3. Contextual core-NPC encounter (may require the event as context).
        enc = check_contextual_encounter(location_id)
        if enc:
            return ("contextual", enc)
        # 4. Minor incident, once per instance.
        inc = active_incident_at(location_id)
        if inc and not incident_already_seen(inc["id"]):
            return ("incident", inc)
        # ─────────────────────────────────────────────────────────────────
        # 5. Crossover
        if rules["crossovers"]:
            crossover = check_crossover(location_id)
            if crossover:
                return ("crossover", crossover)
        # 6. Ambient template
        if rules["ambient"]:
            ambient = check_location_ambient(location_id)
            if ambient:
                return ("ambient", ambient)
        # 7. Ambient local hanging around (lowest priority — pure texture).
        # Rare by design: presence is still shown passively in flavour text, only
        # the interrupting beat is gated. Strangers barely ever start something;
        # familiar faces a little more often. Plus a global multi-day gap.
        locals_here = ambient_npcs_here(location_id)
        if locals_here and store.day - store.last_ambient_modal_day >= 3:
            aid = locals_here[0]
            if renpy.random.random() < (0.025 if ambient_tier(aid) == "stranger" else 0.065):
                store.last_ambient_modal_day = store.day
                return ("ambient_local", aid)
        return None


# ── NPC crossover scene runner ────────────────────────────────────────────────
# Usage: $ _lw = process_location_entry(location_id)
#        if _lw and _lw[0] == "crossover": call run_crossover(_lw[1])
label run_crossover(template):
    $ _cx_text     = template["text"]
    $ _cx_choices  = template["choices"]
    $ _cx_c0_lbl   = _cx_choices[0][0]
    $ _cx_c1_lbl   = _cx_choices[1][0] if len(_cx_choices) > 1 else "Move on"
    "[_cx_text]"
    menu:
        "[_cx_c0_lbl]":
            $ _apply_crossover_rel_gain(_cx_choices[0][1])
            if _cx_choices[0][2] > 0:
                $ spend_time(_cx_choices[0][2])
        "[_cx_c1_lbl]":
            if len(_cx_choices) > 1:
                $ _apply_crossover_rel_gain(_cx_choices[1][1])
                if _cx_choices[1][2] > 0:
                    $ spend_time(_cx_choices[1][2])
    $ record_crossover(template["id"])
    return
