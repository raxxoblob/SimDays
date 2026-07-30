# Unified NPC interaction hub.
#   Enter a location, "Talk to <someone>" -> their sprite centres, a relationship
#   panel shows on the right, and the ACTIONS sit along the bottom:
#       Talk (pick 1 of 9 shared topics) · Give gift · Invite out · Leave
#   Topics are the SAME for everyone; each person LIKES / DISLIKES different ones,
#   so the same topic lands differently depending on who you're talking to.
#
# To add a character: one NPC_DATA entry (+ a greet label). No per-topic writing.

init python:
    def rel_tier(aff):
        if aff >= 75: return "Close"
        if aff >= 50: return "Good friends"
        if aff >= 25: return "Friends"
        if aff >= 1:  return "Acquaintance"
        return "Stranger"

    # The 9 shared conversation topics.
    TOPICS = [
        ("music",     "Music"),
        ("sports",    "Sports & fitness"),
        ("art",       "Art"),
        ("food",      "Food"),
        ("ambition",  "Money & ambition"),
        ("travel",    "Travel"),
        ("movies",    "Movies & shows"),
        ("nightlife", "Nightlife"),
        ("work",      "Work"),
    ]
    TOPIC_LABEL = dict(TOPICS)

    # say  = the Character variable to speak as (defined in characters.rpy)
    # world/met/min_status = availability (see npc_known)
    # likes/dislikes = which of the 9 topics land well / badly
    MON_FRI = {0, 1, 2, 3, 4}
    MON_SAT = {0, 1, 2, 3, 4, 5}
    WKD     = {5, 6}
    FRISUN  = {4, 5, 6}
    NPC_DATA = {
        "nora": {
            "name": "Nora", "portrait": "portrait_nora", "sprite": "nora_cafe_normal", "say": "n",
            "aff": "nora_affection", "trust": "nora_trust", "greet": "nora_greet",
            "sprites": {"work": "nora_cafe_normal", "casual": "nora_casual_normal"},
            "world": True,
            "sched": [
                (MON_FRI, (7,  16), "location_cafe"),
                ({1, 4},  (17, 22), "location_bar"),
                (WKD,     (10, 14), "location_cafe"),
            ],
            "likes": ["food", "ambition", "movies"], "dislikes": ["nightlife"],
            "topic_arcs": {
                "food": [
                    {"id": "nora_food_1", "label": "arc_nora_food_1"},
                    {"id": "nora_food_2", "req": {"aff": 12, "done": "nora_food_1"}, "label": "arc_nora_food_2"},
                ],
                "ambition": [
                    {"id": "nora_ambition_1", "label": "arc_nora_ambition_1"},
                    {"id": "nora_ambition_2", "req": {"trust": 20, "done": "nora_ambition_1"}, "label": "arc_nora_ambition_2"},
                ],
            },
        },
        "marcus": {
            "name": "Marcus", "portrait": "portrait_marcus", "sprite": "marcus_casual_normal", "say": "m",
            "aff": "marcus_affection", "trust": "marcus_trust", "greet": "marcus_greet",
            "sprites": {"casual": "marcus_casual_normal", "evening": "marcus_bar_normal", "sport": "marcus_park_neutral"},
            "world": True, "sched": [
                (None, (6,  10), "location_park"),
                ({1},  (15, 17), "location_cafe"),    # Tuesday coffee stop (15–16 mutual with Nora)
                (None, (17, 24), "location_bar"),
                (WKD,  (24, 27), "location_nightclub"),
            ],
            "likes": ["sports", "food", "nightlife"], "dislikes": ["art"],
            "topic_arcs": {
                "sports": [
                    {"id": "marcus_sports_1", "label": "arc_marcus_sports_1"},
                    {"id": "marcus_sports_2", "req": {"aff": 15, "done": "marcus_sports_1"}, "label": "arc_marcus_sports_2"},
                ],
                "food": [
                    {"id": "marcus_food_1", "label": "arc_marcus_food_1"},
                    {"id": "marcus_food_2", "req": {"trust": 15, "done": "marcus_food_1"}, "label": "arc_marcus_food_2"},
                ],
            },
        },
        "caroline": {
            "name": "Caroline", "portrait": "portrait_caroline", "sprite": "caroline_normal", "say": "caro",
            "aff": "caroline_affection", "trust": "caroline_trust", "greet": "caroline_greet",
            "met": "caroline_met", "sched": [
                (MON_FRI, (9,  18), "location_office"),
                ({3},     (20, 23), "location_bar"),   # Thursday professional visit
            ],
            "likes": ["work", "ambition", "nightlife"], "dislikes": ["sports"],
        },
        "lena": {
            "name": "Dr. Lena", "portrait": "portrait_lena", "sprite": "drlena_normal", "say": "lena",
            "aff": "lena_affection", "trust": "lena_trust", "greet": "lena_greet",
            "met": "lena_met", "sched": [
                (MON_FRI, (8,  16), "location_hospital"),
                ({2, 4},  (18, 22), "location_bar"),
            ],
            "likes": ["work", "travel", "food"], "dislikes": ["nightlife"],
        },
        "natalie": {
            "name": "Natalie", "portrait": "portrait_natalie", "sprite": "natalie_normal", "say": "nat",
            "aff": "natalie_affection", "trust": "natalie_trust", "greet": "natalie_greet",
            "met": "natalie_met", "sched": [
                (MON_SAT, (7,  15), "location_warehouse"),
                (WKD,     (17, 21), "location_bar"),
            ],
            "likes": ["sports", "work", "ambition"], "dislikes": ["art"],
        },
        "martha": {
            "name": "Martha", "portrait": "portrait_martha", "sprite": "martha_neutral", "say": "ma",
            "aff": "martha_affection", "trust": "martha_trust", "greet": "martha_greet",
            "sprites": {"work": "martha_neutral", "evening": "martha_dress_normal"},
            "met": "martha_met", "story_gate": "caroline_met", "sched": [
                (MON_FRI, (9,  18), "location_office"),
                ({3},     (19, 23), "location_bar"),
            ],
            "likes": ["ambition", "work", "travel"], "dislikes": ["sports"],
        },
        "elle": {
            "name": "Elle", "portrait": "portrait_elle", "sprite": "elle_sundress_normal", "say": "el",
            "aff": "elle_affection", "trust": "elle_trust", "greet": "elle_greet",
            "world": True, "sched": [
                ({1, 3}, (9,  13), "location_cafe"),
                ({2},    (16, 19), "location_sandbeach"),
                (WKD,    (13, 18), "location_sandbeach"),
                (WKD,    (21, 25), "location_nightclub"),
            ],
            "likes": ["travel", "music", "art"], "dislikes": ["work"],
            "topic_arcs": {
                "travel": [
                    {"id": "elle_travel_1", "label": "arc_elle_travel_1"},
                    {"id": "elle_travel_2", "req": {"aff": 15, "done": "elle_travel_1"}, "label": "arc_elle_travel_2"},
                ],
            },
        },
        "zoe": {
            "name": "Zoe", "portrait": "portrait_zoe", "sprite": "zoe_punk_smile", "say": "z",
            "aff": "zoe_affection", "trust": "zoe_trust", "greet": "zoe_greet",
            "world": True, "sched": [
                (WKD,    (12, 18), "location_sandbeach"),
                ({3, 4}, (14, 18), "location_park"),
                ({2},    (14, 17), "location_cafe"),        # Wednesday sketching at Grounds
                (WKD,    (19, 24), "location_sandbeach"),  # covers zoe_beach_night_scene window
                (FRISUN, (24, 27), "location_nightclub"),
            ],
            "likes": ["art", "music", "nightlife"], "dislikes": ["ambition"],
            "topic_arcs": {
                "art": [
                    {"id": "zoe_art_1", "label": "arc_zoe_art_1"},
                    {"id": "zoe_art_2", "req": {"aff": 10, "done": "zoe_art_1"}, "label": "arc_zoe_art_2"},
                    {"id": "zoe_art_3", "req": {"trust": 15, "done": "zoe_art_2"}, "label": "arc_zoe_art_3"},
                    {"id": "zoe_art_4", "req": {"aff": 30, "done": "zoe_art_3"}, "label": "arc_zoe_art_4"},
                ],
                "music": [
                    {"id": "zoe_music_1", "label": "arc_zoe_music_1"},
                    {"id": "zoe_music_2", "req": {"aff": 15, "done": "zoe_music_1"}, "label": "arc_zoe_music_2"},
                ],
            },
        },
        "sam": {
            "name": "Sam", "portrait": "portrait_sam", "sprite": "sam_normal", "say": "sam",
            "aff": "sam_affection", "trust": "sam_trust", "greet": "sam_greet",
            "world": True, "sched": [
                (MON_FRI, (6,  10), "location_park"),
                (MON_FRI, (10, 14), "location_gym"),
                (WKD,     (9,  13), "location_gym"),
                ({4},     (16, 18), "location_park"),  # Friday outdoor exercise (aligns with Zoe park Thu–Fri 14–18)
            ],
            "likes": ["sports", "work", "food"], "dislikes": ["nightlife"],
        },
        "eli": {
            "name": "Eli", "portrait": "portrait_eli", "sprite": "eli_normal", "say": "eli",
            "aff": "eli_affection", "trust": "eli_trust", "greet": "eli_greet",
            "world": True, "sched": [
                (None,      (12, 20), "location_library"),
                ({1, 2, 3}, (20, 23), "location_bar"),
            ],
            "likes": ["work", "movies", "music"], "dislikes": ["sports"],
            "topic_arcs": {
                "work": [
                    {"id": "eli_work_1", "label": "arc_eli_work_1"},
                    {"id": "eli_work_2", "req": {"aff": 10, "done": "eli_work_1"}, "label": "arc_eli_work_2"},
                ],
            },
        },
        "kai": {
            "name": "Kai", "portrait": "portrait_kai", "sprite": "kai_gym_normal", "say": "kai",
            "aff": "kai_affection", "trust": "kai_trust", "greet": "kai_greet",
            "sprites": {"sport": "kai_gym_normal", "casual": "kai_normal"},
            "world": True, "sched": [
                ({1, 3}, (10, 14), "location_cafe"),
                (WKD,    (10, 14), "location_gym"),
                (WKD,    (14, 18), "location_sandbeach"),
                (WKD,    (18, 22), "location_bar"),
                (FRISUN, (22, 27), "location_nightclub"),
            ],
            "likes": ["sports", "music", "nightlife"], "dislikes": ["work"],
        },
        # Chef Rena — career mentor, off-duty at the nadbrzeze diner Mon/Wed nights.
        # aff/trust move only via culinary_arc scenes; no_decay exempts her from
        # the 7-day ignore decay (she's never in the world NPC interaction pool).
        "rena": {
            "name": "Chef Rena", "say": "rena",
            "sprite": "rena_casual_normal",
            "sprites": {"casual": "rena_casual_normal"},
            "aff": "rena_affection", "trust": "rena_trust",
            "met": "rena_met", "no_decay": True,
            "sched": [({0, 2}, (21, 26), "location_diner")],
        },
    }

    def npc_aff(npc_id):   return getattr(store, NPC_DATA[npc_id]["aff"])
    def npc_trust(npc_id): return getattr(store, NPC_DATA[npc_id]["trust"])

    def npc_sprite(npc_id, context=None):
        """Context-appropriate base ('normal') sprite for an NPC, so scenes can
        request an outfit by situation instead of hardcoding a filename that may
        be wrong for the setting (e.g. Nora's barista apron at home).

        `context` keys (e.g. "work", "casual", "evening", "sport") come from the
        NPC's optional "sprites" map in NPC_DATA. Falls back to the default
        "sprite" when the NPC has no outfit set or the context isn't defined.
        Only NPCs with real alternate art carry a "sprites" map; the rest just
        return their single sprite. Expression swaps within a scene still use
        explicit names — this picks the entry outfit."""
        d = NPC_DATA.get(npc_id, {})
        return d.get("sprites", {}).get(context, d["sprite"])

    def npc_is_temporarily_unavailable(npc_id):
        if npc_id == "elle" and store.elle_life_state == "abroad":
            return True
        return False

    def npc_schedule_entries(npc_id):
        if npc_id == "nora" and store.nora_life_state == "school":
            return _NORA_SCHOOL_SCHED   # defined in world_progression.rpy
        sched = NPC_DATA[npc_id].get("sched")
        if sched and npc_id == "rena" and store.day < store.rena_diner_absent_until_day:
            sched = [e for e in sched if e[2] != "location_diner"]
        if sched and npc_id == "lena" and store.day < store.lena_bar_absent_until_day:
            sched = [e for e in sched if e[2] != "location_bar"]
        # Phase 50: Zoe temporary gallery schedule — Sunday 14:00-18:00 during post-opening period
        if (npc_id == "zoe"
                and store.zoe_exhibition_done
                and store.day <= store.zoe_gallery_until_day):
            sched = list(sched) + [({6}, (14, 18), "location_gallery")]
        return sched

    def npc_here(npc_id):
        if npc_is_temporarily_unavailable(npc_id):
            return False
        sched = npc_schedule_entries(npc_id)
        if sched is None:   # no schedule key → NPC is unrestricted
            return True
        if not sched:       # schedule key present but all entries filtered → not here
            return False
        wd = store.day % 7
        for entry in sched:
            days = entry[0]
            h0, h1 = entry[1]
            loc = entry[2] if len(entry) > 2 else None
            if not (days is None or wd in days):
                continue
            if not (h0 <= store.hour < h1):
                continue
            if loc is None or store.current_loc == loc:
                return True
        return False

    def npc_known(npc_id):
        d = NPC_DATA[npc_id]
        gate = d.get("story_gate")
        if gate and not getattr(store, gate, False):
            return False
        if d.get("world"):
            return True
        mv = d.get("met")
        return bool(getattr(store, mv)) if mv else True

    def home_invite_available(npc_id, min_aff=0, min_trust=0):
        """True if npc_id is known and meets the aff/trust thresholds for a home visit."""
        return (npc_known(npc_id)
                and npc_aff(npc_id) >= min_aff
                and npc_trust(npc_id) >= min_trust)

    def npc_talkable(npc_id):
        return npc_here(npc_id) and npc_known(npc_id)

    # ── conversation reactions ─────────────────────────────────────────
    LIKE_LINES = [
        "%s? Now you're speaking my language.",
        "Okay, %s - finally, someone with taste.",
        "Don't get me started on %s. I could go all day.",
    ]
    NEUTRAL_LINES = [
        "%s? Sure, it's fine, I guess.",
        "Eh, no strong feelings on %s either way.",
        "%s, huh. It's alright.",
    ]
    DISLIKE_LINES = [
        "%s? Hard pass, honestly.",
        "Ugh, %s. Really not my thing.",
        "Let's talk about literally anything but %s.",
    ]
    # fired when the same topic has been used 3+ days in a row
    BURNOUT_LINES = [
        "Alex, how much can we talk about %s? Can we please change the subject?",
        "...%s again. I need you to surprise me here.",
        "We've covered %s like ten times now. Let's try something else.",
    ]

    def topic_used_today(npc_id, topic):
        return topic in store._topics_today.get(npc_id, [])

    # ── Relationship memory helpers ────────────────────────────────────────

    def add_relationship_memory(npc_id, memory_id, title):
        mems = dict(store.relationship_memories)
        lst  = list(mems.get(npc_id, []))
        if any(m["id"] == memory_id for m in lst):
            return
        lst.append({"id": memory_id, "title": title, "day": store.day})
        mems[npc_id] = lst
        store.relationship_memories = mems

    def relationship_memory_exists(npc_id, memory_id):
        return any(m["id"] == memory_id
                   for m in store.relationship_memories.get(npc_id, []))

    def relationship_memories_for(npc_id):
        return list(store.relationship_memories.get(npc_id, []))

    # ── Relationship threshold notifications ───────────────────────────────

    _REL_THRESHOLD_MSGS = {
        ("aff", 25): "{name} and you are becoming friends.",
        ("aff", 40): "You and {name} have grown close.",
        ("aff", 60): "{name} clearly enjoys your company.",
        ("aff", 75): "You and {name} have something real.",
        ("trust", 25): "{name} is starting to trust you.",
        ("trust", 40): "{name} trusts your judgement.",
        ("trust", 60): "{name} confides in you.",
    }

    def _check_relationship_thresholds(npc_id):
        """Call after applying aff/trust changes. Fires renpy.notify() for new thresholds.
        FIX 6: key is a 3-tuple (npc_id, stat_type, threshold) so aff 25 and trust 25
        are stored under distinct keys and never suppress each other."""
        d = NPC_DATA.get(npc_id)
        if not d:
            return
        seen = dict(store.relationship_thresholds_seen)
        name = d["name"]
        aff_val   = getattr(store, d["aff"],   0)
        trust_val = getattr(store, d["trust"], 0)
        changed = False
        for (kind, thresh), msg in _REL_THRESHOLD_MSGS.items():
            key = (npc_id, kind, thresh)
            if key in seen:
                continue
            val = aff_val if kind == "aff" else trust_val
            if val >= thresh:
                seen[key] = True
                changed = True
                renpy.notify(msg.format(name=name))
        if changed:
            store.relationship_thresholds_seen = seen
        # Martha corridor gesture — set pending when thresholds first crossed
        if (npc_id == "martha"
                and store.martha_affection >= 40 and store.martha_trust >= 35
                and not store.martha_corridor_done
                and not store.martha_corridor_pending):
            store.martha_corridor_pending = True
            store.martha_corridor_pending_day = store.day
            store.martha_corridor_context = {
                "source": "relationship_threshold",
                "trigger_day": store.day,
            }

    def _apply_aff(npc_id, delta):
        av = NPC_DATA[npc_id]["aff"]
        _old = getattr(store, av)
        _new = max(-100, min(_old + delta, 100))
        _actual = _new - _old
        setattr(store, av, _new)
        if _actual != 0 and store._npc_panel_npc_id == npc_id:
            store._rel_feedback_aff = _actual
        if delta > 0:
            _check_relationship_thresholds(npc_id)

    def _apply_trust(npc_id, delta):
        tv = NPC_DATA[npc_id]["trust"]
        _old = getattr(store, tv)
        _new = max(0, min(_old + delta, 100))
        _actual = _new - _old
        setattr(store, tv, _new)
        if _actual != 0 and store._npc_panel_npc_id == npc_id:
            store._rel_feedback_tr = _actual
        if delta > 0:
            _check_relationship_thresholds(npc_id)

    def _check_talk_followup(npc_id):
        if npc_id == "marcus" and not store.talk_followup_marcus_first_shift_done:
            if "marcus_first_shift_checkin" in store.wed_resolved:
                return "talk_followup_marcus_first_shift"
        if npc_id == "martha":
            if not store.talk_followup_martha_credit_done:
                if relationship_memory_exists("martha", "martha_acknowledged_work"):
                    return "talk_followup_martha_credit"
            if not store.talk_followup_martha_revision_done:
                if store.martha_revision_choice is not None and "wev_corp_final_revision" in store.wed_resolved:
                    return "talk_followup_martha_revision"
            if not store.talk_followup_martha_settled_done:
                if store.corp_shifts >= 3:
                    return "talk_followup_martha_settled"
            if (not store.martha_jealousy_first_notice_done
                    and store.npc_jealousy_pending.get("martha")
                    and store.martha_corridor_done):
                return "martha_jealousy_first_notice"
        if npc_id == "nora":
            if (not store.nora_jealousy_first_notice_done
                    and store.npc_jealousy_pending.get("nora")
                    and store.nora_bad_day_done):
                return "nora_jealousy_first_notice"
        if npc_id == "eli":
            if (not store.eli_jealousy_first_notice_done
                    and store.npc_jealousy_pending.get("eli")
                    and store.eli_deploy_hug_done):
                return "eli_jealousy_first_notice"
        if npc_id == "zoe":
            if (not store.zoe_jealousy_first_notice_done
                    and store.npc_jealousy_pending.get("zoe")
                    and store.zoe_rain_done):
                return "zoe_jealousy_first_notice"
        # Phase 35: post-invitation follow-up (priority below jealousy, above life-progression)
        _inv_fu = store.npc_invitation_followup_pending.get(npc_id)
        if _inv_fu is not None and store.day > _inv_fu.get("completed_day", store.day):
            return _inv_fu["invitation_id"] + "_followup"
        # Phase 42: life-progression follow-ups
        if npc_id == "nora":
            if (not store.nora_school_first_week_followup_done
                    and store.nora_life_state == "school"
                    and store.day > store.nora_school_start_day):
                return "talk_followup_nora_school_first_week"
        if npc_id == "elle":
            if (not store.elle_post_decision_talk_done
                    and store.elle_decision_done
                    and not npc_is_temporarily_unavailable("elle")
                    and (
                        (store.elle_life_state == "returned" and store.elle_return_message_done)
                        or (store.elle_life_state == "staying" and store.elle_decision_callback_done)
                        or (store.elle_life_state == "deferred" and store.elle_decision_callback_done)
                    )):
                return "talk_followup_elle_post_decision"
        # Phase 46: story aftermath (below life-progression, above social-graph callbacks)
        _46_lst = store.npc_story_aftermath_pending.get(npc_id)
        if _46_lst:
            _46_eligible = [e for e in _46_lst if store.day >= e["eligible_day"]]
            if _46_eligible:
                return min(_46_eligible, key=lambda e: e["created_day"])["label"]
        # Phase 49: home-visit callbacks (below Phase 46 aftermath, above Phase 44 crossovers)
        if npc_id == "nora":
            if (not store.nora_home_coffee_followup_done
                    and store.nora_home_coffee_done
                    and store.nora_home_coffee_day >= 0
                    and store.day > store.nora_home_coffee_day):
                return "talk_followup_nora_home_coffee"
        if npc_id == "eli":
            if (not store.eli_home_dinner_followup_done
                    and store.eli_home_dinner_done
                    and store.eli_home_dinner_day >= 0
                    and store.day > store.eli_home_dinner_day):
                return "talk_followup_eli_home_dinner"
        if npc_id == "zoe":
            if (not store.zoe_home_guitar_followup_done
                    and store.zoe_home_guitar_done
                    and store.zoe_home_guitar_day >= 0
                    and store.day > store.zoe_home_guitar_day):
                return "talk_followup_zoe_home_guitar"
        # Phase 50: Zoe exhibition final callback (below Phase 46 aftermath, above Phase 44 crossovers)
        if npc_id == "zoe":
            if (not store.zoe_exhibition_followup_done
                    and store.zoe_exhibition_done
                    and store.day > store.zoe_gallery_until_day
                    and store.npc_story_aftermath_seen.get("zoe_exhibition")):
                return "talk_followup_zoe_exhibition"
        # Phase 44: NPC crossover callbacks (below aftermath, above milestones)
        _44_fired = store.wed_event_last_day
        if npc_id == "nora":
            if (not store.crossover_nora_elle_callback_nora_done
                    and "crossover_nora_elle_grounds" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_nora_elle_grounds", store.day)):
                return "talk_followup_crossover_nora_elle_nora"
        if npc_id == "elle":
            if (not store.crossover_nora_elle_callback_elle_done
                    and "crossover_nora_elle_grounds" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_nora_elle_grounds", store.day)):
                return "talk_followup_crossover_nora_elle_elle"
        if npc_id == "lena":
            if (not store.crossover_lena_marcus_callback_lena_done
                    and "crossover_lena_marcus_bar" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_lena_marcus_bar", store.day)):
                return "talk_followup_crossover_lena_marcus_lena"
        if npc_id == "marcus":
            if (not store.crossover_lena_marcus_callback_marcus_done
                    and "crossover_lena_marcus_bar" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_lena_marcus_bar", store.day)):
                return "talk_followup_crossover_lena_marcus_marcus"
            if (not store.crossover_caroline_marcus_callback_marcus_done
                    and "crossover_caroline_marcus_thursday" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_caroline_marcus_thursday", store.day)):
                return "talk_followup_crossover_caroline_marcus_marcus"
        if npc_id == "sam":
            if (not store.crossover_sam_kai_callback_sam_done
                    and "crossover_sam_kai_gym" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_sam_kai_gym", store.day)):
                return "talk_followup_crossover_sam_kai_sam"
        if npc_id == "kai":
            if (not store.crossover_sam_kai_callback_kai_done
                    and "crossover_sam_kai_gym" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_sam_kai_gym", store.day)):
                return "talk_followup_crossover_sam_kai_kai"
        if npc_id == "caroline":
            if (not store.crossover_caroline_marcus_callback_caroline_done
                    and "crossover_caroline_marcus_thursday" in store.wed_resolved
                    and store.day > _44_fired.get("crossover_caroline_marcus_thursday", store.day)):
                return "talk_followup_crossover_caroline_marcus_caroline"
        # Phase 43: milestone follow-ups (below crossover callbacks, above contextual Talk)
        _mil_lst = store.npc_milestone_followup_pending.get(npc_id)
        if _mil_lst:
            return min(_mil_lst, key=lambda e: e["created_day"])["label"]
        return None

    _CTX_TALK = {
        ("elle",   "location_sandbeach"): ("elle_sandbeach",  ["elle_sandbeach_tide",       "elle_sandbeach_shoes",      "elle_sandbeach_horizon"]),
        ("kai",    "location_sandbeach"): ("kai_sandbeach",   ["kai_sandbeach_water",        "kai_sandbeach_crowd",       "kai_sandbeach_walk"]),
        ("zoe",    "location_sandbeach"): ("zoe_sandbeach",   ["zoe_sandbeach_colour",       "zoe_sandbeach_footprints",  "zoe_sandbeach_wind"]),
        ("marcus", "location_cafe"):      ("marcus_grounds",  ["marcus_grounds_order",       "marcus_grounds_table",      "marcus_grounds_temperature"]),
        ("eli",    "location_library"):   ("eli_library",     ["eli_library_outlet",         "eli_library_bookmark",      "eli_library_keyboard"]),
        ("lena",   "location_hospital"):  ("lena_hospital",   ["lena_hospital_coffee",       "lena_hospital_sign",        "lena_hospital_quiet"]),
        ("sam",    "location_gym"):       ("sam_gym",         ["sam_gym_bench",              "sam_gym_music",             "sam_gym_rest"]),
        ("nora",    "location_cafe"):      ("nora_grounds",    ["nora_grounds_queue",         "nora_grounds_lid",          "nora_grounds_regular"]),
        ("martha",  "location_office"):    ("martha_nexus",    ["martha_nexus_elevator",      "martha_nexus_calendar",     "martha_nexus_badge"]),
        ("natalie", "location_warehouse"): ("natalie_warehouse", ["natalie_warehouse_marker", "natalie_warehouse_noise",   "natalie_warehouse_path"]),
        ("kai",     "location_nightclub"): ("kai_nightclub",   ["kai_nightclub_volume",       "kai_nightclub_exit",        "kai_nightclub_song"]),
        ("caroline", "location_office"):   ("caroline_nexus",  ["caroline_nexus_reception",   "caroline_nexus_floor",      "caroline_nexus_document"]),
        ("zoe",      "location_park"):     ("zoe_park",        ["zoe_park_tree",              "zoe_park_dog",              "zoe_park_path"]),
        ("elle",     "location_cafe"):     ("elle_grounds",    ["elle_grounds_window",        "elle_grounds_spoon",        "elle_grounds_choice"]),
        ("kai",      "location_gym"):      ("kai_gym",         ["kai_gym_mirror",             "kai_gym_machine",           "kai_gym_towel"]),
    }

    def _ctx_talk_label(npc_id):
        entry = _CTX_TALK.get((npc_id, store.current_loc))
        if not entry:
            return None
        ctl_key = npc_id + "|" + store.current_loc
        if store.contextual_talk_last_day.get(ctl_key) == store.day:
            return None
        hist_key, variants = entry
        label = _pick_ambient_variant(hist_key, variants)
        d = dict(store.contextual_talk_last_day)
        d[ctl_key] = store.day
        store.contextual_talk_last_day = d
        return label

    def mark_topic_today(npc_id, topic):
        td = dict(store._topics_today)
        td.setdefault(npc_id, [])
        if topic not in td[npc_id]:
            td[npc_id] = td[npc_id] + [topic]
        store._topics_today = td

    def complete_arc(arc_id):
        d = dict(store.topic_arc_done)
        d[arc_id] = True
        store.topic_arc_done = d

    LOCATION_NAMES = {
        "location_cafe":       "Grounds Café",
        "location_bar":        "the bar",
        "location_gym":        "the gym",
        "location_park":       "the park",
        "location_beach":      "the beach",
        "location_library":    "the library",
        "location_nightclub":  "Neon",
        "location_hospital":   "the hospital",
        "location_warehouse":  "the warehouse",
        "location_office":     "Nexus Tower",
        "location_hub":        "The Hub",
        "location_nadbrzeze":  "the Quayside",
        "location_anchor":     "The Anchor",
    }

    def npc_location_now(npc_id):
        if npc_is_temporarily_unavailable(npc_id):
            return None
        sched = npc_schedule_entries(npc_id)
        if not sched:
            return None
        wd = store.day % 7
        for entry in sched:
            days, (h0, h1) = entry[0], entry[1]
            loc = entry[2] if len(entry) > 2 else None
            if not (days is None or wd in days):
                continue
            if h0 <= store.hour < h1:
                return loc
        return None

    def send_npc_message(npc_id, text):
        _tag = "hi_%s_%d" % (npc_id, store.day)
        queue_phone_message(npc_id, text, store.day, _tag)
        deliver_message_now(_tag)

    def npc_last_message(npc_id):
        for m in reversed(store.npc_messages):
            if m.get("npc_id") == npc_id and m.get("delivered"):
                return m
        return None

    def check_arc(npc_id, topic):
        """Return next available arc stage for this NPC+topic, or None."""
        for stage in NPC_DATA[npc_id].get("topic_arcs", {}).get(topic, []):
            if store.topic_arc_done.get(stage["id"]):
                continue
            req = stage.get("req", {})
            if npc_aff(npc_id) < req.get("aff", 0):
                break
            if npc_trust(npc_id) < req.get("trust", 0):
                break
            flag = req.get("flag")
            if flag and not getattr(store, flag, False):
                break
            done_req = req.get("done")
            if done_req and not store.topic_arc_done.get(done_req):
                break
            return stage
        return None

    def npc_is_angry(npc_id):
        """True when NPC won't engage with intimate actions: hygiene too low or accumulated anger."""
        return store.need_hygiene < 30 or store.npc_anger.get(npc_id, 0) > 0

    def check_jealousy(active_npc_id):
        """NPCs in an active romance with the player (interested/dating/committed)
        react when they see the player get intimate with someone else here.
        Only called on date/hug/kiss actions, not on greeting.

        Gated on romance state, not raw affection: a close platonic friend
        (e.g. Marcus at high affection) is NOT a jealous partner. The active NPC
        is skipped, and so is anyone the player is only romancing on paper but
        who isn't present."""
        jealous_names = []
        for nid, d in NPC_DATA.items():
            if nid == active_npc_id:
                continue
            if romance_is_open(nid) and npc_here(nid):
                _apply_aff(nid, -5)
                _a = dict(store.npc_anger)
                _a[nid] = min(10, _a.get(nid, 0) + 3)
                store.npc_anger = _a
                jealous_names.append(d["name"])
        return jealous_names

    def public_talkable_npcs_here():
        """Ordered list of NPC IDs for whom npc_talkable() is currently True."""
        return [nid for nid in NPC_DATA if npc_talkable(nid)]

    def npc_avatar_path(npc_id):
        p = NPC_DATA[npc_id].get("portrait", "")
        return ("images/ui/icons/%s.png" % p) if p else None

    def portrait_circle(npc_id, sz=100):
        """Circular masked portrait displayable at sz×sz, or fallback silhouette."""
        path = npc_avatar_path(npc_id)
        mask = "images/ui/activity_dot.png"
        if path and renpy.loadable(path):
            return AlphaMask(Transform(path, size=(sz, sz)), Transform(mask, size=(sz, sz)))
        return portrait_circle_fallback(sz)

    def portrait_circle_fallback(sz=100):
        """Gray circular silhouette for unknown/no-portrait NPCs."""
        mask = "images/ui/activity_dot.png"
        sil  = "images/ui/portrait_silhouette.png"
        base = Transform(sil, size=(sz, sz)) if renpy.loadable(sil) else Solid("#3a3a5a", xysize=(sz, sz))
        return AlphaMask(base, Transform(mask, size=(sz, sz)))

    def npc_has_been_encountered(npc_id):
        """True once MC has had a real interaction with npc_id (safe for all NPC types)."""
        d = NPC_DATA.get(npc_id, {})
        if not d.get("world"):
            # Career/story NPCs: gated by their met flag
            mv = d.get("met")
            return bool(getattr(store, mv, False)) if mv else True
        # World NPCs: explicit met flag in NPC_DATA
        mv = d.get("met")
        if mv and getattr(store, mv, False):
            return True
        # Convention met flag: {npc_id}_met  (nora_met, marcus_met, zoe_met, etc.)
        if getattr(store, npc_id + "_met", False):
            return True
        # Phone contact = definitely met
        if npc_id in store.npc_contacts:
            return True
        # Positive affection = previous successful conversation
        aff_var = d.get("aff")
        if aff_var and getattr(store, aff_var, 0) > 0:
            return True
        # Migration-safe encounter dict
        return bool(store.npc_encountered.get(npc_id))

    def mark_npc_encountered(npc_id):
        enc = dict(store.npc_encountered)
        enc[npc_id] = True
        store.npc_encountered = enc

    def location_sprites():
        """All talkable NPCs at the current location, as (npc_id, sprite) pairs.
        Uses sprite_angry key if angry and available, else normal sprite."""
        result = []
        for nid in public_talkable_npcs_here():
            d = NPC_DATA[nid]
            if npc_is_angry(nid) and d.get("sprite_angry"):
                result.append((nid, d["sprite_angry"]))
            else:
                result.append((nid, d["sprite"]))
        return result

    # Pre-existing NPC-to-NPC relationships.
    NPC_RELATIONS = {
        ("marcus",   "sam"):      {"type": "gym_friends"},
        ("nora",     "kai"):      {"type": "regulars"},
        ("zoe",      "elle"):     {"type": "friends"},
        # Phase 44
        ("nora",     "elle"):     {"type": "cafe_familiarity"},
        ("lena",     "marcus"):   {"type": "bar_acquaintances"},
        ("sam",      "kai"):      {"type": "training_regulars"},
        ("caroline", "marcus"):   {"type": "thursday_regulars"},
    }

    def group_scene_check():
        """Returns (npc_a, npc_b) whenever two related NPCs are both talkable here."""
        for (a, b) in NPC_RELATIONS:
            if npc_talkable(a) and npc_talkable(b):
                return (a, b)
        return None

    def group_scene_label(gs):
        """'Name & Name' string for menu display."""
        return NPC_DATA[gs[0]]["name"] + " & " + NPC_DATA[gs[1]]["name"]

    # ── Group conversation helper ────────────────────────────────────────
    # Like do_talk but no time spend (caller handles it) and smaller gains
    # (split attention in a group).
    GROUP_REACT_TEXT = {
        "like":    "{name} lights up.",
        "dislike": "{name} doesn't bite.",
        "neutral": "{name} listens, nods.",
    }

    def _do_talk_group(npc_id, topic):
        _r = renpy.random   # renpy.random is an RNG instance, not an importable module
        d = NPC_DATA[npc_id]
        if topic in d.get("likes", []):
            delta, rtype = _r.randint(5, 10), "like"
        elif topic in d.get("dislikes", []):
            delta, rtype = _r.randint(-4, -1), "dislike"
        else:
            delta, rtype = _r.randint(2, 5), "neutral"
        _apply_aff(npc_id, delta)
        _td = dict(store._topics_today)
        _td.setdefault(npc_id, [])
        if topic not in _td[npc_id]:
            _td[npc_id] = _td[npc_id] + [topic]
        store._topics_today = _td
        return rtype

    def _do_talk_accounting(npc_id):
        spend_time(0.5)
        fs_record_social(npc_id, "talk")
        record_social_attention(npc_id, "talk")

    def do_talk(npc_id, topic):
        d = NPC_DATA[npc_id]
        _do_talk_accounting(npc_id)
        # resolve reaction
        if topic in d.get("likes", []):
            result, delta, pool = "like", 2, LIKE_LINES
        elif topic in d.get("dislikes", []):
            result, delta, pool = "dislike", -1, DISLIKE_LINES
        else:
            result, delta, pool = "neutral", 0, NEUTRAL_LINES
        # record discovery (permanent knowledge about this NPC)
        seen = dict(store._topics_seen.get(npc_id, {}))
        seen[topic] = result
        store._topics_seen[npc_id] = seen
        # social battery: 3+ days in a row on same topic → burnout, no gain
        streak = store._topic_streak.get(npc_id, {}).get(topic, 0)
        if streak >= 3:
            delta, pool = 0, BURNOUT_LINES
        # mark topic as used today
        today = list(store._topics_today.get(npc_id, []))
        if topic not in today:
            today.append(topic)
        store._topics_today[npc_id] = today
        _apply_aff(npc_id, delta)
        gain_aff(d["name"], delta)
        line = renpy.random.choice(pool) % TOPIC_LABEL[topic]
        renpy.say(getattr(store, d["say"]), line)

    # First-contact rebuffs (world characters only, before they know you).
    COLD_REBUFF = [
        "%s glances at you, then pointedly looks away. Not today.",
        "%s pretends not to hear you and drifts off.",
        "%s gives you a quick once-over and keeps walking.",
        "You start to say something - %s is already somewhere else. \"...\"",
    ]

    def cold_approach_ok(npc_id):
        """World strangers may brush you off on first contact. Higher Charisma +
        status = better odds. Once you've broken the ice (affection > 0), never again."""
        d = NPC_DATA[npc_id]
        if not d.get("world") or npc_aff(npc_id) > 0:
            return True
        chance = 45 + store.stat_chr * 2 + status_score() // 3
        if renpy.random.randint(1, 100) <= chance:
            _apply_aff(npc_id, 2)   # broke the ice
            return True
        return False

    GIFT_TYPES = {
        "book":    ("Book",    20, ["movies", "work", "ambition", "art"]),
        "sweets":  ("Sweets",  15, ["food", "nightlife"]),
        "gadget":  ("Gadget",  35, ["music", "movies", "work"]),
        "flowers": ("Flowers", 25, ["travel", "art", "nightlife"]),
    }
    GIFT_LIKE_LINES = {
        "book":    ["A book? Let me guess - you actually paid attention.", "Oh, this one's been on my list. How did you know?"],
        "sweets":  ["Don't tell me you remembered what I said about these.", "Okay, now I feel bad I didn't bring anything for you."],
        "gadget":  ["Okay, this is genuinely useful. Thank you.", "You didn't have to, but I'm very glad you did."],
        "flowers": ["These are beautiful. Seriously.", "You know exactly what you're doing, don't you?"],
    }
    GIFT_DISLIKE_LINES = {
        "book":    ["Oh, a book. That's... thoughtful.", "I'll find a shelf for it. Thanks."],
        "sweets":  ["Sweets? I'm not really a sugar person, but... thanks.", "I'll pass them on. Thank you though."],
        "gadget":  ["I don't really use these, but thanks for thinking of me.", "It's very... technical. I appreciate it."],
        "flowers": ["Flowers. That's sweet of you.", "They're lovely, really. Thank you."],
    }
    GIFT_NEUTRAL_LINES = {
        "book":    ["Oh, nice - thank you.", "That's a thoughtful thing to bring."],
        "sweets":  ["You didn't have to. These are great, thanks.", "Oh, a treat. Perfect timing."],
        "gadget":  ["This is cool, actually. Thanks.", "I wasn't expecting this. Thank you."],
        "flowers": ["These are lovely, thank you.", "That's really kind of you."],
    }

    # ── Hug profiles ──────────────────────────────────────────────────────

    # FIX 7: each profile has two failure keys:
    #   "low_affection" — returned when aff < min_aff (not close enough yet)
    #   "low_trust"     — returned when aff is ok but trust < min_trust (trust not there yet)
    HUG_PROFILES = {
        "martha": {
            "min_aff": 35, "min_trust": 30, "cooldown_days": 4,
            "first": "Martha pauses for a moment, then accepts — brief, controlled, and over quickly. It means something precisely because it's unlike her.",
            "warm":  "A short hug. Martha doesn't linger. Neither of you mentions it.",
            "repeat": "She accepts without surprise this time.",
            "too_soon": "She steps back slightly. \"Not right now.\"",
            "low_affection": "She acknowledges you with a nod. Not there yet.",
            "low_trust": "She gives you a look that means no, politely.",
            "aff_gain": 2, "trust_gain": 1, "repeat_gain": 0,
        },
        "nora": {
            "min_aff": 20, "min_trust": 15, "cooldown_days": 2,
            "first": "Nora hugs you back without making it a thing. Natural, brief, warm.",
            "warm":  "She hugs back and pulls away with a small smile. \"You're going to make that a habit, aren't you?\"",
            "repeat": "Nora leans in easily. Some people are just like that.",
            "too_soon": "She laughs. \"Give it a day.\"",
            "low_affection": "She smiles, a little surprised. \"We're not quite there yet.\"",
            "low_trust": "She smiles but takes a small step back.",
            "aff_gain": 3, "trust_gain": 1, "repeat_gain": 1,
        },
        "zoe": {
            "min_aff": 25, "min_trust": 20, "cooldown_days": 3,
            "first": "Zoe hugs you quickly, then immediately turns away to look at something across the street. \"Anyway.\"",
            "warm":  "She leans in for a second. When she steps back she's already looking elsewhere.",
            "repeat": "Quick, genuine, then immediately deflected.",
            "too_soon": "\"You're very enthusiastic today.\" She doesn't hug back.",
            "low_affection": "She gives you a look. Not hostile — just not yet.",
            "low_trust": "She raises an eyebrow. Doesn't move closer.",
            "aff_gain": 3, "trust_gain": 2, "repeat_gain": 1,
        },
        "eli": {
            "min_aff": 30, "min_trust": 25, "cooldown_days": 5,
            "first": "Eli hugs you back, a little stiffly at first, then relaxes. It's brief and slightly awkward in the best way.",
            "warm":  "They lean in. Still slightly awkward. Still genuine.",
            "repeat": "Less awkward this time. They don't comment on it.",
            "too_soon": "They look slightly uncertain. \"I'm okay. Thanks though.\"",
            "low_affection": "They look a bit startled. \"Oh — I, uh. Hi.\"",
            "low_trust": "They take a small step back. Not unfriendly — just not there yet.",
            "aff_gain": 3, "trust_gain": 2, "repeat_gain": 1,
        },
        "lena": {
            "min_aff": 35, "min_trust": 35, "cooldown_days": 4,
            "first": "Lena accepts the hug quietly — calm, steady, for exactly the right amount of time.",
            "warm":  "She holds for a moment longer than expected. Then: \"Thank you.\"",
            "repeat": "Calm and genuine. She seems to appreciate that you don't make it a performance.",
            "too_soon": "\"I'm all right.\" A gentle decline.",
            "low_affection": "She takes a small step back. Professional warmth, not personal.",
            "low_trust": "She nods but doesn't move closer.",
            "aff_gain": 2, "trust_gain": 2, "repeat_gain": 1,
        },
        "marcus": {
            "min_aff": 20, "min_trust": 15, "cooldown_days": 2,
            "first": "Marcus pulls you in for a proper hug. No ceremony. \"Good to have you around.\"",
            "warm":  "He claps you on the back. \"Yeah, yeah.\" He's smiling.",
            "repeat": "Easy and natural. Marcus is just like that.",
            "too_soon": "He laughs. \"Again? I just saw you.\"",
            "low_affection": "He raises an eyebrow. \"Bit early for that, isn't it?\"",
            "low_trust": "He's friendly but doesn't match the gesture.",
            "aff_gain": 3, "trust_gain": 1, "repeat_gain": 1,
        },
        "kai": {
            "min_aff": 25, "min_trust": 20, "cooldown_days": 3,
            "first": "Kai hugs you back, quick and genuine. \"Don't go soft on me,\" she says, then grins.",
            "warm":  "She leans in briefly. Back to business.",
            "repeat": "Natural and casual. No big deal.",
            "too_soon": "\"You're good.\" She doesn't close the distance.",
            "low_affection": "She tilts her head. \"We barely know each other.\"",
            "low_trust": "She smiles but doesn't reach back.",
            "aff_gain": 3, "trust_gain": 1, "repeat_gain": 1,
        },
        "natalie": {
            "min_aff": 35, "min_trust": 40, "cooldown_days": 6,
            "first": "Natalie goes very still for a moment. Then she accepts — briefly, arms not quite committing. When she steps back she says nothing, but her expression is different.",
            "warm":  "She's less surprised this time. Still brief.",
            "repeat": "She accepts. Still doesn't make it easy, but she accepts.",
            "too_soon": "She holds up one hand. \"Not right now.\"",
            "low_affection": "She looks at you flatly. \"What are you doing?\"",
            "low_trust": "She takes a half-step back. \"I'm fine.\"",
            "aff_gain": 2, "trust_gain": 3, "repeat_gain": 1,
        },
        "caroline": {
            "min_aff": 50, "min_trust": 45, "cooldown_days": 7,
            "first": "Caroline accepts, briefly and precisely. She seems mildly surprised at herself. \"Well. Okay then.\"",
            "warm":  "She doesn't step back. That's new.",
            "repeat": "She barely reacts, but she leans in slightly.",
            "too_soon": "\"I think we're not quite there.\" Perfectly polite refusal.",
            "low_affection": "She looks at you with mild amusement. \"Bold.\" She doesn't move.",
            "low_trust": "She smiles, takes a step back. \"Another time.\"",
            "aff_gain": 2, "trust_gain": 2, "repeat_gain": 0,
        },
        "elle": {
            "min_aff": 20, "min_trust": 15, "cooldown_days": 2,
            "first": "Elle hugs you back warmly. Easy and light.",
            "warm":  "Warm. She pulls back with a smile.",
            "repeat": "Elle hugs easily. It's just who she is.",
            "too_soon": "She laughs. \"Again so soon?\"",
            "low_affection": "She smiles. \"Oh — I, hi! Maybe next time.\"",
            "low_trust": "She smiles, but keeps some distance.",
            "aff_gain": 3, "trust_gain": 1, "repeat_gain": 1,
        },
        "sam": {
            "min_aff": 20, "min_trust": 15, "cooldown_days": 2,
            "first": "Sam hugs you back naturally. \"Good to have you around.\"",
            "warm":  "Easy and warm. Sam doesn't overthink it.",
            "repeat": "Natural, like it's always been this way.",
            "too_soon": "She shakes her head with a grin. \"Again already?\"",
            "low_affection": "She looks slightly caught off guard. \"Oh! We're doing that? Okay.\" She laughs but doesn't lean in.",
            "low_trust": "She smiles but keeps some space.",
            "aff_gain": 3, "trust_gain": 1, "repeat_gain": 1,
        },
    }

    # ── Escalating failure tracking ───────────────────────────────────────
    # ponytail: multiplier caps at 2× on the 3rd+ failure; lockout 3 days after
    # the 3rd consecutive rejection. Upgrade path: per-NPC configurable cap.

    def _apply_escalation(npc_id, action, base_aff_pen, base_trust_pen):
        count = store.failed_physical_attempts.get((npc_id, action), 0)
        if count == 0:
            multiplier = 1.0
        elif count == 1:
            multiplier = 1.5
        else:
            multiplier = 2.0
        _apply_aff(npc_id, int(base_aff_pen * multiplier))
        _apply_trust(npc_id, int(base_trust_pen * multiplier))
        new_count = count + 1
        _fa = dict(store.failed_physical_attempts)
        _fa[(npc_id, action)] = new_count
        store.failed_physical_attempts = _fa
        # 3rd+ failure: 3-day boundary lockout
        if count >= 2:
            _lb = dict(store.physical_boundary_lockout)
            _lb[(npc_id, action)] = store.day + 3
            store.physical_boundary_lockout = _lb

    def do_hug(npc_id):
        """Execute a hug interaction. Returns display text, applies stat effects.
        Side channel: sets store._last_hug_accepted so callers (e.g. the CG
        wrapper) can tell an accepted hug from a rejection/cooldown without
        changing the string return that ~15 tests + 2 scenes rely on."""
        store._last_hug_accepted = False
        hp = HUG_PROFILES.get(npc_id)
        if not hp or npc_id not in NPC_DATA:
            store._last_hug_accepted = True
            return "You share a brief hug."
        aff   = npc_aff(npc_id)
        trust = npc_trust(npc_id)
        last_hug_day = store.npc_last_hug_day.get(npc_id, -999)
        # Lockout check (3+ consecutive failures → 3-day cooldown)
        lockout_day = store.physical_boundary_lockout.get((npc_id, "hug"), -1)
        if store.day <= lockout_day:
            return hp.get("too_soon", "Not right now.")
        # FIX 7: separate failure texts — low_affection fires first (not close enough),
        # low_trust fires when aff is sufficient but trust is not yet there.
        if aff < hp["min_aff"]:
            _apply_escalation(npc_id, "hug",
                hp.get("aff_pen_low_aff", -2),
                hp.get("trust_pen_low_aff", -1))
            return hp.get("low_affection", hp["low_trust"])
        if trust < hp["min_trust"]:
            _apply_escalation(npc_id, "hug",
                hp.get("aff_pen_low_trust", -1),
                hp.get("trust_pen_low_trust", -3))
            return hp["low_trust"]
        # Cooldown active — no penalty, no failure increment
        if store.day - last_hug_day < hp["cooldown_days"]:
            _apply_aff(npc_id, hp.get("repeat_gain", 0))
            return hp["too_soon"]
        # Accepted — reset failure counter
        store._last_hug_accepted = True
        _fa = dict(store.failed_physical_attempts)
        _fa[(npc_id, "hug")] = 0
        store.failed_physical_attempts = _fa
        # First hug ever?
        is_first = not relationship_memory_exists(npc_id, "first_hug_" + npc_id)
        days_since = store.day - last_hug_day  # read before updating
        # Record and apply
        d = dict(store.npc_last_hug_day)
        d[npc_id] = store.day
        store.npc_last_hug_day = d
        if is_first:
            _apply_aff(npc_id, hp["aff_gain"])
            _apply_trust(npc_id, hp["trust_gain"])
            add_relationship_memory(npc_id, "first_hug_" + npc_id, "First hug")
            return hp["first"]
        else:
            _apply_aff(npc_id, hp.get("repeat_gain", 0))
            # warm_after_days defaults to 2× cooldown: waited longer than minimum → warm,
            # hugged at first opportunity → repeat.
            warm_threshold = hp.get("warm_after_days", hp["cooldown_days"] * 2)
            if days_since >= warm_threshold:
                return hp["warm"]
            return hp["repeat"]

    def record_forced_hug(npc_id, aff=None, trust=None):
        """A story-initiated hug (the NPC hugs the player as part of a scripted
        scene). Records the first-hug memory, cooldown, and stat gains WITHOUT
        re-running the consent gate — otherwise a scene that narrates the hug
        could immediately follow it with a rejection line. Defaults to the
        profile's first-hug gains when aff/trust are not given."""
        hp = HUG_PROFILES.get(npc_id, {})
        _d = dict(store.npc_last_hug_day)
        _d[npc_id] = store.day
        store.npc_last_hug_day = _d
        _fa = dict(store.failed_physical_attempts)
        _fa[(npc_id, "hug")] = 0
        store.failed_physical_attempts = _fa
        if npc_id in NPC_DATA:
            _apply_aff(npc_id, aff if aff is not None else hp.get("aff_gain", 4))
            _apply_trust(npc_id, trust if trust is not None else hp.get("trust_gain", 3))
        if not relationship_memory_exists(npc_id, "first_hug_" + npc_id):
            add_relationship_memory(npc_id, "first_hug_" + npc_id, "First hug")

    # ── Dates / outings (v2) ──────────────────────────────────────────────
    # Rewards scale down when you (a) repeat the same venue and (b) go out again
    # inside the cooldown, and scale up/down by whether the NPC likes the venue.
    # This stops the old "same three venues, flat +6/+3 forever" farm.
    DATE_COOLDOWN_DAYS = 4
    DATE_BASE_AFF   = 6
    DATE_BASE_TRUST = 3
    # venue → the NPC "likes"/"dislikes" tag it maps onto
    DATE_VENUE_TAG  = {"dinner": "food", "rooftop": "nightlife", "beach": "travel"}

    def date_outing_rewards(npc_id, venue):
        """(aff_gain, trust_gain, preference) for a date/outing.
        preference in {"preferred","neutral","disliked"} from NPC likes/dislikes.
        Diminishing returns per (npc, venue) repetition; flattened further when
        another outing happens inside DATE_COOLDOWN_DAYS."""
        d = NPC_DATA.get(npc_id, {})
        tag = DATE_VENUE_TAG.get(venue)
        if tag in d.get("likes", []):
            pref, mult = "preferred", 1.5
        elif tag in d.get("dislikes", []):
            pref, mult = "disliked", 0.5
        else:
            pref, mult = "neutral", 1.0
        n = store.npc_date_venue_count.get("%s|%s" % (npc_id, venue), 0)
        rep = 1.0 if n == 0 else (0.5 if n == 1 else 0.2)
        since = store.day - store.npc_last_date_day.get(npc_id, -999)
        cd = 0.4 if since < DATE_COOLDOWN_DAYS else 1.0
        aff = max(1, int(round(DATE_BASE_AFF   * mult * rep * cd)))
        tr  = max(0, int(round(DATE_BASE_TRUST * mult * rep * cd)))
        return aff, tr, pref

    def record_date_outing(npc_id, venue):
        key = "%s|%s" % (npc_id, venue)
        _c = dict(store.npc_date_venue_count)
        _c[key] = _c.get(key, 0) + 1
        store.npc_date_venue_count = _c
        _dd = dict(store.npc_last_date_day)
        _dd[npc_id] = store.day
        store.npc_last_date_day = _dd

    # ── Kiss profiles ─────────────────────────────────────────────────────
    # romance_flag: None = non-romanceable (kiss always romance_locked).
    # valid_contexts: locations where a kiss is contextually appropriate.
    # Default penalties: low_aff aff -7/tr -4; low_trust aff -4/tr -6;
    #   romance_locked aff -4/tr -3; wrong_context aff -1/tr 0.

    KISS_PROFILES = {
        "nora": {
            "min_aff": 45, "min_trust": 40, "cooldown_days": 3,
            "romance_flag": "nora_romance_unlocked",
            "valid_contexts": ["location_cafe", "location_bar"],
            "warm_after_days": 10,
            "first_kiss": "She goes still for just a moment. Then she kisses you back — brief, certain, and exactly right. When she pulls away she's looking at the counter. \"Well,\" she says. \"Okay then.\"",
            "repeat": "She kisses you back easily. Like it's been this way for a while.",
            "warm": "She pauses what she's doing and looks at you properly. The kiss is unhurried. \"You always show up at the right time,\" she says.",
            "too_soon": "She laughs softly. \"Give it a minute.\"",
            "low_affection": "She blinks. \"Whoa. We're not there yet.\" Not unkind — just honest.",
            "low_trust": "She steps back slightly, expression careful. \"Let's slow down.\"",
            "romance_locked":   "She tilts her head. \"What are you doing?\" There's a wall behind her eyes.",
            "romance_unopened": "She tilts her head. \"What are you doing?\" There's a wall behind her eyes.",
            "romance_friends":  "She shakes her head gently. \"We said we'd keep this simple. I haven't forgotten.\"",
            "romance_paused":   "She meets your eyes. \"Give it time. Okay?\"",
            "romance_closed":   "She steps back. Quietly. She doesn't reopen it.",
            "wrong_context": "She glances around. \"Not here. Not like this.\"",
            "aff_gain": 6, "trust_gain": 4, "repeat_gain": 2,
        },
        "marcus": {
            "min_aff": 30, "min_trust": 25, "cooldown_days": 3,
            "romance_flag": None,
            "valid_contexts": ["location_bar", "location_park", "location_nightclub"],
            "first_kiss": "", "repeat": "", "warm": "",
            "too_soon": "\"Easy there.\"",
            "low_affection": "He raises both eyebrows. \"Okay, where did that come from?\"",
            "low_trust": "He steps back, hands up. \"Nah, we're not doing that.\"",
            "romance_locked":     "Marcus gives you a look. \"Come on. Not like that.\"",
            "romance_unavailable": "He looks at you for a second. \"Not right now.\" No door closed, just not open.",
            "wrong_context": "\"Maybe not here, yeah?\"",
            "aff_gain": 0, "trust_gain": 0, "repeat_gain": 0,
        },
        "caroline": {
            "min_aff": 65, "min_trust": 60, "cooldown_days": 5,
            "romance_flag": "caroline_romance_unlocked",
            "valid_contexts": ["location_bar", "location_nightclub"],
            "warm_after_days": 14,
            "first_kiss": "She doesn't move for a moment after. Then: \"That was either brave or catastrophically stupid.\" She doesn't say which. But she doesn't leave.",
            "repeat": "Brief, controlled, and clearly intentional on her end.",
            "warm": "She kisses you first this time. Steps back like she didn't. \"Don't read into it.\"",
            "too_soon": "\"Patience.\" She doesn't elaborate.",
            "low_affection": "She gives you a look that could strip paint. \"Bold. Ill-advised.\"",
            "low_trust": "\"No.\" Flat. Final. No anger — just a closed door.",
            "romance_locked":   "She looks at you steadily. \"We work together. Pick your next words carefully.\"",
            "romance_unopened": "She looks at you steadily. \"We work together. Pick your next words carefully.\"",
            "romance_friends":  "\"We established what this is.\" She doesn't raise her voice. She doesn't need to.",
            "romance_paused":   "A brief glance. \"Not at the moment. Don't push it.\"",
            "romance_closed":   "She doesn't break eye contact. \"This conversation ends here.\"",
            "wrong_context": "She glances pointedly at the surroundings. \"Not at work. Are you serious?\"",
            "aff_gain": 7, "trust_gain": 5, "repeat_gain": 2,
            "aff_pen_low_aff": -8, "trust_pen_low_aff": -5,
            "aff_pen_low_trust": -5, "trust_pen_low_trust": -8,
            "aff_pen_romance_locked": -6, "trust_pen_romance_locked": -4,
        },
        "lena": {
            "min_aff": 55, "min_trust": 55, "cooldown_days": 4,
            "romance_flag": "lena_romance_unlocked",
            "valid_contexts": ["location_bar"],
            "warm_after_days": 12,
            "first_kiss": "She goes quiet after. Not uncomfortable — processing. \"I wasn't expecting that,\" she says finally. A pause. \"I'm glad it happened.\"",
            "repeat": "She kisses you back, calm and deliberate. Everything she does is like that.",
            "warm": "She leans in before you do. Just slightly. \"You know,\" she says quietly, \"this part of the day I actually look forward to.\"",
            "too_soon": "\"I'm still catching my breath from last time.\" A small smile.",
            "low_affection": "She takes a measured step back. \"I think we're moving too fast.\"",
            "low_trust": "Her expression doesn't change but her posture does. \"Not yet. I'm sorry.\"",
            "romance_locked":   "\"I like you. But not like that. Not right now.\" Clean, kind, and closed.",
            "romance_unopened": "\"I like you. But not like that. Not right now.\" Clean, kind, and closed.",
            "romance_friends":  "\"I thought we were clear on where things stand.\" Not harsh — just steady.",
            "romance_paused":   "\"I need a bit more space right now.\" She says it without breaking off the friendship.",
            "romance_closed":   "She's quiet for a moment. \"This is where it stays. I'm sorry.\"",
            "wrong_context": "She glances at the corridor. \"Not here. I'm still on shift.\"",
            "aff_gain": 6, "trust_gain": 5, "repeat_gain": 2,
            "aff_pen_low_aff": -7, "trust_pen_low_aff": -4,
            "aff_pen_low_trust": -4, "trust_pen_low_trust": -7,
        },
        "natalie": {
            "min_aff": 40, "min_trust": 40, "cooldown_days": 7,
            "romance_flag": None,
            "valid_contexts": ["location_bar"],
            "first_kiss": "", "repeat": "", "warm": "",
            "too_soon": "She holds up one hand. Stop.",
            "low_affection": "She stares at you. Then goes back to what she was doing.",
            "low_trust": "\"What exactly do you think this is?\"",
            "romance_locked": "\"No.\" She doesn't raise her voice. She doesn't have to.",
            "wrong_context": "\"Not at work. I will actually fire you.\"",
            "aff_gain": 0, "trust_gain": 0, "repeat_gain": 0,
            "aff_pen_low_aff": -8, "trust_pen_low_aff": -5,
            "aff_pen_low_trust": -5, "trust_pen_low_trust": -8,
        },
        "martha": {
            "min_aff": 50, "min_trust": 50, "cooldown_days": 7,
            "romance_flag": None,
            "valid_contexts": ["location_bar"],
            "too_soon": "She gives you a look that closes the topic.",
            "low_affection": "She turns back to her drink. You've been dismissed.",
            "low_trust": "A sharp glance. \"That's not something I'm interested in.\"",
            "romance_locked":   "\"Ambitious,\" she says. \"Wrong direction entirely.\"",
            "romance_unopened": "She looks at you. Then looks away. \"Not appropriate.\" Said without heat — just a line she's drawn.",
            "romance_friends":  "\"We've established where this stands.\" She says it precisely. No trace of anger.",
            "romance_paused":   "A brief measured look. \"Not now.\"",
            "romance_closed":   "She doesn't react beyond a slight stillness. \"This conversation ends here.\"",
            "first_kiss": "She goes very still. Not startled — processing. Then, carefully: \"That was a deliberate choice.\" A pause. \"So was this.\" She doesn't step away.",
            "repeat": "Brief and controlled. She initiates. Neither of you mentions it.",
            "warm": "She's the one who moves first this time. When she steps back: \"Don't read too much into the pattern.\" She sounds like she knows you will anyway.",
            "wrong_context": "\"At the office? Really?\" Said with the tone she reserves for very bad proposals.",
            "aff_gain": 6, "trust_gain": 5, "repeat_gain": 1,
            "aff_pen_low_aff": -7, "trust_pen_low_aff": -4,
            "aff_pen_low_trust": -4, "trust_pen_low_trust": -7,
            "aff_pen_romance_locked": -6, "trust_pen_romance_locked": -4,
            "warm_after_days": 21,
        },
        "elle": {
            "min_aff": 40, "min_trust": 35, "cooldown_days": 3,
            "romance_flag": "elle_romance_unlocked",
            "valid_contexts": ["location_beach", "location_sandbeach", "location_cafe", "location_bar", "location_nightclub"],
            "warm_after_days": 9,
            "first_kiss": "She laughs a little — surprise, not rejection. Then she kisses you back. When she pulls away she's looking at the horizon. \"Well. That was... yeah.\"",
            "repeat": "She kisses you back warmly. Light and easy.",
            "warm": "She closes the distance first. \"I missed you,\" she says after, like it's nothing.",
            "too_soon": "She laughs. \"You're very eager today.\"",
            "low_affection": "She smiles carefully. \"Oh — I don't think so. Not yet.\"",
            "low_trust": "She shakes her head gently. \"I really like you. But not yet.\"",
            "romance_locked":   "\"Hey.\" She takes a small step back. \"Can we just be this for now?\"",
            "romance_unopened": "\"Hey.\" She takes a small step back. \"Can we just be this for now?\"",
            "romance_friends":  "She shakes her head. \"I like us the way we are. Let's not complicate it.\"",
            "romance_paused":   "She smiles, but it doesn't quite reach. \"Not yet. I need a bit more time.\"",
            "romance_closed":   "She looks at you kindly. \"We're better as friends. I mean it.\"",
            "wrong_context": "She looks around, amused. \"Maybe somewhere a bit less... here?\"",
            "aff_gain": 6, "trust_gain": 4, "repeat_gain": 2,
        },
        "zoe": {
            "min_aff": 50, "min_trust": 45, "cooldown_days": 4,
            "romance_flag": "zoe_romance_unlocked",
            "valid_contexts": ["location_beach", "location_sandbeach", "location_park", "location_bar", "location_nightclub"],
            "warm_after_days": 12,
            "first_kiss": "She kisses you back, and then immediately steps away and looks at something in the middle distance. \"Okay,\" she says. \"Okay.\" And then nothing else for a while.",
            "repeat": "Quick and real. She's already looking away before it's over.",
            "warm": "She doesn't deflect this time. She leans into it. \"Don't make it weird,\" she says, which is how you know it already means something.",
            "too_soon": "\"You just kissed me, like, three days ago.\" She doesn't sound upset. Just noting it.",
            "low_affection": "She gives you a flat look. \"Hm. No.\"",
            "low_trust": "She takes a step back. Just one. Says nothing.",
            "romance_locked":   "She looks at you for a moment. Then away. \"I don't — we're not doing that.\"",
            "romance_unopened": "She looks at you for a moment. Then away. \"I don't — we're not doing that.\"",
            "romance_friends":  "She tilts her chin. \"We talked about this. I said where we are.\"",
            "romance_paused":   "She puts two fingers on your shoulder. Stops you. Says nothing.",
            "romance_closed":   "\"I need you to hear me. We're not going there.\" She's not angry. It's just closed.",
            "wrong_context": "She glances around. \"Not exactly the vibe, is it.\"",
            "aff_gain": 6, "trust_gain": 5, "repeat_gain": 2,
            "aff_pen_low_aff": -7, "trust_pen_low_aff": -4,
            "aff_pen_low_trust": -4, "trust_pen_low_trust": -6,
        },
        "sam": {
            "min_aff": 30, "min_trust": 25, "cooldown_days": 3,
            "romance_flag": None,
            "valid_contexts": ["location_park", "location_gym", "location_bar"],
            "first_kiss": "", "repeat": "", "warm": "",
            "too_soon": "She steps back, eyebrows up. \"Whoa, hey.\"",
            "low_affection": "She blinks. \"Oh — no, we're not — no. Sorry.\"",
            "low_trust": "She puts a hand on your arm. Stops you. \"We're friends. Okay?\"",
            "romance_locked":     "\"I don't think of you that way. Sorry.\" Genuinely kind about it.",
            "romance_unavailable": "She tilts her head. \"I don't know what that was, but not yet.\" Not a no.",
            "wrong_context": "\"Not at the gym, please.\" She laughs a little.",
            "aff_gain": 0, "trust_gain": 0, "repeat_gain": 0,
        },
        "eli": {
            "min_aff": 30, "min_trust": 25, "cooldown_days": 5,
            "romance_flag": None,
            "valid_contexts": ["location_bar", "location_library"],
            "first_kiss": "", "repeat": "", "warm": "",
            "too_soon": "They lean back slightly. \"Uh — I'm fine, thanks.\"",
            "low_affection": "They look alarmed. \"I — what? No. Sorry.\"",
            "low_trust": "They go very still. \"Please don't do that.\"",
            "romance_locked": "\"I — yeah, that's not something I'm into. Like, at all. Sorry.\" They look genuinely uncomfortable.",
            "wrong_context": "They gesture at the surroundings. \"In the library? There are people here.\"",
            "aff_gain": 0, "trust_gain": 0, "repeat_gain": 0,
        },
        "kai": {
            "min_aff": 30, "min_trust": 25, "cooldown_days": 3,
            "romance_flag": None,
            "valid_contexts": ["location_beach", "location_sandbeach", "location_bar", "location_nightclub"],
            "first_kiss": "", "repeat": "", "warm": "",
            "too_soon": "She puts a hand on your chest. Stops you. Shakes her head.",
            "low_affection": "She tilts her head back. \"Huh. No.\"",
            "low_trust": "\"Not happening.\" Friendly, but final.",
            "romance_locked":     "\"Hey, you're great. But this?\" She shakes her head. \"Not what we are.\"",
            "romance_unavailable": "She goes quiet for a moment. \"Maybe another version of this. Not right now.\"",
            "wrong_context": "She looks around. \"There's a whole beach. Pick your moment better.\"",
            "aff_gain": 0, "trust_gain": 0, "repeat_gain": 0,
        },
    }

    # ── Romance state architecture ─────────────────────────────────────────
    # Valid states: unopened | friends | interested | dating | committed | paused | closed
    # Non-romanceable NPCs are not in ROMANCE_PROFILES; do_kiss always returns romance_locked for them.

    ROMANCE_PROFILES = {
        "nora": {
            "min_aff_open": 45, "min_trust_open": 40, "momentum_to_reopen": 30,
            "legacy_flag": "nora_romance_unlocked",
        },
        "elle": {
            "min_aff_open": 40, "min_trust_open": 35, "momentum_to_reopen": 25,
            "legacy_flag": "elle_romance_unlocked",
        },
        "zoe": {
            "min_aff_open": 50, "min_trust_open": 45, "momentum_to_reopen": 35,
            "legacy_flag": "zoe_romance_unlocked",
        },
        "caroline": {
            "min_aff_open": 65, "min_trust_open": 60, "momentum_to_reopen": 40,
            "legacy_flag": "caroline_romance_unlocked",
        },
        "lena": {
            "min_aff_open": 55, "min_trust_open": 55, "momentum_to_reopen": 35,
            "legacy_flag": "lena_romance_unlocked",
        },
        "martha": {
            "min_aff_open": 65, "min_trust_open": 65, "momentum_to_reopen": 45,
            # no legacy_flag — Martha was never in the old boolean system
        },
    }

    # Which non-romanceable NPCs are intentionally disabled vs. planned future content.
    # Does not affect gameplay — documents design intent so kiss text can be written accordingly.
    ROMANCE_AVAILABILITY = {
        "marcus":  "planned",
        "kai":     "planned",
        "sam":     "planned",
        "eli":     "disabled",
        "natalie": "disabled",
    }

    # Phase 6B — per-NPC social personality profiles
    # jealousy: "none" | "low" | "medium" | "high"
    # jealousy_unlock: store variable name (str) that must be True; None = always unlocked
    # jealousy_threshold: tension required to set pending; None = never fires
    NPC_SOCIAL_PROFILES = {
        "marcus":   {"social_openness": "high",   "initiative": "high",   "jealousy": "none",   "jealousy_unlock": None,                "jealousy_threshold": None, "jealousy_cooldown": None, "trust_sensitivity": "medium", "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "direct",       "romance_scope": "friendship_only"},
        "rena":     {"social_openness": "medium",  "initiative": "low",    "jealousy": "none",   "jealousy_unlock": None,                "jealousy_threshold": None, "jealousy_cooldown": None, "trust_sensitivity": "high",   "forgiveness": "low",    "status_sensitivity": "medium", "conflict_style": "professional", "romance_scope": "friendship_only"},
        "nora":     {"social_openness": "high",   "initiative": "high",   "jealousy": "medium", "jealousy_unlock": "nora_bad_day_done", "jealousy_threshold": 10,   "jealousy_cooldown": 7,    "trust_sensitivity": "medium", "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "gentle",       "romance_scope": "romanceable"},
        "martha":   {"social_openness": "low",    "initiative": "low",    "jealousy": "low",    "jealousy_unlock": "martha_corridor_done", "jealousy_threshold": 7, "jealousy_cooldown": 7,    "trust_sensitivity": "high",   "forgiveness": "low",    "status_sensitivity": "high",   "conflict_style": "indirect",     "romance_scope": "romanceable"},
        "lena":     {"social_openness": "medium",  "initiative": "medium", "jealousy": "low",    "jealousy_unlock": None,                "jealousy_threshold": 15,   "jealousy_cooldown": 7,    "trust_sensitivity": "medium", "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "analytical",   "romance_scope": "romanceable"},
        "natalie":  {"social_openness": "high",   "initiative": "high",   "jealousy": "none",   "jealousy_unlock": None,                "jealousy_threshold": None, "jealousy_cooldown": None, "trust_sensitivity": "low",    "forgiveness": "high",   "status_sensitivity": "low",    "conflict_style": "expressive",   "romance_scope": "friendship_only"},
        "elle":     {"social_openness": "high",   "initiative": "high",   "jealousy": "medium", "jealousy_unlock": None,                "jealousy_threshold": 10,   "jealousy_cooldown": 7,    "trust_sensitivity": "low",    "forgiveness": "high",   "status_sensitivity": "high",   "conflict_style": "expressive",   "romance_scope": "romanceable"},
        "caroline": {"social_openness": "medium",  "initiative": "medium", "jealousy": "medium", "jealousy_unlock": None,                "jealousy_threshold": 10,   "jealousy_cooldown": 7,    "trust_sensitivity": "high",   "forgiveness": "medium", "status_sensitivity": "medium", "conflict_style": "composed",     "romance_scope": "romanceable"},
        "zoe":      {"social_openness": "low",    "initiative": "medium", "jealousy": "high",   "jealousy_unlock": "zoe_rain_done",     "jealousy_threshold": 6,    "jealousy_cooldown": 5,    "trust_sensitivity": "high",   "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "deflection",   "romance_scope": "romanceable"},
        "eli":      {"social_openness": "medium",  "initiative": "low",    "jealousy": "medium", "jealousy_unlock": "eli_deploy_hug_done", "jealousy_threshold": 7, "jealousy_cooldown": 6,    "trust_sensitivity": "medium", "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "professional", "romance_scope": "friendship_only"},
        "sam":      {"social_openness": "high",   "initiative": "high",   "jealousy": "none",   "jealousy_unlock": None,                "jealousy_threshold": None, "jealousy_cooldown": None, "trust_sensitivity": "low",    "forgiveness": "high",   "status_sensitivity": "low",    "conflict_style": "direct",       "romance_scope": "friendship_only"},
        "kai":      {"social_openness": "medium",  "initiative": "medium", "jealousy": "none",   "jealousy_unlock": None,                "jealousy_threshold": None, "jealousy_cooldown": None, "trust_sensitivity": "medium", "forgiveness": "medium", "status_sensitivity": "low",    "conflict_style": "encouraging",  "romance_scope": "friendship_only"},
    }

    def npc_social_profile(npc_id):
        return NPC_SOCIAL_PROFILES.get(npc_id, {})

    def npc_social_trait(npc_id, trait, fallback=None):
        return NPC_SOCIAL_PROFILES.get(npc_id, {}).get(trait, fallback)

    # NPCs with implemented jealousy conversations this phase
    _JEALOUSY_IMPLEMENTED = frozenset({"zoe", "nora", "martha", "eli"})
    # Per-NPC done flags; completed first notices must not create unusable pending
    _JEALOUSY_FIRST_NOTICE_DONE_FLAGS = {
        "zoe":    "zoe_jealousy_first_notice_done",
        "nora":   "nora_jealousy_first_notice_done",
        "martha": "martha_jealousy_first_notice_done",
        "eli":    "eli_jealousy_first_notice_done",
    }
    # tension delta table: action_type -> base attention points
    # hug excluded: non-romantic in this phase, creates no jealousy tension
    _SOCIAL_ATT_BASE = {"talk": 1, "gift": 1, "kiss": 5, "date": 3, "flirt": 3}

    def _social_tension_delta(base, jealousy_level):
        if jealousy_level == "low":
            return base // 2
        if jealousy_level == "high":
            return (base * 3 + 1) // 2   # ceiling of 150%
        return base  # medium

    def record_social_attention(target_npc_id, action_type):
        """Accumulate jealousy tension on NPCs observing the interaction.
        Only converts tension to a pending conversation for _JEALOUSY_IMPLEMENTED NPCs."""
        base = _SOCIAL_ATT_BASE.get(action_type, 0)
        if base == 0:
            return
        is_romantic = action_type in ("kiss", "flirt", "date")
        # friendship-only targets + non-romantic action → no observer jealousy
        if not is_romantic and target_npc_id not in ROMANCE_PROFILES:
            return
        tension  = dict(store.npc_jealousy_tension)
        pending  = dict(store.npc_jealousy_pending)
        last_day = dict(store.npc_jealousy_last_day)
        attention = dict(store.npc_social_attention)
        changed = False
        for nid, profile in NPC_SOCIAL_PROFILES.items():
            if nid == target_npc_id:
                continue
            if profile["jealousy"] == "none":
                continue
            if not npc_here(nid):
                continue
            # friendship-only observers don't react to non-romantic actions
            if profile["romance_scope"] == "friendship_only" and not is_romantic:
                continue
            # jealousy_unlock must be satisfied
            unlock = profile["jealousy_unlock"]
            if unlock and not getattr(store, unlock, False):
                continue
            # per-NPC cooldown gap since last resolved jealousy
            cooldown = profile["jealousy_cooldown"] or 5
            if (store.day - last_day.get(nid, -999)) < cooldown:
                continue
            # do not overwrite an existing pending reaction (wait for it to resolve)
            if nid in pending:
                continue
            delta = _social_tension_delta(base, profile["jealousy"])
            if delta == 0:
                continue
            tension[nid] = tension.get(nid, 0) + delta
            attention[nid] = attention.get(nid, 0) + delta
            changed = True
            thresh = profile["jealousy_threshold"]
            if thresh is not None and nid in _JEALOUSY_IMPLEMENTED and tension[nid] >= thresh:
                done_flag = _JEALOUSY_FIRST_NOTICE_DONE_FLAGS.get(nid)
                if done_flag and getattr(store, done_flag, False):
                    tension[nid] = thresh - 1  # cap: no repeat dialogue yet
                else:
                    pending[nid] = {"target": target_npc_id, "action": action_type, "day": store.day}
                    tension[nid] = max(0, tension[nid] - thresh)
        if changed:
            store.npc_jealousy_tension  = tension
            store.npc_jealousy_pending  = pending
            store.npc_social_attention  = attention

    _VALID_ROMANCE_STATES = frozenset(
        ("unopened", "friends", "interested", "dating", "committed", "paused", "closed")
    )

    def get_romance_state(npc_id):
        return store.romance_states.get(npc_id, "unopened")

    def set_romance_state(npc_id, state, source=None):
        if state not in _VALID_ROMANCE_STATES:
            renpy.log("set_romance_state: invalid state %r for %s — ignored" % (state, npc_id))
            return
        _prev = get_romance_state(npc_id)
        _rs = dict(store.romance_states)
        _rs[npc_id] = state
        store.romance_states = _rs
        if source is not None:
            _rc = dict(store.romance_previous_choice)
            _rc[npc_id] = source
            store.romance_previous_choice = _rc
            _rd = dict(store.romance_last_choice_day)
            _rd[npc_id] = store.day
            store.romance_last_choice_day = _rd
            _rm = dict(store.romance_route_memories)
            _rm[npc_id] = list(_rm.get(npc_id, [])) + [
                {"from": _prev, "to": state, "source": source, "day": store.day}
            ]
            store.romance_route_memories = _rm

    def get_romance_momentum(npc_id):
        return store.romance_momentum.get(npc_id, 0)

    def add_romance_momentum(npc_id, amount, source=None):
        _m = dict(store.romance_momentum)
        _m[npc_id] = max(0, min(100, _m.get(npc_id, 0) + amount))
        store.romance_momentum = _m

    def romance_is_open(npc_id):
        return get_romance_state(npc_id) in ("interested", "dating", "committed")

    def romance_can_be_reopened(npc_id):
        _s = get_romance_state(npc_id)
        if _s == "closed":
            return False
        if _s == "paused":
            return store.day > store.romance_pause_until_day.get(npc_id, -1)
        return True

    def pause_romance(npc_id, days, source=None):
        set_romance_state(npc_id, "paused", source=source)
        _rp = dict(store.romance_pause_until_day)
        _rp[npc_id] = store.day + days
        store.romance_pause_until_day = _rp

    def refresh_romance_pause(npc_id):
        if get_romance_state(npc_id) != "paused":
            return
        if store.day <= store.romance_pause_until_day.get(npc_id, -1):
            return
        # Recover to the pre-pause state (friends or unopened); never auto-recover to interested+
        _prev = "unopened"
        for _entry in reversed(store.romance_route_memories.get(npc_id, [])):
            if _entry.get("to") == "paused" and _entry.get("from") in ("unopened", "friends"):
                _prev = _entry["from"]
                break
        _rs = dict(store.romance_states)
        _rs[npc_id] = _prev
        store.romance_states = _rs

    def permanently_close_romance(npc_id, source=None):
        set_romance_state(npc_id, "closed", source=source)
        _rpc = dict(store.romance_permanent_closed)
        _rpc[npc_id] = True
        store.romance_permanent_closed = _rpc

    def can_offer_romance_reopen(npc_id):
        if not romance_can_be_reopened(npc_id):
            return False
        if get_romance_state(npc_id) not in ("unopened", "friends"):
            return False
        rp = ROMANCE_PROFILES.get(npc_id)
        if not rp:
            return False
        return (get_romance_momentum(npc_id) >= rp["momentum_to_reopen"]
                and npc_aff(npc_id) >= rp["min_aff_open"]
                and npc_trust(npc_id) >= rp["min_trust_open"])

    def legacy_romance_unlocked(npc_id):
        rp = ROMANCE_PROFILES.get(npc_id)
        if not rp:
            return False
        flag = rp.get("legacy_flag")
        if not flag:
            return False
        return getattr(store, flag, False)

    def sync_legacy_romance_flags(npc_id):
        """Lazy migration: if the old bool is True and no new state exists, set 'interested'."""
        if npc_id in store.romance_states:
            return
        if legacy_romance_unlocked(npc_id):
            _rs = dict(store.romance_states)
            _rs[npc_id] = "interested"
            store.romance_states = _rs

    def do_kiss(npc_id):
        """Execute a kiss attempt. Returns (outcome_key, display_text).
        outcome_key: low_affection | low_trust | romance_locked | romance_unopened
                     | romance_friends | romance_paused | romance_closed
                     | wrong_context | too_soon | first_kiss | repeat | warm"""
        kp = KISS_PROFILES.get(npc_id)
        if not kp:
            return ("low_affection", "This doesn't feel right.")
        aff   = npc_aff(npc_id)
        trust = npc_trust(npc_id)
        # Lockout check (3+ consecutive failures → 3-day cooldown)
        lockout_day = store.physical_boundary_lockout.get((npc_id, "kiss"), -1)
        if store.day <= lockout_day:
            return ("too_soon", kp.get("too_soon", "Not right now."))
        # Affection gate
        if aff < kp["min_aff"]:
            _apply_escalation(npc_id, "kiss",
                kp.get("aff_pen_low_aff", -7),
                kp.get("trust_pen_low_aff", -4))
            return ("low_affection", kp.get("low_affection", "This doesn't feel right."))
        # Trust gate
        if trust < kp["min_trust"]:
            _apply_escalation(npc_id, "kiss",
                kp.get("aff_pen_low_trust", -4),
                kp.get("trust_pen_low_trust", -6))
            return ("low_trust", kp.get("low_trust", "She pulls back."))
        # Romance gate — ROMANCE_PROFILES is the single source of romanceability
        if npc_id not in ROMANCE_PROFILES:
            _avail = ROMANCE_AVAILABILITY.get(npc_id, "disabled")
            if _avail == "planned":
                # Content not yet written — zero penalties, no escalation, no momentum change
                return ("romance_unavailable", kp.get("romance_unavailable", "That moment isn't there yet."))
            # disabled — permanent, apply full escalation
            _apply_escalation(npc_id, "kiss",
                kp.get("aff_pen_romance_locked", -4),
                kp.get("trust_pen_romance_locked", -3))
            return ("romance_locked", kp.get("romance_locked", "That's not where this is going."))
        # Romanceable NPC — use state architecture (lazy-migrate legacy bool first)
        sync_legacy_romance_flags(npc_id)
        refresh_romance_pause(npc_id)
        _rs = get_romance_state(npc_id)
        if _rs == "closed":
            return ("romance_closed", kp.get("romance_closed", "That's not something that can happen."))
        if _rs == "paused":
            return ("romance_paused", kp.get("romance_paused", kp.get("too_soon", "Not right now.")))
        if not romance_is_open(npc_id):
            if _rs == "friends":
                # Graduated escalation — friendship route must stay reopenable, but repeated violations escalate
                # ponytail: O(n) dict read; upgrade to persistent counter if tracking > 10 NPCs becomes expensive
                _fc = store.failed_physical_attempts.get((npc_id, "kiss"), 0)
                if _fc == 0:
                    _apply_aff(npc_id, kp.get("aff_pen_romance_friends", -1))
                elif _fc == 1:
                    _apply_aff(npc_id, -2)
                    _apply_trust(npc_id, -1)
                else:
                    _apply_aff(npc_id, -3)
                    _apply_trust(npc_id, -3)
                    pause_romance(npc_id, 14, source="boundary_violation_friends")
                _fa2 = dict(store.failed_physical_attempts)
                _fa2[(npc_id, "kiss")] = _fc + 1
                store.failed_physical_attempts = _fa2
                return ("romance_friends", kp.get("romance_friends", kp.get("romance_locked", "That's not where this is going.")))
            # unopened: light escalation + drain momentum
            _apply_escalation(npc_id, "kiss",
                kp.get("aff_pen_romance_unopened", -2),
                kp.get("trust_pen_romance_unopened", -1))
            add_romance_momentum(npc_id, -5, source="kiss_too_early")
            return ("romance_unopened", kp.get("romance_unopened", kp.get("romance_locked", "That's not where this is going.")))
        # Context gate (no failure escalation — just a light nudge)
        valid_contexts = kp.get("valid_contexts", [])
        if valid_contexts and store.current_loc not in valid_contexts:
            _apply_aff(npc_id, kp.get("aff_pen_wrong_context", -1))
            _tr_pen = kp.get("trust_pen_wrong_context", 0)
            if _tr_pen != 0:
                _apply_trust(npc_id, _tr_pen)
            return ("wrong_context", kp.get("wrong_context", "This isn't the right moment."))
        # Cooldown gate — no penalty, no failure increment
        last_kiss_day = store.npc_last_kiss_day.get(npc_id, -999)
        if store.day - last_kiss_day < kp["cooldown_days"]:
            return ("too_soon", kp.get("too_soon", "Not yet."))
        # Accepted — reset failure counter, record day
        _fa = dict(store.failed_physical_attempts)
        _fa[(npc_id, "kiss")] = 0
        store.failed_physical_attempts = _fa
        _lk = dict(store.npc_last_kiss_day)
        _lk[npc_id] = store.day
        store.npc_last_kiss_day = _lk
        # First kiss?
        if not relationship_memory_exists(npc_id, "first_kiss_" + npc_id):
            add_relationship_memory(npc_id, "first_kiss_" + npc_id, "First kiss")
            _apply_aff(npc_id, kp.get("aff_gain", 5))
            _apply_trust(npc_id, kp.get("trust_gain", 3))
            # State progression: a first kiss moves an open romance from
            # "interested" to "dating". "dating"/"committed" stay as-is (no demotion).
            if get_romance_state(npc_id) == "interested":
                set_romance_state(npc_id, "dating", source="first_kiss")
            return ("first_kiss", kp.get("first_kiss", "A first kiss."))
        # Repeat / warm
        days_since = store.day - last_kiss_day
        warm_threshold = kp.get("warm_after_days", kp["cooldown_days"] * 2)
        _apply_aff(npc_id, kp.get("repeat_gain", 1))
        if days_since >= warm_threshold:
            return ("warm", kp.get("warm", "A warm, familiar kiss."))
        return ("repeat", kp.get("repeat", "She kisses you back."))

    def gift_count_for(npc_id):
        return sum(1 for g in store.gift_log if g.get("npc_id") == npc_id)

    def do_gift(npc_id, gift_type):
        if store.gifts.get(gift_type, 0) <= 0:
            return
        store.gifts[gift_type] -= 1
        _gl = list(store.gift_log)
        _gl.append({"npc_id": npc_id, "gift_type": gift_type, "day": store.day})
        store.gift_log = _gl
        d = NPC_DATA[npc_id]
        interests = GIFT_TYPES[gift_type][2]
        likes     = d.get("likes", [])
        dislikes  = d.get("dislikes", [])
        if any(i in likes for i in interests):
            # diminishing returns: track (week_index, count) per NPC
            gw   = store.npc_gift_week.get(npc_id, (-1, 0))
            week = store.day // 7
            if gw[0] != week:
                gw = (week, 0)
            count = gw[1]
            if count == 0:
                delta = 5
                line = renpy.random.choice(GIFT_LIKE_LINES[gift_type])
            elif count == 1:
                delta = 2
                line = renpy.random.choice(GIFT_NEUTRAL_LINES[gift_type])
            else:
                delta = 0
                line = "You can tell she's been here before."
            ngw = dict(store.npc_gift_week)
            ngw[npc_id] = (week, count + 1)
            store.npc_gift_week = ngw
        elif any(i in dislikes for i in interests):
            delta = 1
            line = renpy.random.choice(GIFT_DISLIKE_LINES[gift_type])
        else:
            delta = 3
            line = renpy.random.choice(GIFT_NEUTRAL_LINES[gift_type])
        if delta > 0:
            _apply_aff(npc_id, delta)
            gain_aff(d["name"], delta)
        record_social_attention(npc_id, "gift")
        # Martha gift accusation — set pending on exactly the 3rd gift.
        # gift_log already includes the current gift so count == 3 means this IS the 3rd.
        # ponytail: == 3 prevents re-trigger on 4th+ gifts.
        if (npc_id == "martha"
                and gift_count_for("martha") == 3
                and not store.martha_gift_accusation_done
                and store.martha_gift_scene_pending is None):
            _gc = gift_count_for("martha")
            store.martha_gift_scene_pending = {
                "trigger_day":      store.day,
                "gift_id":          gift_type,
                "gift_name":        GIFT_TYPES[gift_type][0],
                "gift_count":       _gc,
                "trigger_location": store.current_loc,
                "variant":          "immediate",
            }
        renpy.say(getattr(store, d["say"]), line)


# ── Relationship panel (right, under the topbar) ───────────────────────
# _rb_prev_* are set to -1 by npc_interact on entry so the first render never
# flashes; a gain flips the fill to a bright colour for FLASH_LEN seconds.
define FLASH_LEN = 0.9

transform _rel_label_float:
    alpha 1.0 yoffset 0
    linear 0.9 alpha 0.0 yoffset -20

default _rb_prev_aff = -1
default _topics_seen    = {}   # {npc_id: {topic: "like"|"dislike"|"neutral"}}
default _topics_today   = {}   # {npc_id: [topics]} — cleared in new_day()
default _topic_streak   = {}   # {npc_id: {topic: consecutive_days}}
default npc_last_seen   = {}   # {npc_id: day} — updated on every npc_interact entry
default _rb_prev_tr = -1
default _rb_flash_aff = 0.0
default _rb_flash_tr = 0.0

screen npc_relbar(npc_id):
    zorder 25
    $ _aff = npc_aff(npc_id)
    $ _tr = npc_trust(npc_id)
    $ _tier = rel_tier(_aff)
    $ _nm = NPC_DATA[npc_id]["name"]

    # arm a colour flash whenever a value climbs since the last render
    if _rb_prev_aff >= 0 and _aff > _rb_prev_aff:
        $ _rb_flash_aff = _time.time()
    if _rb_prev_tr >= 0 and _tr > _rb_prev_tr:
        $ _rb_flash_tr = _time.time()
    if _rb_prev_aff >= 0 and _aff < _rb_prev_aff:
        $ _rb_flash_aff_neg = _time.time()
    if _rb_prev_tr >= 0 and _tr < _rb_prev_tr:
        $ _rb_flash_tr_neg = _time.time()
    $ _rb_prev_aff = _aff
    $ _rb_prev_tr = _tr
    $ _aff_hot = (_time.time() - _rb_flash_aff) < FLASH_LEN
    $ _tr_hot = (_time.time() - _rb_flash_tr) < FLASH_LEN
    $ _aff_hot_neg = (_time.time() - _rb_flash_aff_neg) < FLASH_LEN
    $ _tr_hot_neg = (_time.time() - _rb_flash_tr_neg) < FLASH_LEN
    # keep re-rendering so the flash window can close on its own
    # ponytail: always-on 15fps tick; fine for the single relbar shown in-chat
    timer 0.06 repeat True action NullAction()

    $ _portrait_path = "images/ui/icons/%s.png" % NPC_DATA[npc_id].get("portrait", "")
    $ _has_portrait  = bool(NPC_DATA[npc_id].get("portrait")) and renpy.loadable(_portrait_path)

    frame:
        xpos 1260
        ypos 150
        xsize 400
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 20)
        vbox:
            spacing 10
            # portrait + name row
            hbox:
                spacing 16
                if _has_portrait:
                    add portrait_circle(npc_id, 90)
                vbox:
                    spacing 4
                    yalign 0.5
                    text "[_nm]" font PROFILE_FONT size 28 color "#ffffff"
                    text "[_tier]" font PROFILE_FONT size 15 color "#9fb6d6"
            null height 4
            fixed:
                xsize 356
                ysize 30
                text "Affection" font PROFILE_FONT size 17 color "#cfe0f5" xpos 0 ypos 4
                # negative half (110–184): right_bar grows leftward from center as _aff < 0
                bar:
                    xpos 110 ypos 7
                    value AnimatedValue(100 + _aff, 100, delay=FLASH_LEN)
                    xsize 74 ysize 16
                    left_bar Frame("images/ui/bar_track.png", 14, 0) right_bar ("#e86a55" if _aff_hot_neg else Frame("images/ui/bar_fill_chr.png", 14, 0)) thumb Null()
                # neutral midpoint marker
                frame:
                    xpos 184 ypos 7
                    xsize 2 ysize 16
                    padding (0, 0, 0, 0)
                    background "#ffffff50"
                # positive half (186–260): left_bar grows rightward from center as _aff > 0
                bar:
                    xpos 186 ypos 7
                    value AnimatedValue(max(0, _aff), 100, delay=FLASH_LEN)
                    xsize 74 ysize 16
                    left_bar ("#ffd76a" if _aff_hot else Frame("images/ui/bar_fill_chr.png", 14, 0)) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_aff]" font PROFILE_FONT size 17 color ("#ffd76a" if _aff_hot else ("#e86a55" if _aff_hot_neg else "#ffffff")) xpos 270 ypos 4
                if (_aff_hot or _aff_hot_neg) and _rel_feedback_aff != 0:
                    $ _aff_fb_str = ("+%d" % _rel_feedback_aff) if _rel_feedback_aff > 0 else ("%d" % _rel_feedback_aff)
                    $ _aff_fb_col = "#ffd76a" if _rel_feedback_aff > 0 else "#e86a55"
                    text _aff_fb_str at _rel_label_float font ACT_FONT size 14 color _aff_fb_col xpos 310 ypos -4
            fixed:
                xsize 356
                ysize 30
                text "Trust" font PROFILE_FONT size 17 color "#cfe0f5" xpos 0 ypos 4
                bar:
                    xpos 110 ypos 7
                    value AnimatedValue(_tr, 100, delay=FLASH_LEN)
                    xsize 150 ysize 16
                    left_bar ("#7fe0ff" if _tr_hot else Frame("images/ui/bar_fill_int.png", 14, 0)) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_tr]" font PROFILE_FONT size 17 color ("#7fe0ff" if _tr_hot else "#ffffff") xpos 270 ypos 4
                if (_tr_hot or _tr_hot_neg) and _rel_feedback_tr != 0:
                    $ _tr_fb_str = ("+%d" % _rel_feedback_tr) if _rel_feedback_tr > 0 else ("%d" % _rel_feedback_tr)
                    $ _tr_fb_col = "#7fe0ff" if _rel_feedback_tr > 0 else "#e86a55"
                    text _tr_fb_str at _rel_label_float font ACT_FONT size 14 color _tr_fb_col xpos 310 ypos -4


# ── Main action bar (bottom) — icon tiles ──────────────────────────────
screen npc_actions(npc_id):
    zorder 22
    $ _gift_ok   = sum(gifts.values()) > 0
    $ _date_ok   = npc_aff(npc_id) >= 30
    $ _num_ok    = npc_aff(npc_id) >= 25 and npc_id not in npc_contacts
    $ _angry     = npc_is_angry(npc_id)
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (18, 14, 18, 14)
        vbox:
            spacing 4
            if _angry:
                $ _angry_hint = "You need a shower first." if need_hygiene < 30 else (NPC_DATA[npc_id]["name"] + " is upset with you.")
                text "[_angry_hint]" font ACT_FONT size 13 color "#e86a55" xalign 0.5
            hbox:
                spacing 16
                for _icon, _lbl, _ret, _ok in [
                        ("act_talk",   "Talk",                    "talk",   True),
                        ("act_gift",   "Gift (%d)" % sum(gifts.values()),  "gift",   _gift_ok),
                        ("act_hug",    "Hug",                     "hug",    not _angry),
                        ("act_kiss",   "Kiss",                    "kiss",   not _angry),
                        ("act_invite", "Invite",                  "date",   _date_ok and not _angry),
                        ("act_phone",  "Get #",                   "number", _num_ok and not _angry),
                        ("act_leave",  "Leave",                   "leave",  True)]:
                    button:
                        sensitive _ok
                        action Return(_ret)
                        background None
                        hover_background None
                        vbox:
                            spacing 4
                            add Transform("images/ui/icons/%s.png" % _icon, size=(72, 72), alpha=(1.0 if _ok else 0.35)) xalign 0.5
                            text _lbl font ACT_FONT size 15 xalign 0.5 color ("#cfe0f5" if _ok else "#4a6080") hover_color "#ffffff"


# ── Gift type picker ──────────────────────────────────────────────────
screen npc_gift_select():
    zorder 22
    frame:
        xalign 0.5
        yalign 0.5
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 18)
        vbox:
            spacing 12
            text "Choose a gift:" font ACT_FONT size 20 color "#9fb6d6" xalign 0.5
            for _gkey, (_gname, _gcost, _gints) in GIFT_TYPES.items():
                $ _ghave = gifts.get(_gkey, 0)
                button:
                    xsize 280
                    sensitive _ghave > 0
                    background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                    hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                    action Return(_gkey)
                    text "[_gname]  (x[_ghave])" font ACT_FONT size 17 color ("#cfe0f5" if _ghave > 0 else "#4a6080") hover_color "#ffffff" xalign 0.5
            textbutton "Cancel" action Return("back") xalign 0.5 text_font ACT_FONT text_size 15 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Topic picker — 3×3 icon grid ───────────────────────────────────────
screen npc_topics(npc_id):
    zorder 22
    $ _likes    = NPC_DATA[npc_id].get("likes", [])
    $ _dislikes = NPC_DATA[npc_id].get("dislikes", [])
    frame:
        xpos 960
        xanchor 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 18)
        vbox:
            spacing 14
            hbox:
                xsize 464
                text "Talk about..." font ACT_FONT size 20 color "#9fb6d6" xalign 0.0 yalign 0.5
                textbutton "Back" action Return("back") xalign 1.0 text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"
            vpgrid:
                cols 3
                spacing 10
                for key, label in TOPICS:
                    $ _tint  = ("#ffd76a" if key in _likes else ("#6b82a6" if key in _dislikes else "#cfe0f5"))
                    $ _used  = topic_used_today(npc_id, key)
                    $ _badge = _topics_seen.get(npc_id, {}).get(key)
                    $ _arc_avail = (not _used) and (check_arc(npc_id, key) is not None)
                    button:
                        xysize (148, 120)
                        sensitive not _used
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        action Return(key)
                        vbox:
                            spacing 6
                            xalign 0.5 yalign 0.5
                            fixed:
                                xysize (60, 60)
                                xalign 0.5
                                add Transform("images/ui/icons/topic_%s.png" % key, size=(60, 60), alpha=(0.35 if _used else 1.0))
                                if _badge == "like":
                                    text "+" xpos 42 ypos 0 size 18 color "#39c07a" font ACT_FONT
                                elif _badge == "dislike":
                                    text "−" xpos 42 ypos 0 size 18 color "#e86a55" font ACT_FONT
                                if _arc_avail:
                                    text "★" xpos 0 ypos 0 size 14 color "#f0d060" font ACT_FONT
                            text label font ACT_FONT size 15 color ("#445060" if _used else _tint) hover_color "#ffffff" xalign 0.5


# ── Driver ─────────────────────────────────────────────────────────────
label npc_interact(npc_id):
    $ renpy.hide_screen("npc_relbar")
    $ renpy.hide("npcsprite")
    $ renpy.hide("npcsprite2")
    $ _rb_prev_aff = -1   # -1 = don't flash on the opening render
    $ _rb_prev_tr = -1
    $ _rel_feedback_aff = 0
    $ _rel_feedback_tr = 0
    $ _rb_flash_aff = 0.0
    $ _rb_flash_tr = 0.0
    $ _rb_flash_aff_neg = 0.0
    $ _rb_flash_tr_neg = 0.0
    # update last-seen day for this NPC (feeds ignore-decay in new_day)
    $ store.npc_last_seen[npc_id] = day
    $ _spr = NPC_DATA[npc_id]["sprite"]
    show expression _spr as npcsprite at sprite_c
    show screen npc_relbar(npc_id)
    $ _npc_panel_npc_id = npc_id
    $ _nm = NPC_DATA[npc_id]["name"]
    # cold approach: a stranger might brush you off
    if not cold_approach_ok(npc_id):
        $ _rb = renpy.random.choice(COLD_REBUFF) % _nm
        "[_rb]"
        $ _npc_panel_npc_id = None
        hide screen npc_relbar
        hide npcsprite
        hide npcsprite2
        return
    # Approach succeeded or NPC already known — record encounter now.
    $ mark_npc_encountered(npc_id)
    if need_hygiene < 25:
        "[_nm] leans back a little, trying to be polite about it. You could really use a shower."
    call expression NPC_DATA[npc_id]["greet"]
    $ _act = ""
    while _act != "leave":
        $ _act = renpy.call_screen("npc_actions", npc_id)
        if _act == "talk":
            $ _fu_label = _check_talk_followup(npc_id)
            if _fu_label:
                call expression _fu_label
            else:
                $ _ctx_label = _ctx_talk_label(npc_id)
                if _ctx_label:
                    call expression _ctx_label
                    $ _do_talk_accounting(npc_id)
                else:
                    $ _t = renpy.call_screen("npc_topics", npc_id)
                    if _t != "back":
                        $ _arc = check_arc(npc_id, _t)
                        if _arc is not None:
                            call expression _arc["label"]
                        else:
                            $ do_talk(npc_id, _t)
        elif _act == "gift":
            $ _g = renpy.call_screen("npc_gift_select")
            if _g != "back":
                $ do_gift(npc_id, _g)
        elif _act == "hug":
            $ _jealous = check_jealousy(npc_id)
            if _jealous:
                $ _jn = " and ".join(_jealous)
                "[_jn] clocks the embrace. Their expression flickers."
            call do_hug_interaction(npc_id)
            if store._last_hug_accepted:
                $ record_social_attention(npc_id, "hug")
            $ spend_time(0.1)
        elif _act == "kiss":
            $ _jealous = check_jealousy(npc_id)
            if _jealous:
                $ _jn = " and ".join(_jealous)
                "[_jn] catches your eye. Their expression shifts."
            call do_kiss_interaction(npc_id)
            if _kiss_outcome in ("first_kiss", "warm", "repeat"):
                $ record_social_attention(npc_id, "kiss")
            $ spend_time(0.1)
        elif _act == "number":
            $ store.npc_contacts = store.npc_contacts + [npc_id]
            $ _apply_aff(npc_id, 2)
            "[_nm] smiles. \"Sure, here you go.\" Number saved."
        elif _act == "date":
            $ _jealous = check_jealousy(npc_id)
            if _jealous:
                $ _jn = " and ".join(_jealous)
                "[_jn] catches your attention drift toward [_nm]. Something shifts in their expression."
            call npc_date(npc_id)
            if store._last_date_completed:
                $ record_social_attention(npc_id, "date")
            $ _act = "leave"   # a date is the whole evening
    $ _npc_panel_npc_id = None
    hide screen npc_relbar
    hide npcsprite
    hide npcsprite2
    return


# ── Dates / outings v2 (works for everyone; unlocks at affection 30) ───
# Romanceable NPCs go on a "date"; everyone else gets a framed-as-friends
# "outing". Rewards are venue-preference- and repetition-aware (see
# date_outing_rewards) and the closing beat reflects the romance state.
label npc_date(npc_id):
    $ store._last_date_completed = False
    $ _nm = NPC_DATA[npc_id]["name"]
    $ _spr = NPC_DATA[npc_id]["sprite"]
    $ _c = getattr(store, NPC_DATA[npc_id]["say"])
    $ _romanceable = npc_id in ROMANCE_PROFILES
    $ _date_prompt = ("Take %s out — where?" % _nm) if _romanceable else ("Hang out with %s — where?" % _nm)
    $ _venue = None
    menu:
        "[_date_prompt]"
        "Dinner out (3h)":
            $ _venue = "dinner"
            scene restaurantnight
        "Rooftop drinks (3h)":
            $ _venue = "rooftop"
            scene bar_rooftop_night
        "A walk on the beach (3h)":
            $ _venue = "beach"
            scene beachnight
        "Actually, never mind":
            return
    show screen hud
    show expression _spr as npcsprite at sprite_c
    $ _date_owarn = _overlap_warning_text(3)
    if _date_owarn:
        menu:
            "[_date_owarn]\nContinue anyway?"
            "Continue":
                pass
            "Go back":
                return
    $ spend_time(3)
    python:
        _aff_gain, _tr_gain, _date_pref = date_outing_rewards(npc_id, _venue)
        _apply_aff(npc_id, _aff_gain)
        _apply_trust(npc_id, _tr_gain)          # clamped path, not raw setattr
        record_date_outing(npc_id, _venue)
        _date_rs = get_romance_state(npc_id)
    # Preference flavour
    if _date_pref == "preferred":
        "[_nm] lights up — this is exactly their kind of evening."
    elif _date_pref == "disliked":
        "[_nm] is a good sport about it, but you can tell it isn't quite their scene."
    # Closing beat scales with the relationship
    if _romanceable and _date_rs in ("dating", "committed"):
        $ renpy.say(_c, "I needed this. Just us, no noise.")
    elif _romanceable and _date_rs == "interested":
        $ renpy.say(_c, "That felt like a little more than two friends killing an evening. I liked it.")
    else:
        $ renpy.say(_c, "That was fun. We should do it again sometime.")
    hide npcsprite
    hide npcsprite2
    $ store._last_date_completed = True
    return


# ══ Greetings (scale with affection) ═══════════════════════════════════
label nora_greet:
    # Track actual interaction (café + bar) — not location entry.
    # Feeds the 8-day ignore timer in new_day().
    $ nora_last_seen_day = day
    if nora_affection >= 50:
        n "Hey, you. I was hoping you'd come in today."
    elif nora_affection >= 25:
        n "There you are. The usual?"
    else:
        n "Back already? Coffee's that good, or...?"
    return

label marcus_greet:
    if marcus_affection >= 50:
        m "Was just about to text you. What's up, man?"
    elif marcus_affection >= 25:
        m "There he is. Grab a seat."
    else:
        m "Hey, neighbor. Surviving?"
    return

label caroline_greet:
    if caroline_affection >= 50:
        caro "There's my favorite source of interesting problems. Sit."
    elif caroline_affection >= 25:
        caro "Look who it is. Whatever you did, I already know."
    else:
        caro "HR. If you're not on fire, make it quick."
    return

label lena_greet:
    if lena_affection >= 50:
        lena "Oh good, a face that isn't a chart. Two minutes, they're yours."
    elif lena_affection >= 25:
        lena "Hey. Still standing? Good. Half my morning wasn't."
    else:
        lena "If you're not bleeding, you're in the wrong line - but hi."
    return

label natalie_greet:
    if natalie_affection >= 50:
        nat "There's my reliable one. Don't let it go to your head."
    elif natalie_affection >= 25:
        nat "You again. Fine. You work harder than half the floor, so - what."
    else:
        nat "You lost? Break room's that way."
    return

label martha_greet:
    if martha_affection >= 50:
        ma "Oh good, it's you. I was getting bored being the smartest person in the room."
    elif martha_affection >= 25:
        ma "You clean up better than I expected. Impress me, or at least don't bore me."
    else:
        ma "So the new blood has ambitions. We'll see if they survive this place."
    return

label elle_greet:
    if elle_affection >= 50:
        el "Hey, stranger! Wednesday's better already. Sit, the water's perfect."
    elif elle_affection >= 25:
        el "Oh - hi! Didn't think I'd see you out here again. Good surprise."
    else:
        el "Hi there. You look a little lost for a beach. First time?"
    return

label zoe_greet:
    if zoe_affection >= 50:
        z "Hey, you. Pull up some grass. I'm avoiding a canvas that's avoiding me."
    elif zoe_affection >= 25:
        z "Oh, it's you. Good - I needed an excuse to stop pretending to sketch."
    else:
        z "You're blocking my light. ...Kidding. Mostly. I'm Zoe."
    return

label sam_greet:
    if sam_affection >= 50:
        sam "Hey! Perfect timing, I need a break before my legs stage a mutiny."
    elif sam_affection >= 25:
        sam "Oh hey, it's you! Still can't keep up, but I respect the effort."
    else:
        sam "Morning! You run, or just admiring people who do? I'm Sam."
    return

label eli_greet:
    if eli_affection >= 50:
        eli "Oh good, a friendly face. Save me from this thesis for five minutes?"
    elif eli_affection >= 25:
        eli "Hey. Sorry - deep in it. But a break's probably healthy. Allegedly."
    else:
        eli "Uh, hi. I'm Eli. Don't mind the mess, this is just... my whole personality."
    return

label kai_greet:
    if kai_affection >= 50:
        kai "Yo! Was just thinking about you. Good timing as always."
    elif kai_affection >= 25:
        kai "Hey! You're back. This beach has a way of pulling people in, right?"
    else:
        kai "Sup. You look like someone who doesn't come here enough."
    return


# ── Physical interaction wrappers ──────────────────────────────────────

label do_hug_interaction(npc_id):
    $ _hug_text = do_hug(npc_id)
    $ _hug_cg_name = "cg_" + npc_id + "_hug"
    # Only show the embrace CG when the hug was actually accepted — otherwise the
    # image (a full hug) would contradict a rejection/cooldown line.
    if store._last_hug_accepted and renpy.has_image(_hug_cg_name):
        show expression _hug_cg_name as interaction_cg with dissolve
        show screen hud
        "[_hug_text]"
        hide interaction_cg with dissolve
    else:
        "[_hug_text]"
    return

label do_kiss_interaction(npc_id):
    $ (_kiss_outcome, _kiss_text) = do_kiss(npc_id)
    if _kiss_outcome == "first_kiss":
        $ _fk_label = "scene_first_kiss_" + npc_id
        if renpy.has_label(_fk_label):
            call expression _fk_label
        else:
            "[_kiss_text]"
    else:
        "[_kiss_text]"
    return


# ── First-kiss scenes (romanceable NPCs) ───────────────────────────────
# Each: hides relbar → full-screen CG dissolve → narration → ends the interaction.

label scene_first_kiss_nora:
    hide screen npc_relbar
    scene cg_nora_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return

label scene_first_kiss_elle:
    hide screen npc_relbar
    scene cg_elle_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return

label scene_first_kiss_zoe:
    hide screen npc_relbar
    scene cg_zoe_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return

label scene_first_kiss_caroline:
    hide screen npc_relbar
    scene cg_caroline_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return

label scene_first_kiss_lena:
    hide screen npc_relbar
    scene cg_lena_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return

label scene_first_kiss_martha:
    hide screen npc_relbar
    scene cg_martha_kiss with dissolve
    show screen hud
    "[_kiss_text]"
    $ _act = "leave"
    return


# ── Phase 2: one-time Talk follow-up labels ────────────────────────────

label talk_followup_marcus_first_shift:
    $ talk_followup_marcus_first_shift_done = True
    $ spend_time(0.5)
    $ fs_record_social("marcus", "talk")
    if marcus_first_shift_choice == "barely":
        m "Still surviving the job?"
        mc "Barely."
        m "Consistent, at least."
    elif marcus_first_shift_choice == "used_to_it":
        m "Still think you could get used to the job?"
        mc "Ask me after the fifth shift."
        m "Good answer."
    else:
        m "Still surviving the job?"
        mc "So far."
        m "Good."
        m "The first shift proves you can show up."
        m "The fifth proves it wasn't an accident."
    return

label talk_followup_martha_credit:
    $ talk_followup_martha_credit_done = True
    $ spend_time(0.5)
    $ fs_record_social("martha", "talk")
    ma "The next summary is yours too."
    mc "That almost sounded like trust."
    ma "Don't make me revise it."
    return

label talk_followup_martha_revision:
    $ talk_followup_martha_revision_done = True
    $ spend_time(0.5)
    $ fs_record_social("martha", "talk")
    if martha_revision_choice == "update":
        ma "The revision reached the meeting on time."
        mc "You could say thank you."
        ma "I could also revise it again."
    else:
        ma "You were right about the duplicate attachments."
        mc "I was hoping never to hear that sentence."
        ma "Don't become dependent on it."
    return

label talk_followup_martha_settled:
    $ talk_followup_martha_settled_done = True
    $ spend_time(0.5)
    $ fs_record_social("martha", "talk")
    ma "You stopped asking where the templates are."
    mc "I know where they are now."
    ma "That wasn't praise."
    mc "It sounded close."
    ma "Then your standards are adapting."
    return

# Phase 35 — post-invitation Talk follow-up labels

label marcus_park_invite_followup:
    $ _do_talk_accounting("marcus")
    m "You still counting that shot?"
    mc "It went in."
    m "After the rebound."
    mc "Still went in."
    m "That is not how counting works."
    $ _fu_d = dict(store.npc_invitation_followup_pending); del _fu_d["marcus"]; store.npc_invitation_followup_pending = _fu_d
    return

label nora_grounds_invite_followup:
    $ _do_talk_accounting("nora")
    n "I changed the drink."
    mc "Because of my opinion?"
    n "Despite your opinion."
    mc "Good to know I helped."
    n "You created resistance. Similar effect."
    $ _fu_d = dict(store.npc_invitation_followup_pending); del _fu_d["nora"]; store.npc_invitation_followup_pending = _fu_d
    return

label zoe_park_invite_followup:
    $ _do_talk_accounting("zoe")
    z "I kept the second version."
    mc "The one you were less annoyed by?"
    z "I corrected that."
    mc "The drawing?"
    z "The annoyance."
    $ _fu_d = dict(store.npc_invitation_followup_pending); del _fu_d["zoe"]; store.npc_invitation_followup_pending = _fu_d
    return

label eli_library_invite_followup:
    $ _do_talk_accounting("eli")
    eli "The second outlet stopped working."
    mc "You jinxed it."
    eli "I documented it."
    mc "That is not the same."
    eli "It is more useful."
    $ _fu_d = dict(store.npc_invitation_followup_pending); del _fu_d["eli"]; store.npc_invitation_followup_pending = _fu_d
    return

# Phase 6B — Zoe jealousy pilot conversation
label zoe_jealousy_first_notice:
    $ zoe_jealousy_first_notice_done = True
    $ _jzp = dict(store.npc_jealousy_pending)
    $ _jzp.pop("zoe", None)
    $ store.npc_jealousy_pending = _jzp
    $ _jzld = dict(store.npc_jealousy_last_day)
    $ _jzld["zoe"] = day
    $ store.npc_jealousy_last_day = _jzld
    $ spend_time(0.5)
    $ fs_record_social("zoe", "talk")
    z "You've been spending a lot of time with her."
    mc "Are you keeping track?"
    z "No."
    z "I noticed."
    menu:
        "\"It doesn't mean anything.\"":
            mc "It doesn't mean anything."
            $ _apply_trust("zoe", -1)
            z "That wasn't what I asked."
        "\"I didn't realise it bothered you.\"":
            mc "I didn't realise it bothered you."
            z "I didn't say it did."
            mc "You didn't have to."
        "\"Are you jealous?\"":
            mc "Are you jealous?"
            $ _apply_aff("zoe", -1)
            z "That's a very confident interpretation."
    $ add_relationship_memory("zoe", "zoe_first_jealousy_notice", "Zoe noticed who I was spending time with")
    return

label nora_jealousy_first_notice:
    $ nora_jealousy_first_notice_done = True
    $ _njp = dict(store.npc_jealousy_pending)
    $ _njp.pop("nora", None)
    $ store.npc_jealousy_pending = _njp
    $ _njld = dict(store.npc_jealousy_last_day)
    $ _njld["nora"] = day
    $ store.npc_jealousy_last_day = _njld
    $ spend_time(0.5)
    $ fs_record_social("nora", "talk")
    n "You've been popular lately."
    mc "That sounds dangerous."
    n "Only for your schedule."
    mc "Is that what this is about?"
    n "I'm deciding."
    menu:
        "\"Are you jealous?\"":
            mc "Are you jealous?"
            n "A little."
            n "Don't look so pleased with yourself."
        "\"You could have just asked.\"":
            mc "You could have just asked."
            n "I just did."
        "\"It's none of your business.\"":
            mc "It's none of your business."
            $ _apply_aff("nora", -1)
            n "Right."
            n "Good to know."
    $ add_relationship_memory("nora", "nora_first_jealousy_notice", "Nora admitted she had noticed my attention elsewhere")
    return

label martha_jealousy_first_notice:
    $ martha_jealousy_first_notice_done = True
    $ _mjp = dict(store.npc_jealousy_pending)
    $ _mjp.pop("martha", None)
    $ store.npc_jealousy_pending = _mjp
    $ _mjld = dict(store.npc_jealousy_last_day)
    $ _mjld["martha"] = day
    $ store.npc_jealousy_last_day = _mjld
    $ spend_time(0.5)
    $ fs_record_social("martha", "talk")
    ma "Your private life has become surprisingly public."
    mc "Is this professional feedback?"
    ma "I haven't decided."
    mc "Then what is it?"
    ma "An observation."
    menu:
        "\"Does it bother you?\"":
            mc "Does it bother you?"
            ma "That depends on whether you intended me to notice."
        "\"I wasn't trying to make a point.\"":
            mc "I wasn't trying to make a point."
            ma "Good."
            ma "It would have been an imprecise one."
        "\"You're overthinking it.\"":
            mc "You're overthinking it."
            $ _apply_trust("martha", -1)
            ma "And you're underestimating it."
    $ add_relationship_memory("martha", "martha_first_jealousy_notice", "Martha confronted me about what she had noticed")
    return

label eli_jealousy_first_notice:
    $ eli_jealousy_first_notice_done = True
    $ _ejp = dict(store.npc_jealousy_pending)
    $ _ejp.pop("eli", None)
    $ store.npc_jealousy_pending = _ejp
    $ _ejld = dict(store.npc_jealousy_last_day)
    $ _ejld["eli"] = day
    $ store.npc_jealousy_last_day = _ejld
    $ spend_time(0.5)
    $ fs_record_social("eli", "talk")
    e "You don't have to explain anything."
    mc "I wasn't going to."
    e "Okay."
    "A quiet pause."
    mc "You clearly want to say something."
    e "Wanting to and being entitled to are different things."
    menu:
        "\"It matters what you think.\"":
            mc "It matters what you think."
            e "Then don't make me guess."
        "\"There's nothing to explain.\"":
            mc "There's nothing to explain."
            $ _apply_trust("eli", -1)
            e "Then we're done."
        "\"Are you upset?\"":
            mc "Are you upset?"
            $ _apply_aff("eli", -1)
            e "I'm adjusting my expectations."
    $ add_relationship_memory("eli", "eli_first_jealousy_notice", "Eli withdrew after noticing my attention elsewhere")
    return


# ── Phase 21: Sandbeach contextual Talk ─────────────────────────────────────

label elle_sandbeach_tide:
    el "The water was farther out earlier."
    mc "You've been watching it?"
    el "Not deliberately."
    mc "That sounds convincing."
    el "I had a better spot before the tide disagreed."
    return

label elle_sandbeach_shoes:
    mc "You brought shoes onto the sand."
    el "I also brought the intention to keep sand out of them."
    mc "How is that going?"
    el "The intention remains strong."
    return

label elle_sandbeach_horizon:
    el "The horizon looks closer when the air is clear."
    mc "It is not."
    el "I know."
    mc "Then why say it?"
    el "Because knowing something isn't the same as how it looks."
    return

label kai_sandbeach_water:
    mc "Going in?"
    kai "I considered it."
    mc "And?"
    kai "The water made a counterargument."
    return

label kai_sandbeach_crowd:
    kai "It's quieter over here."
    mc "There are still people everywhere."
    kai "Quieter isn't the same as empty."
    mc "Fair."
    return

label kai_sandbeach_walk:
    mc "How far did you walk?"
    kai "Far enough to stop counting."
    mc "That doesn't answer the question."
    kai "It answers why I don't know."
    return

label zoe_sandbeach_colour:
    z "The water isn't blue today."
    mc "It looks blue."
    z "That's the problem."
    mc "What colour is it?"
    z "I haven't decided."
    return

label zoe_sandbeach_footprints:
    z "Someone walked through the part I was drawing."
    mc "The sand?"
    z "The footprints."
    mc "They made more footprints."
    z "Different ones."
    return

label zoe_sandbeach_wind:
    "The wind lifts the edge of Zoe's page."
    "She presses it flat with one hand."
    mc "Need help?"
    z "I need the wind to develop restraint."
    mc "I'll speak to it."
    z "Be firm."
    return


# ── Phase 25: Contextual public Talk rollout A ───────────────────────────────

label marcus_grounds_order:
    m "I ordered the simple one."
    mc "Which one is simple?"
    m "The one with the shortest name."
    mc "That doesn't make it simple."
    m "It makes it easier to say confidently."
    return

label marcus_grounds_table:
    mc "You've been looking at that table for a while."
    m "It's close to the door and far from the speaker."
    mc "Strategic."
    m "I take coffee seating seriously."
    return

label marcus_grounds_temperature:
    m "This is still too hot."
    mc "You bought it ten minutes ago."
    m "I expected progress."
    mc "It's coffee, not a negotiation."
    m "Everything is a negotiation if you wait long enough."
    return

label eli_library_outlet:
    eli "That outlet doesn't work."
    mc "How do you know?"
    eli "I tried it."
    mc "Once?"
    eli "Four times, with decreasing optimism."
    return

label eli_library_bookmark:
    mc "You're using a receipt as a bookmark."
    eli "It was available."
    mc "It's from three months ago."
    eli "It has proven reliable."
    return

label eli_library_keyboard:
    "A keyboard clicks rapidly from the next table."
    eli "They've been writing the same sentence for five minutes."
    mc "How can you tell?"
    eli "The backspace key has a distinct sound."
    return

label lena_hospital_coffee:
    mc "Is that coffee still warm?"
    lena "That stopped being the relevant question an hour ago."
    mc "What's the relevant question?"
    lena "Whether I remember where I left it."
    return

label lena_hospital_sign:
    lena "That sign has been pointing the wrong way all week."
    mc "Nobody changed it?"
    lena "Several people discussed changing it."
    mc "Productive."
    lena "There were notes."
    return

label lena_hospital_quiet:
    mc "It's unusually quiet."
    lena "Never say that in a hospital."
    mc "Why?"
    lena "Because the building takes it personally."
    return

label sam_gym_bench:
    sam "Someone moved this bench."
    mc "By how much?"
    sam "Not enough to notice."
    mc "You noticed."
    sam "Exactly."
    return

label sam_gym_music:
    mc "Do you actually like this song?"
    sam "Not anymore."
    mc "What changed?"
    sam "It started for the fourth time."
    return

label sam_gym_rest:
    sam "You're supposed to rest between sets."
    mc "I am resting."
    sam "You're reorganising the weights."
    mc "Resting productively."
    sam "That isn't a thing."
    return


# ── Phase 26: Contextual public Talk rollout B ───────────────────────────────

label nora_grounds_queue:
    n "The queue always gets longer when somebody asks whether we're busy."
    mc "Maybe they want confirmation."
    n "They usually ask while standing in the queue."
    mc "Strong evidence."
    n "I'm considering putting it on the menu."
    return

label nora_grounds_lid:
    n "That lid doesn't fit."
    mc "It looks like it fits."
    n "That is how it gains your trust."
    mc "You make disposable cups sound dangerous."
    n "Complacency is dangerous."
    return

label nora_grounds_regular:
    mc "You remembered their order."
    n "They order the same thing every time."
    mc "Still counts."
    n "It stops counting after the twentieth time."
    return

label martha_nexus_elevator:
    ma "The elevator stopped on every floor."
    mc "Busy building."
    ma "Nobody entered or left."
    mc "Less busy building."
    ma "More indecisive elevator."
    return

label martha_nexus_calendar:
    mc "Your calendar has no empty space."
    ma "There are seven minutes at twelve forty-three."
    mc "That isn't empty space."
    ma "It is if nobody notices."
    return

label martha_nexus_badge:
    ma "Your badge is upside down."
    mc "It still works."
    ma "That wasn't my objection."
    mc "What was?"
    ma "That I noticed."
    return

label natalie_warehouse_marker:
    nat "Who left the marker without the cap?"
    mc "Is that important?"
    nat "Not until every label becomes unreadable."
    mc "Then it becomes important?"
    nat "Then it becomes expensive."
    return

label natalie_warehouse_noise:
    "A pallet jack rattles somewhere behind the shelving."
    mc "That sounds healthy."
    nat "It sounds temporary."
    mc "Which part?"
    nat "The pallet jack."
    return

label natalie_warehouse_path:
    nat "Keep the walkway clear."
    mc "It is clear."
    nat "It was not clear ten seconds ago."
    mc "Fast improvement."
    nat "Late improvement."
    return

label kai_nightclub_volume:
    mc "Can you hear me?"
    kai "Mostly."
    mc "What did I say?"
    kai "That proves less than you think."
    return

label kai_nightclub_exit:
    kai "The exit sign is brighter than everything else in here."
    mc "Planning ahead?"
    kai "Appreciating useful design."
    mc "Very festive."
    kai "I have range."
    return

label kai_nightclub_song:
    kai "This song was better outside."
    mc "You heard it outside?"
    kai "Through three walls."
    mc "And that improved it?"
    kai "Significantly."
    return


# ── Phase 27: Contextual public Talk rollout C ───────────────────────────────

label caroline_nexus_reception:
    caro "Reception called twice."
    mc "About what?"
    caro "They did not say."
    mc "Are you going to call back?"
    caro "Eventually they will become specific."
    return

label caroline_nexus_floor:
    mc "You pressed the wrong floor."
    caro "No."
    mc "The doors opened on the wrong floor."
    caro "The elevator misunderstood."
    mc "Naturally."
    return

label caroline_nexus_document:
    caro "This document is marked confidential."
    mc "It is sitting beside the printer."
    caro "Which is why I am standing beside the printer."
    mc "Protecting it?"
    caro "Judging whoever left it."
    return

label zoe_park_tree:
    z "That tree leans more than it did yesterday."
    mc "You measured it?"
    z "No."
    mc "Then how do you know?"
    z "It looks more committed."
    return

label zoe_park_dog:
    "A dog stops beside Zoe and studies her sketchbook."
    z "No."
    mc "It hasn't done anything."
    z "It is considering it."
    "The dog loses interest and walks away."
    z "Correct decision."
    return

label zoe_park_path:
    mc "Why are you sitting beside the path instead of on the bench?"
    z "The bench faces the wrong direction."
    mc "For what?"
    z "Everything."
    return

label elle_grounds_window:
    el "This table gets better light."
    mc "You moved two metres."
    el "Exactly."
    mc "Significant journey."
    el "Worth it."
    return

label elle_grounds_spoon:
    mc "You haven't used the spoon."
    el "I might."
    mc "For what?"
    el "That depends on whether the coffee improves."
    mc "Will stirring help?"
    el "It will create activity."
    return

label elle_grounds_choice:
    el "I always choose faster when the menu is shorter."
    mc "There are six options."
    el "And I have been considering them for ten minutes."
    mc "Efficient."
    el "I did not say I was good at it."
    return

label kai_gym_mirror:
    mc "You keep looking at the mirror."
    kai "I am checking the space behind me."
    mc "Very practical."
    kai "That is why the mirror is there."
    mc "I thought it was for form."
    kai "That too."
    return

label kai_gym_machine:
    kai "This machine has twelve adjustment points."
    mc "Is that too many?"
    kai "It has one useful position."
    mc "Which one?"
    kai "I am still negotiating."
    return

label kai_gym_towel:
    mc "That towel has been on the bench for a while."
    kai "It is reserving the bench."
    mc "For who?"
    kai "Someone with a strong sense of entitlement."
    return


label npc_interact_from_dock:
    $ _npc = _dock_npc
    $ _return = _dock_return or "location_centrum"
    $ _dock_npc = None
    $ _dock_return = None
    hide screen people_here_dock
    call npc_interact(_npc)
    jump expression _return


label show_public_sprites:
    $ _nc = len(_vis)
    hide npcsprite
    hide npcsprite2
    hide npcsprite3
    hide npcsprite4
    if _nc >= 4:
        show expression _vis[0][1] as npcsprite  at sprite_quad_d
        show expression _vis[1][1] as npcsprite2 at sprite_quad_a
        show expression _vis[2][1] as npcsprite3 at sprite_quad_b
        show expression _vis[3][1] as npcsprite4 at sprite_quad_c
    elif _nc == 3:
        show expression _vis[0][1] as npcsprite  at sprite_tri_r
        show expression _vis[1][1] as npcsprite2 at sprite_tri_l
        show expression _vis[2][1] as npcsprite3 at sprite_tri_c
    elif _nc == 2:
        show expression _vis[0][1] as npcsprite  at sprite_duo_r
        show expression _vis[1][1] as npcsprite2 at sprite_duo_l
    elif _nc == 1:
        show expression _vis[0][1] as npcsprite  at sprite_solo
    return
