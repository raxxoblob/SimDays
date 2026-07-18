# Work events — story beats that fire every 2–4 shifts per career.
# Each career has a pool; unseen events are prioritised before repeating.

init python:
    def _work_event_roll(cid):
        """Increment shift counter; fire on variable cadence (skip first, then 2–4 shifts)."""
        sw = dict(store.shifts_worked)
        sw[cid] = sw.get(cid, 0) + 1
        store.shifts_worked = sw
        n = sw[cid]
        if n <= 1:
            return False
        last = store._career_event_last.get(cid, 0)
        gap  = store._career_event_gap.get(cid, 3)
        if n - last >= gap:
            d = dict(store._career_event_last); d[cid] = n;  store._career_event_last = d
            g = dict(store._career_event_gap);  g[cid] = renpy.random.randint(2, 4); store._career_event_gap = g
            return True
        return False

    def _mark_wev(cid, eid):
        d = dict(store.work_events_seen)
        lst = list(d.get(cid, []))
        if eid not in lst: lst.append(eid)
        d[cid] = lst
        store.work_events_seen = d

    def _pick_wev(cid, pool):
        seen = store.work_events_seen.get(cid, [])
        unseen = [e for e in pool if e not in seen]
        return renpy.random.choice(unseen if unseen else pool)

    def _work_perf(delta):
        # corporate_style modifiers: ambitious gets +2 on positive events when fresh;
        # reliable gets -2 damage reduction on negative events (never below 1 loss).
        if store.job_id == "corporate":
            style = store.corporate_style
            if delta > 0 and style == "ambitious" and not worn_out():
                delta += 2
            elif delta < 0 and style == "reliable":
                delta = min(-1, delta + 2)
        store.job_performance = max(0, min(100, store.job_performance + delta))

    _CAFE_POOL = [
        "wev_cafe_tray", "wev_cafe_rush", "wev_cafe_complaint",
    ]
    _IT_POOL = [
        "wev_it_prod_bug", "wev_it_pr_review",
        "wev_it_scope_creep", "wev_it_help_colleague", "wev_it_deploy_crisis",
    ]
    _CORP_POOL = [
        "wev_corp_colleague", "wev_corp_meeting", "wev_corp_complaint",
        "wev_corp_credit", "wev_corp_budget",
    ]
    _HOSP_POOL = [
        "wev_hosp_case", "wev_hosp_overtime",
        "wev_hosp_difficult_patient", "wev_hosp_shortage", "wev_hosp_near_miss",
    ]


# ── Dispatch ──────────────────────────────────────────────────────────────
label work_event_cafe:
    $ _e = _pick_wev("cafe", _CAFE_POOL)
    call expression _e
    return

label work_event_corporate:
    $ _e = _pick_wev("corporate", _CORP_POOL)
    call expression _e
    return

label work_event_hospital:
    $ _e = _pick_wev("hospital", _HOSP_POOL)
    call expression _e
    return

label work_event_it:
    $ _e = _pick_wev("it", _IT_POOL)
    call expression _e
    return


# ══ CAFE ══════════════════════════════════════════════════════════════════

label wev_cafe_tray:
    "Near the end of the shift Nora's moving too fast and drops a full tray of cups."
    show nora_cafe_sad at sprite_r
    n "Don't say anything. I know."
    menu:
        "Help her clean up.":
            n "Thanks. I owe you one."
            $ _apply_trust("nora", 3)
        "You've got the counter. She can handle it.":
            "She does. Quietly."
    hide nora_cafe_sad
    $ _mark_wev("cafe", "wev_cafe_tray")
    return

label wev_cafe_rush:
    "Fifteen minutes before close, a group of eight walks in."
    show nora_cafe_normal at sprite_r
    n "You take drinks. I'll do food. Don't let them see you panic."
    menu:
        "Stay focused. Work through it.":
            $ _work_perf(8)
            "You get through it. Everything out on time. Henry nods once — as close to praise as he gets."
        "Signal Nora for backup earlier than needed.":
            n "I've got it. Just cover the till."
            $ _apply_aff("nora", 1)
            $ _work_perf(4)
    hide nora_cafe_normal
    $ _mark_wev("cafe", "wev_cafe_rush")
    return

