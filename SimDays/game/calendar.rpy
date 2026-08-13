# Calendar system — view upcoming events and commitments.
# Events are added by the invitation system; the calendar is VIEW-ONLY.
# Attending happens at the location, not by tapping here.

default calendar_events = []

init python:

    def add_calendar_event(title, day, hour, duration=1, category="event",
                           commitment=False, npc_id=None, invitation_id=None):
        eid = "cal_%s_day%d_h%d" % (title[:8].replace(" ", "").lower(), day, int(hour))
        store.calendar_events = list(store.calendar_events) + [{
            "id": eid, "title": title, "day": day, "hour": hour, "duration": duration,
            "category": category, "commitment": commitment, "npc_id": npc_id,
            "invitation_id": invitation_id, "status": "upcoming",
            "consequence_processed": False,
        }]
        return eid

    def get_calendar_events(day=None):
        if day is None: day = store.day
        return sorted([e for e in store.calendar_events if e["day"] >= day],
                      key=lambda e: (e["day"], e.get("hour", 0)))

    def cancel_calendar_commitment(event_id):
        evts = list(store.calendar_events)
        for i, e in enumerate(evts):
            if e["id"] == event_id and e.get("commitment"):
                e = dict(e); e["status"] = "cancelled"
                evts[i] = e
        store.calendar_events = evts

    def _calendar_badge_count():
        """Count of commitment events today or tomorrow."""
        return sum(1 for e in store.calendar_events
                   if e.get("commitment") and e["status"] == "upcoming"
                   and store.day <= e["day"] <= store.day + 1)


# ── Calendar phone screen ────────────────────────────────────────────────────
screen phone_calendar_scr():
    modal True
    use phone_shell:
        $ _cal_evts = get_calendar_events()
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Calendar" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 620
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    if not _cal_evts:
                        null height 20
                        text "No upcoming events." font ACT_FONT size 15 color "#4a6080" xalign 0.5
                    else:
                        $ _last_day_shown = -1
                        for _ce in _cal_evts:
                            if _ce["day"] != _last_day_shown:
                                $ _last_day_shown = _ce["day"]
                                text ("Day %d  (%s)" % (_ce["day"] + 1, DAY_NAMES[_ce["day"] % 7])):
                                    font PROFILE_FONT size 13 color "#5bcafa"
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (10, 7, 10, 7)
                                hbox:
                                    spacing 8
                                    xfill True
                                    yalign 0.5
                                    vbox:
                                        yalign 0.5
                                        spacing 2
                                        hbox:
                                            spacing 6
                                            if _ce.get("commitment"):
                                                text "●" font PROFILE_FONT size 10 color "#ffd66a" yalign 0.5
                                            text _ce["title"] font ACT_FONT size 13 color "#cfe0f5"
                                        $ _hr = int(_ce.get("hour", 0))
                                        $ _sfx = "AM" if _hr < 12 else "PM"
                                        $ _h12 = _hr % 12 or 12
                                        $ _hr_lbl = "%d:00 %s" % (_h12, _sfx)
                                        if _ce.get("npc_id") and _ce["npc_id"] in NPC_DATA:
                                            text ("%s  ·  %s" % (_hr_lbl, NPC_DATA[_ce["npc_id"]]["name"])) font ACT_FONT size 11 color "#7a9ab8"
                                        else:
                                            text _hr_lbl font ACT_FONT size 11 color "#7a9ab8"
            null height 6
            textbutton "Back" action [Hide("phone_calendar_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
