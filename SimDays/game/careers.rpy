# Careers + professional skills (technical scaffold).
# Core stats (STR/INT/CHR/APP) are 0-100. Professional skills are 0-10 and are
# LEARNED (college courses, on-the-job). Careers have rank ladders gated by both.
# This defines the data + helpers; the Performance-bar loop from jobs_system.md
# plugs in on top later.

init python:
    # key -> (label, colour, bar-fill key). 0-10 scale. Reuses existing bar fills
    # so we don't need 7 new colour assets yet.
    PRO_SKILLS = {
        "med":  ("Medicine",    "#ff6f61", "str"),
        "prog": ("Programming", "#4db1ff", "int"),
        "biz":  ("Business",    "#ffd23f", "chr"),
        "cook": ("Cooking",     "#ff9f4d", "hunger"),
        "fit":  ("Fitness",     "#8fd94f", "energy"),
        "mech": ("Mechanics",   "#9aa5b5", "perf"),
        "art":  ("Art",         "#c07bff", "app"),
        "music": ("Music",      "#ff7fb0", "app"),
    }

    SKILL_LEVEL_BENEFITS = {
        "prog": {
            2:  [("Project energy cost", "-3%"),  ("Next unlock", "Basic freelance at level 3")],
            3:  [("Basic freelance", "Unlocked"), ("Next unlock", "Improved pay range at level 4")],
            4:  [("Contract pay range", "+8%"),   ("Next unlock", "Intermediate contracts at level 5")],
            5:  [("Intermediate contracts", "Unlocked (requires portfolio)"), ("Next unlock", "Efficiency at level 6")],
            6:  [("Project energy cost", "-3% more"), ("Next unlock", "Professional contracts at level 7")],
            7:  [("Professional contracts", "Unlocked"), ("Next unlock", "Better clients at level 8")],
            8:  [("Client tier", "Improved"),     ("Next unlock", "Major projects at level 9")],
            9:  [("Major projects", "Unlocked"),  ("Next unlock", "Expert status at level 10")],
            10: [("Expert status", "Achieved"),   ("Freelance capstone", "Available")],
        },
        "music": {
            2:  [("Practice XP", "+5% ordinary training"), ("Next unlock", "Park busking at level 3")],
            3:  [("Park busking", "Unlocked"),   ("Next unlock", "Better tips at level 4")],
            4:  [("Busking tips", "+8%"),        ("Next unlock", "Open Mic at level 5")],
            5:  [("Open Mic", "Unlocked"),       ("Next unlock", "Energy efficiency at level 6")],
            6:  [("Music practice energy", "-3%"), ("Next unlock", "Paid performances at level 7")],
            7:  [("Paid performances", "Unlocked"), ("Next unlock", "More followers at level 8")],
            8:  [("Follower gain", "+10%"),      ("Next unlock", "Major events at level 9")],
            9:  [("Major events", "Unlocked"),   ("Next unlock", "Music capstone at level 10")],
            10: [("Music capstone", "Available"), ("Expert status", "Achieved")],
        },
        "med": {
            2:  [("Medical study XP", "+5%"),       ("Next unlock", "Hospital assistant role at level 2+")],
            3:  [("Diagnosis accuracy", "+5%"),     ("Next unlock", "Clinic procedures at level 4")],
            4:  [("Procedure efficiency", "+5%"),   ("Next unlock", "Advanced study at level 5")],
            5:  [("Advanced courses", "Unlocked"),  ("Next unlock", "Shift income at level 6")],
            6:  [("Shift performance gain", "+5%"), ("Next unlock", "Specialist role at level 7")],
            7:  [("Specialist procedures", "Unlocked"), ("Next unlock", "Research at level 8")],
            8:  [("Research XP", "+5%"),            ("Next unlock", "Senior role at level 9")],
            9:  [("Senior cases", "Unlocked"),      ("Next unlock", "Chief role at level 10")],
            10: [("Chief of Medicine", "Achievable"), ("Medical mastery", "Complete")],
        },
        "biz": {
            2:  [("Negotiation efficiency", "+3%"),  ("Next unlock", "Corporate role at level 1+")],
            3:  [("Business analysis", "+5%"),       ("Next unlock", "Strategy courses at level 4")],
            4:  [("Strategy courses", "Unlocked"),   ("Next unlock", "Management XP at level 5")],
            5:  [("Management techniques", "Improved"), ("Next unlock", "Finance skills at level 6")],
            6:  [("Finance efficiency", "+5%"),      ("Next unlock", "Executive track at level 7")],
            7:  [("Executive leadership", "Unlocked"), ("Next unlock", "Network at level 8")],
            8:  [("Network bonuses", "+5%"),         ("Next unlock", "Director track at level 9")],
            9:  [("Director role", "Achievable"),    ("Next unlock", "Business mastery at level 10")],
            10: [("Business mastery", "Complete"),   ("Director", "Achievable")],
        },
        "cook": {
            2:  [("Meal XP", "+5%"),             ("Next unlock", "New recipes at level 3")],
            3:  [("Intermediate meals", "Unlocked"), ("Next unlock", "Cook efficiency at level 4")],
            4:  [("Cooking efficiency", "+5%"),  ("Next unlock", "Culinary courses at level 5")],
            5:  [("Advanced culinary", "Unlocked"), ("Next unlock", "Professional at level 6")],
            6:  [("Professional techniques", "+5% meal XP"), ("Next unlock", "Sous chef at level 6+")],
            7:  [("Advanced dishes", "Unlocked"), ("Next unlock", "Gourmet at level 8")],
            8:  [("Gourmet meals", "Unlocked"),  ("Next unlock", "Head chef track at level 9")],
            9:  [("Head chef role", "Achievable"), ("Next unlock", "Culinary mastery at level 10")],
            10: [("Culinary mastery", "Complete"), ("Signature dish", "Achievable")],
        },
        "fit": {
            2:  [("Workout XP", "+5%"),          ("Next unlock", "Trainer assistant at level 1+")],
            3:  [("Training programs", "Improved"), ("Next unlock", "Advanced workouts at level 4")],
            4:  [("Advanced training", "Unlocked"), ("Next unlock", "Performance at level 5")],
            5:  [("Performance training", "Unlocked"), ("Next unlock", "Trainer rank at level 5+")],
            6:  [("Elite methods", "+5% XP"),    ("Next unlock", "Head trainer track at level 7")],
            7:  [("Head trainer", "Achievable"), ("Next unlock", "Athletic mastery at level 8")],
            8:  [("Athletic coaching", "+5%"),   ("Next unlock", "Elite athlete at level 9")],
            9:  [("Elite programs", "Unlocked"), ("Next unlock", "Fitness mastery at level 10")],
            10: [("Fitness mastery", "Complete"), ("Personal record", "Achievable")],
        },
        "mech": {
            2:  [("Paid repair jobs", "Unlocked — clients bring you fix-it work"),
                 ("Repair time", "-3%"),         ("Next unlock", "Advanced diagnostics at level 3")],
            3:  [("Diagnostics", "Improved"),    ("Next unlock", "Vehicle systems at level 4")],
            4:  [("Vehicle systems", "Unlocked"), ("Next unlock", "Efficiency at level 5")],
            5:  [("Repair efficiency", "+5%"),   ("Next unlock", "Advanced mechanics at level 6")],
            6:  [("Advanced repairs", "Unlocked"), ("Next unlock", "Master tech at level 7")],
            7:  [("Master techniques", "Unlocked"), ("Next unlock", "Specialist at level 8")],
            8:  [("Specialist repairs", "+5%"),  ("Next unlock", "Expert at level 9")],
            9:  [("Expert diagnostics", "Unlocked"), ("Next unlock", "Master technician at level 10")],
            10: [("Master technician", "Achieved"), ("Certification", "Available")],
        },
        "art": {
            2:  [("Art XP", "+5%"),              ("Next unlock", "Commissions at level 3")],
            3:  [("Commission work", "Unlocked"), ("Next unlock", "Style at level 4")],
            4:  [("Personal style", "+5% quality"), ("Next unlock", "Gallery at level 5")],
            5:  [("Gallery submissions", "Unlocked"), ("Next unlock", "Advanced techniques at level 6")],
            6:  [("Advanced techniques", "+5% XP"), ("Next unlock", "Professional at level 7")],
            7:  [("Professional commissions", "Unlocked"), ("Next unlock", "Exhibition at level 8")],
            8:  [("Exhibition access", "Unlocked"), ("Next unlock", "Master at level 9")],
            9:  [("Master works", "Unlocked"),   ("Next unlock", "Art mastery at level 10")],
            10: [("Art mastery", "Complete"),    ("Signature work", "Achievable")],
        },
    }

    def skill_val(key):
        return getattr(store, "skill_" + key)

    # XP thresholds per level (index = current level, value = XP needed to reach next).
    # Total: 20+35+55+85+125+180+250+340+460+650 = 2200 XP to Lv 10.
    _SKILL_XP = [20, 35, 55, 85, 125, 180, 250, 340, 460, 650]

    def skill_exp_needed(level):
        return _SKILL_XP[level] if level < len(_SKILL_XP) else 9999

    # ── Mastery gates ─────────────────────────────────────────────────────
    # Gates without "source_prefix" are placeholder-only (auto-open, non-blocking).
    SKILL_GATES = {
        "prog": {
            3:  {"desc": "Complete your first freelance project",              "source_prefix": "fl_complete"},
            5:  {"desc": "Complete an intermediate freelance project (4h+)",   "source_prefix": "fl_intermediate"},
            7:  {"desc": "Complete a high-tier freelance contract (skill 6+)", "source_prefix": "fl_hightier"},
            9:  {"desc": "Complete a major programming contract (skill 9+)",   "source_prefix": "fl_major"},
            10: {"desc": "Complete the programming capstone",                  "source_prefix": "fl_capstone"},
        },
        # Music: content-gated by activity availability, NOT skill gates.
        # Busking: Guitar>=1 + own guitar. Open Mic: Guitar>=4 + rep>=8. Gates are placeholder.
        "music": {
            3:  {"desc": "Busking improves tip range at Guitar 3"},
            5:  {"desc": "Open Mic accessible at Guitar 4 + Rep 8"},
            7:  {"desc": "Paid booking unlocks at Guitar 6 + Rep 20"},
            9:  {"desc": "Major performance at Guitar 9 + Rep 60"},
            10: {"desc": "Complete the music capstone"},
        },
        # Placeholder gates (no source_prefix = auto-open, non-blocking for now)
        "med":  {3: {"desc": "Clinical milestone"}, 5: {"desc": "Clinical milestone"}, 7: {"desc": "Clinical milestone"}, 9: {"desc": "Clinical milestone"}, 10: {"desc": "Medical mastery"}},
        "biz":  {3: {"desc": "Business milestone"}, 5: {"desc": "Business milestone"}, 7: {"desc": "Business milestone"}, 9: {"desc": "Business milestone"}, 10: {"desc": "Business mastery"}},
        "cook": {3: {"desc": "Culinary milestone"}, 5: {"desc": "Culinary milestone"}, 7: {"desc": "Culinary milestone"}, 9: {"desc": "Culinary milestone"}, 10: {"desc": "Culinary mastery"}},
        "fit":  {3: {"desc": "Fitness milestone"},  5: {"desc": "Fitness milestone"},  7: {"desc": "Fitness milestone"},  9: {"desc": "Fitness milestone"},  10: {"desc": "Fitness mastery"}},
        "mech": {3: {"desc": "Mechanics milestone"},5: {"desc": "Mechanics milestone"},7: {"desc": "Mechanics milestone"},9: {"desc": "Mechanics milestone"},10: {"desc": "Mechanics mastery"}},
        "art":  {3: {"desc": "Art milestone"},      5: {"desc": "Art milestone"},      7: {"desc": "Art milestone"},      9: {"desc": "Art milestone"},      10: {"desc": "Art mastery"}},
    }
    _GATED_LEVELS = {3, 5, 7, 9, 10}

    def skill_gate_required(key, level):
        """Returns gate dict (with source_prefix) or None if no blocking gate."""
        g = SKILL_GATES.get(key, {}).get(level)
        if g is None: return None
        if not g.get("source_prefix"): return None  # placeholder = auto-open
        return g

    def skill_gate_completed(key, level):
        """True if the gate for key@level is passed (or there is no gate)."""
        g = skill_gate_required(key, level)
        if g is None: return True
        prefix = "%s_%d_" % (key, level)
        return any(k.startswith(prefix) for k in store.skill_gates_completed)

    def complete_skill_gate(key, level, source_id):
        """Record gate completion. source_id must be unique per triggering event."""
        gate_key = "%s_%d_%s" % (key, level, source_id)
        if gate_key not in store.skill_gates_completed:
            d = dict(store.skill_gates_completed)
            d[gate_key] = True
            store.skill_gates_completed = d

    def skill_gate_description(key, level):
        g = SKILL_GATES.get(key, {}).get(level)
        return g.get("desc", "") if g else ""

    def gain_skill(key, amt=1):
        var = "skill_" + key
        lvl = getattr(store, var)
        if lvl >= 10:
            return
        store.skill_exp[key] = store.skill_exp.get(key, 0) + amt
        leveled = 0
        while lvl < 10 and store.skill_exp[key] >= skill_exp_needed(lvl):
            next_lvl = lvl + 1
            if next_lvl in _GATED_LEVELS and not skill_gate_completed(key, next_lvl):
                break  # gate blocks level-up; XP accumulates
            store.skill_exp[key] -= skill_exp_needed(lvl)
            lvl += 1
            leveled += 1
        setattr(store, var, lvl)
        if lvl >= 10:
            store.skill_exp[key] = 0
        label, colour, fillkey = PRO_SKILLS[key]
        icon_path = "images/ui/icons/skill_%s.png" % key
        icon_arg = icon_path if renpy.loadable(icon_path) else None
        if leveled:
            _push_gain(kind="stat", text="%s  Lv %d!" % (label, lvl), color=colour,
                       icon=icon_arg, value=lvl * 10,
                       fill="images/ui/bar_fill_%s.png" % fillkey)
            # Queue level-up notice for display in script context
            _benefits = SKILL_LEVEL_BENEFITS.get(key, {}).get(lvl, [])
            _notices = list(store._pending_levelup_notices)
            _notices.append({"key": key, "label": label, "new_level": lvl, "benefits": _benefits})
            store._pending_levelup_notices = _notices
        else:
            new_exp = store.skill_exp.get(key, 0)
            need    = skill_exp_needed(lvl)
            _push_gain(kind="stat", text="+%d EXP  %s" % (amt, label), color=colour,
                       icon=icon_arg, value=int(new_exp * 100 // max(need, 1)),
                       fill="images/ui/bar_fill_%s.png" % fillkey)
        # Phase 56: record event for day summary
        record_game_event("skill_%s_day%d" % (key, store.day), "skill", label,
                          summary=True,
                          metadata={"key": key, "xp": amt, "new_level": lvl, "leveled": leveled > 0})

    # Career ladders. req keys are store var names (stat_* /100, skill_* /10).
    # flex=True at the top tier = flexible hours (the freedom payoff).
    CAREERS = {
        "hospital": {
            "name": "Medicine - City Hospital", "location": "location_hospital",
            "ranks": [
                {"title": "Clinical Assistant", "req": {"skill_med": 2, "stat_int": 30, "stat_chr": 15},              "pay": 80,  "hours": "Mon-Fri 08-16", "flex": False, "trial": "hospital_trial_resident"},
                {"title": "Resident",          "req": {"skill_med": 5, "stat_int": 45, "degree": "med_bach"},  "pay": 140, "hours": "long shifts",   "flex": False},
                {"title": "Doctor",            "req": {"skill_med": 7, "stat_int": 58, "degree": "med_mast"},  "pay": 240, "hours": "shifts",        "flex": False},
                {"title": "Attending",         "req": {"skill_med": 8, "stat_int": 68, "stat_chr": 45},        "pay": 350, "hours": "mostly set",    "flex": False},
                {"title": "Chief of Medicine", "req": {"skill_med": 9, "stat_int": 78, "stat_chr": 60},        "pay": 480, "hours": "flexible",      "flex": True},
            ],
        },
        "it": {
            "name": "IT - The Hub", "location": "location_hub",
            "ranks": [
                {"title": "Junior Dev",   "req": {"skill_prog": 2, "stat_int": 30},                                          "pay": 100, "hours": "Mon-Fri 09-17", "flex": False},
                {"title": "Mid Dev",      "req": {"skill_prog": 3, "stat_int": 40},                                         "pay": 155, "hours": "Mon-Fri 09-17", "flex": False},
                {"title": "Senior Dev",   "req": {"skill_prog": 5, "stat_int": 55, "stat_chr": 25, "degree": "prog_bach"},  "pay": 230, "hours": "some leeway",  "flex": False, "trial": "it_trial_team_lead"},
                {"title": "Team Lead",    "req": {"skill_prog": 7, "stat_int": 65, "stat_chr": 40, "degree": "prog_mast"},  "pay": 310, "hours": "mostly flex",  "flex": True},
                {"title": "Eng. Manager", "req": {"skill_prog": 8, "stat_int": 75, "stat_chr": 55}, "pay": 400, "hours": "flexible",     "flex": True},
            ],
        },
        "corporate": {
            "name": "Corporate - Nexus Tower", "location": "location_office",
            "ranks": [
                {"title": "Intern",    "req": {"skill_biz": 1, "stat_int": 20, "stat_chr": 20, "stat_app": 20},                      "pay": 85,  "hours": "Mon-Fri 09-18", "flex": False},
                {"title": "Associate", "req": {"skill_biz": 3, "stat_int": 35, "stat_chr": 35},               "pay": 145, "hours": "Mon-Fri 09-18", "flex": False},
                {"title": "Analyst",   "req": {"skill_biz": 5, "stat_int": 50, "stat_chr": 45, "degree": "biz_bach"},  "pay": 220, "hours": "long", "flex": False},
                {"title": "Manager",   "req": {"skill_biz": 7, "stat_int": 55, "stat_chr": 60, "degree": "biz_mast"}, "pay": 310, "hours": "mostly flex",   "flex": True},
                {"title": "Director",  "req": {"skill_biz": 9, "stat_int": 60, "stat_chr": 75},  "pay": 430, "hours": "flexible",      "flex": True},
            ],
        },
        "trainer": {
            "name": "Personal Trainer - Iron Gate", "location": "location_gym",
            "ranks": [
                {"title": "Assistant Trainer", "req": {"skill_fit": 1, "stat_str": 25, "stat_app": 25}, "pay": 65,  "hours": "book clients", "flex": True},
                {"title": "Trainer",           "req": {"skill_fit": 4, "stat_str": 45, "stat_app": 40}, "pay": 115, "hours": "book clients", "flex": True},
                {"title": "Head Trainer",      "req": {"skill_fit": 7, "stat_str": 60, "stat_chr": 45}, "pay": 190, "hours": "flexible",     "flex": True},
            ],
        },
        "culinary": {
            "name": "Kitchen - Eleven", "location": "location_kitchen",
            "ranks": [
                {"title": "Commis",     "req": {"skill_cook": 1, "stat_str": 20},              "pay": 85,  "hours": "evenings",  "flex": False},
                {"title": "Line Cook",  "req": {"skill_cook": 3, "stat_str": 35},              "pay": 135, "hours": "evenings",  "flex": False},
                {"title": "Sous Chef",  "req": {"skill_cook": 6, "stat_str": 45, "stat_chr": 30}, "pay": 220, "hours": "long",   "flex": False},
                {"title": "Head Chef",  "req": {"skill_cook": 9, "stat_str": 55, "stat_chr": 45}, "pay": 340, "hours": "runs the pass", "flex": False},
            ],
        },
    }

    # ── Career arc progress ────────────────────────────────────────────────

    def career_arc_progress(cid):
        """Returns (completed_steps, total_steps) for a career's preview arc."""
        _arc_flags = {
            "corporate": ["martha_met", "corp_task_1_done", "corp_martha_1_done", "corp_martha_2_done", "corp_review_intern_done"],
            "it":        ["eli_met", "it_task_1_done", "it_npc1_done", "it_npc2_done", "it_review_done"],
            "hospital":  ["lena_met", "hosp_task_1_done", "hosp_npc1_done", "hosp_npc2_done", "hosp_review_done"],
            "culinary":  ["rena_met", "cul_task_1_done", "cul_npc1_done", "cul_npc2_done", "cul_review_done"],
            "trainer":   ["kai_met", "tr_task_1_done", "tr_npc1_done", "tr_npc2_done", "tr_review_done"],
        }
        flags = _arc_flags.get(cid, [])
        if not flags:
            return (0, 0)
        done = sum(1 for f in flags if getattr(store, f, False))
        return (done, len(flags))

    # ── Career performance threshold notifications ──────────────────────────

    def career_rank(cid):
        """Current rank index for cid (0-based), from active_careers."""
        return store.active_careers.get(cid, {}).get("rank", 0)

    def career_perf(cid):
        """Current performance 0-100 for cid, from active_careers."""
        return store.active_careers.get(cid, {}).get("perf", 0)

    def _check_career_perf_threshold(perf, cid=None):
        """Notify player when career performance crosses key thresholds (once per rank)."""
        if cid is None:
            cid = store.job_id
        if cid is None:
            return
        _rank = store.active_careers.get(cid, {}).get("rank", 0)
        seen = dict(store.career_perf_thresholds_seen)
        msgs = {50: "Your work is being noticed.", 80: "You're close to a review.", 100: "You're ready for a promotion."}
        changed = False
        for thresh, msg in msgs.items():
            key = (cid, _rank, thresh)
            if key not in seen and perf >= thresh:
                seen[key] = True
                changed = True
                renpy.notify(msg)
        if changed:
            store.career_perf_thresholds_seen = seen

    def meets_req(req):
        for k, v in req.items():
            if k == "degree":
                if v not in store.degrees:
                    return False
            else:
                val = eff_app() if k == "stat_app" else getattr(store, k, 0)
                if val < v:
                    return False
        return True

    # ── Job engine ─────────────────────────────────────────────────────
    # Which stats/skills a shift slowly trains: (kind, key, chance).
    CAREER_TRAIN = {
        "it":        [("stat", "int", 0.5), ("skill", "prog", 0.55)],
        "hospital":  [("stat", "int", 0.3), ("skill", "med",  0.45)],
        "corporate": [("stat", "chr", 0.4), ("skill", "biz",  0.50)],
        "trainer":   [("stat", "str", 0.4), ("skill", "fit",  0.45)],
        "culinary":  [("stat", "str", 0.3), ("skill", "cook", 0.50)],
    }

    def cur_rank(cid=None):
        if cid is None: cid = store.job_id
        if cid is None: return None
        _r = store.active_careers.get(cid, {}).get("rank", 0)
        return CAREERS[cid]["ranks"][_r]

    def _sync_job(cid=None):
        """Sync job_id/job_rank/job_performance display vars from active_careers.
        cid forces a specific career to become the 'active' display career."""
        if cid is not None:
            store.job_id = cid
        if store.job_id is None or store.job_id not in store.active_careers:
            _remaining = list(store.active_careers.keys())
            store.job_id = _remaining[-1] if _remaining else None
        if store.job_id is None:
            store.job_title = None; store.job_next = ""; store.job_schedule = ""
            store.job_rank = 0; store.job_performance = 0
            return
        _career = store.active_careers[store.job_id]
        store.job_rank = _career["rank"]
        store.job_performance = _career["perf"]
        ranks = CAREERS[store.job_id]["ranks"]
        r = ranks[store.job_rank]
        short = CAREERS[store.job_id]["name"].split(" - ")[0]
        store.job_title = "%s - %s" % (r["title"], short)
        store.job_schedule = r["hours"]
        store.job_next = next_rank_hint(ranks[store.job_rank + 1]["req"]) if store.job_rank + 1 < len(ranks) else "(top rank)"

    def can_apply(cid):
        return cid not in store.active_careers and meets_req(CAREERS[cid]["ranks"][0]["req"])

    def apply_job(cid):
        _ac = dict(store.active_careers)
        _ac[cid] = {"rank": 0, "perf": 0}
        store.active_careers = _ac
        _sync_job(cid)

    def quit_job(cid=None):
        if cid is None: cid = store.job_id
        _ac = {k: v for k, v in store.active_careers.items() if k != cid}
        store.active_careers = _ac
        _sync_job()

    def _migrate_career_entry(entry):
        """Ensure old save entries have all new tracking fields."""
        entry = dict(entry)
        entry.setdefault("total_shifts", 0)
        entry.setdefault("rank_shifts", 0)
        entry.setdefault("joined_day", store.day)
        entry.setdefault("last_shift_day", -1)
        return entry

    def do_shift(cid, hours, perf_override=None):
        store.stat_boost_str = 1.0  # supplements are gym-only
        _ac = dict(store.active_careers)
        _career = _migrate_career_entry(_ac.get(cid, {"rank": 0, "perf": 0}))
        r = CAREERS[cid]["ranks"][_career["rank"]]
        spend_time(hours)
        gain_money(r["pay"])
        # spend_time already applies energy decay; extra cost reflects physical demand
        store.need_energy = max(0, store.need_energy - int(hours * 3))
        low = worn_out()
        # Apply workplace context bonus once per career per day (Task 7 guard)
        _ctx_mod = 0
        if store.workplace_context_applied.get(cid) != store.day:
            _ctx = workplace_daily_context(cid)
            if _ctx:
                _ctx_mod = _ctx.get("perf_mod", 0)
            _wca = dict(store.workplace_context_applied)
            _wca[cid] = store.day
            store.workplace_context_applied = _wca
        if perf_override is not None:
            perf_gain = max(1, perf_override // 2) if low else perf_override
        else:
            perf_gain = (6 if low else 13) + _ctx_mod
        _career["perf"] = min(100, _career["perf"] + perf_gain)
        _check_career_perf_threshold(_career["perf"], cid)
        at_cap = _career["perf"] >= 100
        if not low:
            for kind, key, chance in CAREER_TRAIN.get(cid, []):
                # at performance cap: double skill chance (overflow reward)
                effective_chance = min(0.95, chance * 2) if at_cap else chance
                if renpy.random.random() < effective_chance:
                    if kind == "stat": gain_stat(key, 8)
                    else: gain_skill(key, 5)
        _career["total_shifts"] = _career.get("total_shifts", 0) + 1
        _career["rank_shifts"]  = _career.get("rank_shifts",  0) + 1
        _career["last_shift_day"] = store.day
        _ac[cid] = _career
        store.active_careers = _ac
        _sync_job(cid)   # focus on just-worked career so arc scripts see correct job_rank
        return low

    # Minimum shifts at current rank before promotion is allowed.
    _RANK_SHIFT_REQ = [3, 6, 10, 15, 20]  # rank 0→1, 1→2, 2→3, 3→4, 4→5

    def can_promote(cid=None):
        if cid is None: cid = store.job_id
        if cid is None: return False
        _career = _migrate_career_entry(store.active_careers.get(cid, {}))
        if _career.get("perf", 0) < 100: return False
        ranks = CAREERS[cid]["ranks"]
        cur_rank = _career.get("rank", 0)
        if cur_rank + 1 >= len(ranks): return False
        if not meets_req(ranks[cur_rank + 1]["req"]): return False
        req_shifts = _RANK_SHIFT_REQ[cur_rank] if cur_rank < len(_RANK_SHIFT_REQ) else 20
        return _career.get("rank_shifts", 0) >= req_shifts

    def promote(cid=None):
        if cid is None: cid = store.job_id
        if not can_promote(cid): return False
        _ac = dict(store.active_careers)
        _career = _migrate_career_entry(dict(_ac.get(cid, {"rank": 0, "perf": 0})))
        _career["rank"] += 1
        _career["perf"] = 0
        _career["rank_shifts"] = 0  # reset counter for next rank
        _ac[cid] = _career
        store.active_careers = _ac
        _sync_job(cid)
        # Phase 56: record promotion event
        record_game_event(
            "promote_%s_r%d_day%d" % (cid, _career["rank"], store.day),
            "career", "Promoted: " + (store.job_title or cid),
            summary=True, journal=True,
            metadata={"cid": cid, "new_rank": _career["rank"]})
        # Phase 68: promotions travel. Word of mouth grants Respect only —
        # never Affection (see PUBLIC_FACT_TEMPLATES).
        publish_player_fact("got_promoted", "%s_r%d" % (cid, _career["rank"]))
        return True

    # ── Probabilistic promotion system (Phase 60C erratum) ───────────────────
    # Complements the arc-based narrative promotions.
    # Uses active_careers data (rank, perf, rank_shifts) — no separate store vars needed.
    PROMOTION_REQUIREMENTS = {
        "it": [
            {"req_skill": {"prog": 3}, "req_performance": 55, "req_shifts_at_rank": 4,  "base_chance": 0.15},
            {"req_skill": {"prog": 5}, "req_performance": 65, "req_shifts_at_rank": 6,  "base_chance": 0.10},
            {"req_skill": {"prog": 7}, "req_performance": 72, "req_shifts_at_rank": 10, "base_chance": 0.07, "opportunity_only": True},
            {"req_skill": {"prog": 9}, "req_performance": 80, "req_shifts_at_rank": 15, "base_chance": 0.05, "opportunity_only": True},
        ],
        "corporate": [
            {"req_skill": {"biz": 3}, "req_performance": 55, "req_shifts_at_rank": 4,  "base_chance": 0.15},
            {"req_skill": {"biz": 5}, "req_performance": 65, "req_shifts_at_rank": 6,  "base_chance": 0.10},
            {"req_skill": {"biz": 7}, "req_performance": 72, "req_shifts_at_rank": 10, "base_chance": 0.07, "opportunity_only": True},
            {"req_skill": {"biz": 9}, "req_performance": 80, "req_shifts_at_rank": 15, "base_chance": 0.05, "opportunity_only": True},
        ],
        "hospital": [
            {"req_skill": {"med": 3}, "req_performance": 55, "req_shifts_at_rank": 4,  "base_chance": 0.15},
            {"req_skill": {"med": 5}, "req_performance": 65, "req_shifts_at_rank": 6,  "base_chance": 0.10},
            {"req_skill": {"med": 7}, "req_performance": 72, "req_shifts_at_rank": 10, "base_chance": 0.07, "opportunity_only": True},
            {"req_skill": {"med": 9}, "req_performance": 80, "req_shifts_at_rank": 15, "base_chance": 0.05, "opportunity_only": True},
        ],
        "culinary": [
            {"req_skill": {"cook": 3}, "req_performance": 55, "req_shifts_at_rank": 4,  "base_chance": 0.15},
            {"req_skill": {"cook": 5}, "req_performance": 65, "req_shifts_at_rank": 6,  "base_chance": 0.10},
            {"req_skill": {"cook": 7}, "req_performance": 72, "req_shifts_at_rank": 10, "base_chance": 0.07, "opportunity_only": True},
            {"req_skill": {"cook": 9}, "req_performance": 80, "req_shifts_at_rank": 15, "base_chance": 0.05, "opportunity_only": True},
        ],
        "trainer": [
            {"req_skill": {"fit": 2}, "req_performance": 50, "req_shifts_at_rank": 4,  "base_chance": 0.15},
            {"req_skill": {"fit": 4}, "req_performance": 62, "req_shifts_at_rank": 6,  "base_chance": 0.10},
            {"req_skill": {"fit": 6}, "req_performance": 70, "req_shifts_at_rank": 10, "base_chance": 0.07, "opportunity_only": True},
            {"req_skill": {"fit": 8}, "req_performance": 78, "req_shifts_at_rank": 15, "base_chance": 0.05, "opportunity_only": True},
        ],
    }

    def _promo_career_data(cid):
        return _migrate_career_entry(store.active_careers.get(cid, {}))

    def promotion_chance(career_id):
        """Returns float 0..1 if eligible, else None. Uses active_careers data."""
        cid  = career_id
        data = _promo_career_data(cid)
        rank = data.get("rank", 0)
        reqs_list = PROMOTION_REQUIREMENTS.get(cid, [])
        if rank >= len(reqs_list): return None    # already at max rank for this system

        req  = reqs_list[rank]
        perf = data.get("perf", 0)
        rank_shifts = data.get("rank_shifts", 0)

        for sk, min_lv in req["req_skill"].items():
            if skill_val(sk) < min_lv: return None
        if perf < req["req_performance"]: return None
        if rank_shifts < req["req_shifts_at_rank"]: return None

        chance = req["base_chance"]
        sk_name, sk_req = list(req["req_skill"].items())[0]
        sk_margin = skill_val(sk_name) - sk_req
        chance += min(0.12, max(0, sk_margin) / 40.0)   # /40 cap at 12%

        # Absolute performance tiers, independent of eligibility threshold
        if   perf >= 95: chance += 0.10
        elif perf >= 85: chance += 0.06
        elif perf >= 75: chance += 0.03

        extra_shifts = rank_shifts - req["req_shifts_at_rank"]
        chance += min(0.05, max(0, extra_shifts) * 0.01)

        chance += min(0.15, data.get("promotion_pity", 0) * 0.02)
        return min(0.35, chance)

    def promotion_chance_breakdown(career_id):
        """Returns list of (label, pct_int) for UI."""
        cid  = career_id
        data = _promo_career_data(cid)
        rank = data.get("rank", 0)
        req  = PROMOTION_REQUIREMENTS[cid][rank]
        sk_name, sk_req = list(req["req_skill"].items())[0]
        lines = [("Base eligibility", int(req["base_chance"] * 100))]
        sk_margin = skill_val(sk_name) - sk_req
        if sk_margin > 0:
            skill_pct = int(min(0.12, sk_margin / 40.0) * 100)
            lines.append(("Skill above requirement", skill_pct))
        perf = data.get("perf", 0)
        if   perf >= 95: lines.append(("Exceptional performance", 10))
        elif perf >= 85: lines.append(("Strong performance", 6))
        elif perf >= 75: lines.append(("Good performance", 3))
        extra_shifts = data.get("rank_shifts", 0) - req["req_shifts_at_rank"]
        tenure_pct = min(5, max(0, extra_shifts))
        if tenure_pct > 0:
            lines.append(("Experience at rank", tenure_pct))
        pity_pct = min(15, data.get("promotion_pity", 0) * 2)
        if pity_pct > 0:
            lines.append(("Management consideration", pity_pct))
        return lines

    def promotion_requirements_status(career_id):
        """Returns list of (label, met_bool, detail_str) for pre-roll display."""
        cid  = career_id
        data = _promo_career_data(cid)
        rank = data.get("rank", 0)
        reqs_list = PROMOTION_REQUIREMENTS.get(cid, [])
        if rank >= len(reqs_list): return []
        req  = reqs_list[rank]
        out  = []
        for sk, min_lv in req["req_skill"].items():
            cur = skill_val(sk)
            out.append(("%s %d required" % (PRO_SKILLS.get(sk, (sk,))[0], min_lv),
                        cur >= min_lv, "you have %d" % cur))
        perf = data.get("perf", 0)
        out.append(("Performance %d" % req["req_performance"],
                    perf >= req["req_performance"], "you have %d" % perf))
        rs = data.get("rank_shifts", 0)
        out.append(("%d shifts at rank" % req["req_shifts_at_rank"],
                    rs >= req["req_shifts_at_rank"], "you have %d" % rs))
        return out

    def do_promotion_roll(career_id):
        """Returns ('not_eligible', None) | ('rolled', result_dict)."""
        chance = promotion_chance(career_id)
        if chance is None:
            return "not_eligible", None
        data = _promo_career_data(cid=career_id)
        rank = data.get("rank", 0)
        req  = PROMOTION_REQUIREMENTS[career_id][rank]
        import random as _r
        roll = _r.randint(1, 100)
        threshold = max(1, int(chance * 100))
        success   = roll <= threshold
        _ac = dict(store.active_careers)
        _c  = dict(_ac.get(career_id, {}))
        if success:
            _c["promotion_pity"] = 0
            # Narrative/arc labels call promote() separately; for opp_only we set a pending flag.
            if req.get("opportunity_only"):
                store.pending_promotion_opportunity = {
                    "career_id": career_id, "expires_day": store.day + 3}
        else:
            _c["promotion_pity"] = _c.get("promotion_pity", 0) + 1
        _ac[career_id] = _c
        store.active_careers = _ac
        return "rolled", {
            "success":          success,
            "roll":             roll,
            "threshold":        threshold,
            "opportunity_only": req.get("opportunity_only", False),
            "chance_pct":       threshold,
        }

    # ── Career skill map ──────────────────────────────────────────────────────
    _CAREER_SKILL = {
        "it": "prog", "corporate": "biz", "hospital": "med",
        "culinary": "cook", "trainer": "fit",
    }
    # Minimum skill level required to even apply for a role
    _CAREER_MIN_SKILL = {
        "it": 3, "corporate": 3, "hospital": 4, "culinary": 2, "trainer": 2,
    }

    def promotion_check_chance(career_id):
        """Returns calculate_check_chance result for promotion interview."""
        cid = career_id
        rank    = store.active_careers.get(cid, {}).get("rank", 0)
        perf    = store.active_careers.get(cid, {}).get("perf", 0)
        shifts  = store.active_careers.get(cid, {}).get("rank_shifts", 0)
        sk      = _CAREER_SKILL.get(cid, "biz")
        sk_val  = skill_val(sk)
        mods = [
            ("Performance",   min(25, int((perf - 60) * 0.5))),
            ("Career skill",  min(18, int(sk_val * 2.5))),
            ("Shifts at rank", min(10, shifts // 5)),
        ]
        if has_player_state("confident"):  mods.append(("Confident", +5))
        if has_player_state("stressed"):   mods.append(("Stressed",  -6))
        if getattr(store, "promo_prepared_" + cid, False):
            mods.append(("Interview prep", +8))
        return calculate_check_chance("promotion_" + cid, sk_val=0, difficulty=40, modifiers=mods)

    def attempt_promotion(career_id):
        """Roll the promotion check. Returns (success, result_dict)."""
        ch = promotion_check_chance(career_id)
        mods = [(l, v) for l, v in ch["modifier_lines"]
                if l not in ("Skill", "Difficulty", "Prev. experience")]
        result = roll_check("promotion_" + career_id, skill_val=0, difficulty=40,
                            modifiers=mods, stable=False)
        success = result["tier"] in ("success", "great", "critical")
        if success:
            promote(career_id)
        return success, result

    def job_interview_chance(career_id):
        """Returns (chance_data, mods) for a job interview roll."""
        sk      = _CAREER_SKILL.get(career_id, "biz")
        sk_val  = skill_val(sk)
        req_sk  = _CAREER_MIN_SKILL.get(career_id, 3)
        mods = []
        if store.player_portfolio:
            mods.append(("Portfolio", min(10, len(store.player_portfolio) * 2)))
        if getattr(store, "interview_prepared_" + career_id, False):
            mods.append(("Interview prep", +10))
        if has_player_state("confident"):  mods.append(("Confident", +6))
        if has_player_state("stressed"):   mods.append(("Stressed",  -5))
        if store.need_energy < 40:         mods.append(("Tired",     -6))
        difficulty = max(30, 40 + (req_sk - sk_val) * 8)
        return calculate_check_chance("interview_" + career_id, sk_val, difficulty, mods), mods

    def attempt_job_interview(career_id):
        """Roll the interview. Returns (passed, result_dict). Does NOT call apply_job()."""
        ch, mods = job_interview_chance(career_id)
        sk    = _CAREER_SKILL.get(career_id, "biz")
        sk_val = skill_val(sk)
        req_sk = _CAREER_MIN_SKILL.get(career_id, 3)
        difficulty = max(30, 40 + (req_sk - sk_val) * 8)
        result = roll_check("interview_" + career_id, sk_val, difficulty,
                            modifiers=mods, stable=False)
        passed = result["tier"] != "critical_failure"
        # Reset prep flag on attempt
        setattr(store, "interview_prepared_" + career_id, False)
        return passed, result

    def raise_request_chance(career_id, amount_pct=1.05):
        """amount_pct: 1.05=5% raise, 1.15=15% etc. Returns (chance_data, error_str|None)."""
        cid = career_id
        perf   = store.active_careers.get(cid, {}).get("perf", 0)
        rank   = store.active_careers.get(cid, {}).get("rank", 0)
        last_raise = getattr(store, "last_raise_day_" + cid, -99)
        days_since = store.day - last_raise
        if days_since < 14:
            return None, "Too soon since last raise (%d days left)." % (14 - days_since)
        biz = skill_val("biz")
        mods = [
            ("Performance",  min(20, int((perf - 60) * 0.5))),
            ("Business",     min(8, biz * 2)),
            ("Tenure",       min(8, days_since // 7)),
        ]
        if amount_pct >= 1.15: mods.append(("High ask",     -20))
        elif amount_pct >= 1.10: mods.append(("Moderate ask", -10))
        return calculate_check_chance("raise_" + cid, 0, 50, mods), None

    DEGREE_EXAMS = {
        "med_bach":  {"skill": "med",  "min_lvl": 4, "cost": 500,  "hours": 8, "label": "Medicine — Bachelor's"},
        "med_mast":  {"skill": "med",  "min_lvl": 7, "cost": 1300, "hours": 8, "label": "Medicine — Master's"},
        "prog_bach": {"skill": "prog", "min_lvl": 4, "cost": 400,  "hours": 8, "label": "CS — Bachelor's"},
        "prog_mast": {"skill": "prog", "min_lvl": 7, "cost": 1100, "hours": 8, "label": "CS — Master's"},
        "biz_bach":  {"skill": "biz",  "min_lvl": 4, "cost": 450,  "hours": 8, "label": "Business — Bachelor's"},
        "biz_mast":  {"skill": "biz",  "min_lvl": 7, "cost": 1200, "hours": 8, "label": "Business — Master's"},
    }

    _BACH_REQ = {
        "med_mast":  "med_bach",
        "prog_mast": "prog_bach",
        "biz_mast":  "biz_bach",
    }

    def can_sit_exam(deg_id):
        e = DEGREE_EXAMS[deg_id]
        prereq = _BACH_REQ.get(deg_id)
        if prereq and prereq not in store.degrees:
            return False
        # Study is an essential — allowed while in debt (still needs the cash).
        return (deg_id not in store.degrees
                and skill_val(e["skill"]) >= e["min_lvl"]
                and store.money >= e["cost"])

    def sit_exam(deg_id):
        e = DEGREE_EXAMS[deg_id]
        # Charge BEFORE spend_time: an 8h exam can roll past DAY_END into a Monday,
        # whose rent debit could create a loan and make the later charge get refused
        # while the degree was granted anyway. can_sit_exam already ensured funds.
        gain_money(-e["cost"], "study")
        spend_time(e["hours"])
        store.degrees = store.degrees + [deg_id]

    # ── One-time course tiers (4 per skill, each earnable once) ──────────────
    COURSE_TIERS = {
        "prog": [
            {"id": "prog_intro",   "name": "Intro to Programming",    "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "prog_inter",   "name": "Intermediate Development", "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "prog_adv",     "name": "Advanced Programming",     "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "prog_master",  "name": "System Architecture",      "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "med": [
            {"id": "med_intro",   "name": "Medical Fundamentals",       "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "med_inter",   "name": "Clinical Methods",           "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "med_adv",     "name": "Advanced Clinical Practice", "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "med_master",  "name": "Medical Specialisation",     "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "biz": [
            {"id": "biz_intro",   "name": "Business Basics",      "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "biz_inter",   "name": "Strategy & Operations", "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "biz_adv",     "name": "Corporate Finance",     "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "biz_master",  "name": "Executive Leadership",  "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "cook": [
            {"id": "cook_intro",   "name": "Kitchen Fundamentals",    "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "cook_inter",   "name": "Culinary Techniques",     "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "cook_adv",     "name": "Advanced Gastronomy",     "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "cook_master",  "name": "Professional Chef Mastery","min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "fit": [
            {"id": "fit_intro",   "name": "Fitness Foundations",        "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "fit_inter",   "name": "Training Science",           "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "fit_adv",     "name": "Performance Training",       "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "fit_master",  "name": "Elite Athletic Programming", "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "mech": [
            {"id": "mech_intro",   "name": "Auto Basics",          "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "mech_inter",   "name": "Vehicle Systems",      "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "mech_adv",     "name": "Advanced Diagnostics", "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "mech_master",  "name": "Master Technician",    "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "art": [
            {"id": "art_intro",   "name": "Visual Arts Foundation",   "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "art_inter",   "name": "Composition & Colour",     "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "art_adv",     "name": "Advanced Studio Practice", "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "art_master",  "name": "Fine Art Mastery",         "min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
        "music": [
            {"id": "music_intro",   "name": "Music Theory",            "min": 0, "max": 3, "cost": 60,  "hours": 3, "xp": 30},
            {"id": "music_inter",   "name": "Performance Techniques",  "min": 2, "max": 5, "cost": 120, "hours": 3, "xp": 50},
            {"id": "music_adv",     "name": "Advanced Musicianship",   "min": 4, "max": 7, "cost": 220, "hours": 4, "xp": 80},
            {"id": "music_master",  "name": "Professional Performance","min": 6, "max": 9, "cost": 400, "hours": 5, "xp": 110},
        ],
    }

    def available_courses(key):
        """Courses for this skill that are unlocked by level and not yet completed."""
        lvl = skill_val(key)
        return [c for c in COURSE_TIERS.get(key, [])
                if c["id"] not in store.completed_courses
                and c["min"] <= lvl <= c["max"]]

    def take_course_by_id(course_id):
        """Take a specific course by ID. Returns 'ok'/'money'/'done'/'notfound'."""
        for key, tiers in COURSE_TIERS.items():
            for c in tiers:
                if c["id"] == course_id:
                    if course_id in store.completed_courses:
                        return "done"
                    discount = 0.7 if has_event("college_sale") else 1.0
                    cost = int(c["cost"] * discount)
                    if store.money < cost:
                        return "money"
                    gain_money(-cost, "study")
                    spend_time(c["hours"])
                    gain_skill(key, c["xp"])
                    store.need_energy = max(0, store.need_energy - 22)
                    store.completed_courses = list(store.completed_courses) + [course_id]
                    return "ok"
        return "notfound"

    def course_cost(key):
        """Cost of the next available course for key (respects college_sale)."""
        courses = available_courses(key)
        if not courses: return 0
        discount = 0.7 if has_event("college_sale") else 1.0
        return int(courses[0]["cost"] * discount)

    def set_career_perf(cid, value):
        """Set performance for cid to an exact value (used by trial-fail resets)."""
        if cid not in store.active_careers:
            return False
        _ac = dict(store.active_careers)
        _c  = dict(_ac[cid])
        _c["perf"] = max(0, min(100, value))
        _ac[cid] = _c
        store.active_careers = _ac
        if store.job_id == cid:
            store.job_performance = _c["perf"]
        return True

    def take_course(key):
        """Legacy API — delegates to first available tier course."""
        courses = available_courses(key)
        if not courses:
            return "max" if skill_val(key) >= 10 else "done"
        return take_course_by_id(courses[0]["id"])

    # ── Daily diminishing returns for repeatable practice ────────────────────

    def _training_effective_xp(key, base_xp, hours=1):
        """Scale XP based on training hours logged today for this skill.
        Call only for ordinary repeatable practice, not career shifts or story events.
        ponytail: O(1) dict lookup; ceiling = you can't grind past 6h/day effectively."""
        if store.daily_activity_load_day != store.day:
            store.daily_activity_load = {}
            store.daily_activity_load_day = store.day
        h = store.daily_activity_load.get(key, 0)
        d = dict(store.daily_activity_load)
        d[key] = h + hours
        store.daily_activity_load = d
        if h < 2:   return base_xp
        if h < 4:   return int(base_xp * 0.70)
        if h < 6:   return int(base_xp * 0.40)
        return max(1, int(base_xp * 0.15))

    def _update_skill_routine(key):
        """Track consecutive-day practice streaks. Grace: 1-day gap allowed."""
        routines = dict(store.skill_routines)
        entry = dict(routines.get(key, {"streak": 0, "last_day": -1}))
        if entry["last_day"] == store.day:
            return  # already counted today
        if store.day - entry["last_day"] <= 2:
            entry["streak"] = entry.get("streak", 0) + 1
        else:
            entry["streak"] = 1  # reset
        entry["last_day"] = store.day
        routines[key] = entry
        store.skill_routines = routines

    def _routine_bonus(key):
        """Returns XP multiplier from practice streak. 1.0 = no bonus.
        ponytail: max +10%; upgrade path = higher tiers for 30/60-day streaks."""
        streak = store.skill_routines.get(key, {}).get("streak", 0)
        if streak >= 14: return 1.10
        if streak >= 7:  return 1.06
        if streak >= 3:  return 1.03
        return 1.0

    def current_practice_efficiency(key):
        """Returns efficiency percentage string for display, e.g. '70%'."""
        if store.daily_activity_load_day != store.day:
            return "100%"
        h = store.daily_activity_load.get(key, 0)
        if h < 2:   return "100%"
        if h < 4:   return "70%"
        if h < 6:   return "40%"
        return "15%"

    def apply_skill_prog_energy_modifier():
        """Returns energy cost multiplier from prog level. 1.0 = no reduction."""
        lvl = skill_val("prog")
        reduction = 0.03 * (1 if lvl >= 2 else 0) + 0.03 * (1 if lvl >= 6 else 0)
        return max(0.85, 1.0 - reduction)

    def apply_skill_music_energy_modifier():
        """Returns energy cost multiplier from music level."""
        lvl = skill_val("music")
        reduction = 0.03 * (1 if lvl >= 2 else 0) + 0.03 * (1 if lvl >= 6 else 0)
        return max(0.85, 1.0 - reduction)

    def freelance_pay_modifier():
        """Multiplier on freelance pay from prog level. Level 4: +8%."""
        lvl = skill_val("prog")
        return 1.08 if lvl >= 4 else 1.0

    def get_next_skill_unlock(key):
        """Returns description of next locked skill benefit, or None."""
        lvl = skill_val(key)
        benefits = SKILL_LEVEL_BENEFITS.get(key, {})
        for lv in sorted(benefits.keys()):
            if lv > lvl:
                for desc, val in benefits[lv]:
                    if ("unlock" in desc.lower() or "Unlocked" in val
                            or "Achievable" in val or "Available" in val):
                        return "%s at level %d" % (val, lv)
        return None

    def gain_skill_practice(key, base_xp, hours=1):
        """For ordinary repeatable training — applies daily diminishing returns + streak bonus + player state.
        Also runs learning breakthrough check; bonus XP applied immediately, notification via renpy.notify()."""
        effective = _training_effective_xp(key, base_xp, hours)
        bonus = _routine_bonus(key)
        effective = max(1, int(effective * bonus))
        # Player state XP bonuses
        if key in ("prog", "biz") and active_player_state_effect("prog_biz_xp") > 0:
            effective = max(1, int(effective * (1.0 + active_player_state_effect("prog_biz_xp"))))
        elif key in ("art", "music") and active_player_state_effect("art_music_xp") > 0:
            effective = max(1, int(effective * (1.0 + active_player_state_effect("art_music_xp"))))
        # Learning breakthrough (5-8% chance; bonus XP added directly)
        _bt_bonus = _check_learning_breakthrough(key, effective)
        gain_skill(key, effective + _bt_bonus)
        _update_skill_routine(key)
        return effective

    def next_rank_hint(req):
        """Human-readable shortfall for the profile 'Next:' line."""
        parts = []
        for k, v in req.items():
            if k == "degree":
                parts.append(v.replace("_", " ").title())
            else:
                nice = k.replace("stat_", "").replace("skill_", "").upper()
                parts.append("%s %d" % (nice, v))
        return ", ".join(parts)
