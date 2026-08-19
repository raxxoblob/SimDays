# ═══════════════════════════════════════════════════════════════════════════
# STORY / DIRECTING PASS — ZOE + MARCUS
# ═══════════════════════════════════════════════════════════════════════════
# Technical implementation of an authored screenplay. NOTHING here invents a
# system. Every scene hangs off a mechanism that already shipped:
#
#   beach first meeting     locations.rpy  beach_meet_zoe (this file adds ONE
#                           extra route in front of the two existing ones)
#   zoe beat dispatch       zoe_arc.rpy    zoe_arc_beat_for (wrapped, same
#                           interception pattern zoe_onboarding.rpy uses)
#   pre-Talk initiation     interact.rpy   _check_talk_followup (wrapped, same
#                           pattern zoe_arc / zoe_onboarding / marcus_onboarding
#                           / relationship_continuity all use)
#   topic arc selection     interact.rpy   check_arc (wrapped — knowledge gating)
#   bar scene priority      locations.rpy  location_bar, in front of
#                           check_marcus_zoe_bar (the REPEATABLE ambient version)
#   relationship axes       npc_relationships.rpy apply_relationship_change
#   beat cooldowns          location_beats_tier_a.rpy _beat_cooldown_ok
#   old-save backfill       config.after_load_callbacks (zoe_onboarding.rpy owns
#                           `label after_load:` — this file must not redefine it)
#
# ZERO new art: existing zoe_beach_1..7 CGs, existing `bar` / cafe / park
# backgrounds, existing Zoe + Marcus sprites and speaker-turn transforms.
#
# CANON THIS PASS IS BUILT ON
#   Marcus bartender, runs Static   location_beats_tier_a.rpy:911
#   Marcus never at the gym         location_beats_tier_a.rpy:34
#   Marcus wakes at five/six        arcs.rpy arc_marcus_sports_1
#   Marcus basketball offer at 18   arcs.rpy arc_marcus_sports_2
#   Zoe + Marcus, three years       zoe_onboarding.rpy:253
#   Zoe in Static Saturdays 19-24   npc_schedules.rpy
#   Zoe bad typography / posters    zoe_arc.rpy zoe_msg_poster, rc_zoe_micro_sign
#
# ponytail: the four Talk-initiated one-shots below are dispatched from ONE
# _check_talk_followup wrapper with a fixed priority order rather than a
# weighted pool. Ceiling: if this list grows past ~6 entries the ordering
# becomes hard to reason about. Upgrade path — move them into a
# (flag, label, cond) table and sort it the way MARCUS_BEATS already does.
# ═══════════════════════════════════════════════════════════════════════════

# ── Part 5: Marcus, why I stayed ────────────────────────────────────────────
default marcus_why_stayed_done        = False
default marcus_bball_offer_day        = -1     # stamped by arc_marcus_sports_2

# ── Part 6/7: the Static group scene and its two callbacks ──────────────────
default marcus_zoe_static_scene_done  = False
default marcus_zoe_static_day         = -1
default sd_marcus_static_cb_done      = False
default sd_zoe_static_cb_done         = False

# ── Part 8: Zoe disagreement + repair ───────────────────────────────────────
default zoe_disagreement_done         = False
default zoe_disagreement_day          = -1
default zoe_disagreement_repair_done  = True   # True == nothing owed

# ── Part 2: Wednesday first occurrence ──────────────────────────────────────
default zoe_wednesday_first_done      = False

# ── Part 3: coffee callback ─────────────────────────────────────────────────
default zoe_coffee_callback_pending   = False

# ── Old-save migration ──────────────────────────────────────────────────────
default sd_backfilled                 = False
# Story-canon consolidation pass — its own guard, see _sd_backfill().
default sc_backfilled                 = False

# ── Scratch (rollback-safe) ─────────────────────────────────────────────────
default _zw1_silence                  = False
default _zd_back                      = "location_cafe"


