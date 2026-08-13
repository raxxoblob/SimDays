# Topic arc scenes — specific story beats per NPC per topic.
# Each label: dialogue → optional choice → complete_arc + mark_topic_today → return.
# Called from npc_interact when check_arc() finds an available stage.

# ══ ZOE ═══════════════════════════════════════════════════════════════════

label arc_zoe_art_1:
    z "What do I draw? Mostly this."
    "She flips to a page in her sketchbook — waterfront buildings caught in the reflection of broken waves. Lines precise, light somehow alive."
    z "I've been trying to get it right for months. Every time I think I'm close the water changes."
    menu:
        "Can I look?":
            z "Sure."
            "She holds it out. The lines are very good. The light is better than good."
            $ _apply_aff("zoe", 2)
        "It's good.":
            z "It's not, yet. But thanks."
            $ _apply_aff("zoe", 1)
    $ complete_arc("zoe_art_1")
    $ mark_topic_today("zoe", "art")
    return

label arc_zoe_art_2:
    z "There's an exhibition next month. Small gallery, nothing major."
    z "I submitted three pieces. We'll see what they do with them."
    menu:
        "I'd like to see it.":
            z "Yeah?"
            "She looks briefly caught off guard — the expression of someone who had already braced for the more likely response."
            z "I'll let you know when the opening is."
            $ _apply_aff("zoe", 2)
        "What's the theme?":
            z "The city. How it changes while you're looking at something else."
            $ _apply_aff("zoe", 1)
    $ complete_arc("zoe_art_2")
    $ mark_topic_today("zoe", "art")
    return

label arc_zoe_art_3:
    z "The gallery rejected the funding application."
    "She says it the way you'd read out a weather report. Factual. Completely flat."
    z "Three years of work. Five hundred words of justification. Apparently not quite what they were looking for."
    menu:
        "That's genuinely awful. I'm sorry.":
            z "Yeah."
            "A long pause. She looks somewhere past your shoulder."
            z "Thanks for not telling me I'll bounce back."
            $ _apply_trust("zoe", 3)
        "What did they say, exactly?":
            z "That the work is 'technically accomplished but lacks clear commercial direction.'"
            "She says it in perfect quotation marks. Something tightens in her jaw."
            $ _apply_trust("zoe", 1)
            $ _apply_aff("zoe", -1)
        "Maybe the commercial angle isn't the point.":
            z "That's a nice thought."
            "Pause."
            z "Doesn't pay for materials, though."
            $ _apply_trust("zoe", 2)
    $ store.zoe_grant_discussed = True
    $ complete_arc("zoe_art_3")
    $ mark_topic_today("zoe", "art")
    return

label arc_zoe_art_4:
    z "The opening is Friday. I've been standing in the space trying to decide if the work is done, or if I just ran out of time to change it."
    menu:
        "I'll be there.":
            z "Yeah?"
            "A real smile this time — not the careful one she usually has available."
            z "Okay. Good."
            $ _apply_aff("zoe", 3)
            $ store.zoe_exhibition_invited = True
        "You'll know when you see it in the room.":
            z "Maybe."
            "She's quiet for a moment."
            z "Maybe."
            $ _apply_trust("zoe", 2)
            $ store.zoe_exhibition_invited = True
    $ complete_arc("zoe_art_4")
    $ mark_topic_today("zoe", "art")
    return

label arc_zoe_music_1:
    z "Depends on the time of day. Morning is usually something without words. Evening is everything."
    z "Right now there's this band out of Warsaw — they play like they're running out of time."
    $ _apply_aff("zoe", 1)
    $ complete_arc("zoe_music_1")
    $ mark_topic_today("zoe", "music")
    return

label arc_zoe_music_2:
    z "I used to play bass, actually. Did for years."
    z "Just... stopped one day. I think I was trying to be too many things at once."
    menu:
        "Do you miss it?":
            z "Sometimes I see a bass in a shop window and think about it for about thirty seconds."
            z "Then I keep walking."
            $ _apply_trust("zoe", 2)
        "You should pick it up again.":
            z "Yeah, maybe."
            "She's already looking somewhere else."
            $ _apply_aff("zoe", 1)
    $ complete_arc("zoe_music_2")
    $ mark_topic_today("zoe", "music")
    return


# ══ NORA ══════════════════════════════════════════════════════════════════

label arc_nora_food_1:
    n "I make this pasta. My grandmother's recipe. I've been making it since I was about eight."
    n "It's nothing special if you write it down. But there's something about making it."
    $ _apply_aff("nora", 1)
    $ complete_arc("nora_food_1")
    $ mark_topic_today("nora", "food")
    return

