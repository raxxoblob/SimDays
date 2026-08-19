# ═══════════════════════════════════════════════════════════════════════════
# MARCUS — EVERYDAY FRIENDSHIP BEATS
# ═══════════════════════════════════════════════════════════════════════════
# Fourteen small scenes whose only job is that Marcus feels like a person who
# lives here and has noticed you. Not an arc. No CG, no new background, no new
# system, no new sprite — every beat is dialogue-only and never issues `scene`
# or `show`, exactly like the shipping talk_followup_* labels
# (interact.rpy:2355), so the interaction UI keeps owning the sprite and no
# beat can ever contradict where Marcus actually is.
#
# SCHEDULE REALITY (npc_schedules.rpy:60-71 — do not "fix" without re-reading):
#   park      Mon-Fri 07-11   running
#   cafe      Tue    15-17    eating out
#   transit   Mon-Fri 14-16   commuting (not interactable)
#   bar       Mon-Fri 16-24   working his shift
#   bar       Sat-Sun 15-27   working his shift
# He is NEVER at the gym (location_beats_tier_a.rpy:34). The one gym line in
# this file is him RELAYING something he was told, which is why it is a text
# and not a scene.
#
# ANTI-SPAM
#   marcus_beat_last_day  — at most one friendship beat per in-game day.
#   Per beat: the existing tier_a_beat_last_day dict + _beat_cooldown_ok().
#   Deliberately NOT wired to last_tier_a_beat_day: these are conversation
#   beats the player opted into by pressing Talk, and should not eat the
#   city-wide contextual-beat budget that ambush scenes draw from.
#
# RELATIONSHIP AXES — every write goes through apply_relationship_change.
#   ordinary time (food run, five minutes, court, come with me)  fam +1-2
#   he checks on MC (first week, you look dead, need anything)   trust+1 fam+1
#   he reacts to an MC milestone (good shift, promotion)         aff+1 resp+1
#   shared joke / running motif (random story)                   aff+1 fam+1
#   MC supports HIS day (had a day)                              trust+1 fam+1
#   he remembers something MC said (that job again, interview)   trust+2
#   No attraction anywhere: interact.rpy:1381 sets Marcus
#   romance_scope "friendship_only".
# ═══════════════════════════════════════════════════════════════════════════

default marcus_test_label = "marcus_beat_five_minutes"

# ── Story-canon consolidation ───────────────────────────────────────────────
# arc_marcus_food_2 now only HINTS ("family recipe", "inherited"). The mother,
# the physical notepad and the two hundred times are marcus_beat_notepad's.
default mc_knows_marcus_chili_family_recipe = False
default marcus_notepad_done                 = False
default marcus_food2_day                    = -1


