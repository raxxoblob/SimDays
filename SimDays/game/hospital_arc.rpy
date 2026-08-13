# hospital_arc.rpy — Hospital career preview arc (Clinical Assistant → Resident)
# NPC: Dr. Lena — warm, medically precise, carries the weight of the work
# Lena's Character (`lena`) is defined once in characters.rpy — do not redefine
# here; a second `define` with a different color makes the color load-order dependent.
# Work events are appended to _HOSP_POOL on init.

init 1 python:
    _HOSP_ARC_EVENTS = ["wev_hosp_case_presentation", "wev_hosp_overtime_call"]
    try:
        _HOSP_POOL.extend(_HOSP_ARC_EVENTS)
    except NameError:
        _HOSP_POOL = list(_HOSP_ARC_EVENTS)


label hosp_first_day:
    $ lena_met = True
    scene cg_hosp_first_day
    show screen hud
    "Lena walks two steps ahead, already briefing. The ward is quieter than you expected — tired in a specific way."
    scene hospital1
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    lena "Clinical assistant orientation. You're with me today — I'll walk you through the ward, then the first set of charts is yours."
    lena "Two rules. Document what you observe, not what you assume. And if you're unsure: ask once. Still unsure: ask me, not the patient."
    menu:
        "\"What's the most important thing to get right on day one?\"":
            lena "Don't fall behind on charts. Everything flows from the paperwork. If the paperwork's wrong, the treatment plan is wrong."
            $ gain_skill("med", 3)
        "\"How will I know if I'm doing well?\"":
            lena "You won't, at first. You'll know when something goes wrong. That's normal — it's how the skill builds."
        "\"Ready.\"":
            lena "Good."
            "She's already walking."
    "The ward is quieter than you expected. People are tired in a specific way — not tired of being here, just tired."
    hide focus_lena
    $ _apply_trust("lena", 2)
    return


label hosp_task_1:
    $ hosp_task_1_done = True
    $ _hosp_patv = "conservative"
    scene hospital1
    show screen hud
    "The intake is complicated. Mr. Arends, 68 — chest pain, two pages of existing conditions. His daughter is in the room and gives a different medication history than he does."
    show drlena_normal as focus_lena at sprite_r
    lena "I'll be observing. Document what you find. I'll come back when you've finished."
    hide focus_lena
    scene cg_hosp_task_1
    show screen hud
    "The chart is dense. Two accounts. You work through it."
    scene hospital1
    show screen hud
    menu:
        "Document both accounts, flag the discrepancy clearly.":
            "You write up both versions side by side and mark the inconsistency. The chart is dense."
            show drlena_normal as focus_lena at sprite_r
            lena "The discrepancy needs resolving before any prescriptions are written. Good catch."
            $ gain_skill("med", 5)
            $ _apply_trust("lena", 3)
            hide focus_lena
            $ _hosp_patv = "thorough"
        "Ask the patient to clarify which account is correct.":
            "He's not sure. His daughter insists. You document her version with a note about the patient's uncertainty."
            show drlena_normal as focus_lena at sprite_r
            lena "The family member's account can be more reliable. But note the uncertainty — don't resolve it for them. Keep both versions."
            $ gain_skill("med", 3)
            $ _apply_trust("lena", 2)
            hide focus_lena
            $ _hosp_patv = "patient_centered"
        "Document conservatively — only what you can verify.":
            "You limit yourself to what he's confirmed. The chart is thin but clean."
            show drlena_normal as focus_lena at sprite_r
            lena "In doubt, document less and flag more. You erred on the right side. Build confidence and the charts will fill out."
            $ gain_skill("med", 3)
            $ _apply_trust("lena", 2)
            hide focus_lena
            $ _hosp_patv = "conservative"
    if _hosp_patv == "thorough":
        $ queue_phone_message("lena", "The Arends intake — both accounts, discrepancy flagged. That's the correct approach. Don't let the family dynamic pressure you into resolving what isn't yours to resolve.", day + 1, "hosp_task1_followup")
    elif _hosp_patv == "patient_centered":
        $ queue_phone_message("lena", "Documenting the uncertainty alongside the daughter's account was right. Keep both versions when you can't verify. The chart should reflect what you found, not what you concluded.", day + 1, "hosp_task1_followup")
    else:
        $ queue_phone_message("lena", "The conservative chart on Arends was the right instinct at this stage. The skill builds — so will the detail. You erred correctly.", day + 1, "hosp_task1_followup")
    if _hosp_patv in ("thorough", "patient_centered") and not message_already_queued("lena_case_invite"):
        $ queue_phone_message("lena", "Observation round Wednesday — difficult case, third-year presenting. Come if you'd like to see how it works.", day + 3, "lena_case_invite", responses=_LENA_CASE_RESP)
    return


