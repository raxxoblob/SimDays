# Activity chooser - floating left-side list of rounded 'glass' bars.
# No panel background: just the bars themselves (narrower, lighter, nicer type).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

define ACT_FONT = "fonts/Quicksand-SemiBold.ttf"   # swap weight here globally

transform act_item:
    on idle:
        linear 0.12 zoom 1.0 xoffset 0
    on hover:
        linear 0.12 zoom 1.03 xoffset 8   # nudges right on hover for a subtle lift

screen activity(items):
    # left column, ~19% of a 1920 screen; height grows with item count.
    viewport:
        xpos 44
        yalign 0.5
        xsize 372
        ymaximum 720
        mousewheel True
        scrollbars ("vertical" if len(items) > 7 else None)
        vbox:
            spacing 12
            for i in items:
                button:
                    action i.action
                    xysize (360, 72)
                    background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                    hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                    at act_item
                    text i.caption:
                        font ACT_FONT
                        size 22
                        color "#cfe0f5"
                        hover_color "#ffffff"
                        xpos 34
                        yalign 0.5
                        line_leading 2
