# ═══════════════════════════════════════════════════════════════════════════
# RELATIONSHIP CONTINUITY & CHARACTER PRESENCE — ZOE + MARCUS
# ═══════════════════════════════════════════════════════════════════════════
# This pass adds CONTINUITY BETWEEN existing scenes. It re-implements nothing.
# Everything below hangs off a mechanism that already shipped:
#
#   greeting hook          interact.rpy   NPC_DATA[...]["greet"] -> marcus_greet
#                                         / zoe_greet, called by npc_interact
#   farewell hook          interact.rpy   marcus_farewell (this pass adds the
#                                         Zoe arm of the same two-line branch)
#   pre-Talk initiation    interact.rpy   _check_talk_followup, wrapped the same
#                                         way zoe_arc / zoe_onboarding /
#                                         marcus_onboarding already wrap it
#   beat cooldowns         location_beats_tier_a.rpy _beat_cooldown_ok pattern
#                                         (a local dict, so these do NOT eat the
#                                         city-wide contextual-beat budget)
#   variety picker         world_events.rpy _pick_ambient_variant
#   life state             npc_initiative.rpy npc_life_state
#   relationship bands     npc_relationships.rpy npc_relationship_stage
#   phone pool             phone_actionable.rpy _INITIATIVE_* tables
#   expression swap        interact.rpy   show_npc_expr (no-ops outside an
#                                         interaction, so the Scene Tester is
#                                         safe)
#   old-save backfill      config.after_load_callbacks (NOT a second
#                                         `label after_load:` — zoe_onboarding
#                                         owns that label)
#
# ZERO new art: nothing here issues `scene` or `show`, exactly like the
# shipping greeting labels and the marcus_friendship.rpy beats.
#
# CANON THIS PASS IS BUILT ON (each cited where it is used):
#   Marcus bartender, runs Static   location_beats_tier_a.rpy:911, city_events:156
#   Marcus bar hours                npc_schedules.rpy Mon-Fri 16-24, Sat-Sun 15-27
#   Marcus NEVER at the gym         location_beats_tier_a.rpy:34
#   Marcus the lock                 script.rpy:23 + marcus_beat_still_alive
#   Marcus counts the score         arcs.rpy:187 + marcus_ctx_basketball
#   Zoe bad typography              zoe_onboarding.rpy (kiosk sign, the doorway),
#                                   zoe_arc.rpy zoe_msg_poster / zoe_msg_mural,
#                                   zoe_wednesday "local" variant
#   Zoe and Marcus, three years     zoe_onboarding.rpy:253
#   Zoe is in Static on Saturdays   npc_schedules.rpy zoe bar Sat 19-24
#
# ponytail: micro beats and friction are dispatched from the GREETING, not from
# a per-location entry hook. Ceiling: they only ever fire on the first
# conversation of a day, which is also exactly what makes them unfarmable.
# Upgrade path if they need to fire on arrival instead — the labels are all
# location-neutral (no `scene`), so they can be moved onto the location_* Tier A
# chains without rewriting a line.
# ═══════════════════════════════════════════════════════════════════════════

# ── Greeting / farewell bookkeeping ─────────────────────────────────────────
default _rc_greet_done            = False   # scratch: pre-greet handled it
default _rc_micro                 = None    # scratch: chosen micro label
default rc_marcus_greet_day       = -999
default rc_marcus_farewell_day    = -999
default rc_zoe_greet_day          = -999
default rc_zoe_farewell_day       = -999
default rc_zoe_last_seen_day      = -999    # Zoe's own copy, read BEFORE
                                            # npc_last_seen is overwritten
default rc_zoe_greet_gap          = 0
default rc_zoe_sit_day            = -999    # the "Sit." close variant, cd 10
default rc_zoe_wed_farewell_done  = False

# ── Micro interactions ──────────────────────────────────────────────────────
default rc_micro_last             = {}      # {npc_id: day}  — pacing per person
default rc_micro_fired            = {}      # {micro_id: day} — per-beat cooldown

# ── Busy / unavailable ──────────────────────────────────────────────────────
default rc_marcus_busy_day        = -999
default rc_zoe_busy_day           = -999

