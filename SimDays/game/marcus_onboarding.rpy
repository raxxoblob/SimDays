# ═══════════════════════════════════════════════════════════════════════════
# MARCUS — EVERYDAY FRIENDSHIP: STATE, MEMORY, PHONE, CONTEXTUAL TALK
# ═══════════════════════════════════════════════════════════════════════════
# Sibling of marcus_friendship.rpy (the authored beats). This file holds the
# plumbing: state, the daily tick, the initiative-pool registration and the
# Talk router. It builds NOTHING new — every mechanism below already shipped:
#
#   contact / initiative picker   phone_actionable.rpy  _INITIATIVE_* +
#                                 _check_npc_initiative
#   scripted texts                phone_messages.rpy    queue_phone_message
#   invitations & commitments     phone_actionable.rpy  npc_invitation_pending
#                                 (the marcus_park_invite route already exists)
#   Talk extension point          interact.rpy          _check_talk_followup
#                                 (same wrap zoe_onboarding.rpy uses)
#   beat cooldowns                location_beats_tier_a _beat_cooldown_ok
#   relationship writes           npc_relationships.rpy apply_relationship_change
#   memory                        npc_schedules.rpy     add_relationship_memory
#   world knowledge of MC         npc_initiative.rpy    public_player_facts
#
# CANON THIS PASS IS BUILT ON (audited, with sources):
#   job          bartender who runs the bar
#                location_beats_tier_a.rpy:911 "I'm a bartender. Everything I
#                say sounds like a diagnosis." / :749 "bored of my own bar"
#   schedule     npc_schedules.rpy:60-71 — park Mon-Fri 07-11 (running),
#                cafe Tue 15-17, bar Mon-Fri 16-24, bar Sat-Sun 15-27
#   basketball   arcs.rpy:184 semi-pro offer at eighteen, didn't take it
#   chili        arcs.rpy:202 "I can cook exactly one thing properly. Chili."
#                + script.rpy:45 the moving-day pot; recipe is his mother's
#   the lock     script.rpy:23 "That lock's a jerk, you gotta lift the handle
#                while you turn it." (MC = 12, Marcus = 14)
#   early hours  arcs.rpy:176 "Six AM every day. Even weekends." / "I can't
#                sleep past five anyway."  ← the spec's "5 AM" motif, corrected
#   Zoe          location_beats_tier_a.rpy:891 the art-vs-money argument
#   Nora         world_events.rpy:1593 "Do you two know each other?" gag
#   NOT canon    the gym (location_beats_tier_a.rpy:34 "Marcus is NEVER at the
#                gym"), any romance (interact.rpy:1381 romance_scope
#                "friendship_only") — neither is written here.
#
# ponytail: the everyday beats are dispatched through Talk rather than through
# a per-location entry hook. Ceiling: Marcus never opens a beat before you
# speak to him, so the pool reads as "he leads the conversation", not "he
# ambushes you at the door". Upgrade path — add check_* functions to the
# location_park / location_bar Tier A chains in locations.rpy; the beat labels
# are already location-neutral (no `scene`) so they need no rewriting.
# ═══════════════════════════════════════════════════════════════════════════

# ── State ───────────────────────────────────────────────────────────────────
# Every flag below has a named callback. Nothing here stores something Marcus
# could not plausibly have been told or seen.
default marcus_mc_checkin_done      = False   # first-week survive-the-night check
default mc_told_marcus_interview    = False   # MC mentioned an upcoming interview
default marcus_interview_told_day   = -1      # when — drives the 2-day text callback
default marcus_interview_text_sent  = False
default mc_told_marcus_job_trouble  = False   # MC said they dislike the job
default marcus_job_trouble_career   = None    # WHICH job — so "still hate that
                                              # place?" cannot fire about a job
                                              # MC already left
default marcus_job_trouble_day      = -1
default marcus_job_trouble_text_sent = False
default mc_told_marcus_career_good  = False   # MC said the job is fine
default marcus_heard_job_got        = False   # Marcus knows MC is employed
default marcus_heard_promotion      = False   # promotion reaction delivered
default marcus_promo_text_sent      = False
default marcus_known_career         = None    # the career MC last discussed
default marcus_known_rank           = -1      # its rank at that moment
default marcus_had_a_day_last       = -1      # day of the last "I've had a day"
default marcus_had_a_day_topic      = ""      # so MC can ask about it same-day
default marcus_work_check_last      = -1      # day of the last "how's work"
default marcus_ran_out_of_chili     = False   # set by the chili story; read by
                                              # the food-run callback
default marcus_beat_last_day        = -1      # one friendship beat per day
default marcus_ctx_talk_last_day    = -1      # one contextual Talk menu per day
default marcus_bball_talk_done      = False
default marcus_five_am_talk_done    = False
default marcus_court_offer_last_day = -999
default marcus_still_alive_done     = False   # the day 2-5 "Still alive." beat
default marcus_lock_joke_active     = False   # MC took the lock branch of it
default marcus_career_good_day      = -1      # when MC said the job was good —
                                              # drives the 3-7 day callback
default marcus_job_callback_done    = False   # "still hate that place?" answered
                                              # once for THIS complaint
default marcus_five_am_known        = False   # MC has heard the 5/6 AM truth,
                                              # from the scene, the Talk option
                                              # or arc_marcus_sports_1
default mc_knows_marcus_bball_offer = False   # MC has heard about the semi-pro
                                              # offer (arc_marcus_sports_2)
default marcus_last_seen_day        = -999    # stamped in marcus_greet, read
                                              # BEFORE npc_last_seen overwrites
default marcus_greet_late_done      = False   # the "You're late." one-shot
default marcus_greet_late_day       = -999
default marcus_greet_gap            = 0       # days since last seen, captured
                                              # in marcus_greet for the farewell


