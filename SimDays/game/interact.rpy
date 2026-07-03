# Unified NPC interaction hub.
#   Enter a location, "Talk to <someone>" -> their sprite centres, a relationship
#   panel shows on the right, and the ACTIONS sit along the bottom:
#       Talk (pick 1 of 9 shared topics) · Give gift · Invite out · Leave
#   Topics are the SAME for everyone; each person LIKES / DISLIKES different ones,
#   so the same topic lands differently depending on who you're talking to.
#
# To add a character: one NPC_DATA entry (+ a greet label). No per-topic writing.

init python:
    def rel_tier(aff):
        if aff >= 75: return "Close"
        if aff >= 50: return "Good friends"
        if aff >= 25: return "Friends"
        if aff >= 1:  return "Acquaintance"
        return "Stranger"

    # The 9 shared conversation topics.
    TOPICS = [
        ("music",     "Music"),
        ("sports",    "Sports & fitness"),
        ("art",       "Art"),
        ("food",      "Food"),
        ("ambition",  "Money & ambition"),
        ("travel",    "Travel"),
        ("movies",    "Movies & shows"),
        ("nightlife", "Nightlife"),
        ("work",      "Work"),
    ]
    TOPIC_LABEL = dict(TOPICS)

    # say  = the Character variable to speak as (defined in characters.rpy)
    # world/met/min_status = availability (see npc_known)
    # likes/dislikes = which of the 9 topics land well / badly
    MON_FRI = {0, 1, 2, 3, 4}
    MON_SAT = {0, 1, 2, 3, 4, 5}
    NPC_DATA = {
        "nora": {
            "name": "Nora", "sprite": "nora_cafe_normal", "say": "n",
            "aff": "nora_affection", "trust": "nora_trust", "greet": "nora_greet",
            "world": True, "sched": [(None, (8, 18))],
            "likes": ["food", "ambition", "movies"], "dislikes": ["nightlife"],
        },
        "marcus": {
            "name": "Marcus", "sprite": "marcus_casual_normal", "say": "m",
            "aff": "marcus_affection", "trust": "marcus_trust", "greet": "marcus_greet",
            "world": True, "sched": [(None, (6, 11)), (None, (17, 27))],
            "likes": ["sports", "food", "nightlife"], "dislikes": ["art"],
        },
        "caroline": {
            "name": "Caroline", "sprite": "caroline_normal", "say": "caro",
            "aff": "caroline_affection", "trust": "caroline_trust", "greet": "caroline_greet",
            "met": "caroline_met", "sched": [(MON_FRI, (9, 18))],
            "likes": ["work", "ambition", "nightlife"], "dislikes": ["sports"],
        },
        "lena": {
            "name": "Dr. Lena", "sprite": "drlena_normal", "say": "lena",
            "aff": "lena_affection", "trust": "lena_trust", "greet": "lena_greet",
            "met": "lena_met", "sched": [(None, (8, 20))],
            "likes": ["work", "travel", "food"], "dislikes": ["nightlife"],
        },
        "natalie": {
            "name": "Natalie", "sprite": "natalie_normal", "say": "nat",
            "aff": "natalie_affection", "trust": "natalie_trust", "greet": "natalie_greet",
            "met": "natalie_met", "sched": [(MON_SAT, (7, 15))],
            "likes": ["sports", "work", "ambition"], "dislikes": ["art"],
        },
        "martha": {
            "name": "Martha", "sprite": "martha_neutral", "say": "ma",
            "aff": "martha_affection", "trust": "martha_trust", "greet": "martha_greet",
            "met": "martha_met", "min_status": 35, "sched": [(MON_FRI, (9, 18))],
            "likes": ["ambition", "work", "travel"], "dislikes": ["sports"],
        },
        "elle": {
            "name": "Elle", "sprite": "elle_sundress_normal", "say": "el",
            "aff": "elle_affection", "trust": "elle_trust", "greet": "elle_greet",
            "world": True, "sched": [({2}, (16, 19))],
            "likes": ["travel", "music", "art"], "dislikes": ["work"],
        },
    }

    def npc_aff(npc_id):   return getattr(store, NPC_DATA[npc_id]["aff"])
    def npc_trust(npc_id): return getattr(store, NPC_DATA[npc_id]["trust"])

    def npc_here(npc_id):
        sched = NPC_DATA[npc_id].get("sched")
        if not sched:
            return True
        wd = store.day % 7
        for days, (h0, h1) in sched:
            if (days is None or wd in days) and h0 <= store.hour < h1:
                return True
        return False

    def npc_known(npc_id):
        d = NPC_DATA[npc_id]
        if status_score() < d.get("min_status", 0):
            return False
        if d.get("world"):
            return True
        mv = d.get("met")
        return bool(getattr(store, mv)) if mv else True

    def npc_talkable(npc_id):
        return npc_here(npc_id) and npc_known(npc_id)

    # ── conversation reactions ─────────────────────────────────────────
    LIKE_LINES = [
        "%s? Now you're speaking my language.",
        "Okay, %s - finally, someone with taste.",
        "Don't get me started on %s. I could go all day.",
    ]
    NEUTRAL_LINES = [
        "%s? Sure, it's fine, I guess.",
        "Eh, no strong feelings on %s either way.",
        "%s, huh. It's alright.",
    ]
    DISLIKE_LINES = [
        "%s? Hard pass, honestly.",
        "Ugh, %s. Really not my thing.",
        "Let's talk about literally anything but %s.",
    ]

    def _apply_aff(npc_id, delta):
        av = NPC_DATA[npc_id]["aff"]
        setattr(store, av, max(0, min(getattr(store, av) + delta, affection_cap())))

    def do_talk(npc_id, topic):
        d = NPC_DATA[npc_id]
        spend_time(0.5)
        if topic in d.get("likes", []):
            delta, pool = 3, LIKE_LINES
        elif topic in d.get("dislikes", []):
            delta, pool = -1, DISLIKE_LINES
        else:
            delta, pool = 1, NEUTRAL_LINES
        _apply_aff(npc_id, delta)
        line = renpy.random.choice(pool) % TOPIC_LABEL[topic]
        renpy.say(getattr(store, d["say"]), line)

    def do_gift(npc_id):
        if store.gift_count <= 0:
            return
        store.gift_count -= 1
        _apply_aff(npc_id, 8)
        renpy.say(getattr(store, NPC_DATA[npc_id]["say"]),
                  "For me? ...That's genuinely thoughtful. Thank you.")


