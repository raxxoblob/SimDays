# Phase 61 — developer inspection tools. All Function() wrappers return None so
# no debug action can end an unrelated interaction.

init python:

    def _dbg_p61_set_skill(key, lvl):
        setattr(store, "skill_" + key, lvl)
        d = dict(store.skill_exp); d[key] = 0; store.skill_exp = d
        renpy.notify("%s set to Lv %d" % (key, lvl))

    def _dbg_p61_grant(item_id, cond="Good"):
        grant_equipment(item_id, cond)
        renpy.notify("Granted %s (%s)" % (item_id, cond))

    def _dbg_p61_regen_boards():
        store.market_listings = []
        store.market_listings_period = -1
        store.mech_jobs = []
        store.mech_jobs_gen_period = -1
        refresh_market_listings()
        refresh_mech_jobs()
        renpy.notify("Boards regenerated (%d listings, %d jobs)"
                     % (len(store.market_listings), len(store.mech_jobs)))

    def _dbg_p61_master_recipe():
        d = dict(store.recipe_mastery)
        for rid in RECIPES:
            d[rid] = RECIPE_MASTERY_CAP
        store.recipe_mastery = d
        renpy.notify("All recipes maxed mastery")

    def _dbg_p61_gen_city_challenges():
        # advance to a fresh week's schedule containing challenges
        generate_city_events_for_week(store.day // 7)
        renpy.notify("City events (incl. challenges) generated")


screen debug_p61_scr():
    modal True
    zorder 250
    add "#0d1014fa"
    frame:
        xalign 0.5 yalign 0.5
        xsize 1000
        ysize 760
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 8
            text "PHASE 61 INSPECTOR" font PROFILE_FONT size 20 color "#7fd06a" xalign 0.5
            hbox:
                spacing 8
                textbutton "cook=5" action Function(_dbg_p61_set_skill, "cook", 5) text_size 14
                textbutton "cook=9" action Function(_dbg_p61_set_skill, "cook", 9) text_size 14
                textbutton "mech=5" action Function(_dbg_p61_set_skill, "mech", 5) text_size 14
                textbutton "mech=8" action Function(_dbg_p61_set_skill, "mech", 8) text_size 14
                textbutton "biz=6" action Function(_dbg_p61_set_skill, "biz", 6) text_size 14
                textbutton "Master recipes" action Function(_dbg_p61_master_recipe) text_size 14 text_color "#ffd66a"
            hbox:
                spacing 8
                textbutton "Grant Pro Tools" action Function(_dbg_p61_grant, "pro_toolkit", "Good") text_size 14
                textbutton "Grant Chef Kit" action Function(_dbg_p61_grant, "chef_kit", "Used") text_size 14
                textbutton "Grant Q.Guitar" action Function(_dbg_p61_grant, "quality_acoustic", "Poor") text_size 14
                textbutton "Regen boards" action Function(_dbg_p61_regen_boards) text_size 14 text_color "#ffd66a"
                textbutton "Gen city events" action Function(_dbg_p61_gen_city_challenges) text_size 14
            null height 4
            viewport:
                xfill True
                ysize 590
                mousewheel True
                scrollbars "vertical"
                hbox:
                    spacing 20
                    # ── left column ──
                    vbox:
                        spacing 4
                        xsize 470
                        text "EQUIPPED + MODIFIERS" font PROFILE_FONT size 14 color "#5bcafa"
                        for _cat, _clbl in _EQUIP_CATEGORIES:
                            $ _eq = equipped_item(_cat)
                            if _eq:
                                text ("%s: %s [%s]" % (_clbl, EQUIPMENT_DEFS[_eq]["name"], equipment_condition_of(_eq))) font ACT_FONT size 12 color "#cfe0f5"
                                for _lbl, _vs in equipment_effect_summary(_cat):
                                    text ("   %s %s" % (_lbl, _vs)) font ACT_FONT size 11 color "#7fd06a"
                            else:
                                text ("%s: none" % _clbl) font ACT_FONT size 12 color "#4a6080"
                        null height 6
                        text "RECIPE MASTERY / ODDS" font PROFILE_FONT size 14 color "#5bcafa"
                        for _rid, _r in RECIPES.items():
                            $ _rc = cooking_chance(_rid)
                            $ _gob = _rc["distribution"]["great"] + _rc["distribution"]["critical"]
                            text ("%s d%d m%d  Great+ %d%%%s" % (_r["name"], _r["difficulty"], recipe_mastery_points(_rid), _gob, "" if recipe_available(_rid) else "  (LOCKED)")) font ACT_FONT size 11 color ("#cfe0f5" if recipe_available(_rid) else "#5a6a7a")
                    # ── right column ──
                    vbox:
                        spacing 4
                        xsize 470
                        text ("MARKET LISTINGS (seed period %d)" % (day // MARKET_ROTATE)) font PROFILE_FONT size 14 color "#5bcafa"
                        for _l in market_listings:
                            text ("%s $%d %s exp d%d%s" % (_l["item_id"], _l["asking"], _l["condition"], _l["expire_day"] + 1, "  PURCHASED" if _l.get("purchased") else "")) font ACT_FONT size 11 color "#cfe0f5"
                        null height 4
                        text "NEG ATTEMPTS" font PROFILE_FONT size 12 color "#7a9ab8"
                        for _k, _v in _market_neg_attempts.items():
                            text ("%s -> %d" % (_k, _v)) font ACT_FONT size 10 color "#7a9ab8"
                        null height 6
                        text "MECH JOBS" font PROFILE_FONT size 14 color "#5bcafa"
                        for _j in mech_jobs:
                            $ _jc = mech_repair_chance(_j)
                            text ("%s d%d rep %d%% pays $%d%s" % (_j["name"], _j["difficulty"], _jc["success_or_better"], _j["reward"], "  DONE" if _j.get("done") else "")) font ACT_FONT size 11 color "#cfe0f5"
                        null height 6
                        text "CITY CHALLENGES SCHEDULED" font PROFILE_FONT size 14 color "#5bcafa"
                        for _e in city_event_schedule:
                            if city_challenge_spec(_e):
                                $ _ec = city_challenge_chance(_e)
                                text ("%s d%d place-any %d%% [%s]" % (_e["title"], _e["day"] + 1, _ec["success_or_better"], _e["status"])) font ACT_FONT size 11 color "#cfe0f5"
                        null height 6
                        text "WORLD CHALLENGE ODDS" font PROFILE_FONT size 14 color "#5bcafa"
                        for _wid in ("signature_dish_master", "restore_showpiece", "hard_technical_challenge"):
                            if world_challenge_visible(_wid):
                                $ _wc = world_challenge_chance(_wid)
                                text ("%s: %d%%" % (WORLD_CHALLENGES[_wid]["label"], _wc["success_or_better"])) font ACT_FONT size 11 color "#cfe0f5"
                            else:
                                text ("%s: (locked)" % WORLD_CHALLENGES[_wid]["label"]) font ACT_FONT size 11 color "#5a6a7a"
            textbutton "Close" action [Hide("debug_p61_scr"), Show("debug_menu")] xalign 0.5 text_font ACT_FONT text_size 18 text_color "#9fb6d6" text_hover_color "#ffffff"
