# gameplay_expansion_scenes.rpy — 19 gameplay expansion scenes.
# Triggered via pending flags (set in new_day / thresholds / gift system);
# each scene clears its own pending + done flags on completion.
#
# Major scenes (set major_scene_last_day = day): nora_hug_school,
#   martha_corridor_gesture, eli_deploy_hug, lena_shoulder_gesture, car_marcus_drive.
# Minor scenes: all others.


# ── scene_nora_feels_ignored ───────────────────────────────────────────────────
# Fires at café when nora_ignored_pending is True (minor).
# Branches on nora_ignored_response set by phone reply.

label scene_nora_feels_ignored:
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal at sprite_r
    if nora_ignored_response == "honest":
        n "You actually showed up."
        "She's not warm, but she's not cold either."
        scene cg_nora_feels_ignored with dissolve
        show screen hud
        menu:
            "\"I said I would.\"":
                $ _apply_trust("nora", 3)
                n "Yeah. You did."
                "A pause. Something softens."
            "\"I'm here now. That has to count for something.\"":
                $ _apply_trust("nora", 2)
                n "It counts. I'm deciding how much."
    elif nora_ignored_response == "deflect":
        n "Busy week, you said."
        "She looks at you steadily."
        scene cg_nora_feels_ignored with dissolve
        show screen hud
        menu:
            "\"Honestly? Not great. Sorry for going quiet.\"":
                $ _apply_trust("nora", 2)
                n "That's what I thought."
                n "Next time just say so."
            "\"I'm fine. Just needed space.\"":
                $ _apply_trust("nora", 1)
                n "Okay."
                "She doesn't sound convinced."
    elif nora_ignored_response == "sorry":
        n "You apologized. By text."
        "She's not angry. She's measuring."
        scene cg_nora_feels_ignored with dissolve
        show screen hud
        menu:
            "\"I did mean it.\"":
                $ _apply_trust("nora", 3)
                n "Yeah. I know."
                "A beat. She pours you something."
            "\"Then you tell me what you think.\"":
                $ _apply_trust("nora", 2)
                n "I think you were in your head. I think that happens. I think you could have told me."
    else:
        # No reply at all
        n "You didn't reply."
        "She says it plainly. Not an accusation."
        scene cg_nora_feels_ignored with dissolve
        show screen hud
        menu:
            "\"I know. I'm sorry.\"":
                $ _apply_trust("nora", 2)
                n "Okay. Don't do it again."
            "[[Say nothing. Just sit down.]]":
                $ _apply_trust("nora", 1)
                "She watches you for a moment. Then goes back to work."
    hide nora_cafe_normal
    scene expression cafe_bg()
    show screen hud
    $ nora_ignored_done = True
    $ nora_ignored_pending = False
    $ nora_ignored_response = ""
    $ add_relationship_memory("nora", "nora_ignored_repair", "Named the distance")
    return


# ── scene_marcus_missed_commitment ────────────────────────────────────────────
# Fires at park or bar when marcus_missed_pending is set (minor conflict).
# marcus_missed_pending is a dict: {trigger_day, commitment_id, title, location, hour, variant}.

label scene_marcus_missed_commitment:
    $ _mc_bg = "bar" if current_loc == "location_bar" else "parkday"
    $ _mc_days = day - marcus_missed_pending["trigger_day"] if marcus_missed_pending else 0
    $ _mc_title = marcus_missed_pending["title"] if marcus_missed_pending else "our plans"
    $ _missed_loc = marcus_missed_pending.get("location", "there") if marcus_missed_pending else "there"
    $ _missed_title = marcus_missed_pending.get("title", "our plans") if marcus_missed_pending else "our plans"
    scene expression _mc_bg
    show screen hud
    show marcus_casual_normal at sprite_r
    if _mc_days <= 3:
        m "I was at [_missed_loc]. [_missed_title]. You didn't show."
        show marcus_casual_worried at sprite_r, react_nod
        "He says it flat. No performance."
    else:
        m "We still haven't talked about [_mc_title]."
        show marcus_casual_worried at sprite_r, react_nod
        "He doesn't look angry. Just direct."
    # cg_marcus_missed: close-up CG, neutral background — used for both park and bar staging.
    scene cg_marcus_missed with dissolve
    show screen hud
    menu:
        "\"You're right. I should have called.\"":
            $ _apply_trust("marcus", 2)
            m "Yeah. You should have."
            show marcus_casual_normal at sprite_r, react_nod
            m "But you're here now, so."
        "\"Something came up I couldn't move.\"":
            $ _apply_trust("marcus", -1)
            show marcus_casual_worried at sprite_r, react_shake
            m "There's always something. That's not the point."
            "He leaves it there."
        "[[Leave without saying anything.]]":
            $ _apply_trust("marcus", -2)
            $ _apply_aff("marcus", -1)
            "He watches you go. Doesn't call after you."
            hide marcus_casual_normal
            $ marcus_missed_done = True
            $ marcus_missed_pending = None
            return
    $ spend_time(0.5)
    hide marcus_casual_normal
    scene expression _mc_bg
    show screen hud
    $ marcus_missed_done = True
    $ marcus_missed_pending = None
    $ add_relationship_memory("marcus", "marcus_missed_repair", "Stood up and owned it")
    return


# ── scene_wardrobe_martha ─────────────────────────────────────────────────────
# Fires at office on first visit with wardrobe_tier >= 2 (minor, self-staging).

label scene_wardrobe_martha:
    scene goodoffice1
    show screen hud
    show martha_neutral at sprite_r
    "Martha passes your desk and slows, just slightly."
    ma "New wardrobe."
    "It's not a question."
    scene cg_wardrobe_martha with dissolve
    show screen hud
    menu:
        "\"You noticed.\"":
            $ _apply_aff("martha", 4)
            $ _apply_trust("martha", 2)
            ma "I notice most things. It reads well."
        "\"Just an update.\"":
            $ _apply_aff("martha", 2)
            $ _apply_trust("martha", 1)
            ma "A considered one. Good."
        "\"Was the old one that bad?\"":
            $ _apply_aff("martha", 3)
            ma "It was fine. This is better."
        "[[Say nothing. Hold her gaze.]]":
            $ _apply_aff("martha", 1)
            ma "..."
            "A half-nod. She keeps walking."
    $ spend_time(0.25)
    hide martha_neutral
    scene goodoffice1
    show screen hud
    $ martha_wardrobe_done = True
    return


# ── scene_guitar_zoe_busking ──────────────────────────────────────────────────
# Player-initiated from park menu (Thu/Fri, 14-17, skill_music >= 3, minor).

label scene_guitar_zoe_busking:
    scene parkday
    show screen hud
    show zoe_street_neutral at sprite_r
    "You pull out the guitar. Zoe looks up from her sketchbook."
    z "I didn't know you actually played."
    "You start. She doesn't go back to the sketchbook."
    scene cg_zoe_guitar with dissolve
    show screen hud
    menu:
        "Keep playing. Don't perform — just play.":
            $ _apply_aff("zoe", 5)
            $ _apply_trust("zoe", 4)
            z "That was genuinely good."
            z "You've been hiding that."
            $ gain_skill("music", 5)
        "Stop and banter about it.":
            $ _apply_aff("zoe", 3)
            $ _apply_trust("zoe", 2)
            z "You stopped the good part to talk about it. Classic."
            "She's smiling though."
            $ gain_skill("music", 3)
        "Let her take the guitar.":
            "She hesitates — then takes it."
            "Whatever she plays is simple and deliberate. Not showing off. Showing you."
            z "Now you try that bit."
            $ _apply_aff("zoe", 4)
            $ _apply_trust("zoe", 3)
            $ gain_skill("music", 4)
    $ spend_time(2)
    hide zoe_street_neutral
    scene parkday
    show screen hud
    $ zoe_park_guitar_done = True
    $ add_relationship_memory("zoe", "zoe_hears_guitar", "Heard me play in the park")
    return


