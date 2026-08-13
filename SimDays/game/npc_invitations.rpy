# Spontaneous NPC invitations — NPCs invite the player to activities.
# Generated probabilistically each day; accepted invitations add calendar events.
# Missing an accepted invitation costs relationship affection.

init python:

    NPC_INVITATION_TEMPLATES = [
        {"id": "marcus_static_01", "npc": "marcus", "activity": "bar_visit", "activity_type": "casual",
         "location": "location_bar", "scene_type": "bar_drink",
         "title": "Marcus — Static tonight?",
         "message": "Heading to Static later. You around?",
         "duration_hours": 2, "energy_cost": 10, "rel_gain": 5, "rel_stat": "affection",
         "min_rel": 25, "start_hour": 21, "end_hour": 23,
         "cooldown_days": 5, "advance_days": 1},
        {"id": "nora_coffee_01", "npc": "nora", "activity": "coffee", "activity_type": "casual",
         "location": "location_cafe", "scene_type": "coffee",
         "title": "Nora — Coffee tomorrow?",
         "message": "Free for coffee tomorrow morning?",
         "duration_hours": 1, "energy_cost": 5, "rel_gain": 4, "rel_stat": "affection",
         "min_rel": 20, "start_hour": 9, "end_hour": 12,
         "cooldown_days": 4, "advance_days": 1},
        {"id": "zoe_park_01", "npc": "zoe", "activity": "park_walk", "activity_type": "casual",
         "location": "location_park", "scene_type": "park_walk",
         "title": "Zoe — Park afternoon",
         "message": "Going to the park to sketch. Want to join?",
         "duration_hours": 2, "energy_cost": 8, "rel_gain": 5, "rel_stat": "affection",
         "min_rel": 20, "start_hour": 14, "end_hour": 17,
         "cooldown_days": 5, "advance_days": 1},
        {"id": "eli_campus_01", "npc": "eli", "activity": "campus_meetup", "activity_type": "professional",
         "location": "location_hub", "scene_type": "study_session",
         "title": "Eli — Tech talk at the Hub",
         "message": "Demoing something at the Hub. Swing by if you want.",
         "duration_hours": 2, "energy_cost": 8, "rel_gain": 4, "rel_stat": "trust",
         "min_rel": 25, "start_hour": 14, "end_hour": 17,
         "cooldown_days": 6, "advance_days": 1},
    ]

    def invitation_location_background(location_id):
        """Returns the resolved image name for the invitation scene, or None if unmapped."""
        h = int(store.hour)
        _MAP = {
            "location_bar":       "bar",
            "location_cafe":      cafe_bg(),
            "location_park":      "parknight" if h >= 20 else "parkday",
            "location_library":   "librarynight" if h >= 20 else "libraryday",
            "location_hub":       "hub_night" if (h >= 20 or h < 6) else "hub_day",
            "location_hospital":  "hospital_night" if (h >= 20 or h < 6) else "hospital1",
            "location_warehouse": "warehouse",
            "location_diner":     "diner_night",
            "location_nightclub": "nightclub",
            "location_sandbeach": "sandbeach_night" if h >= 19 else "sandbeach_day",
            "location_office":    "goodoffice1",
        }
        return _MAP.get(location_id)

    # ── Invitation schedule overrides ────────────────────────────────────────
    def create_invitation_schedule_override(inv):
        """Called when player accepts an invitation. Pins the NPC at the agreed venue."""
        add_schedule_override(
            npc_id       = inv["npc"],
            day          = inv["proposed_day"],
            hour_start   = inv["start_hour"],
            hour_end     = inv["end_hour"],
            location_id  = inv["location"],
            activity_id  = "meeting_player",
            public       = True,
            interactable = True,
            source_id    = "invitation_" + inv["id"],
            expires_day  = inv["proposed_day"] + 1,
        )

    def remove_invitation_schedule_override(inv_id):
        """Remove the override created by create_invitation_schedule_override."""
        source_id = "invitation_" + inv_id
        store.npc_schedule_overrides = [
            o for o in store.npc_schedule_overrides
            if o.get("source_id") != source_id
        ]

    def can_generate_invitation_for_npc(npc_id, proposed_day=None,
                                        start_hour=None, end_hour=None):
        """Timing args are optional so old call sites keep working; when supplied,
        an NPC already committed elsewhere in that window is never offered (the
        override would be shadowed by resolve_npc_state's first-match-wins)."""
        if len(store.active_npc_invitations) >= 1: return False
        week = store.day // 7
        week_count = store.npc_invitation_week_counts.get(week, 0)
        if week_count >= 2: return False
        last = max((h["day"] for h in store.npc_invitation_history if h["npc"] == npc_id), default=-99)
        if store.day - last < 4: return False
        if proposed_day is not None and start_hour is not None and end_hour is not None:
            if npc_has_override_overlap(npc_id, proposed_day, start_hour, end_hour):
                return False
        return True

    def generate_npc_invitations():
        """Called from new_day() — ~35% chance of one new invitation per day."""
        import random as _r
        _rng = _r.Random(store.day * 31 + len(store.npc_invitation_history))
        if _rng.random() > 0.35: return
        already_active = [i["template_id"] for i in store.active_npc_invitations]
        eligible = [t for t in NPC_INVITATION_TEMPLATES
                    if can_generate_invitation_for_npc(
                        t["npc"], store.day + t["advance_days"],
                        t["start_hour"], t["end_hour"])
                    and getattr(store, t["npc"] + "_met", False)
                    and getattr(store, NPC_DATA[t["npc"]]["aff"], 0) >= t["min_rel"]
                    and t["id"] not in already_active]
        if not eligible: return
        tmpl = _rng.choice(eligible)
        # Phase 66: whether the NPC actually bothers to reach out now depends on
        # the right relationship axes for the activity, not on affection alone.
        # min_rel above is still the hard floor; this is the soft roll on top.
        if _rng.random() > invitation_acceptance_chance(
                tmpl["npc"], tmpl.get("activity_type", "casual")):
            return
        proposed_day = store.day + tmpl["advance_days"]
        inv = {
            "id": "inv_%s_day%d" % (tmpl["id"], store.day),
            "template_id": tmpl["id"], "npc": tmpl["npc"],
            "activity": tmpl["activity"], "location": tmpl["location"],
            "proposed_day": proposed_day, "start_hour": tmpl["start_hour"],
            "end_hour": tmpl["end_hour"], "status": "pending",
            "calendar_event_id": None, "consequence_processed": False,
            "rel_gain": tmpl.get("rel_gain", 3),
            "rel_stat": tmpl.get("rel_stat", "affection"),
        }
        store.active_npc_invitations = list(store.active_npc_invitations) + [inv]
        queue_phone_message(tmpl["npc"], tmpl["message"], store.day,
                            "inv_" + inv["id"])
        week = store.day // 7
        d = dict(store.npc_invitation_week_counts)
        d[week] = d.get(week, 0) + 1
        store.npc_invitation_week_counts = d

    def accept_npc_invitation(inv_id):
        invs = list(store.active_npc_invitations)
        for i, inv in enumerate(invs):
            if inv["id"] == inv_id:
                # Only a pending invitation can be accepted. Guards double-clicks
                # in the phone UI and any already-resolved entry still in the list.
                if inv.get("status") != "pending":
                    return False
                # The slot can be taken between generation and acceptance (e.g. the
                # Summer Festival pins the NPC downtown 17-23). Checked BEFORE the
                # override is inserted, so it can never conflict with itself.
                if npc_has_override_overlap(inv["npc"], inv["proposed_day"],
                                            inv["start_hour"], inv["end_hour"]):
                    store.active_npc_invitations = [x for x in invs if x["id"] != inv_id]
                    store.npc_invitation_history = list(store.npc_invitation_history) + [
                        {"id": inv_id, "npc": inv["npc"], "day": store.day,
                         "status": "cancelled"}]
                    queue_phone_message(
                        inv["npc"],
                        "Sorry — something else came up that day. Rain check?",
                        store.day, "inv_cancel_" + inv_id)
                    return False   # no commitment, no override, no rel penalty
                inv = dict(inv)
                inv["status"] = "accepted"
                tmpl = next((t for t in NPC_INVITATION_TEMPLATES if t["id"] == inv["template_id"]), {})
                cal_id = add_calendar_event(
                    title="%s — %s" % (NPC_DATA[inv["npc"]]["name"], inv["activity"]),
                    day=inv["proposed_day"], hour=inv["start_hour"],
                    duration=inv["end_hour"] - inv["start_hour"],
                    category="social", commitment=True, npc_id=inv["npc"],
                    invitation_id=inv_id)
                inv["calendar_event_id"] = cal_id
                invs[i] = inv
                store.active_npc_invitations = invs
                store.npc_invitation_history = list(store.npc_invitation_history) + [
                    {"id": inv_id, "npc": inv["npc"], "day": store.day, "status": "accepted"}]
                create_invitation_schedule_override(inv)
                return True
        return False

    def decline_npc_invitation(inv_id):
        invs = list(store.active_npc_invitations)
        for i, inv in enumerate(invs):
            if inv["id"] == inv_id:
                if inv.get("status") != "pending":
                    return False   # no second history row, no second penalty
                inv = dict(inv)
                inv["status"] = "declined"
                invs[i] = inv
                store.active_npc_invitations = [x for x in invs if x["id"] != inv_id]
                store.npc_invitation_history = list(store.npc_invitation_history) + [
                    {"id": inv_id, "npc": inv["npc"], "day": store.day, "status": "declined"}]
                return True
        return False

    def hours_until_invitation(inv):
        """Hours until the invitation starts. Negative once it is in the past.
        Same shape as hours_until_commitment() so both stores read alike."""
        return (inv["proposed_day"] - store.day) * 24 + (inv["start_hour"] - store.hour)

    def cancel_accepted_invitation(inv_id):
        """Player-side cancellation of an accepted Phase 68 invitation.

        Returns True if it cancelled, False if already terminal or too late.

        ARCHITECTURAL NOTE: there are two commitment stores and they stay
        separate on purpose. player_commitments (authored scenes) is cancelled
        by cancel_commitment() in phone_messages.rpy; invitations live in
        active_npc_invitations + calendar_events and are cancelled here.
        Accepting an invitation writes NO player_commitments row, so neither
        function can reach the other's data. Do not merge them.
        """
        inv = next((i for i in store.active_npc_invitations if i["id"] == inv_id), None)
        if inv is None:
            return False
        if inv.get("status") != "accepted":
            return False                      # idempotent: already terminal
        hours_until = hours_until_invitation(inv)
        if inv["proposed_day"] < store.day:
            return False                      # past day
        if inv["proposed_day"] == store.day and inv["start_hour"] <= store.hour:
            return False                      # already started
        # Same threshold as the player_commitments Cancel button: < 4h is late.
        late = hours_until < 4

        remove_invitation_schedule_override(inv_id)
        if inv.get("calendar_event_id"):
            cancel_calendar_commitment(inv["calendar_event_id"])

        # Terminal status first — everything below is guarded by it.
        invs = list(store.active_npc_invitations)
        for i, x in enumerate(invs):
            if x["id"] == inv_id:
                x = dict(x)
                x["status"] = "cancelled"
                x["consequence_processed"] = True
                invs[i] = x
                inv = x
                break
        store.active_npc_invitations = invs
        store.npc_invitation_history = list(store.npc_invitation_history) + [
            {"id": inv_id, "npc": inv["npc"], "day": store.day,
             "status": "player_cancelled"}]

        if late:
            # Smaller than the no-show penalty (affection -4 / trust -3 /
            # respect -2) — telling them beats not showing up.
            apply_relationship_change(inv["npc"], "inv_cancel_late_" + inv_id,
                                      "kept_commitment", trust=-2,
                                      bypass_saturation=True)
        # queue_phone_message is already tag-deduplicated.
        queue_phone_message(
            inv["npc"],
            "Okay. Wish you'd said something a little sooner."
            if late else "Sure, no worries. Another time.",
            store.day, "inv_player_cancel_" + inv_id)
        return True

    def _cancel_accepted_invitation_wrapper(inv_id):
        """Phone-UI entry point. Returns None so Ren'Py keeps the screen up."""
        if cancel_accepted_invitation(inv_id):
            renpy.notify("Cancelled.")
            deliver_due_messages()   # surface the reply immediately

    def complete_npc_invitation(inv_id):
        """Call when the player actually attends the invitation event. Cleans up the override."""
        inv_obj = next((i for i in store.active_npc_invitations if i["id"] == inv_id), None)
        if not inv_obj or inv_obj.get("status") in ("completed", "left_early", "cancelled", "missed"):
            return False  # already processed
        remove_invitation_schedule_override(inv_id)
        invs = list(store.active_npc_invitations)
        for i, inv in enumerate(invs):
            if inv["id"] == inv_id and inv["status"] == "accepted":
                inv = dict(inv)
                inv["status"] = "completed"
                inv["consequence_processed"] = True
                invs[i] = inv
                store.active_npc_invitations = invs
                _apply_inv_completion_effects(inv["npc"], inv_id, inv_obj=inv_obj)
                return True
        return False

    def leave_npc_invitation_early(inv_id):
        """Call when player chooses to leave before completing."""
        invs = list(store.active_npc_invitations)
        for i, inv in enumerate(invs):
            if inv["id"] == inv_id and inv["status"] == "accepted":
                inv = dict(inv)
                inv["status"] = "left_early"
                inv["consequence_processed"] = True
                invs[i] = inv
                break
        store.active_npc_invitations = invs
        remove_invitation_schedule_override(inv_id)

    def _apply_inv_completion_effects(npc_id, inv_id, inv_obj=None):
        """Apply rel gain and memory once per invitation. Idempotent via _inv_effects_applied."""
        if inv_id in store._inv_effects_applied: return
        store._inv_effects_applied = list(store._inv_effects_applied) + [inv_id]
        rel_gain = 3
        rel_stat = "affection"
        if inv_obj:
            rel_gain = inv_obj.get("rel_gain", 3)
            rel_stat = inv_obj.get("rel_stat", "affection")
        # Phase 66: a kept commitment is the strongest trust/respect source in
        # the game. Goes through the central API so caps + saturation apply.
        apply_relationship_change(
            npc_id, "invitation_" + inv_id, "kept_commitment",
            affection = rel_gain if rel_stat == "affection" else 1,
            trust     = rel_gain if rel_stat == "trust"     else 2,
            respect   = 2, familiarity = 3, meaningful = True)
        add_relationship_memory(npc_id, "inv_" + inv_id + "_completed",
                                "Met up as arranged.", category="event", visibility="private")
        record_game_event(
            "inv_complete_" + inv_id, "social",
            "Met with " + NPC_DATA.get(npc_id, {}).get("name", npc_id.title()),
            summary=False, journal=False,
            metadata={"npc": npc_id},
        )

    def process_missed_invitations():
        """Called from new_day(). Penalise missed accepted invitations."""
        invs = list(store.active_npc_invitations)
        for i, inv in enumerate(invs):
            if (inv["status"] == "accepted" and
                    store.day > inv["proposed_day"] and
                    not inv.get("consequence_processed")):
                inv = dict(inv)
                inv["status"] = "missed"
                inv["consequence_processed"] = True
                npc_id = inv["npc"]
                apply_relationship_change(npc_id, "missed_" + inv["id"], "kept_commitment",
                                          affection=-4, trust=-3, respect=-2,
                                          bypass_saturation=True)
                remove_invitation_schedule_override(inv["id"])
                invs[i] = inv
                queue_phone_message(npc_id,
                    "Hey, you didn't show. Everything ok?",
                    store.day, "missed_inv_" + inv["id"])
            elif (inv["status"] == "pending" and store.day > inv["proposed_day"]):
                # An ignored invitation has to expire or it blocks every future
                # one forever (can_generate_invitation_for_npc caps the list at 1).
                # No relationship penalty — the player never agreed to anything.
                inv = dict(inv)
                inv["status"] = "expired"
                invs[i] = inv
        store.active_npc_invitations = [x for x in invs
                                        if x["status"] not in ("declined", "missed", "expired",
                                                                "completed", "left_early",
                                                                "cancelled")]

    def _accept_npc_invitation_wrapper(inv_id):
        """Phone-UI entry point. Returns None so Ren'Py keeps the screen up.
        All the logic (conflict check, calendar event, override, history, rain
        check message) lives in accept_npc_invitation — this only reports."""
        inv = next((i for i in store.active_npc_invitations if i["id"] == inv_id), None)
        name = NPC_DATA.get(inv["npc"], {}).get("name", "They") if inv else "They"
        if accept_npc_invitation(inv_id):
            renpy.notify("Added to your calendar.")
        else:
            renpy.notify(name + " had something come up — plan cancelled.")
        deliver_due_messages()   # surface the rain-check text immediately

    def _decline_npc_invitation_wrapper(inv_id):
        """Phone-UI entry point. Returns None."""
        if decline_npc_invitation(inv_id):
            renpy.notify("Declined.")

    # ── Invitation card display helpers ──────────────────────────────────────
    _INV_STATUS_TEXT = {
        "accepted":   "Accepted",
        "completed":  "Went",
        "left_early": "Left early",
        "missed":     "Missed",
        "expired":    "Expired",
        "cancelled":  "Cancelled",
        "declined":   "Declined",
    }

    def invitation_card_lines(inv):
        """(title, when, where, status_text) for one active_npc_invitations entry."""
        npc    = NPC_DATA.get(inv["npc"], {})
        tmpl   = next((t for t in NPC_INVITATION_TEMPLATES
                       if t["id"] == inv.get("template_id")), {})
        d      = inv["proposed_day"]
        when   = ("Today" if d == store.day else
                  "Tomorrow" if d == store.day + 1 else
                  "Day %d (%s)" % (d + 1, DAY_NAMES[d % 7]))
        where  = LOCATION_NAMES.get(inv["location"],
                     inv["location"].replace("location_", "").replace("_", " ").title())
        return (
            tmpl.get("title", "%s — %s" % (npc.get("name", inv["npc"].title()),
                                           inv["activity"].replace("_", " "))),
            "%s  ·  %02d:00–%02d:00  ·  %s" % (when, inv["start_hour"], inv["end_hour"], where),
            tmpl.get("message", ""),
            _INV_STATUS_TEXT.get(inv.get("status"), inv.get("status", "")),
        )

    def invitation_for_message(msg):
        """The active_npc_invitations entry a phone message announced, or None.
        queue_phone_message tags it 'inv_' + inv['id'], and ids start with 'inv_'."""
        tag = msg.get("tag", "")
        if not tag.startswith("inv_inv_"):
            return None
        return next((i for i in store.active_npc_invitations if i["id"] == tag[4:]), None)


