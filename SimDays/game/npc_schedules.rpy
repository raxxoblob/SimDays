# NPC 24-hour schedule system (Section 23) + world reactivity helpers (Section 24A, 24B).
# resolve_npc_state() is the single source of truth for "where is NPC X right now".
# MON_FRI / WKD / FRISUN / MON_SAT are defined in interact.rpy and available here.

init python:

    # ── Home location IDs ─────────────────────────────────────────────────────
    NPC_HOME_LOCATIONS = {
        "nora":     "loc_nora_apt",
        "marcus":   "loc_marcus_apt",
        "zoe":      "loc_zoe_studio",
        "eli":      "loc_eli_dorm",
        "sam":      "loc_sam_house",
        "lena":     "loc_lena_apt",
        "natalie":  "loc_natalie_house",
        "kai":      "loc_kai_apt",
        "martha":   "loc_martha_apt",
        "caroline": "loc_caroline_apt",
        "rena":     "loc_rena_place",
        "elle":     "loc_elle_apt",
        # julia: planned future NPC — no active content yet; removed to avoid ghost schedule entries
    }

    # ── Activity definitions ──────────────────────────────────────────────────
    ACTIVITY_DEFS = {
        "commuting":         {"display": "Commuting",          "depth": "unavailable"},
        "working_shift":     {"display": "Working",            "depth": "brief"},
        "working_overtime":  {"display": "Working (overtime)", "depth": "brief"},
        "studying":          {"display": "Studying",           "depth": "brief"},
        "exercising":        {"display": "Exercising",         "depth": "brief"},
        "socializing":       {"display": "Socializing",        "depth": "full"},
        "relaxing_at_home":  {"display": "At home",            "depth": "unavailable"},
        "sleeping":          {"display": "Sleeping",           "depth": "unavailable"},
        "running":           {"display": "Running",            "depth": "brief"},
        "browsing":          {"display": "Browsing",           "depth": "full"},
        "eating_out":        {"display": "Eating out",         "depth": "full"},
        "lingering":         {"display": "Hanging around",     "depth": "full"},
    }

    # ── Full 24/7 schedules ───────────────────────────────────────────────────
    # (day_set, (h_start, h_end), location_id, activity_id, public, interactable)
    # Home fallback handles anything not listed.
    NPC_FULL_SCHEDULES = {
        "nora": [
            # Mon-Fri commute in
            (MON_FRI, (6,  7),  "city_transit",  "commuting",       False, False),
            # Mon-Fri working at café — brief interaction allowed
            (MON_FRI, (7,  15), "location_cafe", "working_shift",   True,  True),
            # Tue post-shift lingering at café — listed before commute so it takes priority
            ({1},     (15, 17), "location_cafe", "lingering",       True,  True),
            # Mon-Fri commute home (Tue: only fires outside the 15-17 lingering window)
            (MON_FRI, (15, 16), "city_transit",  "commuting",       False, False),
            # Wed wind-down at park
            ({2},     (19, 22), "location_park", "socializing",     True,  True),
            # Thu wind-down at bar
            ({3},     (19, 22), "location_bar",  "socializing",     True,  True),
            # Weekend shifts
            (WKD,     (10, 18), "location_cafe", "working_shift",   True,  True),
        ],
        "marcus": [
            # Mon-Fri morning park jog
            (MON_FRI, (7,  11), "location_park", "running",         True,  True),
            # Tue café stop — listed before Mon-Fri commute/bar so it takes priority at h=15-16
            ({1},     (15, 17), "location_cafe", "eating_out",      True,  True),
            # Mon-Fri commute to bar (Tue: only fires at h=14, which is before the café window)
            (MON_FRI, (14, 16), "city_transit",  "commuting",       False, False),
            # Mon-Fri managing the bar
            (MON_FRI, (16, 24), "location_bar",  "working_shift",   True,  True),
            # Weekend bar shift (15-27, spans past midnight)
            (WKD,     (15, 27), "location_bar",  "working_shift",   True,  True),
        ],
        "zoe": [
            # Mon-Fri classes at The Hub
            (MON_FRI, (9,  13), "location_hub",  "studying",        True,  True),
            # Wed afternoon café
            ({2},     (13, 18), "location_cafe", "browsing",        True,  True),
            # Thu-Fri afternoon park
            ({3, 4},  (14, 18), "location_park", "socializing",     True,  True),
            # Weekend daytime beach
            (WKD,     (12, 18), "location_sandbeach", "socializing", True,  True),
            # Saturday night bar
            ({5},     (19, 24), "location_bar",  "socializing",     True,  True),
        ],
        "eli": [
            # Mon-Fri classes
            (MON_FRI, (9,  12), "location_hub",     "studying",     True,  True),
            # Mon-Fri library
            (MON_FRI, (12, 18), "location_library", "studying",     True,  True),
            # Sat library
            ({5},     (10, 16), "location_library", "studying",     True,  True),
        ],
        "sam": [
            # Mon-Wed-Fri working at gym
            ({0, 2, 4}, (6,  14), "location_gym",  "working_shift", True,  True),
            # Tue-Thu morning park run
            ({1, 3},    (7,  9),  "location_park", "running",       True,  True),
            # Sat morning gym class
            ({5},       (8,  13), "location_gym",  "working_shift", True,  True),
        ],
        "lena": [
            # Mon-Fri hospital shift
            (MON_FRI, (7,  16), "location_hospital", "working_shift", True,  True),
            # Mon-Fri commute
            (MON_FRI, (16, 18), "city_transit",       "commuting",    False, False),
            # Sat half-day
            ({5},     (8,  14), "location_hospital", "working_shift", True,  True),
        ],
        "natalie": [
            # Mon-Fri warehouse
            (MON_FRI, (8,  17), "location_warehouse", "working_shift", True,  True),
            # Mon-Fri commute + errands
            (MON_FRI, (17, 19), "city_transit",        "commuting",    False, False),
        ],
        "kai": [
            # Mon-Fri gym
            (MON_FRI, (8,  16), "location_gym",  "working_shift",  True,  True),
            # Weekend gym
            (WKD,     (9,  14), "location_gym",  "working_shift",  True,  True),
            # Fri-Sat late bar
            ({4, 5},  (20, 27), "location_bar",  "socializing",    True,  True),
        ],
        "martha": [
            # Mon-Fri office
            (MON_FRI, (8,  17), "location_office", "working_shift", True,  True),
            # Thu bar networking
            ({3},     (18, 21), "location_bar",    "socializing",   True,  True),
        ],
        "caroline": [
            # Mon-Fri office
            (MON_FRI, (9,  17), "location_office", "working_shift", True,  True),
            # Fri bar
            ({4},     (18, 22), "location_bar",    "socializing",   True,  True),
        ],
        "rena": [
            # Mon-Fri alternate hub/office
            ({0, 2, 4}, (9, 17), "location_hub",    "working_shift", True,  True),
            ({1, 3},    (9, 17), "location_office", "working_shift", True,  True),
            # Sat park then café
            ({5},       (9, 13), "location_park",   "socializing",   True,  True),
            ({5},       (13,17), "location_cafe",   "browsing",      True,  True),
            # Mon/Wed late-night diner (21-02); suppressed by rena_diner_absent_until_day
            ({0, 2},    (21,26), "location_diner",  "lingering",     True,  True),
        ],
        # Elle — creative/travel type, no regular job
        "elle": [
            # Tue/Thu café browsing
            ({1, 3},    (9,  13), "location_cafe",      "browsing",    True, True),
            # Mon/Wed/Fri morning park
            ({0, 2, 4}, (10, 14), "location_park",      "socializing", True, True),
            # Wed afternoon sandbeach (legacy sched carried forward)
            ({2},       (16, 19), "location_sandbeach", "socializing", True, True),
            # Fri afternoon beach (elle_pier_scene trigger zone)
            ({4},       (14, 18), "location_beach",     "socializing", True, True),
            # Weekend sandbeach afternoon (legacy sched carried forward)
            (WKD,       (13, 18), "location_sandbeach", "socializing", True, True),
            # Weekend nightclub late (legacy sched: 21-25 = 21-01)
            (WKD,       (21, 25), "location_nightclub", "socializing", True, True),
        ],
        # julia: planned future NPC — no active content yet; schedule stub removed
    }

    # ── Core resolver ─────────────────────────────────────────────────────────
    def resolve_npc_state(npc_id, day=None, hour=None):
        """
        Returns a dict:
          location_id, activity_id, public (bool), interactable (bool)
        Never returns None.
        """
        if day  is None: day  = store.day
        if hour is None: hour = store.hour
        h  = float(hour)
        dw = int(day) % 7

        # 1. Check schedule overrides
        for ov in store.npc_schedule_overrides:
            if ov["npc_id"] != npc_id: continue
            if ov["day"] != day: continue
            if not (ov["hour_start"] <= h < ov["hour_end"]): continue
            return {
                "location_id":  ov["location_id"],
                "activity_id":  ov["activity_id"],
                "public":       ov.get("public", True),
                "interactable": ov.get("interactable", True),
            }

        # 2. Walk NPC_FULL_SCHEDULES
        for entry in NPC_FULL_SCHEDULES.get(npc_id, []):
            days_set, hr_range, loc_id, act_id, pub, interact = entry
            if days_set is not None and dw not in days_set: continue
            if not (hr_range[0] <= h < hr_range[1]): continue
            # Per-NPC story-driven suppression: Rena absent from diner after culinary crisis
            if npc_id == "rena" and loc_id == "location_diner":
                if int(day) < getattr(store, "rena_diner_absent_until_day", 0):
                    continue
            return {"location_id": loc_id, "activity_id": act_id,
                    "public": pub, "interactable": interact}

        # 3. Fall back to legacy NPC_DATA["sched"] entries (3-tuple, public+interactable=True)
        try:
            sched = npc_schedule_entries(npc_id)
        except Exception:
            sched = NPC_DATA.get(npc_id, {}).get("sched")
        if sched:
            for entry in sched:
                days_set = entry[0]
                hr_range  = entry[1]
                loc_id    = entry[2] if len(entry) > 2 else None
                if days_set is not None and dw not in days_set: continue
                if not (hr_range[0] <= h < hr_range[1]): continue
                if loc_id:
                    return {"location_id": loc_id, "activity_id": "working_shift",
                            "public": True, "interactable": True}

        # 4. Home fallback
        home = NPC_HOME_LOCATIONS.get(npc_id, "location_home")
        return {"location_id": home, "activity_id": "relaxing_at_home",
                "public": False, "interactable": False}

    # ── Presence / visibility / interactability helpers (Task 2) ─────────────
    def npc_is_present(npc_id, location_id=None):
        """Physical presence only — ignores public/interactable."""
        state = resolve_npc_state(npc_id)
        if location_id is None:
            return True
        return state["location_id"] == location_id

    def npc_is_publicly_visible(npc_id):
        """True when the NPC is at a public location and not hiding."""
        return resolve_npc_state(npc_id)["public"]

    def npc_is_interactable(npc_id):
        """True when the NPC is public and willing to talk."""
        state = resolve_npc_state(npc_id)
        return state["public"] and state["interactable"]

    def npc_here(npc_id, location_id=None):
        """Used in location screens: NPC is present, publicly visible, and interactable.
        If location_id is None, uses store.current_loc.
        Overrides the legacy version in interact.rpy (npc_schedules.rpy loads after)."""
        if npc_is_temporarily_unavailable(npc_id):
            return False
        state = resolve_npc_state(npc_id)
        loc = location_id if location_id is not None else store.current_loc
        return (state["location_id"] == loc
                and state["public"]
                and state["interactable"])

    # ── Interaction depth ─────────────────────────────────────────────────────
    def npc_interaction_depth(npc_id):
        state = resolve_npc_state(npc_id)
        act = state.get("activity_id", "relaxing_at_home")
        if not state.get("public"):       return "unavailable"
        if not state.get("interactable"): return "ambient_only"
        return ACTIVITY_DEFS.get(act, {}).get("depth", "full")

    def npc_public_location_now(npc_id):
        s = resolve_npc_state(npc_id)
        return s["location_id"] if s["public"] else None

    def npc_location_now(npc_id):
        return resolve_npc_state(npc_id)["location_id"]

    def npc_public_availability_text(npc_id):
        state = resolve_npc_state(npc_id)
        if not state.get("public"):
            h = int(store.hour)
            if h >= 22 or h < 7:
                return "Likely home for the evening."
            return "Currently unavailable."
        if not state.get("interactable"):
            return "Around but busy right now."
        loc = state["location_id"]
        try:
            info = store.LOCATION_DEFS.get(loc, {})
        except Exception:
            info = {}
        # Never expose raw private location IDs
        if info.get("private"):
            return "At home."
        display = info.get("display_name",
                           loc.replace("location_", "").replace("_", " ").title())
        return "At %s." % display

    # ── Override management ───────────────────────────────────────────────────
    def add_schedule_override(npc_id, day, hour_start, hour_end, location_id,
                              activity_id, public=True, interactable=True,
                              expires_day=None, source_id=None):
        """Add a schedule override. Deduplicates by (npc_id, source_id) when
        source_id is provided so reload can't double-add the same override."""
        if source_id is not None:
            for o in store.npc_schedule_overrides:
                if o["npc_id"] == npc_id and o.get("source_id") == source_id:
                    return  # already present, skip
        entry = {
            "npc_id": npc_id, "day": day,
            "hour_start": hour_start, "hour_end": hour_end,
            "location_id": location_id, "activity_id": activity_id,
            "public": public, "interactable": interactable,
            "expires_day": expires_day if expires_day is not None else day,
        }
        if source_id is not None:
            entry["source_id"] = source_id
        store.npc_schedule_overrides = list(store.npc_schedule_overrides) + [entry]

    def npc_has_override_overlap(npc_id, day, start_hour, end_hour):
        """True when npc_id already has an override on `day` whose window
        [hour_start, hour_end) overlaps [start_hour, end_hour).
        Half-open: 17-20 and 20-22 do NOT overlap.
        Needed because resolve_npc_state() is first-match-wins — a later
        override inserted over an earlier one is silently shadowed.
        ponytail: linear scan over all overrides. The list is a handful of
        entries (they self-expire daily), so no index is worth keeping."""
        for ov in store.npc_schedule_overrides:
            if ov.get("npc_id") != npc_id:
                continue
            if ov.get("day") != day:
                continue
            if start_hour < ov.get("hour_end", 24) and end_hour > ov.get("hour_start", 0):
                return True
        return False

    def _expire_schedule_overrides():
        """Remove overrides whose expires_day is in the past. Called from new_day()."""
        store.npc_schedule_overrides = [
            o for o in store.npc_schedule_overrides
            if o.get("expires_day", 9999) >= store.day
        ]

    def clear_schedule_overrides(npc_id=None, day=None):
        """Remove overrides where ALL active filters match (intersection).
        - npc_id only  → removes all overrides for that NPC (any day)
        - day only     → removes all overrides for that day (any NPC)
        - both         → removes only entries where npc_id AND day both match
        - neither      → raises ValueError (never wipes everything silently)
        """
        if npc_id is None and day is None:
            raise ValueError("clear_schedule_overrides: must supply npc_id, day, or both")
        store.npc_schedule_overrides = [
            o for o in store.npc_schedule_overrides
            if not (
                (npc_id is None or o["npc_id"] == npc_id)
                and (day is None or o["day"] == day)
            )
        ]

    # ── Section 24A — activity flavor text ───────────────────────────────────
    def npc_activity_flavor_text(npc_id, activity_id):
        lines = {
            ("nora",   "working_shift"): "Nora is on shift. She gives you a quick look but doesn't stop.",
            ("marcus", "working_shift"): "Marcus is behind the bar. He nods but keeps moving.",
            ("zoe",    "studying"):      "Zoe has her sketchbook out. She's focused.",
            ("eli",    "studying"):      "Eli's headphones are on. You'd have to tap her shoulder.",
            ("sam",    "exercising"):    "Sam is mid-set. She holds up one finger — give her a minute.",
            ("kai",    "exercising"):    "Kai is with a client. Not the moment.",
            ("lena",   "working_shift"): "Lena is in consultation. You'll have to wait.",
        }
        return lines.get((npc_id, activity_id), "")

    # ── Section 24B — NPC short-term memory ──────────────────────────────────
    # Canonical definition — interact.rpy's earlier stub is replaced by this one.
    def add_relationship_memory(npc_id, memory_id, summary,
                                category="general", visibility="private",
                                day_value=None, metadata=None):
        key = npc_id + "_memories"
        memories = list(getattr(store, key, []))
        # Skip exact duplicate IDs
        if any(m["id"] == memory_id for m in memories):
            return
        memories.append({
            "id":         memory_id,
            "summary":    summary,
            "category":   category,
            "visibility": visibility,
            "day":        day_value if day_value is not None else store.day,
            "referenced": False,
            "metadata":   metadata or {},
        })
        setattr(store, key, memories)

    def has_relationship_memory(npc_id, memory_id):
        return any(m["id"] == memory_id for m in getattr(store, npc_id + "_memories", []))

    def recent_relationship_memories(npc_id, days=7):
        cutoff = store.day - days
        return [m for m in getattr(store, npc_id + "_memories", []) if m["day"] >= cutoff]

    def mark_memory_referenced(npc_id, memory_id):
        key = npc_id + "_memories"
        memories = list(getattr(store, key, []))
        for m in memories:
            if m["id"] == memory_id: m["referenced"] = True
        setattr(store, key, memories)

    def npc_can_know_event(npc_id, event):
        vis = event.get("visibility", "private")
        if vis == "public": return True
        if vis == "contacts": return getattr(store, npc_id + "_met", False)
        return False


