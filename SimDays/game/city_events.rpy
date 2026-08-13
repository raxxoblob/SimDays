# Dynamic city events — 3 events generated per week, discoverable at locations.
# Attending happens by being at the right location during the event's time window.

init python:

    CITY_EVENT_TEMPLATES = [
        {"id": "open_mic_bar",    "title": "Open Mic Night",       "category": "music",
         "location": "location_bar",     "duration": 3, "hour": 20,
         "desc": "Local musicians take the stage at Static.",
         "req": {}, "rewards": {"music_xp": 8, "rep": 3}, "days": [4, 5]},
        {"id": "career_fair",     "title": "Career Fair",          "category": "career",
         "location": "location_hub",     "duration": 4, "hour": 10,
         "desc": "Companies and candidates meet at The Hub.",
         "req": {}, "rewards": {"biz_xp": 6, "int_stat": 4}, "days": [5, 6]},
        {"id": "art_exhibition",  "title": "Local Art Exhibition", "category": "art",
         "location": "location_park",    "duration": 3, "hour": 13,
         "desc": "Emerging artists display work in the park.",
         "req": {}, "rewards": {"art_xp": 6, "rep": 2}, "days": [5, 6]},
        {"id": "community_wkshp", "title": "Community Workshop",  "category": "skill",
         "location": "location_library", "duration": 2, "hour": 14,
         "desc": "Hands-on skills workshop at the library.",
         "req": {}, "rewards": {"prog_xp": 5, "biz_xp": 5}, "days": [0, 1, 2, 3, 4]},
        {"id": "sport_event",     "title": "Amateur Sports Day",   "category": "fitness",
         "location": "location_gym",     "duration": 3, "hour": 10,
         "desc": "Community sports day at Iron Gate.",
         "req": {"stat_str": 20}, "rewards": {"fit_xp": 8, "str_stat": 6}, "days": [5, 6]},
        {"id": "networking_eve",  "title": "Networking Evening",   "category": "career",
         "location": "location_bar",     "duration": 2, "hour": 19,
         "desc": "Professionals mixing at Static.",
         "req": {"stat_chr": 20}, "rewards": {"biz_xp": 5, "chr_stat": 4}, "days": [2, 3, 4]},
    ]

    def generate_city_events_for_week(week_number):
        if store.city_event_generation_week == week_number: return
        import random as _r
        _rng = _r.Random(week_number * 7919 + 13)
        week_start_day = week_number * 7
        templates = list(CITY_EVENT_TEMPLATES)
        _rng.shuffle(templates)
        picked = []
        used_days = set()
        for tmpl in templates:
            if len(picked) >= 3: break
            valid_days = [week_start_day + d for d in tmpl["days"]
                          if week_start_day + d not in used_days]
            if not valid_days: continue
            event_day = _rng.choice(valid_days)
            used_days.add(event_day)
            eid = "city_%s_w%d" % (tmpl["id"], week_number)
            picked.append({
                "id": eid, "template_id": tmpl["id"], "title": tmpl["title"],
                "category": tmpl["category"], "location": tmpl["location"],
                "day": event_day, "hour": tmpl["hour"], "duration": tmpl["duration"],
                "desc": tmpl["desc"], "req": tmpl["req"], "rewards": tmpl["rewards"],
                "status": "announced", "saved_to_calendar": False,
                "attended": False, "result": None,
            })
        existing_ids = {e["id"] for e in store.city_event_schedule}
        new_events = [e for e in picked if e["id"] not in existing_ids]
        store.city_event_schedule = list(store.city_event_schedule) + new_events
        store.city_event_generation_week = week_number

    def check_city_events_new_week():
        week = store.day // 7
        generate_city_events_for_week(week)

    def _city_event_req_met(req):
        for k, v in req.items():
            # Phase 65: one non-numeric requirement — the art exhibition needs a
            # piece actually entered, not just a stat. Everything else stays a
            # plain "store attribute >= value" check.
            if k == "submitted_artwork":
                if not any(a.get("submitted_to") for a in store.player_artworks):
                    return False
                continue
            if getattr(store, k, 0) < v:
                return False
        return True

    def active_city_events_at(location_id):
        """Events at this location happening during current hour window."""
        current_hour = int(store.hour)
        return [e for e in store.city_event_schedule
                if e["location"] == location_id
                and e["status"] == "announced"
                and e["day"] == store.day
                and e["hour"] <= current_hour < e["hour"] + e["duration"]
                and not e.get("attended")
                and _city_event_req_met(e.get("req", {}))]

    def attend_city_event(event_id):
        evts = list(store.city_event_schedule)
        for i, e in enumerate(evts):
            if e["id"] == event_id and not e.get("attended"):
                e = dict(e)
                e["attended"] = True
                e["status"] = "completed"
                tmpl = next((t for t in CITY_EVENT_TEMPLATES if t["id"] == e["template_id"]), {})
                rewards = tmpl.get("rewards", {})
                for k, v in rewards.items():
                    if k.endswith("_xp"):
                        gain_skill(k[:-3], v)
                    elif k.endswith("_stat"):
                        gain_stat(k[:-5], v * 10)
                    elif k == "rep":
                        store.freelance_reputation = min(100, store.freelance_reputation + v)
                spend_time(e["duration"])
                store.need_energy = max(0, store.need_energy - 15)
                record_game_event("attend_" + event_id, "event", "Attended: " + e["title"],
                    summary=True, journal=True,
                    metadata={"category": e["category"], "rewards": rewards})
                evts[i] = e
                store.city_event_schedule = evts
                return rewards
        return {}

    def expire_city_events():
        updated = []
        for e in store.city_event_schedule:
            if e["status"] == "announced" and store.day > e["day"]:
                e = dict(e)
                e["status"] = "missed"
            updated.append(e)
        store.city_event_schedule = updated

    def _social_badge_count():
        """Count of announced city events not yet saved to calendar."""
        return sum(1 for e in store.city_event_schedule
                   if e["status"] == "announced" and not e.get("saved_to_calendar"))

    def _save_city_event_to_calendar_wrapper(event_id):
        """Function() wrapper — returns None."""
        evts = list(store.city_event_schedule)
        for i, e in enumerate(evts):
            if e["id"] == event_id and not e.get("saved_to_calendar"):
                e = dict(e)
                e["saved_to_calendar"] = True
                add_calendar_event(
                    title=e["title"], day=e["day"], hour=e["hour"],
                    duration=e["duration"], category=e["category"])
                evts[i] = e
        store.city_event_schedule = evts

    def _attend_city_event_wrapper(event_id):
        """Function() wrapper — returns None."""
        attend_city_event(event_id)

    # ── Section 24L — NPC social post generation ──────────────────────────────
    NPC_SOCIAL_POST_TEMPLATES = {
        "nora": [
            {"id": "nora_tired_shift",   "trigger_day_mod": 4, "text": "Another eight-hour shift. Coffee count: four. Regrets: zero."},
            {"id": "nora_weekend_morn",  "trigger_day_mod": 6, "text": "Finally a quiet Saturday morning. I might actually read something."},
        ],
        "marcus": [
            {"id": "marcus_park_morning","trigger_day_mod": 1, "text": "6am run done. Anyone who hasn't tried the east loop is missing out."},
            {"id": "marcus_bar_friday",  "trigger_day_mod": 4, "text": "Static tonight. Come before 9 if you want a seat."},
        ],
        "zoe": [
            {"id": "zoe_park_sketch",    "trigger_day_mod": 3, "text": "Spent three hours in the park today and didn't open my phone once. 10/10."},
        ],
        "eli": [
            {"id": "eli_tech_frustration","trigger_day_mod": 2, "text": "Two hours debugging. The problem was a missing semicolon. I need a career change."},
            {"id": "eli_workshop",        "trigger_day_mod": 3, "text": "Running a small session at the Hub next week. Drop in if you want."},
        ],
        "sam": [
            {"id": "sam_training",        "trigger_day_mod": 1, "text": "New personal record on the morning run. Slow and steady gets results."},
        ],
    }

    def generate_social_posts_for_week(week):
        if store.social_feed_generated_week == week: return
        store.social_feed_generated_week = week
        import random as _r
        rng = _r.Random(week * 9901 + 7)
        week_start_day = week * 7
        posts = list(store.social_feed_posts)
        existing_ids = {p["id"] for p in posts}
        for npc_id, templates in NPC_SOCIAL_POST_TEMPLATES.items():
            if not getattr(store, npc_id + "_met", False): continue
            for tmpl in templates:
                if tmpl["id"] in existing_ids: continue
                if rng.random() > 0.6: continue
                post_day = week_start_day + (tmpl["trigger_day_mod"] % 7)
                posts.insert(0, {"id": tmpl["id"], "npc_id": npc_id, "text": tmpl["text"], "day": post_day})
        store.social_feed_posts = posts

    # ── Section 24M — Phone reminders ─────────────────────────────────────────
    def check_phone_reminders():
        sent = set(store._sent_phone_reminders)
        new_sent = []
        for ev in store.calendar_events:
            rid = "cal_remind_" + str(ev.get("id", ""))
            if rid in sent: continue
            days_until = ev.get("day", 999) - store.day
            if 0 < days_until <= 1:
                renpy.notify("Reminder: %s tomorrow." % ev.get("title", "event"))
                new_sent.append(rid)
        p = store.freelance_active_project
        if p is not None:
            rid = "fl_deadline_" + str(p.get("id", p.get("template_id", "")))
            if rid not in sent:
                days_left = p.get("deadline_day", 999) - store.day
                if 0 < days_left <= 1:
                    renpy.notify("Deadline: '%s' is due tomorrow." % p.get("title", "project"))
                    new_sent.append(rid)
        if new_sent:
            store._sent_phone_reminders = list(store._sent_phone_reminders) + new_sent