label arc_nora_food_2:
    n "I took a pastry course last year. Night classes, three months."
    n "Turns out I'm better at desserts than main courses. No idea what to do with that information."
    menu:
        "Open a patisserie.":
            n "Oh sure. No capital, tiny kitchen, perfect plan."
            "She's smiling though. It's a real smile."
            $ _apply_trust("nora", 2)
        "Maybe it means something.":
            n "Maybe. Or maybe I just really like eating the results."
            $ _apply_aff("nora", 1)
    $ complete_arc("nora_food_2")
    $ mark_topic_today("nora", "food")
    return

label arc_nora_ambition_1:
    n "I've been putting money aside. Not much. But steadily."
    "She doesn't elaborate. The coffee machine does something loud and she lets it."
    menu:
        "For what?":
            n "Does it count as a dream if it's not allowed to be a plan yet?"
            $ _apply_trust("nora", 1)
        "That's smart.":
            n "Or just scared of nothing changing."
            $ _apply_aff("nora", 1)
    $ complete_arc("nora_ambition_1")
    $ mark_topic_today("nora", "ambition")
    return

label arc_nora_ambition_2:
    n "I got in. Culinary programme, other side of the city."
    n "September intake. I have until Friday to say yes."
    "She's looking at the counter. Not at you."
    menu:
        "What's stopping you?":
            n "Fear, I think. Which is not actually a reason. But here we are."
            $ _apply_trust("nora", 3)
            $ store.nora_school_revealed = True
        "You should go.":
            n "Yeah."
            "A pause."
            n "Yeah."
            $ _apply_trust("nora", 2)
            $ _apply_aff("nora", 1)
            $ store.nora_school_revealed = True
        "What would you lose if you don't go?":
            n "That's a worse question than you think."
            "She finally looks up."
            $ _apply_trust("nora", 3)
            $ store.nora_school_revealed = True
    $ complete_arc("nora_ambition_2")
    $ mark_topic_today("nora", "ambition")
    return


# ══ MARCUS ════════════════════════════════════════════════════════════════

label arc_marcus_sports_1:
    m "Six AM every day. Even weekends."
    m "People think it's discipline. Really it's just that I can't sleep past five anyway."
    $ _apply_aff("marcus", 1)
    $ complete_arc("marcus_sports_1")
    $ mark_topic_today("marcus", "sports")
    return

label arc_marcus_sports_2:
    m "I got an offer at eighteen. Semi-pro basketball, small league, city about three hours from here."
    m "Didn't take it."
    "He doesn't say why. You wait."
    menu:
        "Why not?":
            m "My dad was sick. Couldn't leave."
            "Flat. End of subject."
            $ _apply_trust("marcus", 3)
        "Any regrets?":
            m "I try not to deal in those."
            "Then, after a moment:"
            m "Sometimes."
            $ _apply_trust("marcus", 2)
    $ complete_arc("marcus_sports_2")
    $ mark_topic_today("marcus", "sports")
    return

label arc_marcus_food_1:
    m "I can cook exactly one thing properly. Chili."
    m "Everything else I've ever made has been edible, but wrong."
    menu:
        "What goes in it?":
            m "Classified."
            "He's smiling."
            $ _apply_aff("marcus", 1)
        "One thing's enough.":
            m "That's what I keep telling myself."
            $ _apply_aff("marcus", 1)
    $ complete_arc("marcus_food_1")
    $ mark_topic_today("marcus", "food")
    return

label arc_marcus_food_2:
    m "It's my mom's recipe. She wrote it down on a notepad — the actual notepad, which I still have."
    m "I've made it maybe two hundred times. I still check the notepad every time."
    "There's a pause. He doesn't explain further and you don't ask."
    $ _apply_trust("marcus", 3)
    $ complete_arc("marcus_food_2")
    $ mark_topic_today("marcus", "food")
    return


# ══ ELI ═══════════════════════════════════════════════════════════════════

label arc_eli_work_1:
    eli "I'm finishing a part-time MSc. Environmental systems — urban data, policy modelling, that kind of thing."
    eli "It's one of those topics where the more you read, the worse things look."
    $ _apply_aff("eli", 1)
    $ complete_arc("eli_work_1")
    $ mark_topic_today("eli", "work")
    return

