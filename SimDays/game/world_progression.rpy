# world_progression.rpy — independent NPC life progressions (Phase 42+)
# Called once per day from new_day(), after check_missed_commitments(),
# before deliver_due_messages(), so messages queued here deliver the same morning.

init python:

    # Nora's schedule while enrolled in culinary school.
    # Replaces NPC_DATA["nora"]["sched"] via npc_schedule_entries() in interact.rpy.
    # Tuesday evening bar slot is absent by design; Friday bar 17-22 is retained.
    _NORA_SCHOOL_SCHED = [
        ({0, 2, 4}, (7,  16), "location_cafe"),  # Mon, Wed, Fri: Grounds 07-16
        ({1, 3},    (7,  11), "location_cafe"),  # Tue, Thu: Grounds 07-11
        ({4},       (17, 22), "location_bar"),   # Fri: bar 17-22
        ({5, 6},    (10, 14), "location_cafe"),  # Sat, Sun: Grounds 10-14
    ]

    # ── Phase 43: milestone helpers ───────────────────────────────────────────

    # career ID -> (npc_id, label). Corporate handled separately (martha vs caroline).
    _PROMOTION_MENTOR_MAP = {
        "it":       ("eli",  "talk_followup_promo_it"),
        "hospital": ("lena", "talk_followup_promo_hospital"),
        "culinary": ("rena", "talk_followup_promo_culinary"),
        "trainer":  ("kai",  "talk_followup_promo_trainer"),
    }

    def _queue_milestone_followup(npc_id, milestone_id, milestone_type, context, label):
        pending = dict(store.npc_milestone_followup_pending)
        lst = list(pending.get(npc_id, []))
        if any(e["milestone_id"] == milestone_id for e in lst):
            return
        lst.append({
            "milestone_id":   milestone_id,
            "milestone_type": milestone_type,
            "context":        context,
            "created_day":    store.day,
            "label":          label,
        })
        pending[npc_id] = lst
        store.npc_milestone_followup_pending = pending

    def _resolve_oldest_milestone(npc_id):
        pending = dict(store.npc_milestone_followup_pending)
        lst = list(pending.get(npc_id, []))
        if not lst:
            return
        lst.sort(key=lambda e: e["created_day"])
        lst.pop(0)
        if lst:
            pending[npc_id] = lst
        else:
            pending.pop(npc_id, None)
        store.npc_milestone_followup_pending = pending

    def _fire_promotion_reactions(job_id, new_rank, milestone_id):
        if store.marcus_met and "marcus" in store.npc_contacts:
            _tag = "marcus_promo_%s_%d" % (job_id, new_rank)
            if not message_already_queued(_tag):
                queue_phone_message(
                    "marcus",
                    "Heard you moved up. Drinks are still not on me.",
                    store.day, _tag)
        if job_id == "corporate":
            if store.martha_met:
                _queue_milestone_followup("martha", milestone_id, "promotion",
                    {"job_id": job_id, "rank": new_rank},
                    "talk_followup_promo_corporate_martha")
            elif store.caroline_met:
                _queue_milestone_followup("caroline", milestone_id, "promotion",
                    {"job_id": job_id, "rank": new_rank},
                    "talk_followup_promo_corporate_caroline")
        else:
            _entry = _PROMOTION_MENTOR_MAP.get(job_id)
            if _entry is not None:
                _npc_id, _lbl = _entry
                if getattr(store, _npc_id + "_met", False):
                    _queue_milestone_followup(_npc_id, milestone_id, "promotion",
                        {"job_id": job_id, "rank": new_rank}, _lbl)

    def _fire_apartment_reactions(prev_tier, cur_tier, milestone_id):
        if not store.marcus_met:
            return
        _lbl = "talk_followup_apt_%d_to_%d" % (prev_tier, cur_tier)
        _queue_milestone_followup("marcus", milestone_id, "apartment",
            {"from_tier": prev_tier, "to_tier": cur_tier}, _lbl)

    # ── Phase 43B: degree reactions ──────────────────────────────────────────

    _DEGREE_MESSAGES = {
        ("med_bach",  "lena"):     "You finished the bachelor's. That's when it stops feeling like studying.",
        ("med_mast",  "lena"):     "Master's done. The cases will be harder from here, not easier.",
        ("prog_bach", "eli"):      "You got the bachelor's? Prod doesn't care, but it's worth something.",
        ("prog_mast", "eli"):      "Master's. Good. Now they'll blame you first when something breaks.",
        ("biz_bach",  "martha"):   "Credential done. The credential doesn't change anything. What you do next does.",
        ("biz_mast",  "martha"):   "MBA done. People will assume a lot now. Most of it wrong.",
        ("biz_bach",  "caroline"): "I saw you got your degree. Congratulations.",
        ("biz_mast",  "caroline"): "Master's, then. Good.",
    }

    def _fire_degree_reactions(degree_id, milestone_id):
        if degree_id in ("biz_bach", "biz_mast"):
            if store.martha_met:
                _npc_id = "martha"
            elif store.caroline_met:
                _npc_id = "caroline"
            else:
                return
        elif degree_id in ("med_bach", "med_mast"):
            if not store.lena_met:
                return
            _npc_id = "lena"
        elif degree_id in ("prog_bach", "prog_mast"):
            if not store.eli_met:
                return
            _npc_id = "eli"
        else:
            return
        _msg = _DEGREE_MESSAGES.get((degree_id, _npc_id))
        if _msg is None:
            return
        _tag = "%s_degree_%s" % (_npc_id, degree_id)
        _lbl = "talk_followup_degree_%s_%s" % (degree_id, _npc_id)
        if _npc_id in store.npc_contacts:
            if not message_already_queued(_tag):
                queue_phone_message(_npc_id, _msg, store.day, _tag)
        else:
            _queue_milestone_followup(_npc_id, milestone_id, "degree",
                {"degree_id": degree_id}, _lbl)

    # ── Phase 46: story aftermath helpers ────────────────────────────────────

    def _queue_story_aftermath(npc_id, aftermath_id, source, outcome,
                               created_day, eligible_day, label):
        if aftermath_id in store.npc_story_aftermath_seen:
            return
        pending = dict(store.npc_story_aftermath_pending)
        lst = list(pending.get(npc_id, []))
        if any(e["aftermath_id"] == aftermath_id for e in lst):
            return
        lst.append({
            "aftermath_id": aftermath_id,
            "source":       source,
            "outcome":      outcome,
            "created_day":  created_day,
            "eligible_day": eligible_day,
            "label":        label,
        })
        pending[npc_id] = lst
        store.npc_story_aftermath_pending = pending

    def _resolve_story_aftermath(npc_id, aftermath_id):
        seen = dict(store.npc_story_aftermath_seen)
        seen[aftermath_id] = True
        store.npc_story_aftermath_seen = seen
        pending = dict(store.npc_story_aftermath_pending)
        lst = [e for e in pending.get(npc_id, []) if e["aftermath_id"] != aftermath_id]
        if lst:
            pending[npc_id] = lst
        else:
            pending.pop(npc_id, None)
        store.npc_story_aftermath_pending = pending

    def process_world_progression():
        # ── Migration: runs once on first new_day() after Phase 42 loads ─────
        # Existing saves must not receive every historical callback at once.
        if not store.world_progression_initialized:
            store.world_progression_initialized = True
            # Nora: scene done on existing save but school start not yet scheduled
            if store.nora_hug_school_done and store.nora_school_start_day < 0:
                store.nora_school_start_day = store.day + 7
            # Elle: decision scene done on existing save; infer life state
            if store.elle_decision_done and store.elle_life_state == "city":
                _resp = store.elle_travel_2_response
                store.elle_decision_day = store.day
                store.elle_life_state_day = store.day
                if _resp == "take_it":
                    store.elle_life_state = "departure_pending"
                elif _resp == "what_miss":
                    store.elle_life_state = "staying"
                else:
                    store.elle_life_state = "deferred"
                # callbacks not pre-marked: staying fires at day+7, deferred at day+14

        # ── Nora: café → school ───────────────────────────────────────────────
        if (store.nora_life_state == "cafe"
                and store.nora_school_start_day >= 0
                and store.day >= store.nora_school_start_day):
            store.nora_life_state = "school"
            if not message_already_queued("nora_school_started"):
                queue_phone_message(
                    "nora",
                    "First week started. I have burns in places I didn't know could burn. It was good.",
                    store.day, "nora_school_started")

        # ── Elle: departure_pending → abroad (day +3) ─────────────────────────
        if (store.elle_life_state == "departure_pending"
                and store.elle_decision_day >= 0
                and store.day >= store.elle_decision_day + 3):
            store.elle_life_state = "abroad"
            store.elle_life_state_day = store.day
            store.elle_return_day = store.day + 21
            if not message_already_queued("elle_departure"):
                queue_phone_message(
                    "elle",
                    "Boarding. Don't make the far end of the pier sentimental while I'm gone.",
                    store.day, "elle_departure")

        # ── Elle: abroad — postcard at departure +7 ───────────────────────────
        if (store.elle_life_state == "abroad"
                and store.elle_life_state_day >= 0
                and store.day >= store.elle_life_state_day + 7
                and not message_already_queued("elle_postcard")):
            queue_phone_message(
                "elle",
                "First week: the water here is colder than it looks. You'd like the light.",
                store.day, "elle_postcard")

        # ── Elle: abroad → returned (elle_return_day) ─────────────────────────
        if (store.elle_life_state == "abroad"
                and store.elle_return_day >= 0
                and store.day >= store.elle_return_day):
            store.elle_life_state = "returned"
            if not store.elle_return_message_done:
                store.elle_return_message_done = True
                queue_phone_message(
                    "elle",
                    "Back Wednesday. Same far end of the pier.",
                    store.day, "elle_return")

        # ── Elle: staying — callback at decision +7 ───────────────────────────
        if (store.elle_life_state == "staying"
                and store.elle_decision_day >= 0
                and store.day >= store.elle_decision_day + 7
                and not store.elle_decision_callback_done):
            store.elle_decision_callback_done = True
            if not message_already_queued("elle_staying_callback"):
                queue_phone_message(
                    "elle",
                    "Still here. It stopped feeling like indecision once I said it out loud.",
                    store.day, "elle_staying_callback")

        # ── Elle: deferred — callback at decision +14 ─────────────────────────
        if (store.elle_life_state == "deferred"
                and store.elle_decision_day >= 0
                and store.day >= store.elle_decision_day + 14
                and not store.elle_decision_callback_done):
            store.elle_decision_callback_done = True
            if not message_already_queued("elle_deferred_callback"):
                queue_phone_message(
                    "elle",
                    "Deadline passed. I let it. Not sure whether that's relief or cowardice yet.",
                    store.day, "elle_deferred_callback")

        # ── Phase 43: milestone snapshot and detection ────────────────────────
        _43B_MARKER = "_migration:phase43b_degree_loan_snapshots"

        if not store.life_milestones_initialized:
            # New game or first run after Phase 43 load: initialise all snapshots.
            store.life_milestones_initialized = True
            store.life_snapshot_job_id = store.job_id
            store.life_snapshot_job_rank = store.job_rank
            store.life_snapshot_apartment_tier = store.apartment_tier
            store.life_snapshot_degrees = list(store.degrees)
            store.life_snapshot_loan    = store.loan
            _ms = dict(store.life_milestones_seen)
            _ms[_43B_MARKER] = True
            store.life_milestones_seen = _ms
        else:
            _cur_jid   = store.job_id
            _cur_rank  = store.job_rank
            _cur_tier  = store.apartment_tier
            _prev_jid  = store.life_snapshot_job_id
            _prev_rank = store.life_snapshot_job_rank
            _prev_tier = store.life_snapshot_apartment_tier

            # Promotion: same career, rank strictly increased
            if (_cur_jid is not None
                    and _cur_jid == _prev_jid
                    and _cur_rank > _prev_rank):
                _mid = "promotion:%s:%d" % (_cur_jid, _cur_rank)
                _ms = dict(store.life_milestones_seen)
                if _mid not in _ms:
                    _ms[_mid] = True
                    store.life_milestones_seen = _ms
                    _fire_promotion_reactions(_cur_jid, _cur_rank, _mid)

            # Apartment upgrade: tier strictly increased
            if _cur_tier > _prev_tier:
                _amid = "apartment:%d:%d" % (_prev_tier, _cur_tier)
                _ms = dict(store.life_milestones_seen)
                if _amid not in _ms:
                    _ms[_amid] = True
                    store.life_milestones_seen = _ms
                    _fire_apartment_reactions(_prev_tier, _cur_tier, _amid)

            _43b_done = _43B_MARKER in store.life_milestones_seen

            if not _43b_done:
                # Phase 43A existing save: snapshot current state without reacting.
                store.life_snapshot_degrees = list(store.degrees)
                store.life_snapshot_loan    = store.loan
                _ms = dict(store.life_milestones_seen)
                _ms[_43B_MARKER] = True
                store.life_milestones_seen = _ms
            else:
                # Normal detection pass.

                # Degree earned: any degree not in previous snapshot
                _cur_degrees  = list(store.degrees)
                _prev_degrees = list(store.life_snapshot_degrees)
                for _did in _cur_degrees:
                    if _did not in _prev_degrees:
                        _dmid = "degree:%s" % _did
                        _ms = dict(store.life_milestones_seen)
                        if _dmid not in _ms:
                            _ms[_dmid] = True
                            store.life_milestones_seen = _ms
                            _fire_degree_reactions(_did, _dmid)

                # Loan fully repaid: was positive, now zero or below
                _cur_loan  = store.loan
                _prev_loan = store.life_snapshot_loan
                if _prev_loan > 0 and _cur_loan <= 0:
                    _lmid = "finance:loan_repaid"
                    _ms = dict(store.life_milestones_seen)
                    if _lmid not in _ms:
                        _ms[_lmid] = True
                        store.life_milestones_seen = _ms
                        if (store.marcus_met
                                and "marcus" in store.npc_contacts
                                and npc_trust("marcus") >= 20):
                            _ltag = "marcus_loan_repaid"
                            if not message_already_queued(_ltag):
                                queue_phone_message(
                                    "marcus",
                                    "You cleared it? Good. Now don't borrow money to celebrate clearing the money.",
                                    store.day, _ltag)

                # Update snapshots
                store.life_snapshot_degrees = list(store.degrees)
                store.life_snapshot_loan    = store.loan

            # Update job/apartment snapshots every pass regardless of 43B state
            store.life_snapshot_job_id = store.job_id
            store.life_snapshot_job_rank = store.job_rank
            store.life_snapshot_apartment_tier = store.apartment_tier

        # ── Phase 46: story aftermath detection ──────────────────────────────
        if not store.npc_story_aftermath_initialized:
            # Migration: mark existing completed sources as seen; no retroactive queue.
            _46s = dict(store.npc_story_aftermath_seen)
            if store.scene_cul_service_crisis_done:
                _46s["rena_culinary_crisis"] = True
            if store.hospital_hard_case_followup_done:
                _46s["lena_hard_case"] = True
            if store.tr_review_done:
                _46s["kai_trainer_review"] = True
            # Phase 48 migration on first pass
            if store.it_review_done:
                _46s["it_production_incident"] = True
                if not store.it_incident_done:
                    store.it_incident_done = True
                    store.it_incident_followup_done = True
            if store.corp_review_intern_done:
                _46s["corp_reporting_integrity"] = True
                if not store.corp_integrity_done:
                    store.corp_integrity_done = True
                    store.corp_integrity_followup_done = True
            _46s["_migration:phase48_professional_judgment"] = True
            # Phase 50 migration: exhibition already done on old saves → skip aftermath
            if store.zoe_exhibition_done:
                _46s["zoe_exhibition"] = True
                store.zoe_exhibition_aftermath_queued = True
            _46s["_migration:phase50_exhibition"] = True
            store.npc_story_aftermath_seen = _46s
            store.npc_story_aftermath_initialized = True
        else:
            # Phase 48 migration for saves that ran Phase 46 migration before Phase 48 existed
            if "_migration:phase48_professional_judgment" not in store.npc_story_aftermath_seen:
                _48s = dict(store.npc_story_aftermath_seen)
                if store.it_review_done:
                    _48s["it_production_incident"] = True
                    if not store.it_incident_done:
                        store.it_incident_done = True
                        store.it_incident_followup_done = True
                if store.corp_review_intern_done:
                    _48s["corp_reporting_integrity"] = True
                    if not store.corp_integrity_done:
                        store.corp_integrity_done = True
                        store.corp_integrity_followup_done = True
                _48s["_migration:phase48_professional_judgment"] = True
                store.npc_story_aftermath_seen = _48s
            # Phase 50 migration for saves that already passed Phase 46/48 init
            if "_migration:phase50_exhibition" not in store.npc_story_aftermath_seen:
                _50s = dict(store.npc_story_aftermath_seen)
                _50s["_migration:phase50_exhibition"] = True
                if store.zoe_exhibition_done:
                    _50s["zoe_exhibition"] = True
                    store.zoe_exhibition_aftermath_queued = True
                store.npc_story_aftermath_seen = _50s
            if (store.scene_cul_service_crisis_done
                    and "rena_culinary_crisis" not in store.npc_story_aftermath_seen):
                _caf = store.cul_crisis_aftermath
                if _caf == "mixed":
                    store.rena_diner_absent_until_day = store.day + 2
                elif _caf == "bad":
                    store.rena_diner_absent_until_day = store.day + 4
                _queue_story_aftermath(
                    "rena", "rena_culinary_crisis", "culinary_crisis", _caf,
                    store.day, store.day + 1, "aftermath_rena_culinary_crisis")
            if (store.tr_review_done
                    and "kai_trainer_review" not in store.npc_story_aftermath_seen):
                _queue_story_aftermath(
                    "kai", "kai_trainer_review", "trainer_review",
                    store.tr_boundary_outcome,
                    store.day, store.day + 1, "aftermath_kai_trainer_review")
            # Phase 50: Zoe exhibition aftermath — queues 2 days after opening
            if (store.zoe_exhibition_done
                    and store.day >= store.zoe_exhibition_day + 2
                    and not store.zoe_exhibition_aftermath_queued
                    and "zoe_exhibition" not in store.npc_story_aftermath_seen):
                _queue_story_aftermath(
                    "zoe", "zoe_exhibition", "exhibition",
                    store.zoe_exhibition_outcome,
                    store.day, store.day,
                    "story_aftermath_zoe_exhibition")
                store.zoe_exhibition_aftermath_queued = True


