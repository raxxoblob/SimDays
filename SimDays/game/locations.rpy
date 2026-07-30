# All location labels

# ── HOME ──────────────────────────────────────────────────────────────
label location_home:
    if not move_in_complete:
        $ move_in_complete = True
        scene cheaphouse_day with fade
        show screen hud
        "You set your bag down inside apartment 12. Home — for now."
        "The place came furnished — barely. A table, a chair, a mattress that could be worse."
    # Queue home-visit invitations the first time item + relationship conditions are met.
    if (own_programming_kit and eli_affection >= 25 and eli_trust >= 20
            and eli_met and not message_already_queued("eli_side_project_invite")):
        $ queue_phone_message("eli", "You mentioned that kit you bought. I have a small side project that could use a second person. Your place or mine?", day, "eli_side_project_invite", responses=_ELI_SIDE_RESP)
    if (own_coffee_machine and nora_affection >= 30 and nora_trust >= 20
            and nora_met and not message_already_queued("nora_coffee_machine_invite")):
        $ queue_phone_message("nora", "You bought a home coffee machine and didn't ask the person who works with coffee all day? This needs an inspection.", day, "nora_coffee_machine_invite", responses=_NORA_HOME_COFFEE_RESP)
    if (own_guitar and skill_music >= 1 and zoe_affection >= 25
            and zoe_met and not message_already_queued("zoe_guitar_invite")):
        $ queue_phone_message("zoe", "You own a guitar? Either prove it or stop pretending it counts as furniture.", day, "zoe_guitar_invite", responses=_ZOE_GUITAR_RESP)
    if (apartment_tier == 1 and home_coffee_calibrated and nora_met
            and nora_cooking_state == "none"
            and (nora_cooking_declined_day < 0 or day >= nora_cooking_declined_day + 14)):
        $ queue_phone_message("nora", "That kitchen of yours is depressing. Come on — I'll show you what you can do with a bad hob and the right method.", day, "nora_cheap_home_cooking_invite", responses=_NORA_CHEAP_COOK_RESP)
        $ nora_cooking_state = "offered"
    scene expression home_bg()
    show screen hud
    jump location_home_actions

label location_home_actions:
    $ activity_exit_jump = "location_hallway"
    $ activity_exit_name = "Hallway"
    scene expression home_bg()
    show screen hud
    # Commitment triggers for home-visit scenes
    if commitment_available("eli_side_project_1"):
        call home_eli_side_project_scene
        jump location_home_actions
    if commitment_available("nora_coffee_1"):
        call home_nora_coffee_scene
        jump location_home_actions
    if commitment_available("zoe_guitar_1"):
        call home_zoe_guitar_scene
        jump location_home_actions
    if commitment_available("nora_bad_day_1"):
        call scene_nora_bad_day
        jump location_home_actions
    if (nora_cooking_state == "pending"
            and not commitment_available("nora_cheap_home_cooking_1")
            and any(c["id"] == "nora_cheap_home_cooking_1"
                    and not c.get("completed") and not c.get("cancelled")
                    for c in player_commitments)):
        $ nora_cooking_state = "none"
        $ nora_cooking_declined_day = day
    if commitment_available("nora_cheap_home_cooking_1"):
        call scene_nora_cheap_home_cooking
        jump location_home_actions
    # Phase 49: NPC invitation visits dispatched as personal WED events.
    $ _wed_per = wed_poll_personal("location_home")
    if _wed_per:
        call expression _wed_per
        jump location_home_actions

    menu (screen="activity"):
        "Sleep":
            jump action_sleep_menu

        "Cook something" if need_hunger < 90:
            jump location_home_cook

        "Shower (0.5h)" if need_hygiene < 90:
            scene cheap_home_shower
            show screen hud
            $ spend_time(0.5)
            $ need_hygiene = min(100, need_hygiene + 40)
            "You take a quick shower. Feeling fresh."
            jump location_home_actions

        "Nap (3h)" if own_bed:
            $ _nap_owarn = _overlap_warning_text(3)
            if _nap_owarn:
                menu:
                    "[_nap_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_home_actions
            $ spend_time(3)
            $ need_energy = min(100, need_energy + 45)
            "A proper nap on a proper bed. You wake up sharp."
            jump location_home_actions

        "Use computer" if own_computer:
            jump use_computer

        "Practice guitar (2h)" if own_guitar:
            $ _guitar_owarn = _overlap_warning_text(2)
            if _guitar_owarn:
                menu:
                    "[_guitar_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_home_actions
            $ _guitar_uses = activity_use_count_today("home_guitar")
            $ mark_activity_used_today("home_guitar")
            $ spend_time(2)
            if _guitar_uses == 0:
                $ gain_skill("music", 5)
                "You run scales and a couple of songs. Fingers sore, ear sharper."
            elif _guitar_uses == 1:
                $ gain_skill("music", 2)
                "A second session. Progress is slower, but you find a cleaner chord shape."
            else:
                "You noodle for a bit. Your fingers aren't interested today."
            jump location_home_actions

        "Make coffee (0.5h)" if own_coffee_machine:
            $ spend_time(0.5)
            if home_coffee_calibrated:
                $ need_energy = min(100, need_energy + 12)
                "Nora's settings. Comes out right."
            else:
                $ need_energy = min(100, need_energy + 7)
                "Fine. Could be better."
            jump location_home_actions

        "Invite someone for dinner (3h)" if own_kitchen_set:
            call home_dinner_invite_menu
            jump location_home_actions


label location_home_cook:
    scene cheap_home_cook
    show screen hud
    menu (screen="activity"):
        "Toast ($2, +15 hunger)":
            if money < 2:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(0.25)
            $ gain_money(-2)
            $ need_hunger = min(100, need_hunger + 15)
            "Two slices of toast. Better than nothing."
            jump location_home_actions
        "Instant noodles ($3, +22 hunger)":
            if money < 3:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(0.25)
            $ gain_money(-3)
            $ need_hunger = min(100, need_hunger + 22)
            "Straight out of the packet, four minutes. Fine."
            jump location_home_actions
        "Scrambled eggs ($5, +32 hunger)":
            if money < 5:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(0.5)
            $ gain_money(-5)
            $ need_hunger = min(100, need_hunger + 32)
            "Oil, heat, three eggs. You feel a bit more human."
            jump location_home_actions
        "Pasta bolognese ($8, +55 hunger) [[Cooking Lv 2]]" if skill_cook >= 2:
            if money < 8:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(0.5)
            $ gain_money(-8)
            $ need_hunger = min(100, need_hunger + 55)
            $ gain_skill("cook", 2)
            "Proper sauce, actual garlic. Getting the hang of this."
            jump location_home_actions
        "Chicken stir-fry ($10, +65 hunger, +8 energy) [[Cooking Lv 4]]" if skill_cook >= 4:
            if money < 10:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(0.75)
            $ gain_money(-10)
            $ need_hunger = min(100, need_hunger + 65)
            $ need_energy = min(100, need_energy + 8)
            $ gain_skill("cook", 2)
            "Fast, hot, loud. A proper meal - you feel it in the energy too."
            jump location_home_actions
        "Sunday roast ($18, +80 hunger, +15 energy) [[Cooking Lv 7]]" if skill_cook >= 7:
            if money < 18:
                "Not enough cash."
                jump location_home_actions
            $ spend_time(1.0)
            $ gain_money(-18)
            $ need_hunger = min(100, need_hunger + 80)
            $ need_energy = min(100, need_energy + 15)
            $ gain_skill("cook", 3)
            "An afternoon's prep. The apartment smells like a real home. You feel genuinely full for the first time in a while."
            jump location_home_actions
        "Close the fridge.":
            jump location_home_actions

# ponytail: reuses home_bg - swap for a desk/monitor screen background later.
label use_computer:
    scene expression home_bg()
    show screen hud
    menu (screen="activity"):
        "Practice coding (3h)":
            $ spend_time(3)
            $ gain_skill("prog", 7 if own_programming_kit else 5)
            $ need_energy = max(0, need_energy - 15)
            "Three hours deep in a side project. The docs finally click."
            jump use_computer
        "Trade stocks":
            $ store._stock_session_charged = False
            call screen stock_market
            jump use_computer
        "Browse the web (0.5h)":
            $ spend_time(0.5)
            "You fall down a few rabbit holes. Nothing productive."
            jump use_computer
        "Get up":
            jump location_home_actions

# ── CAFE ──────────────────────────────────────────────────────────────
label location_cafe:
    $ current_loc = "location_cafe"
    $ fs_mark("grounds_visited")
    $ fs_record_district("centrum")
    # nora_last_seen_day is set in nora_greet (on actual interaction), not on location entry
    # After-hours commitment (Nora closing) fires at/after close — exempt from the
    # open-check below, since it is by design an out-of-hours meeting.
    if commitment_available("nora_closing_1"):
        call phone_nora_closing_scene
        jump map
    # Venue-open gate FIRST: no ambient scene should stage in a closed café
    # (a scene playing, then "the café is closed" afterwards, is the bug this fixes).
    if not venue_open("coffee_shop"):
        "The café is closed. Come back between 07:00–19:00."
        jump map
    # Priority 2: pending conflict/repair scenes (minor)
    if nora_ignored_pending and nora_met:
        call scene_nora_feels_ignored
    # Priority 3: pending breakthrough scenes (major) — one per day
    if major_scene_last_day != day:
        if nora_hug_school_pending and nora_met:
            call scene_nora_hug_school
    # Priority 4: crossover scenes
    if nora_kai_pending and nora_met and kai_met:
        call scene_nora_kai_crossover
    # Priority 5: Kai café quiet (defers when nora_kai_pending has priority)
    if kai_cafe_quiet_pending and npc_here("kai") and not nora_kai_pending:
        call scene_kai_cafe_quiet
    scene expression cafe_bg()
    show screen hud
    if not nora_met:
        jump cafe_first_visit
    jump cafe_actions

label cafe_first_visit:
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal at sprite_r
    "The place smells of espresso and warm milk. Behind the counter, a woman in an apron looks up from a stack of cups, dark hair coming loose from its bun."
    n "Hey - welcome to Grounds. First time, right? You've got the lost look. Everybody does their first week in this city."
    menu:
        "\"That obvious? Yeah, just moved in.\"":
            $ nora_affection += 4
            n "Thought so. Coffee helps. So does not overthinking the menu - it's mostly just coffee with extra steps."
        "\"I'm looking for work, actually.\"":
            $ nora_affection += 3
            n "Oh? We're always a pair of hands short. Talk to Henry - he owns the place - but honestly, if you can carry a tray without wearing it, you're hired."
        "\"Just here for the coffee.\"":
            n "A man who knows what he wants. Refreshing, honestly."
    n "I'm Nora, by the way. I basically live behind this counter."
    "You introduce yourself."
    n "Good to meet you, [mc_name]. First cup's on me - new-neighbor rate. After that Henry starts counting, so enjoy it."
    $ nora_met = True
    hide nora_cafe_normal
    jump cafe_actions

label cafe_actions:
    if commitment_available("martha_coffee_1"):
        call phone_martha_coffee_scene
    if nora_affection >= 40 and hour >= 19 and not nora_closing_done:
        jump nora_closing_scene
    if nora_trust >= 30 and nora_affection >= 30 and not nora_rent_done and nora_closing_done:
        jump nora_rent_scene
    # Romance reopen — offered once, after the closing scene, if the player let it
    # go ambiguous/platonic and later rebuilt momentum (see can_offer_romance_reopen).
    if (nora_closing_done and not nora_reopen_done and major_scene_last_day != day
            and can_offer_romance_reopen("nora") and hour >= 19):
        call scene_nora_romance_reopen
    if hour >= 19:
        "The café lights are going off. Time to head out."
        jump map
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene expression cafe_bg()
    show screen hud
    $ _group = group_scene_check()
    $ _group_lbl = group_scene_label(_group) if _group else ""
    hide screen people_here_dock
    # World Event Director
    $ _wed_amb = wed_poll_ambient("location_cafe")
    if _wed_amb:
        call expression _wed_amb
    $ _wed_per = wed_poll_personal("location_cafe")
    if _wed_per:
        call expression _wed_per
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("cafe_actions")
    menu (screen="activity"):
        "Join [_group_lbl] →" if _group:
            call group_interact(_group[0], _group[1])
            jump cafe_actions
        "Buy a coffee ($3, 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-3)
            $ _coffee_e = 20 if has_event("cafe_energy") else 10
            $ need_energy = min(100, need_energy + _coffee_e)
            if has_event("cafe_energy"):
                "Double-strength today. You feel the buzz hit immediately."
            else:
                "You sip a good coffee. Worth it."
            jump cafe_actions
        "Work a shift - Barista (4h)":
            jump cafe_work_shift


label cafe_work_shift:
    if hour + 4 > DAY_END:
        "It's too late to start a full shift."
        jump cafe_actions
    if need_energy < 15:
        "You can barely keep your eyes open. Even Henry would send you home. Sleep first."
        jump cafe_actions
    $ _owarn = _overlap_warning_text(4)
    if _owarn:
        menu:
            "[_owarn]\nContinue anyway?"
            "Continue":
                pass
            "Go back":
                jump cafe_actions
    hide npcsprite
    hide npcsprite2
    hide npcsprite3
    hide npcsprite4
    hide screen people_here_dock
    $ active_work_shift = "cafe"
    scene pov_barista
    show screen hud
    $ _cafe_n = store.shifts_worked.get("cafe", 0)
    $ _cafe_pay = 55 if _cafe_n < 5 else (65 if _cafe_n >= 15 else 60)
    $ spend_time(4)
    $ gain_money(_cafe_pay)
    $ store.need_energy = max(0, store.need_energy - 20)
    $ fs_mark("grounds_shift_done")
    $ fs_mark("outside_activity")
    "Four hours of steaming milk and small talk. You pocket $[_cafe_pay]."
    if npc_here("nora"):
        show nora_cafe_normal at sprite_r
        if not cafe_shift_done:
            $ cafe_shift_done = True
            n "Not bad for a first shift. Henry says you're a natural - high praise, he called me 'adequate' for a year."
        else:
            n "Another one down. You're basically furniture now. The good kind."
        if hour >= 20 and not message_already_queued("cafe_nora_late_1"):
            $ queue_phone_message("nora", "I saw you close tonight. Tell me next time — I'll do the last run with you.", day + 1, "cafe_nora_late_1")
        if nora_trust >= 20 and shifts_worked.get("cafe", 0) >= 5 and not message_already_queued("nora_closing_invite"):
            $ queue_phone_message("nora", "Closing crew tomorrow is just me and Henry. Come do the last hour? I'll make it worth it, coffee-wise.", day + 1, "nora_closing_invite", responses=_NORA_CLOSING_RESP)
        if commitment_available("nora_closing_1"):
            call phone_nora_closing_scene
        hide nora_cafe_normal
    if _work_event_roll("cafe"):
        call work_event_cafe
    $ active_work_shift = None
    jump cafe_actions

