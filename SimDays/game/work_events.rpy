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

    def _work_perf(cid_or_delta, delta=None):
        # Accepts _work_perf(delta) or _work_perf("corporate", delta).
        # corporate_style modifiers: ambitious gets +2 on positive events when fresh;
        # reliable gets -2 damage reduction on negative events (never below 1 loss).
        if delta is None:
            cid   = store.job_id
            delta = cid_or_delta
        else:
            cid = cid_or_delta
        if cid is None or cid not in store.active_careers:
            return
        if cid == "corporate":
            style = store.corporate_style
            if delta > 0 and style == "ambitious" and not worn_out():
                delta += 2
            elif delta < 0 and style == "reliable":
                delta = min(-1, delta + 2)
        _ac = dict(store.active_careers)
        _c  = dict(_ac[cid])
        _c["perf"] = max(0, min(100, _c["perf"] + delta))
        _ac[cid] = _c
        store.active_careers = _ac
        store.job_performance = _c["perf"]
        _check_career_perf_threshold(_c["perf"], cid)

    def _wev_relbar_open(npc_id):
        store._rel_feedback_aff = 0
        store._rel_feedback_tr = 0
        store._rb_flash_aff = 0.0
        store._rb_flash_tr = 0.0
        store._rb_flash_aff_neg = 0.0
        store._rb_flash_tr_neg = 0.0
        store._rb_prev_aff = -1
        store._rb_prev_tr = -1
        store._npc_panel_npc_id = npc_id

    def _wev_relbar_close():
        store._npc_panel_npc_id = None

    def _pick_texture_variant(cid, variants):
        """Select a shift-texture variant for the given career.
        Prevents immediate repeat; prefers variants unseen in the last 3 days;
        falls back to least-recently-used if all are recent. Always returns."""
        last  = store.work_texture_last_variant.get(cid)
        days_outer = store.work_texture_variant_days
        days  = days_outer.get(cid, {})
        today = store.day
        candidates = [v for v in variants if v != last] or list(variants)
        fresh = [v for v in candidates if today - days.get(v, -999) > 3]
        chosen = (renpy.random.choice(fresh) if fresh
                  else min(candidates, key=lambda v: days.get(v, -999)))
        lv = dict(store.work_texture_last_variant); lv[cid] = chosen
        store.work_texture_last_variant = lv
        dout = dict(days_outer); din = dict(dout.get(cid, {})); din[chosen] = today
        dout[cid] = din; store.work_texture_variant_days = dout
        return chosen

    _CAFE_POOL = [
        "wev_cafe_tray", "wev_cafe_rush", "wev_cafe_complaint",
        "wev_cafe_machine_hot", "wev_cafe_regular_order", "wev_cafe_closing_check",
        "wev_cafe_shift_texture",
    ]
    _IT_POOL = [
        "wev_it_prod_bug", "wev_it_pr_review",
        "wev_it_scope_creep", "wev_it_help_colleague", "wev_it_deploy_crisis",
        "wev_it_eli_bug_report", "wev_it_eli_code_comment", "wev_it_eli_deploy_window",
        "wev_it_shift_texture",
    ]
    _CORP_POOL = [
        "wev_corp_colleague", "wev_corp_meeting", "wev_corp_complaint",
        "wev_corp_credit", "wev_corp_budget",
        "wev_corp_final_revision", "wev_corp_meeting_moved", "wev_corp_credit_line",
        "wev_corp_shift_texture",
    ]
    _HOSP_POOL = [
        "wev_hosp_case", "wev_hosp_overtime",
        "wev_hosp_difficult_patient", "wev_hosp_shortage", "wev_hosp_near_miss",
        "wev_hosp_read_chart_again", "wev_hosp_difficult_relative", "wev_hosp_quiet_minute",
        "wev_hosp_shift_texture",
    ]
    _WAREHOUSE_POOL = [
        "wev_warehouse_wrong_bay", "wev_warehouse_safety_vest", "wev_warehouse_early_arrival",
        "wev_warehouse_shift_texture",
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

label work_event_warehouse:
    $ _e = _pick_wev("warehouse", _WAREHOUSE_POOL)
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


# ── IT — Phase 5 Eli sprite events ────────────────────────────────────────

label wev_it_eli_bug_report:
    show eli_normal at sprite_r
    eli "You closed the bug."
    mc "It stopped reproducing."
    eli "That isn't the same sentence."
    mc "It feels close."
    eli "It won't when it comes back."
    menu:
        "Reopen it and document the cause.":
            mc "I'll reopen it."
            $ _apply_trust("eli", 1)
            eli "Good."
            eli "A solved problem should be able to explain itself."
            hide eli_normal
            $ _work_perf(4)
        "Wait and see if it returns.":
            mc "I'll wait and see if it returns."
            eli "It will."
            mc "Confident."
            eli "Experienced."
            hide eli_normal
    $ _mark_wev("it", "wev_it_eli_bug_report")
    return


label wev_it_eli_code_comment:
    show eli_normal at sprite_r
    eli "What does this function do?"
    mc "It validates the request."
    eli "I know what it does."
    mc "Then why ask?"
    eli "Because the comment says 'temporary fix.'"
    mc "It was temporary."
    eli "Three months ago."
    hide eli_normal
    $ gain_skill("prog", 2)
    $ _mark_wev("it", "wev_it_eli_code_comment")
    return


label wev_it_eli_deploy_window:
    show eli_normal at sprite_r
    eli "Deployment window opens in ten."
    mc "Everything passed."
    eli "Everything automated passed."
    mc "That's what the tests are for."
    eli "Tests confirm what we remembered to ask."
    "A notification appears on Eli's screen."
    eli "And there is the question we forgot."
    hide eli_normal
    $ _mark_wev("it", "wev_it_eli_deploy_window")
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


# ══ CORPORATE — Phase 1 additions ═════════════════════════════════════════

label wev_corp_final_revision:
    show martha_neutral at sprite_r
    ma "You saw the revised numbers?"
    mc "I saw an email titled 'Final Revision Three.'"
    ma "Then you understand how final it is."
    menu:
        "I'll update the draft.":
            $ martha_revision_choice = "update"
            mc "I'll update the draft."
            ma "Before the meeting, preferably."
            hide martha_neutral
            $ _work_perf(5)
            $ _apply_trust("martha", 1)
        "Which version are we using?":
            $ martha_revision_choice = "clarify"
            mc "Which version are we actually using?"
            ma "The one attached to the most recent email."
            mc "There are two attachments."
            ma "Of course there are."
            hide martha_neutral
    $ _mark_wev("corporate", "wev_corp_final_revision")
    return


label wev_corp_meeting_moved:
    show martha_neutral at sprite_r
    ma "The meeting moved forward."
    mc "By how much?"
    ma "Enough that your current pace is now theoretical."
    mc "When did they tell you?"
    ma "Just now."
    mc "And you're this calm?"
    ma "No."
    ma "I'm efficient."
    hide martha_neutral
    $ gain_skill("biz", 2)
    $ _mark_wev("corporate", "wev_corp_meeting_moved")
    return


label wev_corp_credit_line:
    if "wev_corp_credit" not in work_events_seen.get("corporate", []):
        return
    show martha_neutral at sprite_r
    ma "The director liked the summary."
    mc "The one I wrote?"
    ma "Unless someone else used your name."
    mc "You could just say it was good."
    ma "I could."
    "A short pause."
    ma "It was good."
    hide martha_neutral
    $ _apply_trust("martha", 1)
    $ add_relationship_memory("martha", "martha_acknowledged_work", "Martha acknowledged my work")
    $ _mark_wev("corporate", "wev_corp_credit_line")
    return


# ══ CAFE — Phase 3 additions ══════════════════════════════════════════════

label wev_cafe_machine_hot:
    $ _wev_relbar_open("nora")
    show screen npc_relbar("nora")
    show nora_cafe_talk at sprite_r
    n "The machine's running hot again."
    mc "Is that bad?"
    n "Only if customers prefer coffee to steam."
    menu:
        "Let me recalibrate it.":
            mc "Let me recalibrate it."
            n "You know how?"
            mc "I know how to look confident while checking."
            $ _apply_trust("nora", 1)
            n "Good enough. Start with the pressure."
            hide nora_cafe_talk
            $ _work_perf(6)
        "Should I stop using it?":
            mc "Should I stop using it?"
            n "Not unless you want the queue to become a protest."
            n "Use the other group head until I fix it."
            hide nora_cafe_talk
            $ _work_perf(3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ _mark_wev("cafe", "wev_cafe_machine_hot")
    return

label wev_cafe_regular_order:
    "A customer reaches the counter before Nora looks up."
    show nora_cafe_normal at sprite_r
    n "Large oat latte. Extra hot. No foam."
    mc "They haven't ordered yet."
    n "They order the same thing every Tuesday."
    "The customer begins to speak."
    mc "Large oat latte?"
    "The customer pauses, then nods."
    n "Now don't look proud. It encourages them."
    hide nora_cafe_normal
    $ _work_perf(4)
    $ _mark_wev("cafe", "wev_cafe_regular_order")
    return

label wev_cafe_closing_check:
    show nora_cafe_normal at sprite_r
    n "Before the next rush, check the back counter."
    mc "I already cleaned it."
    n "That wasn't the instruction."
    hide nora_cafe_normal
    "You check beneath the grinder."
    mc "Coffee grounds."
    n "Coffee grounds."
    mc "You knew they were there."
    n "I knew you didn't."
    $ _work_perf(3)
    $ _mark_wev("cafe", "wev_cafe_closing_check")
    return


# ══ HOSPITAL — Phase 3 additions ══════════════════════════════════════════

label wev_hosp_read_chart_again:
    show drlena_normal at sprite_r
    lena "Before you answer, read the chart again."
    mc "I did."
    lena "Then read the part you skipped."
    "You look back at the notes."
    mc "The dosage changed this morning."
    lena "There it is."
    lena "Being quick is useful after being correct."
    hide drlena_normal
    $ gain_skill("med", 2)
    $ _mark_wev("hospital", "wev_hosp_read_chart_again")
    return

label wev_hosp_difficult_relative:
    $ _wev_relbar_open("lena")
    show screen npc_relbar("lena")
    "A raised voice carries from the corridor."
    show drlena_normal at sprite_r
    mc "Should someone go out there?"
    lena "Someone already did."
    mc "Who?"
    lena "You."
    menu:
        "What do I tell them?":
            mc "What do I tell them?"
            lena "What we know."
            $ _apply_trust("lena", 1)
            lena "Not what they want to hear. Not what you're afraid to say."
            hide drlena_normal
            $ _work_perf(6)
        "I'm not ready for that.":
            mc "I'm not ready for that."
            lena "Then stand beside me and listen."
            lena "You'll be ready next time."
            hide drlena_normal
            $ _work_perf(3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ _mark_wev("hospital", "wev_hosp_difficult_relative")
    return

label wev_hosp_quiet_minute:
    "The corridor is briefly quiet."
    show drlena_normal at sprite_r
    mc "Is it always like this?"
    lena "No."
    mc "I meant the noise."
    lena "So did I."
    "A call light activates farther down the hall."
    lena "There it is."
    hide drlena_normal
    $ _mark_wev("hospital", "wev_hosp_quiet_minute")
    return


# ══ WAREHOUSE ══════════════════════════════════════════════════════════════

label wev_warehouse_wrong_bay:
    $ _wev_relbar_open("natalie")
    show screen npc_relbar("natalie")
    show natalie_normal at sprite_r
    nat "That pallet belongs in bay six."
    mc "The label says eight."
    nat "The label is wrong."
    mc "How do you know?"
    nat "Because bay eight is full of something flammable."
    menu:
        "Move it now.":
            mc "I'll move it."
            nat "Check the manifest first."
            $ _apply_trust("natalie", 1)
            nat "Fast mistakes are still mistakes."
            hide natalie_normal
            $ _work_perf(6)
        "Then the label needs fixing.":
            mc "Then the label needs fixing."
            nat "Correct."
            nat "After the pallet stops being in the wrong place."
            hide natalie_normal
            $ _work_perf(3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ _mark_wev("warehouse", "wev_warehouse_wrong_bay")
    return

label wev_warehouse_safety_vest:
    show natalie_normal at sprite_r
    nat "Zip the vest."
    mc "It's thirty degrees in here."
    nat "The forklift doesn't care."
    mc "I can see it."
    nat "The vest is for the driver."
    "You zip the vest."
    nat "Now both of you have a chance."
    hide natalie_normal
    $ _work_perf(2)
    $ _mark_wev("warehouse", "wev_warehouse_safety_vest")
    return

label wev_warehouse_early_arrival:
    $ _wev_relbar_open("natalie")
    show screen npc_relbar("natalie")
    show natalie_normal at sprite_r
    nat "You're early."
    mc "Five minutes."
    nat "That counts."
    mc "I thought you'd say it didn't."
    nat "Five minutes late counts too."
    mc "Fair."
    $ _apply_trust("natalie", 1)
    nat "Consistency usually is."
    hide natalie_normal
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ _mark_wev("warehouse", "wev_warehouse_early_arrival")
    return


# ══ PHASE 7 — SHIFT TEXTURE (replayable, no effects) ══════════════════════

label wev_cafe_shift_texture:
    $ _v = _pick_texture_variant("cafe", ["swapped_cups", "terminal_offline", "empty_pitcher", "grinder_jam", "last_clean_mug"])
    call expression "wev_cafe_tex_" + _v
    $ _mark_wev("cafe", "wev_cafe_shift_texture")
    return

label wev_it_shift_texture:
    $ _v = _pick_texture_variant("it", ["ci_only_failure", "empty_ticket", "merge_conflict", "build_queue", "alert_storm"])
    call expression "wev_it_tex_" + _v
    $ _mark_wev("it", "wev_it_shift_texture")
    return


# ── Café texture variants ───────────────────────────────────────────────────

label wev_cafe_tex_swapped_cups:
    "The labels beneath the counter don't match the cups above them. Two orders waiting."
    menu:
        "Fix the labels before the next order.":
            "You do. No one notices."
        "Hold the current arrangement in your head for the rest of the shift.":
            "It works. Barely."
    return

label wev_cafe_tex_terminal_offline:
    "The payment terminal freezes mid-transaction. The customer is watching."
    menu:
        "Restart it. Apologise.":
            "It comes back. The queue behind them has not."
        "Ask them to pay cash.":
            "They don't have any."
            "You restart it."
    return

label wev_cafe_tex_empty_pitcher:
    "You reach for the milk. The pitcher is empty. The order is already on the counter."
    menu:
        "Top it up before the customer notices.":
            "You do."
        "Tell them there's a brief delay.":
            "They nod."
    return

label wev_cafe_tex_grinder_jam:
    show nora_cafe_normal at sprite_r
    "The grinder stops mid-grind. A smell like burnt rubber."
    n "Don't press it again."
    mc "I wasn't going to."
    n "You were."
    hide nora_cafe_normal
    return

label wev_cafe_tex_last_clean_mug:
    "One clean mug on the shelf. Two orders placed at the same time."
    menu:
        "Use the clean mug, rewash the other one fast.":
            "You make it work."
        "Tell the second customer there's a short wait.":
            "They've waited before."
    return


# ── IT texture variants ─────────────────────────────────────────────────────

label wev_it_tex_ci_only_failure:
    "CI fails on a branch that passed locally. The error references a dependency that didn't exist yesterday."
    menu:
        "Check the lock file.":
            "That's it. Three minutes."
        "Rerun the build.":
            "Same failure. Faster confirmation."
    return

label wev_it_tex_empty_ticket:
    "Your assigned ticket has a title and a due date. The description field is empty."
    menu:
        "Ask the requester what they actually need.":
            "They reply four hours later with the same description."
        "Make your best guess and document it.":
            "You'll be either right, or have evidence you weren't."
    return

label wev_it_tex_merge_conflict:
    "A merge conflict in a file you're certain you didn't touch."
    menu:
        "Trace who changed it last.":
            "Everyone changed it last. Three of them today."
        "Resolve it and move on.":
            "Fastest. Not satisfying."
    return

label wev_it_tex_build_queue:
    "Nine builds ahead of yours. Someone queued a full regression run at noon on a Friday."
    menu:
        "Wait.":
            "You wait."
        "Cancel and requeue at lower priority.":
            "You are lower priority. Everyone else did this too."
    return

label wev_it_tex_alert_storm:
    show eli_normal at sprite_r
    "A monitoring alert. Then another. Then five more."
    mc "Real or noisy?"
    eli "Unclear."
    mc "Helpful."
    eli "Monitoring is not a diagnosis. It is a symptom."
    hide eli_normal
    return

label wev_corp_shift_texture:
    $ _v = _pick_texture_variant("corporate", ["wrong_attachment", "calendar_collision", "reply_all", "spreadsheet_filter", "printer_queue"])
    call expression "wev_corp_tex_" + _v
    $ _mark_wev("corporate", "wev_corp_shift_texture")
    return

label wev_corp_tex_wrong_attachment:
    scene office
    show screen hud
    "You sent the draft. Then immediately opened your sent folder."
    "Wrong file. You send the correct one with no subject line and hope the recipient checks the timestamp."
    return

label wev_corp_tex_calendar_collision:
    scene office
    show screen hud
    "Two meetings, same slot. Both marked required. Both have the same organiser listed."
    menu:
        "Ask which meeting takes priority.":
            "The organiser responds in three minutes. One of them was a mistake."
            $ _work_perf(4)
        "Join the meeting with the more senior attendee.":
            "You join. No one mentions the other meeting."
    return

label wev_corp_tex_reply_all:
    scene office
    show screen hud
    "Someone replied all to the department announcement. Then someone replied all to that."
    "You read the thread to its end. Seventeen messages. Nothing actionable."
    return

label wev_corp_tex_spreadsheet_filter:
    scene office
    show screen hud
    "The report has a filter applied that no one set intentionally. Half the rows are hidden."
    "You clear it. The actual numbers are less interesting than the mystery was."
    $ _work_perf(2)
    return

label wev_corp_tex_printer_queue:
    scene office
    show screen hud
    "The printer has a job stuck at the front of the queue. Owner unknown. Document unnamed."
    "You cancel it. Your document prints. The stuck job reappears two minutes later."
    return

label wev_hosp_shift_texture:
    $ _v = _pick_texture_variant("hospital", ["missing_signature", "lab_callback", "changed_priority", "empty_room", "double_chart"])
    call expression "wev_hosp_tex_" + _v
    $ _mark_wev("hospital", "wev_hosp_shift_texture")
    return

label wev_hosp_tex_missing_signature:
    "The form is complete except for one signature."
    "The person who needs to sign it is no longer on the ward."
    mc "Naturally."
    "You place it in the callback tray and add a note before it disappears into the rest of the paperwork."
    return

label wev_hosp_tex_lab_callback:
    "The phone rings before you finish documenting the previous call."
    "Lab" "Lab calling about the repeat sample."
    mc "Is there a result?"
    "Lab" "There is a problem with the sample."
    mc "Of course there is."
    return

label wev_hosp_tex_changed_priority:
    "The patient marked next is no longer next."
    "A new note changes the priority without changing the queue."
    menu:
        "Review the new case first.":
            "You reopen the notes and reorganise the next steps."
        "Finish the current documentation first.":
            "You complete the current note before moving on."
    return

label wev_hosp_tex_empty_room:
    "You enter the room with the chart open."
    "The bed is empty."
    "The patient has been moved to imaging."
    "The update reached every system except the one you checked."
    mc "Good."
    return

label wev_hosp_tex_double_chart:
    "Two open charts share the same surname."
    "You stop before entering the next value."
    "The dates of birth are different."
    mc "That would have been memorable."
    $ gain_skill("med", 2)
    return

label wev_warehouse_shift_texture:
    $ _v = _pick_texture_variant("warehouse", ["scanner_retry", "blocked_bay", "torn_label", "short_delivery", "loose_wrap"])
    call expression "wev_warehouse_tex_" + _v
    $ _mark_wev("warehouse", "wev_warehouse_shift_texture")
    return

label wev_warehouse_tex_scanner_retry:
    "The scanner rejects the barcode."
    "You try again."
    "It rejects the same barcode more confidently."
    mc "Good talk."
    "You enter the number manually."
    return

label wev_warehouse_tex_blocked_bay:
    "The destination bay is blocked by an unlisted pallet."
    "The manifest insists the space is empty."
    menu:
        "Move the unlisted pallet first.":
            "You verify the label and clear the bay."
        "Use the nearest empty bay temporarily.":
            "You mark the temporary location before moving on."
    return

label wev_warehouse_tex_torn_label:
    "Half the shipping label is missing."
    "The destination code ends after two characters."
    mc "Helpful."
    "You compare the remaining number against the manifest."
    return

label wev_warehouse_tex_short_delivery:
    "The delivery sheet lists twelve units."
    "There are eleven."
    "You count again."
    "There are still eleven."
    mc "Consistent."
    $ _work_perf(-2)
    return

label wev_warehouse_tex_loose_wrap:
    "The plastic wrap shifts when the pallet turns."
    "You stop it before the top box begins moving independently."
    "You tighten the wrap and check the remaining corners."
    return
