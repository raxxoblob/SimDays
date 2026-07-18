# trainer_arc.rpy — Trainer career preview arc (Assistant Trainer → Lead Trainer)
# NPC: Kai (she/her) — head trainer, reads clients, observational before directive
# Sprites: kai_normal — may already exist (Kai is at gym_floor); verify before adding new define.
# Defines _TR_POOL and work_event_trainer.

define kai = Character("Kai", color="#f5a623")

init python:
    _TR_POOL = ["wev_tr_challenging_client", "wev_tr_equipment_issue", "wev_tr_group_class"]


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


label tr_review_asst:
    $ tr_review_done = True
    scene pov_trainer
    show screen hud
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
