# it_arc.rpy — IT career preview arc (Junior Dev → Mid Dev)
# NPC: Eli (she/her) — senior developer, dry, precise, good teacher
# Work events are appended to _IT_POOL on init so they fire via the existing work_event_it label.
# Sprites: eli_normal, eli_focused — add to images.rpy when art is ready.
# Eli's Character (`eli`) is defined once in characters.rpy — do not redefine here
# (a second `define` with a different color makes the color load-order dependent).

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
    if it_incident_followup_done:
        if it_incident_outcome == "rollback":
            eli "The deployment incident — judgment under uncertainty. The rollback was right."
        elif it_incident_outcome == "isolated":
            eli "Controlled scope, complete documentation. That's how recoverable errors stay recoverable."
        elif it_incident_owned_mistake:
            eli "The correction after the concealment mattered. The original call was still wrong."
        else:
            eli "Trust in your decision-making on that incident is limited. That's where we are."
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
    if it_incident_followup_done:
        python:
            _lti_oc = store.it_incident_outcome
            if _lti_oc == "concealed":
                _lti_oc = "concealed_owned" if store.it_incident_owned_mistake else "concealed_defended"
            _queue_story_aftermath("eli", "it_production_incident", "it_incident", _lti_oc,
                                   store.day, store.day + 1, "aftermath_it_production_incident")
    return


# ─── Arc work events appended to _IT_POOL; label bodies live in work_events.rpy


# ── Phase 48: IT production incident ──────────────────────────────────────────

label it_production_incident:
    $ it_incident_done = True
    scene hub_pov
    show screen hud
    "Deployment window opens at six. By six-forty the monitoring board flags a data mismatch."
    "Limited scope — around nine hundred records — but the pattern is irregular in a way that doesn't resolve to an obvious cause."
    eli "How wide?"
    mc "Nine hundred records. The write confirmation went through, but the downstream state doesn't match."
    "A colleague at the next terminal turns around."
    "Colleague" "It might self-correct once the migration completes. We've seen that before. Deploy through it — document it and explain in the morning."
    eli "It's a judgment call."
    "She's not making it for you."
    "Rollback means delay, escalation, and an explanation tonight. Continuing means nine hundred users with inconsistent state until morning."
    $ _wev_relbar_open("eli")
    show screen npc_relbar("eli")
    menu:
        "Stop deployment, roll back and escalate.":
            $ it_incident_choice = "rollback"
            $ it_incident_outcome = "rollback"
            mc "Rollback. Now."
            "You kill the deployment. The monitoring board steadies."
            mc "Nine hundred records with an irregular mismatch doesn't get explained in the morning."
            "The colleague doesn't argue. Eli makes a note."
            $ _work_perf(6)
            $ _apply_trust("eli", 3)
        "Isolate the affected component, document it, deploy the safe portion.":
            $ it_incident_choice = "isolated"
            $ it_incident_outcome = "isolated"
            mc "Split it. Document the mismatch scope, isolate the affected component, and deploy the rest."
            "The colleague pulls up the architecture. Forty minutes of careful partitioning."
            mc "The safe portion ships. The rest waits for root cause."
            "It lands clean."
            $ _work_perf(3)
            $ _apply_trust("eli", 2)
        "Continue deployment and suppress the warning until morning.":
            $ it_incident_choice = "concealed"
            $ it_incident_outcome = "concealed"
            mc "Continue. I'll take the call on it."
            "The flag clears from the active board. The deployment finishes."
            "You write a private note to review the affected records in the morning."
            $ _work_perf(-8)
            $ _apply_trust("eli", -3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ it_incident_followup_pending = True
    $ it_incident_followup_shift = it_shifts + 2
    return


label it_production_incident_followup:
    scene hub_pov
    show screen hud
    if it_incident_outcome == "rollback":
        "Two shifts later: the source analysis comes back. The mismatch wasn't localised — the upstream feed had been corrupted at the source for two days before the deploy."
        eli "Your rollback caught it before it compounded."
        mc "I didn't know how wide it was at the time."
        eli "You didn't need to know. The scope was unclear and the risk was real. That was enough."
        $ _work_perf(2)
        $ _apply_trust("eli", 2)
    elif it_incident_outcome == "isolated":
        "Two shifts later: the case review. The safe portion held; the documentation you attached made the remaining fix traceable."
        eli "The partition worked because the documentation was complete."
        mc "I wasn't certain the boundary would hold."
        eli "It did. The note you left was why the fix took two hours instead of two days."
        $ _work_perf(1)
        $ _apply_trust("eli", 1)
    else:
        "Two shifts later: the incident report. The mismatch reached users. Support tickets opened the morning after the deploy."
        eli "The flag was cleared from the active board."
        mc "I cleared it."
        "She waits."
        $ _wev_relbar_open("eli")
        show screen npc_relbar("eli")
        menu:
            "Acknowledge the call before she asks.":
                $ it_incident_owned_mistake = True
                mc "I made the wrong call. The risk was real and I chose the deadline."
                "Eli doesn't soften."
                eli "What's different next time?"
                mc "Escalate. The delay is recoverable. The user impact isn't."
                eli "That's the right answer. Getting there after the incident is still getting there."
                $ _work_perf(1)
                $ _apply_trust("eli", 2)
                $ it_incident_review_extra_shifts = 1
            "Defend the reasoning.":
                $ it_incident_owned_mistake = False
                mc "The scope looked contained. I made a judgment call with the information I had."
                eli "Nine hundred records with an irregular mismatch pattern isn't contained scope."
                mc "The monitoring had cleared similar flags before."
                eli "This one wasn't similar."
                "She closes the incident report."
                $ _work_perf(-2)
                $ _apply_trust("eli", -2)
                $ it_incident_review_extra_shifts = 2
        $ _wev_relbar_close()
        hide screen npc_relbar
    $ it_incident_followup_done = True
    $ it_incident_followup_pending = False
    if it_review_done:
        python:
            _lti_oc = store.it_incident_outcome
            if _lti_oc == "concealed":
                _lti_oc = "concealed_owned" if store.it_incident_owned_mistake else "concealed_defended"
            _queue_story_aftermath("eli", "it_production_incident", "it_incident", _lti_oc,
                                   store.day, store.day + 1, "aftermath_it_production_incident")
    return
