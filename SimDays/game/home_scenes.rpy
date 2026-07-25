# home_scenes.rpy — home-visit scenes unlocked by owned items + NPC relationships.
# Each scene: NPC-initiated via phone invite → commitment → triggers at location_home.
# Dinner: player-initiated from home menu (own_kitchen_set gate).


# ── Eli: side project ─────────────────────────────────────────────────────────

label home_eli_side_project_scene:
    $ complete_commitment("eli_side_project_1")
    scene expression home_bg()
    show screen hud
    show eli_normal at sprite_r
    "Eli arrives at seven with a laptop bag and no preamble."
    eli "Here's the scope: a small data pipeline. Processing is slow. I want a second read."
    $ _cg = get_home_scene_cg("eli_side_project")
    if _cg:
        scene expression _cg with dissolve
        show screen hud
    "You both pull up the repository. The problem is clear after ten minutes. The fix isn't."
    menu:
        "Work through it correctly. More time, cleaner result.":
            "Three hours. But when it's done it holds."
            $ gain_skill("prog", 6)
            $ _apply_trust("eli", 4)
            $ _apply_aff("eli", 2)
            eli "This holds up. I'll merge it."
        "Quick fix — good enough for now.":
            "Twenty minutes. The pipeline runs. Eli reads the diff for a long time."
            $ gain_skill("prog", 3)
            eli "It works. It'll bite you in six months."
            eli "But you made the call. File it."
            $ _apply_trust("eli", 1)
        "Close the laptops. Just talk.":
            "You close the laptops."
            "Eli talks about the thesis. Environmental systems, policy modelling. The pipeline can wait."
            $ _apply_aff("eli", 5)
            $ _apply_trust("eli", 2)
            eli "We can finish this another time. This was better."
    hide eli_normal
    return


# ── Nora: coffee tasting ──────────────────────────────────────────────────────

label home_nora_coffee_scene:
    $ complete_commitment("nora_coffee_1")
    scene expression home_bg()
    show screen hud
    show nora_casual_normal at sprite_r   # off-duty, at your place — not the barista apron
    "Nora arrives exactly at ten. She walks straight to the machine."
    n "How long have you owned this and not adjusted the grind size?"
    "She doesn't wait for an answer."
    $ _cg = get_home_scene_cg("nora_coffee")
    if _cg:
        scene expression _cg with dissolve
        show screen hud
    n "Okay. Here's what's actually happening between the bean and the cup."
    "She makes three espressos. Talks through each one."
    "The third is the best coffee you've had in your apartment."
    menu:
        "\"How long did it take you to learn all this?\"":
            n "Five years behind a bar. You stop noticing after a while."
            n "Then someone asks and you realise you do know a lot about espresso."
            $ _apply_aff("nora", 4)
        "Just drink and listen.":
            "Nora appreciates the silence. She fills it anyway."
            n "Someday I want my own place. People come for the coffee, not the atmosphere."
            $ _apply_aff("nora", 3)
            $ _apply_trust("nora", 2)
    "When she leaves, your apartment smells like a proper café."
    $ home_coffee_calibrated = True
    hide nora_casual_normal
    return


# ── Zoe: guitar session ───────────────────────────────────────────────────────

label home_zoe_guitar_scene:
    $ complete_commitment("zoe_guitar_1")
    scene expression home_bg()
    show screen hud
    show zoe_street_neutral at sprite_r
    "Zoe arrives with a sketchbook under one arm. She sits in the corner without being asked."
    z "Go on then. Prove it isn't furniture."
    $ _cg = get_home_scene_cg("zoe_guitar")
    if _cg:
        scene expression _cg with dissolve
        show screen hud
    "You pick up the guitar."
    if skill_music >= 5:
        "It comes out better than expected. A couple of wrong notes, then something that actually sounds like music."
        z "Okay. That was actually fine."
        $ _apply_aff("zoe", 5)
        $ _apply_trust("zoe", 3)
        $ gain_skill("music", 5)
    elif skill_music >= 3:
        "Rough around the edges. But there's something there."
        z "Not bad for someone who clearly doesn't practice enough."
        $ _apply_aff("zoe", 3)
        $ gain_skill("music", 4)
    else:
        "It's bad. Not charming-bad. Just bad."
        z "This is the longest minute of my life."
        "She's smiling, though."
        $ _apply_aff("zoe", 2)
        $ gain_skill("music", 3)
    "Zoe sketches while you play. You stop worrying about mistakes."
    menu:
        "Ask her what she's drawing.":
            z "You. Don't look yet."
            $ _apply_aff("zoe", 3)
            z "Okay, now."
            "A quick sketch — guitar, posture, not quite your face. Better than a photo."
        "Keep playing until she asks you to stop.":
            "She doesn't ask you to stop for an hour."
            $ gain_skill("music", 3)
            $ _apply_trust("zoe", 2)
    hide zoe_street_neutral
    return


# ── Dinner invite ─────────────────────────────────────────────────────────────