# init 9: after marcus_onboarding (5/6), zoe_onboarding (4), zoe_arc (2/3) and
# relationship_continuity (7/8), so every wrapper below sits on top of all four.
init 9 python:

    # Emotional Zoe beats that must not stack. Same dict the Tier A pack and
    # zoe_arc both already stamp — no second cooldown store.
    _SD_ZOE_HEAVY = ("zoe_coffee", "zoe_not_ready", "zoe_deadline",
                     "zoe_after_deadline", "zoe_just_stay")

    def _sd_zoe_heavy_gap():
        """Days since the most recent substantial emotional Zoe scene."""
        last = max([store.tier_a_beat_last_day.get(b, -999)
                    for b in _SD_ZOE_HEAVY] + [-999])
        return store.day - last

    def _sd_quiet():
        return not bool(store.story_scene_active)

    def _sd_stage(npc_id):
        try:
            return npc_relationship_stage(npc_id)
        except Exception:
            return "stranger"

    # ── Part 5 eligibility ───────────────────────────────────────────────────
    # Requires: the offer is already on the table (arc_marcus_sports_2), earned
    # Trust/Familiarity, 3+ days since the two other Marcus vulnerability beats,
    # and a quiet context.
    def sd_marcus_why_stayed_ok():
        if store.marcus_why_stayed_done:
            return False
        if not store.mc_knows_marcus_bball_offer:
            return False
        if not _sd_quiet():
            return False
        if _sd_stage("marcus") not in ("friend", "close", "trusted"):
            return False
        if npc_trust("marcus") < 35:
            return False
        # 3+ days after "could've left" (the offer itself) ...
        if store.marcus_bball_offer_day >= 0 and store.day - store.marcus_bball_offer_day < 3:
            return False
        # ... and after "still alive", the other early Marcus opener.
        if store.day - store.tier_a_beat_last_day.get("marcus_fr_still_alive", -999) < 3:
            return False
        return True

    # ── Part 6 eligibility ───────────────────────────────────────────────────
    # Static, the evening window Zoe and Marcus actually share (npc_schedules:
    # zoe bar Sat 19-24, inside Marcus's Sat 15-27 shift). One-shot, and it
    # takes priority over the REPEATABLE marcus_zoe_bar_scene at the same slot.
    def check_marcus_zoe_static_group():
        if store.marcus_zoe_static_scene_done:
            return False
        if not (store.marcus_met and store.zoe_properly_introduced):
            return False
        if not npc_here("marcus", "location_bar"):
            return False
        if not npc_here("zoe", "location_bar"):
            return False
        if not (19.0 <= float(store.hour) < 24.0):
            return False
        # Both established: Marcus a friend, Zoe past the acquaintance band.
        if _sd_stage("marcus") not in ("friend", "close", "trusted"):
            return False
        if _sd_stage("zoe") in ("stranger", "known"):
            return False
        if not _beat_global_ok():
            return False
        return True

    # ── Part 8 eligibility ───────────────────────────────────────────────────
    # Higher gate than rc_zoe_friction_reads_harsh (which is a stranger-to-
    # acquaintance misread). This one needs the relationship to be comfortable
    # enough that disagreeing is safe, and it never lands on an emotional day.
    def sd_zoe_disagreement_ok(loc):
        if store.zoe_disagreement_done:
            return False
        if not store.zoe_met:
            return False
        if loc not in ("location_cafe", "location_park"):
            return False
        if _sd_stage("zoe") not in ("friend", "close", "trusted"):
            return False
        if npc_rel("zoe", "familiarity") < 45:
            return False
        if _sd_zoe_heavy_gap() < 2:
            return False
        return True

    # ── Zoe beat selector wrapper ────────────────────────────────────────────
    # The original keeps absolute priority; this only ever adds a beat the
    # original just declined.
    _zoe_arc_beat_for_pre_sd = zoe_arc_beat_for

    def zoe_arc_beat_for(loc):
        result = _zoe_arc_beat_for_pre_sd(loc)
        if result is not None:
            return result
        if not npc_here("zoe", loc):
            return None
        if not _beat_global_ok():
            return None
        if sd_zoe_disagreement_ok(loc):
            return "zoe_small_disagreement"
        return None

    # ── Talk-initiated one-shots ─────────────────────────────────────────────
    _check_talk_followup_pre_sd = _check_talk_followup

    def _check_talk_followup(npc_id):
        # Part 9: retire any topic arc whose fact an authored scene already
        # delivered. Statement context, once per Talk — see the note on
        # _SD_ARC_FACT_GATE below for why this is not a check_arc wrapper.
        sd_retire_known_arcs(npc_id)
        result = _check_talk_followup_pre_sd(npc_id)
        # The zoe_arc wrapper always answers "zoe_thread_talk" for Zoe, so the
        # Zoe entries below have to sit IN FRONT of the chain, not behind it.
        if npc_id == "zoe" and store.zoe_met:
            if (not store.zoe_disagreement_repair_done
                    and store.zoe_disagreement_day >= 0
                    and 1 <= store.day - store.zoe_disagreement_day <= 3):
                return "zoe_disagreement_repair"
            if (store.marcus_zoe_static_scene_done and not store.sd_zoe_static_cb_done
                    and store.marcus_zoe_static_day >= 0
                    and store.day - store.marcus_zoe_static_day >= 3):
                return "sd_zoe_static_callback"
        if result is not None:
            return result
        if npc_id == "marcus" and store.marcus_met:
            if (store.marcus_zoe_static_scene_done and not store.sd_marcus_static_cb_done
                    and store.marcus_zoe_static_day >= 0
                    and store.day - store.marcus_zoe_static_day >= 3):
                return "sd_marcus_static_callback"
            if sd_marcus_why_stayed_ok():
                return "marcus_why_stayed_scene"
        return None

    # ── Part 9: knowledge gating for the generic topic arcs ──────────────────
    # A topic arc must never re-reveal a fact an AUTHORED scene already
    # delivered. Retiring the stage (rather than editing its dialogue) means the
    # generic do_talk ambient line fires instead — no second version of the
    # reveal exists to drift out of sync.
    #
    # marcus_sports_2 is keyed on marcus_why_stayed_done, NOT on
    # mc_knows_marcus_bball_offer: sports_2 is what SETS that flag, so gating on
    # it would retire the arc before it ever ran.
    #
    # check_arc() itself is deliberately NOT wrapped: interact.rpy:1971 calls it
    # inside the npc_topics vpgrid, i.e. during screen render, where a state
    # write would run on every re-render. Instead the retirement happens once
    # per Talk press, in the _check_talk_followup wrapper above — which is the
    # last statement-context code that runs before the topic screen can open.
    _SD_ARC_FACT_GATE = {
        # Story-canon consolidation: art_2 now only DISCOVERS the gallery
        # ambition, which zoe_not_ready_scene also does (and better), so it is
        # gated on the same fact. Retiring a stage still marks it done, so
        # art_3 downstream of it stays reachable.
        "zoe":    {"zoe_art_2":   "knows_zoe_gallery_goal",     # gallery ambition
                   "zoe_art_3":   "knows_zoe_funding_problem",  # funding pressure
                   "zoe_music_2": "knows_zoe_bass_history"},    # bass history
        # father / why he stayed. NOT keyed on mc_knows_marcus_bball_offer:
        # sports_2 is what SETS that flag, so gating on it would retire the arc
        # before it ever ran.
        "marcus": {"marcus_sports_2": "marcus_why_stayed_done"},
    }

    def sd_retire_known_arcs(npc_id):
        """Idempotent. A topic arc must never re-reveal a fact an AUTHORED scene
        already delivered; retiring the stage (rather than editing its dialogue)
        means the generic do_talk ambient line fires instead, so no second
        version of the reveal exists to drift out of sync."""
        gates = _SD_ARC_FACT_GATE.get(npc_id)
        if not gates:
            return
        d = None
        for arc_id, fact in gates.items():
            if getattr(store, fact, False) and not store.topic_arc_done.get(arc_id):
                if d is None:
                    d = dict(store.topic_arc_done)
                d[arc_id] = True
        if d is not None:
            store.topic_arc_done = d

    # ── Old-save backfill ────────────────────────────────────────────────────
    def _sd_backfill():
        """Idempotent, runs on every load.

        The one thing that MUST be migrated: a save that already completed
        arc_marcus_sports_2 heard the old inline "My dad was sick" reveal, so
        marcus_why_stayed_scene — whose whole premise is that he never told MC —
        would be a continuity error. Those saves are marked done."""
        # ── Story-canon consolidation migration ─────────────────────────────
        # Own guard flag: saves made after the first _sd_backfill already have
        # sd_backfilled=True, so this block cannot hang off it.
        if not store.sc_backfilled:
            store.sc_backfilled = True
            done = store.topic_arc_done
            # Old art_3 delivered the funding rejection inline.
            if done.get("zoe_art_3", False):
                store.zoe_funding_application_known = True
                store.knows_zoe_funding_problem = True
                store.zoe_grant_discussed = True
                if not store.zoe_coffee_done:
                    # Coffee is now the first reveal of a rejection this save
                    # has already heard. Retire it rather than replay it.
                    store.zoe_coffee_done = True
            # Old music_2 delivered the whole bass history. _zoe_sync_knowledge
            # no longer derives it (that would break the fresh-save path), so
            # this is now the only migration point for it.
            if done.get("zoe_music_2", False):
                store.zoe_bass_hint_known = True
                store.knows_zoe_bass_history = True
            # Old food_2 delivered the notepad, the mother and the 200 times.
            if done.get("marcus_food_2", False):
                store.mc_knows_marcus_chili_family_recipe = True
                store.marcus_notepad_done = True
        if store.sd_backfilled:
            return
        store.sd_backfilled = True
        if store.topic_arc_done.get("marcus_sports_2"):
            store.marcus_why_stayed_done = True
            if store.marcus_bball_offer_day < 0:
                store.marcus_bball_offer_day = store.day
        # A save deep enough to have run the repeatable Wednesday beat has
        # already had its ordinary afternoon — the first-occurrence variant
        # would read as a step backwards.
        if store.tier_a_beat_last_day.get("zoe_wednesday", -999) >= 0:
            store.zoe_wednesday_first_done = True
        # An old save may already know a fact through an AUTHORED scene while
        # the matching topic arc is still on the menu. Retire it now rather than
        # waiting for the next Talk.
        try:
            _zoe_sync_knowledge()
        except Exception:
            pass
        sd_retire_known_arcs("zoe")
        sd_retire_known_arcs("marcus")

    try:
        if _sd_backfill not in config.after_load_callbacks:
            config.after_load_callbacks.append(_sd_backfill)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — ZOE, FIRST BEACH INTRO (Marcus route)