# ── Talk follow-up: Nora, first week at school ───────────────────────────────

label talk_followup_nora_school_first_week:
    $ _do_talk_accounting("nora")
    n "It's harder than Grounds. Different kind of hard."
    "She says it like a fact she's still processing."
    n "There, I knew everything. I was competent. I'd built that over three years."
    n "Here, I don't know anything yet. Everything I brought in is wrong in some specific way I didn't predict."
    mc "Like what?"
    n "Temperature. I thought I understood how heat moves through fat."
    n "I've worked with oil every shift for three years. Didn't matter."
    "She's looking at her hands when she says it."
    n "They make you unlearn it first. Then build it again from the right direction."
    mc "Is that bad?"
    n "It's just what it is."
    $ nora_school_first_week_followup_done = True
    $ add_relationship_memory("nora", "nora_school_first_week", "Her first week at culinary school")
    return


# ── Talk follow-up: Elle, after the Portugal decision ────────────────────────

label talk_followup_elle_post_decision:
    $ _do_talk_accounting("elle")
    if elle_life_state == "returned":
        el "The pier looks smaller."
        mc "Same pier."
        el "I know. That's the thing."
        "She stands at the railing. Not unhappy. Recalibrating."
        el "Going was correct. Coming back was also correct. I'm working out how both of those can be true."
        $ add_relationship_memory("elle", "elle_after_portugal_decision", "She came back; the pier looks smaller")
    elif elle_life_state == "staying":
        el "I stopped calling it temporary somewhere around week three."
        "She says it like she's still working out what it means."
        el "It didn't feel like a decision in the moment. It just — stopped being provisional."
        mc "Is that the same thing?"
        el "Close enough."
        $ add_relationship_memory("elle", "elle_after_portugal_decision", "Staying stopped feeling temporary")
    else:
        el "I kept the option open."
        "She doesn't apologise for it."
        el "I thought I was being thoughtful. I'm not sure whether that's true or just what I told myself."
        mc "Does it matter which?"
        el "Probably not yet."
        $ add_relationship_memory("elle", "elle_after_portugal_decision", "She let the deadline pass")
    $ elle_post_decision_talk_done = True
    return


