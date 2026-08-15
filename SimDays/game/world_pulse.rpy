# Phase 67 — Living world pulse.
#
# One generation pass per day, at day start, seeded so that reloading a save
# from the same day reproduces exactly the same world. Everything downstream
# (location entry, busking crowd, marketplace listings, bar attendance) only
# READS what this file produced — nothing generates on location entry.
#
# Relationship to the existing systems:
#   * city_events.rpy  — 3 scheduled events per WEEK, calendar-visible, attend
#                        by being there. Unchanged. World pulse is the daily
#                        layer underneath it.
#   * resolution_checks.daily_condition() — one global weather-ish modifier per
#                        day. Also unchanged; get_location_event_modifiers() is
#                        the per-LOCATION equivalent and the two stack.
#
# Locations used here are only ones that exist in LOCATION_DEFS. The brief's
# location_marketplace / location_downtown / location_workshop are not real
# travelable locations in this game — the marketplace is a phone app
# (marketplace.rpy) so its listing bonus is exposed as a global modifier under
# the pseudo-location "app_marketplace".

default world_pulse_data     = {}    # {day: pulse_dict}
default campaign_seed        = -1    # set once, first time the pulse runs
default _discovered_events   = {}    # {event_key: discovery_channel}
default _event_last_day      = {}    # {template_id: last day it ran} — cooldowns
default _incident_last_day   = {}    # {template_id: last day it ran}
default location_visits      = {}    # {location_id: meaningful visit count}
default _pulse_mail_today    = 0
default _pulse_social_today  = 0
default _pulse_budget_day    = -1
default _loc_visit_day       = {}    # {location_id: last day counted}
default _rare_opportunity_last = {}  # {opportunity_id: last day it fired}