# ═══════════════════════════════════════════════════════════════════════════
# The two existing routes (zoe_beach_approach / zoe_beach_watch) are the
# cold-discovery meeting and are NOT touched. This is the third route, and it
# is the one that fires when Marcus actually named her on move-in day, which is
# what the screenplay's opening line requires.
#
# It does NOT call zoe_beach_intro_tail: the tail's Marcus recognition, the
# page-underneath moment and the contact exchange are all present in this
# screenplay, so calling it would play each of them twice. The flag writes the
# tail owns are performed here instead, through the same single write point
# (_zoe_mark_introduced).
#
# SCRIPT GAP: `mc_arrival_intent` does not exist anywhere in the project, so
# the two-way career/unsure branch cannot be state-driven. The screenplay's
# own "unsure" branch is used as the neutral fallback.
label zoe_beach_marcus_intro:
    scene zoe_beach_1 with dissolve
    show screen hud
    hide screen people_here_dock
    scene zoe_beach_2 with dissolve
    show screen hud
    scene zoe_beach_3 with dissolve
    show screen hud

    mc "Zoe?"
    z "Depends."
    mc "On what?"
    z "Who's asking."
    mc "Marcus said you'd probably be here."
    z "There it is."
    mc "There what is?"
    z "Marcus."
    z "He does this."
    mc "Does what?"
    z "Introduces people who aren't in the same room."
    mc "He said you sketch here."
    z "That's somehow worse."
    mc "Why?"
    z "Now I sound predictable."
    mc "You are here."
    z "Don't help him."

    # [Zoe looks back toward what she is drawing]
    scene zoe_beach_4 with dissolve
    show screen hud

    mc "What are you working on?"
    z "Trying to decide whether that building is ugly or just unfortunate."
    mc "There's a difference?"
    z "Huge difference."
    mc "Which is it?"
    z "Ugly."
    mc "That was fast."
    z "I've been here twenty minutes."

    menu:
        "Ask to see the sketch.":
            mc "Can I see?"
            z "You can."
            z "Whether I'm going to show you is a separate question."
            mc "Right."
            z "You learn quickly."
            $ zoe_first_impression = "curious"
            $ _zoe_rel("zoe_intro", affection=1, familiarity=3)
        "Look at the building instead.":
            mc "I think the sign is worse."
            z "..."
            z "Okay."
            mc "What?"
            z "Nothing."
            z "You actually looked."
            $ zoe_first_impression = "observant"
            $ _zoe_rel("zoe_intro", affection=1, respect=1, familiarity=3)
        "Admit you know nothing about art.":
            mc "I should probably warn you I know nothing about art."
            z "Good."
            mc "Good?"
            z "People who know nothing usually say that."
            z "People who know a little explain perspective to me."
            $ zoe_first_impression = "honest"
            $ _zoe_rel("zoe_intro", affection=1, respect=1, familiarity=2)

    mc "How do you know Marcus?"
    z "Unfortunately."
    mc "That sounds affectionate."
    z "Don't spread that around."
    mc "He called you his friend."
    z "Of course he did."
    mc "You're not?"
    z "I didn't say that."
    z "Marcus decides you're friends roughly fifteen minutes before you do."
    mc "That explains a lot."
    z "How long have you known him?"
    mc "Not long."
    z "Then you're probably already invited somewhere tonight."
    mc "He did mention the bar."
    z "See?"

    # [Zoe returns to drawing]
    scene zoe_beach_5 with dissolve
    show screen hud

    mc "You come here a lot?"
    z "Sometimes."
    z "People move differently when they think nobody's watching."
    mc "That sounds mildly threatening."
    z "It's drawing."
    mc "That's exactly what someone mildly threatening would call it."
    z "Marcus was right."
    mc "About what?"
    z "You'd probably be fine."

    # [Small pause. MC notices another page.]
    pause 0.5

    mc "That one's different."
    z "Which one?"
    mc "The one underneath."
    z "..."
    z "You weren't supposed to see that."
    mc "Sorry."
    z "It's fine."
    mc "Was it yours?"
    z "Technically all of these are mine."
    mc "You know what I meant."
    z "Yeah."

    # [Zoe closes the sketchbook. No anger. Just a boundary.]
    pause 0.5

    z "So."
    z "New in town?"
    mc "That obvious?"
    z "You still look at things."
    mc "People stop?"
    z "Mostly."
    z "Give it six months."

    # Neutral fallback — see the SCRIPT GAP note above.
    mc "Honestly, I'm still figuring out why I'm here."
    z "That's probably healthier than pretending you know."
    mc "You always this encouraging?"
    z "No."
    z "Enjoy it."

    mc "You ask everyone this many questions?"
    z "I think you're ahead."
    mc "Ahead of who?"
    z "Everyone else today."
    mc "High bar?"
    z "There was a man explaining NFTs to his girlfriend earlier."
    mc "I withdraw the question."

    z "I should finish this before the light changes."
    mc "Right."
    z "But..."
    mc "But?"
    z "If Marcus drags you to Static sometime, I'll probably be there."
    mc "Is that an invitation?"
    z "Absolutely not."
    mc "Good."
    z "Good."
    pause 0.5
    z "Maybe see you around."
    mc "Maybe."
    z "And don't tell Marcus he was right."
    mc "About me being fine?"
    z "Especially that."

    # ── Technical hooks. Identical set to zoe_beach_intro_tail's, minus the
    # dialogue it uses to deliver them (all of which is in the screenplay above).
    scene zoe_beach_6 with dissolve
    show screen hud
    scene zoe_beach_7 with dissolve
    show screen hud
    $ knows_zoe_art_interest = True
    $ add_relationship_memory("zoe", "zoe_first_beach", "The building that was ugly, not unfortunate")
    # Contact exchange + zoe_met + bootstrap start day, single write point.
    $ _zoe_mark_introduced("beach")
    $ spend_time(1)
    jump location_beach


# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — WEDNESDAY AT GROUNDS, FIRST OCCURRENCE
# ═══════════════════════════════════════════════════════════════════════════
# zoe_wednesday_grounds_scene (zoe_arc.rpy) is the REPEATABLE version and keeps
# its four-variant topic pool for every later Wednesday. This is the first one.
# Entered by a branch at the top of that label, so it shares its _beat_triggered
# stamp, its Grounds-routine counter and its exit.
#
# SCRIPT GAP: the "Tell her about MC's week" branch asks for a response driven
# by one existing player-state fact. No canonical Zoe line exists for that and
# authoring one is out of scope, so the branch plays its two authored lines and
# rejoins the scene.
#
# OMITTED: the "Marcus's taste in shirts" choice. Marcus has no clothing
# characterisation anywhere in the project (the only "shirt" strings are a
# wardrobe item id and festival staff), so the joke has no canon basis.
label zoe_wednesday_first_scene:
    $ zoe_wednesday_first_done = True
    show zoe_street_talk as focus_zoe at sprite_r

    z "You're early."
    mc "You said three."
    z "It's two fifty-six."
    mc "That's early?"
    z "For you? I don't know yet."
    mc "You've known me long enough to judge my punctuality?"
    z "I've known Marcus long enough to prepare for everyone."

    # [They sit]
    show zoe_street_neutral as focus_zoe at sprite_r

    mc "You working?"
    z "I was."
    mc "Past tense?"
    z "You sat down."
    mc "I can leave."
    z "I didn't say that."

    pause 0.5

    mc "What are you drinking?"
    z "Coffee."
    mc "Very descriptive."
    show zoe_street_laugh as focus_zoe at sprite_r
    z "It's brown and disappointing."
    mc "Why buy it?"
    show zoe_street_talk as focus_zoe at sprite_r
    z "Because sitting in a café with nothing looks like you're waiting for someone."
    mc "And?"
    z "I don't like looking like I'm waiting for someone."

    mc "You were waiting for me."
    show zoe_street_neutral as focus_zoe at sprite_r
    z "I was hoping you wouldn't notice that."
    mc "You literally told me to come."
    z "I know."
    z "It's been a long week."

    mc "Bad?"
    z "Not bad."
    z "Just..."
    z "Everyone wanted something."
    mc "And I don't?"
    z "You haven't yet."
    mc "That's a dangerous amount of faith."
    show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
    z "Don't make me regret it."

    $ _zw1_silence = False
    menu:
        "Ask about her week.":
            mc "What did everyone want?"
            show zoe_street_talk as focus_zoe at sprite_r
            z "Changes."
            z "Favors."
            z "Answers."
            z "A version of me with six additional hours in the day."
            mc "Could be useful."
            show zoe_street_laugh as focus_zoe at sprite_r
            z "I'd waste those too."
        "Tell her about your week.":
            mc "Mine wasn't exactly quiet either."
            show zoe_street_neutral as focus_zoe at sprite_r
            z "Yeah?"
        "Just sit for a minute.":
            $ _zw1_silence = True
            mc "We don't have to talk."
            show zoe_street_neutral as focus_zoe at sprite_r
            z "..."
            z "That's surprisingly appealing."

    if _zw1_silence:
        show zoe_street_talk as focus_zoe at sprite_r
        z "You know what's weird?"
        mc "We lasted fourteen seconds."
        show zoe_street_laugh as focus_zoe at sprite_r
        z "I didn't promise silence."
        mc "Fair."

    show zoe_street_talk as focus_zoe at sprite_r
    z "What's the worst thing you've seen in this city so far?"
    mc "Design-wise?"
    z "I didn't say design-wise."
    mc "You meant design-wise."
    z "Obviously."

    menu:
        "The casino exterior.":
            mc "Casino exterior."
            show zoe_street_talk as focus_zoe at sprite_r, react_nod
            z "Good answer."
            mc "Too easy?"
            z "Neon should require a license."
        "One of the downtown billboards.":
            mc "That giant billboard downtown."
            show zoe_street_talk as focus_zoe at sprite_r
            z "The blue one?"
            mc "Yeah."
            z "I've considered vandalism."

    show zoe_street_neutral as focus_zoe at sprite_r
    mc "You feeling better?"
    z "I wasn't feeling bad."
    mc "Right."
    z "..."
    z "A little."
    mc "Thought so."
    z "Don't be pleased with yourself."
    mc "Too late."
    show zoe_street_talk as focus_zoe at sprite_r
    z "Wednesday again?"
    mc "Is that a real invitation this time?"
    z "No."
    mc "Of course."
    z "Three."
    mc "Two fifty-six."
    show zoe_street_laugh as focus_zoe at sprite_r
    z "You're learning."

    $ _zoe_rel("zoe_wednesday", affection=1, familiarity=3)
    $ add_relationship_memory("zoe", "zoe_wednesday_first", "Two fifty-six at Grounds")
    # Shared routine — same counter guard the repeatable version uses, so one
    # afternoon can never be counted twice.
    if rc_zoe_grounds_count_day != day:
        $ rc_zoe_grounds_count_day = day
        $ zoe_grounds_count += 1
    $ spend_time(1.0)
    $ _zarc_dest = "location_cafe"
    jump zoe_arc_exit


