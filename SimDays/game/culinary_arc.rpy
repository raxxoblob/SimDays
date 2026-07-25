# culinary_arc.rpy — Culinary career preview arc (Commis Chef → Line Cook)
# NPC: Rena — head chef, spare, direct, kitchen-precise. New character.
# Sprites: rena_normal, rena_talk, rena_happy, rena_angry (kitchen); rena_casual_* (off-duty).
# Defines _CUL_POOL and work_event_culinary (no existing pool for this career).

define rena = Character("Rena", color="#e87040")
define srv  = Character("Server",  color="#a0a0a0")
define wkr  = Character("Kitchen", color="#a0a0a0")

init python:
    _CUL_POOL = ["wev_cul_service_rush", "wev_cul_ingredient_shortage", "wev_cul_dish_criticism"]


label work_event_culinary:
    if cul_crisis_aftermath_pending:
        call cul_crisis_aftermath_callback
        return
    $ _ev = _pick_wev("culinary", _CUL_POOL)
    call expression _ev
    return


label cul_first_day:
    $ rena_met = True
    scene kitchen
    show screen hud
    "The kitchen smells of stock and hot steel before you've found your coat."
    "A woman at the pass glances up once. She has the posture of someone who has already decided today's agenda."
    rena "Commis. Knife roll out. Station three."
    "Station three is prep. A cutting board, mise en place containers, a box of onions."
    rena "Brunoise. Uniform. I'll check in an hour."
    "She walks away before you can answer."
    menu:
        "Start cutting. Work carefully.":
            "You work through twenty onions. By the fifteenth you've found a rhythm. Not fast enough, but consistent."
            rena "Consistent size. That's what we're building."
            $ gain_skill("cook", 4)
            $ _apply_trust("rena", 2)
        "Ask how small the brunoise should be.":
            rena "Three millimetres. Don't ask twice."
            "She demonstrates once and moves on."
            $ gain_skill("cook", 3)
            $ _apply_trust("rena", 1)
        "Watch how the other cooks work first.":
            "A minute of watching tells you more than the instructions did. You adapt your grip."
            "Rena notices. She says nothing."
            $ gain_skill("cook", 5)
            $ _apply_trust("rena", 2)
    return


label cul_task_1:
    $ cul_task_1_done = True
    scene pov_chef
    show screen hud
    rena "Saturday service. You're on garnish and pasta for the prix fixe. First ticket in fifteen."
    "Fourteen minutes in, a table of six arrives. Pasta ordered four times. Your mise en place was set for two covers at a time."
    "The timings collapse in your hands."
    menu:
        "Call for help immediately.":
            rena "How many behind?"
            "\"Four on pasta, two in the window.\""
            rena "Fire garnish at three minutes, not two. Go."
            "She's already elsewhere. You follow the instruction. Three of four land on time."
            $ gain_skill("cook", 4)
            $ _apply_trust("rena", 2)
        "Adapt your timing and push through.":
            "You recalculate on the fly. It works for three covers. The fourth goes out two minutes late."
            "The expeditor calls it. You hear it."
            rena "Late, not wrong. Better than wrong."
            $ gain_skill("cook", 5)
            $ _apply_trust("rena", 3)
        "Simplify the garnish to buy time.":
            "You reduce the plate. It goes out faster. It goes out correctly."
            "Later, Rena looks at one of the returned plates."
            rena "You changed the dish."
            "\"Timing was gone. I had to choose.\""
            rena "Next time: ask first, adapt second. But the service didn't break."
            $ gain_skill("cook", 3)
            $ gain_skill("biz", 2)
            $ _apply_trust("rena", 2)
    return


