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

        "Sleep":
            jump action_sleep_menu

        "Cook something" if need_hunger < 90:
            jump location_home_cook

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

        "Use computer" if own_computer:
            jump use_computer

        "Practice guitar (2h)" if own_guitar:
            $ spend_time(2)
            $ gain_skill("music", 5)
            "You run scales and a couple of songs. Fingers sore, ear sharper."
            jump location_home_actions

        "Take the metro (0.5h)":
            jump take_metro

label location_home_cook:
    scene expression home_bg()
    show screen hud
    menu (screen="activity"):
        "Kitchen. What are you making?"
        "Toast ($2, +15 hunger)":
            if money < 2:
                "Not enough for even this. Pick up groceries on your phone."
                jump location_home_cook
            $ spend_time(0.25)
            $ gain_money(-2)
            $ need_hunger = min(100, need_hunger + 15)
            "Two slices of toast. Better than nothing."
            jump location_home_actions
        "Instant noodles ($3, +22 hunger)":
            if money < 3:
                "No noodles in the cupboard."
                jump location_home_cook
            $ spend_time(0.25)
            $ gain_money(-3)
            $ need_hunger = min(100, need_hunger + 22)
            "Straight out of the packet, four minutes. Fine."
            jump location_home_actions
        "Scrambled eggs ($5, +32 hunger)":
            if money < 5:
                "Out of eggs. Get groceries."
                jump location_home_cook
            $ spend_time(0.5)
            $ gain_money(-5)
            $ need_hunger = min(100, need_hunger + 32)
            "Oil, heat, three eggs. You feel a bit more human."
            jump location_home_actions
        "Pasta bolognese ($8, +55 hunger) [[Cooking Lv 2]]":
            if skill_cook < 2:
                "Not there yet - the sauce would be embarrassing. Raise your Cooking skill first."
                jump location_home_cook
            if money < 8:
                "You'd need $8 of groceries for this one."
                jump location_home_cook
            $ spend_time(0.5)
            $ gain_money(-8)
            $ need_hunger = min(100, need_hunger + 55)
            $ gain_skill("cook", 2)
            "Proper sauce, actual garlic. Getting the hang of this."
            jump location_home_actions
        "Chicken stir-fry ($10, +65 hunger, +8 energy) [[Cooking Lv 4]]":
            if skill_cook < 4:
                "High heat, precise timing - you'd ruin it. Cooking Lv 4 needed."
                jump location_home_cook
            if money < 10:
                "Not enough for the ingredients right now."
                jump location_home_cook
            $ spend_time(0.75)
            $ gain_money(-10)
            $ need_hunger = min(100, need_hunger + 65)
            $ need_energy = min(100, need_energy + 8)
            $ gain_skill("cook", 2)
            "Fast, hot, loud. A proper meal - you feel it in the energy too."
            jump location_home_actions
        "Sunday roast ($18, +80 hunger, +15 energy) [[Cooking Lv 7]]":
            if skill_cook < 7:
                "This takes real skill and a whole afternoon. Cooking Lv 7 needed."
                jump location_home_cook
            if money < 18:
                "You'd need $18 for a proper roast's worth of ingredients."
                jump location_home_cook
            $ spend_time(1.0)
            $ gain_money(-18)
            $ need_hunger = min(100, need_hunger + 80)
            $ need_energy = min(100, need_energy + 15)
            $ gain_skill("cook", 3)
            "An afternoon's prep. The apartment smells like a real home. You feel genuinely full for the first time in a while."
            jump location_home_actions
        "Close the fridge.":
            jump location_home_actions

# ponytail: reuses home_bg - swap for a desk/monitor screen background later.
label use_computer:
    scene expression home_bg()
    show screen hud
    menu (screen="activity"):
        "At the computer."
        "Practice coding (3h)":
            $ spend_time(3)
            $ gain_skill("prog", 3)
            "Three hours deep in a side project. The docs finally click."
            jump use_computer
        "Trade stocks":
            call screen stock_market
            jump use_computer
        "Browse the web (0.5h)":
            $ spend_time(0.5)
            "You fall down a few rabbit holes. Nothing productive."
            jump use_computer
        "Get up":
            jump location_home_actions

