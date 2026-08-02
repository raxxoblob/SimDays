# Phone - pure screen overlay. HUD uses Show("phone_home"); Close uses Hide.
# No script Call() involved, so the phone never interrupts or re-triggers labels.

init python:
    _NPC_HI_REPLY = {
        "zoe":     "Hey. You okay?",
        "nora":    "Hi! Just got off a shift. What's up?",
        "marcus":  "Yo. Good timing, I was just thinking about heading out.",
        "elle":    "Oh hey! Was just reading. Everything good?",
        "eli":     "Hey. Needed a break from the thesis anyway.",
        "sam":     "Hey! What are you up to?",
        "kai":     "Oh hey. Wasn't expecting to hear from you.",
        "lena":    "Hi. I have maybe five minutes. What's going on?",
        "caroline":"Hi. Is something wrong with the project?",
        "martha":  "Hey there. How's your day going?",
        "natalie": "Hey! Just saw your message. All good?",
    }

    def phone_say_hi(npc_id):
        td = list(store.npc_texted_today)
        if npc_id in td:
            return
        td.append(npc_id)
        store.npc_texted_today = td
        _apply_trust(npc_id, 1)
        _add_player_message(npc_id, "Hey!")
        reply = _NPC_HI_REPLY.get(npc_id, "Hey.")
        send_npc_message(npc_id, reply)
        renpy.restart_interaction()

    def phone_where_is(npc_id):
        loc = npc_location_now(npc_id)
        name = NPC_DATA[npc_id]["name"]
        _add_player_message(npc_id, "Where are you right now?")
        if loc:
            place = LOCATION_NAMES.get(loc, loc.replace("location_", "").replace("_", " ").title())
            reply = "I'm at %s." % place
        else:
            reply = "Not sure where I'll end up today."
        send_npc_message(npc_id, reply)
        renpy.restart_interaction()

    def _add_player_message(npc_id, text):
        """Append an outgoing player message to the NPC thread."""
        _tag = "_player_%s_%d_%d" % (npc_id, store.day, len(store.npc_messages))
        store.npc_messages.append({
            "npc_id":       npc_id,
            "npc_name":     "",
            "text":         text,
            "send_on_day":  store.day,
            "delivered":    True,
            "delivered_on": store.day,
            "read":         True,
            "replied":      False,
            "replied_with": None,
            "responses":    [],
            "tag":          _tag,
            "is_player":    True,
        })


    # ── Phase 32: active invitation card ─────────────────────────────────────
    _INVITATION_META = {
        "marcus_park_invite":  {"npc_id": "marcus", "location_text": "the park"},
        "nora_grounds_invite": {"npc_id": "nora",   "location_text": "Grounds"},
        "zoe_park_invite":     {"npc_id": "zoe",    "location_text": "the park"},
        "eli_library_invite":  {"npc_id": "eli",    "location_text": "the library"},
        "nora_static_date":    {"npc_id": "nora",   "location_text": "Static",         "display_text": "Date with Nora at Static"},
        "zoe_beach_date":      {"npc_id": "zoe",    "location_text": "the beach",      "display_text": "Date with Zoe at the beach"},
        # Phase 49: home-visit invitations
        "nora_home_coffee":    {"npc_id": "nora",   "location_text": "your apartment", "display_text": "Coffee setup with Nora"},
        "eli_home_dinner":     {"npc_id": "eli",    "location_text": "your apartment", "display_text": "Dinner with Eli"},
        "zoe_home_guitar":     {"npc_id": "zoe",    "location_text": "your apartment", "display_text": "Guitar session with Zoe"},
        # Phase 50: Zoe exhibition
        "zoe_exhibition":      {"npc_id": "zoe",    "location_text": "the gallery",    "display_text": "Zoe's exhibition opening"},
    }

    def phone_active_invitation():
        """Return display dict for the active pending invitation, or None."""
        inv = store.npc_invitation_pending
        if not inv:
            return None
        inv_id = inv.get("invitation_id", "")
        meta   = _INVITATION_META.get(inv_id)
        if not meta:
            return None
        expiry = inv.get("expiry_day", -999)
        if store.day > expiry:
            return None
        npc_id = meta["npc_id"]
        npc    = NPC_DATA.get(npc_id, {})
        remaining = expiry - store.day
        if remaining > 1:
            days_text = "%d days left" % remaining
        elif remaining == 1:
            days_text = "1 day left"
        else:
            days_text = "Expires today"
        return {
            "name":         npc.get("name", npc_id.title()),
            "portrait":     npc.get("portrait", ""),
            "location":     meta["location_text"],
            "days_text":    days_text,
            "display_text": meta.get("display_text", ""),
        }


    # ── Phase 36: chat avatar helpers ────────────────────────────────────────
    _CHAT_AVATAR_MASK = "images/ui/activity_dot.png"
    _MC_CHAT_PORTRAIT = "images/ui/icons/app_contacts.png"

    def _npc_chat_portrait(npc_id):
        """Portrait path for chat avatar; falls back to app_contacts if NPC has none."""
        portrait = NPC_DATA.get(npc_id, {}).get("portrait", "")
        if portrait:
            return "images/ui/icons/%s.png" % portrait
        return _MC_CHAT_PORTRAIT

    def _chat_circle(path):
        """48x48 circular displayable via AlphaMask; identical for NPC and player sides."""
        return AlphaMask(
            Transform(path, size=(48, 48)),
            Transform(_CHAT_AVATAR_MASK, size=(48, 48))
        )

    # Any phone surface open? (home OR any app screen). The HUD peek uses this so
    # it hides while an app is open — not just while phone_home is up.
    _PHONE_SCREENS = ("phone_home", "phone_messages_scr", "phone_contacts_scr", "phone_thread_scr",
                      "phone_goals_scr", "phone_settings", "phone_bank_scr", "phone_help_scr", "stock_market")
    def phone_open():
        return any(renpy.get_screen(s) for s in _PHONE_SCREENS)

    def thread_messages(npc_id):
        """All messages in this NPC's thread, in list order (chronological)."""
        return [m for m in store.npc_messages
                if m.get("npc_id") == npc_id and (m.get("delivered") or m.get("is_player"))]

    def thread_npc_list():
        """NPCs with any thread messages, ordered by most-recent first."""
        _seen = {}  # npc_id -> index of last msg
        for _i, _m in enumerate(store.npc_messages):
            _n = _m.get("npc_id")
            if _n and (_m.get("delivered") or _m.get("is_player")):
                _seen[_n] = _i
        return sorted(_seen.keys(), key=lambda n: -_seen[n])

    def npc_unread_count(npc_id):
        return sum(1 for m in store.npc_messages
                   if m.get("npc_id") == npc_id and m.get("delivered") and not m.get("read") and not m.get("is_player"))


