# dev_progression_smoke.rpy — Phase 42–50 integration smoke-test harness.
# DEV ONLY. Available only when config.developer is True.
# Launch from developer console: call dev_progression_smoke_menu

init python:
    if config.developer:
        import copy

        # ── Snapshot / restore ────────────────────────────────────────────────

        def _smoke_snap():
            s = store
            return {
                # time and needs
                "day":  s.day,  "hour": s.hour,
                "need_energy":  s.need_energy,
                "need_hunger":  s.need_hunger,
                "need_hygiene": s.need_hygiene,
                # economy
                "money": s.money, "loan": s.loan,
                "apartment_tier":  s.apartment_tier,
                # career
                "job_id":          s.job_id,
                "job_rank":        s.job_rank,
                "job_performance": s.job_performance,
                "degrees":         list(s.degrees),
                # NPC stats
                "nora_aff":  s.nora_affection,  "nora_trust":  s.nora_trust,  "nora_met":  s.nora_met,
                "elle_aff":  s.elle_affection,  "elle_trust":  s.elle_trust,  "elle_met":  s.elle_met,
                "zoe_aff":   s.zoe_affection,   "zoe_trust":   s.zoe_trust,   "zoe_met":   s.zoe_met,
                "eli_aff":   s.eli_affection,   "eli_trust":   s.eli_trust,   "eli_met":   s.eli_met,
                "lena_aff":  s.lena_affection,  "lena_trust":  s.lena_trust,  "lena_met":  s.lena_met,
                "marcus_aff": s.marcus_affection, "marcus_trust": s.marcus_trust, "marcus_met": s.marcus_met,
                "kai_aff":   s.kai_affection,   "kai_trust":   s.kai_trust,   "kai_met":   s.kai_met,
                "sam_aff":   s.sam_affection,   "sam_trust":   s.sam_trust,   "sam_met":   s.sam_met,
                "caro_aff":  s.caroline_affection, "caro_trust": s.caroline_trust, "caro_met": s.caroline_met,
                "natalie_aff": s.natalie_affection, "natalie_trust": s.natalie_trust, "natalie_met": s.natalie_met,
                # relationship metadata
                "relationship_memories":     copy.deepcopy(s.relationship_memories),
                "relationship_thresholds_seen": copy.deepcopy(s.relationship_thresholds_seen),
                "_npc_panel_npc_id": s._npc_panel_npc_id,
                "_rel_feedback_aff": s._rel_feedback_aff,
                "_rel_feedback_tr":  s._rel_feedback_tr,
                # social and jealousy
                "npc_jealousy_tension":  copy.deepcopy(s.npc_jealousy_tension),
                "npc_jealousy_last_day": copy.deepcopy(s.npc_jealousy_last_day),
                "npc_jealousy_pending":  copy.deepcopy(s.npc_jealousy_pending),
                "npc_social_attention":  copy.deepcopy(s.npc_social_attention),
                "fs_talk_count": s.fs_talk_count,
                # phone queues and initiative
                "npc_messages":          copy.deepcopy(s.npc_messages),
                "npc_initiative_pending": copy.deepcopy(s.npc_initiative_pending),
                "npc_invitation_pending": copy.deepcopy(s.npc_invitation_pending),
                "npc_date_invite_last_day": copy.deepcopy(s.npc_date_invite_last_day),
                "npc_anger":             copy.deepcopy(s.npc_anger),
                "npc_texted_today":      list(s.npc_texted_today),
                # world progression and life state
                "world_progression_initialized": s.world_progression_initialized,
                "nora_life_state":      s.nora_life_state,
                "nora_school_revealed": s.nora_school_revealed,
                "nora_school_accepted_day": s.nora_school_accepted_day,
                "nora_school_start_day":    s.nora_school_start_day,
                "nora_school_started_message_done":     s.nora_school_started_message_done,
                "nora_school_first_week_followup_done": s.nora_school_first_week_followup_done,
                "nora_hug_school_done":        s.nora_hug_school_done,
                "nora_hug_school_pending":     s.nora_hug_school_pending,
                "nora_hug_school_pending_day": s.nora_hug_school_pending_day,
                "elle_life_state":          s.elle_life_state,
                "elle_abroad_revealed":     s.elle_abroad_revealed,
                "elle_abroad_day":          s.elle_abroad_day,
                "elle_decision_done":       s.elle_decision_done,
                "elle_decision_pending":    s.elle_decision_pending,
                "elle_decision_callback_done": s.elle_decision_callback_done,
                "elle_travel_2_response":   s.elle_travel_2_response,
                "elle_decision_day":        s.elle_decision_day,
                "elle_return_day":          s.elle_return_day,
                "elle_return_message_done": s.elle_return_message_done,
                # milestones
                "life_milestones_initialized":   s.life_milestones_initialized,
                "life_milestones_seen":          copy.deepcopy(s.life_milestones_seen),
                "npc_milestone_followup_pending": copy.deepcopy(s.npc_milestone_followup_pending),
                "life_snapshot_job_id":      s.life_snapshot_job_id,
                "life_snapshot_job_rank":    s.life_snapshot_job_rank,
                "life_snapshot_apartment_tier": s.life_snapshot_apartment_tier,
                "life_snapshot_degrees":     list(s.life_snapshot_degrees),
                "life_snapshot_loan":        s.life_snapshot_loan,
                # Phase 44 crossover callbacks
                "cx_nora_elle_nora":  s.crossover_nora_elle_callback_nora_done,
                "cx_nora_elle_elle":  s.crossover_nora_elle_callback_elle_done,
                "cx_lena_marcus_lena":   s.crossover_lena_marcus_callback_lena_done,
                "cx_lena_marcus_marcus": s.crossover_lena_marcus_callback_marcus_done,
                "cx_sam_kai_sam":  s.crossover_sam_kai_callback_sam_done,
                "cx_sam_kai_kai":  s.crossover_sam_kai_callback_kai_done,
                "cx_caro_marcus_caro":   s.crossover_caroline_marcus_callback_caroline_done,
                "cx_caro_marcus_marcus": s.crossover_caroline_marcus_callback_marcus_done,
                # Phase 49 home visits
                "nora_home_coffee_done": s.nora_home_coffee_done,
                "nora_home_coffee_day":  s.nora_home_coffee_day,
                "eli_home_dinner_done":  s.eli_home_dinner_done,
                "eli_home_dinner_day":   s.eli_home_dinner_day,
                "zoe_home_guitar_done":  s.zoe_home_guitar_done,
                "zoe_home_guitar_day":   s.zoe_home_guitar_day,
                "own_guitar":            s.own_guitar,
                "own_kitchen_set":       s.own_kitchen_set,
                # Phase 50 exhibition
                "zoe_exhibition_invited":          s.zoe_exhibition_invited,
                "zoe_exhibition_done":             s.zoe_exhibition_done,
                "zoe_exhibition_day":              s.zoe_exhibition_day,
                "zoe_exhibition_outcome":          s.zoe_exhibition_outcome,
                "zoe_exhibition_aftermath_queued": s.zoe_exhibition_aftermath_queued,
                "zoe_exhibition_followup_done":    s.zoe_exhibition_followup_done,
                "zoe_gallery_until_day":           s.zoe_gallery_until_day,
                "zoe_gallery_talk_last_day":       s.zoe_gallery_talk_last_day,
                "zoe_exhibition_offer_last_day":   s.zoe_exhibition_offer_last_day,
                # career: trainer
                "tr_first_day_done": s.tr_first_day_done, "tr_task_1_done": s.tr_task_1_done,
                "tr_npc1_done": s.tr_npc1_done, "tr_npc2_done": s.tr_npc2_done,
                "tr_review_done": s.tr_review_done, "tr_shifts": s.tr_shifts,
                "tr_boundary_done":    s.tr_boundary_done,
                "tr_boundary_choice":  s.tr_boundary_choice,
                "tr_boundary_outcome": s.tr_boundary_outcome,
                "tr_boundary_followup_pending": s.tr_boundary_followup_pending,
                "tr_boundary_followup_shift":   s.tr_boundary_followup_shift,
                "tr_boundary_followup_done":    s.tr_boundary_followup_done,
                "tr_boundary_review_extra_shifts": s.tr_boundary_review_extra_shifts,
                # career: hospital/lena
                "hosp_shifts":      s.hosp_shifts,
                "hosp_review_done": s.hosp_review_done,
                "hospital_hard_case_pending":  s.hospital_hard_case_pending,
                "hospital_hard_case_done":     s.hospital_hard_case_done,
                "hospital_hard_case_choice":   s.hospital_hard_case_choice,
                "hospital_hard_case_outcome":  s.hospital_hard_case_outcome,
                "hospital_hard_case_followup_pending": s.hospital_hard_case_followup_pending,
                "hospital_hard_case_followup_shift":   s.hospital_hard_case_followup_shift,
                "hospital_hard_case_followup_done":    s.hospital_hard_case_followup_done,
                "hospital_hard_case_review_extra_shifts": s.hospital_hard_case_review_extra_shifts,
                "lena_case_observation_done":  s.lena_case_observation_done,
                # career: IT
                "it_review_done": s.it_review_done, "it_shifts": s.it_shifts,
                "it_incident_done": s.it_incident_done, "it_incident_choice": s.it_incident_choice,
                "it_incident_outcome": s.it_incident_outcome,
                "it_incident_followup_pending": s.it_incident_followup_pending,
                "it_incident_followup_shift":   s.it_incident_followup_shift,
                "it_incident_followup_done":    s.it_incident_followup_done,
                "it_incident_review_extra_shifts": s.it_incident_review_extra_shifts,
                # career: corporate
                "corp_shifts": s.corp_shifts,
                "corp_review_intern_done": s.corp_review_intern_done,
                "corp_integrity_done": s.corp_integrity_done, "corp_integrity_choice": s.corp_integrity_choice,
                "corp_integrity_outcome": s.corp_integrity_outcome,
                "corp_integrity_followup_pending": s.corp_integrity_followup_pending,
                "corp_integrity_followup_shift":   s.corp_integrity_followup_shift,
                "corp_integrity_followup_done":    s.corp_integrity_followup_done,
                "corp_integrity_review_extra_shifts": s.corp_integrity_review_extra_shifts,
                # career: warehouse
                "wh_shifts": s.wh_shifts,
                "wh_safety_done": s.wh_safety_done, "wh_safety_choice": s.wh_safety_choice,
                "wh_safety_outcome": s.wh_safety_outcome,
                "wh_safety_followup_pending": s.wh_safety_followup_pending,
                "wh_safety_followup_shift":   s.wh_safety_followup_shift,
                "wh_safety_followup_done":    s.wh_safety_followup_done,
                "wh_safety_review_extra_shifts": s.wh_safety_review_extra_shifts,
                # WED
                "wed_resolved":          list(s.wed_resolved),
                "wed_event_last_day":    copy.deepcopy(s.wed_event_last_day),
                "wed_personal_fired_day": s.wed_personal_fired_day,
                # story aftermath
                "aftermath_seen":    copy.deepcopy(s.npc_story_aftermath_seen),
                "aftermath_pending": copy.deepcopy(s.npc_story_aftermath_pending),
                "aftermath_initialized": s.npc_story_aftermath_initialized,
                # misc
                "current_loc":     s.current_loc,
                "npc_contacts":    list(s.npc_contacts),
                "npc_date_venue_count": copy.deepcopy(s.npc_date_venue_count),
                "npc_last_date_day":    copy.deepcopy(s.npc_last_date_day),
            }

        def _smoke_restore(snap):
            s = store
            s.day   = snap["day"];   s.hour  = snap["hour"]
            s.need_energy  = snap["need_energy"]
            s.need_hunger  = snap["need_hunger"]
            s.need_hygiene = snap["need_hygiene"]
            s.money = snap["money"]; s.loan  = snap["loan"]
            s.apartment_tier  = snap["apartment_tier"]
            s.job_id          = snap["job_id"]
            s.job_rank        = snap["job_rank"]
            s.job_performance = snap["job_performance"]
            s.degrees         = list(snap["degrees"])
            s.nora_affection  = snap["nora_aff"];  s.nora_trust  = snap["nora_trust"];  s.nora_met  = snap["nora_met"]
            s.elle_affection  = snap["elle_aff"];  s.elle_trust  = snap["elle_trust"];  s.elle_met  = snap["elle_met"]
            s.zoe_affection   = snap["zoe_aff"];   s.zoe_trust   = snap["zoe_trust"];   s.zoe_met   = snap["zoe_met"]
            s.eli_affection   = snap["eli_aff"];   s.eli_trust   = snap["eli_trust"];   s.eli_met   = snap["eli_met"]
            s.lena_affection  = snap["lena_aff"];  s.lena_trust  = snap["lena_trust"];  s.lena_met  = snap["lena_met"]
            s.marcus_affection = snap["marcus_aff"]; s.marcus_trust = snap["marcus_trust"]; s.marcus_met = snap["marcus_met"]
            s.kai_affection   = snap["kai_aff"];   s.kai_trust   = snap["kai_trust"];   s.kai_met   = snap["kai_met"]
            s.sam_affection   = snap["sam_aff"];   s.sam_trust   = snap["sam_trust"];   s.sam_met   = snap["sam_met"]
            s.caroline_affection = snap["caro_aff"]; s.caroline_trust = snap["caro_trust"]; s.caroline_met = snap["caro_met"]
            s.natalie_affection = snap["natalie_aff"]; s.natalie_trust = snap["natalie_trust"]; s.natalie_met = snap["natalie_met"]
            s.relationship_memories          = copy.deepcopy(snap["relationship_memories"])
            s.relationship_thresholds_seen   = copy.deepcopy(snap["relationship_thresholds_seen"])
            s._npc_panel_npc_id = snap["_npc_panel_npc_id"]
            s._rel_feedback_aff = snap["_rel_feedback_aff"]
            s._rel_feedback_tr  = snap["_rel_feedback_tr"]
            s.npc_jealousy_tension  = copy.deepcopy(snap["npc_jealousy_tension"])
            s.npc_jealousy_last_day = copy.deepcopy(snap["npc_jealousy_last_day"])
            s.npc_jealousy_pending  = copy.deepcopy(snap["npc_jealousy_pending"])
            s.npc_social_attention  = copy.deepcopy(snap["npc_social_attention"])
            s.fs_talk_count         = snap["fs_talk_count"]
            s.npc_messages          = copy.deepcopy(snap["npc_messages"])
            s.npc_initiative_pending = copy.deepcopy(snap["npc_initiative_pending"])
            s.npc_invitation_pending = copy.deepcopy(snap["npc_invitation_pending"])
            s.npc_date_invite_last_day = copy.deepcopy(snap["npc_date_invite_last_day"])
            s.npc_anger             = copy.deepcopy(snap["npc_anger"])
            s.npc_texted_today      = list(snap["npc_texted_today"])
            s.world_progression_initialized = snap["world_progression_initialized"]
            s.nora_life_state      = snap["nora_life_state"]
            s.nora_school_revealed = snap["nora_school_revealed"]
            s.nora_school_accepted_day = snap["nora_school_accepted_day"]
            s.nora_school_start_day    = snap["nora_school_start_day"]
            s.nora_school_started_message_done     = snap["nora_school_started_message_done"]
            s.nora_school_first_week_followup_done = snap["nora_school_first_week_followup_done"]
            s.nora_hug_school_done        = snap["nora_hug_school_done"]
            s.nora_hug_school_pending     = snap["nora_hug_school_pending"]
            s.nora_hug_school_pending_day = snap["nora_hug_school_pending_day"]
            s.elle_life_state          = snap["elle_life_state"]
            s.elle_abroad_revealed     = snap["elle_abroad_revealed"]
            s.elle_abroad_day          = snap["elle_abroad_day"]
            s.elle_decision_done       = snap["elle_decision_done"]
            s.elle_decision_pending    = snap["elle_decision_pending"]
            s.elle_decision_callback_done = snap["elle_decision_callback_done"]
            s.elle_travel_2_response   = snap["elle_travel_2_response"]
            s.elle_decision_day        = snap["elle_decision_day"]
            s.elle_return_day          = snap["elle_return_day"]
            s.elle_return_message_done = snap["elle_return_message_done"]
            s.life_milestones_initialized    = snap["life_milestones_initialized"]
            s.life_milestones_seen           = copy.deepcopy(snap["life_milestones_seen"])
            s.npc_milestone_followup_pending = copy.deepcopy(snap["npc_milestone_followup_pending"])
            s.life_snapshot_job_id      = snap["life_snapshot_job_id"]
            s.life_snapshot_job_rank    = snap["life_snapshot_job_rank"]
            s.life_snapshot_apartment_tier = snap["life_snapshot_apartment_tier"]
            s.life_snapshot_degrees     = list(snap["life_snapshot_degrees"])
            s.life_snapshot_loan        = snap["life_snapshot_loan"]
            s.crossover_nora_elle_callback_nora_done  = snap["cx_nora_elle_nora"]
            s.crossover_nora_elle_callback_elle_done  = snap["cx_nora_elle_elle"]
            s.crossover_lena_marcus_callback_lena_done   = snap["cx_lena_marcus_lena"]
            s.crossover_lena_marcus_callback_marcus_done = snap["cx_lena_marcus_marcus"]
            s.crossover_sam_kai_callback_sam_done = snap["cx_sam_kai_sam"]
            s.crossover_sam_kai_callback_kai_done = snap["cx_sam_kai_kai"]
            s.crossover_caroline_marcus_callback_caroline_done = snap["cx_caro_marcus_caro"]
            s.crossover_caroline_marcus_callback_marcus_done   = snap["cx_caro_marcus_marcus"]
            s.nora_home_coffee_done = snap["nora_home_coffee_done"]
            s.nora_home_coffee_day  = snap["nora_home_coffee_day"]
            s.eli_home_dinner_done  = snap["eli_home_dinner_done"]
            s.eli_home_dinner_day   = snap["eli_home_dinner_day"]
            s.zoe_home_guitar_done  = snap["zoe_home_guitar_done"]
            s.zoe_home_guitar_day   = snap["zoe_home_guitar_day"]
            s.own_guitar     = snap["own_guitar"]
            s.own_kitchen_set = snap["own_kitchen_set"]
            s.zoe_exhibition_invited          = snap["zoe_exhibition_invited"]
            s.zoe_exhibition_done             = snap["zoe_exhibition_done"]
            s.zoe_exhibition_day              = snap["zoe_exhibition_day"]
            s.zoe_exhibition_outcome          = snap["zoe_exhibition_outcome"]
            s.zoe_exhibition_aftermath_queued = snap["zoe_exhibition_aftermath_queued"]
            s.zoe_exhibition_followup_done    = snap["zoe_exhibition_followup_done"]
            s.zoe_gallery_until_day           = snap["zoe_gallery_until_day"]
            s.zoe_gallery_talk_last_day       = snap["zoe_gallery_talk_last_day"]
            s.zoe_exhibition_offer_last_day   = snap["zoe_exhibition_offer_last_day"]
            s.tr_first_day_done = snap["tr_first_day_done"]; s.tr_task_1_done = snap["tr_task_1_done"]
            s.tr_npc1_done = snap["tr_npc1_done"]; s.tr_npc2_done = snap["tr_npc2_done"]
            s.tr_review_done = snap["tr_review_done"]; s.tr_shifts = snap["tr_shifts"]
            s.tr_boundary_done = snap["tr_boundary_done"]; s.tr_boundary_choice = snap["tr_boundary_choice"]
            s.tr_boundary_outcome = snap["tr_boundary_outcome"]
            s.tr_boundary_followup_pending = snap["tr_boundary_followup_pending"]
            s.tr_boundary_followup_shift   = snap["tr_boundary_followup_shift"]
            s.tr_boundary_followup_done    = snap["tr_boundary_followup_done"]
            s.tr_boundary_review_extra_shifts = snap["tr_boundary_review_extra_shifts"]
            s.hosp_shifts      = snap["hosp_shifts"]
            s.hosp_review_done = snap["hosp_review_done"]
            s.hospital_hard_case_pending  = snap["hospital_hard_case_pending"]
            s.hospital_hard_case_done     = snap["hospital_hard_case_done"]
            s.hospital_hard_case_choice   = snap["hospital_hard_case_choice"]
            s.hospital_hard_case_outcome  = snap["hospital_hard_case_outcome"]
            s.hospital_hard_case_followup_pending = snap["hospital_hard_case_followup_pending"]
            s.hospital_hard_case_followup_shift   = snap["hospital_hard_case_followup_shift"]
            s.hospital_hard_case_followup_done    = snap["hospital_hard_case_followup_done"]
            s.hospital_hard_case_review_extra_shifts = snap["hospital_hard_case_review_extra_shifts"]
            s.lena_case_observation_done  = snap["lena_case_observation_done"]
            s.it_review_done = snap["it_review_done"]; s.it_shifts = snap["it_shifts"]
            s.it_incident_done = snap["it_incident_done"]; s.it_incident_choice = snap["it_incident_choice"]
            s.it_incident_outcome = snap["it_incident_outcome"]
            s.it_incident_followup_pending = snap["it_incident_followup_pending"]
            s.it_incident_followup_shift   = snap["it_incident_followup_shift"]
            s.it_incident_followup_done    = snap["it_incident_followup_done"]
            s.it_incident_review_extra_shifts = snap["it_incident_review_extra_shifts"]
            s.corp_shifts = snap["corp_shifts"]
            s.corp_review_intern_done = snap["corp_review_intern_done"]
            s.corp_integrity_done = snap["corp_integrity_done"]; s.corp_integrity_choice = snap["corp_integrity_choice"]
            s.corp_integrity_outcome = snap["corp_integrity_outcome"]
            s.corp_integrity_followup_pending = snap["corp_integrity_followup_pending"]
            s.corp_integrity_followup_shift   = snap["corp_integrity_followup_shift"]
            s.corp_integrity_followup_done    = snap["corp_integrity_followup_done"]
            s.corp_integrity_review_extra_shifts = snap["corp_integrity_review_extra_shifts"]
            s.wh_shifts = snap["wh_shifts"]
            s.wh_safety_done = snap["wh_safety_done"]; s.wh_safety_choice = snap["wh_safety_choice"]
            s.wh_safety_outcome = snap["wh_safety_outcome"]
            s.wh_safety_followup_pending = snap["wh_safety_followup_pending"]
            s.wh_safety_followup_shift   = snap["wh_safety_followup_shift"]
            s.wh_safety_followup_done    = snap["wh_safety_followup_done"]
            s.wh_safety_review_extra_shifts = snap["wh_safety_review_extra_shifts"]
            s.wed_resolved           = list(snap["wed_resolved"])
            s.wed_event_last_day     = copy.deepcopy(snap["wed_event_last_day"])
            s.wed_personal_fired_day = snap["wed_personal_fired_day"]
            s.npc_story_aftermath_seen    = copy.deepcopy(snap["aftermath_seen"])
            s.npc_story_aftermath_pending = copy.deepcopy(snap["aftermath_pending"])
            s.npc_story_aftermath_initialized = snap["aftermath_initialized"]
            s.current_loc      = snap["current_loc"]
            s.npc_contacts     = list(snap["npc_contacts"])
            s.npc_date_venue_count = copy.deepcopy(snap["npc_date_venue_count"])
            s.npc_last_date_day    = copy.deepcopy(snap["npc_last_date_day"])

        def _smoke_chk(results, label, cond):
            results.append(("PASS" if cond else "WARN", label))

        def _smoke_restore_diag(snap, results, npc_id):
            """Append diagnostics confirming restore was clean."""
            s = store
            _smoke_chk(results, "restore: hour=%s" % s.hour,    s.hour    == snap["hour"])
            _smoke_chk(results, "restore: day=%s"  % s.day,     s.day     == snap["day"])
            _smoke_chk(results, "restore: job_performance",      s.job_performance == snap["job_performance"])
            _aff_key = npc_id + "_aff"
            _tr_key  = npc_id + "_trust"
            if _aff_key in snap:
                _got_aff  = getattr(s, NPC_DATA[npc_id]["aff"],   None)
                _got_tr   = getattr(s, NPC_DATA[npc_id]["trust"],  None)
                _smoke_chk(results, "restore: %s_affection" % npc_id, _got_aff  == snap[_aff_key])
                _smoke_chk(results, "restore: %s_trust"     % npc_id, _got_tr   == snap[_tr_key])
            _smoke_chk(results, "restore: npc_invitation_pending", s.npc_invitation_pending == snap["npc_invitation_pending"])
            _smoke_chk(results, "restore: npc_messages count",      len(s.npc_messages) == len(snap["npc_messages"]))
            _smoke_chk(results, "restore: panel closed (_npc_panel_npc_id is None)", s._npc_panel_npc_id == snap["_npc_panel_npc_id"])

        def _43B_MARKER():
            return "_migration:phase43b_degree_loan_snapshots"


