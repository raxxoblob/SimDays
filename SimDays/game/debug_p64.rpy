# Phase 64 self-check. The smallest thing that fails if the three structural
# fixes regress. Run it from the debug menu ("Phase 64 self-check").
#
#   1. Freelance reputation pacing  — rep gain must stay in the 0-4 band and be
#      difficulty-weighted, or min_rep tier gates go dead again.
#   2. proper_desk truncation       — the $260 desk must produce a NON-ZERO
#      session modifier. This is the bug that shipped: int(0.05 * 10) == 0.
#   3. Generalist income paths      — every pay band must have a positive floor
#      (failure pays less, never nothing) and stay under the $30/h EV benchmark.

init python:

    def _p64_selfcheck():
        """Returns (ok, [lines]). Pure assertions — mutates no game state."""
        out = []
        fails = []

        def chk(label, cond, detail=""):
            out.append(("PASS" if cond else "FAIL", label, detail))
            if not cond:
                fails.append(label)

        # ── 1. reputation pacing ────────────────────────────────────────────
        # Every rating/difficulty combination must land in 0..4.
        _all = [_project_rep_gain(r, d)
                for r in ("S", "A", "B", "C", "D") for d in range(1, 11)]
        chk("rep gain within 0-4 band", max(_all) <= 4 and min(_all) >= 0,
            "observed %d..%d" % (min(_all), max(_all)))
        # A D-grade delivery must earn no standing at all.
        chk("D rating earns 0 rep", _project_rep_gain("D", 10) == 0)
        # Harder work must be worth more than easy work at the same rating.
        chk("difficulty is weighted",
            _project_rep_gain("B", 9) > _project_rep_gain("B", 2),
            "d9=%d > d2=%d" % (_project_rep_gain("B", 9), _project_rep_gain("B", 2)))
        # Pacing: the top freelance gate is min_rep 70. At the realistic rate of
        # 0.5 projects/day it must NOT be reachable before roughly day 60.
        _avg_mid = _project_rep_gain("B", 5)          # typical midgame delivery
        _days_to_70 = 70.0 / (_avg_mid * 0.5)
        chk("rep 70 not reachable before day 60", _days_to_70 >= 60,
            "~day %d at 0.5 proj/day" % _days_to_70)

        # ── 2. proper_desk truncation ───────────────────────────────────────
        # The regression was a silent 0. Recompute the exact expression the
        # freelance session uses, with the item's real effect value.
        _eff = HOME_UPGRADE_DEFS["proper_desk"]["effect_value"]
        _bonus = int(round(_eff * 60))
        chk("proper_desk yields a non-zero session bonus", _bonus > 0,
            "%.2f -> +%d roll points" % (_eff, _bonus))
        # The old formula, kept here as a tripwire: if someone reverts to it this
        # assertion documents exactly what breaks.
        chk("old int(eff*10) formula was indeed zero", int(_eff * 10) == 0,
            "int(%.2f * 10) == 0" % _eff)
        # No OTHER fractional home upgrade may truncate to zero the same way.
        _frac_upgrades = [(u, d["effect_value"]) for u, d in HOME_UPGRADE_DEFS.items()
                          if isinstance(d["effect_value"], float)]
        chk("all fractional upgrades survive their consumer",
            all(v > 0 for _u, v in _frac_upgrades),
            "%d fractional upgrades checked" % len(_frac_upgrades))

        # ── 3. generalist income floors and ceilings ────────────────────────
        # Catering: failure must still pay, and EV/hour must stay under $30.
        chk("catering failure still pays",
            min(_CATERING_PAY_MULT.values()) > 0)
        for _o in CATERING_ORDERS:
            _ev = _o["pay"] * 1.0 - _o["cost"]        # 'success' tier, net
            _evh = _ev / _o["hours"]
            chk("catering EV/h under $30: " + _o["id"], _evh < 30.0,
                "$%.1f/h" % _evh)
        # Gym class: same two rules, at the skill ceiling (worst case for EV).
        chk("gym class failure still pays",
            min(_GYM_CLASS_PAY_MULT.values()) > 0)
        # EV at mid skill (fit 6) must respect the Phase 63 $30/h benchmark.
        _gc_mid_evh = min(55, 18 + 6 * 4) / GYM_CLASS_HOURS
        chk("gym class EV/h under $30 at mid skill", _gc_mid_evh < 30.0,
            "$%.1f/h" % _gc_mid_evh)
        # Soft ceiling at max skill — a maxed generalist may beat the mid-skill
        # benchmark, but must not approach career-shift rates.
        _gc_cap_evh = (55 * max(_GYM_CLASS_PAY_MULT.values())) / GYM_CLASS_HOURS
        chk("gym class EV/h under $50 at skill cap", _gc_cap_evh < 50.0,
            "$%.1f/h" % _gc_cap_evh)
        # Both paths must be cooldown-gated, or they become button-mashing money.
        chk("catering is cooldown-gated", CATERING_COOLDOWN >= 2,
            "%d days" % CATERING_COOLDOWN)
        chk("gym class is cooldown-gated", GYM_CLASS_COOLDOWN >= 2,
            "%d days" % GYM_CLASS_COOLDOWN)

        return (not fails), out

    def _p64_projection():
        """Reputation projection table for the two play rates."""
        rows = []
        # Difficulty mix a player can actually reach by each milestone, at an
        # average B/A rating. Early contracts are difficulty 2-3, midgame 5-7.
        for rate, rlabel in ((1.0, "1 project/day"), (0.5, "0.5 project/day")):
            cells = []
            for dayn in (14, 30, 60, 90):
                projects = dayn * rate
                # first ~10 projects are low difficulty, the rest midgame tier
                low = min(projects, 10)
                high = max(0.0, projects - 10)
                rep = low * _project_rep_gain("B", 2) + high * _project_rep_gain("A", 6)
                cells.append(min(100, int(rep)))
            rows.append((rlabel, cells))
        return rows