# ── GYM ───────────────────────────────────────────────────────────────
label location_gym:
    $ current_loc = "location_gym"
    $ fs_record_district("centrum")
    if not venue_open("gym"):
        "The gym is closed for the night."
        jump map
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene gymdaypeople
    show screen hud
    hide screen people_here_dock
    if day >= gym_pass_expires:
        jump gym_reception
    jump gym_floor

label gym_reception:
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene gym_reception
    show screen hud
    "The receptionist looks up. \"Pass or day rate?\""
    menu (screen="activity"):
        "Week pass ($40)":
            if money < 40:
                "Not enough cash."
                jump gym_reception
            $ gain_money(-40)
            $ gym_pass_expires = day + 7
            "She hands over a card. Seven days, unlimited access."
            jump gym_floor
        "Month pass ($120)":
            if money < 120:
                "Not enough cash."
                jump gym_reception
            $ gain_money(-120)
            $ gym_pass_expires = day + 30
            "Better value if you actually show up. She seems mildly sceptical."
            jump gym_floor
        "Day rate ($8)":
            if money < 8:
                "Not enough cash."
                jump gym_reception
            $ gain_money(-8)
            $ gym_pass_expires = day + 1
            "One day. Fair enough."
            jump gym_floor
        "Not today.":
            jump location_centrum

label gym_floor:
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    # ponytail: hour window matches Sam's actual gym schedule (Mon-Fri 10-14, WKD 09-13).
    if sam_affection >= 35 and sam_trust >= 25 and not sam_gym_done and 10 <= hour < 14:
        jump sam_gym_scene
    scene gymdaypeople
    show screen hud
    hide screen people_here_dock
    # World Event Director: personal events at gym (sam_off_routine when off her schedule)
    $ _wed_per = wed_poll_personal("location_gym")
    if _wed_per:
        call expression _wed_per
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("gym_floor")
    menu (screen="activity"):
        "Work a shift (8h)" if job_id == "trainer":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump gym_floor
            if too_tired():
                "You're running on empty. Trainers need rest too."
                jump gym_floor
            $ _tr_owarn = _overlap_warning_text(8)
            if _tr_owarn:
                menu:
                    "[_tr_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump gym_floor
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            scene pov_trainer
            show screen hud
            $ _tired = do_shift("trainer", 8)
            $ tr_shifts += 1
            if not kai_met:
                call tr_first_day
            elif not tr_task_1_done and tr_shifts >= 3:
                call tr_task_1
            elif tr_task_1_done and not tr_npc1_done and tr_shifts >= 5:
                call tr_npc1_kai
            elif tr_npc1_done and not tr_npc2_done and tr_shifts >= 7:
                call tr_npc2_kai
            elif tr_npc2_done and not tr_boundary_done:
                call tr_boundary_case
            elif (tr_boundary_done and tr_boundary_followup_pending
                    and tr_shifts >= tr_boundary_followup_shift
                    and not tr_boundary_followup_done):
                call tr_boundary_followup
            elif (tr_boundary_followup_done and not tr_review_done
                    and tr_shifts >= tr_boundary_followup_shift + tr_boundary_review_extra_shifts
                    and job_performance >= 100 and can_promote()):
                call tr_review_asst
            else:
                if _tired:
                    "Drained, but you kept your energy up for every client. That's the job."
                else:
                    "Back-to-back sessions. You finish knowing exactly what you did today."
            if _work_event_roll("trainer"):
                call work_event_trainer
            jump gym_floor
        "Apply as a Personal Trainer" if job_id is None:
            if can_apply("trainer"):
                $ apply_job("trainer")
                "Kai looks you over, then at your form on the floor. \"You know how to move. Let's see if you can teach it.\" Assistant trainer. Starting Monday."
            else:
                "Kai checks your profile. \"STR and the Athletic Training cert minimum. The college runs the course — come back when you're there.\""
                $ _fs_career_rejection()
            jump gym_floor
        "Train - weights (1.5h, -15 energy)":
            if too_tired():
                "You're too exhausted to lift. Get some rest first."
                jump gym_floor
            $ _sup = "preworkout" if supplements.get("preworkout", 0) > 0 else ("protein" if supplements.get("protein", 0) > 0 else None)
            if _sup:
                $ supplements[_sup] -= 1
            scene pov_gym_weights
            show screen hud
            $ spend_time(1.5)
            $ need_energy = max(0, need_energy - 15)
            $ _str_exp = 30 if has_event("gym_trainer") else 20
            if _sup == "preworkout":
                $ _str_exp = int(_str_exp * 2.0)
            elif _sup == "protein":
                $ _str_exp = int(_str_exp * 1.5)
            $ gain_stat("str", _str_exp)
            $ gain_stat("app", 8)
            if has_event("gym_trainer"):
                "The free trainer spots your form and pushes you hard. Exceptional session."
            elif _sup == "preworkout":
                "Pre-workout in the system. You push past the usual ceiling."
            elif _sup == "protein":
                "Protein shake in the tank. A clean, productive session."
            else:
                "A solid session. You can feel it already."
            $ fs_mark("study_done")
            $ fs_mark("outside_activity")
            jump gym_floor
        "Cardio (1h, -12 energy)":
            if too_tired():
                "You're too exhausted to run. Rest up first."
                jump gym_floor
            scene gym_cardio
            show screen hud
            $ spend_time(1)
            $ need_energy = max(0, need_energy - 12)
            $ gain_stat("str", 10)
            $ gain_stat("app", 4)
            "You run until your lungs complain."
            $ fs_mark("study_done")
            $ fs_mark("outside_activity")
            jump gym_floor
        "Buy Protein Shake ($12)":
            if money < 12:
                "Not enough cash."
                jump gym_floor
            $ gain_money(-12)
            $ supplements["protein"] += 1
            "A vanilla protein powder. Mix with water after training. +50%% STR EXP on the next weights session."
            jump gym_floor
        "Buy Pre-workout ($20)":
            if money < 20:
                "Not enough cash."
                jump gym_floor
            $ gain_money(-20)
            $ supplements["preworkout"] += 1
            "The label is mostly warnings. +100%% STR EXP on the next weights session."
            jump gym_floor

# ── LIBRARY ───────────────────────────────────────────────────────────
label location_library:
    $ current_loc = "location_library"
    $ fs_record_district("centrum")
    if not venue_open("library"):
        "The library is closing. Time to head out."
        jump map
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    hide screen people_here_dock
    $ _wed_amb = wed_poll_ambient("location_library")
    if _wed_amb:
        call expression _wed_amb
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_library")
    menu (screen="activity"):
        "Study — general (2h)":
            if too_tired():
                "Too tired to focus. The words blur. Sleep first."
                jump location_library
            $ _study_owarn = _overlap_warning_text(2)
            if _study_owarn:
                menu:
                    "[_study_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_library
            scene expression ("library_study_night" if hour >= 20 else "library_study_day")
            show screen hud
            $ _study_uses = activity_use_count_today("library_study")
            $ mark_activity_used_today("library_study")
            $ spend_time(2)
            if _study_uses == 0:
                $ gain_stat("int", 10)
                "Two hours of focused reading. Your brain hurts in a good way."
            elif _study_uses == 1:
                $ gain_stat("int", 5)
                "Second session. Progress slows — the mind's full — but you push through."
            else:
                "You're staring at the page. Nothing new is going in. Get some rest."
            $ fs_mark("study_done")
            $ fs_mark("outside_activity")
            jump location_library
        "Self-study a subject (2h, free)":
            if too_tired():
                "Too tired to concentrate on anything. Sleep first."
                jump location_library
            scene expression ("library_study_night" if hour >= 20 else "library_study_day")
            show screen hud
            menu:
                "What are you working through?"
                "Medicine":
                    $ spend_time(2)
                    $ store.need_energy = max(0, store.need_energy - 18)
                    $ gain_skill("med", 2)
                    "Dense textbooks, clinical notes. Slower than a real course, but it sticks."
                "Programming":
                    $ spend_time(2)
                    $ store.need_energy = max(0, store.need_energy - 18)
                    $ _prog_gain = 3 if own_programming_kit else 2
                    $ gain_skill("prog", _prog_gain)
                    "Tutorials, docs, Stack Overflow rabbit holes. You get somewhere."
                "Business":
                    $ spend_time(2)
                    $ store.need_energy = max(0, store.need_energy - 18)
                    $ gain_skill("biz", 2)
                    "Case studies and frameworks. Dry but useful."
                "Art":
                    $ spend_time(2)
                    $ store.need_energy = max(0, store.need_energy - 18)
                    $ gain_skill("art", 2)
                    "Theory, references, sketching. You can feel the improvement in small ways."
            $ fs_mark("study_done")
            $ fs_mark("outside_activity")
            jump location_library

