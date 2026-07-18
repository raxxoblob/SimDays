# phone_messages.rpy — NPC inbox: delayed delivery, actionable responses, commitments.
# v2: responses[], player_commitments, conflict checking, missed-meeting follow-ups.

init python:
    _NPC_DISPLAY = {
        "caroline": "Caroline",
        "martha":   "Martha",
        "eli":      "Eli",
        "lena":     "Dr. Lena",
        "nora":     "Nora",
        "natalie":  "Natalie",
        "kai":      "Kai",
        "rena":     "Chef Rena",
        "sam":      "Sam",
        "zoe":      "Zoe",
        "marcus":   "Marcus",
    }

    _MISSED_TEXTS = {
        "martha":  "I assume something came up.",
        "nora":    "You owe me one unnecessary coffee.",
        "lena":    "You should not accept professional commitments you cannot keep.",
        "eli":     "No problem. Sent you the notes anyway.",
        "natalie": "Shift got covered. Let me know next time.",
    }

    # ── Message helpers ────────────────────────────────────────────────────

    def queue_phone_message(npc_id, text, send_on_day, tag, responses=None):
        if any(m["tag"] == tag for m in store.npc_messages):
            return
        store.npc_messages.append({
            "npc_id":       npc_id,
            "npc_name":     _NPC_DISPLAY.get(npc_id, npc_id.capitalize()),
            "text":         text,
            "send_on_day":  send_on_day,
            "delivered":    False,
            "delivered_on": -1,
            "read":         False,
            "replied":      False,
            "replied_with": None,
            "responses":    list(responses) if responses else [],
            "tag":          tag,
        })

    def deliver_due_messages():
        for m in store.npc_messages:
            if not m.get("delivered") and store.day >= m.get("send_on_day", 0):
                m["delivered"] = True
                m["delivered_on"] = store.day

    def deliver_message_now(tag):
        for m in store.npc_messages:
            if m.get("tag") == tag and not m.get("delivered"):
                m["delivered"] = True
                m["delivered_on"] = store.day
                break

    def unread_message_count():
        return sum(1 for m in store.npc_messages if m["delivered"] and not m["read"])

    def mark_all_messages_read():
        for m in store.npc_messages:
            if m["delivered"]:
                m["read"] = True

    def mark_message_replied(msg, resp_id):
        msg["replied"]      = True
        msg["replied_with"] = resp_id
        msg["read"]         = True

    def message_already_queued(tag):
        return any(m["tag"] == tag for m in store.npc_messages)

    def delivered_messages():
        msgs = [m for m in store.npc_messages if m.get("delivered")]
        return sorted(msgs, key=lambda m: -m.get("delivered_on", m.get("send_on_day", 0)))

    # ── Commitment helpers ─────────────────────────────────────────────────

    def add_commitment(cid, npc_id, title, com_day, hour, location, label, grace=2.0):
        if any(c["id"] == cid for c in store.player_commitments):
            return
        store.player_commitments.append({
            "id":        cid,
            "npc_id":    npc_id,
            "title":     title,
            "day":       com_day,
            "hour":      hour,
            "location":  location,
            "label":     label,
            "grace":     grace,
            "completed": False,
            "missed":    False,
            "cancelled": False,
            "notified":  False,
        })

    def _c_active(c):
        """True when commitment is not in any terminal state."""
        return not c["completed"] and not c["missed"] and not c.get("cancelled", False)

    def upcoming_commitments():
        return sorted(
            [c for c in store.player_commitments
             if c["day"] >= store.day and _c_active(c)],
            key=lambda c: (c["day"], c["hour"])
        )

    def complete_commitment(cid):
        for c in store.player_commitments:
            if c["id"] == cid:
                c["completed"] = True
                break

    def has_conflict(target_day, target_hour, duration=2):
        for c in store.player_commitments:
            if c["day"] == target_day and _c_active(c):
                if abs(c["hour"] - target_hour) < duration:
                    return c
        return None

    def next_weekday(target_wd):
        """Return day number of the next occurrence of target_wd (0=Mon…6=Sun). Never today."""
        offset = (target_wd - store.day % 7) % 7
        if offset == 0:
            offset = 7
        return store.day + offset

    def commitment_available(cid, grace=None):
        """True if commitment cid is today, time is within [hour, hour+grace).
        Uses stored grace if param omitted."""
        for c in store.player_commitments:
            if c["id"] == cid and _c_active(c):
                _g = c.get("grace", 2.0) if grace is None else grace
                return (c["day"] == store.day
                        and c["hour"] <= store.hour < c["hour"] + _g)
        return False

    def mark_commitment_missed(c):
        """Single source of truth for marking a commitment missed + queuing NPC text."""
        if not _c_active(c):
            return
        c["missed"] = True
        _text = _MISSED_TEXTS.get(c["npc_id"], "")
        if _text:
            queue_phone_message(c["npc_id"], _text, store.day,
                                "missed_%s" % c["id"])
        # Scene trigger: marcus missed commitment — store structured context
        if (c.get("npc_id") == "marcus"
                and store.marcus_affection >= 30
                and store.marcus_missed_pending is None):
            _variant = "repeat_miss" if store.marcus_missed_done else "first_miss"
            store.marcus_missed_pending = {
                "trigger_day":    store.day,
                "commitment_id":  c["id"],
                "title":          c["title"],
                "location":       c.get("location", ""),
                "hour":           c["hour"],
                "variant":        _variant,
            }
            store.marcus_missed_done = False  # allow scene to fire again

    def expire_late_commitments():
        """Mark same-day commitments missed when the grace window has closed."""
        for c in store.player_commitments:
            if (c["day"] == store.day and _c_active(c)
                    and store.hour >= c["hour"] + c.get("grace", 2.0)):
                mark_commitment_missed(c)

    def notify_available_commitments():
        """renpy.notify() once per commitment when its window first opens."""
        for c in store.player_commitments:
            if (c["day"] == store.day and _c_active(c)
                    and not c.get("notified", False)
                    and c["hour"] <= store.hour < c["hour"] + c.get("grace", 2.0)):
                c["notified"] = True
                renpy.notify(c["title"] + " — head to " + c["location"])

    # (early_penalty, late_penalty) — late = < 4h before start
    _CANCEL_TRUST_PENALTY = {
        "martha":  (-1, -2),
        "nora":    (-1, -2),
        "eli":     (-1, -2),
        "lena":    (-2, -4),   # professional
        "natalie": (-2, -4),   # professional
    }
    _CANCEL_REPLY_TEXTS = {
        "martha":  "Understood.",
        "nora":    "Okay. Another time.",
        "eli":     "No problem.",
        "lena":    "I see. Please don't do this again.",
        "natalie": "I'll note that.",
    }

    def cancel_commitment(cid, late=False):
        """Cancel a commitment. late=True means < 4h before start — higher penalty.
        Sets cancelled=True (not missed=True) so no-shows are distinguishable."""
        for c in store.player_commitments:
            if c["id"] == cid and _c_active(c):
                c["cancelled"] = True
                _npc    = c["npc_id"]
                _early, _late = _CANCEL_TRUST_PENALTY.get(_npc, (-1, -2))
                _apply_trust(_npc, _late if late else _early)
                _text = _CANCEL_REPLY_TEXTS.get(_npc, "Got it.")
                queue_phone_message(_npc, _text, store.day,
                                    "cancel_%s" % cid)
                break

    def check_missed_commitments():
        """Called at new_day(): anything from yesterday still active is a no-show."""
        for c in store.player_commitments:
            if c["day"] < store.day and _c_active(c):
                mark_commitment_missed(c)

    # ── Agenda / planner helpers ───────────────────────────────────────────

    def today_commitments():
        return [c for c in store.player_commitments
                if c["day"] == store.day and _c_active(c)]

    def tomorrow_commitments():
        return [c for c in store.player_commitments
                if c["day"] == store.day + 1 and _c_active(c)]

    def next_commitment():
        """Soonest active commitment that hasn't started yet (today or later)."""
        candidates = [c for c in store.player_commitments
                      if _c_active(c) and (c["day"] > store.day
                         or (c["day"] == store.day and c["hour"] > store.hour))]
        if not candidates:
            return None
        return min(candidates, key=lambda c: (c["day"], c["hour"]))

    def hours_until_commitment(c):
        return (c["day"] - store.day) * 24 + (c["hour"] - store.hour)

    def commitment_status_text(c):
        if c.get("completed"):   return "Completed"
        if c.get("missed"):      return "Missed"
        if c.get("cancelled"):   return "Cancelled"
        if commitment_available(c["id"]): return "Available now"
        hrs = hours_until_commitment(c)
        if hrs <= 0:             return "Missed"
        if hrs < 0.5:            return "In 30 min"
        if hrs < 24:             return "In %dh" % int(hrs)
        if c["day"] == store.day + 1: return "Tomorrow"
        return "Day %d" % (c["day"] + 1)

    def activity_would_overlap_commitment(duration_hours):
        """Returns first commitment that falls inside [now, now+duration_hours)."""
        end_hour = store.hour + duration_hours
        for c in store.player_commitments:
            if not _c_active(c):
                continue
            if c["day"] != store.day:
                continue
            if store.hour <= c["hour"] < end_hour:
                return c
        return None


