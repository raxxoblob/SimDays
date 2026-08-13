# Phase 65 — Painting flow labels and screens.
# Split from painting.rpy the same way home_items_ui.rpy is split from
# home_items.rpy: rules and data on one side, presentation on the other.

# ── Entry point from the home menu ─────────────────────────────────────────────
# The home menu gains exactly ONE line. Everything else lives in this sub-menu,
# so the flat's action list does not grow by six entries as art skill rises.
label painting_menu:
    $ _p65_expired = expire_painting_commissions()
    if _p65_expired:
        "The deadline came and went without the piece being finished. Someone is disappointed, and they were right to be."
    $ _p65_sessions = available_art_sessions()
    $ _p65_comm     = active_painting_commission()
    $ _p65_offer    = painting_commission_offer()
    $ _p65_commission_note = ("%s, due day %d" % (_p65_comm["client"], _p65_comm["deadline_day"] + 1)) if _p65_comm else ""

    menu:
        "The corner with the easel in it."

        "Practice sketching (1h)" if "sketch_practice" in _p65_sessions:
            call do_painting_flow("sketch_practice")
            jump painting_menu

        "Practice painting (2h)" if "paint_practice" in _p65_sessions:
            call do_painting_flow("paint_practice")
            jump painting_menu

        "Paint a still life (2h)" if "still_life" in _p65_sessions:
            call do_painting_flow("still_life")
            jump painting_menu

        "Paint a canvas (3h)" if "canvas" in _p65_sessions:
            call do_painting_flow("canvas")
            jump painting_menu

        "Create a portfolio piece (4h)" if "portfolio_piece" in _p65_sessions:
            call do_painting_flow("portfolio_piece")
            jump painting_menu

        "Work on the commission — [_p65_commission_note]" if _p65_comm is not None:
            call do_commission_flow
            jump painting_menu

        "Check the commission board" if (_p65_offer is not None and _p65_comm is None):
            call commission_board_flow
            jump painting_menu

        "Your artworks" if len(player_artworks) > 0:
            call my_artworks_flow
            jump painting_menu

        "Step away":
            return


# ── One painting session ───────────────────────────────────────────────────────
label do_painting_flow(sid):
    $ _p65_sid  = sid
    $ _p65_s    = ART_SESSIONS[sid]
    $ _p65_subj = _p65_s.get("subject")
    $ _p65_amb  = "safe"
    $ _p65_appr = "normal"

    # Subject choice for canvas / portfolio piece.
    if _p65_s.get("subject") is None:
        call screen art_subject_scr(sid)
        if _return is None:
            return
        $ _p65_subj = _return

    # Ambition band (portfolio piece only) — this is what sets difficulty 45-70.
    if _p65_s.get("ambition"):
        call screen art_ambition_scr(sid, _p65_subj)
        if _return is None:
            return
        $ _p65_amb = _return

    # Distribution preview before committing, for canvas and above (spec §5).
    # Practice is deliberately NOT dramatic: no preview, no approach, just work.
    if _p65_s.get("approach"):
        call screen painting_approach_scr(sid, _p65_subj, _p65_amb)
        if _return is None:
            return
        $ _p65_appr = _return
    elif not _p65_s.get("practice"):
        call screen painting_confirm_scr(sid, _p65_subj)
        if not _return:
            return

    # Materials. Only kit owners pay — improvising is free and simply worse.
    $ _p65_cost = art_material_cost(sid)
    if _p65_cost > 0:
        if not try_spend(_p65_cost, "discretionary"):
            "You're out of board and can't cover a fresh pack."
            return

    $ _p65_res = do_painting(sid, _p65_subj, _p65_appr, _p65_amb)
    $ _p65_subjname = ART_SUBJECTS[_p65_subj]["name"] if _p65_subj else "Study"

    if _p65_s.get("practice"):
        $ _p65_result_line = _practice_flavour(_p65_res)
        "[_p65_result_line]"
        if _p65_res["artwork"] is not None:
            "You look at it again on the way past. That one's worth keeping."
            call artwork_disposition(_p65_res["artwork"]["id"])
        return

    call screen check_result_scr(_p65_res["roll"], title=("%s — %s" % (_p65_subjname, _p65_res["qlabel"])), xtra_lines=_painting_result_lines(_p65_res))
    if _p65_res["artwork"] is not None:
        call artwork_disposition(_p65_res["artwork"]["id"])
    return