# ── BAR ───────────────────────────────────────────────────────────────
label location_bar:
    $ current_loc = "location_bar"
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    # Priority 2: pending conflict scenes
    if marcus_missed_pending and marcus_affection >= 30:
        call scene_marcus_missed_commitment
    # Priority 2b: Caroline off-work (Thursday 19-22; bypasses npc_here — no bar schedule)
    if caroline_bar_pending and day % 7 == 3 and 19 <= hour < 22:
        call scene_caroline_thursday_bar
    # Caroline romance-opening beat (Thursday, after the first off-work drink)
    if (caroline_bar_done and not caroline_romance_open_done and major_scene_last_day != day
            and caroline_affection >= 65 and caroline_trust >= 60
            and day % 7 == 3 and 19 <= hour < 22):
        call scene_caroline_romance_open
    # Lena romance-opening beat (bar, off shift, after the shoulder-gesture scene)
    if (lena_shoulder_done and not lena_romance_open_done and npc_here("lena")
            and major_scene_last_day != day
            and lena_affection >= 55 and lena_trust >= 55):
        call scene_lena_romance_open
    # Priority 3: major scenes — one per day, late night only
    if major_scene_last_day != day:
        if not car_marcus_drive_done and marcus_affection >= 30 and marcus_trust >= 20 and car_tier >= 1 and hour >= 22:
            call scene_car_marcus_drive
    scene bar
    show screen hud
    hide screen people_here_dock
    # Priority 4: Natalie humanisation (weekend bar schedule, npc_here check)
    if natalie_bar_scene_pending and npc_here("natalie"):
        call scene_natalie_bar_offduty
    # Priority 4b: Martha romance reopen — after the rooftop, at the bar (Wed eve),
    # if the player let it stay ambiguous/platonic and rebuilt momentum.
    if (martha_rooftop_done and not martha_reopen_done and npc_here("martha")
            and major_scene_last_day != day and can_offer_romance_reopen("martha")):
        call scene_martha_romance_reopen
    # Priority 5: Marcus basketball invite — fires once at bar when Marcus is present
    if marcus_basketball_invite_pending and marcus_met and npc_here("marcus"):
        $ marcus_basketball_invite_pending = False
        $ marcus_basketball_invite_done = True
        m "Hey. You free tomorrow morning? I know a court at the park. Eight o'clock, if you can make it."
        menu:
            "I'll be there.":
                $ add_commitment("marcus_basketball_1", "marcus", "Basketball with Marcus", day + 1, 8, "City Park", "nop")
                m "Good. Don't be late."
            "Maybe another time.":
                m "Your loss."
    # World Event Director
    $ _wed_amb = wed_poll_ambient("location_bar")
    if _wed_amb:
        call expression _wed_amb
    $ _wed_per = wed_poll_personal("location_bar")
    if _wed_per:
        call expression _wed_per
    $ _vis = location_sprites()
    call show_public_sprites
    $ _drink_cost = 4 if has_event("bar_happy") else 8
    $ _chr_bonus  = 30 if has_event("bar_happy") else 15
    show screen people_here_dock("location_bar")
    menu (screen="activity"):
        "Have a drink ($[_drink_cost], 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-_drink_cost)
            "The noise and the drinks do their job."
            jump location_bar
        "Socialize (1h)":
            if stat_chr >= 25:
                $ _soc_uses = activity_use_count_today("bar_socialize")
                $ mark_activity_used_today("bar_socialize")
                $ spend_time(1)
                if _soc_uses == 0:
                    $ gain_stat("chr", _chr_bonus)
                    if has_event("bar_happy"):
                        "Happy hour energy in the air — you're electric tonight."
                    else:
                        "You work the room. A few numbers exchanged."
                elif _soc_uses == 1:
                    $ gain_stat("chr", _chr_bonus // 2)
                    "Second round of conversation. Still good, but the fresh energy is gone."
                else:
                    "You've made the rounds. Everyone's heard your best material. Call it a night."
            else:
                "You hover near a few groups but can't quite break in. Maybe with a bit more charm."
            jump location_bar

# ── OFFICE (corporate career) ─────────────────────────────────────────
label location_office:
    $ current_loc = "location_office"
    # Venue-open gate FIRST: no Martha scene should stage when Nexus Tower is
    # closed (weekend/night) — previously the scene played, then the closed
    # message appeared afterwards.
    if not venue_open("office_exec"):
        if day % 7 >= 5:
            "Nexus Tower is dark on weekends. The corporate world takes Saturdays off."
        else:
            "Nexus Tower is locked up for the night."
        jump map
    hide screen people_here_dock
    # Priority 2: pending conflict scenes
    if martha_gift_scene_pending and martha_met and hour >= 9 and hour < 18:
        call scene_martha_gift_accusation
    # Priority 3: pending breakthrough scenes (major) — one per day
    if major_scene_last_day != day:
        if martha_corridor_pending and hour >= 9 and hour < 18:
            call scene_martha_corridor_gesture
    # Priority 4/5: everyday first-time scenes (minor)
    if wardrobe_tier >= 2 and martha_affection >= 25 and martha_met and not martha_wardrobe_done:
        call scene_wardrobe_martha
    if hour < 10 and martha_affection >= 20 and martha_met and not martha_coffee_machine_done:
        call scene_martha_office_coffee
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene goodoffice1
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_office")
    if _wed_amb:
        call expression _wed_amb
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_office")
    menu (screen="activity"):
        "Go to work" if job_id == "corporate":
            if too_tired() or hour + 8 > DAY_END:
                "You're too tired or it's too late to start a shift."
                jump location_office
            $ _corp_owarn = _overlap_warning_text(8)
            if _corp_owarn:
                menu:
                    "[_corp_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_office
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            menu:
                "Handle regular responsibilities.":
                    call corp_regular_work
                "Focus on Project Atlas." if atlas_started and not atlas_completed:
                    call corp_project_work
                "Work alongside Martha." if martha_collab_available():
                    call corp_work_martha
                "Spend some time getting to know the floor.":
                    call corp_network
            if need_energy > 40 and hour + 2 <= DAY_END:
                menu:
                    "Head out.":
                        pass
                    "Stay for overtime.":
                        call corp_overtime
            jump location_office

        "Ask about a promotion" if job_id == "corporate" and can_promote():
            if job_rank == 0 and not corp_review_intern_done:
                if (corp_integrity_followup_done
                        and corp_shifts >= corp_integrity_followup_shift + corp_integrity_review_extra_shifts):
                    call corporate_review_intern
                else:
                    show caroline_normal at sprite_r
                    caro "There's an open matter from the reporting review. Come back once it's resolved."
                    hide caroline_normal
            else:
                $ _trial = cur_rank().get("trial")
                if _trial and not store.promotion_trials.get(("corporate", job_rank), False):
                    call expression _trial
                else:
                    if promote():
                        "New title. Caroline hands you the updated contract with a tight smile."
                    else:
                        "\"Strong quarter - but you need the skills for the next rung first.\""
            jump location_office

        "Apply for the graduate scheme" if job_id is None:
            if can_apply("corporate"):
                call corporate_recruit
            else:
                show caroline_normal as npcsprite at sprite_c
                caro "HR. Let me save us both time - Business 1, INT 20, CHR 20, APP 20. All four, minimum. The college helps."
                hide npcsprite
                $ _fs_career_rejection()
            jump location_office

        "Quit this job" if job_id == "corporate":
            $ quit_job()
            "You hand in your notice. Caroline nods. \"Best of luck.\""
            jump location_office


# ── MALL (shop hub) ───────────────────────────────────────────────────
label location_mall:
    $ fs_record_district("mall")
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_mall")
    if _wed_amb:
        call expression _wed_amb
    call screen mall_hub

label location_shop_clothing:
    $ activity_exit_jump = "location_mall"
    $ activity_exit_name = "Mall"
    scene clothesshop
    show screen hud
    menu (screen="activity"):
        "Buy a casual outfit ($80)" if wardrobe_tier < 1:
            if money < 80:
                "Not enough money."
            else:
                $ gain_money(-80)
                $ wardrobe_tier = 1
                $ gain_stat("app", 3)
                "A clean, well-fitted outfit. You carry yourself a little differently."
            jump location_shop_clothing
        "Upgrade your wardrobe (+status)" if 1 <= wardrobe_tier < 3:
            $ _wd_price = {2: 500, 3: 1000}[wardrobe_tier + 1]
            if money < _wd_price:
                "Not enough money."
            else:
                $ gain_money(-_wd_price)
                $ wardrobe_tier += 1
                "Designer pieces, tailored. You carry yourself differently — people notice."
            jump location_shop_clothing

label location_shop_electronics:
    $ activity_exit_jump = "location_mall"
    $ activity_exit_name = "Mall"
    scene electronicsshop
    show screen hud
    menu (screen="activity"):
        "Buy a gadget ($100)" if not own_programming_kit:
            if money < 100:
                "Not enough money."
            else:
                $ gain_money(-100)
                $ own_programming_kit = True
                $ gain_stat("int", 2)
                "A new toy to tinker with. You spend a few evenings digging into it — and pick up a thing or two."
            jump location_shop_electronics
        "Buy a guitar ($150)" if not own_guitar:
            if money < 150:
                "Not enough money."
            else:
                $ gain_money(-150)
                $ own_guitar = True
                "A decent starter guitar. Now you can practice music at home."
            jump location_shop_electronics
        "Metal detector ($120)" if not own_metal_detector:
            if money < 120:
                "You can't quite afford it right now."
            else:
                $ gain_money(-120)
                $ own_metal_detector = True
                "You pick up a compact metal detector. Good for the beach, if you have time."
            jump location_shop_electronics

label location_shop_gifts:
    $ activity_exit_jump = "location_mall"
    $ activity_exit_name = "Mall"
    scene giftshop
    show screen hud
    menu (screen="activity"):
        "Treat yourself ($30, +energy)":
            if money < 30:
                "Not enough money."
            else:
                $ gain_money(-30)
                $ need_energy = min(100, need_energy + 15)
                "A small indulgence. You feel a little brighter."
            jump location_shop_gifts
        "Buy a coffee machine ($150)" if not own_coffee_machine:
            if money < 150:
                "Not enough money."
            else:
                $ gain_money(-150)
                $ own_coffee_machine = True
                "Compact, capable, and immediately on the counter. You'll figure out the settings."
            jump location_shop_gifts
        "Buy a kitchen set ($200)" if not own_kitchen_set:
            if money < 200:
                "Not enough money."
            else:
                $ gain_money(-200)
                $ own_kitchen_set = True
                "Good pans, proper knives, a cutting board that doesn't slide. Cooking becomes less miserable."
            jump location_shop_gifts
        "Buy a better bed ($400)" if not own_bed:
            if money < 400:
                "Not enough money."
            else:
                $ gain_money(-400)
                $ own_bed = True
                "Delivered and set up at home. Sleep restores fully now - and you can grab a Nap."
            jump location_shop_gifts
        "Buy jewelry (+status)" if jewelry_tier < 3:
            $ _jw_price = [250, 650, 1500][jewelry_tier]
            if money < _jw_price:
                "Not enough money."
            else:
                $ gain_money(-_jw_price)
                $ jewelry_tier += 1
                "A tasteful piece that quietly says you've arrived."
            jump location_shop_gifts
        "Buy a book ($20)":
            if money < 20:
                "Not enough money."
            else:
                $ gain_money(-20)
                $ gifts["book"] += 1
                "A well-chosen paperback. Thoughtful and personal."
            jump location_shop_gifts
        "Buy sweets ($15)":
            if money < 15:
                "Not enough money."
            else:
                $ gain_money(-15)
                $ gifts["sweets"] += 1
                "A box of good chocolates. Hard to go wrong."
            jump location_shop_gifts
        "Buy a gadget ($35)":
            if money < 35:
                "Not enough money."
            else:
                $ gain_money(-35)
                $ gifts["gadget"] += 1
                "A small tech gift. Practical and a little flashy."
            jump location_shop_gifts
        "Buy flowers ($25)":
            if money < 25:
                "Not enough money."
            else:
                $ gain_money(-25)
                $ gifts["flowers"] += 1
                "A fresh bouquet. Classic for a reason."
            jump location_shop_gifts

# ── CAR DEALER (status via car_tier) ──────────────────────────────────
label location_cardealer:
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene cardealer_day
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_cardealer")
    if _wed_amb:
        call expression _wed_amb
    menu (screen="activity"):
        "Buy a used runabout ($1500)" if car_tier < 1:
            if money < 1500:
                "Not enough money. The salesman's smile cools."
            else:
                $ gain_money(-1500)
                $ car_tier = 1
                "Nothing fancy, but it's yours. Wheels change how the city sees you."
            jump location_cardealer
        "Trade up to a nice car ($4000)" if car_tier == 1:
            if money < 4000:
                "Not enough money for the upgrade yet."
            else:
                $ gain_money(-4000)
                $ car_tier = 2
                "Clean lines, leather seats. People clock it in the parking lot."
            jump location_cardealer
        "Buy the luxury model ($12000)" if car_tier == 2:
            if money < 12000:
                "Not enough for the flagship. Come back richer."
            else:
                $ gain_money(-12000)
                $ car_tier = 3
                "The kind of car that opens doors before you say a word."
            jump location_cardealer
        "Your car's top of the line" if car_tier >= 3:
            "Nothing here beats what's already in your garage."
            jump location_cardealer

# ── KITCHEN / Eleven (Culinary career) ────────────────────────────────
label location_kitchen:
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene kitchen
    show screen hud
    menu (screen="activity"):
        "Work a shift (8h)" if job_id == "culinary":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_kitchen
            if too_tired():
                "Too wiped to cook a full service. Go sleep - chef's orders."
                jump location_kitchen
            $ _cul_owarn = _overlap_warning_text(8)
            if _cul_owarn:
                menu:
                    "[_cul_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_kitchen
            scene pov_chef
            show screen hud
            $ _tired = do_shift("culinary", 8)
            $ cul_shifts += 1
            if not rena_met:
                call cul_first_day
            elif not cul_task_1_done and cul_shifts >= 3 and job_rank == 0:
                call cul_task_1
            elif cul_task_1_done and not cul_npc1_done and cul_shifts >= 5 and job_rank == 0:
                call cul_npc1_rena
            elif cul_npc1_done and not cul_npc2_done and cul_shifts >= 7 and job_rank == 0:
                call cul_npc2_rena
            elif cul_npc2_done and not scene_cul_service_crisis_done and cul_shifts >= 10 and job_rank == 0:
                call scene_cul_service_crisis
            elif cul_npc2_done and scene_cul_service_crisis_done and not cul_review_done and job_performance >= 100 and can_promote() and job_rank == 0:
                call cul_review_commis
            else:
                if _tired:
                    "Slammed and half-asleep, you burn a plate and hear about it. Bad night on the line."
                else:
                    "A brutal service, but you kept your station clean and fast. Chef almost nodded."
            if _work_event_roll("culinary"):
                call work_event_culinary
            jump location_kitchen

        "Ask about a promotion" if job_id == "culinary" and job_performance >= 100:
            if promote():
                "The chef grunts approval and hands you a bigger station. Moving up."
            else:
                "\"Not yet. Cook more, cook better, then we talk.\""
            jump location_kitchen

        "Drop off your CV" if job_id is None:
            if can_apply("culinary"):
                $ apply_job("culinary")
                "The head chef eyes your knife roll. \"Commis. Don't bleed on my food.\" You're in."
            else:
                "The head chef barely looks up. \"Not ready. Cooking 1 and some muscle, minimum. Learn to prep first.\""
                $ _fs_career_rejection()
            jump location_kitchen

        "Quit the kitchen" if job_id == "culinary":
            $ quit_job()
            "You hang up the apron. The heat wasn't for you."
            jump location_kitchen


# ── NIGHTCLUB ─────────────────────────────────────────────────────────
label location_nightclub:
    $ current_loc = "location_nightclub"
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    hide screen people_here_dock
    # Priority 3: Zoe spontaneous moment (major, night only)
    if (zoe_moment_deflected_pending and major_scene_last_day != day
            and hour >= 21 and zoe_met):
        call scene_zoe_spontaneous
    # Romance reopen — after the deflected moment, once momentum/aff/trust rebuild.
    if (zoe_moment_deflected_done and not zoe_reopen_done and zoe_met
            and hour >= 21 and major_scene_last_day != day
            and can_offer_romance_reopen("zoe")):
        call scene_zoe_romance_reopen
    scene nightclub
    show screen hud
    $ _vis = location_sprites()
    call show_public_sprites
    $ _group = group_scene_check()
    $ _group_lbl = group_scene_label(_group) if _group else ""
    show screen people_here_dock("location_nightclub")
    menu (screen="activity"):
        "Join [_group_lbl] →" if _group:
            call group_interact(_group[0], _group[1])
            jump location_nightclub
        "Hit the dance floor (1h)":
            $ spend_time(1)
            $ need_energy = max(0, need_energy - 10)
            "You lose an hour to the beat. Worth it."
            jump location_nightclub
        "Work the crowd (1h) [[CHR 30]]":
            if stat_chr < 30:
                "You need CHR 30 to hold this room."
                jump location_nightclub
            $ spend_time(1)
            $ gain_stat("chr", 30 if has_event("club_night") else 15)
            if has_event("club_night"):
                "Industry night — the room is full of people who matter. You're on fire."
            else:
                "You move room to room, easy and loud. A few new contacts."
            jump location_nightclub
        "Buy a round ($15)":
            if money < 15:
                "Not enough cash."
                jump location_nightclub
            $ spend_time(0.5)
            $ gain_money(-15)
            "Drinks all around. Cheap way to be popular for ten minutes."
            jump location_nightclub
        "DJ night - dance floor (1h) [[Fri-Sun]]":
            if day % 7 < 4:
                "DJ nights are Fri–Sun only."
                jump location_nightclub
            $ spend_time(1)
            $ gain_stat("chr", 8)
            $ need_energy = max(0, need_energy - 15)
            "The DJ pushes the crowd up. You lose yourself in it — when you surface you're grinning."
            jump location_nightclub
        "VIP section ($50, +CHR) [[Fri-Sun]]":
            if day % 7 < 4 or money < 50:
                "VIP is Fri–Sun only, $50 entry."
                jump location_nightclub
            $ spend_time(0.5)
            $ gain_money(-50)
            $ gain_stat("chr", 15)
            "The bouncer waves you past the red rope. Different league in here."
            jump location_nightclub

# ── FLEA MARKET (weekend Sat-Sun 09-18) ──────────────────────────────
label location_flea_market:
    $ current_loc = "location_flea_market"
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene mallday  # ponytail: placeholder bg — wants flea_market_day (see to_generate/locations.md)
    show screen hud
    menu (screen="activity"):
        "Browse stalls (1h)":
            $ spend_time(1)
            $ gain_stat("chr", 8)
            if renpy.random.random() < 0.2:
                "You end up in a long chat with a vendor who turns out to know everyone. Useful."
            else:
                "A lap around the stalls. Easy crowd, easy conversation."
            jump location_flea_market
        "Buy a vintage piece ($25, +APP)":
            if money < 25:
                "Not enough cash."
                jump location_flea_market
            $ spend_time(0.5)
            $ gain_money(-25)
            $ gain_stat("app", 3)
            "A score — your eye for style is sharpening."
            jump location_flea_market
        "Buy a book ($12, +INT)":
            if money < 12:
                "Not enough cash."
                jump location_flea_market
            $ spend_time(0.5)
            $ gain_money(-12)
            $ gain_stat("int", 2)
            "A dog-eared paperback from a half-collapsed box. You'll read it tonight."
            jump location_flea_market
        "Haggle with vendors (1h)":
            $ spend_time(1)
            $ gain_stat("chr", 8)
            "Back and forth over prices. Good practice in reading people."
            jump location_flea_market

# ── PARK ──────────────────────────────────────────────────────────────
label location_park:
    $ current_loc = "location_park"
    $ fs_record_district("park")
    $ activity_exit_jump = "map"
    $ activity_exit_name = "City Map"
    $ _sam_marcus_fired = False
    # Priority 2: pending conflict scenes
    if marcus_missed_pending and marcus_affection >= 30:
        call scene_marcus_missed_commitment
    # Priority 3: Sam × Marcus crossover (MAJOR; weekday morning only)
    if (sam_marcus_scene_pending and npc_here("sam") and npc_here("marcus")
            and 6 <= hour < 10 and major_scene_last_day != day):
        call scene_sam_marcus_park
        $ _sam_marcus_fired = True
    # Priority 5: Zoe rain shelter (auto-trigger, Thu/Fri afternoon, minor)
    if (not zoe_rain_done and zoe_met and zoe_affection >= 15
            and day % 7 in [3, 4] and 14 <= hour <= 18):
        call scene_zoe_rain_shelter
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    $ _group = group_scene_check()
    $ _group_lbl = group_scene_label(_group) if _group else ""
    hide screen people_here_dock
    # World Event Director
    $ _wed_amb = wed_poll_ambient("location_park")
    if _wed_amb:
        call expression _wed_amb
    $ _wed_per = wed_poll_personal("location_park")
    if _wed_per:
        call expression _wed_per
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_park")
    menu (screen="activity"):
        "Join [_group_lbl] →" if _group and not _sam_marcus_fired:
            call group_interact(_group[0], _group[1])
            jump location_park
        "Jog (1h)":
            scene expression ("park_jog_night" if hour >= 20 else "park_jog_day")
            show screen hud
            $ _jog_uses = activity_use_count_today("park_jog")
            $ mark_activity_used_today("park_jog")
            $ spend_time(1)
            if _jog_uses == 0:
                $ gain_stat("str", 8 if has_event("park_weather") else 4)
                if has_event("park_weather"):
                    "Perfect conditions. You hit your stride and don't stop. Best run in weeks."
                else:
                    "The air is crisp. Good start to the day."
            elif _jog_uses == 1:
                $ gain_stat("str", 4 if has_event("park_weather") else 2)
                "Second lap. Body's getting used to it — still worthwhile."
            else:
                "You're going through the motions. Not much left to gain today."
            jump location_park
        "Read a book (1.5h)":
            scene expression ("park_readbook_night" if hour >= 20 else "park_readbook_day")
            show screen hud
            $ _read_uses = activity_use_count_today("park_read")
            $ mark_activity_used_today("park_read")
            $ spend_time(1.5)
            if _read_uses == 0:
                $ gain_stat("int", 3)
                "A quiet hour on the bench. A few ideas shake loose."
            elif _read_uses == 1:
                $ gain_stat("int", 1)
                "You read, but your mind is elsewhere. A bit of INT, at least."
            else:
                "You stare at the page. The words blur. Nothing left to take in today."
            jump location_park
        "Play basketball (1.5h)" if hour < 20:
            scene basketball_court_day
            show screen hud
            $ spend_time(1.5)
            $ gain_stat("str", 8)
            "A pickup game on the court. Sweaty, competitive, good."
            jump location_park
        "Play guitar (Zoe's here) (2h)" if own_guitar and skill_music >= 3 and zoe_affection >= 30 and zoe_met and not zoe_park_guitar_done and (day % 7 in [3, 4]) and hour >= 14 and hour <= 17:
            call scene_guitar_zoe_busking
            jump location_park

# ── BEACH ─────────────────────────────────────────────────────────────
label location_beach:
    $ current_loc = "location_beach"
    $ fs_record_district("plaza")
    $ activity_exit_jump = "map"
    $ activity_exit_name = "City Map"
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    if not zoe_met and hour < 19:
        jump beach_meet_zoe
    if elle_affection >= 40 and not elle_pier_done and npc_talkable("elle"):
        jump elle_pier_scene
    # Elle Portugal payoff: fires after pier + decision message received
    if elle_decision_pending and npc_talkable("elle"):
        call scene_elle_portugal_payoff
    # Elle romance-opening beat (beach, after the pier scene)
    if (elle_pier_done and not elle_romance_open_done and npc_talkable("elle")
            and major_scene_last_day != day
            and elle_affection >= 40 and elle_trust >= 35):
        call scene_elle_romance_open
    $ _vis = location_sprites()
    if len(_vis) >= 1:
        show expression _vis[0][1] as npcsprite at sprite_r
    if len(_vis) >= 2:
        show expression _vis[1][1] as npcsprite2 at sprite_l
    $ _wed_amb = wed_poll_ambient("location_beach")
    if _wed_amb:
        call expression _wed_amb
    call screen beach_hub

# ── SANDBEACH (waterfront - swimming & sunbathing) ────────────────────
label location_sandbeach:
    $ current_loc = "location_sandbeach"
    $ activity_exit_jump = "location_beach"
    $ activity_exit_name = "Beach"
    hide screen people_here_dock
    if zoe_affection >= 40 and hour >= 20 and not zoe_beach_night_done:
        jump zoe_beach_night_scene
    scene expression ("sandbeach_night" if hour >= 19 else "sandbeach_day")
    show screen hud
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_sandbeach")
    menu (screen="activity"):
        "Search with metal detector (2h)" if own_metal_detector and hour < 18:
            $ _metal_owarn = _overlap_warning_text(2)
            if _metal_owarn:
                menu:
                    "[_metal_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_sandbeach
            if eli_met and not eli_find_done and npc_talkable("eli"):
                jump eli_find_scene
            else:
                scene sandbeach_day
                show screen hud
                $ spend_time(2)
                $ _sf = renpy.random.choice(["a rusted coin", "an old bottle cap", "a corroded key", "a waterproof lighter"])
                "Two hours sweeping the shoreline. You find [_sf]."
                jump location_sandbeach
        "Relax (1h)":
            $ spend_time(1)
            $ need_energy = min(100, need_energy + 12)
            "The sound of the waves. The city could be anywhere."
            jump location_sandbeach
        "Swim (1h)" if hour < 19:
            if too_tired():
                "You're too worn out to swim. Rest first."
                jump location_sandbeach
            scene sandbeach_swim_day
            show screen hud
            $ spend_time(1)
            $ need_energy = max(0, need_energy - 8)
            $ gain_stat("str", 3)
            "Cold, clear, and exactly what you needed. Your arms are properly tired."
            jump location_sandbeach
        "Sunbathe (1.5h)" if hour < 19:
            scene sandbeach_sunbath_day
            show screen hud
            $ spend_time(1.5)
            $ need_energy = min(100, need_energy + 15)
            $ gain_stat("app", 1)
            "Salt air and sun."
            jump location_sandbeach

# ── Zoe first meet - beach (daytime only, fires once) ─────────────────
label beach_meet_zoe:
    scene zoe_beach_1 with dissolve
    show screen hud
    "The beach out here is better than you expected. Not a resort strip - just sand and water and that particular quiet you only get when the city is far enough away to be decorative."
    "You find a clear patch and almost miss her."
    scene zoe_beach_2 with dissolve
    show screen hud
    "A girl, sitting cross-legged at the shoreline where the sand is still damp. A sketchbook balanced on her knees. Headphones around her neck - not on, just there, like she's not done with the world but keeping the option open."
    scene zoe_beach_3 with dissolve
    show screen hud
    "She holds a charcoal stick the way some people hold a cigarette - like it's part of the hand. The page is full of lines: the angle of waves, the smear of city buildings reflected in moving water."
    "She hasn't looked up once."
    menu:
        "Go over. Say something.":
            jump zoe_beach_approach
        "Stay where you are. You don't break someone's flow.":
            jump zoe_beach_watch

label zoe_beach_approach:
    "You cross the sand. She hears you coming - a slight adjustment of posture, but the charcoal keeps moving."
    "Then you're close enough that staying silent becomes its own thing, and she looks up."
    z "Can I help you?"
    scene zoe_beach_4 with dissolve
    show screen hud
    "Measured. Not unfriendly. The voice of someone who has ranked interrupt-interrupters before and is simply placing you."
    menu:
        "\"I was curious what you're drawing.\"":
            z "Waves. The way the buildings catch in the water when there's a swell."
            scene zoe_beach_5 with dissolve
            show screen hud
            "She angles the sketchbook toward you, briefly - just enough. The lines are loose and confident. Building reflections broken into something almost abstract."
            z "It doesn't translate in a photo. Which is the entire point."
            "She pulls it back."
            z "Most people who interrupt me out here want to know if I'm a 'real artist.' Like there's a counterfeit version."
            menu:
                "\"Are you?\"":
                    z "Define it and I'll tell you. I make things. Whether that qualifies depends on who's reviewing the grant."
                    "She gives you another look. Slower this time."
                    z "You're new. You've got the look."
                    $ zoe_affection += 2
                "\"What does the fake kind look like?\"":
                    z "Ha."
                    "Short. Real. She wasn't expecting that one."
                    z "Sells prints on a website. Talks a lot about their 'process' at dinner parties. But I try not to be mean about it."
                    z "You're new here. I can always tell."
                    $ zoe_affection += 4
            jump zoe_beach_shared
        "\"Hey - I'm [mc_name]. Just moved in.\"":
            z "Zoe."
            "She says it the way you sign a receipt. Efficient. Then she actually looks at you."
            z "New to the city or just new to this part of it?"
            menu:
                "\"New to the city. Still finding my feet.\"":
                    z "Then this is a good first beach. Locals mostly use it. The tourist one's two bays over - noisier, worse coffee, everyone's performing."
                    z "How long have you been here?"
                    "You tell her."
                    z "Long enough to find the beach, not long enough to know anyone. That's the good window, actually. Before the city starts feeling small."
                    $ zoe_affection += 3
                "\"New to this neighborhood. Still working out the city.\"":
                    z "It has a trick to it. Took me a year before I stopped getting turned around by the waterfront."
                    z "Pick a direction and walk until something's worth drawing. That's my method. It's not efficient, but it works."
                    "She seems satisfied you're not about to be annoying."
                    z "You're not the type who talks just to fill silence?"
                    menu:
                        "\"Not really.\"":
                            z "Good. Pull up some sand if you want. I've got ten more minutes of light."
                            $ zoe_affection += 4
                        "\"Sometimes. Depends on the silence.\"":
                            z "Fair. That's actually fair."
                            $ zoe_affection += 3
            jump zoe_beach_shared

label zoe_beach_watch:
    "You hang back. She's in that specific kind of concentration where interrupting would be like tripping a cable mid-charge. You know that state. You respect it."
    "A few minutes go by. The water's good out here. There's a container ship on the horizon - absurdly large, barely moving."
    "She erases something. Makes a short frustrated sound, almost inaudible. Re-draws the line. Erases it again."
    "Her shoulders drop slightly. There's something she's trying to get that isn't coming."
    "You understand that too."
    "Five minutes. Maybe more. Long enough that you stop counting."
    "She stretches - rolls her neck, sets the charcoal down on the sketchbook - and turns to look at the water."
    "Sees you immediately."
    scene zoe_beach_4 with dissolve
    show screen hud
    "A long pause. She looks at you, then back at the water, then at you again."
    z "...You've been standing there this whole time."
    "Not a question."
    z "I would have heard you leave."
    menu:
        "\"I didn't want to interrupt.\"":
            z "You were going to eventually. Everyone does."
            z "What stopped you?"
            menu:
                "\"You were getting somewhere. I could see it from here.\"":
                    "She blinks. Looks at the sketchbook. Then back at you."
                    z "...I wasn't, actually. But that's the right thing to look for."
                    $ zoe_affection += 5
                "\"Breaking flow felt rude.\"":
                    z "Most people don't think about that."
                    z "Sit down. You're making me self-conscious."
                    $ zoe_affection += 3
        "\"You looked like you were in it.\"":
            z "I was. I'm not anymore. Something I was chasing got away from me."
            "She doesn't sound angry. Just honest about it."
            z "You can come over. Since you've been hovering."
            $ zoe_affection += 3
        "[[Say nothing. Just hold up a hand - caught, fair enough.]]":
            "She stares at you for a second. Then a short exhale. Almost a laugh."
            z "Okay."
            z "Come sit. You're going to get a crick in your neck standing like that."
            $ zoe_affection += 4
    "You cross the sand and sit down next to her. She goes back to the page, or pretends to."
    scene zoe_beach_5 with dissolve
    show screen hud
    "The sea does that thing where it sounds like breathing."
    "After a minute:"
    z "What do you see? In the water."
    "It's a test. You can feel it."
    menu:
        "\"Reflections. The city upside-down.\"":
            z "Yeah. That's it exactly."
            z "Nobody looks at that. They look at the waves or the horizon. The interesting part's always in the middle somewhere."
            $ zoe_affection += 3
        "\"Just water. I'm not going to pretend otherwise.\"":
            z "Honest."
            z "The water's fine. It's what it does to everything around it that matters. But that comes with practice."
            $ zoe_affection += 2
        "\"The city. But softer.\"":
            "She looks at you sideways."
            z "Okay. You pass."
            $ zoe_affection += 4
    jump zoe_beach_shared

label zoe_beach_shared:
    "Eventually she closes the sketchbook. Taps it twice with one charcoal-stained finger like she's filing the whole session away."
    z "First time at this beach?"
    "You tell her it is."
    z "It's the right one. The other two are for people who want to be seen at the beach. This one's for people who actually want the beach."
    "She starts brushing sand from her jeans. There's charcoal on two fingers. She doesn't bother with it."
    z "I'm here most weeks when it's not raining. Trying to get the reflections right before the season changes and the light goes flat."
    "She tucks the sketchbook under her arm and stands."
    z "You're not the worst person to run into."
    "She says it the way someone gives a verdict. Which, you think, she basically did."
    "The smile that follows - half-turned away, like she didn't sign off on it - happens anyway."
    scene zoe_beach_6 with dissolve
    show screen hud
    "She walks off down the shore."
    scene zoe_beach_7 with dissolve
    show screen hud
    "You watch for a second."
    "You think: {i}that one's going to be interesting.{/i}"
    $ zoe_met = True
    $ spend_time(1)
    jump location_beach

# ── CENTRUM (downtown hub) ────────────────────────────────────────────
# Clicking the downtown district drops you "on the street" - pick a venue.
label location_centrum:
    scene expression ("centerstreet_night" if (hour >= 20 or hour < 6) else "centerstreet_day")
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_centrum")
    if _wed_amb:
        call expression _wed_amb
    # bottom bar of venue icons (screen handles navigation)
    call screen centrum_hub

# ── WAREHOUSE ─────────────────────────────────────────────────────────
label location_warehouse:
    $ current_loc = "location_warehouse"
    $ fs_record_district("warehouse")
    $ activity_exit_jump = "map"
    $ activity_exit_name = "City Map"
    hide screen people_here_dock
    if commitment_available("natalie_shift_1"):
        call phone_natalie_extra_scene
        jump location_warehouse
    scene warehouse
    show screen hud
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_warehouse")
    menu (screen="activity"):
        "Work a shift (8h)" if stat_str >= 25:
            if too_tired() or hour + 8 > DAY_END:
                "Too tired or too late to start a shift."
                jump location_warehouse
            $ _wh_owarn = _overlap_warning_text(8)
            if _wh_owarn:
                menu:
                    "[_wh_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_warehouse
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            scene pov_warehouse
            show screen hud
            $ _is_sun = (day % 7 == 6)
            $ spend_time(8)
            $ gain_money(170 if _is_sun else 115)
            $ gain_stat("str", 12)
            $ store.need_energy = max(0, store.need_energy - (80 if _is_sun else 40))
            if _is_sun:
                "Sunday overtime. Time-and-a-half and a sore back — Natalie's standard deal. Your back will remind you tomorrow."
            elif not natalie_met:
                $ natalie_met = True
                "Eight hours of hauling. At clock-out the floor manager, Natalie, sizes you up: \"Not useless. I'm Natalie. Don't make me remember your name for the wrong reasons.\""
                $ queue_phone_message("natalie", "First shift done. You held up. Get some sleep.", day, "warehouse_natalie_first")
            else:
                $ wh_shifts += 1
                if not wh_safety_done and wh_shifts >= 5:
                    call wh_damaged_shipment
                elif (wh_safety_done and wh_safety_followup_pending
                        and wh_shifts >= wh_safety_followup_shift
                        and not wh_safety_followup_done):
                    call wh_damaged_shipment_followup
                else:
                    "Eight hours of hauling and stacking. Your back aches; your wallet's heavier."
                    if renpy.random.random() < 0.15 and not message_already_queued("natalie_shift_invite"):
                        $ queue_phone_message("natalie", "Short-handed Saturday. You up for an extra shift? Time and a half, same terms.", day + 1, "natalie_shift_invite", responses=_NATALIE_SHIFT_RESP)
            if _work_event_roll("warehouse"):
                call work_event_warehouse
            jump location_warehouse
        "Apply for work" if stat_str < 25:
            show natalie_normal at sprite_r
            nat "Come back when you can actually lift. STR 25, minimum. Next."
            hide natalie_normal
            jump location_warehouse

# ── HOSPITAL ──────────────────────────────────────────────────────────
label location_hospital:
    $ current_loc = "location_hospital"
    $ fs_record_district("szpital")
    $ activity_exit_jump = "map"
    $ activity_exit_name = "City Map"
    hide screen people_here_dock
    # Priority 3: pending breakthrough scenes (major) — one per day
    if major_scene_last_day != day:
        if lena_shoulder_pending and lena_met:
            call scene_lena_shoulder_gesture
    scene expression ("hospital_night" if (hour >= 20 or hour < 6) else "hospital1")
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_hospital")
    if _wed_amb:
        call expression _wed_amb
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_hospital")
    menu (screen="activity"):
        "Cosmetic treatment ($350, 2h)":
            if money < 350:
                "The clinic coordinator slides the price sheet back. You can't cover $350 today."
            else:
                $ spend_time(2)
                $ gain_money(-350)
                $ gain_stat("app", 2)
                $ cosmetic_boost_until = day + 7
                "A minor procedure. Subtle, but noticeable — you leave looking especially polished. It'll last about a week."
            jump location_hospital

        # Medicine career (shares the engine + CAREERS["hospital"]).
        "Work a shift (8h)" if job_id == "hospital":
            if too_tired() or hour + 8 > DAY_END:
                "You're too tired or it's too late to start a shift."
                jump location_hospital
            $ _hosp_owarn = _overlap_warning_text(8)
            if _hosp_owarn:
                menu:
                    "[_hosp_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_hospital
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            scene pov_doctor
            show screen hud
            $ _tired = do_shift("hospital", 8)
            $ hosp_shifts += 1
            if not lena_met:
                call hosp_first_day
            elif not hosp_task_1_done and hosp_shifts >= 3 and job_rank == 0:
                call hosp_task_1
            elif hosp_task_1_done and not hosp_npc1_done and hosp_shifts >= 5 and job_rank == 0:
                call hosp_npc1_lena
            elif hosp_npc1_done and not hosp_npc2_done and hosp_shifts >= 7 and job_rank == 0:
                call hosp_npc2_lena
            elif hosp_npc2_done and lena_case_observation_done and not hospital_hard_case_done:
                call hospital_hard_case_scene
            elif (hospital_hard_case_done and hospital_hard_case_followup_pending
                    and hosp_shifts >= hospital_hard_case_followup_shift
                    and not hospital_hard_case_followup_done):
                call hospital_hard_case_followup
            elif (hosp_npc2_done and not hosp_review_done
                    and job_performance >= 100 and can_promote() and job_rank == 0
                    and ((not lena_case_observation_done and not hospital_hard_case_done)
                     or (hospital_hard_case_done
                         and hospital_hard_case_followup_done
                         and hosp_shifts >= hospital_hard_case_followup_shift + hospital_hard_case_review_extra_shifts))):
                call hosp_review_assistant
            else:
                if commitment_available("lena_case_1"):
                    call phone_lena_case_scene
                elif _tired:
                    "Exhausted and unfed, you fumble a chart and get chewed out. A shift like this sets you back."
                else:
                    "Charts, rounds, a dozen small crises handled. You earned the coffee."
            # A hard case is a random event, not a result of poor performance.
            # Performance may change the debrief dialogue, but not scene availability.
            # ponytail: ceiling is 25%/shift once prerequisites met; upgrade path is
            #   a dedicated case-type event if the hospital arc gains scripted shifts.
            if (not lena_shoulder_done and not lena_shoulder_pending
                    and lena_break_room_done and hosp_shifts >= 10
                    and job_rank >= 1 and renpy.random.random() < 0.25):
                $ hospital_hard_case_pending = True
                if job_performance >= 70:
                    "You did everything correctly. The outcome wasn't yours to control."
                else:
                    "There are things to review. But not tonight."
            if _work_event_roll("hospital"):
                call work_event_hospital
            if not lena_rooftop_done and job_rank >= 1 and lena_trust >= 25 and hour >= 22:
                jump lena_rooftop_scene
            jump location_hospital

        "Ask about a promotion" if job_id == "hospital" and can_promote():
            $ _trial = cur_rank().get("trial")
            $ _trial_done = store.promotion_trials.get(("hospital", job_rank), False)
            if _trial and not _trial_done:
                call hospital_trial_resident
            else:
                if promote():
                    "You're handed a new badge. The attending smiles. \"Welcome to residency.\""
                    if job_rank >= 1 and not lena_met:
                        $ lena_met = True
                        "A doctor mid-coffee catches you in the hall. \"Fresh resident? I'm Lena. You'll live. Probably.\" You've got a colleague now."
                else:
                    "\"Not quite there. Keep at it.\""
            jump location_hospital

        "Drop off your CV" if job_id is None:
            show drlena_normal at sprite_r
            if can_apply("hospital"):
                "A doctor at the desk skims your file. \"Med Student it is. Try not to faint.\" You're in."
                hide drlena_normal
                $ apply_job("hospital")
            else:
                "A tired doctor hands your CV back. \"Not there yet - Medicine 2, INT 30, CHR 15 minimum. The college teaches it.\""
                hide drlena_normal
                $ _fs_career_rejection()
            jump location_hospital

        "Find Dr. Lena on break (0.5h)" if lena_affection >= 20 and lena_trust >= 15 and lena_met and not lena_break_room_done and hour >= 12 and hour <= 14:
            call scene_lena_hospital_break_room
            jump location_hospital


        "Quit medicine" if job_id == "hospital":
            $ quit_job()
            "You hang up the coat. Not everyone's built for it."
            jump location_hospital


# ── THE HUB (IT career) ───────────────────────────────────────────────
label location_hub:
    $ current_loc = "location_hub"
    $ fs_record_district("centrum")
    if not venue_open("hub"):
        "The Hub is shut. Back at 08:00."
        jump map
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    # Priority 3: pending breakthrough scenes (major) — one per day, evening only
    if major_scene_last_day != day:
        if eli_deploy_pending and eli_met and hour >= 19:
            call scene_eli_deploy_hug
    scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
    show screen hud
    $ _wed_amb = wed_poll_ambient("location_hub")
    if _wed_amb:
        call expression _wed_amb
    menu (screen="activity"):
        "Work a shift (8h)" if job_id == "it":
            $ _it_h = 6 if skill_prog >= 5 else 8
            if hour + _it_h > DAY_END:
                "Too late to start a full shift today."
                jump location_hub
            if too_tired():
                "You're running on empty. Your lead would send you home. Sleep first."
                jump location_hub
            $ _it_owarn = _overlap_warning_text(_it_h)
            if _it_owarn:
                menu:
                    "[_it_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump location_hub
            scene hub_pov
            show screen hud
            $ _tired = do_shift("it", _it_h)
            $ it_shifts += 1
            if not eli_met:
                call it_first_day
            elif not it_task_1_done and it_shifts >= 3:
                call it_task_1
            elif it_task_1_done and not it_npc1_done and it_shifts >= 5:
                call it_npc1_eli
            elif it_npc1_done and not it_npc2_done and it_shifts >= 7:
                call it_npc2_eli
            elif it_npc2_done and not it_incident_done:
                call it_production_incident
            elif (it_incident_done and it_incident_followup_pending
                    and it_shifts >= it_incident_followup_shift
                    and not it_incident_followup_done):
                call it_production_incident_followup
            elif (it_npc2_done and not it_review_done
                    and job_performance >= 100 and can_promote()
                    and it_incident_followup_done
                    and it_shifts >= it_incident_followup_shift + it_incident_review_extra_shifts):
                call it_review_junior
            else:
                if commitment_available("eli_debug_1"):
                    call phone_eli_debug_scene
                elif _tired:
                    "Running on fumes, you ship bugs and miss the standup. At least the commit went through."
                else:
                    "Headphones on, heads down. A good day's work shipped."
            if _work_event_roll("it"):
                call work_event_it
            jump location_hub

        "Ask about a promotion" if job_id == "it" and can_promote():
            $ _trial = cur_rank().get("trial")
            $ _trial_done = store.promotion_trials.get(("it", job_rank), False)
            if _trial and not _trial_done:
                call it_trial_team_lead
            else:
                if promote():
                    "Your lead grins. \"Earned it.\" New title, better pay, higher bar."
                else:
                    "\"Strong quarter - but you need the skills for the next rung first.\""
            jump location_hub

        "Apply for a dev role" if job_id is None:
            if can_apply("it"):
                $ apply_job("it")
                "You nail the interview. Junior Dev at The Hub. Welcome to the grind."
            else:
                "A dev lead skims your work and slides it back. \"Not yet - Programming 2 and INT 30 minimum. The college runs courses.\""
                $ _fs_career_rejection()
            jump location_hub

        "Quit this job" if job_id == "it":
            $ quit_job()
            "You hand in your notice. Free again - broke soon, but free."
            jump location_hub

        "Introduce Eli and Zoe (2h)" if own_programming_kit and eli_affection >= 35 and zoe_affection >= 30 and eli_met and zoe_met and not eli_meets_zoe_done:
            call scene_eli_meets_zoe
            jump location_hub

        "Work on Eli's open source project (2h)" if own_programming_kit and eli_affection >= 30 and eli_trust >= 25 and eli_met and not programming_kit_eli_done and hour >= 17:
            call scene_programming_kit_eli
            jump location_hub


# ── CITY COLLEGE (learn professional skills) ──────────────────────────
label location_college:
    $ current_loc = "location_college"
    $ fs_record_district("centrum")
    if not venue_open("university"):
        if day % 7 >= 5:
            "The college is closed on weekends. Back Monday at 08:00."
        else:
            "The college is closed for the day. Back at 08:00."
        jump map
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "Downtown"
    scene college_day
    show screen hud
    hide screen people_here_dock
    $ _wed_amb = wed_poll_ambient("location_college")
    if _wed_amb:
        call expression _wed_amb
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_college")
    $ _prog_cost = course_cost("prog")
    $ _med_cost  = course_cost("med")
    $ _biz_cost  = course_cost("biz")
    $ _art_cost  = course_cost("art")
    menu (screen="activity"):
        "Programming ($[_prog_cost], 3h, -22 energy)":
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            call college_course("prog")
            jump location_college
        "Medicine ($[_med_cost], 3h, -22 energy)":
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            call college_course("med")
            jump location_college
        "Business ($[_biz_cost], 3h, -22 energy)":
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            call college_course("biz")
            jump location_college
        "Art ($[_art_cost], 3h, -22 energy)":
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            call college_course("art")
            jump location_college
        "Degree examinations →" if skill_med >= 3 or skill_prog >= 3 or skill_biz >= 3:
            hide npcsprite
            hide npcsprite2
            hide npcsprite3
            hide npcsprite4
            hide screen people_here_dock
            jump location_college_exams


label location_college_exams:
    $ activity_exit_jump = "location_college"
    $ activity_exit_name = "Back"
    scene college_day
    show screen hud
    $ _mb_cost  = DEGREE_EXAMS["med_bach"]["cost"]
    $ _mm_cost  = DEGREE_EXAMS["med_mast"]["cost"]
    $ _pb_cost  = DEGREE_EXAMS["prog_bach"]["cost"]
    $ _pm_cost  = DEGREE_EXAMS["prog_mast"]["cost"]
    $ _bb_cost  = DEGREE_EXAMS["biz_bach"]["cost"]
    $ _bm_cost  = DEGREE_EXAMS["biz_mast"]["cost"]
    menu (screen="activity"):
        "Medicine Bachelor's ($[_mb_cost], 8h) [[Req: Med Lv4]]":
            if not can_sit_exam("med_bach") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("med_bach")
            "Eight hours of exams across three halls. You pass. Medicine — Bachelor's earned."
            jump location_college_exams
        "Medicine Master's ($[_mm_cost], 8h) [[Req: Med Lv7]]":
            if not can_sit_exam("med_mast") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("med_mast")
            "The hardest day you've had at a desk. Medicine — Master's earned."
            jump location_college_exams
        "CS Bachelor's ($[_pb_cost], 8h) [[Req: Prog Lv4]]":
            if not can_sit_exam("prog_bach") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("prog_bach")
            "Theory, algorithms, a written section. Computer Science — Bachelor's earned."
            jump location_college_exams
        "CS Master's ($[_pm_cost], 8h) [[Req: Prog Lv7]]":
            if not can_sit_exam("prog_mast") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("prog_mast")
            "Eight hours of advanced systems theory. Computer Science — Master's earned."
            jump location_college_exams
        "Business Bachelor's ($[_bb_cost], 8h) [[Req: Biz Lv4]]":
            if not can_sit_exam("biz_bach") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("biz_bach")
            "Case studies, finance, a group presentation. Business — Bachelor's earned."
            jump location_college_exams
        "Business Master's ($[_bm_cost], 8h) [[Req: Biz Lv7]]":
            if not can_sit_exam("biz_mast") or too_tired():
                "Requirements not met or too tired."
                jump location_college_exams
            $ sit_exam("biz_mast")
            "Strategy, leadership, one brutal oral exam. Business — Master's earned."
            jump location_college_exams


label college_course(key):
    if too_tired():
        "You're too exhausted to absorb anything. Come back after some sleep."
        return
    $ _crs_owarn = _overlap_warning_text(3)
    if _crs_owarn:
        menu:
            "[_crs_owarn]\nContinue anyway?"
            "Continue":
                pass
            "Go back":
                return
    scene college_study
    show screen hud
    $ _r = take_course(key)
    if _r == "money":
        "You can't cover the course fee at your current level. Earn more first."
    elif _r == "max":
        "You've maxed this one out - nothing more they can teach you here."
    else:
        "Three hours of lectures and exercises. It's starting to click."
        $ fs_mark("study_done")
        $ fs_mark("outside_activity")
    return

# ── SLEEP ─────────────────────────────────────────────────────────────
label action_sleep_menu:
    scene cheap_home_sleep
    show screen hud
    menu (screen="activity"):
        "Until morning (8h) — new day, full rest":
            $ _sleep_owarn = _overlap_warning_text(8)
            if _sleep_owarn:
                menu:
                    "[_sleep_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump action_sleep_menu
            jump action_sleep
        "6 hours (+60 energy)":
            $ _sleep_owarn = _overlap_warning_text(6)
            if _sleep_owarn:
                menu:
                    "[_sleep_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump action_sleep_menu
            $ spend_time(6)
            $ need_energy = min(100, need_energy + 60)
            "Six hours. You wake in the dark, properly rested."
            jump location_home_actions
        "4 hours (+40 energy)":
            $ _sleep_owarn = _overlap_warning_text(4)
            if _sleep_owarn:
                menu:
                    "[_sleep_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump action_sleep_menu
            $ spend_time(4)
            $ need_energy = min(100, need_energy + 40)
            "Four hours. Functional, if not fresh."
            jump location_home_actions
        "2 hours (+20 energy)":
            $ _sleep_owarn = _overlap_warning_text(2)
            if _sleep_owarn:
                menu:
                    "[_sleep_owarn]\nContinue anyway?"
                    "Continue":
                        pass
                    "Go back":
                        jump action_sleep_menu
            $ spend_time(2)
            $ need_energy = min(100, need_energy + 20)
            "Two hours. Takes the edge off, nothing more."
            jump location_home_actions
        "Stay up":
            jump location_home_actions

label action_sleep:
    $ new_day()
    scene expression home_bg()
    show screen hud
    $ datestr = "Day %d - %s" % (day + 1, day_name(day))
    "You sleep through the night.\n[datestr]"
    jump map

# Neglect consequences - checked at the map hub (between activities), so it never
# interrupts mid-action and only fires at real extremes.
label check_collapse:
    if need_hunger <= 0:
        scene expression Solid("#000000") with fade
        "The edges of everything go white. You don't remember hitting the floor."
        scene hospital1 with fade
        show screen hud
        "You come round in the ER, a drip in your arm. Skipping every meal finally caught up with you - and the bill isn't cheap."
        $ gain_money(-100)
        $ need_hunger = 60
        $ need_energy = 70
        if job_id is not None:
            $ job_performance = max(0, job_performance - 15)
        $ new_day()
        return
    # energy==0 no longer causes collapse - demanding activities become unavailable instead.
    if not warned_today and (need_hunger < 22 or need_energy < 22 or need_hygiene < 18):
        $ warned_today = True
        if not tip_need_critical_shown:
            $ tip_need_critical_shown = True
            $ renpy.notify("A critical need can block demanding activities — recover early.")
        else:
            $ renpy.notify("Running low - eat, sleep, or shower soon.")
    return

# LEGACY SAVE-COMPATIBILITY STUB.
# take_metro existed in older saves. This label exists only so those save files
# can resume without an "unknown label" error. It immediately redirects to the
# city map. No time is spent, no money is charged, no event fires, no menu shows.
# No new gameplay or UI element should ever jump here.
label take_metro:
    jump map

# ── MAP ────────────────────────────────────────────────────────────────
label map:
    call check_collapse
    $ expire_late_commitments()
    $ notify_available_commitments()
    $ fs_mark("map_visited")
    scene map_city
    show screen hud
    if not tip_map_shown:
        $ tip_map_shown = True
        call screen tutorial_overlay("CITY MAP", "Choose a district or location to travel there immediately. Travel does not advance time, but locations have schedules and opening hours.")
    call screen city_map

# ── NORA - CLOSING TIME ────────────────────────────────────────────────
# Trigger: nora_affection >= 40, hour >= 19, not nora_closing_done
label nora_closing_scene:
    $ nora_closing_done = True
    scene cafenight with dissolve
    show screen hud
    "The café looks different at this hour. Chairs stacked on half the tables. One lamp above the counter. The espresso machine, finally, quiet."
    scene nora_closing_1 with dissolve
    show screen hud
    n "Closing time. Lucky for you there's one cup left in the pot. Come in or don't."
    "She doesn't wait for an answer - pours two cups, sets them on a table, sits down. You sit across from her."
    scene nora_closing_2 with dissolve
    show screen hud
    menu:
        "\"Didn't realise it was so late.\"":
            n "It always is, after a shift. Time does something weird behind the counter."
        "\"I was hoping you'd still be here.\"":
            $ nora_affection = min(100, nora_affection + 1)
            n "That's a thing to say."
    scene nora_closing_3 with dissolve
    show screen hud
    n "You've been in a lot lately. What are you actually looking for in this city?"
    menu:
        "\"A reason to stay.\"":
            $ nora_affection = min(100, nora_affection + 3)
            n "That's the honest answer."
            n "I hope you find one."
        "\"Money, mostly. And something that doesn't feel like wasted time.\"":
            $ nora_trust = min(100, nora_trust + 2)
            n "Yeah. That's most people. They just don't say it out loud."
        "\"Still figuring that out.\"":
            $ nora_affection = min(100, nora_affection + 2)
            n "Same, honestly. I've been figuring it out for three years and counting."
    scene nora_closing_4 with dissolve
    show screen hud
    "She wraps both hands tighter around the cup."
    n "I was supposed to be studying nursing right now. Deferred a year. Then another. Henry offered me full-time and the timing just... worked."
    "She glances at her hands."
    n "I'm good at this job. That's the annoying part. When you're bad at something it's easy to leave."
    scene nora_closing_5 with dissolve
    show screen hud
    menu:
        "\"Then go. You're clearly just waiting for permission.\"":
            $ nora_trust = min(100, nora_trust + 5)
            $ nora_affection = min(100, nora_affection + 4)
            n "...You make it sound that easy."
        "\"Being good at something isn't a reason to stay stuck in it.\"":
            $ nora_trust = min(100, nora_trust + 3)
            $ nora_affection = min(100, nora_affection + 3)
            n "Henry would cope."
            "She says it quietly, like she's testing the idea."
        "\"What's actually stopping you?\"":
            $ nora_trust = min(100, nora_trust + 4)
            $ nora_affection = min(100, nora_affection + 2)
            "She pauses a long time."
            n "Nothing good."
        "\"Let me walk you home.\"" if nora_affection >= 50:
            $ nora_trust = min(100, nora_trust + 4)
            $ nora_affection = min(100, nora_affection + 4)
            n "It's late and I live close."
            "Beat."
            n "You can tell me what you're running from on the way."
        "\"Let me walk you home.\"" if nora_affection < 50:
            $ nora_trust = min(100, nora_trust + 2)
            $ nora_affection = min(100, nora_affection + 2)
            n "I'm fine - it's five minutes."
            "Beat."
            n "Ask me again sometime."
    scene nora_closing_6 with dissolve
    show screen hud
    "She puts on her coat. Keys in hand. She looks around the café for a second - the habit of checking everything before she leaves."
    n "You're easier to talk to when there's no counter in the way."
    "She unlocks the door, holds it open."
    scene nora_closing_7 with dissolve
    show screen hud
    n "Don't tell Henry I gave away his last coffee."
    "The café lights go off as you step outside."
    if get_romance_state("nora") in ("unopened", "friends"):
        menu:
            "\"Next time — not as a customer.\"" if nora_affection >= 50:
                $ set_romance_state("nora", "interested", source="nora_closing_scene")
                $ add_romance_momentum("nora", 15)
                $ add_relationship_memory("nora", "nora_closing_direction_romance", "Said it outside the café after hours")
                "She stops walking. Just for a second."
                n "That's a thing to say in the dark."
                "She doesn't walk it back."
            "\"Same time next week?\"":
                $ set_romance_state("nora", "friends", source="nora_closing_scene")
                $ add_romance_momentum("nora", 5)
                $ add_relationship_memory("nora", "nora_closing_direction_platonic", "Kept it easy after closing")
                n "I'll be here."
                "She says it lightly. The door is still open, in more ways than one."
            "[[Walk. Say nothing.]]":
                $ add_romance_momentum("nora", 2)
                $ _apply_trust("nora", 1)
                $ add_relationship_memory("nora", "nora_closing_direction_withdrawal", "Walked in silence after closing")
                "She doesn't try to fill it. Neither do you."
    jump map

# ── ELLE - BEST SPOT PAST THE PIER ────────────────────────────────────
# Trigger: elle_affection >= 40, Wednesday 16-19, elle present — fires once
label elle_pier_scene:
    $ elle_pier_done = True
    scene elle_pier_1 with dissolve
    show screen hud
    "She doesn't head toward the main strip. She turns the other way, past the pier, where the sand gets quieter."
    el "Come on. I'll show you the actual beach."
    scene elle_pier_2 with dissolve
    show screen hud
    el "Nobody comes this far down. Which is exactly the point."
    "She drops onto a rock and kicks off her sandals. The water out here is the same water, but it feels different without the noise behind it."
    scene elle_pier_3 with dissolve
    show screen hud
    el "I come here when I need to not be anywhere specific, you know?"
    menu:
        "\"You come here a lot?\"":
            $ elle_affection = min(100, elle_affection + 1)
            el "Every Wednesday I can manage. Some weeks it's the only thing that feels like mine."
        "\"What are you running from?\"":
            el "That's a question."
            "She looks at you sideways. Not offended. Considering."
            el "Not running. Just... not arriving yet. There's a difference."
    scene elle_pier_4 with dissolve
    show screen hud
    el "Back home everyone always asks what I'm doing with my life. Out here nobody knows I exist."
    "She says it like it's a relief, not a complaint."
    menu:
        "\"What are you actually doing with your life?\"":
            $ elle_trust = min(100, elle_trust + 3)
            el "Currently? Sitting on a rock, avoiding that exact question. You're terrible at this."
            "She's smiling when she says it."
        "\"Sounds like you needed to disappear for a while.\"":
            $ elle_affection = min(100, elle_affection + 2)
            $ elle_trust = min(100, elle_trust + 2)
            el "Yeah. Something like that."
            "A pause. The sea fills it better than words would."
        "\"I know that feeling.\"":
            $ elle_trust = min(100, elle_trust + 3)
            el "Do you?"
            "She looks at you properly for the first time since you sat down."
            el "Good. Then you get it."
    scene elle_pier_5 with dissolve
    show screen hud
    "You sit there without saying much. The light goes gold and orange."
    scene elle_pier_6 with dissolve
    show screen hud
    el "We should do something normal sometime. Not a beach. Something where we have to actually talk."
    menu:
        "\"Is that an invitation?\"":
            $ elle_affection = min(100, elle_affection + 2)
            el "If you want it to be."
        "\"I'd like that.\"":
            $ elle_affection = min(100, elle_affection + 2)
            el "Me too."
    "You head back through the city."
    jump map

# ── DR. LENA - ROOFTOP, 3 A.M. ────────────────────────────────────────
# Trigger: hospital job rank >= 1, lena_trust >= 25, hour >= 22 — fires once after a night shift
label lena_rooftop_scene:
    $ lena_rooftop_done = True
    scene hospital_rooftop_night with dissolve
    show screen hud
    "The stairwell door is already propped open. You weren't planning to come up here — but the ward feels impossible right now and the sky is the only ceiling that isn't fluorescent."
    scene lena_rooftop_1 with dissolve
    show screen hud
    lena "I figured someone else would come up eventually."
    "She has a paper cup of something. She doesn't look like a doctor right now. She looks like someone who's been at it too long."
    menu:
        "\"Rough shift?\"":
            lena "Twelve beds, two residents calling in. Standard chaos."
            "She says it flat. Not complaining — just cataloguing."
        "\"I didn't know this was up here.\"":
            lena "Most people don't bother finding out. The view's not worth it unless you need it to be."
    scene lena_rooftop_2 with dissolve
    show screen hud
    "You sit on the ledge beside her. The city is quiet at this hour in a way it never is from ground level."
    lena "You did well tonight, by the way. That tachycardia in bed seven — you caught it before I did."
    scene lena_rooftop_3 with dissolve
    show screen hud
    lena "I keep thinking I'll get used to it. The nights where you can't actually fix anything."
    "She's looking out at the city, not at you."
    lena "You just manage. Make it slightly less bad. Go home. Come back."
    menu:
        "\"That sounds exhausting.\"":
            $ lena_trust = min(100, lena_trust + 3)
            lena "It is. But you don't say that out loud usually."
            "A pause."
            lena "It's easier up here."
        "\"Is it worth it?\"":
            $ lena_trust = min(100, lena_trust + 4)
            lena "Ask me on a good day and I'll say yes immediately."
            lena "Ask me at 3am after a shift like tonight and I'll tell you I don't know."
            lena "Both answers are true."
        "\"You're not just managing. You're very good at this.\"":
            $ lena_affection = min(100, lena_affection + 3)
            $ lena_trust = min(100, lena_trust + 2)
            "She glances at you. Something shifts in her expression."
            lena "That's... actually something I needed to hear tonight. Thank you."
    scene lena_rooftop_4 with dissolve
    show screen hud
    "She finishes whatever's in the cup. Sets it down. Looks at the city like she's still processing something she saw eight hours ago."
    lena "I chose this. I want to be clear about that. I'm not here by accident."
    lena "I just didn't account for what it costs."
    scene lena_rooftop_5 with dissolve
    show screen hud
    "She stands, smooths her jacket, picks up the cup."
    lena "Get some sleep. You're back in seven hours."
    "She heads for the door. Stops."
    lena "It helps. Having someone up here who gets it."
    "You take the stairs down."
    $ add_relationship_memory("lena", "lena_rooftop", "The rooftop")
    jump map


# ── ELI — BEACH METAL DETECTOR ────────────────────────────────────────
label eli_find_scene:
    $ eli_find_done = True
    scene sandbeach_day with dissolve
    show screen hud
    "You pull out the metal detector. Eli watches like they're deciding whether to take this seriously."
    scene eli_find_1 with dissolve
    show screen hud
    eli "Does that thing actually find anything?"
    "You tell them: sometimes."
    eli "Define sometimes."
    menu:
        "\"Bottle caps, mostly.\"":
            eli "That's bleak."
            $ _apply_aff("eli", 1)
        "\"You'd be surprised.\"":
            eli "I'm already surprised you own this."
            $ _apply_aff("eli", 2)
    scene eli_find_2 with dissolve
    show screen hud
    "You sweep the shoreline. Eli walks alongside, not helping exactly, but present."
    "There's a rhythm to it — step, sweep, listen."
    "First hit: a 2009 euro coin, warped from salt."
    eli "Keep it?"
    menu:
        "\"It's something.\"":
            "You pocket it."
            $ _apply_trust("eli", 1)
        "\"It's a coin.\"":
            "You toss it back into the sand for the next person."
            $ _apply_aff("eli", 1)
    scene eli_find_3 with dissolve
    show screen hud
    "A second hit — louder. Eli stops talking."
    "You dig. A key, old enough that you can't tell what it opened."
    eli "Someone lost that and had a very bad day."
    "A pause. The sea is unhelpfully indifferent."
    eli "I've never thought about how many things just... stay in the ground. Permanently lost."
    $ _apply_trust("eli", 2)
    scene eli_find_4 with dissolve
    show screen hud
    "Third hit. Strong. Different frequency from the others."
    "You dig for a minute. Something metallic, small. You pull it out."
    menu:
        "\"It's a ring.\"":
            scene eli_find_ring_bonus with dissolve
            show screen hud
            "Gold band. Old. Still intact."
            eli "...huh."
            "They take it carefully. Look at it."
            eli "There's probably no one to give this back to."
            menu:
                "\"Keep it.\"":
                    eli "I feel like we're supposed to feel something about this."
                    "You both look at it for a moment."
                    $ gain_money(15)
                    $ _apply_aff("eli", 3)
                "\"Leave it somewhere visible.\"":
                    "You put it on top of a nearby rock. It won't be there tomorrow. But it's not yours."
                    eli "That's probably the right call."
                    $ _apply_trust("eli", 3)
        "\"Old token. Transport or something.\"":
            eli "Way less dramatic."
            $ gain_money(2)
            $ _apply_aff("eli", 1)
    scene eli_find_5 with dissolve
    show screen hud
    "You pack the detector away. The light is going orange. Eli sits on the sand."
    eli "I'd been meaning to say — you're easier to be around than I expected. At the start."
    "You ask what they expected."
    eli "Someone more eager. You're not."
    menu:
        "\"Is that a compliment?\"":
            eli "It's an observation. But yes."
            $ _apply_aff("eli", 3)
            $ _apply_trust("eli", 2)
        "Say nothing. Let it land.":
            "Eli nods once. Conversation apparently complete."
            $ _apply_trust("eli", 3)
    jump location_sandbeach


# ── MARTHA — ROOFTOP BAR ──────────────────────────────────────────────
label martha_rooftop_scene:
    $ martha_rooftop_done = True
    scene bar_rooftop_night with dissolve
    show screen hud
    "Martha suggested this place. End of quarter, she said. Good enough reason."
    "The rooftop bar is the kind of place that costs more than it shows."
    scene martha_rooftop_1 with dissolve
    show screen hud
    "She's already there. Different from the office — not looser exactly. Less constructed."
    show martha_dress_normal at sprite_r, react_nod
    ma "You found it."
    "She says it like she wasn't entirely sure you would."
    menu:
        "\"You gave good directions.\"":
            ma "I gave you a postcode and a floor number."
            $ _apply_aff("martha", 1)
        "\"I almost went to the wrong bar.\"":
            ma "There are three on this block. It's a recurring problem."
            $ _apply_aff("martha", 2)
    scene martha_rooftop_2 with dissolve
    show screen hud
    hide martha_dress_normal
    "Drinks. The city from above. She's looking at something middle-distance."
    show martha_dress_normal at sprite_r
    ma "I wanted to say something I can't say in the office."
    ma "You've been handled badly there. By a few people. Before you were established."
    ma "I noticed. I didn't always act on it. I wanted you to know I noticed."
    $ _apply_trust("martha", 4)
    menu:
        "\"Why are you telling me now?\"":
            ma "Because you're past the point where it can be used against you."
            "She says it practically. The kindness is in the timing."
            $ _apply_trust("martha", 2)
        "\"Thank you.\"":
            "She looks briefly uncomfortable with the gratitude."
            show martha_dress_normal at sprite_r, react_step_back
            ma "Don't. Just — don't let it happen to the next person."
            $ _apply_aff("martha", 3)
    scene martha_rooftop_3 with dissolve
    show screen hud
    hide martha_dress_normal
    "Halfway through the second drink, the city gets louder and she gets quieter."
    show martha_dress_normal at sprite_r
    ma "I had a plan when I joined Nexus. Very specific. Five years."
    ma "That was nine years ago."
    menu:
        "\"What changed?\"":
            ma "The work kept being interesting. I kept being good at it."
            ma "Those two things are harder to walk away from than I planned for."
            $ _apply_aff("martha", 2)
            $ _apply_trust("martha", 2)
        "\"Is that a bad thing?\"":
            show martha_dress_laugh at sprite_r, react_nod
            ma "Ask me in another nine years."
            "Something almost like a smile."
            $ _apply_aff("martha", 3)
        "\"I think you like it more than you admit.\"":
            "She looks at you for a moment."
            ma "That's probably true."
            $ _apply_aff("martha", 2)
            $ _apply_trust("martha", 3)
    scene martha_rooftop_4 with dissolve
    show screen hud
    hide martha_dress_normal
    "She pours the last of the bottle into your glass before her own. You notice."
    show martha_dress_normal at sprite_r, react_lean_in
    ma "What do you actually want from this? Not the title. Not the review scores."
    "The question is specific enough that you believe she wants an actual answer."
    menu:
        "\"Something I built. That stays.\"":
            ma "That's a real answer."
            "She says it like it surprised her."
            $ _apply_trust("martha", 3)
            $ _apply_aff("martha", 2)
        "\"I don't know yet. I'm still figuring that out.\"":
            ma "That's a better answer than most people give at your stage."
            ma "Most people have a rehearsed version. Yours is honest."
            $ _apply_trust("martha", 4)
        "\"Honestly? To stop worrying about it.\"":
            ma "..."
            ma "That's the most honest thing anyone's said to me at this bar."
            $ _apply_aff("martha", 4)
            $ _apply_trust("martha", 2)
    scene martha_rooftop_5 with dissolve
    show screen hud
    hide martha_dress_normal
    "The bar fills up around you. You stop noticing."
    show martha_dress_normal at sprite_r
    "At some point she refills your glass and says:"
    ma "You're going to be good at this. Whatever you choose."
    "She doesn't wait for a response. Just finishes her drink."
    $ _apply_aff("martha", 3)
    scene martha_rooftop_6 with dissolve
    show screen hud
    hide martha_dress_normal
    "Outside. The city is warm and continuous below."
    show martha_dress_normal at sprite_r
    ma "Same time next quarter."
    "She doesn't frame it as a question."
    if get_romance_state("martha") in ("unopened", "friends") and martha_affection >= 55:
        menu:
            "\"Same time. Somewhere different.\"":
                $ set_romance_state("martha", "interested", source="martha_rooftop_scene")
                $ add_romance_momentum("martha", 15)
                $ add_relationship_memory("martha", "martha_rooftop_direction_romance", "Said something intentional on the rooftop")
                "She's quiet for a moment."
                show martha_dress_normal at sprite_r, react_step_back
                ma "Is that what this was."
                "Not a question. She's filing it."
                ma "I'll note that."
                "She walks toward the stairs without elaborating."
            "\"Same time next quarter.\"":
                $ set_romance_state("martha", "friends", source="martha_rooftop_scene")
                $ add_romance_momentum("martha", 5)
                $ add_relationship_memory("martha", "martha_rooftop_direction_platonic", "Matched her register exactly")
                ma "Good."
                "She says it like a conclusion. Which it is."
            "[[Watch the city. Say nothing.]]":
                $ _apply_trust("martha", 1)
                $ add_romance_momentum("martha", 2)
                $ add_relationship_memory("martha", "martha_rooftop_direction_withdrawal", "Let the question stay open")
                "She follows your gaze for a moment."
                "The silence doesn't need filling. She knows that."
    hide martha_dress_normal
    $ add_relationship_memory("martha", "martha_rooftop", "The rooftop conversation")
    jump map


# ── NORA — RENT CONVERSATION ──────────────────────────────────────────
label nora_rent_scene:
    $ nora_rent_done = True
    scene cafenight with dissolve
    show screen hud
    "Late. You're the only customer left. Nora's filling out a form at the counter."
    scene nora_rent_1 with dissolve
    show screen hud
    n "You ever thought about how much of your life is just paying for the place you sleep?"
    "She says it like she's been thinking about it for a while."
    scene nora_rent_2 with dissolve
    show screen hud
    "The form. You can see the number from where you're sitting."
    n "Landlord's raising it again. Third time in two years."
    scene nora_rent_3 with dissolve
    show screen hud
    menu:
        "\"Is it still worth it?\"":
            n "That's the question I've been avoiding."
            "She puts the pen down."
            $ _apply_trust("nora", 2)
            scene nora_rent_4a with dissolve
            show screen hud
            n "The café's here. Henry's not going to find someone else. That's the trap."
            n "Good enough to stay. Not good enough to actually want."
            scene nora_rent_5a with dissolve
            show screen hud
            n "You're doing that thing where you listen like you actually care what the answer is."
            menu:
                "\"I do.\"":
                    $ _apply_aff("nora", 3)
                    n "Then you're one of the few."
                "Say nothing.":
                    $ _apply_trust("nora", 2)
                    "She goes back to the form."
        "\"Can you negotiate with him?\"":
            n "I tried. He sent back a PDF."
            "You both sit with that."
            $ _apply_trust("nora", 1)
            scene nora_rent_4b with dissolve
            show screen hud
            n "I looked at moving. The numbers don't work unless I also quit, which — no."
            scene nora_rent_5b with dissolve
            show screen hud
            n "It's fine. I'll figure it out. Always do."
            "She says it in a way that suggests she's had to say it a lot."
            menu:
                "\"You don't have to act like it's fine.\"":
                    $ _apply_aff("nora", 3)
                    $ _apply_trust("nora", 2)
                    n "...yeah."
                "\"Let me know if something opens up near me.\"":
                    $ _apply_aff("nora", 2)
                    n "That's either generous or you don't know what I'd be like as a neighbour."
    $ add_relationship_memory("nora", "nora_rent_talk", "The rent conversation")
    jump location_cafe


# ── SAM — GYM ─────────────────────────────────────────────────────────
label sam_gym_scene:
    $ sam_gym_done = True
    scene gym with dissolve
    show screen hud
    "Sam's still here. The gym's nearly empty — just the two of you and the overhead hum."
    scene sam_gym_1 with dissolve
    show screen hud
    sam "I noticed you've been putting in the time. You're consistent. That's rarer than people think."
    scene sam_gym_2 with dissolve
    show screen hud
    "You stretch out by the weights. Sam sits across, water bottle in hand."
    sam "What are you actually training for? Or is it just the routine?"
    scene sam_gym_3 with dissolve
    show screen hud
    menu:
        "\"Mostly the routine.\"":
            sam "That's enough. Most people need a reason. The routine is its own reason."
            $ _apply_trust("sam", 2)
        "\"Something to feel in control of.\"":
            sam "Yeah. I get that."
            "A pause that means they get it more than they're saying."
            $ _apply_trust("sam", 3)
            $ _apply_aff("sam", 2)
        "\"To keep up with you, honestly.\"":
            "Sam looks at you."
            sam "I'm going to pretend I didn't like that."
            $ _apply_aff("sam", 3)
    scene sam_gym_4 with dissolve
    show screen hud
    sam "I used to hate this place. Now it's the only part of the day I don't second-guess."
    "You ask what changed."
    scene sam_gym_5a with dissolve
    show screen hud
    sam "Stopped trying to turn it into something productive. Just — moved."
    menu:
        "\"That's harder than it sounds.\"":
            sam "It really is."
            $ _apply_trust("sam", 2)
            scene sam_gym_6a with dissolve
            show screen hud
            "You finish the session without counting reps. That's the best kind."
            $ gain_stat("str", 5)
            $ _apply_aff("sam", 2)
        "\"I still count every rep.\"":
            sam "You'll get there."
            scene sam_gym_5b with dissolve
            show screen hud
            "Sam shows you one thing. One adjustment in the grip. It makes a difference."
            $ gain_stat("str", 5)
            scene sam_gym_6a with dissolve
            show screen hud
            "By the end you're both quiet. That's fine."
            $ _apply_trust("sam", 2)
    jump location_gym


# ── ZOE — BEACH NIGHT ─────────────────────────────────────────────────
label zoe_beach_night_scene:
    $ zoe_beach_night_done = True
    scene beachnight with dissolve
    show screen hud
    scene zoe_beach_night_1 with dissolve
    show screen hud
    "The beach at this hour is mostly dark. Zoe's at the water's edge, shoes off."
    z "I didn't think you'd actually come."
    "You say you weren't sure either."
    z "Honest. Good."
    menu:
        "\"You looked like you needed the company.\"":
            $ _apply_aff("zoe", 2)
            z "I did. Don't tell me I was obvious."
            scene zoe_beach_night_2a with dissolve
            show screen hud
            "She sits. You follow. The tide doesn't care about either of you."
            z "I've been thinking about whether I'm doing this city right."
            z "Like — is there a right way? Or does everyone feel like they're making it up?"
            $ _apply_trust("zoe", 2)
        "\"I wanted to come.\"":
            $ _apply_aff("zoe", 3)
            z "Okay. That's — okay."
            scene zoe_beach_night_2b with dissolve
            show screen hud
            "She doesn't say anything for a while. The water fills the silence."
            z "This is the only place I don't feel like I should be somewhere else."
            $ _apply_aff("zoe", 2)
    scene zoe_beach_night_3 with dissolve
    show screen hud
    "Later. The city hum, the cold air, neither of you quite ready to leave."
    menu:
        "\"Same time next week?\"":
            z "Don't make it a schedule. Just — show up."
            $ _apply_aff("zoe", 3)
            $ _apply_trust("zoe", 2)
        "Walk her home.":
            z "You don't have to."
            "You go anyway."
            $ _apply_aff("zoe", 4)
    $ add_relationship_memory("zoe", "zoe_beach_night", "Night at the beach")
    jump location_sandbeach


# ── IT TRIAL: Server crisis at 2am ────────────────────────────────────
label it_trial_team_lead:
    scene hub_night
    show screen hud
    "2:47 AM. Your phone won't stop."
    "Slack: @channel — prod is down. Revenue dropping $800/minute."
    "Your lead is overseas. You're the most senior person awake."
    menu:
        "Dig into the logs carefully":
            if stat_int >= 55 or skill_prog >= 4:
                "You comb through stack traces. There — a botched migration."
                "Three commands. Patch, redeploy, monitor. 4:12 AM: green."
                $ store.promotion_trials[("it", store.job_rank)] = True
                $ promote()
                $ gain_stat("int", 15)
                "Monday morning the CEO sends a Slack. Your name is in it."
                "Your lead calls. \"Team Lead. Effective today.\""
            else:
                "Too much to parse. You guess wrong. The rollback takes down two other services."
                $ store.job_performance = 80
                "\"You almost had it. Come back sharper.\""
        "Roll back the last deploy immediately":
            "Wrong call — the rollback cascades and takes down two other services."
            $ store.job_performance = 80
            "Morning comes with a very quiet Slack. \"You almost had it. A few more days.\""
    return


# ── HOSPITAL TRIAL: Difficult case with Dr. Lena ──────────────────────
label hospital_trial_resident:
    scene expression ("hospital_night" if (hour >= 20 or hour < 6) else "hospital1")
    show screen hud
    show drlena_normal at sprite_r
    lena "Complicated presentation. No one agrees on the diagnosis. I need a second pair of eyes."
    lena "What does the blood panel tell you — first instinct?"
    menu:
        "Read the inflammation markers carefully":
            if stat_int >= 45 or skill_med >= 3:
                lena "...That's the right thread. Most residents miss it."
                "You work through the night. The patient stabilizes before dawn."
                lena "I put your name on the case report."
                $ store.promotion_trials[("hospital", store.job_rank)] = True
                $ setattr(store, "lena_trust", min(100, store.lena_trust + 12))
                $ promote()
                $ gain_stat("int", 8)
                "Board approval comes that afternoon. Resident. Finally."
            else:
                lena "We need someone who can commit to a diagnosis. Come back sharper."
                $ store.job_performance = 80
                "A week later: \"When you're ready.\""
        "Admit you'd need more tests first":
            lena "That's honest. But in a crisis I need decisiveness. Go home. Rest."
            $ store.job_performance = 80
            "You leave before sunrise."
    hide drlena_normal
    return


# ── QUAYSIDE (Nadbrzeże) ───────────────────────────────────────────────
label location_nadbrzeze:
    $ current_loc = "location_nadbrzeze"
    $ fs_record_district("nadbrzeze")
    scene expression ("nadbrzeze_night" if (hour >= 19 or hour < 6) else "nadbrzeze_day")
    show screen hud
    call screen nadbrzeze_hub

# ── THE ANCHOR (waterfront bar) ───────────────────────────────────────
label location_anchor:
    $ current_loc = "location_anchor"
    $ activity_exit_jump = "location_nadbrzeze"
    $ activity_exit_name = "Quayside"
    if not venue_open("bar"):
        "The Anchor doesn't open until evening."
        jump location_nadbrzeze
    scene bar
    show screen hud
    menu (screen="activity"):
        "Have a drink ($6, +mood)":
            if money < 6:
                "Not enough cash."
                jump location_anchor
            $ spend_time(0.5)
            $ gain_money(-6)
            $ gain_stat("chr", 5)
            "A cold one by the water. The city feels further away from here."
            jump location_anchor
        "Stay a while (1h, +CHR)":
            $ spend_time(1)
            $ gain_stat("chr", 10)
            "The crowd here is different from the centrum — looser, less on display. Good conversation finds you."
            jump location_anchor
        "Buy a round ($18, +CHR)":
            if money < 18:
                "Not enough cash."
                jump location_anchor
            $ spend_time(0.5)
            $ gain_money(-18)
            $ gain_stat("chr", 18)
            "A round for the bar. Instant friends for the night."
            jump location_anchor

# ── RIVERSIDE TERRACE (outdoor, day–evening) ──────────────────────────
label location_terrace:
    $ current_loc = "location_terrace"
    $ activity_exit_jump = "location_nadbrzeze"
    $ activity_exit_name = "Quayside"
    if not venue_open("terrace"):
        "The terrace is closed."
        jump location_nadbrzeze
    scene expression ("restaurantnight" if hour >= 19 else "restaurantday")
    show screen hud
    menu (screen="activity"):
        "Sit and watch the water (1h)":
            $ spend_time(1)
            $ gain_stat("int", 6)
            "The city hum fades here. You think more clearly."
            jump location_terrace
        "Have a coffee ($4)":
            if money < 4:
                "Not enough cash."
                jump location_terrace
            $ spend_time(0.5)
            $ gain_money(-4)
            $ gain_stat("chr", 4)
            "Outdoor table, river smell, decent espresso."
            jump location_terrace
        "Read (1h, +INT)":
            $ spend_time(1)
            $ gain_stat("int", 12)
            "A chapter in the open air. The light's good."
            jump location_terrace


# ── LATE-NIGHT DINER (nadbrzeże) ──────────────────────────────────────────────

label location_diner:
    $ current_loc = "location_diner"
    $ activity_exit_jump = "location_nadbrzeze"
    $ activity_exit_name = "Quayside"
    if not venue_open("diner"):
        "The diner is closed. It opens at 8pm."
        jump location_nadbrzeze
    scene diner_night
    show screen hud
    hide screen people_here_dock
    if (rena_met and cul_npc1_done and not rena_diner_first_done
            and npc_here("rena") and major_scene_last_day != day):
        call scene_rena_diner_first
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_diner")
    menu (screen="activity"):
        "Order coffee ($3, 0.5h)":
            if try_spend(3):
                $ spend_time(0.5)
                $ need_energy = min(100, need_energy + 8)
                "Late-night filter. Bitter and exactly right."
            else:
                "Not enough cash."
            jump location_diner
        "Order a meal ($8, 1h)":
            if try_spend(8):
                $ spend_time(1)
                $ need_hunger = min(100, need_hunger + 40)
                "The menu is short. Whatever it is, it's done well enough."
            else:
                "Not enough cash."
            jump location_diner
        "Sit for a while (1h)":
            $ spend_time(1)
            $ need_energy = min(100, need_energy + 5)
            "The noise of the night softens here. You don't need to be anywhere."
            jump location_diner
        "Talk to Rena" if npc_here("rena"):
            call rena_diner_talk
            jump location_diner
        "Leave":
            hide rena_casual_normal
            jump location_nadbrzeze


# ── LOMBARD (pawn shop, nadbrzeże) ────────────────────────────────────────────

label location_lombard:
    $ current_loc = "location_lombard"
    $ activity_exit_jump = "location_nadbrzeze"
    $ activity_exit_name = "Quayside"
    if not venue_open("lombard"):
        "The Lombard is closed."
        jump location_nadbrzeze
    scene lombard_day
    show screen hud
    menu (screen="activity"):
        "Browse (1h)":
            $ spend_time(1)
            "Shelves of secondhand things. Someone else's history, priced to move."
            jump location_lombard
        "Leave":
            jump location_nadbrzeze


label scene_rena_diner_first:
    $ rena_diner_first_done = True
    $ add_relationship_memory("rena", "diner_first", "Saw Rena off duty")
    "A booth near the back. Rena, in a dark sweater, a paperback open on the table."
    "She looks up when you come in. Recognition crosses her face without surprise."
    show rena_casual_normal at sprite_r
    rena "Commis."
    "It's not unfriendly. It's just accurate."
    menu:
        "\"Didn't expect to see you here.\"":
            rena "I eat here most weeks. It's someone else's kitchen."
            "She says it like that explains everything. It does."
            $ _apply_aff("rena", 2)
        "\"Good book?\"":
            rena "Third time through. The killer's obvious but the geography is right."
            "She marks her page without being asked. You haven't been dismissed."
            $ _apply_aff("rena", 2)
        "Order something and sit nearby — don't interrupt her.":
            "You don't say anything. Neither does she."
            "After a while she turns a page. The silence is comfortable in the way that silences in kitchens never are."
            $ _apply_trust("rena", 3)
    return


label rena_diner_talk:
    if not talk_followup_rena_taste_again_done and "wev_cul_taste_again" in work_events_seen.get("culinary", []):
        $ talk_followup_rena_taste_again_done = True
        $ fs_record_social("rena", "talk")
        show rena_casual_talk at sprite_r
        rena "You tasted it before I asked today."
        mc "I'm learning."
        rena "You're repeating something correctly."
        rena "Learning comes later."
        return
    if not talk_followup_rena_short_staffed_done and rena_short_staffed_choice is not None:
        $ talk_followup_rena_short_staffed_done = True
        $ fs_record_social("rena", "talk")
        show rena_casual_talk at sprite_r
        if rena_short_staffed_choice == "help":
            rena "You asked where I needed you."
            mc "You sounded surprised."
            rena "I was checking whether it was temporary."
        else:
            rena "You held your station."
            mc "You say that like I was being tested."
            rena "You were."
        return
    show rena_casual_talk at sprite_r
    rena "Still here."
    menu:
        "Ask about the book she's reading.":
            rena "Crime. Eastern European procedurals — the geography holds up better than the plots."
            rena "The detectives are always tired. I find that credible."
            show rena_casual_normal at sprite_r
            $ _apply_aff("rena", 1)
        "Ask if she ever switches off completely.":
            show rena_casual_normal at sprite_r
            rena "I'm here, aren't I?"
            "She orders from someone else's menu without looking at the specials."
            rena "That's switching off."
            $ _apply_aff("rena", 1)
        "Talk about the kitchen.":
            show rena_casual_normal at sprite_r
            rena "Not tonight."
            "It's not harsh. It's a boundary she keeps cleanly."
        "Just check in — nothing specific.":
            show rena_casual_normal at sprite_r
            rena "Still here."
            "She means it as an answer. You let it be one."
    return


# ── INDEPENDENT GALLERY (Phase 50 — temporary event location) ─────────────────
# Accessible only while: a valid Zoe exhibition plan is pending,
# or zoe_exhibition_done and day <= zoe_gallery_until_day.
# Background: gallery_evening (not yet declared); fallback librarynight.

label location_gallery:
    $ current_loc = "location_gallery"
    $ activity_exit_jump = "location_centrum"
    $ activity_exit_name = "City Centre"
    # Safety redirect: no valid plan and no active post-opening period.
    $ _gal_plan_ok = (store.npc_invitation_pending is not None
                      and store.npc_invitation_pending.get("invitation_id") == "zoe_exhibition"
                      and store.day <= store.npc_invitation_pending.get("expiry_day", -999))
    $ _gal_post_ok = store.zoe_exhibition_done and store.day <= store.zoe_gallery_until_day
    if not (_gal_plan_ok or _gal_post_ok):
        jump location_centrum
    $ _gal_bg = "gallery_evening" if renpy.has_image("gallery_evening") else "librarynight"
    # Dispatch WED personal event (the once-only opening scene)
    $ _wed_gal = wed_poll_personal("location_gallery")
    if _wed_gal:
        call expression _wed_gal
        jump location_gallery
    scene expression _gal_bg
    show screen hud
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("location_gallery")
    menu (screen="activity"):
        "Talk to Zoe" if (zoe_exhibition_done
                          and day <= zoe_gallery_until_day
                          and npc_here("zoe")
                          and zoe_gallery_talk_last_day < day):
            $ zoe_gallery_talk_last_day = day
            call zoe_gallery_talk
            jump location_gallery
        "Look at the work (0.5h)" if zoe_exhibition_done and day <= zoe_gallery_until_day:
            $ spend_time(0.5)
            "The work is still up. The corner piece is still in the corner."
            jump location_gallery
        "Leave":
            jump location_centrum