label arc_eli_work_2:
    eli "Sometimes I think — what if the thesis is good and it still doesn't matter?"
    eli "Like the work is fine but the problem is just too big for anyone to fix from a library."
    menu:
        "It still matters that you tried.":
            eli "I hope so."
            "She sounds like she almost believes it."
            $ _apply_trust("eli", 2)
        "So what's the alternative — give up?":
            eli "No. But sometimes I'd like to be angry about it without also having to be hopeful."
            "She's quiet for a second, then nods once."
            $ _apply_trust("eli", 3)
    $ complete_arc("eli_work_2")
    $ mark_topic_today("eli", "work")
    return


# ══ ELLE ══════════════════════════════════════════════════════════════════

label arc_elle_travel_1:
    el "If I could leave tomorrow? Georgia. The country, not the state."
    el "I've had this image in my head for years — mountains, those old stone towers, fog coming off the valleys."
    el "I don't know anyone who's been. I just know I want to go."
    $ _apply_aff("elle", 1)
    $ complete_arc("elle_travel_1")
    $ mark_topic_today("elle", "travel")
    return

label arc_elle_travel_2:
    el "I got offered a position. Marine research project, eighteen months, based in Portugal."
    el "It's everything I wanted three years ago."
    menu:
        "What's changed?":
            el "I don't know. Maybe nothing. Maybe me."
            $ _apply_trust("elle", 2)
            $ store.elle_abroad_revealed = True
            $ store.elle_abroad_day = day
            $ store.elle_travel_2_response = "what_changed"
        "Take it.":
            el "Yeah?"
            "She looks at you for a full second."
            el "Just like that?"
            $ _apply_aff("elle", 2)
            $ store.elle_abroad_revealed = True
            $ store.elle_abroad_day = day
            $ store.elle_travel_2_response = "take_it"
        "What would you miss?":
            el "That's the part I keep circling."
            $ _apply_trust("elle", 3)
            $ store.elle_abroad_revealed = True
            $ store.elle_abroad_day = day
            $ store.elle_travel_2_response = "what_miss"
    $ complete_arc("elle_travel_2")
    $ mark_topic_today("elle", "travel")
    return


# ── Phase 50: Zoe exhibition opening ─────────────────────────────────────────

label zoe_exhibition_opening:
    $ wed_fire("zoe_exhibition_opening")
    $ _gal_bg = "gallery_evening" if renpy.has_image("gallery_evening") else "librarynight"
    scene expression _gal_bg with dissolve
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_l
    "The opening has been running for an hour."
    "The gallery is small — three rooms, white walls, track lighting."
    "People cluster near the entrance with drinks they're holding but not drinking."
    "Zoe is standing near the far wall, not exactly with the other artists."
    "She has a glass of something she hasn't touched."
    "She's watching the entrance."
    "She sees you."
    z "You came."
    mc "You said I could."
    z "I said you were allowed to. That's different."
    "She moves away from the wall. Doesn't lead you anywhere in particular."
    "Four pieces. Three are confident — colour, scale, the kind of statement that fills a room."
    "The fourth is smaller. It's in the corner. The framing is different. The light falls on it wrong, as if it wasn't planned."
    "Zoe hasn't looked at it since you arrived."
    if store.elle_met and not npc_is_temporarily_unavailable("elle"):
        "Near the second room, a woman who might be Elle is taking notes in a small pad."
    if store.nora_met and npc_location_now("nora") != "location_cafe":
        "Later — near closing — Nora appears briefly at the entrance. She stands in front of one piece for a moment, then leaves without staying."
    $ _wev_relbar_open("zoe")
    show screen npc_relbar("zoe")
    menu:
        "Ask about the piece in the corner.":
            z "That one isn't in the programme notes."
            mc "I know. That's why I'm asking."
            "She looks at it. The first time since you arrived."
            z "It's older. I almost didn't include it."
            mc "Why did you?"
            "A long pause."
            z "Because I made it when I thought no one was going to see it."
            z "And that's when I actually made something."
            $ _apply_aff("zoe", 2)
            $ _apply_trust("zoe", 3)
            $ store.zoe_exhibition_outcome = "seen"
        "Help with something practical.":
            "A label on the third piece has slipped — slightly crooked, visibly wrong."
            "You straighten it."
            z "That was bothering me since setup."
            "She doesn't say thank you out loud. She looks at you the way someone does when they mean it."
            "A visitor asks you a question about the work, clearly confusing you for staff."
            "You answer it. Badly, but confidently enough that they seem satisfied."
            z "You just made something up."
            mc "It was plausible."
            z "It was."
            $ _apply_aff("zoe", 2)
            $ _apply_trust("zoe", 2)
            $ store.zoe_exhibition_outcome = "steady"
        "Ask whether this will lead anywhere useful.":
            mc "Is this the kind of thing that gets you commissions? Work?"
            "A short silence."
            z "I don't know. Maybe."
            "She picks up her glass. Doesn't drink from it."
            z "That wasn't really what tonight was."
            "She doesn't explain further."
            $ _apply_aff("zoe", -1)
            $ _apply_trust("zoe", -2)
            $ store.zoe_exhibition_outcome = "pressured"
    $ _wev_relbar_close()
    hide screen npc_relbar
    scene expression _gal_bg
    show screen hud
    show zoe_street_neutral as focus_zoe at sprite_l
    "The opening runs another hour."
    "She doesn't say much more. Neither do you."
    "That's fine."
    hide focus_zoe
    $ spend_time(2.0)
    $ fs_record_social("zoe", "story_event")
    $ record_social_attention("zoe", "story_event")
    $ add_relationship_memory("zoe", "zoe_exhibition_opening", "The gallery opening")
    $ zoe_exhibition_done = True
    $ zoe_exhibition_day = day
    $ zoe_gallery_until_day = day + 14
    python:
        if (store.npc_invitation_pending
                and store.npc_invitation_pending.get("invitation_id") == "zoe_exhibition"):
            store.npc_invitation_pending = None
    return


