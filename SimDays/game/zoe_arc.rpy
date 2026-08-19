# ═══════════════════════════════════════════════════════════════════════════
# ZOE — CHARACTER DEPTH & RELATIONSHIP RHYTHM PASS
# ═══════════════════════════════════════════════════════════════════════════
# This LAYERS ON everything Zoe already has. Nothing here re-implements a
# system that exists:
#   * topic arcs           arcs.rpy        (arc_zoe_art_1..4, arc_zoe_music_1..2)
#   * Tier A location beats location_beats_tier_a.rpy (zoe_outdoor, zoe_walk)
#   * authored scenes       gameplay_expansion_scenes.rpy (rain shelter,
#                           spontaneous, romance reopen), home_scenes.rpy (guitar)
#   * exhibition storyline  arcs.rpy zoe_exhibition_* + locations.rpy gallery
#   * phone initiative      phone_actionable.rpy (_INITIATIVE_MSGS et al)
#   * relationship axes     npc_relationships.rpy (apply_relationship_change)
#
# What this file adds:
#   1. Knowledge facts about Zoe as a specific person, back-filled from the
#      arc flags an existing save already has (_zoe_sync_knowledge).
#   2. Twelve authored beats dispatched by ONE selector (zoe_arc_beat_for)
#      hooked into three locations, sharing the existing Tier A daily budget.
#   3. Fourteen initiative message variants registered into the SHIPPING
#      picker — no second cadence engine.
#   4. A priority Talk menu that sits in front of the generic 9 topics.
#
# ZERO new art dependencies: existing backgrounds, existing Zoe sprites.
#
# SCHEDULE REALITY (npc_schedules.rpy — do not widen these windows blindly):
#   zoe  hub Mon-Fri 09-13, café Wed 13-18, park Thu-Fri 14-18,
#        sandbeach Sat-Sun 12-18, bar Sat 19-24
# ═══════════════════════════════════════════════════════════════════════════

# ── Knowledge facts ─────────────────────────────────────────────────────────
default knows_zoe_art_interest        = False
default knows_zoe_paid_creative_work  = False
default knows_zoe_gallery_goal        = False
default knows_zoe_funding_problem     = False
default knows_zoe_bass_history        = False
default knows_zoe_creative_values     = False

# ── Story-canon consolidation: DISCOVERY facts ──────────────────────────────
# Generic Talk may discover a subject; it may not spend the authored payoff.
# These three are the "subject discovered" half of that split.
default zoe_funding_application_known = False   # arc_zoe_art_3 (she applied)
default zoe_bass_hint_known           = False   # arc_zoe_music_2 ("used to")
# (marcus side lives in marcus_friendship.rpy)

# ── Player-choice memory ────────────────────────────────────────────────────
# One of: None, "warmth", "structure", "asked_her", "no_idea"
default zoe_second_opinion_choice     = None
default zoe_deadline_submitted        = False
default zoe_deadline_result           = "pending"   # "pending"/"success"/"rejection"

# ── Beat bookkeeping ────────────────────────────────────────────────────────
default zoe_print_done                = False
default zoe_beige_done                = False
default zoe_second_opinion_pending    = False
default zoe_second_opinion_done       = False
default zoe_second_opinion_day        = -1
default zoe_second_opinion_callback_done = False
default zoe_bass_window_done          = False
default zoe_bass_followup_done        = False
default zoe_coffee_pending            = False
default zoe_coffee_done               = False
default zoe_not_ready_done            = False
default zoe_noticed_callback_done     = False
default zoe_deadline_scene_done       = False
default zoe_deadline_day              = -1
default zoe_deadline_followup_done    = False
default zoe_after_deadline_done       = False
default zoe_just_stay_done            = False
default zoe_thread_gain_day           = -1
# Greeting callbacks to existing scenes (zoe_greet in interact.rpy).
default zoe_rain_greet_said           = False
default zoe_guitar_bass_greet_said    = False
default _zarc_dest                    = "location_park"


init 2 python:

    # ── Knowledge back-fill ──────────────────────────────────────────────────
    # An existing save may already have had these conversations through the
    # topic arcs. Deriving the facts instead of demanding the new scenes first
    # is what stops a callback reading as amnesia.
    def _zoe_sync_knowledge():
        done = store.topic_arc_done
        if done.get("zoe_art_1"):
            store.knows_zoe_art_interest = True
        if done.get("zoe_art_2") or store.zoe_exhibition_invited:
            store.knows_zoe_gallery_goal = True
            store.knows_zoe_art_interest = True
        # NOT derived from zoe_art_3 / zoe_music_2 any more: since the canon
        # consolidation those arcs only DISCOVER their subject, so deriving the
        # strong fact from them would spend the authored payoff before it runs
        # (and would send zoe_bass_window_scene straight to its callback
        # branch). Old saves that heard the old versions are migrated once, in
        # _sd_backfill (story_direct_pass.rpy).
        if store.zoe_grant_discussed:
            store.knows_zoe_funding_problem = True

    def _zoe_fam():
        return npc_rel("zoe", "familiarity")

    def _zoe_rel(source_id, affection=0, trust=0, respect=0, familiarity=0,
                 attraction=0):
        """Affection/Trust go through the legacy helpers so the interaction
        toast + threshold notify still fire; the Phase 66 axes go through the
        single mutation point. Both paths are already wired to each other."""
        if affection:
            _apply_aff("zoe", affection)
        if trust:
            _apply_trust("zoe", trust)
        if respect or familiarity or attraction:
            apply_relationship_change("zoe", source_id=source_id,
                                      source_category="story_moment",
                                      respect=respect, familiarity=familiarity,
                                      attraction=attraction)

    def _zoe_talk_gain(source_id, **kw):
        """The two always-available Talk threads are repeatable, so they get one
        relationship gain per day — the same anti-spam intent as the generic
        topic system's burnout, without a second burnout table."""
        if store.zoe_thread_gain_day >= store.day:
            return
        store.zoe_thread_gain_day = store.day
        _zoe_rel(source_id, **kw)

    # ── Beat selector ────────────────────────────────────────────────────────
    # ONE dispatcher, three location hooks. Priority: phone-promised scenes,
    # then callbacks that owe the player a payoff, then one-shot reveals, then
    # the repeatable ordinary-time beat.
    #
    # ponytail: every one-shot below fires the first time its window is hit
    # rather than rolling — these are twelve authored beats over a whole
    # playthrough, not ambient texture, so the pity/roll machinery would only
    # add ways to never see them. Upgrade path if this file grows past ~20
    # beats: route the one-shots through _beat_stable_roll like the Tier A pack.
    def zoe_arc_beat_for(loc):
        if not store.zoe_met:
            return None
        if not npc_here("zoe", loc):
            return None
        if not _beat_global_ok():
            return None
        _zoe_sync_knowledge()
        h = float(store.hour)
        fam = _zoe_fam()
        trust = store.zoe_trust

        # 1. Promised by a text she already sent.
        if store.zoe_second_opinion_pending and loc in ("location_park", "location_cafe"):
            return "zoe_second_opinion_scene"
        if store.zoe_coffee_pending and loc in ("location_cafe", "location_park"):
            return "zoe_coffee_not_advice_scene"

        # 2. Callbacks — each checks its own prerequisite fact.
        if (store.zoe_deadline_submitted and not store.zoe_after_deadline_done
                and store.day - store.zoe_deadline_day >= 4):
            return "zoe_after_deadline_scene"
        if (store.zoe_second_opinion_choice and not store.zoe_noticed_callback_done
                and store.zoe_second_opinion_done and fam >= 40):
            return "zoe_noticed_callback_scene"

        # 3. One-shot reveals, cheapest requirement first.
        if not store.zoe_print_done and loc == "location_hub" and 9 <= h < 13:
            return "zoe_print_scene"
        if (not store.zoe_beige_done and store.knows_zoe_art_interest
                and fam >= 25 and loc == "location_cafe"):
            return "zoe_beige_client_scene"
        if (not store.zoe_bass_window_done and fam >= 20
                and loc == "location_hub" and 9 <= h < 13):
            return "zoe_bass_window_scene"
        if (not store.zoe_not_ready_done and trust >= 30 and fam >= 45
                and store.knows_zoe_paid_creative_work and loc == "location_park"):
            return "zoe_not_ready_scene"
        if (not store.zoe_deadline_scene_done and store.zoe_not_ready_done
                and trust >= 35 and loc in ("location_park", "location_cafe")):
            return "zoe_deadline_scene"
        if (not store.zoe_just_stay_done and fam >= 60 and trust >= 55
                and loc == "location_park"):
            return "zoe_just_stay_scene"

        # 4. Ordinary time. Repeatable, café only, 6-day cooldown.
        if (loc == "location_cafe" and fam >= 30
                and _beat_cooldown_ok("zoe_wednesday", 6)):
            return "zoe_wednesday_grounds_scene"
        return None

    # ── Talk priority menu ───────────────────────────────────────────────────
    # Wraps the shipping resolver rather than editing its 150 lines of
    # if-chains (same interception pattern npc_relationships.rpy uses on
    # _apply_aff). The original keeps absolute priority; ours is the last word
    # before the generic topic screen.
    _check_talk_followup_pre_zoe = _check_talk_followup

    def _check_talk_followup(npc_id):
        result = _check_talk_followup_pre_zoe(npc_id)
        if result is not None:
            return result
        if npc_id == "zoe" and store.zoe_met:
            _zoe_sync_knowledge()
            return "zoe_thread_talk"
        return None


