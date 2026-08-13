# Phase 62 — UI for the home/lifestyle item economy.
# Screens only; all logic lives in home_items.rpy.
#   home_shop_scr   — phone "Home" app: browse and buy by category
#   home_rooms_scr  — room-by-room overview, swap the active item per slot
#   home_wardrobe_scr — clothing categories
#   item_detail_scr — shared detail/confirm panel (buy or equip)

init python:

    _P62_CAT_COLORS = {"owned": "#7fd06a", "equipped": "#5bcafa", "afford": "#cfe0f5",
                       "poor": "#4a6080"}

    def _p62_item_row_color(item_id):
        if is_equipped(item_id):
            return _P62_CAT_COLORS["equipped"]
        if owns_item(item_id):
            return _P62_CAT_COLORS["owned"]
        return _P62_CAT_COLORS["afford"] if can_buy_item(item_id) else _P62_CAT_COLORS["poor"]

    def _p62_item_tag(item_id):
        if is_equipped(item_id):
            return ("Equipped", "#5bcafa")
        if owns_item(item_id):
            return ("Owned", "#7fd06a")
        return ("$%d" % ITEM_CATALOG[item_id]["price_new"],
                "#ffd66a" if can_buy_item(item_id) else "#4a6080")


default _p62_shop_cat = "bedroom"
default _p62_item = None
default _p62_name = ""
default _p62_equip_after = False


