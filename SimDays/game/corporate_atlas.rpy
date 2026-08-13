# Project Atlas — Associate arc for the corporate career.
# Six scenes spanning ~8 shifts at rank Associate (job_rank == 1).
# Triggered from location_office. atlas_score - atlas_risk determines outcome.
# caroline_style carries forward from the Intern arc throughout.


# ── SCENE 1: PROJECT ASSIGNMENT ───────────────────────────────────────────
label corporate_atlas_intro:
    scene goodoffice1
    show screen hud
    "Caroline's assistant flags you on the way in. Third floor. Now."
    show caroline_normal as focus_caroline at sprite_r
    caro "Close the door."
    "She doesn't look up until you do."
    caro "I'm giving you Atlas. Client presentation to the Nexus board in three weeks."
    caro "Meridian Group — financial services, mid-size, looking to enter three new market segments. You'll build the analysis and the presentation from the ground up."
    caro "Martha is already across the Meridian account. She's a resource. She is not the responsible party. You are."
    caro "This is the kind of project that determines what the Associate track looks like for you."
    "A pause. She's waiting for a response, not a question."
    menu:
        "I'll make sure they remember who delivered it.":
            if corporate_style == "ambitious":
                caro "You said something like that in your interview."
                caro "Let's see if it holds at a scale that actually matters."
            else:
                caro "That's one way to approach it."
            $ atlas_route = "ambitious"
            $ atlas_score += 1
            $ atlas_risk += 1
        "I'll make sure the work is solid before anything leaves this floor.":
            if corporate_style == "reliable":
                caro "That's what I'd expect from you."
                caro "Don't let it become an excuse to move slowly. Three weeks isn't long."
            else:
                caro "Good. Meridian will see the seams if you rush it."
            $ atlas_route = "reliable"
            $ atlas_score += 1
        "I'll speak to everyone involved before committing to a direction.":
            if corporate_style == "people_first":
                caro "You've done that before. It's worked."
                caro "Don't let it become a way to avoid making the call yourself."
            else:
                caro "That's a longer road. Make sure the destination is still on time."
            $ atlas_route = "people_first"
            $ atlas_martha_involved = True
            $ atlas_score += 1
    hide focus_caroline
    "Three weeks. One responsible party. You."
    $ atlas_started = True
    $ atlas_intro_done = True
    $ atlas_stage = 1
    $ atlas_shifts = 0
    return


# ── SCENE 2: RESEARCH ─────────────────────────────────────────────────────
label corporate_atlas_research:
    scene goodoffice1
    show screen hud
    "Ten days in."
    "The Meridian files are thorough on the surface and shallow underneath."
    "Three of the growth projections rely on a regulatory environment that shifted eighteen months ago. Caroline's framing assumes a clear runway. The data doesn't."
    "You sit with it for a while."
    menu:
        "Ask Martha. She's already across the account.":
            show martha_neutral as focus_martha at sprite_r
            if martha_trust >= 20:
                ma "I was wondering when you'd get there."
                ma "The Q3 figures are the problem. Meridian's been running pre-reform assumptions on segment two. Nobody corrected them."
                ma "I flagged it six months ago on a different brief. Didn't go anywhere."
                "She pulls up the file without being asked."
                $ _apply_trust("martha", 2)
                $ atlas_score += 2
            else:
                ma "The regulatory gap. Yes, I noticed."
                ma "What do you need?"
                "She helps. It's efficient and a little impersonal — you haven't quite earned the shorthand yet."
                $ _apply_trust("martha", 1)
                $ atlas_score += 1
            hide focus_martha
            $ atlas_martha_involved = True
            $ atlas_credit_choice = "shared"
        "Work through it yourself.":
            "Three days of cross-referencing public filings and internal reports."
            "The gap is real. You can work around it — or you can restructure the whole recommendation."
            "You restructure."
            if corporate_style == "ambitious":
                "The extra exposure bothers you less than it probably should. You file that away for later."
                $ atlas_score += 1
            $ atlas_score += 2
            $ atlas_risk += 1
            $ _work_perf("corporate", 3)
        "Send Caroline a quick holding email." if corporate_style != "reliable":
            "You flag the issue. You haven't solved it yet, but she'll know you've seen it."
            show caroline_normal as focus_caroline at sprite_r
            caro "Thanks for the heads-up. Keep moving — we'll address it in the review."
            hide focus_caroline
            "She doesn't sound worried. That's not necessarily reassuring."
            $ atlas_score += 1
            $ atlas_risk += 2
    $ atlas_research_done = True
    $ atlas_stage = 2
    return