# ── Invitation cards — used inside the phone Messages app ────────────────────
screen npc_invitation_cards():
    for _iv in active_npc_invitations:
        $ _iv_c = invitation_card_lines(_iv)   # (title, when, message, status)
        frame:
            xfill True
            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
            padding (12, 10, 12, 10)
            vbox:
                spacing 4
                xfill True
                text "Invitation" font PROFILE_FONT size 11 color "#5bcafa"
                hbox:
                    spacing 10
                    yalign 0.5
                    add _chat_circle(_npc_chat_portrait(_iv["npc"])) yalign 0.0
                    vbox:
                        xfill True
                        spacing 2
                        text _iv_c[0] font PROFILE_FONT size 14 color "#cfe0f5"
                        if _iv_c[2]:
                            text _iv_c[2] font ACT_FONT size 12 color "#9fb6d6"
                        text _iv_c[1] font ACT_FONT size 11 color "#7a9ab8"
                if _iv.get("status") == "pending":
                    hbox:
                        spacing 8
                        xalign 1.0
                        button:
                            xysize (86, 30)
                            background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                            action Function(_accept_npc_invitation_wrapper, _iv["id"])
                            text "Accept" font ACT_FONT size 12 color "#7fd06a" hover_color "#ffffff" align (0.5, 0.5)
                        button:
                            xysize (86, 30)
                            background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                            action Function(_decline_npc_invitation_wrapper, _iv["id"])
                            text "Decline" font ACT_FONT size 12 color "#c06060" hover_color "#ff8080" align (0.5, 0.5)
                elif _iv.get("status") == "accepted":
                    # Eligibility mirrors cancel_accepted_invitation's guard;
                    # the function is still the only place it is enforced.
                    hbox:
                        spacing 8
                        xalign 1.0
                        yalign 0.5
                        text _iv_c[3] font ACT_FONT size 12 color "#4a8a6a" yalign 0.5
                        if _iv["proposed_day"] > day or (_iv["proposed_day"] == day and _iv["start_hour"] > hour):
                            button:
                                xysize (86, 30)
                                background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                                hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                                action Function(_cancel_accepted_invitation_wrapper, _iv["id"])
                                text "Cancel" font ACT_FONT size 12 color "#c06060" hover_color "#ff8080" align (0.5, 0.5)
                        else:
                            text "Already started" font ACT_FONT size 11 color "#4a6080" yalign 0.5
                else:
                    text _iv_c[3] font ACT_FONT size 12 color "#4a8a6a" xalign 1.0

    # ── Generic invitation scene content ─────────────────────────────────────
    INV_SCENE_LINES = {
        "bar_drink": {
            "marcus": ["Marcus has a corner table saved. He slides you a glass without asking.",
                       "The bar is loud but it's easier to talk here than it looks."],
            "default": ["You find a table and order something. It's good to be out."],
        },
        "coffee": {
            "nora": ["Nora is already there, hands around a mug, looking like she needed this.",
                     "You talk for a while. It's the kind of conversation that doesn't have to go anywhere."],
            "default": ["You sit down and talk over coffee. Time passes easily."],
        },
        "study_session": {
            "eli": ["Eli has notes spread across the table. She pushes some aside to make room.",
                    "You work in parallel for a while. Occasionally one of you says something."],
            "default": ["You find a table and get some work done together."],
        },
        "park_walk": {
            "zoe": ["Zoe sets the pace — not fast, not slow. She points out things you walk past every day.",
                    "You talk, or don't. Either way it's fine."],
            "default": ["You walk for a while. The city looks different on foot."],
        },
        "public_outing": {
            "default": ["You meet up and spend some time out. It's a good break from the usual."],
        },
    }

    def invitation_arrival_text(inv):
        npc = inv.get("npc", "")
        templates = {
            "marcus": "Marcus is already here. He spots you as soon as you walk in.",
            "nora":   "Nora waves from across the room.",
            "zoe":    "Zoe is outside, looking at something on her phone. She looks up.",
            "eli":    "Eli is at a corner table, laptop open. She closes it when she sees you.",
        }
        return templates.get(npc, NPC_DATA.get(npc, {}).get("name", npc.title()) + " is here, as arranged.")