# ═══════════════════════════════════════════════════════════════════════════
# PART 5 — MARCUS, WHY I STAYED
# ═══════════════════════════════════════════════════════════════════════════
# Dialogue-only, exactly like every marcus_friendship.rpy beat: it is reached
# through Talk, so the interaction UI owns the sprite and this can never
# contradict where Marcus actually is.
#
# arc_marcus_sports_2 now raises the offer and DEFLECTS ("It wasn't the right
# time."); this is the reveal. The knowledge gate in _SD_ARC_FACT_GATE retires
# sports_2 afterwards so the father can never be revealed twice.
label marcus_why_stayed_scene:
    $ marcus_why_stayed_done = True
    $ _do_talk_accounting("marcus")

    mc "Can I ask you something?"
    m "You just did."
    mc "You know what I mean."
    m "Yeah."
    mc "That basketball offer."
    m "What about it?"
    mc "You never actually told me why you stayed."
    m "Didn't I?"
    mc "You said it wasn't the right time."
    m "Sounds like me."
    mc "Marcus."
    m "..."
    m "My dad was sick."

    mc "Oh."
    m "Yeah."
    mc "Was it bad?"
    m "Bad enough."
    mc "So you stayed."
    m "There wasn't really a decision."
    mc "There was."
    m "Didn't feel like one."

    pause 0.5

    m "The offer wasn't some guaranteed career."
    m "It was a chance."
    m "Could've gone nowhere."
    mc "Still think about it?"
    m "Sometimes."

    mc "Last time you said no first."
    m "Did I?"
    mc "Then 'sometimes.'"
    m "Right."
    m "That's the official answer."
    mc "Which one?"
    m "Both."

    m "I don't regret staying."
    m "That's different from not wondering."
    mc "What do you think would've happened?"
    m "Depends on the day."
    m "Some days I'm obviously a star."
    mc "Obviously."
    m "Packed arenas."
    m "Terrible shoe deal."
    mc "Why terrible?"
    m "I have principles."
    mc "Sure."
    m "Other days I blow my knee out in week two and end up selling insurance."
    mc "Very specific."
    m "I've considered this."

    mc "You ever tell your dad?"
    m "Tell him what?"
    mc "That you still think about it."
    m "No."
    mc "Why?"
    m "Because he'd make it about him."
    mc "Wasn't it?"
    m "That's exactly why."

    m "Anyway."
    mc "You do that."
    m "Do what?"
    mc "Say something serious and then 'anyway.'"
    m "Useful word."
    mc "Cowardly word."
    m "Also useful."

    m "You playing another game or what?"
    mc "You changing the subject?"
    m "Aggressively."
    mc "Fine."
    m "Good."
    pause 0.5
    m "And hey."
    mc "Yeah?"
    m "Don't make it weird."
    mc "Wouldn't dream of it."
    m "Perfect."

    $ apply_relationship_change("marcus", source_id="marcus_why_stayed",
                                source_category="story_moment",
                                trust=3, familiarity=1)
    $ add_relationship_memory("marcus", "marcus_why_stayed", "Why he never took the offer")
    return


