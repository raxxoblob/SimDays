# Corporate shift activity system.
# Each label handles one activity type at Nexus Tower.
# Called from location_office; all return after completing.
# Overtime is a post-shift secondary decision in location_office.

init python:
    MARTHA_COLLAB_COOLDOWN = 3   # days between "work alongside Martha" sessions

    def martha_collab_available():
        """True if Martha is available to work with — roughly once every 3 days."""
        return store.martha_met and (store.day - store.martha_last_collab) >= MARTHA_COLLAB_COOLDOWN

    def martha_collab_status():
        """(available, reason) for the work-choice screen. The option is always
        listed; when it can't be picked the screen says why instead of hiding it."""
        if not store.martha_met:
            return (False, "You haven't met Martha yet")
        _wait = MARTHA_COLLAB_COOLDOWN - (store.day - store.martha_last_collab)
        if _wait > 0:
            return (False, "She's booked up — %d more day%s" % (_wait, "" if _wait == 1 else "s"))
        return (True, "Available today")

    # ── Project Atlas progress ────────────────────────────────────────────────
    # (completion flag, focused sessions required, phase name, what happens next).
    # These thresholds ARE corp_project_work's gates below — change both together.
    # Presentation has no session gate: it fires as soon as crunch is done.
    ATLAS_MILESTONES = [
        ("atlas_research_done",     2, "Research",
         "dig into the Meridian Group data"),
        ("atlas_problem_done",      4, "Problem",
         "take the segment-two problem to Martha"),
        ("atlas_crunch_done",       6, "Crunch",
         "build the recommendation"),
        ("atlas_presentation_done", 0, "Presentation",
         "present to Meridian's board"),
    ]

    def atlas_phase_info():
        """Pure read — no state change. Returns:
          phase     current milestone name (or Not started / Debrief / Complete)
          sessions  focused Atlas sessions logged so far (atlas_shifts)
          next      one-line description of the next milestone, or None
          next_at   session count that unlocks it, or None if it isn't gated
          remaining focused sessions still needed, or 0 if the gate is already met
        """
        _s = store.atlas_shifts
        if not store.atlas_started:
            return {"phase": "Not started", "sessions": _s, "next": None,
                    "next_at": None, "remaining": None}
        if store.atlas_completed:
            return {"phase": "Complete", "sessions": _s, "next": None,
                    "next_at": None, "remaining": None}
        for _flag, _need, _name, _desc in ATLAS_MILESTONES:
            if not getattr(store, _flag, False):
                return {"phase": _name, "sessions": _s, "next": _desc,
                        "next_at": (_need or None),
                        "remaining": (max(0, _need - _s) if _need else 0)}
        return {"phase": "Debrief", "sessions": _s,
                "next": "the fallout lands on your next shift",
                "next_at": None, "remaining": 0}

    def atlas_progress_line():
        """Explicit end-of-session feedback for a focused shift that didn't open
        a milestone scene. Replaces the old 'progress is real, even when
        invisible' line — the progress is now actually stated."""
        _i = atlas_phase_info()
        _txt = "Project Atlas — %s phase. %d focused session%s logged." % (
            _i["phase"], _i["sessions"], "" if _i["sessions"] == 1 else "s")
        if _i["remaining"]:
            _txt += " %d more before you %s." % (_i["remaining"], _i["next"])
        elif _i["next"]:
            _txt += " Next: %s." % _i["next"]
        return _txt

    # ── Work-choice option table ──────────────────────────────────────────────
    # Every effect below is read off the label it describes. Performance figures
    # are do_shift()'s: the default shift gains 13 (6 when worn out); the other
    # three pass perf_override, and a worn-out override halves to max(1, n // 2).
    CORP_SHIFT_HOURS = 8

    def corp_work_options():
        """[(key, title, available, why_not, [(effect, category), ...])] for the
        work-choice screen. Pure read — safe to call every render."""
        _pay = cur_rank("corporate")["pay"]
        _worn = worn_out()
        _mav, _mwhy = martha_collab_status()
        _ai = atlas_phase_info()
        # Networking has weekly diminishing returns (corp_network below).
        _wk = store.day // 7
        _used = store.network_week_count if store.network_week_idx == _wk else 0
        if _used < 2:
            _net_fx = ("+3 Office reputation, 40% chance of +5 Charisma", "gain")
        elif _used == 2:
            _net_fx = ("+1 Office reputation (3rd session this week)", "info")
        else:
            _net_fx = ("No effect — 4th+ session this week", "info")

        _opts = []
        _opts.append(("regular", "Handle regular responsibilities", True, None, [
            ("%dh" % CORP_SHIFT_HOURS, "time"),
            ("+$%d" % _pay, "earn"),
            ("Performance +%d" % (6 if _worn else 13), "gain"),
            ("Business / Charisma training, work events, promotion roll", "gain"),
            ("Advances the main career storyline", "info"),
        ]))

        _atlas_fx = [
            ("%dh" % CORP_SHIFT_HOURS, "time"),
            ("+$%d" % _pay, "earn"),
            ("Performance +%d (reduced — narrow focus)" % (2 if _worn else 5), "need"),
        ]
        if store.atlas_started and not store.atlas_completed:
            _atlas_fx.append(("Atlas: %s phase, session %d" % (_ai["phase"], _ai["sessions"] + 1), "gain"))
            if _ai["remaining"]:
                _atlas_fx.append(("%d more session%s to %s" % (
                    _ai["remaining"], "" if _ai["remaining"] == 1 else "s", _ai["next"]), "info"))
            elif _ai["next"]:
                _atlas_fx.append(("Milestone ready: %s" % _ai["next"], "gain"))
            _opts.append(("project", "Focus on Project Atlas", True, None, _atlas_fx))
        else:
            _opts.append(("project", "Focus on Project Atlas", False,
                          ("Already delivered" if store.atlas_completed
                           else "Caroline hasn't handed you the project yet"), _atlas_fx))

        _opts.append(("martha", "Work alongside Martha", _mav, (None if _mav else _mwhy), [
            ("%dh" % CORP_SHIFT_HOURS, "time"),
            ("+$%d" % _pay, "earn"),
            ("Performance +%d" % (3 if _worn else 6), "gain"),
            ("Martha trust +1-2, sometimes affection +1", "gain"),
            ("One scene from her collaboration pool", "info"),
        ]))

        _opts.append(("network", "Spend some time getting to know the floor", True, None, [
            ("%dh" % CORP_SHIFT_HOURS, "time"),
            ("+$%d" % _pay, "earn"),
            ("Performance +%d (lowest — you're not at your desk)" % (1 if _worn else 2), "need"),
            _net_fx,
            ("Reputation opens rumours, referrals and hallway scenes", "info"),
        ]))
        return _opts

    _MARTHA_COLLAB_POOL = [
        "mco_kellner_review",
        "mco_report_draft",
        "mco_end_of_day_note",
    ]

    _NET_POOL = [
        "net_martha_venting",
        "net_office_rumour",
        "net_team_coffee",
        "net_analyst_chat",
    ]