# ── SCENE 3: THE PROBLEM ──────────────────────────────────────────────────
label corporate_atlas_problem:
    scene goodoffice1
    show screen hud
    show martha_neutral as focus_martha at sprite_r
    "Martha finds you before you find her."
    ma "We need to talk about the segment three recommendation."
    "She pulls up a chair without waiting to be invited."
    ma "The growth projection works on paper. But Meridian has roughly two thousand people in segment three's primary market. The restructuring we're recommending cuts that by thirty percent."
    ma "That's the number that doesn't appear anywhere in the slide."
    "A pause."
    ma "Caroline knows."
    menu:
        "It's not our job to make that call. We give the client the best strategic option.":
            hide focus_martha
            show caroline_normal as focus_caroline at sprite_r
            "Caroline agrees."
            caro "The recommendation is sound. Meridian's board will make their own decisions about implementation. We don't run the company."
            caro "Keep it in."
            hide focus_caroline
            "Martha doesn't come to your desk for the rest of the afternoon."
            $ atlas_score += 2
            $ atlas_risk += 2
            $ _apply_trust("caroline", 2)
            $ _apply_trust("martha", -2)
        "At minimum, there should be a note. Something the client can see.":
            ma "A note."
            "She says it flat. Not a question."
            hide focus_martha
            show caroline_normal as focus_caroline at sprite_r
            "You take it to Caroline."
            caro "A disclosure. Fine. One line, appendix, keep it clean."
            hide focus_caroline
            show martha_neutral as focus_martha at sprite_r
            "Martha reads the final version later. She doesn't say thank you."
            "She sits closer at the next team briefing."
            hide focus_martha
            $ atlas_score += 1
            $ atlas_risk = max(0, atlas_risk - 1)
            $ _apply_trust("martha", 3)
            $ _apply_trust("caroline", -1)
        "There's a third version. Same outcome for Meridian, different timeline for the workforce." if corporate_style == "people_first" or skill_biz >= 3:
            ma "I'm listening."
            "You've been turning it over since yesterday. A phased transition — the strategic recommendation holds, but the implementation window is longer."
            ma "It's more expensive in year one."
            "Yes."
            ma "Caroline won't like the cost projection."
            "No."
            hide focus_martha
            "You take it to Caroline anyway."
            show caroline_normal as focus_caroline at sprite_r
            caro "..."
            caro "The board will push back on the extended timeline."
            "She looks at the numbers for a long time."
            caro "It's defensible. Frame it as the conservative scenario. Put it in."
            hide focus_caroline
            show martha_neutral as focus_martha at sprite_r
            "Martha meets your eye when you walk back to your desk. Just briefly."
            hide focus_martha
            $ atlas_score += 3
            $ atlas_risk = max(0, atlas_risk - 1)
            $ _apply_trust("martha", 1)
            $ _apply_trust("caroline", 1)
    $ atlas_problem_done = True
    $ atlas_stage = 3
    return