init 5 python:

    # ── Sprite selection ─────────────────────────────────────────────────────
    # Beat labels never `scene` or `show` — the interaction UI owns the sprite
    # (see talk_followup_marcus_first_shift, interact.rpy:2355). This map only
    # exists for the Scene Tester launcher, which has no UI around it.
    _MF_SPRITES = {
        "location_bar":  {"normal": "marcus_bar_normal",   "talk": "marcus_bar_talk",
                          "laugh":  "marcus_bar_talk",     "sad":  "marcus_bar_normal"},
        "location_park": {"normal": "marcus_park_neutral", "talk": "marcus_park_talk",
                          "laugh":  "marcus_park_laugh",   "sad":  "marcus_park_sad"},
    }
    _MF_SPRITES_DEFAULT = {"normal": "marcus_casual_normal", "talk": "marcus_casual_talk",
                           "laugh":  "marcus_casual_laugh",  "sad":  "marcus_casual_worried"}

    def mf_sprite(expr="talk"):
        table = _MF_SPRITES.get(store.current_loc, _MF_SPRITES_DEFAULT)
        return table.get(expr, table["normal"])

    # ── Career reading ───────────────────────────────────────────────────────
    # apply_job() writes {"rank": 0}; promote() raises it. So rank 0 == the job
    # is new, rank >= 1 == MC has been promoted at least once.
    def mf_career():
        """(state, career_id, rank). state in none/new/established."""
        ac = store.active_careers
        if not ac:
            return ("none", None, -1)
        cid = store.job_id if store.job_id in ac else sorted(ac.keys())[0]
        rank = ac.get(cid, {}).get("rank", 0)
        return (("new" if rank <= 0 else "established"), cid, rank)

    def mf_career_name():
        _s, cid, _r = mf_career()
        if cid is None:
            return "the job"
        try:
            return CAREERS[cid]["name"]
        except Exception:
            return store.job_title or "the job"

    def mf_sync_known():
        """Single write point for 'Marcus has now been told where MC works'."""
        _s, cid, rank = mf_career()
        store.marcus_known_career = cid
        store.marcus_known_rank   = rank
        if cid is not None:
            store.marcus_heard_job_got = True

    def mf_promotion_due():
        """A promotion Marcus has not reacted to yet. Word of mouth already
        carries it (careers.rpy:466 publish_player_fact('got_promoted')), so
        him knowing is not a leap."""
        _s, cid, rank = mf_career()
        if cid is None or rank < 1:
            return False
        if store.marcus_known_career != cid:
            return False
        return rank > store.marcus_known_rank

    def mf_job_change_since_complaint():
        """MC complained about a job and is no longer in it."""
        if not store.mc_told_marcus_job_trouble:
            return False
        _s, cid, _r = mf_career()
        return cid != store.marcus_job_trouble_career

    def mf_interview_unresolved():
        """MC said an interview was coming and Marcus has not since been told
        where MC works. He cannot read an employment contract — the ONLY thing
        that closes this thread without an answer is him already knowing the
        current job, which is exactly marcus_known_career matching it."""
        if not store.mc_told_marcus_interview:
            return False
        _s, cid, _r = mf_career()
        if cid is not None and store.marcus_known_career == cid:
            return False
        return True

    def mf_recent_career_win():
        """A career milestone in the last 3 days that the city can hear about.
        Reads the two existing records — the journal entry promote() writes and
        the Phase 68 public fact — rather than inventing a new signal."""
        for e in store.player_journal:
            if e.get("category") == "career" and store.day - e.get("day", -999) <= 3:
                return True
        for f in store.public_player_facts.values():
            if f.get("type") == "got_promoted" and store.day - f.get("day", -999) <= 3:
                return True
        return False

    def mf_rough_patch():
        """Something Marcus can see for himself: MC is worn out and employed."""
        _s, cid, _r = mf_career()
        return cid is not None and worn_out()

    # ── Old-save backfill ────────────────────────────────────────────────────
    def _marcus_backfill():
        """A save from before this file existed can already be forty days into
        knowing Marcus. Deriving the flags is what stops a first-week check-in
        firing at a close friend. Idempotent."""
        # Derived every load, not once: the two sports arcs can be completed
        # through the ordinary Talk grid at any point, and the phone/beat gates
        # that read these flags must not lag behind that.
        _arcs = store.topic_arc_done
        if _arcs.get("marcus_sports_1") or store.marcus_five_am_talk_done:
            store.marcus_five_am_known = True
        if _arcs.get("marcus_sports_2"):
            store.mc_knows_marcus_bball_offer = True

        if store.marcus_mc_checkin_done:
            return
        try:
            stage = npc_relationship_stage("marcus")
        except Exception:
            stage = "stranger"
        if store.day > 6 or stage in ("friendly", "friend", "close", "trusted"):
            store.marcus_mc_checkin_done = True
            # He also already knows where MC works, if anywhere.
            if store.active_careers and store.marcus_known_career is None:
                mf_sync_known()

    try:
        if _marcus_backfill not in config.after_load_callbacks:
            config.after_load_callbacks.append(_marcus_backfill)
    except Exception:
        pass

    # ── Daily tick ───────────────────────────────────────────────────────────
    # Hung off _check_npc_initiative (data.rpy:1065 calls it once per new_day,
    # right after _zoe_bootstrap_tick). Wrapping it instead of editing
    # new_day() keeps the ordering guarantee: Zoe's scripted bootstrap texts
    # are queued first, then Marcus's scripted texts, and only then does the
    # shared one-contact-per-day picker run. None of the three compete, because
    # queue_phone_message does not spend the initiative budget.
    def _marcus_daily_tick():
        _marcus_backfill()

        # Interview callback — 2 days after MC mentioned it, and only while the
        # career state has not already answered the question.
        if (store.mc_told_marcus_interview and not store.marcus_interview_text_sent
                and store.marcus_interview_told_day >= 0
                and store.day >= store.marcus_interview_told_day + 2
                and mf_interview_unresolved()
                and "marcus" in store.npc_contacts):
            queue_phone_message("marcus", "Did the interview happen?",
                                store.day, "marcus_interview_callback",
                                responses=_MARCUS_INTERVIEW_CB_RESP)
            store.marcus_interview_text_sent = True

        # Job-trouble callback — a decent gap, and never about a job MC left.
        if (store.mc_told_marcus_job_trouble and not store.marcus_job_trouble_text_sent
                and store.marcus_job_trouble_day >= 0
                and store.day >= store.marcus_job_trouble_day + 5
                and not mf_job_change_since_complaint()
                and "marcus" in store.npc_contacts):
            queue_phone_message("marcus", "Still at that place you hated?",
                                store.day, "marcus_jobtrouble_callback",
                                responses=_MARCUS_JOBTROUBLE_CB_RESP)
            store.marcus_job_trouble_text_sent = True

        # Promotion congratulation — once, and only for a promotion the city
        # actually heard about.
        if (not store.marcus_promo_text_sent and mf_promotion_due()
                and "marcus" in store.npc_contacts):
            queue_phone_message(
                "marcus",
                "Heard you moved up. Drinks on me. Cheap drinks. I'm not made of money.",
                store.day, "marcus_promotion_callback",
                responses=_MARCUS_PROMO_CB_RESP)
            store.marcus_promo_text_sent = True

    _check_npc_initiative_pre_marcus = _check_npc_initiative

    def _check_npc_initiative():
        _marcus_daily_tick()
        _check_npc_initiative_pre_marcus()

    # ── Talk router ──────────────────────────────────────────────────────────
    # Same interception zoe_onboarding.rpy uses on this function. The original
    # keeps absolute priority; this only ever answers when it declined. Every
    # branch below is once-per-day at most, and each ends by handing control
    # back — the generic "Talk about..." grid is never removed.
    _check_talk_followup_pre_marcus = _check_talk_followup

    def _check_talk_followup(npc_id):
        result = _check_talk_followup_pre_marcus(npc_id)
        if result is not None:
            return result
        if npc_id != "marcus" or not store.marcus_met:
            return None
        # 1. First week.
        if mf_first_week_checkin_ready():
            return "marcus_first_week_checkin"
        # 2. A callback he is owed, or that MC owes him.
        if mf_ctx_options(high_only=True):
            return "marcus_ctx_talk"
        # 3. He leads with something of his own.
        beat = mf_pick_beat()
        if beat is not None:
            return beat
        # 4. Ordinary contextual openers.
        if mf_ctx_options():
            return "marcus_ctx_talk"
        return None

    def mf_first_week_checkin_ready():
        return (not store.marcus_mc_checkin_done
                and store.marcus_met
                and store.move_in_complete)

    # ── Contextual Talk options ──────────────────────────────────────────────
    # (id, menu text, priority) — priority 1 items are callbacks and jump the
    # queue; priority 2 items are ordinary and only surface once a day.
    def mf_ctx_options(high_only=False):
        out = []
        _s, cid, _r = mf_career()
        if mf_interview_unresolved() and store.marcus_interview_told_day >= 0:
            out.append(("interview", "Tell him how the interview went", 1))
        # Only when MC has news he does not have. The recurring "still hate
        # that place?" belongs to marcus_beat_that_job_again — this is the
        # MC-volunteers-it half, so the two never contend.
        if mf_job_change_since_complaint():
            out.append(("jobupdate", "Update him on work", 1))
        if store.marcus_had_a_day_last == store.day and store.marcus_had_a_day_topic:
            out.append(("whathappened", "Ask what happened", 1))
        if high_only:
            return out
        if store.marcus_ctx_talk_last_day == store.day:
            return []
        try:
            stage = npc_relationship_stage("marcus")
        except Exception:
            stage = "stranger"
        if stage in ("friendly", "friend", "close", "trusted"):
            out.append(("week", "\"How's your week going?\"", 2))
        # Only once MC actually knows about the offer — the line references it
        # directly, so without arc_marcus_sports_2 it is MC quoting something
        # nobody told them.
        if (stage in ("friend", "close", "trusted")
                and store.mc_knows_marcus_bball_offer
                and not store.marcus_bball_talk_done):
            out.append(("basketball", "Ask about the basketball", 2))
        if stage in ("friend", "close", "trusted") and not store.marcus_five_am_talk_done:
            out.append(("fiveam", "\"Do you actually get up at six?\"", 2))
        return out