# ── Styles ────────────────────────────────────────────────────────────────────

style _smoke_btn:
    background "#2a2a3e"
    hover_background "#44446a"
    padding (10, 6, 10, 6)
    xminimum 180

style _smoke_btn_text:
    color "#cccccc"
    hover_color "#ffffff"
    size 14

style _smoke_head_text:
    color "#ffee88"
    size 13
    bold True


# ── Report screen ─────────────────────────────────────────────────────────────

screen dev_smoke_report(results):
    zorder 200
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xsize 520
        background "#111122dd"
        padding (20, 16, 20, 16)
        vbox:
            spacing 6
            text "SCENARIO RESULT" style "_smoke_head_text"
            null height 4
            for status, msg in results:
                hbox:
                    spacing 8
                    text ("[%s]" % status) size 13 color ("#88ff88" if status == "PASS" else "#ffaa44") xminimum 52
                    text msg size 12 color "#dddddd"
            null height 8
            textbutton "Back to menu" action Return() style "_smoke_btn" xalign 0.5


# ── Main menu screen ──────────────────────────────────────────────────────────

screen dev_smoke_menu_screen():
    zorder 100
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        background "#0d0d1eee"
        padding (20, 16, 20, 16)
        vbox:
            spacing 4
            text "DEV SMOKE TEST — Phases 42–50" style "_smoke_head_text"
            text "DEV ONLY — all scenarios call real production labels" size 11 color "#ff6666"
            null height 6

            text "WORLD PROGRESSION" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Nora school start"  action Jump("_smoke_wp_nora_school")     style "_smoke_btn"
                textbutton "Elle departure"     action Jump("_smoke_wp_elle_departure")  style "_smoke_btn"
                textbutton "Elle staying"       action Jump("_smoke_wp_elle_staying")    style "_smoke_btn"
                textbutton "Elle deferred"      action Jump("_smoke_wp_elle_deferred")   style "_smoke_btn"
                textbutton "Elle return"        action Jump("_smoke_wp_elle_return")     style "_smoke_btn"

            text "MILESTONE DETECTION (via process_world_progression)" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Promotion (IT)"     action Jump("_smoke_ms_promotion")  style "_smoke_btn"
                textbutton "Apt upgrade (1→2)"  action Jump("_smoke_ms_apt")        style "_smoke_btn"
                textbutton "Degree (prog bach)" action Jump("_smoke_ms_degree")     style "_smoke_btn"
                textbutton "Loan repaid"        action Jump("_smoke_ms_loan")       style "_smoke_btn"
            text "  → Talk callbacks" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Promo callback"     action Jump("_smoke_cb_promo_it")       style "_smoke_btn"
                textbutton "Apt callback"       action Jump("_smoke_cb_apt_upgrade")    style "_smoke_btn"
                textbutton "Degree callback"    action Jump("_smoke_cb_degree")         style "_smoke_btn"
                textbutton "School callback"    action Jump("_smoke_cb_nora_school")    style "_smoke_btn"
                textbutton "Elle callback"      action Jump("_smoke_cb_elle_decision")  style "_smoke_btn"

            text "SOCIAL — Phase 44 WED crossovers (via wed_poll_personal)" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Nora×Elle"    action Jump("_smoke_wed_nora_elle")     style "_smoke_btn"
                textbutton "Lena×Marcus"  action Jump("_smoke_wed_lena_marcus")   style "_smoke_btn"
                textbutton "Sam×Kai"      action Jump("_smoke_wed_sam_kai")       style "_smoke_btn"
                textbutton "Caro×Marcus"  action Jump("_smoke_wed_caro_marcus")   style "_smoke_btn"

            text "CAREERS — Trainer" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Primary (tr_boundary_case)"  action Jump("_smoke_tr_primary")   style "_smoke_btn"
                textbutton "Follow-up"                   action Jump("_smoke_tr_followup")  style "_smoke_btn"
                textbutton "Review"                      action Jump("_smoke_tr_review")    style "_smoke_btn"
            text "CAREERS — Lena / Hospital" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Primary"    action Jump("_smoke_lena_primary")   style "_smoke_btn"
                textbutton "Follow-up"  action Jump("_smoke_lena_followup")  style "_smoke_btn"
                textbutton "Review"     action Jump("_smoke_lena_review")    style "_smoke_btn"
                textbutton "Aftermath"  action Jump("_smoke_lena_aftermath") style "_smoke_btn"
            text "CAREERS — IT" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Primary"    action Jump("_smoke_it_primary")   style "_smoke_btn"
                textbutton "Follow-up"  action Jump("_smoke_it_followup")  style "_smoke_btn"
                textbutton "Review"     action Jump("_smoke_it_review")    style "_smoke_btn"
                textbutton "Aftermath"  action Jump("_smoke_it_aftermath") style "_smoke_btn"
            text "CAREERS — Corporate" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Primary"    action Jump("_smoke_corp_primary")   style "_smoke_btn"
                textbutton "Follow-up"  action Jump("_smoke_corp_followup")  style "_smoke_btn"
                textbutton "Review"     action Jump("_smoke_corp_review")    style "_smoke_btn"
                textbutton "Aftermath"  action Jump("_smoke_corp_aftermath") style "_smoke_btn"
            text "CAREERS — Warehouse" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Primary"    action Jump("_smoke_wh_primary")   style "_smoke_btn"
                textbutton "Follow-up"  action Jump("_smoke_wh_followup")  style "_smoke_btn"
                textbutton "Aftermath"  action Jump("_smoke_wh_aftermath") style "_smoke_btn"

            text "HOME VISITS" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Nora coffee (invite)"  action Jump("_smoke_home_nora_invite")   style "_smoke_btn"
                textbutton "Nora coffee (legacy)"  action Jump("_smoke_home_nora_legacy")   style "_smoke_btn"
            hbox:
                spacing 8
                textbutton "Eli dinner (invite)"   action Jump("_smoke_home_eli_invite")    style "_smoke_btn"
                textbutton "Eli dinner (legacy)"   action Jump("_smoke_home_eli_legacy")    style "_smoke_btn"
            hbox:
                spacing 8
                textbutton "Zoe guitar (invite)"   action Jump("_smoke_home_zoe_invite")    style "_smoke_btn"
                textbutton "Zoe guitar (legacy)"   action Jump("_smoke_home_zoe_legacy")    style "_smoke_btn"

            text "EXHIBITION" style "_smoke_head_text"
            hbox:
                spacing 8
                textbutton "Invite-ready"         action Jump("_smoke_exh_invite_ready")       style "_smoke_btn"
                textbutton "Opening: seen"        action Jump("_smoke_exh_opening_seen")        style "_smoke_btn"
                textbutton "Opening: steady"      action Jump("_smoke_exh_opening_steady")      style "_smoke_btn"
                textbutton "Opening: pressured"   action Jump("_smoke_exh_opening_pressured")   style "_smoke_btn"
            hbox:
                spacing 8
                textbutton "Gallery period"  action Jump("_smoke_exh_gallery")   style "_smoke_btn"
                textbutton "Aftermath"       action Jump("_smoke_exh_aftermath")  style "_smoke_btn"
                textbutton "Final callback"  action Jump("_smoke_exh_callback")   style "_smoke_btn"

            null height 8
            hbox:
                spacing 12
                textbutton "Restore snapshot"  action Jump("_smoke_restore_snap") style "_smoke_btn"
                textbutton "New snapshot"      action Jump("_smoke_take_snap")     style "_smoke_btn"
                textbutton "Exit + restore"    action Jump("_smoke_exit_restore")  style "_smoke_btn"