label hosp_npc1_lena:
    $ hosp_npc1_done = True
    $ _hosp_presv = "observed_method"
    scene hospital1
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    "Lena invites you along for rounds."
    hide focus_lena
    scene cg_hosp_npc1
    show screen hud
    "At the first bed she shifts register — warmer, slower. She leans slightly. No clinical terms. He answers more completely than he had to."
    scene hospital1
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    "After the room:"
    lena "What did you notice?"
    menu:
        "\"You didn't start with the medical questions.\"":
            lena "People will tell you what you need if they trust you're interested in what they're saying. The clinical picture is in what they choose to share."
            lena "The textbook gives you the framework. What's in front of you is the patient."
            $ gain_skill("med", 5)
            $ _apply_trust("lena", 3)
            $ _hosp_presv = "observed_method"
        "\"You seemed different in there.\"":
            lena "Yes."
            "A pause, not uncomfortable."
            lena "The work requires it. You'll find your version."
            $ _apply_aff("lena", 2)
            $ _hosp_presv = "observed_shift"
        "\"How do you always know the right thing to say?\"":
            lena "I don't. I know how to listen well enough that they tell me."
            $ gain_skill("med", 3)
            $ _apply_trust("lena", 2)
            $ _hosp_presv = "asked_how"
    hide focus_lena
    if _hosp_presv == "observed_method":
        $ queue_phone_message("lena", "The rounds — you noticed what mattered. That's the foundation. The rest of it builds from there.", day + 1, "hosp_npc1_followup")
    elif _hosp_presv == "observed_shift":
        $ queue_phone_message("lena", "You'll find your register in there. It won't look exactly like mine — it shouldn't. That's how it works.", day + 1, "hosp_npc1_followup")
    else:
        $ queue_phone_message("lena", "It's not always. It's frequently enough that it looks like always. That difference matters more than it sounds.", day + 1, "hosp_npc1_followup")
    return


label hosp_npc2_lena:
    $ hosp_npc2_done = True
    $ _hosp_npc2v = "silent"
    scene cg_hosp_npc2
    show screen hud
    "Room 7 was a referral from the ED that didn't stabilise in time. You weren't directly responsible — the chain was long and none of it was yours to make."
    "But you were there. You charted the last observations."
    scene hospital_break_room
    show screen hud
    "You're in the break room, not eating, not doing anything."
    show drlena_normal as focus_lena at sprite_r
    "Lena comes in. She doesn't make it a teaching moment. She sits down."
    lena "You'll think about this one for a while. That's how it should work."
    menu:
        "Say nothing. Sit with it.":
            "She doesn't leave. After a few minutes she makes tea, puts one in front of you without asking."
            $ _apply_aff("lena", 3)
            $ _apply_trust("lena", 2)
            $ _hosp_npc2v = "silent"
        "\"How do you handle it?\"":
            lena "I put it somewhere specific. Not away — somewhere I can find it again. You learn what it means over time."
            lena "The ones that still sit with you after fifteen years — those are the ones that made you the doctor you are."
            $ _apply_trust("lena", 3)
            $ gain_skill("med", 3)
            $ _hosp_npc2v = "asked"
        "\"Was there anything else that could have been done?\"":
            "She considers the question properly."
            lena "That's the right thing to want to know. Probably not. But go back through it when you're ready — not to find blame, to understand."
            $ gain_skill("med", 4)
            $ _apply_trust("lena", 3)
            $ _hosp_npc2v = "analytical"
    hide focus_lena
    if _hosp_npc2v == "silent":
        $ queue_phone_message("lena", "You stayed this afternoon. That was the right thing. Some of this is just about being present. Room 7 was a hard one.", day + 2, "hosp_npc2_followup")
    elif _hosp_npc2v == "asked":
        $ queue_phone_message("lena", "The question you asked in the break room — it's the right one. The answer takes years. You're asking it earlier than I did.", day + 2, "hosp_npc2_followup")
    else:
        $ queue_phone_message("lena", "You asked what else could have been done. That instinct — to understand rather than assign blame — is going to serve you well here.", day + 2, "hosp_npc2_followup")
    return