# ── Phone app: Home & Equipment shop ───────────────────────────────────────────
screen home_shop_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Home & Equipment" font PROFILE_FONT size 20 color "#ffffff" xalign 0.5
            text ("$%d  ·  %d affordable" % (money, affordable_item_count())) font ACT_FONT size 12 color "#ffd66a" xalign 0.5
            null height 6

            # category tabs
            vpgrid:
                cols 4
                spacing 4
                xalign 0.5
                allow_underfull True
                for _c, _clbl in SHOP_CATEGORIES:
                    textbutton _clbl:
                        action SetVariable("_p62_shop_cat", _c)
                        xsize 82
                        background (Frame("images/ui/act_bar_hover_clean.png", 8, 8, 8, 8) if _p62_shop_cat == _c else None)
                        xpadding 2 ypadding 3
                        text_font ACT_FONT text_size 11
                        text_color ("#ffffff" if _p62_shop_cat == _c else "#7a9ab8")
                        text_hover_color "#ffffff"
                        text_xalign 0.5
            null height 6

            viewport:
                xfill True
                ysize 520
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    for _iid in shop_items(_p62_shop_cat):
                        $ _id = ITEM_CATALOG[_iid]
                        $ _tag, _tagcol = _p62_item_tag(_iid)
                        button:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                            padding (10, 7, 10, 7)
                            action Function(renpy.call_in_new_context, "p62_item_ctx", _iid)
                            vbox:
                                spacing 2
                                xfill True
                                hbox:
                                    xfill True
                                    text _id["label"] font PROFILE_FONT size 13 color _p62_item_row_color(_iid) yalign 0.5
                                    text _tag font PROFILE_FONT size 12 color _tagcol yalign 0.5 xalign 1.0
                                text _id["description"] font ACT_FONT size 10 color "#7a9ab8"
            null height 4
            if savings_target_text():
                text savings_target_text() font ACT_FONT size 11 color "#ffd66a" xalign 0.5
            null height 4
            textbutton "Your place — room by room" action Show("home_rooms_scr") xalign 0.5 text_font ACT_FONT text_size 13 text_color "#5bcafa" text_hover_color "#ffffff"
            null height 2
            textbutton "Back" action [Hide("home_shop_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 19 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Item detail / confirm ──────────────────────────────────────────────────────
# Returns one of: ("buy", equip_after) / ("equip",) / ("save",) / None
screen item_detail_scr(item_id):
    modal True
    zorder 220
    add "#000000cc"
    $ _d = ITEM_CATALOG[item_id]
    $ _owned = owns_item(item_id)
    $ _equipped = is_equipped(item_id)
    $ _slotted = _d["slot"] is not None
    $ _delta = equip_delta(item_id)
    frame:
        xalign 0.5 yalign 0.5
        xsize 600
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 7
            text _d["label"] font PROFILE_FONT size 19 color "#cfe0f5" xalign 0.5
            text _d["description"] font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            null height 2

            if _slotted:
                $ _room, _slot = item_room_slot(item_id)
                $ _roomlbl = "Wardrobe" if _room == "wardrobe" else HOME_ROOM_LABELS.get(_room, _room)
                $ _slotlbl = SLOT_LABELS.get(_slot, _slot.replace("_", " ").title())
                hbox:
                    xfill True
                    text ("%s — %s" % (_roomlbl, _slotlbl)) font ACT_FONT size 11 color "#5bcafa" yalign 0.5
                    text ("Currently: %s" % current_slot_occupant_label(item_id)) font ACT_FONT size 11 color "#7a9ab8" yalign 0.5 xalign 1.0
            else:
                text "Lifestyle item — no slot. You own it because you want it." font ACT_FONT size 11 color "#5bcafa"

            null height 4
            if _delta:
                text ("Change if equipped:" if not _equipped else "Active bonuses:") font ACT_FONT size 11 color "#9fb6d6"
                for _dl, _dv in _delta:
                    hbox:
                        xfill True
                        text ("  " + _dl) font ACT_FONT size 11 color "#7a9ab8" yalign 0.5
                        text _dv font ACT_FONT size 11 color "#ffd66a" yalign 0.5 xalign 1.0
            elif item_modifier_lines(item_id):
                text "Current bonuses:" font ACT_FONT size 11 color "#9fb6d6"
                for _dl, _dv in item_modifier_lines(item_id):
                    hbox:
                        xfill True
                        text ("  " + _dl) font ACT_FONT size 11 color "#7a9ab8" yalign 0.5
                        text _dv font ACT_FONT size 11 color "#ffd66a" yalign 0.5 xalign 1.0
            else:
                text "No mechanical bonus. It just makes the place better." font ACT_FONT size 11 color "#4a6080"

            if _d["unlocks"]:
                text ("Unlocks: " + ", ".join(u.replace("_", " ") for u in _d["unlocks"])) font ACT_FONT size 10 color "#7fd06a"
            if _owned:
                text ("Condition: %s" % item_condition(item_id)) font ACT_FONT size 10 color "#7a9ab8"

            null height 8
            if not _owned:
                if _d["shop_available"]:
                    button:
                        action Return(("buy", True))
                        sensitive can_buy_item(item_id)
                        xfill True
                        background "#1a2a3a"
                        hover_background "#1e3a5f"
                        padding (14, 8)
                        text ("Buy for $%d and use it now" % _d["price_new"]) font ACT_FONT size 14 color ("#cfe0f5" if can_buy_item(item_id) else "#4a6080")
                    if _slotted:
                        button:
                            action Return(("buy", False))
                            sensitive can_buy_item(item_id)
                            xfill True
                            background "#1a2a3a"
                            hover_background "#1e3a5f"
                            padding (14, 8)
                            text ("Buy for $%d, keep in storage" % _d["price_new"]) font ACT_FONT size 13 color ("#9fb6d6" if can_buy_item(item_id) else "#4a6080")
                    if not can_buy_item(item_id):
                        text ("You have $%d. You need $%d more." % (money, max(0, _d["price_new"] - money))) font ACT_FONT size 11 color "#e07a6a" xalign 0.5
                    if _d["price_new"] >= 800:
                        button:
                            action Return(("save",))
                            xfill True
                            background "#1a2a3a"
                            hover_background "#1e3a5f"
                            padding (14, 7)
                            text ("Stop saving for this" if savings_target == item_id else "Set as savings goal") font ACT_FONT size 12 color "#ffd66a"
                if _d["available_used"]:
                    text ("Sometimes turns up second-hand around $%d." % _d["price_used"]) font ACT_FONT size 10 color "#7a9ab8" xalign 0.5
            elif _slotted and not _equipped:
                button:
                    action Return(("equip",))
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 8)
                    text "Use this one" font ACT_FONT size 14 color "#cfe0f5"
            elif _equipped:
                text "In use." font ACT_FONT size 13 color "#5bcafa" xalign 0.5
            else:
                text "Owned." font ACT_FONT size 13 color "#7fd06a" xalign 0.5

            null height 6
            button action Return(None) xalign 0.5 background "#1e3a5f" padding (18, 6):
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# Runs in a new context so it can be launched from the phone or an activity menu.
label p62_item_ctx(item_id):
    $ _p62_item = item_id
    call screen item_detail_scr(_p62_item)
    $ _p62_choice = _return
    if _p62_choice is None:
        return
    if _p62_choice[0] == "save":
        $ _set_savings_target(_p62_item)
        return
    $ _p62_name = ITEM_CATALOG[_p62_item]["label"]
    if _p62_choice[0] == "equip":
        $ equip_item(_p62_item)
        "You set up the [_p62_name]."
        return
    # buy
    $ _p62_equip_after = _p62_choice[1]
    if buy_item(_p62_item):
        if _p62_equip_after and ITEM_CATALOG[_p62_item]["slot"]:
            $ equip_item(_p62_item)
            "You buy the [_p62_name] and set it up."
        else:
            "You buy the [_p62_name]."
    else:
        "You can't cover that right now."
    return


# ── Room-by-room overview ──────────────────────────────────────────────────────
screen home_rooms_scr():
    modal True
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 780
        ysize 640
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 16, 22, 16)
        vbox:
            spacing 8
            text "Your Place" font PROFILE_FONT size 23 color "#ffffff" xalign 0.5
            text home_visual_text() font ACT_FONT size 13 color "#9fb6d6" xalign 0.5
            hbox:
                spacing 18
                xalign 0.5
                text ("Look: %d/4" % home_visual_tier()) font ACT_FONT size 11 color "#7a9ab8"
                text ("Sociable: %d/30" % home_social_quality()) font ACT_FONT size 11 color "#7a9ab8"
                text ("Sleep: +%d%%" % int(round(sleep_recovery_modifier() * 100))) font ACT_FONT size 11 color "#7a9ab8"
            null height 2
            viewport:
                xfill True
                ysize 470
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    for _room, _rlbl, _slots in HOME_ROOMS:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (12, 8, 12, 8)
                            vbox:
                                spacing 3
                                text _rlbl font PROFILE_FONT size 14 color "#5bcafa"
                                for _slot in _slots:
                                    $ _cur = equipped_in(_room, _slot)
                                    $ _alts = [i for i in ITEM_CATALOG
                                               if ITEM_CATALOG[i]["slot"] == _slot
                                               and _room_for_item(i) == _room
                                               and owns_item(i) and i != _cur]
                                    hbox:
                                        xfill True
                                        text SLOT_LABELS.get(_slot, _slot) font ACT_FONT size 11 color "#7a9ab8" yalign 0.5 xsize 150
                                        if _cur:
                                            button:
                                                action Function(renpy.call_in_new_context, "p62_item_ctx", _cur)
                                                background None
                                                hover_background None
                                                yalign 0.5
                                                text ITEM_CATALOG[_cur]["label"] font ACT_FONT size 12 color "#cfe0f5" hover_color "#ffffff"
                                        else:
                                            text "—" font ACT_FONT size 12 color "#4a6080" yalign 0.5
                                        if _alts:
                                            hbox:
                                                xalign 1.0
                                                spacing 6
                                                yalign 0.5
                                                for _alt in _alts:
                                                    textbutton ("→ " + ITEM_CATALOG[_alt]["label"]):
                                                        action [Function(_equip_item_wrapper, _alt), renpy.restart_interaction]
                                                        xpadding 6 ypadding 2
                                                        background Frame("images/ui/act_bar_idle.png", 8, 8, 8, 8)
                                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 8, 8, 8, 8)
                                                        text_font ACT_FONT text_size 10 text_color "#7fd06a" text_hover_color "#ffffff"
                    # lifestyle shelf
                    $ _life = [i for i, d in ITEM_CATALOG.items() if d["category"] == "lifestyle" and owns_item(i)]
                    frame:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Things You Own" font PROFILE_FONT size 14 color "#5bcafa"
                            if _life:
                                for _l in _life:
                                    text ("· " + ITEM_CATALOG[_l]["label"]) font ACT_FONT size 12 color "#cfe0f5"
                            else:
                                text "Nothing yet. Nothing here has to earn its keep." font ACT_FONT size 11 color "#4a6080"
                    # strings state
                    if own_guitar or equipped_in("music_corner", "instrument"):
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (12, 8, 12, 8)
                            vbox:
                                spacing 3
                                text "Guitar Strings" font PROFILE_FONT size 14 color "#5bcafa"
                                text strings_state_text() font ACT_FONT size 12 color "#cfe0f5"
            hbox:
                xalign 0.5
                spacing 20
                textbutton "Wardrobe" action Show("home_wardrobe_scr") text_font ACT_FONT text_size 17 text_color "#5bcafa" text_hover_color "#ffffff"
                textbutton "Close" action Return() text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Wardrobe ───────────────────────────────────────────────────────────────────