# ── CAFE ──────────────────────────────────────────────────────────────
label location_cafe:
    if not venue_open("coffee_shop"):
        "The café is closed. Come back between 07:00–19:00."
        jump take_metro
    scene expression cafe_bg()
    show screen hud
    if not nora_met:
        jump cafe_first_visit
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
    if nora_affection >= 40 and hour >= 19 and not nora_closing_done:
        jump nora_closing_scene
    if hour >= 19:
        "The café lights are going off. Time to head out."
        jump take_metro
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

        "Take the metro (0.5h)":
            jump take_metro

label cafe_work_shift:
    if hour + 4 > DAY_END:
        "It's too late to start a full shift."
        jump cafe_actions
    if need_energy < 15:
        "You can barely keep your eyes open. Even Henry would send you home. Sleep first."
        jump cafe_actions
    scene pov_barista
    show screen hud
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
    if not venue_open("gym"):
        "The gym is closed for the night."
        jump take_metro
    scene gymdaypeople
    show screen hud
    menu (screen="activity"):
        "What do you want to do at the gym?"
        "Train - weights (1.5h)":
            if too_tired():
                "You're too wiped out to lift anything worth lifting. Sleep first."
                jump location_gym
            scene pov_gym_weights
            show screen hud
            $ spend_time(1.5)
            $ need_energy = max(0, need_energy - 15)
            $ gain_stat("str", 2)
            $ gain_stat("app", 1)
            "A solid session. You can feel it already."
            jump location_gym
        "Cardio run (1h)":
            if too_tired():
                "Too exhausted to run. Get some sleep first."
                jump location_gym
            scene gym_cardio
            show screen hud
            $ spend_time(1)
            $ need_energy = max(0, need_energy - 12)
            $ gain_stat("str", 1)
            "You run until your lungs complain."
            jump location_gym
        "Take the metro (0.5h)":
            jump take_metro

# ── LIBRARY ───────────────────────────────────────────────────────────
label location_library:
    if not venue_open("library"):
        "The library is closing. Time to head out."
        jump take_metro
    scene expression ("librarynight" if hour >= 20 else "libraryday")
    show screen hud
    if npc_talkable("eli"):
        show eli_normal as npcsprite at sprite_r
    menu (screen="activity"):
        "What do you want to do at the library?"
        "Study — general (2h)":
            if too_tired():
                "Too tired to focus. The words blur. Sleep first."
                jump location_library
            $ spend_time(2)
            $ gain_stat("int", 2)
            "Two hours of focused reading. Your brain hurts in a good way."
            jump location_library
        "Self-study a subject (2h, free)":
            if too_tired():
                "Too tired to concentrate on anything. Sleep first."
                jump location_library
            menu:
                "What are you working through?"
                "Medicine":
                    $ spend_time(2)
                    $ need_energy = max(0, need_energy - 10)
                    $ gain_skill("med", 1)
                    "Dense textbooks, clinical notes. Slower than a real course, but it sticks."
                "Programming":
                    $ spend_time(2)
                    $ need_energy = max(0, need_energy - 10)
                    $ gain_skill("prog", 1)
                    "Tutorials, docs, Stack Overflow rabbit holes. You get somewhere."
                "Business":
                    $ spend_time(2)
                    $ need_energy = max(0, need_energy - 10)
                    $ gain_skill("biz", 1)
                    "Case studies and frameworks. Dry but useful."
                "Art":
                    $ spend_time(2)
                    $ need_energy = max(0, need_energy - 10)
                    $ gain_skill("art", 1)
                    "Theory, references, sketching. You can feel the improvement in small ways."
            jump location_library
        "Talk to Eli" if npc_talkable("eli"):
            call npc_interact("eli")
            jump location_library
        "Take the metro (0.5h)":
            jump take_metro

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
        "Take the metro (0.5h)":
            jump take_metro

# ── OFFICE ────────────────────────────────────────────────────────────
label location_office:
    if not venue_open("office_exec"):
        "Nexus Tower is locked up for the night."
        jump take_metro
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
        "Take the metro (0.5h)":
            jump take_metro

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
label location_cardealer:
    scene cardealer_day
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
        "Take the metro (0.5h)":
            jump take_metro