label cul_npc1_rena:
    $ cul_npc1_done = True
    scene kitchen
    show screen hud
    "You're in early. Rena is already at the pass, breaking down her mise en place."
    "She doesn't acknowledge you, but she doesn't tell you to leave."
    "You start your own prep. After a while she speaks without looking up."
    rena "You're rushing your knife work."
    "She puts her knife down and moves around the pass."
    rena "Grip here. Knuckle guide. Wrist doesn't move — the weight does the work."
    "She shows you once. Steps back."
    menu:
        "Practice until you match her pace.":
            "You work through a rack of carrots. You don't match her pace. You don't waste pieces."
            rena "Consistent. Speed comes."
            $ gain_skill("cook", 6)
            $ _apply_trust("rena", 3)
        "Ask what she was thinking about while she was working.":
            rena "Tonight's service. What goes wrong. How not to let it."
            rena "Prep isn't about the vegetables."
            $ gain_skill("cook", 4)
            $ _apply_aff("rena", 2)
        "Ask about her training.":
            rena "Lyon. Three years. Then a stage in Tokyo."
            rena "Different languages. Same kitchen."
            "She goes back to her mise en place. The conversation is over, but something in her posture is marginally more open."
            $ _apply_trust("rena", 2)
            $ _apply_aff("rena", 2)
    return


label cul_npc2_rena:
    $ cul_npc2_done = True
    scene kitchen
    show screen hud
    "After service. Kitchen clean. Brigade out. Rena is still here, breaking down her side station."
    "You start on your own station without being asked."
    "After a while:"
    rena "Why the kitchen?"
    menu:
        "Tell her honestly — you wanted to make things with your hands.":
            rena "That's the one that lasts."
            "A pause."
            rena "The hours are wrong. The pay is wrong. But nothing else feels this real."
            $ _apply_aff("rena", 3)
        "\"I'm still figuring that out.\"":
            rena "Good. The ones who know too early stop looking."
            $ _apply_trust("rena", 2)
            $ _apply_aff("rena", 2)
        "Ask her the same question back.":
            "She wipes down the steel. Doesn't answer immediately."
            rena "I had a job at an investment firm for eight months after school."
            rena "After the first service in a real kitchen I called in sick and never went back."
            rena "That was the answer."
            $ _apply_aff("rena", 4)
    return


# ─── Service Crisis ────────────────────────────────────────────────────────────
# All 22 CG files confirmed present at 1672×941. Fallback: if a branch CG is
# missing at show time, the scene is still playable via kitchen bg + Rena sprites
# — no conditional guards needed for currently-present files.

