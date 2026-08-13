# Phase 68 — NPC initiative, personal lives, follow-ups, word of mouth, identity.
#
# This LAYERS ON the initiative system already in phone_actionable.rpy
# (_check_npc_initiative + _INITIATIVE_MSGS + npc_initiative_last_global_day).
# That system already enforces "one unprompted NPC message per day" and picks a
# sender by texting tier and social trait — rebuilding it would be pure churn.
# Phase 68 adds the things it does not do:
#
#   * personal-life states that change how often an NPC reaches out and how
#     available they are (68.3)
#   * event invitations that reference a REAL Phase 67 world event (68.2)
#   * NPC-initiated cancellations, rate-limited and penalty-free (68.4)
#   * a delayed follow-up queue so reactions land days later (68.5)
#   * public facts propagating by word of mouth, respect only (68.6)
#   * soft player identity flags (68.7)
#   * failure-response content (68.8)
#
# EVERY channel above shares one daily budget with the existing initiative
# system: at most ONE unprompted NPC contact per day. See _initiative_budget().

default _initiative_evaluated_day = -1
default _npc_personal_life        = {}   # {npc_id: {"state","expires_day","started_day"}}
default _npc_life_history         = {}   # {npc_id: last state} — avoids immediate repeats
default _followup_queue           = []
default _followup_last_day        = -1
default public_player_facts       = {}   # {fact_id: {...}}
default _player_identity_flags    = {}
default _npc_cancel_last_day      = {}   # {npc_id: day} — max one per NPC per week
default _failure_content_last     = {}   # {trigger: day}
default _nights_active            = 0    # public locations after 22:00
default _p68_contact_day          = -1   # which day the shared contact budget was spent
default _npc_initiative_cooldowns = {}   # {npc_id: last day THIS system contacted you}
default _p68_night_day            = -1   # last day a late-night visit was counted


