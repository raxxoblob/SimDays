# Returning client system — client profiles, trust, and repeat offers.

init python:

    RETURNING_CLIENT_DEFS = {
        "crane_logistics": {
            "display_name": "Crane Logistics",
            "domain": "programming",
            "initial_project_ids": ["script_01"],
            "follow_up_projects": [
                {"id": "crane_followup_01", "title": "Expand automation system",
                 "min_skill": 40, "min_rep": 5, "hours": 5, "days": 5, "pay": 300, "exp": 150,
                 "mail_on_complete": "The expanded script is saving us real time every week. Good work."},
                {"id": "crane_followup_02", "title": "Database integration",
                 "min_skill": 60, "min_rep": 12, "hours": 7, "days": 6, "pay": 460, "exp": 220,
                 "mail_on_complete": "Exactly what we needed. We'll be in touch for the next phase."},
            ],
        },
        "hazel_creative": {
            "display_name": "Hazel Creative",
            "domain": "programming",
            "initial_project_ids": ["wp_plugin_01"],
            "follow_up_projects": [
                {"id": "hazel_followup_01", "title": "Custom booking widget",
                 "min_skill": 40, "min_rep": 5, "hours": 5, "days": 6, "pay": 290, "exp": 140,
                 "mail_on_complete": "The client loved it! Let us know when you're free again."},
                {"id": "hazel_followup_02", "title": "Agency portfolio site",
                 "min_skill": 60, "min_rep": 12, "hours": 8, "days": 7, "pay": 500, "exp": 240,
                 "mail_on_complete": "Stunning work. We're recommending you to a contact."},
            ],
        },
        "pulse_digital": {
            "display_name": "Pulse Digital",
            "domain": "programming",
            "initial_project_ids": ["rest_api_01"],
            "follow_up_projects": [
                {"id": "pulse_followup_01", "title": "API rate limiting and caching",
                 "min_skill": 50, "min_rep": 8, "hours": 6, "days": 5, "pay": 380, "exp": 180,
                 "mail_on_complete": "Performance is way up. You clearly know what you're doing."},
                {"id": "pulse_followup_02", "title": "Full backend service",
                 "min_skill": 70, "min_rep": 16, "hours": 9, "days": 8, "pay": 620, "exp": 280,
                 "mail_on_complete": "This is exactly the quality we were looking for. Call it a standing arrangement."},
            ],
        },
    }

    # Flat list of all follow-up templates for offer-list lookup.
    # Format matches FREELANCE_TEMPLATES so the computer screen can use them.
    _RETURNING_CLIENT_TEMPLATES = []
    for _cid, _cdef in RETURNING_CLIENT_DEFS.items():
        for _fp in _cdef["follow_up_projects"]:
            _RETURNING_CLIENT_TEMPLATES.append({
                "id": _fp["id"],
                "title": _fp["title"],
                "client": _cdef["display_name"],
                "client_id": _cid,
                "min_skill": _fp["min_skill"],
                "min_rep": _fp["min_rep"],
                "hours": _fp["hours"],
                "days": _fp["days"],
                "pay": _fp["pay"],
                "exp": _fp["exp"],
                "mail_on_complete": _fp.get("mail_on_complete", ""),
            })
    del _cid, _cdef, _fp   # cleanup loop vars


    def ensure_client_profile(client_id, display_name="", domain="programming"):
        if client_id not in store.client_profiles:
            d = dict(store.client_profiles)
            d[client_id] = {
                "client_id": client_id, "display_name": display_name, "domain": domain,
                "completed_projects": 0, "failed_projects": 0, "total_paid": 0,
                "trust": 20, "average_score": 0, "last_project_day": -1,
                "next_offer_day": -1, "repeat_client_unlocked": False,
                "referred_clients": [], "active_project_id": None,
            }
            store.client_profiles = d

    def update_client_after_project(client_id, result):
        ensure_client_profile(client_id)
        d = dict(store.client_profiles)
        c = dict(d[client_id])
        c["completed_projects"] += 1
        c["total_paid"] = c.get("total_paid", 0) + result.get("pay", 0)
        old_avg = c.get("average_score", 0)
        total = c["completed_projects"]
        c["average_score"] = int((old_avg * (total - 1) + result["score"]) / total)
        c["trust"] = max(0, min(100, c.get("trust", 20) + result.get("trust_change", 0)))
        c["last_project_day"] = store.day
        cooldown = 7 if result["rating"] in ("S", "A") else 10
        c["next_offer_day"] = store.day + cooldown
        if c["trust"] >= 30 and c["completed_projects"] >= 2:
            c["repeat_client_unlocked"] = True
        d[client_id] = c
        store.client_profiles = d

    def client_can_return(client_id):
        c = store.client_profiles.get(client_id, {})
        return (c.get("repeat_client_unlocked") and
                store.day >= c.get("next_offer_day", 999) and
                c.get("trust", 0) >= 20 and
                c.get("active_project_id") is None)

    def client_trust_level(client_id):
        trust = store.client_profiles.get(client_id, {}).get("trust", 0)
        if trust >= 70: return "trusted"
        if trust >= 40: return "familiar"
        return "new"

    def _returning_client_next_project(client_id):
        """Returns the next unlocked follow-up project template dict, or None."""
        cdef = RETURNING_CLIENT_DEFS.get(client_id)
        if not cdef:
            return None
        done_ids = set(h["template_id"] for h in store.freelance_history)
        for fp in cdef["follow_up_projects"]:
            if fp["id"] not in done_ids:
                return fp
        return None

    def check_returning_client_offers():
        """Called from new_day(). Queues follow-up offers for eligible returning clients."""
        for client_id, cdef in RETURNING_CLIENT_DEFS.items():
            if not client_can_return(client_id):
                continue
            fp = _returning_client_next_project(client_id)
            if fp is None:
                continue
            # Don't queue if already in active offers
            if fp["id"] in store.freelance_offers:
                continue
            # Check skill + rep gate
            if skill_val("prog") < fp["min_skill"]:
                continue
            if store.freelance_reputation < fp["min_rep"]:
                continue
            # Mark client as having an active project offered
            d = dict(store.client_profiles)
            c = dict(d.get(client_id, {}))
            c["active_project_id"] = fp["id"]
            d[client_id] = c
            store.client_profiles = d
            # Add to freelance offers
            store.freelance_offers = list(store.freelance_offers) + [fp["id"]]
            queue_mail(
                cdef["display_name"],
                "New project available: " + fp["title"],
                "We have another project we'd like you to handle. Check the freelance board for details.",
                "freelance", store.day,
                "rc_offer_%s_%d" % (fp["id"], store.day))
