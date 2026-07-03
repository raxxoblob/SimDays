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

        "Nap (3h)" if own_bed:
            $ spend_time(3)
            $ need_energy = min(100, need_energy + 45)
            "A proper nap on a proper bed. You wake up sharp."
            jump location_home_actions

        "Practice coding (3h)" if own_computer:
            $ spend_time(3)
            $ gain_skill("prog", 1)
            "Three hours deep in a side project. The docs finally click."
            jump location_home_actions

        "Trade stocks" if own_computer:
            call screen stock_market
            jump location_home_actions

        "Practice guitar (2h)" if own_guitar:
            $ spend_time(2)
            $ gain_skill("music", 1)
            "You run scales and a couple of songs. Fingers sore, ear sharper."
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
    if npc_talkable("nora"):
        show nora_cafe_normal as npcsprite at sprite_r

    menu (screen="activity"):
        "What do you want to do at the cafe?"

        "Buy a coffee ($3, 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-3)
            $ need_hunger = min(100, need_hunger + 10)
            "You sip a good coffee. Worth it."
            jump cafe_actions

        "Talk to Nora" if npc_talkable("nora"):
            call npc_interact("nora")
            jump cafe_actions

        "Work a shift - Barista (4h)":
            jump cafe_work_shift

        "Leave to City Map":
            jump map

label cafe_work_shift:
    if hour + 4 > DAY_END:
        "It's too late to start a full shift."
        jump cafe_actions
    $ spend_time(4)
    $ gain_money(60)
    "Four hours of steaming milk and small talk. You pocket $60."
    if npc_here("nora"):
        show nora_cafe_normal at sprite_r
        if not cafe_shift_done:
            $ cafe_shift_done = True
            n "Not bad for a first shift. Henry says you're a natural - high praise, he called me 'adequate' for a year."
        else:
            n "Another one down. You're basically furniture now. The good kind."
        hide nora_cafe_normal
    jump cafe_actions

# ── GYM ───────────────────────────────────────────────────────────────
label location_gym:
    scene gymdaypeople
    show screen hud
    menu (screen="activity"):
        "What do you want to do at the gym?"
        "Train - weights (1.5h)":
            $ spend_time(1.5)
            $ gain_stat("str", 2)
            $ gain_stat("app", 1)
            "A solid session. You can feel it already."
            jump location_gym
        "Cardio run (1h)":
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
        "Study (2h)":
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
        "Socialize (1h)":
            if stat_chr >= 25:
                $ spend_time(1)
                $ gain_stat("chr", 2)
                "You work the room. A few numbers exchanged."
            else:
                "You hover near a few groups but can't quite break in. Maybe with a bit more charm."
            jump location_bar
        "Leave to City Map":
            jump map

# ── OFFICE ────────────────────────────────────────────────────────────
label location_office:
    scene goodoffice1
    show screen hud
    menu (screen="activity"):
        "Nexus Tower - corporate floor."
        "Work a shift (8h)" if stat_int >= 20:
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_office
            $ spend_time(8)
            $ gain_money(120)
            $ gain_stat("int", 1)
            if not caroline_met:
                $ caroline_met = True
                $ martha_met = True
                "A long first day. HR's Caroline clocks you on the way out - \"I keep tabs on everyone.\" A sharp woman by the windows barely looks up: Martha, apparently, and unimpressed."
            else:
                "A long day of meetings and spreadsheets. The pay is solid."
            jump location_office
        "Apply for work" if stat_int < 20:
            show caroline_normal at sprite_r
            caro "HR. Let me save us both time - these roles need a sharper head than that. INT 20, minimum. The college helps."
            hide caroline_normal
            jump location_office
        "Talk to Caroline" if npc_talkable("caroline"):
            call npc_interact("caroline")
            jump location_office
        "Talk to Martha" if npc_talkable("martha"):
            call npc_interact("martha")
            jump location_office
        "Leave to City Map":
            jump map

# ── MALL (shop hub) ───────────────────────────────────────────────────
label location_mall:
    scene expression ("mallnight" if hour >= 19 else "mallday")
    call screen mall_hub

label location_shop_clothing:
    scene clothesshop
    show screen hud
    menu (screen="activity"):
        "Clothing store."
        "Buy an outfit ($80)":
            if money < 80:
                "Not enough money."
            else:
                $ gain_money(-80)
                $ gain_stat("app", 2)
                "New fit. You look sharper."
            jump location_shop_clothing
        "Upgrade your wardrobe ($200, +status)" if wardrobe_tier < 3:
            if money < 200:
                "Not enough money."
            else:
                $ gain_money(-200)
                $ wardrobe_tier += 1
                "Designer pieces, tailored. You carry yourself differently - people notice."
            jump location_shop_clothing
        "Back to the mall":
            jump location_mall