# ── Relationship panel (right, under the topbar) ───────────────────────
screen npc_relbar(npc_id):
    zorder 25
    $ _aff = npc_aff(npc_id)
    $ _tr = npc_trust(npc_id)
    $ _tier = rel_tier(_aff)
    $ _nm = NPC_DATA[npc_id]["name"]
    frame:
        xpos 1500
        ypos 150
        xsize 400
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 20)
        vbox:
            spacing 10
            text "[_nm]" font PROFILE_FONT size 30 color "#ffffff"
            text "[_tier]  (cap [affection_cap()])" font PROFILE_FONT size 16 color "#9fb6d6"
            null height 4
            hbox:
                spacing 10
                text "Affection" font PROFILE_FONT size 17 color "#cfe0f5" yalign 0.5 xsize 116
                bar:
                    value StaticValue(_aff, 100)
                    xsize 150 ysize 16 yalign 0.5
                    left_bar Frame("images/ui/bar_fill_str.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_aff]" font PROFILE_FONT size 17 color "#ffffff" yalign 0.5
            hbox:
                spacing 10
                text "Trust" font PROFILE_FONT size 17 color "#cfe0f5" yalign 0.5 xsize 116
                bar:
                    value StaticValue(_tr, 100)
                    xsize 150 ysize 16 yalign 0.5
                    left_bar Frame("images/ui/bar_fill_int.png", 14, 0) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_tr]" font PROFILE_FONT size 17 color "#ffffff" yalign 0.5


# reusable glass action button
screen _act_btn(label, ret, enabled=True):
    button:
        sensitive enabled
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
        padding (22, 12, 22, 12)
        action Return(ret)
        text label font ACT_FONT size 20 color ("#cfe0f5" if enabled else "#6b82a6") hover_color "#ffffff"


# ── Main action bar (bottom) ───────────────────────────────────────────
screen npc_actions(npc_id):
    zorder 22
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (18, 12, 18, 12)
        hbox:
            spacing 12
            use _act_btn("Talk", "talk")
            use _act_btn("Give gift (%d)" % gift_count, "gift", gift_count > 0)
            use _act_btn("Invite out", "date", npc_aff(npc_id) >= 30)
            use _act_btn("Leave", "leave")