# ── Phase 43: promotion Talk follow-ups ──────────────────────────────────────

label talk_followup_promo_corporate_martha:
    $ _do_talk_accounting("martha")
    ma "You're aware the title changes what people bring to you — not what you actually know."
    mc "I assumed that."
    ma "Good. The ones who need to hear it twice spend the first month repeating their new rank to whoever will listen."
    "She looks back at what she was reading."
    ma "The accountability catches up faster than the authority does. Be ready for that."
    $ _resolve_oldest_milestone("martha")
    return


label talk_followup_promo_corporate_caroline:
    $ _do_talk_accounting("caroline")
    caro "I heard about your promotion."
    "She says it neutrally. Not warmly, not coldly."
    caro "The view from the new floor is different. That's not a compliment or a warning — it's just what happens."
    $ _resolve_oldest_milestone("caroline")
    return


label talk_followup_promo_it:
    $ _do_talk_accounting("eli")
    eli "You know the actual change isn't the access level."
    mc "What is it?"
    eli "The next deployment that breaks something — that one's yours. Not as in blame. As in: you're the one who figures it out."
    "She's not saying it to alarm you."
    eli "It's different. That's all."
    $ _resolve_oldest_milestone("eli")
    return


label talk_followup_promo_hospital:
    $ _do_talk_accounting("lena")
    lena "At your new rank, they look to you first. Not always for answers — sometimes just to see whether you're steady."
    "She says it the same way she says most things: like information, not advice."
    lena "The instinct is to have an answer ready. It's not always the right instinct."
    $ _resolve_oldest_milestone("lena")
    return