# ── KITCHEN / Eleven (Culinary career) ────────────────────────────────
label location_kitchen:
    scene kitchen
    show screen hud
    menu (screen="activity"):
        "Eleven - the kitchen. Heat, steel, tickets."

        "Work a shift (8h)" if job_id == "culinary":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_kitchen
            if too_tired():
                "Too wiped to cook a full service. Go sleep - chef's orders."
                jump location_kitchen
            scene pov_chef
            show screen hud
            $ _tired = do_shift("culinary", 8)
            if _tired:
                "Slammed and half-asleep, you burn a plate and hear about it. Bad night on the line."
            else:
                "A brutal service, but you kept your station clean and fast. Chef almost nodded."
            jump location_kitchen

        "Ask about a promotion" if job_id == "culinary" and job_performance >= 100:
            if promote():
                "The chef grunts approval and hands you a bigger station. Moving up."
            else:
                "\"Not yet. Cook more, cook better, then we talk.\""
            jump location_kitchen

        "Drop off your CV" if job_id is None:
            if can_apply("culinary"):
                $ apply_job("culinary")
                "The head chef eyes your knife roll. \"Commis. Don't bleed on my food.\" You're in."
            else:
                "The head chef barely looks up. \"Not ready. Cooking 1 and some muscle, minimum. Learn to prep first.\""
            jump location_kitchen

        "Quit the kitchen" if job_id == "culinary":
            $ quit_job()
            "You hang up the apron. The heat wasn't for you."
            jump location_kitchen

        "Take the metro (0.5h)":
            jump take_metro

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
        "Take the metro (0.5h)":
            jump take_metro

# ── PARK ──────────────────────────────────────────────────────────────
label location_park:
    scene expression ("parknight" if hour >= 20 else "parkday")
    show screen hud
    if npc_talkable("zoe"):
        show zoe_punk_smile as npcsprite at sprite_r
    elif npc_talkable("sam"):
        show sam_normal as npcsprite at sprite_r
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
        "Play basketball (1.5h)":
            scene basketball_court_day
            show screen hud
            $ spend_time(1.5)
            $ gain_stat("str", 2)
            "A pickup game on the court. Sweaty, competitive, good."
            jump location_park
        "Talk to Zoe" if npc_talkable("zoe"):
            call npc_interact("zoe")
            jump location_park
        "Talk to Sam" if npc_talkable("sam"):
            call npc_interact("sam")
            jump location_park
        "Take the metro (0.5h)":
            jump take_metro

# ── BEACH ─────────────────────────────────────────────────────────────
label location_beach:
    scene expression ("beachnight" if hour >= 19 else "beachday")
    show screen hud
    if not zoe_met and hour < 19:
        jump beach_meet_zoe
    if elle_affection >= 40 and not elle_pier_done and npc_talkable("elle"):
        jump elle_pier_scene
    if npc_talkable("elle"):
        show elle_sundress_normal as npcsprite at sprite_r
    elif npc_talkable("kai"):
        show kai_normal as npcsprite at sprite_r
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
        "Talk to Kai" if npc_talkable("kai"):
            call npc_interact("kai")
            jump location_beach
        "Take the metro (0.5h)":
            jump take_metro

# ── Zoe first meet - beach (daytime only, fires once) ─────────────────
label beach_meet_zoe:
    scene zoe_beach_1 with dissolve
    show screen hud
    "The beach out here is better than you expected. Not a resort strip - just sand and water and that particular quiet you only get when the city is far enough away to be decorative."
    "You find a clear patch and almost miss her."
    scene zoe_beach_2 with dissolve
    show screen hud
    "A girl, sitting cross-legged at the shoreline where the sand is still damp. A sketchbook balanced on her knees. Headphones around her neck - not on, just there, like she's not done with the world but keeping the option open."
    scene zoe_beach_3 with dissolve
    show screen hud
    "She holds a charcoal stick the way some people hold a cigarette - like it's part of the hand. The page is full of lines: the angle of waves, the smear of city buildings reflected in moving water."
    "She hasn't looked up once."
    scene beachday with dissolve
    show screen hud
    show zoe_street_neutral at sprite_r
    menu:
        "Go over. Say something.":
            jump zoe_beach_approach
        "Stay where you are. You don't break someone's flow.":
            jump zoe_beach_watch