# ── Friction and repair ─────────────────────────────────────────────────────
default rc_marcus_f1_done         = False   # pushed after a decline
default rc_marcus_f2_done         = False   # competitive about the score
default rc_marcus_friction_day    = -999
default rc_marcus_repair_done     = True    # True == nothing owed
default rc_zoe_f1_done            = False   # read a comment harshly
default rc_zoe_f2_done            = False   # curt because stressed
default rc_zoe_friction_day       = -999
default rc_zoe_repair_done        = True

# ── Shared routines ─────────────────────────────────────────────────────────
default zoe_grounds_count         = 0
default marcus_bar_count          = 0
default rc_zoe_grounds_count_day  = -999
default rc_marcus_bar_count_day   = -999
default rc_backfilled             = False


# init 7: after marcus_onboarding.rpy (init 5/6), zoe_onboarding.rpy (init 4)
# and zoe_arc.rpy (init 2/3), so the _check_talk_followup wrap below sits on top
# of all three and the phone tables it extends already exist.
init 7 python:

    _RC_MICRO_GAP      = 5    # days between ANY two micro beats for one person
    _RC_MICRO_COOLDOWN = 14   # days before the SAME micro beat can come back

    def _rc_stage(npc_id):
        try:
            return npc_relationship_stage(npc_id)
        except Exception:
            return "stranger"

    def _rc_known(npc_id):
        return _rc_stage(npc_id) not in ("stranger", "known")

    def _rc_friend(npc_id):
        return _rc_stage(npc_id) in ("friend", "close", "trusted")

    def _rc_close(npc_id):
        return _rc_stage(npc_id) in ("close", "trusted")

    def _rc_life(npc_id):
        try:
            return npc_life_state(npc_id)
        except Exception:
            return None

    def _rc_quiet():
        """False while an authored scene owns the screen. Friction and micro
        beats are never allowed to land on top of a vulnerability scene."""
        return not bool(store.story_scene_active)

    # ── Micro dispatcher ─────────────────────────────────────────────────────
    # Local cooldown dicts on purpose: these are 10-30 line nothings the player
    # opted into by talking to someone, and must not spend the Tier A
    # one-contextual-beat-per-day budget that ambush scenes draw from.
    def _rc_micro_ok(npc_id):
        if not _rc_quiet():
            return False
        return store.day - store.rc_micro_last.get(npc_id, -999) >= _RC_MICRO_GAP

    def _rc_micro_avail(micro_id):
        return store.day - store.rc_micro_fired.get(micro_id, -999) >= _RC_MICRO_COOLDOWN

    def rc_micro_fired(npc_id, micro_id):
        """Write point. Spends the per-person pacing budget AND stamps the
        per-beat cooldown, so a beat can never be re-entered by walking out and
        back in: the greeting itself is already once-per-day gated."""
        d = dict(store.rc_micro_last)
        d[npc_id] = store.day
        store.rc_micro_last = d
        f = dict(store.rc_micro_fired)
        f[micro_id] = store.day
        store.rc_micro_fired = f

    # (micro_id, label, eligibility). No relationship write anywhere in these.
    RC_MARCUS_MICRO = [
        # Bar equivalent of the gym-etiquette complaint. He is NEVER at the gym
        # (location_beats_tier_a.rpy:34) — this is a customer, in his own bar.
        ("rc_m_micro_customer", "rc_marcus_micro_customer",
         lambda: store.current_loc == "location_bar"),
        # Occupation-neutral on purpose: it must be tellable at the park too.
        ("rc_m_micro_dumb",     "rc_marcus_micro_dumb",     lambda: True),
        ("rc_m_micro_ten",      "rc_marcus_micro_ten_minutes",
         lambda: _rc_friend("marcus")),
        # NPC-to-NPC. Basis: zoe's schedule puts her in the bar Sat 19-24, which
        # is inside his Sat 15-27 shift, and zoe_onboarding.rpy:253 has them
        # three years deep.
        ("rc_m_micro_zoe",      "rc_marcus_micro_zoe",
         lambda: store.zoe_properly_introduced and _rc_known("marcus")),
        # The lock, version 3. Only once MC has moved somewhere the joke can
        # land, and only if MC actually took the lock branch in the first place.
        ("rc_m_micro_lock",     "rc_marcus_micro_lock",
         lambda: store.apartment_tier >= 2 and store.marcus_lock_joke_active),
    ]

    RC_ZOE_MICRO = [
        ("rc_z_micro_sign",   "rc_zoe_micro_sign",   lambda: True),
        ("rc_z_micro_obs",    "rc_zoe_micro_observation",
         lambda: store.knows_zoe_art_interest),
        ("rc_z_micro_break",  "rc_zoe_micro_break",  lambda: _rc_friend("zoe")),
        # NPC-to-NPC. Basis: arc_marcus_sports_2 + marcus_ctx_basketball
        # ("I count a bit"), gated so MC has actually heard the reference.
        ("rc_z_micro_marcus", "rc_zoe_micro_marcus",
         lambda: store.marcus_met and store.mc_knows_marcus_bball_offer),
    ]

    def rc_pick_micro(npc_id):
        """Least-recently-seen eligible micro, or None. Reads state only —
        rc_micro_fired() is the write point, called by the label itself."""
        if not _rc_micro_ok(npc_id):
            return None
        pool = RC_MARCUS_MICRO if npc_id == "marcus" else RC_ZOE_MICRO
        eligible = []
        for mid, lbl, cond in pool:
            if not _rc_micro_avail(mid):
                continue
            try:
                if not cond():
                    continue
            except Exception:
                continue
            eligible.append((mid, lbl))
        if not eligible:
            return None
        eligible.sort(key=lambda e: store.rc_micro_fired.get(e[0], -999))
        return eligible[0][1]

    # ── Busy / unavailable ───────────────────────────────────────────────────
    def rc_marcus_busy():
        """His REAL shift (npc_schedules.rpy: bar Mon-Fri 16-24, Sat-Sun 15-27),
        in the bar, before he counts you as a friend. No fabricated windows."""
        if store.current_loc != "location_bar":
            return False
        if _rc_friend("marcus"):
            return False
        if store.rc_marcus_busy_day == store.day:
            return False
        h = float(store.hour)
        return h >= (15.0 if (store.day % 7) >= 5 else 16.0)

    def rc_zoe_busy():
        """Her own life state, not a made-up calendar: busy_work / stressed_week
        are the two NPC_PERSONAL_LIFE_WEIGHTS entries Zoe actually rolls that
        mean client work and a rough stretch."""
        if _rc_close("zoe"):
            return False
        if store.rc_zoe_busy_day == store.day:
            return False
        if not _rc_known("zoe"):
            return False
        return _rc_life("zoe") in ("busy_work", "stressed_week")

    # ── Pre-Talk initiation ──────────────────────────────────────────────────
    # Same wrap the other three files use, but deliberately in FRONT of the
    # existing chain rather than behind it: sitting in front is what turns a
    # menu item MC has to pick into the character opening the subject.
    #
    # Every label returned below closes its own thread on entry
    # (marcus_ctx_interview clears mc_told_marcus_interview,
    # zoe_talk_deadline_followup sets zoe_deadline_followup_done,
    # zoe_talk_second_opinion_callback sets zoe_second_opinion_callback_done),
    # so none of them needs — or could benefit from — a separate one-shot flag.
    _check_talk_followup_pre_rc = _check_talk_followup

    def _check_talk_followup(npc_id):
        if npc_id == "marcus" and store.marcus_met:
            # Marcus priority 1: an interview he was told about and has not been
            # given an answer to. mf_interview_unresolved() already refuses to
            # fire once the career state answers the question by itself.
            if (mf_interview_unresolved()
                    and store.marcus_interview_told_day >= 0
                    and store.day > store.marcus_interview_told_day):
                return "marcus_ctx_interview"
            # Marcus priority 2 ("Still hate that place?") already initiates via
            # mf_pick_beat -> marcus_beat_that_job_again. Not duplicated here.
        elif npc_id == "zoe" and store.zoe_met:
            if (store.zoe_deadline_submitted
                    and not store.zoe_deadline_followup_done
                    and store.zoe_deadline_day >= 0
                    and store.day - store.zoe_deadline_day >= 3):
                return "zoe_talk_deadline_followup"
            if (store.zoe_second_opinion_choice
                    and store.zoe_second_opinion_done
                    and not store.zoe_second_opinion_callback_done
                    and store.zoe_second_opinion_day >= 0
                    and store.day - store.zoe_second_opinion_day >= 3):
                return "zoe_talk_second_opinion_callback"
        return _check_talk_followup_pre_rc(npc_id)

    # ── Old-save backfill ────────────────────────────────────────────────────
    def _rc_backfill():
        """Idempotent, runs on every load. A save made before this file existed
        can already be forty days into both friendships — this is what stops the
        first greeting after loading reading as a five-day absence, and what
        gives an existing routine credit for the Wednesdays it already had.

        Nothing here can invent a relationship: if the stage is already
        friend/close, the stage-banded greetings and farewells simply select the
        right band on the very next interaction with no migration at all."""
        if store.rc_zoe_last_seen_day <= -999:
            store.rc_zoe_last_seen_day = store.npc_last_seen.get("zoe", -999)
        if store.marcus_last_seen_day <= -999:
            store.marcus_last_seen_day = store.npc_last_seen.get("marcus", -999)
        if store.rc_backfilled:
            return
        store.rc_backfilled = True
        # One count each, and only where there is a real record of it happening.
        # Not two: the shorthand must still be earned by one more real visit.
        if store.tier_a_beat_last_day.get("zoe_wednesday", -999) >= 0:
            store.zoe_grounds_count = max(store.zoe_grounds_count, 1)
        if store.bar_game_cooldowns.get("pool_marcus", -999) >= 0:
            store.marcus_bar_count = max(store.marcus_bar_count, 1)

    try:
        if _rc_backfill not in config.after_load_callbacks:
            config.after_load_callbacks.append(_rc_backfill)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# SHARED ROUTINES — shorthand texts, registered into the SHIPPING picker