label scene_cul_service_crisis:
    $ major_scene_last_day = day

    # ── Opening — normal kitchen bg, Rena at the pass ─────────────────────────
    scene kitchen
    show screen hud
    show rena_normal at sprite_r
    "Rena tapped the edge of the pass twice."
    "Not loudly. She never needed to."
    "The first tickets had not arrived yet, but every station was already waiting for her."
    rena "Tonight does not reward speed."
    "A short pause."
    rena "It rewards not doing the same job twice."
    mc "Comforting."
    rena "It was not meant to be."
    "Rena checks the empty ticket rail."
    rena "Call problems when they are small."
    rena "If I have to discover one myself, it is no longer small."
    mc "Understood."
    rena "Good. Then we do not need to discuss it again."
    hide rena_normal

    # ── CG 1 — Rush ───────────────────────────────────────────────────────────
    scene cg_cul_crisis_rush with dissolve
    "The first forty minutes passed without a gap between orders."
    "Heat gathered beneath the lights."
    "Metal struck metal. Pans changed hands. Tickets covered the rail faster than finished plates could clear it."
    rena "Two minutes on garnish."
    rena "Fish station, confirm."
    wkr "Confirmed."
    rena "Table eight walks first. Twelve follows."
    mc "Sauce in ninety seconds."
    "Rena looked briefly toward the station."
    rena "You have sixty."
    mc "Of course I do."
    rena "You said ninety. The room gave you sixty."
    "Rena immediately returned to the pass."
    "She did not sound angry."
    "That somehow made the missing thirty seconds feel more real."

    # ── CG 2 — Pressure ───────────────────────────────────────────────────────
    scene cg_cul_crisis_pressure with dissolve
    "The rail filled."
    "One plate waited for garnish."
    "Another waited for the same sauce as table twelve."
    "A third ticket arrived before the second had been fully read."
    srv "Rena, table six is ready."
    rena "Walk six."
    rena "Hold twelve."
    mc "Thirty seconds."
    rena "You said that twenty seconds ago."
    mc "I know."
    rena "Then do not spend another one explaining it."
    "A pan hissed too loudly."
    "The sauce tightened around the edge."
    "The heat came down. The spoon drew a line through it."

    # ── CG 3 — Sauce close-up ─────────────────────────────────────────────────
    scene cg_cul_crisis_sauce_closeup with dissolve
    "The line left by the spoon should have closed smoothly."
    "It did not."
    "A thin sheen of fat gathered near the edge of the pan."
    "The centre still held together. The outside had already begun to separate."
    mc "No."
    rena "Table twelve, walking in two."
    "Three plates were waiting for that sauce."
    "The kitchen continued moving as though nothing had changed."
    "There was still time to say something."
    "There was also just enough time to believe it could be fixed without anyone knowing."

    # ── CG 4 — Table waiting ──────────────────────────────────────────────────
    scene cg_cul_crisis_table_waiting with dissolve
    srv "Rena. Twelve is asking."
    "Rena checked the rail without looking away from the pass."
    rena "Tell them five minutes."
    srv "They were already told two."
    "Rena finally looked toward the server."
    rena "Then do not lie to them twice."
    rena "Tell them five."
    srv "Five."
    rena "And bring them bread."
    "Five honest minutes."
    "The sauce did not have five."
    "A look down at the pan."
    "A beat of silence beneath the kitchen noise."

    # ── CG 5 — Rena notices ───────────────────────────────────────────────────
    scene cg_cul_crisis_rena_notices with dissolve
    "Rena returned one ticket to the rail."
    "Then she saw that the station had stopped."
    "Only for a second."
    "That was enough."
    show rena_normal at sprite_r
    rena "What exactly happened?"
    menu:
        "\"Tell her now. 'The sauce is splitting.'\"":
            jump _cul_crisis_A
        "\"Try to recover it before she has to know.\"":
            jump _cul_crisis_B
        "\"Stop the affected dishes. Nothing leaves like this.\"":
            jump _cul_crisis_C
        "\"Send them. Maybe no one notices.\"":
            jump _cul_crisis_D


    # ── Branch A — Tell Rena immediately ──────────────────────────────────────
    label _cul_crisis_A:
        $ cul_crisis_branch = "tell"
        $ cul_crisis_rena_informed = True
        $ cul_crisis_bad_plate = False
        hide rena_normal
        scene cg_cul_crisis_admit with dissolve
        mc "The sauce is splitting."
        show rena_talk at sprite_r
        rena "How long have you known?"
        mc "Less than thirty seconds."
        "Rena looked at the pan."
        hide rena_talk
        show rena_normal at sprite_r
        rena "Good."
        mc "Good?"
        rena "You told me at thirty."
        rena "Not at zero."
        "Rena turned slightly toward the pass."
        rena "Hold twelve. Clean remake."
        srv "How long?"
        rena "Five true minutes."
        "Rena turned back."
        hide rena_normal
        show rena_talk at sprite_r
        rena "Fresh pan."

        scene cg_cul_crisis_guided_recovery with dissolve
        show rena_talk at sprite_r
        rena "Two spoonfuls from the base."
        rena "Off the heat."
        rena "Whisk from the centre. Not the edge."
        mc "Like this?"
        rena "If you have time to ask, you are not looking at it."
        "The oily line began to disappear."
        "The sauce tightened, then smoothed."
        hide rena_talk
        show rena_normal at sprite_r
        rena "Now taste it."
        mc "It is right."
        rena "Then finish the plates."

        scene cg_cul_crisis_clean_send with dissolve
        show rena_normal at sprite_r
        srv "Table twelve?"
        "Rena checked the final plate."
        rena "Walk twelve."
        "The server took the dishes."
        "An exhale. Quiet enough that only Rena heard it."
        rena "Do that after service."
        mc "Right."
        hide rena_normal
        show rena_happy at sprite_r
        rena "You made a mistake."
        rena "You did not make me discover it."
        rena "Back to work."
        hide rena_happy
        $ cul_crisis_technical = "recovered"
        $ cul_crisis_aftermath = "good"
        $ _apply_trust("rena", 3)
        $ _apply_aff("rena", 1)
        $ gain_skill("cook", 4)
        $ _work_perf(3)
        jump _cul_crisis_last_ticket


    # ── Branch B — Solo recovery ───────────────────────────────────────────────
    label _cul_crisis_B:
        $ cul_crisis_branch = "solo"
        $ cul_crisis_rena_informed = False
        $ cul_crisis_bad_plate = False
        hide rena_normal
        scene cg_cul_crisis_solo_attempt with dissolve
        mc "Nothing happened."
        show rena_normal at sprite_r
        "Rena watched for a fraction of a second."
        rena "That was not an answer."
        mc "I have it."
        rena "Then have it quickly."
        hide rena_normal
        "Rena returned to the pass."
        "The pan came away from the heat."
        "A small amount of base. A faster whisk. No announcement. No stopped plates."
        "Fix it first. Explain it later."

        if skill_cook >= 2:
            scene cg_cul_crisis_solo_success with dissolve
            "The texture closed."
            "The surface smoothed."
            "The spoon left a clean line that disappeared almost immediately."
            mc "Walk twelve."
            "The plates left."
            show rena_normal at sprite_r
            "Rena turned toward the station after the server took them."
            rena "What happened?"
            mc "The sauce split."
            rena "And?"
            mc "I recovered it."
            "Rena looked at the empty space where the plates had been."
            rena "You recovered the sauce."
            rena "You did not recover the time you spent deciding whether to tell me."
            mc "The food was right."
            rena "This time."
            "A ticket arrived."
            rena "Back to service."
            rena "We discuss the rest when the rail is empty."
            hide rena_normal
            $ cul_crisis_technical = "recovered"
            $ cul_crisis_aftermath = "mixed"
            $ _apply_trust("rena", -1)
            $ gain_skill("cook", 5)
            $ _work_perf(2)
        else:
            scene cg_cul_crisis_solo_failure with dissolve
            "The sauce loosened."
            "For one second it looked as though it might come back."
            "Then the emulsion broke completely."
            show rena_normal at sprite_r
            "Rena turned from the pass."
            rena "Step back."
            mc "I can still recover it."
            rena "No."
            "Rena approached the station."
            rena "You already spent the time you had."
            "A step aside."
            hide rena_normal
            show rena_talk at sprite_r
            rena "Fresh pan."
            rena "Start again."
            "Rena turned to the server."
            rena "Table twelve is delayed."
            srv "How long?"
            rena "Seven minutes."
            srv "They will not like that."
            rena "They would like the alternative less."
            hide rena_talk
            show rena_normal at sprite_r
            "Rena looked back at the station."
            rena "You call the next problem before you negotiate with it."
            hide rena_normal
            "Seven minutes. Clean restart."
            $ cul_crisis_technical = "failed"
            $ cul_crisis_aftermath = "bad"
            $ _apply_trust("rena", -3)
            $ _work_perf(-5)
        jump _cul_crisis_last_ticket


    # ── Branch C — Stop the dishes ─────────────────────────────────────────────
    label _cul_crisis_C:
        $ cul_crisis_branch = "stop"
        $ cul_crisis_rena_informed = True
        $ cul_crisis_bad_plate = False
        hide rena_normal
        scene cg_cul_crisis_stop_pass with dissolve
        mc "Hold twelve."
        "The server reached for the plates and stopped."
        srv "They are waiting."
        mc "Then they wait."
        show rena_normal at sprite_r
        "Rena turned."
        rena "Reason."
        mc "The sauce is breaking."
        mc "These do not leave."
        "A brief pause. Rena checked the plate."
        rena "Correct."
        rena "Move them."

        scene cg_cul_crisis_resequence with dissolve
        hide rena_normal
        show rena_talk at sprite_r
        "Rena pulled the affected tickets aside."
        rena "Walk fourteen first."
        rena "Fire twelve again."
        rena "Tell the floor seven minutes."
        srv "Seven?"
        rena "Seven true minutes."
        rena "Not three imaginary ones."
        "The server left."
        hide rena_talk
        show rena_normal at sprite_r
        rena "New sauce."
        mc "Understood."
        rena "You protected the standard."
        rena "Now recover the timing."
        "The kitchen closed around the new sequence."
        "Unrelated plates continued to leave."
        "Table twelve moved backward without disappearing."

        scene cg_cul_crisis_delayed_send with dissolve
        show rena_normal at sprite_r
        "Rena checked the replacement plate."
        rena "Sauce."
        mc "Stable."
        "Rena tasted it."
        rena "Walk twelve."
        "The server took the dishes."
        mc "Seven minutes."
        rena "Yes."
        mc "That still feels like a failure."
        rena "It is a delay."
        rena "Do not confuse an imperfect result with a dishonest one."
        rena "Back to work."
        hide rena_normal
        $ cul_crisis_technical = "remade"
        $ cul_crisis_aftermath = "good"
        $ _apply_trust("rena", 2)
        $ gain_skill("cook", 2)
        $ _work_perf(1)
        jump _cul_crisis_last_ticket


    # ── Branch D — Send anyway ─────────────────────────────────────────────────
    label _cul_crisis_D:
        $ cul_crisis_branch = "send"
        $ cul_crisis_rena_informed = False
        $ cul_crisis_bad_plate = True
        hide rena_normal
        scene cg_cul_crisis_send_anyway with dissolve
        "The sauce still looked acceptable from a distance."
        "Under the heat lamps, the shine almost passed for intentional."
        mc "Walk twelve."
        "The server took them."
        "Rena remained occupied with another ticket."
        "The plates crossed the pass."
        "The problem left the kitchen."

        scene cg_cul_crisis_dining_consequence with dissolve
        "Two minutes later, a fork stopped halfway back to the plate."
        "The guest did not raise their voice."
        "They did not need to."
        "The server looked down at the sauce."
        "The plate began its journey back."

        scene cg_cul_crisis_returned_plate with dissolve
        "The server placed the plate on the pass."
        srv "Table twelve says the sauce is oily."
        show rena_normal at sprite_r
        "Rena looked at the dish."
        "She touched the sauce with the edge of a spoon."
        "Then she looked toward the station."
        rena "When did you know?"
        mc "Before it left."
        "A pause."
        rena "Then this is not about sauce."
        mc "I thought it might hold."
        rena "You did not think it would hold."
        rena "You hoped nobody would notice."
        hide rena_normal
        show rena_talk at sprite_r
        "Rena moved the plate aside."
        rena "Remake it."
        mc "Rena—"
        rena "After service."
        rena "Not now."
        hide rena_talk
        show rena_normal at sprite_r
        "Rena turned back to the pass."
        rena "Fresh table twelve. Seven minutes."
        hide rena_normal
        "The table was remade. Service continued."
        $ cul_crisis_technical = "failed"
        $ cul_crisis_aftermath = "bad"
        $ _apply_trust("rena", -4)
        $ _work_perf(-8)
        jump _cul_crisis_last_ticket


    # ── Common ending — last ticket ───────────────────────────────────────────
    label _cul_crisis_last_ticket:
        scene cg_cul_crisis_last_ticket with dissolve
        "The final ticket remained alone on the rail."
        "No new paper appeared behind it."
        "The last plate crossed the pass."
        show rena_normal at sprite_r
        "Rena removed the ticket."
        "The kitchen noise began to fall away."
        rena "Clean down."
        hide rena_normal
        wkr "Service clear."
        rena "Quietly."
        "Burners clicked off."
        "Pans entered the sink."
        "Without the tickets, the room suddenly seemed larger."
        "Rena waited until the other staff had moved away."
        if cul_crisis_aftermath == "good":
            jump _cul_crisis_aftermath_good
        elif cul_crisis_aftermath == "mixed":
            jump _cul_crisis_aftermath_mixed
        else:
            jump _cul_crisis_aftermath_bad


    # ── Good aftermath ────────────────────────────────────────────────────────
    label _cul_crisis_aftermath_good:
        scene cg_cul_crisis_after_good with dissolve
        show rena_normal at sprite_r
        "Rena stood beside the cleaned pass."
        "Not opposite. Beside."
        rena "Do you know why I asked when you noticed?"
        mc "To see how long I waited."
        rena "To see which problem I was dealing with."
        mc "The sauce."
        rena "No."
        rena "The sauce was simple."
        rena "The question was whether I could trust the information from your station."
        if cul_crisis_branch == "tell":
            rena "You called it early."
            rena "That gave us choices."
            mc "I still caused the delay."
            rena "You caused a problem."
            rena "You prevented a failure."
        else:
            rena "You stopped the plate before you had permission."
            mc "I knew it was wrong."
            rena "That is why it was the correct decision."
            mc "You are not angry about the delay?"
            rena "I dislike delays."
            rena "I dislike serving food we know is wrong more."
        rena "Next shift, I will give you one call at the pass."
        mc "One?"
        hide rena_normal
        show rena_happy at sprite_r
        rena "Earn the second."
        hide rena_happy
        if cul_crisis_branch == "tell":
            $ add_relationship_memory("rena", "crisis_tell", "Called the sauce problem early. Choices remained.")
        else:
            $ add_relationship_memory("rena", "crisis_stop", "Stopped a compromised plate at the pass.")
        jump _cul_crisis_close


    # ── Mixed aftermath ───────────────────────────────────────────────────────
    label _cul_crisis_aftermath_mixed:
        scene cg_cul_crisis_after_mixed with dissolve
        show rena_normal at sprite_r
        "Rena stood on the opposite side of the pass."
        rena "You recovered the sauce."
        mc "Yes."
        rena "And you believe that ends the discussion."
        mc "The plate was right."
        rena "The plate was right."
        rena "Your timing was not."
        mc "I knew I could fix it."
        rena "No."
        rena "You believed you might fix it."
        rena "There is a difference."
        mc "So I should have called you even if I could handle it?"
        rena "You should have called the risk."
        rena "I do not need every problem handed to me."
        rena "I need to know which problems can reach the pass."
        "A pause."
        mc "Understood."
        rena "Good."
        rena "Next time, prove it before the dining room becomes part of the experiment."
        hide rena_normal
        $ add_relationship_memory("rena", "crisis_solo", "Recovered the sauce alone. Concealed the risk.")
        jump _cul_crisis_close


    # ── Bad aftermath ─────────────────────────────────────────────────────────
    label _cul_crisis_aftermath_bad:
        scene cg_cul_crisis_after_bad with dissolve
        show rena_angry at sprite_r
        if cul_crisis_branch == "solo":
            rena "The first mistake was technical."
            mc "The sauce."
            rena "Yes."
            rena "The second was waiting until you no longer had a choice."
            mc "I thought I could recover it."
            rena "You were allowed to try."
            rena "You were not allowed to hide the cost of trying."
            mc "I understand."
            rena "No."
            rena "You understand that it went badly."
            rena "Understanding the rule comes next."
            rena "Tomorrow, you call every change at your station."
            rena "Even the ones you solve."
            hide rena_angry
            $ add_relationship_memory("rena", "crisis_solo_fail", "Technical mistake, delayed escalation.")
        else:
            rena "The sauce was a mistake."
            rena "Sending it was a decision."
            mc "I know."
            rena "No."
            rena "You know because it came back."
            rena "I need to know what you understood before it left."
            mc "I hoped it would pass."
            rena "You hoped the dining room would pay for your silence."
            "A long pause."
            mc "I am sorry."
            rena "Apologies matter after the truth."
            rena "You had the truth at the station."
            rena "You chose not to use it."
            mc "What happens now?"
            rena "Tomorrow, you work."
            rena "You tell me every call before you make it."
            rena "And you rebuild the part that did not come back on that plate."
            mc "Your trust."
            rena "Yes."
            rena "That."
            hide rena_angry
            $ add_relationship_memory("rena", "crisis_send", "Sent compromised food knowing the risk.")
        jump _cul_crisis_close


    # ── Closing ───────────────────────────────────────────────────────────────
    label _cul_crisis_close:
        scene kitchen with dissolve
        if cul_crisis_aftermath == "good":
            show rena_happy at sprite_r
        elif cul_crisis_aftermath == "mixed":
            show rena_normal at sprite_r
        else:
            show rena_angry at sprite_r
        "The kitchen looked ordinary again."
        "Clean steel. Empty rail. Cooling lights."
        "But the next shift would not begin from the same place."
        if cul_crisis_aftermath == "good":
            hide rena_happy
        elif cul_crisis_aftermath == "mixed":
            hide rena_normal
        else:
            hide rena_angry
        $ scene_cul_service_crisis_done = True
        $ cul_crisis_aftermath_pending = True
        return


