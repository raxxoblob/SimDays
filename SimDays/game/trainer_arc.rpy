# trainer_arc.rpy — Trainer career preview arc (Assistant Trainer → Lead Trainer)
# NPC: Kai (she/her) — head trainer, reads clients, observational before directive
# Sprites: kai_normal — may already exist (Kai is at gym_floor); verify before adding new define.
# Defines _TR_POOL and work_event_trainer.

init python:
    _TR_POOL = ["wev_tr_challenging_client", "wev_tr_equipment_issue", "wev_tr_group_class", "wev_trainer_shift_texture"]


label work_event_trainer:
    $ _ev = _pick_wev("trainer", _TR_POOL)
    call expression _ev
    return


label tr_first_day:
    $ kai_met = True
    scene cg_tr_first_day
    show screen hud
    "You shadow Kai for the 7am session — a regular, mid-40s, been training here two years."
    scene pov_trainer
    show screen hud
    "She barely speaks during the session. She cues, adjusts, watches. The client barely notices the adjustments."
    "After they leave:"
    kai "What did you see?"
    menu:
        "\"Their left shoulder was compensating on the press.\"":
            kai "Yes. They've been doing it eight months. I'm working it out slowly — if I correct it too fast, they'll stop trusting the process."
            kai "Observation first. Always."
            $ gain_skill("fit", 4)
            $ _apply_trust("kai", 3)
        "\"You barely talked during the session.\"":
            kai "The talking is in the adjustments. If you're narrating everything, they stop feeling what's happening."
            $ _apply_trust("kai", 2)
        "\"They looked comfortable with you.\"":
            kai "Two years. But comfort isn't automatic — you maintain it. Every session."
            kai "That's the first thing to understand."
            $ gain_skill("fit", 3)
            $ _apply_trust("kai", 2)
    return


label tr_task_1:
    $ tr_task_1_done = True
    scene pov_trainer
    show screen hud
    kai "New client. Intake form says general fitness, weight loss, no injury history. It's yours. I'll be on the floor."
    "The client is twenty-three, gym-anxious, talks a lot when nervous."
    scene cg_tr_task_1
    show screen hud
    "During the assessment you discover they haven't done structured exercise before. 'Some gym experience' meant the treadmill, twice."
    scene pov_trainer
    show screen hud
    menu:
        "Adjust the plan on the spot — start simpler than the intake suggests.":
            "You rebuild the session mentally while they talk. Bodyweight first. Lower the stakes."
            "They finish looking surprised at themselves."
            kai "You read them right. The plan matters less than the first experience."
            $ gain_skill("fit", 5)
            $ _apply_trust("kai", 3)
        "Stick to the plan — they said they had experience.":
            "The session works mechanically. They complete it. They're quiet at the end."
            "They don't rebook immediately."
            kai "The form was what they wished was true. What did the actual session tell you?"
            $ _apply_trust("kai", 1)
            $ gain_skill("fit", 3)
        "Check in mid-session: ask them how they're finding it.":
            "They tell you. You adjust. The session shifts into something they can stay with."
            kai "Good. Asking mid-session is harder than adjusting upfront. You made them feel like it was their decision."
            $ gain_skill("fit", 5)
            $ _apply_trust("kai", 4)
    return


label tr_npc1_kai:
    $ tr_npc1_done = True
    scene cg_tr_npc1
    show screen hud
    "Between sessions, Kai walks you through a client's twelve-week plan."
    scene pov_trainer
    show screen hud
    kai "Why three days a week and not four?"
    menu:
        "\"Recovery. Three days gives enough time between sessions.\"":
            kai "That's the technical answer. What's the real answer?"
            kai "Four days means four choices to come. Three means the choice is smaller. For a first-year client, compliance is the programme."
            $ gain_skill("fit", 5)
            $ _apply_trust("kai", 3)
        "\"Their schedule was tight.\"":
            kai "Right. But there's another layer."
            "She explains the compliance reasoning. Three minutes. By the end you have a different understanding of what periodization actually does."
            $ gain_skill("fit", 4)
            $ _apply_trust("kai", 2)
        "\"I don't know — what's the right answer?\"":
            kai "The honest answer. Good."
            "She walks through the logic without condescension. The plan becomes legible."
            $ gain_skill("fit", 5)
            $ _apply_trust("kai", 3)
    kai "Programming isn't just physical. It's a conversation about what they can sustain."
    return