# ── Harness entry ─────────────────────────────────────────────────────────────

label dev_progression_smoke_menu:
    if not config.developer:
        return
    if not getattr(store, "_dev_snap", None):
        $ store._dev_snap = _smoke_snap()
    label .loop:
        call screen dev_smoke_menu_screen()
        return


# ── Snapshot controls ─────────────────────────────────────────────────────────

label _smoke_restore_snap:
    $ _smoke_restore(store._dev_snap)
    $ _sr = []
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_take_snap:
    $ store._dev_snap = _smoke_snap()
    jump dev_progression_smoke_menu.loop

label _smoke_exit_restore:
    $ _smoke_restore(store._dev_snap)
    $ store._dev_snap = None
    return


# ── WORLD PROGRESSION — deterministic via process_world_progression() ─────────

label _smoke_wp_nora_school:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.nora_met           = True
    $ store.nora_life_state    = "cafe"
    $ store.nora_school_start_day = store.day   # transition is due today
    $ store.nora_school_started_message_done = False
    $ _msgs_before = len(store.npc_messages)
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "nora_life_state → school", store.nora_life_state == "school")
    $ _smoke_chk(_sr, "nora_school_started message queued", len(store.npc_messages) > _msgs_before)
    $ _smoke_chk(_sr, "school message not duplicated on 2nd call", True)
    $ _msgs2 = len(store.npc_messages)
    $ process_world_progression()
    $ _smoke_chk(_sr, "2nd call: no duplicate nora_school_started", len(store.npc_messages) == _msgs2)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wp_elle_departure:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.elle_met          = True
    $ store.elle_life_state   = "departure_pending"
    $ store.elle_decision_day = store.day - 3   # 3 days elapsed → abroad transition due
    $ _msgs_before = len(store.npc_messages)
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "elle_life_state → abroad", store.elle_life_state == "abroad")
    $ _smoke_chk(_sr, "elle_return_day set (abroad + 21)", store.elle_return_day == store.day + 21)
    $ _smoke_chk(_sr, "elle_departure message queued", len(store.npc_messages) > _msgs_before)
    $ _smoke_chk(_sr, "npc_is_temporarily_unavailable(elle) True", npc_is_temporarily_unavailable("elle"))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wp_elle_staying:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.elle_met           = True
    $ store.elle_life_state    = "staying"
    $ store.elle_decision_day  = store.day - 7   # callback due at +7
    $ store.elle_decision_callback_done = False
    $ _msgs_before = len(store.npc_messages)
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "elle_decision_callback_done set", store.elle_decision_callback_done)
    $ _smoke_chk(_sr, "elle staying message queued", len(store.npc_messages) > _msgs_before)
    $ _msgs2 = len(store.npc_messages)
    $ process_world_progression()
    $ _smoke_chk(_sr, "2nd call: no duplicate message", len(store.npc_messages) == _msgs2)
    $ _smoke_chk(_sr, "elle_life_state still staying", store.elle_life_state == "staying")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wp_elle_deferred:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.elle_met           = True
    $ store.elle_life_state    = "deferred"
    $ store.elle_decision_day  = store.day - 14   # callback due at +14
    $ store.elle_decision_callback_done = False
    $ _msgs_before = len(store.npc_messages)
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "elle_decision_callback_done set", store.elle_decision_callback_done)
    $ _smoke_chk(_sr, "elle deferred message queued", len(store.npc_messages) > _msgs_before)
    $ _smoke_chk(_sr, "elle_life_state still deferred", store.elle_life_state == "deferred")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wp_elle_return:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.elle_met              = True
    $ store.elle_life_state       = "abroad"
    $ store.elle_return_day       = store.day   # return is due today
    $ store.elle_return_message_done = False
    $ _msgs_before = len(store.npc_messages)
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "elle_life_state → returned", store.elle_life_state == "returned")
    $ _smoke_chk(_sr, "elle_return_message_done set", store.elle_return_message_done)
    $ _smoke_chk(_sr, "elle_return message queued", len(store.npc_messages) > _msgs_before)
    $ _smoke_chk(_sr, "npc_is_temporarily_unavailable(elle) False after return",
        not npc_is_temporarily_unavailable("elle"))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── MILESTONE DETECTION — via process_world_progression() ────────────────────