# ── Topic picker (the 9 shared topics) ─────────────────────────────────
screen npc_topics(npc_id):
    zorder 22
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 16, 22, 16)
        vbox:
            spacing 12
            text "Talk about..." font ACT_FONT size 20 color "#9fb6d6" xalign 0.5
            vpgrid:
                cols 3
                spacing 12
                for key, label in TOPICS:
                    button:
                        xsize 240
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        padding (16, 10, 16, 10)
                        action Return(key)
                        text label font ACT_FONT size 19 color "#cfe0f5" hover_color "#ffffff" xalign 0.5
            textbutton "Back" action Return("back") xalign 0.5 text_font ACT_FONT text_size 18 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Driver ─────────────────────────────────────────────────────────────
label npc_interact(npc_id):
    $ _spr = NPC_DATA[npc_id]["sprite"]
    show expression _spr as npcsprite at sprite_c
    show screen npc_relbar(npc_id)
    $ _nm = NPC_DATA[npc_id]["name"]
    if need_hygiene < 25:
        "[_nm] leans back a little, trying to be polite about it. You could really use a shower."
    call expression NPC_DATA[npc_id]["greet"]
    $ _act = ""
    while _act != "leave":
        $ _act = renpy.call_screen("npc_actions", npc_id)
        if _act == "talk":
            $ _t = renpy.call_screen("npc_topics", npc_id)
            if _t != "back":
                $ do_talk(npc_id, _t)
        elif _act == "gift":
            $ do_gift(npc_id)
        elif _act == "date":
            call npc_date(npc_id)
            $ _act = "leave"   # a date is the whole evening
    hide screen npc_relbar
    hide npcsprite
    return


# ── Dates (works for everyone; unlocks at affection 30) ────────────────
label npc_date(npc_id):
    $ _nm = NPC_DATA[npc_id]["name"]
    $ _spr = NPC_DATA[npc_id]["sprite"]
    $ _c = getattr(store, NPC_DATA[npc_id]["say"])
    menu:
        "Take [_nm] where?"
        "Dinner out (3h)":
            scene restaurantnight
        "Rooftop drinks (3h)":
            scene bar_rooftop_night
        "A walk on the beach (3h)":
            scene beachnight
        "Actually, never mind":
            return
    show screen hud
    show expression _spr as npcsprite at sprite_c
    $ spend_time(3)
    $ _apply_aff(npc_id, 6)
    $ setattr(store, NPC_DATA[npc_id]["trust"], npc_trust(npc_id) + 3)
    $ renpy.say(_c, "This was... really nice. Let's do it again sometime.")
    hide npcsprite
    return


# ══ Greetings (scale with affection) ═══════════════════════════════════
label nora_greet:
    if nora_affection >= 50:
        n "Hey, you. I was hoping you'd come in today."
    elif nora_affection >= 25:
        n "There you are. The usual?"
    else:
        n "Back already? Coffee's that good, or...?"
    return

label marcus_greet:
    if marcus_affection >= 50:
        m "Was just about to text you. What's up, man?"
    elif marcus_affection >= 25:
        m "There he is. Grab a seat."
    else:
        m "Hey, neighbor. Surviving?"
    return

label caroline_greet:
    if caroline_affection >= 50:
        caro "There's my favorite source of interesting problems. Sit."
    elif caroline_affection >= 25:
        caro "Look who it is. Whatever you did, I already know."
    else:
        caro "HR. If you're not on fire, make it quick."
    return

label lena_greet:
    if lena_affection >= 50:
        lena "Oh good, a face that isn't a chart. Two minutes, they're yours."
    elif lena_affection >= 25:
        lena "Hey. Still standing? Good. Half my morning wasn't."
    else:
        lena "If you're not bleeding, you're in the wrong line - but hi."
    return

label natalie_greet:
    if natalie_affection >= 50:
        nat "There's my reliable one. Don't let it go to your head."
    elif natalie_affection >= 25:
        nat "You again. Fine. You work harder than half the floor, so - what."
    else:
        nat "You lost? Break room's that way."
    return

label martha_greet:
    if martha_affection >= 50:
        ma "Oh good, it's you. I was getting bored being the smartest person in the room."
    elif martha_affection >= 25:
        ma "You clean up better than I expected. Impress me, or at least don't bore me."
    else:
        ma "So the new blood has ambitions. We'll see if they survive this place."
    return

label elle_greet:
    if elle_affection >= 50:
        el "Hey, stranger! Wednesday's better already. Sit, the water's perfect."
    elif elle_affection >= 25:
        el "Oh - hi! Didn't think I'd see you out here again. Good surprise."
    else:
        el "Hi there. You look a little lost for a beach. First time?"
    return