# ── Debug screen: NPC schedule inspector ─────────────────────────────────────
screen debug_schedule_scr():
    modal True
    zorder 260
    add "#000000e0"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 960
        ysize 900
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 10
            hbox:
                text "NPC SCHEDULES" font PROFILE_FONT size 26 color "#ffdd44" yalign 0.5
                textbutton "✕ Close" action Hide("debug_schedule_scr") xalign 1.0 text_size 18 text_color "#9fb6d6"
            text "Day [store.day] ([DAY_NAMES[store.day % 7]])  Hour [store.hour:.1f]" size 15 color "#8aaecc"
            null height 4
            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 820
                xfill True
                vbox:
                    spacing 8
                    xsize 900
                    for _nid in ["nora","marcus","zoe","eli","sam","lena","natalie","kai","martha","caroline","rena"]:
                        python:
                            _st  = resolve_npc_state(_nid)
                            _dep = npc_interaction_depth(_nid)
                        frame:
                            background "#1e2530"
                            padding (12, 8, 12, 8)
                            xfill True
                            hbox:
                                spacing 12
                                text "[_nid]" font PROFILE_FONT size 16 color "#ffd66a" xsize 120 yalign 0.5
                                vbox:
                                    spacing 2
                                    text "loc: [_st['location_id']]  act: [_st['activity_id']]" size 14 color "#cfe0f5"
                                    text "public=[_st['public']]  interact=[_st['interactable']]  depth=[_dep]" size 13 color "#8aaecc"