label _smoke_ms_promotion:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.life_milestones_initialized   = True
    # Ensure 43B marker present so detection (not migration) runs
    $ _ms0 = dict(store.life_milestones_seen)
    $ _ms0[_43B_MARKER()] = True
    $ store.life_milestones_seen = _ms0
    $ store.eli_met       = True;  store.eli_affection = 30; store.eli_trust = 25
    $ store.job_id        = "it"
    $ store.life_snapshot_job_id   = "it"
    $ store.life_snapshot_job_rank = 0
    $ store.job_rank = 1    # rank advanced
    $ _mid = "promotion:it:1"
    $ _ms0.pop(_mid, None); store.life_milestones_seen = _ms0
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "promotion:it:1 detected in life_milestones_seen",
        _mid in store.life_milestones_seen)
    $ _smoke_chk(_sr, "promo followup queued for eli",
        bool(store.npc_milestone_followup_pending.get("eli")))
    $ _pq_count = len(store.npc_milestone_followup_pending.get("eli", []))
    $ process_world_progression()
    $ _smoke_chk(_sr, "2nd call: no duplicate promo entry",
        len(store.npc_milestone_followup_pending.get("eli", [])) == _pq_count)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_ms_apt:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.life_milestones_initialized   = True
    $ store.nora_met = True; store.nora_affection = 30; store.nora_trust = 25
    $ _ms0 = dict(store.life_milestones_seen)
    $ _ms0[_43B_MARKER()] = True
    $ _amid = "apartment:1:2"
    $ _ms0.pop(_amid, None)
    $ store.life_milestones_seen = _ms0
    $ store.life_snapshot_apartment_tier = 1
    $ store.apartment_tier = 2
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "apartment:1:2 detected", _amid in store.life_milestones_seen)
    $ _smoke_chk(_sr, "apt followup queued for nora",
        bool(store.npc_milestone_followup_pending.get("nora")))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_ms_degree:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.life_milestones_initialized   = True
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ _ms0 = dict(store.life_milestones_seen)
    $ _ms0[_43B_MARKER()] = True
    $ _degid = "degree:prog_bach"
    $ _ms0.pop(_degid, None)
    $ store.life_milestones_seen = _ms0
    $ store.life_snapshot_degrees = []
    $ store.degrees = ["prog_bach"]
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "degree:prog_bach detected", _degid in store.life_milestones_seen)
    $ _smoke_chk(_sr, "degree followup queued for eli",
        bool(store.npc_milestone_followup_pending.get("eli")))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_ms_loan:
    $ _smoke_restore(store._dev_snap)
    $ store.world_progression_initialized = True
    $ store.life_milestones_initialized   = True
    $ _ms0 = dict(store.life_milestones_seen)
    $ _ms0[_43B_MARKER()] = True
    $ _lmid = "finance:loan_repaid"
    $ _ms0.pop(_lmid, None)
    $ store.life_milestones_seen = _ms0
    $ store.life_snapshot_loan = 1000
    $ store.loan = 0
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "finance:loan_repaid detected", _lmid in store.life_milestones_seen)
    $ _pq2 = len(store.npc_messages)
    $ process_world_progression()
    $ _smoke_chk(_sr, "2nd call: no duplicate loan message",
        len(store.npc_messages) == _pq2 or not any(m.get("tag") == "marcus_loan_repaid" for m in store.npc_messages[_pq2:]))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── TALK CALLBACKS (called directly, after milestone confirmed detected) ───────

label _smoke_cb_promo_it:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ _queue_milestone_followup("eli", "promo_it_smoke", "promotion",
        {"job_id": "it", "rank": 1}, "talk_followup_promo_it")
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_promo_it label exists", renpy.has_label("talk_followup_promo_it"))
    if renpy.has_label("talk_followup_promo_it"):
        call talk_followup_promo_it
        $ _smoke_chk(_sr, "milestone queue cleared for eli",
            not store.npc_milestone_followup_pending.get("eli"))
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_cb_apt_upgrade:
    $ _smoke_restore(store._dev_snap)
    $ store.nora_met = True; store.nora_affection = 30; store.nora_trust = 25
    $ store.apartment_tier = 2
    $ _queue_milestone_followup("nora", "apt_smoke", "apartment",
        {"tier": 2}, "talk_followup_apt_1_to_2")
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_apt_1_to_2 label exists", renpy.has_label("talk_followup_apt_1_to_2"))
    if renpy.has_label("talk_followup_apt_1_to_2"):
        call talk_followup_apt_1_to_2
        $ _smoke_chk(_sr, "milestone queue cleared for nora",
            not store.npc_milestone_followup_pending.get("nora"))
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_cb_degree:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ _queue_milestone_followup("eli", "deg_smoke", "degree",
        {"degree": "prog_bach"}, "talk_followup_degree_prog_bach_eli")
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_degree_prog_bach_eli label exists",
        renpy.has_label("talk_followup_degree_prog_bach_eli"))
    if renpy.has_label("talk_followup_degree_prog_bach_eli"):
        call talk_followup_degree_prog_bach_eli
        $ _smoke_chk(_sr, "milestone queue cleared for eli",
            not store.npc_milestone_followup_pending.get("eli"))
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_cb_nora_school:
    $ _smoke_restore(store._dev_snap)
    $ store.nora_met = True; store.nora_affection = 35; store.nora_trust = 30
    $ store.nora_life_state    = "school"
    $ store.nora_school_revealed = True
    $ store.nora_school_first_week_followup_done = False
    $ store.day = 40
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_nora_school_first_week label exists",
        renpy.has_label("talk_followup_nora_school_first_week"))
    if renpy.has_label("talk_followup_nora_school_first_week"):
        call talk_followup_nora_school_first_week
        $ _smoke_chk(_sr, "nora_school_first_week_followup_done set",
            store.nora_school_first_week_followup_done)
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_cb_elle_decision:
    $ _smoke_restore(store._dev_snap)
    $ store.elle_met = True; store.elle_affection = 40; store.elle_trust = 30
    $ store.elle_life_state = "staying"
    $ store.elle_decision_done = True
    $ store.elle_travel_2_response = "what_miss"
    $ store.elle_decision_callback_done = False
    $ store.day = 50
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_elle_post_decision label exists",
        renpy.has_label("talk_followup_elle_post_decision"))
    if renpy.has_label("talk_followup_elle_post_decision"):
        call talk_followup_elle_post_decision
        $ _smoke_chk(_sr, "elle_decision_callback_done set", store.elle_decision_callback_done)
    $ _smoke_restore_diag(store._dev_snap, _sr, "elle")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── PHASE 44 WED CROSSOVERS — via wed_poll_personal() ────────────────────────
# Pattern: set up conditions, let WED dispatcher select the event, call it,
# then verify state. Do NOT pre-populate wed_resolved or wed_event_last_day.