label home_dinner_invite_menu:
    scene expression home_bg()
    show screen hud
    $ _dinner_ok = any(
        home_invite_available(nid, min_aff=20, min_trust=15)
        for nid in ["martha", "nora", "zoe", "marcus", "lena", "kai", "eli"]
    )
    if not _dinner_ok:
        "Nobody's close enough to invite over yet."
        return
    menu (screen="activity"):
        "Invite Martha (3h)"   if home_invite_available("martha",  min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_martha
        "Invite Nora (3h)"     if home_invite_available("nora",    min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_nora
        "Invite Zoe (3h)"      if home_invite_available("zoe",     min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_zoe
        "Invite Marcus (3h)"   if home_invite_available("marcus",  min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_marcus
        "Invite Dr. Lena (3h)" if home_invite_available("lena",    min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_lena
        "Invite Kai (3h)"      if home_invite_available("kai",     min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_kai
        "Invite Eli (3h)"      if home_invite_available("eli",     min_aff=20, min_trust=15):
            $ spend_time(3)
            call home_dinner_scene_eli
        "Not tonight":
            pass
    return


label home_dinner_scene_martha:
    scene expression home_bg()
    show screen hud
    show martha_dress_normal at sprite_r
    "Martha arrives on time. She glances at the kitchen before she says hello."
    ma "You're more organised than I expected."
    menu:
        "\"I had time to prepare.\"":
            ma "Good. Preparation is undervalued."
            $ _apply_trust("martha", 2)
        "\"The chaos is in the bedroom.\"":
            "A pause. Something that might be a smile."
            $ _apply_aff("martha", 3)
    "She eats without complaining. You decide that counts."
    ma "This was a good idea. Don't tell Caroline I said that."
    $ _apply_aff("martha", 3)
    $ _apply_trust("martha", 2)
    hide martha_dress_normal
    return


label home_dinner_scene_nora:
    scene expression home_bg()
    show screen hud
    show nora_casual_normal at sprite_r   # dinner guest at your place, off-duty
    "Nora was a guest for exactly six minutes before she was in the kitchen."
    n "You were going to deglaze with water. I saw you reach for the tap."
    "You were."
    n "Wine. Always wine. Or stock — but you don't have stock, so. Wine."
    menu:
        "\"I thought the host was supposed to cook.\"":
            n "You are cooking. I'm supervising. There's a difference."
            $ _apply_aff("nora", 4)
        "Let her take over completely.":
            "The best meal you've had in your apartment. Nora doesn't mention it."
            $ _apply_aff("nora", 3)
            $ _apply_trust("nora", 3)
    "You eat at the counter because neither of you notices the table until it's too late."
    $ _apply_aff("nora", 3)
    hide nora_casual_normal
    return


label home_dinner_scene_zoe:
    scene expression home_bg()
    show screen hud
    show zoe_street_neutral at sprite_r
    "Zoe shows up with a bottle of something obscure and a slightly suspicious expression."
    z "This is either really good or from a petrol station. I genuinely don't know."
    "It turns out to be really good."
    menu:
        "Ask her to stay longer after dinner.":
            z "I wasn't planning to leave yet anyway."
            $ _apply_aff("zoe", 5)
            $ _apply_trust("zoe", 2)
        "Talk about her current project.":
            z "The client wants beige. Everywhere. Functional beige."
            z "I'm going to give them functional beige and then paint something completely different at home."
            $ _apply_trust("zoe", 3)
    $ _apply_aff("zoe", 3)
    hide zoe_street_neutral
    return


label home_dinner_scene_marcus:
    scene expression home_bg()
    show screen hud
    show marcus_casual_normal at sprite_r
    "Marcus looks around when he comes in."
    m "The place finally looks like someone lives here."
    "He means it as a compliment."
    menu:
        "\"It took a while.\"":
            m "That's how most things work."
            $ _apply_trust("marcus", 2)
        "\"Still a work in progress.\"":
            m "Aren't we all."
            $ _apply_aff("marcus", 3)
    "He eats two portions and tells you about a construction job that went badly — somehow funny."
    $ _apply_aff("marcus", 4)
    hide marcus_casual_normal
    return


label home_dinner_scene_lena:
    scene expression home_bg()
    show screen hud
    show drlena_normal at sprite_r
    "Lena arrives directly from a shift. She looks tired in a way she doesn't mention."
    lena "I should have changed. Sorry."
    menu:
        "\"How was the shift?\"":
            lena "Long. But there was a good outcome."
            lena "That's the part worth remembering."
            $ _apply_trust("lena", 3)
        "Don't ask. Just pour her a drink.":
            lena "Thank you. I needed this."
            $ _apply_aff("lena", 5)
    "A quiet dinner. She relaxes slowly, like something stops running."
    $ _apply_aff("lena", 3)
    $ _apply_trust("lena", 2)
    # Extended kitchen scene if she stays for a drink
    if not kitchen_lena_extended_done and lena_trust >= 30 and own_kitchen_set:
        call scene_kitchen_lena_extended
    hide drlena_normal
    return


label home_dinner_scene_kai:
    scene expression home_bg()
    show screen hud
    show kai_normal at sprite_r   # home dinner — casual, not gym kit
    "Kai checks the portion size before she sits down."
    kai "Okay, this is a real amount of food. I was worried."
    menu:
        "\"I made extra.\"":
            kai "Smart. I always eat extra."
            $ _apply_aff("kai", 3)
        "Work out the protein content together.":
            kai "Finally, someone asks the right questions."
            "She pulls out her phone and calculates it."
            $ _apply_aff("kai", 4)
            $ _apply_trust("kai", 2)
    "She eats quickly and with focus. It's somehow a compliment to the food."
    kai "Same time next week?"
    $ _apply_aff("kai", 3)
    hide kai_normal
    return


# ── Eli: dinner ───────────────────────────────────────────────────────────────

label home_dinner_scene_eli:
    scene expression home_bg()
    show screen hud
    show eli_normal at sprite_r
    "Eli arrives at exactly the time you agreed. She has brought a packet of jasmine rice."
    "She looks at the table, looks at the rice, looks at you."
    eli "I didn't think that through."
    "She says it calmly. Like a bug she's just spotted."
    $ _cg = get_home_scene_cg("eli_dinner")
    if _cg:
        scene expression _cg with dissolve
        show screen hud
    "The meal is fine — whatever you made. Eli eats with careful attention."
    "Halfway through, she notices something about your setup — the way the monitor is positioned, the cable routing on your desk, a book left out at an odd angle. She tilts her head slightly."
    eli "You put the router there on purpose."
    "It's not a question."
    menu:
        "\"You notice a lot.\"":
            eli "I notice most things. It's not always useful."
            $ _apply_trust("eli", 3)
            "A pause. She looks back at the rice, still on the counter."
            eli "Here it is. The rice was a mistake."
            "She seems genuinely pleased with this conclusion."
        "Ask what she's been working on.":
            eli "The thesis chapter I've been avoiding for six weeks. I finally opened it this morning."
            $ _apply_aff("eli", 2)
            eli "Coming here felt easier. Which is probably the point."
            $ _apply_trust("eli", 2)
        "[[Wait and see if she says something unprompted.]]":
            "She does. Eventually."
            eli "I don't come to people's homes very often. This is — it's good. Thank you."
            "She says it to the table. Means it to you."
            $ _apply_aff("eli", 3)
            $ _apply_trust("eli", 2)
    "Near the end of the meal the intellectual scaffolding drops for one sentence."
    eli "I like it here."
    "She doesn't follow it up. The jasmine rice is still on the counter."
    $ _apply_aff("eli", 3)
    $ add_relationship_memory("eli", "eli_home_dinner", "Home dinner — the rice")
    $ eli_dinner_done = True
    hide eli_normal
    return


# ── Nora: cheap-home cooking ──────────────────────────────────────────────────
# Only available when apartment_tier == 1; guard enforced by phone-queue condition.
# Prerequisite: home_coffee_calibrated (set by home_nora_coffee_scene).
# State: nora_cooking_state (none|offered|pending|done); cooldown via nora_cooking_declined_day.

label scene_nora_cheap_home_cooking:
    $ complete_commitment("nora_cheap_home_cooking_1")
    if apartment_tier != 1:
        # Commitment fired after player moved out of the cheap home. The cheap-hob
        # lesson was specific to that kitchen; moving ends the opportunity permanently.
        scene expression home_bg()
        show screen hud
        show nora_casual_normal at sprite_r
        n "I had this all planned out. The hob, the timing — built around that kitchen."
        n "Not this one. That was a cheap-hob lesson. It doesn't translate."
        hide nora_casual_normal
        $ nora_cooking_state = "done"
        return
    scene expression home_bg()
    show screen hud
    show nora_casual_normal at sprite_r
    "Nora arrives at six, looks at your kitchen once, and starts rearranging the worktop without asking."
    n "The hob's uneven. You've been compensating for the left burner without noticing."
    "She's right. You have been."
    scene cg_nora_cooking_cheap with dissolve
    show screen hud
    n "Okay. Limited equipment, limited space. You work with what's there."
    "She moves quickly, no wasted motion. The kitchen stops looking like a problem."
    menu:
        "Help where she lets you.":
            n "Hold this. Don't stir — just hold."
            "You hold. You don't stir."
            $ _apply_aff("nora", 4)
            $ _apply_trust("nora", 2)
        "Stay out of the way and watch.":
            "You stay out of the way. It's genuinely faster."
            n "See? The kitchen's not the problem."
            $ _apply_aff("nora", 3)
            $ _apply_trust("nora", 3)
    "The result is better than anything you've managed in here on your own."
    n "It's a bad kitchen. But it's workable if you stop fighting it."
    $ _apply_aff("nora", 2)
    $ nora_cooking_state = "done"
    hide nora_casual_normal
    return