# ═══════════════════════════════════════════════════════════════════════════
# BEATS
# Every label: set_hud("hidden") + story_scene_active on entry, both restored
# on every exit path (zoe_arc_exit).
# ═══════════════════════════════════════════════════════════════════════════

label zoe_arc_exit:
    hide focus_zoe
    $ story_scene_active = False
    $ set_hud("full")
    jump expression _zarc_dest


# ── A. THE PRINT ────────────────────────────────────────────────────────────
# Hub, weekday morning. How she LOOKS at a thing, not that she likes art.
label zoe_print_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_print")
    scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "There's a print taped inside the window of the unit next door — a harbour, sold at a size nobody has wall for. Zoe is standing far too close to it."
    show zoe_street_talk as focus_zoe at sprite_r
    z "The water's wrong and I can't stop looking at it."
    mc "Wrong how?"
    show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
    z "It's lit from the left. Everything else in the frame is lit from behind. So either the sun moved, or they painted the boats on Tuesday and the water on Thursday."
    if knows_zoe_art_interest:
        z "You've heard me do this before. I'm aware."
    menu:
        "\"Does that ruin it?\"":
            show zoe_street_neutral as focus_zoe at sprite_r
            z "That's the annoying part. No."
            "She steps back, tilts her head, and takes another thirty seconds over it."
            z "The wrongness is doing something. I'd have to look at it for a week to work out what."
            $ _zoe_rel("zoe_print", affection=2, familiarity=2)
        "\"You'd have done it differently.\"":
            show zoe_street_laugh as focus_zoe at sprite_r
            z "I'd have done it worse, but I'd have been consistent about it."
            "She says it without any of the false modesty people usually pack around a sentence like that."
            $ _zoe_rel("zoe_print", affection=1, respect=1, familiarity=2)
        "\"I hadn't noticed.\"":
            show zoe_street_talk as focus_zoe at sprite_r, react_nod
            z "Nobody does. That's not a criticism, it's most of the job."
            "She points at the boats, then the water, and once you've seen it you can't unsee it."
            $ _zoe_rel("zoe_print", affection=1, familiarity=2)
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Anyway. I've now spent four minutes of my life on a print in a window I don't like."
    $ knows_zoe_art_interest = True
    $ zoe_print_done = True
    $ add_relationship_memory("zoe", "zoe_print_window", "The harbour print with the wrong light")
    $ spend_time(0.3)
    $ _zarc_dest = "location_hub"
    jump zoe_arc_exit


# ── B. THE CLIENT WANTS BEIGE ───────────────────────────────────────────────
# Café. She has a job. The job is not the work. Both are true at once.
label zoe_beige_client_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_beige")
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock
    show zoe_street_talk as focus_zoe at sprite_r
    "Zoe has a laptop open and three colour swatches laid out beside it, all of which are the same colour."
    z "Client feedback. \"Warmer, but not warm.\" \"Confident, but approachable.\" \"You know.\""
    mc "Do you know?"
    show zoe_street_laugh as focus_zoe at sprite_r
    z "Yes. They want beige. They've wanted beige since March. They're just not allowed to say beige out loud."
    "She turns the laptop. Two versions. One of them is clearly better and clearly not what was asked for."
    menu:
        "\"So give them the good one.\"":
            show zoe_street_neutral as focus_zoe at sprite_r, react_nod
            z "I'll give them both. They'll pick beige."
            z "That's fine. It's their sign, on their building, for their customers. I'm not the last word on it and I don't want to be."
            $ _zoe_rel("zoe_beige", affection=1, respect=2, familiarity=2)
        "\"Doesn't that grind you down?\"":
            show zoe_street_talk as focus_zoe at sprite_r
            z "Everyone assumes it should. It doesn't."
            z "This pays for the paper. What's on the paper at eleven at night is mine and nobody gets feedback rounds on it."
            $ _zoe_rel("zoe_beige", trust=2, familiarity=2)
        "\"Which one's yours?\"":
            show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
            z "Neither. They're both for them."
            "A beat."
            z "That's not a sad answer. It's just a different drawer."
            $ _zoe_rel("zoe_beige", trust=2, respect=1, familiarity=2)
    show zoe_street_neutral as focus_zoe at sprite_r
    z "I'll send both tonight and we'll see how long they take to choose beige."
    $ knows_zoe_paid_creative_work = True
    $ knows_zoe_creative_values = True
    $ zoe_beige_done = True
    $ add_relationship_memory("zoe", "zoe_beige_client", "The client who wanted beige")
    $ spend_time(0.5)
    $ _zarc_dest = "location_cafe"
    jump zoe_arc_exit