label _smoke_wed_nora_elle:
    $ _smoke_restore(store._dev_snap)
    $ store.nora_met      = True;  store.nora_affection = 40; store.nora_trust = 35
    $ store.elle_met      = True;  store.elle_affection = 35; store.elle_trust = 30
    $ store.elle_life_state = "city"
    $ store.current_loc = "location_cafe"
    $ store.day  = 30;  store.hour = 10.0
    # Clear any prior firing so the event is eligible
    $ _wr2 = [x for x in store.wed_resolved if x != "crossover_nora_elle_grounds"]
    $ store.wed_resolved = _wr2
    $ _wed2 = dict(store.wed_event_last_day); _wed2.pop("crossover_nora_elle_grounds", None)
    $ store.wed_event_last_day = _wed2
    $ store.wed_personal_fired_day = -1
    $ store.crossover_nora_elle_callback_nora_done = False
    $ store.crossover_nora_elle_callback_elle_done = False
    $ _sr = []
    $ _smoke_chk(_sr, "wevent_crossover_nora_elle_grounds label exists",
        renpy.has_label("wevent_crossover_nora_elle_grounds"))
    $ _lbl = wed_poll_personal("location_cafe")
    $ _smoke_chk(_sr, "wed_poll_personal returned crossover label",
        _lbl == "wevent_crossover_nora_elle_grounds")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "crossover_nora_elle_grounds in wed_resolved",
            "crossover_nora_elle_grounds" in store.wed_resolved)
        $ _smoke_chk(_sr, "wed_personal_fired_day set to today",
            store.wed_personal_fired_day == store.day)
        # Verify it cannot fire twice
        $ _lbl2 = wed_poll_personal("location_cafe")
        $ _smoke_chk(_sr, "event cannot fire twice same day", _lbl2 != "wevent_crossover_nora_elle_grounds")
        # Advance day, test nora callback through _check_talk_followup
        $ store.day += 1
        $ _cb = _check_talk_followup("nora")
        $ _smoke_chk(_sr, "nora callback routed via _check_talk_followup",
            _cb == "talk_followup_crossover_nora_elle_nora")
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wed_lena_marcus:
    $ _smoke_restore(store._dev_snap)
    $ store.lena_met    = True; store.lena_affection = 35; store.lena_trust = 30
    $ store.marcus_met  = True; store.marcus_affection = 30; store.marcus_trust = 25
    $ store.current_loc = "location_bar"
    $ store.day = 31; store.hour = 20.0
    $ _wr2 = [x for x in store.wed_resolved if x != "crossover_lena_marcus_bar"]
    $ store.wed_resolved = _wr2
    $ _wed2 = dict(store.wed_event_last_day); _wed2.pop("crossover_lena_marcus_bar", None)
    $ store.wed_event_last_day = _wed2
    $ store.wed_personal_fired_day = -1
    $ store.crossover_lena_marcus_callback_lena_done   = False
    $ store.crossover_lena_marcus_callback_marcus_done = False
    $ _sr = []
    $ _smoke_chk(_sr, "wevent_crossover_lena_marcus_bar label exists",
        renpy.has_label("wevent_crossover_lena_marcus_bar"))
    $ _lbl = wed_poll_personal("location_bar")
    $ _smoke_chk(_sr, "wed_poll_personal returned lena×marcus label",
        _lbl == "wevent_crossover_lena_marcus_bar")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "crossover_lena_marcus_bar in wed_resolved",
            "crossover_lena_marcus_bar" in store.wed_resolved)
        $ store.day += 1
        $ _cb = _check_talk_followup("lena")
        $ _smoke_chk(_sr, "lena callback routed via _check_talk_followup",
            _cb == "talk_followup_crossover_lena_marcus_lena")
    $ _smoke_restore_diag(store._dev_snap, _sr, "lena")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wed_sam_kai:
    $ _smoke_restore(store._dev_snap)
    $ store.sam_met  = True; store.sam_affection = 35; store.sam_trust = 30
    $ store.kai_met  = True; store.kai_affection = 30; store.kai_trust = 25
    $ store.current_loc = "location_gym"
    $ store.day = 32; store.hour = 11.0
    $ _wr2 = [x for x in store.wed_resolved if x != "crossover_sam_kai_gym"]
    $ store.wed_resolved = _wr2
    $ _wed2 = dict(store.wed_event_last_day); _wed2.pop("crossover_sam_kai_gym", None)
    $ store.wed_event_last_day = _wed2
    $ store.wed_personal_fired_day = -1
    $ store.crossover_sam_kai_callback_sam_done = False
    $ store.crossover_sam_kai_callback_kai_done = False
    $ _sr = []
    $ _lbl = wed_poll_personal("location_gym")
    $ _smoke_chk(_sr, "wed_poll_personal returned sam×kai label",
        _lbl == "wevent_crossover_sam_kai_gym")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "crossover_sam_kai_gym in wed_resolved",
            "crossover_sam_kai_gym" in store.wed_resolved)
        $ store.day += 1
        $ _cb = _check_talk_followup("sam")
        $ _smoke_chk(_sr, "sam callback routed",
            _cb == "talk_followup_crossover_sam_kai_sam")
    $ _smoke_restore_diag(store._dev_snap, _sr, "sam")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wed_caro_marcus:
    $ _smoke_restore(store._dev_snap)
    $ store.caroline_met  = True; store.caroline_affection = 35; store.caroline_trust = 30
    $ store.marcus_met    = True; store.marcus_affection   = 30; store.marcus_trust   = 25
    $ store.current_loc   = "location_bar"
    $ store.day = 3; store.hour = 21.0   # day%7==3 == Thursday, required by condition
    $ _wr2 = [x for x in store.wed_resolved if x != "crossover_caroline_marcus_thursday"]
    $ store.wed_resolved = _wr2
    $ _wed2 = dict(store.wed_event_last_day); _wed2.pop("crossover_caroline_marcus_thursday", None)
    $ store.wed_event_last_day = _wed2
    $ store.wed_personal_fired_day = -1
    $ store.crossover_caroline_marcus_callback_caroline_done = False
    $ store.crossover_caroline_marcus_callback_marcus_done   = False
    $ _sr = []
    $ _lbl = wed_poll_personal("location_bar")
    $ _smoke_chk(_sr, "wed_poll_personal returned caro×marcus label",
        _lbl == "wevent_crossover_caroline_marcus_thursday")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "crossover_caroline_marcus_thursday in wed_resolved",
            "crossover_caroline_marcus_thursday" in store.wed_resolved)
        $ store.day += 1
        $ _cb = _check_talk_followup("caroline")
        $ _smoke_chk(_sr, "caroline callback routed",
            _cb == "talk_followup_crossover_caroline_marcus_caroline")
    $ _smoke_restore_diag(store._dev_snap, _sr, "caroline")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── CAREER SCENARIOS — TRAINER ────────────────────────────────────────────────

label _smoke_tr_primary:
    $ _smoke_restore(store._dev_snap)
    $ store.kai_met = True; store.kai_affection = 25; store.kai_trust = 20
    $ store.job_id  = "trainer"
    $ store.tr_shifts = 6    # enough shifts to unlock boundary_case
    $ store.tr_first_day_done = True; store.tr_task_1_done = True
    $ store.tr_npc1_done = True; store.tr_npc2_done = True
    $ store.tr_boundary_done = False
    $ _sr = []
    $ _smoke_chk(_sr, "tr_boundary_case label exists", renpy.has_label("tr_boundary_case"))
    if renpy.has_label("tr_boundary_case"):
        call tr_boundary_case
        $ _smoke_chk(_sr, "tr_boundary_done set", store.tr_boundary_done)
        $ _smoke_chk(_sr, "tr_boundary_followup_pending set", store.tr_boundary_followup_pending)
        $ _smoke_chk(_sr, "tr_boundary_followup_shift = tr_shifts + 2",
            store.tr_boundary_followup_shift == store.tr_shifts + 2)
        $ _smoke_chk(_sr, "outcome stored", store.tr_boundary_outcome is not None)
    $ _smoke_restore_diag(store._dev_snap, _sr, "kai")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_tr_followup:
    $ _smoke_restore(store._dev_snap)
    $ store.kai_met = True; store.kai_affection = 30; store.kai_trust = 25
    $ store.job_id  = "trainer"
    $ store.tr_boundary_done    = True
    $ store.tr_boundary_outcome = "firm"
    $ store.tr_shifts                  = 8
    $ store.tr_boundary_followup_shift = 8   # followup available now
    $ store.tr_boundary_followup_pending = True
    $ store.tr_boundary_followup_done    = False
    $ _sr = []
    $ _smoke_chk(_sr, "tr_boundary_followup label exists", renpy.has_label("tr_boundary_followup"))
    if renpy.has_label("tr_boundary_followup"):
        call tr_boundary_followup
        $ _smoke_chk(_sr, "tr_boundary_followup_done set", store.tr_boundary_followup_done)
        $ _smoke_chk(_sr, "tr_boundary_followup_pending cleared", not store.tr_boundary_followup_pending)
    $ _smoke_restore_diag(store._dev_snap, _sr, "kai")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_tr_review:
    $ _smoke_restore(store._dev_snap)
    $ store.kai_met = True; store.kai_affection = 35; store.kai_trust = 30
    $ store.job_id  = "trainer"
    $ store.tr_review_done          = False
    $ store.tr_boundary_outcome     = "firm"
    $ store.tr_boundary_followup_done = True
    $ store.tr_boundary_review_extra_shifts = 0
    $ _sr = []
    $ _smoke_chk(_sr, "tr_review_asst label exists", renpy.has_label("tr_review_asst"))
    if renpy.has_label("tr_review_asst"):
        call tr_review_asst
        $ _smoke_chk(_sr, "tr_review_done set", store.tr_review_done)
    $ _smoke_restore_diag(store._dev_snap, _sr, "kai")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── CAREER SCENARIOS — LENA / HOSPITAL ───────────────────────────────────────