# ── scene_lena_hospital_break_room ────────────────────────────────────────────
# Player-initiated from hospital menu (12-14, not done, minor).

label scene_lena_hospital_break_room:
    scene expression ("hospital_break_room_day" if hour < 20 else "hospital_break_room")
    show screen hud
    show drlena_normal at sprite_r
    "You find her in the break room. Coffee going cold. She doesn't look up immediately."
    lena "Sit down."
    "She moves her coat off the other chair."
    lena "Quiet works too. You don't have to talk."
    menu:
        "Sit and say nothing for a while.":
            $ _apply_trust("lena", 3)
            $ _apply_aff("lena", 2)
            "The silence is comfortable. That says something."
        "\"How long have you been on?\"":
            lena "Sixteen hours."
            lena "Don't look at me like that. I'm fine."
            $ _apply_trust("lena", 2)
            $ _apply_aff("lena", 2)
    $ spend_time(0.5)
    hide drlena_normal
    scene expression ("hospital_break_room_day" if hour < 20 else "hospital_break_room")
    show screen hud
    $ lena_break_room_done = True
    $ add_relationship_memory("lena", "lena_break_room", "Found her on break")
    return


# ── scene_martha_office_coffee ────────────────────────────────────────────────
# Morning encounter (hour < 10) at office (minor, self-staging).

label scene_martha_office_coffee:
    scene nexus_coffee_machine
    show screen hud
    show martha_neutral at sprite_r
    "Martha is already at the machine when you come in. She doesn't look surprised."
    ma "You're early."
    "She pours a second cup without being asked."
    menu:
        "Take it. \"Thank you.\"":
            $ _apply_aff("martha", 2)
            $ _apply_trust("martha", 1)
            ma "Day starts better."
        "\"I didn't know you were in this early.\"":
            $ _apply_aff("martha", 2)
            ma "I'm always in this early. You're just noticing now."
    $ spend_time(0.25)
    hide martha_neutral
    scene nexus_coffee_machine
    show screen hud
    $ martha_coffee_machine_done = True
    return


# ── scene_nora_bad_day ────────────────────────────────────────────────────────
# Fires at home via commitment (nora_bad_day_1, hour >= 19).
# Nora is off-duty. No café sprite fallback — use casual or no sprite at all.

label scene_nora_bad_day:
    $ complete_commitment("nora_bad_day_1")
    $ _nora_bd_cg = "nora_bad_day_cheap" if apartment_tier == 1 else ("nora_bad_day_good" if apartment_tier == 2 else "nora_bad_day_rich")
    # Establishing shot — Nora arriving at the apartment
    scene expression _nora_bd_cg with dissolve
    show screen hud
    "She shows up at seven-fifteen with a paper bag and no fuss."
    # Transition to home bg for the conversation
    scene expression home_bg() with dissolve
    show screen hud
    # Off-duty Nora: casual sprite if available, no sprite otherwise (not café outfit)
    if renpy.loadable("images/characters/nora/nora_casual_neutral.png"):
        show nora_casual_normal at sprite_r
    n "I said bread. I meant it."
    "She puts it on the counter. Doesn't ask how you are."
    if own_coffee_machine and home_coffee_calibrated:
        n "You still have the machine on my settings?"
        "She's already checking."
        n "Good. That's something."
    menu:
        "\"I don't know where to start.\"":
            $ _apply_trust("nora", 3)
            $ _apply_aff("nora", 2)
            n "Then don't start. Just be here for a minute."
            "You sit. She makes herself at home in the kitchen."
        "\"How was your day?\"":
            n "Terrible. But I'm not here about my day."
            $ _apply_aff("nora", 3)
            $ _apply_trust("nora", 2)
        "[[Say nothing. Just let her in.]]":
            $ _apply_trust("nora", 5)
            $ _apply_aff("nora", 2)
            "She reads the room correctly and doesn't push."
    "Later. The bread is half-gone and the room feels different."
    "She doesn't say anything as she leaves. Just presses your arm briefly at the door."
    $ nora_touched_arm = True
    $ spend_time(1.5)
    if renpy.loadable("images/characters/nora/nora_casual_neutral.png"):
        hide nora_casual_normal
    scene expression home_bg()
    show screen hud
    $ nora_bad_day_done = True
    $ nora_bad_day_pending = False
    $ add_relationship_memory("nora", "nora_visits_bad_day", "She brought bread")
    return


# ── scene_kitchen_lena_extended ───────────────────────────────────────────────
# Continuation of home_dinner_scene_lena. Lena is still in work clothes.
# ponytail: drlena_normal is scrubs + neutral expression — she came from shift.
#   If a casual/off-duty Lena sprite is added later, swap this.

label scene_kitchen_lena_extended:
    $ _lena_ext_cg = None if apartment_tier == 1 else ("lena_dinner_good" if apartment_tier == 2 else "lena_dinner_rich")
    if _lena_ext_cg:
        scene expression _lena_ext_cg with dissolve
        show screen hud
    else:
        scene expression home_bg() with dissolve
        show screen hud
    show drlena_normal at sprite_r
    "She's still in scrubs — came straight from the hospital. She doesn't comment on it."
    "She doesn't move toward the door."
    lena "If you have something to drink, I'm not in any hurry."
    "You find something. She settles into the chair like she fits there."
    menu:
        "Open up about something.":
            $ _apply_trust("lena", 3)
            $ _apply_aff("lena", 2)
            lena "I didn't know that about you."
            lena "Thank you for saying it."
        "Ask about her.":
            lena "Me?"
            "A pause. Like she hasn't been asked recently."
            lena "I went into medicine because I thought I'd be good at it. I was right. That's not the same as it being easy."
            $ _apply_trust("lena", 3)
            $ _apply_aff("lena", 2)
    $ spend_time(1.0)
    hide drlena_normal
    scene expression home_bg()
    show screen hud
    $ kitchen_lena_extended_done = True
    $ add_relationship_memory("lena", "lena_dinner_extended", "She stayed after dinner")
    return


# ── scene_martha_corridor_gesture ─────────────────────────────────────────────
# Fires at office (9-18) when martha_corridor_pending is True (MAJOR).

