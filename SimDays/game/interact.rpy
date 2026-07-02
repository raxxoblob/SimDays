# Unified NPC interaction hub. Enter a location, "Talk to <someone>" you know ->
# their sprite moves CENTRE, a relationship panel shows on the RIGHT, and the
# action choices (talk topics + future hug/date + leave) sit along the BOTTOM.
# The location's activity menu is gone while you talk - you converse freely.
#
# To add a character: give them an entry in NPC_DATA + greet/topic labels.

init python:
    def rel_tier(aff):
        if aff >= 75: return "Close"
        if aff >= 50: return "Good friends"
        if aff >= 25: return "Friends"
        if aff >= 1:  return "Acquaintance"
        return "Stranger"

    # This is the scheduler. Human-readable version: ../../../character_schedule.md
    # (keep the two in sync).
    # topics: (caption, label, condition callable or None)
    # sched: list of (weekday-set or None, (h_start, h_end)) - when they're present.
    # gate:  callable or None - a progression lock (e.g. must be a Resident to chat).
    # Weekdays: Mon=0 ... Sun=6.
    MON_FRI = {0, 1, 2, 3, 4}
    MON_SAT = {0, 1, 2, 3, 4, 5}
    NPC_DATA = {
        "nora": {
            "name": "Nora", "sprite": "nora_cafe_normal",
            "aff": "nora_affection", "trust": "nora_trust", "greet": "nora_greet",
            "world": True, "sched": [(None, (8, 18))],
            "topics": [
                ("Small talk",  "nora_t_small", None),
                ("Her plans",   "nora_t_dream", None),
                ("The cafe",    "nora_t_cafe",  None),
            ],
        },
        "marcus": {
            "name": "Marcus", "sprite": "marcus_casual_normal",
            "aff": "marcus_affection", "trust": "marcus_trust", "greet": "marcus_greet",
            "world": True, "sched": [(None, (6, 11)), (None, (17, 27))],
            "topics": [
                ("How's the bar?", "marcus_t_bar",  None),
                ("Just hang out",  "marcus_t_hang", None),
                ("You good?",      "marcus_t_deep", (lambda: store.marcus_trust >= 30)),
            ],
        },
        "caroline": {
            "name": "Caroline", "sprite": "caroline_normal",
            "aff": "caroline_affection", "trust": "caroline_trust", "greet": "caroline_greet",
            # Career NPC: invisible until introduced (met via corporate work).
            "met": "caroline_met", "sched": [(MON_FRI, (9, 18))],
            "topics": [
                ("Office gossip", "caroline_t_gossip", None),
                ("Small talk",    "caroline_t_small",  None),
                ("Ask a favor",   "caroline_t_favor",  (lambda: store.caroline_trust >= 30)),
            ],
        },
        "lena": {
            "name": "Dr. Lena", "sprite": "drlena_normal",
            "aff": "lena_affection", "trust": "lena_trust", "greet": "lena_greet",
            # Career NPC: met once you make Resident. Then shift hours apply.
            "met": "lena_met", "sched": [(None, (8, 20))],
            "topics": [
                ("How's the ward?", "lena_t_ward",   None),
                ("Ask for advice",  "lena_t_advice", None),
                ("You okay?",       "lena_t_deep",   (lambda: store.lena_trust >= 30)),
            ],
        },
        "natalie": {
            "name": "Natalie", "sprite": "natalie_normal",
            "aff": "natalie_affection", "trust": "natalie_trust", "greet": "natalie_greet",
            # Career NPC: met once you've worked a warehouse shift.
            "met": "natalie_met", "sched": [(MON_SAT, (7, 15))],
            "topics": [
                ("Talk shop", "natalie_t_shop", None),
                ("Just chat", "natalie_t_chat", None),
            ],
        },
        "elle": {
            "name": "Elle", "sprite": "elle_sundress_normal",
            "aff": "elle_affection", "trust": "elle_trust", "greet": "elle_greet",
            # World NPC (beach regular) - Wednesday afternoons only, met by showing up.
            "world": True, "sched": [({2}, (16, 19))],
            "topics": [
                ("Small talk", "elle_t_small", None),
                ("The beach",  "elle_t_beach", None),
            ],
        },
    }

    def npc_aff(npc_id):   return getattr(store, NPC_DATA[npc_id]["aff"])
    def npc_trust(npc_id): return getattr(store, NPC_DATA[npc_id]["trust"])

    def npc_here(npc_id):
        """Is this NPC physically present right now (their schedule window)?"""
        sched = NPC_DATA[npc_id].get("sched")
        if not sched:
            return True
        wd = store.day % 7
        for days, (h0, h1) in sched:
            if (days is None or wd in days) and h0 <= store.hour < h1:
                return True
        return False

    def npc_known(npc_id):
        """Do we know them? World characters: always. Career characters: only
        once introduced (their met flag set through the career)."""
        d = NPC_DATA[npc_id]
        if d.get("world"):
            return True
        mv = d.get("met")
        return bool(getattr(store, mv)) if mv else True

    def npc_talkable(npc_id):
        """Show a 'Talk to X' option? Must be present AND known."""
        return npc_here(npc_id) and npc_known(npc_id)