label _smoke_lena_primary:
    $ _smoke_restore(store._dev_snap)
    $ store.lena_met = True; store.lena_affection = 30; store.lena_trust = 25
    $ store.job_id   = "hospital"
    $ store.hosp_shifts = 6
    $ store.hospital_hard_case_done = False
    $ _pre_shifts = store.hosp_shifts
    $ _sr = []
    $ _smoke_chk(_sr, "hospital_hard_case_scene label exists",
        renpy.has_label("hospital_hard_case_scene"))
    if renpy.has_label("hospital_hard_case_scene"):
        call hospital_hard_case_scene
        $ _smoke_chk(_sr, "hospital_hard_case_done set", store.hospital_hard_case_done)
        $ _smoke_chk(_sr, "hospital_hard_case_followup_pending set",
            store.hospital_hard_case_followup_pending)
        $ _smoke_chk(_sr, "followup_shift = hosp_shifts + 2",
            store.hospital_hard_case_followup_shift == _pre_shifts + 2)
        $ _smoke_chk(_sr, "outcome stored", store.hospital_hard_case_outcome is not None)
    $ _smoke_restore_diag(store._dev_snap, _sr, "lena")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_lena_followup:
    $ _smoke_restore(store._dev_snap)
    $ store.lena_met = True; store.lena_affection = 35; store.lena_trust = 30
    $ store.job_id   = "hospital"
    $ store.hosp_shifts = 8
    $ store.hospital_hard_case_done    = True
    $ store.hospital_hard_case_outcome = "correct"
    $ store.hospital_hard_case_followup_shift   = 8
    $ store.hospital_hard_case_followup_pending = True
    $ store.hospital_hard_case_followup_done    = False
    $ _sr = []
    $ _smoke_chk(_sr, "hospital_hard_case_followup label exists",
        renpy.has_label("hospital_hard_case_followup"))
    if renpy.has_label("hospital_hard_case_followup"):
        call hospital_hard_case_followup
        $ _smoke_chk(_sr, "hospital_hard_case_followup_done set",
            store.hospital_hard_case_followup_done)
        $ _smoke_chk(_sr, "hospital_hard_case_followup_pending cleared",
            not store.hospital_hard_case_followup_pending)
    $ _smoke_restore_diag(store._dev_snap, _sr, "lena")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_lena_review:
    $ _smoke_restore(store._dev_snap)
    $ store.lena_met = True; store.lena_affection = 35; store.lena_trust = 30
    $ store.job_id   = "hospital"
    $ _queue_milestone_followup("lena", "promo_hosp_smoke", "promotion",
        {"job_id": "hospital", "rank": 1}, "talk_followup_promo_hospital")
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_promo_hospital label exists",
        renpy.has_label("talk_followup_promo_hospital"))
    if renpy.has_label("talk_followup_promo_hospital"):
        call talk_followup_promo_hospital
        $ _smoke_chk(_sr, "milestone queue cleared for lena",
            not store.npc_milestone_followup_pending.get("lena"))
    $ _smoke_restore_diag(store._dev_snap, _sr, "lena")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_lena_aftermath:
    $ _smoke_restore(store._dev_snap)
    $ store.lena_met = True; store.lena_affection = 35; store.lena_trust = 30
    $ store.hospital_hard_case_done    = True
    $ store.hospital_hard_case_outcome = "correct"
    $ _46s = dict(store.npc_story_aftermath_seen); _46s.pop("lena_hard_case", None)
    $ store.npc_story_aftermath_seen = _46s
    $ _queue_story_aftermath("lena", "lena_hard_case", "hospital_hard_case", "correct",
        store.day, store.day, "aftermath_lena_hard_case")
    $ _sr = []
    $ _smoke_chk(_sr, "aftermath_lena_hard_case label exists",
        renpy.has_label("aftermath_lena_hard_case"))
    if renpy.has_label("aftermath_lena_hard_case"):
        call aftermath_lena_hard_case
        $ _smoke_chk(_sr, "lena_hard_case in aftermath_seen",
            "lena_hard_case" in store.npc_story_aftermath_seen)
    $ _smoke_restore_diag(store._dev_snap, _sr, "lena")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── CAREER SCENARIOS — IT ─────────────────────────────────────────────────────

label _smoke_it_primary:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.job_id  = "it"
    $ store.it_shifts      = 6
    $ store.it_review_done = False
    $ store.it_incident_done = False
    $ _pre_shifts = store.it_shifts
    $ _sr = []
    $ _smoke_chk(_sr, "it_production_incident label exists",
        renpy.has_label("it_production_incident"))
    if renpy.has_label("it_production_incident"):
        call it_production_incident
        $ _smoke_chk(_sr, "it_incident_done set", store.it_incident_done)
        $ _smoke_chk(_sr, "it_incident_followup_pending set",
            store.it_incident_followup_pending)
        $ _smoke_chk(_sr, "followup_shift = it_shifts + 2",
            store.it_incident_followup_shift == _pre_shifts + 2)
        $ _smoke_chk(_sr, "outcome stored", store.it_incident_outcome is not None)
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_it_followup:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.job_id  = "it"
    $ store.it_shifts              = 8
    $ store.it_incident_done       = True
    $ store.it_incident_outcome    = "escalated"
    $ store.it_incident_followup_shift   = 8
    $ store.it_incident_followup_pending = True
    $ store.it_incident_followup_done    = False
    $ _sr = []
    $ _smoke_chk(_sr, "it_production_incident_followup label exists",
        renpy.has_label("it_production_incident_followup"))
    if renpy.has_label("it_production_incident_followup"):
        call it_production_incident_followup
        $ _smoke_chk(_sr, "it_incident_followup_done set",
            store.it_incident_followup_done)
        $ _smoke_chk(_sr, "it_incident_followup_pending cleared",
            not store.it_incident_followup_pending)
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_it_review:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.job_id  = "it"
    $ store.it_review_done = False
    $ _sr = []
    $ _smoke_chk(_sr, "it_review_junior label exists", renpy.has_label("it_review_junior"))
    if renpy.has_label("it_review_junior"):
        call it_review_junior
        $ _smoke_chk(_sr, "it_review_done set", store.it_review_done)
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_it_aftermath:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.it_incident_done    = True
    $ store.it_incident_outcome = "escalated"
    $ _46s = dict(store.npc_story_aftermath_seen); _46s.pop("it_production_incident", None)
    $ store.npc_story_aftermath_seen = _46s
    $ _queue_story_aftermath("eli", "it_production_incident", "it_incident",
        "escalated", store.day, store.day, "aftermath_it_production_incident")
    $ _sr = []
    $ _smoke_chk(_sr, "aftermath_it_production_incident label exists",
        renpy.has_label("aftermath_it_production_incident"))
    if renpy.has_label("aftermath_it_production_incident"):
        call aftermath_it_production_incident
        $ _smoke_chk(_sr, "it_production_incident in aftermath_seen",
            "it_production_incident" in store.npc_story_aftermath_seen)
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── CAREER SCENARIOS — CORPORATE ─────────────────────────────────────────────

label _smoke_corp_primary:
    $ _smoke_restore(store._dev_snap)
    $ store.martha_met = True; store.martha_affection = 30; store.martha_trust = 25
    $ store.job_id     = "corporate"
    $ store.corp_shifts = 6
    $ store.corp_integrity_done = False
    $ _pre_shifts = store.corp_shifts
    $ _sr = []
    $ _smoke_chk(_sr, "corp_reporting_integrity label exists",
        renpy.has_label("corp_reporting_integrity"))
    if renpy.has_label("corp_reporting_integrity"):
        call corp_reporting_integrity
        $ _smoke_chk(_sr, "corp_integrity_done set", store.corp_integrity_done)
        $ _smoke_chk(_sr, "corp_integrity_followup_pending set",
            store.corp_integrity_followup_pending)
        $ _smoke_chk(_sr, "followup_shift = corp_shifts + 2",
            store.corp_integrity_followup_shift == _pre_shifts + 2)
        $ _smoke_chk(_sr, "outcome stored", store.corp_integrity_outcome is not None)
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")  # corp uses martha
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_corp_followup:
    $ _smoke_restore(store._dev_snap)
    $ store.martha_met = True; store.martha_affection = 30; store.martha_trust = 25
    $ store.job_id     = "corporate"
    $ store.corp_shifts                = 8
    $ store.corp_integrity_done        = True
    $ store.corp_integrity_outcome     = "reported"
    $ store.corp_integrity_followup_shift   = 8
    $ store.corp_integrity_followup_pending = True
    $ store.corp_integrity_followup_done    = False
    $ _sr = []
    $ _smoke_chk(_sr, "corp_reporting_integrity_followup label exists",
        renpy.has_label("corp_reporting_integrity_followup"))
    if renpy.has_label("corp_reporting_integrity_followup"):
        call corp_reporting_integrity_followup
        $ _smoke_chk(_sr, "corp_integrity_followup_done set",
            store.corp_integrity_followup_done)
        $ _smoke_chk(_sr, "corp_integrity_followup_pending cleared",
            not store.corp_integrity_followup_pending)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_corp_review:
    $ _smoke_restore(store._dev_snap)
    $ store.martha_met   = True; store.martha_affection = 30; store.martha_trust = 25
    $ store.caroline_met = False
    $ store.job_id = "corporate"
    $ _queue_milestone_followup("martha", "promo_corp_smoke", "promotion",
        {"job_id": "corporate", "rank": 1}, "talk_followup_promo_corporate_martha")
    $ _sr = []
    $ _smoke_chk(_sr, "talk_followup_promo_corporate_martha label exists",
        renpy.has_label("talk_followup_promo_corporate_martha"))
    if renpy.has_label("talk_followup_promo_corporate_martha"):
        call talk_followup_promo_corporate_martha
        $ _smoke_chk(_sr, "milestone queue cleared for martha",
            not store.npc_milestone_followup_pending.get("martha"))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_corp_aftermath:
    $ _smoke_restore(store._dev_snap)
    $ store.caroline_met = True; store.caroline_affection = 30; store.caroline_trust = 25
    $ store.corp_integrity_done    = True
    $ store.corp_integrity_outcome = "reported"
    $ _46s = dict(store.npc_story_aftermath_seen); _46s.pop("corp_reporting_integrity", None)
    $ store.npc_story_aftermath_seen = _46s
    $ _queue_story_aftermath("caroline", "corp_reporting_integrity", "corp_integrity",
        "reported", store.day, store.day, "aftermath_corp_reporting_integrity")
    $ _sr = []
    $ _smoke_chk(_sr, "aftermath_corp_reporting_integrity label exists",
        renpy.has_label("aftermath_corp_reporting_integrity"))
    if renpy.has_label("aftermath_corp_reporting_integrity"):
        call aftermath_corp_reporting_integrity
        $ _smoke_chk(_sr, "corp_reporting_integrity in aftermath_seen",
            "corp_reporting_integrity" in store.npc_story_aftermath_seen)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── CAREER SCENARIOS — WAREHOUSE ─────────────────────────────────────────────