label scene_martha_corridor_gesture:
    $ major_scene_last_day = day
    # ponytail: martha_corridor_context.source can differentiate origin in future.
    $ _corridor_src = martha_corridor_context.get("source", "relationship_threshold") if martha_corridor_context else "relationship_threshold"
    scene hallway
    show screen hud
    show martha_neutral at sprite_r
    "The corridor is empty. She's walking past when she stops."
    "Her hand rests on your shoulder — brief, deliberate, like a full stop."
    scene cg_martha_gesture with dissolve
    show screen hud
    "She doesn't explain it."
    menu:
        "Hold the moment. Don't speak.":
            $ _apply_trust("martha", 4)
            $ _apply_aff("martha", 3)
            "She nods once and keeps walking."
        "\"Was that—\"":
            $ _apply_trust("martha", 2)
            $ _apply_aff("martha", 2)
            ma "Don't."
            "She says it almost warmly."
    $ spend_time(0.25)
    hide martha_neutral
    scene hallway
    show screen hud
    $ martha_corridor_done = True
    $ martha_corridor_pending = False
    $ add_relationship_memory("martha", "martha_corridor_touch", "Corridor gesture")
    return


# ── scene_nora_hug_school ─────────────────────────────────────────────────────
# Fires at café when nora_hug_school_pending is True (MAJOR).
# ponytail: cg_nora_hug_school not yet generated — using café bg.

label scene_nora_hug_school:
    $ major_scene_last_day = day
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal at sprite_r
    "Nora looks different today. Not the tired-good kind. The actual kind."
    n "I said yes."
    "She says it like it cost her something."
    n "To the programme. The culinary one."
    menu:
        "\"I knew you would.\"":
            $ _apply_aff("nora", 4)
            n "Did you."
            n "Then you had more faith in me than I did."
        "\"That's huge. Really.\"":
            $ _apply_aff("nora", 5)
            n "Don't make it weird."
            "She's smiling too much for that to land."
    "She steps around the counter. The hug happens before either of you has thought about it."
    hide nora_cafe_normal
    scene cg_nora_hug_school    # CG: Nora hug at café
    show screen hud
    $ _hug_text = do_hug("nora")
    "[_hug_text]"
    $ spend_time(0.5)
    scene expression cafe_bg()    # return to café bg after CG
    show screen hud
    $ nora_hug_school_done = True
    $ nora_hug_school_pending = False
    $ add_relationship_memory("nora", "nora_school_hug", "She said yes to the program")
    $ nora_school_accepted_day = day
    $ nora_school_start_day = day + 14
    return


# ── scene_eli_deploy_hug ──────────────────────────────────────────────────────
# Fires at hub (hour >= 19) when eli_deploy_pending is True (MAJOR).

label scene_eli_deploy_hug:
    $ major_scene_last_day = day
    scene hub_pov
    show screen hud
    show eli_normal at sprite_r
    "Eli is standing over the dashboard. Something just went green."
    eli "It's live."
    "She says it like she can't believe it yet."
    scene cg_eli_deploy_hug with dissolve
    show screen hud
    "You lean over to look at the screen. Your shoulder meets hers."
    "A half-second of stillness."
    "Then Eli hugs you. Briefly, slightly surprised at herself."
    # Scene-initiated hug — Eli chose this. Don't re-run the consent gate (which
    # could return a rejection line and contradict the narration above).
    $ record_forced_hug("eli")
    $ spend_time(0.5)
    hide eli_normal
    scene hub_pov
    show screen hud
    $ eli_deploy_hug_done = True
    $ eli_deploy_pending = False
    $ add_relationship_memory("eli", "eli_deploy_moment", "The deploy went live")
    return


# ── scene_lena_shoulder_gesture ───────────────────────────────────────────────
# Fires at hospital when lena_shoulder_pending is True (MAJOR).

label scene_lena_shoulder_gesture:
    $ major_scene_last_day = day
    scene hospital1
    show screen hud
    show drlena_normal at sprite_r, react_lean_in
    "She finds you in the corridor. Doesn't say why."
    "She puts a hand on your shoulder. Steady, deliberate."
    scene cg_lena_shoulder with dissolve
    show screen hud
    "It stays for exactly as long as it needs to."
    "Then she's gone."
    $ _apply_trust("lena", 5)
    $ _apply_aff("lena", 2)
    $ spend_time(0.25)
    hide drlena_normal
    scene hospital1
    show screen hud
    $ lena_shoulder_done = True
    $ lena_shoulder_pending = False
    $ add_relationship_memory("lena", "lena_shoulder_gesture", "After the hard case")
    return


# ── scene_nora_kai_crossover ──────────────────────────────────────────────────
# Fires at café when nora_kai_pending is True (crossover, minor).

label scene_nora_kai_crossover:
    scene expression cafe_bg()
    show screen hud
    show kai_normal at sprite_l
    show nora_cafe_normal at sprite_r
    "Kai is at the counter when you arrive. Nora has her arms crossed."
    kai "All I'm saying is a flat white is just a latte with delusions."
    n "A flat white is a fundamentally different microfoam structure and you know that."
    scene cg_nora_kai with dissolve
    show screen hud
    kai "Nobody can taste the difference."
    n "I can taste the difference."
    menu:
        "Side with Nora. \"The microfoam matters.\"":
            $ _apply_aff("nora", 3)
            $ _apply_aff("kai", -1)
            n "Thank you. Finally."
            kai "Outnumbered. Unfair."
        "Side with Kai. \"It's mostly vibes.\"":
            $ _apply_aff("kai", 3)
            $ _apply_aff("nora", -1)
            kai "There it is. Someone sensible."
            n "You're both wrong and I will explain why."
        "\"You're both right, depending on the cup.\"":
            $ _apply_aff("nora", 2)
            $ _apply_aff("kai", 2)
            "A pause. They look at each other."
            kai "That's annoyingly diplomatic."
            n "It's also correct."
    $ spend_time(1.0)
    hide kai_normal
    hide nora_cafe_normal
    scene expression cafe_bg()
    show screen hud
    $ nora_kai_crossover_done = True
    $ nora_kai_pending = False
    $ nora_kai_pending_day = -1
    return


# ── scene_eli_meets_zoe ───────────────────────────────────────────────────────
# Player-initiated from hub menu (minor, self-staging).

label scene_eli_meets_zoe:
    scene hub_pov
    show screen hud
    show eli_normal at sprite_r
    show zoe_street_neutral at sprite_l
    "You'd wondered what would happen if they were in the same room."
    "Within three minutes they're arguing about generative art like they've met before."
    scene cg_eli_zoe_collab with dissolve
    show screen hud
    eli "The output isn't art — the constraint system is."
    z "That's the most IT-person take on art I've ever heard."
    eli "It's also correct."
    menu:
        "Let them run. Stay quiet.":
            $ _apply_aff("eli", 2)
            $ _apply_aff("zoe", 2)
            "By the end they've exchanged contacts without you suggesting it."
        "\"You're both describing the same thing from different angles.\"":
            $ _apply_aff("eli", 2)
            $ _apply_aff("zoe", 2)
            "A pause. They look at each other."
            z "...maybe."
            eli "Possibly."
    $ spend_time(2.0)
    hide eli_normal
    hide zoe_street_neutral
    scene hub_pov
    show screen hud
    $ eli_meets_zoe_done = True
    $ add_relationship_memory("eli", "eli_meets_zoe", "Met Zoe")
    $ add_relationship_memory("zoe", "zoe_meets_eli", "Met Eli")
    return


# ── scene_car_marcus_drive ────────────────────────────────────────────────────
# Fires at bar (hour >= 22, car_tier >= 1) — late night drive (MAJOR).
# Three images: car_interior_night (neutral bg), car_interior_pov (driving),
# car_marcus_night (Marcus focus). No sprites over car images.