label hosp_review_assistant:
    $ hosp_review_done = True
    scene hospital1
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    if hospital_hard_case_done and hospital_hard_case_followup_done:
        if hospital_hard_case_outcome == "escalated":
            lena "The escalation on that case — you chose the harder path. That's not nothing."
        elif hospital_hard_case_outcome == "reassessed":
            lena "Your documentation on the ambiguous case was exactly what that situation needed."
        elif hospital_hard_case_owned_mistake:
            lena "You reported the mistake before I had to ask. I don't forget that."
        else:
            lena "Your reasoning on the hard case still concerns me. We've talked about it. Watch it doesn't happen again."
        python:
            _lhc_oc = store.hospital_hard_case_outcome
            if _lhc_oc == "dismissed":
                _lhc_oc = "dismissed_owned" if store.hospital_hard_case_owned_mistake else "dismissed_defended"
            _queue_story_aftermath("lena", "lena_hard_case", "hospital_hard_case", _lhc_oc,
                                   store.day, store.day + 2, "aftermath_lena_hard_case")
            store.lena_bar_absent_until_day = store.day + 3
    "Lena finds you between rounds."
    lena "The formal notification comes through tomorrow. I wanted to tell you first."
    lena "You're moving to resident. The clinical director signed off this morning."
    menu:
        "\"Thank you. For everything on the ward.\"":
            lena "You did the work. I just gave you the patients."
            $ _apply_aff("lena", 2)
        "\"What changes when I'm a resident?\"":
            lena "More decisions are yours to make. More of the picture is yours to read. The paperwork expands."
            lena "The part that doesn't change: you still ask when you're uncertain."
            $ gain_skill("med", 4)
        "\"What should I be ready for?\"":
            lena "The patients are the same. Your relationship to what they need — that shifts. Take it one day."
            $ _apply_trust("lena", 2)
    hide focus_lena
    $ promote()
    return


# ─── Arc work events (appended to _HOSP_POOL) ──────────────────────────────

label wev_hosp_case_presentation:
    $ _mark_wev("hospital", "wev_hosp_case_presentation")
    scene hospital1
    show screen hud
    "Morning rounds. The attending asks you to present the new admission's case."
    "You've read the chart. Halfway through you stumble — the imaging contradicts the blood panel. You hadn't noticed."
    show drlena_normal as focus_lena at sprite_r
    lena "Take your time."
    menu:
        "Acknowledge the discrepancy and keep presenting.":
            "\"The imaging and the bloods don't align — flagged for follow-up. Working hypothesis is...\""
            "The attending nods. Lena says nothing. Her silence is specific."
            $ gain_skill("med", 5)
            $ _work_perf(4)
        "Rush through it and hope nobody notices.":
            "The attending notices. The follow-up question lands exactly where you didn't want it to."
            $ _work_perf(-2)
    hide focus_lena
    return


label wev_hosp_overtime_call:
    $ _mark_wev("hospital", "wev_hosp_overtime_call")
    scene hospital1
    show screen hud
    "A nurse coordinator at 4pm: \"Orla called in sick. Can you stay until nine?\""
    menu:
        "Stay.":
            if need_energy < 30:
                "You're already flagging but you say yes."
                $ spend_time(4)
                $ need_energy = max(0, need_energy - 15)
                "It shows by the end. A senior nurse quietly takes over your last chart."
                $ _work_perf(-2)
            else:
                $ spend_time(4)
                $ need_energy = max(0, need_energy - 12)
                $ gain_money(40)
                "Four more hours. Harder than the first eight, but manageable."
                $ _work_perf(3)
        "You can't tonight.":
            "\"No problem. We'll manage.\""
            "They will."
    return


# ── Phase 47: hard-case arc ─────────────────────────────────────────────────

