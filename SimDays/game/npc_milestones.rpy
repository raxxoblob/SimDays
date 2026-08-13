# NPC personal milestone chains (Section 24J).
# check_npc_milestones() is called from new_day() in data.rpy.

init python:

    NPC_MILESTONE_CHAINS = {
        "nora": [
            {"id": "nora_ms_1", "day_trigger": 7,  "req_flag": None,
             "social_post": "Starting the evening management module this week.",
             "topic_unlock": "nora_management_start"},
            {"id": "nora_ms_2", "day_trigger": 21, "req_flag": "nora_ms_1",
             "social_post": "Halfway through. Harder than I expected.",
             "topic_unlock": "nora_management_mid"},
            {"id": "nora_ms_3", "day_trigger": 42, "req_flag": "nora_ms_2",
             "social_post": "Done. I don't know what comes next but at least I finished something.",
             "topic_unlock": "nora_management_done"},
        ],
        "marcus": [
            {"id": "marcus_ms_1", "day_trigger": 10, "req_flag": None,
             "social_post": "Static's new menu is a mess. Sorting it out this week.",
             "topic_unlock": "marcus_static_menu"},
            {"id": "marcus_ms_2", "day_trigger": 28, "req_flag": "marcus_ms_1",
             "social_post": "New drink on the board Friday. Come try it.",
             "topic_unlock": "marcus_new_drink"},
        ],
        "zoe": [
            {"id": "zoe_ms_1", "day_trigger": 8,  "req_flag": None,
             "social_post": "Started something new. Haven't shown anyone yet.",
             "topic_unlock": "zoe_new_piece"},
            {"id": "zoe_ms_2", "day_trigger": 25, "req_flag": "zoe_ms_1",
             "social_post": "It might actually be good. I hate that I can't tell.",
             "topic_unlock": "zoe_piece_progress"},
            {"id": "zoe_ms_3", "day_trigger": 45, "req_flag": "zoe_ms_2",
             "social_post": "Submitted it to a local show. Don't ask me how it went.",
             "topic_unlock": "zoe_piece_submitted"},
        ],
        "eli": [
            {"id": "eli_ms_1", "day_trigger": 12, "req_flag": None,
             "social_post": "Side project is finally taking shape.",
             "topic_unlock": "eli_side_project_start"},
            {"id": "eli_ms_2", "day_trigger": 30, "req_flag": "eli_ms_1",
             "social_post": "Showed it to someone. They had notes. They were right.",
             "topic_unlock": "eli_side_project_review"},
        ],
        "sam": [
            {"id": "sam_ms_1", "day_trigger": 5,  "req_flag": None,
             "social_post": "New training block starts Monday. Three months minimum.",
             "topic_unlock": "sam_training_block"},
            {"id": "sam_ms_2", "day_trigger": 28, "req_flag": "sam_ms_1",
             "social_post": "First month done. Body cooperating. Good sign.",
             "topic_unlock": "sam_training_month"},
        ],
    }

    def _add_npc_social_post(npc_id, post_id, text):
        posts = list(store.social_feed_posts)
        if any(p["id"] == post_id for p in posts): return
        posts.insert(0, {"id": post_id, "npc_id": npc_id, "text": text, "day": store.day})
        store.social_feed_posts = posts

    def check_npc_milestones():
        for npc_id, chain in NPC_MILESTONE_CHAINS.items():
            for ms in chain:
                if getattr(store, "npc_ms_" + ms["id"], False): continue
                if ms.get("req_flag") and not getattr(store, "npc_ms_" + ms["req_flag"], False): continue
                if store.day < ms["day_trigger"]: continue
                setattr(store, "npc_ms_" + ms["id"], True)
                if ms.get("social_post"):
                    _add_npc_social_post(npc_id, ms["id"], ms["social_post"])