init 5 python:

    # ── The pool ─────────────────────────────────────────────────────────────
    # (beat_id, label, cooldown_days, eligibility). Reactive beats come first;
    # the ordinary-time block below them rotates.
    def _mf_stage():
        try:
            return npc_relationship_stage("marcus")
        except Exception:
            return "stranger"

    def _mf_close():
        return _mf_stage() in ("close", "trusted")

    def _mf_friendly():
        return _mf_stage() in ("friendly", "friend", "close", "trusted")

    MARCUS_BEATS = [
        # ── Reactive (something about MC's life changed) ─────────────────────
        # One-shot authored openers first — they are the only beats that can
        # never come back, so they must not lose a roll to a rotating one.
        ("marcus_fr_still_alive", "marcus_beat_still_alive", 99,
         # Day 2-5, after the first-week check-in landed (Talk OR text), and
         # only in the building he actually lives in.
         lambda: (not store.marcus_still_alive_done
                  and store.marcus_mc_checkin_done
                  and 2 <= store.day <= 5)),
        ("marcus_fr_5am",         "marcus_beat_5am",         99,
         # His real schedule: park, Mon-Fri, 07-11 (npc_schedules.rpy:60).
         # "Early" is the front half of that window.
         lambda: (not store.marcus_five_am_known
                  and store.current_loc == "location_park"
                  and store.hour < 9.0)),
        ("marcus_fr_job_good",    "marcus_beat_job_still_good", 99,
         # 3-7 days after MC said the job was going well, same job, and the
         # thread has not since turned sour. Outside that window it retires
         # rather than asking about a stale claim.
         lambda: (store.mc_told_marcus_career_good
                  and store.marcus_career_good_day >= 0
                  and 3 <= store.day - store.marcus_career_good_day <= 7
                  and not store.mc_told_marcus_job_trouble
                  and mf_career()[1] == store.marcus_known_career
                  and mf_career()[1] is not None)),
        ("marcus_fr_good_shift",  "marcus_beat_good_shift",  6,
         lambda: mf_recent_career_win()),
        # The payoff arc_marcus_food_2 deliberately does not spend. One-shot,
        # and it must sit at least 3 days behind the hint that set it up.
        ("marcus_fr_notepad",     "marcus_beat_notepad",     99,
         lambda: (store.mc_knows_marcus_chili_family_recipe
                  and not store.marcus_notepad_done
                  and _mf_stage() in ("friend", "close", "trusted")
                  and npc_trust("marcus") >= 30
                  and store.marcus_food2_day >= 0
                  and store.day - store.marcus_food2_day >= 3
                  and not store.story_scene_active)),
        ("marcus_fr_you_look_dead", "marcus_beat_you_look_dead", 5,
         # The shipping wevent_marcus_low_energy_comment (world_events.rpy:1158)
         # covers the first three times MC looks wrecked. This picks up after it
         # retires rather than duplicating it.
         lambda: (store.need_energy < 30
                  and store.wed_marcus_low_energy_count >= 3)),
        ("marcus_fr_bad_shift",   "marcus_beat_bad_shift",   6,
         lambda: mf_rough_patch() and store.mc_told_marcus_job_trouble),
        ("marcus_fr_that_job",    "marcus_beat_that_job_again", 6,
         # One ask per complaint: marcus_job_callback_done closes it, and only
         # a NEW complaint re-opens it.
         lambda: (store.mc_told_marcus_job_trouble
                  and not store.marcus_job_callback_done
                  and not mf_job_change_since_complaint()
                  and store.day - store.marcus_job_trouble_day >= 3)),
        ("marcus_fr_how_work",    "marcus_beat_how_work",    4,
         lambda: store.day - store.marcus_work_check_last >= 4),
        # ── Ordinary time ───────────────────────────────────────────────────
        ("marcus_fr_had_a_day",   "marcus_beat_had_a_day",   5,  lambda: True),
        ("marcus_fr_random_story","marcus_beat_random_story",5,  lambda: True),
        ("marcus_fr_five_minutes","marcus_beat_five_minutes",4,  lambda: True),
        ("marcus_fr_food_run",    "marcus_beat_food_run",    6,
         # Only where a food run is physically plausible: the café on his Tuesday
         # stop, or the bar he is standing behind.
         lambda: store.current_loc in ("location_cafe", "location_bar")),
        ("marcus_fr_court",       "marcus_beat_court_later", 7,
         lambda: (store.npc_invitation_pending is None
                  and store.day - store.marcus_court_offer_last_day >= 6
                  and _mf_friendly())),
        ("marcus_fr_come_with",   "marcus_beat_come_with_me",6,  lambda: _mf_friendly()),
        ("marcus_fr_need_any",    "marcus_beat_need_anything",7, lambda: _mf_close()),
        # Friend stage, not Acquaintance: he needs a relationship before he is
        # allowed to turn up with no reason at all.
        ("marcus_fr_nothing",     "marcus_beat_nothing_really",8,
         lambda: _mf_stage() in ("friend", "close", "trusted")),
    ]

    # Reactive beats jump the rotation. Named explicitly rather than sliced, so
    # adding a beat to the list can never silently change which ones are urgent.
    MARCUS_REACTIVE_IDS = ("marcus_fr_still_alive", "marcus_fr_5am",
                           "marcus_fr_job_good", "marcus_fr_notepad",
                           "marcus_fr_good_shift",
                           "marcus_fr_you_look_dead", "marcus_fr_bad_shift",
                           "marcus_fr_that_job", "marcus_fr_how_work")

    def mf_pick_beat():
        """One beat per day, cooldown-respecting, reactive beats first.
        Returns a label or None. Reads state only — mf_beat_fired() is the
        write point, called by the beat itself."""
        if not store.marcus_met:
            return None
        if store.marcus_beat_last_day == store.day:
            return None
        eligible = []
        for bid, lbl, cd, cond in MARCUS_BEATS:
            if not _beat_cooldown_ok(bid, cd):
                continue
            try:
                if not cond():
                    continue
            except Exception:
                continue
            eligible.append((bid, lbl))
        if not eligible:
            return None
        for bid, lbl in eligible:
            if bid in MARCUS_REACTIVE_IDS:
                return lbl
        # Otherwise rotate the ordinary-time block: least recently seen first.
        eligible.sort(key=lambda e: store.tier_a_beat_last_day.get(e[0], -999))
        return eligible[0][1]

    def mf_beat_fired(beat_id):
        """Spends the daily Marcus-beat budget and stamps the cooldown."""
        store.marcus_beat_last_day = store.day
        d = dict(store.tier_a_beat_last_day)
        d[beat_id] = store.day
        store.tier_a_beat_last_day = d

    # Rotating small stories. Every topic here has canonical support:
    # chili (arcs.rpy:202 + script.rpy:45), the bar (he runs it), the lock
    # (script.rpy:23), basketball (arcs.rpy:184), Nora (world_events.rpy:1593).
    MARCUS_STORY_VARIANTS = ["mstory_tonic", "mstory_lock", "mstory_nora",
                             "mstory_chili", "mstory_regular"]
    MARCUS_DAY_TOPICS = ["delivery", "cancelled", "game", "chili"]


