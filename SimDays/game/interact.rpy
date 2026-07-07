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
    WKD     = {5, 6}
    FRISUN  = {4, 5, 6}
    NPC_DATA = {
        "nora": {
            "name": "Nora", "portrait": "portrait_nora", "sprite": "nora_cafe_normal", "say": "n",
            "aff": "nora_affection", "trust": "nora_trust", "greet": "nora_greet",
            "world": True,
            "sched": [
                (MON_FRI, (7,  16), "location_cafe"),
                ({1, 4},  (17, 22), "location_bar"),
                (WKD,     (10, 14), "location_cafe"),
            ],
            "likes": ["food", "ambition", "movies"], "dislikes": ["nightlife"],
        },
        "marcus": {
            "name": "Marcus", "portrait": "portrait_marcus", "sprite": "marcus_casual_normal", "say": "m",
            "aff": "marcus_affection", "trust": "marcus_trust", "greet": "marcus_greet",
            "world": True, "sched": [
                (None, (6,  10), "location_park"),
                (None, (17, 24), "location_bar"),
                (WKD,  (23, 27), "location_nightclub"),
            ],
            "likes": ["sports", "food", "nightlife"], "dislikes": ["art"],
        },
        "caroline": {
            "name": "Caroline", "portrait": "portrait_caroline", "sprite": "caroline_normal", "say": "caro",
            "aff": "caroline_affection", "trust": "caroline_trust", "greet": "caroline_greet",
            "met": "caroline_met", "sched": [(MON_FRI, (9, 18), "location_office")],
            "likes": ["work", "ambition", "nightlife"], "dislikes": ["sports"],
        },
        "lena": {
            "name": "Dr. Lena", "portrait": "portrait_lena", "sprite": "drlena_normal", "say": "lena",
            "aff": "lena_affection", "trust": "lena_trust", "greet": "lena_greet",
            "met": "lena_met", "sched": [
                (MON_FRI, (8,  16), "location_hospital"),
                ({2, 4},  (18, 22), "location_bar"),
            ],
            "likes": ["work", "travel", "food"], "dislikes": ["nightlife"],
        },
        "natalie": {
            "name": "Natalie", "portrait": "portrait_natalie", "sprite": "natalie_normal", "say": "nat",
            "aff": "natalie_affection", "trust": "natalie_trust", "greet": "natalie_greet",
            "met": "natalie_met", "sched": [
                (MON_SAT, (7,  15), "location_warehouse"),
                (WKD,     (17, 21), "location_bar"),
            ],
            "likes": ["sports", "work", "ambition"], "dislikes": ["art"],
        },
        "martha": {
            "name": "Martha", "portrait": "portrait_martha", "sprite": "martha_neutral", "say": "ma",
            "aff": "martha_affection", "trust": "martha_trust", "greet": "martha_greet",
            "met": "martha_met", "story_gate": "caroline_met", "sched": [
                (MON_FRI, (9,  18), "location_office"),
                ({3},     (19, 23), "location_bar"),
            ],
            "likes": ["ambition", "work", "travel"], "dislikes": ["sports"],
        },
        "elle": {
            "name": "Elle", "portrait": "portrait_elle", "sprite": "elle_sundress_normal", "say": "el",
            "aff": "elle_affection", "trust": "elle_trust", "greet": "elle_greet",
            "world": True, "sched": [
                ({1, 3}, (9,  13), "location_cafe"),
                ({2},    (16, 19), "location_beach"),
                (WKD,    (13, 18), "location_beach"),
                (WKD,    (21, 25), "location_nightclub"),
            ],
            "likes": ["travel", "music", "art"], "dislikes": ["work"],
        },
        "zoe": {
            "name": "Zoe", "portrait": "portrait_zoe", "sprite": "zoe_punk_smile", "say": "z",
            "aff": "zoe_affection", "trust": "zoe_trust", "greet": "zoe_greet",
            "world": True, "sched": [
                (WKD,    (12, 18), "location_beach"),
                ({3, 4}, (14, 18), "location_park"),
                (FRISUN, (21, 27), "location_nightclub"),
            ],
            "likes": ["art", "music", "nightlife"], "dislikes": ["ambition"],
        },
        "sam": {
            "name": "Sam", "portrait": "portrait_sam", "sprite": "sam_normal", "say": "sam",
            "aff": "sam_affection", "trust": "sam_trust", "greet": "sam_greet",
            "world": True, "sched": [
                (MON_FRI, (6,  10), "location_park"),
                (MON_FRI, (10, 14), "location_gym"),
                (WKD,     (9,  13), "location_gym"),
            ],
            "likes": ["sports", "work", "food"], "dislikes": ["nightlife"],
        },
        "eli": {
            "name": "Eli", "portrait": "portrait_eli", "sprite": "eli_normal", "say": "eli",
            "aff": "eli_affection", "trust": "eli_trust", "greet": "eli_greet",
            "world": True, "sched": [
                (None,      (12, 20), "location_library"),
                ({1, 2, 3}, (20, 23), "location_bar"),
            ],
            "likes": ["work", "movies", "music"], "dislikes": ["sports"],
        },
        "kai": {
            "name": "Kai", "portrait": "portrait_kai", "sprite": "kai_normal", "say": "kai",
            "aff": "kai_affection", "trust": "kai_trust", "greet": "kai_greet",
            "world": True, "sched": [
                ({1, 3}, (10, 14), "location_cafe"),
                (WKD,    (10, 14), "location_gym"),
                (WKD,    (14, 18), "location_beach"),
                (WKD,    (18, 22), "location_bar"),
                (FRISUN, (22, 27), "location_nightclub"),
            ],
            "likes": ["sports", "music", "nightlife"], "dislikes": ["work"],
        },
    }

    def npc_aff(npc_id):   return getattr(store, NPC_DATA[npc_id]["aff"])
    def npc_trust(npc_id): return getattr(store, NPC_DATA[npc_id]["trust"])

    def npc_here(npc_id):
        sched = NPC_DATA[npc_id].get("sched")
        if not sched:
            return True
        wd = store.day % 7
        for entry in sched:
            days = entry[0]
            h0, h1 = entry[1]
            loc = entry[2] if len(entry) > 2 else None
            if not (days is None or wd in days):
                continue
            if not (h0 <= store.hour < h1):
                continue
            if loc is None or store.current_loc == loc:
                return True
        return False

    def npc_known(npc_id):
        d = NPC_DATA[npc_id]
        gate = d.get("story_gate")
        if gate and not getattr(store, gate, False):
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
    # fired when the same topic has been used 3+ days in a row
    BURNOUT_LINES = [
        "Alex, how much can we talk about %s? Can we please change the subject?",
        "...%s again. I need you to surprise me here.",
        "We've covered %s like ten times now. Let's try something else.",
    ]

    def topic_used_today(npc_id, topic):
        return topic in store._topics_today.get(npc_id, [])

    def _apply_aff(npc_id, delta):
        av = NPC_DATA[npc_id]["aff"]
        setattr(store, av, max(0, min(getattr(store, av) + delta, 100)))

    def npc_is_angry(npc_id):
        """True when NPC won't engage with intimate actions: hygiene too low or accumulated anger."""
        return store.need_hygiene < 30 or store.npc_anger.get(npc_id, 0) > 0

    def check_jealousy(active_npc_id):
        """NPCs with aff >= 60 at the same location react when player gets intimate.
        Only called on date/hug/invite actions, not on greeting."""
        jealous_names = []
        for nid, d in NPC_DATA.items():
            if nid == active_npc_id:
                continue
            aff = getattr(store, d["aff"], 0)
            if aff >= 60 and npc_here(nid):
                _apply_aff(nid, -5)
                _a = dict(store.npc_anger)
                _a[nid] = min(10, _a.get(nid, 0) + 3)
                store.npc_anger = _a
                jealous_names.append(d["name"])
        return jealous_names

    def location_sprites():
        """All talkable NPCs at the current location, as (npc_id, sprite) pairs.
        Uses sprite_angry key if angry and available, else normal sprite."""
        result = []
        for nid, d in NPC_DATA.items():
            if npc_talkable(nid):
                if npc_is_angry(nid) and d.get("sprite_angry"):
                    result.append((nid, d["sprite_angry"]))
                else:
                    result.append((nid, d["sprite"]))
        return result

    # Pre-existing NPC-to-NPC relationships.
    NPC_RELATIONS = {
        ("marcus", "sam"):  {"type": "gym_friends"},
        ("nora",   "kai"):  {"type": "regulars"},
        ("zoe",    "elle"): {"type": "friends"},
    }

    def group_scene_check():
        """Returns (npc_a, npc_b) whenever two related NPCs are both talkable here."""
        for (a, b) in NPC_RELATIONS:
            if npc_talkable(a) and npc_talkable(b):
                return (a, b)
        return None

    def group_scene_label(gs):
        """'Name & Name' string for menu display."""
        return NPC_DATA[gs[0]]["name"] + " & " + NPC_DATA[gs[1]]["name"]

    # ── Group conversation helper ────────────────────────────────────────
    # Like do_talk but no time spend (caller handles it) and smaller gains
    # (split attention in a group).
    GROUP_REACT_TEXT = {
        "like":    "{name} lights up.",
        "dislike": "{name} doesn't bite.",
        "neutral": "{name} listens, nods.",
    }

    def _do_talk_group(npc_id, topic):
        import renpy.random as _r
        d = NPC_DATA[npc_id]
        if topic in d.get("likes", []):
            delta, rtype = _r.randint(5, 10), "like"
        elif topic in d.get("dislikes", []):
            delta, rtype = _r.randint(-4, -1), "dislike"
        else:
            delta, rtype = _r.randint(2, 5), "neutral"
        _apply_aff(npc_id, delta)
        _td = dict(store._topics_today)
        _td.setdefault(npc_id, [])
        _td[npc_id] = _td[npc_id] + [topic]
        store._topics_today = _td
        return rtype

    def do_talk(npc_id, topic):
        d = NPC_DATA[npc_id]
        spend_time(0.5)
        # resolve reaction
        if topic in d.get("likes", []):
            result, delta, pool = "like", 2, LIKE_LINES
        elif topic in d.get("dislikes", []):
            result, delta, pool = "dislike", -1, DISLIKE_LINES
        else:
            result, delta, pool = "neutral", 0, NEUTRAL_LINES
        # record discovery (permanent knowledge about this NPC)
        seen = dict(store._topics_seen.get(npc_id, {}))
        seen[topic] = result
        store._topics_seen[npc_id] = seen
        # social battery: 3+ days in a row on same topic → burnout, no gain
        streak = store._topic_streak.get(npc_id, {}).get(topic, 0)
        if streak >= 3:
            delta, pool = 0, BURNOUT_LINES
        # mark topic as used today
        today = list(store._topics_today.get(npc_id, []))
        if topic not in today:
            today.append(topic)
        store._topics_today[npc_id] = today
        _apply_aff(npc_id, delta)
        gain_aff(d["name"], delta)
        line = renpy.random.choice(pool) % TOPIC_LABEL[topic]
        renpy.say(getattr(store, d["say"]), line)

    # First-contact rebuffs (world characters only, before they know you).
    COLD_REBUFF = [
        "%s glances at you, then pointedly looks away. Not today.",
        "%s pretends not to hear you and drifts off.",
        "%s gives you a quick once-over and keeps walking.",
        "You start to say something - %s is already somewhere else. \"...\"",
    ]

    def cold_approach_ok(npc_id):
        """World strangers may brush you off on first contact. Higher Charisma +
        status = better odds. Once you've broken the ice (affection > 0), never again."""
        d = NPC_DATA[npc_id]
        if not d.get("world") or npc_aff(npc_id) > 0:
            return True
        chance = 45 + store.stat_chr * 2 + status_score() // 3
        if renpy.random.randint(1, 100) <= chance:
            _apply_aff(npc_id, 2)   # broke the ice
            return True
        return False

    GIFT_TYPES = {
        "book":    ("Book",    20, ["movies", "work", "ambition", "art"]),
        "sweets":  ("Sweets",  15, ["food", "nightlife"]),
        "gadget":  ("Gadget",  35, ["music", "movies", "work"]),
        "flowers": ("Flowers", 25, ["travel", "art", "nightlife"]),
    }
    GIFT_LIKE_LINES = {
        "book":    ["A book? Let me guess - you actually paid attention.", "Oh, this one's been on my list. How did you know?"],
        "sweets":  ["Don't tell me you remembered what I said about these.", "Okay, now I feel bad I didn't bring anything for you."],
        "gadget":  ["Okay, this is genuinely useful. Thank you.", "You didn't have to, but I'm very glad you did."],
        "flowers": ["These are beautiful. Seriously.", "You know exactly what you're doing, don't you?"],
    }
    GIFT_DISLIKE_LINES = {
        "book":    ["Oh, a book. That's... thoughtful.", "I'll find a shelf for it. Thanks."],
        "sweets":  ["Sweets? I'm not really a sugar person, but... thanks.", "I'll pass them on. Thank you though."],
        "gadget":  ["I don't really use these, but thanks for thinking of me.", "It's very... technical. I appreciate it."],
        "flowers": ["Flowers. That's sweet of you.", "They're lovely, really. Thank you."],
    }
    GIFT_NEUTRAL_LINES = {
        "book":    ["Oh, nice - thank you.", "That's a thoughtful thing to bring."],
        "sweets":  ["You didn't have to. These are great, thanks.", "Oh, a treat. Perfect timing."],
        "gadget":  ["This is cool, actually. Thanks.", "I wasn't expecting this. Thank you."],
        "flowers": ["These are lovely, thank you.", "That's really kind of you."],
    }

    def do_gift(npc_id, gift_type):
        if store.gifts.get(gift_type, 0) <= 0:
            return
        store.gifts[gift_type] -= 1
        d = NPC_DATA[npc_id]
        interests = GIFT_TYPES[gift_type][2]
        likes     = d.get("likes", [])
        dislikes  = d.get("dislikes", [])
        if any(i in likes for i in interests):
            delta = 5
            line = renpy.random.choice(GIFT_LIKE_LINES[gift_type])
        elif any(i in dislikes for i in interests):
            delta = 1
            line = renpy.random.choice(GIFT_DISLIKE_LINES[gift_type])
        else:
            delta = 3
            line = renpy.random.choice(GIFT_NEUTRAL_LINES[gift_type])
        _apply_aff(npc_id, delta)
        gain_aff(d["name"], delta)
        renpy.say(getattr(store, d["say"]), line)


