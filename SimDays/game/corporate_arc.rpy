# Corporate career arc — Nexus Tower scenes.
# Triggered from location_office; all labels end with return.
# corporate_style: "ambitious" / "reliable" / "people_first" — set at recruitment.


# ── RECRUITMENT ───────────────────────────────────────────────────────────
label corporate_recruit:
    scene goodoffice1
    show screen hud
    "Nexus Tower. Glass and steel and the specific kind of quiet that means people are performing productivity."
    "The receptionist checks your name against a list and points you upstairs. Third floor. Caroline Vance, HR Director."
    show caroline_normal at sprite_r
    caro "On time. Good start."
    caro "I'll be direct — we don't hire on credentials alone. We hire for how people handle pressure and ambiguity."
    caro "One scenario. You're three days from a client deadline. Your analyst flags a significant error. Fixing it properly takes two days. Patching it takes four hours."
    menu:
        "Fix it properly and tell the client there's a delay.":
            caro "Integrity over optics. I can work with that."
            "She makes a note. Something in her expression settles — not warmth, but a kind of respect for the answer."
            $ corporate_style = "reliable"
        "Patch it, deliver on time, fix it quietly after.":
            caro "Pragmatic. Possibly too pragmatic — depends what's in the patch."
            "The pause before she writes is doing something. You can't tell what yet."
            $ corporate_style = "ambitious"
        "Tell the client, offer a discount, fix it right.":
            caro "Client-facing instinct. Expensive, but defensible."
            "She tilts her head slightly, as if recalibrating something."
            $ corporate_style = "people_first"
    caro "We'll be in touch."
    hide caroline_normal
    "She isn't immediately."
    "The email arrives three days later. Start Monday."
    "On the way out, someone holds the elevator door."
    show martha_neutral at sprite_r
    ma "New intake?"
    menu:
        "Just got the call.":
            ma "Congratulations."
            "She says it plainly, without filler. You weren't expecting that."
        "Looks that way.":
            ma "They moved fast. They must have liked you."
    ma "Martha. Analytics."
    hide martha_neutral
    "The elevator opens. She goes left. You go right. You don't know yet which direction matters more."
    $ apply_job("corporate")
    $ caroline_met = True
    return


# ── FIRST DAY ─────────────────────────────────────────────────────────────
label corporate_first_day:
    scene goodoffice1
    show screen hud
    "The desk is clean. That's about all you can say for it."
    "HR sends three documents, a badge, and a message: 'Ask Martha if you need anything.'"
    show martha_neutral at sprite_r
    ma "Survived the morning?"
    menu:
        "Mostly. The system logins took forty minutes.":
            ma "Standard. IT lost the onboarding doc last quarter and nobody's noticed yet."
            $ _apply_aff("martha", 1)
        "It's a lot to take in.":
            ma "It levels off. By week three you'll know which meetings you can skip."
    ma "Your first real task will come from Caroline. Probably tomorrow."
    ma "In the meantime — the Kellner account files are on the shared drive. Read them. Even if nobody asks, you'll want to know."
    menu:
        "Why the Kellner account specifically?":
            ma "Because it comes up in every meeting and most people here still don't understand it."
            "She goes back to her screen. Conversation apparently over."
            $ _apply_trust("martha", 2)
        "Good to know. Thanks.":
            ma "Don't thank me. Just do it."
            $ _apply_aff("martha", 1)
    hide martha_neutral
    "You find the Kellner files. They take three hours. You understand about sixty percent of it."
    "That's a start."
    $ martha_met = True
    return


