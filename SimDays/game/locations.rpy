# All location labels

# ── HOME ──────────────────────────────────────────────────────────────
label location_home:
    scene expression home_bg()
    show screen hud
    jump location_home_actions

label location_home_actions:
    scene expression home_bg()
    show screen hud

    menu (screen="activity"):
        "What do you want to do at home?"

        "Sleep - end the day (8h)":
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
    if not nora_met:
        jump cafe_first_visit
    else:
        jump cafe_actions

label cafe_first_visit:
    scene expression cafe_bg()
    show screen hud
    show nora_cafe_normal at sprite_r
    "The place smells of espresso and warm milk. Behind the counter, a woman in an apron looks up from a stack of cups, dark hair coming loose from its bun."
    n "Hey - welcome to Grounds. First time, right? You've got the lost look. Everybody does their first week in this city."
    menu:
        "\"That obvious? Yeah, just moved in.\"":
            $ nora_affection += 4
            n "Thought so. Coffee helps. So does not overthinking the menu - it's mostly just coffee with extra steps."
        "\"I'm looking for work, actually.\"":
            $ nora_affection += 3
            n "Oh? We're always a pair of hands short. Talk to Henry - he owns the place - but honestly, if you can carry a tray without wearing it, you're hired."
        "\"Just here for the coffee.\"":
            n "A man who knows what he wants. Refreshing, honestly."
    n "I'm Nora, by the way. I basically live behind this counter."
    "You introduce yourself."
    n "Good to meet you, [mc_name]. First cup's on me - new-neighbor rate. After that Henry starts counting, so enjoy it."
    $ nora_met = True
    hide nora_cafe_normal
    jump cafe_actions

label cafe_actions:
    scene expression cafe_bg()
    show screen hud

    menu (screen="activity"):
        "What do you want to do at the cafe?"

        "Buy a coffee ($3, 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-3)
            $ need_hunger = min(100, need_hunger + 10)
            "You sip a good coffee. Worth it."
            jump cafe_actions

        "Talk to Nora" if nora_met and npc_here("nora"):
            call npc_interact("nora")
            jump cafe_actions

        "Nora's off shift" if nora_met and not npc_here("nora"):
            "Nora's not behind the counter right now. She works days."
            jump cafe_actions

        "Work a shift - Barista (4h, +$60)":
            jump cafe_work_shift

        "Leave to City Map":
            jump map

label cafe_work_shift:
    if hour + 4 > DAY_END:
        "It's too late to start a full shift."
        jump cafe_actions
    $ spend_time(4)
    $ gain_money(60)
    $ gain_stat("chr", 1)
    "Four hours of steaming milk and small talk. You pocket $60."
    if nora_met:
        show nora_cafe_normal at sprite_r
        n "Not bad for your first shift. Henry says you're a natural. That's high praise - he called me 'adequate' for a year."
        hide nora_cafe_normal
    jump cafe_actions

# ── GYM ───────────────────────────────────────────────────────────────
label location_gym:
    scene gymdaypeople
    show screen hud
    menu (screen="activity"):
        "What do you want to do at the gym?"
        "Train - weights (1.5h, +2 STR, +1 APP)":
            $ spend_time(1.5)
            $ gain_stat("str", 2)
            $ gain_stat("app", 1)
            "A solid session. You can feel it already."
            jump location_gym
        "Cardio run (1h, +1 STR)":
            $ spend_time(1)
            $ gain_stat("str", 1)
            "You run until your lungs complain."
            jump location_gym
        "Leave to City Map":
            jump map

# ── LIBRARY ───────────────────────────────────────────────────────────
label location_library:
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    menu (screen="activity"):
        "What do you want to do at the library?"
        "Study (2h, +2 INT)":
            $ spend_time(2)
            $ gain_stat("int", 2)
            "Two hours of focused reading. Your brain hurts in a good way."
            jump location_library
        "Leave to City Map":
            jump map

