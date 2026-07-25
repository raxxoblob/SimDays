# ═══════════════════════════════════════════════════════════════════════════
# DEV ONLY — Sprite Reaction Preview
# Does NOT appear in any game menu. Safe to leave in the repo.
# Does NOT modify any game variable, affection, trust, time, or story flag.
#
# Launch from developer console:
#   jump test_sprite_reactions
# ═══════════════════════════════════════════════════════════════════════════

image _test_preview_bg = Solid("#1c1c2e")

# ── Subtle variants (roughly half the displacement of the normal transforms)

transform _preview_bounce_subtle:
    yoffset 96
    ease 0.09 yoffset 90
    ease 0.14 yoffset 96

transform _preview_shake_subtle:
    xoffset 0
    linear 0.06 xoffset 4
    linear 0.06 xoffset -3
    linear 0.07 xoffset 2
    linear 0.07 xoffset 0

transform _preview_step_back_subtle:
    yoffset 96
    ease 0.10 yoffset 101
    ease 0.16 yoffset 96

transform _preview_lean_in_subtle:
    yoffset 96
    ease 0.12 yoffset 92
    ease 0.16 yoffset 96

transform _preview_nod_subtle:
    yoffset 96
    ease 0.08 yoffset 100
    ease 0.10 yoffset 96

transform _preview_sigh_subtle:
    yoffset 96
    ease 0.16 yoffset 101
    ease 0.22 yoffset 96

# ── Styles ──────────────────────────────────────────────────────────────────

style _preview_btn:
    background "#2e2e3e"
    hover_background "#4a4a6a"
    selected_background "#2a3a5a"
    selected_hover_background "#3a4a7a"
    padding (10, 6, 10, 6)
    xminimum 88

style _preview_btn_text:
    color "#cccccc"
    hover_color "#ffffff"
    selected_color "#88aaff"
    size 13

# ── Preview screen ───────────────────────────────────────────────────────────

screen sprite_reaction_preview(intensity):
    zorder 100

    frame:
        xalign 1.0
        yalign 0.5
        xoffset -14
        xsize 300
        background "#161620"
        padding (14, 14, 14, 14)

        vbox:
            spacing 8

            text "REACTION PREVIEW" size 13 color "#ffff66"
            text "DEV ONLY" size 10 color "#ff6666"

            null height 4

            hbox:
                spacing 6
                yalign 0.5
                text "Intensity:" size 12 color "#999999" yalign 0.5
                textbutton "Subtle" action Return(("intensity", "subtle")) style "_preview_btn" selected (intensity == "subtle")
                textbutton "Normal" action Return(("intensity", "normal")) style "_preview_btn" selected (intensity == "normal")

            null height 2

            frame:
                background "#0e0e1a"
                padding (8, 8, 8, 8)

                vbox:
                    spacing 7

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Bounce"    action Return(("anim", "bounce"))    style "_preview_btn"
                        text "quick upward hop"          size 11 color "#777777" yalign 0.5

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Shake"     action Return(("anim", "shake"))     style "_preview_btn"
                        text "short horizontal rattle"   size 11 color "#777777" yalign 0.5

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Step back" action Return(("anim", "step_back")) style "_preview_btn"
                        text "small downward recoil"     size 11 color "#777777" yalign 0.5

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Lean in"   action Return(("anim", "lean_in"))   style "_preview_btn"
                        text "small upward emphasis"     size 11 color "#777777" yalign 0.5

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Nod"       action Return(("anim", "nod"))       style "_preview_btn"
                        text "tiny dip and return"       size 11 color "#777777" yalign 0.5

                    hbox:
                        spacing 10
                        yalign 0.5
                        textbutton "Sigh"      action Return(("anim", "sigh"))      style "_preview_btn"
                        text "slower downward settle"    size 11 color "#777777" yalign 0.5

            null height 2

            hbox:
                spacing 8
                textbutton "Reset" action Return(("anim", "reset")) style "_preview_btn"
                textbutton "Exit"  action Return(("exit",  None))   style "_preview_btn"

            null height 4

            text "sprite: nora_cafe_normal" size 10 color "#444466"
            text "position: sprite_c" size 10 color "#444466"

# ── Preview label ────────────────────────────────────────────────────────────

label test_sprite_reactions:
    # DEV ONLY — jump test_sprite_reactions from console to enter
    scene _test_preview_bg
    show nora_cafe_normal at sprite_c

    $ _tr_intensity = "normal"

    label .loop:
        call screen sprite_reaction_preview(_tr_intensity)
        $ _tr_result = _return

        if _tr_result[0] == "exit":
            hide nora_cafe_normal
            return

        if _tr_result[0] == "intensity":
            $ _tr_intensity = _tr_result[1]
            jump test_sprite_reactions.loop

        if _tr_result[0] == "anim":
            $ _tr_anim = _tr_result[1]

            if _tr_anim == "reset":
                show nora_cafe_normal at sprite_c
                jump test_sprite_reactions.loop

            if _tr_anim == "bounce":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_bounce_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_bounce

            elif _tr_anim == "shake":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_shake_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_shake

            elif _tr_anim == "step_back":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_step_back_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_step_back

            elif _tr_anim == "lean_in":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_lean_in_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_lean_in

            elif _tr_anim == "nod":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_nod_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_nod

            elif _tr_anim == "sigh":
                if _tr_intensity == "subtle":
                    show nora_cafe_normal at sprite_c, _preview_sigh_subtle
                else:
                    show nora_cafe_normal at sprite_c, react_sigh

            # Wait for the animation to complete before reopening the panel.
            # 0.7s covers the longest transform (react_sigh at 0.38s) with margin.
            $ renpy.pause(0.7, hard=True)

            jump test_sprite_reactions.loop