# ── C. SECOND OPINION ───────────────────────────────────────────────────────
# She texts first. Not a hidden-correct-answer test — every route is a real
# answer and she engages with the reason, not the pick.
label zoe_second_opinion_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_second_opinion")
    $ zoe_second_opinion_pending = False
    if current_loc == "location_cafe":
        scene expression cafe_bg()
        $ _zso_back = "location_cafe"
    else:
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zso_back = "location_park"
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She has two sheets out before you've fully sat down."
    z "Same brief, same everything. One's built on a diagonal, one's built on a grid. I've looked at them until they both look wrong."
    mc "And you want—"
    show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
    z "A second opinion. Not reassurance. Different thing."
    if skill_art >= 20:
        z "You'll actually see it, which means I don't get to hide behind explaining."
    menu:
        "\"The diagonal. It moves — the grid just sits there.\"":
            $ zoe_second_opinion_choice = "warmth"
            show zoe_street_talk as focus_zoe at sprite_r
            z "It does move. That's the argument for it and the argument against it."
            z "Fine. Noted."
            $ _zoe_rel("zoe_second_opinion", affection=2, respect=1, familiarity=2)
        "\"The grid. Everything has a reason to be where it is.\"":
            $ zoe_second_opinion_choice = "structure"
            show zoe_street_talk as focus_zoe at sprite_r, react_nod
            z "That's the one I keep going back to and I've been assuming that's cowardice."
            z "Maybe it isn't."
            $ _zoe_rel("zoe_second_opinion", affection=1, respect=2, trust=1, familiarity=2)
        "\"Which one do you keep looking at?\"":
            $ zoe_second_opinion_choice = "asked_her"
            show zoe_street_neutral as focus_zoe at sprite_r
            z "That's cheating."
            "Pause."
            z "The diagonal. I look at the diagonal and I send the grid. Every time."
            $ _zoe_rel("zoe_second_opinion", trust=3, familiarity=2)
        "\"I don't know anything about this.\"":
            $ zoe_second_opinion_choice = "no_idea"
            show zoe_street_laugh as focus_zoe at sprite_r
            z "Good. Neither do the people who'll see it."
            mc "Then — the second one. It's easier to look at. That's all I've got."
            z "That's not nothing. That's most of it, actually."
            $ _zoe_rel("zoe_second_opinion", affection=2, familiarity=2)
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Right. That's enough of that. I'll ruin it later."
    $ zoe_second_opinion_done = True
    $ zoe_second_opinion_day = day
    $ knows_zoe_paid_creative_work = True
    $ add_relationship_memory("zoe", "zoe_second_opinion", "Two layouts, and the reason you gave")
    $ spend_time(0.5)
    $ _zarc_dest = _zso_back
    jump zoe_arc_exit


# ── D. BASS IN THE WINDOW ───────────────────────────────────────────────────
# Deliberately unresolved. Nobody starts a band.
label zoe_bass_window_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_bass")
    scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She's stopped walking. The music shop window has a short-scale bass in it, sunburst, priced like an apology."
    if knows_zoe_bass_history:
        # Callback version — she already told you, so she doesn't tell you again.
        show zoe_street_talk as focus_zoe at sprite_r
        z "Don't."
        mc "I didn't say anything."
        z "You were going to make a face."
        "She looks at it for a while longer than a person who has finished with something looks at it."
        z "Thirty seconds. That's the deal I have with myself."
        menu:
            "\"You're at about ninety.\"":
                show zoe_street_laugh as focus_zoe at sprite_r
                z "The deal is flexible."
                $ _zoe_rel("zoe_bass", affection=2, familiarity=1)
            "[[Wait it out with her.]]":
                "You stand there. She doesn't explain and you don't ask. Eventually she starts walking again and you go with her."
                $ _zoe_rel("zoe_bass", trust=3, familiarity=2)
    else:
        show zoe_street_talk as focus_zoe at sprite_r
        if zoe_bass_hint_known:
            # She already let "used to" slip in a generic conversation. This is
            # the same reveal, entered through the door she left open.
            mc "This the bass thing?"
            z "Unfortunately."
        z "I played for six years. Bass. Not well at first, and then actually quite well."
        mc "What happened?"
        z "Nothing happened. That's the boring part."
        z "I was trying to be three things at once and one of them had to go, and it went. I don't remember deciding."
        menu:
            "\"Do you miss it?\"":
                show zoe_street_neutral as focus_zoe at sprite_r
                z "I notice it. That's different from missing it and I'm not sure which one is worse."
                $ _zoe_rel("zoe_bass", trust=3, familiarity=2)
            "\"Six years is a long time to just stop.\"":
                show zoe_street_talk as focus_zoe at sprite_r, react_nod
                z "It is."
                "She doesn't add anything to that, and the silence isn't uncomfortable so you leave it alone."
                $ _zoe_rel("zoe_bass", trust=2, affection=1, familiarity=2)
        show zoe_street_neutral as focus_zoe at sprite_r
        z "Anyway. I look in every window. I've never gone in. I'd like that to stay unexamined."
    $ knows_zoe_bass_history = True
    $ zoe_bass_window_done = True
    $ add_relationship_memory("zoe", "zoe_bass_window", "The bass in the music shop window")
    $ spend_time(0.3)
    $ _zarc_dest = "location_hub"
    jump zoe_arc_exit


# ── E. COFFEE, NOT ADVICE ───────────────────────────────────────────────────
# She asked for presence. The best Trust outcome is giving her presence.
# The clumsy supportive answer costs almost nothing — she can tell you meant it.
label zoe_coffee_not_advice_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_coffee")
    $ zoe_coffee_pending = False
    if current_loc == "location_park":
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zc_back = "location_park"
    else:
        scene expression cafe_bg()
        $ _zc_back = "location_cafe"
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She's already got two coffees. She doesn't look up when you sit."

    mc "How bad?"
    z "You already broke the rule."
    mc "I asked how bad."
    z "That's adjacent to advice."
    mc "Fine."
    mc "Coffee."
    z "Coffee."

    pause 0.5

    show zoe_street_talk as focus_zoe at sprite_r
    z "They said no."
    mc "The funding?"
    z "Yeah."
    mc "Sorry."
    z "Thanks."
    pause 0.5
    show zoe_street_neutral as focus_zoe at sprite_r
    z "See?"
    mc "See what?"
    z "Perfect response."
    mc "I said one word."
    z "Exactly."

    z "I spent three weeks convincing myself I didn't care."
    mc "Did it work?"
    z "Beautifully."
    mc "Until they replied."
    z "Until they replied."

    menu:
        "\"They were wrong.\"":
            mc "They were wrong."
            show zoe_street_talk as focus_zoe at sprite_r
            z "Maybe."
            mc "That's it?"
            z "You don't know if they were wrong."
            z "You haven't seen the whole proposal."
            mc "I know you cared about it."
            show zoe_street_neutral as focus_zoe at sprite_r
            z "..."
            z "That's annoyingly better."
            $ _zoe_rel("zoe_coffee", trust=3, affection=1, familiarity=2)
        "\"Want to talk about it?\"":
            mc "Want to talk about it?"
            show zoe_street_neutral as focus_zoe at sprite_r
            z "Not really."
            mc "Okay."
            z "..."
            z "Maybe later."
            $ _zoe_rel("zoe_coffee", trust=2, familiarity=2)
        "[[Say nothing.]]":
            mc "..."
            show zoe_street_neutral as focus_zoe at sprite_r, react_nod
            z "Thank you."
            mc "For what?"
            z "Not fixing it."
            $ _zoe_rel("zoe_coffee", trust=4, affection=1, familiarity=2)

    show zoe_street_talk as focus_zoe at sprite_r
    z "Tell me something stupid."
    mc "What?"
    z "Something that doesn't matter."
    mc "That's a lot of pressure."
    z "I believe in you."

    if marcus_five_am_known:
        mc "Marcus thinks waking up at five is a personality."
        show zoe_street_laugh as focus_zoe at sprite_r
        z "He told you?"
        mc "That he can't sleep?"
        z "Oh, this is excellent."
        mc "I was told specifically not to tell you."
        z "And yet."
        mc "I may have misunderstood the assignment."
        z "You understood it perfectly."
    else:
        mc "I saw a guy miss a trash can from about two feet away today."
        show zoe_street_laugh as focus_zoe at sprite_r
        z "How badly?"
        mc "Different direction."
        z "Okay."
        z "That's helping."

    show zoe_street_neutral as focus_zoe at sprite_r
    mc "Want another coffee?"
    z "No."
    mc "Want advice now?"
    z "Absolutely not."
    mc "Progress."
    z "..."
    z "Thanks for coming."
    mc "Any time."
    show zoe_street_talk as focus_zoe at sprite_r
    z "Careful."
    mc "What?"
    z "I might remember that."
    # This scene is the ONLY place the rejection is delivered. Both facts are
    # set here so nothing downstream has to ask which route told the player.
    $ store.knows_zoe_funding_problem = True
    $ store.zoe_grant_discussed = True
    $ zoe_coffee_callback_pending = True
    $ zoe_coffee_done = True
    $ add_relationship_memory("zoe", "zoe_coffee_not_advice", "The bad email, and not fixing it")
    $ spend_time(1.0)
    $ _zarc_dest = _zc_back
    jump zoe_arc_exit


