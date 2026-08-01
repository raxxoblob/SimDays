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

    def skill_val(key):
        return getattr(store, "skill_" + key)

    def skill_exp_needed(level):
        # 18, 30, 48, 72, 102, 138, 180, 228, 282, 342
        # level 0->1 ≈ 3 courses, 1->2 ≈ 5, 2->3 ≈ 8, 3->4 ≈ 12...
        return 18 + 12 * level + 3 * level * (level - 1)

    def gain_skill(key, amt=1):
        var = "skill_" + key
        lvl = getattr(store, var)
        if lvl >= 10:
            return
        store.skill_exp[key] = store.skill_exp.get(key, 0) + amt
        leveled = 0
        while lvl < 10 and store.skill_exp[key] >= skill_exp_needed(lvl):
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
        else:
            new_exp = store.skill_exp.get(key, 0)
            need    = skill_exp_needed(lvl)
            _push_gain(kind="stat", text="+%d EXP  %s" % (amt, label), color=colour,
                       icon=icon_arg, value=int(new_exp * 100 // max(need, 1)),
                       fill="images/ui/bar_fill_%s.png" % fillkey)

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

    def _check_career_perf_threshold(perf):
        """Notify player when career performance crosses key thresholds (once per rank).
        FIX 5: key is a 3-tuple (job_id, job_rank, threshold) so hitting 80 in IT
        does not suppress the 80 notification in corporate, and each new rank resets."""
        if store.job_id is None:
            return
        seen = dict(store.career_perf_thresholds_seen)
        msgs = {50: "Your work is being noticed.", 80: "You're close to a review.", 100: "You're ready for a promotion."}
        changed = False
        for thresh, msg in msgs.items():
            key = (store.job_id, store.job_rank, thresh)
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

    def cur_rank():
        if store.job_id is None:
            return None
        return CAREERS[store.job_id]["ranks"][store.job_rank]

    def _sync_job():
        if store.job_id is None:
            store.job_title = None; store.job_next = ""; store.job_schedule = ""
            return
        ranks = CAREERS[store.job_id]["ranks"]
        r = ranks[store.job_rank]
        short = CAREERS[store.job_id]["name"].split(" - ")[0]
        store.job_title = "%s - %s" % (r["title"], short)
        store.job_schedule = r["hours"]
        store.job_next = next_rank_hint(ranks[store.job_rank + 1]["req"]) if store.job_rank + 1 < len(ranks) else "(top rank)"

    def can_apply(cid):
        return store.job_id is None and meets_req(CAREERS[cid]["ranks"][0]["req"])

    def apply_job(cid):
        store.job_id = cid; store.job_rank = 0; store.job_performance = 0
        _sync_job()

    def quit_job():
        store.job_id = None; store.job_rank = 0; store.job_performance = 0
        _sync_job()

    def do_shift(cid, hours, perf_override=None):
        store.stat_boost_str = 1.0  # supplements are gym-only
        r = CAREERS[cid]["ranks"][store.job_rank]
        spend_time(hours)
        gain_money(r["pay"])
        # spend_time already applies energy decay; extra cost reflects physical demand
        store.need_energy = max(0, store.need_energy - int(hours * 3))
        low = worn_out()
        if perf_override is not None:
            perf_gain = max(1, perf_override // 2) if low else perf_override
        else:
            perf_gain = 6 if low else 13
        store.job_performance = min(100, store.job_performance + perf_gain)
        _check_career_perf_threshold(store.job_performance)
        at_cap = store.job_performance >= 100
        if not low:
            for kind, key, chance in CAREER_TRAIN.get(cid, []):
                # at performance cap: double skill chance (overflow reward)
                effective_chance = min(0.95, chance * 2) if at_cap else chance
                if renpy.random.random() < effective_chance:
                    if kind == "stat": gain_stat(key, 8)
                    else: gain_skill(key, 5)
        _sync_job()
        return low

    def can_promote():
        if store.job_id is None or store.job_performance < 100:
            return False
        ranks = CAREERS[store.job_id]["ranks"]
        return store.job_rank + 1 < len(ranks) and meets_req(ranks[store.job_rank + 1]["req"])

    def promote():
        if not can_promote():
            return False
        store.job_rank += 1; store.job_performance = 0
        _sync_job()
        return True

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

    def course_cost(key):
        """Current discounted cost of a course (accessible in menu sensitive exprs)."""
        lvl = skill_val(key)
        base = 50 + lvl * 20
        return int(base * (0.7 if has_event("college_sale") else 1.0))

    def take_course(key):
        lvl = skill_val(key)
        if lvl >= 10: return "max"
        cost = course_cost(key)
        if store.money < cost: return "money"
        spend_time(3)
        gain_money(-cost, "study")   # study bypasses the debt gate but still costs cash
        gain_skill(key, 10)
        store.need_energy = max(0, store.need_energy - 22)
        return "ok"

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
