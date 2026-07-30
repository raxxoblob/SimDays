# Developer visual check — Phase 52 presentation audit.
# Access: label dev_presentation_check
# Shows: normalized icon grid, People Here layouts (1/2/3/4), portrait states,
#        conversation sprite scale, phone shell with content.

init python:
    if config.developer:
        _DEV_CHECK_NPCS_4 = ["nora", "zoe", "eli", "marcus"]
        _DEV_CHECK_NPCS_3 = ["nora", "zoe", "eli"]
        _DEV_CHECK_NPCS_2 = ["nora", "zoe"]
        _DEV_CHECK_NPCS_1 = ["nora"]

        # NPCs for known/unknown demo: nora=known (has portrait+aff), sam=world NPC (may be unknown)
        _DEV_CHECK_KNOWN   = "nora"
        _DEV_CHECK_UNKNOWN = "sam"


screen dev_presentation_check():
    modal True
    add "#000000cc"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1440
        ysize 900
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (28, 20, 28, 20)
        vbox:
            spacing 16
            hbox:
                xfill True
                text "Phase 52 — Presentation Check" font PROFILE_FONT size 28 color "#5bcafa" yalign 0.5
                textbutton "Close" action Hide("dev_presentation_check") text_font ACT_FONT text_size 18 text_color "#9fb6d6" text_hover_color "#ffffff" xalign 1.0

            # ── Row 1: icon samples + portrait states ─────────────────────────────
            hbox:
                spacing 24
                # Location icons sample (from generated/)
                frame:
                    xsize 420
                    background "#0e1a22"
                    padding (12, 10, 12, 10)
                    vbox:
                        spacing 6
                        text "Location icons (normalized 84%)" font PROFILE_FONT size 13 color "#9fb6d6"
                        hbox:
                            spacing 8
                            for _ico in ["icon_coffee_shop", "icon_gym", "icon_hospital", "icon_park", "icon_bar"]:
                                add Transform("images/ui/generated/%s.png" % _ico, size=(66, 66))
                # Action icons sample (from generated/)
                frame:
                    xsize 360
                    background "#0e1a22"
                    padding (12, 10, 12, 10)
                    vbox:
                        spacing 6
                        text "Action icons (normalized 88%)" font PROFILE_FONT size 13 color "#9fb6d6"
                        hbox:
                            spacing 8
                            for _ico in ["act_talk", "act_hug", "act_invite", "act_gift", "act_leave"]:
                                add Transform("images/ui/generated/%s.png" % _ico, size=(66, 66))
                # Portrait states
                frame:
                    xsize 400
                    background "#0e1a22"
                    padding (12, 10, 12, 10)
                    vbox:
                        spacing 8
                        text "Portrait states" font PROFILE_FONT size 13 color "#9fb6d6"
                        hbox:
                            spacing 12
                            vbox:
                                spacing 4
                                xalign 0.5
                                add portrait_circle(_DEV_CHECK_KNOWN, 96) xalign 0.5
                                text "Known" font ACT_FONT size 11 color "#b0c4d8" xalign 0.5
                            vbox:
                                spacing 4
                                xalign 0.5
                                add portrait_circle_fallback(96) xalign 0.5
                                text "Stranger" font ACT_FONT size 11 color "#b0c4d8" xalign 0.5
                            vbox:
                                spacing 4
                                xalign 0.5
                                add portrait_circle(_DEV_CHECK_KNOWN, 90) xalign 0.5
                                text "Relbar (90)" font ACT_FONT size 11 color "#b0c4d8" xalign 0.5

            # ── Row 2: People Here dock layouts ──────────────────────────────────
            frame:
                xfill True
                background "#0e1a22"
                padding (12, 10, 12, 10)
                vbox:
                    spacing 8
                    text "People Here dock — 1 / 2 / 3 / 4 NPC layouts" font PROFILE_FONT size 13 color "#9fb6d6"
                    hbox:
                        spacing 32
                        for _cfg in [_DEV_CHECK_NPCS_1, _DEV_CHECK_NPCS_2, _DEV_CHECK_NPCS_3, _DEV_CHECK_NPCS_4]:
                            frame:
                                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                                padding (10, 8, 10, 8)
                                hbox:
                                    spacing 8
                                    for _nid in _cfg:
                                        $ _enc2 = npc_has_been_encountered(_nid)
                                        vbox:
                                            spacing 4
                                            xalign 0.5
                                            xysize (108, 128)
                                            if _enc2:
                                                add portrait_circle(_nid, 100) xalign 0.5
                                            else:
                                                add portrait_circle_fallback(100) xalign 0.5
                                            text (NPC_DATA[_nid]["name"] if _enc2 else "Stranger"):
                                                size 10 font ACT_FONT color "#b0c4d8" xalign 0.5

            # ── Row 3: sprite scale + phone shell preview ─────────────────────────
            hbox:
                spacing 24
                # Sprite scale note
                frame:
                    xsize 460
                    background "#0e1a22"
                    padding (16, 12, 16, 12)
                    vbox:
                        spacing 8
                        text "Conversation sprite scale" font PROFILE_FONT size 13 color "#9fb6d6"
                        text "sprite_c/r/l: xysize (660, 900)" font ACT_FONT size 13 color "#cfe0f5"
                        text "yoffset 96 (micro-anim base unchanged)" font ACT_FONT size 12 color "#7a9ab8"
                        text "Visible above dialogue bar:" font ACT_FONT size 12 color "#7a9ab8"
                        text "(900 - 96 - 200) / 1080 ≈ 55.9%" font PROFILE_FONT size 14 color "#39c07a"
                        text "Target: 55–65%  ✓" font ACT_FONT size 12 color "#39c07a"
                # Phone shell preview
                frame:
                    xsize 560
                    background "#0e1a22"
                    padding (16, 12, 16, 12)
                    vbox:
                        spacing 8
                        text "Phone shell containment" font PROFILE_FONT size 13 color "#9fb6d6"
                        text "phone_frame: xpos 1460, ypos 390, 460×690" font ACT_FONT size 12 color "#cfe0f5"
                        text "sub-apps: xpos 1462, ypos 392, 456×682" font ACT_FONT size 12 color "#cfe0f5"
                        text "Affected: Messages, Contacts, Goals, Settings, Bank, Help" font ACT_FONT size 11 color "#7a9ab8"
                        text "Not contained: Map, Jobs, Stocks (full-screen)" font ACT_FONT size 11 color "#4a6080"
                        text "phone_frame shows on app open, hides on Back" font ACT_FONT size 11 color "#7a9ab8"


label dev_presentation_check:
    if not config.developer:
        jump map
    show screen dev_presentation_check
    $ renpy.pause()
    hide screen dev_presentation_check
    jump map