# ── F. NOT READY TO SHOW IT ─────────────────────────────────────────────────
label zoe_not_ready_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_not_ready")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She has a folder she hasn't opened yet, and she's had it on her lap for the whole conversation."
    show zoe_street_talk as focus_zoe at sprite_r
    z "This isn't the client thing. This is the other thing."
    z "It's not finished and it's not ready and I'm going to show you anyway, which I'd like on the record as a bad decision."
    "Six pieces. The harbour, but taken apart — the same water in six different weathers, and one of them barely reads as water at all."
    menu:
        "\"What do you see in it?\"":
            show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
            z "Six attempts at one hour of the day. Five of them are me being competent."
            z "The sixth one I don't understand and that's the one I'd keep."
            $ _zoe_rel("zoe_not_ready", trust=4, respect=1, familiarity=2)
        "\"The fifth one is doing something the others aren't.\"" if skill_art >= 20:
            show zoe_street_neutral as focus_zoe at sprite_r
            z "Say more."
            mc "It stopped describing the water. It's just the light off it."
            "She looks at you, then at the sheet, then back."
            z "Right. Yes. That one stays and the other five are argument."
            $ _zoe_rel("zoe_not_ready", trust=3, respect=3, familiarity=2)
        "[[Just look. Take your time.]]":
            "You go through them twice. She watches your hands more than your face."
            show zoe_street_neutral as focus_zoe at sprite_r, react_nod
            z "You went back to the same one."
            mc "I did."
            z "So did I."
            $ _zoe_rel("zoe_not_ready", trust=4, affection=1, familiarity=2)
    show zoe_street_talk as focus_zoe at sprite_r
    # ONE gallery object across the whole story: the small gallery raised in
    # arc_zoe_art_2, submitted to in zoe_deadline_scene, answered in
    # zoe_after_deadline_scene, walked into in zoe_exhibition_opening.
    z "There's an open submission for a small gallery next month."
    z "These could go in."
    z "I haven't decided if that's a good idea."
    mc "Do you want my opinion?"
    z "Absolutely not."
    pause 0.5
    z "Ask me again when I've stopped carrying the folder everywhere."
    $ knows_zoe_gallery_goal = True
    $ knows_zoe_creative_values = True
    $ zoe_not_ready_done = True
    $ add_relationship_memory("zoe", "zoe_not_ready", "The six harbour pieces, unfinished")
    $ spend_time(0.5)
    $ _zarc_dest = "location_park"
    jump zoe_arc_exit


# ── G. THE THING YOU NOTICED ────────────────────────────────────────────────
# Requires zoe_second_opinion_choice. She references the CONTENT of what you
# said, never "remember when we talked".
label zoe_noticed_callback_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_noticed")
    if current_loc == "location_cafe":
        scene expression cafe_bg()
        $ _zn_back = "location_cafe"
    elif current_loc == "location_hub":
        scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
        $ _zn_back = "location_hub"
    else:
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zn_back = "location_park"
    show screen hud
    hide screen people_here_dock
    show zoe_street_talk as focus_zoe at sprite_r
    if zoe_second_opinion_choice == "warmth":
        z "I redid the grid version so it moves. Diagonal underneath, grid on top."
        z "You said the grid just sits there. It was sitting there. I'd stopped being able to tell."
    elif zoe_second_opinion_choice == "structure":
        z "I kept the grid. And then I made it more of a grid, because you said everything had a reason to be where it was and two things didn't."
        z "Now they do."
    elif zoe_second_opinion_choice == "asked_her":
        z "I sent the diagonal."
        show zoe_street_neutral as focus_zoe at sprite_r
        z "You didn't tell me which one. You made me say which one I keep looking at, and then I had to live with having said it."
    else:
        z "I went with the one that's easier to look at."
        z "You said that like it was an apology. It's the entire brief. I've been overthinking it for two weeks."
    menu:
        "\"Did it work?\"":
            show zoe_street_laugh as focus_zoe at sprite_r
            z "Ask me in a month. But it's better, and I know why it's better, which is the rarer of the two."
            $ _zoe_rel("zoe_noticed", affection=2, respect=2, familiarity=2)
        "\"You've been thinking about that for a while.\"":
            show zoe_street_neutral as focus_zoe at sprite_r
            z "Yes."
            "She doesn't dress it up, which from her is the whole admission."
            $ _zoe_rel("zoe_noticed", trust=3, affection=1, familiarity=2)
    $ zoe_noticed_callback_done = True
    $ zoe_second_opinion_callback_done = True
    $ mark_memory_referenced("zoe", "zoe_second_opinion")
    $ spend_time(0.3)
    $ _zarc_dest = _zn_back
    jump zoe_arc_exit


