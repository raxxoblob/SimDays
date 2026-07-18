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
        reply = _NPC_HI_REPLY.get(npc_id, "Hey.")
        send_npc_message(npc_id, reply)
        renpy.restart_interaction()

    def phone_where_is(npc_id):
        loc = npc_location_now(npc_id)
        name = NPC_DATA[npc_id]["name"]
        if loc:
            place = LOCATION_NAMES.get(loc, loc.replace("location_", "").replace("_", " ").title())
            renpy.notify("%s is at %s right now." % (name, place))
        else:
            renpy.notify("Not sure where %s is right now." % name)
        renpy.restart_interaction()


transform _phone_in():
    yoffset 700 alpha 0.0
    easein 0.28 yoffset 0 alpha 1.0

screen phone_home():
    modal True
    add "#000000aa"
    $ _clock = time_label(hour)
    $ _day   = day_name(day)

    # phone.png (1024x1536) displayed at 460x690, bottom-right corner
    # screen area inside bezel: ~x=96-364, y=88-640 at display scale
    fixed:
        at _phone_in
        xpos 1460
        ypos 390
        xysize (460, 690)

        # phone image with wallpaper baked in
        add Transform("images/ui/phone.png", size=(460, 690))

        # content overlaid on the screen area
        fixed:
            xpos 96
            ypos 30
            xsize 268
            ysize 610

            vbox:
                spacing 0
                xalign 0.5

                null height 8
                text "[_clock]   [_day]" font PROFILE_FONT size 16 color "#cfe0f5" xalign 0.5
                null height 18

                $ _apps = [
                    ("app_messages",  "Messages",  [Hide("phone_home"), Show("phone_messages_scr")]),
                    ("app_contacts",  "Contacts",  [Hide("phone_home"), Show("phone_messages_scr")]),
                    ("app_map",       "Map",        Hide("phone_home")),
                    ("app_jobs",      "Jobs",       Hide("phone_home")),
                    ("app_bank",      "Bank",       [Hide("phone_home"), Show("phone_bank_scr")]),
                    ("app_stocks",    "Stocks",     [Hide("phone_home"), Show("stock_market")]),
                    ("app_tips",      "Goals",      [Hide("phone_home"), Show("phone_goals_scr")]),
                    ("app_settings",  "Settings",   [Hide("phone_home"), Show("phone_settings")]),
                ]
                vpgrid:
                    cols 3
                    spacing 10
                    xalign 0.5
                    for _icon, _lbl, _act in _apps:
                        button:
                            xysize (78, 96)
                            background None
                            hover_background None
                            action _act
                            vbox:
                                spacing 4
                                add Transform("images/ui/icons/%s.png" % _icon, size=(66, 66)) xalign 0.5
                                text _lbl font ACT_FONT size 11 color "#ffffff" xalign 0.5

                null height 14
                textbutton "Close" action Hide("phone_home") xalign 0.5 text_font ACT_FONT text_size 15 text_color "#9fb6d6" text_hover_color "#ffffff"


# text-row helper used by sub-screens (messages list, groceries)
screen _phone_app(label, act):
    button:
        xfill True
        ysize 68
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
        action act
        text label font ACT_FONT size 22 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)


