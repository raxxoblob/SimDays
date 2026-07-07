# Phone - pure screen overlay. HUD uses Show("phone_home"); Close uses Hide.
# No script Call() involved, so the phone never interrupts or re-triggers labels.


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
            text "Messages" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 4
            # ── City News (system events) ──────────────────────────────
            if daily_events:
                for _ev in daily_events:
                    frame:
                        xfill True
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        padding (14, 10, 14, 10)
                        vbox:
                            spacing 2
                            text _ev["from"] font PROFILE_FONT size 13 color "#5bcafa"
                            text _ev["body"] font ACT_FONT size 14 color "#cfe0f5"
            else:
                text "No new messages today." font ACT_FONT size 15 color "#4a6080"
            # ── NPC contacts ──────────────────────────────────────────
            $ _known = [k for k in npc_contacts if k in NPC_DATA]
            if _known:
                null height 6
                text "Contacts" font PROFILE_FONT size 17 color "#9fb6d6"
                for _k in _known:
                    use _phone_app(NPC_DATA[_k]["name"], [Hide("phone_messages_scr"), Show("phone_home")])
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
                text "Loan:     $[loan]  (10%/wk)" font PROFILE_FONT size 16 color "#e86a55"
            if savings > 0:
                text "Savings:  $[savings]  (2%/wk)" font PROFILE_FONT size 16 color "#5bcafa"
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
                text "Savings (2%/wk)" font PROFILE_FONT size 15 color "#9fb6d6"
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
