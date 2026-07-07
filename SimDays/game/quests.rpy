# Quest/objective system. All completion logic is derived from existing store
# variables — no separate quest state. active_quests() / completed_quests()
# are called at render time by phone_goals_scr.

init python:
    def _q(qid, title, body, show_fn, done_fn):
        return {"id": qid, "title": title, "body": body, "show": show_fn, "done": done_fn}

    QUESTS = [
        _q("explore",
           "Find Your Feet",
           "Get out of the apartment. Visit the café and talk to your neighbor.",
           lambda: True,
           lambda: store.marcus_met and store.nora_met),

        _q("get_job",
           "Find Work",
           "Rent doesn't pay itself. Apply at Nexus Tower, The Hub, or the hospital.",
           lambda: store.marcus_met or store.nora_met,
           lambda: store.job_id is not None),

        _q("first_pay",
           "Earn Your First Paycheck",
           "Work a full shift and collect your first real paycheck.",
           lambda: store.job_id is not None,
           lambda: store.job_performance >= 13),

        _q("stat_30",
           "Hitting Your Stride",
           "Push STR, INT, CHR, or APP to 30 through training and socializing.",
           lambda: store.marcus_met or store.nora_met,
           lambda: max(store.stat_str, store.stat_int, store.stat_chr, store.stat_app) >= 30),

        _q("first_number",
           "Get Someone's Number",
           "Build affection to 25 with someone and ask for their number.",
           lambda: store.marcus_met or store.nora_met,
           lambda: len(store.npc_contacts) >= 1),

        _q("first_promo",
           "Move Up the Ladder",
           "Build job performance to 100 and meet the next rank's requirements.",
           lambda: store.job_id is not None,
           lambda: store.job_rank >= 1),

        _q("know_marcus",
           "Marcus Has Your Back",
           "Build your friendship with Marcus — affection 40.",
           lambda: store.marcus_met,
           lambda: store.marcus_affection >= 40),

        _q("know_nora",
           "Regular at Grounds",
           "Become a regular at the café — Nora's affection 40.",
           lambda: store.nora_met,
           lambda: store.nora_affection >= 40),

        _q("know_zoe",
           "Get to Know Zoe",
           "Spend time with Zoe and grow closer — affection 40.",
           lambda: store.zoe_met,
           lambda: store.zoe_affection >= 40),

        _q("first_date",
           "Take Someone Out",
           "Ask someone on a date — affection 30 unlocks the invite.",
           lambda: store.marcus_affection >= 28 or store.nora_affection >= 28 or store.zoe_affection >= 28,
           lambda: store.marcus_trust >= 6 or store.nora_trust >= 6 or store.zoe_trust >= 6),

        _q("financial",
           "Financial Cushion",
           "Save $1,000 with no outstanding loan.",
           lambda: store.job_id is not None,
           lambda: store.money >= 1000 and store.loan == 0),
    ]

    def active_quests():
        return [q for q in QUESTS if q["show"]() and not q["done"]()]

    def completed_quests():
        return [q for q in QUESTS if q["show"]() and q["done"]()]
