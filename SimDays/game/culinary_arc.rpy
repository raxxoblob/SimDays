# culinary_arc.rpy — Culinary career preview arc (Commis Chef → Line Cook)
# NPC: Rena — head chef, spare, direct, kitchen-precise. New character.
# Sprites: rena_normal — add to images.rpy when art is ready.
# Defines _CUL_POOL and work_event_culinary (no existing pool for this career).

define rena = Character("Rena", color="#e87040")

init python:
    _CUL_POOL = ["wev_cul_service_rush", "wev_cul_ingredient_shortage", "wev_cul_dish_criticism"]


label work_event_culinary:
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


label cul_review_commis:
    $ cul_review_done = True
    scene kitchen
    show screen hud
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