label tr_npc2_kai:
    $ tr_npc2_done = True
    scene pov_trainer
    show screen hud
    "Your last client of the day kept their session — third rebook after two cancellations."
    "They were quiet throughout. Not focused-quiet — somewhere-else quiet."
    scene cg_tr_npc2
    show screen hud
    "After they leave, Kai is still on the floor. She saw the session."
    scene pov_trainer
    show screen hud
    menu:
        "\"Something was off with them today.\"":
            kai "Yes."
            "She doesn't add to it immediately."
            kai "The training is the easy part. Anyone can count reps. The rest is whether you stay interested in the person."
            kai "Today you kept the session consistent. That was the right call — they needed the routine."
            $ _apply_trust("kai", 3)
            $ _apply_aff("kai", 2)
        "\"I wasn't sure what to do in there.\"":
            kai "That's an honest answer."
            kai "You kept it professional and let them set the pace. When someone needs the hour to be normal, normal is the thing you give them."
            $ _apply_trust("kai", 2)
            $ _apply_aff("kai", 2)
        "\"Is this always part of the job?\"":
            kai "The physical stuff is what gets people through the door. The rest is why you either stay in this career or you don't."
            "She says it without drama. Like it's a fact she's made her peace with."
            $ _apply_aff("kai", 3)
    return


label tr_boundary_case:
    $ _wev_relbar_open("kai")
    show screen npc_relbar("kai")
    scene pov_trainer
    show screen hud
    show kai_gym_normal at sprite_r
    "Your 9am is a regular — twelve sessions in, trains for recreational half-marathons."
    "They arrive moving carefully. Before the warm-up finishes, they stop."
    "Client" "Sharp. Just inside the knee. Started yesterday."
    mc "How sharp?"
    "Client" "Not constant. Just — catches when I bend past a certain point."
    "They have a charity run in nine days."
    "Client" "I can push through it. I just need to get through this week."
    "Kai is at the other end of the floor with her own client."
    menu:
        "Stop the session and refer to a physio.":
            $ tr_boundary_choice = "referred"
            $ tr_boundary_outcome = "referred"
            mc "We're not training on that today."
            "Client" "It's not that bad."
            mc "Sharp knee pain before a warm-up is your body asking to be heard."
            mc "I'd refer you to a physio before we touch another session. Nine days is enough time for an assessment."
            "Client" "...Okay."
            "They don't look happy. They look relieved."
            $ _work_perf(6)
            $ _apply_trust("kai", 3)
        "Modify to pain-free movement and document it.":
            $ tr_boundary_choice = "managed"
            $ tr_boundary_outcome = "managed"
            mc "We're not going anywhere near that range of motion today."
            "You rebuild the session: upper body, seated core, nothing that loads the knee past ninety degrees."
            "You write it down — pain onset, location, what you avoided and why."
            "The client finishes looking surprised the hour was still useful."
            $ _work_perf(3)
            $ _apply_trust("kai", 2)
        "Continue carefully — the client knows their body.":
            $ tr_boundary_choice = "continued"
            $ tr_boundary_outcome = "aggravated"
            mc "We'll take it easy. Listen to the signals."
            "The client appreciates being trusted."
            "Halfway through the session the catching becomes a catch-and-lock."
            "You stop immediately, but the session ends early."
            "The client limps slightly on the way to the changing room."
            $ _work_perf(-8)
            $ _apply_trust("kai", -3)
    hide kai_gym_normal
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ tr_boundary_done = True
    $ tr_boundary_followup_pending = True
    $ tr_boundary_followup_shift = tr_shifts + 2
    return


