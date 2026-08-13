# Phase 61 — Second-hand marketplace (phone app).
# A controlled, deterministically-rotating listing board. Listings are STABLE
# across reload (seeded per period; the screen never rerolls). Opening the app
# does not advance RNG.
#
# ANTI-ARBITRAGE: the player CANNOT sell items back. The marketplace is a money
# SINK (buy gear / opportunities), not a source. With no resale path, buy-repair-
# sell arbitrage is structurally impossible — expected profit per hour = $0.
# Repaired items only improve the player's own equipment (see mechanics), they
# are never re-listed. (ponytail: no resale system by design; if a sell feature
# is ever added, it must price below purchase and respect §16.)

default market_listings          = []
default market_listings_period   = -1
default _market_neg_attempts     = {}   # (listing_id, discount) -> committed attempts

init python:

    MARKET_ROTATE = 3   # days per rotation

    # value = fair mid-price at "Good" condition.
    MARKET_ITEM_POOL = {
        "used_acoustic":    {"cat": "music",    "name": "Used Acoustic Guitar",   "value": 300, "grant": "equip"},
        "quality_acoustic": {"cat": "music",    "name": "Quality Acoustic Guitar", "value": 520, "grant": "equip", "rare": True},
        "used_desktop":     {"cat": "computer", "name": "Refurbished Desktop",     "value": 340, "grant": "equip"},
        "dev_workstation":  {"cat": "computer", "name": "Developer Workstation",   "value": 760, "grant": "equip", "rare": True},
        "used_cookware":    {"cat": "kitchen",  "name": "Cast-Iron Cookware Set",  "value": 150, "grant": "equip"},
        "chef_kit":         {"cat": "kitchen",  "name": "Chef Knife & Pan Set",    "value": 300, "grant": "equip", "rare": True},
        "used_toolkit":     {"cat": "tools",    "name": "Used Tool Kit",           "value": 140, "grant": "equip"},
        "pro_toolkit":      {"cat": "tools",    "name": "Pro Tool Kit",            "value": 320, "grant": "equip", "rare": True},
        # legacy capability items at second-hand prices
        "flag_guitar":      {"cat": "music",    "name": "Beginner Guitar",         "value": 110, "grant": "flag", "flag": "own_guitar"},
        "flag_coffee":      {"cat": "home",     "name": "Coffee Machine",          "value": 110, "grant": "flag", "flag": "own_coffee_machine"},
        "flag_kitchen_set": {"cat": "kitchen",  "name": "Kitchen Starter Set",     "value": 150, "grant": "flag", "flag": "own_kitchen_set"},
        "flag_bed":         {"cat": "home",     "name": "Quality Bed Frame",       "value": 300, "grant": "flag", "flag": "own_bed"},
        "flag_sketchbook":  {"cat": "hobby",    "name": "Sketchbook & Supplies",   "value": 30,  "grant": "flag", "flag": "own_sketchbook"},
        "flag_book":        {"cat": "hobby",    "name": "Reference Book",          "value": 25,  "grant": "flag", "flag": "own_book"},
    }

    # ── Phase 62: the catalog feeds the same pool ─────────────────────────────
    # Every ITEM_CATALOG entry with available_used=True becomes a listing
    # candidate. grant "item" routes through grant_item() (which writes to the
    # same owned_equipment inventory), so condition scaling applies identically.
    # The legacy tiered guitars/computers/cookware/tools above are superseded by
    # named catalog items and are dropped from rotation to avoid near-duplicates.
    _MARKET_LEGACY_RETIRED = {"used_acoustic", "quality_acoustic", "used_desktop",
                              "dev_workstation", "used_cookware", "chef_kit",
                              "used_toolkit", "pro_toolkit"}

    _MARKET_CAT_FOR_ITEM = {
        "workspace": "workspace", "bedroom": "bedroom", "kitchen": "kitchen",
        "music": "music", "workshop": "tools", "living_room": "living_room",
        "lifestyle": "lifestyle", "wardrobe": "wardrobe",
    }
    MARKET_CATEGORY_LABELS = {
        "workspace": "Workspace", "bedroom": "Bedroom", "kitchen": "Kitchen",
        "music": "Music", "tools": "Tools", "living_room": "Living Room",
        "lifestyle": "Lifestyle", "wardrobe": "Wardrobe", "home": "Home",
        "hobby": "Hobby", "computer": "Computer",
    }

    def _seed_market_pool_from_catalog():
        for iid in _MARKET_LEGACY_RETIRED:
            MARKET_ITEM_POOL.pop(iid, None)
        for iid, d in ITEM_CATALOG.items():
            if not d["available_used"]:
                continue
            MARKET_ITEM_POOL[iid] = {
                "cat":   _MARKET_CAT_FOR_ITEM.get(d["category"], "home"),
                "name":  d["label"],
                "value": d["price_used"],
                "grant": "item",
                # big-ticket items show up rarely so they stay aspirational
                "rare":  d["price_new"] >= 500,
            }

    _COND_PRICE_MULT = {"Poor": 0.55, "Used": 0.75, "Good": 0.9, "Excellent": 1.05}
    _SELLERS = [
        ("a student",           -5),
        ("a downsizing family",  0),
        ("a hobbyist",           2),
        ("a small resale shop",  8),
        ("a collector",          5),
    ]

    def _item_already_owned(item_id):
        d = MARKET_ITEM_POOL.get(item_id)
        if not d:
            return True
        if d["grant"] == "item":
            return owns_item(item_id)
        if d["grant"] == "equip":
            return item_id in store.owned_equipment
        return getattr(store, d["flag"], False)

    def listing_repair_eligible(listing):
        """Poor-condition gear can be restored via the Phase 61 mechanics bench."""
        return listing.get("condition") == "Poor"

    def listing_condition_text(listing):
        if listing_repair_eligible(listing):
            ok = skill_val("mech") >= 4
            return ("Condition: Poor — Repair possible (Mechanics 4+)"
                    if ok else "Condition: Poor — Repair needs Mechanics 4+")
        return "Condition: " + listing.get("condition", "Good")

    def refresh_market_listings():
        """Deterministic per-period board; prune expired/purchased, add once."""
        period = store.day // MARKET_ROTATE
        kept = [l for l in store.market_listings
                if not l.get("purchased") and store.day <= l.get("expire_day", -1)]
        store.market_listings = kept
        if store.market_listings_period == period:
            return
        store.market_listings_period = period
        import random as _r
        rng = _r.Random(period * 8221 + 17)
        # Busy-market daily condition adds a listing (exposed in the app header).
        base_n = 6
        if daily_condition().get("effects", {}).get("cafe_crowd", 0) or \
           daily_condition().get("effects", {}).get("park_attendance", 0):
            base_n += 1
        # Phase 67: a flea market anywhere in the city puts more stuff up for
        # sale. The marketplace is a phone app with no location of its own, so
        # this reads the GLOBAL modifier rather than a per-location one.
        base_n += global_event_modifier("marketplace_listing_bonus", 0)
        candidates = list(MARKET_ITEM_POOL.keys())
        rng.shuffle(candidates)
        existing = {l["id"] for l in store.market_listings}
        added = []
        for item_id in candidates:
            if len(added) >= base_n:
                break
            d = MARKET_ITEM_POOL[item_id]
            # rare items appear less often
            if d.get("rare") and rng.random() > 0.4:
                continue
            lid = "mkt_%s_p%d" % (item_id, period)
            if lid in existing:
                continue
            cond = rng.choice(["Poor", "Used", "Used", "Good", "Good", "Excellent"])
            seller_name, seller_diff = rng.choice(_SELLERS)
            base = d["value"] * _COND_PRICE_MULT[cond]
            markup = rng.uniform(0.98, 1.18)   # some sellers ask above fair
            asking = int(round(base * markup / 5.0) * 5)
            fair_low = int(base * 0.85)
            fair_high = int(base * 1.05)
            added.append({
                "id": lid, "item_id": item_id, "cat": d["cat"], "name": d["name"],
                "seller": seller_name, "seller_diff": seller_diff,
                "asking": asking, "condition": cond,
                "fair_low": fair_low, "fair_high": fair_high,
                "neg_difficulty": 45, "expire_day": store.day + MARKET_ROTATE * 2,
                "purchased": False,
            })
        store.market_listings = list(store.market_listings) + added

    def market_active_listings():
        return [l for l in store.market_listings
                if not l.get("purchased") and store.day <= l.get("expire_day", -1)
                and not _item_already_owned(l["item_id"])]

    # ── Negotiation ──────────────────────────────────────────────────────────
    # Offer tiers as (discount_percent, aggressive_bool). 0 = buy at asking.
    def market_offer_price(listing, discount_pct):
        return int(round(listing["asking"] * (1.0 - discount_pct / 100.0) / 5.0) * 5)

    def _neg_engine_difficulty(listing, discount_pct):
        return int(listing["neg_difficulty"] + discount_pct * 1.15 + listing["seller_diff"])

    def _neg_mods():
        mods = []
        if has_player_state("confident"): mods.append(("Confident", +5))
        return mods

    def market_negotiation_chance(listing, discount_pct):
        """No side effects. Success = seller accepts the lower price."""
        return calculate_check_chance(
            "neg_%s_%d" % (listing["id"], discount_pct),
            skill_val("biz"), _neg_engine_difficulty(listing, discount_pct),
            _neg_mods())

    def market_negotiate(listing, discount_pct):
        """Resolve a negotiation attempt (anti-save-scum stable per attempt).
        Returns dict: accepted(bool), walked(bool), price, result."""
        key = "%s_%d" % (listing["id"], discount_pct)
        attempt_no = store._market_neg_attempts.get(key, 0) + 1
        result = roll_check("neg_%s_%d" % (listing["id"], discount_pct),
                            skill_val("biz"), _neg_engine_difficulty(listing, discount_pct),
                            _neg_mods(), attempt_number=attempt_no, stable=True)
        d = dict(store._market_neg_attempts)
        d[key] = attempt_no
        store._market_neg_attempts = d
        price = market_offer_price(listing, discount_pct)
        accepted = result["tier"] in ("success", "great", "critical")
        walked = False
        if not accepted and discount_pct >= 25 and result["tier"] == "critical_failure":
            walked = True
            _remove_listing(listing["id"])
        return {"accepted": accepted, "walked": walked, "price": price, "result": result}

    def _remove_listing(listing_id):
        ls = list(store.market_listings)
        for i, l in enumerate(ls):
            if l["id"] == listing_id:
                l = dict(l); l["purchased"] = True; ls[i] = l
        store.market_listings = ls

    def market_buy(listing, price):
        """Charge and grant. Returns True on success. Marks listing purchased."""
        if not try_spend(int(price), "discretionary"):
            return False
        d = MARKET_ITEM_POOL[listing["item_id"]]
        if d["grant"] == "item":
            grant_item(listing["item_id"], listing["condition"])
        elif d["grant"] == "equip":
            grant_equipment(listing["item_id"], listing["condition"])
        else:
            setattr(store, d["flag"], True)
        _remove_listing(listing["id"])
        record_game_event("mkt_buy_%s_day%d" % (listing["item_id"], store.day), "purchase",
            "Bought: " + listing["name"], summary=True, journal=False,
            metadata={"item": listing["item_id"], "price": int(price), "condition": listing["condition"]})
        return True