# What to do with a piece the moment it comes off the easel.
label artwork_disposition(aid):
    $ _p65_art = artwork_by_id(aid)
    if _p65_art is None:
        return
    $ _p65_artname = _p65_art["subject"]
    $ _p65_val = _p65_art["estimated_value"]
    menu:
        "\"[_p65_artname]\" — you'd put it at about $[_p65_val]."

        "Add it to your portfolio":
            $ update_artwork(aid, in_portfolio=True)
            $ record_game_event("artfolio_%s" % aid, "project", "Portfolio: \"%s\"" % _p65_artname, summary=True, journal=False, portfolio_domain="art", metadata={"artwork": aid})
            "It goes in the folder with the others. A body of work, slowly."

        "Hang it on the wall":
            $ update_artwork(aid, displayed=True)
            "You find a nail and a stretch of wall. The room changes slightly."

        "Put it in storage":
            "It goes behind the wardrobe with the rest of them."
    return


init python:
    def _practice_flavour(res):
        """Practice is quiet. One honest line, keyed to how it actually went."""
        return {
            "critical_failure": "Nothing works today. The proportions are wrong and you know it while you're doing it.",
            "weak":             "An hour of not much. Still, your hand is steadier than it was.",
            "success":          "Steady work. Nothing to keep, but something moved.",
            "great":            "Somewhere in the second half it stops being effort and starts being looking.",
            "critical":         "One of those sessions. You lose track of the time entirely.",
        }[res["tier"]]


# ── Commissions ────────────────────────────────────────────────────────────────
label commission_board_flow:
    $ _p65_offer = painting_commission_offer()
    if _p65_offer is None:
        "Nothing on the board."
        return
    $ _p65_lo, _p65_hi = commission_pay_range(_p65_offer)
    $ _p65_ohrs    = ("%g" % _p65_offer["hours"])
    $ _p65_opay    = _p65_offer["pay"]
    $ _p65_oclient = _p65_offer["client"]
    $ _p65_olabel  = _p65_offer["label"]
    $ _p65_odays   = _p65_offer["days"]
    $ _p65_ochance = commission_chance(_p65_offer)["success_or_better"]
    "[_p65_oclient]: \"[_p65_olabel].\""
    menu:
        "$[_p65_opay] on delivery — $[_p65_lo]-[_p65_hi] depending how it lands. [_p65_ohrs]h of work, [_p65_odays] days to do it. [_p65_ochance]% to meet the brief."
        "Take it":
            $ accept_painting_commission(_p65_offer)
            "You write the date down. That's a real commitment now."
        "Leave it":
            pass
    return


label do_commission_flow:
    $ _p65_comm = active_painting_commission()
    if _p65_comm is None:
        return
    call screen commission_confirm_scr
    if _return is None:
        return
    $ _p65_appr = _return
    $ _p65_cost = art_material_cost("canvas")
    if _p65_cost > 0:
        if not try_spend(_p65_cost, "discretionary"):
            "You can't cover the materials for it right now."
            return
    $ _p65_cres = do_commission_work(_p65_comm, _p65_appr)
    call screen check_result_scr(_p65_cres["roll"], title=("Commission — " + _p65_cres["qlabel"]), xtra_lines=_commission_result_lines(_p65_cres))
    if _p65_cres["tier"] == "critical_failure":
        "They look at it for a long time without saying anything. Then they pay you something, because they said they would."
    elif not _p65_cres["met"]:
        "\"It's — yeah. Thank you.\" They pay less than agreed and you don't argue, because they're right to."
    elif _p65_cres["tier"] in ("great", "critical"):
        "They go quiet, then ask whether you take on more of this sort of thing. You say yes before you've finished thinking about it."
    else:
        "They're pleased. It goes up on their wall while you're still standing there."
    return


# ── My Artworks ────────────────────────────────────────────────────────────────
label my_artworks_flow:
    if not player_artworks:
        "You haven't made anything yet."
        return
    call screen my_artworks_scr
    if _return is None:
        return
    call artwork_actions(_return)
    jump my_artworks_flow