# ── Relationship panel (right side, under the topbar) ──────────────────
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
            text "[_tier]" font PROFILE_FONT size 17 color "#9fb6d6"
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


# ── Action bar (bottom) - talk topics + future actions + leave ─────────
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
            for cap, lbl, cond in NPC_DATA[npc_id]["topics"]:
                if cond is None or cond():
                    button:
                        action Return(lbl)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                        padding (22, 12, 22, 12)
                        text cap font ACT_FONT size 20 color "#cfe0f5" hover_color "#ffffff"

            # future actions (locked for now)
            button:
                sensitive False
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                padding (22, 12, 22, 12)
                text "Hug (soon)" font ACT_FONT size 20 color "#6b82a6"
            button:
                sensitive False
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                padding (22, 12, 22, 12)
                text "Invite out (soon)" font ACT_FONT size 20 color "#6b82a6"

            button:
                action Return("leave")
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                padding (22, 12, 22, 12)
                text "Leave" font ACT_FONT size 20 color "#cfe0f5" hover_color "#ffffff"


# ── Driver: centre the sprite, show stats, loop topics until you leave ──
label npc_interact(npc_id):
    $ _spr = NPC_DATA[npc_id]["sprite"]
    show expression _spr as npcsprite at sprite_c
    show screen npc_relbar(npc_id)
    call expression NPC_DATA[npc_id]["greet"]
    while True:
        $ _act = renpy.call_screen("npc_actions", npc_id)
        if _act == "leave":
            break
        call expression _act
    hide screen npc_relbar
    hide npcsprite
    return


# ══ Nora ═══════════════════════════════════════════════════════════════
label nora_greet:
    if nora_affection >= 50:
        n "Hey, you. I was hoping you'd come in today."
    elif nora_affection >= 25:
        n "There you are. The usual?"
    else:
        n "Back already? Coffee's that good, or...?"
    return

label nora_t_small:
    $ spend_time(0.5)
    $ nora_affection += 2
    n "Settling in okay? First city's always a lot."
    menu:
        "\"Still figuring it out.\"":
            n "Aren't we all. You'll find your feet. Or your favorite bar. Whichever's first."
            $ nora_trust += 1
        "\"Getting there.\"":
            n "That's the spirit. Fake it till the rent's paid."
    return

label nora_t_dream:
    $ spend_time(0.5)
    if nora_affection >= 40:
        n "Between us? This isn't the endgame. I'm saving for night classes. Nursing, if I don't lose my nerve."
        menu:
            "\"You'd be great at it.\"":
                n "...Yeah? That means more than you'd think. Most people just nod."
                $ nora_affection += 4
                $ nora_trust += 2
            "\"Why nursing?\"":
                n "I like being the person who actually helps when it all goes sideways."
                $ nora_affection += 2
                $ nora_trust += 1
    else:
        n "Big plans? Ha. Ask me again once you've bought more than one coffee."
        $ nora_affection += 1
    return

label nora_t_cafe:
    $ spend_time(0.5)
    $ nora_affection += 1
    n "See the guy in the corner? Same order for three years. I respect the commitment, I just don't get it."
    return


# ══ Marcus ═════════════════════════════════════════════════════════════
label marcus_greet:
    if marcus_affection >= 50:
        m "Was just about to text you. What's up, man?"
    elif marcus_affection >= 25:
        m "There he is. Grab a seat."
    else:
        m "Hey, neighbor. Surviving?"
    return