# ── Phone geometry ─────────────────────────────────────────────────────
# phone.png is 1024x1536 (aspect 0.667), shown at PHONE_W x PHONE_H on the right.
# The glass sits inside the bezel at these offsets (measured from the art):
# x≈0.195w, y≈0.10h, size 0.605w x 0.80h. Every app screen renders its content
# inside this rect via `use phone_shell`, so apps look like real phone screens
# instead of windows centred on the game screen.
define PHONE_W     = 600
define PHONE_H     = 900
define PHONE_X     = 1290
define PHONE_Y     = 158   # centred between the top HUD (ends ~137) and the bottom edge
define PHONE_SCR_X = 117
define PHONE_SCR_Y = 92
define PHONE_SCR_W = 363
define PHONE_SCR_H = 716

# Shared phone chrome: dark overlay + phone art + a dark "app screen" backdrop
# over the wallpaper. App screens do `use phone_shell:` then their content,
# which is transcluded into the glass rect.
screen phone_shell():
    modal True
    add "#000000aa"
    fixed:
        xpos PHONE_X
        ypos PHONE_Y
        xysize (PHONE_W, PHONE_H)
        add Transform("images/ui/phone.png", size=(PHONE_W, PHONE_H))
        fixed:
            xpos PHONE_SCR_X
            ypos PHONE_SCR_Y
            xysize (PHONE_SCR_W, PHONE_SCR_H)
            add Solid("#0b1016ee")          # app backdrop so content reads over the wallpaper
            transclude

