# Phase 61 — Cooking system.
# A real repeatable Culinary activity built on the Phase 60 roll engine.
# SKILL (skill_cook) sets capability; recipe DIFFICULTY sets the challenge;
# recipe MASTERY + kitchen EQUIPMENT + APPROACH modify odds; RNG sets quality.
# A poor roll never produces nothing — the meal is always at least edible.
#
# Cooking tier language (maps onto the 5 engine tiers):
#   critical_failure -> Poor      weak -> Decent     success -> Good
#   great -> Great                critical -> Exceptional

default recipe_mastery       = {}   # recipe_id -> mastery points 0..RECIPE_MASTERY_CAP
default _cooking_rare_seen    = []   # unique rare-outcome ids already granted
default known_recipe_variations = []
default _cook_assist          = None  # ("label", points) when cooking with a helper

init python:

    RECIPE_MASTERY_CAP = 100

    # difficulty is 1-10 (design scale); mapped to the engine's 1-100 space below.
    # hunger/energy are the BASE (Good-tier) restoration before quality scaling.
    RECIPES = {
        # ── Beginner (1-3) ────────────────────────────────────────
        "scrambled_eggs": {"name": "Scrambled Eggs", "min_cook": 0, "difficulty": 1,
                           "time": 0.5,  "cost": 4,  "hunger": 30, "energy": 0,  "xp": 3},
        "grilled_sandwich":{"name": "Grilled Sandwich","min_cook": 0, "difficulty": 1,
                           "time": 0.25, "cost": 4,  "hunger": 26, "energy": 0,  "xp": 3},
        "veggie_soup":    {"name": "Vegetable Soup", "min_cook": 1, "difficulty": 2,
                           "time": 0.75, "cost": 6,  "hunger": 38, "energy": 2,  "xp": 4},
        "pasta_primavera":{"name": "Pasta Primavera","min_cook": 1, "difficulty": 2,
                           "time": 1.0,  "cost": 8,  "hunger": 45, "energy": 2,  "xp": 5},
        "pancakes":       {"name": "Pancakes",       "min_cook": 1, "difficulty": 3,
                           "time": 0.75, "cost": 6,  "hunger": 40, "energy": 4,  "xp": 6},
        # ── Intermediate (4-6) ────────────────────────────────────
        "chicken_stirfry":{"name": "Chicken Stir-Fry","min_cook": 3, "difficulty": 4,
                           "time": 1.0,  "cost": 11, "hunger": 55, "energy": 8,  "xp": 9},
        "beef_tacos":     {"name": "Beef Tacos",     "min_cook": 4, "difficulty": 5,
                           "time": 1.0,  "cost": 13, "hunger": 58, "energy": 6,  "xp": 11},
        "baked_salmon":   {"name": "Baked Salmon",   "min_cook": 4, "difficulty": 5,
                           "time": 1.5,  "cost": 16, "hunger": 60, "energy": 8,  "xp": 12},
        "mushroom_risotto":{"name":"Mushroom Risotto","min_cook": 5, "difficulty": 6,
                           "time": 1.5,  "cost": 15, "hunger": 62, "energy": 6,  "xp": 14},
        # ── Advanced (7-8) ────────────────────────────────────────
        "sunday_roast":   {"name": "Sunday Roast",   "min_cook": 6, "difficulty": 7,
                           "time": 2.0,  "cost": 20, "hunger": 75, "energy": 12, "xp": 17},
        "chocolate_souffle":{"name":"Chocolate Soufflé","min_cook": 7,"difficulty": 8,
                           "time": 1.5,  "cost": 18, "hunger": 42, "energy": 6,  "xp": 19},
        "seared_duck":    {"name": "Seared Duck Breast","min_cook": 7,"difficulty": 8,
                           "time": 2.0,  "cost": 24, "hunger": 70, "energy": 10, "xp": 20},
        # ── High-tier (9-10) ──────────────────────────────────────
        "tasting_menu":   {"name": "Three-Course Tasting Menu","min_cook": 9,"difficulty": 9,
                           "time": 3.0,  "cost": 40, "hunger": 85, "energy": 15, "xp": 24},
        "signature_dish": {"name": "Signature Dish",  "min_cook": 9, "difficulty": 10,
                           "time": 3.0,  "cost": 45, "hunger": 90, "energy": 18, "xp": 26},
    }

    # design difficulty 1..10 -> engine difficulty (higher = harder).
    def _recipe_engine_difficulty(d):
        return 28 + d * 5   # d1=33 .. d5=53 .. d10=78

    def recipe_mastery_points(rid):
        return store.recipe_mastery.get(rid, 0)

    def recipe_mastery_mod(rid):
        # 0..100 points -> 0..12 roll points. Diminishing is in the GAIN curve.
        return int(min(12, recipe_mastery_points(rid) * 0.12))

    def recipe_time(rid, approach="normal"):
        r = RECIPES[rid]
        t = r["time"]
        # high mastery + good kitchen shave a little prep time.
        if recipe_mastery_points(rid) >= 60:
            t *= 0.9
        t *= (1.0 - float(equipment_modifier("kitchen", "cook_time")))
        if approach == "careful":
            t += 0.5
        return max(0.25, round(t * 4) / 4.0)   # snap to quarter-hours

    def recipe_energy_cost(rid, approach="normal"):
        r = RECIPES[rid]
        base = 6 + r["difficulty"]   # d1=7 .. d10=16
        if approach == "ambitious":
            base += 3
        return base

    def recipe_available(rid):
        return skill_val("cook") >= RECIPES[rid]["min_cook"]

    def _cooking_mods(rid, approach="normal"):
        """Modifier list (label,value) shared by preview and resolution."""
        mods = []
        m = recipe_mastery_mod(rid)
        if m:                                mods.append(("Recipe experience", m))
        k = equipment_modifier("kitchen", "cook_quality")
        if k:                                mods.append(("Kitchen gear", k))
        # Phase 62: cookware has a comfortable difficulty ceiling. Above it you
        # can still attempt the dish — it is just harder without the right pans.
        _ceiling = home_modifier("recipe_difficulty_max", room="kitchen") or 4
        if RECIPES[rid]["difficulty"] > _ceiling:
            mods.append(("Cookware not up to it", -4))
        if has_player_state("inspired"):     mods.append(("Inspired", +5))
        if has_player_state("focused"):      mods.append(("Focused", +3))
        if store.need_energy < 25:           mods.append(("Low energy", -5))
        if approach == "careful":            mods.append(("Careful approach", +6))
        elif approach == "ambitious":        mods.append(("Ambitious approach", -6))
        if store._cook_assist:               mods.append(store._cook_assist)
        return mods

    def cooking_chance(rid, approach="normal"):
        r = RECIPES[rid]
        return calculate_check_chance(
            "cook_" + rid, skill_val("cook"),
            _recipe_engine_difficulty(r["difficulty"]),
            _cooking_mods(rid, approach))

    # Cooking tier -> (hunger multiplier, xp multiplier, display label, color)
    _COOK_QUALITY = {
        "critical_failure": (0.60, 0.6, "Poor",        "#e05050"),
        "weak":             (0.85, 0.8, "Decent",      "#cc9040"),
        "success":          (1.00, 1.0, "Good",        "#7ccc60"),
        "great":            (1.12, 1.15,"Great",       "#5bcafa"),
        "critical":         (1.22, 1.3, "Exceptional", "#ffd66a"),
    }

    def cooking_quality_label(tier):
        return _COOK_QUALITY[tier][2]

    def _cook_xp_efficiency(rid):
        """XP scales down when a recipe is far below the player's skill (anti-farm),
        up modestly when it stretches them. §27."""
        gap = RECIPES[rid]["difficulty"] - skill_val("cook")
        if gap <= -4:  return 0.4
        if gap <= -2:  return 0.7
        if gap <= 2:   return 1.0
        return 1.25

    def _gain_recipe_mastery(rid, tier):
        pts = recipe_mastery_points(rid)
        # diminishing: big early, tiny once practiced. Poor/Decent still progress.
        base = {"critical_failure": 2, "weak": 3, "success": 5,
                "great": 6, "critical": 7}[tier]
        if pts >= 60:   base = max(1, base // 3)
        elif pts >= 30: base = max(1, base // 2)
        d = dict(store.recipe_mastery)
        d[rid] = min(RECIPE_MASTERY_CAP, pts + base)
        store.recipe_mastery = d

    def do_cook(rid, approach="normal"):
        """Resolve one cook. Charges cost/time/energy, always grants XP + a meal.
        Returns a result dict for the outcome screen."""
        r = RECIPES[rid]
        # cost is already gated by the caller, but charge through try_spend for safety
        _t = recipe_time(rid, approach)
        _e = recipe_energy_cost(rid, approach)
        spend_time(_t)
        store.need_energy = max(0, store.need_energy - _e)

        mods = _cooking_mods(rid, approach)
        result = roll_check("cook_" + rid, skill_val("cook"),
                            _recipe_engine_difficulty(r["difficulty"]),
                            mods, stable=False)
        tier = result["tier"]
        hmult, xmult, qlabel, qcolor = _COOK_QUALITY[tier]

        # ── meal effect (always at least edible) ──────────────────
        hunger_gain = int(round(r["hunger"] * hmult)) + int(home_upgrade_effect("meal_hunger"))
        store.need_hunger = min(100, store.need_hunger + hunger_gain)
        energy_gain = 0
        if r["energy"] > 0 and tier in ("success", "great", "critical"):
            energy_gain = int(round(r["energy"] * (hmult if tier != "success" else 1.0)))
            store.need_energy = min(100, store.need_energy + energy_gain)

        # ── guaranteed Culinary XP (DR-limited so easy recipes can't be farmed) ──
        base_xp = max(1, int(round(r["xp"] * xmult * _cook_xp_efficiency(rid))))
        eff_xp = gain_skill_practice("cook", base_xp, max(1, int(_t)))

        # ── recipe mastery ────────────────────────────────────────
        _gain_recipe_mastery(rid, tier)

        # ── rare outcomes (content, not cash) ─────────────────────
        rare = _cooking_rare_outcome(rid, tier, approach)

        # ── portfolio only for genuinely notable dishes ───────────
        if tier == "critical" and r["difficulty"] >= 7:
            record_game_event("cook_%s_day%d" % (rid, store.day), "project",
                "Cooked an exceptional %s" % r["name"], summary=True, journal=False,
                portfolio_domain="culinary",
                metadata={"recipe": rid, "tier": tier})

        return {
            "roll": result, "tier": tier, "qlabel": qlabel, "qcolor": qcolor,
            "hunger_gain": hunger_gain, "energy_gain": energy_gain,
            "xp": eff_xp, "rare": rare, "recipe": rid,
        }

    def _cooking_rare_outcome(rid, tier, approach):
        """One-shot content unlocks with duplicate protection. Ambitious pushes luck."""
        if tier not in ("great", "critical"):
            return None
        chance = 0.10 if tier == "great" else 0.22
        if approach == "ambitious":
            chance += 0.08
        if renpy.random.random() > chance:
            return None
        r = RECIPES[rid]
        pool = []
        # discover a variation (once per recipe)
        var_id = "var_" + rid
        if var_id not in store.known_recipe_variations:
            pool.append(("variation", var_id))
        # social-worthy photo for impressive dishes
        if r["difficulty"] >= 6:
            pool.append(("photo", "cookphoto_%s_day%d" % (rid, store.day)))
        # brief Inspired state
        pool.append(("inspired", "cookinsp_%s_day%d" % (rid, store.day)))
        # NPC asks for the recipe (flavour message)
        if r["difficulty"] >= 5:
            pool.append(("npc_recipe", "cookask_%s_day%d" % (rid, store.day)))
        pool = [p for p in pool if p[1] not in store._cooking_rare_seen]
        if not pool:
            return None
        kind, uid = renpy.random.choice(pool)
        store._cooking_rare_seen = list(store._cooking_rare_seen) + [uid]
        if kind == "variation":
            store.known_recipe_variations = list(store.known_recipe_variations) + [var_id]
            return ("variation", "You worked out a variation on %s. Odds nudge up next time." % r["name"])
        if kind == "inspired":
            add_player_state("inspired", uid)
            return ("inspired", "The cooking put you in a good headspace. (Inspired)")
        if kind == "photo":
            _post = "That %s came out plate-worthy. Worth a photo." % r["name"]
            store.social_feed_posts = [{"id": uid, "npc_id": "you", "text": _post, "day": store.day}] + list(store.social_feed_posts)
            return ("photo", "You snapped a photo of the %s for your feed." % r["name"])
        if kind == "npc_recipe":
            return ("npc_recipe", "A friend asked you for the %s recipe." % r["name"])
        return None


# ── Cooking list / preview screen ───────────────────────────────────────────────
# Returns a recipe_id to cook, or None to close.
screen cooking_list_scr():
    modal True
    zorder 210
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 720
        ysize 600
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 8
            text "COOK A MEAL" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            hbox:
                xalign 0.5
                spacing 16
                text ("Culinary Lv %d" % skill_val("cook")) font ACT_FONT size 13 color "#ff9f4d"
                text ("Balance: $%d" % money) font ACT_FONT size 13 color "#ffd66a"
            null height 4
            viewport:
                xfill True
                ysize 480
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    for _rid, _r in RECIPES.items():
                        $ _avail = recipe_available(_rid)
                        $ _ch = cooking_chance(_rid)
                        $ _gob = _ch["distribution"]["great"] + _ch["distribution"]["critical"]
                        frame:
                            xfill True
                            background "#1a2230"
                            padding (14, 10, 14, 10)
                            hbox:
                                spacing 12
                                xfill True
                                vbox:
                                    spacing 3
                                    xsize 420
                                    text _r["name"] font PROFILE_FONT size 14 color ("#cfe0f5" if _avail else "#5a6a7a")
                                    hbox:
                                        spacing 10
                                        text ("Diff %d" % _r["difficulty"]) font ACT_FONT size 11 color "#7090b0"
                                        text ("%sh" % recipe_time(_rid)) font ACT_FONT size 11 color "#7090b0"
                                        text ("$%d" % _r["cost"]) font ACT_FONT size 11 color "#7090b0"
                                        text ("Mastery %d" % recipe_mastery_points(_rid)) font ACT_FONT size 11 color "#8a6ac0"
                                    if _avail:
                                        hbox:
                                            spacing 5
                                            for _tid in ("critical_failure","weak","success","great","critical"):
                                                text ("%s %d%%" % (cooking_quality_label(_tid), _ch["distribution"][_tid])) font ACT_FONT size 10 color tier_color(_tid)
                                    else:
                                        text ("Requires Culinary %d (would-be Great+ %d%%)" % (_r["min_cook"], _gob)) font ACT_FONT size 11 color "#5a6a7a"
                                vbox:
                                    xalign 1.0
                                    spacing 4
                                    if _avail:
                                        $ _can_pay = money >= _r["cost"]
                                        button:
                                            action Return(_rid)
                                            sensitive _can_pay
                                            background "#1e3a5f"
                                            padding (12, 6)
                                            text ("Cook" if _can_pay else "No $") font ACT_FONT size 13 color ("#5bcafa" if _can_pay else "#4a6080") hover_color "#ffffff" xalign 0.5
                                    else:
                                        text "Locked" font ACT_FONT size 12 color "#4a6080" xalign 1.0
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8)
                text "Close" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"


# ── Cook flow (replaces the old flat location_home_cook) ────────────────────────
label do_cook_flow:
    # expects store._cook_rid set by caller (or via cooking_list_scr)
    call screen cooking_list_scr
    $ _cook_choice = _return
    if _cook_choice is None:
        return
    $ store._cook_rid = _cook_choice
    $ _crecipe = RECIPES[_cook_choice]
    $ _capproach = "normal"
    # Approach selection only for harder recipes (difficulty >= 5).
    if _crecipe["difficulty"] >= 5:
        call screen cooking_approach_scr(_cook_choice)
        if _return is None:
            jump do_cook_flow
        $ _capproach = _return
    # Charge ingredient cost up front (food essential — allowed in debt).
    if not try_spend(_crecipe["cost"], "food"):
        "You can't cover the ingredients for that."
        jump do_cook_flow
    scene cheap_home_cook
    show screen hud
    $ _cook_res = do_cook(_cook_choice, _capproach)
    call screen check_result_scr(_cook_res["roll"], title=("%s — %s" % (_crecipe["name"], _cook_res["qlabel"])), xtra_lines=_cook_meal_lines(_cook_res))
    if _cook_res["rare"] is not None:
        $ _rk, _rt = _cook_res["rare"]
        "[_rt]"
    jump do_cook_flow

# ── Cook together (home-visit integration, §6) ──────────────────────────────────
label cook_together_flow(npc_id):
    $ _ct_npc = npc_id
    $ store._cook_assist = npc_cook_assist(npc_id)
    if store._cook_assist:
        "[NPC_DATA[_ct_npc]['name']] rolls up their sleeves. \"Right — what are we making?\""
    else:
        "\"I'm no chef, but I'll chop whatever you point at.\""
    call do_cook_flow
    $ store._cook_assist = None
    $ _ct_rel = complete_cook_together(_ct_npc)
    if _ct_rel > 0:
        "You share the meal. Easy company. [NPC_DATA[_ct_npc]['name']] lingers a while."
    else:
        "Nice enough, though you've done this a lot lately."
    return

init python:
    def _cook_meal_lines(res):
        lines = ["+%d hunger" % res["hunger_gain"]]
        if res["energy_gain"] > 0:
            lines.append("+%d energy" % res["energy_gain"])
        lines.append("+%d Culinary XP" % res["xp"])
        return lines


# ── Approach selection screen ───────────────────────────────────────────────────
screen cooking_approach_scr(rid):
    modal True
    zorder 220
    add "#000000cc"
    $ _r = RECIPES[rid]
    frame:
        xalign 0.5 yalign 0.5
        xsize 560
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text ("%s — pick your approach" % _r["name"]) font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            null height 4
            for _appr, _albl, _adesc in [
                ("careful",   "Careful",   "More time, safer — fewer poor results."),
                ("normal",    "Standard",  "Balanced."),
                ("ambitious", "Ambitious", "Riskier odds, but a top result gives bonus mastery/luck."),
            ]:
                $ _ac = cooking_chance(rid, _appr)
                button:
                    action Return(_appr)
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10)
                    vbox:
                        spacing 3
                        hbox:
                            xfill True
                            text _albl font ACT_FONT size 15 color "#cfe0f5" yalign 0.5
                            text ("Great+ %d%%" % (_ac["distribution"]["great"] + _ac["distribution"]["critical"])) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                        text _adesc font ACT_FONT size 11 color "#7a9ab8"
                        hbox:
                            spacing 6
                            for _tid in ("critical_failure","weak","success","great","critical"):
                                text ("%s %d%%" % (cooking_quality_label(_tid), _ac["distribution"][_tid])) font ACT_FONT size 10 color tier_color(_tid)
            null height 4
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Phase 64: catering orders ───────────────────────────────────────────────────
# The generalist archetype ended day 90 on ~$1.3k because cooking, mechanics and
# fitness produced XP and enjoyment but zero disposable income. This is the
# cooking half of the fix: an occasional paid order, deliberately capped well
# under a career shift. Mechanics already had a paid path (the Phase 61 repair
# bench); fitness gets a paid class at the gym.