label hospital_hard_case_scene:
    $ _wev_relbar_open("lena")
    show screen npc_relbar("lena")
    scene hospital1
    show screen hud
    "A patient's condition changes halfway through an otherwise routine case."
    "The signs are concerning — but ambiguous. Borderline readings, no clear pattern yet."
    show drlena_normal as focus_lena at sprite_r
    "Another staff member leans in."
    "Staff" "Could be nothing. We can check again after the current procedure."
    hide focus_lena
    "Lena is occupied on the other side of the ward."
    menu:
        "Stop the procedure and escalate immediately.":
            $ hospital_hard_case_choice = "escalated"
            $ hospital_hard_case_outcome = "escalated"
            mc "We stop here. I'm calling for senior review."
            "Staff" "Are you sure? The readings could still normalise."
            mc "We're not waiting to find out."
            "The procedure halts. The review is requested."
            $ _work_perf(6)
            $ _apply_trust("lena", 3)
        "Pause, reassess, and document the change before deciding.":
            $ hospital_hard_case_choice = "reassessed"
            $ hospital_hard_case_outcome = "reassessed"
            mc "Hold on. Let me document what we're seeing and request a second opinion before we continue."
            "The staff member steps back. You record the change in full."
            "Within the hour, a senior reviews the case."
            $ _work_perf(3)
            $ _apply_trust("lena", 2)
        "Continue the routine process — the concern is probably minor.":
            $ hospital_hard_case_choice = "dismissed"
            $ hospital_hard_case_outcome = "dismissed"
            mc "It's likely just a variation. Let's continue."
            "Staff" "Okay."
            "You continue. The patient requires additional intervention later in the shift."
            $ _work_perf(-8)
            $ _apply_trust("lena", -3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ hospital_hard_case_done = True
    $ hospital_hard_case_followup_pending = True
    $ hospital_hard_case_followup_shift = hosp_shifts + 2
    return


label hospital_hard_case_followup:
    scene hospital1
    show screen hud
    show drlena_normal as focus_lena at sprite_r
    if hospital_hard_case_outcome == "escalated":
        "The patient from the earlier case received attention sooner because of the escalation."
        lena "The decision to stop was correct. The reading was early but the pattern was real."
        mc "I wasn't certain at the time."
        lena "You didn't need to be certain. You needed to be concerned enough to stop. You were."
        hide focus_lena
        $ _work_perf(2)
        $ _apply_trust("lena", 2)
    elif hospital_hard_case_outcome == "reassessed":
        "The documentation from your hold became part of the case record."
        lena "Your notes captured the change clearly. That's what supported the later decision."
        mc "I wasn't sure stopping was right at the time."
        lena "The documentation made the choice defensible. That's the point of it."
        hide focus_lena
        $ _work_perf(1)
        $ _apply_trust("lena", 1)
    else:
        "Two additional interventions were required after you continued the routine process."
        lena "You saw the case update?"
        mc "Yes."
        "She waits."
        hide focus_lena
        $ _wev_relbar_open("lena")
        show screen npc_relbar("lena")
        show drlena_normal as focus_lena at sprite_r
        menu:
            "Report the mistake before Lena asks.":
                $ hospital_hard_case_owned_mistake = True
                mc "I got it wrong. The signs were concerning and I kept going."
                "Lena doesn't move to reassure."
                lena "What would you do now?"
                mc "Stop. Document. Call for review."
                lena "Then you've learned it. The hard way costs more, but it stays."
                hide focus_lena
                $ _work_perf(1)
                $ _apply_trust("lena", 2)
                $ hospital_hard_case_review_extra_shifts = 1
            "Wait and defend the original reasoning.":
                $ hospital_hard_case_owned_mistake = False
                mc "The readings were ambiguous. I made a reasonable call with what I had."
                lena "Sharp enough to notice. Not decisive enough to act on it."
                mc "I—"
                lena "We continue. But this will weigh on how I assess your readiness."
                hide focus_lena
                $ _work_perf(-2)
                $ _apply_trust("lena", -2)
                $ hospital_hard_case_review_extra_shifts = 2
        $ _wev_relbar_close()
        hide screen npc_relbar
    $ hospital_hard_case_followup_done = True
    $ hospital_hard_case_followup_pending = False
    if hosp_review_done:
        python:
            _lhc_oc = store.hospital_hard_case_outcome
            if _lhc_oc == "dismissed":
                _lhc_oc = "dismissed_owned" if store.hospital_hard_case_owned_mistake else "dismissed_defended"
            _queue_story_aftermath("lena", "lena_hard_case", "hospital_hard_case", _lhc_oc,
                                   store.day, store.day + 2, "aftermath_lena_hard_case")
            store.lena_bar_absent_until_day = store.day + 3
    return