# ── FIRST ASSIGNMENT ──────────────────────────────────────────────────────
label corporate_task_1:
    scene cg_corp_first_day
    show screen hud
    "Caroline doesn't knock. She stands in the doorway long enough to confirm you're paying attention."
    scene goodoffice1
    show screen hud
    show caroline_normal at sprite_r
    caro "I need a competitive analysis on Vantage Corp by Friday. Summary, three pages, key risks highlighted."
    "She doesn't say where the data is. Doesn't say what format. Doesn't define 'key risks.'"
    hide caroline_normal
    scene cg_corp_task_arrive
    show screen hud
    "The internal archive is quieter than the main floor. Older filing systems, better lighting."
    scene cg_corp_task_files
    show screen hud
    "Two hours of reports, public filings, industry summaries. The shape of it starts coming together."
    scene goodoffice1
    show screen hud
    $ _corp_t1v = "independent"
    menu:
        "Ask for more detail before she leaves.":
            show caroline_normal at sprite_r
            caro "Sources: internal reports, public filings. Format: executive summary at the top, detail below."
            caro "Key risks: whatever keeps the client awake. I appreciate the question — most people just guess."
            hide caroline_normal
            $ _apply_trust("caroline", 3)
            $ _work_perf(5)
            $ corp_review_score += 1
            $ _corp_t1v = "methodical"
        "Figure it out yourself. Ask if you get stuck.":
            "You do figure it out. Mostly. The version you hand in is tighter than it has any right to be."
            $ _work_perf(8)
            $ corp_review_score += 2
            $ _corp_t1v = "independent"
        "Ask Martha after Caroline leaves.":
            show martha_neutral at sprite_r
            ma "She wants two columns: what Vantage is doing right and what they're hiding."
            ma "She never says it that way, but that's what she means."
            hide martha_neutral
            $ _apply_trust("martha", 3)
            $ _work_perf(6)
            $ corp_review_score += 1
            $ _corp_t1v = "collaborative"
        "Push for a presentation slot instead of a written report." if corporate_style == "ambitious":
            show caroline_normal at sprite_r
            caro "..."
            caro "That's not what I asked for."
            "A beat."
            caro "But if you can make it land in ten minutes, Thursday, three o'clock."
            hide caroline_normal
            "High risk. You prepare for two days straight."
            $ _work_perf(12)
            $ _apply_trust("caroline", 1)
            $ corp_review_score += 2
            $ _corp_t1v = "ambitious"
        "Document your methodology as you go — make it reproducible." if corporate_style == "reliable":
            "You write the analysis and a clean methodology note alongside it. Nobody asked for the second document."
            "Caroline finds it on Friday. Doesn't say anything. Forwards it to the team."
            $ _work_perf(7)
            $ _apply_trust("caroline", 4)
            $ corp_review_score += 2
            $ _corp_t1v = "reliable"
        "Run a quick read-through with a colleague before submitting." if corporate_style == "people_first":
            show martha_neutral at sprite_r
            ma "You want me to proofread it?"
            ma "Fine. Page two, third paragraph — Vantage's market share figure is wrong by a year."
            hide martha_neutral
            "It would have been embarrassing."
            $ _apply_trust("martha", 4)
            $ _work_perf(7)
            $ corp_review_score += 2
            $ _corp_t1v = "people_first"
    $ corp_task_1_done = True
    if _corp_t1v == "methodical":
        $ queue_phone_message("caroline", "The Vantage analysis. You asked the right questions before starting. Most people guess. Good start.", day + 1, "corp_task1_followup")
    elif _corp_t1v == "independent":
        $ queue_phone_message("caroline", "The analysis landed clean. No format questions, no follow-up. That's rarer than it should be on a first submission.", day + 1, "corp_task1_followup")
    elif _corp_t1v == "collaborative":
        $ queue_phone_message("caroline", "I noticed you spoke with Martha before finalising. That kind of lateral thinking is exactly what this floor needs.", day + 1, "corp_task1_followup")
    elif _corp_t1v == "ambitious":
        $ queue_phone_message("caroline", "You took the Thursday slot. I don't make exceptions as a habit. Don't interpret it as a pattern — interpret it as one thing you earned.", day + 1, "corp_task1_followup")
    elif _corp_t1v == "reliable":
        $ queue_phone_message("caroline", "The methodology note wasn't requested. I forwarded it to the team. Don't make unsolicited extras routine — but that one was worth reading.", day + 1, "corp_task1_followup")
    else:
        $ queue_phone_message("caroline", "The analysis caught its own error before submission. Whatever your review process was — keep it.", day + 1, "corp_task1_followup")
    return