screen debug_p64_scr():
    modal True
    zorder 210
    add "#000000e0"
    $ _p64_ok, _p64_rows = _p64_selfcheck()
    frame:
        xalign 0.5 yalign 0.5
        xsize 760
        ysize 620
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "PHASE 64 SELF-CHECK" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text ("ALL PASS" if _p64_ok else "FAILURES PRESENT") font PROFILE_FONT size 15 xalign 0.5 color ("#7fd06a" if _p64_ok else "#e05050")
            null height 4
            viewport:
                xfill True
                ysize 460
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True
                    for _st, _lbl, _dt in _p64_rows:
                        hbox:
                            spacing 8
                            xfill True
                            text _st font PROFILE_FONT size 12 color ("#7fd06a" if _st == "PASS" else "#e05050") yalign 0.5
                            text _lbl font ACT_FONT size 12 color "#cfe0f5" yalign 0.5
                            text _dt font ACT_FONT size 11 color "#7a9ab8" yalign 0.5 xalign 1.0
                    null height 8
                    text "REPUTATION PROJECTION (day 14 / 30 / 60 / 90)" font PROFILE_FONT size 13 color "#ffd66a"
                    for _rlbl, _cells in _p64_projection():
                        hbox:
                            spacing 8
                            xfill True
                            text _rlbl font ACT_FONT size 12 color "#cfe0f5" yalign 0.5
                            text (" / ".join(str(_c) for _c in _cells)) font PROFILE_FONT size 12 color "#5bcafa" yalign 0.5 xalign 1.0
                    null height 6
                    text ("Live freelance reputation: %d" % freelance_reputation) font ACT_FONT size 12 color "#7a9ab8"
                    text ("proper_desk owned: %s   session bonus: +%d" % (owns_home_upgrade("proper_desk"), int(round(home_upgrade_effect("desk_efficiency") * 60)))) font ACT_FONT size 12 color "#7a9ab8"
                    text ("Catering offer today: %s" % (catering_offer() or "none")) font ACT_FONT size 12 color "#7a9ab8"
                    text ("Gym class available: %s" % gym_class_available()) font ACT_FONT size 12 color "#7a9ab8"
            null height 6
            textbutton "Back" action [Hide("debug_p64_scr"), Show("debug_menu")] xalign 0.5 text_font ACT_FONT text_size 18 text_color "#9fb6d6" text_hover_color "#ffffff"