label location_shop_electronics:
    scene electronicsshop
    show screen hud
    menu (screen="activity"):
        "Electronics store."
        "Buy a gadget ($100)":
            if money < 100:
                "Not enough money."
            else:
                $ gain_money(-100)
                $ gain_stat("int", 1)
                "A new toy to tinker with. You learn a thing or two."
            jump location_shop_electronics
        "Buy a guitar ($150)" if not own_guitar:
            if money < 150:
                "Not enough money."
            else:
                $ gain_money(-150)
                $ own_guitar = True
                "A decent starter guitar. Now you can practice music at home."
            jump location_shop_electronics
        "Back to the mall":
            jump location_mall

label location_shop_gifts:
    scene giftshop
    show screen hud
    menu (screen="activity"):
        "Gift & lifestyle shop."
        "Treat yourself ($30, +energy)":
            if money < 30:
                "Not enough money."
            else:
                $ gain_money(-30)
                $ need_energy = min(100, need_energy + 15)
                "A small indulgence. You feel a little brighter."
            jump location_shop_gifts
        "Buy a better bed ($400)" if not own_bed:
            if money < 400:
                "Not enough money."
            else:
                $ gain_money(-400)
                $ own_bed = True
                "Delivered and set up at home. Sleep restores fully now - and you can grab a Nap."
            jump location_shop_gifts
        "Buy jewelry ($250, +status)" if jewelry_tier < 3:
            if money < 250:
                "Not enough money."
            else:
                $ gain_money(-250)
                $ jewelry_tier += 1
                "A tasteful piece that quietly says you've arrived."
            jump location_shop_gifts
        "Buy a gift ($40)":
            if money < 40:
                "Not enough money."
            else:
                $ gain_money(-40)
                $ gift_count += 1
                "A nicely wrapped little something. Give it to someone you're getting to know."
            jump location_shop_gifts
        "Back to the mall":
            jump location_mall

# ── CAR DEALER (status via car_tier) ──────────────────────────────────
# ponytail: reuses carworkshop bg + garage icon as placeholders - swap for a
# proper showroom/dealer background + icon when generated.
label location_cardealer:
    scene carworkshop
    show screen hud
    menu (screen="activity"):
        "City Motors - the showroom floor."
        "Buy a used runabout ($1500)" if car_tier < 1:
            if money < 1500:
                "Not enough money. The salesman's smile cools."
            else:
                $ gain_money(-1500)
                $ car_tier = 1
                "Nothing fancy, but it's yours. Wheels change how the city sees you."
            jump location_cardealer
        "Trade up to a nice car ($5000)" if car_tier == 1:
            if money < 5000:
                "Not enough money for the upgrade yet."
            else:
                $ gain_money(-5000)
                $ car_tier = 2
                "Clean lines, leather seats. People clock it in the parking lot."
            jump location_cardealer
        "Buy the luxury model ($15000)" if car_tier == 2:
            if money < 15000:
                "Not enough for the flagship. Come back richer."
            else:
                $ gain_money(-15000)
                $ car_tier = 3
                "The kind of car that opens doors before you say a word."
            jump location_cardealer
        "Your car's top of the line" if car_tier >= 3:
            "Nothing here beats what's already in your garage."
            jump location_cardealer
        "Leave to City Map":
            jump map

# ── NIGHTCLUB ─────────────────────────────────────────────────────────
label location_nightclub:
    scene nightclub
    show screen hud
    menu (screen="activity"):
        "The club - lights, bass, a wall of bodies."
        "Hit the dance floor (1h)":
            $ spend_time(1)
            $ need_energy = max(0, need_energy - 10)
            "You lose an hour to the beat. Worth it."
            jump location_nightclub
        "Work the crowd (1h)":
            if stat_chr >= 30:
                $ spend_time(1)
                $ gain_stat("chr", 2)
                "You move room to room, easy and loud. A few new contacts."
            else:
                "The in-crowd closes ranks. You can't quite break in yet - not smooth enough."
            jump location_nightclub
        "Buy a round ($15)":
            $ spend_time(0.5)
            $ gain_money(-15)
            "Drinks all around. Cheap way to be popular for ten minutes."
            jump location_nightclub
        "Leave to City Map":
            jump map