label zoe_beach_approach:
    "You cross the sand. She hears you coming - a slight adjustment of posture, but the charcoal keeps moving."
    "Then you're close enough that staying silent becomes its own thing, and she looks up."
    scene beachday with dissolve
    show screen hud
    show zoe_street_neutral at sprite_r
    z "Can I help you?"
    scene zoe_beach_4 with dissolve
    show screen hud
    "Measured. Not unfriendly. The voice of someone who has ranked interrupt-interrupters before and is simply placing you."
    menu:
        "\"I was curious what you're drawing.\"":
            z "Waves. The way the buildings catch in the water when there's a swell."
            scene zoe_beach_5 with dissolve
            show screen hud
            "She angles the sketchbook toward you, briefly - just enough. The lines are loose and confident. Building reflections broken into something almost abstract."
            scene beachday with dissolve
            show screen hud
            show zoe_street_talk at sprite_r
            z "It doesn't translate in a photo. Which is the entire point."
            show zoe_street_neutral at sprite_r
            "She pulls it back."
            z "Most people who interrupt me out here want to know if I'm a 'real artist.' Like there's a counterfeit version."
            menu:
                "\"Are you?\"":
                    show zoe_street_talk at sprite_r
                    z "Define it and I'll tell you. I make things. Whether that qualifies depends on who's reviewing the grant."
                    "She gives you another look. Slower this time."
                    z "You're new. You've got the look."
                    $ zoe_affection += 2
                "\"What does the fake kind look like?\"":
                    show zoe_street_smile at sprite_r
                    z "Ha."
                    "Short. Real. She wasn't expecting that one."
                    show zoe_street_talk at sprite_r
                    z "Sells prints on a website. Talks a lot about their 'process' at dinner parties. But I try not to be mean about it."
                    z "You're new here. I can always tell."
                    $ zoe_affection += 4
            jump zoe_beach_shared
        "\"Hey - I'm [mc_name]. Just moved in.\"":
            z "Zoe."
            "She says it the way you sign a receipt. Efficient. Then she actually looks at you."
            z "New to the city or just new to this part of it?"
            menu:
                "\"New to the city. Still finding my feet.\"":
                    z "Then this is a good first beach. Locals mostly use it. The tourist one's two bays over - noisier, worse coffee, everyone's performing."
                    z "How long have you been here?"
                    "You tell her."
                    z "Long enough to find the beach, not long enough to know anyone. That's the good window, actually. Before the city starts feeling small."
                    $ zoe_affection += 3
                "\"New to this neighborhood. Still working out the city.\"":
                    z "It has a trick to it. Took me a year before I stopped getting turned around by the waterfront."
                    z "Pick a direction and walk until something's worth drawing. That's my method. It's not efficient, but it works."
                    "She seems satisfied you're not about to be annoying."
                    z "You're not the type who talks just to fill silence?"
                    menu:
                        "\"Not really.\"":
                            z "Good. Pull up some sand if you want. I've got ten more minutes of light."
                            $ zoe_affection += 4
                        "\"Sometimes. Depends on the silence.\"":
                            z "Fair. That's actually fair."
                            $ zoe_affection += 3
            scene beachday with dissolve
            show screen hud
            jump zoe_beach_shared