label talk_followup_promo_culinary:
    $ _do_talk_accounting("rena")
    rena "You know what's harder than one good plate?"
    mc "Every plate."
    rena "Every plate. Same heat. Same hands. Eighty covers."
    "She doesn't elaborate. The promotion means you already know what she's about to say."
    $ _resolve_oldest_milestone("rena")
    return


label talk_followup_promo_trainer:
    $ _do_talk_accounting("kai")
    kai "Being a trainer isn't about knowing what you can do."
    mc "It's about knowing what they can't."
    kai "Close. What they think they can't but actually can — and knowing when to stop before you find out the hard way."
    "He says it without drama."
    $ _resolve_oldest_milestone("kai")
    return


# ── Phase 43: apartment upgrade Talk follow-ups ───────────────────────────────

label talk_followup_apt_1_to_2:
    $ _do_talk_accounting("marcus")
    m "You moved."
    mc "Better place."
    m "Still feels like yours, though."
    "He glances around — not evaluating, just taking it in."
    m "Good. You kept the stuff that matters."
    $ _resolve_oldest_milestone("marcus")
    return


label talk_followup_apt_2_to_3:
    $ _do_talk_accounting("marcus")
    m "You're paying how much for this?"
    mc "Don't ask."
    m "I'm asking."
    "He looks around with an expression that's mostly impressed and somewhat horrified."
    m "It's a lot. For a place to sleep and eat."
    mc "And other things."
    m "Right. The ambience."
    $ _resolve_oldest_milestone("marcus")
    return


