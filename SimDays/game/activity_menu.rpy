# Activity chooser - floating left-side list of rounded 'glass' bars.
# No panel background: just the bars themselves (narrower, lighter, nicer type).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

define ACT_FONT = "fonts/Quicksand-SemiBold.ttf"   # swap weight here globally

init python:
    from functools import lru_cache as _lru_cache

    @_lru_cache(maxsize=128)
    def _split_caption(cap):
        # strip trailing [[...]] lock annotation, then split at first (
        if "[[" in cap:
            cap = cap[:cap.index("[[")].rstrip()
        idx = cap.find("(")
        if idx > 0:
            return cap[:idx].rstrip(), cap[idx:]
        return cap, ""

    # ── Activity effects (hover tooltip) ──────────────────────────────────────
    # There is no in-engine effect list — each activity's effects are inline in its
    # menu branch — so this table mirrors them. Keyed by (current_loc, name) where
    # name is the caption before the "(...)". Each effect is (text, category);
    # category picks the colour. Values are the BASE case (event/supplement bonuses
    # still apply in-game but aren't spelled out). Unlisted activities show no panel.
    ACT_FX_COLOR = {
        "gain": "#7fd06a",   # stat/skill/need gains
        "cost": "#e8704d",   # money out
        "need": "#e8a24d",   # need drain (energy/hunger/hygiene down)
        "time": "#8fb0d0",   # time spent
        "info": "#b6c8dc",   # neutral note
        "earn": "#ffd66a",   # money in
    }
    ACTIVITY_EFFECTS = {
        # ── Grounds / café ───────────────────────────────────────────────
        ("location_cafe", "Buy a coffee"):        [("0.5h", "time"), ("-$3", "cost"), ("+10 Energy", "gain")],
        ("location_cafe", "Work a shift - Barista"): [("4h", "time"), ("+pay", "earn"), ("+Service exp", "gain"), ("-Energy", "need")],
        # ── Gym ──────────────────────────────────────────────────────────
        ("location_gym", "Train - weights"):      [("1.5h", "time"), ("-15 Energy", "need"), ("+20 Str exp", "gain"), ("+8 Appearance", "gain")],
        ("location_gym", "Cardio"):               [("1h", "time"), ("-12 Energy", "need"), ("+10 Str exp", "gain"), ("+4 Appearance", "gain")],
        ("location_gym", "Week pass"):            [("-$40", "cost"), ("7-day access", "info")],
        ("location_gym", "Month pass"):           [("-$120", "cost"), ("30-day access", "info")],
        ("location_gym", "Day rate"):             [("-$8", "cost"), ("1-day access", "info")],
        ("location_gym", "Buy Protein Shake"):    [("-$12", "cost"), ("+1 Protein", "info")],
        ("location_gym", "Work a shift"):         [("8h", "time"), ("+pay", "earn"), ("-Energy", "need")],
        # ── Park ─────────────────────────────────────────────────────────
        ("location_park", "Jog"):                 [("1h", "time"), ("+4 Str exp", "gain")],
        ("location_park", "Read a book"):         [("1.5h", "time"), ("+3 Int exp", "gain")],
        ("location_park", "Play basketball"):     [("1.5h", "time"), ("+8 Str exp", "gain")],
        # ── Bar ──────────────────────────────────────────────────────────
        ("location_bar", "Have a drink"):         [("0.5h", "time"), ("-$ drink", "cost")],
        ("location_bar", "Socialize"):            [("1h", "time"), ("+Charisma", "gain"), ("needs Chr 25", "info")],
    }

    def activity_fx(caption):
        """Effect list for an activity caption at the current location, or None."""
        name = _split_caption(caption)[0]
        return ACTIVITY_EFFECTS.get((store.current_loc, name))

default activity_exit_jump = "map"
default activity_exit_name = "City"

transform act_item:
    on idle:
        linear 0.12 zoom 1.0 xoffset 0
    on hover:
        linear 0.12 zoom 1.03 xoffset 8   # nudges right on hover for a subtle lift
    on insensitive:
        zoom 1.0 xoffset 0