label scene_car_marcus_drive:
    $ major_scene_last_day = day
    scene car_interior_night    # bg: establishing — empty car interior, night
    show screen hud
    "He sees the car."
    m "This yours?"
    "You tell him it is."
    m "Alright. I'll let you drive me home."
    "He says it like he's doing you a favour."
    scene car_interior_pov      # bg: player POV — steering wheel, road ahead
    show screen hud             # no sprite overlay — pov IS the camera
    "You pull away from the bar. The city slides past the windows."
    "Marcus shifts in the passenger seat."
    menu:
        "Drive in silence. Let the city go by.":
            scene car_marcus_night  # CG: Marcus in passenger seat — image IS Marcus
            show screen hud         # ponytail: do not add sprite_r on top of car_marcus_night
            m "Good night for it."
            $ _apply_aff("marcus", 3)
            $ _apply_trust("marcus", 2)
            "He doesn't say anything else. That's enough."
        "Put something on.":
            scene car_marcus_night  # CG: Marcus in passenger seat
            show screen hud
            m "I know this one."
            "He doesn't sing along. Just nods."
            $ _apply_aff("marcus", 3)
            $ _apply_trust("marcus", 2)
        "\"You good?\"":
            scene car_marcus_night  # CG: Marcus in passenger seat
            show screen hud
            m "Tonight? Yeah."
            "He pauses."
            m "Some nights aren't. But tonight's fine."
            $ _apply_trust("marcus", 3)
            $ _apply_aff("marcus", 2)
    scene car_interior_night with dissolve  # return to neutral establishing bg
    show screen hud
    $ spend_time(0.5)
    $ car_marcus_drive_done = True
    $ add_relationship_memory("marcus", "marcus_night_drive", "Late night drive")
    return


# ── scene_martha_gift_accusation ─────────────────────────────────────────────
# Fires at office (9-18) when martha_gift_scene_pending is set (minor conflict).
# martha_gift_scene_pending is a dict: {trigger_day, gift_id, gift_name, gift_count, trigger_location, variant}.

label scene_martha_gift_accusation:
    $ _gift_days = day - martha_gift_scene_pending["trigger_day"] if martha_gift_scene_pending else 0
    $ _gift_name = martha_gift_scene_pending.get("gift_name", "the gift") if martha_gift_scene_pending else "the gift"
    $ _gift_count = martha_gift_scene_pending.get("gift_count", 2) if martha_gift_scene_pending else 2
    scene goodoffice1
    show screen hud
    show martha_neutral at sprite_r
    "She closes the door behind her."
    if _gift_days <= 3:
        ma "I want to ask you something directly."
    else:
        ma "I've been meaning to bring something up."
    scene cg_martha_gift with dissolve
    show screen hud
    ma "[_gift_name]. And the ones before it."
    "She's not angry. She's precise."
    ma "Why?"
    menu:
        "\"Because I wanted to. No agenda.\"":
            $ _apply_trust("martha", 3)
            ma "Good."
            ma "I can work with that."
        "\"I thought it was appropriate given the working relationship.\"":
            $ _apply_trust("martha", -1)
            ma "It's borderline. Be careful."
            "She doesn't sound offended. Just honest."
        "\"You're impressive. I notice impressive people.\"":
            $ _apply_trust("martha", -2)
            ma "I see."
            "A long pause."
            ma "Don't let flattery become a tool, [mc_name]. It's a short-run strategy."
    $ spend_time(0.25)
    hide martha_neutral
    scene goodoffice1
    show screen hud
    $ martha_gift_accusation_done = True
    $ martha_gift_scene_pending = None
    return


# ── scene_programming_kit_eli ─────────────────────────────────────────────────
# Player-initiated from hub menu (hour >= 17, own_programming_kit, minor).

label scene_programming_kit_eli:
    scene hub_pov
    show screen hud
    show eli_normal at sprite_r
    "Eli pulls out a breadboard. Half a circuit, some ambition."
    eli "I need a second pair of eyes. This is the prototype."
    scene cg_eli_hardware with dissolve
    show screen hud
    if skill_prog >= 5:
        "You see the issue in the first pass. Clean fix."
        eli "That was faster than I expected."
        eli "Write up what you found. I want it in the docs."
        $ _apply_trust("eli", 3)
        $ _apply_aff("eli", 2)
        $ gain_skill("prog", 5)
    elif skill_prog >= 3:
        "You work through it together. Two hours, one working prototype."
        eli "Not bad. You've got good instincts."
        $ _apply_trust("eli", 3)
        $ _apply_aff("eli", 2)
        $ gain_skill("prog", 3)
    else:
        "It takes longer than either of you expected. But you stay with it."
        eli "You're patient. That's actually half the job."
        $ _apply_trust("eli", 2)
        $ _apply_aff("eli", 2)
        $ gain_skill("prog", 3)
    $ spend_time(2.0)
    hide eli_normal
    scene hub_pov
    show screen hud
    $ programming_kit_eli_done = True
    $ add_relationship_memory("eli", "eli_open_source_hardware", "Hardware test session")
    return


# ── scene_zoe_rain_shelter ────────────────────────────────────────────────────
# Auto-triggers at location_park on Thu/Fri 14-18 when zoe_affection >= 15 (minor).

label scene_zoe_rain_shelter:
    scene parkday_rain    # bg: rain variant of the park
    show screen hud
    show zoe_street_neutral at sprite_r
    "The sky changes faster than it should. You make it to the park shelter just ahead of it."
    "Zoe is already there. Her sketchbook is still in her bag, untouched. She has charcoal in one hand."
    z "Every park has exactly one good rain shelter. I've been here eight months and this is the first time I've actually used this one."
    menu:
        "\"Good shelter.\"":
            z "Best in the park. I've evaluated all of them."
            "She takes out the sketchbook. Starts working."
        "[[Lean against the post. Don't say anything.]]":
            "She glances. Goes back to drawing. After a beat:"
            z "You don't mind rain."
            menu:
                "\"Not particularly.\"":
                    $ _apply_trust("zoe", 1)
                "\"I've seen worse.\"":
                    $ _apply_trust("zoe", 1)
        "\"Are you actually going to sketch in the rain?\"":
            z "The rain is from over there. I'm standing over here."
            "She draws it — the angle, the dry arc."
            $ _apply_aff("zoe", 1)
    "She works. You stand and watch the park go blurred. There's nowhere to be."
    "After a while she tilts the sketchbook toward you without being asked. The park, in lines, rain trails, a suggestion of the city behind the trees."
    menu:
        "\"It's the rain, but as lines.\"":
            z "Yes. Exactly."
            $ _apply_aff("zoe", 3)
        "\"The park in a different light.\"":
            z "Roughly."
            "She takes it back."
            $ _apply_aff("zoe", 2)
        "[[Say nothing. Just look at it.]]":
            "She watches your face while you look. Then takes it back. \"Enough.\""
            $ _apply_trust("zoe", 2)
        "\"I don't know what to call it.\"":
            z "That's fine. Not everything needs a label."
            $ _apply_trust("zoe", 1)
    "The rain slows. Zoe taps the finished sketch twice."
    menu:
        "[[Leave first.]]":
            z "Good rain."
        "[[Wait for her to leave.]]":
            z "You know where the shelter is now."
            "She goes. Brief smile."
    $ spend_time(1.0)
    hide zoe_street_neutral
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    $ zoe_rain_done = True
    $ add_relationship_memory("zoe", "zoe_rain_shelter", "Rain shelter in the park")
    return


