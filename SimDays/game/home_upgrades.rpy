# Home upgrade system — one-time purchases that give persistent gameplay effects.

init python:

    HOME_UPGRADE_DEFS = {
        "better_mattress": {
            "title": "Better Mattress",
            "desc": "Restful sleep. Full-sleep energy recovery +8.",
            "cost": 380, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "sleep_energy", "effect_value": 8,
        },
        "proper_desk": {
            "title": "Proper Desk",
            "desc": "Ergonomic setup. Computer work and study energy cost -5%.",
            "cost": 260, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "desk_efficiency", "effect_value": 0.05,
        },
        "faster_internet": {
            "title": "Faster Internet",
            "desc": "Reliable connection. +1 freelance offer per daily refresh.",
            "cost": 180, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "freelance_offers", "effect_value": 1,
        },
        "kitchen_equipment": {
            "title": "Kitchen Equipment",
            "desc": "Better tools. Home meals restore +5 more hunger.",
            "cost": 220, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "meal_hunger", "effect_value": 5,
        },
        "acoustic_treatment": {
            "title": "Acoustic Treatment",
            "desc": "Soundproofing panels. Guitar practice energy cost -8%.",
            "cost": 290, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "guitar_energy", "effect_value": 0.08,
        },
        "basic_home_gym": {
            "title": "Basic Home Gym",
            "desc": "Dumbbells and mat. Unlocks short home workout (1h, +12 STR XP).",
            "cost": 450, "min_apt_tier": 1, "prereqs": [],
            "effect_type": "home_workout", "effect_value": 1,
        },
    }

    def owns_home_upgrade(uid):
        return uid in store.home_upgrades

    def can_buy_home_upgrade(uid):
        d = HOME_UPGRADE_DEFS.get(uid)
        if not d: return False
        if owns_home_upgrade(uid): return False
        if store.apartment_tier < d["min_apt_tier"]: return False
        if store.money < d["cost"]: return False
        return all(owns_home_upgrade(p) for p in d["prereqs"])

    def buy_home_upgrade(uid):
        d = HOME_UPGRADE_DEFS.get(uid)
        if not d or not can_buy_home_upgrade(uid): return False
        gain_money(-d["cost"], "upgrade")
        store.home_upgrades = list(store.home_upgrades) + [uid]
        record_game_event("upgrade_%s_day%d" % (uid, store.day), "purchase",
            "Purchased: " + d["title"], summary=True, journal=False,
            metadata={"upgrade_id": uid, "cost": d["cost"]})
        return True

    def home_upgrade_effect(effect_type):
        """Returns total additive value for an effect type from all owned upgrades."""
        total = 0
        for uid in store.home_upgrades:
            d = HOME_UPGRADE_DEFS.get(uid, {})
            if d.get("effect_type") == effect_type:
                total += d.get("effect_value", 0)
        return total

    def available_home_upgrades():
        return [uid for uid, d in HOME_UPGRADE_DEFS.items()
                if not owns_home_upgrade(uid) and store.apartment_tier >= d["min_apt_tier"]]

    def _buy_upgrade_wrapper(uid):
        """Function() wrapper — returns None."""
        buy_home_upgrade(uid)


# ── Home upgrades screen ───────────────────────────────────────────────────────
screen home_upgrades_scr():
    modal True
    add "#000000aa"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 680
        ysize 580
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (20, 16, 20, 16)
        vbox:
            spacing 10
            text "Home Upgrades" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            text ("Balance: $%d" % money) font ACT_FONT size 14 color "#ffd66a" xalign 0.5
            null height 2
            viewport:
                xfill True
                ysize 440
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    for _uid, _udef in HOME_UPGRADE_DEFS.items():
                        $ _owned = owns_home_upgrade(_uid)
                        $ _buyable = can_buy_home_upgrade(_uid)
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (12, 10, 12, 10)
                            vbox:
                                spacing 4
                                hbox:
                                    xfill True
                                    text _udef["title"] font PROFILE_FONT size 14 color ("#7fd06a" if _owned else "#cfe0f5") yalign 0.5
                                    if _owned:
                                        text "✓ Owned" font ACT_FONT size 12 color "#7fd06a" yalign 0.5 xalign 1.0
                                    else:
                                        text ("$%d" % _udef["cost"]) font PROFILE_FONT size 14 color "#ffd66a" yalign 0.5 xalign 1.0
                                text _udef["desc"] font ACT_FONT size 12 color "#7a9ab8"
                                if not _owned:
                                    textbutton "Buy":
                                        sensitive _buyable
                                        action [Function(_buy_upgrade_wrapper, _uid), renpy.restart_interaction]
                                        xalign 1.0
                                        background Frame("images/ui/act_bar_idle.png", 12, 12, 12, 12)
                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 12, 12, 12, 12)
                                        insensitive_background Frame("images/ui/act_bar_idle.png", 12, 12, 12, 12)
                                        xpadding 10 ypadding 5
                                        text_font ACT_FONT text_size 13
                                        text_color ("#cfe0f5" if _buyable else "#4a6080")
                                        text_hover_color "#ffffff"
            textbutton "Close" action Return() xalign 0.5 text_font ACT_FONT text_size 19 text_color "#9fb6d6" text_hover_color "#ffffff"
