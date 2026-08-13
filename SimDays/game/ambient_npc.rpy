# Phase 67 — ambient locals, minor incidents and contextual core-NPC encounters.
#
# Ambient locals are NOT relationship NPCs: they have no affection/trust, no
# schedule entries and no NPC_DATA record. They exist so that a location has
# faces in it, and so that repeated visits are recognised. All they track is a
# familiarity counter that changes what they say.
#
# Presence is DETERMINISTIC for a given (day, hour-band, location) so re-entering
# the same screen never reshuffles who is there — the Phase 67 performance rule.

default _ambient_familiarity  = {}   # {ambient_id: int}
default _ambient_met          = []   # ambient ids the player has actually spoken to
default _ambient_last_talk    = {}   # {ambient_id: day}
default _encounter_last_day   = {}   # {encounter_id: day}
default _incident_resolved    = []   # incident instance ids already played
# ponytail: one global counter, not per-location/per-ambient — generic locals are
# texture, so a single shared gap is enough. Upgrade to {location_id: day} if a
# per-place rhythm is ever wanted.
default last_ambient_modal_day = -99  # day a generic ambient-local modal last fired


init 1 python:

    # ── 67.8 Ambient locals ──────────────────────────────────────────────────
    AMBIENT_NPC = {
        "darren": {
            "name": "Darren", "locations": ["location_bar"], "hours": (18, 24),
            "interests": ["bar_games", "music"], "event_affinities": ["bar_trivia_night"],
            "blurb": "a man who has clearly owned that barstool for years",
        },
        "maya": {
            "name": "Maya", "locations": ["location_park"], "hours": (10, 18),
            "interests": ["art"], "event_affinities": ["art_market_park"],
            "blurb": "someone sketching with more confidence than technique",
        },
        "chris": {
            "name": "Chris", "locations": ["location_gym"], "hours": (7, 12),
            "interests": ["fitness"], "event_affinities": ["gym_challenge"],
            "blurb": "a lifter who racks his plates without being asked",
        },
        "rachel": {
            "name": "Rachel", "locations": ["location_cafe"], "hours": (8, 12),
            "interests": ["cooking", "books"], "event_affinities": ["cafe_tasting"],
            "blurb": "a woman with the same window seat every morning",
        },
        "ben": {
            "name": "Ben", "locations": ["location_library", "location_cafe"], "hours": (13, 19),
            "interests": ["programming"], "event_affinities": ["library_workshop"],
            "blurb": "someone typing far too fast to be writing prose",
        },
        "tony": {
            "name": "Tony", "locations": ["location_hub"], "hours": (10, 16),
            "interests": ["mechanics"], "event_affinities": ["hub_flea_market"],
            "blurb": "a man surrounded by parts of something that used to work",
        },
        "priya": {
            "name": "Priya", "locations": ["location_library"], "hours": (9, 15),
            "interests": ["books"], "event_affinities": [],
            "blurb": "a librarian who reshelves while walking",
        },
        "oskar_j": {
            "name": "Oskar", "locations": ["location_bar"], "hours": (20, 26),
            "interests": ["music"], "event_affinities": ["bar_trivia_night"],
            "blurb": "the guy who always knows what's playing",
        },
        "dee": {
            "name": "Dee", "locations": ["location_cafe", "location_park"], "hours": (12, 18),
            "interests": ["social"], "event_affinities": ["park_busy_afternoon"],
            "blurb": "someone who seems to know everyone by first name",
        },
        "hana": {
            "name": "Hana", "locations": ["location_sandbeach"], "hours": (16, 22),
            "interests": ["music", "social"], "event_affinities": ["beach_evening"],
            "blurb": "a swimmer who never seems to be cold",
        },
        "vic": {
            "name": "Vic", "locations": ["location_gym"], "hours": (17, 21),
            "interests": ["fitness"], "event_affinities": ["gym_challenge"],
            "blurb": "the evening regular with a laminated programme",
        },
        "sonia": {
            "name": "Sonia", "locations": ["location_hub"], "hours": (11, 18),
            "interests": ["programming", "social"], "event_affinities": ["library_workshop"],
            "blurb": "someone running a whiteboard session for an audience of one",
        },
    }

    def ambient_familiarity(aid):
        return store._ambient_familiarity.get(aid, 0)

    def ambient_tier(aid):
        f = ambient_familiarity(aid)
        if f >= 6: return "regular"
        if f >= 3: return "recognized"
        return "stranger"

    def _bump_ambient_familiarity(aid, amount=1):
        d = dict(store._ambient_familiarity)
        d[aid] = min(20, d.get(aid, 0) + amount)
        store._ambient_familiarity = d
        if aid not in store._ambient_met:
            store._ambient_met = list(store._ambient_met) + [aid]

    def _ambient_hour_band(hour=None):
        h = float(store.hour if hour is None else hour)
        return int(h) // 4          # six 4-hour bands per day

    def ambient_npcs_here(location_id=None, day=None, hour=None):
        """Deterministic list of ambient locals at this location in this
        4-hour band. Same inputs -> same answer, so re-entering the screen never
        reshuffles the room. At most 2, usually 0-1."""
        loc = location_id if location_id is not None else store.current_loc
        d = store.day if day is None else day
        band = _ambient_hour_band(hour)
        h = float(store.hour if hour is None else hour)
        pool = []
        for aid, a in AMBIENT_NPC.items():
            if loc not in a["locations"]:
                continue
            h0, h1 = a["hours"]
            # Windows may run past midnight (hours >= 24).
            if not (h0 <= h < h1 or (h1 > 24 and h + 24 < h1 and h < h0)):
                continue
            pool.append(aid)
        if not pool:
            return []
        import random as _r
        rng = _r.Random(d * 7717 + band * 131 + _det_hash(loc) % 9973
                        + _ensure_campaign_seed())
        rng.shuffle(pool)
        # Familiar faces are more likely to be around than never-seen ones —
        # this is what makes a location feel like it has regulars.
        out = []
        for aid in pool:
            p = 0.35 + 0.06 * ambient_familiarity(aid)
            # An event at this location fills the place up.
            evt = active_world_event_at(loc, d, hour)
            if evt and evt["template_id"] in AMBIENT_NPC[aid]["event_affinities"]:
                p += 0.4
            if rng.random() < min(0.9, p):
                out.append(aid)
            if len(out) >= 2:
                break
        return out

    def ambient_present_text(aid):
        a = AMBIENT_NPC[aid]
        tier = ambient_tier(aid)
        if tier == "regular":
            return "%s is here. He nods before you've finished walking in." % a["name"] \
                if aid in ("darren", "chris", "ben", "tony", "oskar_j", "vic") else \
                "%s is here. She waves you over without looking up." % a["name"]
        if tier == "recognized":
            return "%s is here again — %s." % (a["name"], a["blurb"])
        return "There's %s." % a["blurb"]

    # ── 67.10 Contextual core-NPC encounters ─────────────────────────────────
    # These are chance meetings with real NPCs OUTSIDE their schedule, gated on
    # familiarity so a stranger never gets a personal moment.
    CONTEXTUAL_NPC_ENCOUNTERS = {
        "eli_hub_laptop": {
            "npc": "eli", "location": "location_hub", "event_context": None,
            "weight": 15, "cooldown_days": 10, "familiarity_min": 15,
            "hours": (10, 18),
            "intro": "Eli is squinting at an absurdly old laptop someone has handed her.",
            "label": "eli_encounter_hub",
        },
        "marcus_bar_pool": {
            "npc": "marcus", "location": "location_bar",
            "weight": 15, "cooldown_days": 8, "familiarity_min": 20,
            "hours": (19, 24),
            "intro": "Marcus waves you over to the pool table.",
            "label": "marcus_encounter_bar_pool",
        },
        "zoe_art_market": {
            "npc": "zoe", "location": "location_park",
            "event_context": "art_market_park",
            "weight": 25, "cooldown_days": 14, "familiarity_min": 10,
            "hours": (10, 18),
            "intro": "Zoe is arguing with a vendor about canvas quality.",
            "label": "zoe_encounter_art_market",
        },
        "nora_cafe_busy": {
            "npc": "nora", "location": "location_cafe",
            "incident_context": "cafe_crowded",
            "weight": 20, "cooldown_days": 5, "familiarity_min": 0,
            "hours": (12, 16),
            "intro": "Nora gives you an apologetic look from behind the counter.",
            "label": "nora_encounter_busy",
        },
        "sam_gym_challenge": {
            "npc": "sam", "location": "location_gym",
            "event_context": "gym_challenge",
            "weight": 20, "cooldown_days": 12, "familiarity_min": 15,
            "hours": (10, 16),
            "intro": "Sam is by the board, reading the day's totals with a flat expression.",
            "label": "sam_encounter_challenge",
        },
    }

    def check_contextual_encounter(location_id):
        """Reads pre-computed pulse state only. Returns an encounter dict or None."""
        evt = active_world_event_at(location_id)
        inc = active_incident_at(location_id)
        h = float(store.hour)
        candidates = []
        for eid, e in CONTEXTUAL_NPC_ENCOUNTERS.items():
            if e["location"] != location_id:
                continue
            h0, h1 = e.get("hours", (0, 24))
            if not (h0 <= h < h1):
                continue
            if store.day - store._encounter_last_day.get(eid, -999) < e["cooldown_days"]:
                continue
            npc = e["npc"]
            if not npc_known(npc):
                continue
            if npc_rel(npc, "familiarity") < e.get("familiarity_min", 0):
                continue
            # Don't double up on an NPC who is already scheduled to be here.
            if npc_here(npc, location_id):
                continue
            ctx = e.get("event_context")
            if ctx and not (evt and evt["template_id"] == ctx):
                continue
            ictx = e.get("incident_context")
            if ictx and not (inc and inc["template_id"] == ictx):
                continue
            candidates.append((eid, e["weight"]))
        if not candidates:
            return None
        total = float(sum(w for _, w in candidates))
        # ~1 in 4 qualifying visits actually produce an encounter.
        if renpy.random.random() > min(0.30, total / 100.0):
            return None
        pick = renpy.random.random() * total
        for eid, w in candidates:
            pick -= w
            if pick <= 0:
                d = dict(store._encounter_last_day); d[eid] = store.day
                store._encounter_last_day = d
                return dict(CONTEXTUAL_NPC_ENCOUNTERS[eid], id=eid)
        return None

    # ── Incident outcome application ─────────────────────────────────────────
    _INCIDENT_SKILLS = {"music", "art", "fit", "biz", "prog", "cook", "mech", "int", "chr"}

    def apply_incident_outcome(kind, amount):
        if kind == "none" or not amount:
            return ""
        if kind == "mood":
            store.need_energy = min(100, store.need_energy + amount)
            return "+%d Energy" % amount
        if kind in ("int", "chr", "str", "app"):
            setattr(store, "stat_" + kind,
                    min(100, getattr(store, "stat_" + kind, 0) + max(1, amount // 2)))
            return "+%d %s" % (max(1, amount // 2), kind.upper())
        if kind in _INCIDENT_SKILLS:
            gain_skill_practice(kind, amount, hours=0)
            return "+%d %s XP" % (amount, kind)
        return ""

    def incident_actions_available(incident):
        t = LOCATION_INCIDENT_TEMPLATES.get(incident["template_id"], {})
        out = []
        for a in t.get("actions", []):
            cond = a.get("cond")
            if cond:
                try:
                    if not eval(cond, {"__builtins__": {}}, vars(store)):
                        continue
                except Exception:
                    continue
            out.append(a)
        return out

    def mark_incident_seen(incident_id):
        if incident_id not in store._incident_resolved:
            store._incident_resolved = list(store._incident_resolved) + [incident_id]

    def incident_already_seen(incident_id):
        return incident_id in store._incident_resolved


# ── Runner labels ─────────────────────────────────────────────────────────────
# process_location_entry() returns a tag; locations.rpy calls the matching label.

label run_world_event_arrival(evt):
    $ discover_event(evt["id"], "location")
    $ _wp_name = evt["name"]
    $ _wp_blurb = evt.get("blurb", "")
    "[_wp_name] — [_wp_blurb]"
    if evt["npcs"]:
        $ _wp_names = ", ".join(NPC_DATA[n]["name"] for n in evt["npcs"] if n in NPC_DATA)
        "You spot [_wp_names] in the crowd."
    return

label run_location_incident(inc):
    $ mark_incident_seen(inc["id"])
    $ _inc_intro = inc["intro"]
    "[_inc_intro]"
    $ _inc_acts = incident_actions_available(inc)
    if not _inc_acts:
        return
    $ _inc_labels = [a["label"] for a in _inc_acts] + ["Leave it"]
    $ _inc_pick = renpy.display_menu([(l, i) for i, l in enumerate(_inc_labels)])
    if _inc_pick >= len(_inc_acts):
        return
    $ _inc_kind, _inc_amt = _inc_acts[_inc_pick]["outcome"]
    $ _inc_result = apply_incident_outcome(_inc_kind, _inc_amt)
    if _inc_result:
        "([_inc_result])"
    return

label run_ambient_local(aid):
    $ _amb_name = AMBIENT_NPC[aid]["name"]
    $ _amb_tier = ambient_tier(aid)
    $ _amb_intro = ambient_present_text(aid)
    "[_amb_intro]"
    if _amb_tier == "stranger":
        "You don't know them. They're just here, the way people are."
        menu:
            "Say hello":
                $ _bump_ambient_familiarity(aid)
                "\"Hey.\" A short nod back. That's the whole exchange, and it's fine."
            "Leave them to it":
                pass
    elif _amb_tier == "recognized":
        "You've seen [_amb_name] enough times now that not saying anything would be odd."
        menu:
            "Chat for a minute":
                $ _bump_ambient_familiarity(aid)
                $ _amb_tip = _ambient_tip_line(aid)
                "[_amb_tip]"
            "Just a nod":
                $ _bump_ambient_familiarity(aid, 0)
    else:
        "\"There you are,\" [_amb_name] says, like you were expected."
        menu:
            "Catch up":
                $ _bump_ambient_familiarity(aid)
                $ _amb_tip = _ambient_tip_line(aid)
                "[_amb_tip]"
            "Not today":
                pass
    return


init 1 python:
    # Regulars pass on what's coming up — this is a DISCOVERY CHANNEL, not a
    # reward. It marks a future event as known so it shows on the phone.
    def _ambient_tip_line(aid):
        a = AMBIENT_NPC[aid]
        for ahead in (1, 2, 3):
            for evt in world_events_on_day(store.day + ahead):
                if evt["template_id"] in a["event_affinities"] and not event_discovered(evt["id"]):
                    discover_event(evt["id"], "ambient")
                    return ("\"You know there's %s here %s? Worth a look.\""
                            % (evt["name"], "tomorrow" if ahead == 1 else "in a few days"))
        tier = ambient_tier(aid)
        if tier == "regular":
            return "\"Same as ever. Which is the point, mostly.\""
        return "\"Not much going on. Quiet week.\""


# ── 67.10 Core NPC encounter scenes ───────────────────────────────────────────

label run_contextual_encounter(enc):
    # Canonical focused presentation — see "FOCUSED SPRITE CONTRACT" in images.rpy.
    # Clear the public location slots first: these encounters used to show a raw
    # `at center` sprite (no SPRITE_SCALE, no y-offset) on a `npcs` tag that sat
    # alongside whoever the location had already rendered.
    $ clear_npc_sprites()
    $ _enc_npc = enc["npc"]
    $ _enc_intro = enc["intro"]
    "[_enc_intro]"
    call expression enc["label"] from _call_ctx_encounter
    return

label eli_encounter_hub:
    show expression npc_sprite("eli") as focus_eli at sprite_crop(sprite_display_scale("eli"), _SPRITE_XP_R, sprite_display_y_offset("eli"))
    eli "Someone donated this to the club. It boots. That is the whole of its good news."
    menu:
        "Offer to help":
            $ apply_relationship_change("eli", "encounter_hub_help", "helping_npc",
                                        trust=2, respect=2, familiarity=2)
            eli "Hold the case open. Don't let it close on my hand again."
            "Twenty minutes later it has a working fan and a slightly different problem."
        "Ask why she bothers":
            $ apply_relationship_change("eli", "encounter_hub_ask", "meaningful_talk",
                                        affection=1, familiarity=2, meaningful=True)
            eli "Because someone will use it. That's usually enough of a reason."
    hide focus_eli
    return

label marcus_encounter_bar_pool:
    show expression npc_sprite("marcus", "evening") as focus_marcus at sprite_crop(sprite_display_scale("marcus"), _SPRITE_XP_R, sprite_display_y_offset("marcus"))
    m "You're just in time to lose at something."
    menu:
        "Play a frame":
            $ rel_shared_activity("marcus", "encounter_bar_pool", affection=2, trust=1, familiarity=3)
            "You lose. He is unbearable about it for exactly one minute, then buys the next round."
        "Just watch":
            $ rel_casual_talk("marcus", "encounter_bar_pool_watch", affection=1, familiarity=2)
            m "Fine. But you're calling the shots then."
    hide focus_marcus
    return

label zoe_encounter_art_market:
    show expression npc_sprite("zoe") as focus_zoe at sprite_crop(sprite_display_scale("zoe"), _SPRITE_XP_R, sprite_display_y_offset("zoe"))
    z "He's selling primed board as canvas. At canvas prices."
    menu:
        "Back her up":
            $ apply_relationship_change("zoe", "encounter_art_market_back", "shared_activity",
                                        affection=2, trust=2, familiarity=3)
            z "See, that's why I like having you around. Witnesses."
        "Suggest she let it go":
            $ apply_relationship_change("zoe", "encounter_art_market_calm", "casual_talk",
                                        affection=1, familiarity=2)
            z "I will. In a minute. After he admits it."
    hide focus_zoe
    return

label nora_encounter_busy:
    show expression npc_sprite("nora", "work") as focus_nora at sprite_crop(sprite_display_scale("nora"), _SPRITE_XP_R, sprite_display_y_offset("nora"))
    n "Two minutes. Or forty. I genuinely can't tell yet."
    menu:
        "Wait it out":
            $ apply_relationship_change("nora", "encounter_busy_wait", "kept_commitment",
                                        affection=2, trust=2, familiarity=2, meaningful=True)
            "You wait. When the queue finally breaks she puts a coffee down in front of you without being asked."
        "Come back later":
            $ rel_casual_talk("nora", "encounter_busy_leave", affection=0, familiarity=1)
            n "Smart. Go on."
    hide focus_nora
    return

label sam_encounter_challenge:
    show expression npc_sprite("sam") as focus_sam at sprite_crop(sprite_display_scale("sam"), _SPRITE_XP_R, sprite_display_y_offset("sam"))
    sam "Half of these are going to hurt themselves for a number on a whiteboard."
    menu:
        "Ask what she'd do differently":
            $ apply_relationship_change("sam", "encounter_challenge_ask", "meaningful_talk",
                                        trust=2, respect=2, familiarity=2, meaningful=True)
            sam "Publish the programme, not the total. Nobody would come."
        "Point out she's still here":
            $ apply_relationship_change("sam", "encounter_challenge_tease", "casual_talk",
                                        affection=2, familiarity=2)
            sam "...Someone has to spot them."
    hide focus_sam
    return


# Single dispatcher for the Phase 67 living-world kinds, so the 13 location
# entry blocks in locations.rpy each needed only one generic `else:` branch.
label run_living_world_extra(kind, payload):
    if kind == "world_event":
        call run_world_event_arrival(payload)
    elif kind == "contextual":
        call run_contextual_encounter(payload)
    elif kind == "incident":
        call run_location_incident(payload)
    elif kind == "ambient_local":
        call run_ambient_local(payload)
    return