# ── Relationship panel (right, under the topbar) ───────────────────────
# _rb_prev_* are set to -1 by npc_interact on entry so the first render never
# flashes; a gain flips the fill to a bright colour for FLASH_LEN seconds.
define FLASH_LEN = 0.9
default _rb_prev_aff = -1
default _topics_seen    = {}   # {npc_id: {topic: "like"|"dislike"|"neutral"}}
default _topics_today   = {}   # {npc_id: [topics]} — cleared in new_day()
default _topic_streak   = {}   # {npc_id: {topic: consecutive_days}}
default npc_last_seen   = {}   # {npc_id: day} — updated on every npc_interact entry
default _rb_prev_tr = -1
default _rb_flash_aff = 0.0
default _rb_flash_tr = 0.0

screen npc_relbar(npc_id):
    zorder 25
    $ _aff = npc_aff(npc_id)
    $ _tr = npc_trust(npc_id)
    $ _tier = rel_tier(_aff)
    $ _nm = NPC_DATA[npc_id]["name"]

    # arm a colour flash whenever a value climbs since the last render
    if _rb_prev_aff >= 0 and _aff > _rb_prev_aff:
        $ _rb_flash_aff = _time.time()
    if _rb_prev_tr >= 0 and _tr > _rb_prev_tr:
        $ _rb_flash_tr = _time.time()
    $ _rb_prev_aff = _aff
    $ _rb_prev_tr = _tr
    $ _aff_hot = (_time.time() - _rb_flash_aff) < FLASH_LEN
    $ _tr_hot = (_time.time() - _rb_flash_tr) < FLASH_LEN
    # keep re-rendering so the flash window can close on its own
    # ponytail: always-on 15fps tick; fine for the single relbar shown in-chat
    timer 0.06 repeat True action NullAction()

    $ _portrait_path = "images/ui/icons/%s.png" % NPC_DATA[npc_id].get("portrait", "")
    $ _has_portrait  = bool(NPC_DATA[npc_id].get("portrait")) and renpy.loadable(_portrait_path)

    frame:
        xpos 1260
        ypos 150
        xsize 400
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 20)
        vbox:
            spacing 10
            # portrait + name row
            hbox:
                spacing 16
                if _has_portrait:
                    add _portrait_path xysize (90, 90)
                vbox:
                    spacing 4
                    yalign 0.5
                    text "[_nm]" font PROFILE_FONT size 28 color "#ffffff"
                    text "[_tier]" font PROFILE_FONT size 15 color "#9fb6d6"
            null height 4
            fixed:
                xsize 356
                ysize 30
                text "Affection" font PROFILE_FONT size 17 color "#cfe0f5" xpos 0 ypos 4
                bar:
                    xpos 110 ypos 7
                    value AnimatedValue(_aff, 100, delay=FLASH_LEN)
                    xsize 150 ysize 16
                    left_bar ("#ffd76a" if _aff_hot else Frame("images/ui/bar_fill_chr.png", 14, 0)) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_aff]" font PROFILE_FONT size 17 color ("#ffd76a" if _aff_hot else "#ffffff") xpos 270 ypos 4
            fixed:
                xsize 356
                ysize 30
                text "Trust" font PROFILE_FONT size 17 color "#cfe0f5" xpos 0 ypos 4
                bar:
                    xpos 110 ypos 7
                    value AnimatedValue(_tr, 100, delay=FLASH_LEN)
                    xsize 150 ysize 16
                    left_bar ("#7fe0ff" if _tr_hot else Frame("images/ui/bar_fill_int.png", 14, 0)) right_bar Frame("images/ui/bar_track.png", 14, 0) thumb Null()
                text "[_tr]" font PROFILE_FONT size 17 color ("#7fe0ff" if _tr_hot else "#ffffff") xpos 270 ypos 4


