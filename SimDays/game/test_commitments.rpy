# test_commitments.rpy — regression tests for the 5 commitment paths.
# Call `label test_commitments_run` from a dev menu or directly.
# Prints PASS/FAIL to console. Fully restores game state — safe on any save.

init python:
    def _run_commitment_tests():
        import copy
        import store as _s

        # ── Full state snapshot ───────────────────────────────────────────
        _snap = {
            "day":         _s.day,
            "hour":        _s.hour,
            "current_loc": _s.current_loc,
            "commitments": copy.deepcopy(_s.player_commitments),
            "messages":    copy.deepcopy(_s.npc_messages),
            # trust vars for every NPC that cancel_commitment touches
            "lena_trust":    _s.lena_trust,
            "natalie_trust": _s.natalie_trust,
            "martha_trust":  _s.martha_trust,
            "nora_trust":    _s.nora_trust,
            "eli_trust":     _s.eli_trust,
            # accepted flags
            "martha_coffee_accepted":  _s.martha_coffee_accepted,
            "nora_closing_accepted":   _s.nora_closing_accepted,
        }

        def _restore():
            _s.day             = _snap["day"]
            _s.hour            = _snap["hour"]
            _s.current_loc     = _snap["current_loc"]
            _s.player_commitments = copy.deepcopy(_snap["commitments"])
            _s.npc_messages    = copy.deepcopy(_snap["messages"])
            _s.lena_trust      = _snap["lena_trust"]
            _s.natalie_trust   = _snap["natalie_trust"]
            _s.martha_trust    = _snap["martha_trust"]
            _s.nora_trust      = _snap["nora_trust"]
            _s.eli_trust       = _snap["eli_trust"]
            _s.martha_coffee_accepted = _snap["martha_coffee_accepted"]
            _s.nora_closing_accepted  = _snap["nora_closing_accepted"]

        passed = 0
        failed = 0

        def check(label, cond):
            nonlocal passed, failed
            if cond:
                print("  PASS  %s" % label)
                passed += 1
            else:
                print("  FAIL  %s" % label)
                failed += 1

        print("\n=== Commitment path tests ===")

        # ─── 1. Martha coffee ────────────────────────────────────────────
        print("─ 1. Martha: invite → accept → available → complete → gone from Upcoming")
        _restore()
        _s.day  = 10
        _s.hour = 12.0
        add_commitment("martha_coffee_1", "martha", "Coffee with Martha", 11, 17, "Café Grounds", "phone_martha_coffee_scene")
        check("shows in Upcoming", any(c["id"] == "martha_coffee_1" for c in upcoming_commitments()))
        _s.day  = 11
        _s.hour = 17.5
        check("available inside window", commitment_available("martha_coffee_1"))
        complete_commitment("martha_coffee_1")
        check("gone from Upcoming after complete", not any(c["id"] == "martha_coffee_1" for c in upcoming_commitments()))

        # ─── 2. Eli debug session ────────────────────────────────────────
        print("─ 2. Eli: tomorrow 19:00, 2h grace, window boundaries correct")
        _restore()
        _s.day  = 5
        _s.hour = 14.0
        add_commitment("eli_debug_1", "eli", "Late debug session with Eli", 6, 19, "The Hub", "phone_eli_debug_scene")
        check("shows in Upcoming", any(c["id"] == "eli_debug_1" for c in upcoming_commitments()))
        _s.day  = 6
        _s.hour = 18.9
        check("not available before window", not commitment_available("eli_debug_1"))
        _s.hour = 19.5
        check("available inside window", commitment_available("eli_debug_1"))
        _s.hour = 21.1   # 19 + 2 = 21 → past grace
        check("not available past grace", not commitment_available("eli_debug_1"))
        expire_late_commitments()
        check("marked missed after expiry", any(c["id"] == "eli_debug_1" and c["missed"] for c in _s.player_commitments))

        # ─── 3. Lena case observation ────────────────────────────────────
        print("─ 3. Lena: next Wednesday, professional cancel penalty")
        _restore()
        _s.day  = 3   # Thursday
        _s.hour = 10.0
        _target = next_weekday(2)   # Wednesday
        add_commitment("lena_case_1", "lena", "Case observation with Dr. Lena", _target, 14, "Hospital", "phone_lena_case_scene")
        check("scheduled on a Wednesday", _target % 7 == 2)
        check("scheduled in the future", _target > _s.day)
        _s.day  = _target
        _s.hour = 14.0
        check("available at 14:00", commitment_available("lena_case_1"))
        _before = _s.lena_trust
        cancel_commitment("lena_case_1", late=False)
        check("marked cancelled (not missed)", any(c["id"] == "lena_case_1" and c.get("cancelled") for c in _s.player_commitments))
        check("early cancel: small penalty", 0 < _before - _s.lena_trust <= 2)

        # ─── 4. Nora closing ────────────────────────────────────────────
        print("─ 4. Nora: 21:00 window, late no-show → missed message queued")
        _restore()
        _s.day  = 2
        _s.hour = 10.0
        add_commitment("nora_closing_1", "nora", "Close the café with Nora", 3, 21, "Café Grounds", "phone_nora_closing_scene")
        _s.day  = 3
        _s.hour = 21.0
        check("available at 21:00", commitment_available("nora_closing_1"))
        _s.hour = 23.1   # 21 + 2 = 23 → past grace
        expire_late_commitments()
        check("marked missed after 23:00", any(c["id"] == "nora_closing_1" and c["missed"] for c in _s.player_commitments))
        check("missed message queued (dedup-safe)", any(m.get("tag") == "missed_nora_closing_1" for m in _s.npc_messages))
        # second expiry call must not double-queue
        _msg_count_before = len(_s.npc_messages)
        expire_late_commitments()
        check("expire idempotent — no duplicate message", len(_s.npc_messages) == _msg_count_before)

        # ─── 5. Natalie extra shift ─────────────────────────────────────
        print("─ 5. Natalie: Saturday 8am, grace=1h, entry trigger, late-cancel vs early-cancel")
        _restore()
        _s.day  = 1   # Tuesday
        _s.hour = 9.0
        _sat = next_weekday(5)
        add_commitment("natalie_shift_1", "natalie", "Extra shift (Natalie)", _sat, 8, "Warehouse", "phone_natalie_extra_scene", grace=1.0)
        check("grace stored as 1.0", next(c["grace"] for c in _s.player_commitments if c["id"] == "natalie_shift_1") == 1.0)
        _s.day  = _sat
        _s.hour = 8.0
        check("available at 08:00", commitment_available("natalie_shift_1"))
        _s.hour = 9.1   # 8 + 1 = 9 → past grace
        check("not available at 09:06", not commitment_available("natalie_shift_1"))
        # early cancel vs late cancel penalty magnitude
        _restore()
        _sat2 = next_weekday(5)
        add_commitment("natalie_shift_1", "natalie", "Extra shift (Natalie)", _sat2, 8, "Warehouse", "phone_natalie_extra_scene", grace=1.0)
        _s.day  = _sat2
        _s.hour = 1.0   # 7h before — early cancel
        _before_early = _s.natalie_trust
        cancel_commitment("natalie_shift_1", late=False)
        _early_loss = _before_early - _s.natalie_trust
        _restore()
        add_commitment("natalie_shift_1", "natalie", "Extra shift (Natalie)", _sat2, 8, "Warehouse", "phone_natalie_extra_scene", grace=1.0)
        _s.day  = _sat2
        _s.hour = 7.5   # 0.5h before — late cancel
        _before_late = _s.natalie_trust
        cancel_commitment("natalie_shift_1", late=True)
        _late_loss = _before_late - _s.natalie_trust
        check("late-cancel penalty > early-cancel penalty", _late_loss > _early_loss)
        check("cancelled flag set (not missed)", any(c["id"] == "natalie_shift_1" and c.get("cancelled") for c in _s.player_commitments))

        # ── Final restore + summary ───────────────────────────────────────
        _restore()
        print("\n=== %d passed, %d failed ===" % (passed, failed))
        return failed == 0


label test_commitments_run:
    $ _ok = _run_commitment_tests()
    if _ok:
        "All commitment tests passed."
    else:
        "Some commitment tests FAILED — check console."
    return