label wev_cafe_complaint:
    "A regular complains his coffee is wrong. It isn't."
    menu:
        "Remake it anyway.":
            $ gain_money(-3)
            $ _work_perf(5)
            "He accepts it without thanking you."
        "Explain politely that the order is correct.":
            $ _rc = renpy.random.random()
            if _rc > 0.5:
                "He reconsiders. Backs down. Doesn't apologise."
                $ _work_perf(6)
            else:
                "He escalates to Henry. Henry sides with the customer. This is the job."
                $ _work_perf(-4)
        "Offer a discount and move on.":
            $ gain_money(-2)
            $ _work_perf(3)
            "Easiest option. Not the most satisfying."
    $ _mark_wev("cafe", "wev_cafe_complaint")
    return


# ══ IT ════════════════════════════════════════════════════════════════════

label wev_it_prod_bug:
    "An alert at 14:00. Something pushed to prod this morning is failing in ways it wasn't failing this morning."
    menu:
        "Quick rollback — ship the real fix tonight.":
            $ _rc = renpy.random.random()
            if _rc > 0.4:
                $ _work_perf(12)
                $ gain_skill("prog", 3)
                "Clean rollback, fix ready by close. Your lead notices."
            else:
                $ _work_perf(-8)
                "The rollback introduces a second issue. A long afternoon."
        "Careful — reproduce first, then fix.":
            $ _work_perf(5)
            $ gain_skill("prog", 4)
            "Slower but clean. No new fires."
        "Escalate to senior.":
            $ _work_perf(-4)
            $ _apply_trust("eli", 1)
            "They handle it. You learned how."
    $ _mark_wev("it", "wev_it_prod_bug")
    return

label wev_it_pr_review:
    "Your PR gets flagged in code review. Three comments, one of them blunt."
    menu:
        "Address every point. Thank them.":
            $ _work_perf(3)
            $ _apply_trust("eli", 2)
            $ gain_skill("prog", 3)
            "The second review passes in twenty minutes."
        "Push back on the main one.":
            $ _apply_trust("eli", -1)
            $ gain_skill("prog", 2)
            "You're probably right. Doesn't matter. Pick your battles."
    $ _mark_wev("it", "wev_it_pr_review")
    return

label wev_it_scope_creep:
    "The client emails at eleven. They want a new feature. You're two-thirds done with the current sprint."
    menu:
        "Push back — this goes in the next sprint.":
            $ _rc = renpy.random.random()
            if _rc > 0.45:
                $ _work_perf(8)
                "They accept it. Your lead approves."
            else:
                $ _work_perf(-5)
                "They escalate. You get the feature anyway, on top of everything else."
        "Absorb it. Adjust the scope yourself.":
            $ spend_time(1)
            $ store.need_energy = max(0, store.need_energy - 15)
            $ _work_perf(10)
            $ gain_skill("prog", 2)
            "You fit it in. It costs you an evening."
        "Escalate to your manager.":
            $ _apply_trust("eli", 1)
            $ _work_perf(4)
            "Your lead handles the client. You handle the code."
    $ _mark_wev("it", "wev_it_scope_creep")
    return

label wev_it_help_colleague:
    "A junior on the team is stuck. You recognise the problem — you hit the same wall two weeks ago."
    menu:
        "Sit down and walk them through it.":
            $ _work_perf(-5)
            $ gain_skill("prog", 3)
            "Your own sprint takes a hit. Theirs doesn't."
        "Point them to the relevant docs.":
            $ _work_perf(2)
            "They get there eventually."
        "You're behind yourself. Tell them to ask someone else.":
            $ _work_perf(6)
            "Your work is clean. The junior figures it out alone. Slower."
    $ _mark_wev("it", "wev_it_help_colleague")
    return