# Shared upcoming-commitments panel.
# compact=True → no cancel button, smaller meta line (for the HUD phone sidebar).
# compact=False → full cancel button with Return(None) (for phone_inbox_modal).
screen commitments_list(compact=False):
    $ _uc = upcoming_commitments()
    if _uc:
        frame:
            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
            padding (14, 10)
            xfill True
            vbox:
                spacing 6
                text "Upcoming" font ACT_FONT size (16 if not compact else 14) color "#9fb6d6"
                for _cm in _uc:
                    $ _ca         = commitment_available(_cm["id"])
                    $ _hrs_left   = (_cm["day"] - store.day) * 24 + (_cm["hour"] - store.hour)
                    $ _is_today   = _cm["day"] == store.day
                    $ _is_tmrw    = _cm["day"] == store.day + 1
                    $ _late_cncl  = _hrs_left < 4
                    $ _day_str    = "Today" if _is_today else ("Tomorrow" if _is_tmrw else ("Day " + str(_cm["day"] + 1)))
                    hbox:
                        xfill True
                        spacing 8
                        text "▸" font ACT_FONT size (14 if not compact else 12) color ("#5bcafa" if _ca else "#4a6080") yalign 0.5
                        vbox:
                            xexpand True
                            spacing 2
                            text _cm["title"] font ACT_FONT size (16 if not compact else 13) color "#cfe0f5"
                            text (_day_str + "  ·  " + "%02d:00" % _cm["hour"] + "  ·  " + _cm["location"]) font ACT_FONT size (13 if not compact else 11) color "#4a6080"
                            if _ca:
                                text "Available now" font ACT_FONT size (12 if not compact else 11) color "#5bcafa"
                            elif _is_today and _hrs_left > 0:
                                text ("In %.0fh" % _hrs_left) font ACT_FONT size (12 if not compact else 11) color "#9fb6d6"
                        if not compact:
                            textbutton "Cancel":
                                action [Function(cancel_commitment, _cm["id"], _late_cncl), Return(None)]
                                text_font ACT_FONT
                                text_size 13
                                text_color "#c06060"
                                text_hover_color "#ff8080"
                                yalign 0.5


