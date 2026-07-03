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

    def gain_skill(key, amt=1):
        """Raise a professional skill (0-10) and flash a toast (reuses gains.py)."""
        var = "skill_" + key
        new = min(10, getattr(store, var) + amt)
        setattr(store, var, new)
        label, colour, fillkey = PRO_SKILLS[key]
        icon = "images/ui/icons/skill_%s.png" % key
        _push_gain(kind="stat", text="+%d %s" % (amt, label), color=colour,
                   icon=(icon if renpy.loadable(icon) else None),
                   value=new * 10, fill="images/ui/bar_fill_%s.png" % fillkey)

    # Career ladders. req keys are store var names (stat_* /100, skill_* /10).
    # flex=True at the top tier = flexible hours (the freedom payoff).
    CAREERS = {
        "hospital": {
            "name": "Medicine - City Hospital", "location": "location_hospital",
            "ranks": [
                {"title": "Med Student",       "req": {"skill_med": 1, "stat_int": 20},              "pay": 40,  "hours": "Mon-Fri 08-16", "flex": False},
                {"title": "Resident",          "req": {"skill_med": 3, "stat_int": 35},              "pay": 90,  "hours": "long shifts",   "flex": False},
                {"title": "Doctor",            "req": {"skill_med": 5, "stat_int": 50},              "pay": 160, "hours": "shifts",        "flex": False},
                {"title": "Attending",         "req": {"skill_med": 7, "stat_int": 60, "stat_chr": 40}, "pay": 240, "hours": "mostly set", "flex": False},
                {"title": "Chief of Medicine", "req": {"skill_med": 9, "stat_int": 70, "stat_chr": 55}, "pay": 340, "hours": "flexible",   "flex": True},
            ],
        },
        "it": {
            "name": "IT - The Hub", "location": "location_hub",
            "ranks": [
                {"title": "Junior Dev",   "req": {"skill_prog": 1, "stat_int": 25},               "pay": 70,  "hours": "Mon-Fri 09-17", "flex": False},
                {"title": "Mid Dev",      "req": {"skill_prog": 3, "stat_int": 40},               "pay": 120, "hours": "Mon-Fri 09-17", "flex": False},
                {"title": "Senior Dev",   "req": {"skill_prog": 5, "stat_int": 55, "stat_chr": 25}, "pay": 190, "hours": "some leeway",  "flex": False},
                {"title": "Team Lead",    "req": {"skill_prog": 7, "stat_int": 65, "stat_chr": 40}, "pay": 260, "hours": "mostly flex",  "flex": True},
                {"title": "Eng. Manager", "req": {"skill_prog": 8, "stat_int": 75, "stat_chr": 55}, "pay": 340, "hours": "flexible",     "flex": True},
            ],
        },
        "corporate": {
            "name": "Corporate - Nexus Tower", "location": "location_office",
            "ranks": [
                {"title": "Intern",    "req": {"skill_biz": 1, "stat_int": 20, "stat_chr": 20},  "pay": 50,  "hours": "Mon-Fri 09-18", "flex": False},
                {"title": "Associate", "req": {"skill_biz": 3, "stat_int": 35, "stat_chr": 35},  "pay": 110, "hours": "Mon-Fri 09-18", "flex": False},
                {"title": "Analyst",   "req": {"skill_biz": 5, "stat_int": 50, "stat_chr": 45},  "pay": 180, "hours": "long",          "flex": False},
                {"title": "Manager",   "req": {"skill_biz": 7, "stat_int": 55, "stat_chr": 60},  "pay": 260, "hours": "mostly flex",   "flex": True},
                {"title": "Director",  "req": {"skill_biz": 9, "stat_int": 60, "stat_chr": 75},  "pay": 380, "hours": "flexible",      "flex": True},
            ],
        },
        "trainer": {
            "name": "Personal Trainer - Iron Gate", "location": "location_gym",
            "ranks": [
                {"title": "Assistant Trainer", "req": {"skill_fit": 1, "stat_str": 25, "stat_app": 25}, "pay": 45, "hours": "book clients", "flex": True},
                {"title": "Trainer",           "req": {"skill_fit": 4, "stat_str": 45, "stat_app": 40}, "pay": 100, "hours": "book clients", "flex": True},
                {"title": "Head Trainer",      "req": {"skill_fit": 7, "stat_str": 60, "stat_chr": 45}, "pay": 170, "hours": "flexible",     "flex": True},
            ],
        },
        "culinary": {
            "name": "Kitchen - Eleven", "location": "location_restaurant",
            "ranks": [
                {"title": "Commis",     "req": {"skill_cook": 1, "stat_str": 20},              "pay": 55,  "hours": "evenings",  "flex": False},
                {"title": "Line Cook",  "req": {"skill_cook": 3, "stat_str": 35},              "pay": 100, "hours": "evenings",  "flex": False},
                {"title": "Sous Chef",  "req": {"skill_cook": 6, "stat_str": 45, "stat_chr": 30}, "pay": 165, "hours": "long",   "flex": False},
                {"title": "Head Chef",  "req": {"skill_cook": 9, "stat_str": 55, "stat_chr": 45}, "pay": 250, "hours": "runs the pass", "flex": False},
            ],
        },
        "warehouse": {
            "name": "LogiCity Warehouse", "location": "location_warehouse",
            "ranks": [
                {"title": "Floor Worker",     "req": {"stat_str": 25},                          "pay": 90,  "hours": "Mon-Sat 07-15", "flex": False},
                {"title": "Crew Lead",        "req": {"stat_str": 45, "skill_mech": 3},         "pay": 140, "hours": "Mon-Sat 07-15", "flex": False},
                {"title": "Shift Supervisor", "req": {"stat_str": 55, "skill_mech": 6, "stat_chr": 30}, "pay": 200, "hours": "set shifts", "flex": False},
            ],
        },
    }

    def meets_req(req):
        return all(getattr(store, k, 0) >= v for k, v in req.items())

    # ── Job engine ─────────────────────────────────────────────────────
    # Which stats/skills a shift slowly trains: (kind, key, chance).
    CAREER_TRAIN = {
        "it":        [("stat", "int", 0.5), ("skill", "prog", 0.3)],
        "hospital":  [("stat", "int", 0.4), ("skill", "med", 0.3)],
        "corporate": [("stat", "chr", 0.4), ("skill", "biz", 0.3)],
        "trainer":   [("stat", "str", 0.4), ("skill", "fit", 0.3)],
        "culinary":  [("stat", "str", 0.3), ("skill", "cook", 0.4)],
        "warehouse": [("stat", "str", 0.5), ("skill", "mech", 0.25)],
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

    def do_shift(cid, hours):
        r = CAREERS[cid]["ranks"][store.job_rank]
        spend_time(hours)
        gain_money(r["pay"])
        # Show up wrecked and you actually LOSE ground; rested, you climb.
        low = worn_out()
        if low:
            store.job_performance = max(0, store.job_performance - 6)
        else:
            store.job_performance = min(100, store.job_performance + 13)
            for kind, key, chance in CAREER_TRAIN.get(cid, []):
                if renpy.random.random() < chance:
                    if kind == "stat": gain_stat(key, 1)
                    else: gain_skill(key, 1)
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

    def take_course(key, cost=60):
        if store.money < cost: return "money"
        if skill_val(key) >= 10:  return "max"
        spend_time(3)
        gain_money(-cost)
        gain_skill(key, 1)
        return "ok"

    def next_rank_hint(req):
        """Human-readable shortfall for the profile 'Next:' line."""
        parts = []
        for k, v in req.items():
            nice = k.replace("stat_", "").replace("skill_", "").upper()
            parts.append("%s %d" % (nice, v))
        return ", ".join(parts)