# ═══════════════════════════════════════════════════════════════════════════
# FIRST-WEEK CHECK-IN
# ═══════════════════════════════════════════════════════════════════════════
# Reachable two ways, both already existing routes: this Talk branch, and the
# marcus_msg_first_week initiative text (registered below). Whichever lands
# first sets the flag; the other stands down.
label marcus_first_week_checkin:
    $ marcus_mc_checkin_done = True
    $ _do_talk_accounting("marcus")
    m "Apartment still standing?"
    menu:
        "\"Mostly.\"":
            mc "Mostly."
            m "Mostly is the correct answer. Anyone who says yes hasn't looked behind the fridge."
        "\"The lock's still trying to kill me.\"":
            mc "The lock's still trying to kill me."
            m "Lift the handle. I told you. Lift, then turn."
            mc "I lift. It doesn't care."
            m "It cares. It's just proud."
        "\"I slept about four hours.\"":
            mc "I slept about four hours."
            m "First night in a new place. That's standard."
            m "Second night you'll sleep like the dead and wake up confused about which wall the window's on."

    $ _s, _cid, _rk = mf_career()
    if _cid is not None:
        m "You've got something lined up already, right? Work."
        mc "Yeah. [job_title]."
        m "Huh."
        "He takes that in without commentary, which from Marcus is closer to approval than most things he says out loud."
        $ mf_sync_known()
    else:
        m "Any idea what you're doing for work?"
        menu:
            "\"Not a clue.\"":
                mc "Not a clue."
                m "Fair enough."
                "He doesn't fill the pause with advice. He just lets it sit there, which is somehow less awkward than if he had."
            "\"I've got an interview coming up.\"":
                mc "I've got an interview coming up."
                $ mc_told_marcus_interview  = True
                $ marcus_interview_told_day = day
                $ add_relationship_memory("marcus", "marcus_knows_interview",
                                          "I told Marcus about an interview", category="career")
                m "Alright."
                m "I'm not going to ask what it is. You'll tell me if it goes well and lie about it if it doesn't."
            "\"Something that isn't this.\"":
                mc "Something that isn't this."
                m "That's most people's plan. It works out about half the time."
                mc "Encouraging."
                m "I said half."

    m "Anyway. Fourteen. Knock if the water does the thing."
    # Contact exchange. The same one line interact.rpy's "number" action runs —
    # earned by the conversation rather than by an affection threshold. Without
    # it _texting_tier("marcus") is None and EVERY Marcus text, including the
    # ones that shipped before this pass, is unreachable.
    if "marcus" not in npc_contacts:
        m "Actually — give me your phone. Knocking's fine but it's a lot of stairs."
        "He puts himself in under \"Marcus 14\", which is either a joke about the door or a filing system."
        $ store.npc_contacts = store.npc_contacts + ["marcus"]
    $ apply_relationship_change("marcus", source_id="marcus_first_week_checkin",
                                source_category="meaningful_talk",
                                trust=1, familiarity=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTUAL TALK
# ═══════════════════════════════════════════════════════════════════════════
# Priority menu. "More topics..." reproduces the exact three lines from
# npc_interact's generic branch (interact.rpy:2043-2049), so the standard Talk
# grid stays reachable from here.
label marcus_ctx_talk:
    $ _mf_opts = mf_ctx_options()
    if not _mf_opts:
        $ _mf_opts = mf_ctx_options(high_only=True)
    $ marcus_ctx_talk_last_day = day
    $ _mf_menu = [(_t, _i) for _i, _t, _p in sorted(_mf_opts, key=lambda o: o[2])]
    $ _mf_menu.append(("More topics...", "more"))
    $ _mf_pick = renpy.display_menu(_mf_menu)

    if _mf_pick == "interview":
        call marcus_ctx_interview
    elif _mf_pick == "jobupdate":
        call marcus_ctx_job_update
    elif _mf_pick == "whathappened":
        call marcus_ctx_what_happened
    elif _mf_pick == "week":
        call marcus_ctx_week
    elif _mf_pick == "basketball":
        call marcus_ctx_basketball
    elif _mf_pick == "fiveam":
        call marcus_ctx_five_am
    else:
        $ _mf_t = renpy.call_screen("npc_topics", "marcus")
        if _mf_t != "back":
            $ _mf_arc = check_arc("marcus", _mf_t)
            if _mf_arc is not None:
                call expression _mf_arc["label"]
            else:
                $ do_talk("marcus", _mf_t)
    return


label marcus_ctx_interview:
    $ _do_talk_accounting("marcus")
    $ mc_told_marcus_interview = False
    $ _s, _cid, _rk = mf_career()
    m "So. The interview."
    if _cid is not None and _cid != marcus_known_career:
        mc "I got it."
        m "Course you did."
        mc "You have no idea what the job is."
        m "I know you turned up. That's most of it."
        $ mf_sync_known()
        $ apply_relationship_change("marcus", source_id="marcus_interview_good",
                                    source_category="meaningful_talk",
                                    affection=1, respect=1, trust=2)
    else:
        menu:
            "\"It didn't happen.\"":
                mc "It didn't happen."
                m "Okay."
                m "That's not a story. That's a Tuesday."
            "\"They went with someone else.\"":
                mc "They went with someone else."
                m "Right."
                "He doesn't say anything encouraging. He also doesn't change the subject, which is the part you notice."
                m "You want the bad news or the actual news?"
                mc "There's a difference?"
                m "Bad news is you didn't get it. Actual news is you got asked in. Those are different sentences."
            "\"Still waiting.\"":
                mc "Still waiting."
                m "Then stop checking your phone every nine minutes. I can see you doing it."
        $ apply_relationship_change("marcus", source_id="marcus_interview_followup",
                                    source_category="meaningful_talk",
                                    trust=2, familiarity=1)
    $ add_relationship_memory("marcus", "marcus_interview_answered",
                              "Marcus asked how the interview went", category="career")
    return


label marcus_ctx_job_update:
    $ _do_talk_accounting("marcus")
    $ _s, _cid, _rk = mf_career()
    if mf_job_change_since_complaint():
        m "Wait. You're not at that place anymore."
        mc "No."
        m "Good. That place sucked."
        mc "You never went there."
        m "I didn't have to. I heard about it every time you sat down."
        $ mc_told_marcus_job_trouble = False
        $ marcus_job_trouble_career  = None
        $ mf_sync_known()
        $ apply_relationship_change("marcus", source_id="marcus_job_upgraded",
                                    source_category="meaningful_talk",
                                    trust=2, affection=1)
    else:
        m "Still hate that place?"
        menu:
            "\"Less than I did.\"":
                mc "Less than I did."
                m "That's how it usually goes. It stops being a crisis and starts being a Tuesday."
                $ mc_told_marcus_job_trouble = False
                $ mc_told_marcus_career_good = True
            "\"More, actually.\"":
                mc "More, actually."
                m "Yeah."
                "He doesn't argue with it. He also doesn't tell you to quit, which is the advice everyone else leads with."
                m "You don't have to decide anything today."
                $ marcus_job_trouble_day = day
                $ marcus_job_trouble_text_sent = False
            "\"I don't want to talk about it.\"":
                mc "I don't want to talk about it."
                m "Done."
                "And it is. He moves straight on to something about a delivery he's been arguing with all week."
        $ apply_relationship_change("marcus", source_id="marcus_job_update",
                                    source_category="meaningful_talk",
                                    trust=2, familiarity=1)
    return


label marcus_ctx_what_happened:
    $ _do_talk_accounting("marcus")
    mc "You said you'd had a day. What happened?"
    if marcus_had_a_day_topic == "delivery":
        m "Twelve crates of tonic. I ordered two."
        mc "What are you going to do with twelve crates of tonic?"
        m "I've had four hours to think about that and I've got nothing."
    elif marcus_had_a_day_topic == "cancelled":
        m "Guy cancelled. Two hours before. Text of one word."
        mc "Which word?"
        m "\"Rain.\""
        mc "Was it raining?"
        m "It was not raining."
    elif marcus_had_a_day_topic == "game":
        m "We were up nine with four minutes left."
        mc "And?"
        m "And I'd rather talk about the tonic."
    elif marcus_had_a_day_topic == "chili":
        m "I tried making something that wasn't chili."
        mc "How was it?"
        m "It was food. Technically."
        m "Never again."
        $ marcus_ran_out_of_chili = True
    else:
        m "Nothing that survives being explained out loud."
        mc "Try me."
        m "No. It was funnier when it was happening to me."
    $ marcus_had_a_day_topic = ""
    $ apply_relationship_change("marcus", source_id="marcus_asked_what_happened",
                                source_category="meaningful_talk",
                                trust=1, familiarity=1)
    return


label marcus_ctx_week:
    $ _do_talk_accounting("marcus")
    mc "How's your week going?"
    $ _mf_life = npc_life_state("marcus")
    if _mf_life == "busy_work":
        m "Long. Two people off, so I'm doing three jobs and none of them well."
    elif _mf_life == "social_week":
        m "Busy. Good busy. I've said yes to about four things I should have said no to."
    elif _mf_life == "training_focus":
        m "Six every morning. Even the ones where it's raining and I hate myself."
    elif _mf_life == "stressed_week":
        m "It's been a week."
        "He leaves it at that, and it's clear he'd rather it stayed there."
    else:
        m "Same shape as every week. Bar, park, bar."
        mc "That's not a week, that's a loop."
        m "It's a loop I picked."
    $ apply_relationship_change("marcus", source_id="marcus_week_check",
                                source_category="casual_talk",
                                trust=1, familiarity=1)
    return


label marcus_ctx_basketball:
    $ marcus_bball_talk_done = True
    $ _do_talk_accounting("marcus")
    mc "You still play? Properly, I mean."
    m "Define properly."
    mc "The way you played when someone offered you money for it."
    "That lands. He doesn't flinch, but he takes a second."
    m "No."
    m "I play the way you play when nobody's counting. Which is better, honestly. Nobody's counting."
    mc "You count."
    m "I count a bit."
    $ apply_relationship_change("marcus", source_id="marcus_basketball_talk",
                                source_category="meaningful_talk",
                                affection=1, familiarity=2, trust=1)
    return


label marcus_ctx_five_am:
    $ marcus_five_am_talk_done = True
    $ marcus_five_am_known     = True
    $ complete_arc("marcus_sports_1")
    $ _do_talk_accounting("marcus")
    mc "Do you actually get up at six? Every day?"
    m "Six every day. Even weekends."
    mc "That's discipline."
    m "That's what people say."
    m "Really I just can't sleep past five, so I've had an hour to lie there and decide it was my idea."
    $ apply_relationship_change("marcus", source_id="marcus_five_am_talk",
                                source_category="casual_talk",
                                affection=1, familiarity=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# PHONE — registered into the EXISTING initiative pool
# ═══════════════════════════════════════════════════════════════════════════
# phone_actionable.rpy owns the picker, the one-contact-per-day budget, the
# per-NPC cooldown and the tier gate. All this block does is extend its data
# tables, which is exactly how Phases 49/50 added their own variants.
#
# Tiers: 0 acquaintance, 1 familiar, 2 close, 3 very close.
# None of these variants is in _INV_VARIANTS except marcus_msg_court — the
# rest deliberately create no commitment and go nowhere. That is the point.
init 6 python:

    _MARCUS_FIRST_WEEK_RESP = [
        {"id": "mostly", "text": "Mostly.",                       "label": "npc_ini_marcus_first_week_mostly"},
        {"id": "lock",   "text": "The lock's still winning.",     "label": "npc_ini_marcus_first_week_lock"},
        {"id": "fine",   "text": "It's fine. Really.",            "label": "npc_ini_marcus_first_week_fine"},
    ]
    _MARCUS_WORKGO_RESP = [
        {"id": "fine",   "text": "Fine.",                         "label": "npc_ini_marcus_workgo_fine"},
        {"id": "bad",    "text": "Bad.",                          "label": "npc_ini_marcus_workgo_bad"},
        {"id": "long",   "text": "Long.",                         "label": "npc_ini_marcus_workgo_long"},
    ]
    _MARCUS_SLEEP_RESP = [
        {"id": "will",   "text": "I will.",                       "label": "npc_ini_marcus_sleep_will"},
        {"id": "wont",   "text": "I won't.",                      "label": "npc_ini_marcus_sleep_wont"},
        {"id": "rude",   "text": "Rude.",                         "label": "npc_ini_marcus_sleep_rude"},
    ]
    _MARCUS_COURT_RESP = [
        {"id": "yes",    "text": "Court later. Yeah.",            "label": "npc_ini_marcus_court_yes"},
        {"id": "maybe",  "text": "Maybe.",                        "label": "npc_ini_marcus_court_maybe"},
        {"id": "no",     "text": "Can't today.",                  "label": "npc_ini_marcus_court_no"},
    ]
    _MARCUS_SQUATRACK_RESP = [
        {"id": "angry",  "text": "I am angry about this.",        "label": "npc_ini_marcus_squatrack_angry"},
        {"id": "forty",  "text": "Forty minutes?",                "label": "npc_ini_marcus_squatrack_forty"},
        {"id": "why",    "text": "Why were you counting?",        "label": "npc_ini_marcus_squatrack_why"},
    ]
    _MARCUS_NOTCHILI_RESP = [
        {"id": "what",   "text": "What was it?",                  "label": "npc_ini_marcus_notchili_what"},
        {"id": "good",   "text": "Was it good?",                  "label": "npc_ini_marcus_notchili_good"},
        {"id": "brave",  "text": "Brave.",                        "label": "npc_ini_marcus_notchili_brave"},
    ]
    _MARCUS_ZOEMUSIC_RESP = [
        {"id": "agree",  "text": "She's right.",                  "label": "npc_ini_marcus_zoemusic_agree"},
        {"id": "defend", "text": "Defend yourself.",              "label": "npc_ini_marcus_zoemusic_defend"},
        {"id": "what",   "text": "What did you play?",            "label": "npc_ini_marcus_zoemusic_what"},
    ]
    _MARCUS_NOREASON_RESP = [
        {"id": "why",    "text": "Why?",                          "label": "npc_ini_marcus_noreason_why"},
        {"id": "hi",     "text": "Hi.",                           "label": "npc_ini_marcus_noreason_hi"},
        {"id": "ok",     "text": "Okay.",                         "label": "npc_ini_marcus_noreason_ok"},
    ]
    # ── Authored message pack ───────────────────────────────────────────────
    # ponytail: where the screenplay gives Marcus a second line ("Vending
    # machine won.") it is joined into the same bubble with a newline rather
    # than delivered as a second text. Ceiling: one bubble, two lines, instead
    # of two timestamps. Upgrade path — queue_phone_message the tail from the
    # reply label, or give npc_messages a "tail" field.
    #
    # Every MC response below is a line MC already says somewhere canonical, and
    # every Marcus reply is a line Marcus already says. Nothing new is written.
    _MARCUS_HUNGRY_RESP = [
        {"id": "sentence", "text": "That's not a sentence.",       "label": "npc_ini_marcus_hungry_sentence"},
    ]
    _MARCUS_GOOD_RESP = [
        {"id": "yeah",   "text": "Yeah.",                          "label": "npc_ini_marcus_good_yeah"},
        {"id": "not",    "text": "Not really.",                    "label": "npc_ini_marcus_good_not"},
    ]
    _MARCUS_TONIGHT_RESP = [
        {"id": "sure",   "text": "Sure.",                          "label": "npc_ini_marcus_tonight_sure"},
        {"id": "not",    "text": "Not tonight.",                   "label": "npc_ini_marcus_tonight_not"},
    ]
    _MARCUS_FIVEAM_RESP = [
        {"id": "flex",   "text": "That's not a flex.",             "label": "npc_ini_marcus_fiveam_flex"},
        {"id": "brave",  "text": "Brave.",                         "label": "npc_ini_marcus_fiveam_brave"},
    ]
    _MARCUS_FREE_RESP = [
        {"id": "why2",   "text": "Yeah. Why?",                     "label": "npc_ini_marcus_free_yeah"},
        {"id": "why",    "text": "Why?",                           "label": "npc_ini_marcus_free_why"},
    ]

    # Scripted callbacks — queued directly by _marcus_daily_tick, not by the picker.
    _MARCUS_INTERVIEW_CB_RESP = [
        {"id": "got",    "text": "I got it.",                     "label": "npc_ini_marcus_interview_cb_got"},
        {"id": "didnt",  "text": "I didn't get it.",              "label": "npc_ini_marcus_interview_cb_didnt"},
        {"id": "waiting","text": "Still waiting.",                "label": "npc_ini_marcus_interview_cb_waiting"},
    ]
    _MARCUS_JOBTROUBLE_CB_RESP = [
        {"id": "still",  "text": "Still there.",                  "label": "npc_ini_marcus_jobtrouble_cb_still"},
        {"id": "left",   "text": "Not anymore.",                  "label": "npc_ini_marcus_jobtrouble_cb_left"},
        {"id": "better", "text": "It got better.",                "label": "npc_ini_marcus_jobtrouble_cb_better"},
    ]
    _MARCUS_PROMO_CB_RESP = [
        {"id": "yes",    "text": "Cheap drinks it is.",           "label": "npc_ini_marcus_promo_cb_yes"},
        {"id": "how",    "text": "How did you hear?",             "label": "npc_ini_marcus_promo_cb_how"},
        {"id": "modest", "text": "It's not a big deal.",          "label": "npc_ini_marcus_promo_cb_modest"},
    ]

    _INITIATIVE_MSGS.update({
        # Check-ins — low tier, the common case.
        "marcus_msg_first_week":  {"text": "Apartment still standing?",
                                   "responses": _MARCUS_FIRST_WEEK_RESP},
        "marcus_msg_workgo":      {"text": "How'd work go?",
                                   "responses": _MARCUS_WORKGO_RESP},
        "marcus_msg_sleep":       {"text": "You looked dead earlier. Sleep.",
                                   "responses": _MARCUS_SLEEP_RESP},
        # Invitation — the only one here that can become a commitment.
        "marcus_msg_court":       {"text": "Court later?",
                                   "responses": _MARCUS_COURT_RESP},
        # Own-life observations — no action, no commitment, pure texture.
        "marcus_msg_squatrack":   {"text": "Guy at the gym just did curls in the squat rack for forty minutes. I need you to be angry about this with me.",
                                   "responses": _MARCUS_SQUATRACK_RESP},
        "marcus_msg_notchili":    {"text": "I tried cooking something that wasn't chili.",
                                   "responses": _MARCUS_NOTCHILI_RESP},
        "marcus_msg_zoemusic":    {"text": "Apparently Zoe thinks my taste in music is a public safety issue.",
                                   "responses": _MARCUS_ZOEMUSIC_RESP},
        "marcus_msg_noreason":    {"text": "No reason. Just checking the phone works.",
                                   "responses": _MARCUS_NOREASON_RESP},
        # ── Authored pack (M1-M8 + the Scene 8 opener) ──────────────────────
        "marcus_msg_alive":       {"text": "You alive?\nHaven't seen you around.",
                                   "responses": _MARCUS_NOREASON_RESP},
        "marcus_msg_hungry":      {"text": "Food?",
                                   "responses": _MARCUS_HUNGRY_RESP},
        "marcus_msg_court30":     {"text": "Court in 30.\nThis is me asking politely.",
                                   "responses": _MARCUS_COURT_RESP},
        "marcus_msg_howdit":      {"text": "How'd it go?",
                                   "responses": _MARCUS_INTERVIEW_CB_RESP},
        "marcus_msg_vending":     {"text": "I just watched a guy argue with a vending machine.\nVending machine won.",
                                   "responses": _MARCUS_NOREASON_RESP},
        "marcus_msg_tonight":     {"text": "You doing anything tonight?",
                                   "responses": _MARCUS_TONIGHT_RESP},
        "marcus_msg_minute":      {"text": "Haven't seen you in a minute.\nYou good?",
                                   "responses": _MARCUS_GOOD_RESP},
        "marcus_msg_fiveam":      {"text": "Been awake since 5.\nStill not impressive.",
                                   "responses": _MARCUS_FIVEAM_RESP},
        "marcus_msg_free":        {"text": "You free?",
                                   "responses": _MARCUS_FREE_RESP},
    })

    _INITIATIVE_VARIANTS["marcus"] = _INITIATIVE_VARIANTS["marcus"] + [
        "marcus_msg_first_week", "marcus_msg_workgo", "marcus_msg_sleep",
        "marcus_msg_court", "marcus_msg_squatrack", "marcus_msg_notchili",
        "marcus_msg_zoemusic", "marcus_msg_noreason",
        "marcus_msg_alive", "marcus_msg_hungry", "marcus_msg_court30",
        "marcus_msg_howdit", "marcus_msg_vending", "marcus_msg_tonight",
        "marcus_msg_minute", "marcus_msg_fiveam", "marcus_msg_free",
    ]

    _INV_VARIANTS.add("marcus_msg_court")
    # "Court in 30" is a real commitment, same as "Court later?".
    _INV_VARIANTS.add("marcus_msg_court30")

    _VARIANT_WEIGHTS.update({
        "marcus_msg_first_week": 6,   # heavily favoured while it is eligible at all
        "marcus_msg_workgo":     4,
        "marcus_msg_sleep":      3,
        "marcus_msg_court":      2,   # invitation weight, same as marcus_msg_park
        "marcus_msg_squatrack":  3,
        "marcus_msg_notchili":   3,
        "marcus_msg_zoemusic":   3,
        "marcus_msg_noreason":   2,
        "marcus_msg_alive":      3,
        "marcus_msg_hungry":     3,
        "marcus_msg_court30":    2,
        "marcus_msg_howdit":     5,   # only eligible with real pending context
        "marcus_msg_vending":    3,
        "marcus_msg_tonight":    3,
        "marcus_msg_minute":     4,
        "marcus_msg_fiveam":     2,
        "marcus_msg_free":       2,
    })

    _VARIANT_MIN_TIER.update({
        "marcus_msg_first_week": 0,
        "marcus_msg_workgo":     0,
        "marcus_msg_sleep":      1,
        "marcus_msg_court":      1,
        "marcus_msg_squatrack":  1,
        "marcus_msg_notchili":   1,
        "marcus_msg_zoemusic":   1,
        "marcus_msg_noreason":   2,
        "marcus_msg_alive":      0,
        "marcus_msg_hungry":     1,
        "marcus_msg_court30":    1,
        "marcus_msg_howdit":     0,
        "marcus_msg_vending":    1,
        "marcus_msg_tonight":    1,
        "marcus_msg_minute":     2,
        "marcus_msg_fiveam":     1,
        "marcus_msg_free":       2,
    })

    _VARIANT_CONDITIONS.update({
        # Day 1-4 only, and only if the Talk route has not already run it.
        "marcus_msg_first_week": lambda: (not store.marcus_mc_checkin_done
                                          and store.day <= 4),
        "marcus_msg_workgo":     lambda: (store.marcus_heard_job_got
                                          and bool(store.active_careers)),
        "marcus_msg_sleep":      lambda: store.last_day_worn_out,
        "marcus_msg_court":      lambda: (store.npc_invitation_pending is None
                                          and store.day - store.marcus_court_offer_last_day >= 6),
        # Only after MC has actually met Zoe — otherwise it is a text about a
        # stranger. zoe_properly_introduced is zoe_onboarding.rpy's flag.
        "marcus_msg_zoemusic":   lambda: store.zoe_properly_introduced,
        "marcus_msg_notchili":   lambda: store.marcus_chili,
        # ── Authored pack gates ─────────────────────────────────────────────
        # M1: a real gap since he last actually saw MC.
        "marcus_msg_alive":      lambda: (store.day - store.npc_last_seen.get("marcus", -999)) >= 4,
        # M3: same commitment guard the other court text uses.
        "marcus_msg_court30":    lambda: (store.npc_invitation_pending is None
                                          and store.day - store.marcus_court_offer_last_day >= 6),
        # M4: NEVER without something he is actually waiting to hear about.
        # mf_interview_unresolved() is the only such thread in the game — if MC
        # never told him about an interview this can never fire.
        "marcus_msg_howdit":     lambda: (store.mc_told_marcus_interview
                                          and store.marcus_interview_told_day >= 0
                                          and store.day > store.marcus_interview_told_day
                                          and mf_interview_unresolved()),
        # M6: early friendship, before "no reason" is allowed.
        "marcus_msg_tonight":    lambda: _mf_stage() in ("friendly", "friend"),
        # M7: after an absence, friend stage.
        "marcus_msg_minute":     lambda: (_mf_friendly()
                                          and (store.day - store.npc_last_seen.get("marcus", -999)) >= 6),
        # M8: only once MC has heard the 5 AM truth, from any of the three routes.
        "marcus_msg_fiveam":     lambda: store.marcus_five_am_known,
        # Scene 8's opener. Friend stage, same gate as the beat itself.
        "marcus_msg_free":       lambda: _mf_stage() in ("friend", "close", "trusted"),
    })

    # Early-window pacing. The base cooldown is 3 (phone_actionable.rpy
    # _INITIATIVE_COOLDOWNS); for the first fortnight Marcus texts a little
    # more, which is what a new friend actually does.
    # ponytail: implemented as a wrapper on _effective_cooldown rather than a
    # curve. Ceiling: one flat -1 for 14 days. Upgrade path — make
    # _INITIATIVE_COOLDOWNS a callable per NPC if another character needs this.
    _effective_cooldown_pre_marcus = _effective_cooldown

    def _effective_cooldown(npc_id):
        base = _effective_cooldown_pre_marcus(npc_id)
        if npc_id == "marcus" and store.day <= 14 and store.marcus_met:
            return max(_MIN_EFFECTIVE_COOLDOWN, base - 1)
        return base


# ── Reply labels ────────────────────────────────────────────────────────────
# Same shape as every npc_ini_marcus_* label in phone_actionable.rpy: a reply
# text, then _clear_initiative_pending. Scripted-callback labels are not in the
# picker so they do not clear pending.

label npc_ini_marcus_first_week_mostly:
    $ marcus_mc_checkin_done = True
    $ queue_phone_message("marcus", "Mostly is the correct answer.", day, "marcus_msg_first_week_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_first_week_lock:
    $ marcus_mc_checkin_done = True
    $ queue_phone_message("marcus", "Lift the handle. LIFT. Then turn.", day, "marcus_msg_first_week_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_first_week_fine:
    $ marcus_mc_checkin_done = True
    $ queue_phone_message("marcus", "Sure. Knock on fourteen when it isn't.", day, "marcus_msg_first_week_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_workgo_fine:
    $ mc_told_marcus_career_good = True
    $ mf_sync_known()
    $ queue_phone_message("marcus", "Fine is underrated.", day, "marcus_msg_workgo_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_workgo_bad:
    $ mc_told_marcus_job_trouble = True
    $ marcus_job_trouble_career  = mf_career()[1]
    $ marcus_job_trouble_day     = day
    $ marcus_job_trouble_text_sent = False
    $ mf_sync_known()
    $ queue_phone_message("marcus", "That place sucks. Come by the bar, I'll overpour.", day, "marcus_msg_workgo_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_workgo_long:
    $ mf_sync_known()
    $ queue_phone_message("marcus", "Eat something that isn't from a machine.", day, "marcus_msg_workgo_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_sleep_will:
    $ queue_phone_message("marcus", "Good.", day, "marcus_msg_sleep_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_sleep_wont:
    $ queue_phone_message("marcus", "At least you're honest about it.", day, "marcus_msg_sleep_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_sleep_rude:
    $ queue_phone_message("marcus", "Respectfully.", day, "marcus_msg_sleep_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_court_yes:
    $ marcus_court_offer_last_day = day
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "marcus", "invitation_id": "marcus_park_invite", "target_location": "location_park", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("marcus", "Morning then. I'm there anyway.", day, "marcus_msg_court_r1")
    else:
        $ queue_phone_message("marcus", "You've already got something on. Next time.", day, "marcus_msg_court_r1b")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_court_maybe:
    $ marcus_court_offer_last_day = day
    $ queue_phone_message("marcus", "Maybe. The word of champions.", day, "marcus_msg_court_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_court_no:
    $ marcus_court_offer_last_day = day
    $ queue_phone_message("marcus", "Fine. I'll play badly on my own.", day, "marcus_msg_court_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_squatrack_angry:
    $ queue_phone_message("marcus", "Thank you. That's all I needed.", day, "marcus_msg_squatrack_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_squatrack_forty:
    $ queue_phone_message("marcus", "Forty. I timed the last twenty out of spite.", day, "marcus_msg_squatrack_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_squatrack_why:
    $ queue_phone_message("marcus", "Because I am a serious person with a rich inner life.", day, "marcus_msg_squatrack_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_notchili_what:
    $ marcus_ran_out_of_chili = True
    $ queue_phone_message("marcus", "We're not naming it. It didn't earn a name.", day, "marcus_msg_notchili_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_notchili_good:
    $ marcus_ran_out_of_chili = True
    $ queue_phone_message("marcus", "Never again.", day, "marcus_msg_notchili_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_notchili_brave:
    $ marcus_ran_out_of_chili = True
    $ queue_phone_message("marcus", "Brave is one word. The notepad stays shut next time.", day, "marcus_msg_notchili_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_zoemusic_agree:
    $ queue_phone_message("marcus", "You two deserve each other.", day, "marcus_msg_zoemusic_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_zoemusic_defend:
    $ queue_phone_message("marcus", "I can't. That's the worst part.", day, "marcus_msg_zoemusic_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_zoemusic_what:
    $ queue_phone_message("marcus", "Doesn't matter. She'd have found something.", day, "marcus_msg_zoemusic_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_noreason_why:
    $ queue_phone_message("marcus", "No reason. You need a reason now?", day, "marcus_msg_noreason_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_noreason_hi:
    $ queue_phone_message("marcus", "Hi.", day, "marcus_msg_noreason_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_noreason_ok:
    $ queue_phone_message("marcus", "Okay.", day, "marcus_msg_noreason_r3")
    $ _clear_initiative_pending("marcus")
    return

# ── Authored pack replies ───────────────────────────────────────────────────

label npc_ini_marcus_hungry_sentence:
    $ queue_phone_message("marcus", "It is when you're hungry.", day, "marcus_msg_hungry_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_good_yeah:
    $ queue_phone_message("marcus", "Cool.", day, "marcus_msg_minute_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_good_not:
    $ queue_phone_message("marcus", "Okay.", day, "marcus_msg_minute_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_tonight_sure:
    # Reuses his existing standing offer verbatim — he is behind the bar
    # 16-24 every weekday, so "tonight" means the bar.
    $ queue_phone_message("marcus", "Come by. I'm behind the bar till late anyway.", day, "marcus_msg_tonight_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_tonight_not:
    # Declining costs nothing. No relationship write at all.
    $ queue_phone_message("marcus", "All good.\nI'll pretend I had a backup plan.", day, "marcus_msg_tonight_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_fiveam_flex:
    $ queue_phone_message("marcus", "Wasn't meant to be.", day, "marcus_msg_fiveam_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_fiveam_brave:
    $ queue_phone_message("marcus", "Don't tell anyone.", day, "marcus_msg_fiveam_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_free_yeah:
    $ queue_phone_message("marcus", "Come downstairs.", day, "marcus_msg_free_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_free_why:
    $ queue_phone_message("marcus", "You've asked two questions already.", day, "marcus_msg_free_r2")
    $ _clear_initiative_pending("marcus")
    return


# ── Scripted callback replies ───────────────────────────────────────────────

label npc_ini_marcus_interview_cb_got:
    $ mc_told_marcus_interview = False
    $ mf_sync_known()
    $ apply_relationship_change("marcus", source_id="marcus_interview_text",
                                source_category="meaningful_talk",
                                affection=1, respect=1)
    $ queue_phone_message("marcus", "Course you did.", day, "marcus_interview_cb_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_interview_cb_didnt:
    $ mc_told_marcus_interview = False
    $ apply_relationship_change("marcus", source_id="marcus_interview_text",
                                source_category="meaningful_talk", trust=2)
    $ queue_phone_message("marcus", "Their loss. Genuinely, not as a thing people say.", day, "marcus_interview_cb_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_interview_cb_waiting:
    # Stays open: he'll ask again once the state moves.
    $ marcus_interview_told_day = day
    $ marcus_interview_text_sent = False
    $ queue_phone_message("marcus", "Then stop checking your phone. I can feel you doing it.", day, "marcus_interview_cb_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_jobtrouble_cb_still:
    $ marcus_job_trouble_day = day
    $ marcus_job_trouble_text_sent = False
    $ apply_relationship_change("marcus", source_id="marcus_jobtrouble_text",
                                source_category="meaningful_talk", trust=2)
    $ queue_phone_message("marcus", "Come by. I'm behind the bar till late anyway.", day, "marcus_jobtrouble_cb_r1")
    return

label npc_ini_marcus_jobtrouble_cb_left:
    $ mc_told_marcus_job_trouble = False
    $ marcus_job_trouble_career  = None
    $ mf_sync_known()
    $ queue_phone_message("marcus", "Good. That place sucked.", day, "marcus_jobtrouble_cb_r2")
    return

label npc_ini_marcus_jobtrouble_cb_better:
    $ mc_told_marcus_job_trouble = False
    $ mc_told_marcus_career_good = True
    $ queue_phone_message("marcus", "Things do that sometimes. Nobody reports it.", day, "marcus_jobtrouble_cb_r3")
    return

label npc_ini_marcus_promo_cb_yes:
    $ marcus_heard_promotion = True
    $ mf_sync_known()
    $ apply_relationship_change("marcus", source_id="marcus_promotion_text",
                                source_category="meaningful_talk",
                                affection=1, respect=1)
    $ queue_phone_message("marcus", "Sunday. Bring nothing. That's the deal.", day, "marcus_promo_cb_r1")
    return

label npc_ini_marcus_promo_cb_how:
    $ marcus_heard_promotion = True
    $ mf_sync_known()
    $ apply_relationship_change("marcus", source_id="marcus_promotion_text",
                                source_category="meaningful_talk",
                                affection=1, respect=1)
    $ queue_phone_message("marcus", "I run a bar. People talk over drinks. It's the whole business model.", day, "marcus_promo_cb_r2")
    return

label npc_ini_marcus_promo_cb_modest:
    $ marcus_heard_promotion = True
    $ mf_sync_known()
    $ apply_relationship_change("marcus", source_id="marcus_promotion_text",
                                source_category="meaningful_talk", respect=1)
    $ queue_phone_message("marcus", "It's a bit of a deal. Let it be a bit of a deal.", day, "marcus_promo_cb_r3")
    return