# ── SCENE 4: CRUNCH ───────────────────────────────────────────────────────
label corporate_atlas_crunch:
    scene goodoffice1
    show screen hud
    "Eight-thirty PM. Most of the floor is empty."
    "Presentation tomorrow at eleven."
    "The deck is close. Not finished. Three sections still need proper narrative. The executive summary is two pages too long."
    menu:
        "Stay and finish it yourself.":
            if worn_out():
                "You're already running low. The kind of tired where you read the same sentence four times and it still doesn't resolve."
                "You stay anyway."
                $ atlas_risk += 1
            $ spend_time(3)
            $ need_energy = max(0, need_energy - 25)
            $ atlas_score += 2
            "Two in the morning. It's done. Not perfect. But close enough that you can defend every line."
        "Ask Martha if she can stay.":
            if martha_trust < 20:
                show martha_neutral as focus_martha at sprite_r
                ma "I have somewhere to be."
                hide focus_martha
                "Fair enough."
                "You close the blinds and stay alone."
                $ spend_time(3)
                $ need_energy = max(0, need_energy - 25)
                $ atlas_score += 1
            else:
                show martha_neutral as focus_martha at sprite_r
                if not atlas_martha_involved:
                    ma "You've been running this alone for three weeks."
                    "A beat."
                    ma "Now you need help the night before."
                    menu:
                        "I should have brought you in earlier. That's on me.":
                            ma "Yes."
                            "A pause."
                            ma "But here we are."
                            $ _apply_trust("martha", 1)
                        "I'm asking now.":
                            "She holds the look for a second longer than comfortable."
                            ma "Fine. Where are we?"
                else:
                    ma "Executive summary or segment three first?"
                $ spend_time(2)
                $ need_energy = max(0, need_energy - 15)
                $ atlas_score += 2
                $ atlas_martha_involved = True
                $ _apply_trust("martha", 1)
                hide focus_martha
                "You finish by midnight. It's better than it would have been alone."
        "Leave it. It's good enough at this point.":
            "You close the laptop."
            $ atlas_risk += 2
            if atlas_score >= 5:
                "Maybe it is. The foundation is solid enough to carry a few rough edges."
            else:
                "You hope the presentation carries what the research couldn't."
    $ atlas_crunch_done = True
    $ atlas_stage = 4
    return


# ── SCENE 5: PRESENTATION ─────────────────────────────────────────────────
label corporate_atlas_presentation:
    scene goodoffice1
    show screen hud
    $ _atlas_result = atlas_score - atlas_risk
    "Conference room B. Meridian's CFO and two directors. Caroline at the back wall. Martha two seats to her right."
    "You present."
    if _atlas_result >= 6:
        # ── Success
        "The room shifts about eight minutes in — the specific change in posture that means people have stopped evaluating and started listening."
        "The segment three slide gets a question. You answer it cleanly. So does the data."
        "Meridian's CFO closes his notebook before you've finished the last section."
        show caroline_normal as focus_caroline at sprite_r
        caro "Well done."
        "She says it in front of the room. That's not a small thing."
        if atlas_martha_involved and atlas_credit_choice == "shared":
            show martha_neutral as focus_martha at sprite_r
            caro "The Meridian account framing was already in good shape when this started. That work held."
            "She's looking at Martha when she says it."
            ma "We built on it."
            "Martha looks at you when she says 'we.'"
            hide focus_martha
        elif atlas_martha_involved:
            show martha_neutral as focus_martha at sprite_r
            "Martha is watching from her seat. She doesn't say anything."
            "She's waiting to see what you do with this moment."
            hide focus_martha
        hide focus_caroline
        $ _work_perf("corporate", 15)
        $ corp_review_score += 2
        $ gain_skill("biz", 8)
    elif _atlas_result >= 3:
        # ── Mixed
        "Most of it lands. The segment three recommendation generates harder questions than the model suggested."
        "The CFO pushes on the timeline. You give him the honest answer about the year-one cost."
        "It's not the room you wanted. But it's not a collapse either."
        show caroline_normal as focus_caroline at sprite_r
        caro "The growth projections will need to be revisited. I'll set up a follow-up call with their team."
        "She's not pleased. She's also not shutting it down."
        hide focus_caroline
        $ _work_perf("corporate", 8)
        $ corp_review_score += 1
        $ gain_skill("biz", 5)
    else:
        # ── Failure
        "The CFO stops you on slide four."
        "The regulatory gap — he's already across it. So is his team. Has been for months."
        "The next forty minutes are a recovery exercise. You answer what you can and acknowledge what you can't."
        "It's the second kind of performance review you don't write down."
        show caroline_normal as focus_caroline at sprite_r
        "Caroline finds you in the corridor when Meridian's team has left."
        caro "We'll regroup this week. I need to understand what happened on the research side."
        "It's not a firing. It's something more uncomfortable — an open question."
        hide focus_caroline
        $ _work_perf("corporate", -5)
        $ gain_skill("biz", 3)
    $ atlas_presentation_done = True
    $ atlas_stage = 5
    return