# ═══════════════════════════════════════════════════════════════════════════
# PART 6 — MC + MARCUS + ZOE AT STATIC
# ═══════════════════════════════════════════════════════════════════════════
# One-shot. Sits in FRONT of marcus_zoe_bar_scene (location_beats_tier_a.rpy),
# which is the repeatable ambient version of the same slot and continues to
# work afterwards. Existing `bar` background, existing sprites, no new CG.
label marcus_zoe_static_small_group:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("marcus_zoe_static")
    $ marcus_zoe_static_scene_done = True
    $ marcus_zoe_static_day = day
    scene bar
    show screen hud
    hide screen people_here_dock
    show marcus_bar_talk as focus_marcus at sprite_r
    show zoe_street_neutral as focus_zoe at sprite_l

    m "There he is."
    show zoe_street_talk as focus_zoe at sprite_l
    z "You said seven."
    mc "It is seven."
    z "He said seven."
    show marcus_bar_talk as focus_marcus at sprite_r, react_lean_in
    m "Why is everyone obsessed with numbers?"
    z "Because that's how time works."
    m "Debatable."

    # [MC sits]
    show marcus_bar_normal as focus_marcus at sprite_r

    mc "How long have you two been here?"
    show zoe_street_talk as focus_zoe at sprite_l
    z "Nine minutes."
    show marcus_bar_talk as focus_marcus at sprite_r
    m "She's been complaining for eight."
    z "He picked the table."
    mc "What's wrong with the table?"
    z "Nothing."
    m "See?"
    show zoe_street_angry as focus_zoe at sprite_l, react_shake
    z "The light is directly above us."
    m "Still nothing."
    z "You look like you're being interrogated."
    show marcus_bar_talk as focus_marcus at sprite_r, react_nod
    m "I look great."
    show zoe_street_talk as focus_zoe at sprite_l
    z "Those are separate statements."

    menu:
        "Side with Zoe.":
            mc "She's right. The light's terrible."
            show marcus_bar_talk as focus_marcus at sprite_r, react_step_back
            m "Unbelievable."
            show zoe_street_laugh as focus_zoe at sprite_l
            z "Thank you."
            show marcus_bar_talk as focus_marcus at sprite_r
            m "He knew you first."
            z "And yet."
        "Side with Marcus.":
            mc "It's a table."
            show zoe_street_angry as focus_zoe at sprite_l
            z "Both of you are exhausting."
            show marcus_bar_talk as focus_marcus at sprite_r, react_bounce
            m "We won."
            show zoe_street_talk as focus_zoe at sprite_l
            z "There wasn't a vote."
        "Refuse to choose.":
            mc "I'm staying out of this."
            show marcus_bar_talk as focus_marcus at sprite_r
            m "Coward."
            show zoe_street_talk as focus_zoe at sprite_l, react_nod
            z "Smart."

    show marcus_bar_talk as focus_marcus at sprite_r
    m "Tell him what you said about my playlist."
    show zoe_street_neutral as focus_zoe at sprite_l
    z "No."
    m "Because you know you were wrong."
    z "Because I already said it once."
    mc "Now I need to know."
    show zoe_street_talk as focus_zoe at sprite_l
    z "He has a playlist called 'Locked In.'"
    mc "That's not that bad."
    show zoe_street_laugh as focus_zoe at sprite_l
    z "It has three Imagine Dragons songs."
    show marcus_bar_talk as focus_marcus at sprite_r, react_lean_in
    m "Okay, first of all—"

    show zoe_street_talk as focus_zoe at sprite_l, react_nod
    z "I rest my case."
    show marcus_bar_talk as focus_marcus at sprite_r
    m "You don't have a case."
    mc "I'm starting to understand why you two are friends."
    show zoe_street_neutral as focus_zoe at sprite_l
    z "We're not."
    show marcus_bar_talk as focus_marcus at sprite_r
    m "See? She does this."
    show zoe_street_talk as focus_zoe at sprite_l
    z "I am sitting here voluntarily."
    m "Exactly."
    z "That proves poor judgment, not friendship."

    # [Marcus goes to get drinks. MC and Zoe briefly alone.]
    hide focus_marcus
    pause 0.5

    mc "You do like him."
    show zoe_street_neutral as focus_zoe at sprite_l
    z "Obviously."
    mc "You make that sound painful."
    z "It is sometimes."

    show marcus_bar_talk as focus_marcus at sprite_r
    m "Were you talking about me?"
    show zoe_street_neutral as focus_zoe at sprite_l
    z "No."
    mc "Yes."
    show marcus_bar_talk as focus_marcus at sprite_r, react_nod
    m "Thank you."
    show zoe_street_angry as focus_zoe at sprite_l, react_shake
    z "Unbelievable."

    $ apply_relationship_change("marcus", source_id="marcus_zoe_static_group",
                                source_category="casual_talk", familiarity=1)
    $ apply_relationship_change("zoe", source_id="marcus_zoe_static_group",
                                source_category="casual_talk", familiarity=1)
    $ add_relationship_memory("marcus", "marcus_zoe_static", "The table with the light directly above it")
    # Same routine counter the shorthand text reads (relationship_continuity).
    if rc_marcus_bar_count_day != day:
        $ rc_marcus_bar_count_day = day
        $ marcus_bar_count += 1
    $ spend_time(1.0)
    # M4 — group recognition. Fires once after dating begins.
    if (get_romance_state("zoe") in ("dating", "committed")
            and not zoe_m4_marcus_done
            and not story_scene_active):
        call zoe_m4_marcus_recognition
    hide focus_marcus
    hide focus_zoe
    $ story_scene_active = False
    $ set_hud("full")
    jump location_bar