label artwork_actions(aid):
    $ _p65_art = artwork_by_id(aid)
    if _p65_art is None:
        return
    $ _p65_artname  = _p65_art["subject"]
    $ _p65_val      = _p65_art["estimated_value"]
    $ _p65_free     = artwork_is_free(_p65_art)
    # Spec section 7: work you have recorded in your portfolio is not for sale.
    # Submitting to an exhibition is still allowed — that is what a portfolio is for.
    $ _p65_sellable = _p65_free and not _p65_art["in_portfolio"]
    $ _p65_gallery  = art_rep_gate_open("gallery_sale")
    $ _p65_street_p = art_sale_price(_p65_art, "street", preview=True) if _p65_free else 0
    $ _p65_gall_p   = art_sale_price(_p65_art, "gallery", preview=True) if _p65_free else 0
    $ _p65_exhibs   = scheduled_art_exhibitions()
    $ _p65_can_sub  = (_p65_free and art_rep_gate_open("exhibition_entry")
                       and quality_at_least(_p65_art["quality"], "success")
                       and len(_p65_exhibs) > 0)
    $ _p65_can_gift = (not _p65_art["sold"] and not _p65_art["gifted_to"]
                       and not _p65_art["submitted_to"])
    menu:
        "\"[_p65_artname]\" — appraised at $[_p65_val]."

        "Hang it on the wall" if (not _p65_art["displayed"]) and _p65_can_gift:
            $ update_artwork(aid, displayed=True)
            "It goes up. You catch sight of it later and it's still yours, which is a strange feeling."

        "Take it down" if _p65_art["displayed"]:
            $ update_artwork(aid, displayed=False)
            "You take it down. The wall looks bare where it was."

        "Add to portfolio" if not _p65_art["in_portfolio"]:
            $ update_artwork(aid, in_portfolio=True)
            $ record_game_event("artfolio_%s" % aid, "project", "Portfolio: \"%s\"" % _p65_artname, summary=True, journal=False, portfolio_domain="art", metadata={"artwork": aid})
            "Into the folder."

        "Sell it on the street (about $[_p65_street_p], 1h)" if _p65_sellable:
            call sell_artwork_flow(aid, "street")

        "Consign it to the gallery (about $[_p65_gall_p])" if (_p65_sellable and _p65_gallery):
            call sell_artwork_flow(aid, "gallery")

        "Give it to someone" if _p65_can_gift:
            call gift_artwork_flow(aid)

        "Submit it to an exhibition" if _p65_can_sub:
            call submit_artwork_flow(aid)

        "Back":
            pass
    return


label sell_artwork_flow(aid, channel):
    $ _p65_chan = channel
    if _p65_chan == "gallery" and art_market_saturated():
        "The gallery already has two of your pieces out this week. \"I can take it, but not at the price I'd want to give you.\""
    $ _p65_price = sell_artwork(artwork_by_id(aid), _p65_chan)
    if _p65_chan == "street":
        $ spend_time(1)
        "An hour on the pavement with it propped against your knees. Someone stops, haggles a little, and carries it off under one arm. $[_p65_price]."
    else:
        "They take it on consignment, write you a receipt, and it sells inside the week. $[_p65_price]."
    return


label gift_artwork_flow(aid):
    call screen artwork_gift_scr
    if _return is None:
        return
    $ _p65_npc = _return
    $ _p65_delta, _p65_interest = gift_artwork(artwork_by_id(aid), _p65_npc)
    $ _p65_result_line = art_gift_line(_p65_interest)
    $ _p65_npcname = NPC_DATA[_p65_npc]["name"]
    # No show_npc_expr here: the recipient is not necessarily on screen, and a
    # sprite shown from a menu would persist over the home background.
    "You give it to [_p65_npcname]."
    "[_p65_result_line]"
    return


label submit_artwork_flow(aid):
    $ _p65_ev = scheduled_art_exhibitions()[0]
    $ _p65_evtitle = _p65_ev["title"]
    $ update_artwork(aid, submitted_to=_p65_ev["id"])
    $ _p65_artname = artwork_by_id(aid)["subject"]
    "You fill in the entry form for the [_p65_evtitle] and hand \"[_p65_artname]\" across the desk. It's out of your hands now."
    return