# ── Work-choice screen ────────────────────────────────────────────────────────
# Replaces the old bare 4-line menu, which showed neither cost nor consequence
# and silently HID the Martha option on cooldown. Returns one of
# "regular" / "project" / "martha" / "network", or None for "not today".
screen corp_work_choice_scr():
    modal True
    zorder 260
    $ _cw_rank = cur_rank("corporate")
    $ _cw_perf = career_perf("corporate")
    frame:
        xalign 0.5 yalign 0.5
        xsize 900
        background "#12161ef8"
        padding (26, 18, 26, 20)
        vbox:
            spacing 6
            text "NEXUS TOWER — SHIFT" font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            hbox:
                spacing 18
                xalign 0.5
                text ("%s" % _cw_rank["title"]) font PROFILE_FONT size 13 color "#cfe0f5"
                text ("Performance %d/100" % _cw_perf) font ACT_FONT size 13 color ("#7ccc60" if _cw_perf >= 80 else "#8fb0d0")
                text ("Business Lv %d" % skill_val("biz")) font ACT_FONT size 13 color "#8fb0d0"
                text ("Shift %dh" % CORP_SHIFT_HOURS) font ACT_FONT size 13 color "#8fb0d0"
                text ("Pay $%d" % _cw_rank["pay"]) font ACT_FONT size 13 color "#ffd66a"
            null height 6
            for _key, _title, _avail, _why, _fx in corp_work_options():
                button:
                    xfill True
                    action (Return(_key) if _avail else NullAction())
                    background ("#1a2230" if _avail else "#141820")
                    hover_background ("#24354e" if _avail else "#141820")
                    padding (14, 9)
                    vbox:
                        spacing 3
                        hbox:
                            spacing 8
                            xfill True
                            text _title:
                                font PROFILE_FONT size 14
                                color ("#cfe0f5" if _avail else "#4a5665")
                            if not _avail:
                                text ("Unavailable — %s" % _why):
                                    font ACT_FONT size 12 color "#8a6a4a" xalign 1.0
                        hbox:
                            spacing 12
                            box_wrap True
                            for _etxt, _ecat in _fx:
                                text _etxt:
                                    font ACT_FONT size 12
                                    color (ACT_FX_COLOR.get(_ecat, "#b6c8dc") if _avail else "#3a4450")
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (20, 7)
                text "Not today" font PROFILE_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── REGULAR WORK ──────────────────────────────────────────────────────────