label tr_boundary_followup:
    scene pov_trainer
    show screen hud
    show kai_gym_normal at sprite_r
    if tr_boundary_outcome == "referred":
        "The referred client returns with a physio report and a revised training plan."
        "Iliotibial band — tightness compounding over their mileage increase. Three weeks modified; back to full in four to six."
        "The plan they bring you is more specific than the one you had."
        kai "Good call on the referral."
        mc "It was the only call."
        kai "The ones who think there's a grey zone there are the ones I watch."
        hide kai_gym_normal
        $ _apply_trust("kai", 2)
        $ _work_perf(2)
    elif tr_boundary_outcome == "managed":
        "The client has been back twice since. The documentation you wrote became the basis for their revised plan."
        kai "Your notes were clear. That matters — if anything had developed, the chain was there."
        mc "I wasn't sure it was enough at the time."
        kai "That's why you wrote it down."
        hide kai_gym_normal
        $ _apply_trust("kai", 1)
        $ _work_perf(1)
    else:
        "Two sessions cancelled without rescheduling. A message this morning."
        "'Pain got worse after the gym session. Seeing a doctor. Not sure about the rest of the programme.'"
        kai "You saw the message?"
        mc "Yes."
        "She waits."
        hide kai_gym_normal
        $ _wev_relbar_open("kai")
        show screen npc_relbar("kai")
        show kai_gym_normal at sprite_r
        menu:
            "Own it.":
                $ tr_boundary_owned_mistake = True
                mc "I made the wrong call. They said the pain was sharp and I let them continue."
                "Kai doesn't fill the silence right away."
                kai "What would you do differently?"
                mc "Stop the session. Refer. Regardless of what they wanted."
                kai "Then you understand it now."
                kai "Knowing what you'd change is the start of not making the same call again."
                $ _apply_trust("kai", 2)
                $ _work_perf(1)
                $ tr_boundary_review_extra_shifts = 1
            "Defend the decision.":
                $ tr_boundary_owned_mistake = False
                mc "They insisted. I modified the intensity. I didn't think it would escalate."
                kai "Sharp pain before a warm-up."
                mc "I know."
                kai "That's not a grey zone."
                "She looks at the floor. Not angry — deliberate."
                kai "We'll keep working. But this goes into how I think about your progression."
                $ _apply_trust("kai", -2)
                $ tr_boundary_review_extra_shifts = 2
        $ _wev_relbar_close()
        hide screen npc_relbar
        hide kai_gym_normal
    $ tr_boundary_followup_done = True
    $ tr_boundary_followup_pending = False
    return


label tr_review_asst:
    $ tr_review_done = True
    scene pov_trainer
    show screen hud
    if tr_boundary_outcome == "referred":
        kai "The knee client — that referral was the right call. That kind of judgment is the last thing I can teach in a timeline."
    elif tr_boundary_outcome == "managed":
        kai "The documentation on the knee session — that's professional practice. Most people either ignore it or overcorrect. You found the line."
    elif tr_boundary_owned_mistake:
        kai "The knee session. You got it wrong and said so. That's harder than getting it right in the first place."
    else:
        kai "We've covered the knee session. Your reasoning at the time still concerns me. I need to see you think differently under that kind of pressure."
    kai "You're not assisting anymore."
    kai "Morning slot, Monday to Friday — yours. Your own client book starts Monday. Trainer, effective immediately."
    menu:
        "\"That was faster than I expected.\"":
            kai "You adjusted to your clients instead of adjusting your clients to a plan. That's the one thing I can't teach in a timeline."
            $ _apply_trust("kai", 2)
        "\"What does Lead Trainer look different?\"":
            kai "You own the relationship from intake to programme review. No checking with me — your call, your accountability."
            kai "I'm available. But you're not asking permission anymore."
            $ gain_skill("fit", 4)
        "\"Thank you for the chance.\"":
            kai "You earned the slot. I moved the paperwork."
            "She sounds like she means it."
            $ _apply_aff("kai", 2)
    $ promote()
    return


# ─── Arc work events ───────────────────────────────────────────────────────

label wev_tr_challenging_client:
    $ _mark_wev("trainer", "wev_tr_challenging_client")
    scene pov_trainer
    show screen hud
    "Your 10am client wants to go heavier than their programme calls for. They've been pushing for two sessions."
    menu:
        "Hold the line — explain the reason clearly.":
            "You explain progressive overload. They listen, not entirely convinced."
            "You hold the programme. They come back next week."
            $ gain_skill("fit", 4)
            $ _work_perf(3)
        "Give them one heavier set at the end as a concession.":
            "One set, controlled, to acknowledge the goal."
            "They're pleased. The form holds."
            $ gain_skill("fit", 3)
            $ _work_perf(3)
        "Let them lead — it's their workout.":
            "They go heavier. Form breaks on the third rep."
            "Nobody gets hurt, but the session ends with both of you aware of what almost happened."
            $ _work_perf(-2)
    return