# ── Marketplace phone app ───────────────────────────────────────────────────────
screen phone_marketplace_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Marketplace" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            $ _busy = daily_condition().get("effects", {}).get("cafe_crowd", 0) or daily_condition().get("effects", {}).get("park_attendance", 0)
            if _busy:
                text "Busy market today — extra listings." font ACT_FONT size 11 color "#7fd06a" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 600
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    $ _listings = market_active_listings()
                    if not _listings:
                        null height 20
                        text "No listings right now. New stock rotates in every few days." font ACT_FONT size 13 color "#4a6080" xalign 0.5
                    for _l in _listings:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 8, 10, 8)
                            vbox:
                                spacing 3
                                hbox:
                                    xfill True
                                    text _l["name"] font PROFILE_FONT size 13 color "#cfe0f5" yalign 0.5
                                    text ("$%d" % _l["asking"]) font PROFILE_FONT size 14 color "#ffd66a" yalign 0.5 xalign 1.0
                                hbox:
                                    spacing 8
                                    text MARKET_CATEGORY_LABELS.get(_l["cat"], _l["cat"]) font ACT_FONT size 11 color "#5bcafa"
                                    text ("from %s" % _l["seller"]) font ACT_FONT size 11 color "#7a9ab8"
                                text listing_condition_text(_l) font ACT_FONT size 11 color ("#e0a86a" if listing_repair_eligible(_l) else "#7fd06a")
                                text ("Fair value: $%d–$%d" % (_l["fair_low"], _l["fair_high"])) font ACT_FONT size 10 color "#4a6080"
                                textbutton "Inspect / Negotiate":
                                    action Function(renpy.call_in_new_context, "market_negotiate_ctx", _l["id"])
                                    background Frame("images/ui/act_bar_idle.png", 10, 10, 10, 10)
                                    hover_background Frame("images/ui/act_bar_hover_clean.png", 10, 10, 10, 10)
                                    xpadding 8 ypadding 4
                                    text_font ACT_FONT text_size 11 text_color "#5bcafa" text_hover_color "#ffffff"
            null height 6
            textbutton "Back" action [Hide("phone_marketplace_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# Negotiation / buy screen. Non-phone modal so results can pop cleanly.
screen market_negotiate_scr(listing_id):
    modal True
    zorder 220
    add "#000000cc"
    $ _l = next((l for l in market_listings if l["id"] == listing_id), None)
    frame:
        xalign 0.5 yalign 0.5
        xsize 560
        background "#12161ef8"
        padding (24, 20, 24, 22)
        if _l is None or _l.get("purchased"):
            vbox:
                spacing 12
                text "This listing is gone." font ACT_FONT size 15 color "#cfe0f5" xalign 0.5
                button action Return(None) xalign 0.5 background "#1e3a5f" padding (18, 7):
                    text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"
        else:
            vbox:
                spacing 8
                text _l["name"] font PROFILE_FONT size 17 color "#cfe0f5" xalign 0.5
                text ("%s  ·  from %s  ·  Fair $%d–$%d" % (_l["condition"], _l["seller"], _l["fair_low"], _l["fair_high"])) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                $ _idef = MARKET_ITEM_POOL[_l["item_id"]]
                if _idef["grant"] == "item":
                    text ITEM_CATALOG[_l["item_id"]]["description"] font ACT_FONT size 11 color "#7a9ab8"
                    $ _mkt_delta = market_listing_delta(_l)
                    if _mkt_delta:
                        null height 2
                        text "If you equip it (at this condition):" font ACT_FONT size 11 color "#9fb6d6"
                        for _dl, _dv in _mkt_delta:
                            text ("  %s  %s" % (_dl, _dv)) font ACT_FONT size 10 color "#ffd66a"
                    else:
                        null height 2
                        text "No mechanical bonus — you would own it because you want it." font ACT_FONT size 10 color "#4a6080"
                    if listing_repair_eligible(_l):
                        text "Poor condition scales its bonus down; restoring it at the repair bench recovers that." font ACT_FONT size 10 color "#e0a86a"
                elif _idef["grant"] == "equip" and EQUIPMENT_DEFS.get(_l["item_id"], {}).get("effects"):
                    null height 2
                    text "Equipment bonuses (at this condition):" font ACT_FONT size 11 color "#9fb6d6"
                    for _eff, _raw in EQUIPMENT_DEFS[_l["item_id"]]["effects"].items():
                        $ _factor = _EQUIP_CONDITION_FACTOR.get(_l["condition"], 0.9)
                        if isinstance(_raw, float):
                            text ("  %s  %d%%" % (EFFECT_LABELS.get(_eff, _eff), int(round(min(_EQUIP_FRAC_CAP, _raw * _factor) * 100)))) font ACT_FONT size 10 color "#ffd66a"
                        else:
                            text ("  %s  +%d" % (EFFECT_LABELS.get(_eff, _eff), int(min(_EQUIP_POINT_CAP, round(_raw * _factor))))) font ACT_FONT size 10 color "#ffd66a"
                null height 6
                # Buy at asking
                button:
                    action Return(("buy", _l["asking"], 0))
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 9)
                    hbox:
                        xfill True
                        text ("Buy now — $%d" % _l["asking"]) font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                        text "Guaranteed" font PROFILE_FONT size 12 color "#7fd06a" yalign 0.5 xalign 1.0
                # Offers
                for _disc in (10, 20, 30):
                    $ _oc = market_negotiation_chance(_l, _disc)
                    $ _oprice = market_offer_price(_l, _disc)
                    $ _aggro = _disc >= 25
                    button:
                        action Return(("neg", _oprice, _disc))
                        xfill True
                        background "#1a2a3a"
                        hover_background "#1e3a5f"
                        padding (14, 9)
                        vbox:
                            spacing 1
                            hbox:
                                xfill True
                                text ("Offer $%d (-%d%%)" % (_oprice, _disc)) font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                                text ("%d%%" % _oc["success_or_better"]) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                            if _aggro:
                                text "Lowball — seller may walk away." font ACT_FONT size 10 color "#e07a6a"
                null height 6
                button action Return(None) xalign 0.5 background "#1e3a5f" padding (18, 7):
                    text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# Runs in a NEW context (launched from the phone via renpy.call_in_new_context),
# so it can use `call screen` + dialogue while the phone stays open underneath.
label market_negotiate_ctx(listing_id):
    $ _mkt_lid = listing_id
    jump market_negotiate_loop

label market_negotiate_loop:
    call screen market_negotiate_scr(_mkt_lid)
    # market_negotiate_scr contract: ("buy"|"neg", price, discount) | None.
    # Guard the 3-way unpack below — a bool from the screen layer would raise
    # TypeError, and `is None` alone doesn't catch it.
    $ _mkt_choice = _return
    if not isinstance(_mkt_choice, tuple) or len(_mkt_choice) != 3:
        return
    $ _l = next((l for l in market_listings if l["id"] == _mkt_lid), None)
    if _l is None or _l.get("purchased"):
        return
    $ _mode, _price, _disc = _mkt_choice
    if _mode == "buy":
        if market_buy(_l, _price):
            "Bought the [_l['name']] for $[_price]."
        else:
            "You can't cover that right now."
        return
    else:
        $ _neg = market_negotiate(_l, _disc)
        call screen check_result_scr(_neg["result"], title="Negotiation", details=_market_neg_detail(_neg))
        if _neg["walked"]:
            "The seller shakes their head and pulls the listing. Gone."
            return
        if _neg["accepted"]:
            if market_buy(_l, _neg["price"]):
                "Deal. You take the [_l['name']] for $[_neg['price']]."
            else:
                "You talked them down — then realised you can't afford it."
            return
        else:
            "No deal at that price. It's still available at $[_l['asking']] if you want it."
            jump market_negotiate_loop

init python:
    def _market_neg_detail(neg):
        if neg["walked"]:
            return "The seller walked away."
        if neg["accepted"]:
            return "Accepted - $%d." % neg["price"]
        return "Rejected. Original price still stands."


# The catalog is built at init -1/0; seed the pool from it once afterwards.
init 2 python:
    _seed_market_pool_from_catalog()

    def market_listing_delta(listing):
        """Modifier delta this listing would produce if bought AND equipped, at
        the listing's condition. Uses the same maths as the live modifiers."""
        iid = listing["item_id"]
        if iid not in ITEM_CATALOG:
            return []
        prev = store.equipment_condition.get(iid)
        c = dict(store.equipment_condition)
        c[iid] = listing["condition"]
        store.equipment_condition = c
        try:
            out = equip_delta_at_condition(iid)
        finally:
            c = dict(store.equipment_condition)
            if prev is None:
                c.pop(iid, None)
            else:
                c[iid] = prev
            store.equipment_condition = c
        return out