label wev_it_deploy_crisis:
    "Friday, 16:45. Production deploy starts. Something immediately breaks."
    "It's yours. You pushed twenty minutes ago."
    menu:
        "Own it. Stay and fix it properly.":
            $ spend_time(2)
            $ store.need_energy = max(0, store.need_energy - 20)
            $ _work_perf(15)
            $ gain_skill("prog", 5)
            "You leave at nine. The fix is clean. Nobody emails you over the weekend."
        "Quick patch — get it stable, fix properly Monday.":
            $ _rc = renpy.random.random()
            if _rc > 0.5:
                $ _work_perf(8)
                "It holds. Monday comes, the real fix goes in."
            else:
                $ _work_perf(-10)
                "The patch fails at midnight. On-call gets paged. Your Monday starts with a meeting."
        "Hand it to on-call. It's technically their problem now.":
            $ _work_perf(-12)
            $ _apply_trust("eli", -3)
            "Technically, yes. Nobody forgets."
    $ _mark_wev("it", "wev_it_deploy_crisis")
    return


# ══ CORPORATE ═════════════════════════════════════════════════════════════

label wev_corp_colleague:
    show martha_neutral at sprite_r
    ma "Hendricks is swamped. His report is due at five. He won't make it."
    menu:
        "Cover for him — finish it yourself.":
            ma "That's above and beyond."
            $ _work_perf(-6)
            $ _apply_trust("martha", 3)
            "You lose an hour but Hendricks owes you one."
        "Not your problem. You have your own deadline.":
            "You do. You hit it. Hendricks misses his."
    hide martha_neutral
    $ _mark_wev("corporate", "wev_corp_colleague")
    return

label wev_corp_meeting:
    show caroline_normal at sprite_r
    caro "Boardroom. Five minutes. Stratford wants an update on the Kellner account."
    "You haven't looked at the Kellner account this week."
    menu:
        "Wing it.":
            $ _rc = renpy.random.random()
            if _rc > 0.5:
                caro "...Actually not terrible."
                $ _work_perf(8)
            else:
                caro "We'll circle back. With actual numbers next time."
                $ _work_perf(-5)
        "Ask Martha quietly for the key figures first.":
            ma "Margin's at 14. Three open items. Go."
            $ _work_perf(-4)
            $ _apply_trust("martha", 2)
            "You survive."
    hide caroline_normal
    $ _mark_wev("corporate", "wev_corp_meeting")
    return

label wev_corp_complaint:
    show caroline_normal at sprite_r
    caro "Harmon's client is escalating. They're asking for whoever handled their account."
    "That's you."
    menu:
        "Take the call. Stay professional.":
            $ _apply_trust("caroline", 2)
            "An unpleasant twenty minutes. They calm down. You handled it."
        "Forward it to the junior.":
            caro "Careful with that."
            $ _work_perf(5)
            $ _apply_trust("caroline", -3)
    hide caroline_normal
    $ _mark_wev("corporate", "wev_corp_complaint")
    return

label wev_corp_credit:
    show martha_neutral at sprite_r
    "In the morning briefing, Reeves presents the restructuring idea you floated last week."
    "Word for word. Your idea. His mouth."
    menu:
        "Say nothing. Note it.":
            "You do."
            $ _work_perf(0)
        "Interrupt and clarify the origin.":
            "The room notices. Reeves doesn't apologise."
            $ _work_perf(-5)
            $ _apply_trust("caroline", 1)
            "Caroline saw. That's enough."
        "Talk to Martha about it after.":
            ma "He does this. I'll make sure Stratford hears your name next time."
            $ _apply_trust("martha", 4)
    hide martha_neutral
    $ _mark_wev("corporate", "wev_corp_credit")
    return

label wev_corp_budget:
    show caroline_normal at sprite_r
    caro "Fifteen percent cut, effective next month. Something from your project has to go."
    "She's looking at you."
    menu:
        "Protect the junior — cut the vendor contract instead.":
            caro "Creative. I'll see what I can do."
            $ _apply_trust("caroline", 3)
            $ _work_perf(-5)
        "Keep the senior. Cut the junior.":
            "The project stays stable. Nobody's happy."
            $ _work_perf(5)
        "Suggest shifting the cost to another project.":
            caro "That's someone else's problem. Do better."
            $ _apply_trust("caroline", -4)
            $ _work_perf(4)
    hide caroline_normal
    $ _mark_wev("corporate", "wev_corp_budget")
    return