label wev_tr_equipment_issue:
    $ _mark_wev("trainer", "wev_tr_equipment_issue")
    scene pov_trainer
    show screen hud
    "The squat rack is occupied. The two dumbbells you need are taken. Your client's programme calls for both."
    menu:
        "Redesign the session using available equipment.":
            "Bulgarian split squat variation with a single dumbbell and the bench."
            "The client barely notices the change."
            $ gain_skill("fit", 5)
            $ _work_perf(4)
        "Have them warm up while you wait.":
            "Five minutes becomes ten. The session runs short."
            "The client is understanding. The session was fine, not great."
            $ _work_perf(1)
    return


label wev_tr_group_class:
    $ _mark_wev("trainer", "wev_tr_group_class")
    scene pov_trainer
    show screen hud
    "You're covering a group conditioning class. Halfway through, one participant is visibly struggling — red-faced, compensation pattern in the movement."
    menu:
        "Stop them discreetly and assess.":
            "You cue a water break for the group, move to them quietly."
            "First class back after an illness. You modify the remaining exercises. They finish."
            $ gain_skill("fit", 5)
            $ _work_perf(5)
        "Call a general pace reduction for the whole class.":
            "You lower intensity for everyone. The participant recovers. A few fitter members look mildly frustrated."
            "Good call for safety. Slightly messy in execution."
            $ gain_skill("fit", 3)
            $ _work_perf(2)
    return

label wev_trainer_shift_texture:
    $ _v = _pick_texture_variant("trainer", ["no_show", "wrong_weight", "busy_floor", "broken_clip", "client_shortcut"])
    call expression "wev_trainer_tex_" + _v
    $ _mark_wev("trainer", "wev_trainer_shift_texture")
    return

label wev_trainer_tex_no_show:
    scene pov_trainer
    show screen hud
    "The appointment time passes."
    "The client does not arrive."
    "Five minutes later, a message appears."
    "'Running five minutes late.'"
    mc "Impressive timing."
    return

label wev_trainer_tex_wrong_weight:
    scene pov_trainer
    show screen hud
    "You check the bar before the next set."
    "One side is heavier than the other."
    "The difference is small enough to miss and large enough to matter."
    mc "Reset it."
    $ gain_skill("fit", 3)
    return

label wev_trainer_tex_busy_floor:
    scene pov_trainer
    show screen hud
    "Every bench is occupied."
    "Two clients reach the cable station at the same time."
    menu:
        "Reorder the session.":
            "You move the next exercise earlier and keep the session moving."
            $ _work_perf(2)
        "Wait for the planned equipment.":
            "You use the pause to review the next set."
    return

label wev_trainer_tex_broken_clip:
    scene pov_trainer
    show screen hud
    "The cable attachment clip does not close completely."
    "You remove it before anyone loads the machine."
    "A working replacement is three steps away."
    mc "Better now than halfway through a set."
    return

label wev_trainer_tex_client_shortcut:
    scene pov_trainer
    show screen hud
    "Client" "Can we skip the warm-up today?"
    mc "Why?"
    "Client" "I'm already warm."
    "The client gestures toward the walk from the changing room."
    mc "We're keeping the warm-up."
    return


# ── Phase 64: paid group class ──────────────────────────────────────────────────
# The fitness half of the generalist income fix. Not a career: an occasional
# stand-in slot the gym offers you once you visibly know what you are doing.
# Capped around $50/week EV — a trainer shift still pays several times more.

default gym_class_last_day = -99
default gym_classes_led    = 0