# ── Social phone screen ────────────────────────────────────────────────────────
screen phone_social_scr():
    modal True
    use phone_shell:
        $ _social_events = [e for e in city_event_schedule if e["status"] == "announced"]
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "City Events" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 610
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    if not _social_events:
                        null height 20
                        text "No upcoming events this week." font ACT_FONT size 15 color "#4a6080" xalign 0.5
                    for _se in sorted(_social_events, key=lambda x: x["day"]):
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 8, 10, 8)
                            vbox:
                                spacing 4
                                hbox:
                                    xfill True
                                    text _se["title"] font PROFILE_FONT size 13 color "#cfe0f5" yalign 0.5
                                    $ _se_day_lbl = "Day %d" % (_se["day"] + 1)
                                    text _se_day_lbl font ACT_FONT size 11 color "#5bcafa" yalign 0.5 xalign 1.0
                                text _se["desc"] font ACT_FONT size 12 color "#7a9ab8"
                                hbox:
                                    spacing 10
                                    $ _se_hr = int(_se["hour"])
                                    $ _se_sfx = "AM" if _se_hr < 12 else "PM"
                                    $ _se_h12 = _se_hr % 12 or 12
                                    text ("%d:00 %s" % (_se_h12, _se_sfx)) font ACT_FONT size 11 color "#4a6080"
                                    text ("%dh" % _se["duration"]) font ACT_FONT size 11 color "#4a6080"
                                if not _se.get("saved_to_calendar"):
                                    textbutton "Save to Calendar":
                                        action Function(_save_city_event_to_calendar_wrapper, _se["id"])
                                        background Frame("images/ui/act_bar_idle.png", 10, 10, 10, 10)
                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 10, 10, 10, 10)
                                        xpadding 8 ypadding 4
                                        text_font ACT_FONT text_size 11 text_color "#5bcafa" text_hover_color "#ffffff"
                                else:
                                    text "✓ Saved" font ACT_FONT size 11 color "#7fd06a"
            # NPC social posts
            null height 10
            text "From your contacts" font PROFILE_FONT size 16 color "#5bcafa" xalign 0.0
            null height 4
            $ _npc_posts = [p for p in store.social_feed_posts if p.get("day", 0) <= store.day][:10]
            if not _npc_posts:
                text "No posts yet." font ACT_FONT size 13 color "#4a6080"
            for _post in _npc_posts:
                frame:
                    xfill True
                    background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                    padding (10, 8, 10, 8)
                    vbox:
                        spacing 3
                        hbox:
                            xfill True
                            text _post.get("npc_id", "?").capitalize() font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5
                            $ _pd = "Day %d" % (_post.get("day", 0) + 1)
                            text _pd font ACT_FONT size 11 color "#5bcafa" yalign 0.5 xalign 1.0
                        text _post.get("text", "") font ACT_FONT size 13 color "#cfe0f5"
            null height 6
            textbutton "Back" action [Hide("phone_social_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