# ── scene_zoe_spontaneous ─────────────────────────────────────────────────────
# Pending: triggers at location_nightclub when hour >= 21 (MAJOR).
# ponytail: CG shows the moment before her retreat — no sprite overlay on top.

label scene_zoe_spontaneous:
    $ major_scene_last_day = day
    scene nightclub    # bg: nightclub
    show screen hud
    show zoe_street_neutral at sprite_r, react_lean_in
    "They've been in the corner for the last hour. Zoe has been good company — the kind where you don't notice time."
    "She says something. Not loud enough to be a statement, but specific."
    if zoe_rain_done:
        z "I keep finding you in the right places."
    else:
        z "I usually get bored. I haven't."
    "She's closer than she usually is. She's looking at you differently."
    "Then something resets."
    "She looks at her drink. \"Anyway.\" She gestures at the room. \"I should—\""
    "She doesn't finish the sentence."
    hide zoe_street_neutral
    scene nightclub
    show screen hud
    menu:
        "\"You don't have to do that.\"":
            # Romantic direction — call the deflection out directly
            scene cg_zoe_almost
            show screen hud
            scene nightclub
            show screen hud
            show zoe_street_neutral at sprite_r
            z "Do what?"
            "\"The thing where you walk it back.\""
            "Long pause. She's working out whether to be annoyed or impressed."
            show zoe_street_talk at sprite_r
            z "I wasn't walking anything back."
            show zoe_street_smile at sprite_r, react_bounce
            "\"I know.\""
            "She looks at you for a long moment. The nightclub keeps going around both of you."
            show zoe_street_neutral at sprite_r, react_nod
            z "Okay."
            "Just that. But she doesn't change the subject."
            if get_romance_state("zoe") in ("unopened", "friends"):
                $ set_romance_state("zoe", "interested", source="scene_zoe_spontaneous")
                $ add_romance_momentum("zoe", 15)
                $ add_relationship_memory("zoe", "zoe_spontaneous_direction_romance", "Called her deflection at the nightclub")
            $ _apply_trust("zoe", 3)
            $ _apply_aff("zoe", 4)
        "[Say what she said, once, quietly. Then change the subject yourself.]":
            # Platonic close-friend direction — mirror her, then close the moment on your terms
            scene nightclub
            show screen hud
            show zoe_street_smile at sprite_r, react_bounce
            "She actually smiles. Not the careful one."
            "You change the subject. She lets you. Properly lets you — like it was agreed."
            if get_romance_state("zoe") in ("unopened", "friends"):
                $ set_romance_state("zoe", "friends", source="scene_zoe_spontaneous")
                $ add_romance_momentum("zoe", 5)
                $ add_relationship_memory("zoe", "zoe_spontaneous_direction_platonic", "Mirrored her and closed the moment together")
            $ _apply_aff("zoe", 4)
            $ _apply_trust("zoe", 3)
        "[Let her redirect. Talk about something else.]":
            # Withdrawal — give her the exit she was already reaching for
            scene nightclub
            show screen hud
            show zoe_street_neutral at sprite_r, react_sigh
            "She visibly relaxes. The cover works."
            "She glances at you once — brief — before the conversation shifts."
            $ add_romance_momentum("zoe", 2)
            $ _apply_trust("zoe", 2)
    hide zoe_street_neutral
    scene nightclub
    show screen hud
    "Later, separating:"
    z "See you."
    "She doesn't say anything else. She never does after one of these."
    $ spend_time(1.0)
    $ zoe_moment_deflected_done = True
    $ zoe_moment_deflected_pending = False
    $ add_relationship_memory("zoe", "zoe_almost_moment", "The moment at the nightclub")
    return


# ── scene_nora_romance_reopen ─────────────────────────────────────────────────
# Triggered after player chose platonic/withdrawal at nora_closing_scene and
# momentum later crosses threshold. Nora references the prior choice explicitly.
label scene_nora_romance_reopen:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    $ _nora_prior_state = get_romance_state("nora")
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal at sprite_r
    "It's quieter than usual. Last customer left ten minutes ago."
    "She's wiping down the counter. Not rushing."
    n "You said next week. I wasn't sure what you meant by that."
    if _nora_prior_state == "friends":
        n "The 'same time next week' version. The regular version."
    else:
        n "Or maybe you didn't mean anything. You walked off before I could ask."
    "You consider your answer."
    menu:
        "\"I meant something different. I think you know that.\"" if nora_affection >= 50 and nora_trust >= 45:
            show nora_cafe_laugh at sprite_r
            n "Yeah. I know."
            "A beat. Then she sets the cloth down."
            n "Same time. Somewhere different. Deal?"
            $ set_romance_state("nora", "interested", source="scene_nora_romance_reopen")
            $ add_romance_momentum("nora", 20)
            $ add_relationship_memory("nora", "nora_reopen_romance", "Cleared the ambiguity after the closing scene")
            $ _apply_trust("nora", 3)
            $ _apply_aff("nora", 4)
        "\"Same time, same place. I like the coffee.\"":
            n "That's a terrible reason."
            n "But okay."
            $ set_romance_state("nora", "friends", source="scene_nora_romance_reopen")
            $ add_romance_momentum("nora", 8)
            $ add_relationship_memory("nora", "nora_reopen_platonic", "Settled back into regulars after ambiguity")
            $ _apply_aff("nora", 2)
        "[Change the subject. Let it stay ambiguous.]":
            "She lets you change it."
            "But she watches you leave."
            $ add_romance_momentum("nora", 5)
            $ _apply_trust("nora", 1)
    hide nora_cafe_normal
    hide nora_cafe_laugh
    $ nora_reopen_done = True
    $ spend_time(0.5)
    return


# ── scene_zoe_romance_reopen ──────────────────────────────────────────────────
# Triggered after player chose platonic/withdrawal at scene_zoe_spontaneous and
# momentum later crosses threshold.
label scene_zoe_romance_reopen:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    $ _zoe_prior_state = get_romance_state("zoe")
    scene nightclub
    show screen hud
    show zoe_street_neutral at sprite_r
    "She finds you at the bar. Leans against it instead of sitting."
    z "So are we still pretending that moment didn't happen?"
    if _zoe_prior_state == "friends":
        z "You mirrored me. Neat move. But it was still a moment."
    else:
        z "You gave me the exit. I used it. That's not the same as it not existing."
    menu:
        "\"No. We're not.\"" if zoe_affection >= 50 and zoe_trust >= 45:
            z "Okay. Good."
            "She doesn't make it bigger than that. But she doesn't move away either."
            $ set_romance_state("zoe", "interested", source="scene_zoe_romance_reopen")
            $ add_romance_momentum("zoe", 20)
            $ add_relationship_memory("zoe", "zoe_reopen_romance", "Stopped pretending after the nightclub moment")
            $ _apply_trust("zoe", 3)
            $ _apply_aff("zoe", 4)
        "\"I think we handled it fine.\"":
            z "That's a very diplomatic answer."
            "She almost smiles."
            $ set_romance_state("zoe", "friends", source="scene_zoe_romance_reopen")
            $ add_romance_momentum("zoe", 8)
            $ add_relationship_memory("zoe", "zoe_reopen_platonic", "Agreed it was handled — closed the loop")
            $ _apply_aff("zoe", 2)
        "[Shrug. Order another drink.]":
            "She watches you for a second."
            z "Fair enough."
            "She orders the same."
            $ add_romance_momentum("zoe", 5)
            $ _apply_trust("zoe", 1)
    hide zoe_street_neutral
    $ zoe_reopen_done = True
    $ spend_time(1.0)
    return