# ── H. WEDNESDAY AT GROUNDS ─────────────────────────────────────────────────
# No revelation. Ordinary time, which is the thing that was missing.
label zoe_wednesday_grounds_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_wednesday")
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She's in the corner with the bad table and the good light, which is the trade she always makes."
    # First occurrence is authored (story_direct_pass.rpy). Every later
    # Wednesday uses the variant pool below. Old saves that already ran this
    # beat are migrated past it by _sd_backfill().
    if not zoe_wednesday_first_done:
        jump zoe_wednesday_first_scene
    python:
        _zw_pool = []
        if knows_zoe_paid_creative_work:
            _zw_pool.append("client")
        if knows_zoe_bass_history:
            _zw_pool.append("music")
        _zw_pool += ["local", "small"]
        _zw = _pick_ambient_variant("zoe_wednesday_topic", _zw_pool)
    if _zw == "client":
        show zoe_street_talk as focus_zoe at sprite_r
        z "Two rounds of feedback today and both of them were the word 'pop'."
        mc "What does it mean?"
        z "Nothing. It's a noise people make when a thing is finished and they're not ready for it to be."
    elif _zw == "music":
        show zoe_street_talk as focus_zoe at sprite_r
        z "Whoever does the playlist in here has started sneaking in basslines you can actually hear."
        z "It's ruining my concentration and I'd like them to keep doing it."
    elif _zw == "local":
        show zoe_street_talk as focus_zoe at sprite_r
        z "They've repainted the shutters on the corner unit. Grey to a slightly different grey."
        z "Someone was paid for that decision. I think about it most days now."
    else:
        show zoe_street_talk as focus_zoe at sprite_r
        z "I've been putting the milk in first this week. No reason. Just seeing what happens."
        mc "And?"
        z "Nothing happens. That's the finding."
    "The rest of it is an hour of nothing in particular. Nobody needs anything from anybody."
    show zoe_street_laugh as focus_zoe at sprite_r
    z "Same table next week, probably. I'm nothing if not predictable about furniture."
    $ _zoe_rel("zoe_wednesday", affection=1, familiarity=3)
    # Shared routine (relationship_continuity.rpy): two of these unlock the
    # "Grounds?" shorthand text. Shares rc_zoe_grounds_count_day with the
    # greeting counter so one afternoon can never count twice.
    if rc_zoe_grounds_count_day != day:
        $ rc_zoe_grounds_count_day = day
        $ zoe_grounds_count += 1
    $ spend_time(1.0)
    $ _zarc_dest = "location_cafe"
    jump zoe_arc_exit


# ── J. THE DEADLINE ─────────────────────────────────────────────────────────
# Extends the open call raised in F. Depth changes how personally she involves
# you, not whether you get a quest checklist.
label zoe_deadline_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_deadline")
    if current_loc == "location_cafe":
        scene expression cafe_bg()
        $ _zd_back = "location_cafe"
    else:
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zd_back = "location_park"
    show screen hud
    hide screen people_here_dock
    show zoe_street_talk as focus_zoe at sprite_r
    z "I sent them."

    mc "The harbour pieces?"
    z "Six of them."
    mc "All six?"
    z "I had a bad five minutes."

    pause 0.5

    show zoe_street_neutral as focus_zoe at sprite_r
    z "Then I had a worse five minutes and nearly withdrew them."
    mc "But you didn't."
    z "No."

    menu:
        "\"Good.\"":
            mc "Good."
            z "Very nuanced feedback."
            mc "You submitted them. I'm allowed one uncomplicated response."
            z "Fine."
            z "One."
            $ _zoe_rel("zoe_deadline", affection=2, familiarity=2)

        "\"How do you feel?\"":
            mc "How do you feel?"
            z "Like I've accidentally mailed someone a part of my brain."
            mc "So, normal."
            z "Completely."
            $ _zoe_rel("zoe_deadline", trust=2, familiarity=2)

        "\"Which one nearly stopped you?\"":
            mc "Which one nearly stopped you?"
            z "The one I don't understand."
            mc "That's the one you said you'd keep."
            z "I know."
            z "That's the problem."
            $ _zoe_rel("zoe_deadline", trust=3, respect=1, familiarity=2)

    show zoe_street_talk as focus_zoe at sprite_r
    z "Anyway."
    z "They're gone."
    mc "Now you wait."
    z "Don't use my own material against me."
    # NO ROLL. The submission is a story beat, not a lottery: the answer is
    # authored in zoe_after_deadline_scene and is the same every playthrough.
    # zoe_deadline_result is kept only because the memory id below reads it.
    $ zoe_deadline_result = "success"
    $ zoe_deadline_submitted = True
    $ zoe_deadline_day = day
    $ zoe_deadline_scene_done = True
    $ knows_zoe_gallery_goal = True
    $ add_relationship_memory("zoe", "zoe_deadline_submitted", "She sent the harbour set to an open call")
    $ spend_time(0.5)
    $ _zarc_dest = _zd_back
    jump zoe_arc_exit


# ── K. AFTER THE DEADLINE ───────────────────────────────────────────────────
# Mandatory echo, and the single authored answer to the open call. Being taken
# is not a state change to her whole personality — it is four things on a wall.
label zoe_after_deadline_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_after_deadline")
    if current_loc == "location_cafe":
        scene expression cafe_bg()
        $ _zk_back = "location_cafe"
    elif current_loc == "location_hub":
        scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
        $ _zk_back = "location_hub"
    else:
        scene expression ("parknight" if hour >= 20 else "parkday")
        $ _zk_back = "location_park"
    show screen hud
    hide screen people_here_dock
    # NO ROLL. One authored answer — the open call raised in zoe_not_ready_scene
    # and submitted to in zoe_deadline_scene took four of the six, and this is
    # the invitation the shipping exhibition path is waiting for.
    show zoe_street_neutral as focus_zoe at sprite_r
    z "They took them."

    mc "The harbour set?"
    z "Four of the six."

    mc "That's good."
    z "Yes."

    pause 0.5

    show zoe_street_talk as focus_zoe at sprite_r
    mc "You don't sound convinced."
    z "I'm convinced it's good."
    z "I'm less convinced I enjoy four things I made being attached to a wall where strangers can stand in front of them."

    menu:
        "\"Which two didn't they take?\"":
            mc "Which two didn't they take?"
            z "The safest one."
            mc "And?"
            z "The other safest one."
            mc "That feels significant."
            z "Don't."
            $ _zoe_rel("zoe_after_deadline", trust=2, respect=1, familiarity=2)

        "\"When's the opening?\"":
            mc "When's the opening?"
            z "Friday."
            mc "You want me there?"
            z "..."
            z "I was getting to that."
            $ _zoe_rel("zoe_after_deadline", affection=2, trust=1, familiarity=2)

        "\"You did the hard part.\"":
            mc "You did the hard part."
            z "No."
            z "The hard part apparently has track lighting and free wine."
            $ _zoe_rel("zoe_after_deadline", affection=1, familiarity=2)

    show zoe_street_neutral as focus_zoe at sprite_r
    z "Come, if you want."
    mc "That an invitation?"
    z "Don't make me repeat it."
    # THE canonical exhibition arm. zoe_msg_exhibition_invite
    # (phone_actionable.rpy) reads this flag, queues npc_invitation_pending
    # "zoe_exhibition", and the gallery (locations.rpy) runs
    # zoe_exhibition_opening. No parallel invitation object is created.
    $ store.zoe_exhibition_invited = True
    $ zoe_after_deadline_done = True
    $ zoe_deadline_followup_done = True
    $ add_relationship_memory("zoe", "zoe_deadline_result_" + zoe_deadline_result,
                              "How the open call went")
    $ spend_time(0.5)
    $ _zarc_dest = _zk_back
    jump zoe_arc_exit


