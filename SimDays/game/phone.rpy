# The phone - a frameless overlay (no plugin, no art needed). Open from the HUD
# button (bottom-right) or the P key. Apps: Messages, Stocks, Groceries, Settings.

# one big glass app button
screen _phone_app(label, ret):
    button:
        xfill True
        ysize 68
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
        action Return(ret)
        text label font ACT_FONT size 22 color "#cfe0f5" hover_color "#ffffff" align (0.5, 0.5)


screen phone_home():
    modal True
    add "#000000aa"
    $ _clock = time_label(hour)
    frame:
        xalign 0.985
        yalign 0.5
        xsize 380
        ysize 720
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (24, 22, 24, 22)
        vbox:
            spacing 14
            text "[_clock]" font PROFILE_FONT size 20 color "#9fb6d6" xalign 0.5
            text "Phone" font PROFILE_FONT size 30 color "#ffffff" xalign 0.5
            null height 6
            use _phone_app("Messages", "messages")
            use _phone_app("Stocks", "stocks")
            use _phone_app("Groceries", "groceries")
            use _phone_app("Settings", "settings")
            null height 6
            textbutton "Close" action Return("close") xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


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
            $ _contacts = [k for k in NPC_DATA if npc_known(k)]
            if _contacts:
                for _k in _contacts:
                    use _phone_app(NPC_DATA[_k]["name"], _k)
            else:
                text "No contacts yet. Meet people out in the city." font PROFILE_FONT size 16 color "#9fb6d6"
            null height 6
            textbutton "Back" action Return("back") xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


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
            textbutton "Back" action Return("back") xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Driver ─────────────────────────────────────────────────────────────
label open_phone:
    $ _pact = ""
    while _pact != "close":
        $ _pact = renpy.call_screen("phone_home")
        if _pact == "stocks":
            call screen stock_market
        elif _pact == "messages":
            call phone_messages
        elif _pact == "groceries":
            call phone_groceries
        elif _pact == "settings":
            call screen phone_settings
    return


label phone_messages:
    while True:
        $ _who = renpy.call_screen("phone_messages_scr")
        if _who == "back":
            return
        $ _nm = NPC_DATA[_who]["name"]
        $ _c = getattr(store, NPC_DATA[_who]["say"])
        menu:
            "Text [_nm]:"
            "Say hi (+a little affection)":
                $ _apply_aff(_who, 2)
                $ renpy.say(_c, "Hey! Good to hear from you.")
            "Invite out" if npc_aff(_who) >= 30:
                call npc_date(_who)
                return
            "Never mind":
                pass


label phone_groceries:
    menu:
        "Order online:"
        "Grocery run - stock the fridge ($40)":
            if money < 40:
                "Your card gets declined. Embarrassing."
            else:
                $ gain_money(-40)
                $ spend_time(0.5)
                $ need_hunger = min(100, need_hunger + 60)
                "A box of groceries at the door within the hour. Fridge stocked."
            jump phone_groceries
        "Takeout delivered ($20)":
            if money < 20:
                "Not enough for delivery right now."
            else:
                $ gain_money(-20)
                $ spend_time(0.5)
                $ need_hunger = min(100, need_hunger + 40)
                "Hot food at the door. Worth every cent."
            jump phone_groceries
        "Back":
            return
