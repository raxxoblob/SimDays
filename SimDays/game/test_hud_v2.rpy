# test_hud_v2.rpy — smallest runnable check for the HUD V2 helpers and assets.
# Run via: jump test_hud_v2_run   (dev console). Restores every value it touches.

init python:
    def _run_hud_v2_tests():
        out = []
        def check(name, cond):
            out.append(("PASS" if cond else "FAIL") + "  " + name)

        snap = (store.player_states, store.current_loc, store.need_energy,
                store.need_hunger, store.need_hygiene, store.money, store.day,
                store.hud_mode, store.stock_owned, store.stock_price)
        try:
            # ── assets ────────────────────────────────────────────────────────
            for k, p in HUD2_ICONS.items():
                check("icon loadable: " + k, renpy.loadable(p))
            for p in ("images/ui/hud2/panel_r18.png", "images/ui/hud2/panel_r18_line.png",
                      "images/ui/hud2/bar5.png", "images/ui/hud2/bar8.png"):
                check("shape loadable: " + p, renpy.loadable(p))
            check("every state def has its own icon",
                  all(s in HUD2_ICONS for s in PLAYER_STATE_DEFS))
            check("unknown state falls back to wellbeing",
                  hud2_state_icon("nope_not_a_state") == HUD2_ICONS["wellbeing"])
            check("hygiene icon registered", "hygiene" in HUD2_ICONS)
            check("hygiene icon loadable", renpy.loadable(HUD2_ICONS["hygiene"]))

            # ── geometry stays on screen ──────────────────────────────────────
            check("right island fits", HUD2["right_x"] + HUD2["right_w"] <= 1920)
            check("islands do not overlap",
                  HUD2["left_x"] + HUD2["left_w"] < HUD2["right_x"])
            # hbox holds 9 children (5 segments + 4 dividers) => 8 spacing gaps
            check("segments fit inside the right island",
                  5 * HUD2["seg_w"] + 4 * 1 + 8 * HUD2["seg_gap"]
                  <= HUD2["right_w"] - 2 * HUD2["pad_x"])
            for i, w in ((0, HUD2["panel_w"]), (1, HUD2["panel_w"]),
                         (2, HUD2["panel_w"]), (3, HUD2["panel_w"]),
                         (4, HUD2["panel_w_wide"])):
                check("panel %d stays on screen" % i,
                      0 <= hud2_panel_x(i, w) and hud2_panel_x(i, w) + w <= 1920)

            # ── state helpers ─────────────────────────────────────────────────
            store.player_states = []
            check("no states -> 'No effects'", hud2_state_label() == "No effects")
            check("no states -> primary None", hud2_primary_state() is None)
            store.player_states = [{"state_id": "stressed", "source_id": "t1",
                                    "started_day": store.day, "expires_day": store.day + 2}]
            check("one state shows its title", hud2_state_label() == "Stressed")
            check("days_left is derived from expires_day",
                  hud2_active_states()[0]["days_left"] == 2)
            check("effect text comes from the state def",
                  hud2_active_states()[0]["desc"] == PLAYER_STATE_DEFS["stressed"]["desc"])
            store.player_states = store.player_states + [
                {"state_id": "focused", "source_id": "t2",
                 "started_day": store.day, "expires_day": store.day + 1}]
            check("two states -> '+1' suffix", hud2_state_label().endswith("+1"))
            check("priority follows PLAYER_STATE_DEFS order",
                  hud2_primary_state()["id"] == "focused")
            store.player_states = [{"state_id": "focused", "source_id": "t3",
                                    "started_day": store.day, "expires_day": store.day}]
            check("expired states are filtered out", hud2_active_states() == [])

            # ── location helper ───────────────────────────────────────────────
            store.current_loc = "location_cafe"
            check("known location uses LOCATION_NAMES",
                  hud2_location_label() == "Grounds Café")
            store.current_loc = "location_bar"
            check("leading 'the ' is stripped", hud2_location_label() == "Bar")
            store.current_loc = "location_some_new_place"
            check("unknown location is prettified",
                  hud2_location_label() == "Some New Place")
            store.current_loc = ""
            check("empty location does not crash", bool(hud2_location_label()))

            # ── need read-outs match the canonical thresholds ─────────────────
            store.need_energy = 19
            check("energy 19 is blocked", too_tired() and hud2_energy_status()[0] == "Exhausted")
            store.need_energy = 25
            check("energy 25 is worn out", worn_out() and hud2_energy_status()[0] == "Worn out")
            store.need_energy = 80
            store.need_hunger = 80
            check("energy 80 has no penalty",
                  not worn_out() and hud2_energy_effect().startswith("No penalties"))
            store.need_hunger = 24
            check("hunger 24 is starving",
                  worn_out() and hud2_hunger_status()[0] == "Starving")
            store.need_hunger = 90
            check("high hunger reads as full, not hungry", hud2_hunger_status()[0] == "Fed")
            store.need_hygiene = 100
            check("clean hygiene shows no penalty", "no Appearance penalty" in hud2_hygiene_note())
            store.need_hygiene = 10
            check("filthy hygiene matches eff_app debuff", "-22" in hud2_hygiene_note())

            # ── hygiene segment thresholds (eff_app tiers: 60/40/20 → −0/5/12/22) ────
            store.need_hygiene = 80
            check("hygiene 80 → Clean", hud2_hygiene_status()[0] == "Clean")
            check("hygiene 80 → no penalty text", hud2_hygiene_effect() == "No Appearance penalty.")
            store.need_hygiene = 50
            check("hygiene 50 → Unkempt (below 60)", hud2_hygiene_status()[0] == "Unkempt")
            check("hygiene 50 → -5 text", "−5" in hud2_hygiene_effect())
            store.need_hygiene = 30
            check("hygiene 30 → Grubby (below 40)", hud2_hygiene_status()[0] == "Grubby")
            check("hygiene 30 → -12 text", "−12" in hud2_hygiene_effect())
            store.need_hygiene = 10
            check("hygiene 10 → Filthy (below 20)", hud2_hygiene_status()[0] == "Filthy")
            check("hygiene 10 → -22 text", "−22" in hud2_hygiene_effect())

            # ── hud_mode infrastructure ───────────────────────────────────────
            check("hud_mode default is 'full'", store.hud_mode == "full")
            store.hud_mode = "hidden"
            check("hud_mode 'hidden' is accepted", store.hud_mode == "hidden")
            store.hud_mode = "minimal"
            check("hud_mode 'minimal' is accepted", store.hud_mode == "minimal")
            store.hud_mode = "full"

            # ── portfolio_value() old-save safety ─────────────────────────────
            _saved_owned = dict(store.stock_owned)
            _saved_price = dict(store.stock_price)
            store.stock_owned  = {"GHOST": 10, "AAPL": 5}
            store.stock_price  = {"AAPL": 100}   # GHOST is missing
            _pv = portfolio_value()
            check("portfolio_value with unknown symbol returns 0 for that sym",
                  _pv == 500)   # only AAPL: 5 * 100 = 500; GHOST contributes 0
            store.stock_owned  = {"GHOST": 10}
            store.stock_price  = {}
            check("portfolio_value all unknown → 0", portfolio_value() == 0)
            store.stock_owned  = _saved_owned
            store.stock_price  = _saved_price

            # ── money formatting ──────────────────────────────────────────────
            check("money is grouped", hud2_money_str(999999) == "$999,999")
            check("zero money", hud2_money_str(0) == "$0")
            check("stock value never raises", isinstance(hud2_stock_value(), (int, float)))

            # ── people here returns names, never raw ids ──────────────────────
            store.current_loc = "location_cafe"
            people = hud2_people_here()
            check("people_here returns strings", all(isinstance(p, str) for p in people))
            check("people_here exposes no npc ids",
                  not any(p in NPC_DATA for p in people))
        finally:
            (store.player_states, store.current_loc, store.need_energy,
             store.need_hunger, store.need_hygiene, store.money, store.day,
             store.hud_mode, store.stock_owned, store.stock_price) = snap

        fails = [l for l in out if l.startswith("FAIL")]
        return "\n".join(fails if fails else out[:1] + ["... %d checks, all PASS" % len(out)])


label test_hud_v2_run:
    $ _hud2_report = _run_hud_v2_tests()
    "HUD V2 self-check:\n\n[_hud2_report]"
    return