# ── MARTHA — FIRST REAL CONVERSATION ─────────────────────────────────────
label corporate_martha_1:
    scene cg_corp_martha1_desk with dissolve
    show screen hud
    "Martha stops by your desk at ten past six."
    scene goodoffice1
    show screen hud
    show martha_neutral at sprite_r
    ma "You turned the Vantage analysis in early."
    menu:
        "It wasn't that complicated once I had the framing.":
            ma "No. But most people take until Friday to work out what they're actually being asked."
            "Something shifts in her face — very slightly, in a way you'd miss if you weren't paying attention."
            $ _apply_trust("martha", 2)
            $ _apply_aff("martha", 1)
        "I had help getting there.":
            ma "I know. I'm not asking you to deny it."
            ma "I'm saying you used the help well. That's the relevant part."
            $ _apply_trust("martha", 3)
    if corporate_style == "ambitious":
        ma "Caroline mentioned your interview answer. The pragmatic one."
        ma "Works here, up to a point. Past that point it works against you."
        "She says it like she's done it herself once."
    elif corporate_style == "reliable":
        ma "You told Caroline you'd take the delay over the patch."
        ma "She didn't say it, but that answer stayed with her."
    elif corporate_style == "people_first":
        ma "The client-first answer. I wouldn't have taken it at face value."
        ma "Apparently Caroline did. That's worth knowing."
    $ _corp_m1v = "curious"
    menu:
        "What are you actually testing me for?":
            ma "I'm not testing you."
            "She picks up her bag."
            ma "I'm deciding whether you're worth talking to properly. There's a difference."
            $ _apply_trust("martha", 2)
            $ corp_review_score += 1
            $ _corp_m1v = "direct"
        "Why does it matter to you?":
            ma "Because I've watched six people sit at that desk and none of them lasted past a year."
            "Flat. Like she's citing a statistic."
            $ _apply_aff("martha", 2)
            $ _corp_m1v = "curious"
        "Say nothing. Let her finish.":
            "She waits. Then nods once, as if the silence was the right answer."
            $ _apply_trust("martha", 3)
            $ corp_review_score += 1
            $ _corp_m1v = "quiet"
    hide martha_neutral
    $ corp_martha_1_done = True
    if _corp_m1v == "direct":
        $ queue_phone_message("martha", "For the record — I wasn't testing you. But that's the right instinct to trust when you're new somewhere.", day + 1, "corp_martha1_followup")
    elif _corp_m1v == "curious":
        $ queue_phone_message("martha", "Six people at that desk. Three left before the year was up. The pattern's clear enough if you're looking. I thought you should know it.", day + 1, "corp_martha1_followup")
    else:
        $ queue_phone_message("martha", "Some conversations don't need the last word. That was one of them.", day + 1, "corp_martha1_followup")
    return