# ── Phase 43B: degree Talk follow-ups ────────────────────────────────────────

label talk_followup_degree_med_bach_lena:
    $ _do_talk_accounting("lena")
    lena "A bachelor's in medicine means you know enough to know what you don't know."
    "She says it without condescension."
    lena "That's the right place to be."
    $ _resolve_oldest_milestone("lena")
    return


label talk_followup_degree_med_mast_lena:
    $ _do_talk_accounting("lena")
    lena "The master's changes the questions people will bring you."
    "She doesn't seem particularly surprised."
    lena "That's not a warning. It's just what it is."
    $ _resolve_oldest_milestone("lena")
    return


label talk_followup_degree_prog_bach_eli:
    $ _do_talk_accounting("eli")
    eli "The degree doesn't make the code run."
    mc "I know."
    eli "I know you know. I'm saying it anyway — it took me too long to stop caring whether I had the paper."
    "She looks at her screen."
    eli "It's worth something. Just not what most people think it is."
    $ _resolve_oldest_milestone("eli")
    return


label talk_followup_degree_prog_mast_eli:
    $ _do_talk_accounting("eli")
    eli "Master's. They're going to assume that means you can architect anything."
    mc "Can't I?"
    eli "You can try. Most of what's real you'll learn from the third time something breaks at 2am."
    $ _resolve_oldest_milestone("eli")
    return