init 1 python:

    # ── 67.2 Major event templates ───────────────────────────────────────────
    # day_weights: weekday index (0=Mon) -> weight. A weekday absent from the
    # map cannot host the event at all (this replaces the brief's "other": 0).
    WORLD_EVENT_TEMPLATES = {
        "art_market_park": {
            "name": "Local Art Market",
            "location": "location_park",
            "hours": (10, 18),
            "day_weights": {5: 3, 6: 2},
            "cooldown_days": 7,
            "npc_affinities": ["art"],
            "ambient_count": 3,
            "location_modifiers": {"social_density": 20, "art_reputation_gain": 1,
                                   "busking_crowd": 8},
            "announcement": {"mail": True, "social": True, "advance_days": 1},
            "aftermath": {"social": True},
            "blurb": "Stalls, canvases and a lot of opinions about framing.",
        },
        "bar_trivia_night": {
            "name": "Trivia Night",
            "location": "location_bar",
            "hours": (19, 23),
            "day_weights": {3: 2, 4: 3, 5: 2},
            "cooldown_days": 4,
            "npc_affinities": ["social", "bar_games"],
            "ambient_count": 2,
            "location_modifiers": {"bar_attendance": 25, "social_density": 15},
            "announcement": {"social": True, "advance_days": 1},
            "blurb": "Static runs a quiz. The regulars take it far too seriously.",
        },
        "gym_challenge": {
            "name": "Local Lifting Challenge",
            "location": "location_gym",
            "hours": (10, 16),
            "day_weights": {5: 3, 6: 2},
            "cooldown_days": 10,
            "npc_affinities": ["fitness"],
            "ambient_count": 2,
            "location_modifiers": {"fitness_event_bonus": 15, "social_density": 10},
            "announcement": {"mail": True, "social": True, "advance_days": 2},
            "blurb": "Iron Gate clears the floor for a one-day total.",
        },
        "park_busy_afternoon": {
            "name": "Busy Park Afternoon",
            "location": "location_park",
            "hours": (13, 19),
            "day_weights": {5: 2, 6: 2},
            "cooldown_days": 3,
            "npc_affinities": ["social"],
            "ambient_count": 2,
            "location_modifiers": {"social_density": 15, "busking_crowd": 12},
            "blurb": "Half the neighbourhood decided on the same idea.",
        },
        "library_workshop": {
            "name": "Community Code Workshop",
            "location": "location_library",
            "hours": (14, 19),
            "day_weights": {1: 2, 3: 2, 5: 1},
            "cooldown_days": 8,
            "npc_affinities": ["programming"],
            "ambient_count": 2,
            "location_modifiers": {"study_focus": 10},
            "announcement": {"social": True, "advance_days": 1},
            "blurb": "Laptops, extension cords, and somebody's home-made slides.",
        },
        "cafe_tasting": {
            "name": "Roastery Tasting",
            "location": "location_cafe",
            "hours": (11, 16),
            "day_weights": {2: 2, 5: 3},
            "cooldown_days": 9,
            "npc_affinities": ["cooking"],
            "ambient_count": 2,
            "location_modifiers": {"social_density": 18, "cafe_crowd": 10},
            "announcement": {"social": True, "advance_days": 1},
            "aftermath": {"social": True},
            "blurb": "Small cups, strong opinions, a visiting roaster.",
        },
        "hub_flea_market": {
            "name": "Hub Flea Market",
            "location": "location_hub",
            "hours": (9, 17),
            "day_weights": {5: 3, 6: 3},
            "cooldown_days": 5,
            "npc_affinities": ["mechanics", "shopping"],
            "ambient_count": 2,
            "location_modifiers": {"social_density": 12, "marketplace_listing_bonus": 2},
            "announcement": {"social": True, "advance_days": 1},
            "blurb": "Trestle tables of other people's abandoned projects.",
        },
        "beach_evening": {
            "name": "Beach Evening",
            "location": "location_sandbeach",
            "hours": (18, 23),
            "day_weights": {4: 2, 5: 3, 6: 1},
            "cooldown_days": 6,
            "npc_affinities": ["social", "music"],
            "ambient_count": 2,
            "location_modifiers": {"social_density": 22, "busking_crowd": 10},
            "announcement": {"social": True, "advance_days": 1},
            "blurb": "Somebody brought a speaker. Somebody else brought firewood.",
        },
    }

    # ── 67.3 Minor incident templates ────────────────────────────────────────
    # Incidents are flavour + 1-3 choices, no calendar footprint, no mail.
    LOCATION_INCIDENT_TEMPLATES = {
        "cafe_musician": {
            "location": "location_cafe", "name": "Local Musician",
            "weight": 20, "cooldown_days": 3, "hours": (14, 20),
            "intro": "A musician has set up a small acoustic set in the corner.",
            "actions": [
                {"label": "Listen for a bit", "outcome": ("mood", 4)},
                {"label": "Ask about local venues", "cond": "skill_music >= 30",
                 "outcome": ("music", 6)},
            ],
        },
        "cafe_crowded": {
            "location": "location_cafe", "name": "Unusually Busy",
            "weight": 15, "cooldown_days": 2, "hours": (12, 16),
            "intro": "The cafe is packed today. Finding a seat takes a moment.",
            "location_modifiers": {"social_density": 20, "cafe_crowd": 8},
            "actions": [{"label": "Find a spot", "outcome": ("none", 0)}],
        },
        "park_portrait_artist": {
            "location": "location_park", "name": "Street Portraits",
            "weight": 15, "cooldown_days": 4, "hours": (10, 17),
            "intro": "Someone is doing quick street portraits near the fountain.",
            "actions": [
                {"label": "Watch", "outcome": ("art", 4)},
                {"label": "Pose", "outcome": ("mood", 5)},
            ],
        },
        "bar_pool_argument": {
            "location": "location_bar", "name": "Pool Table Dispute",
            "weight": 20, "cooldown_days": 3, "hours": (19, 24),
            "intro": "Two regulars are deep in an argument about a pool shot.",
            "actions": [
                {"label": "Watch the drama", "outcome": ("mood", 3)},
                {"label": "Offer to referee", "outcome": ("chr", 4)},
            ],
        },
        "gym_trainer_demo": {
            "location": "location_gym", "name": "Trainer Demo",
            "weight": 15, "cooldown_days": 4, "hours": (10, 14),
            "intro": "A trainer is demonstrating a new routine near the free weights.",
            "actions": [
                {"label": "Watch", "outcome": ("fit", 3)},
                {"label": "Join in", "cond": "skill_fit >= 20", "outcome": ("fit", 7)},
            ],
        },
        "library_study_group": {
            "location": "location_library", "name": "Study Group",
            "weight": 15, "cooldown_days": 4, "hours": (13, 19),
            "intro": "A study group has taken over the long table, whispering furiously.",
            "location_modifiers": {"study_focus": 5},
            "actions": [{"label": "Join the edge of it", "outcome": ("int", 4)}],
        },
        "hub_pitch_practice": {
            "location": "location_hub", "name": "Pitch Practice",
            "weight": 12, "cooldown_days": 5, "hours": (11, 18),
            "intro": "Someone is rehearsing a pitch to an audience of two and a plant.",
            "actions": [
                {"label": "Listen", "outcome": ("biz", 4)},
                {"label": "Give honest feedback", "cond": "skill_biz >= 30",
                 "outcome": ("biz", 7)},
            ],
        },
        "park_lost_dog": {
            "location": "location_park", "name": "Lost Dog",
            "weight": 10, "cooldown_days": 6, "hours": (8, 20),
            "intro": "A very determined small dog is running loops with no owner in sight.",
            "actions": [{"label": "Help catch it", "outcome": ("mood", 6)}],
        },
    }

    # ── 67.12 Weekly rhythms ─────────────────────────────────────────────────
    # These are PROBABILITY BIASES, not guaranteed events: templates named here
    # get their weight multiplied on the matching weekday.
    WORLD_WEEKLY_RHYTHMS = {
        3: ["bar_trivia_night"],
        4: ["bar_trivia_night", "beach_evening"],
        5: ["park_busy_afternoon", "art_market_park", "hub_flea_market", "cafe_tasting"],
        6: ["park_busy_afternoon", "hub_flea_market"],
    }
    _RHYTHM_MULT = 2.0

    # Per-day budget. Deliberately small: the world should feel alive, not busy.
    PULSE_MAX_MAJOR_EVENTS   = 1
    PULSE_MAX_INCIDENTS      = 2
    PULSE_MAX_MAIL_PER_DAY   = 2
    PULSE_MAX_SOCIAL_PER_DAY = 3

    def _pulse_location_open(location_id):
        return is_location_unlocked(location_id)

    # ── Stable seeding ───────────────────────────────────────────────────────
    def _ensure_campaign_seed():
        if store.campaign_seed < 0:
            # Derived from the save's own start, not from wall-clock time, so a
            # replayed save regenerates identically.
            import time as _t
            store.campaign_seed = int(_t.time()) % 1000000
        return store.campaign_seed

    def _pulse_rng(day, salt=0):
        import random as _r
        return _r.Random(day * 100003 + _ensure_campaign_seed() + salt)

    def _stable_sample(candidates, max_count, day, event_id):
        """Deterministic weighted sample of (item, weight) pairs."""
        rng = _pulse_rng(day, salt=_det_hash(event_id) % 9973)
        pool = list(candidates)
        out = []
        while pool and len(out) < max_count:
            total = float(sum(max(0.01, w) for _, w in pool))
            pick = rng.random() * total
            for i, (item, w) in enumerate(pool):
                pick -= max(0.01, w)
                if pick <= 0:
                    out.append(item)
                    pool.pop(i)
                    break
            else:
                out.append(pool.pop()[0])
        return out

    # ── 67.1 Daily pulse ─────────────────────────────────────────────────────
    def generate_world_pulse(target_day):
        """Generate (once) the world events for target_day. Idempotent."""
        if target_day in store.world_pulse_data:
            return store.world_pulse_data[target_day]
        result = {"day": target_day, "major_events": [], "minor_incidents": [],
                  "generated": True}
        rng = _pulse_rng(target_day)
        wd = int(target_day) % 7

        # --- major events -----------------------------------------------------
        rhythm = WORLD_WEEKLY_RHYTHMS.get(wd, [])
        weighted = []
        for tid, t in WORLD_EVENT_TEMPLATES.items():
            w = t["day_weights"].get(wd, 0)
            if not w:
                continue
            last = store._event_last_day.get(tid, -999)
            if target_day - last < t["cooldown_days"]:
                continue
            if not _pulse_location_open(t["location"]):
                continue
            if tid in rhythm:
                w *= _RHYTHM_MULT
            weighted.append((tid, w))
        # Even on a busy Saturday the world is not guaranteed to do something.
        if weighted and rng.random() < _pulse_event_chance(wd):
            for tid in _stable_sample(weighted, PULSE_MAX_MAJOR_EVENTS,
                                      target_day, "major"):
                t = WORLD_EVENT_TEMPLATES[tid]
                evt = {"id": "%s_d%d" % (tid, target_day), "template_id": tid,
                       "name": t["name"], "location": t["location"],
                       "hours": list(t["hours"]), "day": target_day,
                       "blurb": t.get("blurb", ""),
                       "location_modifiers": dict(t.get("location_modifiers", {})),
                       "npcs": [], "resolved": False}
                evt["npcs"] = populate_event_npcs(t, evt, target_day)
                result["major_events"].append(evt)
                ld = dict(store._event_last_day); ld[tid] = target_day
                store._event_last_day = ld

        # --- minor incidents --------------------------------------------------
        inc_weighted = []
        for tid, t in LOCATION_INCIDENT_TEMPLATES.items():
            last = store._incident_last_day.get(tid, -999)
            if target_day - last < t["cooldown_days"]:
                continue
            if not _pulse_location_open(t["location"]):
                continue
            # Don't stack an incident on top of a major event at the same place.
            if any(e["location"] == t["location"] for e in result["major_events"]):
                continue
            inc_weighted.append((tid, t["weight"]))
        n_inc = 0
        if inc_weighted:
            n_inc = 1 if rng.random() < 0.55 else (2 if rng.random() < 0.25 else 0)
        for tid in _stable_sample(inc_weighted, min(n_inc, PULSE_MAX_INCIDENTS),
                                  target_day, "incident"):
            t = LOCATION_INCIDENT_TEMPLATES[tid]
            result["minor_incidents"].append({
                "id": "%s_d%d" % (tid, target_day), "template_id": tid,
                "location": t["location"], "name": t.get("name", tid),
                "hours": list(t["hours"]), "day": target_day,
                "intro": t["intro"],
                "location_modifiers": dict(t.get("location_modifiers", {})),
                "seen": False,
            })
            ld = dict(store._incident_last_day); ld[tid] = target_day
            store._incident_last_day = ld

        wp = dict(store.world_pulse_data)
        wp[target_day] = result
        # Keep the archive bounded — 30 days back is plenty for aftermath.
        for d in list(wp):
            if d < target_day - 30:
                del wp[d]
        store.world_pulse_data = wp
        return result

    def _pulse_event_chance(weekday):
        return 0.75 if weekday >= 5 else 0.35

    def world_pulse_today():
        return store.world_pulse_data.get(store.day, {"major_events": [],
                                                      "minor_incidents": []})

    # ── 67.4 Location modifiers ──────────────────────────────────────────────
    def _pulse_window_active(entry, hour=None):
        h = float(store.hour if hour is None else hour)
        h0, h1 = entry["hours"]
        return h0 <= h < h1

    def get_location_event_modifiers(location_id):
        """Every gameplay modifier active at this location right now.
        Busking, bar games, the marketplace app etc. call THIS — they never
        check event ids. Layers on top of daily_condition()."""
        mods = {}
        pulse = world_pulse_today()
        for evt in pulse.get("major_events", []):
            if evt["location"] == location_id and _pulse_window_active(evt):
                mods.update(evt.get("location_modifiers", {}))
        for inc in pulse.get("minor_incidents", []):
            if inc["location"] == location_id and _pulse_window_active(inc):
                for k, v in inc.get("location_modifiers", {}).items():
                    mods[k] = mods.get(k, 0) + v
        return mods

    def location_event_modifier(location_id, key, base=0):
        return base + get_location_event_modifiers(location_id).get(key, 0)

    def global_event_modifier(key, base=0):
        """For systems with no physical location (the marketplace phone app).
        Sums the key across every active event today."""
        total = base
        pulse = world_pulse_today()
        for evt in pulse.get("major_events", []) + pulse.get("minor_incidents", []):
            if _pulse_window_active(evt):
                total += evt.get("location_modifiers", {}).get(key, 0)
        return total

    def active_world_event_at(location_id, day=None, hour=None):
        d = store.day if day is None else day
        for evt in store.world_pulse_data.get(d, {}).get("major_events", []):
            if evt["location"] == location_id and _pulse_window_active(evt, hour):
                return evt
        return None

    def active_incident_at(location_id, day=None, hour=None):
        d = store.day if day is None else day
        for inc in store.world_pulse_data.get(d, {}).get("minor_incidents", []):
            if inc["location"] == location_id and _pulse_window_active(inc, hour):
                return inc
        return None

    def world_events_on_day(day):
        return store.world_pulse_data.get(day, {}).get("major_events", [])

    # ── 67.5 Discovery channels ──────────────────────────────────────────────
    def discover_event(event_id, channel):
        if event_id not in store._discovered_events:
            d = dict(store._discovered_events)
            d[event_id] = channel
            store._discovered_events = d

    def event_discovered(event_id):
        return event_id in store._discovered_events

    def known_upcoming_events(days_ahead=3):
        """Events the player has actually heard about — for the calendar/phone."""
        out = []
        for d in range(store.day, store.day + days_ahead + 1):
            for e in world_events_on_day(d):
                if event_discovered(e["id"]):
                    out.append(e)
        return out

    # ── 67.6 Announcements + aftermath ───────────────────────────────────────
    def _pulse_budget_reset():
        if store._pulse_budget_day != store.day:
            store._pulse_budget_day = store.day
            store._pulse_mail_today = 0
            store._pulse_social_today = 0

    def _pulse_can_mail():
        _pulse_budget_reset()
        return store._pulse_mail_today < PULSE_MAX_MAIL_PER_DAY

    def _pulse_can_social():
        _pulse_budget_reset()
        return store._pulse_social_today < PULSE_MAX_SOCIAL_PER_DAY

    def _pulse_social_post(post_id, text, npc_id="cityfeed"):
        if not _pulse_can_social():
            return False
        if any(p.get("id") == post_id for p in store.social_feed_posts):
            return False
        store.social_feed_posts = [{"id": post_id, "npc_id": npc_id,
                                    "text": text, "day": store.day}] + list(store.social_feed_posts)
        store._pulse_social_today += 1
        return True

    def announce_world_events(current_day):
        """Deliver mail/social for events happening in the next few days.
        Runs at day start, respects the 2-mail / 3-post daily budget."""
        for ahead in (1, 2):
            target = current_day + ahead
            generate_world_pulse(target)
            for evt in world_events_on_day(target):
                t = WORLD_EVENT_TEMPLATES.get(evt["template_id"], {})
                ann = t.get("announcement")
                if not ann or ann.get("advance_days", 1) != ahead:
                    continue
                if ann.get("mail") and _pulse_can_mail():
                    tag = "wpulse_mail_" + evt["id"]
                    if not mail_already_queued(tag):
                        queue_mail("City Events Board", evt["name"],
                                   "%s\n\n%s, %02d:00-%02d:00, in %d day%s."
                                   % (evt.get("blurb", ""),
                                      LOCATION_DEFS.get(evt["location"], {}).get(
                                          "display_name", evt["location"]),
                                      evt["hours"][0], evt["hours"][1],
                                      ahead, "" if ahead == 1 else "s"),
                                   "city", current_day, tag)
                        store._pulse_mail_today += 1
                        discover_event(evt["id"], "mail")
                if ann.get("social"):
                    if _pulse_social_post("wpulse_soc_" + evt["id"],
                                          "%s — %s. %s" % (evt["name"],
                                                           "tomorrow" if ahead == 1 else "in two days",
                                                           evt.get("blurb", ""))):
                        discover_event(evt["id"], "social")

    def resolve_world_event_aftermath(current_day):
        """Yesterday's events get a closing social post (once)."""
        for evt in world_events_on_day(current_day - 1):
            if evt.get("resolved"):
                continue
            evt["resolved"] = True
            t = WORLD_EVENT_TEMPLATES.get(evt["template_id"], {})
            if t.get("aftermath", {}).get("social"):
                _pulse_social_post("wpulse_after_" + evt["id"],
                                   "%s wrapped up yesterday. Bigger turnout than expected."
                                   % evt["name"])

    # ── 67.7 NPC event population ────────────────────────────────────────────
    # Maps event affinity tags to the Phase 65 NPC_INTERESTS domains. Tags with
    # no domain equivalent ("social", "shopping", "bar_games") fall back to a
    # flat baseline so sociable NPCs can still show up.
    _AFFINITY_DOMAIN = {"art": "art", "music": "music", "fitness": "fitness",
                        "programming": "programming", "cooking": "cooking",
                        "mechanics": "mechanics", "food": "cooking"}
    _SOCIAL_TAGS = frozenset(("social", "shopping", "bar_games", "nightlife"))

    def _npc_available_for_event(npc_id, template, target_day):
        if not npc_known(npc_id):
            return False
        if npc_is_temporarily_unavailable(npc_id):
            return False
        if NPC_DATA.get(npc_id, {}).get("no_decay"):
            return False   # mentor NPCs live entirely inside their arcs
        h0, h1 = template["hours"]
        # Don't pull an NPC out of a shift they are contracted to.
        state = resolve_npc_state(npc_id, day=target_day, hour=(h0 + h1) / 2.0)
        if state["activity_id"] in ("working_shift", "working_overtime", "commuting"):
            return False
        # Don't collide with a commitment the player already has with them.
        for o in store.npc_schedule_overrides:
            if o["npc_id"] == npc_id and o["day"] == target_day:
                return False
        return True

    def _event_affinity_score(npc_id, affinities):
        best = 0
        for a in affinities:
            dom = _AFFINITY_DOMAIN.get(a)
            if dom:
                best = max(best, npc_interest(npc_id, dom))
            elif a in _SOCIAL_TAGS:
                # Sociability proxy: the Phase 66 profile, not a new table.
                best = max(best, int(round(npc_rel_profile(npc_id)["openness"] * 2)))
        return best

    def populate_event_npcs(template, event, target_day):
        """Pick up to 3 attending NPCs and pin them there with schedule
        overrides, using the existing npc_schedules.rpy mechanism."""
        affinities = template.get("npc_affinities") or []
        if not affinities:
            return []
        candidates = []
        for npc_id in NPC_DATA:
            if not _npc_available_for_event(npc_id, template, target_day):
                continue
            score = _event_affinity_score(npc_id, affinities)
            if score > 0:
                candidates.append((npc_id, score))
        if not candidates:
            return []
        selected = _stable_sample(candidates, 3, target_day, event["id"])
        h0, h1 = template["hours"]
        for npc_id in selected:
            add_schedule_override(
                npc_id=npc_id, day=target_day,
                hour_start=h0, hour_end=min(h1, h0 + 4),
                location_id=template["location"], activity_id="socializing",
                public=True, interactable=True,
                source_id="wpulse_" + event["id"],
                expires_day=target_day + 1)
        return selected

    # ── 67.13 Location familiarity ───────────────────────────────────────────
    # "Meaningful" = one count per location per day, not per screen refresh.
    def record_location_visit(location_id):
        # One count per location per day. Uses its own map rather than
        # _lw_visit_tokens, which location_ambient.rpy resets every new_day()
        # and keys per-visit-hour.
        if store._loc_visit_day.get(location_id) == store.day:
            return
        d = dict(store._loc_visit_day); d[location_id] = store.day
        store._loc_visit_day = d
        v = dict(store.location_visits)
        v[location_id] = v.get(location_id, 0) + 1
        store.location_visits = v

    def location_familiarity_tier(location_id):
        n = store.location_visits.get(location_id, 0)
        if n >= 15: return "regular"     # ambient locals recognise you by name
        if n >= 5:  return "known_face"  # staff nod
        return "new"

    def location_recognition_line(location_id):
        tier = location_familiarity_tier(location_id)
        if tier == "regular":
            return "The staff start your usual before you reach the counter."
        if tier == "known_face":
            return "You get a nod on the way in."
        return ""

    # ── 67.11 Rare opportunity leads ─────────────────────────────────────────
    # These NEVER pay out directly — they send mail that unlocks a normal,
    # already-balanced opportunity. See the economy note in
    # tests/phase67_selfcheck.py.
    RARE_OPPORTUNITY_TEMPLATES = {
        "cafe_freelance_lead": {
            "activity": "programming_session", "location": "location_cafe",
            "min_skill": ("prog", 4), "chance": 0.03, "cooldown_days": 14,
            "sender": "R. Vance",
            "subject": "Saw you working at the cafe",
            "body": "You looked like you knew what you were doing. We have a "
                    "small piece of work if you want to talk about it. "
                    "Check the freelance board this week.",
        },
        "busking_venue_contact": {
            "activity": "busking", "min_skill": ("guitar", 5),
            "min_reputation": ("music_reputation", 15),
            "chance": 0.04, "cooldown_days": 14,
            "sender": "The Anchor",
            "subject": "Heard you in the park",
            "body": "We book short sets on weeknights. If you want a slot, "
                    "come find us — the open mic is the usual way in.",
        },
        "art_market_commission": {
            "activity": "art_market_participation",
            "min_reputation": ("art_reputation", 8),
            "chance": 0.15, "cooldown_days": 21,
            "sender": "Private buyer",
            "subject": "About the piece at the market",
            "body": "I would like something similar, but mine. The commission "
                    "board is the right place to arrange it.",
        },
    }

    def maybe_rare_opportunity(activity_id, location_id=None):
        """Call at the END of a relevant activity. At most one lead per call and
        never more than the daily mail budget allows."""
        for oid, t in RARE_OPPORTUNITY_TEMPLATES.items():
            if t["activity"] != activity_id:
                continue
            if t.get("location") and location_id != t["location"]:
                continue
            last = store._rare_opportunity_last.get(oid, -999)
            if store.day - last < t["cooldown_days"]:
                continue
            if "min_skill" in t:
                sk, lvl = t["min_skill"]
                if getattr(store, "skill_" + sk, 0) < lvl:
                    continue
            if "min_reputation" in t:
                var, lvl = t["min_reputation"]
                if getattr(store, var, 0) < lvl:
                    continue
            if renpy.random.random() > t["chance"]:
                continue
            if not _pulse_can_mail():
                continue
            tag = "rare_opp_%s_d%d" % (oid, store.day)
            if mail_already_queued(tag):
                continue
            queue_mail(t["sender"], t["subject"], t["body"], "opportunity",
                       store.day, tag)
            store._pulse_mail_today += 1
            d = dict(store._rare_opportunity_last); d[oid] = store.day
            store._rare_opportunity_last = d
            renpy.notify("New mail — %s" % t["subject"])
            return oid
        return None

    # ── Day-start entry point ────────────────────────────────────────────────
    def process_world_pulse_day():
        """Called once from new_day(). Everything heavy happens here."""
        _pulse_budget_reset()
        resolve_world_event_aftermath(store.day)
        generate_world_pulse(store.day)
        announce_world_events(store.day)

