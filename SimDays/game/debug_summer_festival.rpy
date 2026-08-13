# Summer Festival debug. tests/summer_festival_selfcheck.py is the authoritative
# runnable check; this screen is for driving the event by hand in-game.

init python:

    _SF_DEFAULT_STATE = {
        "scheduled_day": -1, "eligible": False, "discovered": False,
        "attended": False, "missed": False, "blackout_choice": None,
        "blackout_result": None, "shelter_focus": None,
        "keepsake_awarded": False, "follow_up_mail_queued": False,
        "aftermath_done": False, "sync_run_day": -1,
    }

    def _debug_festival_force_schedule():
        for _n in SF_NPCS:
            setattr(store, _n + "_met", True)
        _debug_festival_reset()
        schedule_summer_festival(force_day=store.day + 2)
        renpy.notify("Festival scheduled for day %d"
                     % (store.summer_festival_state["scheduled_day"] + 1))

    def _debug_festival_reset():
        store.summer_festival_state = dict(_SF_DEFAULT_STATE)
        store.npc_schedule_overrides = [
            o for o in store.npc_schedule_overrides
            if o.get("source_id") != "summer_festival"]
        store.player_mail = [m for m in store.player_mail
                             if not m["tag"].startswith("summer_festival")]
        store.npc_messages = [m for m in store.npc_messages
                              if not m["tag"].startswith("summer_festival")]
        store.social_feed_posts = [p for p in store.social_feed_posts
                                   if not str(p.get("id", "")).startswith("sf_")]
        renpy.notify("Festival state reset")

    def _debug_festival_simulate_missed():
        sf = store.summer_festival_state
        if sf["scheduled_day"] < 0:
            schedule_summer_festival(force_day=store.day - 1)
        sf["scheduled_day"] = store.day - 1
        sf["attended"] = False
        renpy.notify("missed=%s" % check_festival_expiry())

    def _debug_festival_state_lines():
        sf = store.summer_festival_state
        return ["%-22s %s" % (k, sf.get(k)) for k in sorted(_SF_DEFAULT_STATE)]

    def _debug_festival_override_lines():
        rows = [o for o in store.npc_schedule_overrides
                if o.get("source_id") == "summer_festival"]
        if not rows:
            return ["(no festival overrides)"]
        return ["%-8s d%-4d %02d-%02d  %s" % (o["npc_id"], o["day"],
                                              o["hour_start"], o["hour_end"],
                                              o["location_id"]) for o in rows]


screen debug_sf_scr():
    modal True
    zorder 210
    add "#000000e0"
    frame:
        xalign 0.5 yalign 0.5
        xsize 860
        ysize 660
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 6
            text "DOWNTOWN SUMMER FESTIVAL" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            text "day %d (%s), %02d:00   ·   eligible now: %s" % (
                    day + 1, DAY_NAMES[day % 7], int(hour),
                    summer_festival_eligible()) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            null height 4
            viewport:
                xfill True
                ysize 520
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 3
                    xfill True

                    text "STATE" font PROFILE_FONT size 13 color "#ffd66a"
                    for _l in _debug_festival_state_lines():
                        text _l font ACT_FONT size 12 color "#cfe0f5"

                    null height 6
                    text "NPC SCHEDULE OVERRIDES" font PROFILE_FONT size 13 color "#ffd66a"
                    for _l in _debug_festival_override_lines():
                        text _l font ACT_FONT size 12 color "#7a9ab8"

                    null height 6
                    text "open right now: %s" % summer_festival_open_now() font ACT_FONT size 12 color "#5bcafa"

                    null height 8
                    text "ACTIONS" font PROFILE_FONT size 13 color "#ffd66a"
                    vbox:
                        spacing 4
                        textbutton "Force eligible + schedule (day+2)" action Function(_debug_festival_force_schedule) text_size 14
                        textbutton "Mark discovered" action SetDict(summer_festival_state, "discovered", True) text_size 14
                        textbutton "Run daily sync now" action [SetDict(summer_festival_state, "sync_run_day", -1), Function(sync_summer_festival)] text_size 14
                        textbutton "Start festival directly" action [Hide("debug_sf_scr"), Jump("summer_festival_main")] text_size 14
                        textbutton "Jump to blackout — technical branch" action [Hide("debug_sf_scr"), Jump("summer_festival_blackout_technical")] text_size 14
                        textbutton "Simulate missed festival" action Function(_debug_festival_simulate_missed) text_size 14
                        textbutton "Trigger next-day aftermath (attended)" action Function(_queue_festival_aftermath, True) text_size 14
                        textbutton "Trigger next-day aftermath (missed)" action Function(_queue_festival_aftermath, False) text_size 14
                        textbutton "Reset state" action Function(_debug_festival_reset) text_size 14 text_color "#e05533"

            null height 4
            textbutton "Close" action [Hide("debug_sf_scr"), Show("debug_menu")] xalign 0.5 text_size 16 text_color "#9fb6d6"