# ── MARTHA — SECOND SCENE ─────────────────────────────────────────────────
label corporate_martha_2:
    scene cg_corp_lunch_wide
    show screen hud
    "The break room. First time she's initiated anything that isn't work."
    scene goodoffice1
    show screen hud
    show martha_neutral at sprite_r
    ma "I'm getting coffee. You want one?"
    "The coffee machine makes a sound like it's negotiating with itself."
    ma "How long have you been here now?"
    "You tell her."
    ma "It feels longer when you're new. Then one day it starts feeling shorter."
    ma "Neither is a good sign."
    $ _corp_m2v = "personal"
    menu:
        "Do you actually like working here?":
            ma "I'm good at it."
            "A pause."
            ma "That's not the same thing."
            $ _apply_trust("martha", 3)
            $ _corp_m2v = "honest"
        "Sounds like you've been here a while.":
            ma "Six years. I was going to leave after two. Then after four."
            ma "You know how that goes."
            $ _apply_aff("martha", 2)
            $ _apply_trust("martha", 2)
            $ _corp_m2v = "personal"
        "Is this a warning?":
            ma "Call it an observation."
            "She hands you the coffee. Holds it a second longer than necessary."
            $ _apply_aff("martha", 3)
            $ _corp_m2v = "cautious"
    ma "You're doing better than most, for what it's worth."
    ma "I thought you should hear it."
    menu:
        "Why are you telling me?":
            ma "Because nobody told me."
            "She says it like it's nothing. It isn't."
            $ _apply_trust("martha", 3)
            $ corp_review_score += 1
        "Thank you.":
            "She looks briefly uncomfortable, as if she'd forgotten she said something kind."
            ma "Don't read too much into it."
            $ _apply_aff("martha", 2)
            $ corp_review_score += 1
    hide martha_neutral
    $ corp_martha_2_done = True
    if _corp_m2v == "honest":
        $ queue_phone_message("martha", "What I said this afternoon — 'good at it' is a lower bar than it sounds. Worth knowing the distinction.", day + 2, "corp_martha2_followup")
    elif _corp_m2v == "personal":
        $ queue_phone_message("martha", "Six years goes faster than it sounds. You stop noticing when the work is actually interesting. Still figuring out which one this is.", day + 2, "corp_martha2_followup")
    else:
        $ queue_phone_message("martha", "It wasn't a warning about the job. More a general observation. You'll know the difference when it matters.", day + 2, "corp_martha2_followup")
    if martha_trust >= 20 and not message_already_queued("martha_coffee_invite"):
        $ queue_phone_message("martha", "Coffee after work this week? There's a place near the office I've been meaning to get to.", day + 3, "martha_coffee_invite", responses=_MARTHA_COFFEE_RESP)
    return


