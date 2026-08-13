# NPC home visit system — invite NPCs over for shared activities.

init python:

    HOME_VISIT_ACTIVITIES = {
        "coffee_talk":    {"title": "Coffee and talk",      "hours": 1, "energy": 8,  "rel_gain": 4, "cooldown_days": 3},
        "watch_movie":    {"title": "Watch a movie",        "hours": 2, "energy": 6,  "rel_gain": 5, "cooldown_days": 4},
        "cook_together":  {"title": "Cook together",        "hours": 2, "energy": 12, "rel_gain": 6, "cooldown_days": 4, "req_skill_cook": 2},
        "study_together": {"title": "Work or study",        "hours": 2, "energy": 10, "rel_gain": 4, "cooldown_days": 3},
        "play_music":     {"title": "Play music together",  "hours": 2, "energy": 10, "rel_gain": 6, "cooldown_days": 5, "npcs": ["zoe", "nora"]},
    }

    NPC_HOME_COMPATIBILITY = {
        "marcus": ["coffee_talk", "watch_movie", "study_together"],
        "nora":   ["coffee_talk", "watch_movie", "cook_together", "play_music"],
        "zoe":    ["coffee_talk", "watch_movie", "play_music"],
        "eli":    ["coffee_talk", "study_together"],
    }

    def can_invite_npc_home(npc_id):
        if store.home_visit_today: return False
        if not getattr(store, npc_id + "_met", False): return False
        if npc_id not in NPC_HOME_COMPATIBILITY: return False
        rel = getattr(store, NPC_DATA[npc_id]["aff"], 0)
        if rel < 20: return False
        last = store.npc_home_visit_cooldowns.get(npc_id, -99)
        if store.day - last < 2: return False
        return True

    def available_home_visit_activities(npc_id):
        compat = NPC_HOME_COMPATIBILITY.get(npc_id, [])
        result = []
        for act_id in compat:
            act = HOME_VISIT_ACTIVITIES[act_id]
            if "req_skill_cook" in act and skill_val("cook") < act["req_skill_cook"]:
                continue
            if "npcs" in act and npc_id not in act["npcs"]:
                continue
            result.append(act_id)
        return result

    def _activity_recent_uses(npc_id, act_id):
        key_pair = (npc_id, act_id)
        cooldown = HOME_VISIT_ACTIVITIES[act_id]["cooldown_days"]
        return sum(1 for e in store.home_visit_history[-10:]
                   if e.get("npc") == npc_id and e.get("activity") == act_id
                   and store.day - e.get("day", 0) <= cooldown)

    # ── Home-visit schedule overrides ────────────────────────────────────────
    def create_home_visit_override(npc_id, duration_hours=2):
        """Pin the NPC at the player's home for the duration of the visit."""
        add_schedule_override(
            npc_id       = npc_id,
            day          = store.day,
            hour_start   = int(store.hour),
            hour_end     = int(store.hour) + duration_hours,
            location_id  = "location_home",
            activity_id  = "visiting_player",
            public       = False,
            interactable = True,
            source_id    = "home_visit_" + npc_id,
            expires_day  = store.day + 1,
        )

    def remove_home_visit_override(npc_id):
        """Remove the override created by create_home_visit_override."""
        source_id = "home_visit_" + npc_id
        store.npc_schedule_overrides = [
            o for o in store.npc_schedule_overrides
            if o.get("source_id") != source_id
        ]

    # ── Phase 62: home quality modifier ──────────────────────────────────────
    # The visit system itself is unchanged. This is a quality modifier only —
    # nobody refuses to come over because the sofa is cheap.
    _QUALITY_FLAVOR = [
        "",
        "The place is comfortable enough for it.",
        "Your place is a genuinely nice spot to spend an evening.",
        "Your place is the sort of flat people are happy to be invited to.",
    ]

    def home_visit_quality_bonus(act_id):
        """Extra relationship gain from the home setup. 0 for a bare flat.
        Screen-based activities lean on the living room; work/study leans on the
        workspace instead."""
        if act_id == "study_together":
            return study_focus_modifier() // 2      # 0-2
        return home_social_bonus()                  # 0-3

    def home_visit_quality_text(act_id):
        if act_id == "study_together":
            return "You both get real work done at a proper desk." if study_focus_modifier() >= 3 else ""
        return _QUALITY_FLAVOR[home_social_tier()]

    def complete_home_visit(npc_id, act_id):
        act = HOME_VISIT_ACTIVITIES[act_id]
        recent = _activity_recent_uses(npc_id, act_id)
        rel_mult_list = [1.0, 0.5, 0.1]
        rel_mult = rel_mult_list[min(recent, 2)]
        rel_gain = max(0, int(act["rel_gain"] * rel_mult))
        # quality bonus scales with the repetition multiplier too, so a nice flat
        # cannot be farmed by inviting the same person to the same thing daily.
        rel_gain += int(round(home_visit_quality_bonus(act_id) * rel_mult))
        create_home_visit_override(npc_id, act["hours"])
        spend_time(act["hours"])
        store.need_energy = max(0, store.need_energy - act["energy"])
        if rel_gain > 0:
            aff_var = NPC_DATA[npc_id]["aff"]
            setattr(store, aff_var, min(100, getattr(store, aff_var, 0) + rel_gain))
        store.home_visit_today = True
        d = dict(store.npc_home_visit_cooldowns)
        d[npc_id] = store.day
        store.npc_home_visit_cooldowns = d
        store.home_visit_history = list(store.home_visit_history) + [
            {"npc": npc_id, "activity": act_id, "day": store.day, "rel_gain": rel_gain}]
        record_game_event("home_visit_%s_%s_day%d" % (npc_id, act_id, store.day),
            "relation", "%s visited — %s" % (NPC_DATA[npc_id]["name"], act["title"]),
            summary=True, journal=(recent == 0),
            metadata={"npc": npc_id, "activity": act_id, "rel_gain": rel_gain})
        remove_home_visit_override(npc_id)
        return rel_gain

    def _complete_home_visit_wrapper(npc_id, act_id):
        """Function() wrapper — returns None."""
        complete_home_visit(npc_id, act_id)

    # ── Phase 61: "Cook together" uses the real Cooking system ────────────────
    # Culinary-capable NPCs give a small preparation bonus.
    _NPC_COOK_ASSIST = {"nora": ("Nora assists", 6)}

    def npc_cook_assist(npc_id):
        return _NPC_COOK_ASSIST.get(npc_id)

    def complete_cook_together(npc_id):
        """Relationship / cooldown bookkeeping for a cook-together visit. Time,
        energy, cost, meal and XP are handled by the Cooking system itself, so
        this only applies the (diminishing) relationship effect + visit flags."""
        act_id = "cook_together"
        act = HOME_VISIT_ACTIVITIES[act_id]
        recent = _activity_recent_uses(npc_id, act_id)
        rel_mult = [1.0, 0.5, 0.1][min(recent, 2)]
        rel_gain = max(0, int(act["rel_gain"] * rel_mult))
        # Phase 62 §7: dinner at home gets a small extra bump on a good setup.
        if home_social_quality() >= 12:
            rel_gain += int(round(1 * rel_mult))
        if rel_gain > 0:
            aff_var = NPC_DATA[npc_id]["aff"]
            setattr(store, aff_var, min(100, getattr(store, aff_var, 0) + rel_gain))
        store.home_visit_today = True
        d = dict(store.npc_home_visit_cooldowns)
        d[npc_id] = store.day
        store.npc_home_visit_cooldowns = d
        store.home_visit_history = list(store.home_visit_history) + [
            {"npc": npc_id, "activity": act_id, "day": store.day, "rel_gain": rel_gain}]
        record_game_event("cook_together_%s_day%d" % (npc_id, store.day),
            "relation", "%s cooked with you" % NPC_DATA[npc_id]["name"],
            summary=True, journal=(recent == 0),
            metadata={"npc": npc_id, "activity": act_id, "rel_gain": rel_gain})
        return rel_gain

    def _home_visit_act_label(npc_id, act_id):
        """Return a short flavour line for a completed home visit."""
        name = NPC_DATA.get(npc_id, {}).get("name", npc_id)
        act  = HOME_VISIT_ACTIVITIES.get(act_id, {})
        line = "%s came over. %s. Good evening." % (name, act.get("title", "You hung out"))
        q = home_visit_quality_text(act_id)
        if q:
            line += " " + q
        # Phase 65: a visitor who genuinely cares about art reacts to your own
        # work on the wall. Returns None for everyone else, so nothing changes.
        art_line = displayed_artwork_comment(npc_id)
        if art_line:
            line += "