screen home_wardrobe_scr():
    modal True
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 700
        ysize 560
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 16, 22, 16)
        vbox:
            spacing 8
            text "Wardrobe" font PROFILE_FONT size 23 color "#ffffff" xalign 0.5
            text "Clothes don't wear out and never need washing. Pick what fits the day." font ACT_FONT size 11 color "#7a9ab8" xalign 0.5
            null height 2
            viewport:
                xfill True
                ysize 420
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 7
                    xfill True
                    for _wc, _wlbl in WARDROBE_CATEGORIES:
                        $ _cur = wardrobe_equipped_in(_wc)
                        $ _opts = [i for i, d in ITEM_CATALOG.items()
                                   if d["category"] == "wardrobe" and d["slot"] == _wc and owns_item(i)]
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (12, 8, 12, 8)
                            vbox:
                                spacing 3
                                hbox:
                                    xfill True
                                    text _wlbl font PROFILE_FONT size 13 color "#5bcafa" yalign 0.5
                                    text (ITEM_CATALOG[_cur]["label"] if _cur else "Nothing owned") font ACT_FONT size 12 color ("#cfe0f5" if _cur else "#4a6080") yalign 0.5 xalign 1.0
                                if _opts:
                                    hbox:
                                        spacing 6
                                        for _o in _opts:
                                            textbutton ITEM_CATALOG[_o]["label"]:
                                                action [Function(_equip_item_wrapper, _o), renpy.restart_interaction]
                                                sensitive (_o != _cur)
                                                xpadding 7 ypadding 3
                                                background Frame("images/ui/act_bar_idle.png", 8, 8, 8, 8)
                                                hover_background Frame("images/ui/act_bar_hover_clean.png", 8, 8, 8, 8)
                                                text_font ACT_FONT text_size 10
                                                text_color ("#5bcafa" if _o == _cur else "#7fd06a")
                                                text_hover_color "#ffffff"
                                else:
                                    text "Buy something in this category from the Home app." font ACT_FONT size 10 color "#4a6080"
            text ("Everyday confidence: +%d" % wardrobe_confidence()) font ACT_FONT size 12 color "#ffd66a" xalign 0.5
            textbutton "Close" action [Hide("home_wardrobe_scr")] xalign 0.5 text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Debug (Phase 62) ───────────────────────────────────────────────────────────
