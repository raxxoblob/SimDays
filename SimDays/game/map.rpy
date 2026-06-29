# City map screen

screen city_map():
    tag menu
    zorder 5

    # Semi-transparent panel on the left
    frame:
        xpos 30
        ypos 70
        xsize 220
        background "#00000099"
        padding (12, 12)
        vbox:
            spacing 4
            text "[ CITY MAP ]" style "map_title"
            text "[day_name(day)], Day [day+1]" style "map_subtitle"
            null height 8

            textbutton "🏠  Home"          action Jump("location_home")    style "map_btn"
            textbutton "☕  Coffee Shop"   action Jump("location_cafe")    style "map_btn"
            textbutton "💪  Gym"           action Jump("location_gym")     style "map_btn"
            textbutton "📚  Library"       action Jump("location_library") style "map_btn"
            textbutton "🍸  Bar"           action Jump("location_bar")     style "map_btn"
            textbutton "🏢  Nexus Tower"   action Jump("location_office")  style "map_btn"
            textbutton "🛍  Mall"           action Jump("location_mall")    style "map_btn"
            textbutton "🌳  Park"          action Jump("location_park")    style "map_btn"
            textbutton "🏖  Beach"         action Jump("location_beach")   style "map_btn"
            null height 8
            textbutton "💤  Sleep / End Day" action Jump("action_sleep")   style "map_btn_sleep"

style map_title:
    size 13
    color "#f0c040"
    bold True

style map_subtitle:
    size 11
    color "#aaaaaa"

style map_btn:
    size 15
    color "#ffffff"
    hover_color "#f0c040"
    idle_background  "#00000000"
    hover_background "#ffffff22"
    padding (6, 3, 6, 3)

style map_btn_sleep:
    size 14
    color "#88aaff"
    hover_color "#aaccff"
    idle_background  "#00000000"
    hover_background "#ffffff22"
    padding (6, 3, 6, 3)