# ── L. JUST STAY ────────────────────────────────────────────────────────────
# Friendship-capable by default. The romantic variant is one extra line, only
# where the relationship already has that context.
label zoe_just_stay_scene:
    $ set_hud("hidden")
    $ story_scene_active = True
    $ _beat_triggered("zoe_just_stay")
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "She's got a canvas bag with her and she's mentioned it twice without saying what's in it."
    z "I was going to drop something off at the framers and it's on the way, roughly."
    mc "Roughly."
    show zoe_street_talk as focus_zoe at sprite_r
    z "Within about a mile of on the way."
    "You end up sitting down instead. The bag stays shut. The framers is presumably closed by now."
    "It goes on longer than it needs to and neither of you does anything about that."
    menu:
        "\"So what did you actually need?\"":
            pass
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Nothing."
    "A beat. She looks at the bag, then at the path, then at you."
    show zoe_street_talk as focus_zoe at sprite_r
    z "I was trying to make that sound less weird."
    menu:
        "\"It didn't sound weird.\"":
            show zoe_street_neutral as focus_zoe at sprite_r, react_nod
            z "It sounded a bit weird."
            z "Stay anyway."
            $ _zoe_rel("zoe_just_stay", trust=4, affection=2, familiarity=3)
        "\"You could've just said.\"":
            show zoe_street_laugh as focus_zoe at sprite_r
            z "I know. I'm working up to it. This was the draft."
            $ _zoe_rel("zoe_just_stay", trust=3, affection=3, familiarity=3)
    if get_romance_state("zoe") in ("interested", "dating", "committed"):
        show zoe_street_neutral as focus_zoe at sprite_r, react_lean_in
        z "For the record, I'm aware of what this is. I just wanted an hour where neither of us had to say it."
        $ _zoe_rel("zoe_just_stay", attraction=4)
    $ zoe_just_stay_done = True
    $ add_relationship_memory("zoe", "zoe_just_stay", "The bag she never opened")
    $ spend_time(1.0)
    $ _zarc_dest = "location_park"
    jump zoe_arc_exit


# ═══════════════════════════════════════════════════════════════════════════
# CONTEXTUAL TALK — priority threads in front of the generic 9 topics
# ═══════════════════════════════════════════════════════════════════════════

label zoe_thread_talk:
    menu:
        "Ask how the submission went" if zoe_deadline_submitted and not zoe_deadline_followup_done:
            call zoe_talk_deadline_followup
        "Ask about the bass" if knows_zoe_bass_history and not zoe_bass_followup_done:
            call zoe_talk_bass_followup
        "Ask which version she used" if zoe_second_opinion_choice and not zoe_second_opinion_callback_done:
            call zoe_talk_second_opinion_callback
        "What are you working on?":
            call zoe_talk_working_on
        "Just hang out":
            call zoe_talk_hang_out
        "More topics...":
            call zoe_talk_more
    return


label zoe_talk_deadline_followup:
    z "Nothing yet. Galleries answer on gallery time, which is a season, not a date."
    z "You'll know when I know. Possibly before I've decided how I feel about it."
    $ zoe_deadline_followup_done = True
    $ _zoe_rel("zoe_talk_deadline", trust=1, familiarity=1)
    $ _do_talk_accounting("zoe")
    return


label zoe_talk_bass_followup:
    mc "Ever get any closer to the shop door?"
    z "I got as far as reading the price tag properly. That's not closer, that's research."
    "She thinks about it for a second longer than the joke needs."
    z "It's still there. I check."
    $ zoe_bass_followup_done = True
    $ _zoe_rel("zoe_talk_bass", trust=2, familiarity=1)
    $ _do_talk_accounting("zoe")
    return


label zoe_talk_second_opinion_callback:
    if zoe_second_opinion_choice == "asked_her":
        z "The diagonal. Same as I always do. You just made me admit it first."
    elif zoe_second_opinion_choice == "no_idea":
        z "The easy one. Turns out 'easy to look at' was the brief the whole time."
    else:
        z "I used most of yours and about a third of mine, and I'm not telling you which third."
    $ zoe_second_opinion_callback_done = True
    $ _zoe_rel("zoe_talk_second_opinion", affection=1, respect=1, familiarity=1)
    $ _do_talk_accounting("zoe")
    return


label zoe_talk_working_on:
    if zoe_deadline_submitted:
        z "Waiting. Which is technically a medium."
    elif knows_zoe_gallery_goal:
        z "The harbour set. Still. It's at the stage where I'm making it worse to find out where better is."
    elif knows_zoe_paid_creative_work:
        z "Client things. A logo that has to say 'family-run' and 'premium' at the same time, which are opposites."
    elif knows_zoe_art_interest:
        z "Water, mostly. It keeps changing while I'm looking at it, which I'm choosing to take personally."
    else:
        z "Lines on paper. That's as specific as it gets before I know you better."
    $ _zoe_talk_gain("zoe_talk_working", affection=1, familiarity=1)
    $ _do_talk_accounting("zoe")
    return


label zoe_talk_hang_out:
    if _zoe_fam() >= 50:
        z "Fine by me. I've hit the part of the day where I stop being useful anyway."
        "You don't do anything in particular for a while. It's easily the better half of the afternoon."
    else:
        z "Sure. I'm not going to entertain you, though."
        "She goes back to her sketchbook. You stay. It's oddly companionable."
    $ _zoe_talk_gain("zoe_talk_hangout", affection=1, familiarity=2)
    $ _do_talk_accounting("zoe")
    return


label zoe_talk_more:
    # Mirrors the fall-through in npc_interact: contextual talk first, then the
    # generic topic screen (which routes into the topic arcs).
    $ _ctx_label = _ctx_talk_label("zoe")
    if _ctx_label:
        call expression _ctx_label
        $ _do_talk_accounting("zoe")
    else:
        $ _t = renpy.call_screen("npc_topics", "zoe")
        if _t != "back":
            $ _arc = check_arc("zoe", _t)
            if _arc is not None:
                call expression _arc["label"]
            else:
                $ do_talk("zoe", _t)
    return


# ═══════════════════════════════════════════════════════════════════════════
# PHONE INITIATIVE — registered into the SHIPPING picker
# ═══════════════════════════════════════════════════════════════════════════
# No new cadence engine. The existing per-NPC cooldown (zoe: 4, tier-adjusted
# to 5/4/3/3) plus the one-contact-per-day global budget already produce the
# target cadence: ~7-10 days at acquaintance, ~4-7 comfortable, ~3-6 close.
# Mix is controlled by _VARIANT_WEIGHTS: observation 4, project 3,
# invitation 2, personal 2.