screen phone_messages_scr():
    on "show" action [Function(deliver_due_messages), Function(mark_all_messages_read)]
    modal True
    add "#000000aa"
    frame:
        xalign 0.985
        yalign 0.5
        xsize 380
        ysize 720
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (24, 16, 24, 16)
        vbox:
            spacing 0
            text "Messages" font PROFILE_FONT size 26 color "#ffffff" xalign 0.5
            null height 8
            viewport:
                ysize 620
                mousewheel True
                vbox:
                    spacing 8
                    xsize 332
                    # ── Upcoming commitments ──────────────────────────
                    use commitments_list(compact=True)
                    # ── Agenda: today + tomorrow ──────────────────────
                    $ _today_c = today_commitments()
                    $ _tmrw_c  = tomorrow_commitments()
                    if _today_c or _tmrw_c:
                        null height 4
                        text "Agenda" font PROFILE_FONT size 15 color "#9fb6d6"
                        null height 2
                        for _ac in (_today_c + _tmrw_c):
                            $ _ac_status = commitment_status_text(_ac)
                            $ _ac_color  = "#5bcafa" if commitment_available(_ac["id"]) else ("#4a6080" if _ac_status in ("Completed","Missed","Cancelled") else "#9fb6d6")
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (10, 6, 10, 6)
                                hbox:
                                    xfill True
                                    spacing 6
                                    vbox:
                                        xexpand True
                                        spacing 1
                                        text _ac["title"] font ACT_FONT size 13 color "#cfe0f5"
                                        text ("%02d:00  ·  " % _ac["hour"] + _ac["location"]) font ACT_FONT size 11 color "#4a6080"
                                    text _ac_status font ACT_FONT size 11 color _ac_color yalign 0.5
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
                    # ── NPC Inbox ────────────────────────────────────
                    $ _inbox = delivered_messages()
                    if _inbox:
                        null height 4
                        text "Messages" font PROFILE_FONT size 15 color "#9fb6d6"
                        null height 2
                        for _imsg in _inbox:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (12, 8, 12, 8)
                                vbox:
                                    spacing 4
                                    text _imsg["npc_name"] font PROFILE_FONT size 12 color ("#5bcafa" if not _imsg["read"] else "#3a5068")
                                    text _imsg["text"] font ACT_FONT size 13 color ("#cfe0f5" if not _imsg["read"] else "#4a6080")
                                    $ _has_r = bool(_imsg.get("responses")) and not _imsg.get("replied")
                                    $ _is_r  = _imsg.get("replied", False)
                                    if _has_r:
                                        hbox:
                                            spacing 6
                                            for _rsp in _imsg["responses"]:
                                                button:
                                                    xysize (120, 30)
                                                    background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                                    hover_background Frame("images/ui/act_bar_hover.png", 16, 16, 16, 16)
                                                    action [Function(mark_message_replied, _imsg, _rsp["id"]), Hide("phone_messages_scr"), Hide("phone_home"), Function(renpy.jump, _rsp["label"])]
                                                    text _rsp["text"] font ACT_FONT size 12 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                                    elif _is_r and _imsg.get("replied_with"):
                                        $ _rt = next((r["text"] for r in _imsg.get("responses", []) if r["id"] == _imsg.get("replied_with")), "")
                                        if _rt:
                                            text ("You: " + _rt) font ACT_FONT size 11 color "#4a7a9b"
                    # ── NPC Contacts ──────────────────────────────────
                    $ _known = [k for k in npc_contacts if k in NPC_DATA]
                    if _known:
                        null height 4
                        text "Contacts" font PROFILE_FONT size 15 color "#9fb6d6"
                        null height 2
                        for _k in _known:
                            $ _last  = npc_last_message(_k)
                            $ _texted = _k in npc_texted_today
                            $ _loc   = npc_location_now(_k)
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (12, 8, 12, 8)
                                vbox:
                                    spacing 4
                                    hbox:
                                        spacing 6
                                        text NPC_DATA[_k]["name"] font PROFILE_FONT size 14 color "#cfe0f5" yalign 0.5
                                        if _loc:
                                            $ _pname = LOCATION_NAMES.get(_loc, "")
                                            if _pname:
                                                text ("@ " + _pname) font ACT_FONT size 11 color "#4a8a6a" yalign 0.5
                                    if _last:
                                        $ _msg_today = _last.get("delivered_on", _last.get("send_on_day", _last.get("day", -1))) == day
                                        text _last["text"] font ACT_FONT size 12 color ("#9fb6d6" if _msg_today else "#3a5068")
                                    $ _rmems = relationship_memories_for(_k)
                                    if _rmems:
                                        $ _recent_mems = _rmems[-2:]
                                        for _rm in _recent_mems:
                                            text ("• " + _rm["title"] + " — Day " + str(_rm["day"] + 1)) font ACT_FONT size 11 color "#3a5068"
                                    hbox:
                                        spacing 8
                                        button:
                                            xysize (120, 32)
                                            sensitive not _texted
                                            background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                                            hover_background Frame("images/ui/act_bar_hover.png", 20, 20, 20, 20)
                                            action Function(phone_say_hi, _k)
                                            text "Say hi" font ACT_FONT size 13 color ("#7a9ab8" if _texted else "#cfe0f5") hover_color "#ffffff" align (0.5, 0.5)
                                        button:
                                            xysize (130, 32)
                                            background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                                            hover_background Frame("images/ui/act_bar_hover.png", 20, 20, 20, 20)
                                            action Function(phone_where_is, _k)
                                            text "Where are you?" font ACT_FONT size 11 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                    elif not daily_events:
                        text "No messages." font ACT_FONT size 15 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("phone_messages_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"



screen phone_goals_scr():
    modal True
    add "#000000aa"
    frame:
        xalign 0.985
        yalign 0.5
        xsize 380
        ysize 720
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (24, 22, 24, 22)
        vbox:
            spacing 8
            text "Goals" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 4
            $ _active = active_quests()
            $ _done   = completed_quests()
            viewport:
                ysize 590
                mousewheel True
                vbox:
                    spacing 8
                    xsize 332
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
                    else:
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
            textbutton "Back" action [Hide("phone_goals_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_settings():
    modal True
    add "#000000aa"
    frame:
        xalign 0.985
        yalign 0.5
        xsize 380
        ysize 720
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (26, 22, 26, 22)
        vbox:
            spacing 16
            text "Settings" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 6
            text "Text speed" font PROFILE_FONT size 17 color "#cfe0f5"
            bar value Preference("text speed") xsize 300
            text "Music volume" font PROFILE_FONT size 17 color "#cfe0f5"
            bar value Preference("music volume") xsize 300
            text "Sound volume" font PROFILE_FONT size 17 color "#cfe0f5"
            bar value Preference("sound volume") xsize 300
            null height 6
            textbutton "Auto-forward: toggle" action Preference("auto-forward", "toggle") text_font ACT_FONT text_size 18
            textbutton "Fullscreen: toggle" action Preference("display", "toggle") text_font ACT_FONT text_size 18
            null height 8
            textbutton "Back" action [Hide("phone_settings"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_bank_scr():
    modal True
    add "#000000aa"
    frame:
        xalign 0.985
        yalign 0.5
        xsize 380
        ysize 720
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (24, 22, 24, 22)
        vbox:
            spacing 10
            text "City Bank" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 6
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
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
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
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        action [SetVariable("money", money - _repay_full), SetVariable("loan", loan - _repay_full), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Repay all  (-$%d)" % _repay_full font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                if _repay_half < _repay_full:
                    button:
                        xfill True ysize 56
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
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
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        action [SetVariable("money", money - _dep), SetVariable("savings", savings + _dep), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Deposit $%d" % _dep font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
                if savings > 0:
                    button:
                        xfill True ysize 56
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        action [SetVariable("money", money + savings), SetVariable("savings", 0), Hide("phone_bank_scr"), Show("phone_home")]
                        text "Withdraw all  +$[savings]" font ACT_FONT size 17 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)
            null height 8
            textbutton "Back" action [Hide("phone_bank_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
