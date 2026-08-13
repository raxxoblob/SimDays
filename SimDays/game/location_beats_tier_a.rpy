# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTUAL TIER A LOCATION BEATS — content pack 1
# ═══════════════════════════════════════════════════════════════════════════
# Sibling of location_beats.rpy (which holds the one-shot Nora cover-shift
# beat). Split out purely for file size — same conventions, same hook shape.
#
# PRIORITY ORDER, per location entry:
#   1. Hard authored commitment / major story event   (already in locations.rpy)
#   2. One-shot authored beats                        (nora_cover_shift etc.)
#   3. Contextual Tier A beats                        (THIS FILE)
#   4. Normal location gameplay                       (the activity menu)
#
# ANTI-SPAM
#   Global: at most ONE Tier A contextual beat per in-game day, city-wide.
#           store.last_tier_a_beat_day (data.rpy).
#   Per beat: store.tier_a_beat_last_day[beat_id] + a per-beat cooldown_days.
#   Pity: store.tier_a_beat_miss_count[beat_id] raises the chance every time a
#         genuinely valid opportunity rolls a miss, so a player who keeps
#         showing up at the right place eventually gets the scene.
#
# EVERY beat here is repeatable (cooldown-gated). None is a one-shot — the
# one-shot pattern already exists in location_beats.rpy and none of these ten
# is a story milestone.
#
# ZERO new assets: existing backgrounds and existing character sprites only.
#
# SCHEDULE REALITY (audited against npc_schedules.rpy — do not "fix" these
# windows without re-reading NPC_FULL_SCHEDULES):
#   nora   café Mon-Fri 07-15 (shift), Tue 15-17 lingering, Sat/Sun 10-18 shift
#   marcus park Mon-Fri 07-11 (running), bar Mon-Fri 16-24 / Sat-Sun 15-27
#   zoe    hub Mon-Fri 09-13, café Wed 13-18, park Thu-Fri 14-18,
#          sandbeach Sat-Sun 12-18, bar Sat 19-24
#   eli    hub Mon-Fri 09-12, library Mon-Fri 12-18, library Sat 10-16
# Marcus is NEVER at the gym and Marcus and Eli never share a location — see
# the header notes on beats 5 and 9.
# ═══════════════════════════════════════════════════════════════════════════