# ── Main action bar (bottom) — icon tiles ──────────────────────────────
screen npc_actions(npc_id):
    zorder 22
    $ _gift_ok   = sum(gifts.values()) > 0
    $ _date_ok   = npc_aff(npc_id) >= 30
    $ _hug_ok    = npc_aff(npc_id) >= 15
    $ _num_ok    = npc_aff(npc_id) >= 25 and npc_id not in npc_contacts
    $ _angry     = npc_is_angry(npc_id)
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (18, 14, 18, 14)
        vbox:
            spacing 4
            if _angry:
                $ _angry_hint = "You need a shower first." if need_hygiene < 30 else (NPC_DATA[npc_id]["name"] + " is upset with you.")
                text "[_angry_hint]" font ACT_FONT size 13 color "#e86a55" xalign 0.5
            hbox:
                spacing 16
                for _icon, _lbl, _ret, _ok in [
                        ("act_talk",   "Talk",                    "talk",   True),
                        ("act_gift",   "Gift (%d)" % sum(gifts.values()),  "gift",   _gift_ok),
                        ("act_hug",    "Hug",                     "hug",    _hug_ok and not _angry),
                        ("act_invite", "Invite",                  "date",   _date_ok and not _angry),
                        ("act_phone",  "Get #",                   "number", _num_ok and not _angry),
                        ("act_leave",  "Leave",                   "leave",  True)]:
                    button:
                        sensitive _ok
                        action Return(_ret)
                        background None
                        hover_background None
                        vbox:
                            spacing 4
                            add Transform("images/ui/icons/%s.png" % _icon, size=(72, 72), alpha=(1.0 if _ok else 0.35)) xalign 0.5
                            text _lbl font ACT_FONT size 15 xalign 0.5 color ("#cfe0f5" if _ok else "#4a6080") hover_color "#ffffff"