" + art_line
        return line


# ── Home visit selection screen ────────────────────────────────────────────────
screen home_visit_scr(available_guests):
    modal True
    add "#000000cc"
    frame:
        xalign 0.5
        yalign 0.4
        xsize 560
        background "#12161ef8"
        padding (28, 22, 28, 22)
        vbox:
            spacing 12
            text "Invite someone over" font PROFILE_FONT size 22 color "#ffd66a" xalign 0.5
            null height 4
            for _hv_npc in available_guests:
                $ _hv_name = NPC_DATA[_hv_npc]["name"]
                $ _hv_acts = available_home_visit_activities(_hv_npc)
                if _hv_acts:
                    text _hv_name font PROFILE_FONT size 16 color "#cfe0f5"
                    for _hv_act in _hv_acts:
                        $ _hv_act_info = HOME_VISIT_ACTIVITIES[_hv_act]
                        if _hv_act == "cook_together":
                            textbutton "Cook together  (uses the kitchen)":
                                action Return((_hv_npc, _hv_act))
                                text_size 15
                                xpadding 8 ypadding 4
                        else:
                            $ _hv_act_lbl  = "%s  (%dh, -%d energy)" % (_hv_act_info["title"], _hv_act_info["hours"], _hv_act_info["energy"])
                            textbutton _hv_act_lbl:
                                action [Function(_complete_home_visit_wrapper, _hv_npc, _hv_act), Return((_hv_npc, _hv_act))]
                                text_size 15
                                xpadding 8 ypadding 4
            null height 6
            textbutton "Cancel":
                xalign 0.5
                action Return(None)
                text_size 16 text_color "#9fb6d6"
