# Activity chooser - floating left-side list of rounded 'glass' bars.
# No panel background: just the bars themselves (narrower, lighter, nicer type).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

define ACT_FONT = "fonts/Quicksand-SemiBold.ttf"   # swap weight here globally

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
                    button:
                        action i.action
                        sensitive i.sensitive
                        xysize (360, 72)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        insensitive_background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        at act_item
                        text i.caption:
                            font ACT_FONT
                            size 20
                            color "#cfe0f5"
                            hover_color "#ffffff"
                            insensitive_color "#4e606e"
                            xpos 30
                            xsize 300
                            yalign 0.5
                            line_leading 0

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        vbox:
            xsize 150
            spacing 4
            imagebutton:
                xalign 0.5
                idle  Transform("images/ui/icons/icon_metro.png", size=(120, 120))
                hover Transform("images/ui/icons/icon_metro.png", size=(132, 132))
                action Jump(activity_exit_jump)
            text "[activity_exit_name]" xalign 0.5 size 16 color "#ffffff"