label zoe_beach_watch:
    "You hang back. She's in that specific kind of concentration where interrupting would be like tripping a cable mid-charge. You know that state. You respect it."
    "A few minutes go by. The water's good out here. There's a container ship on the horizon - absurdly large, barely moving."
    "She erases something. Makes a short frustrated sound, almost inaudible. Re-draws the line. Erases it again."
    "Her shoulders drop slightly. There's something she's trying to get that isn't coming."
    "You understand that too."
    "Five minutes. Maybe more. Long enough that you stop counting."
    "She stretches - rolls her neck, sets the charcoal down on the sketchbook - and turns to look at the water."
    "Sees you immediately."
    scene zoe_beach_4 with dissolve
    show screen hud
    "A long pause. She looks at you, then back at the water, then at you again."
    scene beachday with dissolve
    show screen hud
    show zoe_street_surprised at sprite_r
    z "...You've been standing there this whole time."
    "Not a question."
    z "I would have heard you leave."
    menu:
        "\"I didn't want to interrupt.\"":
            show zoe_street_talk at sprite_r
            z "You were going to eventually. Everyone does."
            z "What stopped you?"
            menu:
                "\"You were getting somewhere. I could see it from here.\"":
                    "She blinks. Looks at the sketchbook. Then back at you."
                    show zoe_street_neutral at sprite_r
                    z "...I wasn't, actually. But that's the right thing to look for."
                    $ zoe_affection += 5
                "\"Breaking flow felt rude.\"":
                    z "Most people don't think about that."
                    show zoe_street_neutral at sprite_r
                    z "Sit down. You're making me self-conscious."
                    $ zoe_affection += 3
        "\"You looked like you were in it.\"":
            show zoe_street_talk at sprite_r
            z "I was. I'm not anymore. Something I was chasing got away from me."
            "She doesn't sound angry. Just honest about it."
            show zoe_street_neutral at sprite_r
            z "You can come over. Since you've been hovering."
            $ zoe_affection += 3
        "[Say nothing. Just hold up a hand - caught, fair enough.]":
            show zoe_street_talk at sprite_r
            "She stares at you for a second. Then a short exhale. Almost a laugh."
            z "Okay."
            show zoe_street_neutral at sprite_r
            z "Come sit. You're going to get a crick in your neck standing like that."
            $ zoe_affection += 4
    "You cross the sand and sit down next to her. She goes back to the page, or pretends to."
    scene zoe_beach_5 with dissolve
    show screen hud
    "The sea does that thing where it sounds like breathing."
    scene beachday with dissolve
    show screen hud
    show zoe_street_neutral at sprite_r
    "After a minute:"
    z "What do you see? In the water."
    "It's a test. You can feel it."
    menu:
        "\"Reflections. The city upside-down.\"":
            show zoe_street_talk at sprite_r
            z "Yeah. That's it exactly."
            z "Nobody looks at that. They look at the waves or the horizon. The interesting part's always in the middle somewhere."
            show zoe_street_neutral at sprite_r
            $ zoe_affection += 3
        "\"Just water. I'm not going to pretend otherwise.\"":
            show zoe_street_talk at sprite_r
            z "Honest."
            z "The water's fine. It's what it does to everything around it that matters. But that comes with practice."
            $ zoe_affection += 2
        "\"The city. But softer.\"":
            show zoe_street_smile at sprite_r
            "She looks at you sideways."
            z "Okay. You pass."
            show zoe_street_neutral at sprite_r
            $ zoe_affection += 4
    jump zoe_beach_shared

label zoe_beach_shared:
    "Eventually she closes the sketchbook. Taps it twice with one charcoal-stained finger like she's filing the whole session away."
    z "First time at this beach?"
    "You tell her it is."
    show zoe_street_talk at sprite_r
    z "It's the right one. The other two are for people who want to be seen at the beach. This one's for people who actually want the beach."
    "She starts brushing sand from her jeans. There's charcoal on two fingers. She doesn't bother with it."
    show zoe_street_neutral at sprite_r
    z "I'm here most weeks when it's not raining. Trying to get the reflections right before the season changes and the light goes flat."
    "She tucks the sketchbook under her arm and stands."
    z "You're not the worst person to run into."
    "She says it the way someone gives a verdict. Which, you think, she basically did."
    show zoe_street_smile at sprite_r
    "The smile that follows - half-turned away, like she didn't sign off on it - happens anyway."
    scene zoe_beach_6 with dissolve
    show screen hud
    "She walks off down the shore."
    scene zoe_beach_7 with dissolve
    show screen hud
    "You watch for a second."
    "You think: {i}that one's going to be interesting.{/i}"
    scene beachday with dissolve
    show screen hud
    $ zoe_met = True
    $ spend_time(1)
    hide zoe_street_neutral
    hide zoe_street_smile
    hide zoe_street_talk
    hide zoe_street_surprised
    jump location_beach

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
            if too_tired():
                "Too exhausted to haul anything safely. Natalie would send you home. Sleep first."
                jump location_warehouse
            scene pov_warehouse
            show screen hud
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
        "Take the metro (0.5h)":
            jump take_metro

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
            if too_tired():
                "You can't work a medical shift this drained - patient safety. Sleep first."
                jump location_hospital
            scene pov_doctor
            show screen hud
            $ _tired = do_shift("hospital", 8)
            if _tired:
                "Exhausted and unfed, you fumble a chart and get chewed out. A shift like this sets you back."
            else:
                "Charts, rounds, a dozen small crises handled. You earned the coffee."
            if not lena_rooftop_done and job_rank >= 1 and lena_trust >= 25 and hour >= 22:
                jump lena_rooftop_scene
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

        "Take the metro (0.5h)":
            jump take_metro