# ── Phase 50: Zoe exhibition aftermath (Phase 46 system) ─────────────────────

label story_aftermath_zoe_exhibition:
    $ _do_talk_accounting("zoe")
    if zoe_exhibition_outcome == "seen":
        z "You asked about the one nobody else asked about."
        mc "It was the most interesting piece."
        "A beat."
        z "It wasn't meant to be."
        "She says it as a fact, not a complaint."
        z "I kept it small because I didn't think anyone would know what they were looking at."
        mc "I didn't, exactly. I just noticed you weren't looking at it."
        "Another beat."
        z "That's the same thing."
        "She doesn't say more than that."
    elif zoe_exhibition_outcome == "steady":
        z "The label thing."
        mc "I fixed it."
        z "I know."
        "She's quiet for a moment."
        z "The opening would have been a lot worse."
        mc "It went fine."
        z "It went fine because of that. And the visitor."
        "She means the one you lied to."
        z "I'm saying it practically."
        "She does mean it practically. It still lands."
    else:
        z "The work was finished before anyone decided whether it was useful."
        "She's not angry. She's settled."
        mc "I know. I shouldn't have framed it that way."
        z "No."
        "A pause."
        z "It's a fair question for most things. It wasn't the right moment."
        "She gives you space to sit with that."
        mc "I was wrong to ask it then."
        z "Yeah."
        "She nods. That's enough for her."
    $ _resolve_story_aftermath("zoe", "zoe_exhibition")
    return


# ── Phase 50: Zoe exhibition final callback ───────────────────────────────────

label talk_followup_zoe_exhibition:
    $ zoe_exhibition_followup_done = True
    $ _do_talk_accounting("zoe")
    if zoe_exhibition_outcome == "seen":
        z "I took the small one down this morning."
        mc "The corner piece?"
        z "I kept it at home."
        "She doesn't explain why."
        "She doesn't need to."
    elif zoe_exhibition_outcome == "steady":
        z "The gallery's wrapped. I left one piece — the lighting was still good on it."
        mc "Which one?"
        z "Near the window. I'll collect it."
        "She probably won't for a while."
    else:
        z "Everything's down. One piece wasn't collected."
        "A beat."
        z "It's in storage. I'll work it out."
        "She says it without tension. The opening is behind her."
    return


# ── Phase 50: gallery-specific Zoe Talk ──────────────────────────────────────

label zoe_gallery_talk:
    $ _do_talk_accounting("zoe")
    if zoe_exhibition_outcome == "seen":
        z "I'm still deciding how much of it I want to explain to people."
        mc "You don't have to explain it."
        z "I know."
        "She looks at the corner piece."
        z "That's the problem."
    elif zoe_exhibition_outcome == "steady":
        z "Someone moved the third piece two centimetres to the left. I can tell."
        mc "Does it matter?"
        z "No. But I notice."
        "She's scanning the room with the focus of someone doing a silent inventory."
    else:
        z "People keep asking me what it sold for."
        "A beat."
        z "That's not what it was."
        mc "I know."
        "She looks at you briefly. Something settles."
    return
