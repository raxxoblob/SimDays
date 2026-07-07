# Activity chooser - floating left-side list of rounded 'glass' bars.
# No panel background: just the bars themselves (narrower, lighter, nicer type).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

define ACT_FONT = "fonts/Quicksand-SemiBold.ttf"   # swap weight here globally

init python:
    import re as _re
    def _split_caption(cap):
        """Split 'Name ($X, +Y) [[Lock]]' into (name, cost_str).
        Strips [[...]] requirement hints from both parts."""
        plain = _re.sub(r'\s*\[\[.*?\]\]', '', cap)
        idx = plain.find('(')
        if idx > 0:
            return plain[:idx].strip(), plain[idx:].strip()
        return plain.strip(), ''

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
            for i in items:
                if i.action is not None:
                    $ _nm, _cs = _split_caption(i.caption)
                    button:
                        action i.action
                        sensitive getattr(i, 'sensitive', True)
                        xysize (360, 76)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        insensitive_background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        at act_item
                        fixed:
                            yalign 0.5
                            xsize 340
                            xpos 10
                            text _nm:
                                font ACT_FONT size 19 color "#cfe0f5" hover_color "#ffffff" insensitive_color "#4e606e" xpos 14 xsize 195 yalign 0.5 line_leading 0
                            if _cs:
                                text _cs:
                                    font ACT_FONT size 12 color "#527090" hover_color "#8ab0d0" insensitive_color "#3a4a56" xpos 212 xsize 128 yalign 0.5 line_leading 0 xalign 1.0

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        vbox:
            xsize 150
            spacing 4
            $ _exit_icon = "apartment_ext" if activity_exit_name == "Hallway" else "metro"
            imagebutton:
                xalign 0.5
                idle  Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(120, 120))
                hover Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(132, 132))
                action Jump(activity_exit_jump)
            text "[activity_exit_name]" xalign 0.5 size 16 color "#ffffff"