init 3 python:

    # ── Response option lists ────────────────────────────────────────────────
    _ZOE_SECOND_OPINION_RESP = [
        {"id": "yes",   "text": "Show me.",                  "label": "npc_ini_zoe_secopin_yes"},
        {"id": "diff",  "text": "What's the difference?",    "label": "npc_ini_zoe_secopin_diff"},
        {"id": "later", "text": "Not today.",                "label": "npc_ini_zoe_secopin_later"},
    ]
    _ZOE_BAD_EMAIL_RESP = [
        {"id": "coffee", "text": "Coffee. I won't fix it.",  "label": "npc_ini_zoe_bademail_coffee"},
        {"id": "what",   "text": "How bad?",                 "label": "npc_ini_zoe_bademail_what"},
    ]
    _ZOE_ALIVE_RESP = [
        {"id": "yes",   "text": "Barely.",                   "label": "npc_ini_zoe_alive_yes"},
        {"id": "soon",  "text": "I'll come find you.",       "label": "npc_ini_zoe_alive_soon"},
    ]
    _ZOE_PERSONALLY_RESP = [
        {"id": "sorry", "text": "That's on me.",             "label": "npc_ini_zoe_personally_sorry"},
        {"id": "joke",  "text": "Mostly?",                   "label": "npc_ini_zoe_personally_joke"},
    ]
    _ZOE_MURAL_RESP = [
        {"id": "worse", "text": "Worse how?",                "label": "npc_ini_zoe_mural_worse"},
        {"id": "like",  "text": "I like that mural.",        "label": "npc_ini_zoe_mural_like"},
    ]
    _ZOE_BEIGE_CB_RESP = [
        {"id": "called","text": "You called it.",            "label": "npc_ini_zoe_beigecb_called"},
        {"id": "paid",  "text": "Did they pay?",             "label": "npc_ini_zoe_beigecb_paid"},
    ]
    _ZOE_BASS_CB_RESP = [
        {"id": "buy",   "text": "Go in.",                    "label": "npc_ini_zoe_basscb_buy"},
        {"id": "noted", "text": "Noted.",                    "label": "npc_ini_zoe_basscb_noted"},
    ]
    _ZOE_POSTER_RESP = [
        {"id": "agree", "text": "Strong feelings are the point.", "label": "npc_ini_zoe_poster_agree"},
        {"id": "what",  "text": "What's negative space?",    "label": "npc_ini_zoe_poster_what"},
    ]
    _ZOE_PARK_HOUR_RESP = [
        {"id": "yes",   "text": "On my way.",                "label": "npc_ini_zoe_parkhour_yes"},
        {"id": "no",    "text": "Can't today.",              "label": "npc_ini_zoe_parkhour_no"},
    ]
    _ZOE_GROUNDS_RESP = [
        {"id": "yes",   "text": "Yes.",                      "label": "npc_ini_zoe_grounds_yes"},
        {"id": "no",    "text": "No.",                       "label": "npc_ini_zoe_grounds_no"},
    ]
    _ZOE_LEAVE_FLAT_RESP = [
        {"id": "yes",   "text": "Where are we going?",       "label": "npc_ini_zoe_leaveflat_yes"},
        {"id": "no",    "text": "Go without me.",            "label": "npc_ini_zoe_leaveflat_no"},
    ]
    _ZOE_SUBMITTED_RESP = [
        {"id": "guess", "text": "Personality, guaranteed.",  "label": "npc_ini_zoe_submitted_guess"},
        {"id": "done",  "text": "It's out of your hands.",   "label": "npc_ini_zoe_submitted_done"},
    ]
    _ZOE_BRIEFS_RESP = [
        {"id": "which", "text": "Which brief wins?",         "label": "npc_ini_zoe_briefs_which"},
        {"id": "luck",  "text": "Good luck.",                "label": "npc_ini_zoe_briefs_luck"},
    ]
    _ZOE_SECOPIN_CB_RESP = [
        {"id": "which", "text": "Which one did you use?",    "label": "npc_ini_zoe_secopincb_which"},
        {"id": "glad",  "text": "Glad it helped.",           "label": "npc_ini_zoe_secopincb_glad"},
    ]

    _ZOE_ARC_MSGS = {
        # Observation / callback — 40% of the pool by weight.
        "zoe_msg_mural":            {"text": "Saw that mural at Quayside again. It's worse in daylight.",
                                     "responses": _ZOE_MURAL_RESP},
        "zoe_msg_beige_callback":   {"text": "The beige client chose the beige version. Art survives another day.",
                                     "responses": _ZOE_BEIGE_CB_RESP},
        "zoe_msg_bass_window":      {"text": "There's a bass in the window at the music shop on Crestwell. Thought you should know.",
                                     "responses": _ZOE_BASS_CB_RESP},
        "zoe_msg_poster":           {"text": "New exhibition poster went up at Grounds. Someone has very strong feelings about negative space.",
                                     "responses": _ZOE_POSTER_RESP},
        "zoe_msg_secopin_callback": {"text": "For the record, I used the one you didn't pick. You were still right about the reason.",
                                     "responses": _ZOE_SECOPIN_CB_RESP},
        # Light invitation — 30%.
        "zoe_msg_park_hour":        {"text": "Park? I have about an hour before I have to pretend to be productive.",
                                     "responses": _ZOE_PARK_HOUR_RESP},
        "zoe_msg_grounds_yesno":    {"text": "Grounds? Yes or no.",
                                     "responses": _ZOE_GROUNDS_RESP},
        "zoe_msg_leave_flat":       {"text": "I need to leave the flat. Come with?",
                                     "responses": _ZOE_LEAVE_FLAT_RESP},
        "zoe_msg_second_opinion":   {"text": "Need a second opinion. Not reassurance. Different thing.",
                                     "responses": _ZOE_SECOND_OPINION_RESP},
        # Project update — 20%.
        "zoe_msg_submitted_client": {"text": "Submitted the client work. Waiting for the inevitable feedback that it 'needs more personality'.",
                                     "responses": _ZOE_SUBMITTED_RESP},
        "zoe_msg_studio_briefs":    {"text": "Studio time tomorrow. Somehow have to turn three conflicting briefs into one coherent thing.",
                                     "responses": _ZOE_BRIEFS_RESP},
        # Personal / check-in — 10%, comfortable and up.
        "zoe_msg_alive":            {"text": "You alive?",
                                     "responses": _ZOE_ALIVE_RESP},
        "zoe_msg_taking_personally":{"text": "Haven't seen you all week. Starting to take it personally. ...mostly joking.",
                                     "responses": _ZOE_PERSONALLY_RESP},
        "zoe_msg_bad_email":        {"text": "Coffee? Not advice. Important distinction.",
                                     "responses": _ZOE_BAD_EMAIL_RESP},
    }

    def _zoe_gap_days():
        """Days since the player last actually interacted with Zoe.
        npc_last_seen is stamped in npc_interact, not on location entry."""
        return store.day - store.npc_last_seen.get("zoe", -999)

    _ZOE_ARC_MIN_TIER = {
        "zoe_msg_mural":             0,
        "zoe_msg_poster":            0,
        "zoe_msg_studio_briefs":     0,
        "zoe_msg_submitted_client":  1,
        "zoe_msg_park_hour":         1,
        "zoe_msg_grounds_yesno":     1,
        "zoe_msg_leave_flat":        1,
        "zoe_msg_second_opinion":    1,
        "zoe_msg_beige_callback":    1,
        "zoe_msg_bass_window":       1,
        "zoe_msg_secopin_callback":  1,
        "zoe_msg_alive":             1,
        "zoe_msg_taking_personally": 2,
        "zoe_msg_bad_email":         2,
    }
    _ZOE_ARC_WEIGHTS = {
        "zoe_msg_mural":             4,
        "zoe_msg_poster":            4,
        "zoe_msg_beige_callback":    4,
        "zoe_msg_bass_window":       4,
        "zoe_msg_secopin_callback":  4,
        "zoe_msg_park_hour":         2,
        "zoe_msg_grounds_yesno":     2,
        "zoe_msg_leave_flat":        2,
        "zoe_msg_second_opinion":    2,
        "zoe_msg_submitted_client":  3,
        "zoe_msg_studio_briefs":     3,
        "zoe_msg_alive":             2,
        "zoe_msg_taking_personally": 2,
        "zoe_msg_bad_email":         2,
    }
    _ZOE_ARC_CONDITIONS = {
        # Each callback checks the fact it is calling back to.
        "zoe_msg_beige_callback":    lambda: store.zoe_beige_done,
        "zoe_msg_bass_window":       lambda: store.knows_zoe_bass_history,
        "zoe_msg_poster":            lambda: store.knows_zoe_art_interest,
        "zoe_msg_submitted_client":  lambda: store.knows_zoe_paid_creative_work,
        "zoe_msg_studio_briefs":     lambda: store.knows_zoe_paid_creative_work,
        "zoe_msg_secopin_callback":  lambda: (store.zoe_second_opinion_done
                                              and not store.zoe_second_opinion_callback_done
                                              and store.day - store.zoe_second_opinion_day >= 3),
        # Scene-promising messages: only when the scene is actually available.
        "zoe_msg_second_opinion":    lambda: (store.knows_zoe_art_interest
                                              and not store.zoe_second_opinion_done
                                              and not store.zoe_second_opinion_pending),
        # The Coffee scene IS the funding rejection. It can only be offered
        # once the player knows an application exists (arc_zoe_art_3), so
        # mc "The funding?" is never a line about something he never heard of.
        "zoe_msg_bad_email":         lambda: (store.zoe_funding_application_known
                                              and not store.zoe_coffee_done
                                              and not store.zoe_coffee_pending),
        # "You disappeared" — gap only, and never a penalty.
        "zoe_msg_alive":             lambda: _zoe_gap_days() >= 5,
        "zoe_msg_taking_personally": lambda: _zoe_gap_days() >= 7,
    }

    _INITIATIVE_MSGS.update(_ZOE_ARC_MSGS)
    _INITIATIVE_VARIANTS["zoe"] = _INITIATIVE_VARIANTS["zoe"] + list(_ZOE_ARC_MSGS.keys())
    _VARIANT_MIN_TIER.update(_ZOE_ARC_MIN_TIER)
    _VARIANT_WEIGHTS.update(_ZOE_ARC_WEIGHTS)
    _VARIANT_CONDITIONS.update(_ZOE_ARC_CONDITIONS)


