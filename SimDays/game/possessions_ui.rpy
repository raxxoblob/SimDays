# Phase 69 UI — the Possessions app (phone) and its computer wrapper.
#
# Tabs: Keepsakes / Artwork / Gear / Bests / To Earn.
#   Artwork reads player_artworks (Phase 65) — never copied.
#   Gear reads owned_home_items() (Phase 61/62) — never copied. It links out to
#   the existing Gear screen rather than re-implementing equipping.
#   "To Earn" is the anticipation half: what exists and how you get it.

init python:

    P69_TABS = [
        ("keepsakes", "Kept"),
        ("artwork",   "Art"),
        ("gear",      "Gear"),
        ("bests",     "Bests"),
        ("locked",    "To Earn"),
    ]

    def _p69_kept():
        """Keepsakes and collectibles, newest first."""
        items = [p for p in store.player_possessions
                 if p.get("category") in ("keepsake", "collectible")]
        return sorted(items, key=lambda p: (not p.get("featured"), -p.get("acquired_day", 0)))

    def _p69_swatch(item_id):
        cat = POSSESSION_CATALOG.get(item_id, {})
        return POSSESSION_CATEGORY_COLOR.get(cat.get("category", "keepsake"), "#7a9ab8")

    def _p69_sell_wrapper(instance_id):
        """Function() wrapper — returns None."""
        sell_possession(instance_id)
        store._selected_possession = None

    def _p69_feature_wrapper(instance_id, value):
        feature_possession(instance_id, value)