# Standard shift: full performance gain, fires work events, triggers arc scenes.
label corp_regular_work:
    # Corporate shift POV. pov_corporate is currently the goodoffice1 fallback
    # (see images.rpy — no generic Nexus work POV art exists yet). Authored CG
    # scenes below override it with their own `scene`; location_office re-runs
    # `scene goodoffice1` on the jump back, restoring the normal office view.
    scene pov_corporate
    show screen hud
    $ _tired = do_shift("corporate", 8)
    # Aftermath fires from any shift type the day after presentation
    if career_rank("corporate") == 1 and atlas_presentation_done and not atlas_aftermath_done:
        call corporate_atlas_aftermath
        return
    if career_rank("corporate") == 0:
        # Intern arc — scenes gate on corp_shifts
        $ corp_shifts += 1
        if not martha_met:
            call corporate_first_day
        elif not corp_task_1_done and corp_shifts >= 2:
            call corporate_task_1
        elif corp_task_1_done and not corp_martha_1_done and corp_shifts >= 4:
            call corporate_martha_1
        elif corp_martha_1_done and martha_trust >= 20 and not corp_martha_2_done and corp_shifts >= 6:
            call corporate_martha_2
        elif corp_martha_2_done and not corp_integrity_done:
            call corp_reporting_integrity
        elif (corp_integrity_done and corp_integrity_followup_pending
                and corp_shifts >= corp_integrity_followup_shift
                and not corp_integrity_followup_done):
            call corp_reporting_integrity_followup
        elif _tired:
            "Running on empty, you limp to end of day. Your manager notices the slippage."
        else:
            "A long day of meetings and spreadsheets. The pay is solid."
    elif career_rank("corporate") == 1:
        # Atlas intro fires during regular work — Caroline introduces the project in passing
        if not atlas_started:
            call corporate_atlas_intro
        elif _tired:
            "Running on empty. Atlas is somewhere in the background."
        else:
            "Standard day. The work moves, if not quickly."
    else:
        if _tired:
            "Running on empty."
        else:
            "A long day of meetings and spreadsheets. The pay is solid."
    if _work_event_roll("corporate"):
        call work_event_corporate
    $ _inc = _career_incident_check("corporate", career_rank("corporate"))
    if _inc:
        $ store._inc_incident = _inc
        $ store._inc_cid = "corporate"
        call career_incident_handler
    $ _ptr, _prd = do_promotion_roll("corporate")
    if _ptr == "rolled":
        $ _prbd = promotion_chance_breakdown("corporate")
        call screen career_promotion_status_scr("corporate", _prd, _prbd)
        if _prd["success"] and not _prd.get("opportunity_only"):
            $ promote("corporate")
    return


# ── PROJECT WORK ──────────────────────────────────────────────────────────
# Dedicated focus: lower performance gain, advances Atlas arc, guaranteed skill.
# atlas_shifts counts only these sessions — so "min 2 project sessions" between scenes.
label corp_project_work:
    # Corporate shift POV. pov_corporate is currently the goodoffice1 fallback
    # (see images.rpy — no generic Nexus work POV art exists yet). Authored CG
    # scenes below override it with their own `scene`; location_office re-runs
    # `scene goodoffice1` on the jump back, restoring the normal office view.
    scene pov_corporate
    show screen hud
    $ _tired = do_shift("corporate", 8, perf_override=5)
    # Aftermath fires here too, in case player chose project work the day after presentation
    if atlas_presentation_done and not atlas_aftermath_done:
        call corporate_atlas_aftermath
        return
    $ atlas_shifts += 1
    if not atlas_research_done and atlas_shifts >= 2:
        call corporate_atlas_research
    elif atlas_research_done and not atlas_problem_done and atlas_shifts >= 4:
        call corporate_atlas_problem
    elif atlas_problem_done and not atlas_crunch_done and atlas_shifts >= 6:
        call corporate_atlas_crunch
    elif atlas_crunch_done and not atlas_presentation_done:
        call corporate_atlas_presentation
    elif _tired:
        "Worn out. The project inches forward anyway."
        $ _atlas_note = atlas_progress_line()
        "[_atlas_note]"
    else:
        # "Meridian" is intentional, not stale: Meridian Group is the client
        # Project Atlas is built for (corporate_atlas.rpy, Caroline's briefing).
        # Named together here so the two words stop reading as two projects.
        "A day deep in the Meridian Group files — the client Project Atlas is built around."
        $ _atlas_note = atlas_progress_line()
        "[_atlas_note]"
    return