# ═══════════════════════════════════════════════════════════════════════════
# PART 7 — CROSS-CALLBACKS
# ═══════════════════════════════════════════════════════════════════════════
# Dialogue-only one-shots, dispatched by the _check_talk_followup wrapper above
# 3+ days after the group scene.
label sd_marcus_static_callback:
    $ sd_marcus_static_cb_done = True
    m "Zoe still blaming me for the table?"
    mc "I think she's moved on."
    m "She hasn't."
    $ mark_memory_referenced("marcus", "marcus_zoe_static")
    $ _do_talk_accounting("marcus")
    return


label sd_zoe_static_callback:
    $ sd_zoe_static_cb_done = True
    z "Marcus changed his playlist."
    mc "Really?"
    z "No."
    z "But hope is important."
    $ _do_talk_accounting("zoe")
    return


# ═══════════════════════════════════════════════════════════════════════════
# PART 8 — ZOE, A SMALL DISAGREEMENT (+ REPAIR)
# ═══════════════════════════════════════════════════════════════════════════
# rc_zoe_friction_reads_harsh (relationship_continuity.rpy) is a DIFFERENT
# beat: there, she misreads a compliment MC gave her own work, at acquaintance
# stage, and it closes without either of you doing anything. This one is a
# genuine difference of taste at friend stage, and it is repaired on purpose.
# Both are kept; the gates do not overlap (fam >= 45 + friend stage here).
#
# The referent for "that": the exhibition poster at Grounds, which is already
# canon (zoe_arc.rpy zoe_msg_poster — "Someone has very strong feelings about
# negative space") and is the only standing design object in her locations.
label zoe_small_disagreement:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_disagreement")
    $ zoe_disagreement_done = True
    $ zoe_disagreement_day = day
    $ zoe_disagreement_repair_done = False
    if current_loc == "location_park":
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zd_back = "location_park"
    else:
        scene expression cafe_bg()
        $ _zd_back = "location_cafe"
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She has stopped in front of the exhibition poster — the one with the very strong feelings about negative space."

    show zoe_street_angry as focus_zoe at sprite_r
    z "I hate that."
    mc "I kind of like it."
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Really?"
    mc "Yeah."
    z "Why?"
    mc "Do I need a defense?"
    z "No."
    z "I'm trying to understand."
    mc "You sounded more like you were trying to diagnose me."
    z "..."
    z "Okay."
    mc "Okay?"
    show zoe_street_talk as focus_zoe at sprite_r
    z "That came out worse than I meant it."

    menu:
        "Tease her.":
            mc "You mean I can like something you don't?"
            show zoe_street_laugh as focus_zoe at sprite_r
            z "Apparently."
            mc "Big day."
            z "Don't push it."
            $ _zoe_rel("zoe_disagreement", affection=1, familiarity=1)
        "Be direct.":
            mc "You don't have to agree with me."
            show zoe_street_neutral as focus_zoe at sprite_r, react_nod
            z "I know."
            z "I'm not always good at sounding like I know."
            $ _zoe_rel("zoe_disagreement", trust=2, familiarity=1)
        "Drop it.":
            mc "It's fine."
            show zoe_street_neutral as focus_zoe at sprite_r
            z "..."
            z "Still."
            z "Noted."
            $ _zoe_rel("zoe_disagreement", familiarity=1)

    $ add_relationship_memory("zoe", "zoe_disagreement", "The poster you liked and she didn't")
    $ spend_time(0.3)
    $ _zarc_dest = _zd_back
    jump zoe_arc_exit