# ── Shared body: used by both the phone app and the computer app ──────────────
screen p69_possessions_body(width, height):
    $ _kept = _p69_kept()

    vbox:
        spacing 8
        xsize width

        # Tabs
        hbox:
            spacing 4
            xalign 0.5
            for _tid, _tlbl in P69_TABS:
                textbutton _tlbl:
                    action [SetVariable("_possessions_tab", _tid),
                            SetVariable("_selected_possession", None)]
                    background ("#1e3a5f" if _possessions_tab == _tid else "#141c26")
                    padding (8, 4)
                    text_font ACT_FONT text_size 12
                    text_color ("#ffffff" if _possessions_tab == _tid else "#7a9ab8")
                    text_hover_color "#ffffff"

        # Detail panel for the selected keepsake
        $ _sel = possession_by_id(_selected_possession) if _selected_possession else None
        if _sel:
            $ _selcat = POSSESSION_CATALOG.get(_sel["item_id"], {})
            frame:
                xfill True
                background Solid("#ffffff12")
                padding (12, 10)
                vbox:
                    spacing 4
                    xfill True
                    text _selcat.get("name", _sel["item_id"]):
                        font PROFILE_FONT size 14 color "#f0ece4"
                    if _selcat.get("description"):
                        text _selcat["description"] font ACT_FONT size 12 color "#9fb6d6"
                    text ("Acquired: day %d" % (_sel.get("acquired_day", 0) + 1)):
                        font ACT_FONT size 11 color "#4a6080"
                    text ("Source: %s" % _sel.get("acquired_source", "unknown")):
                        font ACT_FONT size 11 color "#4a6080"
                    hbox:
                        spacing 8
                        textbutton ("Unfeature" if _sel.get("featured") else "Feature"):
                            action Function(_p69_feature_wrapper, _sel["id"],
                                            not _sel.get("featured"))
                            background "#1a2a3a" hover_background "#1e3a5f" padding (10, 4)
                            text_font ACT_FONT text_size 11 text_color "#5bcafa"
                        if _selcat.get("sellable") and not _sel.get("featured"):
                            textbutton ("Sell ($%d)" % _selcat.get("sell_value", 0)):
                                action Function(_p69_sell_wrapper, _sel["id"])
                                background "#1a2a3a" hover_background "#1e3a5f" padding (10, 4)
                                text_font ACT_FONT text_size 11 text_color "#ffd66a"
                        textbutton "Close":
                            action SetVariable("_selected_possession", None)
                            background None padding (8, 4)
                            text_font ACT_FONT text_size 11 text_color "#7a9ab8"

        viewport:
            xfill True
            ysize height
            mousewheel True
            scrollbars "vertical"
            vbox:
                spacing 6
                xfill True

                # ── Keepsakes ────────────────────────────────────────────────
                if _possessions_tab == "keepsakes":
                    if not _kept:
                        text "Nothing kept yet. Win something.":
                            font ACT_FONT size 12 color "#4a6080"
                    for _p in _kept:
                        $ _c = POSSESSION_CATALOG.get(_p["item_id"], {})
                        $ _icon = possession_icon(_c.get("icon_key", "_fallback"))
                        button:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                            padding (10, 8)
                            action SetVariable("_selected_possession", _p["id"])
                            hbox:
                                spacing 10
                                if _icon:
                                    add _icon xysize (36, 36) yalign 0.5
                                else:
                                    add Solid(_p69_swatch(_p["item_id"])) xysize (6, 34) yalign 0.5
                                vbox:
                                    spacing 2
                                    text _c.get("name", _p["item_id"]):
                                        font PROFILE_FONT size 13 color "#cfe0f5"
                                    hbox:
                                        spacing 8
                                        text ("Day %d" % (_p.get("acquired_day", 0) + 1)):
                                            font ACT_FONT size 11 color "#4a6080"
                                        if _p.get("featured"):
                                            text "Featured" font ACT_FONT size 11 color "#ffd66a"

                # ── Artwork (read-only view of player_artworks) ───────────────
                elif _possessions_tab == "artwork":
                    if not player_artworks:
                        text "No finished pieces yet." font ACT_FONT size 12 color "#4a6080"
                    else:
                        text ("%d pieces  ·  %d on the wall"
                              % (len(player_artworks), displayed_artwork_count())):
                            font ACT_FONT size 11 color "#7a9ab8"
                    for _a in reversed(player_artworks):
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 8)
                            vbox:
                                spacing 2
                                text ("%s — %s" % (_a["subject"], art_quality_label(_a["quality"]))):
                                    font PROFILE_FONT size 13 color "#cfe0f5"
                                hbox:
                                    spacing 8
                                    text ("Day %d" % (_a["day"] + 1)) font ACT_FONT size 11 color "#4a6080"
                                    text ("$%d" % _a["estimated_value"]) font ACT_FONT size 11 color "#7fd06a"
                                    if _a.get("exhibited_as"):
                                        text _a["exhibited_as"] font ACT_FONT size 11 color "#ffd66a"
                    textbutton "Open the art log":
                        action [Hide("phone_possessions_scr"), Show("my_artworks_scr")]
                        background None
                        text_font ACT_FONT text_size 12 text_color "#5bcafa"

                # ── Gear (read-only view of the Phase 61/62 inventory) ────────
                elif _possessions_tab == "gear":
                    $ _gear = owned_home_items()
                    text ("%d owned items  ·  %d equipped"
                          % (len(_gear), len(all_equipped_items()))):
                        font ACT_FONT size 11 color "#7a9ab8"
                    for _g in sorted(_gear, key=lambda i: ITEM_CATALOG[i]["label"]):
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 6)
                            hbox:
                                spacing 8
                                text ITEM_CATALOG[_g]["label"]:
                                    font PROFILE_FONT size 12 color "#cfe0f5"
                                text item_condition(_g):
                                    font ACT_FONT size 11 color "#7a9ab8"
                                if is_equipped(_g):
                                    text "· in use" font ACT_FONT size 11 color "#7fd06a"
                    textbutton "Manage gear":
                        action [Hide("phone_possessions_scr"), Show("equipment_scr")]
                        background None
                        text_font ACT_FONT text_size 12 text_color "#5bcafa"

                # ── Personal bests + accomplishments ──────────────────────────
                elif _possessions_tab == "bests":
                    text "Personal bests" font PROFILE_FONT size 13 color "#9fb6d6"
                    if not player_personal_bests:
                        text "Nothing recorded yet." font ACT_FONT size 12 color "#4a6080"
                    for _k in sorted(player_personal_bests):
                        $ _pb = personal_best_display(_k)
                        if _pb:
                            hbox:
                                xfill True
                                text _pb[0] font ACT_FONT size 12 color "#7a9ab8"
                                text _pb[1] font PROFILE_FONT size 12 color "#ffd66a" xalign 1.0
                    null height 6
                    text "Accomplishments" font PROFILE_FONT size 13 color "#9fb6d6"
                    if not player_accomplishments:
                        text "Nothing yet." font ACT_FONT size 12 color "#4a6080"
                    for _acc in accomplishments_by_category():
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 6)
                            vbox:
                                spacing 2
                                text _acc["title"] font PROFILE_FONT size 12 color "#cfe0f5"
                                text _acc["description"] font ACT_FONT size 11 color "#7a9ab8"
                                text ("Day %d" % (_acc["day"] + 1)) font ACT_FONT size 11 color "#4a6080"

                # ── To earn ──────────────────────────────────────────────────
                else:
                    text "Out there somewhere:" font ACT_FONT size 11 color "#7a9ab8"
                    for _iid, _d in unearned_possessions():
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 6)
                            vbox:
                                spacing 2
                                text _d["name"] font PROFILE_FONT size 12 color "#6a7f96"
                                text _d.get("hint", "") font ACT_FONT size 11 color "#4a6080"


screen phone_possessions_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Possessions" font PROFILE_FONT size 20 color "#ffffff" xalign 0.5
            null height 6
            use p69_possessions_body(PHONE_SCR_W - 24, 560)
            null height 6
            textbutton "Back":
                action [Hide("phone_possessions_scr"), Show("phone_home")]
                xalign 0.5
                text_font ACT_FONT text_size 15 text_color "#9fb6d6" text_hover_color "#ffffff"


# Computer version — reuses the same body inside the Phase 64 app shell.
screen capp_possessions():
    use computer_app_shell("Collection"):
        use p69_possessions_body(1500, 690)