label talk_followup_degree_biz_bach_martha:
    $ _do_talk_accounting("martha")
    ma "The bachelor's is a threshold. What's on the other side is on you."
    mc "I assumed that."
    ma "Most people do. Fewer are prepared for it."
    "She returns to what she was doing."
    $ _resolve_oldest_milestone("martha")
    return


label talk_followup_degree_biz_mast_martha:
    $ _do_talk_accounting("martha")
    ma "MBA done."
    "She doesn't elaborate immediately."
    ma "Now people will assume you have opinions on things you've never touched. Have them anyway — or admit you don't. Pick one and be consistent."
    $ _resolve_oldest_milestone("martha")
    return


label talk_followup_degree_biz_bach_caroline:
    $ _do_talk_accounting("caroline")
    caro "You finished the degree."
    "She says it the way she says most things — neutral, informational."
    caro "That gets you further than people expect. Less than they'll tell you."
    $ _resolve_oldest_milestone("caroline")
    return


label talk_followup_degree_biz_mast_caroline:
    $ _do_talk_accounting("caroline")
    caro "Master's done. The credential carries weight in certain rooms."
    "She doesn't specify which rooms."
    caro "You'll find out which ones."
    $ _resolve_oldest_milestone("caroline")
    return


# ── Phase 46: story aftermath labels ─────────────────────────────────────────