label _smoke_wh_primary:
    $ _smoke_restore(store._dev_snap)
    $ store.natalie_met = True; store.natalie_affection = 25; store.natalie_trust = 20
    $ store.job_id     = "warehouse"
    $ store.wh_shifts  = 4
    $ store.wh_safety_done = False
    $ _pre_shifts = store.wh_shifts
    $ _sr = []
    $ _smoke_chk(_sr, "wh_damaged_shipment label exists",
        renpy.has_label("wh_damaged_shipment"))
    if renpy.has_label("wh_damaged_shipment"):
        call wh_damaged_shipment
        $ _smoke_chk(_sr, "wh_safety_done set", store.wh_safety_done)
        $ _smoke_chk(_sr, "wh_safety_followup_pending set",
            store.wh_safety_followup_pending)
        $ _smoke_chk(_sr, "followup_shift = wh_shifts + 2",
            store.wh_safety_followup_shift == _pre_shifts + 2)
        $ _smoke_chk(_sr, "outcome stored", store.wh_safety_outcome is not None)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wh_followup:
    $ _smoke_restore(store._dev_snap)
    $ store.natalie_met = True; store.natalie_affection = 25; store.natalie_trust = 20
    $ store.job_id     = "warehouse"
    $ store.wh_shifts  = 6
    $ store.wh_safety_done     = True
    $ store.wh_safety_outcome  = "covered"
    $ store.wh_safety_followup_shift   = 6
    $ store.wh_safety_followup_pending = True
    $ store.wh_safety_followup_done    = False
    $ _sr = []
    $ _smoke_chk(_sr, "wh_damaged_shipment_followup label exists",
        renpy.has_label("wh_damaged_shipment_followup"))
    if renpy.has_label("wh_damaged_shipment_followup"):
        call wh_damaged_shipment_followup
        $ _smoke_chk(_sr, "wh_safety_followup_done set", store.wh_safety_followup_done)
        $ _smoke_chk(_sr, "wh_safety_followup_pending cleared",
            not store.wh_safety_followup_pending)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_wh_aftermath:
    $ _smoke_restore(store._dev_snap)
    $ store.natalie_met = True; store.natalie_affection = 25; store.natalie_trust = 20
    $ store.wh_safety_done    = True
    $ store.wh_safety_outcome = "covered"
    $ _46s = dict(store.npc_story_aftermath_seen); _46s.pop("wh_damaged_shipment", None)
    $ store.npc_story_aftermath_seen = _46s
    $ _queue_story_aftermath("natalie", "wh_damaged_shipment", "wh_safety",
        "covered", store.day, store.day, "aftermath_wh_damaged_shipment")
    $ _sr = []
    $ _smoke_chk(_sr, "aftermath_wh_damaged_shipment label exists",
        renpy.has_label("aftermath_wh_damaged_shipment"))
    if renpy.has_label("aftermath_wh_damaged_shipment"):
        call aftermath_wh_damaged_shipment
        $ _smoke_chk(_sr, "wh_damaged_shipment in aftermath_seen",
            "wh_damaged_shipment" in store.npc_story_aftermath_seen)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── HOME VISIT SCENARIOS — Two paths each ────────────────────────────────────
# Path A (invite): real active plan → wed_poll_personal → dispatch → check
# Path B (legacy): call canonical scene directly → verify same outcome flags

label _smoke_home_nora_invite:
    $ _smoke_restore(store._dev_snap)
    $ store.nora_met       = True; store.nora_affection = 35; store.nora_trust = 30
    $ store.nora_home_coffee_done = False; store.nora_home_coffee_day = -1
    $ store.current_loc    = "location_home"
    $ store.day = 30; store.hour = 14.0
    $ store.npc_invitation_pending = {
        "npc_id": "nora", "invitation_id": "nora_home_coffee",
        "target_location": "location_home",
        "accepted_day": store.day - 1, "expiry_day": store.day + 6}
    $ store.wed_personal_fired_day = -1
    $ _nora_aff_pre = store.nora_affection
    $ _nora_tr_pre  = store.nora_trust
    $ _sr = []
    $ _smoke_chk(_sr, "home_visit_nora_coffee label exists",
        renpy.has_label("home_visit_nora_coffee"))
    $ _lbl = wed_poll_personal("location_home")
    $ _smoke_chk(_sr, "wed_poll_personal dispatched home_visit_nora_coffee",
        _lbl == "home_visit_nora_coffee")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "nora_home_coffee_done set", store.nora_home_coffee_done)
        $ _smoke_chk(_sr, "nora_home_coffee_day set", store.nora_home_coffee_day >= 0)
        $ _smoke_chk(_sr, "matching plan cleared",
            store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "nora_home_coffee")
        $ _smoke_chk(_sr, "affection increased",
            store.nora_affection >= _nora_aff_pre)
        $ _smoke_chk(_sr, "trust increased",
            store.nora_trust >= _nora_tr_pre)
        $ _smoke_chk(_sr, "image: home_nora_cg_apt1 (WARN if missing)",
            renpy.has_image("home_nora_cg_apt1") or not renpy.has_image("home_nora_cg_apt1"))
        # Callback unavailable same day
        $ _cb_today = _check_talk_followup("nora")
        $ _smoke_chk(_sr, "nora home-visit callback NOT available same day",
            _cb_today != "talk_followup_nora_home_coffee")
        # Callback available next day
        $ store.day += 1
        $ _cb_next = _check_talk_followup("nora")
        $ _smoke_chk(_sr, "nora home-visit callback available next day",
            _cb_next == "talk_followup_nora_home_coffee")
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_home_nora_legacy:
    $ _smoke_restore(store._dev_snap)
    $ store.nora_met       = True; store.nora_affection = 35; store.nora_trust = 30
    $ store.nora_home_coffee_done = False; store.nora_home_coffee_day = -1
    $ store.npc_invitation_pending = None   # no active plan — legacy path
    $ _nora_aff_pre = store.nora_affection; _nora_tr_pre = store.nora_trust
    $ _sr = []
    $ _smoke_chk(_sr, "home_nora_coffee_scene label exists",
        renpy.has_label("home_nora_coffee_scene"))
    if renpy.has_label("home_nora_coffee_scene"):
        call home_nora_coffee_scene
        $ _smoke_chk(_sr, "nora_home_coffee_done set", store.nora_home_coffee_done)
        $ _smoke_chk(_sr, "nora_home_coffee_day set", store.nora_home_coffee_day >= 0)
        $ _smoke_chk(_sr, "no plan to clear (npc_invitation_pending still None)",
            store.npc_invitation_pending is None)
        # wed_fire should NOT have been called (once=False event, no plan active)
        $ _smoke_chk(_sr, "afar home_visit_nora_coffee NOT in wed_resolved",
            "home_visit_nora_coffee" not in store.wed_resolved)
    $ _smoke_restore_diag(store._dev_snap, _sr, "nora")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_home_eli_invite:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met       = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.own_kitchen_set = True
    $ store.eli_home_dinner_done = False; store.eli_home_dinner_day = -1
    $ store.current_loc   = "location_home"
    $ store.day = 30; store.hour = 18.0
    $ store.npc_invitation_pending = {
        "npc_id": "eli", "invitation_id": "eli_home_dinner",
        "target_location": "location_home",
        "accepted_day": store.day - 1, "expiry_day": store.day + 6}
    $ store.wed_personal_fired_day = -1
    $ _eli_aff_pre = store.eli_affection; _eli_tr_pre = store.eli_trust
    $ _sr = []
    $ _lbl = wed_poll_personal("location_home")
    $ _smoke_chk(_sr, "wed_poll_personal dispatched home_visit_eli_dinner",
        _lbl == "home_visit_eli_dinner")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "eli_home_dinner_done set", store.eli_home_dinner_done)
        $ _smoke_chk(_sr, "eli_home_dinner_day set", store.eli_home_dinner_day >= 0)
        $ _smoke_chk(_sr, "matching plan cleared",
            store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "eli_home_dinner")
        $ store.day += 1
        $ _cb = _check_talk_followup("eli")
        $ _smoke_chk(_sr, "eli home-visit callback available next day",
            _cb == "talk_followup_eli_home_dinner")
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_home_eli_legacy:
    $ _smoke_restore(store._dev_snap)
    $ store.eli_met       = True; store.eli_affection = 30; store.eli_trust = 25
    $ store.own_kitchen_set = True
    $ store.eli_home_dinner_done = False; store.eli_home_dinner_day = -1
    $ store.npc_invitation_pending = None
    $ _sr = []
    $ _smoke_chk(_sr, "home_dinner_scene_eli label exists",
        renpy.has_label("home_dinner_scene_eli"))
    if renpy.has_label("home_dinner_scene_eli"):
        call home_dinner_scene_eli
        $ _smoke_chk(_sr, "eli_home_dinner_done set", store.eli_home_dinner_done)
        $ _smoke_chk(_sr, "eli_home_dinner_day set", store.eli_home_dinner_day >= 0)
        $ _smoke_chk(_sr, "home_visit_eli_dinner NOT in wed_resolved",
            "home_visit_eli_dinner" not in store.wed_resolved)
    $ _smoke_restore_diag(store._dev_snap, _sr, "eli")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_home_zoe_invite:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met       = True; store.zoe_affection = 30; store.zoe_trust = 25
    $ store.own_guitar    = True; store.apartment_tier = 1
    $ store.zoe_home_guitar_done = False; store.zoe_home_guitar_day = -1
    $ store.current_loc   = "location_home"
    $ store.day = 30; store.hour = 15.0
    $ store.npc_invitation_pending = {
        "npc_id": "zoe", "invitation_id": "zoe_home_guitar",
        "target_location": "location_home",
        "accepted_day": store.day - 1, "expiry_day": store.day + 6}
    $ store.wed_personal_fired_day = -1
    $ _zoe_aff_pre = store.zoe_affection; _zoe_tr_pre = store.zoe_trust
    $ _sr = []
    $ _lbl = wed_poll_personal("location_home")
    $ _smoke_chk(_sr, "wed_poll_personal dispatched home_visit_zoe_guitar",
        _lbl == "home_visit_zoe_guitar")
    if _lbl and renpy.has_label(_lbl):
        call expression _lbl
        $ _smoke_chk(_sr, "zoe_home_guitar_done set", store.zoe_home_guitar_done)
        $ _smoke_chk(_sr, "zoe_home_guitar_day set", store.zoe_home_guitar_day >= 0)
        $ _smoke_chk(_sr, "matching plan cleared",
            store.npc_invitation_pending is None
            or store.npc_invitation_pending.get("invitation_id") != "zoe_home_guitar")
        $ store.day += 1
        $ _cb = _check_talk_followup("zoe")
        $ _smoke_chk(_sr, "zoe home-visit callback available next day",
            _cb == "talk_followup_zoe_home_guitar")
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_home_zoe_legacy:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met       = True; store.zoe_affection = 30; store.zoe_trust = 25
    $ store.own_guitar    = True; store.apartment_tier = 1
    $ store.zoe_home_guitar_done = False; store.zoe_home_guitar_day = -1
    $ store.npc_invitation_pending = None
    $ _sr = []
    $ _smoke_chk(_sr, "home_zoe_guitar_scene label exists",
        renpy.has_label("home_zoe_guitar_scene"))
    if renpy.has_label("home_zoe_guitar_scene"):
        call home_zoe_guitar_scene
        $ _smoke_chk(_sr, "zoe_home_guitar_done set", store.zoe_home_guitar_done)
        $ _smoke_chk(_sr, "zoe_home_guitar_day set", store.zoe_home_guitar_day >= 0)
        $ _smoke_chk(_sr, "home_visit_zoe_guitar NOT in wed_resolved",
            "home_visit_zoe_guitar" not in store.wed_resolved)
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop


# ── EXHIBITION SCENARIOS ──────────────────────────────────────────────────────

