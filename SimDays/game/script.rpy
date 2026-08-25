# Fallback no-op definitions (overridden by real implementations in other .rpy files)
python:
    # Adult content toggle — set to False for a clean build while testing.
    adult_mode = True

    def is_adult(*a, **kw):
        return adult_mode

    def stocks_init(*a, **kw): pass
    def refresh_market_listings(*a, **kw): pass
    def refresh_mech_jobs(*a, **kw): pass
    def sms_daily_check(*a, **kw): pass
    def wed_poll_personal(*a, **kw): return None
    def _fs_set_track_baseline(*a, **kw): pass
    def marcus_is_home(*a, **kw): return False
    def npc_interact(*a, **kw): pass

# Entry point

label start:
    $ stocks_init()
    $ refresh_market_listings()   # Phase 61: seed day-1 second-hand board
    $ refresh_mech_jobs()         # Phase 61: seed day-1 repair board
    python:
        try:
            sms_daily_check()
        except Exception:
            pass
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

    # Zoe onboarding (zoe_onboarding.rpy): she's a name before she's a person.
    m "And don't just sit in there unpacking for a week. Beach out past the plaza's decent this time of day."
    m "Zoe's usually down there sketching something and hating it."
    m "If you see a girl staring at people like she's deciding whether they were badly designed — that's Zoe."
    menu:
        "\"Friend of yours?\"":
            m "Yeah. She'll deny I said that with too much confidence."
        "\"I'll keep that in mind.\"":
            m "Do. She's worth the walk."
    $ marcus_mentioned_zoe = True

    scene intro7 with dissolve
    m "Anytime, neighbor."
    "He heads for the stairs with a lazy wave, towel bouncing on his shoulder."

    $ marcus_met = True
    $ onboarding_state = "complete"
    $ move_in_complete = False
    $ first_steps_track = None

    scene hallway with fade
    show screen hud
    jump location_hallway


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


# The stairwell - pick a door or head to the city map.
label location_hallway:
    scene hallway
    show screen hud
    python:
        try:
            sms_daily_check()
        except Exception:
            pass
    if not marcus_met:
        jump marcus_intro_hallway
    $ _wed_per = wed_poll_personal("location_hallway")
    if _wed_per:
        call expression _wed_per
    call screen hallway_hub


label marcus_intro_hallway:
    show screen hud
    "As you climb the stairwell, a door on the landing swings open."

    m "Hey. New tenant? I'm Marcus — fourteen."
    mc "Hey. [mc_name]. Just moved into twelve."
    m "Figured. Heard someone moving boxes at six in the morning."
    mc "Sorry about that."
    m "Don't be. It's a good floor. Where'd you move from?"

    menu:
        "I was in the gym most days back home. Needed a change of scenery.":
            $ store.stat_str = min(100, store.stat_str + 15)
            m "Ha. Iron Gate's two blocks west. You'll fit right in."
        "I was finishing a degree. More theory than I wanted.":
            $ store.stat_int = min(100, store.stat_int + 15)
            m "City College is decent. Or just jump straight in — depends what you studied."
        "Sales job. Lots of talking, not enough living.":
            $ store.stat_chr = min(100, store.stat_chr + 15)
            m "Sales. So you can read a room. That goes a long way here."
        "Honestly? Not much. Fresh start.":
            $ store.stat_str = min(100, store.stat_str + 5)
            $ store.stat_int = min(100, store.stat_int + 5)
            $ store.stat_chr = min(100, store.stat_chr + 5)
            $ store.stat_app = min(100, store.stat_app + 5)
            m "Fair enough. Clean slate."

    m "And what's the actual plan? Something lined up, or still figuring it out?"

    menu:
        "Get in shape first. Clear my head. Build something concrete.":
            $ store.stat_str = min(100, store.stat_str + 15)
            m "Gym and early nights, then. Solid."
        "Career first. Stable income, see what opens up.":
            $ store.stat_int = min(100, store.stat_int + 15)
            m "Nexus Tower's hiring. So is The Hub if you're technical. Both walkable."
        "Meet people. New city, new chapter.":
            $ store.stat_chr = min(100, store.stat_chr + 15)
            m "Grounds café on the corner's good for that. Bar on weekends."
        "I don't know yet. That's kind of the point.":
            $ store.stat_app = min(100, store.stat_app + 15)
            m "Underrated answer. Pressure kills good decisions."

    m "Well. Twelve's got better morning light, by the way. Lucky you."
    m "I'm around most evenings if you need anything. Knock on fourteen."

    m "Get the boxes inside first."
    mc "That obvious?"
    m "You're carrying one upside down."
    "A beat."
    m "When you're done, knock on fourteen."
    mc "Your place?"
    m "Yeah."
    m "You can walk into the city blind if you want."
    m "But you'll waste three days learning what I can tell you in ten minutes."
    mc "Is this the part where you sell me something?"
    m "Coffee."
    m "Bad coffee. Advice is free."

    $ store.marcus_met = True
    $ store.marcus_affection += 5
    jump location_hallway


# Marcus's place (14). Routes to full home location when access is granted.
label marcus_talk:
    scene expression ("marcus_home_night" if (hour >= 20 or hour < 6) else "marcus_home_day")
    show screen hud
    if not move_in_complete:
        show marcus_casual_normal as focus_marcus at sprite_c
        m "Good — before you head back. Two minutes. Won't cost you anything."
        m "Activities use time. Walking between places doesn't. That's the first thing people miss."
        m "Watch the three bars up top. Hunger, energy, hygiene. Let any of them crash and your day falls apart fast."
        m "If you need income first, Grounds is the easy door — café downtown. Low barrier, enough to cover the basics."
        m "The real careers ask more. Medicine, programming, business, cooking, fitness. Some need a degree further down the line."
        m "People here have their own schedules. If someone isn't where you expected, they're somewhere else."
        m "Phone keeps your messages, contacts and commitments. You don't have to come back here to use it."
        m "So. What do you need first?"
        menu:
            "Money.":
                $ first_steps_track = "money"
                mc "Money."
                m "Grounds. Corner of the Centrum. Tell them you can carry a tray."
            "A real career.":
                $ first_steps_track = "career"
                mc "A proper career."
                m "Then check what it needs before you apply. Build the skill first."
            "People.":
                $ first_steps_track = "people"
                mc "People."
                m "Go somewhere because someone might actually be there."
            "I want to look around.":
                $ first_steps_track = "explore"
                mc "I want to see the city."
                m "Map's in the phone. Rest is up to you."
        $ _fs_set_track_baseline()
        $ move_in_complete = True
        hide focus_marcus
    if marcus_home_state != "locked" and marcus_is_home():
        jump location_marcus_home
    call npc_interact("marcus")
    jump location_hallway