# ═══════════════════════════════════════════════════════════════════════════
# No second cadence engine. These are two more rows in the tables
# phone_actionable.rpy already owns; the one-contact-per-day global budget and
# the per-NPC cooldown are unchanged. The only new thing is the condition: a
# routine has to have happened twice before either of them can be sent.
init 8 python:

    _ZOE_GROUNDS_SHORT_RESP = [
        {"id": "wed",   "text": "Wednesday?", "label": "npc_ini_zoe_gshort_wed"},
        {"id": "three", "text": "Three.",     "label": "npc_ini_zoe_gshort_three"},
    ]
    _MARCUS_STATIC_SHORT_RESP = [
        {"id": "yes",  "text": "Yeah.",  "label": "npc_ini_marcus_static_yes"},
        {"id": "no",   "text": "Can't.", "label": "npc_ini_marcus_static_no"},
    ]

    _INITIATIVE_MSGS.update({
        "zoe_msg_grounds_short":   {"text": "Grounds?",
                                    "responses": _ZOE_GROUNDS_SHORT_RESP},
        "marcus_msg_static_short": {"text": "Static tonight?",
                                    "responses": _MARCUS_STATIC_SHORT_RESP},
    })
    _INITIATIVE_VARIANTS["zoe"] = _INITIATIVE_VARIANTS["zoe"] + ["zoe_msg_grounds_short"]
    _INITIATIVE_VARIANTS["marcus"] = _INITIATIVE_VARIANTS["marcus"] + ["marcus_msg_static_short"]
    _VARIANT_MIN_TIER.update({"zoe_msg_grounds_short": 1, "marcus_msg_static_short": 1})
    _VARIANT_WEIGHTS.update({"zoe_msg_grounds_short": 3, "marcus_msg_static_short": 3})
    _VARIANT_CONDITIONS.update({
        # Shorthand only exists once the thing it is short FOR has happened.
        "zoe_msg_grounds_short":   lambda: store.zoe_grounds_count >= 2,
        "marcus_msg_static_short": lambda: store.marcus_bar_count >= 2,
    })