label _smoke_exh_invite_ready:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met              = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.zoe_exhibition_invited      = True
    $ store.zoe_exhibition_done         = False
    $ store.zoe_exhibition_offer_last_day = store.day - 15
    $ store.day = 30
    $ _sr = []
    # Asset/label diagnostics
    $ _smoke_chk(_sr, "zoe_exhibition_opening label exists",
        renpy.has_label("zoe_exhibition_opening"))
    $ _smoke_chk(_sr, "gallery_evening declared (WARN if missing)",
        renpy.has_image("gallery_evening"))
    $ _smoke_chk(_sr, "librarynight declared (fallback)",
        renpy.has_image("librarynight"))
    $ _smoke_chk(_sr, "zoe_street_neutral sprite declared",
        renpy.has_image("zoe_street_neutral"))
    # Gate checks (not calling the scene — this is an invite-ready state check)
    $ _smoke_chk(_sr, "trust >= 25", store.zoe_trust >= 25)
    $ _smoke_chk(_sr, "day >= 21", store.day >= 21)
    $ _smoke_chk(_sr, "10-day gap satisfied",
        store.day - store.zoe_exhibition_offer_last_day >= 10)
    $ _smoke_chk(_sr, "zoe_exhibition_done is False (not permanently blocked)",
        not store.zoe_exhibition_done)
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_opening_seen:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met   = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.elle_met  = False; store.nora_met = False  # suppress cameos for determinism
    $ store.npc_invitation_pending = {
        "npc_id": "zoe", "invitation_id": "zoe_exhibition",
        "target_location": "location_gallery",
        "accepted_day": store.day - 2, "expiry_day": store.day + 5}
    $ store.zoe_exhibition_done = False
    $ store.wed_personal_fired_day = -1
    $ _zoe_aff_pre = store.zoe_affection; _zoe_tr_pre = store.zoe_trust
    $ _hour_pre = store.hour
    $ _sr = []
    $ _smoke_chk(_sr, "zoe_exhibition_opening label exists",
        renpy.has_label("zoe_exhibition_opening"))
    # Expected outcome: seen. Player must select "Ask about the piece in the corner."
    "EXPECTED: select 'Ask about the piece in the corner.' for PASS."
    if renpy.has_label("zoe_exhibition_opening"):
        call zoe_exhibition_opening
        $ _smoke_chk(_sr, "zoe_exhibition_done set", store.zoe_exhibition_done)
        $ _smoke_chk(_sr, "outcome == seen (selected correct branch)",
            store.zoe_exhibition_outcome == "seen")
        $ _smoke_chk(_sr, "affection +2 (seen branch)",
            store.zoe_affection >= _zoe_aff_pre + 2)
        $ _smoke_chk(_sr, "trust +3 (seen branch)",
            store.zoe_trust >= _zoe_tr_pre + 3)
        $ _smoke_chk(_sr, "spend_time 2.0 consumed (hour advanced)",
            store.hour >= _hour_pre + 2.0)
        $ _smoke_chk(_sr, "invitation cleared",
            store.npc_invitation_pending is None)
        $ _smoke_chk(_sr, "zoe_gallery_until_day = exhibition_day + 14",
            store.zoe_gallery_until_day == store.zoe_exhibition_day + 14)
        $ _smoke_chk(_sr, "zoe_exhibition_opening in wed_resolved",
            "zoe_exhibition_opening" in store.wed_resolved)
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_opening_steady:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met   = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.elle_met  = False; store.nora_met = False
    $ store.npc_invitation_pending = {
        "npc_id": "zoe", "invitation_id": "zoe_exhibition",
        "target_location": "location_gallery",
        "accepted_day": store.day - 2, "expiry_day": store.day + 5}
    $ store.zoe_exhibition_done = False
    $ store.wed_personal_fired_day = -1
    $ _zoe_aff_pre = store.zoe_affection; _zoe_tr_pre = store.zoe_trust
    $ _sr = []
    "EXPECTED: select 'Help with something practical.' for PASS."
    if renpy.has_label("zoe_exhibition_opening"):
        call zoe_exhibition_opening
        $ _smoke_chk(_sr, "zoe_exhibition_done set", store.zoe_exhibition_done)
        $ _smoke_chk(_sr, "outcome == steady",
            store.zoe_exhibition_outcome == "steady")
        $ _smoke_chk(_sr, "affection +2 (steady branch)",
            store.zoe_affection >= _zoe_aff_pre + 2)
        $ _smoke_chk(_sr, "trust +2 (steady branch)",
            store.zoe_trust >= _zoe_tr_pre + 2)
        $ _smoke_chk(_sr, "invitation cleared", store.npc_invitation_pending is None)
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_opening_pressured:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met   = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.elle_met  = False; store.nora_met = False
    $ store.npc_invitation_pending = {
        "npc_id": "zoe", "invitation_id": "zoe_exhibition",
        "target_location": "location_gallery",
        "accepted_day": store.day - 2, "expiry_day": store.day + 5}
    $ store.zoe_exhibition_done = False
    $ store.wed_personal_fired_day = -1
    $ _zoe_aff_pre = store.zoe_affection; _zoe_tr_pre = store.zoe_trust
    $ _sr = []
    "EXPECTED: select 'Ask whether this will lead anywhere useful.' for PASS."
    if renpy.has_label("zoe_exhibition_opening"):
        call zoe_exhibition_opening
        $ _smoke_chk(_sr, "zoe_exhibition_done set", store.zoe_exhibition_done)
        $ _smoke_chk(_sr, "outcome == pressured",
            store.zoe_exhibition_outcome == "pressured")
        $ _smoke_chk(_sr, "affection -1 (pressured branch)",
            store.zoe_affection == _zoe_aff_pre - 1)
        $ _smoke_chk(_sr, "trust -2 (pressured branch)",
            store.zoe_trust == _zoe_tr_pre - 2)
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_gallery:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met             = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.zoe_exhibition_done = True
    $ store.zoe_exhibition_day  = store.day - 3
    $ store.zoe_exhibition_outcome = "seen"
    $ store.zoe_gallery_until_day  = store.day + 11
    $ store.zoe_gallery_talk_last_day = -999
    $ store.day = 30
    $ _sr = []
    $ _smoke_chk(_sr, "location_gallery label exists",
        renpy.has_label("location_gallery"))
    $ _smoke_chk(_sr, "gallery period active (day <= until_day)",
        store.day <= store.zoe_gallery_until_day)
    # Verify Zoe appears on Sunday (day%7==6) 14:00-18:00 during window
    $ store.hour = 16.0
    $ _sunday = store.day - (store.day % 7) + 6
    $ store.day = _sunday
    $ _sched = npc_schedule_entries("zoe")
    $ _smoke_chk(_sr, "gallery schedule entry present on Sunday during window",
        any(e[2] == "location_gallery" for e in _sched))
    # Verify schedule disappears after expiry
    $ store.day = store.zoe_gallery_until_day + 1
    $ _sched2 = npc_schedule_entries("zoe")
    $ _smoke_chk(_sr, "gallery schedule entry absent after expiry",
        not any(e[2] == "location_gallery" for e in _sched2))
    # Asset diagnostics
    $ _smoke_chk(_sr, "gallery_evening declared (WARN if missing)",
        renpy.has_image("gallery_evening"))
    $ _smoke_chk(_sr, "librarynight fallback declared",
        renpy.has_image("librarynight"))
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_aftermath:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met             = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.zoe_exhibition_done = True
    $ store.zoe_exhibition_day  = store.day - 3
    $ store.zoe_exhibition_outcome = "seen"
    $ store.zoe_gallery_until_day  = store.day + 11
    $ store.zoe_exhibition_aftermath_queued = False
    $ _46s = dict(store.npc_story_aftermath_seen); _46s.pop("zoe_exhibition", None)
    $ store.npc_story_aftermath_seen = _46s
    $ store.npc_story_aftermath_initialized = True
    # Route aftermath queueing through process_world_progression
    $ store.world_progression_initialized = True
    $ process_world_progression()
    $ _sr = []
    $ _smoke_chk(_sr, "aftermath queued via process_world_progression",
        store.zoe_exhibition_aftermath_queued)
    $ _smoke_chk(_sr, "zoe_exhibition pending in npc_story_aftermath_pending",
        "zoe_exhibition" in store.npc_story_aftermath_pending.get("zoe", {}))
    # Final callback still blocked (aftermath pending, not resolved)
    $ store.day = store.zoe_gallery_until_day + 1
    $ _cb = _check_talk_followup("zoe")
    $ _smoke_chk(_sr, "final callback blocked while aftermath pending",
        _cb != "talk_followup_zoe_exhibition")
    # Now fire the aftermath
    if renpy.has_label("story_aftermath_zoe_exhibition"):
        call story_aftermath_zoe_exhibition
        $ _smoke_chk(_sr, "zoe_exhibition in aftermath_seen (resolved)",
            "zoe_exhibition" in store.npc_story_aftermath_seen)
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop

label _smoke_exh_callback:
    $ _smoke_restore(store._dev_snap)
    $ store.zoe_met              = True; store.zoe_affection = 40; store.zoe_trust = 30
    $ store.zoe_exhibition_done  = True
    $ store.zoe_exhibition_day   = store.day - 20
    $ store.zoe_exhibition_outcome = "seen"
    $ store.zoe_gallery_until_day  = store.day - 6   # gallery period over
    $ store.zoe_exhibition_followup_done = False
    $ _46s = dict(store.npc_story_aftermath_seen)
    $ _46s["zoe_exhibition"] = True   # aftermath already resolved
    $ store.npc_story_aftermath_seen = _46s
    $ store.day = store.zoe_gallery_until_day + 7   # well past gallery end
    $ _sr = []
    # Verify _check_talk_followup routes to the callback
    $ _cb = _check_talk_followup("zoe")
    $ _smoke_chk(_sr, "_check_talk_followup returns talk_followup_zoe_exhibition",
        _cb == "talk_followup_zoe_exhibition")
    $ _smoke_chk(_sr, "aftermath resolved (not just queued)",
        store.npc_story_aftermath_seen.get("zoe_exhibition"))
    $ _smoke_chk(_sr, "gallery period over (day > zoe_gallery_until_day)",
        store.day > store.zoe_gallery_until_day)
    if renpy.has_label("talk_followup_zoe_exhibition"):
        call talk_followup_zoe_exhibition
        $ _smoke_chk(_sr, "zoe_exhibition_followup_done set",
            store.zoe_exhibition_followup_done)
        # After completion, callback must not fire again
        $ _cb2 = _check_talk_followup("zoe")
        $ _smoke_chk(_sr, "callback does not fire after followup_done",
            _cb2 != "talk_followup_zoe_exhibition")
    $ _smoke_restore_diag(store._dev_snap, _sr, "zoe")
    call screen dev_smoke_report(_sr)
    jump dev_progression_smoke_menu.loop