# ── INTERN → ASSOCIATE REVIEW ─────────────────────────────────────────────
# corp_review_score ceiling is ~8 (task_1: 2, martha_1: 1, martha_2: 1, style option: +1-2 bonus).
# Three outcomes: strong (≥4), standard (≥2), conditional (performance-only).
label corporate_review_intern:
    scene cg_corp_review_report
    show screen hud
    "Caroline's office. There's a printed copy of your Vantage analysis on the desk with marks."
    scene goodoffice1
    show screen hud
    "The chair across from her desk is fractionally lower than hers. You notice this on the way in."
    show caroline_normal at sprite_r
    caro "Three months. I wanted to do this properly."
    caro "Your output is consistent. The Vantage analysis was used in the Kellner pitch — Stratford didn't credit you, but I did. Internally."
    if corporate_style == "reliable":
        caro "Your instinct is to do things right before doing them fast. That's an asset here, with the right limits."
    elif corporate_style == "ambitious":
        caro "You're results-focused. That reads well in some rooms and very poorly in others. You're learning which is which."
    elif corporate_style == "people_first":
        caro "You've built trust quickly. Martha mentioned it — which she doesn't do."
    if corp_integrity_followup_done:
        if corp_integrity_outcome == "disclosed":
            caro "The reporting situation — integrity before presentation. That's a short list."
        elif corp_integrity_outcome == "qualified":
            caro "Transparency with controlled delivery. The reconciliation note did its job."
        elif corp_integrity_owned_mistake:
            caro "The admission mattered. The alteration was still serious."
        else:
            caro "Target pressure doesn't remove your responsibility for the figure you submitted."
    if corp_review_score >= 4:
        # Strong outcome — earned it visibly
        if martha_trust >= 20:
            caro "Martha vouched for you. She doesn't do that lightly."
            "A beat. Something settles in the room."
        caro "Associate. Effective Monday. And — I mean this — well done."
        "She says it like it costs her something, which makes it feel more real."
        menu:
            "Thank you.":
                caro "Don't thank me. Give me a reason to do it again in six months."
            "What should I focus on next?":
                caro "Analyst track requires a Business degree. Start planning now, not when you're already at the ceiling."
                $ _apply_trust("caroline", 2)
            "Is there anything I should have done differently?":
                caro "Honestly? Not much. That's a short list."
                $ _apply_trust("caroline", 3)
                $ _apply_aff("caroline", 1)
        $ promote()
        "You leave with a new title and the specific quiet confidence of someone who knows they earned it."
    elif corp_review_score >= 2:
        # Standard outcome — promotion with a note
        caro "Associate. Effective Monday."
        caro "One thing. You're capable of more initiative than you've shown. Don't wait to be asked."
        menu:
            "Understood.":
                caro "Good."
            "What did you have in mind specifically?":
                caro "You'll know it when you see it. That's the point."
                $ _apply_trust("caroline", 2)
        $ promote()
        "New title. You take it as the floor, not the ceiling."
    else:
        # Conditional outcome — perf is 100 (so can_promote() passed), but arc choices were passive
        caro "Associate. Effective Monday."
        "She slides the contract across."
        caro "I'll be direct. Your numbers are there. The rest of it — judgment, initiative — I'm still reading."
        caro "The Associate track will tell me more. Don't make me regret the decision."
        menu:
            "I won't.":
                "She nods once. Conversation over."
            "What specifically are you watching for?":
                caro "How you handle the first thing that goes wrong. Everyone's capable when it's easy."
                $ _apply_trust("caroline", 3)
        $ promote()
        "You got what you came for. The terms weren't quite what you expected."
    hide caroline_normal
    $ corp_review_intern_done = True
    if corp_integrity_followup_done:
        python:
            _lci_oc = store.corp_integrity_outcome
            if _lci_oc == "smoothed":
                _lci_oc = "smoothed_owned" if store.corp_integrity_owned_mistake else "smoothed_defended"
            _queue_story_aftermath("caroline", "corp_reporting_integrity", "corp_integrity", _lci_oc,
                                   store.day, store.day + 1, "aftermath_corp_reporting_integrity")
    if corp_review_score >= 4:
        $ queue_phone_message("caroline", "Three months on record as strong. Enjoy the title this weekend — Associate track expectations start Monday, 9am.", day + 1, "corp_review_followup")
    elif corp_review_score >= 2:
        $ queue_phone_message("caroline", "The initiative note was a nudge, not a criticism. Associate is the right next step. Monday, 9am.", day + 1, "corp_review_followup")
    else:
        $ queue_phone_message("caroline", "The contract's done. Monday. The numbers were right. I'm still reading the rest.", day + 1, "corp_review_followup")
    return


# ── Phase 48: corporate reporting integrity ───────────────────────────────────