label cul_crisis_aftermath_callback:
    $ cul_crisis_aftermath_pending = False
    scene kitchen
    show screen hud
    show rena_normal at sprite_r
    if cul_crisis_aftermath == "good":
        rena "The crisis service."
        "A pause. She doesn't look up from the pass."
        if cul_crisis_branch == "tell":
            rena "You called it when you knew."
            rena "That is the standard."
            rena "Keep doing that."
        else:
            rena "You stopped the plate."
            rena "The table had a gap. Nothing came back."
            rena "That was the correct sequence."
        $ _apply_trust("rena", 1)
    elif cul_crisis_aftermath == "mixed":
        rena "The sauce recovered."
        rena "You waited before you moved."
        rena "Next time — the second you know the risk exists, you name it."
        rena "Not weakness. That is how the kitchen keeps running."
    else:
        rena "You have thought about it."
        "It is not a question."
        rena "Good. Do not stop."
    hide rena_normal
    return


label cul_review_commis:
    $ cul_review_done = True
    scene kitchen
    show screen hud
    show rena_normal at sprite_r
    if cul_crisis_aftermath == "good":
        rena "During the crisis service — you told me when you knew."
        "She says it like she's noting a fact, not offering a compliment."
        rena "That's the standard. It's harder to do than it looks."
    elif cul_crisis_aftermath == "bad":
        rena "The plates that came back."
        "A pause. She looks at the pass, not at you."
        rena "You know what the error was. Don't repeat it."
    rena "You're moving to line cook. More heat, more responsibility, more station ownership."
    rena "Your mise en place has been clean for two weeks. Your timing is still developing. That's acceptable."
    menu:
        "\"Thank you. I'll keep working on the timing.\"":
            rena "See that you do."
            "A beat. The corners of her mouth don't quite move."
            rena "You've been reliable. That counts."
            $ _apply_trust("rena", 2)
        "\"What's the line cook station like?\"":
            rena "More covers, faster decisions, less forgiveness for errors. You'll learn what you can handle."
            $ gain_skill("cook", 3)
        "\"I'm ready.\"":
            rena "I know. Otherwise you wouldn't be moving."
            $ _apply_trust("rena", 1)
    hide rena_normal
    $ promote()
    return


