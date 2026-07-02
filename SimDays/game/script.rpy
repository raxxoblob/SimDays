# Entry point

label start:
    # Move-in day intro (M0). No HUD during the cinematic - it's a cutscene.
    scene hallway with fade
    "Day 1."
    "The stairwell smells of old wood, fresh paint, and someone's cooking two floors down."
    "One bag on your shoulder. A key in your pocket. Apartment 12 - small, cheap, and, as of this morning, yours."
    "One plan: make something of yourself in this city."
    "Well. First things first."

    scene intro1 with dissolve
    "You slide the key into the lock of number 12. It sticks."
    mc "Come on... there we go."

    scene intro2 with dissolve
    "A door opens down the hall. Footsteps - then a guy about your age, easy grin, a dish towel over one shoulder."

    scene intro3 with dissolve
    m "Hey - new blood! Heard the key fight through the wall. That lock's a jerk, you gotta lift the handle while you turn it."

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
    m "Marcus. Marc. I'm right next door - 14. Lived here two years, so if the hot water does the cold-then-boiling thing, that's normal. Ride it out."
    m "Anyway - who am I gonna be yelling at through the wall? What's your name?"

    # Name entry - sets the MC's name (blank falls back to the default).
    $ mc_name = renpy.input("What's your name?", default=mc_name, length=20).strip()
    $ mc_name = mc_name or "Alex"

    m "[mc_name]. Good to meet you, man."
    m "Moving's the worst. You eat yet? I've got half a pot of chili doing nothing."

    menu:
        "\"Yeah, actually - that'd be great.\"":
            $ marcus_affection += 5
            $ marcus_trust += 2
            $ marcus_chili = True
            scene intro5 with dissolve
            m "Ha - a man who says yes to free chili. Say no more."
            "He ducks back into 14 and returns with a bowl, still steaming, and presses it into your hands."
            $ need_hunger = min(100, need_hunger + 40)
            m "Eat first, unpack later. Trust me, it's the only way to survive moving day."
            mc "...Okay, this is actually really good."
            m "Told you."
        "\"I'm good, gotta unpack. Rain check?\"":
            $ marcus_affection += 2
            m "No worries. Door's 14 when you're hungry - or bored."
        "\"I don't really know you, man.\"":
            m "Fair. Respect the caution. Offer stands anyway."

    scene intro6 with dissolve
    m "Tell you what - you need anything, a name, a couch, twenty bucks till payday, you knock. That's the deal here."
    m "Oh - one thing. You'll want money before rent hits. There's a café downtown, \"Grounds,\" always short-staffed. Tell 'em you can carry a tray, they'll take you."
    mc "Noted. Thanks, Marc."

    scene intro7 with dissolve
    m "Anytime, neighbor."
    "He heads for the stairs with a lazy wave, towel bouncing on his shoulder."

    $ marcus_met = True

    # Into the world - you start inside your own place (apartment 12).
    scene cheaphouse_day with fade
    show screen hud
    "You drop your bag inside apartment 12. Home. For now."
    jump location_home


# Nicer neighbourhoods you can't afford to live in yet (locked homes).
label zone_locked_uptown:
    scene map_city
    "Uptown. Gated lawns, glass and stone, cars worth more than a year of your rent."
    "Nothing for you here - yet. Come back when your name opens doors like these."
    jump map

label zone_locked_suburbs:
    scene map_city
    "The Suburbs. Quiet streets, real houses, room to breathe."
    "Someday, maybe. For now your lease says apartment 12, downtown."
    jump map


# The stairwell - pick a door (clickable), or take the metro back to the city.
label location_hallway:
    scene hallway
    call screen hallway_hub


# Marcus's place (14). Left panel = actions; talking opens centred choices.
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

# Left-side action hub at Marcus's place.
label marcus_actions:
    show marcus_casual_normal as marcus at sprite_r
    menu (screen="activity"):
        "Marcus's place (14)."

        "Talk to Marcus":
            jump marcus_chat

        "Head out":
            hide marcus
            jump location_hallway

# The conversation itself - standard centred Ren'Py choices.
label marcus_chat:
    menu:
        "\"How's the bar?\"":
            show marcus_casual_talk as marcus at sprite_r
            m "Static? Busy. Loud. Tips are decent if you can fake liking the music."
            if marcus_affection >= 40:
                m "I keep thinking... I could run a place better than this. Smaller. Mine."
            $ marcus_affection += 1
            jump marcus_chat

        "\"Just hanging out.\"":
            show marcus_casual_laugh as marcus at sprite_r
            m "We should ball sometime. Park, Saturday. You'll lose, but you'll have fun."
            $ marcus_affection += 2
            jump marcus_chat

        "\"You good?\"" if marcus_trust >= 30:
            show marcus_casual_talk as marcus at sprite_r
            m "Honestly? Money's tight, the owner's a pain. But I'm figuring it out. Thanks for asking."
            $ marcus_trust += 2
            jump marcus_chat

        "(That's enough for now.)":
            show marcus_casual_normal as marcus at sprite_r
            jump marcus_actions
