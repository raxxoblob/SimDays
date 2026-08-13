# Phase 61 — Mechanics: practical repair challenges (safe replace vs skill-based repair).
# A rotating board of small fix-it jobs. Each job offers:
#   * Diagnose (optional): time + small XP, reveals the fault, raises repair odds.
#   * Replace part: guaranteed fix, costs more, little XP, smaller net pay.
#   * Attempt repair: cheap materials + a visible-odds skill check, XP either way.
# Failed genuine attempts always grant Mechanics XP and can be retried (a NEW
# attempt = a new roll; the SAME attempt is reload-stable via stable seeding).
#
# Money design: jobs pay a modest fixed reward, are limited in volume and rotate
# with a cooldown, so repairs cannot out-earn a career shift (see debug economy).

default mech_jobs            = []   # active job dicts
default mech_jobs_gen_period = -1
default _mech_attempts       = {}   # job_id -> committed attempt count (anti-save-scum seed)
default _mech_diagnosed      = []   # job_ids the player has diagnosed
default _mech_referrals      = []   # unique referral content ids already granted

init python:

    MECH_PROJECT_TEMPLATES = {
        "dead_headphones": {"name": "Dead Headphones", "difficulty": 2, "replace": 35,
                            "materials": 6,  "reward": 26, "diagnosable": False, "part": ""},
        "desk_lamp":       {"name": "Flickering Desk Lamp", "difficulty": 2, "replace": 30,
                            "materials": 5,  "reward": 22, "diagnosable": False, "part": ""},
        "wall_clock":      {"name": "Stopped Wall Clock", "difficulty": 3, "replace": 40,
                            "materials": 8,  "reward": 30, "diagnosable": False, "part": ""},
        "broken_speaker":  {"name": "Broken Bluetooth Speaker", "difficulty": 3, "replace": 45,
                            "materials": 10, "reward": 38, "diagnosable": True,  "part": "a loose solder joint"},
        "guitar_setup":    {"name": "Guitar Needing a Setup", "difficulty": 4, "replace": 60,
                            "materials": 12, "reward": 48, "diagnosable": True,  "part": "high action at the nut"},
        "door_lock":       {"name": "Jammed Door Lock", "difficulty": 5, "replace": 80,
                            "materials": 15, "reward": 60, "diagnosable": True,  "part": "a worn pin tumbler"},
        "microwave":       {"name": "Faulty Microwave", "difficulty": 5, "replace": 90,
                            "materials": 20, "reward": 70, "diagnosable": True,  "part": "a blown thermal fuse"},
        "laptop_fan":      {"name": "Noisy Laptop Fan", "difficulty": 6, "replace": 120,
                            "materials": 25, "reward": 95, "diagnosable": True,  "part": "a seized fan bearing"},
    }

    MECH_JOBS_ROTATE = 3       # days between board refreshes
    _MECH_DIAGNOSIS_BASE = 8   # roll points from a completed diagnosis
    MECH_JOBS_MIN_SKILL = 2    # paid client work unlocks at Mechanics Lv 2

    def _mech_engine_difficulty(d):
        return 28 + d * 5

    def refresh_mech_jobs():
        """Deterministic per-period board. Prunes expired/completed; adds the
        current period's jobs once. Never rerolls on screen open."""
        period = store.day // MECH_JOBS_ROTATE
        # prune
        kept = [j for j in store.mech_jobs
                if not j.get("done") and store.day <= j.get("expire_day", -1)]
        store.mech_jobs = kept
        # Lv0-1: nobody trusts you with their stuff yet. Don't populate a board
        # of jobs the player can only lose money on. Note: gate is checked before
        # gen_period is stamped, so the board fills the moment they hit Lv2.
        if skill_val("mech") < MECH_JOBS_MIN_SKILL:
            return
        if store.mech_jobs_gen_period == period:
            return
        store.mech_jobs_gen_period = period
        import random as _r
        rng = _r.Random(period * 6733 + 41)
        n = 2 + (1 if daily_condition().get("effects", {}).get("indoor_crowd", 0) else 0)
        tids = list(MECH_PROJECT_TEMPLATES.keys())
        rng.shuffle(tids)
        existing = {j["id"] for j in store.mech_jobs}
        added = []
        for tid in tids:
            if len(added) >= n:
                break
            jid = "mech_%s_p%d" % (tid, period)
            if jid in existing:
                continue
            t = MECH_PROJECT_TEMPLATES[tid]
            added.append({
                "id": jid, "tid": tid, "name": t["name"], "difficulty": t["difficulty"],
                "replace": t["replace"], "materials": t["materials"], "reward": t["reward"],
                "diagnosable": t["diagnosable"], "part": t["part"],
                "expire_day": store.day + MECH_JOBS_ROTATE + 1, "done": False,
            })
        store.mech_jobs = list(store.mech_jobs) + added

    def _mech_repair_mods(job):
        mods = []
        t = equipment_modifier("tools", "repair_chance")
        if t:                             mods.append(("Tool kit", t))
        if job["id"] in store._mech_diagnosed:
            dbonus = _MECH_DIAGNOSIS_BASE + equipment_modifier("tools", "diagnosis")
            mods.append(("Diagnosis", dbonus))
        if has_player_state("focused"):   mods.append(("Focused", +3))
        if store.need_energy < 25:        mods.append(("Low energy", -4))
        return mods

    def mech_repair_chance(job):
        return calculate_check_chance(
            "mech_" + job["id"], skill_val("mech"),
            _mech_engine_difficulty(job["difficulty"]),
            _mech_repair_mods(job))

    def mech_diagnose(job):
        """1h + small XP. Reveals the fault and unlocks the diagnosis modifier."""
        spend_time(1.0)
        store.need_energy = max(0, store.need_energy - 4)
        gain_skill_practice("mech", 3, 1)
        if job["id"] not in store._mech_diagnosed:
            store._mech_diagnosed = list(store._mech_diagnosed) + [job["id"]]

    def mech_replace(job):
        """Guaranteed fix via a bought part. Small XP, smaller net pay."""
        if not try_spend(job["replace"], "discretionary"):
            return None
        spend_time(0.5)
        gain_skill_practice("mech", 2, 1)
        gain_money(job["reward"])
        _mech_complete(job)
        return {"mode": "replace", "net": job["reward"] - job["replace"]}

    def mech_attempt_repair(job):
        """Skill check. Materials + time always spent; XP always gained. On
        success the owner pays the reward. Failure can be retried (new roll)."""
        if not try_spend(job["materials"], "discretionary"):
            return None
        # Time scales with difficulty so high-value jobs can't beat a career shift
        # on $/hour (see economy audit / debug_p61).
        _t = 1.0 + 0.25 * job["difficulty"]
        spend_time(_t)
        store.need_energy = max(0, store.need_energy - 8)
        attempt_no = store._mech_attempts.get(job["id"], 0) + 1
        result = roll_check("mech_" + job["id"], skill_val("mech"),
                            _mech_engine_difficulty(job["difficulty"]),
                            _mech_repair_mods(job),
                            attempt_number=attempt_no, stable=True)
        d = dict(store._mech_attempts)
        d[job["id"]] = attempt_no
        store._mech_attempts = d
        tier = result["tier"]
        # XP: genuine attempt always teaches something; harder jobs teach more.
        xp = max(1, int(round((4 + job["difficulty"]) *
                               {"critical_failure": 0.7, "weak": 0.9, "success": 1.0,
                                "great": 1.1, "critical": 1.25}[tier] *
                               _mech_xp_efficiency(job))))
        eff_xp = gain_skill_practice("mech", xp, 1)

        out = {"result": result, "tier": tier, "xp": eff_xp, "reward": 0,
               "bonus": None, "completed": False}
        if tier in ("success", "great", "critical"):
            reward = job["reward"]
            if tier == "great":
                # efficient: partial materials refund
                refund = job["materials"] // 2
                store.money += refund
                out["bonus"] = "Efficient work — $%d materials refunded." % refund
            if tier == "critical":
                out["bonus"] = _mech_referral(job)
            gain_money(reward)
            out["reward"] = reward
            out["completed"] = True
            _mech_complete(job)
        # weak / critical_failure: job stays on the board, retry allowed (new attempt).
        return out

    def _mech_xp_efficiency(job):
        gap = job["difficulty"] - skill_val("mech")
        if gap <= -4:  return 0.4
        if gap <= -2:  return 0.7
        if gap <= 2:   return 1.0
        return 1.25

    def _mech_referral(job):
        uid = "mechref_%s_day%d" % (job["tid"], store.day)
        if uid in store._mech_referrals:
            return "Clean repair."
        store._mech_referrals = list(store._mech_referrals) + [uid]
        store.freelance_reputation = min(100, store.freelance_reputation + 1)
        return "Spotless. They said they'll recommend you. (+reputation)"

    def _mech_complete(job):
        js = list(store.mech_jobs)
        for i, j in enumerate(js):
            if j["id"] == job["id"]:
                j = dict(j)
                j["done"] = True
                js[i] = j
        store.mech_jobs = js
        record_game_event("mechfix_%s_day%d" % (job["tid"], store.day), "project",
            "Repaired: " + job["name"], summary=True, journal=False,
            metadata={"job": job["tid"]})

    # ── Restore owned second-hand equipment (ties marketplace <-> mechanics) ──
    def restorable_equipment():
        """Owned equipment items below Excellent condition that have a mechanical
        effect worth improving."""
        out = []
        for item_id in store.owned_equipment:
            d = EQUIPMENT_DEFS.get(item_id)
            if not d or not d.get("effects"):
                continue
            if equipment_condition_of(item_id) != "Excellent":
                out.append(item_id)
        return out

    def restore_equipment_chance(item_id):
        d = EQUIPMENT_DEFS[item_id]
        diff = 3 + d["tier"] * 2   # tier1=5, tier3=9
        mods = []
        t = equipment_modifier("tools", "repair_chance")
        if t: mods.append(("Tool kit", t))
        if store.need_energy < 25: mods.append(("Low energy", -4))
        return calculate_check_chance("restore_" + item_id, skill_val("mech"),
                                      _mech_engine_difficulty(diff), mods)

    def restore_equipment(item_id):
        d = EQUIPMENT_DEFS[item_id]
        diff = 3 + d["tier"] * 2
        materials = 8 + d["tier"] * 4
        if not try_spend(materials, "discretionary"):
            return None
        spend_time(1.5)
        store.need_energy = max(0, store.need_energy - 8)
        mods = []
        t = equipment_modifier("tools", "repair_chance")
        if t: mods.append(("Tool kit", t))
        if store.need_energy < 25: mods.append(("Low energy", -4))
        attempt_no = store._mech_attempts.get("restore_" + item_id, 0) + 1
        result = roll_check("restore_" + item_id, skill_val("mech"),
                            _mech_engine_difficulty(diff), mods,
                            attempt_number=attempt_no, stable=True)
        am = dict(store._mech_attempts)
        am["restore_" + item_id] = attempt_no
        store._mech_attempts = am
        gain_skill_practice("mech", max(1, 3 + diff // 2), 1)
        improved = None
        if result["tier"] in ("success", "great", "critical"):
            improved = improve_equipment_condition(item_id)
            if result["tier"] == "critical" and improved:
                improved2 = improve_equipment_condition(item_id)
                if improved2:
                    improved = improved2
        return {"result": result, "tier": result["tier"], "improved": improved,
                "item": item_id}


# ── Repair bench screen ─────────────────────────────────────────────────────────
label repair_bench:
    call refresh_and_show_mech
    return

label refresh_and_show_mech:
    $ refresh_mech_jobs()
    call screen mech_bench_scr
    # mech_bench_scr contract: ("job", job_id) | ("restore", item_id) | None.
    # Ren'Py can still hand back a bool here (Dismiss/end_interaction from an
    # overlay), so treat anything that isn't a 2-tuple as "close".
    $ _mb = _return
    if not isinstance(_mb, tuple) or len(_mb) < 2:
        return
    if _mb[0] == "job":
        $ store._mech_cur_job = next((j for j in store.mech_jobs if j["id"] == _mb[1]), None)
        if store._mech_cur_job is not None:
            call mech_job_flow(store._mech_cur_job["id"])
    elif _mb[0] == "restore":
        call mech_restore_flow(_mb[1])
    jump refresh_and_show_mech

label mech_job_flow(job_id):
    $ _job = next((j for j in store.mech_jobs if j["id"] == job_id), None)
    if _job is None:
        return
    call screen mech_job_scr(job_id)
    $ _act = _return
    if _act is None:
        return
    if _act == "diagnose":
        $ mech_diagnose(_job)
        "You open it up and trace the fault. It's [_job['part']]."
        jump mech_job_flow
    elif _act == "replace":
        $ _rr = mech_replace(_job)
        if _rr is None:
            "You can't afford the replacement part."
            jump mech_job_flow
        "Swapped the part. It works. Clean and certain — you pocket $[_job['reward']]."
        return
    elif _act == "repair":
        $ _rr = mech_attempt_repair(_job)
        if _rr is None:
            "You can't afford the materials."
            jump mech_job_flow
        call screen check_result_scr(_rr["result"], title=(_job["name"] + " — Repair"), xtra_lines=_mech_result_lines(_rr))
        if _rr["bonus"]:
            "[_rr['bonus']]"
        if _rr["completed"]:
            return
        jump mech_job_flow
    return

label mech_restore_flow(item_id):
    $ _ri = item_id
    call screen mech_restore_scr(item_id)
    $ _act = _return
    if _act != "restore":
        return
    $ _rr = restore_equipment(_ri)
    if _rr is None:
        "You can't afford the materials."
        return
    call screen check_result_scr(_rr["result"], title=(EQUIPMENT_DEFS[_ri]["name"] + " — Restore"), xtra_lines=_mech_restore_lines(_rr))
    return

init python:
    def _mech_result_lines(rr):
        lines = ["+%d Mechanics XP" % rr["xp"]]
        if rr["reward"] > 0:
            lines.append("Paid: +$%d" % rr["reward"])
        elif rr["tier"] == "weak":
            lines.append("Partial fix — needs another go (odds improved).")
        else:
            lines.append("Didn't hold — you can try again (odds improved).")
        return lines

    def _mech_restore_lines(rr):
        if rr["improved"]:
            return ["Condition improved to %s." % rr["improved"]]
        return ["No improvement this time — try again."]


# Return contract for mech_bench_scr:
#   ("job", job_id)      -> open the fix-it job flow
#   ("restore", item_id) -> open the restoration flow
#   None                 -> close the bench
# No other return shape is produced by this screen. Callers must still guard,
# because Ren'Py itself can end a `call screen` with a bool.
screen mech_bench_scr():
    modal True
    zorder 210
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 900
        ysize 700
        background "#12161ef8"
        padding (26, 20, 26, 20)
        vbox:
            spacing 8
            text "REPAIR BENCH" font PROFILE_FONT size 22 color "#cfe0f5" xalign 0.5
            hbox:
                xalign 0.5
                spacing 18
                text ("Mechanics Lv %d" % skill_val("mech")) font ACT_FONT size 15 color "#9fb6d6"
                $ _tk = equipped_item("tools")
                text ("Tools: %s" % (EQUIPMENT_DEFS[_tk]["name"] if _tk else "none")) font ACT_FONT size 15 color "#7a9ab8"
            null height 4
            viewport:
                xfill True
                ysize 555
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    text "PAID REPAIR JOBS" font PROFILE_FONT size 17 color "#5bcafa"
                    if skill_val("mech") < MECH_JOBS_MIN_SKILL:
                        frame:
                            xfill True
                            background "#1a2230"
                            padding (16, 12, 16, 12)
                            vbox:
                                spacing 4
                                text ("Unlocks at Mechanics Lv %d" % MECH_JOBS_MIN_SKILL) font PROFILE_FONT size 16 color "#e0b060"
                                text "Practice Mechanics or take Auto Basics to qualify." font ACT_FONT size 14 color "#9fb6d6"
                    elif not [j for j in mech_jobs if not j.get("done")]:
                        text "No jobs on the board right now. Check back in a few days." font ACT_FONT size 14 color "#7a9ab8"
                    else:
                        for _j in mech_jobs:
                            if not _j.get("done"):
                                $ _jc = mech_repair_chance(_j)
                                frame:
                                    xfill True
                                    background "#1a2230"
                                    padding (16, 12, 16, 12)
                                    hbox:
                                        spacing 14
                                        xfill True
                                        vbox:
                                            spacing 5
                                            xsize 610
                                            hbox:
                                                spacing 10
                                                text _j["name"] font PROFILE_FONT size 17 color "#cfe0f5"
                                                if _j["id"] in _mech_diagnosed:
                                                    text "diagnosed" font ACT_FONT size 13 color "#7fd06a" yalign 0.5
                                            hbox:
                                                spacing 18
                                                text ("Requires Mech Lv %d" % MECH_JOBS_MIN_SKILL) font ACT_FONT size 14 color "#7a9ab8"
                                                text ("Difficulty %d" % _j["difficulty"]) font ACT_FONT size 14 color "#7a9ab8"
                                                text ("Time %.2gh" % (1.0 + 0.25 * _j["difficulty"])) font ACT_FONT size 14 color "#7a9ab8"
                                            hbox:
                                                spacing 18
                                                text ("Materials $%d" % _j["materials"]) font ACT_FONT size 14 color "#9fb6d6"
                                                text ("Part $%d" % _j["replace"]) font ACT_FONT size 14 color "#9fb6d6"
                                                text ("Chance %d%%" % _jc["success_or_better"]) font ACT_FONT size 15 color "#5bcafa"
                                                text ("Pays $%d" % _j["reward"]) font ACT_FONT size 15 color "#ffd66a"
                                        button:
                                            action Return(("job", _j["id"]))
                                            yalign 0.5
                                            xalign 1.0
                                            background "#1e3a5f"
                                            padding (16, 8)
                                            text "Open" font ACT_FONT size 15 color "#5bcafa" hover_color "#ffffff" xalign 0.5
                    null height 10
                    if restorable_equipment():
                        text "RESTORE YOUR GEAR" font PROFILE_FONT size 17 color "#5bcafa"
                        for _it in restorable_equipment():
                            $ _rc = restore_equipment_chance(_it)
                            $ _rcond = equipment_condition_of(_it)
                            $ _rnext = CONDITION_ORDER[min(CONDITION_ORDER.index(_rcond) + 1, len(CONDITION_ORDER) - 1)] if _rcond in CONDITION_ORDER else _rcond
                            $ _rmat = 8 + EQUIPMENT_DEFS[_it]["tier"] * 4
                            frame:
                                xfill True
                                background "#1a2230"
                                padding (16, 12, 16, 12)
                                hbox:
                                    spacing 14
                                    xfill True
                                    vbox:
                                        spacing 5
                                        xsize 610
                                        text EQUIPMENT_DEFS[_it]["name"] font PROFILE_FONT size 17 color "#cfe0f5"
                                        hbox:
                                            spacing 18
                                            text ("Condition %s" % _rcond) font ACT_FONT size 14 color "#7a9ab8"
                                            text ("Materials $%d" % _rmat) font ACT_FONT size 14 color "#9fb6d6"
                                            text "Time 1.5h" font ACT_FONT size 14 color "#7a9ab8"
                                        hbox:
                                            spacing 18
                                            text ("Chance %d%%" % _rc["success_or_better"]) font ACT_FONT size 15 color "#5bcafa"
                                            text ("Would become %s" % _rnext) font ACT_FONT size 15 color "#7fd06a"
                                    button:
                                        action Return(("restore", _it))
                                        yalign 0.5
                                        xalign 1.0
                                        background "#1e3a5f"
                                        padding (16, 8)
                                        text "Restore" font ACT_FONT size 15 color "#5bcafa" hover_color "#ffffff" xalign 0.5
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (24, 10)
                text "Close" font PROFILE_FONT size 16 color "#5bcafa" hover_color "#ffffff"


# Return contract for mech_job_scr:
#   "diagnose" | "replace" | "repair" | None (back). Caller compares with ==,
#   so an unexpected bool falls through to the no-op return rather than crashing.
screen mech_job_scr(job_id):
    modal True
    zorder 220
    add "#000000cc"
    $ _j = next((j for j in mech_jobs if j["id"] == job_id), None)
    frame:
        xalign 0.5 yalign 0.5
        xsize 540
        background "#12161ef8"
        padding (24, 20, 24, 22)
        if _j is None:
            vbox:
                spacing 10
                text "Job no longer available." font ACT_FONT size 14 color "#cfe0f5"
                textbutton "Close" action Return(None) text_font ACT_FONT text_size 13 text_color "#5bcafa"
        else:
            $ _jc = mech_repair_chance(_j)
            vbox:
                spacing 10
                text _j["name"] font PROFILE_FONT size 17 color "#cfe0f5" xalign 0.5
                text ("Difficulty %d  ·  Pays $%d on success" % (_j["difficulty"], _j["reward"])) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                null height 4
                # Replace (safe)
                button:
                    action Return("replace")
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10)
                    vbox:
                        spacing 2
                        hbox:
                            xfill True
                            text "Replace the part" font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                            text "Guaranteed" font PROFILE_FONT size 12 color "#7fd06a" yalign 0.5 xalign 1.0
                        text ("Buy part: $%d  ·  0.5h  ·  net $%+d" % (_j["replace"], _j["reward"] - _j["replace"])) font ACT_FONT size 11 color "#7a9ab8"
                # Repair (risky)
                button:
                    action Return("repair")
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10)
                    vbox:
                        spacing 2
                        hbox:
                            xfill True
                            text "Attempt the repair" font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                            text ("%d%%" % _jc["success_or_better"]) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                        text ("Materials: $%d  ·  %.2gh  ·  Mechanics XP either way" % (_j["materials"], 1.0 + 0.25 * _j["difficulty"])) font ACT_FONT size 11 color "#7a9ab8"
                        for _lbl, _val in _jc["modifier_lines"]:
                            text ("%s  %+d%%" % (_lbl, _val)) font ACT_FONT size 10 color ("#7fd06a" if _val >= 0 else "#e07a6a")
                # Diagnose
                if _j["diagnosable"] and _j["id"] not in _mech_diagnosed:
                    $ _before = _jc["success_or_better"]
                    $ _after = calculate_check_chance("mech_" + _j["id"], skill_val("mech"), _mech_engine_difficulty(_j["difficulty"]), _mech_repair_mods(_j) + [("Diagnosis", _MECH_DIAGNOSIS_BASE + equipment_modifier("tools", "diagnosis"))])["success_or_better"]
                    button:
                        action Return("diagnose")
                        xfill True
                        background "#1a2a3a"
                        hover_background "#1e3a5f"
                        padding (14, 10)
                        vbox:
                            spacing 2
                            text "Diagnose first (1h)" font ACT_FONT size 14 color "#cfe0f5"
                            text ("Repair odds: %d%% → %d%%" % (_before, _after)) font ACT_FONT size 11 color "#7fd06a"
                null height 4
                button:
                    action Return(None)
                    xalign 0.5
                    background "#1e3a5f"
                    padding (18, 7)
                    text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# Return contract for mech_restore_scr: "restore" | None (back).
screen mech_restore_scr(item_id):
    modal True
    zorder 220
    add "#000000cc"
    $ _d = EQUIPMENT_DEFS[item_id]
    $ _rc = restore_equipment_chance(item_id)
    $ _mat = 8 + _d["tier"] * 4
    frame:
        xalign 0.5 yalign 0.5
        xsize 520
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text ("Restore %s" % _d["name"]) font PROFILE_FONT size 17 color "#cfe0f5" xalign 0.5
            text ("Condition: %s" % equipment_condition_of(item_id)) font ACT_FONT size 13 color "#7a9ab8" xalign 0.5
            null height 4
            button:
                action Return("restore")
                xfill True
                background "#1a2a3a"
                hover_background "#1e3a5f"
                padding (14, 10)
                vbox:
                    spacing 2
                    hbox:
                        xfill True
                        text "Attempt restoration" font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                        text ("%d%%" % _rc["success_or_better"]) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                    text ("Materials: $%d  ·  1.5h  ·  success raises condition one step" % _mat) font ACT_FONT size 11 color "#7a9ab8"
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"
