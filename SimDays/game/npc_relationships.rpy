# Phase 66 — Relationship depth.
#
# ── Storage decision (66.1) ──────────────────────────────────────────────────
# The game already stores Affection and Trust as ~24 per-NPC store variables
# (nora_affection, nora_trust, ...), addressed indirectly through
# NPC_DATA[npc_id]["aff"] / ["trust"]. Those variables are read in roughly 500
# places (story gates in data.rpy/new_day, arc requirements, hug/kiss profiles,
# invitation eligibility, dev smoke tests) and written from 565 _apply_aff /
# _apply_trust call sites.
#
# So this file uses a HYBRID of spec option B:
#
#   * affection / trust  -> stay in the legacy per-NPC variables. npc_rel() and
#                           set_npc_rel() proxy to them. Zero migration, zero
#                           desync risk, every existing gate keeps working.
#   * respect / familiarity / attraction (the NEW axes)
#                        -> live in the central `npc_relationships` dict,
#                           lazily seeded from the legacy values on first access.
#
# Trying to *move* affection/trust into the dict would mean editing ~500 read
# sites for no gameplay gain — the definition of code that should never be
# written. The cost of the hybrid is one indirection in npc_rel(); documented
# here so nobody "tidies" it later.
#
# ── Central mutation point (66.3) ────────────────────────────────────────────
# apply_relationship_change() is the only function gameplay code should call.
# _apply_aff() / _apply_trust() are REDEFINED at the bottom of this file to
# route through it with source_category="authored" (caps + saturation bypassed),
# so all 565 existing authored-scene call sites keep their exact old numbers
# while still accruing Familiarity and emitting the developer trace. See 66.9.

default npc_relationships   = {}   # {npc_id: {"respect": int, "familiarity": int, "attraction": int, "_seeded": True}}
default _rel_saturation     = {}   # {npc_id: {source_category: [day, count]}}
default _rel_source_totals  = {}   # {npc_id: {source_category: {axis: total_contributed}}}
default _rel_trace          = []   # developer-only ring buffer of recent changes
default _rel_trace_enabled  = False
default _chemistry_floor_migrated = False   # old-save Chemistry floor (66.10)