init python:

    # ── Beat selector infrastructure ──────────────────────────────────────────

    def _beat_global_ok():
        """True when the global one-contextual-beat-per-day budget is free."""
        return store.last_tier_a_beat_day != store.day

    def _beat_cooldown_ok(beat_id, cooldown_days):
        """True when beat_id has not fired within the last cooldown_days."""
        last = store.tier_a_beat_last_day.get(beat_id, -999)
        return (store.day - last) >= cooldown_days

    def _beat_triggered(beat_id):
        """Called by the scene label when a beat actually fires: spends the
        global daily budget and stamps the per-beat cooldown."""
        store.last_tier_a_beat_day = store.day
        d = dict(store.tier_a_beat_last_day)
        d[beat_id] = store.day
        store.tier_a_beat_last_day = d
        _beat_clear_pity(beat_id)

    def _beat_clear_pity(beat_id):
        m = dict(store.tier_a_beat_miss_count)
        m.pop(beat_id, None)
        store.tier_a_beat_miss_count = m

    def _beat_seed_of(beat_id):
        """Deterministic string fold. Deliberately NOT hash(): CPython
        randomises str hashing per process, so hash() would give a different
        answer for the same day after a restart — i.e. save-scummable."""
        acc = 0
        for ch in beat_id:
            acc = (acc * 131 + ord(ch)) % 1000003
        return acc

    def _beat_stable_roll(beat_id, chance_pct, pity_per_miss=0, pity_cap=100):
        """Roll for a contextual beat. Stable per (beat_id, day): reloading or
        re-entering the location cannot re-roll it.

        The result is frozen into tier_a_beat_roll_cache the first time it is
        asked for on a given day, which is also the only moment the pity
        counter moves — so calling this five times in one day (five café
        visits) costs exactly one missed opportunity, not five.

        Call it LAST in a check function: everything before it is a hard
        requirement, so a cached roll always means a genuine opportunity.

        # ponytail: this is the one eligibility helper that writes state
        # (roll cache + pity). It is idempotent within a day, which is what
        # makes that safe. Upgrade path if beats multiply: move the cache to a
        # single per-day dict cleared in new_day() instead of per-beat stamps.
        """
        cached = store.tier_a_beat_roll_cache.get(beat_id)
        if cached and cached[0] == store.day:
            return bool(cached[1])

        misses = store.tier_a_beat_miss_count.get(beat_id, 0)
        total = min(pity_cap, chance_pct + misses * pity_per_miss)

        import random as _r
        rng = _r.Random(store.day * 100003 + _beat_seed_of(beat_id))
        result = rng.randint(1, 100) <= total

        cache = dict(store.tier_a_beat_roll_cache)
        cache[beat_id] = [store.day, bool(result)]
        store.tier_a_beat_roll_cache = cache

        if not result:
            m = dict(store.tier_a_beat_miss_count)
            m[beat_id] = misses + 1
            store.tier_a_beat_miss_count = m
        else:
            _beat_clear_pity(beat_id)
        return result

    def _beat_fam(npc_id):
        return npc_rel(npc_id, "familiarity")

    def _beat_festival_attended():
        try:
            return bool(store.summer_festival_state.get("attended"))
        except Exception:
            return False

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 1 — Zoe, outdoor run-in.  location_sandbeach, Sat/Sun 12-18.
    # The spec asked for "the real outdoor location Zoe can appear at": the
    # beach it is — location_sandbeach is a real label and her weekend
    # 12-18 socializing block is the only outdoor daytime slot she owns that
    # isn't already spoken for by the park beats.
    # ═════════════════════════════════════════════════════════════════════════
    def check_zoe_outdoor():
        if not store.zoe_met:
            return False
        if not npc_here("zoe", "location_sandbeach"):
            return False
        if not (12.0 <= float(store.hour) < 18.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("zoe_outdoor", 5):
            return False
        chance = 12 + (4 if _beat_fam("zoe") >= 30 else 0)
        return _beat_stable_roll("zoe_outdoor", chance,
                                 pity_per_miss=3, pity_cap=28)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 2 — Zoe, walk with me?  location_park, Thu/Fri 14-18.
    # Spec window was 10:00-18:00; her park block is 14-18 Thu/Fri, so the
    # intersection is the real window.
    # ═════════════════════════════════════════════════════════════════════════
    def check_zoe_walk():
        if not store.zoe_met:
            return False
        if not npc_here("zoe", "location_park"):
            return False
        if not (14.0 <= float(store.hour) < 18.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("zoe_walk", 4):
            return False
        chance = 10 + (3 if _beat_fam("zoe") >= 30 else 0)
        return _beat_stable_roll("zoe_walk", chance,
                                 pity_per_miss=3, pity_cap=22)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 3 — Eli, quick favour.  location_library, Mon-Fri 12-18 / Sat 10-16.
    # ═════════════════════════════════════════════════════════════════════════
    def check_eli_favor():
        if not store.eli_met:
            return False
        if not npc_here("eli", "location_library"):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("eli_favor", 6):
            return False
        # Alternative requirement: any one of these is enough of a reason for
        # her to ask you rather than the room.
        if not (_beat_fam("eli") >= 35 or store.skill_prog >= 3
                or _beat_festival_attended()):
            return False
        chance = 10 + (4 if store.skill_prog >= 3 else 0)
        return _beat_stable_roll("eli_favor", chance,
                                 pity_per_miss=3, pity_cap=22)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 4 — Eli, after your shift?  location_hub, Mon-Fri 09-12.
    # There is no `on_shift` variable in this codebase. `active_work_shift` is
    # only set for the four hours a shift label is executing, so it can never
    # be observed from a location entry. The workplace-visitor condition is
    # therefore: The Hub is MC's workplace (`"it" in active_careers`) and Eli
    # — who is MC's actual colleague there, see it_npc1_eli — is on site.
    # ═════════════════════════════════════════════════════════════════════════
    def check_eli_after_shift():
        if not store.eli_met:
            return False
        if "it" not in store.active_careers:
            return False
        if not npc_here("eli", "location_hub"):
            return False
        if not (9.0 <= float(store.hour) < 12.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("eli_after_shift", 7):
            return False
        return _beat_stable_roll("eli_after_shift", 8,
                                 pity_per_miss=2, pity_cap=18)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 5 — Marcus, spot me / pace me.  location_park, Mon-Fri 07-11.
    # Spec asked for the gym. Marcus has NO gym schedule slot anywhere in
    # NPC_FULL_SCHEDULES (the gym belongs to Sam and Kai), and inventing one
    # would be a ghost schedule entry. His real fitness slot is the weekday
    # morning park run — and marcus_park_* sprites already exist for it — so
    # the favour is "pace the last loop with me" instead of "spot me".
    # ═════════════════════════════════════════════════════════════════════════
    def check_marcus_park_favor():
        if not store.marcus_met:
            return False
        if not npc_here("marcus", "location_park"):
            return False
        if not (7.0 <= float(store.hour) < 11.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("marcus_park_favor", 5):
            return False
        return _beat_stable_roll("marcus_park_favor", 14,
                                 pity_per_miss=3, pity_cap=26)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 6 — Marcus, one game.  location_bar, from 18:00.
    # The bar is location_bar, not "location_static". Resolves through the real
    # bar_games architecture: call bar_game_play("pool", "pool_marcus").
    # Rivalry history = "marcus_pool" in bar_first_wins.
    # ═════════════════════════════════════════════════════════════════════════
    def check_marcus_one_game():
        if not store.marcus_met:
            return False
        if not npc_here("marcus", "location_bar"):
            return False
        if float(store.hour) < 18.0:
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("marcus_one_game", 4):
            return False
        return _beat_stable_roll("marcus_one_game", 16,
                                 pity_per_miss=3, pity_cap=28)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 7 — Nora, you look exhausted.  location_cafe, MC low on energy.
    # 30 is the codebase's existing "low energy" line (bar_game_chance applies
    # its Low energy penalty below 30); too_tired() at 20 is the hard block.
    # She notices. She does NOT restore energy.
    # ═════════════════════════════════════════════════════════════════════════
    BEAT_LOW_ENERGY = 30

    def check_nora_exhausted():
        if not store.nora_met:
            return False
        if store.nora_life_state != "cafe":
            return False
        if not npc_here("nora", "location_cafe"):
            return False
        if store.need_energy >= BEAT_LOW_ENERGY:
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("nora_exhausted", 4):
            return False
        return _beat_stable_roll("nora_exhausted", 16,
                                 pity_per_miss=3, pity_cap=28)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 8 — Nora, walking out together.  location_cafe, weekend 17-18.
    # Spec asked for 18:00-19:00. Nora is at the café until 18:00 on her
    # weekend shift and never later than that on any day (Mon-Fri ends 15:00,
    # Tue lingering ends 17:00), so 18-19 is an empty window — the real
    # clocking-off hour is 17:00-18:00 at the weekend.
    #
    # OBSOLESCENCE — this is the weak version of the same moment. It must never
    # pre-empt nora_closing_scene (cafe_actions: nora_affection >= 40 and
    # hour >= 19 and not nora_closing_done) or the scheduled closing
    # commitment. If either could still happen, this beat stands down for good.
    # ═════════════════════════════════════════════════════════════════════════
    # ── Nora after-hours café gates (single source of truth) ─────────────────
    # Used by locations.rpy for BOTH the after-hours entry exemption in
    # label location_cafe and the in-menu checks in cafe_actions, and by
    # _nora_closing_still_possible() below. Hour is checked at the call site:
    # cafe_actions uses hour >= 19, the entry exemption uses 19 <= hour < 21.
    def _nora_closing_commitment_accepted():
        """A phone-booked closing commitment is live right now."""
        return commitment_available("nora_closing_1")

    def _nora_auto_closing_eligible():
        """Unscheduled closing scene — she's still locking up alone.
        Requires cafe life-state: once she's left for school she's never
        here after hours, and the scene is narratively about her shift."""
        return (store.nora_life_state == "cafe"
                and not store.nora_closing_done
                and store.nora_affection >= 40)

    def _nora_romance_reopen_eligible():
        """Post-closing reopen — offered once, one major scene per day.
        Also requires cafe life-state: the scene is set in her café and
        presupposes she still has keys / closing responsibility."""
        return (store.nora_life_state == "cafe"
                and store.nora_closing_done and not store.nora_reopen_done
                and store.major_scene_last_day != store.day
                and can_offer_romance_reopen("nora"))

    def _nora_closing_still_possible():
        """True while the stronger closing scene is still on the table."""
        return (_nora_closing_commitment_accepted()
                or _nora_auto_closing_eligible())

    def check_nora_walk_out():
        if not store.nora_met:
            return False
        if store.nora_life_state != "cafe":
            return False
        if not npc_here("nora", "location_cafe"):
            return False
        if not (17.0 <= float(store.hour) < 18.0):
            return False
        if _beat_fam("nora") < 30:
            return False
        if _nora_closing_still_possible():
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("nora_walk_out", 6):
            return False
        chance = 8 + (3 if _beat_fam("nora") >= 45 else 0)
        return _beat_stable_roll("nora_walk_out", chance,
                                 pity_per_miss=3, pity_cap=20)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 9 — already here.  location_bar, Saturday 19-24: Marcus + Zoe.
    # Spec asked for Marcus + Eli. Their schedules never intersect — Marcus is
    # park/bar, Eli is hub/library, on no day and at no hour do they share a
    # location (NPC_CROSSOVER_TEMPLATES reaches the same conclusion and pairs
    # Eli with Zoe at the hub instead). Marcus's only real shared-location
    # window with another met-able NPC in the evening is Zoe's Saturday bar
    # block, so this is Marcus + Zoe.
    # ═════════════════════════════════════════════════════════════════════════
    def check_marcus_zoe_bar():
        if not (store.marcus_met and store.zoe_met):
            return False
        if not npc_here("marcus", "location_bar"):
            return False
        if not npc_here("zoe", "location_bar"):
            return False
        if not (19.0 <= float(store.hour) < 24.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("marcus_zoe_bar", 8):
            return False
        return _beat_stable_roll("marcus_zoe_bar", 14,
                                 pity_per_miss=3, pity_cap=26)

    # ═════════════════════════════════════════════════════════════════════════
    # BEAT 10 — cross-thread.  location_cafe, Wednesday 13-15: Zoe + Nora.
    # The audit confirms the spec's preferred pairing IS possible: Nora is on
    # shift Mon-Fri 07-15 and Zoe browses the café Wed 13-18, so Wed 13:00-15:00
    # has both. No invented friendship history — they are two people who use
    # the same café and are mid-conversation when MC walks in.
    # ═════════════════════════════════════════════════════════════════════════
    def check_cross_zoe_nora():
        if not (store.zoe_met and store.nora_met):
            return False
        if store.nora_life_state != "cafe":
            return False
        if not npc_here("nora", "location_cafe"):
            return False
        if not npc_here("zoe", "location_cafe"):
            return False
        if not (13.0 <= float(store.hour) < 15.0):
            return False
        if not _beat_global_ok():
            return False
        if not _beat_cooldown_ok("cross_zoe_nora", 10):
            return False
        return _beat_stable_roll("cross_zoe_nora", 14,
                                 pity_per_miss=3, pity_cap=26)


# ═════════════════════════════════════════════════════════════════════════════
# SCENES
# Every label: set_hud("hidden") + story_scene_active True on entry, and both
# restored on every single exit path.
# ═════════════════════════════════════════════════════════════════════════════

# ── BEAT 1 — Zoe: outdoor run-in ─────────────────────────────────────────────
label zoe_outdoor_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_outdoor")
    $ _zf = npc_rel("zoe", "familiarity")
    scene sandbeach_day
    show screen hud
    hide screen people_here_dock

    show zoe_beach_neutral at sprite_r
    "You'd got about twenty paces down the sand before you registered that the person sitting on the breakwater was someone you knew."
    show zoe_beach_talk at sprite_r, react_step_back
    z "Okay, that's uncanny. I was about to text you about something else entirely."
    mc "Should I be worried?"
    show zoe_beach_talk at sprite_r
    z "Probably. It's about a colour."

    if _zf >= 30:
        show zoe_beach_laugh at sprite_r, react_bounce
        z "There's a specific grey the water does about an hour before it turns. I've been failing at it for three days."
        mc "And the beach is helping?"
        z "The beach is gloating."
    else:
        show zoe_beach_talk at sprite_r
        z "I'm out here trying to look at water without immediately deciding what's wrong with it. It's going badly."

    if _beat_festival_attended():
        show zoe_beach_talk at sprite_r, react_lean_in
        z "This is the most quiet I've had since the festival, and I'm wasting it on a grey."

    menu:
        "\"I'll sit for a bit.\"":
            jump zoe_outdoor_stay
        "\"I'll leave you to it.\"":
            jump zoe_outdoor_go


label zoe_outdoor_stay:
    mc "I'll sit for a bit."
    show zoe_beach_neutral at sprite_r, react_nod
    z "Suit yourself. Fair warning: I'm not going to be good company. I'm going to be squinting."
    "She squints. You sit. For half an hour the conversation is mostly about how much the wind is a problem for anybody with paper."
    $ spend_time(0.5)
    if npc_rel("zoe", "familiarity") >= 30:
        # Only counts as time together once she's comfortable enough for it to
        # be time together rather than time near each other.
        $ apply_relationship_change(
            "zoe",
            source_id="zoe_outdoor_beat",
            source_category="casual_talk",
            familiarity=2,
        )
        show zoe_beach_laugh at sprite_r
        z "Same time next weekend, probably. I'll still be losing."
    else:
        "By the time you stand up she's stopped narrating and started actually working. You take that as the exit cue."
    jump zoe_outdoor_exit


label zoe_outdoor_go:
    mc "I'll leave you to it."
    show zoe_beach_neutral at sprite_r, react_nod
    z "Good instinct."
    # No penalty. Nothing was asked for.
    jump zoe_outdoor_exit


label zoe_outdoor_exit:
    hide zoe_beach_neutral
    hide zoe_beach_talk
    hide zoe_beach_laugh
    $ story_scene_active = False
    $ set_hud("full")
    jump location_sandbeach


# ── BEAT 2 — Zoe: walk with me? ──────────────────────────────────────────────
label zoe_walk_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_walk")
    $ _zf = npc_rel("zoe", "familiarity")
    scene parkday
    show screen hud
    hide screen people_here_dock

    show zoe_street_neutral at sprite_r
    "Zoe is already standing, bag over one shoulder, like she'd decided to leave several minutes ago and hasn't got round to it."
    show zoe_street_talk at sprite_r, react_lean_in
    z "Perfect. I need to walk and I need to not be alone with my own opinions. Come round the long way?"
    mc "How long is the long way?"
    show zoe_street_laugh at sprite_r
    z "Half an hour. Forty if I'm being annoying about a tree."

    if store.skill_art >= 2:
        show zoe_street_talk at sprite_r, react_nod
        z "And you'll actually get why I'm being annoying about the tree, which is worse for both of us."

    menu:
        "\"Alright. Long way.\"":
            jump zoe_walk_yes
        "\"Another time — I've got things.\"":
            jump zoe_walk_no


label zoe_walk_yes:
    mc "Alright. Long way."
    show zoe_street_laugh at sprite_r, react_bounce
    z "Excellent. You've made a mistake and I respect it."
    "The long way turns out to be a loop she's clearly done a hundred times, narrated like a tour of things that have personally disappointed her."
    "Somewhere near the end she stops narrating, which is somehow the friendlier half."
    $ spend_time(0.5)
    $ apply_relationship_change(
        "zoe",
        source_id="zoe_walk_beat",
        source_category="shared_activity",
        familiarity=2,
        affection=1,
    )
    jump zoe_walk_exit


label zoe_walk_no:
    mc "Another time — I've got things."
    show zoe_street_neutral at sprite_r, react_nod
    z "Fine. I'll be annoying about the tree on my own."
    # No penalty — she was offering, not asking.
    jump zoe_walk_exit


label zoe_walk_exit:
    hide zoe_street_neutral
    hide zoe_street_talk
    hide zoe_street_laugh
    $ story_scene_active = False
    $ set_hud("full")
    jump location_park


# ── BEAT 3 — Eli: quick favour ───────────────────────────────────────────────
label eli_favor_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("eli_favor")
    scene libraryday
    show screen hud
    hide screen people_here_dock

    show eli_neutral at sprite_r
    "Eli is standing at the end of the stacks with one headphone off, which for her is roughly the body language of a flare gun."
    show eli_talk at sprite_r, react_lean_in
    eli "Hey. Can I borrow a brain for ninety seconds? Mine's been in the same argument since eleven."
    mc "Go ahead."

    if store.skill_prog >= 3:
        show eli_talk at sprite_r
        eli "Two ways to do the same thing. One's shorter and I can't explain it to anyone. One's longer and boring and everybody understands it instantly."
        eli "I keep picking the short one and then defending it for an hour, which is not, mathematically, shorter."
        menu:
            "\"Boring one. You already know.\"":
                mc "Boring one. You already know."
                show eli_laugh at sprite_r, react_bounce
                eli "I did know. I wanted someone else to say it so I could be annoyed at them instead of me."
                $ apply_relationship_change(
                    "eli",
                    source_id="eli_favor_beat",
                    source_category="helping_npc",
                    trust=2,
                    familiarity=1,
                )
            "\"Keep the clever one and write down why.\"":
                mc "Keep the clever one. Just write down why, next to it."
                show eli_talk at sprite_r, react_nod
                eli "...That's irritatingly reasonable. The explaining was the whole cost and I never thought about paying it once."
                $ apply_relationship_change(
                    "eli",
                    source_id="eli_favor_beat",
                    source_category="competence_display",
                    respect=3,
                    familiarity=1,
                )
    else:
        show eli_talk at sprite_r
        eli "If you've read something twice and it still doesn't land — is that the writing, or is that you?"
        mc "Depends how good you were feeling before you started."
        show eli_talk at sprite_r, react_nod
        eli "Hm."
        menu:
            "\"It's the writing. Move on.\"":
                mc "It's the writing. Move on."
                show eli_laugh at sprite_r
                eli "Permission granted by an outside party. That's all I needed, honestly."
                $ apply_relationship_change(
                    "eli",
                    source_id="eli_favor_beat",
                    source_category="helping_npc",
                    trust=2,
                    familiarity=1,
                )
            "\"Read it out loud once.\"":
                mc "Read it out loud once. If it survives your own voice it's fine."
                show eli_talk at sprite_r, react_nod
                eli "That's a horrible test and I'm going to use it forever."
                $ apply_relationship_change(
                    "eli",
                    source_id="eli_favor_beat",
                    source_category="helping_npc",
                    trust=1,
                    respect=2,
                    familiarity=1,
                )

    show eli_neutral at sprite_r
    eli "Okay. Headphone's going back on. Thank you."
    $ spend_time(0.5)
    hide eli_neutral
    hide eli_talk
    hide eli_laugh
    $ story_scene_active = False
    $ set_hud("full")
    jump location_library


# ── BEAT 4 — Eli: after your shift? ──────────────────────────────────────────
label eli_after_shift_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("eli_after_shift")
    scene hub_day
    show screen hud
    hide screen people_here_dock

    show eli_neutral at sprite_r
    "She's at the wrong end of the floor for her own work, holding a coffee she clearly bought as a reason to be standing there."
    show eli_talk at sprite_r, react_lean_in
    eli "You're here all day, right? The whole eight?"
    mc "That's the arrangement."
    show eli_talk at sprite_r
    eli "Right. So — after. Are you a person who does anything after, or does the day just end?"

    menu:
        "\"I could do something after.\"":
            mc "I could do something after."
            show eli_laugh at sprite_r, react_bounce
            eli "Noted. Not a plan. I'm bad at plans, they make me want to cancel them."
            eli "But noted."
            # Deliberately no commitment: add_commitment() would create a hard
            # obligation the player never agreed to. Social acknowledgement only.
            $ apply_relationship_change(
                "eli",
                source_id="eli_after_shift_beat",
                source_category="casual_talk",
                familiarity=2,
            )
        "\"Today the day just ends.\"":
            mc "Today? The day just ends."
            show eli_talk at sprite_r, react_nod
            eli "Honest. Fine. I'll ask on a better day."
            # No penalty — nothing was promised.

    show eli_neutral at sprite_r
    "She takes the coffee back to her own end of the floor at a speed that suggests she's finished the part she'd rehearsed."
    hide eli_neutral
    hide eli_talk
    hide eli_laugh
    $ story_scene_active = False
    $ set_hud("full")
    jump location_hub


# ── BEAT 5 — Marcus: pace the last loop ──────────────────────────────────────
label marcus_park_favor_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("marcus_park_favor")
    scene parkday
    show screen hud
    hide screen people_here_dock

    show marcus_park_neutral at sprite_r
    "Marcus is walking it off at the top of the path, hands on his head, breathing like a man who has made a decision he regrets."
    show marcus_park_talk at sprite_r, react_lean_in
    m "Hey. Do me a favour. Run the last loop with me."
    mc "Why?"
    show marcus_park_talk at sprite_r
    m "Because on my own I'm going to call it here and pretend I did four."

    if store.skill_fit >= 3:
        show marcus_park_laugh at sprite_r, react_bounce
        m "And you'll make it easy, which is insulting, but I'll take it."

    menu:
        "\"One loop.\"":
            jump marcus_park_favor_yes
        "\"I've got my own thing to do.\"":
            jump marcus_park_favor_no


label marcus_park_favor_yes:
    mc "One loop."
    show marcus_park_neutral at sprite_r, react_nod
    m "One loop."
    "It is not a conversation. It's twenty minutes of two people not being the first to slow down, which is apparently its own kind of talking."
    show marcus_park_laugh at sprite_r
    m "Four. Officially four."
    $ spend_time(20 / 60.0)
    $ store.need_energy = max(0, store.need_energy - 4)
    $ apply_relationship_change(
        "marcus",
        source_id="marcus_park_favor_beat",
        source_category="shared_activity",
        familiarity=2,
        affection=1,
    )
    jump marcus_park_favor_exit


label marcus_park_favor_no:
    mc "I've got my own thing to do."
    show marcus_park_neutral at sprite_r, react_nod
    m "Fair. I'll lie to myself about it later."
    # No penalty.
    jump marcus_park_favor_exit


label marcus_park_favor_exit:
    hide marcus_park_neutral
    hide marcus_park_talk
    hide marcus_park_laugh
    $ story_scene_active = False
    $ set_hud("full")
    jump location_park


# ── BEAT 6 — Marcus: one game ────────────────────────────────────────────────
label marcus_one_game_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("marcus_one_game")
    $ _beaten_marcus = "marcus_pool" in store.bar_first_wins
    scene bar
    show screen hud
    hide screen people_here_dock

    show marcus_bar_normal at sprite_r
    "Marcus racks the balls with the specific efficiency of a man who is technically still working."
    show marcus_bar_talk at sprite_r, react_lean_in

    if _beaten_marcus:
        m "There he is. You know I've thought about that game more than is healthy."
        mc "You brought it up, not me."
        show marcus_bar_talk at sprite_r, react_nod
        m "One game. I've got twenty minutes and a grudge."
    else:
        m "One game. Table's free and I'm bored of my own bar."
        mc "Just one?"
        show marcus_bar_talk at sprite_r, react_nod
        m "That's what everyone says."

    menu:
        "\"Rack them.\"":
            mc "Rack them."
            show marcus_bar_normal at sprite_r
            m "Money on the table first. House rule. My house."
            hide marcus_bar_normal
            hide marcus_bar_talk
            $ story_scene_active = False
            $ set_hud("full")
            # Resolved by the real bar-games system, not a bespoke roll.
            call bar_game_play("pool", "pool_marcus")
            jump location_bar
        "\"Not tonight.\"":
            mc "Not tonight."
            show marcus_bar_normal at sprite_r, react_nod
            m "Table'll be here."
            # No penalty.
            hide marcus_bar_normal
            hide marcus_bar_talk
            $ story_scene_active = False
            $ set_hud("full")
            jump location_bar


# ── BEAT 7 — Nora: you look exhausted ────────────────────────────────────────
label nora_exhausted_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("nora_exhausted")
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock

    show nora_cafe_normal at sprite_r
    "You get about as far as ordering before she puts the cup down and just looks at you."
    show nora_cafe_talk at sprite_r, react_lean_in
    n "Okay. What's happening to you."
    mc "Nothing's happening to me."
    show nora_cafe_sad at sprite_r, react_sigh
    n "You've got the face people have in here at six in the morning. It's not six in the morning."
    # She is a barista, not a mechanic: no energy restoration here by design.
    n "I'd offer you a triple, but honestly at this point that's just being cruel with extra steps."

    menu:
        "\"It's been a long stretch.\"":
            mc "It's been a long stretch. It'll ease off."
            show nora_cafe_talk at sprite_r, react_nod
            n "That's what I said for about two years."
            n "For what it's worth: it does ease off. It just doesn't ease off because you decided it should."
            $ apply_relationship_change(
                "nora",
                source_id="nora_exhausted_beat",
                source_category="meaningful_talk",
                trust=3,
                familiarity=1,
            )
        "\"I'm fine.\"":
            mc "I'm fine."
            show nora_cafe_normal at sprite_r, react_shake
            n "Sure."
            n "Well. The chairs are free and nobody's counting how long you sit in one."
            $ apply_relationship_change(
                "nora",
                source_id="nora_exhausted_beat",
                source_category="casual_talk",
                familiarity=1,
            )
        "\"Say the thing you're clearly about to say.\"":
            mc "Say the thing you're clearly about to say."
            show nora_cafe_laugh at sprite_r, react_bounce
            n "Go home. Eat something that isn't from here. That's the whole speech."
            show nora_cafe_talk at sprite_r
            n "I've given it to about forty people. You're the first one who asked for it."
            $ apply_relationship_change(
                "nora",
                source_id="nora_exhausted_beat",
                source_category="meaningful_talk",
                trust=2,
                familiarity=2,
            )

    scene expression cafe_bg()
    show screen hud
    $ story_scene_active = False
    $ set_hud("full")
    jump cafe_actions


# ── BEAT 8 — Nora: walking out together ──────────────────────────────────────
label nora_walk_out_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("nora_walk_out")
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock

    show nora_cafe_normal at sprite_r
    "She's already got her coat over the back of a chair and the apron half untied — the last ten minutes of a shift, where nobody does any work."
    show nora_cafe_talk at sprite_r, react_nod
    n "You've got about eight minutes of me and then I turn into a person who does not work here."
    mc "What happens then?"
    show nora_cafe_laugh at sprite_r
    n "I walk to the crossing and complain about the bus. It's a whole thing."

    menu:
        "\"I'm going that way anyway.\"":
            mc "I'm going that way anyway."
            show nora_cafe_talk at sprite_r, react_nod
            n "Then you're getting the bus complaint. That's the deal, I don't make the rules."
            "You end up at the crossing together at eighteen minutes past, which is late enough that the complaint has real feeling in it."
            "She goes left. You don't. That's the whole thing."
            $ spend_time(0.5)
            $ apply_relationship_change(
                "nora",
                source_id="nora_walk_out_beat",
                source_category="casual_talk",
                familiarity=2,
                affection=1,
            )
        "\"I'll let you get out of here.\"":
            mc "I'll let you get out of here."
            show nora_cafe_normal at sprite_r, react_nod
            n "Appreciated. Genuinely — the eight minutes are the worst part."
            # No penalty.

    scene expression cafe_bg()
    show screen hud
    $ story_scene_active = False
    $ set_hud("full")
    jump cafe_actions


# ── BEAT 9 — Marcus + Zoe: already here ──────────────────────────────────────
label marcus_zoe_bar_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("marcus_zoe_bar")
    scene bar
    show screen hud
    hide screen people_here_dock

    show marcus_bar_talk at sprite_r
    show zoe_street_talk at sprite_l
    # They finish the sentence before they notice MC — the point of the beat.
    m "— no, because the second you charge for it, it's a job. That's not a bad thing. That's just what it is."
    show zoe_street_angry at sprite_l, react_shake
    z "It's a bad thing when you say it like that. You say it like it's a diagnosis."
    show marcus_bar_talk at sprite_r
    m "I'm a bartender. Everything I say sounds like a diagnosis."
    show zoe_street_talk at sprite_l
    z "You could stop."
    show marcus_bar_normal at sprite_r, react_step_back
    m "...Oh. Hey."
    show zoe_street_neutral at sprite_l, react_nod
    z "You're a witness now. Sorry. It's mostly his fault."

    menu:
        "\"Go on then. Both of you.\"":
            jump marcus_zoe_bar_join
        "\"I'll leave you two to it.\"":
            jump marcus_zoe_bar_pass


label marcus_zoe_bar_join:
    mc "Go on then. Both of you."
    show marcus_bar_talk at sprite_r, react_lean_in
    m "Right. She sells one painting and now money's a moral problem."
    show zoe_street_laugh at sprite_l, react_bounce
    z "One painting is data."
    m "One painting is one painting."
    "It goes on for half an hour and doesn't resolve, which appears to be the format. Neither of them looks like they want it to."
    $ spend_time(0.5)
    $ apply_relationship_change(
        "marcus",
        source_id="marcus_zoe_bar_beat",
        source_category="casual_talk",
        familiarity=2,
    )
    $ apply_relationship_change(
        "zoe",
        source_id="marcus_zoe_bar_beat",
        source_category="casual_talk",
        familiarity=2,
    )
    jump marcus_zoe_bar_exit


label marcus_zoe_bar_pass:
    mc "I'll leave you two to it."
    show zoe_street_talk at sprite_l, react_nod
    z "Coward."
    show marcus_bar_talk at sprite_r
    m "Smart man."
    # No penalty either way.
    jump marcus_zoe_bar_exit


label marcus_zoe_bar_exit:
    hide marcus_bar_normal
    hide marcus_bar_talk
    hide zoe_street_neutral
    hide zoe_street_talk
    hide zoe_street_laugh
    hide zoe_street_angry
    $ story_scene_active = False
    $ set_hud("full")
    jump location_bar


# ── BEAT 10 — Zoe + Nora: cross-thread at the café ───────────────────────────
label cross_zoe_nora_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("cross_zoe_nora")
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock

    show nora_cafe_talk at sprite_r
    show zoe_street_talk at sprite_l
    # Mid-conversation. Two regulars of the same café — no invented history.
    n "— all I'm saying is you've been ordering the same thing for four months and telling me you're experimenting."
    show zoe_street_laugh at sprite_l, react_bounce
    z "I'm experimenting with commitment."
    show nora_cafe_laugh at sprite_r
    n "That's the most artist thing anyone's said to me at this counter."
    show zoe_street_neutral at sprite_l, react_step_back
    z "Oh — hey. She's bullying me."
    show nora_cafe_talk at sprite_r, react_nod
    n "I'm doing customer service."

    menu:
        "\"Pull up a stool.\"":
            mc "Room for one more?"
            show nora_cafe_talk at sprite_r, react_nod
            n "There's always room, that's the tragedy of a Wednesday."
            "Twenty-five minutes of nothing in particular: the same order, the bus, a man outside who has been on the phone since before you arrived."
            "Nora keeps working the whole time and somehow stays in the conversation. Zoe doesn't order anything different."
            $ spend_time(0.5)
            $ apply_relationship_change(
                "nora",
                source_id="cross_zoe_nora_beat",
                source_category="casual_talk",
                familiarity=2,
            )
            $ apply_relationship_change(
                "zoe",
                source_id="cross_zoe_nora_beat",
                source_category="casual_talk",
                familiarity=2,
            )
        "\"Don't let me interrupt.\"":
            mc "Don't let me interrupt."
            show zoe_street_talk at sprite_l, react_nod
            z "Too late, but appreciated."
            # No penalty.

    scene expression cafe_bg()
    show screen hud
    $ story_scene_active = False
    $ set_hud("full")
    jump cafe_actions