label npc_ini_zoe_gshort_wed:
    $ _apply_aff("zoe", 1)
    $ queue_phone_message("zoe", "Obviously.", day, "zoe_msg_gshort_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_gshort_three:
    $ _apply_aff("zoe", 1)
    $ queue_phone_message("zoe", "Three.", day, "zoe_msg_gshort_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_marcus_static_yes:
    $ queue_phone_message("marcus", "Good. I'm behind the bar either way.", day, "marcus_msg_static_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_static_no:
    # Declining Marcus has never cost anything and does not start now.
    $ queue_phone_message("marcus", "Another one, then.", day, "marcus_msg_static_r2")
    $ _clear_initiative_pending("marcus")
    return


# ═══════════════════════════════════════════════════════════════════════════
# MARCUS — GREETING WRAPPERS
# ═══════════════════════════════════════════════════════════════════════════
# marcus_greet (interact.rpy:2172) already carries the five stage variants and
# marcus_farewell already carries the four contextual sign-offs. This pass does
# not rewrite either — it brackets them: `pre` can pre-empt the greeting, `post`
# runs after it.

label rc_marcus_greet_pre:
    $ _rc_greet_done = False

    # Same-day repeat. Nothing stage-specific ever fires twice in one day, and
    # this is also the gate that makes the micro pool below unfarmable.
    if rc_marcus_greet_day == day:
        $ _rc_greet_done = True
        m "Back."
        return
    $ rc_marcus_greet_day = day

    # 1. Repair. He owes it before he says anything else.
    if (not rc_marcus_repair_done and rc_marcus_friction_day >= 0
            and day - rc_marcus_friction_day >= 1
            and day - rc_marcus_friction_day <= 4 and not story_scene_active):
        # marcus_greet stamps marcus_last_seen_day itself, but this path skips
        # it — without the stamp the NEXT greeting reads today as an absence.
        $ marcus_last_seen_day = day
        $ _rc_greet_done = True
        call rc_marcus_repair
        return

    # 2. Busy. His real shift, and you are not a friend yet.
    if rc_marcus_busy():
        $ marcus_last_seen_day = day
        $ rc_marcus_busy_day = day
        $ _rc_greet_done = True
        m "I'm a bit busy. Later?"
        return

    # 3. Bad day. ONE line, in front of the ordinary greeting — not a scene.
    if npc_life_state("marcus") == "busy_work":
        m "Long one today."
    return


label rc_marcus_greet_post:
    # Routine counter. Once per day, and only where the routine actually is.
    if current_loc == "location_bar" and rc_marcus_bar_count_day != day:
        $ rc_marcus_bar_count_day = day
        $ marcus_bar_count += 1

    # Friction F2 — competitive about a game that actually happened.
    # bar_game_cooldowns["pool_marcus"] is stamped by record_bar_game_result,
    # so this cannot fire about a match nobody played.
    if (not rc_marcus_f2_done and not story_scene_active
            and _rc_friend("marcus")
            and day - bar_game_cooldowns.get("pool_marcus", -999) <= 2):
        call rc_marcus_friction_competitive
        return

    $ _rc_micro = rc_pick_micro("marcus")
    if _rc_micro:
        call expression _rc_micro
    return


# ═══════════════════════════════════════════════════════════════════════════
# ZOE — GREETING, STAGE BANDS, FAREWELL
# ═══════════════════════════════════════════════════════════════════════════

label rc_zoe_greet_pre:
    $ _rc_greet_done = False
    # rc_zoe_last_seen_day is our own copy: npc_interact already stamped
    # npc_last_seen for today by the time a greeting runs, exactly the reason
    # marcus_greet and nora_greet each keep one.
    $ _rc_zgap = (day - rc_zoe_last_seen_day) if rc_zoe_last_seen_day >= 0 else 0

    if rc_zoe_greet_day == day:
        $ _rc_greet_done = True
        z "You again."
        return
    $ rc_zoe_greet_gap     = _rc_zgap
    $ rc_zoe_greet_day     = day
    $ rc_zoe_last_seen_day = day

    # 1. Repair.
    if (not rc_zoe_repair_done and rc_zoe_friction_day >= 0
            and day - rc_zoe_friction_day >= 1
            and day - rc_zoe_friction_day <= 4 and not story_scene_active):
        $ _rc_greet_done = True
        call rc_zoe_repair
        return

    # 2. Friction F2 — curt because she is in a rough stretch. Resolves inside
    #    the same interaction, so it does not need a repair of its own.
    if (not rc_zoe_f2_done and not story_scene_active
            and _rc_known("zoe")
            and npc_life_state("zoe") == "stressed_week"):
        $ _rc_greet_done = True
        call rc_zoe_friction_curt
        return

    # 3. Busy. Her own life state, not a fabricated calendar.
    if rc_zoe_busy():
        $ rc_zoe_busy_day = day
        $ _rc_greet_done = True
        z "Can't. Deadline."
        z "Another day."
        return

    # 4. Bad day. ONE line in front of the ordinary greeting.
    if npc_life_state("zoe") == "busy_work":
        z "Client call ran long. I'm still half in it."
    return


label rc_zoe_stage_greet:
    # Dating / committed: occasionally use a low-key romantic greeting (40% chance).
    # Does NOT replace the stage ladder — mixes in with it.
    $ _rm_rs = get_romance_state("zoe")
    if (_rm_rs in ("dating", "committed")
            and rc_zoe_greet_gap < 3
            and renpy.random.random() < 0.40):
        if _rm_rs == "committed":
            $ _rm_line = renpy.random.choice([
                "There you are.",
                "Good. You saved me from pretending I came here to work.",
                "I was starting to think I'd have to text you.",
            ])
        else:
            $ _rm_line = renpy.random.choice([
                "There you are.",
                "Hey. I was starting to think I'd have to text you.",
            ])
        z "[_rm_line]"
        $ rc_zoe_greet_day = day
        return
    $ _rc_zst = npc_relationship_stage("zoe")
    if rc_zoe_greet_gap >= 5 and _rc_zst not in ("stranger", "known"):
        z "You alive?"
    elif _rc_zst in ("close", "trusted") and day - rc_zoe_sit_day >= 10:
        $ rc_zoe_sit_day = day
        z "Sit. I need another opinion."
        mc "On what?"
        z "Haven't decided yet. Sit anyway."
    elif _rc_zst in ("friend", "close", "trusted"):
        z "You have five minutes?"
    elif _rc_zst in ("acquaintance", "friendly"):
        z "There you are."
    elif _rc_zst == "known":
        z "Oh. Hey."
    else:
        z "You're blocking my light. ...Kidding. Mostly. I'm Zoe."
    return


label rc_zoe_greet_post:
    # Routine counter: a Wednesday at Grounds. day % 7 == 2 is Wednesday, the
    # same arithmetic npc_schedules and the Scene Tester already use, and it is
    # her real café block (Wed 13-18).
    if (current_loc == "location_cafe" and day % 7 == 2
            and rc_zoe_grounds_count_day != day):
        $ rc_zoe_grounds_count_day = day
        $ zoe_grounds_count += 1

    # Friction F1 — she reads something MC said harder than MC meant it.
    # Requires an opinion MC actually gave her (zoe_second_opinion_scene).
    if (not rc_zoe_f1_done and not story_scene_active
            and zoe_second_opinion_done and zoe_second_opinion_day >= 0
            and day - zoe_second_opinion_day >= 2
            and npc_relationship_stage("zoe") in ("friendly", "friend", "close", "trusted")):
        call rc_zoe_friction_reads_harsh
        return

    $ _rc_micro = rc_pick_micro("zoe")
    if _rc_micro:
        call expression _rc_micro
    return


# Called from npc_interact's exit, next to marcus_farewell.
label zoe_farewell:
    if rc_zoe_farewell_day == day:
        return
    $ rc_zoe_farewell_day = day
    if not _rc_known("zoe"):
        return
    if (not rc_zoe_wed_farewell_done and zoe_grounds_count >= 1
            and current_loc == "location_cafe"):
        # Only once the Wednesday has happened at least once — otherwise the
        # single word refers to nothing.
        $ rc_zoe_wed_farewell_done = True
        z "Wednesday?"
        return
    if (rc_zoe_greet_gap >= 5 and knows_zoe_art_interest and player_portfolio):
        # Only where MC has actually made something the city has on record —
        # player_portfolio is written by record_game_event's portfolio_domain.
        z "Send me that thing you mentioned."
        return
    if _rc_close("zoe"):
        z "Go. You're distracting me."
        return
    if _rc_friend("zoe"):
        z "Don't vanish for another week."
    return


# ═══════════════════════════════════════════════════════════════════════════
# MICRO INTERACTIONS — MARCUS
# ═══════════════════════════════════════════════════════════════════════════
# No CG. No relationship write. No spend_time. They exist to prove he has a life
# running whether or not you are standing in it.

label rc_marcus_micro_customer:
    $ rc_micro_fired("marcus", "rc_m_micro_customer")
    m "Guy at the end has been nursing one drink since half four."
    mc "Is that a problem?"
    m "No."
    m "He's been telling me about it, though. Every twenty minutes. Same drink, new update."
    mc "What kind of update?"
    m "\"Still going.\""
    $ show_npc_expr("marcus", "laugh")
    "He delivers it the way you'd read out a hostage note."
    m "He tips fine. I've made my peace with it."
    return


label rc_marcus_micro_dumb:
    $ rc_micro_fired("marcus", "rc_m_micro_dumb")
    m "I walked to the shop this morning, stood in it for a minute, and walked back."
    mc "Did you buy anything?"
    m "No."
    mc "What did you go for?"
    m "That's the part I'm still working on."
    "He doesn't seem troubled by it. He seems to have filed it and moved on."
    return


label rc_marcus_micro_ten_minutes:
    $ rc_micro_fired("marcus", "rc_m_micro_ten")
    m "I've got ten minutes before something."
    mc "Before what?"
    m "Doesn't matter. Ten minutes."
    "He doesn't fill them. You stand there, he stands there, and about four minutes in he points out that the streetlight on the corner has been coming on an hour early all week."
    m "Right. That was the ten."
    mc "You had four left."
    m "I'm banking them."
    return


label rc_marcus_micro_zoe:
    $ rc_micro_fired("marcus", "rc_m_micro_zoe")
    m "Zoe was in Saturday. Asked if I'd seen you."
    mc "What did you tell her?"
    m "That I'd seen you."
    mc "That's it?"
    m "She didn't ask for a report."
    "He goes back to whatever he was doing, which as far as he's concerned is the end of it."
    return


# The lock, version 3. script.rpy:23 set it up, marcus_beat_still_alive's lock
# branch armed it (marcus_lock_joke_active), mstory_lock is version 2. This only
# exists once MC has moved somewhere the joke can actually land.
label rc_marcus_micro_lock:
    $ rc_micro_fired("marcus", "rc_m_micro_lock")
    m "New place. How's the lock?"
    mc "It just... opens."
    m "Yeah."
    "He nods at that for slightly longer than the sentence needs."
    m "Enjoy it. You've lost something and you don't know it yet."
    mc "I've lost a lock that was actively trying to kill me."
    m "You've lost a thing to be right about."
    return


# ═══════════════════════════════════════════════════════════════════════════
# MICRO INTERACTIONS — ZOE
# ═══════════════════════════════════════════════════════════════════════════

# The bad-typography motif. Rotated by _pick_ambient_variant, the same soft
# variety picker zoe_wednesday_grounds_scene and the ambient system already use.
label rc_zoe_micro_sign:
    $ rc_micro_fired("zoe", "rc_z_micro_sign")
    $ _rc_zs = _pick_ambient_variant("rc_zoe_sign", ["laundry", "menu", "flyer"])
    if _rc_zs == "laundry":
        z "The launderette has a new sign."
        mc "Bad?"
        z "It's set in two weights of the same typeface. Not two typefaces. Two weights."
        z "Which means somebody had the correct font already open and chose that."
        mc "Is that worse?"
        z "It's so much worse."
    elif _rc_zs == "menu":
        z "Somebody has centred every line on the specials board."
        mc "And?"
        z "Eleven lines. All centred. Nothing for your eye to hang on."
        z "I've read it four times and I still don't know what the soup is."
    else:
        z "There's a flyer on the pole outside with the phone number in Comic Sans."
        mc "Only the number?"
        z "Only the number. The rest of it is completely fine."
        z "So they own a second font. They chose this."
    "She has already moved on. It cost her about nine seconds and she will do it again tomorrow."
    return


label rc_zoe_micro_observation:
    $ rc_micro_fired("zoe", "rc_z_micro_obs")
    z "Don't look yet."
    mc "At what?"
    z "The glass behind you. Give it ten seconds."
    "You give it ten seconds. The light comes off the windows across the way and for about a second and a half the whole row goes the colour of the inside of a shell."
    $ show_npc_expr("zoe", "talk")
    z "There. That happens at about this time for a fortnight a year and then it stops."
    mc "How do you know that?"
    z "Because I've been sitting in this chair for two years being annoyed I can't paint it."
    return


label rc_zoe_micro_break:
    $ rc_micro_fired("zoe", "rc_z_micro_break")
    z "I've got five minutes and I'm not spending them on the file that's open."
    mc "What do you want to do with them?"
    z "Nothing. That's the whole offer."
    "So you do nothing, at a table, for five minutes. She turns her pencil over twice and doesn't draw anything with it."
    z "Right. That was the five."
    return


label rc_zoe_micro_marcus:
    $ rc_micro_fired("zoe", "rc_z_micro_marcus")
    z "Is Marcus still mentioning the score?"
    mc "Which score?"
    z "Any of them. It genuinely doesn't matter which one."
    "She turns a page without looking up."
    z "He's impossible when he wins something. He's worse when he nearly wins something."
    mc "You've thought about this."
    z "I've had three years of data."
    return


# ═══════════════════════════════════════════════════════════════════════════
# FRICTION AND REPAIR
# ═══════════════════════════════════════════════════════════════════════════
# Small. One-shot. Never during a scene (every entry point checks
# story_scene_active). Each friction re-arms its character's repair, so the
# repair can fire once per friction and never before one.

# F1 — called from the decline branches in marcus_friendship.rpy. Guarded here
# rather than at each call site so the three call sites stay one line each.
label rc_marcus_friction_push:
    if rc_marcus_f1_done or story_scene_active:
        return
    if not _rc_friend("marcus"):
        return
    $ rc_marcus_f1_done      = True
    $ rc_marcus_friction_day = day
    $ rc_marcus_repair_done  = False
    m "Come on."
    mc "I said no."
    m "I heard \"maybe.\""
    mc "You heard no."
    m "Fine. I heard no."
    "He drops it, and he actually drops it, which is not the same thing as sulking about having dropped it."
    return


label rc_marcus_friction_competitive:
    $ rc_marcus_f2_done      = True
    $ rc_marcus_friction_day = day
    $ rc_marcus_repair_done  = False
    mc "You're being weird about this."
    m "I'm fine."
    mc "You keep mentioning the score."
    m "Because it was a good score."
    return


label rc_marcus_repair:
    $ rc_marcus_repair_done = True
    if day - rc_marcus_friction_day <= 1:
        m "I was annoying yesterday. More than usual."
    else:
        m "I was annoying the other day. More than usual."
    mc "You were."
    m "Noted. That's the whole apology, don't wait for more."
    return


label rc_zoe_friction_reads_harsh:
    $ rc_zoe_f1_done      = True
    $ rc_zoe_friction_day = day
    $ rc_zoe_repair_done  = False
    z "That thing you said about the layout."
    mc "What about it?"
    z "Is that what you actually think?"
    mc "I said I liked it."
    z "I know what you said."
    "A short silence that belongs entirely to her. Then she turns the page back over and the moment closes without either of you doing anything about it."
    return


# F2 resolves inside the same interaction — she corrects herself before you have
# gone anywhere, which is why it does not arm a repair.
label rc_zoe_friction_curt:
    $ rc_zoe_f2_done      = True
    $ rc_zoe_friction_day = day
    z "Not now."
    mc "I literally just said hello."
    z "I know."
    "She puts the pencil down flat, which from her is most of an apology."
    z "Give me a minute."
    "You give her a minute. She takes about forty seconds of it."
    $ show_npc_expr("zoe", "talk")
    z "Right. Hello."
    return


label rc_zoe_repair:
    $ rc_zoe_repair_done = True
    if day - rc_zoe_friction_day <= 1:
        z "I was short with you yesterday. That wasn't really about you."
    else:
        z "I was short with you the other day. That wasn't really about you."
    mc "I know."
    z "Good. I'm not doing the long version of it."
    return


# ═══════════════════════════════════════════════════════════════════════════
# SCENE TESTER LAUNCHER
# ═══════════════════════════════════════════════════════════════════════════
# The labels above all `return` (they are `call`ed from the greeting), so the
# tester's plain Jump() needs a call frame. Same exception the file already
# makes for dst_nora_reopen_launch and marcus_friendship_test.
#
# Scene Tester presets and registry entries for this pack live in
# debug_scene_tester.rpy — gameplay files must not name, read or write the
# debug tester registry.
default rc_test_label = "rc_zoe_micro_sign"
default rc_test_npc   = "zoe"

label rc_continuity_test:
    $ set_hud("hidden")
    $ story_scene_active = True
    show screen hud
    hide screen people_here_dock
    if rc_test_npc == "marcus":
        show expression mf_sprite("normal") as focus_marcus at sprite_r
    else:
        show zoe_street_neutral as focus_zoe at sprite_r
    # The friction/micro labels refuse to run while a scene owns the screen —
    # correct in gameplay, useless in a tester, so the flag is dropped for the
    # duration of the call and restored on the way out.
    $ story_scene_active = False
    call expression rc_test_label
    $ story_scene_active = True
    hide focus_marcus
    hide focus_zoe
    $ story_scene_active = False
    $ set_hud("full")
    jump map
