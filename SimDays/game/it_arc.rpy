# it_arc.rpy — IT career preview arc (Junior Dev → Mid Dev)
# NPC: Eli (she/her) — senior developer, dry, precise, good teacher
# Work events are appended to _IT_POOL on init so they fire via the existing work_event_it label.
# Sprites: eli_normal, eli_focused — add to images.rpy when art is ready.
# Eli's Character (`eli`) is defined once in characters.rpy — do not redefine here
# (a second `define` with a different color makes the color load-order dependent).

init 1 python:
    _IT_ARC_EVENTS = ["wev_it_prod_bug", "wev_it_pr_review", "wev_it_scope_creep"]
    try:
        _IT_POOL.extend(_IT_ARC_EVENTS)
    except NameError:
        _IT_POOL = list(_IT_ARC_EVENTS)


label it_first_day:
    $ eli_met = True
    scene cg_it_first_day
    show screen hud
    "The Hub is open-plan and loud in the quiet way offices get loud — too many keyboards, not enough walls."
    scene hub_pov
    show screen hud
    "Your induction pack is on your desk. Next to it: a sticky note."
    "\"Ticket #4471 — flaky test, login service. Fix by EOD. — E\""
    "Before you finish reading it, someone drops into the chair beside you."
    eli "You found the desk. Good. I'm Eli."
    eli "Senior dev. I'll be your point of contact for the first month, which means I'll answer your questions once and expect you to remember."
    menu:
        "\"What's #4471 actually doing?\"":
            eli "Failing one in five in CI but not locally. Start with the test runner logs. Don't touch the implementation until you understand why it's failing."
            $ gain_skill("prog", 3)
        "\"Is there documentation for the codebase?\"":
            eli "There's a wiki. Last updated in 2019. Treat it as archaeology rather than instruction."
            $ _work_perf(2)
        "\"Happy to be here.\"":
            eli "Sure."
            "She's already turned back to her monitor."
    eli "Standup's at nine. Don't be late for standup."
    $ _apply_trust("eli", 2)
    return


label it_task_1:
    $ it_task_1_done = True
    $ _it_t1v = "independent"
    scene hub_pov
    show screen hud
    eli "Client report this morning. Login service dropping sessions on mobile — intermittently, same pattern as the test. I'm assigning it to you."
    eli "Priority one. They've escalated once already."
    "The ticket is a wall of text. Stack traces, screenshots, one angry note from the account manager."
    scene cg_it_task_1
    show screen hud
    "Priority one. You open the logs."
    scene hub_pov
    show screen hud
    menu:
        "Work through the stack trace methodically.":
            "You start at the top and work down. Two hours. When you find it — a race condition in session refresh — you have a complete picture."
            $ gain_skill("prog", 5)
            $ _work_perf(5)
            eli "Took longer than it needed to. But you got there without guessing. Write the test first next time."
            $ _apply_trust("eli", 2)
            $ _it_t1v = "stack"
        "Check git blame to understand the context first.":
            "Six commits. The problematic logic was introduced fourteen months ago during a crunch push. The message says \"quick fix — revisit.\""
            "It was never revisited."
            $ gain_skill("prog", 4)
            $ gain_skill("biz", 3)
            eli "Good instinct. Understanding the why is half the fix."
            $ _apply_trust("eli", 3)
            $ _it_t1v = "git"
        "Ask Eli for help.":
            eli "What have you already tried?"
            "You walk her through it. She stops you twice to ask why you ruled something out."
            eli "The race condition is in session refresh. Go fix it."
            "The guidance saves two hours. Being guided feels useful and slightly uncomfortable."
            $ gain_skill("prog", 3)
            $ _apply_trust("eli", 1)
            $ _it_t1v = "asked"
    if _it_t1v == "stack":
        $ queue_phone_message("eli", "The session bug — your analysis was complete. Write the test first next time and it's a model approach.", day + 1, "it_task1_followup")
    elif _it_t1v == "git":
        $ queue_phone_message("eli", "The git blame on the session bug — good instinct. That commit was a crunch push. Knowing the history is half the fix.", day + 1, "it_task1_followup")
    else:
        $ queue_phone_message("eli", "You asked when you were stuck this morning. Right reflex. Solo figuring-out costs more time than most people admit.", day + 1, "it_task1_followup")
    return