label aftermath_rena_culinary_crisis:
    $ _do_talk_accounting("rena")
    if store.cul_crisis_aftermath == "good":
        rena "You caught it early."
        mc "The team noticed it first."
        rena "Someone had to act on it. You did."
        "She refills her glass without offering an opinion on how it should have gone differently."
        rena "That's the thing with service. The problem happens. What matters is when you decide to move."
    elif store.cul_crisis_aftermath == "mixed":
        "She's quiet for a moment. Not occupied — considering."
        rena "The service ran."
        mc "Yes."
        rena "A service running is not the same as a service handled."
        "She doesn't labour it."
        rena "You know that. So we don't need to spend more time on it than it deserves."
    else:
        rena "The dish itself was recoverable. You know that."
        mc "Yes."
        rena "What wasn't recoverable was the window you let close."
        "She looks at her glass rather than at you."
        rena "Concealing a problem doesn't protect the service. It delays the damage and removes the option to fix it."
        rena "We continue. But I'll need to see more over time."
    $ _resolve_story_aftermath("rena", "rena_culinary_crisis")
    return



label aftermath_kai_trainer_review:
    $ _do_talk_accounting("kai")
    if store.tr_boundary_outcome == "referred":
        kai "Stopping a client can take more authority than pushing them."
        mc "They didn't want to stop."
        kai "That's when it's hardest. They came to train. You're the one who has to say no."
        "She straightens a weight on the rack she's passing."
        kai "The clients who push back when you stop them are the ones who need it most."
    elif store.tr_boundary_outcome == "managed":
        kai "The documentation was the right call."
        mc "I wasn't sure it would matter."
        kai "It matters when something develops later and you need a chain of decisions."
        "She pauses."
        kai "Just don't let modification become a habit. It's not permission to keep going. It's a ceiling, not a floor."
    elif store.tr_boundary_owned_mistake:
        kai "You made a wrong call and changed direction when you understood it."
        "She doesn't say it to console — she says it as a professional observation."
        kai "That's a better outcome than the ones who never correct, or the ones who correct but don't know why."
        mc "It doesn't undo the harm."
        kai "No. But it's where the difference shows up in ten years."
    else:
        kai "I still don't agree with your reasoning on the knee session."
        mc "I understand."
        kai "I'm not sure you do yet. But the work continues and we'll see."
        "She leaves it there. Not warm — open."
    $ _resolve_story_aftermath("kai", "kai_trainer_review")
    return


label aftermath_lena_hard_case:
    $ _do_talk_accounting("lena")
    if store.hospital_hard_case_outcome == "escalated":
        lena "You made the call under ambiguous conditions. That's harder than it looks from the outside."
        mc "The readings weren't definitive."
        lena "They rarely are. You don't wait for certainty before you act — you wait long enough to be sure you're not overreacting."
        "She turns a glass on the bar."
        lena "You found that line. Don't lose track of where it was."
        mc "I won't."
        lena "I know."
    elif store.hospital_hard_case_outcome == "reassessed":
        lena "The documentation mattered. I want you to know that."
        mc "I wasn't sure stopping was the right call."
        lena "Stopping to document isn't stopping. It's part of the decision."
        "She's quiet for a moment."
        lena "The mistake people make is treating observation and action as opposites. They're not. Observation is an action."
        mc "I'll remember that."
    elif store.hospital_hard_case_owned_mistake:
        lena "You told me before I had to ask. That's not a small thing in that environment."
        "She doesn't look away."
        lena "I don't excuse the original decision. You know that."
        mc "Yes."
        lena "But what you do after a mistake matters as much as the mistake itself. Sometimes more."
        lena "You've shown me you can correct. I need to see you're not making the same call again."
    else:
        lena "I'm still thinking about your reasoning on that case."
        mc "I know."
        lena "You saw ambiguity and treated it as permission to continue. That's the pattern I'm watching."
        "She holds her drink."
        lena "It's not about that specific patient. It's about how you read uncertainty. I need to see it change."
        mc "I'm working on it."
        lena "Good."
    $ _resolve_story_aftermath("lena", "lena_hard_case")
    return