# ── WORK WITH MARTHA ──────────────────────────────────────────────────────
# Moderate performance, trust gains, Martha collab scene from rotating pool.
# Cooldown: available roughly once every 3 days.
label corp_work_martha:
    # Corporate shift POV. pov_corporate is currently the goodoffice1 fallback
    # (see images.rpy — no generic Nexus work POV art exists yet). Authored CG
    # scenes below override it with their own `scene`; location_office re-runs
    # `scene goodoffice1` on the jump back, restoring the normal office view.
    scene pov_corporate
    show screen hud
    $ _tired = do_shift("corporate", 8, perf_override=6)
    $ martha_last_collab = day
    if career_rank("corporate") == 1 and martha_trust >= 15 and corp_martha_1_done and not mco_client_call_done:
        call mco_client_call
    else:
        $ _mco = _pick_wev("martha_collab", _MARTHA_COLLAB_POOL)
        call expression _mco
    if _tired:
        "Even working alongside Martha, by the end you're running close to empty."
    if not martha_rooftop_done and martha_affection >= 40 and martha_trust >= 35 and hour >= 19:
        jump martha_rooftop_scene
    return

label mco_kellner_review:
    scene goodoffice1
    show martha_neutral as focus_martha at sprite_r
    ma "The Kellner segment B numbers."
    ma "Do you know why they keep shifting quarter on quarter?"
    menu:
        "Market volatility — that's how I read it.":
            ma "That's part of it. But the way it's reported makes it look like client error on our side. That matters when it escalates."
            "You file it away."
            $ _apply_trust("martha", 1)
        "I haven't looked closely yet.":
            ma "Look closely."
            "She walks you through it. Twenty minutes. More useful than you expected."
            $ _apply_trust("martha", 2)
    hide focus_martha
    $ _mark_wev("martha_collab", "mco_kellner_review")
    return

label mco_report_draft:
    scene goodoffice1
    show martha_neutral as focus_martha at sprite_r
    ma "I'm restructuring the Hartwell summary. Two options — lead with the risk section, or bury it in appendix B."
    ma "Guess which one Caroline wants."
    menu:
        "Lead with risk. Let the client see it upfront.":
            ma "That's what they need. Not necessarily what Caroline wants to send."
            "A pause."
            ma "I'll lead with it anyway. Good to know you'd make the same call."
            $ _apply_trust("martha", 2)
            $ _apply_aff("martha", 1)
        "If Caroline wants appendix B, she usually has a reason.":
            ma "There's always a reason. Doesn't always make it right."
            "She goes back to the draft."
            $ _apply_trust("martha", 1)
    hide focus_martha
    $ _mark_wev("martha_collab", "mco_report_draft")
    return

label mco_end_of_day_note:
    scene goodoffice1
    show martha_neutral as focus_martha at sprite_r
    "Six-thirty. Most of the floor is quiet."
    ma "How long do you think you'll stay in corporate?"
    menu:
        "Long enough to make it worth it.":
            ma "That's the standard answer."
            "She doesn't seem dissatisfied by it. Just unsurprised."
            $ _apply_trust("martha", 1)
        "I'm not sure yet. Are you?":
            ma "I've been not sure for six years."
            "She picks up her bag."
            ma "That's an answer too."
            $ _apply_trust("martha", 2)
            $ _apply_aff("martha", 1)
        "I'm focused on getting to Analyst right now.":
            ma "Short answer. Usually the right one to give."
            "She means it as a compliment. You think."
            $ _apply_trust("martha", 1)
    hide focus_martha
    $ _mark_wev("martha_collab", "mco_end_of_day_note")
    return