# ── Gift type picker ──────────────────────────────────────────────────
screen npc_gift_select():
    zorder 22
    frame:
        xalign 0.5
        yalign 0.5
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 18)
        vbox:
            spacing 12
            text "Choose a gift:" font ACT_FONT size 20 color "#9fb6d6" xalign 0.5
            for _gkey, (_gname, _gcost, _gints) in GIFT_TYPES.items():
                $ _ghave = gifts.get(_gkey, 0)
                button:
                    xsize 280
                    sensitive _ghave > 0
                    background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                    hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                    action Return(_gkey)
                    text "[_gname]  (x[_ghave])" font ACT_FONT size 17 color ("#cfe0f5" if _ghave > 0 else "#4a6080") hover_color "#ffffff" xalign 0.5
            textbutton "Cancel" action Return("back") xalign 0.5 text_font ACT_FONT text_size 15 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Topic picker — 3×3 icon grid ───────────────────────────────────────
screen npc_topics(npc_id):
    zorder 22
    $ _likes    = NPC_DATA[npc_id].get("likes", [])
    $ _dislikes = NPC_DATA[npc_id].get("dislikes", [])
    frame:
        xpos 960
        xanchor 0.5
        yalign 1.0
        yoffset -26
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (22, 18, 22, 18)
        vbox:
            spacing 14
            hbox:
                xsize 464
                text "Talk about..." font ACT_FONT size 20 color "#9fb6d6" xalign 0.0 yalign 0.5
                textbutton "Back" action Return("back") xalign 1.0 text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"
            vpgrid:
                cols 3
                spacing 10
                for key, label in TOPICS:
                    $ _tint  = ("#ffd76a" if key in _likes else ("#6b82a6" if key in _dislikes else "#cfe0f5"))
                    $ _used  = topic_used_today(npc_id, key)
                    $ _badge = _topics_seen.get(npc_id, {}).get(key)
                    button:
                        xysize (148, 120)
                        sensitive not _used
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        action Return(key)
                        vbox:
                            spacing 6
                            xalign 0.5 yalign 0.5
                            fixed:
                                xysize (60, 60)
                                xalign 0.5
                                add Transform("images/ui/icons/topic_%s.png" % key, size=(60, 60), alpha=(0.35 if _used else 1.0))
                                if _badge == "like":
                                    text "+" xpos 42 ypos 0 size 18 color "#39c07a" font ACT_FONT
                                elif _badge == "dislike":
                                    text "−" xpos 42 ypos 0 size 18 color "#e86a55" font ACT_FONT
                            text label font ACT_FONT size 15 color ("#445060" if _used else _tint) hover_color "#ffffff" xalign 0.5