init python:

    GYM_CLASS_HOURS      = 1.5
    GYM_CLASS_ENERGY     = 18
    GYM_CLASS_COOLDOWN   = 3      # days
    GYM_CLASS_MIN_FIT    = 4
    _GYM_CLASS_CHANCE    = 0.60   # ~1-2 slots a week once off cooldown
    _GYM_CLASS_DIFFICULTY = 45

    # A class that goes badly still gets paid — the members turned up and the
    # hour happened. It just pays the floor (Phase 60/61 forward-progress rule).
    _GYM_CLASS_PAY_MULT = {"critical_failure": 0.60, "weak": 0.80,
                           "success": 1.00, "great": 1.15, "critical": 1.30}

    def gym_class_base_pay():
        # fit4 -> $34, fit6 -> $42, fit8 -> $50, fit10 -> $55 (hard ceiling).
        # Tuned so EV/hour at mid skill (fit 6) stays under the Phase 63 $30/h
        # benchmark: $42 / 1.5h = $28/h.
        return min(55, 18 + skill_val("fit") * 4)

    def gym_class_available():
        """Stable per day — seeded on the day number, so it cannot be rerolled
        by walking out of the gym and back in."""
        if skill_val("fit") < GYM_CLASS_MIN_FIT:
            return False
        if store.day - store.gym_class_last_day < GYM_CLASS_COOLDOWN:
            return False
        import random as _r
        return _r.Random(store.day * 733 + 29).random() <= _GYM_CLASS_CHANCE

    def _gym_class_mods():
        mods = []
        if skill_val("fit") >= 7:            mods.append(("Experienced coach", +6))
        if store.gym_classes_led >= 3:       mods.append(("Regulars know you", +4))
        if has_player_state("confident"):    mods.append(("Confident", +5))
        if store.need_energy < 30:           mods.append(("Low energy", -8))
        return mods

    def gym_class_pay_range():
        base = gym_class_base_pay()
        return (int(round(base * min(_GYM_CLASS_PAY_MULT.values()))),
                int(round(base * max(_GYM_CLASS_PAY_MULT.values()))))

    def gym_class_chance():
        return calculate_check_chance("gym_class", skill_val("fit"),
                                      _GYM_CLASS_DIFFICULTY, _gym_class_mods())

    def do_gym_class():
        """Charges time + energy, rolls the session, pays out. No cash cost."""
        spend_time(GYM_CLASS_HOURS)
        store.need_energy = max(0, store.need_energy - GYM_CLASS_ENERGY)
        result = roll_check("gym_class", skill_val("fit"), _GYM_CLASS_DIFFICULTY,
                            _gym_class_mods(), stable=False)
        tier = result["tier"]
        pay = int(round(gym_class_base_pay() * _GYM_CLASS_PAY_MULT[tier]))
        gain_money(pay, "fitness")
        store.gym_class_last_day = store.day
        store.gym_classes_led   += 1
        xp = gain_skill_practice("fit", 8, 1)
        gain_stat("str", 6)
        record_game_event("gym_class_day%d" % store.day, "career",
                          "Led a group class at the gym", summary=True, journal=False,
                          metadata={"pay": pay, "tier": tier})
        return {"roll": result, "tier": tier, "pay": pay, "xp": xp}

    def _gym_class_lines(res):
        return [("Paid", "$%d" % res["pay"]), ("Fitness XP", "+%d" % res["xp"]),
                ("STR", "+6")]


label gym_class_flow:
    if not gym_class_available():
        "No class needs covering today."
        return
    $ _gc_lo, _gc_hi = gym_class_pay_range()
    $ _gc_chance = gym_class_chance()["success_or_better"]
    $ _gc_hrs = ("%g" % GYM_CLASS_HOURS)
    "The desk flags you down. \"Our circuit instructor called in sick. Can you take the class?\""
    menu:
        "[_gc_hrs]h. Pays $[_gc_lo]-[_gc_hi]. [_gc_chance]% to run it well."
        "Take the class":
            pass
        "Not today":
            return
    $ _gc_res = do_gym_class()
    call screen check_result_scr(_gc_res["roll"], title="Group Class", xtra_lines=_gym_class_lines(_gc_res))
    if _gc_res["tier"] in ("critical_failure", "weak"):
        "You lose the room somewhere in the middle and never quite get it back. They still clap."
    else:
        "You read the room, scale the moves, and finish them on the floor. Two people ask when you're on next."
    return
