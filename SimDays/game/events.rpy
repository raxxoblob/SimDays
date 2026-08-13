# Central event logger — record_game_event routes all trackable moments here.
# Consumed by: day summary overlay, player journal, player portfolio.

init python:

    def record_game_event(event_id, category, title, day=None, summary=True,
                          journal=False, portfolio_domain=None, metadata=None):
        """Central event recorder. All systems route through here.
        category: "money", "skill", "relation", "project", "career", "purchase", "journal"
        summary=True: adds to current_day_activity (day summary popup)
        journal=True: adds to player_journal
        portfolio_domain: if set, adds to player_portfolio
        metadata: plain dict (strings/numbers/lists/dicts/bools only)
        """
        if day is None:
            day = store.day
        if metadata is None:
            metadata = {}

        if summary:
            _acts = list(store.current_day_activity)
            _acts.append({
                "id": event_id,
                "category": category,
                "title": title,
                "day": day,
                "metadata": metadata,
            })
            store.current_day_activity = _acts

        if journal:
            _jl = list(store.player_journal)
            _jl.append({
                "id": event_id,
                "day": day,
                "category": category,
                "title": title,
                "metadata": metadata,
            })
            store.player_journal = _jl

        if portfolio_domain:
            _pf = dict(store.player_portfolio)
            _pf[event_id] = {
                "id": event_id,
                "domain": portfolio_domain,
                "title": title,
                "day": day,
                "metadata": metadata,
            }
            store.player_portfolio = _pf


label check_levelup_notices:
    python:
        _notices = list(store._pending_levelup_notices)
        store._pending_levelup_notices = []
    for _notice in _notices:
        call screen skill_levelup_scr(_notice)
    return


screen skill_levelup_scr(notice):
    modal True
    add "#000000cc"
    frame:
        xalign 0.5
        yalign 0.4
        xsize 560
        background "#12161ef8"
        padding (28, 22, 28, 22)
        vbox:
            spacing 14
            # Header
            text (notice["label"].upper() + "  " + str(notice["new_level"] - 1) + " → " + str(notice["new_level"])):
                font PROFILE_FONT size 26 color "#ffd66a" xalign 0.5
            null height 4
            # Benefits list
            if notice["benefits"]:
                for _b_desc, _b_val in notice["benefits"]:
                    hbox:
                        spacing 8
                        xfill True
                        text _b_desc font ACT_FONT size 16 color "#cfe0f5" xsize 330
                        text _b_val font PROFILE_FONT size 16 color "#7fd06a" xalign 1.0
            else:
                text "New possibilities unlocked." font ACT_FONT size 15 color "#7a9ab8" xalign 0.5
            null height 4
            # Next unlock teaser
            $ _next_unlock = get_next_skill_unlock(notice["key"])
            if _next_unlock:
                text ("Next: " + _next_unlock) font ACT_FONT size 13 color "#4a6080" xalign 0.5
            null height 6
            textbutton "Continue":
                xalign 0.5
                action Return()
                background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20, 20, 20)
                xpadding 30 ypadding 10
                text_font ACT_FONT text_size 18 text_color "#cfe0f5" text_hover_color "#ffffff"