# ── Generic invitation scene runner ──────────────────────────────────────────
label run_npc_invitation(inv_id):
    $ _inv = next((i for i in store.active_npc_invitations if i["id"] == inv_id), None)
    if _inv is None:
        return
    $ _inv_tmpl  = next((t for t in NPC_INVITATION_TEMPLATES if t["id"] == _inv.get("template_id")), {})
    $ _inv_npc   = _inv["npc"]
    $ _inv_loc   = _inv["location"]
    $ _inv_stype = _inv_tmpl.get("scene_type", "bar_drink")
    $ _inv_dur   = _inv_tmpl.get("duration_hours", int(float(_inv.get("end_hour", 0)) - float(_inv.get("start_hour", 0))))
    $ _bg = invitation_location_background(_inv_loc)
    if _bg is None:
        $ renpy.log("Missing invitation background for: " + str(_inv_loc))
        $ renpy.notify("Location not available.")
        return
    scene expression _bg with dissolve
    show screen hud
    $ _inv_arr = invitation_arrival_text(_inv)
    "[_inv_arr]"
    $ _inv_spr = npc_sprite(_inv_npc, "casual")
    show expression _inv_spr as npc_meeting at right with dissolve
    menu:
        "Spend time together ([_inv_dur]h)":
            call run_inv_scene_by_type(_inv_stype, _inv_npc, _inv_dur)
            $ complete_npc_invitation(inv_id)
        "Leave early":
            $ leave_npc_invitation_early(inv_id)
    hide npc_meeting with dissolve
    return


label run_inv_scene_by_type(scene_type, npc_id, duration):
    $ _inv_lines = INV_SCENE_LINES.get(scene_type, {}).get(npc_id, INV_SCENE_LINES.get(scene_type, {}).get("default", ["You spend some time together."]))
    $ _inv_line_count = len(_inv_lines)
    $ _inv_line_i = 0
    while _inv_line_i < _inv_line_count:
        $ _inv_cur_line = _inv_lines[_inv_line_i]
        $ _inv_line_i += 1
        "[_inv_cur_line]"
    $ spend_time(duration)
    return
