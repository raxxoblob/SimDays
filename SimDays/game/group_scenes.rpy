# Group interaction — fires whenever two related NPCs are at the same location.
# Repeatable: no "seen" tracking. Scripted one-time scenes go here later as
# separate labels called from NPC_RELATIONS["scene"] when that key is added.


label group_interact(npc_a, npc_b):
    $ _gna  = NPC_DATA[npc_a]["name"]
    $ _gnb  = NPC_DATA[npc_b]["name"]
    $ _gused = []   # topics used this session
    show expression NPC_DATA[npc_a]["sprite"] as npcsprite  at sprite_r
    show expression NPC_DATA[npc_b]["sprite"] as npcsprite2 at sprite_l
    show screen hud
    "[_gna] and [_gnb] make room as you join them."

    $ _group_on = True
    while _group_on:
        menu (screen="activity"):
            "Music" if "music" not in _gused:
                $ _gused = _gused + ["music"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "music")
                $ _grb = _do_talk_group(npc_b, "music")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Sports & fitness" if "sports" not in _gused:
                $ _gused = _gused + ["sports"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "sports")
                $ _grb = _do_talk_group(npc_b, "sports")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Art" if "art" not in _gused:
                $ _gused = _gused + ["art"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "art")
                $ _grb = _do_talk_group(npc_b, "art")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Food" if "food" not in _gused:
                $ _gused = _gused + ["food"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "food")
                $ _grb = _do_talk_group(npc_b, "food")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Money & ambition" if "ambition" not in _gused:
                $ _gused = _gused + ["ambition"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "ambition")
                $ _grb = _do_talk_group(npc_b, "ambition")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Travel" if "travel" not in _gused:
                $ _gused = _gused + ["travel"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "travel")
                $ _grb = _do_talk_group(npc_b, "travel")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Movies" if "movies" not in _gused:
                $ _gused = _gused + ["movies"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "movies")
                $ _grb = _do_talk_group(npc_b, "movies")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Nightlife" if "nightlife" not in _gused:
                $ _gused = _gused + ["nightlife"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "nightlife")
                $ _grb = _do_talk_group(npc_b, "nightlife")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Work & life" if "work" not in _gused:
                $ _gused = _gused + ["work"]
                $ spend_time(0.5)
                $ _gra = _do_talk_group(npc_a, "work")
                $ _grb = _do_talk_group(npc_b, "work")
                "[_gna]: [GROUP_REACT_TEXT[_gra].format(name=_gna)]"
                "[_gnb]: [GROUP_REACT_TEXT[_grb].format(name=_gnb)]"
            "Leave":
                $ _group_on = False

    hide npcsprite
    hide npcsprite2
    return
