# Quest/objective system. All completion logic is derived from existing store
# variables — no separate quest state. active_quests() / completed_quests()
# are called at render time by phone_goals_scr.

init python:
    def _q(qid, title, body, show_fn, done_fn):
        return {"id": qid, "title": title, "body": body, "show": show_fn, "done": done_fn}

    # Design: exactly ONE quest is visible at the very start — the onboarding.
    # Every other quest is gated by its `show` lambda so it only appears once the
    # player has *engaged* with the relevant content (met someone, taken a job,
    # started a career track, gone into debt, …). Career-skill quests unlock by
    # taking that job. See phone_goals_scr.
    QUESTS = [
        # ── Onboarding — the only quest shown at the start of a new game ──────
        _q("onboarding",
           "Find Your Feet",
           "Settle in: head to Grounds café, meet your neighbour Marcus and the barista Nora, and pick up a shift for some cash. Zoe's around the city too — worth crossing paths.",
           lambda: True,
           lambda: store.marcus_met and store.nora_met and (store.fs_grounds_shift_done or bool(store.active_careers))),

        # ── Everything below is unlocked by playing ──────────────────────────
        _q("meet_zoe",
           "Cross Paths with Zoe",
           "Zoe turns up around the city — the park, the club, out at night. Find her.",
           lambda: (store.marcus_met or store.nora_met) and not store.zoe_met,
           lambda: store.zoe_met),

        _q("get_job",
           "Find Work",
           "Rent doesn't pay itself. Apply at Nexus Tower, The Hub, or the hospital.",
           lambda: (store.marcus_met or store.nora_met) and not store.active_careers,
           lambda: bool(store.active_careers)),

        _q("first_pay",
           "Earn Your First Paycheck",
           "Work a full shift and collect your first real paycheck.",
           lambda: bool(store.active_careers),
           lambda: any(v.get("perf", 0) >= 13 for v in store.active_careers.values())),

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
           lambda: bool(store.active_careers),
           lambda: any(v.get("rank", 0) >= 1 for v in store.active_careers.values())),

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
           lambda: bool(store.active_careers),
           lambda: store.money >= 1000 and store.loan == 0),

        _q("attend_first_commitment",
           "Keep Your Word",
           "You accepted an invitation. Show up.",
           # show when there is at least one real active commitment (npc_id in NPC_DATA filters test entries)
           lambda: any(not c["completed"] and not c["missed"] and not c.get("cancelled")
                       and c.get("npc_id") in NPC_DATA
                       for c in store.player_commitments),
           # done when a real NPC commitment (not a test stub) has been completed
           lambda: any(c["completed"] and c.get("npc_id") in NPC_DATA
                       for c in store.player_commitments)),

        _q("buy_first_home_item",
           "Make It Home",
           "Buy something that makes your apartment feel less temporary.",
           # unlocks once you've earned some income of your own (not the starting cash)
           lambda: bool(store.active_careers) or store.fs_grounds_shift_done,
           lambda: any([store.own_guitar, store.own_bed, store.own_programming_kit, store.own_coffee_machine, store.own_kitchen_set])),

        _q("recover_from_debt",
           "Back in the Black",
           "Pay off what you owe.",
           lambda: store.loan > 0 or "recover_from_debt" in store.quests_completed,
           lambda: store.loan == 0 and store.money >= 0),

        # Career-track skill goals — each unlocks only when you take that job.
        _q("prog_skill", "Sharpen Your Code",
           "You're on the IT track. Push Programming to Lv3.",
           lambda: "it" in store.active_careers,
           lambda: store.skill_prog >= 30),

        _q("biz_skill", "Learn the Business",
           "You're in the corporate world. Push Business to Lv3.",
           lambda: "corporate" in store.active_careers,
           lambda: store.skill_biz >= 30),

        _q("med_skill", "Bedside Manner",
           "You're on the medical track. Push Medicine to Lv3.",
           lambda: "hospital" in store.active_careers,
           lambda: store.skill_med >= 30),

        _q("cook_skill", "Find Your Palate",
           "You're working the kitchen. Push Cooking to Lv3.",
           lambda: "culinary" in store.active_careers,
           lambda: store.skill_cook >= 30),

        _q("fit_skill", "Train the Trainer",
           "You're coaching clients. Push Fitness to Lv3.",
           lambda: "trainer" in store.active_careers,
           lambda: store.skill_fit >= 30),

        _q("reach_mentor_trust",
           "Earn Their Trust",
           "Build real trust with a career mentor (Trust 30).",
           lambda: bool(store.active_careers),
           lambda: (
               (store.martha_met and store.martha_trust >= 30) or
               (store.eli_met    and store.eli_trust    >= 30) or
               (store.lena_met   and store.lena_trust   >= 30) or
               (store.kai_affection > 0 and store.kai_trust >= 30) or
               (store.rena_met   and store.rena_trust   >= 30)
           )),

        _q("complete_preview_arc",
           "Prove Yourself",
           "Complete your career's preview arc.",
           lambda: bool(set(store.active_careers.keys()) & {"corporate","it","hospital","culinary","trainer"}),
           lambda: any(career_arc_progress(c)[1] > 0 and career_arc_progress(c)[0] >= career_arc_progress(c)[1]
                       for c in store.active_careers)),

        _q("ready_for_promotion",
           "Time for a Promotion",
           "You're performing well. Push to 100 and request a review.",
           # show early (80) as a heads-up; done when promotion actually happens (rank increases)
           lambda: bool(store.active_careers) and any(v.get("perf", 0) >= 80 for v in store.active_careers.values()),
           lambda: any(v.get("rank", 0) > 0 for v in store.active_careers.values())),
    ]

    def _stamp_quest_if_done(q):
        """Stamp a quest as completed the first time its done() lambda fires."""
        if q["id"] not in store.quests_completed and q["done"]():
            store.quests_completed = list(store.quests_completed) + [q["id"]]

    def active_quests():
        result = []
        for q in QUESTS:
            if q["show"]():
                _stamp_quest_if_done(q)
                if q["id"] not in store.quests_completed:
                    result.append(q)
        return result

    def completed_quests():
        for q in QUESTS:
            if q["show"]():
                _stamp_quest_if_done(q)
        return [q for q in QUESTS if q["show"]() and q["id"] in store.quests_completed]