default catering_last_day = -99
default catering_completed = 0

init python:

    CATERING_ORDERS = [
        {"id": "bake_sale",    "label": "Tray of cakes for a school bake sale",
         "hours": 2.0, "cost": 14, "pay": 55,  "difficulty": 40, "min_cook": 3},
        {"id": "office_lunch", "label": "Lunch platter for a small office",
         "hours": 2.5, "cost": 22, "pay": 85,  "difficulty": 50, "min_cook": 5},
        {"id": "birthday",     "label": "Birthday dinner for eight",
         "hours": 3.0, "cost": 30, "pay": 115, "difficulty": 62, "min_cook": 7},
    ]
    CATERING_COOLDOWN = 3      # days between orders
    _CATERING_CHANCE  = 0.55   # ~1-2 orders a week once off cooldown

    # Failure never pays zero — a mediocre batch still gets delivered, at a
    # discount and with an unhappy customer (Phase 60/61 forward-progress rule).
    _CATERING_PAY_MULT = {"critical_failure": 0.50, "weak": 0.75,
                          "success": 1.00, "great": 1.15, "critical": 1.30}

    def catering_unlocked():
        """Needs the skill AND cookware above the baseline tier."""
        return (skill_val("cook") >= 3
                and equipment_modifier("kitchen", "cook_quality") > 0)

    def catering_offer():
        """Today's order, or None. Stable for the whole day — seeded on the day
        number, so it cannot be rerolled by leaving and re-entering the kitchen."""
        if not catering_unlocked():
            return None
        if store.day - store.catering_last_day < CATERING_COOLDOWN:
            return None
        import random as _r
        rng = _r.Random(store.day * 911 + 17)
        if rng.random() > _CATERING_CHANCE:
            return None
        open_orders = [o for o in CATERING_ORDERS if skill_val("cook") >= o["min_cook"]]
        return rng.choice(open_orders) if open_orders else None

    def _catering_mods():
        mods = []
        k = equipment_modifier("kitchen", "cook_quality")
        if k:                            mods.append(("Kitchen gear", k))
        if has_player_state("inspired"): mods.append(("Inspired", +5))
        if has_player_state("focused"):  mods.append(("Focused", +3))
        if store.need_energy < 25:       mods.append(("Low energy", -5))
        if store.catering_completed >= 3: mods.append(("Repeat customers", +4))
        return mods

    def catering_pay_range(order):
        """(min, max) net pay, shown before the player commits."""
        lo = int(round(order["pay"] * min(_CATERING_PAY_MULT.values()))) - order["cost"]
        hi = int(round(order["pay"] * max(_CATERING_PAY_MULT.values()))) - order["cost"]
        return lo, hi

    def catering_chance(order):
        return calculate_check_chance("catering_" + order["id"], skill_val("cook"),
                                      order["difficulty"], _catering_mods())

    def do_catering(order):
        """Charges time + energy, rolls quality, pays out. Returns a result dict.
        Ingredient cost is charged by the caller through try_spend."""
        spend_time(order["hours"])
        store.need_energy = max(0, store.need_energy - (8 + int(order["hours"] * 4)))
        result = roll_check("catering_" + order["id"], skill_val("cook"),
                            order["difficulty"], _catering_mods(), stable=False)
        tier = result["tier"]
        pay = int(round(order["pay"] * _CATERING_PAY_MULT[tier]))
        gain_money(pay, "catering")
        store.catering_last_day  = store.day
        store.catering_completed += 1
        xp = gain_skill_practice("cook", 6 + order["min_cook"], max(1, int(order["hours"])))
        record_game_event("catering_%s_day%d" % (order["id"], store.day),
                          "project", "Catering: " + order["label"],
                          summary=True, journal=False,
                          portfolio_domain=("culinary" if tier == "critical" else None),
                          metadata={"order": order["id"], "pay": pay, "tier": tier})
        return {"roll": result, "tier": tier, "pay": pay, "xp": xp,
                "net": pay - order["cost"], "qlabel": cooking_quality_label(tier)}

    def _catering_result_lines(res, order):
        return [("Paid", "$%d" % res["pay"]),
                ("Ingredients", "-$%d" % order["cost"]),
                ("Net", "$%d" % res["net"]),
                ("Culinary XP", "+%d" % res["xp"])]