init python:
    def _dbg_p62_grant(item_id):
        """Function() wrapper — returns None."""
        grant_item(item_id, "Excellent")

    def _dbg_p62_grant_all_in(category):
        """Function() wrapper — returns None."""
        for i, d in ITEM_CATALOG.items():
            if d["category"] == category and d["price_new"] > 0:
                grant_item(i, "Excellent")

    def _dbg_p62_set_strings(days_ago):
        """Function() wrapper — returns None."""
        store.guitar_strings_last_refreshed = store.day - days_ago

    def _dbg_p62_reset_morning():
        """Function() wrapper — returns None."""
        store._morning_item_used = None

    def _dbg_p62_set_target(item_id):
        """Function() wrapper — returns None."""
        store.savings_target = None if item_id == "None" else item_id

    def _dbg_p62_clear():
        """Function() wrapper — returns None. Wipes Phase 62 ownership/slots."""
        store.owned_equipment = [i for i in store.owned_equipment if i not in ITEM_CATALOG]
        store.home_slots = {}
        store.wardrobe_equipped = {}
        store.savings_target = None
        store.guitar_strings_last_refreshed = -999

    def _dbg_p62_econ():
        """Economy audit numbers, computed live from the catalog."""
        bands = [(0, 40), (40, 150), (150, 400), (400, 900), (900, 2000), (2000, 5000)]
        out = []
        for lo, hi in bands:
            n = sum(1 for d in ITEM_CATALOG.values()
                    if d["shop_available"] and lo <= d["price_new"] < hi and d["price_new"] > 0)
            out.append(("$%d-%d" % (lo, hi), n))
        return out