# ── Driver ─────────────────────────────────────────────────────────────
label npc_interact(npc_id):
    $ renpy.hide_screen("npc_relbar")
    $ renpy.hide("npcsprite")
    $ renpy.hide("npcsprite2")
    $ _rb_prev_aff = -1   # -1 = don't flash on the opening render
    $ _rb_prev_tr = -1
    # update last-seen day for this NPC (feeds ignore-decay in new_day)
    $ store.npc_last_seen[npc_id] = day
    $ _spr = NPC_DATA[npc_id]["sprite"]
    show expression _spr as npcsprite at sprite_c
    show screen npc_relbar(npc_id)
    $ _nm = NPC_DATA[npc_id]["name"]
    # cold approach: a stranger might brush you off
    if not cold_approach_ok(npc_id):
        $ _rb = renpy.random.choice(COLD_REBUFF) % _nm
        "[_rb]"
        hide screen npc_relbar
        hide npcsprite
        hide npcsprite2
        return
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
            $ _g = renpy.call_screen("npc_gift_select")
            if _g != "back":
                $ do_gift(npc_id, _g)
        elif _act == "hug":
            $ _jealous = check_jealousy(npc_id)
            if _jealous:
                $ _jn = " and ".join(_jealous)
                "[_jn] clocks the embrace. Their expression flickers."
            $ _apply_aff(npc_id, 3)
            $ spend_time(0.1)
            "[_nm] smiles and leans in. A brief, warm hug."
        elif _act == "number":
            $ store.npc_contacts = store.npc_contacts + [npc_id]
            $ _apply_aff(npc_id, 2)
            "[_nm] smiles. \"Sure, here you go.\" Number saved."
        elif _act == "date":
            $ _jealous = check_jealousy(npc_id)
            if _jealous:
                $ _jn = " and ".join(_jealous)
                "[_jn] catches your attention drift toward [_nm]. Something shifts in their expression."
            call npc_date(npc_id)
            $ _act = "leave"   # a date is the whole evening
    hide screen npc_relbar
    hide npcsprite
    hide npcsprite2
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
    hide npcsprite2
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