# ── BAR ───────────────────────────────────────────────────────────────
label location_bar:
    scene bar
    show screen hud
    menu (screen="activity"):
        "What do you want to do at the bar?"
        "Have a drink ($8, 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-8)
            "The noise and the drinks do their job."
            jump location_bar
        "Socialize (1h, +2 CHR)" if stat_chr >= 25:
            $ spend_time(1)
            $ gain_stat("chr", 2)
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
    menu (screen="activity"):
        "Nexus Tower - corporate floor."
        "Work a shift (8h, +$120, +1 INT)" if stat_int >= 20:
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_office
            $ spend_time(8)
            $ gain_money(120)
            $ gain_stat("int", 1)
            if not caroline_met:
                $ caroline_met = True
                "A long first day. On the way out, HR's Caroline clocks you: \"New blood. I keep tabs on everyone - nothing personal.\" You've met."
            else:
                "A long day of meetings and spreadsheets. The pay is solid."
            jump location_office
        "Ask about work (need INT 20)" if stat_int < 20:
            "The receptionist smiles thinly: these roles need more experience. (Need INT 20.)"
            jump location_office
        "Talk to Caroline" if npc_talkable("caroline"):
            call npc_interact("caroline")
            jump location_office

        "Caroline's not in" if npc_known("caroline") and not npc_here("caroline"):
            "HR's dark. Caroline works weekday office hours - come back then."
            jump location_office
        "Leave to City Map":
            jump map

# ── MALL ──────────────────────────────────────────────────────────────
label location_mall:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    show screen hud
    menu (screen="activity"):
        "The mall. Pick a shop."
        "Clothes shop - outfit ($80, +2 APP)":
            if money < 80:
                "Not enough money."
            else:
                $ gain_money(-80)
                $ gain_stat("app", 2)
                "New fit. You look sharper."
            jump location_mall
        "Leave to City Map":
            jump map

# ── PARK ──────────────────────────────────────────────────────────────
label location_park:
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    menu (screen="activity"):
        "The park."
        "Morning jog (1h, +1 STR)":
            $ spend_time(1)
            $ gain_stat("str", 1)
            "The air is crisp. Good start to the day."
            jump location_park
        "Read a book (1.5h, +1 INT)":
            $ spend_time(1.5)
            $ gain_stat("int", 1)
            "A quiet hour on the bench."
            jump location_park
        "Leave to City Map":
            jump map

# ── BEACH ─────────────────────────────────────────────────────────────
label location_beach:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    menu (screen="activity"):
        "The beach."
        "Relax (1h)":
            $ spend_time(1)
            $ need_energy = min(100, need_energy + 10)
            "The waves and sun do wonders."
            jump location_beach
        "Talk to Elle" if npc_here("elle"):
            call npc_interact("elle")
            jump location_beach
        "Leave to City Map":
            jump map

# ── CENTRUM (downtown hub) ────────────────────────────────────────────
# Clicking the downtown district drops you "on the street" - pick a venue.
label location_centrum:
    scene expression ("centerstreet_night" if (hour >= 20 or hour < 6) else "centerstreet_day")
    # bottom bar of venue icons (screen handles navigation)
    call screen centrum_hub

# ── WAREHOUSE ─────────────────────────────────────────────────────────
label location_warehouse:
    scene warehouse
    show screen hud
    menu (screen="activity"):
        "LogiCity Warehouse."
        "Work a shift (8h, +$110, +2 STR)" if stat_str >= 25:
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_warehouse
            $ spend_time(8)
            $ gain_money(110)
            $ gain_stat("str", 2)
            if not natalie_met:
                $ natalie_met = True
                "Eight hours of hauling. At clock-out the floor manager, Natalie, sizes you up: \"Not useless. I'm Natalie. Don't make me remember your name for the wrong reasons.\""
            else:
                "Eight hours of hauling and stacking. Your back aches; your wallet's heavier."
            jump location_warehouse
        "Ask about work (need STR 25)" if stat_str < 25:
            "The foreman looks you over: \"Come back when you can lift, kid.\" (Need STR 25.)"
            jump location_warehouse
        "Talk to Natalie" if npc_talkable("natalie"):
            call npc_interact("natalie")
            jump location_warehouse

        "Natalie's off the floor" if npc_known("natalie") and not npc_here("natalie"):
            "She's not on the floor right now. Day shifts only."
            jump location_warehouse
        "Leave to City Map":
            jump map

