# Player states — short-duration buffs/debuffs triggered by gameplay events.
# At most 2 unique states active at once. States expire automatically.

init python:

    PLAYER_STATE_DEFS = {
        "focused":   {"title": "Focused",   "desc": "+8% Programming/Business practice XP",   "effect_type": "prog_biz_xp",    "effect_value": 0.08, "max_days": 3},
        "inspired":  {"title": "Inspired",  "desc": "+8% Art/Guitar practice XP",              "effect_type": "art_music_xp",   "effect_value": 0.08, "max_days": 3},
        "confident": {"title": "Confident", "desc": "+5 to public performance/social scores",  "effect_type": "social_score",   "effect_value": 5,    "max_days": 2},
        "stressed":  {"title": "Stressed",  "desc": "Computer work costs +8% more Energy",     "effect_type": "prog_energy_up", "effect_value": 0.08, "max_days": 2},
        "lonely":    {"title": "Lonely",    "desc": "Encourages social activity",               "effect_type": "social_hint",    "effect_value": 1,    "max_days": 3},
    }

    def add_player_state(state_id, source_id, duration=None):
        if state_already_triggered_from_source(source_id): return
        existing = [s for s in store.player_states if s["state_id"] == state_id]
        active_non_same = [s for s in store.player_states if s["state_id"] != state_id]
        if len(active_non_same) >= 2 and not existing: return  # cap at 2 unique
        d = PLAYER_STATE_DEFS.get(state_id, {})
        dur = duration or d.get("max_days", 2)
        entry = {"state_id": state_id, "source_id": source_id,
                 "started_day": store.day, "expires_day": store.day + dur}
        if existing:
            store.player_states = [e for e in store.player_states if e["state_id"] != state_id] + [entry]
        else:
            store.player_states = list(store.player_states) + [entry]
        renpy.notify("%s — %s" % (d.get("title", state_id), d.get("desc", "")))

    def remove_player_state(state_id):
        store.player_states = [s for s in store.player_states if s["state_id"] != state_id]

    def has_player_state(state_id):
        return any(s["state_id"] == state_id for s in store.player_states)

    def active_player_state_effect(effect_type):
        for s in store.player_states:
            d = PLAYER_STATE_DEFS.get(s["state_id"], {})
            if d.get("effect_type") == effect_type:
                return d.get("effect_value", 0)
        return 0

    def expire_player_states():
        store.player_states = [s for s in store.player_states if s["expires_day"] > store.day]

    def state_already_triggered_from_source(source_id):
        return any(s.get("source_id") == source_id for s in store.player_states)

    def _add_player_state_wrapper(state_id, source_id):
        """Function() wrapper — returns None."""
        add_player_state(state_id, source_id)
