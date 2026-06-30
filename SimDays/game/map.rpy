# City map screen

screen city_map():
    tag menu
    zorder 5

    # Semi-transparent panel on the left
    frame:
        xpos 30
        ypos 70
        xsize 240
        background "#000000aa"
        padding (14, 14, 14, 14)
        vbox:
            spacing 2
            text "CITY MAP" style "map_title"
            text "[day_name(day)], Day [day+1]" style "map_subtitle"
            null height 10

            textbutton "Home"          action Jump("location_home")    style "map_btn"
            textbutton "Coffee Shop"    action Jump("location_cafe")    style "map_btn"
            textbutton "Gym"            action Jump("location_gym")     style "map_btn"
            textbutton "Library"        action Jump("location_library") style "map_btn"
            textbutton "Bar"            action Jump("location_bar")     style "map_btn"
            textbutton "Nexus Tower"    action Jump("location_office")  style "map_btn"
            textbutton "Mall"           action Jump("location_mall")    style "map_btn"
            textbutton "Park"           action Jump("location_park")    style "map_btn"
            textbutton "Beach"          action Jump("location_beach")   style "map_btn"
            null height 10
            textbutton "Sleep / End Day" action Jump("action_sleep")    style "map_btn_sleep"


# ── Styles ────────────────────────────────────────────────────────────
# Text displayables (text statement) -> plain text styles
style map_title is default:
    size 16
    color "#f0c040"
    bold True

style map_subtitle is default:
    size 12
    color "#aaaaaa"

# Buttons: the button style holds background/padding,
# the matching <name>_text style holds the text color/size.
style map_btn is button:
    background None
    hover_background "#ffffff22"
    padding (8, 4, 8, 4)
    xfill True

style map_btn_text is button_text:
    size 16
    idle_color "#ffffff"
    hover_color "#f0c040"

style map_btn_sleep is button:
    background None
    hover_background "#ffffff22"
    padding (8, 4, 8, 4)
    xfill True

style map_btn_sleep_text is button_text:
    size 15
    idle_color "#88aaff"
    hover_color "#aaccff"