# ── HOSPITAL ──────────────────────────────────────────────────────────
label location_hospital:
    scene expression ("hospital_night" if (hour >= 20 or hour < 6) else "hospital1")
    show screen hud
    menu (screen="activity"):
        "City Hospital - reception. Antiseptic and quiet hurry."

        "Cosmetic touch-up (+2 APP, $200, 2h)":
            if money < 200:
                "The clinic coordinator slides the price sheet back. You can't cover $200 today."
            else:
                $ spend_time(2)
                $ gain_money(-200)
                $ gain_stat("app", 2)
                "A minor cosmetic procedure. A little sharper in the mirror on the way out."
            jump location_hospital

        # Medicine career (shares the engine + CAREERS["hospital"]).
        "Work a shift (8h)" if job_id == "hospital":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_hospital
            $ _tired = do_shift("hospital", 8)
            if _tired:
                "A brutal shift on no sleep. You get through it - barely."
            else:
                "Charts, rounds, a dozen small crises handled. You earned the coffee."
            jump location_hospital

        "Ask about a promotion" if job_id == "hospital" and job_performance >= 100:
            if promote():
                "Dr. Grant signs off with a rare nod. \"Don't make me regret it.\" Promoted."
                if job_rank >= 1 and not lena_met:
                    $ lena_met = True
                    "A doctor mid-coffee catches you in the hall. \"Fresh resident? I'm Lena. You'll live. Probably.\" You've got a colleague now."
            else:
                "\"Not yet. Get the skills and the hours in first.\""
            jump location_hospital

        "Drop off your CV (apply for medicine)" if job_id is None and can_apply("hospital"):
            $ apply_job("hospital")
            "The chief reviews your file. \"Med Student it is. Try not to faint.\" You're in."
            jump location_hospital

        "Drop off your CV (apply for medicine)" if job_id is None and not can_apply("hospital"):
            "A tired doctor skims your CV and hands it back. \"You're not there yet - Medicine 1 and INT 20, minimum. The college teaches it.\""
            jump location_hospital

        "Talk to Dr. Lena" if npc_talkable("lena"):
            call npc_interact("lena")
            jump location_hospital

        "Dr. Lena's on rounds" if npc_known("lena") and not npc_here("lena"):
            "She's somewhere in the ward, not the desk. Catch her on a day shift."
            jump location_hospital

        "Quit medicine" if job_id == "hospital":
            $ quit_job()
            "You hang up the coat. Not everyone's built for it."
            jump location_hospital

        "Leave to City Map":
            jump map

# ── THE HUB (IT career) ───────────────────────────────────────────────
label location_hub:
    scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
    show screen hud
    menu (screen="activity"):
        "The Hub - IT coworking."

        "Work a shift (8h)" if job_id == "it":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_hub
            $ _tired = do_shift("it", 8)
            if _tired:
                "You push through running on fumes - not your sharpest code."
            else:
                "Headphones on, heads down. A good day's work shipped."
            jump location_hub

        "Ask about a promotion" if job_id == "it" and job_performance >= 100:
            if promote():
                "Your lead grins. \"Earned it.\" New title, better pay, higher bar."
            else:
                "\"Strong quarter - but you need the skills for the next rung first.\""
            jump location_hub

        "Apply for a dev role" if job_id is None and can_apply("it"):
            $ apply_job("it")
            "You nail the interview. Junior Dev at The Hub. Welcome to the grind."
            jump location_hub

        "Apply for a dev role (need Programming 1 + INT 25)" if job_id is None and not can_apply("it"):
            "They skim your resume and pass. Come back with Programming 1 and INT 25 - the college teaches code."
            jump location_hub

        "Quit this job" if job_id == "it":
            $ quit_job()
            "You hand in your notice. Free again - broke soon, but free."
            jump location_hub

        "Leave to City Map":
            jump map

# ── CITY COLLEGE (learn professional skills) ──────────────────────────
label location_college:
    scene college_day
    show screen hud
    menu (screen="activity"):
        "City College - take a course to raise a professional skill. (3h, $60 each)"

        "Programming course":
            call college_course("prog")
            jump location_college
        "Medicine course":
            call college_course("med")
            jump location_college
        "Business course":
            call college_course("biz")
            jump location_college
        "Art course":
            call college_course("art")
            jump location_college

        "Leave to City Map":
            jump map

label college_course(key):
    $ _r = take_course(key)
    if _r == "money":
        "You can't cover the $60 course fee right now."
    elif _r == "max":
        "You've maxed this one out - nothing more they can teach you here."
    else:
        "Three hours of lectures and exercises. It's starting to click."
    return

# ── SLEEP ─────────────────────────────────────────────────────────────
label action_sleep:
    $ new_day()
    scene expression home_bg()
    show screen hud
    $ datestr = "Day %d - %s" % (day + 1, day_name(day))
    "You sleep through the night.\n[datestr]"
    jump map

# ── MAP ────────────────────────────────────────────────────────────────
label map:
    scene map_city
    show screen hud
    call screen city_map