default _p62_dbg_cat = "bedroom"

screen debug_p62_scr():
    modal True
    zorder 250
    add "#000000dd"
    frame:
        xalign 0.5 yalign 0.5
        xsize 1180
        ysize 900
        background "#0d1219f8"
        padding (20, 16, 20, 16)
        vbox:
            spacing 6
            text "Phase 62 — Home / Items / Wardrobe" font PROFILE_FONT size 20 color "#ffd66a" xalign 0.5
            hbox:
                spacing 26
                xalign 0.5
                text ("visual_tier: %d" % home_visual_tier()) font ACT_FONT size 13 color "#7fd06a"
                text ("home_social_quality: %d" % home_social_quality()) font ACT_FONT size 13 color "#7fd06a"
                text ("sleep_recovery: +%.0f%%" % (sleep_recovery_modifier() * 100)) font ACT_FONT size 13 color "#7fd06a"
                text ("workspace_q: %d" % workspace_quality()) font ACT_FONT size 13 color "#7fd06a"
                text ("strings: %+d" % strings_modifier()) font ACT_FONT size 13 color "#7fd06a"
            null height 2
            hbox:
                spacing 12
                xfill True
                # left: live totals + tools
                vbox:
                    xsize 560
                    spacing 5
                    text "Live category totals (legacy + home merged)" font PROFILE_FONT size 13 color "#5bcafa"
                    for _c, _clbl in _EQUIP_CATEGORIES:
                        $ _summ = equipment_effect_summary(_c)
                        text ("%s: %s" % (_clbl, ", ".join("%s %s" % (a, b) for a, b in _summ) if _summ else "—")) font ACT_FONT size 11 color "#cfe0f5"
                    null height 4
                    text "Equipped by room" font PROFILE_FONT size 13 color "#5bcafa"
                    viewport:
                        ysize 230
                        mousewheel True
                        scrollbars "vertical"
                        vbox:
                            spacing 1
                            for _room, _rlbl, _slots in HOME_ROOMS:
                                for _slot in _slots:
                                    $ _cur = equipped_in(_room, _slot)
                                    text ("%s/%s: %s" % (_rlbl, _slot, ITEM_CATALOG[_cur]["label"] if _cur else "—")) font ACT_FONT size 10 color ("#cfe0f5" if _cur else "#4a6080")
                            for _wc, _wlbl in WARDROBE_CATEGORIES:
                                $ _cur = wardrobe_equipped_in(_wc)
                                text ("wardrobe/%s: %s" % (_wc, ITEM_CATALOG[_cur]["label"] if _cur else "—")) font ACT_FONT size 10 color ("#cfe0f5" if _cur else "#4a6080")
                    null height 4
                    text "Price bands (shop items)" font PROFILE_FONT size 13 color "#5bcafa"
                    for _bl, _bn in _dbg_p62_econ():
                        text ("%s: %d items" % (_bl, _bn)) font ACT_FONT size 10 color "#cfe0f5"
                    null height 4
                    hbox:
                        spacing 8
                        textbutton "strings fresh" action [Function(_dbg_p62_set_strings, 0), renpy.restart_interaction] text_size 11 text_color "#5bcafa"
                        textbutton "strings 8d old" action [Function(_dbg_p62_set_strings, 8), renpy.restart_interaction] text_size 11 text_color "#5bcafa"
                        textbutton "reset morning" action [Function(_dbg_p62_reset_morning), renpy.restart_interaction] text_size 11 text_color "#5bcafa"
                        textbutton "wipe P62" action [Function(_dbg_p62_clear), renpy.restart_interaction] text_size 11 text_color "#e07a6a"
                    hbox:
                        spacing 8
                        text "savings target:" font ACT_FONT size 11 color "#7a9ab8" yalign 0.5
                        for _st in ("large_tv", "desktop_workstation", "pro_workstation", "None"):
                            textbutton _st:
                                action [Function(_dbg_p62_set_target, _st), renpy.restart_interaction]
                                text_font ACT_FONT text_size 10
                                text_color ("#ffd66a" if savings_target == _st or (_st == "None" and savings_target is None) else "#7a9ab8")

                # right: catalog browser / granting
                vbox:
                    xsize 540
                    spacing 4
                    text ("Catalog (%d items) — click to grant" % len(ITEM_CATALOG)) font PROFILE_FONT size 13 color "#5bcafa"
                    hbox:
                        spacing 3
                        box_wrap True
                        for _c, _clbl in SHOP_CATEGORIES:
                            textbutton _clbl:
                                action SetVariable("_p62_dbg_cat", _c)
                                xpadding 5 ypadding 2
                                text_font ACT_FONT text_size 10
                                text_color ("#ffffff" if _p62_dbg_cat == _c else "#7a9ab8")
                    textbutton ("grant all in " + _p62_dbg_cat):
                        action [Function(_dbg_p62_grant_all_in, _p62_dbg_cat), renpy.restart_interaction]
                        text_size 11 text_color "#7fd06a"
                    viewport:
                        ysize 620
                        mousewheel True
                        scrollbars "vertical"
                        vbox:
                            spacing 1
                            for _iid in shop_items(_p62_dbg_cat):
                                $ _d = ITEM_CATALOG[_iid]
                                hbox:
                                    xfill True
                                    textbutton ("%s $%d" % (_d["label"], _d["price_new"])):
                                        action [Function(_dbg_p62_grant, _iid), renpy.restart_interaction]
                                        text_font ACT_FONT text_size 10
                                        text_color ("#7fd06a" if owns_item(_iid) else "#cfe0f5")
                                        text_hover_color "#ffffff"
                                        xpadding 0 ypadding 0
                                    text (", ".join("%s %s" % (a, b) for a, b in item_modifier_lines(_iid)) or "cosmetic") font ACT_FONT size 9 color "#7a9ab8" xalign 1.0 yalign 0.5
            null height 4
            textbutton "Back" action [Hide("debug_p62_scr"), Show("debug_menu")] xalign 0.5 text_font ACT_FONT text_size 16 text_color "#9fb6d6" text_hover_color "#ffffff"