# ── THE HUB (IT career) ───────────────────────────────────────────────
label location_hub:
    if not venue_open("hub"):
        "The Hub is shut. Back at 08:00."
        jump take_metro
    scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
    show screen hud
    menu (screen="activity"):
        "The Hub - IT coworking."

        "Work a shift (8h)" if job_id == "it":
            if hour + 8 > DAY_END:
                "Too late to start a full shift today."
                jump location_hub
            if too_tired():
                "You're running on empty. Your lead would send you home. Sleep first."
                jump location_hub
            scene hub_pov
            show screen hud
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

        "Take the metro (0.5h)":
            jump take_metro

# ── CITY COLLEGE (learn professional skills) ──────────────────────────
label location_college:
    if not venue_open("university"):
        "The college is closed for the day. Back at 08:00."
        jump take_metro
    scene college_day
    show screen hud
    menu (screen="activity"):
        "City College — courses raise a professional skill. Cost rises with your level. (3h)"

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

        "Take the metro (0.5h)":
            jump take_metro

label college_course(key):
    if too_tired():
        "You're too exhausted to absorb anything. Come back after some sleep."
        return
    $ _r = take_course(key)
    if _r == "money":
        "You can't cover the course fee at your current level. Earn more first."
    elif _r == "max":
        "You've maxed this one out - nothing more they can teach you here."
    else:
        "Three hours of lectures and exercises. It's starting to click."
    return

# ── SLEEP ─────────────────────────────────────────────────────────────
label action_sleep_menu:
    scene expression home_bg()
    show screen hud
    menu (screen="activity"):
        "How long do you want to sleep?"
        "Until morning (8h) — new day, full rest":
            jump action_sleep
        "6 hours (+60 energy)":
            $ spend_time(6)
            $ need_energy = min(100, need_energy + 60)
            "Six hours. You wake in the dark, properly rested."
            jump location_home_actions
        "4 hours (+40 energy)":
            $ spend_time(4)
            $ need_energy = min(100, need_energy + 40)
            "Four hours. Functional, if not fresh."
            jump location_home_actions
        "2 hours (+20 energy)":
            $ spend_time(2)
            $ need_energy = min(100, need_energy + 20)
            "Two hours. Takes the edge off, nothing more."
            jump location_home_actions
        "Stay up":
            jump location_home_actions

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
    # energy==0 no longer causes collapse - demanding activities become unavailable instead.
    if not warned_today and (need_hunger < 22 or need_energy < 22 or need_hygiene < 18):
        $ warned_today = True
        $ renpy.notify("Running low - eat, sleep, or shower soon.")
    return

label take_metro:
    $ spend_time(0.5)
    "You take the metro. Thirty minutes of city views."
    jump map

# ── MAP ────────────────────────────────────────────────────────────────
label map:
    call check_collapse
    scene map_city
    show screen hud
    call screen city_map