# Dialogue-only, Talk-initiated, 1-3 days later. Cannot fire before the
# disagreement: zoe_disagreement_repair_done defaults True (nothing owed).
label zoe_disagreement_repair:
    $ zoe_disagreement_repair_done = True
    z "For the record."
    mc "Dangerous start."
    z "I still hate that thing you liked."
    mc "Great."
    z "But I don't think you're wrong for liking it."
    mc "Growth."
    z "Don't make me take it back."
    $ mark_memory_referenced("zoe", "zoe_disagreement")
    $ _zoe_rel("zoe_disagreement_repair", trust=1, familiarity=1)
    $ _do_talk_accounting("zoe")
    return


# ═══════════════════════════════════════════════════════════════════════════
# SELF-CHECK — the gate logic, not the dialogue
# ═══════════════════════════════════════════════════════════════════════════
# Runnable from the debug menu. Asserts the four rules a player could actually
# hit backwards: no duplicate father reveal, no repair before its disagreement,
# no group callback before the group scene, no Wednesday-first after the
# repeatable one has already run.
label sd_selfcheck:
    python:
        _fails = []

        def _chk(cond, msg):
            if not cond:
                _fails.append(msg)

        _old = dict(store.topic_arc_done)
        _old_done = store.marcus_why_stayed_done
        _old_bf = store.sd_backfilled
        _old_wed = store.zoe_wednesday_first_done
        _old_beats = dict(store.tier_a_beat_last_day)
        _old_dis = store.zoe_disagreement_done
        _old_rep = store.zoe_disagreement_repair_done
        _old_disday = store.zoe_disagreement_day
        _old_grp = store.marcus_zoe_static_scene_done
        _old_mcb = store.sd_marcus_static_cb_done
        _old_bass = store.knows_zoe_bass_history

        # 1. Old save that already heard the inline reveal is migrated.
        # (sc_backfilled pinned True: the canon-consolidation block reads
        # topic_arc_done too, and this check fakes that dict.)
        store.sc_backfilled = True
        store.topic_arc_done = {"marcus_sports_2": True}
        store.marcus_why_stayed_done = False
        store.sd_backfilled = False
        _sd_backfill()
        _chk(store.marcus_why_stayed_done,
             "backfill: old sports_2 save did NOT get marcus_why_stayed_done")

        # 2. ...and the topic arc is then retired instead of re-revealing.
        _chk(_SD_ARC_FACT_GATE["marcus"]["marcus_sports_2"] == "marcus_why_stayed_done",
             "arc gate: sports_2 must key on marcus_why_stayed_done")
        store.knows_zoe_bass_history = True
        store.topic_arc_done = dict(store.topic_arc_done)
        store.topic_arc_done.pop("zoe_music_2", None)
        sd_retire_known_arcs("zoe")
        _chk(store.topic_arc_done.get("zoe_music_2"),
             "arc gate: zoe_music_2 not retired although the bass is already known")
        _chk(not sd_marcus_why_stayed_ok(),
             "why-stayed: fired again after being marked done")

        # 3. Repair can never precede its disagreement.
        store.zoe_disagreement_done = False
        store.zoe_disagreement_repair_done = True
        store.zoe_disagreement_day = -1
        _chk(_check_talk_followup("zoe") != "zoe_disagreement_repair",
             "repair: offered before the disagreement happened")

        # 4. Cross-callbacks need the group scene AND 3 days.
        store.marcus_zoe_static_scene_done = False
        store.sd_marcus_static_cb_done = False
        _chk(_check_talk_followup("marcus") != "sd_marcus_static_callback",
             "callback: offered before the Static group scene")

        # 5. Wednesday-first stands down for a save that already had one.
        store.zoe_wednesday_first_done = False
        store.sd_backfilled = False
        store.tier_a_beat_last_day = dict(store.tier_a_beat_last_day)
        store.tier_a_beat_last_day["zoe_wednesday"] = 1
        _sd_backfill()
        _chk(store.zoe_wednesday_first_done,
             "backfill: repeatable Wednesday already run, first-occurrence not retired")

        store.topic_arc_done = _old
        store.marcus_why_stayed_done = _old_done
        store.sd_backfilled = _old_bf
        store.zoe_wednesday_first_done = _old_wed
        store.tier_a_beat_last_day = _old_beats
        store.zoe_disagreement_done = _old_dis
        store.zoe_disagreement_repair_done = _old_rep
        store.zoe_disagreement_day = _old_disday
        store.marcus_zoe_static_scene_done = _old_grp
        store.sd_marcus_static_cb_done = _old_mcb
        store.knows_zoe_bass_history = _old_bass

    if _fails:
        "SELF-CHECK FAILED:"
        python:
            for _f in _fails:
                renpy.say(None, _f)
    else:
        "Story-directing pass self-check: all gates OK."
    return