label marcus_t_bar:
    $ spend_time(0.5)
    $ marcus_affection += 1
    m "Static? Busy. Loud. Tips are decent if you can fake liking the music."
    if marcus_affection >= 40:
        m "I keep thinking... I could run a place better than this. Smaller. Mine."
    return

label marcus_t_hang:
    $ spend_time(0.5)
    $ marcus_affection += 2
    m "We should ball sometime. Park, Saturday. You'll lose, but you'll have fun."
    return

label marcus_t_deep:
    $ spend_time(0.5)
    $ marcus_trust += 2
    m "Honestly? Money's tight, the owner's a pain. But I'm figuring it out. Thanks for asking."
    return


# ══ Caroline (Nexus Tower - HR, knows everything) ══════════════════════
label caroline_greet:
    if caroline_affection >= 50:
        caro "There's my favorite source of interesting problems. Sit."
    elif caroline_affection >= 25:
        caro "Look who it is. Don't worry, whatever you did, I already know."
    else:
        caro "HR. If you're not on fire, make it quick - if you are, still make it quick."
    return

label caroline_t_gossip:
    $ spend_time(0.5)
    $ caroline_affection += 2
    caro "Bradley's on his third coffee and second bad decision. Analyst pool's a warzone. You didn't hear it from me."
    return

label caroline_t_small:
    $ spend_time(0.5)
    $ caroline_affection += 1
    caro "People think HR is paperwork. It's psychology with a stapler."
    return

label caroline_t_favor:
    $ spend_time(0.5)
    $ caroline_trust += 2
    caro "A favor. Interesting. I keep a ledger - favors in, favors out. You're... in credit. Barely. What do you need?"
    return


# ══ Dr. Lena (City Hospital) ═══════════════════════════════════════════
label lena_greet:
    if lena_affection >= 50:
        lena "Oh good, a face that isn't a chart. Two minutes, they're all yours."
    elif lena_affection >= 25:
        lena "Hey. Still standing? Good. Half my morning wasn't."
    else:
        lena "If you're not bleeding, you're in the wrong line - but hi."
    return

label lena_t_ward:
    $ spend_time(0.5)
    $ lena_affection += 2
    lena "Understaffed, over-caffeinated, running on adrenaline and vending-machine crackers. So, normal."
    return

label lena_t_advice:
    $ spend_time(0.5)
    $ lena_affection += 1
    if skill_med >= 3:
        lena "You've got the basics down. Trick now is staying calm when everyone else isn't."
    else:
        lena "Want in on medicine? Hit the books first. The college runs courses - come back when you know an artery from an anecdote."
    return

label lena_t_deep:
    $ spend_time(0.5)
    $ lena_trust += 2
    lena "Honestly? I love the work and it's eating me alive. Both true. Thanks for asking - most people don't."
    return


# ══ Natalie (LogiCity Warehouse - manager) ═════════════════════════════
label natalie_greet:
    if natalie_affection >= 50:
        nat "There's my reliable one. Don't let it go to your head."
    elif natalie_affection >= 25:
        nat "You again. Fine. You work harder than half the floor, so - what."
    else:
        nat "You lost? Break room's that way. Clock's on the wall."
    return

label natalie_t_shop:
    $ spend_time(0.5)
    $ natalie_affection += 2
    nat "Rule one: lift with your legs. Rule two: don't make me say rule one twice. You'll be fine."
    return

label natalie_t_chat:
    $ spend_time(0.5)
    $ natalie_affection += 1
    nat "Twelve years on this floor. Started stacking, now I run it. Nobody handed me anything. Respect that, we'll get along."
    return


# ══ Elle (beach - Wednesday afternoons) ════════════════════════════════
label elle_greet:
    if elle_affection >= 50:
        el "Hey, stranger! Wednesday's better already. Sit, the water's perfect."
    elif elle_affection >= 25:
        el "Oh - hi! Didn't think I'd see you out here again. Good surprise."
    else:
        el "Hi there. You look a little lost for a beach. First time?"
    return

label elle_t_small:
    $ spend_time(0.5)
    $ elle_affection += 2
    el "I basically live out here on my days off. Sun, water, nobody emailing me. Bliss."
    return

label elle_t_beach:
    $ spend_time(0.5)
    $ elle_affection += 1
    el "Best spot's past the pier - fewer people, better light around five. That's my little secret. Was."
    return