# ═══════════════════════════════════════════════════════════════════════════════
# SCREENS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Subject picker ─────────────────────────────────────────────────────────────
screen art_subject_scr(sid):
    modal True
    zorder 215
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 600
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text "What are you painting?" font PROFILE_FONT size 17 color "#9fb6d6" xalign 0.5
            text ("Art Lv %d" % skill_val("art")) font ACT_FONT size 12 color "#ff9f4d" xalign 0.5
            null height 4
            for _sj in ART_SUBJECTS:
                $ _sjd = ART_SUBJECTS[_sj]
                $ _sjok = art_subject_available(_sj)
                button:
                    action Return(_sj)
                    sensitive _sjok
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10, 14, 10)
                    vbox:
                        spacing 3
                        hbox:
                            xfill True
                            text _sjd["name"] font ACT_FONT size 15 color ("#cfe0f5" if _sjok else "#5a6a7a") yalign 0.5
                            if _sjok:
                                text ("Mastery %d" % painting_mastery_points(_sj)) font ACT_FONT size 12 color "#8a6ac0" yalign 0.5 xalign 1.0
                            else:
                                text ("Needs Art %d" % _sjd["min_art"]) font ACT_FONT size 12 color "#5a6a7a" yalign 0.5 xalign 1.0
                        text _sjd["desc"] font ACT_FONT size 11 color "#7a9ab8"
            null height 4
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7, 18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Ambition picker (portfolio piece) ──────────────────────────────────────────
screen art_ambition_scr(sid, subj_id):
    modal True
    zorder 216
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 620
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text "How far are you pushing it?" font PROFILE_FONT size 17 color "#9fb6d6" xalign 0.5
            text "Harder work is worth more. That is the whole trade." font ACT_FONT size 11 color "#7a9ab8" xalign 0.5
            null height 4
            for _aid, _albl, _adiff, _amult, _adesc in ART_AMBITION:
                $ _ach = painting_chance(sid, subj_id, "normal", _aid)
                button:
                    action Return(_aid)
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10, 14, 10)
                    vbox:
                        spacing 3
                        hbox:
                            xfill True
                            text _albl font ACT_FONT size 15 color "#cfe0f5" yalign 0.5
                            text ("Value x%.2f" % _amult) font PROFILE_FONT size 12 color "#ffd66a" yalign 0.5 xalign 1.0
                        text _adesc font ACT_FONT size 11 color "#7a9ab8"
                        hbox:
                            spacing 6
                            text ("Difficulty %d" % art_session_difficulty(sid, subj_id, _aid)) font ACT_FONT size 11 color "#7090b0"
                            text ("Striking+ %d%%" % (_ach["distribution"]["great"] + _ach["distribution"]["critical"])) font ACT_FONT size 11 color "#5bcafa"
            null height 4
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7, 18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Approach + distribution preview ────────────────────────────────────────────
screen painting_approach_scr(sid, subj_id, ambition):
    modal True
    zorder 217
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 600
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 10
            text ("%s — pick your approach" % ART_SUBJECTS[subj_id]["name"]) font PROFILE_FONT size 16 color "#9fb6d6" xalign 0.5
            use art_gear_line()
            null height 4
            for _appr, _albl, _adesc in [
                ("careful",   "Careful",   "Half an hour longer, safer — fewer ruined pieces."),
                ("normal",    "Standard",  "Balanced."),
                ("ambitious", "Ambitious", "Riskier odds, but a top result is worth more."),
            ]:
                $ _ac = painting_chance(sid, subj_id, _appr, ambition)
                button:
                    action Return(_appr)
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 10, 14, 10)
                    vbox:
                        spacing 3
                        hbox:
                            xfill True
                            text _albl font ACT_FONT size 15 color "#cfe0f5" yalign 0.5
                            text ("Striking+ %d%%" % (_ac["distribution"]["great"] + _ac["distribution"]["critical"])) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                        text _adesc font ACT_FONT size 11 color "#7a9ab8"
                        hbox:
                            spacing 6
                            for _tid in ("critical_failure", "weak", "success", "great", "critical"):
                                text ("%s %d%%" % (art_quality_label(_tid), _ac["distribution"][_tid])) font ACT_FONT size 10 color tier_color(_tid)
            null height 4
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7, 18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── Simple confirm + odds (still life) ─────────────────────────────────────────
screen painting_confirm_scr(sid, subj_id):
    modal True
    zorder 217
    add "#000000cc"
    $ _pc = painting_chance(sid, subj_id)
    $ _ps = ART_SESSIONS[sid]
    frame:
        xalign 0.5 yalign 0.5
        xsize 540
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 8
            text ART_SUBJECTS[subj_id]["name"] font PROFILE_FONT size 18 color "#cfe0f5" xalign 0.5
            text ART_SUBJECTS[subj_id]["desc"] font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            null height 4
            text ("Time %gh  ·  Energy -%d  ·  Materials $%d" % (_ps["hours"], _ps["energy"], art_material_cost(sid))) font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
            use art_gear_line()
            null height 4
            text "How it's likely to come out:" font ACT_FONT size 13 color "#9fb6d6" xalign 0.5
            for _tid in ("critical", "great", "success", "weak", "critical_failure"):
                hbox:
                    xalign 0.5
                    spacing 10
                    text art_quality_label(_tid) font ACT_FONT size 12 color tier_color(_tid) xsize 150
                    text ("%d%%" % _pc["distribution"][_tid]) font PROFILE_FONT size 12 color "#ffd66a"
            null height 6
            hbox:
                xalign 0.5
                spacing 12
                button:
                    action Return(True)
                    background "#1e3a5f"
                    padding (20, 8, 20, 8)
                    text "Start" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"
                button:
                    action Return(False)
                    background "#1e3a5f"
                    padding (20, 8, 20, 8)
                    text "Not now" font PROFILE_FONT size 14 color "#9fb6d6" hover_color "#ffffff"


