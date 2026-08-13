# Project evaluation and result display.
# evaluate_project() is the single scoring function for all project domains.

init python:

    def evaluate_project(project, preparation=None):
        """Returns a result dict: {score, rating, components, pay_modifier, rep_gain, trust_change}"""
        if preparation is None:
            preparation = {}
        score = 50
        components = []

        # Phase 60B: skill vs difficulty differential
        difficulty = project.get("difficulty", project.get("required_skill", 1))
        skill_key  = _project_domain_skill(project.get("domain", "programming"))
        player_lvl = skill_val(skill_key)
        skill_diff = (player_lvl - difficulty) * 4
        skill_diff = max(-20, min(20, skill_diff))
        if skill_diff != 0:
            score += skill_diff
            components.append(("Skill vs difficulty", "%+d" % skill_diff))

        # Session quality accumulator
        q_bonus = min(20, project.get("quality_bonus", 0))
        q_penalty = min(10, project.get("quality_penalty", 0))
        if q_bonus:
            score += q_bonus
            components.append(("Session quality bonus", "+%d" % q_bonus))
        if q_penalty:
            score -= q_penalty
            components.append(("Session quality penalty", "-%d" % q_penalty))

        score = max(0, min(100, score))

        # Deadline bonus
        deadline_day = project.get("deadline_day", store.day)
        days_early = deadline_day - store.day
        if days_early >= 2:
            score += 10
            components.append(("Delivered early", "+10"))
        elif days_early >= 0:
            score += 5
            components.append(("Delivered on time", "+5"))
        else:
            late_pen = min(20, abs(days_early) * 5)
            score -= late_pen
            components.append(("Late delivery", "-%d" % late_pen))

        # Preparation bonuses
        if preparation.get("tested"):
            score += 10
            components.append(("Test and review completed", "+10"))
        if preparation.get("polished"):
            score += 5
            components.append(("Polished", "+5"))
        if preparation.get("client_brief_reviewed"):
            score += 3
            components.append(("Brief reviewed", "+3"))

        # Repeat client trust
        client_id = project.get("client_id") or _client_id_from_name(project.get("client", ""))
        if client_id:
            trust = store.client_profiles.get(client_id, {}).get("trust", 0)
            trust_bonus = min(8, trust // 10)
            if trust_bonus > 0:
                score += trust_bonus
                components.append(("Client trust", "+%d" % trust_bonus))

        # Execution roll: variable result on top of deterministic base
        adj_score, exec_result = _freelance_execution_roll(project, score)
        tier_delta = adj_score - score
        if tier_delta != 0:
            components.append(("Execution", ("%+d" % tier_delta)))
        score = adj_score
        rating = project_score_to_rating(score)
        pay_mod = {"S": 1.10, "A": 1.05, "B": 1.0, "C": 1.0, "D": 1.0}.get(rating, 1.0)
        rep_gain_base = _project_rep_gain(rating, difficulty)
        trust_change = {"S": 8, "A": 5, "B": 2, "C": -2, "D": -6}.get(rating, 0)
        return {
            "score": score, "rating": rating, "components": components,
            "pay_modifier": pay_mod, "rep_gain": rep_gain_base,
            "trust_change": trust_change,
            "exec_result":  exec_result,   # roll_check dict for result screen
        }

    # Phase 64 reputation pacing. Was rating-only {S:12,A:8,B:5,C:2,D:0}, which
    # saturated freelance_reputation at 100 in ~20 days and made every min_rep
    # tier gate dead by the time the player could read them. Now 0-4 per project,
    # weighted toward harder contracts (rarer work = more prestige).
    # At ~0.5 projects/day: rep ~10 by day 14, ~25 by day 30, ~55 by day 60,
    # ~95 by day 90 — the gates stay live through the whole midgame.
    _PROJECT_REP_BY_RATING = {"S": 2, "A": 2, "B": 1, "C": 1, "D": 0}

    def _project_rep_gain(rating, difficulty):
        base = _PROJECT_REP_BY_RATING.get(rating, 1)
        if base == 0:
            return 0                      # a D delivery earns no standing
        if difficulty >= 8:
            return base + 2
        if difficulty >= 5:
            return base + 1
        return base

    def project_score_to_rating(score):
        if score >= 95: return "S"
        if score >= 80: return "A"
        if score >= 65: return "B"
        if score >= 50: return "C"
        return "D"

    def _project_domain_skill(domain):
        return {"programming": "prog", "music": "music", "art": "art",
                "mechanics": "mech"}.get(domain, "prog")

    def _client_id_from_name(name):
        return name.lower().replace(" ", "_").replace(".", "") if name else None

    def add_project_to_portfolio(project, result):
        eid = "project_%s_day%d" % (project.get("template_id", "custom"), store.day)
        record_game_event(eid, "project", project.get("title", "Project"),
            summary=True, journal=result["rating"] in ("S", "A"),
            portfolio_domain=project.get("domain", "programming"),
            metadata={
                "client": project.get("client", ""),
                "client_id": project.get("client_id") or _client_id_from_name(project.get("client", "")),
                "pay": project.get("pay", 0),
                "rating": result["rating"],
                "score": result["score"],
                "template_id": project.get("template_id", ""),
                "required_skill": project.get("required_skill", 1),
                "major": project.get("required_skill", 1) >= 7,
            })

    def _freelance_submit_wrapper():
        """Calls freelance_submit() and stores result in _pending_project_result. Returns None."""
        freelance_submit()
        # freelance_submit() now stores _pending_project_result itself

    def _freelance_negotiate_wrapper(template_id):
        """Try negotiate +15% from a screen Action. Returns None (screens discard it)."""
        t = next((x for x in _all_freelance_templates() if x["id"] == template_id), None)
        if t is None: return
        neg = negotiate_freelance_rate(t, target_pct=1.15)
        if neg.get("withdrawn"):
            renpy.notify("The client withdrew the offer.")
            store.freelance_offers = [x for x in store.freelance_offers if x != template_id]
            return
        if neg["success"]:
            accept_freelance(template_id, override_pay=int(t["pay"] * 1.15))
        else:
            renpy.notify(neg["response"])


# ── Project result screen ─────────────────────────────────────────────────────
screen project_result_scr(result, project):
    modal True
    add "#000000cc"
    frame:
        xalign 0.5
        yalign 0.4
        xsize 600
        background "#12161ef8"
        padding (28, 22, 28, 22)
        vbox:
            spacing 12
            # Header
            $ _r_colour = {"S": "#ffd66a", "A": "#7fd06a", "B": "#5bcafa", "C": "#8fb0d0", "D": "#e8a24d"}.get(result["rating"], "#cfe0f5")
            text ("PROJECT COMPLETED — RATING  " + result["rating"]):
                font PROFILE_FONT size 24 color _r_colour xalign 0.5
            null height 4
            # Component breakdown
            if result["components"]:
                for _comp_label, _comp_val in result["components"]:
                    hbox:
                        spacing 8
                        xfill True
                        text _comp_label font ACT_FONT size 14 color "#cfe0f5" xsize 340
                        text _comp_val font PROFILE_FONT size 14 color "#7fd06a" xalign 1.0
            null height 4
            # Final quality
            hbox:
                spacing 8
                xfill True
                text "Final quality" font PROFILE_FONT size 15 color "#9fb6d6" xsize 340
                text ("%d / 100" % result["score"]) font PROFILE_FONT size 15 color _r_colour xalign 1.0
            null height 2
            # Pay
            if project.get("pay", 0) > 0:
                hbox:
                    spacing 8
                    xfill True
                    text "Payment (queued)" font ACT_FONT size 14 color "#9fb6d6" xsize 340
                    text ("$%d" % project.get("pay", 0)) font PROFILE_FONT size 14 color "#ffd66a" xalign 1.0
            # Reputation
            if result["rep_gain"] > 0:
                hbox:
                    spacing 8
                    xfill True
                    text "Reputation" font ACT_FONT size 14 color "#9fb6d6" xsize 340
                    text ("+%d" % result["rep_gain"]) font PROFILE_FONT size 14 color "#7fd06a" xalign 1.0
            # Execution roll tier (if present)
            if result.get("exec_result"):
                $ _er = result["exec_result"]
                hbox:
                    spacing 8
                    xfill True
                    text "Execution" font ACT_FONT size 14 color "#9fb6d6" xsize 340
                    text tier_label(_er["tier"]) font ACT_FONT size 14 color tier_color(_er["tier"]) xalign 1.0
            # Portfolio
            text "Added to portfolio." font ACT_FONT size 13 color "#4a8a6a" xalign 0.5
            null height 6
            textbutton "Continue":
                xalign 0.5
                action Return()
                background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20, 20, 20)
                xpadding 30 ypadding 10
                text_font ACT_FONT text_size 18 text_color "#cfe0f5" text_hover_color "#ffffff"


label show_project_result:
    if store._pending_project_result is not None:
        $ _pr = store._pending_project_result
        call screen project_result_scr(_pr["result"], _pr["project"])
        $ store._pending_project_result = None
    return