# ══ HOSPITAL ══════════════════════════════════════════════════════════════

label wev_hosp_case:
    show drlena_normal at sprite_r
    lena "Room 4 is unusual. Presentation doesn't match the chart."
    menu:
        "Consult Lena.":
            lena "Good instinct. Here's what I'd check."
            $ _work_perf(-5)
            $ _apply_trust("lena", 3)
        "Handle it yourself.":
            $ _rc = renpy.random.random()
            if _rc > 0.55:
                "You get it right. Lena reviews your notes later and says nothing — which is approval."
                $ _work_perf(8)
            else:
                "Your call is off. Lena corrects it quietly, which is the professional version of a problem."
                $ _work_perf(-8)
    hide drlena_normal
    $ _mark_wev("hospital", "wev_hosp_case")
    return

label wev_hosp_overtime:
    show drlena_normal at sprite_r
    lena "We're short tonight. Four more hours if you can do it."
    menu:
        "Stay.":
            $ gain_money(60)
            $ store.need_energy = max(0, store.need_energy - 20)
            $ _work_perf(5)
            "Four more hours. You leave when the city is dark and quiet."
        "Can't tonight.":
            lena "Understood."
    hide drlena_normal
    $ _mark_wev("hospital", "wev_hosp_overtime")
    return

label wev_hosp_difficult_patient:
    show drlena_normal at sprite_r
    lena "Room 9 is refusing the procedure. They're your patient. Talk to them."
    "The patient is scared, not irrational. They just need someone to actually explain it."
    menu:
        "Use logic. Walk through the clinical reasoning.":
            $ _rc = renpy.random.random()
            if _rc > 0.5:
                $ _work_perf(8)
                $ gain_skill("med", 2)
                "They come around. It takes half an hour."
            else:
                $ _work_perf(-3)
                "They need more time. Lena takes over."
        "Use empathy. Sit with their fear first.":
            $ _work_perf(6)
            $ gain_skill("med", 2)
            $ gain_stat("chr", 8)
            "It takes longer but they agree. Lena watches from the door."
        "Call Lena in directly.":
            lena "I'll handle it."
            $ _apply_trust("lena", 1)
            $ _work_perf(-3)
    hide drlena_normal
    $ _mark_wev("hospital", "wev_hosp_difficult_patient")
    return

label wev_hosp_shortage:
    "The pharmacy flags a supply issue — the medication for three patients isn't in stock."
    "It won't arrive until morning. You have options, but none are simple."
    menu:
        "Use the approved alternative.":
            $ _work_perf(6)
            $ gain_skill("med", 2)
            "It works. You document everything carefully."
        "Wait for the restock. Adjust care plans.":
            $ _work_perf(-5)
            "Safe. Slow. The patients aren't happy."
        "Spend an hour calling pharmacies across the city.":
            $ spend_time(1)
            $ store.need_energy = max(0, store.need_energy - 10)
            $ _work_perf(10)
            $ gain_skill("med", 3)
            "You find it. Two pharmacies away. Lena hears about it the next morning."
    $ _mark_wev("hospital", "wev_hosp_shortage")
    return

label wev_hosp_near_miss:
    "You catch it before it reaches the patient. Wrong dosage on a chart — yours."
    "No harm done. But five minutes later and it would have been different."
    menu:
        "Report it formally through incident review.":
            $ _work_perf(-8)
            $ gain_skill("med", 5)
            "It goes on record. Lena reads it and doesn't say much, which means something."
        "Note it in your own log. Learn from it quietly.":
            $ gain_skill("med", 2)
            "You won't make that error again."
        "Tell Lena directly.":
            show drlena_normal at sprite_r
            lena "Thank you for telling me. That's the right call."
            $ _apply_trust("lena", 4)
            $ _work_perf(-3)
            $ gain_skill("med", 3)
            hide drlena_normal
    $ _mark_wev("hospital", "wev_hosp_near_miss")
    return