# Shared one-liner describing what your gear is contributing.
screen art_gear_line():
    $ _agb = art_gear_bonus()
    if _agb > 0:
        text ("Easel and materials: +%d to the roll" % _agb) font ACT_FONT size 11 color "#7fd06a" xalign 0.5
    else:
        text "Improvising with what you have." font ACT_FONT size 11 color "#cc9040" xalign 0.5


# ── Commission confirm ─────────────────────────────────────────────────────────
screen commission_confirm_scr():
    modal True
    zorder 218
    add "#000000cc"
    $ _cm = active_painting_commission()
    frame:
        xalign 0.5 yalign 0.5
        xsize 600
        background "#12161ef8"
        padding (24, 20, 24, 22)
        if _cm is None:
            vbox:
                text "Nothing outstanding." font ACT_FONT size 14 color "#cfe0f5"
                textbutton "Close" action Return(None) text_font ACT_FONT text_size 13 text_color "#5bcafa"
        else:
            vbox:
                spacing 8
                text _cm["client"] font PROFILE_FONT size 17 color "#cfe0f5" xalign 0.5
                text _cm["label"] font ACT_FONT size 12 color "#7a9ab8" xalign 0.5
                null height 4
                hbox:
                    xalign 0.5
                    spacing 16
                    text ("$%d agreed" % _cm["pay"]) font ACT_FONT size 13 color "#ffd66a"
                    text ("%gh" % _cm["hours"]) font ACT_FONT size 13 color "#7a9ab8"
                    text ("Due day %d" % (_cm["deadline_day"] + 1)) font ACT_FONT size 13 color "#7a9ab8"
                text ("Client expects at least: %s" % art_quality_label(_cm["min_quality"])) font ACT_FONT size 12 color "#9fb6d6" xalign 0.5
                use art_gear_line()
                null height 4
                for _appr, _albl in [("careful", "Careful"), ("normal", "Standard"), ("ambitious", "Ambitious")]:
                    $ _cc = commission_chance(_cm, _appr)
                    button:
                        action Return(_appr)
                        xfill True
                        background "#1a2a3a"
                        hover_background "#1e3a5f"
                        padding (14, 9, 14, 9)
                        hbox:
                            xfill True
                            text _albl font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                            text ("Meets the brief %d%%" % _cc["success_or_better"]) font PROFILE_FONT size 13 color "#ffd66a" yalign 0.5 xalign 1.0
                null height 4
                button:
                    action Return(None)
                    xalign 0.5
                    background "#1e3a5f"
                    padding (18, 7, 18, 7)
                    text "Not today" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"