label it_npc1_eli:
    $ it_npc1_done = True
    $ _it_n1v = "passive"
    scene hub_pov
    show screen hud
    scene cg_it_npc1
    show screen hud
    "Your PR notification: seven inline comments, two requests for changes, one 'this whole section needs a rethink.'"
    scene hub_pov
    show screen hud
    eli "Did you read through all of it?"
    menu:
        "\"I read it. Some comments I don't fully follow.\"":
            eli "Which ones?"
            "You pull up the PR. You go through the three you're uncertain about."
            eli "This one — you're naming a function after what it does today. When this gets extended in six months, the name will lie."
            eli "The others are style. You can push back on style. You can't push back on naming."
            $ gain_skill("prog", 5)
            $ _apply_trust("eli", 3)
            $ _it_n1v = "naming"
        "\"I can make all the changes.\"":
            eli "I didn't ask if you could. I asked if you read through it."
            "A beat."
            eli "Go read it. Come back when you have a question."
            $ _work_perf(2)
            $ _it_n1v = "passive"
        "\"I'd push back on the error handling comment.\"":
            eli "Go on."
            "You explain. She listens without interrupting."
            eli "You're not wrong. But you're optimising for now, not six months from now. The extra branch costs three lines and saves whoever maintains this from guessing."
            eli "You can still push back. Know why you're doing it."
            $ gain_skill("prog", 6)
            $ _apply_trust("eli", 4)
            $ _it_n1v = "pushback"
    if _it_n1v == "naming":
        $ queue_phone_message("eli", "The naming comment on your PR — that one matters most. Functions lie when they outlive their original scope. You'll see it.", day + 1, "it_npc1_followup")
    elif _it_n1v == "pushback":
        $ queue_phone_message("eli", "Your pushback on the error handling was technically defensible. Right starting point. Next step: know when the extra branch is worth the three lines.", day + 1, "it_npc1_followup")
    else:
        $ queue_phone_message("eli", "Read the review before acting on it. Understanding the comment is the review. Making changes without understanding them is just noise.", day + 1, "it_npc1_followup")
    return


label it_npc2_eli:
    $ it_npc2_done = True
    $ _it_n2v = "quiet"
    scene hub_pov
    show screen hud
    scene cg_it_npc2
    show screen hud
    "The deploy goes to prod at six-fifteen. You're still here. Eli is still here."
    "The smoke tests run. The dashboard is green. Neither of you moves."
    scene hub_pov
    show screen hud
    "After a few minutes:"
    eli "Good deploy. No alerts in ten minutes means no fire."
    menu:
        "\"Why are you still here after everyone left?\"":
            eli "Same reason you are. You want to see how it lands."
            eli "After a while you stop being able to hand that part off."
            $ _apply_aff("eli", 2)
            $ _it_n2v = "curious"
        "Stay quiet. Let the silence run.":
            "Eli glances at you once. Something shifts slightly in how she's sitting."
            eli "This team has had three re-orgs in four years. Everyone who stayed did it for the same reason — the work itself."
            eli "Don't tell the new hires. It ruins the mystique."
            $ _apply_aff("eli", 3)
            $ _it_n2v = "quiet"
        "\"Is The Hub actually a good place to work?\"":
            eli "Depends what you're comparing it to. The codebase is a mess. Product decisions are sometimes baffling."
            eli "But the problems are real. That part's still true."
            $ _apply_trust("eli", 2)
            $ _it_n2v = "direct"
    if _it_n2v == "curious":
        $ queue_phone_message("eli", "Same reason I still watch deploys land: I want to see how it holds. Habit at this point. Good deploy tonight.", day + 2, "it_npc2_followup")
    elif _it_n2v == "direct":
        $ queue_phone_message("eli", "The Hub question. Short answer: the problems are real. That's still true. Everything else is negotiable.", day + 2, "it_npc2_followup")
    else:
        $ queue_phone_message("eli", "Good deploy. No fire in ten minutes means the work held. Thanks for staying to see it through.", day + 2, "it_npc2_followup")
    if _it_n2v in ("curious", "quiet") and not message_already_queued("eli_debug_invite"):
        $ queue_phone_message("eli", "Staying late tomorrow — profiling the auth service. Second pair of eyes if you're around.", day, "eli_debug_invite", responses=_ELI_DEBUG_RESP)
    return


label it_review_junior:
    $ it_review_done = True
    scene hub_pov
    show screen hud
    eli "HR will send you something official. I wanted to tell you before the system does."
    eli "You're not junior anymore."
    menu:
        "\"What changed?\"":
            eli "You stopped asking whether something was worth understanding. You just understood it."
            eli "That's the threshold. Not a skill level — a habit."
            $ gain_skill("prog", 5)
        "\"Thank you.\"":
            eli "Don't thank me. You did the work."
            "A pause."
            eli "But you're welcome."
        "\"What's the next threshold?\"":
            eli "You start having opinions about the architecture. Other people's opinions bother you for reasons you can explain."
            eli "Right now you're fixing problems. Next level you're preventing them."
            $ gain_skill("prog", 3)
            $ gain_skill("biz", 2)
    $ promote()
    return


# ─── Arc work events appended to _IT_POOL; label bodies live in work_events.rpy