label zoe_greet:
    if zoe_affection >= 50:
        z "Hey, you. Pull up some grass. I'm avoiding a canvas that's avoiding me."
    elif zoe_affection >= 25:
        z "Oh, it's you. Good - I needed an excuse to stop pretending to sketch."
    else:
        z "You're blocking my light. ...Kidding. Mostly. I'm Zoe."
    return

label sam_greet:
    if sam_affection >= 50:
        sam "Hey! Perfect timing, I need a break before my legs stage a mutiny."
    elif sam_affection >= 25:
        sam "Oh hey, it's you! Still can't keep up, but I respect the effort."
    else:
        sam "Morning! You run, or just admiring people who do? I'm Sam."
    return

label eli_greet:
    if eli_affection >= 50:
        eli "Oh good, a friendly face. Save me from this thesis for five minutes?"
    elif eli_affection >= 25:
        eli "Hey. Sorry - deep in it. But a break's probably healthy. Allegedly."
    else:
        eli "Uh, hi. I'm Eli. Don't mind the mess, this is just... my whole personality."
    return

label kai_greet:
    if kai_affection >= 50:
        kai "Yo! Was just thinking about you. Good timing as always."
    elif kai_affection >= 25:
        kai "Hey! You're back. This beach has a way of pulling people in, right?"
    else:
        kai "Sup. You look like someone who doesn't come here enough."
    return