# Standalone callable inbox — home "Check phone" uses this.
# Returns None (Close) or a label name string (response clicked).
screen phone_inbox_modal():
    modal True
    on "show" action [Function(deliver_due_messages), Function(mark_all_messages_read)]
    add "#000000b0"

    frame:
        xalign 0.5
        yalign 0.43
        xsize 740
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (28, 22)

        vbox:
            spacing 14

            # Header
            hbox:
                xfill True
                text "Inbox" font ACT_FONT size 28 color "#cfe0f5" yalign 0.5
                if unread_message_count() > 0:
                    $ _ub = unread_message_count()
                    text ("  · " + ("9+" if _ub > 9 else str(_ub)) + " new") font ACT_FONT size 16 color "#5bcafa" yalign 1.0
                textbutton "Close":
                    action [Function(mark_all_messages_read), Return(None)]
                    text_font ACT_FONT
                    text_size 18
                    text_color "#7a9ab8"
                    text_hover_color "#ffffff"
                    xalign 1.0 yalign 0.5

            # Upcoming commitments
            use commitments_list(compact=False)

            # Messages
            $ _dm = delivered_messages()
            if not _dm:
                text "No messages yet." font ACT_FONT size 18 color "#3a5068" xalign 0.5

            else:
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ysize 500
                    xsize 684

                    vbox:
                        spacing 8
                        for _m in _dm:
                            $ _has_resp    = bool(_m.get("responses"))
                            $ _is_replied  = _m.get("replied", False)
                            $ _disp_day    = _m.get("delivered_on", _m["send_on_day"])
                            frame:
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (14, 10)
                                xfill True

                                vbox:
                                    spacing 6
                                    # Sender + day
                                    hbox:
                                        xfill True
                                        text _m["npc_name"] font ACT_FONT size 18 color ("#5bcafa" if not _m["read"] else "#3a5068")
                                        text ("Day " + str(_disp_day + 1)) font ACT_FONT size 14 color "#2a3040" yalign 1.0
                                    # Body
                                    text _m["text"] font ACT_FONT size 16 color ("#cfe0f5" if not _m["read"] else "#5a7090")
                                    # Responses
                                    if _has_resp and not _is_replied:
                                        hbox:
                                            spacing 8
                                            for _resp in _m["responses"]:
                                                textbutton _resp["text"]:
                                                    action [Function(mark_message_replied, _m, _resp["id"]), Return(_resp["label"])]
                                                    text_font ACT_FONT
                                                    text_size 15
                                                    text_color "#cfe0f5"
                                                    text_hover_color "#ffffff"
                                                    background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                                                    hover_background Frame("images/ui/act_bar_hover.png", 20, 20, 20, 20)
                                                    padding (12, 6)
                                    elif _is_replied and _m.get("replied_with"):
                                        $ _rtext = next((r["text"] for r in _m.get("responses", []) if r["id"] == _m.get("replied_with")), "")
                                        if _rtext:
                                            text ("You: " + _rtext) font ACT_FONT size 14 color "#4a7a9b"