# ── NORA - CLOSING TIME ────────────────────────────────────────────────
# Trigger: nora_affection >= 40, hour >= 19, not nora_closing_done
label nora_closing_scene:
    $ nora_closing_done = True
    scene cafenight with dissolve
    show screen hud
    "The café looks different at this hour. Chairs stacked on half the tables. One lamp above the counter. The espresso machine, finally, quiet."
    scene nora_closing_1 with dissolve
    show screen hud
    n "Closing time. Lucky for you there's one cup left in the pot. Come in or don't."
    "She doesn't wait for an answer - pours two cups, sets them on a table, sits down. You sit across from her."
    scene nora_closing_2 with dissolve
    show screen hud
    menu:
        "\"Didn't realise it was so late.\"":
            n "It always is, after a shift. Time does something weird behind the counter."
        "\"I was hoping you'd still be here.\"":
            $ nora_affection = min(100, nora_affection + 1)
            n "That's a thing to say."
    scene nora_closing_3 with dissolve
    show screen hud
    n "You've been in a lot lately. What are you actually looking for in this city?"
    menu:
        "\"A reason to stay.\"":
            $ nora_affection = min(100, nora_affection + 3)
            n "That's the honest answer."
            n "I hope you find one."
        "\"Money, mostly. And something that doesn't feel like wasted time.\"":
            $ nora_trust = min(100, nora_trust + 2)
            n "Yeah. That's most people. They just don't say it out loud."
        "\"Still figuring that out.\"":
            $ nora_affection = min(100, nora_affection + 2)
            n "Same, honestly. I've been figuring it out for three years and counting."
    scene nora_closing_4 with dissolve
    show screen hud
    "She wraps both hands tighter around the cup."
    n "I was supposed to be studying nursing right now. Deferred a year. Then another. Henry offered me full-time and the timing just... worked."
    "She glances at her hands."
    n "I'm good at this job. That's the annoying part. When you're bad at something it's easy to leave."
    scene nora_closing_5 with dissolve
    show screen hud
    menu:
        "\"Then go. You're clearly just waiting for permission.\"":
            $ nora_trust = min(100, nora_trust + 5)
            $ nora_affection = min(100, nora_affection + 4)
            n "...You make it sound that easy."
        "\"Being good at something isn't a reason to stay stuck in it.\"":
            $ nora_trust = min(100, nora_trust + 3)
            $ nora_affection = min(100, nora_affection + 3)
            n "Henry would cope."
            "She says it quietly, like she's testing the idea."
        "\"What's actually stopping you?\"":
            $ nora_trust = min(100, nora_trust + 4)
            $ nora_affection = min(100, nora_affection + 2)
            "She pauses a long time."
            n "Nothing good."
        "\"Let me walk you home.\"" if nora_affection >= 50:
            $ nora_trust = min(100, nora_trust + 4)
            $ nora_affection = min(100, nora_affection + 4)
            n "It's late and I live close."
            "Beat."
            n "You can tell me what you're running from on the way."
        "\"Let me walk you home.\"" if nora_affection < 50:
            $ nora_trust = min(100, nora_trust + 2)
            $ nora_affection = min(100, nora_affection + 2)
            n "I'm fine - it's five minutes."
            "Beat."
            n "Ask me again sometime."
    scene nora_closing_6 with dissolve
    show screen hud
    "She puts on her coat. Keys in hand. She looks around the café for a second - the habit of checking everything before she leaves."
    n "You're easier to talk to when there's no counter in the way."
    "She unlocks the door, holds it open."
    scene nora_closing_7 with dissolve
    show screen hud
    n "Don't tell Henry I gave away his last coffee."
    scene cafenight with dissolve
    show screen hud
    "The café lights go off as you step outside."
    jump take_metro

# ── ELLE - BEST SPOT PAST THE PIER ────────────────────────────────────
# Trigger: elle_affection >= 40, Wednesday 16-19, elle present — fires once
label elle_pier_scene:
    $ elle_pier_done = True
    scene elle_pier_1 with dissolve
    show screen hud
    "She doesn't head toward the main strip. She turns the other way, past the pier, where the sand gets quieter."
    el "Come on. I'll show you the actual beach."
    scene elle_pier_2 with dissolve
    show screen hud
    el "Nobody comes this far down. Which is exactly the point."
    "She drops onto a rock and kicks off her sandals. The water out here is the same water, but it feels different without the noise behind it."
    scene elle_pier_3 with dissolve
    show screen hud
    el "I come here when I need to not be anywhere specific, you know?"
    menu:
        "\"You come here a lot?\"":
            $ elle_affection = min(100, elle_affection + 1)
            el "Every Wednesday I can manage. Some weeks it's the only thing that feels like mine."
        "\"What are you running from?\"":
            el "That's a question."
            "She looks at you sideways. Not offended. Considering."
            el "Not running. Just... not arriving yet. There's a difference."
    scene elle_pier_4 with dissolve
    show screen hud
    el "Back home everyone always asks what I'm doing with my life. Out here nobody knows I exist."
    "She says it like it's a relief, not a complaint."
    menu:
        "\"What are you actually doing with your life?\"":
            $ elle_trust = min(100, elle_trust + 3)
            el "Currently? Sitting on a rock, avoiding that exact question. You're terrible at this."
            "She's smiling when she says it."
        "\"Sounds like you needed to disappear for a while.\"":
            $ elle_affection = min(100, elle_affection + 2)
            $ elle_trust = min(100, elle_trust + 2)
            el "Yeah. Something like that."
            "A pause. The sea fills it better than words would."
        "\"I know that feeling.\"":
            $ elle_trust = min(100, elle_trust + 3)
            el "Do you?"
            "She looks at you properly for the first time since you sat down."
            el "Good. Then you get it."
    scene elle_pier_5 with dissolve
    show screen hud
    "You sit there without saying much. The light goes gold and orange."
    scene elle_pier_6 with dissolve
    show screen hud
    el "We should do something normal sometime. Not a beach. Something where we have to actually talk."
    menu:
        "\"Is that an invitation?\"":
            $ elle_affection = min(100, elle_affection + 2)
            el "If you want it to be."
        "\"I'd like that.\"":
            $ elle_affection = min(100, elle_affection + 2)
            el "Me too."
    scene beachday with dissolve
    show screen hud
    "You walk back along the shore toward the metro stop."
    jump take_metro