label aftermath_it_production_incident:
    $ _do_talk_accounting("eli")
    if store.it_incident_outcome == "rollback":
        eli "You had nine hundred records with an irregular pattern and a colleague telling you to let it run."
        mc "I didn't like the shape of it."
        eli "That's what judgment looks like before it's confirmed as right. You don't always get the confirmation."
        mc "This time we got it."
        eli "This time. File the shape of that feeling away."
    elif store.it_incident_outcome == "isolated":
        eli "The partition held because the documentation was complete."
        mc "I wasn't certain the boundary would hold."
        eli "Most of the time it won't. You document it anyway."
        mc "For the next person."
        eli "For you, in three months, when you've forgotten what you were thinking."
    elif store.it_incident_owned_mistake:
        eli "You got what you were trying to avoid — the user impact — and you owned it."
        mc "Not the order I'd have chosen."
        eli "No. What changed?"
        mc "I know what the delay actually costs versus what the impact costs."
        eli "That's the part you can only learn the hard way. You've learned it."
    else:
        eli "The deadline reasoning didn't hold up."
        mc "The scope looked contained."
        eli "You flagged it yourself before you suppressed it."
        "She doesn't say it unkindly."
        eli "You knew. That's the part worth sitting with."
    $ _resolve_story_aftermath("eli", "it_production_incident")
    return


label aftermath_corp_reporting_integrity:
    $ _do_talk_accounting("caroline")
    if store.corp_integrity_outcome == "disclosed":
        caro "The reporting situation. The data turned out to be wrong at the source."
        mc "I didn't know that at the time."
        caro "No. You stopped a number from going to the board because you weren't certain it was correct."
        mc "That's what I'm supposed to do."
        caro "Yes. I'm telling you it was noticed."
    elif store.corp_integrity_outcome == "qualified":
        caro "The reconciliation note."
        mc "It held the figure from being treated as final."
        caro "People use what's in those decks to make decisions. Your note drew the right line."
        mc "It was the only defensible one."
        caro "That's the right way to think about it."
    elif store.corp_integrity_owned_mistake:
        caro "The written account you submitted."
        mc "It was complete."
        caro "It was. That's not a small thing."
        mc "The alteration was still wrong."
        caro "Yes. But how you handled what came after matters. Both things are on record."
    else:
        caro "Target pressure is real. I understand why you made the call you made."
        mc "You asked me to reconcile it."
        caro "I asked you to reconcile the discrepancy. Not replace the source figure."
        "A pause."
        caro "What you submit is what others act on. That's the weight of it."
    $ _resolve_story_aftermath("caroline", "corp_reporting_integrity")
    return


label aftermath_wh_damaged_shipment:
    $ _do_talk_accounting("natalie")
    if store.wh_safety_outcome == "stopped":
        nat "The pallet failed sitting still."
        mc "I know."
        nat "You said stop, and it stopped."
        mc "I didn't know it would fail while stationary."
        nat "That's why we have the rule. You don't need to know. You need to see the shape and call it."
        mc "I called it."
        nat "Yeah."
    elif store.wh_safety_outcome == "rerouted":
        nat "The process audit came back."
        mc "Did they find what caused the near-misses?"
        nat "Same loading sequence, different pallets. Your dispatch note is in the report."
        mc "It seemed worth documenting."
        nat "It was. Things like that sit in the near-miss list for years if no one writes them down."
    elif store.wh_safety_owned_mistake:
        nat "The written account."
        mc "I moved it knowing it wasn't secure. I wanted to make the window."
        nat "Did the deadline change when the shipment was damaged?"
        mc "No."
        nat "Deadlines don't move when the job goes wrong. That's the part that changes how you look at them."
    else:
        nat "The schedule was behind."
        mc "I know that's not the point."
        nat "You flagged the corner. You moved it anyway."
        mc "I thought the risk was manageable."
        nat "Did the window change your definition of manageable?"
        "She doesn't wait for an answer."
    $ _resolve_story_aftermath("natalie", "wh_damaged_shipment")
    return