# ── NETWORK ───────────────────────────────────────────────────────────────
# Low performance gain; builds office_reputation and CHR. Diminishing returns
# after 2 sessions per week — full effect, half effect, then almost nothing.
label corp_network:
    if atlas_aftermath_done and atlas_martha_involved and not corp_net_credit_hallway_done:
        call corp_net_credit_hallway
        return
    # Corporate shift POV. pov_corporate is currently the goodoffice1 fallback
    # (see images.rpy — no generic Nexus work POV art exists yet). Authored CG
    # scenes below override it with their own `scene`; location_office re-runs
    # `scene goodoffice1` on the jump back, restoring the normal office view.
    scene pov_corporate
    show screen hud
    $ _tired = do_shift("corporate", 8, perf_override=2)
    $ _week = day // 7
    if network_week_idx < _week:
        $ network_week_count = 0
        $ network_week_idx = _week
    $ network_week_count += 1
    if network_week_count <= 2:
        $ office_reputation = min(100, office_reputation + 3)
        if renpy.random.random() < 0.4:
            $ gain_stat("chr", 5)
        $ _ne = _pick_wev("corp_net", _NET_POOL)
        call expression _ne
    elif network_week_count == 3:
        $ office_reputation = min(100, office_reputation + 1)
        "The rounds are familiar now. Useful for keeping up appearances. Less useful for finding anything new."
    else:
        "You circulate. People are polite. Nothing really lands today."
    if _tired:
        "You're running low by the time you wind down."
    return

label net_martha_venting:
    scene goodoffice1
    show martha_neutral as focus_martha at sprite_r
    "Martha at the coffee machine. The posture of someone who needed a quiet minute."
    ma "The Remington account. They've moved the deliverable date twice in two weeks."
    menu:
        "That's a billing conversation at some point.":
            ma "It's a billing conversation right now. Caroline won't push it."
            "She pours her coffee."
            ma "Good instinct, though."
            $ _apply_trust("martha", 1)
        "How are you handling it?":
            ma "The same way I handle everything. Finish the work; let the politics be someone else's problem."
            "She says it without self-pity. It's just how she's built."
            $ _apply_aff("martha", 1)
    hide focus_martha
    $ _mark_wev("corp_net", "net_martha_venting")
    return

label net_office_rumour:
    scene goodoffice1
    "You catch the tail end of a conversation near the break room."
    "Two people from the strategy floor. Something about the Q2 review, structural changes, headcount."
    "They notice you and change the subject."
    "Not unusual. But you file the shape of it away."
    $ office_reputation = min(100, office_reputation + 1)
    $ _mark_wev("corp_net", "net_office_rumour")
    return

label net_team_coffee:
    scene goodoffice1
    "The informal eleven o'clock. Six people around the small table by the windows."
    "No agenda. Project updates, weekend plans, a complaint about the printer on floor four."
    "You stay for twenty minutes. Nothing strategic. Just present."
    "These conversations are how people remember you exist."
    $ office_reputation = min(100, office_reputation + 2)
    if renpy.random.random() < 0.3:
        $ gain_stat("chr", 5)
    $ _mark_wev("corp_net", "net_team_coffee")
    return

label net_analyst_chat:
    scene goodoffice1
    "One of the analysts from the floor above stops you in the corridor."
    "She's been on a different strand of the same client family — different angle, different framing."
    "You compare notes for ten minutes. Nothing she says is exactly new."
    "But the way she's structured it is different from yours. You take two things from it."
    $ gain_skill("biz", 30)
    $ _mark_wev("corp_net", "net_analyst_chat")
    return


# ── OVERTIME ──────────────────────────────────────────────────────────────
# Post-shift secondary decision: extra 2h, extra pay, performance boost.
# High energy cost. Offered from location_office after any main activity.
label corp_net_credit_hallway:
    $ corp_net_credit_hallway_done = True
    scene cg_corp_credit_lobby
    show screen hud
    "The lobby. Marble floor, glass front. You hear your name before you see her."
    scene cg_corp_credit_martha
    show screen hud
    "Martha close, voice low."
    scene goodoffice1
    show screen hud
    show martha_neutral as focus_martha at sprite_r
    if atlas_credit_choice == "self":
        ma "The Meridian credit situation. That kind of thing travels further than you'd expect here."
        ma "I'm not making a judgement. Just — be aware."
        $ queue_phone_message("martha", "The credit conversation after Meridian. That kind of thing travels further than you'd expect. Something to keep in mind going forward.", day + 1, "corp_hallway_followup")
    elif atlas_credit_choice == "shared":
        ma "Word came back about how you handled the Meridian credit. That was the right call."
        $ queue_phone_message("martha", "I heard how you handled the Meridian credit situation. That was the right approach. For whatever that's worth.", day + 1, "corp_hallway_followup")
    else:
        ma "Someone mentioned your name in the Meridian context this week."
        ma "Positively, for what it's worth."
        $ queue_phone_message("martha", "Someone mentioned your name in the Meridian context this week. Positively. Those things tend to be worth noting.", day + 1, "corp_hallway_followup")
    hide focus_martha
    return