# ── DR. LENA - ROOFTOP, 3 A.M. ────────────────────────────────────────
# Trigger: hospital job rank >= 1, lena_trust >= 25, hour >= 22 — fires once after a night shift
label lena_rooftop_scene:
    $ lena_rooftop_done = True
    scene hospital_rooftop_night with dissolve
    show screen hud
    "The stairwell door is already propped open. You weren't planning to come up here — but the ward feels impossible right now and the sky is the only ceiling that isn't fluorescent."
    scene lena_rooftop_1 with dissolve
    show screen hud
    lena "I figured someone else would come up eventually."
    "She has a paper cup of something. She doesn't look like a doctor right now. She looks like someone who's been at it too long."
    menu:
        "\"Rough shift?\"":
            lena "Twelve beds, two residents calling in. Standard chaos."
            "She says it flat. Not complaining — just cataloguing."
        "\"I didn't know this was up here.\"":
            lena "Most people don't bother finding out. The view's not worth it unless you need it to be."
    scene lena_rooftop_2 with dissolve
    show screen hud
    "You sit on the ledge beside her. The city is quiet at this hour in a way it never is from ground level."
    lena "You did well tonight, by the way. That tachycardia in bed seven — you caught it before I did."
    scene lena_rooftop_3 with dissolve
    show screen hud
    lena "I keep thinking I'll get used to it. The nights where you can't actually fix anything."
    "She's looking out at the city, not at you."
    lena "You just manage. Make it slightly less bad. Go home. Come back."
    menu:
        "\"That sounds exhausting.\"":
            $ lena_trust = min(100, lena_trust + 3)
            lena "It is. But you don't say that out loud usually."
            "A pause."
            lena "It's easier up here."
        "\"Is it worth it?\"":
            $ lena_trust = min(100, lena_trust + 4)
            lena "Ask me on a good day and I'll say yes immediately."
            lena "Ask me at 3am after a shift like tonight and I'll tell you I don't know."
            lena "Both answers are true."
        "\"You're not just managing. You're very good at this.\"":
            $ lena_affection = min(100, lena_affection + 3)
            $ lena_trust = min(100, lena_trust + 2)
            "She glances at you. Something shifts in her expression."
            lena "That's... actually something I needed to hear tonight. Thank you."
    scene lena_rooftop_4 with dissolve
    show screen hud
    "She finishes whatever's in the cup. Sets it down. Looks at the city like she's still processing something she saw eight hours ago."
    lena "I chose this. I want to be clear about that. I'm not here by accident."
    lena "I just didn't account for what it costs."
    scene lena_rooftop_5 with dissolve
    show screen hud
    "She stands, smooths her jacket, picks up the cup."
    lena "Get some sleep. You're back in seven hours."
    "She heads for the door. Stops."
    lena "It helps. Having someone up here who gets it."
    scene hospital_rooftop_night with dissolve
    show screen hud
    "You take the stairs down and head for the metro."
    jump take_metro
