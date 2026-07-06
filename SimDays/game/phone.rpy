# Phone - pure screen overlay. HUD uses Show("phone_home"); Close uses Hide.
# No script Call() involved, so the phone never interrupts or re-triggers labels.

init python:
    def _phone_order(kind):
        if kind == "full":
            if store.money < 40: return
            gain_money(-40); spend_time(0.5)
            store.need_hunger = min(100, store.need_hunger + 60)
        elif kind == "takeout":
            if store.money < 20: return
            gain_money(-20); spend_time(0.5)
            store.need_hunger = min(100, store.need_hunger + 40)


screen _phone_app(label, act):
    button:
        xfill True
        ysize 68
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
        action act
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
            use _phone_app("Messages",  [Hide("phone_home"), Show("phone_messages_scr")])
            use _phone_app("Stocks",    [Hide("phone_home"), Show("stock_market")])
            use _phone_app("Groceries", [Hide("phone_home"), Show("phone_groceries_scr")])
            use _phone_app("Settings",  [Hide("phone_home"), Show("phone_settings")])
            null height 6
            textbutton "Close" action Hide("phone_home") xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


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
                    use _phone_app(NPC_DATA[_k]["name"], [Hide("phone_messages_scr"), Show("phone_home")])
            else:
                text "No contacts yet. Meet people out in the city." font PROFILE_FONT size 16 color "#9fb6d6"
            null height 6
            textbutton "Back" action [Hide("phone_messages_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


screen phone_groceries_scr():
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
            spacing 14
            text "Groceries" font PROFILE_FONT size 28 color "#ffffff" xalign 0.5
            null height 6
            use _phone_app("Grocery run — stock the fridge ($40)", Function(_phone_order, "full"))
            use _phone_app("Takeout delivered ($20)",               Function(_phone_order, "takeout"))
            null height 6
            textbutton "Back" action [Hide("phone_groceries_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


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
