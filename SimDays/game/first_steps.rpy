# first_steps.rpy — Optional First Steps card and permanent Help section.
# All objectives are non-blocking. Card disappears when completed or hidden.

init python:
    # ── Track baseline snapshot ───────────────────────────────────────────────
    def _fs_set_track_baseline():
        """Record state snapshots at the moment a track is chosen (called from start:)."""
        track = store.first_steps_track
        if track == "career":
            store.fs_career_skill_baseline = {
                k: getattr(store, "skill_" + k, 0) for k in store.PRO_SKILLS
            }
        elif track == "people":
            store.fs_people_baseline_met = [
                k for k in store.NPC_DATA if getattr(store, k + "_met", False)
            ]
            store.fs_people_baseline_contacts = list(store.npc_contacts)
            store.fs_talk_count_baseline = store.fs_talk_count

    # ── Immediate hooks (call these at the point where something relevant happens) ──

    def fs_mark(flag_name):
        """Set fs_<flag_name> = True and immediately evaluate objectives."""
        setattr(store, "fs_" + flag_name, True)
        fs_refresh()

    def fs_record_district(district_key):
        """Record a MAP zone visit for the Explore track. district_key = MAP_ZONES key."""
        if district_key not in store.fs_visited_districts:
            store.fs_visited_districts = list(store.fs_visited_districts) + [district_key]
            fs_refresh()

    def fs_record_social(npc_id, interaction_type="talk"):
        """Record a social interaction for the People track and refresh objectives."""
        store.fs_talk_count = store.fs_talk_count + 1
        fs_refresh()

    def fs_record_skill_gain(skill_key, prev_level, new_level):
        """Called when a professional skill level rises. Triggers objective refresh."""
        if new_level > prev_level:
            fs_refresh()

    def _fs_career_rejection():
        """Shared hook for any career application that fails a requirements check."""
        if not store.tip_career_reject_shown:
            store.tip_career_reject_shown = True
            renpy.notify("Check Profile (Me) to track what each career needs.")
        store.fs_career_req_seen = True
        fs_refresh()

    # ── Core refresh (evaluate all objectives; fire completion exactly once) ───

    def fs_refresh():
        track = store.first_steps_track
        if not track or store.first_steps_completed or store.first_steps_hidden:
            return
        objectives = FIRST_STEPS.get(track, {}).get("objectives", [])
        if not objectives:
            return
        progress = dict(store.first_steps_progress)
        changed = False
        all_done = True
        for obj in objectives:
            if not progress.get(obj["id"], False):
                try:
                    done = obj["done"]()
                except Exception:
                    done = False
                if done:
                    progress[obj["id"]] = True
                    changed = True
                else:
                    all_done = False
        if changed:
            store.first_steps_progress = progress
        if all_done and not store.first_steps_completed:
            store.first_steps_completed = True
            if not message_already_queued("fs_complete"):
                queue_phone_message("marcus", "Heard you found your footing. Good.", store.day + 1, "fs_complete")
                _apply_trust("marcus", 1)

    def fs_update():
        """Alias for fs_refresh() — kept for any legacy callers."""
        fs_refresh()

    # ── Objective definitions ─────────────────────────────────────────────────

    FIRST_STEPS = {
        "money": {
            "title": "Getting Started — Money",
            "objectives": [
                {"id": "map_open",   "label": "Open the city map",       "done": lambda: store.fs_map_visited},
                {"id": "cafe_visit", "label": "Visit Grounds",            "done": lambda: store.fs_grounds_visited},
                {"id": "cafe_shift", "label": "Complete a Grounds shift", "done": lambda: store.fs_grounds_shift_done},
            ],
        },
        "career": {
            "title": "Getting Started — Career",
            "objectives": [
                {"id": "career_req", "label": "Apply for a career (see requirements)", "done": lambda: store.fs_career_req_seen},
                {"id": "study_done", "label": "Study or train once",                   "done": lambda: store.fs_study_done},
                {"id": "skill_up",   "label": "Improve a professional skill",          "done": lambda: any(
                    getattr(store, "skill_" + k, 0) > store.fs_career_skill_baseline.get(k, 0)
                    for k in store.PRO_SKILLS
                )},
            ],
        },
        "people": {
            "title": "Getting Started — People",
            "objectives": [
                {"id": "new_npc",   "label": "Meet someone new",             "done": lambda: any(
                    getattr(store, k + "_met", False)
                    for k in store.NPC_DATA if k not in store.fs_people_baseline_met
                )},
                {"id": "contacts",  "label": "Save a contact",               "done": lambda: any(
                    c for c in store.npc_contacts if c not in store.fs_people_baseline_contacts
                )},
                {"id": "two_talks", "label": "Have two more conversations",  "done": lambda:
                    store.fs_talk_count >= store.fs_talk_count_baseline + 2
                },
            ],
        },
        "explore": {
            "title": "Getting Started — Explore",
            "objectives": [
                {"id": "map_open",    "label": "Open the city map",             "done": lambda: store.fs_map_visited},
                {"id": "two_places",  "label": "Visit two different districts", "done": lambda: len(store.fs_visited_districts) >= 2},
                {"id": "outside_act", "label": "Do something outside home",     "done": lambda: store.fs_outside_activity},
            ],
        },
    }

    HELP_PAGES = [
        {
            "title": "Time and Activities",
            "body": "Activities advance the clock — you'll see the duration in the menu. Travelling between locations is free: moving around the city never costs time. Plan your day around what you want to accomplish.",
        },
        {
            "title": "Needs",
            "body": "Hunger, Energy and Hygiene are shown in the top bar. Low Energy blocks demanding activities. Low Hygiene reduces how others read your Appearance. Address them before the bars hit critical.",
        },
        {
            "title": "Work and Careers",
            "body": "Grounds is the easiest starting job — no requirements, immediate income. Other careers require skills, education, or both. Performance improves with shifts. Promotion happens when performance hits 100 and all rank requirements are met.",
        },
        {
            "title": "Skills and Education",
            "body": "Professional skills (Service, Medicine, Programming, Business, Fitness, Music, Art) improve through work and practice. City College offers structured courses. The Library lets you self-study for free. Some career ranks eventually need a degree.",
        },
        {
            "title": "People and Schedules",
            "body": "NPCs follow their own daily schedules. If someone isn't where you expected, they may be elsewhere or off the clock. Use your phone to check where a contact is. Talk regularly — people notice when you show up.",
        },
        {
            "title": "Commitments",
            "body": "When you agree to meet someone, it becomes a Commitment in your phone. A reminder appears on the HUD when one is approaching. Missing a commitment affects your relationship with that person.",
        },
    ]


screen phone_help_scr():
    frame:
        xpos 1462
        ypos 392
        xsize 456
        ysize 682
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (24, 16, 24, 16)
        vbox:
            spacing 8
            text "Help" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 4
            viewport:
                ysize 560
                mousewheel True
                vbox:
                    spacing 12
                    xfill True
                    for _hp in HELP_PAGES:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                            padding (14, 10, 14, 10)
                            vbox:
                                spacing 6
                                text _hp["title"] font PROFILE_FONT size 13 color "#5bcafa"
                                text _hp["body"] font ACT_FONT size 12 color "#cfe0f5"
            null height 4
            textbutton "Back" action [Hide("phone_help_scr"), Show("phone_goals_scr")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
