# All location labels

# ── HOME ──────────────────────────────────────────────────────────────
label location_home:
    scene expression home_bg()
    show screen hud
    jump location_home_actions

label location_home_actions:
    scene expression home_bg()
    show screen hud

    menu:
        "What do you want to do at home?"

        "Sleep — end the day (8h)":
            jump action_sleep

        "Cook and eat (1h)" if need_hunger < 90:
            $ spend_time(1)
            $ need_hunger = min(100, need_hunger + 50)
            "You cook a simple meal. Hunger restored."
            jump location_home_actions

        "Shower (0.5h)" if need_hygiene < 90:
            $ spend_time(0.5)
            $ need_hygiene = min(100, need_hygiene + 40)
            "You take a quick shower. Feeling fresh."
            jump location_home_actions

        "Browse phone (0.5h)":
            $ spend_time(0.5)
            "You scroll through your phone. Nothing interesting."
            jump location_home_actions

        "Leave to City Map":
            jump map

# ── CAFE ──────────────────────────────────────────────────────────────
label location_cafe:
    scene expression cafe_bg()
    show screen hud
    if not zoe_met:
        jump cafe_first_visit
    else:
        jump cafe_actions

label cafe_first_visit:
    scene expression cafe_bg()
    show screen hud
    show zoe_punk_smile at sprite_c
    "A girl behind the counter catches your eye — red hair, green eyes, a gold star clip."
    z "Hey! First time here? I'm Zoe."
    menu:
        "\"Nice place. Yeah, first time.\"":
            $ zoe_affection += 5
            z "Right? I love working here. Well, most of the time."
            "She smiles and goes back to the espresso machine."
        "\"Just passing through.\"":
            z "Cool. Let me know if you need anything."
    $ zoe_met = True
    hide zoe_punk_smile
    jump cafe_actions

label cafe_actions:
    scene expression cafe_bg()
    show screen hud

    menu:
        "What do you want to do at the cafe?"

        "Buy a coffee ($3, 0.5h)":
            $ spend_time(0.5)
            $ money -= 3
            $ need_hunger = min(100, need_hunger + 10)
            "You sip a good coffee. Worth it."
            jump cafe_actions

        "Talk to Zoe (1h)" if zoe_met:
            jump cafe_talk_zoe

        "Work a shift — Barista (4h, +$60)":
            jump cafe_work_shift

        "Leave to City Map":
            jump map

label cafe_talk_zoe:
    $ spend_time(1)
    $ zoe_affection += 3
    scene expression cafe_bg()
    show screen hud
    show zoe_punk_smile at sprite_c
    if zoe_affection < 20:
        z "So what do you do when you're not hanging around cafes?"
        menu:
            "\"Still figuring that out.\"":
                z "Ha. Honest. I respect that."
                $ zoe_trust += 2
            "\"Looking for work, actually.\"":
                z "This place is hiring if you're interested. Henry's not scary, I promise."
                $ zoe_affection += 2
    elif zoe_affection < 40:
        z "You're becoming a regular, you know."
        menu:
            "\"Worst things to be.\"":
                z "True. At least you tip well."
                $ zoe_affection += 3
            "\"The coffee's that good.\"":
                z "I'll tell Henry you said that. He'll frame it."
    else:
        z "Hey, I finished a new sketch last night. Wanna see?"
        menu:
            "\"Absolutely.\"":
                z "It's nothing serious — just city rooftops. But I kinda love it."
                $ zoe_affection += 5
                $ zoe_trust += 3
            "\"Maybe another time.\"":
                z "Sure. No pressure."
    hide zoe_punk_smile
    jump cafe_actions

label cafe_work_shift:
    if hour + 4 > DAY_END:
        "It's too late to start a full shift."
        jump cafe_actions
    $ spend_time(4)
    $ money += 60
    $ stat_chr = min(100, stat_chr + 1)
    "Four hours of steaming milk and small talk. You pocket $60."
    if zoe_met:
        show zoe_punk_smile at sprite_r
        z "Not bad for your first shift. Henry said you're a natural."
        hide zoe_punk_smile
    jump cafe_actions

# ── GYM ───────────────────────────────────────────────────────────────
label location_gym:
    scene gymdaypeople
    show screen hud
    menu:
        "What do you want to do at the gym?"
        "Train — weights (1.5h, +2 STR, +1 APP)":
            $ spend_time(1.5)
            $ stat_str = min(100, stat_str + 2)
            $ stat_app = min(100, stat_app + 1)
            "A solid session. You can feel it already."
            jump location_gym
        "Cardio run (1h, +1 STR)":
            $ spend_time(1)
            $ stat_str = min(100, stat_str + 1)
            "You run until your lungs complain."
            jump location_gym
        "Leave to City Map":
            jump map