# ── scene_martha_romance_reopen ───────────────────────────────────────────────
# Triggered after player chose platonic/withdrawal at martha_rooftop_scene and
# momentum later crosses threshold.
label scene_martha_romance_reopen:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    $ _martha_prior_state = get_romance_state("martha")
    scene bar
    show screen hud
    show martha_dress_normal at sprite_r
    "She's already at the table when you arrive. Two glasses, not one."
    ma "Your behaviour since that conversation has been inconsistent with your answer."
    "No preamble. That's Martha."
    if _martha_prior_state == "friends":
        ma "You said same time, same quarter. Then you rearranged twice and showed up early both times."
    else:
        ma "You didn't say anything. Then you've been — attentive. More than professionally necessary."
    "You sit down."
    menu:
        "\"You're right. My answer was incomplete.\"" if martha_affection >= 65 and martha_trust >= 60:
            "Something shifts in her posture. Not much. Enough."
            ma "I appreciate the correction."
            "She lifts her glass. A small gesture. An acknowledgement."
            $ set_romance_state("martha", "interested", source="scene_martha_romance_reopen")
            $ add_romance_momentum("martha", 20)
            $ add_relationship_memory("martha", "martha_reopen_romance", "Corrected the rooftop answer in the bar")
            $ _apply_trust("martha", 4)
            $ _apply_aff("martha", 4)
        "\"I've been consistent. You're reading into it.\"":
            "Long pause."
            ma "Perhaps."
            "She doesn't sound convinced, but she accepts it."
            $ set_romance_state("martha", "friends", source="scene_martha_romance_reopen")
            $ add_romance_momentum("martha", 8)
            $ add_relationship_memory("martha", "martha_reopen_platonic", "Held the professional frame after the rooftop")
            $ _apply_aff("martha", 2)
        "[Let the silence sit. See what she does with it.]":
            "She lets it sit too."
            "Eventually she moves on to the agenda."
            "But she poured two glasses."
            $ add_romance_momentum("martha", 6)
            $ _apply_trust("martha", 2)
    hide martha_dress_normal
    $ martha_reopen_done = True
    $ spend_time(1.0)
    return


# ══ Romance-opening scenes (Caroline / Lena / Elle) ═══════════════════════════
# These NPCs have romance profiles + kiss content but, unlike Nora/Zoe/Martha,
# had no scene that ever set state to "interested" — so the kiss was unreachable.
# Each fires once, at the NPC's venue, after their closeness scene and once aff/
# trust clear the profile's opening thresholds. The romantic option opens romance
# ("interested"); the platonic option settles to "friends" (still reopenable later
# via the can_offer_romance_reopen path). Mirrors nora_closing_scene's structure.

label scene_caroline_romance_open:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    scene bar
    show screen hud
    show caroline_normal at sprite_r
    "She's at the same corner table. She doesn't look surprised to see you — she rarely does."
    caro "You keep turning up where I am. I've stopped calling it coincidence."
    "She turns the glass a quarter-turn on the table. Precise, like everything she does."
    caro "So. Are we colleagues who happen to drink in the same places, or is this something you're doing on purpose?"
    "It isn't a trap. It's a genuine question, asked the way she asks everything — as if the answer is data she intends to use."
    menu:
        "\"On purpose. I think you already knew that.\"" if caroline_affection >= 65 and caroline_trust >= 60:
            caro "I suspected. I don't act on suspicion."
            "A pause. Then, evenly:"
            caro "Now I have confirmation. That changes the calculation."
            "She doesn't smile, exactly. But something in her posture opens by a degree."
            $ set_romance_state("caroline", "interested", source="scene_caroline_romance_open")
            $ add_romance_momentum("caroline", 20)
            $ add_relationship_memory("caroline", "caroline_romance_open", "Told her it was on purpose")
            $ _apply_trust("caroline", 4)
            $ _apply_aff("caroline", 4)
        "\"Colleagues who drink well. Nothing more.\"":
            caro "Sensible. Probably correct."
            "She accepts it without visible disappointment. Whether that's genuine or discipline, you can't tell."
            $ set_romance_state("caroline", "friends", source="scene_caroline_romance_open")
            $ add_romance_momentum("caroline", 6)
            $ add_relationship_memory("caroline", "caroline_romance_declined", "Kept it to colleagues")
            $ _apply_aff("caroline", 2)
        "[Let the question hang. Order a drink instead.]":
            "You signal the bartender rather than answer."
            caro "That's an answer too. Just a slower one."
            $ add_romance_momentum("caroline", 4)
            $ _apply_trust("caroline", 1)
    hide caroline_normal
    $ caroline_romance_open_done = True
    $ spend_time(1.0)
    return


label scene_lena_romance_open:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    scene bar
    show screen hud
    show drlena_normal at sprite_r
    "She's off shift — you can tell because she's not scanning the room for the next emergency."
    lena "Can I ask you something without it turning weird?"
    "She doesn't wait long for permission. She's decided to say it either way."
    lena "I look forward to this. Whatever this is. I wanted to know if I'm the only one holding it that way."
    menu:
        "\"You're not. I've been holding it the same way.\"" if lena_affection >= 55 and lena_trust >= 55:
            "She lets out a breath she was clearly holding."
            lena "Okay. Good. Then I'm glad I said it."
            "She's steady again almost at once — but warmer now, like a decision has been filed and she's at peace with it."
            $ set_romance_state("lena", "interested", source="scene_lena_romance_open")
            $ add_romance_momentum("lena", 20)
            $ add_relationship_memory("lena", "lena_romance_open", "Said it back, at the bar")
            $ _apply_trust("lena", 4)
            $ _apply_aff("lena", 4)
        "\"I value this. As a friendship.\"":
            lena "That's — yes. That's a good thing to be clear about."
            "If there's a flicker of something else, she folds it away with the same care she gives everything."
            $ set_romance_state("lena", "friends", source="scene_lena_romance_open")
            $ add_romance_momentum("lena", 6)
            $ add_relationship_memory("lena", "lena_romance_declined", "Named it as friendship")
            $ _apply_aff("lena", 2)
        "[Answer honestly, but don't commit.]":
            "You give her something true and incomplete."
            lena "That's fair. I asked a big question at a small table."
            $ add_romance_momentum("lena", 4)
            $ _apply_trust("lena", 2)
    hide drlena_normal
    $ lena_romance_open_done = True
    $ spend_time(1.0)
    return


