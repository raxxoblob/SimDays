# Entry point

label start:
    # Move-in day intro (M0). No HUD during the cinematic — it's a cutscene.
    scene intro1 with fade
    "Day 1. One bag, one plan: make something of yourself."
    "You slide the key into the lock of apartment 12. It sticks."
    mc "Come on... there we go."

    scene intro2 with dissolve
    "A door opens down the hall. Footsteps — then a guy about your age, easy grin, a dish towel over one shoulder."

    scene intro3 with dissolve
    m "Hey — new blood! Heard the key fight through the wall. That lock's a jerk, you gotta lift the handle while you turn it."

    menu:
        "\"Thanks. I'm still figuring the place out.\"":
            $ marcus_affection += 3
            m "No shame in it. First week's always a mess."
        "\"I had it handled.\"":
            $ marcus_affection += 1
            m "Sure you did, champ."
            "He laughs, not unkindly."
        "(Say nothing, just nod.)":
            m "Strong silent type. Okay. I can work with that."

    scene intro4 with dissolve
    m "Marcus. Marc. I'm right next door — 14. Lived here two years, so if the hot water does the cold-then-boiling thing, that's normal. Ride it out."
    "You introduce yourself."
    m "Good to meet you, man. Moving's the worst. You eat yet? I've got half a pot of chili doing nothing."

    menu:
        "\"Yeah, actually — that'd be great.\"":
            $ marcus_affection += 5
            $ marcus_trust += 2
            $ marcus_chili = True
            scene intro5 with dissolve
            m "Ha — a man who says yes to free chili. We're gonna get along."
        "\"I'm good, gotta unpack. Rain check?\"":
            $ marcus_affection += 2
            m "No worries. Door's 14 when you're hungry — or bored."
        "\"I don't really know you, man.\"":
            m "Fair. Respect the caution. Offer stands anyway."

    scene intro6 with dissolve
    m "Tell you what — you need anything, a name, a couch, twenty bucks till payday, you knock. That's the deal here."
    m "Oh — one thing. You'll want money before rent hits. There's a café downtown, \"Grounds,\" always short-staffed. Tell 'em you can carry a tray, they'll take you."
    mc "Noted. Thanks, Marc."

    scene intro7 with dissolve
    m "Anytime, neighbor."
    "He heads for the stairs with a lazy wave, towel bouncing on his shoulder."

    $ marcus_met = True

    # Into the world.
    scene cheaphouse_day with fade
    show screen hud
    "You drop your bag inside apartment 12. Home. For now."
    jump map


# The stairwell — pick a door (clickable), or take the metro back to the city.
label location_hallway:
    scene hallway
    call screen hallway_hub


# Repeatable chat with Marcus (knock on 14, or find him at the bar later).
label marcus_talk:
    scene expression ("marcus_home_night" if (hour >= 20 or hour < 6) else "marcus_home_day")
    show screen hud
    show marcus_casual_normal as marcus at sprite_r
    # Greeting scales with how well he knows you.
    if marcus_affection >= 50:
        m "Was just about to text you. What's up, man?"
    elif marcus_affection >= 25:
        m "There he is. Grab a spot."
    else:
        m "Hey, neighbor. Surviving?"

    label marcus_talk_menu:
        menu (screen="activity"):
            "Talk to Marcus."

            "\"How's the bar?\"":
                show marcus_casual_talk as marcus at sprite_r
                m "Static? Busy. Loud. Tips are decent if you can fake liking the music."
                if marcus_affection >= 40:
                    m "I keep thinking... I could run a place better than this. Smaller. Mine."
                $ marcus_affection += 1
                jump marcus_talk_menu

            "\"Just hanging out.\"":
                show marcus_casual_laugh as marcus at sprite_r
                m "We should ball sometime. Park, Saturday. You'll lose, but you'll have fun."
                $ marcus_affection += 2
                jump marcus_talk_menu

            "\"You good?\"" if marcus_trust >= 30:
                show marcus_casual_talk as marcus at sprite_r
                m "Honestly? Money's tight, the owner's a pain. But I'm figuring it out. Thanks for asking."
                $ marcus_trust += 2
                jump marcus_talk_menu

            "Head out":
                hide marcus
                jump location_hallway