init 1 python:

    # ── 68.3 Personal life states ────────────────────────────────────────────
    NPC_PERSONAL_LIFE_STATES = {
        "busy_work":        {"duration_range": (2, 5), "availability_modifier": -0.30,
                             "initiative_modifier": 0.7, "dialogue_tags": ["tired", "busy"],
                             "blurb": "buried in work"},
        "creative_project": {"duration_range": (3, 7), "availability_modifier": 0.0,
                             "initiative_modifier": 1.5, "dialogue_tags": ["excited", "focused"],
                             "blurb": "deep in something they made up themselves"},
        "social_week":      {"duration_range": (3, 5), "availability_modifier": 0.20,
                             "initiative_modifier": 1.5, "dialogue_tags": ["social", "energetic"],
                             "blurb": "out more than usual"},
        "stressed_week":    {"duration_range": (2, 4), "availability_modifier": -0.40,
                             "initiative_modifier": 0.3, "dialogue_tags": ["stressed", "withdrawn"],
                             "blurb": "having a rough stretch"},
        "recovering":       {"duration_range": (1, 3), "availability_modifier": -0.50,
                             "initiative_modifier": 0.4, "dialogue_tags": ["tired", "low_energy"],
                             "blurb": "run down"},
        "training_focus":   {"duration_range": (3, 6), "availability_modifier": -0.10,
                             "initiative_modifier": 1.0, "dialogue_tags": ["focused", "determined"],
                             "blurb": "mid-programme and protective of it"},
        "planning_something": {"duration_range": (2, 4), "availability_modifier": 0.0,
                             "initiative_modifier": 1.8, "dialogue_tags": ["mysterious", "excited"],
                             "blurb": "working up to telling you something"},
    }

    # Weights come from the Phase 66 characterisation audit. An NPC only gets a
    # state that their scenes actually support — Rena, for example, has no
    # "social_week" because nothing in culinary_arc.rpy suggests one.
    NPC_PERSONAL_LIFE_WEIGHTS = {
        # 6am runs every day incl. weekends (arcs.rpy:176), money tight to
        # payday (world_events.rpy:854), runs a bar most evenings.
        "marcus":   {"training_focus": 25, "social_week": 20, "busy_work": 12,
                     "stressed_week": 8},
        # Months on one harbour series, gallery arc, day job with a beige client
        # (home_scenes.rpy:236). Creative project is her default mode.
        "zoe":      {"creative_project": 30, "planning_something": 15,
                     "busy_work": 10, "stressed_week": 10},
        # Deploys + on-call (it_arc.rpy:136) plus a thesis chapter she is
        # avoiding (arcs.rpy:229).
        "eli":      {"busy_work": 25, "creative_project": 15, "stressed_week": 12,
                     "recovering": 8},
        # Five years of shifts, a night pastry course, a September intake
        # decision (arcs.rpy:119, :149).
        "nora":     {"busy_work": 18, "planning_something": 14, "social_week": 12,
                     "recovering": 8},
        # Rigid programme, tracks rest days "like they're debts"
        # (world_events.rpy:2505); one missed session destabilised her (:917).
        "sam":      {"training_focus": 30, "recovering": 10, "busy_work": 10,
                     "stressed_week": 8},
        # Full client book, drained by performing energy
        # (gameplay_expansion_scenes.rpy:1206).
        "kai":      {"busy_work": 20, "social_week": 22, "recovering": 12,
                     "training_focus": 10},
        # 16-hour shifts (gameplay_expansion_scenes.rpy:228), carries hard cases
        # home (hospital_arc.rpy:155).
        "lena":     {"busy_work": 30, "stressed_week": 15, "recovering": 12},
        # Warehouse shifts plus coaching three nights a week (:1158).
        "natalie":  {"busy_work": 25, "training_focus": 20, "recovering": 8},
        # Six years in and ambivalent (corporate_arc.rpy:252), buried in the
        # Meridian account (corporate_atlas.rpy:70).
        "martha":   {"busy_work": 30, "stressed_week": 15, "planning_something": 8},
        # Owns client pitches and board deadlines (corporate_atlas.rpy:15).
        "caroline": {"busy_work": 32, "stressed_week": 14},
        # 18-month Portugal post she keeps circling (arcs.rpy:265, :283).
        "elle":     {"planning_something": 25, "social_week": 15, "busy_work": 10},
        # Service-shaped and constant. Deliberately no social/creative states.
        "rena":     {"busy_work": 35, "recovering": 8},
    }

    def npc_personal_life(npc_id):
        rec = store._npc_personal_life.get(npc_id)
        if rec and rec.get("expires_day", -1) >= store.day:
            return rec
        return None

    def npc_life_state(npc_id):
        rec = npc_personal_life(npc_id)
        return rec["state"] if rec else None

    def npc_life_tags(npc_id):
        st = npc_life_state(npc_id)
        return NPC_PERSONAL_LIFE_STATES.get(st, {}).get("dialogue_tags", [])

    def npc_availability_modifier(npc_id):
        st = npc_life_state(npc_id)
        return NPC_PERSONAL_LIFE_STATES.get(st, {}).get("availability_modifier", 0.0)

    def npc_initiative_modifier(npc_id):
        st = npc_life_state(npc_id)
        return NPC_PERSONAL_LIFE_STATES.get(st, {}).get("initiative_modifier", 1.0)

    def _roll_personal_life(npc_id, current_day):
        weights = NPC_PERSONAL_LIFE_WEIGHTS.get(npc_id)
        if not weights:
            return
        import random as _r
        rng = _r.Random(current_day * 8837 + _det_hash(npc_id) % 9973
                        + _ensure_campaign_seed())
        # Most days an NPC is simply having a normal week.
        if rng.random() > 0.18:
            return
        last = store._npc_life_history.get(npc_id)
        pool = [(s, w) for s, w in weights.items() if s != last] or list(weights.items())
        total = float(sum(w for _, w in pool))
        pick = rng.random() * total
        chosen = pool[-1][0]
        for s, w in pool:
            pick -= w
            if pick <= 0:
                chosen = s
                break
        lo, hi = NPC_PERSONAL_LIFE_STATES[chosen]["duration_range"]
        life = dict(store._npc_personal_life)
        life[npc_id] = {"state": chosen, "started_day": current_day,
                        "expires_day": current_day + rng.randint(lo, hi)}
        store._npc_personal_life = life
        hist = dict(store._npc_life_history); hist[npc_id] = chosen
        store._npc_life_history = hist

    def _expire_personal_lives(current_day):
        store._npc_personal_life = {
            k: v for k, v in store._npc_personal_life.items()
            if v.get("expires_day", -1) >= current_day}

    # ── Shared daily contact budget ──────────────────────────────────────────
    # The existing _check_npc_initiative() sets npc_initiative_last_global_day
    # when it fires. Phase 68's channels check the SAME day marker, so the
    # player never gets an initiative text, a follow-up and an event invite on
    # the same morning.
    def _initiative_budget_spent():
        return (store.npc_initiative_last_global_day >= store.day
                or store._p68_contact_day >= store.day)

    def _spend_initiative_budget():
        store._p68_contact_day = store.day

    # ── 68.2 Event invitations (the Phase 67 <-> 68 bridge) ──────────────────
    _EVENT_INVITE_LINES = {
        "marcus":  "There's %s on tomorrow. I'm going either way. Come if you want.",
        "nora":    "%s tomorrow. I'm going after my shift — say if you want company.",
        "zoe":     "%s is tomorrow. I need someone to stop me buying things.",
        "eli":     "%s tomorrow. I'll be there for the first hour at least.",
        "sam":     "%s tomorrow. Bring water.",
        "kai":     "%s tomorrow! Tell me you're coming.",
        "elle":    "%s tomorrow — I'd like it if you were there.",
        "natalie": "%s tomorrow, if you're around.",
        "lena":    "There's %s tomorrow. I get out at six.",
        "martha":  "%s is tomorrow. I intend to be there for exactly one hour.",
        "caroline":"%s tomorrow. I am told attendance is good for one's profile.",
    }

    def _try_event_invite(current_day):
        """An NPC attending tomorrow's world event invites the player to it."""
        target = current_day + 1
        for evt in world_events_on_day(target):
            for npc_id in evt.get("npcs", []):
                if npc_id not in _EVENT_INVITE_LINES:
                    continue
                if npc_rel(npc_id, "familiarity") < 25:
                    continue
                if current_day - store._npc_initiative_cooldowns.get(npc_id, -999) < 5:
                    continue
                chance = (invitation_acceptance_chance(npc_id, "casual")
                          * npc_initiative_modifier(npc_id))
                if renpy.random.random() > min(0.8, chance):
                    continue
                tag = "p68_evt_inv_%s_%s" % (npc_id, evt["id"])
                if message_already_queued(tag):
                    continue
                line = _EVENT_INVITE_LINES[npc_id] % evt["name"]
                queue_phone_message(npc_id, line, current_day, tag)
                deliver_message_now(tag)
                discover_event(evt["id"], "npc")
                add_calendar_event(title="%s — %s" % (NPC_DATA[npc_id]["name"], evt["name"]),
                                   day=target, hour=evt["hours"][0],
                                   duration=min(3, evt["hours"][1] - evt["hours"][0]),
                                   category="social", commitment=False, npc_id=npc_id)
                cd = dict(store._npc_initiative_cooldowns)
                cd[npc_id] = current_day
                store._npc_initiative_cooldowns = cd
                return True
        return False

    # ── 68.4 NPC-initiated plan changes ──────────────────────────────────────
    _CANCEL_LINES = {
        "busy_work":     "Something's landed at work and it isn't moving. I have to bail on tomorrow. Sorry.",
        "stressed_week": "I'm going to be bad company tomorrow. Can we push it? I'd rather see you when I'm actually there.",
        "recovering":    "I'm wrecked. If I come tomorrow I'll just be asleep at the table. Rain check?",
        "training_focus":"I've got a session tomorrow I can't move. Different day?",
        None:            "Something's come up for tomorrow. Sorry — my fault, not yours.",
    }

    def maybe_npc_cancellation(npc_id, commitment):
        """Called at day start for each upcoming commitment. Returns a dict or
        None. The player NEVER takes a trust hit for an NPC cancelling."""
        if commitment.get("authored"):
            return None                        # major story beats are immune
        if store.day - store._npc_cancel_last_day.get(npc_id, -999) < 7:
            return None                        # max one per NPC per week
        hours_away = (commitment["day"] - store.day) * 24 + (commitment["hour"] - store.hour)
        if hours_away < 1:
            return None                        # too late to cancel politely
        profile = npc_rel_profile(npc_id)
        state = npc_life_state(npc_id)
        chance = 0.04
        chance += max(0.0, -npc_availability_modifier(npc_id)) * 0.15
        chance += profile["boundary_strength"] * 0.03
        # People who have shown up for you a lot cancel less.
        chance *= max(0.4, 1.0 - npc_rel(npc_id, "trust") / 250.0)
        if renpy.random.random() > chance:
            return None
        d = dict(store._npc_cancel_last_day); d[npc_id] = store.day
        store._npc_cancel_last_day = d
        return {"type": "cancel", "message": _CANCEL_LINES.get(state, _CANCEL_LINES[None])}

    def _process_npc_cancellations(current_day):
        for c in list(store.player_commitments):
            if c.get("completed") or c.get("missed") or c.get("cancelled"):
                continue
            if c["day"] != current_day + 1:
                continue                        # only tomorrow's plans
            npc_id = c.get("npc_id")
            if not npc_id or npc_id not in NPC_DATA:
                continue
            res = maybe_npc_cancellation(npc_id, c)
            if not res:
                continue
            c["cancelled"] = True
            c["cancelled_by_npc"] = True
            queue_phone_message(npc_id, res["message"], current_day,
                                "p68_npc_cancel_" + c["id"])
            deliver_message_now("p68_npc_cancel_" + c["id"])
            # No trust penalty for the player. A small familiarity bump because
            # they bothered to tell you.
            apply_relationship_change(npc_id, "npc_cancel", "casual_talk",
                                      familiarity=1, bypass_saturation=True)
            return True
        return False

    # ── 68.5 Follow-up queue ─────────────────────────────────────────────────
    FOLLOWUP_TEMPLATES = {
        "generic_thanks":     "Thanks again for the other day. I meant to say it at the time.",
        "generic_comment":    "Been thinking about what you said. Still chewing on it.",
        "generic_checkin":    "You've been quiet. All fine?",
        "challenge_win":      "Heard you won that thing. Obviously you did.",
        "promotion":          "Congratulations on the promotion. Don't let it change your coffee order.",
        "performance":        "Somebody said you played. Why did I hear it from somebody?",
        "encourage_setback":  "Heard it didn't go your way. It happens to everyone who actually tries things.",
    }

    def enqueue_followup(npc_id, followup_type, trigger_source, template,
                         delay_min=1, delay_max=3, priority=5, conditions=None):
        fid = "fu_%s_%s_d%d" % (npc_id, trigger_source, store.day)
        if any(f["id"] == fid for f in store._followup_queue):
            return None
        store._followup_queue = list(store._followup_queue) + [{
            "id": fid, "npc_id": npc_id, "type": followup_type,
            "trigger_source": trigger_source,
            "eligible_from_day": store.day + delay_min,
            "eligible_until_day": store.day + delay_max + 1,
            "priority": priority, "conditions": conditions or {},
            "completed": False, "template": template,
        }]
        return fid

    def process_followup_queue(current_day):
        """At most one follow-up delivered per day, highest priority first,
        oldest first inside a priority band. Expired entries are dropped."""
        q = [f for f in store._followup_queue
             if not f["completed"] and f["eligible_until_day"] >= current_day]
        ready = [f for f in q if f["eligible_from_day"] <= current_day
                 and npc_known(f["npc_id"])]
        store._followup_queue = q
        if not ready or store._followup_last_day >= current_day:
            return None
        ready.sort(key=lambda f: (-f["priority"], f["eligible_from_day"], f["id"]))
        f = ready[0]
        text = FOLLOWUP_TEMPLATES.get(f["template"], FOLLOWUP_TEMPLATES["generic_comment"])
        queue_phone_message(f["npc_id"], text, current_day, "p68_" + f["id"])
        deliver_message_now("p68_" + f["id"])
        f["completed"] = True
        store._followup_queue = [dict(x) if x["id"] != f["id"] else f
                                 for x in store._followup_queue]
        store._followup_last_day = current_day
        return f["id"]

    # ── 68.6 Public facts / word of mouth ────────────────────────────────────
    PUBLIC_FACT_TEMPLATES = {
        "won_city_challenge": {"max_npcs": 3, "propagation_delay": 1,
                               "affects": {"respect": 3},
                               "dialogue_tag": "knows_won_challenge",
                               "followup_template": "challenge_win"},
        "got_promoted":       {"max_npcs": 2, "propagation_delay": 1,
                               "affects": {"respect": 2},
                               "dialogue_tag": "knows_promotion",
                               "followup_template": "promotion"},
        "public_performance": {"max_npcs": 4, "propagation_delay": 1,
                               "affects": {"respect": 2, "affection": 1},
                               "dialogue_tag": "saw_performance",
                               "followup_template": "performance"},
    }

    def publish_player_fact(fact_type, detail=""):
        """Record something the city could plausibly hear about."""
        t = PUBLIC_FACT_TEMPLATES.get(fact_type)
        if not t:
            return None
        fid = "%s_%s_d%d" % (fact_type, detail or "x", store.day)
        if fid in store.public_player_facts:
            return fid
        facts = dict(store.public_player_facts)
        facts[fid] = {"type": fact_type, "day": store.day, "detail": detail,
                      "propagated_to": [], "done": False}
        store.public_player_facts = facts
        return fid

    def _fact_audience(fact_type, day):
        """Who would plausibly hear it: people who were at an event with you
        recently, plus contacts you actually know. Respect only."""
        out = []
        for npc_id in NPC_DATA:
            if not npc_known(npc_id):
                continue
            if NPC_DATA[npc_id].get("no_decay"):
                continue
            score = npc_rel(npc_id, "familiarity")
            # Shared event attendance in the last week is the strongest signal.
            for d in range(max(0, day - 7), day + 1):
                for e in world_events_on_day(d):
                    if npc_id in e.get("npcs", []) and event_discovered(e["id"]):
                        score += 40
                        break
            if score >= 25:
                out.append((npc_id, score))
        out.sort(key=lambda x: -x[1])
        return [n for n, _ in out]

    def propagate_public_facts(current_day):
        for fid, f in list(store.public_player_facts.items()):
            if f.get("done"):
                continue
            t = PUBLIC_FACT_TEMPLATES[f["type"]]
            if current_day - f["day"] < t["propagation_delay"]:
                continue
            audience = [n for n in _fact_audience(f["type"], f["day"])
                        if n not in f["propagated_to"]][:t["max_npcs"]]
            for npc_id in audience:
                apply_relationship_change(
                    npc_id, "wom_" + fid, "reputation",
                    respect=t["affects"].get("respect", 0),
                    affection=t["affects"].get("affection", 0))
                add_relationship_memory(npc_id, t["dialogue_tag"],
                                        "Heard about what you did.",
                                        category="reputation", visibility="public")
            if audience:
                enqueue_followup(audience[0], "reaction", f["type"],
                                 t["followup_template"], delay_min=1, delay_max=4,
                                 priority=7)
            facts = dict(store.public_player_facts)
            facts[fid] = dict(f, propagated_to=f["propagated_to"] + audience, done=True)
            store.public_player_facts = facts

    # ── 68.7 Soft player identity ────────────────────────────────────────────
    def _kept_commitments():
        return sum(1 for c in store.player_commitments if c.get("completed"))

    def _missed_commitments():
        return sum(1 for c in store.player_commitments if c.get("missed"))

    PLAYER_IDENTITY_RULES = {
        "reliable": {
            "condition": lambda: (_kept_commitments() >= 5
                                  and _kept_commitments() > _missed_commitments() * 2),
            "tag": "player_reliable",
            "desc": "You show up when you say you will.",
        },
        "gym_regular": {
            "condition": lambda: store.location_visits.get("location_gym", 0) >= 10,
            "tag": "player_gym_regular",
            "desc": "You're part of the furniture at Iron Gate.",
        },
        "cafe_regular": {
            "condition": lambda: store.location_visits.get("location_cafe", 0) >= 12,
            "tag": "player_cafe_regular",
            "desc": "They start your order when you walk in.",
        },
        "night_owl": {
            "condition": lambda: store._nights_active >= 15,
            "tag": "player_night_owl",
            "desc": "The city after ten is your normal hours.",
        },
        "creative": {
            "condition": lambda: len([a for a in store.player_artworks
                                      if a.get("quality") in ("great", "critical")]) >= 3,
            "tag": "player_creative",
            "desc": "People have started calling you an artist out loud.",
        },
    }

    def update_player_identity(current_day):
        flags = dict(store._player_identity_flags)
        for key, rule in PLAYER_IDENTITY_RULES.items():
            try:
                on = bool(rule["condition"]())
            except Exception:
                on = False
            if on and not flags.get(key):
                flags[key] = True
                renpy.notify(rule["desc"])
            elif not on and flags.get(key):
                # Identity is soft: it can lapse if you stop doing the thing.
                flags.pop(key, None)
        store._player_identity_flags = flags

    def player_has_identity(key):
        return bool(store._player_identity_flags.get(key))

    def player_identity_tags():
        return [PLAYER_IDENTITY_RULES[k]["tag"]
                for k in store._player_identity_flags if k in PLAYER_IDENTITY_RULES]

    def record_night_activity():
        """Call when the player is at a public location after 22:00.
        One count per night."""
        if store.hour < 22 and store.hour >= 6:
            return
        if store._p68_night_day == store.day:
            return
        store._p68_night_day = store.day
        store._nights_active += 1

    # ── 68.8 Failure content ─────────────────────────────────────────────────
    FAILURE_CONTENT = {
        "promotion_failed": {"cooldown_days": 14,
                             "mail": ("Your manager", "About the review",
                                      "The panel went with someone else this cycle. "
                                      "The feedback was specific, which is better than "
                                      "the alternative. Come and talk it through."),
                             "npc_pool": ["martha", "caroline"],
                             "template": "encourage_setback"},
        "open_mic_poor":    {"cooldown_days": 7, "npc_pool": ["zoe", "marcus", "kai"],
                             "template": "encourage_setback"},
        "city_challenge_failed": {"cooldown_days": 5, "social": True,
                             "npc_pool": ["sam", "marcus"],
                             "template": "encourage_setback"},
    }

    def trigger_failure_content(trigger):
        """Call from the failing system. Not every failure produces content."""
        t = FAILURE_CONTENT.get(trigger)
        if not t:
            return False
        if store.day - store._failure_content_last.get(trigger, -999) < t["cooldown_days"]:
            return False
        d = dict(store._failure_content_last); d[trigger] = store.day
        store._failure_content_last = d
        if t.get("mail") and _pulse_can_mail():
            sender, subject, body = t["mail"]
            queue_mail(sender, subject, body, "career", store.day,
                       "p68_fail_%s_d%d" % (trigger, store.day))
            store._pulse_mail_today += 1
        if t.get("social"):
            _pulse_social_post("p68_fail_soc_%s_d%d" % (trigger, store.day),
                               "Not every attempt lands. Back next time.", "you")
        pool = [n for n in t.get("npc_pool", [])
                if npc_known(n) and npc_rel(n, "familiarity") >= 30]
        if pool:
            enqueue_followup(pool[0], "check_in", trigger, t["template"],
                             delay_min=1, delay_max=3, priority=6)
        return True

    # ── 68.1 Day-start orchestration ─────────────────────────────────────────
    def _prioritized_npc_list():
        """Closest relationships get first refusal on the daily contact slot."""
        return sorted((n for n in NPC_DATA if npc_known(n)
                       and not NPC_DATA[n].get("no_decay")),
                      key=lambda n: -(npc_rel(n, "familiarity")
                                      + max(0, npc_rel(n, "affection"))))

    def evaluate_npc_initiatives(current_day):
        """Phase 68's own initiative pass. Idempotent per day, and it shares the
        one-contact-per-day budget with phone_actionable's _check_npc_initiative
        (which runs earlier in new_day())."""
        if store._initiative_evaluated_day == current_day:
            return
        store._initiative_evaluated_day = current_day
        if _initiative_budget_spent():
            return
        # Priority order: a real event tomorrow > a delayed follow-up.
        if _try_event_invite(current_day):
            _spend_initiative_budget()
            return
        if process_followup_queue(current_day):
            _spend_initiative_budget()
            return

    def process_npc_lives_day():
        """Single entry point called from new_day() after the world pulse."""
        current_day = store.day
        _expire_personal_lives(current_day)
        for npc_id in NPC_PERSONAL_LIFE_WEIGHTS:
            if npc_known(npc_id) and not npc_personal_life(npc_id):
                _roll_personal_life(npc_id, current_day)
        propagate_public_facts(current_day)
        update_player_identity(current_day)
        _process_npc_cancellations(current_day)
        evaluate_npc_initiatives(current_day)