# ── SCENE 6: AFTERMATH ────────────────────────────────────────────────────
label corporate_atlas_aftermath:
    scene goodoffice1
    show screen hud
    $ _atlas_result = atlas_score - atlas_risk
    "The day after."
    if _atlas_result >= 6:
        "The Meridian debrief is already in the shared folder. Your name is in the subject line."
    elif _atlas_result >= 3:
        "The follow-up call with Meridian is scheduled for next Thursday. People are being professional about it."
    else:
        "Caroline's call with the Meridian account lead is happening right now. You're not in it."
    show martha_neutral as focus_martha at sprite_r
    "Martha finds you at eleven. She brings two coffees and doesn't explain why."
    if _atlas_result >= 6:
        if atlas_martha_involved:
            ma "Good presentation."
            menu:
                "We built something that held up.":
                    ma "Yes."
                    "A pause that isn't uncomfortable."
                    ma "We did."
                    $ _apply_trust("martha", 2)
                    $ _apply_aff("martha", 1)
                "You saw the gap in segment two before I did. The whole thing pivoted on that.":
                    "She's quiet for a moment."
                    ma "I appreciate you saying it. In here, not just in the room."
                    $ _apply_trust("martha", 3)
                    $ _apply_aff("martha", 2)
        else:
            ma "You pulled it off."
            "Something in her tone is weighing something."
            menu:
                "I had good material to work from.":
                    ma "You had the same data I had six months ago. You did something different with it."
                    "That's not quite a compliment and not quite a challenge."
                    $ _apply_trust("martha", 1)
                "It came together in the last few days.":
                    ma "It usually does. For people who put in the days before that."
                    "She means it. The observation lands differently for it."
                    $ _apply_trust("martha", 2)
    elif _atlas_result >= 3:
        ma "The CFO question on segment three."
        "Not a question — a reference point."
        ma "You held the room when it got difficult."
        menu:
            "Barely.":
                ma "Barely is what the client remembers."
                $ _apply_trust("martha", 2)
            "I should have seen it coming in the research stage.":
                ma "Yes. But you answered it when it counted."
                ma "Those aren't the same failure."
                $ _apply_trust("martha", 3)
    else:
        if atlas_martha_involved:
            ma "The regulatory gap."
            "She doesn't say 'I told you.' She doesn't have to."
            ma "We should have pushed harder on the reframe. When we had time to push."
            menu:
                "That's on me. I moved too slowly.":
                    ma "We had the window. We didn't use it well."
                    "The 'we' costs her something. You notice that."
                    $ _apply_trust("martha", 2)
                "I should have escalated sooner when I saw the gap.":
                    ma "Yes. Earlier is always better than in front of the CFO."
                    $ _apply_trust("martha", 1)
        else:
            ma "You ran this without much help."
            "A beat."
            ma "That's a choice. It has a cost. You know that now."
            menu:
                "Yeah.":
                    ma "Good."
                    $ _apply_trust("martha", 1)
                "Next time will be different.":
                    ma "I'll hold you to it."
                    $ _apply_trust("martha", 2)
    "A longer silence. The coffee goes cold at a reasonable pace."
    menu:
        "\"It was a team effort.\" (Say it where Caroline can hear.)":
            show caroline_normal as focus_caroline at sprite_r
            "You say it when Caroline stops by. In front of Martha."
            if _atlas_result >= 6:
                caro "Noted."
                "She sounds like she means it."
            else:
                caro "Let's focus on getting the Meridian follow-up right."
            hide focus_caroline
            $ _apply_trust("martha", 3)
            $ atlas_credit_choice = "shared"
        "\"It was my project. I own the outcome either way.\"":
            "You mean it in both directions — the wins and the gaps."
            if _atlas_result >= 6:
                $ _work_perf("corporate", 3)
                $ _apply_trust("martha", -2)
            else:
                "Martha hears it. Says nothing. The nothing means something."
                $ _apply_trust("martha", 1)
            $ atlas_credit_choice = "self"
        "Say nothing. Let what happened speak for itself." if corporate_style == "people_first" or corporate_style == "reliable":
            "Martha looks at you sideways."
            ma "That's a choice too."
            "It's not nothing. She noticed you're not planting a flag."
            $ _apply_trust("martha", 1)
            $ atlas_credit_choice = "modest"
    hide focus_martha
    $ atlas_completed = True
    $ atlas_aftermath_done = True
    $ atlas_stage = 6
    return