label scene_elle_romance_open:
    $ major_scene_last_day = day   # one major scene per day — no same-visit chaining
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    show elle_sundress_normal at sprite_r
    "She's got her feet in the sand and her eyes on the water, the way she is when she's decided to stop performing for a bit."
    el "Can I say a thing? And you don't have to match it, I just want it out loud."
    "She glances over, half a laugh already in her voice, covering for the fact that she means it."
    el "I like when it's you. More than the beach-friends version. I've been sitting on that for a while."
    menu:
        "\"Then let's not do the beach-friends version.\"" if elle_affection >= 40 and elle_trust >= 35:
            show elle_sundress_normal at sprite_r
            "She grins, properly this time, and looks back at the water like she needs a second."
            el "Okay. Okay, good. I was ninety percent sure and ten percent about to feel very silly."
            $ set_romance_state("elle", "interested", source="scene_elle_romance_open")
            $ add_romance_momentum("elle", 20)
            $ add_relationship_memory("elle", "elle_romance_open", "Said it back on the beach")
            $ _apply_trust("elle", 4)
            $ _apply_aff("elle", 4)
        "\"I like the beach-friends version. A lot.\"":
            el "Yeah? Good. That's — yeah, that works too."
            "She means it, mostly. She's good at meaning things mostly."
            $ set_romance_state("elle", "friends", source="scene_elle_romance_open")
            $ add_romance_momentum("elle", 6)
            $ add_relationship_memory("elle", "elle_romance_declined", "Kept it to beach friends")
            $ _apply_aff("elle", 2)
        "[Smile. Let the water fill the gap.]":
            "You don't answer with words. She lets it go, but she noticed you didn't say no."
            $ add_romance_momentum("elle", 4)
            $ _apply_trust("elle", 1)
    hide elle_sundress_normal
    $ elle_romance_open_done = True
    $ spend_time(1.0)
    return


# ════ CONTENT PACK 2 ══════════════════════════════════════════════════════════


# ── scene_caroline_thursday_bar ───────────────────────────────────────────────
# Fires at location_bar on Thursday 19-22 when caroline_bar_pending is True.
# Caroline has no bar schedule — her presence here is intentional: she invited
# herself to an off-site drink after a long project week.
# No CG (the dissonance of seeing her out of context is the point).

label scene_caroline_thursday_bar:
    $ major_scene_last_day = day   # counts as the day's major scene (blocks same-visit chaining into romance-open)
    scene bar
    show screen hud
    show caroline_normal at sprite_r
    "The bar is mid-evening loud. You spot Caroline at a corner table — a glass of something pale in front of her, phone face-down."
    "She's still in work clothes. The formal blazer looks slightly incongruous here, out of its element. So does she, except that she doesn't seem to mind."
    "She sees you immediately. She doesn't pretend she didn't."
    caro "Well. If you need a seat, there's one."
    "She does not wave you over. She simply states the fact."
    "You sit. She takes a slow drink. Something about the way she holds the glass suggests the day is finished and she's decided to be done with it."
    caro "It ends the same every week. I keep thinking it won't."
    "She's not complaining. Just reporting."
    "Then, without preamble, she asks you something — something specific and personal. Something you mentioned in passing weeks ago that you hadn't expected her to file."
    caro "How is it going? The thing you said you were working on."
    menu:
        "Answer honestly.":
            $ _apply_trust("caroline", 3)
            caro "That's what I thought."
            "She picks up her drink. Doesn't explain what she thought."
        "Deflect with something light.":
            $ _apply_aff("caroline", 2)
            caro "Sensible."
            "She seems to find this genuinely acceptable."
        "[Say nothing for a moment.]":
            $ _apply_trust("caroline", 2)
            $ _apply_aff("caroline", 1)
            "She nods once. Moves on."
    "She finishes her drink. Stands."
    caro "I'm not in the habit of running into colleagues after hours."
    "A pause."
    caro "But this was fine."
    "She leaves without looking back. You're left with the faint unsettling sense that Caroline noticed more than she ever said."
    $ spend_time(1.0)
    $ _apply_aff("caroline", 2)
    $ caroline_bar_done = True
    $ caroline_bar_pending = False
    $ caroline_bar_pending_day = -1
    hide caroline_normal
    return


# ── scene_natalie_bar_offduty ─────────────────────────────────────────────────
# Fires at location_bar on weekend (Sat-Sun) when natalie_bar_scene_pending is True
# and npc_here("natalie") returns True (Sat-Sun 17-21 per schedule).
# No CG.

label scene_natalie_bar_offduty:
    $ major_scene_last_day = day   # counts as the day's major scene (blocks same-visit chaining into romance-reopen)
    scene bar
    show screen hud
    show natalie_normal at sprite_r
    "Natalie is at the bar not doing anything. Drink in front of her, not talking to anyone, watching the room with the same flat attention she uses on the warehouse floor."
    "You sit down. She makes room without ceremony, without greeting."
    "The silence that follows doesn't bother her. She finishes a thought, drinks, starts another."
    nat "I coach three nights a week. Muay Thai. The gym two streets from the warehouse."
    "She says it the same way she'd say she takes the metro. A fact, not an offer. You're probably the first person from the warehouse who's ever seen this version of her."
    "She looks at you for a moment. The same direct look she uses when she's about to say something she's been thinking about for a while."
    menu:
        "Ask who she trains.":
            $ _apply_aff("natalie", 2)
            nat "Kids, mostly. Some adults who think they're tougher than they are."
            "She almost smiles."
            nat "The kids figure it out faster."
        "Ask why she coaches when she already works the longest hours on the floor.":
            $ _apply_trust("natalie", 3)
            nat "Because hauling freight pays the rent. This is the part that's actually mine."
            "A pause. She doesn't add anything to that."
        "[Don't ask. Just listen to whatever she says next.]":
            $ _apply_trust("natalie", 2)
            $ _apply_aff("natalie", 1)
            "She takes a slow drink."
            nat "The warehouse pays the bills. This is the part that stays."
    "She finishes her drink before you do. Stands."
    nat "Same time next weekend, if you end up here."
    "Not an invitation. An observation about what will probably happen."
    "She goes."
    $ spend_time(1.0)
    $ _apply_aff("natalie", 2)
    $ _apply_trust("natalie", 2)
    $ natalie_bar_scene_done = True
    $ natalie_bar_scene_pending = False
    $ natalie_bar_scene_pending_day = -1
    $ add_relationship_memory("natalie", "natalie_muaythai_revealed", "Off the clock — Muay Thai coach")
    hide natalie_normal
    return


# ── scene_kai_cafe_quiet ──────────────────────────────────────────────────────
# Fires at location_cafe on Tue/Thu 10-14 when kai_cafe_quiet_pending is True
# and not nora_kai_pending. Uses kai_normal (non-gym sprite) + cafeday bg.
# No CG.