# ─── Arc work events ───────────────────────────────────────────────────────

label wev_cul_service_rush:
    $ _mark_wev("culinary", "wev_cul_service_rush")
    scene pov_chef
    show screen hud
    "A table for two becomes eight — the reservation system has a duplicate. Six more covers than projected."
    "Your mise en place is two-thirds spent."
    menu:
        "Adapt and communicate with the pass.":
            "You call it out clearly. The expeditor adjusts the fire order. You make it work."
            $ gain_skill("cook", 4)
            $ _work_perf(4)
        "Push through quietly without flagging it.":
            "You get through it. Barely. One dish is plated less carefully than it should be."
            "The expeditor notices."
            $ _work_perf(1)
    return


label wev_cul_ingredient_shortage:
    $ _mark_wev("culinary", "wev_cul_ingredient_shortage")
    scene kitchen
    show screen hud
    "The lamb delivery didn't come in. It's on the menu tonight."
    rena "Figure it out. Service in forty minutes."
    menu:
        "Propose a substitute you know works.":
            "Beef bavette. Similar prep time, same price point. You make the case quickly."
            rena "Write it on the spec board. Tell the waitstaff."
            $ gain_skill("cook", 5)
            $ _apply_trust("rena", 2)
        "Ask the senior cook what they'd do.":
            "They give you an answer. Not the one Rena would have given, but workable."
            "You adapt. Rena watches but says nothing."
            $ gain_skill("cook", 3)
    return


label wev_cul_dish_criticism:
    $ _mark_wev("culinary", "wev_cul_dish_criticism")
    scene kitchen
    show screen hud
    "A returned dish. The head waiter sets it on the pass."
    "\"Table says over-salted.\""
    rena "Look at you."
    menu:
        "Taste it. Confirm whether the criticism is correct.":
            "You taste it. They're right."
            "\"Sauce reduction went too far. My station.\""
            rena "Redo. Two minutes."
            "You plate clean. The dish goes back out."
            $ _work_perf(3)
        "Defend it — it was seasoned correctly at the pass.":
            rena "Taste it."
            "You taste it. They're right."
            "You don't say anything."
            rena "Redo."
            $ _work_perf(-1)
    return
