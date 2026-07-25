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
        # -- Ambient events -------------------------------------------------
        "metro_delay": {
            "type":         "ambient",
            "label":        "wevent_metro_delay",
            "locations":    ["location_hub", "location_hospital"],
            "min_day":      3,
            "once":         False,
            "priority":     1,
            "cooldown":     5,
            "weight":       0.30,
        },
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
        return store.wed_ambient_today.get(location) or None

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


# ── Personal event: Marcus loan ───────────────────────────────────────────

label wevent_marcus_loan:
    # Narrative eligibility check — structural eligibility was confirmed by the WED poll.
    if not marcus_met or marcus_trust < 20 or wed_marcus_loan_state != "none":
        return
    $ wed_fire("marcus_loan")
    $ wed_marcus_loan_state = "offered"
    show marcus_casual_normal at sprite_r
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
    show sam_normal at sprite_r
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
    hide sam_normal
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
                jump take_metro
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
                jump take_metro
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
    show marcus_casual_normal at sprite_r
    m "Hey. The $120 — here."
    "He hands it back without ceremony."
    m "Appreciate it. Seriously."
    $ gain_money(120)
    $ _apply_trust("marcus", 2)
    $ wed_marcus_loan_state = "resolved_repaid"
    hide marcus_casual_normal
    return

label wevcb_marcus_loan_partial:
    show marcus_casual_normal at sprite_r
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
    hide marcus_casual_normal
    return

label wevcb_marcus_loan_solved:
    show marcus_casual_normal at sprite_r
    m "Sorted it out, by the way. Just so you know."
    "He doesn't make it into a thing."
    $ _apply_trust("marcus", 1)
    $ wed_marcus_loan_state = "resolved_solved"
    hide marcus_casual_normal
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
    show marcus_casual_normal at sprite_r

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
    show marcus_casual_normal at sprite_r
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