# ── PARK ──────────────────────────────────────────────────────────────
label location_park:
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    menu (screen="activity"):
        "The park."
        "Morning jog (1h)":
            $ spend_time(1)
            $ gain_stat("str", 1)
            "The air is crisp. Good start to the day."
            jump location_park
        "Read a book (1.5h)":
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
    if npc_talkable("elle"):
        show elle_sundress_normal as npcsprite at sprite_r
    menu (screen="activity"):
        "The beach."
        "Relax (1h)":
            $ spend_time(1)
            $ need_energy = min(100, need_energy + 10)
            "The waves and sun do wonders."
            jump location_beach
        "Talk to Elle" if npc_talkable("elle"):
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
    if npc_talkable("natalie"):
        show natalie_normal as npcsprite at sprite_r
    menu (screen="activity"):
        "LogiCity Warehouse."
        "Work a shift (8h)" if stat_str >= 25:
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
        "Apply for work" if stat_str < 25:
            show natalie_normal at sprite_r
            nat "Come back when you can actually lift. STR 25, minimum. Next."
            hide natalie_normal
            jump location_warehouse
        "Talk to Natalie" if npc_talkable("natalie"):
            call npc_interact("natalie")
            jump location_warehouse
        "Leave to City Map":
            jump map

# ── HOSPITAL ──────────────────────────────────────────────────────────
label location_hospital:
    scene expression ("hospital_night" if (hour >= 20 or hour < 6) else "hospital1")
    show screen hud
    if npc_talkable("lena"):
        show drlena_normal as npcsprite at sprite_r
    menu (screen="activity"):
        "City Hospital - reception. Antiseptic and quiet hurry."

        "Cosmetic touch-up ($200, 2h)":
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
                "Exhausted and unfed, you fumble a chart and get chewed out. A shift like this sets you back."
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

        "Drop off your CV" if job_id is None:
            show drlena_normal at sprite_r
            if can_apply("hospital"):
                "A doctor at the desk skims your file. \"Med Student it is. Try not to faint.\" You're in."
                hide drlena_normal
                $ apply_job("hospital")
            else:
                "A tired doctor hands your CV back. \"Not there yet - Medicine 1 and INT 20, minimum. The college teaches it.\""
                hide drlena_normal
            jump location_hospital

        "Talk to Dr. Lena" if npc_talkable("lena"):
            call npc_interact("lena")
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
                "Running on fumes, you ship bugs and miss the standup. Your lead notices. Performance took a hit."
            else:
                "Headphones on, heads down. A good day's work shipped."
            jump location_hub

        "Ask about a promotion" if job_id == "it" and job_performance >= 100:
            if promote():
                "Your lead grins. \"Earned it.\" New title, better pay, higher bar."
            else:
                "\"Strong quarter - but you need the skills for the next rung first.\""
            jump location_hub

        "Apply for a dev role" if job_id is None:
            if can_apply("it"):
                $ apply_job("it")
                "You nail the interview. Junior Dev at The Hub. Welcome to the grind."
            else:
                "A dev lead skims your work and slides it back. \"Not yet - Programming 1 and INT 25, minimum. The college runs courses.\""
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

# Neglect consequences - checked at the map hub (between activities), so it never
# interrupts mid-action and only fires at real extremes.
label check_collapse:
    if need_hunger <= 0:
        scene expression Solid("#000000") with fade
        "The edges of everything go white. You don't remember hitting the floor."
        scene hospital1 with fade
        show screen hud
        "You come round in the ER, a drip in your arm. Skipping every meal finally caught up with you - and the bill isn't cheap."
        $ gain_money(-100)
        $ need_hunger = 60
        $ need_energy = 70
        if job_id is not None:
            $ job_performance = max(0, job_performance - 15)
        $ new_day()
        return
    if need_energy <= 0:
        scene expression Solid("#000000") with fade
        "Your body overrules you. You black out where you stand."
        $ new_day()
        # A blackout is NOT a good night's sleep - you wake groggy, grimy, and behind.
        $ need_energy = 45
        $ need_hygiene = max(0, need_hygiene - 20)
        if job_id is not None:
            $ job_performance = max(0, job_performance - 15)
        scene expression home_bg() with fade
        show screen hud
        "You come to hours later, wherever you dropped - stiff, filthy, head pounding. The day's gone and you feel worse than before."
        return
    if not warned_today and (need_hunger < 18 or need_energy < 18 or need_hygiene < 18):
        $ warned_today = True
        $ renpy.notify("You're running on fumes - eat, sleep, or clean up soon.")
    return

# ── MAP ────────────────────────────────────────────────────────────────
label map:
    call check_collapse
    scene map_city
    show screen hud
    call screen city_map