label corp_reporting_integrity:
    $ corp_integrity_done = True
    scene goodoffice1
    show screen hud
    show caroline_normal at sprite_r
    "Three days before the executive review. Caroline stops at your desk with the summary deck."
    caro "The Q3 Vantage segment. The board expects it at 4.2. Your current source gives 3.8."
    "A discrepancy of four-tenths across a reported segment — not trivial."
    caro "I need this reconciled before Monday."
    "She means use the expected number and sort it out after the meeting."
    mc "What's the source for the 3.8?"
    caro "Confirmed. The 4.2 is the target we submitted in Q2."
    "She waits. The review is in three days."
    $ _wev_relbar_open("caroline")
    show screen npc_relbar("caroline")
    menu:
        "Stop submission and disclose the discrepancy.":
            $ corp_integrity_choice = "disclosed"
            $ corp_integrity_outcome = "disclosed"
            mc "I can't submit 4.2. The source is 3.8. That's a material difference."
            caro "I'm aware of that."
            mc "Then I need to flag it through the right channel and pause submission until it's cleared."
            "A pause."
            caro "That will delay the deck."
            mc "Yes."
            "She takes the deck back."
            hide caroline_normal
            $ _work_perf(6)
            $ _apply_trust("caroline", 3)
        "Submit with the discrepancy explicitly marked and attach reconciliation.":
            $ corp_integrity_choice = "qualified"
            $ corp_integrity_outcome = "qualified"
            mc "I'll submit with the 3.8, note the Q2 target for reference, and attach a reconciliation note."
            "A beat."
            caro "That draws attention to the gap."
            mc "It also means no one acts on an incorrect figure."
            "She considers this."
            caro "Do it carefully."
            hide caroline_normal
            $ _work_perf(3)
            $ _apply_trust("caroline", 2)
        "Replace the figure with the expected target.":
            $ corp_integrity_choice = "smoothed"
            $ corp_integrity_outcome = "smoothed"
            mc "I can reconcile it after the meeting."
            "You update the deck. The figure becomes 4.2."
            "The problem will be there on Tuesday when you open the source file."
            hide caroline_normal
            $ _work_perf(-8)
            $ _apply_trust("caroline", -3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ corp_integrity_followup_pending = True
    $ corp_integrity_followup_shift = corp_shifts + 2
    return


label corp_reporting_integrity_followup:
    scene goodoffice1
    show screen hud
    show caroline_normal at sprite_r
    if corp_integrity_outcome == "disclosed":
        "Two shifts later: the source data was reanalysed before the meeting. The Q3 Vantage figure had been pulled from a pre-adjustment extract — the correct number aligned closer to the board's expectation than the discrepancy had suggested."
        caro "The delay was the right call."
        mc "I didn't know that at the time."
        caro "That's the point. You didn't know — and you didn't submit anyway."
        hide caroline_normal
        $ _work_perf(2)
        $ _apply_trust("caroline", 2)
    elif corp_integrity_outcome == "qualified":
        "Two shifts later: the reconciliation note had been picked up before the deck went to the board — the qualified figure was held pending clarification rather than treated as final."
        caro "The note did its job."
        mc "It flagged the gap without stopping the submission."
        caro "Which is why the data error didn't make it into the board summary. Your note, your work."
        hide caroline_normal
        $ _work_perf(1)
        $ _apply_trust("caroline", 1)
    else:
        "Two shifts later: a strategy team sharing the same client family cross-referenced the segment. The 4.2 didn't match their independently sourced data."
        caro "How did the figure become 4.2?"
        mc "You asked me to reconcile it."
        "A pause."
        caro "I asked you to reconcile the gap. Not replace the source number."
        hide caroline_normal
        $ _wev_relbar_open("caroline")
        show screen npc_relbar("caroline")
        show caroline_normal at sprite_r
        menu:
            "Report what you changed.":
                $ corp_integrity_owned_mistake = True
                mc "I replaced the figure. The source was 3.8 — I changed it to 4.2 in the deck."
                caro "Why?"
                mc "Because you needed it reconciled before Monday and I made the wrong call about what that meant."
                "She doesn't defend the original request."
                caro "This goes to compliance. I'll need your written account by end of day."
                hide caroline_normal
                $ _work_perf(1)
                $ _apply_trust("caroline", 2)
                $ corp_integrity_review_extra_shifts = 1
            "Argue that the requested target was reasonable.":
                $ corp_integrity_owned_mistake = False
                mc "The Q2 target was the board-approved expectation. Using it wasn't unreasonable."
                caro "The Q2 target and the Q3 source are different documents."
                mc "The intent was to present the business's trajectory."
                caro "The intent doesn't appear in the report. The number does."
                "She closes the folder."
                hide caroline_normal
                $ _work_perf(-2)
                $ _apply_trust("caroline", -2)
                $ corp_integrity_review_extra_shifts = 2
        $ _wev_relbar_close()
        hide screen npc_relbar
    $ corp_integrity_followup_done = True
    $ corp_integrity_followup_pending = False
    if corp_review_intern_done:
        python:
            _lci_oc = store.corp_integrity_outcome
            if _lci_oc == "smoothed":
                _lci_oc = "smoothed_owned" if store.corp_integrity_owned_mistake else "smoothed_defended"
            _queue_story_aftermath("caroline", "corp_reporting_integrity", "corp_integrity", _lci_oc,
                                   store.day, store.day + 1, "aftermath_corp_reporting_integrity")
    return