screen phone_home():
    modal True
    add "#000000aa"
    $ _clock = time_label(hour)
    $ _day   = day_name(day)

    fixed:
        xpos PHONE_X
        ypos PHONE_Y
        xysize (PHONE_W, PHONE_H)

        # phone image with wallpaper baked in (home keeps the wallpaper visible)
        add Transform("images/ui/phone.png", size=(PHONE_W, PHONE_H))

        # content overlaid on the screen area
        fixed:
            xpos PHONE_SCR_X
            ypos PHONE_SCR_Y
            xysize (PHONE_SCR_W, PHONE_SCR_H)

            vbox:
                spacing 0
                xalign 0.5
                xsize PHONE_SCR_W

                null height 10
                text "[_clock]   [_day]" font PROFILE_FONT size 18 color "#cfe0f5" xalign 0.5
                null height 22

                $ _apps = [
                    ("app_messages",  "Messages",  [Hide("phone_home"), Show("phone_messages_scr")]),
                    ("app_contacts",  "Contacts",  [Hide("phone_home"), Show("phone_contacts_scr")]),
                    ("app_map",       "Map",        Hide("phone_home")),
                    ("app_jobs",      "Jobs",       [Hide("phone_home"), Show("phone_jobs_scr")]),
                    ("app_bank",      "Bank",       [Hide("phone_home"), Show("phone_bank_scr")]),
                    ("app_stocks",    "Stocks",     [Hide("phone_home"), Show("stock_market")]),
                    ("app_tips",      "Goals",      [Hide("phone_home"), Show("phone_goals_scr")]),
                    ("app_settings",  "Settings",   [Hide("phone_home"), Show("phone_settings")]),
                ]
                vpgrid:
                    cols 3
                    spacing 12
                    xalign 0.5
                    for _icon, _lbl, _act in _apps:
                        button:
                            xysize (104, 118)
                            background None
                            hover_background None
                            action _act
                            vbox:
                                spacing 5
                                add Transform("images/ui/icons/%s.png" % _icon, size=(82, 82)) xalign 0.5
                                $ _app_lbl = _lbl + ((" (%d)" % len(gigs_board)) if (_icon == "app_jobs" and gigs_board) else "")
                                text _app_lbl font ACT_FONT size 13 color ("#7fd06a" if (_icon == "app_jobs" and gigs_board) else "#ffffff") xalign 0.5

                null height 12
                $ _inv = phone_active_invitation()
                if _inv:
                    frame:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                        padding (10, 8, 10, 8)
                        vbox:
                            spacing 3
                            text "Active Plan" font PROFILE_FONT size 11 color "#5bcafa" xalign 0.5
                            null height 2
                            hbox:
                                spacing 8
                                yalign 0.5
                                if _inv["portrait"]:
                                    add ("images/ui/icons/%s.png" % _inv["portrait"]) xysize (40, 40) yalign 0.5
                                vbox:
                                    xfill True
                                    yalign 0.5
                                    spacing 2
                                    text (_inv["display_text"] or ("Meet " + _inv["name"] + " at " + _inv["location"])) font ACT_FONT size 12 color "#cfe0f5"
                                    text _inv["days_text"] font ACT_FONT size 11 color "#7a9ab8"
                    null height 8
                textbutton "Close" action Hide("phone_home") xalign 0.5 text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"


# text-row helper used by sub-screens (messages list, groceries)
screen _phone_app(label, act):
    button:
        xfill True
        ysize 68
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
        action act
        text label font ACT_FONT size 22 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)