label corp_overtime:
    $ _ot_pay = int(cur_rank()["pay"] * 0.35)
    $ spend_time(2)
    $ gain_money(_ot_pay)
    $ need_energy = max(0, need_energy - 15)
    $ _work_perf(6)
    scene cg_corp_overtime_empty
    show screen hud
    "The floor clears out in stages. You stay."
    "Two hours of the specific quiet that only exists after everyone leaves."
    scene nexus_office_night
    show screen hud
    scene cg_corp_overtime_coffee
    show screen hud
    "You make a coffee at some point. It's the kind of thing you do without deciding to."
    scene goodoffice1
    show screen hud
    scene cg_corp_close_screen with dissolve
    show screen hud
    if need_energy < 25:
        "By the end you're running on the kind of empty that takes a full night to fix."
    else:
        "You close out. The screen goes dark first."
    return


# ── MARTHA CLIENT CALL (rank 1, trust ≥ 15) ──────────────────────────────────
label mco_client_call:
    $ mco_client_call_done = True
    $ _corp_promised_client  = False
    $ _corp_measured_in_call = False
    $ _corp_client_reframe   = False
    scene cg_corp_client_call
    show screen hud
    "The Hartwell call starts on time. Two faces on the screen — one partially visible, one leaning forward."
    "The leaning one is not happy. Delays on the Meridian segment are, in his exact words, 'commercially unacceptable.'"
    scene nexus_meeting_room
    show screen hud
    show martha_neutral as focus_martha at sprite_r
    ma "Mr. Hartwell. The current timeline reflects the scope as we understand it. Before we discuss revision—"
    "He cuts in. He wants a date. He wants it now."
    hide focus_martha
    scene cg_corp_client_handoff
    show screen hud
    "Martha's posture doesn't shift. Her head turns, fractionally, toward you."
    "It's not a question. It's an opening."
    scene nexus_meeting_room
    show screen hud
    menu:
        "Give him a specific date — two weeks earlier than planned.":
            "You name the date before you've finished calculating whether it's possible."
            "Hartwell goes quieter. Not satisfied — quieter."
            $ _corp_promised_client = True
            $ _apply_trust("martha", -1)
        "Acknowledge the concern, ask what's driving the urgency.":
            "\"Understood. What's the downstream dependency? That'll tell us where we have flexibility.\""
            "A pause. He tells you. You write it down."
            $ _corp_measured_in_call = True
            $ _apply_trust("martha", 2)
            $ gain_skill("biz", 30)
        "Reframe — the timeline is a quality gate, not a project problem.":
            "\"The current timeline exists because we're building something that holds on first deployment. A rushed revision risks the outcome Hartwell cares about.\""
            "Three seconds of quiet on the other end."
            $ _corp_client_reframe = True
            $ _apply_trust("martha", 1)
            $ gain_skill("biz", 40)
    "Martha closes the call. Thanks them for their time. Screen goes dark."
    scene cg_corp_client_after
    show screen hud
    "She sits back. The pen is on the table."
    scene nexus_meeting_room
    show screen hud
    show martha_neutral as focus_martha at sprite_r
    if _corp_promised_client:
        ma "You gave them a date."
        ma "Can we hit it?"
        menu:
            "\"Probably.\"":
                ma "Probably is not a contract term."
                $ _apply_trust("martha", 1)
            "\"I'd need to check.\"":
                ma "Then next time, check first."
                ma "The instinct to give them something was right. The execution needs work."
                $ _apply_trust("martha", 2)
    elif _corp_measured_in_call:
        ma "Asking for the dependency. That's the right question."
        ma "Most people try to answer what they were asked. You answered what mattered."
        $ _apply_trust("martha", 1)
        $ corp_review_score += 1
    else:
        ma "The quality-gate reframe. Bold."
        "A pause."
        ma "It worked this time. Can you back it up?"
        menu:
            "\"Yes.\"":
                ma "Good. Write it up before end of day."
                $ _apply_trust("martha", 2)
                $ corp_review_score += 1
            "\"I'll need help with the specifics.\"":
                ma "Then ask. That's what I'm here for."
                $ _apply_trust("martha", 2)
    hide focus_martha
    $ _mark_wev("martha_collab", "mco_client_call")
    return