# ── My Artworks list ───────────────────────────────────────────────────────────
screen my_artworks_scr():
    modal True
    zorder 210
    add "#000000cc"
    default _af = "all"
    frame:
        xalign 0.5 yalign 0.5
        xsize 720
        ysize 600
        background "#12161ef8"
        padding (22, 18, 22, 18)
        vbox:
            spacing 8
            text "YOUR ARTWORKS" font PROFILE_FONT size 18 color "#9fb6d6" xalign 0.5
            hbox:
                xalign 0.5
                spacing 16
                text ("Art Lv %d" % skill_val("art")) font ACT_FONT size 13 color "#ff9f4d"
                text ("Reputation %d" % art_reputation) font ACT_FONT size 13 color "#8a6ac0"
                text ("%d pieces" % len(player_artworks)) font ACT_FONT size 13 color "#7a9ab8"
            hbox:
                xalign 0.5
                spacing 6
                for _fid, _flbl in ARTWORK_FILTERS:
                    button:
                        action SetLocalVariable("_af", _fid)
                        background ("#1e3a5f" if _af == _fid else "#1a2230")
                        padding (10, 5, 10, 5)
                        text _flbl font ACT_FONT size 11 color ("#5bcafa" if _af == _fid else "#7a9ab8")
            null height 4
            viewport:
                xfill True
                ysize 440
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    $ _alist = filtered_artworks(_af)
                    if not _alist:
                        null height 20
                        text "Nothing here." font ACT_FONT size 14 color "#4a6080" xalign 0.5
                    for _a in _alist:
                        frame:
                            xfill True
                            background "#1a2230"
                            padding (14, 10, 14, 10)
                            hbox:
                                spacing 12
                                xfill True
                                vbox:
                                    spacing 3
                                    xsize 440
                                    hbox:
                                        spacing 8
                                        text _a["subject"] font PROFILE_FONT size 14 color "#cfe0f5"
                                        text art_quality_label(_a["quality"]) font ACT_FONT size 12 color tier_color(_a["quality"]) yalign 0.5
                                    hbox:
                                        spacing 10
                                        text ("Day %d" % (_a["day"] + 1)) font ACT_FONT size 11 color "#7090b0"
                                        text ("Art %d" % _a["art_skill"]) font ACT_FONT size 11 color "#7090b0"
                                        text ("$%d" % _a["estimated_value"]) font ACT_FONT size 11 color "#ffd66a"
                                    hbox:
                                        spacing 8
                                        if _a["displayed"]:
                                            text "On the wall" font ACT_FONT size 10 color "#7fd06a"
                                        if _a["in_portfolio"]:
                                            text "Portfolio" font ACT_FONT size 10 color "#5bcafa"
                                        if _a["gifted_to"]:
                                            text ("Given to %s" % NPC_DATA[_a["gifted_to"]]["name"]) font ACT_FONT size 10 color "#ff7fb0"
                                        if _a["submitted_to"]:
                                            text "Entered" font ACT_FONT size 10 color "#ffd66a"
                                        if _a["sold"]:
                                            text ("Sold for $%d" % _a.get("sold_for", 0)) font ACT_FONT size 10 color "#8a6ac0"
                                button:
                                    action Return(_a["id"])
                                    xalign 1.0
                                    background "#1e3a5f"
                                    padding (12, 6, 12, 6)
                                    text "Open" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"
            null height 6
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (20, 8, 20, 8)
                text "Close" font PROFILE_FONT size 14 color "#5bcafa" hover_color "#ffffff"


# ── Gift recipient picker ──────────────────────────────────────────────────────
screen artwork_gift_scr():
    modal True
    zorder 220
    add "#000000cc"
    frame:
        xalign 0.5 yalign 0.5
        xsize 520
        background "#12161ef8"
        padding (24, 20, 24, 22)
        vbox:
            spacing 8
            text "Who are you giving it to?" font PROFILE_FONT size 17 color "#9fb6d6" xalign 0.5
            null height 4
            $ _gnpcs = artwork_giftable_npcs()
            if not _gnpcs:
                text "Nobody you know well enough." font ACT_FONT size 13 color "#4a6080" xalign 0.5
            for _gn in _gnpcs:
                button:
                    action Return(_gn)
                    xfill True
                    background "#1a2a3a"
                    hover_background "#1e3a5f"
                    padding (14, 9, 14, 9)
                    hbox:
                        xfill True
                        text NPC_DATA[_gn]["name"] font ACT_FONT size 14 color "#cfe0f5" yalign 0.5
                        # The interest level is not spelled out as a number —
                        # the player learns it from how people react.
                        text ("Affection %d" % npc_aff(_gn)) font ACT_FONT size 12 color "#7a9ab8" yalign 0.5 xalign 1.0
            null height 4
            button:
                action Return(None)
                xalign 0.5
                background "#1e3a5f"
                padding (18, 7, 18, 7)
                text "Back" font ACT_FONT size 13 color "#5bcafa" hover_color "#ffffff"
