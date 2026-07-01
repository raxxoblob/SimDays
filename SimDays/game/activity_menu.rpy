# Activity chooser — left-side panel of pill items (icon + label).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

transform act_item:
    on idle:
        linear 0.10 zoom 1.0
    on hover:
        linear 0.10 zoom 1.04

screen activity(items):
    # left panel, ~24% of a 1920 screen; height grows with item count (Frame stretch)
    frame:
        xpos 40
        yalign 0.5
        background Frame("images/ui/activity_panel.png", 40, 50, 40, 130)
        padding (30, 40, 30, 54)

        viewport:
            xsize 392
            ymaximum 560
            mousewheel True
            scrollbars ("vertical" if len(items) > 5 else None)
            vbox:
                spacing 12
                for i in items:
                    button:
                        action i.action
                        xysize (384, 84)
                        background Frame("images/ui/activity_item.png", 58, 30, 58, 30)
                        at act_item
                        hbox:
                            yalign 0.5
                            spacing 14
                            add "images/ui/activity_dot.png" xysize (54, 54) yalign 0.5
                            text i.caption font "fonts/VarelaRound.ttf" size 21 color "#0a3a6e" hover_color "#1565c0" yalign 0.5
