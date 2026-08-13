# Phase 67 debug — world pulse, incidents, ambient locals, location modifiers.
# tests/phase67_selfcheck.py is the authoritative runnable check.

init python:

    _P67_LOCATIONS = ["location_cafe", "location_bar", "location_park",
                      "location_gym", "location_library", "location_hub",
                      "location_sandbeach", "location_nightclub",
                      "location_hospital", "location_office"]

    def _p67_force_pulse():
        wp = dict(store.world_pulse_data)
        wp.pop(store.day, None)
        store.world_pulse_data = wp
        generate_world_pulse(store.day)
        renpy.notify("World pulse regenerated for day %d" % store.day)

    def _p67_force_event(template_id):
        t = WORLD_EVENT_TEMPLATES[template_id]
        pulse = store.world_pulse_data.setdefault(store.day,
                    {"day": store.day, "major_events": [], "minor_incidents": [],
                     "generated": True})
        evt = {"id": "%s_d%d_dbg" % (template_id, store.day),
               "template_id": template_id, "name": t["name"],
               "location": t["location"], "hours": [0, 27], "day": store.day,
               "blurb": t.get("blurb", ""),
               "location_modifiers": dict(t.get("location_modifiers", {})),
               "npcs": [], "resolved": False}
        evt["npcs"] = populate_event_npcs(t, evt, store.day)
        pulse["major_events"] = [evt]
        store.world_pulse_data = dict(store.world_pulse_data)
        renpy.notify("Forced %s at %s (all day)" % (t["name"], t["location"]))

    def _p67_clear_cooldowns():
        store._event_last_day = {}
        store._incident_last_day = {}
        store._encounter_last_day = {}
        store._incident_resolved = []
        store._rare_opportunity_last = {}
        renpy.notify("Phase 67 cooldowns cleared")

    def _p67_reveal_all():
        for d in range(store.day, store.day + 4):
            generate_world_pulse(d)
            for e in world_events_on_day(d):
                discover_event(e["id"], "debug")
        renpy.notify("All upcoming events revealed")

    def _p67_hide_all():
        store._discovered_events = {}
        renpy.notify("Event discovery cleared")

    def _p67_mod_line(loc):
        m = get_location_event_modifiers(loc)
        return ("%-22s %s" % (loc.replace("location_", ""),
                              ", ".join("%s+%d" % (k, v) for k, v in sorted(m.items()))
                              if m else "-"))


screen debug_p67_scr():
    modal True
    zorder 210
    add "#000000e0"
    frame:
        xalign 0.5 yalign 0.5
        xsize 900
        ysize 680
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "PHASE 67 — WORLD PULSE" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text "day %d, %02d:00   ·   campaign seed %d" % (day, int(hour), campaign_seed) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            null height 4
            viewport:
                xfill True
                ysize 540
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True
                    $ _pulse = world_pulse_today()

                    text "TODAY'S PULSE" font PROFILE_FONT size 13 color "#ffd66a"
                    if _pulse.get("major_events"):
                        for _e in _pulse["major_events"]:
                            text ("EVENT  %s @ %s  %02d-%02d  npcs: %s  [%s]"
                                  % (_e["name"], _e["location"].replace("location_", ""),
                                     _e["hours"][0], _e["hours"][1],
                                     ", ".join(_e["npcs"]) or "none",
                                     _discovered_events.get(_e["id"], "undiscovered"))) font ACT_FONT size 12 color "#5bcafa"
                    else:
                        text "no major event today" font ACT_FONT size 12 color "#7a9ab8"
                    if _pulse.get("minor_incidents"):
                        for _i in _pulse["minor_incidents"]:
                            text ("INCIDENT  %s @ %s  %02d-%02d  %s"
                                  % (_i["name"], _i["location"].replace("location_", ""),
                                     _i["hours"][0], _i["hours"][1],
                                     "seen" if incident_already_seen(_i["id"]) else "unseen")) font ACT_FONT size 12 color "#8fe0a0"
                    else:
                        text "no incidents today" font ACT_FONT size 12 color "#7a9ab8"
                    text ("budget used today: %d/%d mail, %d/%d posts"
                          % (_pulse_mail_today, PULSE_MAX_MAIL_PER_DAY,
                             _pulse_social_today, PULSE_MAX_SOCIAL_PER_DAY)) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "NEXT 3 DAYS" font PROFILE_FONT size 13 color "#ffd66a"
                    for _d in range(day + 1, day + 4):
                        $ _evs = world_events_on_day(_d)
                        text ("d%d: %s" % (_d, ", ".join("%s@%s%s" % (
                                e["name"], e["location"].replace("location_", ""),
                                "" if event_discovered(e["id"]) else " (unknown)")
                                for e in _evs) or "-")) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "ACTIVE MODIFIERS PER LOCATION (right now)" font PROFILE_FONT size 13 color "#ffd66a"
                    for _loc in _P67_LOCATIONS:
                        text _p67_mod_line(_loc) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "AMBIENT LOCALS AT CURRENT LOCATION" font PROFILE_FONT size 13 color "#ffd66a"
                    $ _here = ambient_npcs_here(current_loc)
                    text ("%s: %s" % (current_loc.replace("location_", ""),
                                      ", ".join("%s (%s, fam %d)" % (AMBIENT_NPC[a]["name"],
                                                                     ambient_tier(a),
                                                                     ambient_familiarity(a))
                                                for a in _here) or "nobody")) font ACT_FONT size 12 color "#7a9ab8"
                    text ("location familiarity: %s (%d visits)"
                          % (location_familiarity_tier(current_loc),
                             location_visits.get(current_loc, 0))) font ACT_FONT size 11 color "#7a9ab8"

                    null height 6
                    text "EVENT COOLDOWNS" font PROFILE_FONT size 13 color "#ffd66a"
                    for _tid in sorted(WORLD_EVENT_TEMPLATES):
                        $ _last = _event_last_day.get(_tid, -999)
                        $ _rem = max(0, WORLD_EVENT_TEMPLATES[_tid]["cooldown_days"] - (day - _last))
                        text ("%-22s %s" % (_tid, "ready" if _rem <= 0 else "%d day(s)" % _rem)) font ACT_FONT size 11 color ("#8fe0a0" if _rem <= 0 else "#7a9ab8")

                    null height 8
                    text "ACTIONS" font PROFILE_FONT size 13 color "#ffd66a"
                    hbox:
                        spacing 8
                        box_wrap True
                        textbutton "Regenerate today" action Function(_p67_force_pulse) text_size 12
                        textbutton "Clear cooldowns" action Function(_p67_clear_cooldowns) text_size 12
                        textbutton "Reveal all events" action Function(_p67_reveal_all) text_size 12
                        textbutton "Hide all events" action Function(_p67_hide_all) text_size 12
                    null height 4
                    text "Force an event (all day, at its own location):" font ACT_FONT size 11 color "#7a9ab8"
                    hbox:
                        spacing 6
                        box_wrap True
                        for _tid in sorted(WORLD_EVENT_TEMPLATES):
                            textbutton _tid action Function(_p67_force_event, _tid) text_size 11

            null height 4
            textbutton "Close" action [Hide("debug_p67_scr"), Show("debug_menu")] xalign 0.5 text_size 16 text_color "#9fb6d6"