screen phone_messages_scr():
    modal True
    on "show" action [Function(deliver_due_messages), Function(mark_all_messages_read)]
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Messages" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 620
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    # ── Upcoming commitments ──────────────────────────
                    use commitments_list(compact=True)
                    # ── City News ─────────────────────────────────────
                    if daily_events:
                        for _ev in daily_events:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (12, 8, 12, 8)
                                vbox:
                                    spacing 2
                                    text _ev["from"] font PROFILE_FONT size 12 color "#5bcafa"
                                    text _ev["body"] font ACT_FONT size 13 color "#cfe0f5"
                    # ── Conversations list ────────────────────────────
                    $ _tnpcs = thread_npc_list()
                    if _tnpcs:
                        null height 4
                        for _tn in _tnpcs:
                            $ _tn_msgs   = thread_messages(_tn)
                            $ _tn_last   = _tn_msgs[-1] if _tn_msgs else None
                            $ _tn_unread = npc_unread_count(_tn)
                            $ _tn_np     = _npc_chat_portrait(_tn)
                            button:
                                xfill True
                                ysize 72
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                                action [SetVariable("_active_thread_npc", _tn), Function(mark_all_messages_read), Hide("phone_messages_scr"), Show("phone_thread_scr")]
                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    xpos 8
                                    add _chat_circle(_tn_np) yalign 0.5
                                    vbox:
                                        xfill True
                                        yalign 0.5
                                        spacing 2
                                        hbox:
                                            xfill True
                                            spacing 6
                                            text NPC_DATA[_tn]["name"] font PROFILE_FONT size 14 color ("#ffffff" if _tn_unread else "#cfe0f5") yalign 0.5
                                            if _tn_unread:
                                                text ("●") font PROFILE_FONT size 10 color "#5bcafa" yalign 0.5
                                        if _tn_last:
                                            $ _preview = (_tn_last["text"][:38] + "…") if len(_tn_last["text"]) > 38 else _tn_last["text"]
                                            $ _prev_color = "#4a7a9b" if _tn_last.get("is_player") else ("#cfe0f5" if _tn_unread else "#4a6080")
                                            text _preview font ACT_FONT size 12 color _prev_color
                    elif not daily_events:
                        text "No messages yet." font ACT_FONT size 15 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("phone_messages_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Contacts app ──────────────────────────────────────────────────────────
screen phone_contacts_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Contacts" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 620
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    $ _known = [k for k in npc_contacts if k in NPC_DATA]
                    if _known:
                        for _k in _known:
                            $ _loc    = npc_location_now(_k)
                            $ _np_cir = _chat_circle(_npc_chat_portrait(_k))
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (10, 8, 10, 8)
                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    add _np_cir yalign 0.5
                                    vbox:
                                        xfill True
                                        yalign 0.5
                                        spacing 2
                                        text NPC_DATA[_k]["name"] font PROFILE_FONT size 15 color "#cfe0f5"
                                        if _loc:
                                            $ _pname = LOCATION_NAMES.get(_loc, "")
                                            if _pname:
                                                text ("@ " + _pname) font ACT_FONT size 11 color "#4a8a6a"
                                    button:
                                        xysize (70, 36)
                                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                                        action [SetVariable("_active_thread_npc", _k), Hide("phone_contacts_scr"), Show("phone_thread_scr")]
                                        text "Chat" font ACT_FONT size 13 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                    else:
                        text "No contacts yet." font ACT_FONT size 15 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("phone_contacts_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Conversation thread ───────────────────────────────────────────────────
screen phone_thread_scr():
    modal True
    on "show" action Function(mark_all_messages_read)
    use phone_shell:
        $ _tnpc   = store._active_thread_npc
        $ _tname  = NPC_DATA[_tnpc]["name"] if (_tnpc and _tnpc in NPC_DATA) else ""
        $ _texted = _tnpc in npc_texted_today if _tnpc else True
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            # Header
            null height 6
            hbox:
                xfill True
                xpos 4
                spacing 6
                button:
                    xysize (28, 28)
                    background None
                    hover_background Frame("images/ui/act_bar_idle.png", 10, 10, 10, 10)
                    action [Hide("phone_thread_scr"), Show("phone_messages_scr")]
                    text "‹" font PROFILE_FONT size 22 color "#7fb0d6" hover_color "#ffffff" align (0.5, 0.5)
                text _tname font PROFILE_FONT size 18 color "#ffffff" yalign 0.5
            null height 6
            # Messages viewport — yinitial 1.0 scrolls to bottom
            viewport:
                xfill True
                ysize 530
                mousewheel True
                scrollbars "vertical"
                yinitial 1.0
                vbox:
                    spacing 6
                    xfill True
                    $ _tmsgs = thread_messages(_tnpc) if _tnpc else []
                    if not _tmsgs:
                        text "No messages yet." font ACT_FONT size 14 color "#4a6080" xalign 0.5 yalign 0.5
                    for _tm in _tmsgs:
                        $ _is_pl = _tm.get("is_player", False)
                        if _is_pl:
                            # Player bubble — right side
                            hbox:
                                xalign 1.0
                                frame:
                                    xmaximum 240
                                    background "#1e4060e8"
                                    padding (10, 7, 10, 7)
                                    text _tm["text"] font ACT_FONT size 13 color "#a8d0f0"
                        else:
                            # NPC bubble — left side with avatar
                            hbox:
                                spacing 8
                                yalign 0.0
                                add _chat_circle(_npc_chat_portrait(_tnpc)) yalign 0.0
                                vbox:
                                    spacing 4
                                    frame:
                                        xmaximum 220
                                        background "#16202ae8"
                                        padding (10, 7, 10, 7)
                                        text _tm["text"] font ACT_FONT size 13 color "#cfe0f5"
                                    # Actionable responses
                                    $ _has_r = bool(_tm.get("responses")) and not _tm.get("replied")
                                    $ _is_r  = _tm.get("replied", False)
                                    if _has_r:
                                        hbox:
                                            spacing 6
                                            for _rsp in _tm["responses"]:
                                                button:
                                                    xysize (110, 28)
                                                    background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                                                    hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                                                    action [Function(mark_message_replied, _tm, _rsp["id"]), Hide("phone_thread_scr"), Hide("phone_home"), Function(renpy.jump, _rsp["label"])]
                                                    text _rsp["text"] font ACT_FONT size 11 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                                    elif _is_r and _tm.get("replied_with"):
                                        $ _rt = next((r["text"] for r in _tm.get("responses", []) if r["id"] == _tm.get("replied_with")), "")
                                        if _rt:
                                            hbox:
                                                xalign 0.0
                                                frame:
                                                    xmaximum 200
                                                    background "#1e4060e8"
                                                    padding (8, 5, 8, 5)
                                                    text ("You: " + _rt) font ACT_FONT size 11 color "#4a7a9b"
            # Action area
            null height 6
            hbox:
                spacing 8
                xalign 0.5
                if _tnpc:
                    button:
                        xysize (100, 32)
                        sensitive not _texted
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        action Function(phone_say_hi, _tnpc)
                        text "Say hi" font ACT_FONT size 13 color ("#4a6080" if _texted else "#cfe0f5") hover_color "#ffffff" align (0.5, 0.5)
                    button:
                        xysize (126, 32)
                        background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                        action Function(phone_where_is, _tnpc)
                        text "Where are you?" font ACT_FONT size 11 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
            null height 4
            textbutton "Back" action [Hide("phone_thread_scr"), Show("phone_messages_scr")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_goals_scr():
    modal True
    on "show" action Function(fs_refresh)
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 8
            null height 8
            text "Goals" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            null height 2
            $ _active = active_quests()
            $ _done   = completed_quests()
            viewport:
                xfill True
                ysize 570
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    # ── First Steps card ─────────────────────────────
                    $ _fs_track = first_steps_track
                    $ _fs_data  = FIRST_STEPS.get(_fs_track, {}) if _fs_track else {}
                    if _fs_track and not first_steps_hidden and not first_steps_completed and _fs_data:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                            padding (14, 10, 14, 10)
                            vbox:
                                spacing 6
                                hbox:
                                    xfill True
                                    text _fs_data["title"] font PROFILE_FONT size 13 color "#e0c060" yalign 0.5
                                    textbutton "Hide" action SetVariable("first_steps_hidden", True) text_font ACT_FONT text_size 11 text_color "#4a6080" text_hover_color "#9fb6d6" xalign 1.0 yalign 0.5
                                for _obj in _fs_data.get("objectives", []):
                                    $ _obj_done = first_steps_progress.get(_obj["id"], False)
                                    hbox:
                                        spacing 6
                                        text ("✓" if _obj_done else "○") font PROFILE_FONT size 12 color ("#39c07a" if _obj_done else "#5bcafa") yalign 0.5
                                        text _obj["label"] font ACT_FONT size 12 color ("#3a5a4a" if _obj_done else "#cfe0f5") yalign 0.5
                    elif _fs_track and first_steps_completed:
                        frame:
                            xfill True
                            background "#0e1a22"
                            padding (14, 8, 14, 8)
                            hbox:
                                spacing 8
                                text "✓" font PROFILE_FONT size 13 color "#39c07a" yalign 0.5
                                text (_fs_data.get("title", "First Steps") + " — done") font ACT_FONT size 12 color "#3a5a4a" yalign 0.5
                    # ── Active quests ─────────────────────────────────
                    if _active:
                        for _qst in _active:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (14, 10, 14, 10)
                                vbox:
                                    spacing 3
                                    hbox:
                                        spacing 6
                                        text "○" font PROFILE_FONT size 13 color "#5bcafa" yalign 0.5
                                        text _qst["title"] font PROFILE_FONT size 13 color "#cfe0f5" yalign 0.5
                                    text _qst["body"] font ACT_FONT size 12 color "#7a96a8"
                    elif not _fs_track:
                        text "All current goals complete." font ACT_FONT size 15 color "#4a6080"
                    if _done:
                        null height 4
                        text "Completed" font PROFILE_FONT size 13 color "#4a6a5a"
                        null height 2
                        for _qst in _done:
                            frame:
                                xfill True
                                background "#0e1a22"
                                padding (14, 8, 14, 8)
                                hbox:
                                    spacing 8
                                    text "✓" font PROFILE_FONT size 13 color "#39c07a" yalign 0.5
                                    text _qst["title"] font PROFILE_FONT size 13 color "#3a5a4a" yalign 0.5
            null height 4
            hbox:
                spacing 10
                xalign 0.5
                textbutton "Help" action [Hide("phone_goals_scr"), Show("phone_help_scr")] text_font ACT_FONT text_size 16 text_color "#5bcafa" text_hover_color "#ffffff"
                textbutton "Back" action [Hide("phone_goals_scr"), Show("phone_home")] text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_settings():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 14
            null height 8
            text "Settings" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            null height 4
            text "Text speed" font PROFILE_FONT size 16 color "#cfe0f5"
            bar value Preference("text speed") xsize 300 xalign 0.5
            text "Music volume" font PROFILE_FONT size 16 color "#cfe0f5"
            bar value Preference("music volume") xsize 300 xalign 0.5
            text "Sound volume" font PROFILE_FONT size 16 color "#cfe0f5"
            bar value Preference("sound volume") xsize 300 xalign 0.5
            null height 4
            textbutton "Auto-forward: toggle" action Preference("auto-forward", "toggle") text_font ACT_FONT text_size 17 xalign 0.5
            textbutton "Fullscreen: toggle" action Preference("display", "toggle") text_font ACT_FONT text_size 17 xalign 0.5
            null height 6
            textbutton "Back" action [Hide("phone_settings"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_bank_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 10
            null height 8
            text "City Bank" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            null height 4
            text "Balance:  $[money]" font PROFILE_FONT size 18 color "#39c07a"
            if loan > 0:
                text "Loan:     $[loan]  (5%%/wk)" font PROFILE_FONT size 16 color "#e86a55"
            if savings > 0:
                text "Savings:  $[savings]  (2%%/wk)" font PROFILE_FONT size 16 color "#5bcafa"
            null height 8
            # ── Borrow ───────────────────────────────────────────────
            if loan == 0:
                text "Borrow" font PROFILE_FONT size 15 color "#9fb6d6"
                for _amt in [200, 500, 1000]:
                    button:
                        xfill True ysize 56
                        sensitive money < _amt * 2
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        action [SetVariable("loan", loan + _amt), SetVariable("money", money + _amt), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Take $%d loan" % _amt font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
            # ── Repay ────────────────────────────────────────────────
            if loan > 0:
                null height 4
                text "Repay loan" font PROFILE_FONT size 15 color "#9fb6d6"
                $ _repay_full = min(loan, money)
                $ _repay_half = min(loan // 2 + 1, money)
                if _repay_full > 0:
                    button:
                        xfill True ysize 56
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        action [SetVariable("money", money - _repay_full), SetVariable("loan", loan - _repay_full), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Repay all  (-$%d)" % _repay_full font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                if _repay_half < _repay_full:
                    button:
                        xfill True ysize 56
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        action [SetVariable("money", money - _repay_half), SetVariable("loan", loan - _repay_half), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Repay half  (-$%d)" % _repay_half font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
            # ── Savings ──────────────────────────────────────────────
            if loan == 0:
                null height 4
                text "Savings (2%%/wk)" font PROFILE_FONT size 15 color "#9fb6d6"
                for _dep in [100, 500]:
                    button:
                        xfill True ysize 56
                        sensitive money >= _dep
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        action [SetVariable("money", money - _dep), SetVariable("savings", savings + _dep), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Deposit $%d" % _dep font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                if savings > 0:
                    button:
                        xfill True ysize 56
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        action [SetVariable("money", money + savings), SetVariable("savings", 0), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Withdraw all  +$[savings]" font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
            null height 8
            textbutton "Back" action [Hide("phone_bank_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