label do_catering_flow:
    $ _cat_order = catering_offer()
    if _cat_order is None:
        "No orders waiting."
        return
    $ _cat_lo, _cat_hi = catering_pay_range(_cat_order)
    $ _cat_chance = catering_chance(_cat_order)["success_or_better"]
    $ _cat_lbl = _cat_order["label"]
    $ _cat_hrs = ("%g" % _cat_order["hours"])
    $ _cat_cost = _cat_order["cost"]
    "A message: [_cat_lbl]."
    menu:
        "Takes [_cat_hrs]h, $[_cat_cost] of ingredients. Net $[_cat_lo]-[_cat_hi]. [_cat_chance]% to hit the brief."
        "Take the order":
            pass
        "Turn it down":
            return
    if not try_spend(_cat_order["cost"], "food"):
        "You can't cover the ingredients for that."
        return
    scene cheap_home_cook
    show screen hud
    $ _cat_res = do_catering(_cat_order)
    call screen check_result_scr(_cat_res["roll"], title=("Catering — " + _cat_res["qlabel"]), xtra_lines=_catering_result_lines(_cat_res, _cat_order))
    if _cat_res["tier"] in ("critical_failure", "weak"):
        "They pay, but they don't look thrilled. You know exactly which part let it down."
    else:
        "They're delighted. Someone asks whether you do this regularly."
    return
