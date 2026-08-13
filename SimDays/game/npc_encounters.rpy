# NPC encounters — ambient and interactive moments when entering locations.
# At most 1 encounter per day. ~45% chance when eligible templates exist.

init python:

    NPC_ENCOUNTER_TEMPLATES = [
        {"id": "marcus_bar_01", "npc": "marcus", "type": "ambient",
         "location": "location_bar", "hours": [19, 20, 21, 22],
         "text": "Marcus is at the bar with someone, deep in conversation. He waves briefly.",
         "cooldown_days": 3},
        {"id": "nora_library_01", "npc": "nora", "type": "ambient",
         "location": "location_library", "hours": [10, 11, 12, 13, 14],
         "text": "Nora is at a corner table, surrounded by notes. She looks focused.",
         "cooldown_days": 3},
        {"id": "zoe_park_01", "npc": "zoe", "type": "interactive",
         "location": "location_park", "hours": [12, 13, 14, 15, 16],
         "text": "Zoe is sitting on the grass, sketchbook open.",
         "choices": [
             {"label": "Sit with her for a bit", "rel_gain": 3, "time": 0.5},
             {"label": "Wave and walk on",        "rel_gain": 1, "time": 0},
         ],
         "cooldown_days": 4, "min_rel": 15},
        {"id": "eli_cafe_01", "npc": "eli", "type": "interactive",
         "location": "location_cafe", "hours": [9, 10, 11],
         "text": "Eli is at a corner table with her laptop, headphones on one ear.",
         "choices": [
             {"label": "Join her for a bit",    "rel_gain": 3, "time": 1},
             {"label": "Just grab your coffee", "rel_gain": 0, "time": 0},
         ],
         "cooldown_days": 4, "min_rel": 20},
        {"id": "rena_kitchen_01", "npc": "rena", "type": "ambient",
         "location": "location_kitchen", "hours": [15, 16, 17],
         "text": "Rena is checking inventory with a clipboard, muttering something under her breath.",
         "cooldown_days": 4},
        {"id": "marcus_nora_cafe_01", "npcs": ["marcus", "nora"], "type": "interactive",
         "location": "location_cafe", "hours": [11, 12],
         "text": "Marcus and Nora are at a table together, mid-debate about something.",
         "choices": [
             {"label": "Join them",  "rel_gain": 2, "time": 1, "both": True},
             {"label": "Leave them", "rel_gain": 0, "time": 0},
         ],
         "cooldown_days": 7, "min_rel": 20},
        {"id": "zoe_gallery_park_01", "npc": "zoe", "type": "ambient",
         "location": "location_park", "hours": [14, 15, 16],
         "text": "Zoe has a small painting propped against the bench. She's studying it critically.",
         "cooldown_days": 5},
        {"id": "kai_gym_01", "npc": "kai", "type": "interactive",
         "location": "location_gym", "hours": [8, 9, 10, 16, 17],
         "text": "Kai is spotting someone on the bench press, calling out encouragement.",
         "choices": [
             {"label": "Work in nearby", "rel_gain": 2, "time": 1},
             {"label": "Nod and train",  "rel_gain": 0, "time": 0},
         ],
         "cooldown_days": 4, "min_rel": 15},
    ]

    def _encounter_on_cooldown(tmpl_id):
        last = max((h["day"] for h in store.npc_encounter_history if h["template_id"] == tmpl_id), default=-99)
        tmpl = next((t for t in NPC_ENCOUNTER_TEMPLATES if t["id"] == tmpl_id), {})
        return store.day - last < tmpl.get("cooldown_days", 3)

    def check_location_encounter(location_id):
        if (store.npc_encounter_last_day == store.day and
                store.npc_encounter_daily_count >= 1):
            return None
        current_hour = int(store.hour)
        eligible = []
        for t in NPC_ENCOUNTER_TEMPLATES:
            if t["location"] != location_id: continue
            if current_hour not in t["hours"]: continue
            if _encounter_on_cooldown(t["id"]): continue
            # Single-NPC check
            npc_id = t.get("npc")
            if npc_id:
                if not getattr(store, npc_id + "_met", False): continue
            else:
                # Multi-NPC: check first NPC in list
                npcs = t.get("npcs", [])
                if npcs and not getattr(store, npcs[0] + "_met", False): continue
            # Relationship gate
            min_rel = t.get("min_rel", 0)
            if min_rel > 0 and npc_id:
                aff = getattr(store, NPC_DATA.get(npc_id, {}).get("aff", "_x"), 0)
                if aff < min_rel: continue
            eligible.append(t)
        if not eligible: return None
        import random as _r
        _rng = _r.Random(store.day * 100 + int(store.hour) + hash(location_id) % 1000)
        if _rng.random() > 0.45: return None
        return _rng.choice(eligible)

    def record_encounter(tmpl_id):
        store.npc_encounter_history = list(store.npc_encounter_history) + [
            {"template_id": tmpl_id, "day": store.day}]
        if store.npc_encounter_last_day != store.day:
            store.npc_encounter_last_day = store.day
            store.npc_encounter_daily_count = 0
        store.npc_encounter_daily_count += 1

    def _apply_encounter_choice_wrapper(enc, choice):
        """Wrapper to call _apply_encounter_choice via Function(); returns None."""
        _apply_encounter_choice(enc, choice)

    def _apply_encounter_choice(enc, choice):
        """Apply relationship and time effects from an encounter choice."""
        rel_gain = choice.get("rel_gain", 0)
        time_cost = choice.get("time", 0)
        if time_cost > 0:
            spend_time(time_cost)
        if choice.get("both"):
            # Multi-NPC encounter — apply to all listed NPCs
            for npc_id in enc.get("npcs", []):
                if rel_gain > 0:
                    aff_var = NPC_DATA.get(npc_id, {}).get("aff")
                    if aff_var:
                        setattr(store, aff_var, min(100, getattr(store, aff_var, 0) + rel_gain))
        else:
            npc_id = enc.get("npc")
            if npc_id and rel_gain > 0:
                aff_var = NPC_DATA.get(npc_id, {}).get("aff")
                if aff_var:
                    setattr(store, aff_var, min(100, getattr(store, aff_var, 0) + rel_gain))


# Encounter display label.
# Usage: $ _cur_enc = check_location_encounter("location_foo")
#        if _cur_enc: call run_encounter(_cur_enc)
label run_encounter(enc):
    $ record_encounter(enc["id"])
    $ _enc_text = enc["text"]
    "[_enc_text]"
    if enc.get("type") == "interactive" and enc.get("choices"):
        $ _enc_c0_lbl  = enc["choices"][0]["label"]
        $ _enc_c1_lbl  = enc["choices"][1]["label"]
        $ _enc_choice  = None
        menu:
            "[_enc_c0_lbl]":
                $ _enc_choice = enc["choices"][0]
            "[_enc_c1_lbl]":
                $ _enc_choice = enc["choices"][1]
        if _enc_choice is not None:
            $ _apply_encounter_choice(enc, _enc_choice)
    return
