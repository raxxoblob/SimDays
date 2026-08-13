# Always-on HUD. The visuals live in hud_v2.rpy (day/time island top-left, needs
# island top-centre). This screen keeps the name `hud` because ~414
# `show screen hud` statements across the script reference it.
#
# What stays here: the global key bindings, the bottom-corner phone peek and
# "Me" button, the tooltip line and the next-commitment reminder — i.e. the
# non-island chrome that already existed.

screen hud():
    zorder 10

    key "K_c" action ToggleScreen("profile")
    key "K_p" action Show("phone_home")

    if hud_mode == "full":
        use hud_v2
    elif hud_mode == "minimal":
        use hud_v2_minimal
    else:
        null   # "hidden" — islands suppressed; null prevents empty-branch lint warning

    # phone peek — hidden whenever any phone surface (home or an app) is open
    if not phone_open():
        imagebutton:
            xpos 1460 ypos 986
            idle  Transform("images/ui/phone.png", crop=(0, 0, 1024, 215), size=(460, 94))
            hover Transform("images/ui/phone.png", crop=(0, 0, 1024, 215), size=(470, 97))
            action Show("phone_home")
        if unread_message_count() > 0:
            $ _hud_uc = unread_message_count()
            text ("(" + ("9+" if _hud_uc > 9 else str(_hud_uc)) + ")") xpos 1875 ypos 988 font "fonts/Quicksand-SemiBold.ttf" size 20 color "#e05533" outlines [(2, "#000000", 0, 0)]

    # "Me" / stats button — upper-right corner, same height and shell as the HUD
    # islands (HUD2_BG + HUD2_LINE) so the top row reads as one band.
    button:
        xpos HUD2["me_x"]
        ypos HUD2["top_y"]
        xysize (HUD2["me_w"], HUD2["island_h"])
        padding (0, 0, 0, 0)
        background HUD2_BG
        hover_background HUD2_BG_HOVER
        action ToggleScreen("profile")
        tooltip "Your stats, skills, work and assets."
        frame:
            background HUD2_LINE
            xfill True
            yfill True
            padding (0, 0, 0, 0)
            text "Me":
                font HUD2["font"] size 24 color HUD2["text_cap"] align (0.5, 0.5)

    $ _tt = GetTooltip()
    if _tt:
        text "[_tt]":
            xalign 0.5 ypos 126 size 17 color "#ffffff"
            font "fonts/Quicksand-SemiBold.ttf"
            outlines [(2, "#000000cc", 0, 0)]

    # Next-commitment reminder: show when ≤3h away regardless of notified state.
    # FIX 4: notified only gates the one-time toast in phone_messages.notify_available_commitments.
    $ _nc = next_commitment()
    if _nc and hours_until_commitment(_nc) <= 3 and hours_until_commitment(_nc) > 0:
        $ _nc_hrs = hours_until_commitment(_nc)
        $ _nc_time = "in 30min" if _nc_hrs < 0.5 else ("in %dh" % int(_nc_hrs) if _nc_hrs >= 1 else "in 30min")
        $ _nc_txt  = _nc["title"] + " — " + _nc_time
        text "[_nc_txt]":
            xalign 0.5 ypos 150 size 14 color "#5bcafa"
            font "fonts/Quicksand-SemiBold.ttf"
            outlines [(2, "#000000cc", 0, 0)]