label scene_kai_cafe_quiet:
    scene expression cafe_bg()
    show screen hud
    show kai_normal at sprite_r
    if npc_here("nora"):
        show nora_cafe_normal at sprite_l
    "Kai is at the counter, coffee in hand, not in gym clothes. She's looking at her phone but not really reading it."
    "Nora serves her without asking what she wants — regulars tab."
    "When you sit down, Kai puts the phone away instead of looking up. Like she was waiting for the distraction."
    "After a while she says:"
    kai "Everyone wants the energy all the time. Like if I have a flat day, I'm failing them."
    "Not a complaint. More like she's noticing the thing for the first time by saying it out loud."
    menu:
        "\"That sounds exhausting.\"":
            $ _apply_trust("kai", 3)
            kai "It's just part of it."
            "A pause."
            kai "But yeah. Sometimes."
        "\"You don't have to be the energy.\"":
            $ _apply_aff("kai", 3)
            kai "People pay for a session and they want..."
            "She stops. Considers."
            kai "I know. I know that. I just forget it sometimes."
        "[Say nothing. Let her sit with it for a second.]":
            $ _apply_trust("kai", 2)
            $ _apply_aff("kai", 2)
            "She drinks her coffee. The silence doesn't bother her."
            kai "See, this is the part nobody tells you about."
    "She finishes the coffee. Back to herself — or close enough to the version she usually shows."
    kai "Same time Thursday?"
    "It's her slot anyway. The offer to share it is new."
    $ spend_time(0.5)
    $ _apply_aff("kai", 2)
    $ _apply_trust("kai", 2)
    $ kai_cafe_quiet_done = True
    $ kai_cafe_quiet_pending = False
    $ kai_cafe_quiet_pending_day = -1
    $ add_relationship_memory("kai", "kai_cafe_quiet", "Between sets — the quiet version")
    hide kai_normal
    if npc_here("nora"):
        hide nora_cafe_normal
    return


# ── scene_elle_portugal_payoff ────────────────────────────────────────────────
# Fires at location_beach (or location_sandbeach) when elle_decision_pending is True
# and npc_talkable("elle") returns True.
# CG: cg_elle_portugal_turn (at emotional peak, then return to sprite).
# Branches on elle_travel_2_response stored during arc_elle_travel_2.

label scene_elle_portugal_payoff:
    $ major_scene_last_day = day   # counts as the day's major scene (blocks same-visit chaining into romance-open)
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    show elle_sundress_normal at sprite_r
    "Elle is at the waterline, shoes off. The same posture as always — like the sea owes her something and she's waiting patiently to collect."
    "When you approach, she turns without surprise."
    el "I was starting to think you weren't going to come."
    scene cg_elle_portugal_turn with dissolve
    show screen hud
    # Branch on the player's earlier response in arc_elle_travel_2.
    if elle_travel_2_response == "take_it":
        el "You made it sound obvious. I think you were right."
        "A beat."
        el "I'm going. Three weeks first. Then I decide whether the eighteen months is real."
        "She says it like it's settled. It is."
    elif elle_travel_2_response == "what_miss":
        el "I kept making that list. It got long."
        "She looks at the water."
        el "So I'm staying. For now."
        "For now is doing a lot of work in that sentence."
    else:
        # "what_changed" or None / fallback
        el "I'm going to defer it. One year. See what the year says."
        "She almost laughs at herself."
        el "I know. It's very me."
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    show elle_sundress_normal at sprite_r
    menu:
        "\"That's the right call.\"" if elle_trust >= 35:
            $ _apply_trust("elle", 3)
            el "You don't know that."
            "Beat."
            el "But thanks."
        "\"Are you sure?\"":
            $ _apply_trust("elle", 2)
            el "No. But I'm done being unsure about being unsure."
        "\"What happens next?\"":
            $ _apply_aff("elle", 3)
            el "I go to the beach, or I go to Portugal. Either way, I figure it out."
            "She almost laughs."
        "[Don't say anything. Sit down next to her.]":
            $ _apply_trust("elle", 3)
            $ _apply_aff("elle", 2)
            "She sits too. For a while, neither of you says anything."
            el "You're good at this part."
    "The light goes gold."
    el "I'll let you know how it ends up."
    "Something shifts in her face — not sadness, just the weight of a thing decided."
    el "It means something that you came."
    "She goes."
    $ spend_time(1.0)
    $ _apply_aff("elle", 2)
    $ elle_decision_done = True
    $ elle_decision_pending = False
    $ add_relationship_memory("elle", "elle_portugal_moment", "She told me what she decided")
    $ elle_decision_day = day
    $ elle_life_state = "departure_pending" if elle_travel_2_response == "take_it" else ("staying" if elle_travel_2_response == "what_miss" else "deferred")
    hide elle_sundress_normal
    return


# ── scene_sam_marcus_park ─────────────────────────────────────────────────────
# MAJOR scene. Fires at location_park Mon-Fri 06-10 when both npc_here("sam")
# and npc_here("marcus") return True and sam_marcus_scene_pending is set.
# CG: cg_sam_marcus_court (at the court moment, then return to sprites).
# Branch: sam_leads = (sam_affection >= marcus_affection).

label scene_sam_marcus_park:
    scene basketball_court_day
    show screen hud
    show marcus_park_neutral at sprite_l
    show sam_normal at sprite_r
    "You arrive at the park early. Sam and Marcus are already at the court — mid-argument, low-stakes, the kind they've clearly had before."
    m "You count every rep. That's why you plateau."
    sam "You stop counting and you get sloppy."
    "They're both half-right and they know it."
    "They turn to you at the same moment."
    m "Tiebreaker. Come on."
    scene cg_sam_marcus_court with dissolve
    show screen hud
    $ _sam_leads = sam_affection >= marcus_affection
    if _sam_leads:
        menu:
            "Side with Sam. \"Counting keeps you honest.\"":
                $ _apply_aff("sam", 3)
                $ _apply_trust("sam", 2)
                $ _apply_aff("marcus", -1)
                sam "Finally."
                m "Two against one. Fine. Next week I'll destroy both of you."
            "Side with Marcus. \"At some point you have to trust your body.\"":
                $ _apply_aff("marcus", 3)
                $ _apply_aff("sam", -1)
                sam "You're wrong. But okay."
            "[Split it.] \"Count to build the habit, then drop the count.\"":
                $ _apply_aff("sam", 2)
                $ _apply_aff("marcus", 2)
                sam "That's... actually fine."
                m "You're going to be unbearable about this."
    else:
        menu:
            "Side with Marcus. \"Listening to your body beats counting reps.\"":
                $ _apply_aff("marcus", 3)
                $ _apply_trust("marcus", 2)
                $ _apply_aff("sam", -1)
                m "See."
                sam "Still wrong. But noted."
            "Side with Sam. \"Structure first.\"":
                $ _apply_aff("sam", 3)
                $ _apply_aff("marcus", -1)
                m "I'm surrounded by people who love spreadsheets."
            "[Split it.] \"Both. At different stages.\"":
                $ _apply_aff("sam", 2)
                $ _apply_aff("marcus", 2)
                m "You're not picking a side."
                sam "They're right."
    scene basketball_court_day
    show screen hud
    show marcus_park_neutral at sprite_l
    show sam_normal at sprite_r
    "You play. It's nothing serious — three-person casual shooting, the kind where score doesn't matter."
    "By the end both of them are more interested in the next coffee than the argument."
    sam "Same time tomorrow?"
    "Marcus doesn't say yes. He'll be there. He always is."
    $ spend_time(1.5)
    $ _apply_trust("sam", 1)
    $ _apply_trust("marcus", 1)
    $ major_scene_last_day = day
    $ sam_marcus_scene_done = True
    $ sam_marcus_scene_pending = False
    $ sam_marcus_scene_pending_day = -1
    $ add_relationship_memory("sam", "sam_marcus_court", "Early court — the three of us")
    $ add_relationship_memory("marcus", "marcus_sam_court", "Early morning court")
    hide marcus_park_neutral
    hide sam_normal
    return