screen activity(items):
    default _hover_fx = None
    default _hover_nm = None
    # left column, ~19% of a 1920 screen; height grows with item count.
    viewport:
        xpos 44
        ypos 360          # sits below the top-left gain toasts so they don't overlap
        xsize 372
        ymaximum 660
        mousewheel True
        scrollbars ("vertical" if len(items) > 7 else None)
        vbox:
            spacing 12
            $ _in_debt = in_debt()
            for i in items:
                if i.action is not None:
                    $ _nm, _cs = _split_caption(i.caption)
                    button:
                        action i.action
                        sensitive (getattr(i, 'sensitive', True) and not (_in_debt and "$" in _cs))
                        xysize (360, 76)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        insensitive_background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hovered [SetScreenVariable("_hover_fx", activity_fx(i.caption)), SetScreenVariable("_hover_nm", _nm)]
                        unhovered SetScreenVariable("_hover_fx", None)
                        at act_item
                        fixed:
                            yalign 0.5
                            xsize 340
                            xpos 10
                            text _nm:
                                font ACT_FONT size 19 color "#cfe0f5" hover_color "#ffffff" insensitive_color "#4e606e" xpos 14 xsize 195 yalign 0.5 line_leading 0
                            if _cs:
                                text _cs:
                                    font ACT_FONT size 12 color "#527090" hover_color "#8ab0d0" insensitive_color "#3a4a56" xpos 212 xsize 128 yalign 0.5 line_leading 0

    # Effects popup — appears to the right of the hovered activity bar.
    if _hover_fx:
        frame:
            xpos 430 ypos 372
            background Frame("images/ui/act_bar_idle.png", 24, 24, 24, 24)
            padding (18, 14, 20, 14)
            vbox:
                spacing 7
                text _hover_nm font ACT_FONT size 17 color "#ffffff"
                null height 2
                for _fx_txt, _fx_cat in _hover_fx:
                    text _fx_txt:
                        font ACT_FONT size 20 bold True
                        color ACT_FX_COLOR.get(_fx_cat, "#cfe0f5")
                        outlines [(2, "#000000cc", 0, 0)]

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        vbox:
            xsize 150
            spacing 4
            $ _exit_icon = "apartment_ext" if activity_exit_name == "Hallway" else "hub"  # ponytail: hub is a placeholder; a proper icon_city_map.png is needed
            imagebutton:
                xalign 0.5
                idle  Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(120, 120))
                hover Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(132, 132))
                action [Hide("people_here_dock"), Jump(activity_exit_jump)]
            text "[activity_exit_name]" xalign 0.5 size 16 color "#ffffff"


screen people_here_dock(return_location):
    zorder 11
    if (current_loc in ("location_cafe", "location_park", "location_bar", "location_sandbeach",
                        "location_library", "location_hospital", "location_gym", "location_nightclub",
                        "location_office", "location_warehouse", "location_diner", "location_college")
            and not renpy.get_screen("profile")
            and not renpy.get_screen("phone_home")
            and not renpy.get_screen("npc_relbar")):
        $ _dock_npcs = [n for n in public_talkable_npcs_here() if NPC_DATA[n].get("portrait")]
        $ _dock_vis  = _dock_npcs[:4]
        $ _dock_extra = len(_dock_npcs) - 4
        if _dock_vis:
            frame:
                xpos 44
                ypos 164
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                padding (10, 8, 10, 8)
                hbox:
                    spacing 8
                    for npc_id in _dock_vis:
                        $ _enc = npc_has_been_encountered(npc_id)
                        $ _disp = NPC_DATA[npc_id]["name"] if _enc else "Stranger"
                        button:
                            xysize (108, 128)
                            background None
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                            action [SetVariable("_dock_npc", npc_id), SetVariable("_dock_return", return_location), Jump("npc_interact_from_dock")]
                            vbox:
                                spacing 4
                                xalign 0.5
                                # portrait always visible — strangers are named "Stranger"
                                # below but still show their face icon
                                add portrait_circle(npc_id, 100) xalign 0.5
                                text _disp:
                                    size 10 font ACT_FONT color "#b0c4d8" hover_color "#e0ecff"
                                    xalign 0.5
                    if _dock_extra > 0:
                        vbox:
                            yalign 0.5
                            text ("+%d" % _dock_extra):
                                size 13 font ACT_FONT color "#6a8098"
                                align (0.5, 0.5)