init 1 python:

    # ── Axis metadata ────────────────────────────────────────────────────────
    REL_AXES = ("affection", "trust", "respect", "familiarity", "attraction")
    _REL_NEW_AXES = ("respect", "familiarity", "attraction")

    # Only these NPCs have romance content (ROMANCE_PROFILES lives in
    # interact.rpy); attraction is tracked but hidden for everyone else.
    def npc_is_romance_capable(npc_id):
        try:
            return npc_id in ROMANCE_PROFILES
        except NameError:
            return False

    # ── Lazy migration (66.1 / 66.12) ────────────────────────────────────────
    # Heuristics, applied ONCE per NPC on first access of the new axes:
    #   familiarity = max(aff, trust) * 0.7 + (30 if met)
    #       Rationale: an old save with aff 50 has clearly spent time with the
    #       NPC. 0.7 keeps familiarity below the "close" band so returning
    #       players still have runway; the +30 for a met NPC encodes "you are
    #       not strangers" without granting it to never-met NPCs.
    #   respect = trust * 0.5 + 10
    #       Rationale: pre-Phase-66 the only thing that moved slowly and was
    #       earned by competence was Trust. Half of it is a conservative floor;
    #       +10 is the "you exist and you are not useless" baseline everyone
    #       starts with once known.
    #   attraction = 0 (no pre-existing signal to migrate from)
    def _seed_npc_relationship(npc_id):
        d = NPC_DATA.get(npc_id, {})
        aff = getattr(store, d.get("aff", ""), 0) or 0
        tr  = getattr(store, d.get("trust", ""), 0) or 0
        met_var = d.get("met")
        met = True if d.get("world") else bool(getattr(store, met_var, False)) if met_var else False
        # The +30 "you are not strangers" bonus is only for saves that already
        # have a relationship. On a brand-new game every axis is 0, so a world
        # NPC you have never spoken to must still read as a stranger — without
        # the `> 0` guard, day 1 would open with everyone at Acquaintance.
        prior = max(aff, tr)
        fam = int(prior * 0.7) + (30 if (met and prior > 0) else 0)
        rec = {
            "familiarity": max(0, min(100, fam)),
            "respect":     max(0, min(100, int(tr * 0.5) + (10 if met else 0))),
            "attraction":  0,
            "_seeded":     True,
        }
        nr = dict(store.npc_relationships)
        nr[npc_id] = rec
        store.npc_relationships = nr
        return rec

    def _npc_rel_record(npc_id):
        rec = store.npc_relationships.get(npc_id)
        if rec is None or not rec.get("_seeded"):
            return _seed_npc_relationship(npc_id)
        return rec

    def npc_rel(npc_id, axis, default=0):
        """Get a relationship axis value. Initialises the new axes lazily from
        the legacy affection/trust variables the first time an NPC is touched."""
        d = NPC_DATA.get(npc_id)
        if axis == "affection":
            return getattr(store, d["aff"], default) if d else default
        if axis == "trust":
            return getattr(store, d["trust"], default) if d else default
        return _npc_rel_record(npc_id).get(axis, default)

    def set_npc_rel(npc_id, axis, value):
        """Set a relationship axis (clamped). Affection keeps its historical
        -100 floor; every other axis is 0-100."""
        d = NPC_DATA.get(npc_id)
        if axis == "affection":
            if not d: return
            setattr(store, d["aff"], max(-100, min(100, int(value))))
            return
        if axis == "trust":
            if not d: return
            setattr(store, d["trust"], max(0, min(100, int(value))))
            return
        rec = dict(_npc_rel_record(npc_id))
        rec[axis] = max(0, min(100, int(value)))
        nr = dict(store.npc_relationships)
        nr[npc_id] = rec
        store.npc_relationships = nr

    # ── 66.2 Relationship profiles ───────────────────────────────────────────
    # Every field is 0-1. See the per-NPC comment for the dialogue evidence that
    # justifies each non-0.5 value. Where the scenes say nothing, the value is
    # 0.5 on purpose — an honest "no evidence", not a guess.
    DEFAULT_REL_PROFILE = {
        "openness": 0.5, "trust_pace": 0.5, "affection_pace": 0.5,
        "respect_pace": 0.5, "gift_receptiveness": 0.5, "boundary_strength": 0.5,
        "social_selectiveness": 0.5, "status_sensitivity": 0.5,
        "romantic_openness": 0.5, "saturation_rate": 0.5,
    }

    # Every value below is backed by a cited line. Where the scene audit found
    # NO evidence for an axis, the value is left at the 0.5 default and the
    # comment says so - deliberately not guessed.
    NPC_RELATIONSHIP_PROFILES = {
        # Guarded, not warm-open: world_events.rpy:1443 "I'm waiting to see
        # whether you're polite." / :2196 "Before you ask, it isn't on the menu."
        # Trust is late - money and the culinary programme only surface in later
        # arc beats (arcs.rpy:134, :148). Warmth arrives then gets deflected:
        # gameplay_expansion_scenes.rpy:412 "Don't make it weird."
        # Respect = follow-through + plain honesty (:40 "Next time just say so.").
        # Punishes low effort rather than repetition (world_events.rpy:2204
        # "Too quick. Try again."), so saturation is below default.
        # status_sensitivity / gift_receptiveness: no evidence -> 0.5.
        "nora": {
            "openness": 0.5, "trust_pace": 0.35, "affection_pace": 0.5,
            "respect_pace": 0.6, "gift_receptiveness": 0.5, "boundary_strength": 0.5,
            "social_selectiveness": 0.6, "status_sensitivity": 0.5,
            "romantic_openness": 0.55, "saturation_rate": 0.4,
        },
        # Opens cold with strangers (world_events.rpy:1347 "Machine on the left
        # eats coins."). Fast on practical need (:854 asks for $120), slow on the
        # personal (arcs.rpy:193 "I try not to deal in those."). Warmth fast and
        # reciprocal (:1030 "I'll buy coffee after."). Respect = showing up
        # (gameplay_expansion_scenes.rpy:114 "There's always something. That's
        # not the point."). Explicitly anti-status (world_events.rpy:1204).
        # Actively seeks and brokers company (:2484 "I just moved a stool.").
        # Dislikes owing (:1016 clears the debt immediately) -> boundary above
        # default. romantic / saturation: no evidence -> 0.5.
        "marcus": {
            "openness": 0.85, "trust_pace": 0.45, "affection_pace": 0.7,
            "respect_pace": 0.65, "gift_receptiveness": 0.5, "boundary_strength": 0.6,
            "social_selectiveness": 0.15, "status_sensitivity": 0.1,
            "romantic_openness": 0.5, "saturation_rate": 0.5,
        },
        # Instantly open but oblique (world_events.rpy:1279 "Don't turn
        # around."). Fast surface, late substance (arcs.rpy:450 "I'm still
        # deciding how much of it I want to explain."). Respect = noticing
        # (arcs.rpy:385 "You asked about the one nobody else asked about.").
        # Explicitly anti-commercial (:461-463 "That's not what it was.").
        # Works alone by default, invites narrowly (world_events.rpy:1770).
        # REWARDS recurrence rather than tiring of it
        # (gameplay_expansion_scenes.rpy:767 "I keep finding you in the right
        # places.") -> saturation well below default.
        # gift_receptiveness: no evidence -> 0.5.
        "zoe": {
            "openness": 0.7, "trust_pace": 0.35, "affection_pace": 0.65,
            "respect_pace": 0.6, "gift_receptiveness": 0.5, "boundary_strength": 0.55,
            "social_selectiveness": 0.6, "status_sensitivity": 0.1,
            "romantic_openness": 0.6, "saturation_rate": 0.3,
        },
        # Reserved and task-framed (it_arc.rpy:19 "I'll answer your questions
        # once and expect you to remember."). Trust in small increments
        # (home_scenes.rpy:344 "I don't come to people's homes very often.").
        # Warmth lands awkwardly (:459-461). Respect = reasoning and habit
        # (it_arc.rpy:183 "That's the threshold. Not a skill level - a habit.")
        # and he refuses credit (:186 "Don't thank me. You did the work.").
        # Solitary, rations invitations (world_events.rpy:2174).
        # Explicit anti-repetition (it_arc.rpy:102 "I didn't ask if you could.").
        # gift / romantic: no evidence -> 0.5 (not in ROMANCE_PROFILES anyway).
        "eli": {
            "openness": 0.25, "trust_pace": 0.4, "affection_pace": 0.35,
            "respect_pace": 0.8, "gift_receptiveness": 0.5, "boundary_strength": 0.6,
            "social_selectiveness": 0.75, "status_sensitivity": 0.15,
            "romantic_openness": 0.5, "saturation_rate": 0.7,
        },
        # Brisk and functional with strangers (world_events.rpy:1261 "Water." /
        # "That wasn't a question."). Candid fast on the ONE topic - the missed
        # session (:919-924) - guarded elsewhere. Care delivered as correction
        # (:1233 "Knowing when to stop counts too."), so affection_pace is low.
        # Respect = adherence to the programme (:2397 "I wrote it for a
        # reason."). Parallel presence, not company (:1753). Names static
        # repetition and leaves (:1767-1769 "You're always here." / "I'm
        # moving."). status / gift / romantic: no evidence -> 0.5.
        "sam": {
            "openness": 0.5, "trust_pace": 0.45, "affection_pace": 0.3,
            "respect_pace": 0.75, "gift_receptiveness": 0.5, "boundary_strength": 0.5,
            "social_selectiveness": 0.7, "status_sensitivity": 0.5,
            "romantic_openness": 0.5, "saturation_rate": 0.6,
        },
        # High-energy open front, which she names as performance
        # (gameplay_expansion_scenes.rpy:1206 "Everyone wants the energy all the
        # time."). One scripted off-duty beat is the only crack (:1213 "But
        # yeah. Sometimes.") -> low trust_pace despite high openness. This is the
        # case the brief warns about: sociable does NOT mean trusting.
        # Warmth easy (home_scenes.rpy:304 "Same time next week?"). Respect =
        # judgment about people (trainer_arc.rpy:118). Professionally
        # boundary-vigilant (:198 "The ones who think there's a grey zone...").
        # Converts contact into standing slots -> low saturation.
        "kai": {
            "openness": 0.85, "trust_pace": 0.3, "affection_pace": 0.75,
            "respect_pace": 0.6, "gift_receptiveness": 0.5, "boundary_strength": 0.65,
            "social_selectiveness": 0.2, "status_sensitivity": 0.2,
            "romantic_openness": 0.5, "saturation_rate": 0.3,
        },
        # Verbally direct and volunteers the vulnerable thing herself
        # (gameplay_expansion_scenes.rpy:1064-1066 "Can I say a thing? ... I've
        # been sitting on that for a while."). Initiates romance (:1071).
        # Sociable, has an existing circle. Respect = being steadying (:1292
        # "You're good at this part."). Uncomfortable at being ANTICIPATED
        # (world_events.rpy:2456-2460 "Your barista knows my order." / "I'm not
        # sure how I feel about that.") -> boundary above default even though
        # gift reactions specifically are unevidenced.
        "elle": {
            "openness": 0.8, "trust_pace": 0.7, "affection_pace": 0.75,
            "respect_pace": 0.5, "gift_receptiveness": 0.5, "boundary_strength": 0.55,
            "social_selectiveness": 0.3, "status_sensitivity": 0.5,
            "romantic_openness": 0.8, "saturation_rate": 0.5,
        },
        # Composed and professionally guarded (hospital_arc.rpy:24). Deflects
        # first, then reciprocates (gameplay_expansion_scenes.rpy:229 "I'm fine."
        # -> :345 "I went into medicine because I thought I'd be good at it.").
        # Warmth measured and gratitude-shaped (home_scenes.rpy:276).
        # Respect = self-reported honesty (hospital_arc.rpy:186 "You reported the
        # mistake before I had to ask.") and she declines credit (:201) ->
        # respect_pace high, status_sensitivity low. Chooses solitude
        # (world_events.rpy:2473). Raises romance herself (:1029).
        # gift / saturation: no evidence -> 0.5.
        "lena": {
            "openness": 0.35, "trust_pace": 0.5, "affection_pace": 0.4,
            "respect_pace": 0.8, "gift_receptiveness": 0.5, "boundary_strength": 0.6,
            "social_selectiveness": 0.7, "status_sensitivity": 0.3,
            "romantic_openness": 0.6, "saturation_rate": 0.5,
        },
        # Terse and operational (warehouse_arc.rpy:12 "Urgent dispatch on bay
        # four."). Exactly one confiding beat, on her own turf
        # (gameplay_expansion_scenes.rpy:1169 "This is the part that's actually
        # mine."). Warmest gesture is a conditional standing invite (:1177).
        # Respect = judgment plus writing the call down (warehouse_arc.rpy:75
        # "Someone needed to write it down. You did."). Everything else - gifts,
        # romance, saturation, status, selectiveness - no evidence -> 0.5.
        "natalie": {
            "openness": 0.35, "trust_pace": 0.35, "affection_pace": 0.3,
            "respect_pace": 0.75, "gift_receptiveness": 0.5, "boundary_strength": 0.5,
            "social_selectiveness": 0.5, "status_sensitivity": 0.5,
            "romantic_openness": 0.5, "saturation_rate": 0.5,
        },
        # Openly evaluative (corporate_arc.rpy:204 "I'm deciding whether you're
        # worth talking to properly." / :209 "six people sat at that desk").
        # Retracts warmth in the same breath (:262 -> :272 "Don't read too much
        # into it."). Respect = competence AND credit-honesty (world_events.rpy
        # :1810-1812 "You built it." / "There's a large difference.").
        # Status-aware but anti-flattery (gameplay_expansion_scenes.rpy:648
        # "Don't let flattery become a tool.").
        # GIFTS: the only NPC with direct evidence. scene_martha_gift_accusation
        # (gameplay_expansion_scenes.rpy:618-654) fires on the third gift -
        # ":632 [gift]. And the ones before it." / ":642 It's borderline. Be
        # careful." Lowest gift_receptiveness and highest boundary_strength in
        # the cast, and the number the expensive-early rule was written for.
        # Reads patterns rather than single acts (:940) -> high saturation.
        "martha": {
            "openness": 0.15, "trust_pace": 0.25, "affection_pace": 0.3,
            "respect_pace": 0.9, "gift_receptiveness": 0.15, "boundary_strength": 0.95,
            "social_selectiveness": 0.8, "status_sensitivity": 0.7,
            "romantic_openness": 0.3, "saturation_rate": 0.75,
        },
        # Closed and formal by default (corporate_atlas.rpy:13 "Close the
        # door."). Explicitly refuses to act on inference
        # (gameplay_expansion_scenes.rpy:994 "I don't act on suspicion.") ->
        # lowest trust_pace in the cast. Warmth rationed and immediately
        # re-priced (corporate_arc.rpy:321 -> :325 "Give me a reason to do it
        # again in six months."). Respect = judgment under pressure and
        # integrity over optics (:446 "You didn't know - and you didn't submit
        # anyway."). Extremely room-aware (:304 "That reads well in some rooms
        # and very poorly in others."). Boundary language around after-hours
        # contact (:1132) -> high boundary_strength. Names repeated proximity
        # (:988 "I've stopped calling it coincidence.") -> high saturation.
        "caroline": {
            "openness": 0.2, "trust_pace": 0.2, "affection_pace": 0.3,
            "respect_pace": 0.85, "gift_receptiveness": 0.35, "boundary_strength": 0.75,
            "social_selectiveness": 0.75, "status_sensitivity": 0.8,
            "romantic_openness": 0.4, "saturation_rate": 0.7,
        },
        # Imperatives only with new staff (culinary_arc.rpy:34 "Commis. Knife
        # roll out. Station three."). Trust is an explicit ledger (:577 "I will
        # give you one call at the pass." / :581 "Earn the second.").
        # Praise deliberately withheld (:873-875 "That was not praise.").
        # Respect = honesty TIMING then consistency (:311-312 "You made a
        # mistake. You did not make me discover it.") -> highest respect_pace.
        # Anti-prestige: walked out of an investment firm after one real service
        # (:142) -> lowest status_sensitivity. Most explicitly anti-repetition
        # NPC in the script (:203-205 "You said that twenty seconds ago." /
        # "Then do not spend another one explaining it.") -> highest saturation.
        # gift / romantic: no evidence -> 0.5. NPC_DATA marks her no_decay and
        # she is outside the world interaction pool, so most of this is dormant.
        "rena": {
            "openness": 0.2, "trust_pace": 0.3, "affection_pace": 0.2,
            "respect_pace": 0.95, "gift_receptiveness": 0.5, "boundary_strength": 0.7,
            "social_selectiveness": 0.75, "status_sensitivity": 0.05,
            "romantic_openness": 0.5, "saturation_rate": 0.9,
        },
    }

    def npc_rel_profile(npc_id):
        p = dict(DEFAULT_REL_PROFILE)
        p.update(NPC_RELATIONSHIP_PROFILES.get(npc_id, {}))
        return p

    # ── 66.4 Source-category soft caps ───────────────────────────────────────
    # A cap is a CEILING ON THE AXIS, not a running total: once the axis is at
    # or above the cap, this source contributes nothing more. Calibrated against
    # the shipping numbers — a talk gives +1..3 affection, so "casual_talk"
    # capping affection at 40 means small talk alone plateaus you at the top of
    # the old "Friends" tier (rel_tier: 25-49) and the last half needs real
    # content. Trust never moved from talking at all pre-66; 15 keeps that
    # essentially true while removing the hard zero.
    RELATIONSHIP_SOURCE_CAPS = {
        "casual_talk":       {"affection": 40,  "trust": 15,  "respect": 10,  "familiarity": 80},
        "meaningful_talk":   {"affection": 65,  "trust": 55,  "respect": 35,  "familiarity": 90},
        "gift":              {"affection": 50,  "trust": 5,   "respect": 15,  "familiarity": 20},
        "shared_activity":   {"affection": 55,  "trust": 40,  "respect": 20,  "familiarity": 75},
        "kept_commitment":   {"affection": 30,  "trust": 85,  "respect": 80,  "familiarity": 50},
        "helping_npc":       {"affection": 40,  "trust": 75,  "respect": 70,  "familiarity": 40},
        "competence_display":{"affection": 20,  "trust": 30,  "respect": 85,  "familiarity": 20},
        "reputation":        {"affection": 0,   "trust": 10,  "respect": 60,  "familiarity": 15},
        "story_moment":      {"affection": 100, "trust": 100, "respect": 100, "familiarity": 100},
        # "authored" = the 565 legacy _apply_aff/_apply_trust call sites in
        # hand-written scenes. Uncapped by design: those numbers were balanced
        # by hand and Phase 66 must not silently re-balance the whole script.
        "authored":          {"affection": 100, "trust": 100, "respect": 100, "familiarity": 100},
    }

    def _source_cap(source_category, axis):
        return RELATIONSHIP_SOURCE_CAPS.get(source_category, {}).get(axis, 100)

    # ── 66.5 Saturation ──────────────────────────────────────────────────────
    _SATURATION_STEPS = (1.0, 0.6, 0.3, 0.05)

    def _saturation_count(npc_id, source_category):
        rec = store._rel_saturation.get(npc_id, {}).get(source_category)
        if not rec or rec[0] != store.day:
            return 0
        return rec[1]

    def _bump_saturation(npc_id, source_category):
        sat = dict(store._rel_saturation)
        per = dict(sat.get(npc_id, {}))
        rec = per.get(source_category)
        per[source_category] = [store.day, (rec[1] + 1) if (rec and rec[0] == store.day) else 1]
        sat[npc_id] = per
        store._rel_saturation = sat

    def relationship_saturation_multiplier(npc_id, source_category):
        """1.0 down to 0.05 as the same source repeats today. saturation_rate
        scales how fast the drop-off bites: 1.0 = as written, 0.0 = never
        saturates. Rate 0.5 (the default) halves the penalty."""
        n = _saturation_count(npc_id, source_category)
        base = _SATURATION_STEPS[min(n, len(_SATURATION_STEPS) - 1)]
        rate = npc_rel_profile(npc_id)["saturation_rate"]
        # rate 0.5 (default) -> exactly the table above. rate 1.0 doubles the
        # penalty, rate 0.0 removes it entirely.
        return max(0.02, min(1.0, 1.0 - (1.0 - base) * (rate / 0.5)))

    _PACE_KEY = {"affection": "affection_pace", "trust": "trust_pace",
                 "respect": "respect_pace", "familiarity": "openness",
                 "attraction": "romantic_openness"}

    def _rel_axis_floor(axis):
        return -100 if axis == "affection" else 0

    # ── 66.3 Central API ─────────────────────────────────────────────────────
    def apply_relationship_change(npc_id, source_id, source_category,
                                  affection=0, trust=0, respect=0, familiarity=0,
                                  attraction=0, meaningful=False,
                                  bypass_saturation=False):
        """The single relationship mutation point.

        Applies personality pace multipliers, source-category soft caps, daily
        saturation and gift-repetition penalties, then writes through
        set_npc_rel(). Returns the dict of applied deltas.

        Never call set_npc_rel() from gameplay code — call this."""
        if npc_id not in NPC_DATA:
            return {}
        profile = npc_rel_profile(npc_id)
        requested = {"affection": affection, "trust": trust, "respect": respect,
                     "familiarity": familiarity, "attraction": attraction}
        if not any(requested.values()):
            return {}

        # Saturation (meaningful and story moments ignore it).
        if bypass_saturation or meaningful or source_category in ("story_moment", "authored"):
            sat_mult = 1.0
        else:
            sat_mult = relationship_saturation_multiplier(npc_id, source_category)

        # Gift repetition penalty (66.6).
        gift_mult = _gift_repetition_multiplier(npc_id) if source_category == "gift" else 1.0

        applied = {}
        for axis, raw in requested.items():
            if not raw:
                continue
            pace = profile[_PACE_KEY[axis]]
            # pace 0.5 is neutral; 0 halves, 1 gives +50%.
            delta = raw * (0.5 + pace) * sat_mult * gift_mult
            # Losses are never damped by pace/saturation — being careless
            # costs the same whether or not the NPC is easy-going.
            if raw < 0:
                delta = raw
            delta = int(round(delta))
            if delta == 0 and raw > 0:
                delta = 1 if (raw >= 1 and sat_mult > 0.2) else 0
            if delta == 0:
                continue
            old = npc_rel(npc_id, axis)
            new = old + delta
            if delta > 0 and not bypass_saturation:
                cap = _source_cap(source_category, axis)
                if old >= cap:
                    continue                 # this source can't push further
                new = min(new, cap)
            new = max(_rel_axis_floor(axis), min(100, new))
            if new == old:
                continue
            set_npc_rel(npc_id, axis, new)
            applied[axis] = new - old

        if applied and not (bypass_saturation or meaningful
                            or source_category in ("story_moment", "authored")):
            _bump_saturation(npc_id, source_category)
        if applied:
            _record_source_total(npc_id, source_category, applied)
            _check_relationship_thresholds(npc_id)
            _rel_log(npc_id, source_id, source_category, requested, applied,
                     sat_mult, gift_mult)
        return applied

    def _record_source_total(npc_id, source_category, applied):
        tot = dict(store._rel_source_totals)
        per = dict(tot.get(npc_id, {}))
        cat = dict(per.get(source_category, {}))
        for a, v in applied.items():
            cat[a] = cat.get(a, 0) + v
        per[source_category] = cat
        tot[npc_id] = per
        store._rel_source_totals = tot

    def _rel_log(npc_id, source_id, cat, requested, applied, sat_mult, gift_mult):
        if not renpy.config.developer:
            return
        entry = {"day": store.day, "hour": store.hour, "npc": npc_id,
                 "src": source_id, "cat": cat,
                 "req": {k: v for k, v in requested.items() if v},
                 "got": dict(applied), "sat": round(sat_mult, 2),
                 "gift": round(gift_mult, 2)}
        store._rel_trace = (list(store._rel_trace) + [entry])[-60:]
        if store._rel_trace_enabled:
            renpy.log("REL %s %s/%s req=%s got=%s sat=%.2f" %
                      (npc_id, cat, source_id, entry["req"], entry["got"], sat_mult))

    # ── 66.6 Gift evaluation ─────────────────────────────────────────────────
    # Gift history reuses the shipping `gift_log` list
    # ({npc_id, gift_type, day}) — no second parallel store.
    def npc_gift_history(npc_id, limit=None):
        h = [g for g in store.gift_log if g.get("npc_id") == npc_id]
        return h[-limit:] if limit else h

    def _gift_repetition_multiplier(npc_id):
        """Same NPC, gifts within the last 7 days: 1.0 / 0.6 / 0.3 / 0.1."""
        recent = [g for g in npc_gift_history(npc_id) if store.day - g.get("day", -99) <= 7]
        n = max(0, len(recent) - 1)   # the current gift is already logged
        return (1.0, 0.6, 0.3)[n] if n < 3 else 0.1

    def _gift_value(item_id):
        """Item value in dollars. Understands GIFT_TYPES and ITEM_CATALOG."""
        try:
            if item_id in GIFT_TYPES:
                return GIFT_TYPES[item_id][1]
        except NameError:
            pass
        try:
            return ITEM_CATALOG.get(item_id, {}).get("price_new", 0)
        except NameError:
            return 0

    def _gift_topics(item_id):
        try:
            if item_id in GIFT_TYPES:
                return GIFT_TYPES[item_id][2]
        except NameError:
            pass
        return []

    def evaluate_gift(npc_id, item_id, occasion=None):
        """Returns {"affection", "trust", "respect", "reaction"}.

        affection = value curve (diminishing, capped at +6) x receptiveness,
                    + thoughtfulness bonus when the item hits a liked topic or
                    a hobby domain they care about, - penalty when it hits a
                    disliked topic.
        respect   = +1 only for a genuinely thoughtful gift; NEGATIVE when the
                    gift is expensive relative to how well they know you and
                    their boundary_strength is high (the "buying me?" read).
        trust     = never moved by objects. Capped at 5 in the source table.
        """
        d = NPC_DATA.get(npc_id, {})
        profile = npc_rel_profile(npc_id)
        value = _gift_value(item_id)
        topics = _gift_topics(item_id)
        likes, dislikes = d.get("likes", []), d.get("dislikes", [])

        # Base: sqrt-ish diminishing curve on price, hard-capped.
        base = min(6.0, (value ** 0.5) / 2.2)
        aff = base * (0.5 + profile["gift_receptiveness"])

        thoughtful = any(t in likes for t in topics)
        if thoughtful:
            aff += 2.0
        elif any(t in dislikes for t in topics):
            aff -= 1.5
        # Hobby-domain match (Phase 65 registry) counts as thoughtfulness too.
        try:
            if any(npc_interest(npc_id, dom) >= 2 for dom in _GIFT_DOMAINS.get(item_id, ())):
                aff += 1.0
                thoughtful = True
        except NameError:
            pass

        if occasion:
            aff += 1.5

        fam = npc_rel(npc_id, "familiarity")
        respect = 1 if thoughtful else 0
        reaction = "positive" if aff >= 2 else ("neutral" if aff > 0 else "neutral")

        # Expensive-early rule (66.6). Excess is measured against a familiarity
        # allowance of ~$7 per familiarity point.
        excess = value - max(50, fam * 7)
        if fam < 30 and value > 200 and profile["boundary_strength"] > 0.6:
            reaction = "uncomfortable"
            aff = min(aff, 1.0)
            respect = -int(round(profile["boundary_strength"] * 3))
            add_relationship_memory(npc_id, "received_expensive_gift_early",
                                    "You gave them something far too expensive far too early.",
                                    category="relationship")
        elif excess > 0 and profile["boundary_strength"] > 0.6 and fam < 50:
            reaction = "uncomfortable"
            aff *= 0.5
            respect = min(respect, 0)

        return {"affection": max(-3, int(round(aff))),
                "trust": 0,
                "respect": respect,
                "reaction": reaction}

    # item_id -> hobby domains, for the NPC_INTERESTS thoughtfulness bonus.
    _GIFT_DOMAINS = {"book": ("art",), "gadget": ("programming",),
                     "sweets": ("cooking",), "flowers": ("art",)}

    # ── 66.7 Relationship stages ─────────────────────────────────────────────
    # Ordered most-specific first so the multi-axis combinations actually get a
    # chance to match. Calibrated against the shipping rel_tier() bands
    # (25 = Friends, 50 = Good friends, 75 = Close) so a save that reads
    # "Good friends" today reads "friend" or better here.
    def npc_relationship_stage(npc_id):
        a = npc_rel(npc_id, "affection")
        t = npc_rel(npc_id, "trust")
        r = npc_rel(npc_id, "respect")
        f = npc_rel(npc_id, "familiarity")
        if f < 10:                                  return "stranger"
        if t >= 70 and r >= 50 and f >= 55:         return "trusted"
        if a >= 60 and t >= 55 and f >= 60:         return "close"
        if f >= 50 and a >= 45 and t >= 35:         return "friend"
        if f >= 35 and a >= 30 and t >= 15:         return "friendly"
        if f < 20 and a < 20:                       return "known"
        return "acquaintance"

    REL_STAGE_LABELS = {
        "stranger": "Stranger", "known": "Known", "acquaintance": "Acquaintance",
        "friendly": "Friendly", "friend": "Friend", "close": "Close",
        "trusted": "Trusted",
    }

    def npc_relationship_stage_label(npc_id):
        return REL_STAGE_LABELS.get(npc_relationship_stage(npc_id), "Acquaintance")

    # ── 66.8 Invitation acceptance ───────────────────────────────────────────
    def invitation_acceptance_chance(npc_id, activity_type="casual"):
        profile = npc_rel_profile(npc_id)
        f = npc_rel(npc_id, "familiarity") / 100.0
        a = max(0, npc_rel(npc_id, "affection")) / 100.0
        t = npc_rel(npc_id, "trust") / 100.0
        r = npc_rel(npc_id, "respect") / 100.0
        if activity_type == "casual":
            base = f * 0.5 + a * 0.3 + profile["openness"] * 0.2
        elif activity_type == "home_visit":
            base = t * 0.5 + f * 0.3 + a * 0.2
        elif activity_type == "professional":
            base = r * 0.5 + f * 0.3 + profile["status_sensitivity"] * 0.2
        elif activity_type == "romantic":
            attr = npc_rel(npc_id, "attraction") / 100.0
            base = attr * 0.4 + a * 0.3 + t * 0.2 + f * 0.1
        else:
            base = f * 0.4 + a * 0.4 + profile["openness"] * 0.2
        # Selective people say no more often even when they like you.
        base *= (1.3 - profile["social_selectiveness"] * 0.5)
        # Phase 68: what week they are having. Defined in npc_initiative.rpy;
        # guarded so Phase 66 stands alone if that file is ever removed.
        try:
            base *= max(0.2, 1.0 + npc_availability_modifier(npc_id))
        except NameError:
            pass
        return min(0.95, max(0.05, base))

    # ── 66.9 Legacy call-site interception ───────────────────────────────────
    # interact.rpy runs at init 0, so its _apply_aff/_apply_trust already exist
    # here. We keep them (they own the toast + threshold notify) and wrap them,
    # so every one of the 565 authored call sites routes through the Phase 66
    # bookkeeping without a single edit. Authored scenes bypass caps and
    # saturation by design — see RELATIONSHIP_SOURCE_CAPS["authored"].
    _apply_aff_legacy   = _apply_aff
    _apply_trust_legacy = _apply_trust

    # Familiarity accrual for authored beats: a scene that moves affection also
    # means time spent together. Half the affection delta, min 1, cap 90.
    def _authored_familiarity(npc_id, delta):
        if delta <= 0:
            return
        cur = npc_rel(npc_id, "familiarity")
        if cur >= 90:
            return
        set_npc_rel(npc_id, "familiarity", min(90, cur + max(1, int(delta * 0.5))))

    def _apply_aff(npc_id, delta):
        _apply_aff_legacy(npc_id, delta)
        _authored_familiarity(npc_id, delta)
        if renpy.config.developer:
            _rel_log(npc_id, "legacy", "authored", {"affection": delta},
                     {"affection": delta}, 1.0, 1.0)

    def _apply_trust(npc_id, delta):
        _apply_trust_legacy(npc_id, delta)
        # Trust earned in an authored beat implies competence/reliability was
        # shown; give respect a small share so it isn't dead on old saves.
        if delta > 0:
            cur = npc_rel(npc_id, "respect")
            set_npc_rel(npc_id, "respect", min(80, cur + max(1, int(delta * 0.4))))
        _authored_familiarity(npc_id, delta)
        if renpy.config.developer:
            _rel_log(npc_id, "legacy", "authored", {"trust": delta},
                     {"trust": delta}, 1.0, 1.0)

    # ── Convenience wrappers for new gameplay code ───────────────────────────
    def rel_casual_talk(npc_id, source_id, affection=1, familiarity=2):
        return apply_relationship_change(npc_id, source_id, "casual_talk",
                                         affection=affection, familiarity=familiarity)

    def rel_shared_activity(npc_id, source_id, affection=3, trust=1, familiarity=3):
        return apply_relationship_change(npc_id, source_id, "shared_activity",
                                         affection=affection, trust=trust,
                                         familiarity=familiarity)

    def rel_kept_commitment(npc_id, source_id):
        return apply_relationship_change(npc_id, source_id, "kept_commitment",
                                         affection=1, trust=3, respect=2, familiarity=2,
                                         meaningful=True)

    def rel_competence(npc_id, source_id, respect=2):
        return apply_relationship_change(npc_id, source_id, "competence_display",
                                         respect=respect, familiarity=1)

    def clear_rel_saturation(npc_id=None):
        if npc_id is None:
            store._rel_saturation = {}
        else:
            sat = dict(store._rel_saturation)
            sat.pop(npc_id, None)
            store._rel_saturation = sat

    # ── 66.10 Old-save Chemistry floor ──────────────────────────────────────
    # Phase 66 seeded attraction=0 (no historic signal). Now Chemistry is
    # player-visible; a save already at dating/committed must not show 0.
    # Runs once post-load per save. Never lowers existing attraction.
    def _migrate_chemistry_floors():
        if store._chemistry_floor_migrated:
            return
        store._chemistry_floor_migrated = True
        _CHEM_FLOORS = {"interested": 25, "dating": 45, "committed": 60}
        try:
            _profiles = ROMANCE_PROFILES
        except NameError:
            return
        for _nid in list(_profiles.keys()):
            try:
                _state = get_romance_state(_nid)
            except NameError:
                return
            _floor = _CHEM_FLOORS.get(_state)
            if _floor is None:
                continue
            _cur = npc_rel(_nid, "attraction")
            if _cur < _floor:
                set_npc_rel(_nid, "attraction", _floor)

    if _migrate_chemistry_floors not in config.after_load_callbacks:
        config.after_load_callbacks.append(_migrate_chemistry_floors)