# ═══════════════════════════════════════════════════════════════════════════
# A. STILL ALIVE
# ═══════════════════════════════════════════════════════════════════════════
# Day 2-5 incidental. Costs no time on purpose — it is the length of a landing
# conversation, not a scene. One-shot.
#
# "You said you wake up at five." is NOT a continuity error: arcs.rpy:176 has
# him up at SIX and unable to sleep past FIVE. He is awake at five and does not
# want company until six. Both lines are true at once.
label marcus_beat_still_alive:
    $ mf_beat_fired("marcus_fr_still_alive")
    $ marcus_still_alive_done = True
    $ _do_talk_accounting("marcus")

    m "Still alive."
    mc "Barely."
    m "Good."
    mc "That's your standard?"
    m "First week in a new place? Absolutely."
    m "Apartment behaving?"
    menu:
        "\"Mostly.\"":
            mc "Mostly."
            m "That's what you want from a building."
            m "Low expectations. Long life."
        "\"The lock still hates me.\"":
            mc "The lock still hates me."
            m "Knew it."
            m "You've got to establish dominance early."
            mc "Over a lock?"
            m "Especially over a lock."
            # Feeds the mstory_lock variant of the random-story beat, which is
            # already written as a callback to exactly this.
            $ marcus_lock_joke_active = True
        "\"I'm starting to settle in.\"":
            mc "I'm starting to settle in."
            m "Yeah?"
            m "Good."
            m "Takes a minute before a new place stops feeling like somebody else's apartment."
    mc "How long did it take you?"
    m "Couple weeks."
    m "Then I started leaving laundry on chairs."
    m "That's when you know it's home."
    mc "That's the milestone?"
    m "One of them."
    m "Anyway."
    m "You need anything, knock."
    m "Unless it's before six."
    mc "You said you wake up at five."
    m "Yeah."
    m "Doesn't mean I want company."
    $ apply_relationship_change("marcus", source_id="marcus_still_alive",
                                source_category="casual_talk",
                                familiarity=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# B. HOW'S WORK
# ═══════════════════════════════════════════════════════════════════════════
label marcus_beat_how_work:
    $ mf_beat_fired("marcus_fr_how_work")
    $ marcus_work_check_last = day
    $ _do_talk_accounting("marcus")
    $ _mfs, _mfc, _mfr = mf_career()

    if mf_promotion_due():
        m "Heard you moved up."
        mc "Word travels."
        m "I pour drinks for a living. Word is the product."
        "He looks at you for a second longer than he normally bothers to."
        m "Look at you."
        $ marcus_heard_promotion = True
        $ mf_sync_known()
        $ add_relationship_memory("marcus", "marcus_knows_promotion_%d" % day,
                                  "Marcus heard about my promotion", category="career")
        $ apply_relationship_change("marcus", source_id="marcus_promotion_reaction",
                                    source_category="meaningful_talk",
                                    affection=1, respect=1)

    elif _mfs == "none":
        m "You figure out the work thing yet?"
        mc "Not really."
        m "Fair."
        m "You've been here, what, five minutes?"
        mc "Feels longer."
        m "That's rent."
        menu:
            "\"I'm looking.\"":
                mc "I'm looking."
                m "You'll find something."
                mc "That confidence based on anything?"
                m "No."
                m "But I said it like it was."
            "\"I've been doing odd jobs.\"":
                mc "I've been doing odd jobs."
                m "Honestly?"
                m "Could be worse."
                m "Nobody schedules a meeting about synergy when you're carrying boxes."
            "\"I'm not rushing it.\"":
                mc "I'm not rushing it."
                m "Also fair."
                m "Just don't become one with the couch."
        mc "How would I know?"
        m "I'll tell you."
        m "That's what friends are for."
        $ apply_relationship_change("marcus", source_id="marcus_how_work_none",
                                    source_category="casual_talk",
                                    trust=1, familiarity=1)

    elif _mfs == "new":
        $ mf_sync_known()
        m "So."
        mc "So?"
        m "New job."
        m "You survived."
        mc "So far."
        m "That's usually how they get you."
        menu:
            "\"It's actually going well.\"":
                mc "It's actually going well."
                $ mc_told_marcus_career_good = True
                $ marcus_career_good_day     = day
                m "Look at that."
                m "Competent adult."
                mc "Don't sound so surprised."
                m "I'm proud."
                m "And a little surprised."
            "\"I have no idea what I'm doing.\"":
                mc "I have no idea what I'm doing."
                m "Perfect."
                mc "Perfect?"
                m "Means you're new."
                m "If you still have no idea in six months, then we worry."
            "\"I already hate it.\"":
                mc "I already hate it."
                $ mc_told_marcus_job_trouble = True
                $ mc_told_marcus_career_good = False
                $ marcus_job_trouble_career  = _mfc
                $ marcus_job_trouble_day     = day
                $ marcus_job_trouble_text_sent = False
                $ marcus_job_callback_done   = False
                $ add_relationship_memory("marcus", "marcus_knows_job_trouble",
                                          "I told Marcus I don't like the job", category="career")
                m "Oh, strong start."
                mc "Yeah."
                m "Give it a minute."
                m "If you still hate it after the money hits your account, then it's real."
        $ apply_relationship_change("marcus", source_id="marcus_how_work_new",
                                    source_category="casual_talk",
                                    trust=1, familiarity=1)

    else:
        $ mf_sync_known()
        m "Work still treating you like a human being?"
        mc "Define human."
        m "Bad sign."
        menu:
            "\"It's fine.\"":
                mc "It's fine."
                m "Most convincing review I've ever heard."
            "\"Busy.\"":
                mc "Busy."
                m "You always say that like it's temporary."
            "\"Honestly? Pretty good.\"":
                mc "Honestly? Pretty good."
                $ mc_told_marcus_career_good = True
                $ marcus_career_good_day     = day
                m "Good."
                m "You should keep one of those."
        mc "One of what?"
        m "Jobs you don't hate."
        m "Apparently they're rare."
        $ apply_relationship_change("marcus", source_id="marcus_how_work_est",
                                    source_category="casual_talk",
                                    trust=1, familiarity=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# B2. JOB STILL GOOD  (callback to "It's actually going well", 3-7 days on)
# ═══════════════════════════════════════════════════════════════════════════
# One-shot. The eligibility check in MARCUS_BEATS already proved the career is
# unchanged and the thread has not turned sour, so the positive continuation
# is the only reachable one — there is no version of this scene where he asks
# and the answer contradicts what the state says.
label marcus_beat_job_still_good:
    $ mf_beat_fired("marcus_fr_job_good")
    $ marcus_career_good_day = -1      # thread closed; never asked twice
    $ _do_talk_accounting("marcus")
    m "Job still good?"
    mc "You remembered?"
    m "I remember things."
    mc "Sometimes."
    m "Don't ruin this for me."
    mc "Yeah. Still good."
    m "Nice."
    m "That's almost suspicious."
    $ apply_relationship_change("marcus", source_id="marcus_job_still_good",
                                source_category="meaningful_talk",
                                trust=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# C. MARCUS HAD A DAY
# ═══════════════════════════════════════════════════════════════════════════
# He leads. MC's part is to be there. The topic is stored so the same-day
# contextual Talk option "Ask what happened" can pick it back up.
label marcus_beat_had_a_day:
    $ mf_beat_fired("marcus_fr_had_a_day")
    $ marcus_had_a_day_last  = day
    $ marcus_had_a_day_topic = _pick_ambient_variant("marcus_had_a_day", MARCUS_DAY_TOPICS)
    $ _do_talk_accounting("marcus")

    m "I've had the dumbest day."
    mc "Good dumb or bad dumb?"
    m "There's good dumb?"
    mc "You're asking me?"
    m "Fair."

    mc "What happened?"
    m "Nothing important."
    mc "You opened with 'I've had the dumbest day.'"
    m "Yeah."
    mc "That's generally followed by the day."
    m "I wanted sympathy."
    mc "You want the premium package or basic?"
    m "What comes with premium?"
    mc "Follow-up questions."
    m "Basic."

    pause 0.5

    m "Had three things go wrong before lunch."
    mc "What things?"
    m "Premium behavior."
    mc "Sorry."

    # ONE canonical-safe detail from his established life. The four variants are
    # unchanged: marcus_ctx_what_happened (marcus_onboarding.rpy:528) reads
    # marcus_had_a_day_topic back the same day, so the pool must stay intact.
    if marcus_had_a_day_topic == "game":
        m "Plans fell through."
        m "Then I lost a game I absolutely should've won."
        mc "There it is."
        m "What?"
        mc "That's why you're upset."
        m "I'm not upset."
        mc "You brought up the game second."
        m "Because I was building tension."
    elif marcus_had_a_day_topic == "delivery":
        m "Supplier sent twelve crates of tonic. I ordered two."
        mc "What happens to the other ten?"
        m "They're in the corridor behind the bar, judging me."
        mc "Can't you send them back?"
        m "I could. But then I'd have to speak to Dennis, and I've decided I'd rather have the crates."
    elif marcus_had_a_day_topic == "cancelled":
        m "Guy cancelled on me two hours out. One-word text."
        mc "What was the word?"
        m "\"Rain.\""
        mc "Was it raining?"
        m "It was not raining. I checked. I went outside and checked, like a lunatic."
    else:
        m "I tried to cook something that wasn't chili."
        mc "That's allowed?"
        m "That's what I thought. Turns out I know one recipe and everything else I make is a rumour of food."
        m "Never again."
        $ marcus_ran_out_of_chili = True

    mc "You want to do something?"
    m "Yeah."
    mc "What?"
    m "No idea."
    mc "You do this a lot."
    m "It's worked so far."
    $ apply_relationship_change("marcus", source_id="marcus_had_a_day",
                                source_category="meaningful_talk",
                                trust=1, familiarity=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# D. FOOD RUN
# ═══════════════════════════════════════════════════════════════════════════
label marcus_beat_food_run:
    $ mf_beat_fired("marcus_fr_food_run")
    $ _do_talk_accounting("marcus")
    $ _mf_food_go = False
    m "You eaten?"
    mc "That's a weird hello."
    m "It's not a hello."
    m "I'm getting food."
    m "You coming?"
    menu:
        "\"Sure.\"":
            mc "Sure."
            m "Good."
            mc "What are we getting?"
            m "Hadn't got that far."
            mc "You invited me before deciding where?"
            m "I needed commitment first."
            mc "That's backwards."
            m "And yet you're coming."
            $ _mf_food_go = True
        "\"Depends where.\"":
            mc "Depends where."
            m "Wrong attitude."
            mc "That's a reasonable question."
            m "No, now I know you're going to judge the choice."
            mc "I was always going to judge the choice."
            m "Fair."
            $ _mf_food_go = True
        "\"Not tonight.\"":
            mc "Not tonight."
            m "All right."
            m "More food for me."
            mc "You say that like you're winning."
            m "I am."
            # Declining costs nothing. It never has. He is, however, allowed to
            # push once in a whole playthrough (relationship_continuity.rpy).
            call rc_marcus_friction_push

    if _mf_food_go:
        mc "So how was your day?"
        m "Fine."
        mc "That's it?"
        m "You asked how it was."
        mc "Yeah."
        m "And it was fine."
        mc "You're terrible at this."
        m "Okay."
        # Deliberately unplaced. He runs a bar, but this is not a bar story and
        # must never be given a workplace.
        m "Some guy argued with me for ten minutes today about something he was completely wrong about."
        mc "What about?"
        m "Not important."
        mc "You brought it up."
        m "I wanted sympathy, not follow-up questions."
        mc "That's not how conversation works."
        m "Starting to regret inviting you."
        $ spend_time(20 / 60.0)
        $ store.need_hunger = min(100, store.need_hunger + 12)
        $ apply_relationship_change("marcus", source_id="marcus_food_run",
                                    source_category="shared_activity",
                                    familiarity=2, affection=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# D2. FIVE AM
# ═══════════════════════════════════════════════════════════════════════════
# Park, before 09:00, on his real running schedule. One-shot.
#
# CANON: arcs.rpy:176 (arc_marcus_sports_1) already carries "Six AM every day"
# and "can't sleep past five". This scene is the in-person, MC-led version of
# the same fact, so it CLOSES both other routes rather than sitting alongside
# them: it completes marcus_sports_1 and sets marcus_five_am_talk_done, and it
# is itself gated on neither having happened.
label marcus_beat_5am:
    $ mf_beat_fired("marcus_fr_5am")
    $ marcus_five_am_known    = True
    $ marcus_five_am_talk_done = True
    $ complete_arc("marcus_sports_1")
    $ mark_topic_today("marcus", "sports")
    $ _do_talk_accounting("marcus")

    mc "Why are you awake?"
    m "Good morning to you too."
    mc "It's barely morning."
    m "I've been up for an hour."
    mc "That's not a flex."
    m "Wasn't meant to be."
    mc "You do this every day?"
    m "Pretty much."
    mc "Why?"
    m "Can't sleep past five."
    mc "Seriously?"
    m "Yeah."
    mc "I thought this was some discipline thing."
    m "People think that."
    m "Makes me sound impressive, so I don't always correct them."
    mc "And now you've ruined it."
    m "Trusted you with the truth."
    mc "Brave."
    m "Don't tell anyone."
    if zoe_properly_introduced:
        m "Especially Zoe."
        mc "Why?"
        m "I don't need that becoming material."
    $ apply_relationship_change("marcus", source_id="marcus_five_am_scene",
                                source_category="meaningful_talk",
                                affection=1, familiarity=1, trust=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# E. FIVE MINUTES
# ═══════════════════════════════════════════════════════════════════════════
# Deliberately about nothing. Not every scene needs plot.
label marcus_beat_five_minutes:
    $ mf_beat_fired("marcus_fr_five_minutes")
    $ _do_talk_accounting("marcus")
    m "You've got that face."
    mc "What face?"
    m "The one where you're doing arithmetic about your own week."
    mc "I might be."
    m "Stop it for five minutes."
    "He doesn't offer anything to replace it with. He just stands there and complains about the state of the pavement outside, at unnecessary length, until the arithmetic stops."
    m "There. Better."
    mc "That was five minutes of you being annoyed about a kerb."
    m "And you're not doing sums anymore. You're welcome."
    $ apply_relationship_change("marcus", source_id="marcus_five_minutes",
                                source_category="casual_talk",
                                familiarity=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# F. COURT LATER
# ═══════════════════════════════════════════════════════════════════════════
# Hands off to the SHIPPING invitation route — npc_invitation_pending with
# invitation_id "marcus_park_invite", which wevent_marcus_park_invite_scene
# (world_events.rpy:2072) already resolves at the park. No new commitment code.
label marcus_beat_court_later:
    $ mf_beat_fired("marcus_fr_court")
    $ marcus_court_offer_last_day = day
    $ _do_talk_accounting("marcus")
    m "Court later?"
    menu:
        "\"Yeah, alright.\"":
            mc "Yeah, alright."
            m "Morning. I'm at the park anyway, so you're not putting me out."
            mc "Generous."
            m "I'm a generous man with a fixed routine."
            $ store.npc_invitation_pending = {"npc_id": "marcus", "invitation_id": "marcus_park_invite", "target_location": "location_park", "accepted_day": day, "expiry_day": day + 7}
            $ renpy.notify("Marcus is expecting you at the park.")
            $ apply_relationship_change("marcus", source_id="marcus_court_invite",
                                        source_category="shared_activity",
                                        familiarity=2, affection=1)
        "\"Not this week.\"":
            mc "Not this week."
            m "Fine. I'll shoot badly in private."
            # No penalty. Declining Marcus has never cost anything.
            call rc_marcus_friction_push
    return


# ═══════════════════════════════════════════════════════════════════════════
# G. YOU LOOK DEAD
# ═══════════════════════════════════════════════════════════════════════════
# He notices. He does not fix it — no energy restored, no stat, no command.
label marcus_beat_you_look_dead:
    $ mf_beat_fired("marcus_fr_you_look_dead")
    $ _do_talk_accounting("marcus")
    m "You look terrible."
    mc "Thanks."
    m "Respectfully."
    mc "That doesn't help."
    m "You sleep?"
    menu:
        "\"Not enough.\"":
            mc "Not enough."
            m "Yeah. I can see that."
            mc "Again. Helpful."
            m "Go home early."
            mc "You my mother now?"
            m "No."
            m "I'd be meaner."
        "\"Long shift.\"":
            mc "Long shift."
            m "Figured."
            m "You want food or sleep?"
            mc "Those are my options?"
            m "Those are the ones I'm qualified to recommend."
        "\"I'm fine.\"":
            mc "I'm fine."
            m "Sure."
            mc "You don't believe me?"
            m "I believe you believe you."
    m "Anyway."
    m "Don't die."
    mc "Great advice."
    m "Free, too."
    # No energy restored. He notices; he does not fix it.
    $ apply_relationship_change("marcus", source_id="marcus_you_look_dead",
                                source_category="meaningful_talk",
                                trust=1, familiarity=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# H. THAT JOB AGAIN
# ═══════════════════════════════════════════════════════════════════════════
# Only reachable while mc_told_marcus_job_trouble is set AND MC is still in
# the job they complained about (marcus_job_trouble_career).
label marcus_beat_that_job_again:
    $ mf_beat_fired("marcus_fr_that_job")
    $ _do_talk_accounting("marcus")
    # Answered once, whatever the answer. He does not become the guy who asks
    # about your job every single time he sees you.
    $ marcus_job_callback_done = True
    m "Still hate that place?"
    menu:
        "\"A little less.\"":
            mc "A little less."
            m "Growth."
            mc "That's generous."
            m "I'm supportive now."
            $ mc_told_marcus_job_trouble = False
        "\"More, actually.\"":
            mc "More, actually."
            m "Impressive."
            m "Usually there's a honeymoon period."
            # Still true, so marcus_beat_bad_shift stays reachable — but the
            # callback itself is spent.
            $ marcus_job_trouble_day = day
        "\"I think I'm getting used to it.\"":
            mc "I think I'm getting used to it."
            m "Careful."
            m "That's how they keep you."
            $ mc_told_marcus_job_trouble = False
    $ apply_relationship_change("marcus", source_id="marcus_that_job_again",
                                source_category="meaningful_talk",
                                trust=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# I. GOOD SHIFT
# ═══════════════════════════════════════════════════════════════════════════
# Gated on mf_recent_career_win(): a career journal entry or a "got_promoted"
# public fact inside three days. Both are things the city already carries.
label marcus_beat_good_shift:
    $ mf_beat_fired("marcus_fr_good_shift")
    $ _do_talk_accounting("marcus")
    m "Something went right for you this week."
    mc "How do you know that?"
    m "You walked in differently."
    menu:
        "Tell him.":
            # Show the two specific questions instead of narrating that he
            # asked them.
            mc "It went well. That's all."
            m "That's never all."
            mc "What do you want, a report?"
            m "One sentence."

            mc "I knew what I was doing today."
            m "Before somebody told you?"
            mc "Mostly."
            m "There it is."

            mc "There what is?"
            m "The face."
            mc "What face?"
            m "The one you walked in with."

            mc "You're very pleased with yourself."
            m "I'm observant."
            $ apply_relationship_change("marcus", source_id="marcus_good_shift",
                                        source_category="meaningful_talk",
                                        affection=1, respect=1)
        "\"It's not a big thing.\"":
            mc "It's not a big thing."
            m "Sure."
            m "Let it be a small thing you're allowed to be pleased about, then."
            $ apply_relationship_change("marcus", source_id="marcus_good_shift",
                                        source_category="meaningful_talk",
                                        affection=1, respect=1)
    $ mf_sync_known()
    return


# ═══════════════════════════════════════════════════════════════════════════
# J. BAD SHIFT
# ═══════════════════════════════════════════════════════════════════════════
# No motivational speech. He reacts the way a friend does.
label marcus_beat_bad_shift:
    $ mf_beat_fired("marcus_fr_bad_shift")
    $ _do_talk_accounting("marcus")
    m "That place sucks."
    mc "Yeah."
    m "Food?"
    menu:
        "\"Food.\"":
            mc "Food."
            "That's the whole conversation. He gets something out from under the bar, puts it in front of you, and talks about absolutely nothing for a while."
            $ spend_time(20 / 60.0)
            $ store.need_hunger = min(100, store.need_hunger + 10)
            $ apply_relationship_change("marcus", source_id="marcus_bad_shift",
                                        source_category="shared_activity",
                                        trust=1, familiarity=2)
        "\"I want to go home.\"":
            mc "I want to go home."
            m "Then go home."
            m "Fourteen's next door to twelve if it gets loud in there."
            $ apply_relationship_change("marcus", source_id="marcus_bad_shift",
                                        source_category="meaningful_talk",
                                        trust=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# K. RANDOM STORY
# ═══════════════════════════════════════════════════════════════════════════
# Pure texture. Rotated by _pick_ambient_variant (world_events.rpy:828), the
# same soft-variety picker the ambient system uses.
label marcus_beat_random_story:
    $ mf_beat_fired("marcus_fr_random_story")
    $ _do_talk_accounting("marcus")
    $ _mf_story = _pick_ambient_variant("marcus_friendship_story", MARCUS_STORY_VARIANTS)

    if _mf_story == "mstory_tonic":
        m "Someone tried to pay for a round entirely in coins tonight."
        mc "Did you let them?"
        m "I counted it. All of it. In front of them."
        mc "Why?"
        m "Because they watched me do it and that was the punishment."
    elif _mf_story == "mstory_lock":
        m "Number nine's lock went the same way yours did."
        mc "You told them to lift the handle."
        m "I told them to lift the handle. They said they were lifting the handle."
        mc "Were they?"
        m "They were not lifting the handle. Nobody lifts the handle. I've lived here two years and I'm the only person in this building who lifts the handle."
    elif _mf_story == "mstory_nora":
        m "Went for coffee. Got asked if I wanted notes of anything."
        mc "Did you?"
        m "I want coffee. I want it to taste like coffee did before it developed a personality."
        mc "Did you tell her that?"
        m "I didn't have to. She'd already started making it."
    elif _mf_story == "mstory_chili":
        m "Made chili on Sunday. Two hundredth time, roughly."
        mc "You still check the recipe?"
        m "Every time."
        mc "You must know it."
        m "I do know it. That's not the point of checking it."
        "He doesn't explain what the point is, and you don't ask, because it's fairly obvious."
    else:
        m "There's a guy who's been coming in every Thursday for a year and I still don't know his name."
        mc "Ask him."
        m "It's been a year. It'd be rude now."
        mc "So what do you call him?"
        m "Thursday."
        mc "To his face?"
        m "He answers to it. That's the worst part."

    $ apply_relationship_change("marcus", source_id="marcus_random_story",
                                source_category="casual_talk",
                                affection=1, familiarity=1)
    return


# ═══════════════════════════════════════════════════════════════════════════
# K2. THE NOTEPAD
# ═══════════════════════════════════════════════════════════════════════════
# The payoff arc_marcus_food_2 hands off rather than spends. Dialogue-only,
# like every other beat in this file, so the interaction UI owns the sprite.
# CANON it rests on: he cooks exactly one thing (arc_marcus_food_1), roughly
# two hundred times (mstory_chili), and he checks the recipe every time.
label marcus_beat_notepad:
    $ mf_beat_fired("marcus_fr_notepad")
    $ _do_talk_accounting("marcus")

    m "I changed the chili."

    mc "You said that like a confession."
    m "It sort of is."

    mc "What did you change?"
    m "Smoked paprika."
    mc "Scandalous."
    m "You joke."

    pause 0.5

    m "My mom wrote the recipe down when I moved out."
    mc "The family one?"
    m "Yeah."

    m "Actual paper."
    m "Bad handwriting."
    m "Oil stain in one corner."
    m "I've made the thing probably two hundred times."

    mc "You still use the recipe?"
    m "Every time."

    menu:
        "\"You don't need it anymore.\"":
            mc "You don't need it anymore."
            m "I know."
            mc "Then why check?"
            m "Because that's not the point."
            pause 0.5
            mc "Right."
            $ apply_relationship_change(
                "marcus",
                source_id="marcus_notepad",
                source_category="story_moment",
                trust=3,
                familiarity=1)

        "\"Does she know you still have it?\"":
            mc "Does she know you still have it?"
            m "Probably."
            mc "Probably?"
            m "She's my mother."
            m "She knows things I haven't told her."
            $ apply_relationship_change(
                "marcus",
                source_id="marcus_notepad",
                source_category="story_moment",
                trust=2,
                affection=1,
                familiarity=1)

        "[[Let it sit.]":
            "You don't make a joke out of it."
            m "..."
            m "Anyway."
            mc "Useful word."
            m "Extremely."
            $ apply_relationship_change(
                "marcus",
                source_id="marcus_notepad",
                source_category="story_moment",
                trust=3,
                familiarity=1)

    mc "So is smoked paprika staying?"
    m "Absolutely not."
    mc "Good."
    m "Respect the source material."

    $ store.marcus_notepad_done = True
    $ add_relationship_memory("marcus", "marcus_notepad",
                              "The handwritten chili recipe")
    return


# ═══════════════════════════════════════════════════════════════════════════
# L. NEED ANYTHING
# ═══════════════════════════════════════════════════════════════════════════
# Close/Trusted only. Direct, practical, and short. He does not become a
# therapist — the offer is a distraction or a conversation, and either is fine.
label marcus_beat_need_anything:
    $ mf_beat_fired("marcus_fr_need_any")
    $ _do_talk_accounting("marcus")
    m "You good?"
    menu:
        "\"Yeah.\"":
            mc "Yeah."
            m "Cool."
            "And that's it. He doesn't test it, doesn't circle back, doesn't do the thing where someone asks twice."
            $ apply_relationship_change("marcus", source_id="marcus_need_anything",
                                        source_category="meaningful_talk",
                                        trust=1, familiarity=1)
        "\"Not really.\"":
            mc "Not really."
            m "Okay."
            m "Want to talk about it, or do you want me to distract you?"
            menu:
                "\"Talk.\"":
                    mc "Talk."
                    m "Go."
                    "He listens the whole way through without once starting a sentence with \"well, have you tried\"."
                    m "That's rough."
                    mc "That's it?"
                    m "That's it. It's rough. I'm not going to pretend I've got a fix for it."
                    $ apply_relationship_change("marcus", source_id="marcus_need_anything_talk",
                                                source_category="meaningful_talk",
                                                trust=2, familiarity=1)
                "\"Distract me.\"":
                    mc "Distract me."
                    m "Easy."
                    "Forty minutes of a story about a supplier, a stolen crate and a man called Dennis, told with a level of detail that no story about a supplier has ever earned."
                    m "Better?"
                    mc "Marginally."
                    m "I'll take marginally."
                    $ spend_time(0.5)
                    $ apply_relationship_change("marcus", source_id="marcus_need_anything_distract",
                                                source_category="shared_activity",
                                                trust=1, familiarity=2)
    return


# ═══════════════════════════════════════════════════════════════════════════
# M. COME WITH ME
# ═══════════════════════════════════════════════════════════════════════════
label marcus_beat_come_with_me:
    $ mf_beat_fired("marcus_fr_come_with")
    $ _do_talk_accounting("marcus")
    m "I've got to drop something off two streets over. Come with me."
    mc "Why?"
    m "Because it's a ten-minute walk and I'd rather not do it thinking."
    menu:
        "Go.":
            mc "Fine."
            "It is, in fact, a ten-minute walk. He hands a box to a man who doesn't look up, and on the way back he points out three things about the street you'd walked past for weeks without registering."
            m "That's it. That was the whole thing."
            mc "I know."
            m "Just checking you weren't waiting for a twist."
            $ spend_time(20 / 60.0)
            $ apply_relationship_change("marcus", source_id="marcus_come_with_me",
                                        source_category="shared_activity",
                                        familiarity=2)
        "\"I'll pass.\"":
            mc "I'll pass."
            m "Understood. I'll think, then."
            call rc_marcus_friction_push
    return


# ═══════════════════════════════════════════════════════════════════════════
# N. NOTHING, REALLY
# ═══════════════════════════════════════════════════════════════════════════
# The proof that the relationship is established: he no longer needs a reason.
label marcus_beat_nothing_really:
    $ mf_beat_fired("marcus_fr_nothing")
    $ _do_talk_accounting("marcus")
    mc "So what are we doing?"
    m "Walking."
    mc "Where?"
    m "No idea."
    mc "You dragged me downstairs to walk nowhere?"
    m "I didn't drag you."
    mc "You texted me 'come downstairs.'"
    m "And you came."
    mc "Because I assumed there was a reason."
    m "There was."
    mc "Which was?"
    m "I wanted to get out."
    mc "That's it?"
    m "Yeah."
    "A beat."
    m "What?"
    mc "Nothing."
    m "You need an agenda now?"
    mc "Apparently not."
    m "Good."
    m "You're learning."
    mc "So."
    mc "What's new?"
    mc "You brought me out here. You go first."
    m "Nothing."
    mc "Seriously?"
    m "Pretty much."
    mc "This is a terrible conversation."
    m "And yet you're still here."

    $ spend_time(20 / 60.0)
    $ apply_relationship_change("marcus", source_id="marcus_nothing_really",
                                source_category="meaningful_talk",
                                affection=1, familiarity=3, trust=1)

    # If a work thread of his is genuinely still open, he reopens it here
    # rather than a new one being written for the walk.
    # ponytail: reuse costs a second _do_talk_accounting (another 30 min).
    # Ceiling: a walk-plus-real-conversation reads as an hour, which is fine;
    # upgrade path is a no_accounting argument on the two callback labels.
    $ _mf_open = None
    if (mc_told_marcus_career_good and marcus_career_good_day >= 0
            and not mc_told_marcus_job_trouble
            and mf_career()[1] is not None
            and mf_career()[1] == marcus_known_career):
        $ _mf_open = "marcus_beat_job_still_good"
    elif (mc_told_marcus_job_trouble and not marcus_job_callback_done
            and not mf_job_change_since_complaint()):
        $ _mf_open = "marcus_beat_that_job_again"

    if _mf_open is not None:
        m "How's the new work thing, actually?"
        mc "You already asked me that."
        m "Yeah."
        m "Things change."
        call expression _mf_open
    else:
        m "You settling in okay?"
        mc "Yeah."
        m "Good."
        mc "That's all you wanted to know?"
        m "For now."
        mc "Deep."
        m "I'm layered."
    return


# ═══════════════════════════════════════════════════════════════════════════
# SCENE TESTER LAUNCHER
# ═══════════════════════════════════════════════════════════════════════════
# Beat labels `return` (they are `call`ed from npc_interact), so the tester
# cannot Jump() straight at them. This wrapper gives them a call frame and a
# real exit, and shows a sprite the interaction UI would normally own.
label marcus_friendship_test:
    $ set_hud("hidden")
    $ story_scene_active = True
    show screen hud
    hide screen people_here_dock
    show expression mf_sprite("normal") as focus_marcus at sprite_r
    call expression marcus_test_label
    hide focus_marcus
    $ story_scene_active = False
    $ set_hud("full")
    jump map