# ── Reply labels ────────────────────────────────────────────────────────────
# Same shape as every other initiative reply: one line back, clear the pending
# slot. The two scene-promising messages also arm their scene flag.

label npc_ini_zoe_secopin_yes:
    $ zoe_second_opinion_pending = True
    $ queue_phone_message("zoe", "Park or Grounds, whichever you hit first. I'll have both out.", day, "zoe_msg_secopin_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_secopin_diff:
    $ zoe_second_opinion_pending = True
    $ queue_phone_message("zoe", "About four degrees and my entire sense of self. Come look.", day, "zoe_msg_secopin_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_secopin_later:
    $ queue_phone_message("zoe", "Fine. They'll still be wrong tomorrow.", day, "zoe_msg_secopin_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_bademail_coffee:
    $ zoe_coffee_pending = True
    $ queue_phone_message("zoe", "Correct answer. Grounds, or the park if I've moved.", day, "zoe_msg_bademail_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_bademail_what:
    $ zoe_coffee_pending = True
    $ queue_phone_message("zoe", "Bad enough that I'm asking. Not bad enough to type.", day, "zoe_msg_bademail_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_alive_yes:
    $ queue_phone_message("zoe", "Acceptable.", day, "zoe_msg_alive_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_alive_soon:
    $ queue_phone_message("zoe", "I'll be somewhere findable.", day, "zoe_msg_alive_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_personally_sorry:
    $ queue_phone_message("zoe", "It isn't. That was the joke half.", day, "zoe_msg_personally_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_personally_joke:
    $ queue_phone_message("zoe", "Mostly.", day, "zoe_msg_personally_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_mural_worse:
    $ queue_phone_message("zoe", "The shadows were painted at night. Now they point the wrong way for eleven hours a day.", day, "zoe_msg_mural_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_mural_like:
    $ queue_phone_message("zoe", "So do I. That's what makes it unbearable.", day, "zoe_msg_mural_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_beigecb_called:
    $ queue_phone_message("zoe", "I always call it. It's my one gift.", day, "zoe_msg_beigecb_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_beigecb_paid:
    $ queue_phone_message("zoe", "Thirty days from invoice, allegedly.", day, "zoe_msg_beigecb_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_basscb_buy:
    $ queue_phone_message("zoe", "Absolutely not. I'm just reporting the weather.", day, "zoe_msg_basscb_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_basscb_noted:
    $ queue_phone_message("zoe", "Good. That's all it was.", day, "zoe_msg_basscb_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_poster_agree:
    $ queue_phone_message("zoe", "They're the only feelings worth having about a poster.", day, "zoe_msg_poster_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_poster_what:
    $ queue_phone_message("zoe", "The bit that isn't the thing. There is a great deal of it on this poster.", day, "zoe_msg_poster_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_parkhour_yes:
    $ _apply_aff("zoe", 1)
    $ queue_phone_message("zoe", "Bench near the far gate. I'm the one squinting.", day, "zoe_msg_parkhour_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_parkhour_no:
    # No penalty. She offered; she didn't ask.
    $ queue_phone_message("zoe", "Fine. I'll be productive out of spite.", day, "zoe_msg_parkhour_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_grounds_yes:
    $ _apply_aff("zoe", 1)
    $ queue_phone_message("zoe", "Good. Corner table. Bad chair, good light.", day, "zoe_msg_grounds_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_grounds_no:
    $ queue_phone_message("zoe", "Respect the brevity.", day, "zoe_msg_grounds_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_leaveflat_yes:
    $ _apply_aff("zoe", 1)
    $ queue_phone_message("zoe", "Unclear. That's the appeal.", day, "zoe_msg_leaveflat_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_leaveflat_no:
    $ queue_phone_message("zoe", "I will. Reluctantly and at length.", day, "zoe_msg_leaveflat_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_submitted_guess:
    $ queue_phone_message("zoe", "You've done this before.", day, "zoe_msg_submitted_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_submitted_done:
    $ queue_phone_message("zoe", "It is never out of my hands. That's the flaw in the system.", day, "zoe_msg_submitted_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_briefs_which:
    $ queue_phone_message("zoe", "The one from the person who signs things.", day, "zoe_msg_briefs_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_briefs_luck:
    $ queue_phone_message("zoe", "Luck is not the constraint. Time is.", day, "zoe_msg_briefs_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_secopincb_which:
    $ zoe_second_opinion_callback_done = True
    if zoe_second_opinion_choice == "asked_her":
        $ queue_phone_message("zoe", "The diagonal. You already knew that, you just made me say it.", day, "zoe_msg_secopincb_r1")
    else:
        $ queue_phone_message("zoe", "The other one. But I moved it because of what you said, so you're implicated.", day, "zoe_msg_secopincb_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_secopincb_glad:
    $ zoe_second_opinion_callback_done = True
    $ queue_phone_message("zoe", "I didn't say it helped. I said you were right.", day, "zoe_msg_secopincb_r2")
    $ _clear_initiative_pending("zoe")
    return

# Scene Tester presets and registry entries for this pack live in
# debug_scene_tester.rpy — gameplay files must not name, read or write the
# debug tester registry (invariant enforced by
# tests/location_beats_selfcheck.py section G, which greps for the symbol).