# ── LIBRARY ───────────────────────────────────────────────────────────
label location_library:
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    menu:
        "What do you want to do at the library?"
        "Study (2h, +2 INT)":
            $ spend_time(2)
            $ stat_int = min(100, stat_int + 2)
            "Two hours of focused reading. Your brain hurts in a good way."
            jump location_library
        "Leave to City Map":
            jump map

# ── BAR ───────────────────────────────────────────────────────────────
label location_bar:
    scene bar
    show screen hud
    menu:
        "What do you want to do at the bar?"
        "Have a drink ($8, 0.5h)":
            $ spend_time(0.5)
            $ money -= 8
            "The noise and the drinks do their job."
            jump location_bar
        "Socialize (1h, +2 CHR)" if stat_chr >= 25:
            $ spend_time(1)
            $ stat_chr = min(100, stat_chr + 2)
            "You work the room. A few numbers exchanged."
            jump location_bar
        "Socialize (need CHR 25)" if stat_chr < 25:
            "You hover near a few groups but can't quite break in. Need more Charisma."
            jump location_bar
        "Leave to City Map":
            jump map

# ── OFFICE ────────────────────────────────────────────────────────────
label location_office:
    scene goodoffice1
    show screen hud
    if stat_int < 20:
        "The receptionist politely tells you this position requires more experience. (Need INT 20)"
        jump map
    menu:
        "Nexus Tower — corporate floor."
        "Work a shift (8h, +$120, +1 INT)":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_office
            $ spend_time(8)
            $ money += 120
            $ stat_int = min(100, stat_int + 1)
            "A long day of meetings and spreadsheets. The pay is solid."
            jump location_office
        "Leave to City Map":
            jump map

# ── MALL ──────────────────────────────────────────────────────────────
label location_mall:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    menu:
        "The mall. Pick a shop."
        "Clothes shop — outfit ($80, +2 APP)":
            if money < 80:
                "Not enough money."
            else:
                $ money -= 80
                $ stat_app = min(100, stat_app + 2)
                "New fit. You look sharper."
            jump location_mall
        "Leave to City Map":
            jump map

# ── PARK ──────────────────────────────────────────────────────────────
label location_park:
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    menu:
        "The park."
        "Morning jog (1h, +1 STR)":
            $ spend_time(1)
            $ stat_str = min(100, stat_str + 1)
            "The air is crisp. Good start to the day."
            jump location_park
        "Read a book (1.5h, +1 INT)":
            $ spend_time(1.5)
            $ stat_int = min(100, stat_int + 1)
            "A quiet hour on the bench."
            jump location_park
        "Leave to City Map":
            jump map

# ── BEACH ─────────────────────────────────────────────────────────────
label location_beach:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    menu:
        "The beach."
        "Relax (1h)":
            $ spend_time(1)
            $ need_energy = min(100, need_energy + 10)
            "The waves and sun do wonders."
            jump location_beach
        "Leave to City Map":
            jump map

# ── CENTRUM (downtown hub) ────────────────────────────────────────────
# Clicking the downtown district drops you "on the street" — pick a venue.
label location_centrum:
    scene expression ("centerstreet_night" if (hour >= 20 or hour < 6) else "centerstreet_day")
    # bottom bar of venue icons (screen handles navigation)
    call screen centrum_hub

# ── WAREHOUSE ─────────────────────────────────────────────────────────
label location_warehouse:
    scene warehouse
    show screen hud
    if stat_str < 25:
        "The foreman looks you over: \"Come back when you can lift, kid.\" (Need STR 25)"
        jump map
    menu:
        "LogiCity Warehouse."
        "Work a shift (8h, +$110, +2 STR)":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_warehouse
            $ spend_time(8)
            $ money += 110
            $ stat_str = min(100, stat_str + 2)
            "Eight hours of hauling and stacking. Your back aches; your wallet's heavier."
            jump location_warehouse
        "Leave to City Map":
            jump map

# ── HOSPITAL ──────────────────────────────────────────────────────────
label location_hospital:
    scene hospital1
    show screen hud
    "City Hospital. Clean, quiet, smells of antiseptic. Nothing you need here right now."
    # ponytail: stub — no health system yet; future: treat injuries, medical job, an NPC.
    jump map

# ── SLEEP ─────────────────────────────────────────────────────────────
label action_sleep:
    $ new_day()
    scene expression home_bg()
    show screen hud
    $ datestr = "Day %d — %s" % (day + 1, day_name(day))
    "You sleep through the night.\n[datestr]"
    jump map

# ── MAP ────────────────────────────────────────────────────────────────
label map:
    scene map_city
    show screen hud
    call screen city_map
