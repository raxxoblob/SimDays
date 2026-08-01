# Gig work — temporary jobs posted to the phone's "Jobs" app.
# Each day there's a 40% chance a new gig gets posted. A gig stays on the board
# for a per-gig number of days, and each gig can only be worked during its own
# hours window (shown in the listing). You apply; you're accepted only if you
# meet the skill/stat requirement, otherwise they pass. Accepting runs a short
# scene that spends the hours and pays out (money + skill/stat exp). Reuses the
# career requirement checker (meets_req) and the standard gain_*/spend_time.

default gigs_board   = {}     # {gig_id: expiry_day}  — posted gigs and when they drop
default _pending_gig = None   # gig the player just accepted (read by do_gig)

define GIG_POST_CHANCE = 0.40   # daily chance a new gig appears

init python:
    # id, title, blurb, requirement (stat_/skill_/degree like CAREERS),
    # window (open, close hours — close may exceed 24 for late-night),
    # days (how long it stays posted), hours (work duration), pay,
    # optional skill exp / stat gains, energy drain, scene bg, closing line.
    GIG_POOL = [
        {"id": "lifeguard", "title": "Beach Lifeguard (1 day)",
         "blurb": "Cover a sick guard for a day at the shore.",
         "req": {"stat_str": 30}, "window": (9, 17), "days": 1,
         "hours": 6, "pay": 95, "energy": 30, "stat": [("str", 12)], "bg": "beachnight",
         "line": "Six hours, whistle in hand, eyes on the water. Nobody drowns on your watch."},
        {"id": "dev", "title": "Freelance Dev Gig",
         "blurb": "A startup needs a small feature shipped this week.",
         "req": {"skill_prog": 3}, "window": (9, 22), "days": 3,
         "hours": 5, "pay": 180, "energy": 18, "exp": [("prog", 12)], "bg": "hub_night",
         "line": "You knock out the feature, push it, and invoice. Clean work, good money."},
        {"id": "guitar", "title": "Fill-in Bar Gig",
         "blurb": "A bar's act cancelled — they need a musician tonight.",
         "req": {"skill_music": 2}, "window": (20, 27), "days": 1,
         "hours": 3, "pay": 70, "energy": 12, "exp": [("music", 10)], "stat": [("chr", 6)], "bg": "bar",
         "line": "Three sets, a few requests, a couple of tips in the jar. Not bad for a fill-in."},
        {"id": "catering", "title": "Catering Shift",
         "blurb": "An event caterer is short-staffed for the next couple of evenings.",
         "req": {"skill_cook": 2}, "window": (15, 22), "days": 2,
         "hours": 4, "pay": 80, "energy": 22, "exp": [("cook", 10)], "bg": "restaurantnight",
         "line": "Plated two hundred covers without a single one coming back. The chef nods once — high praise."},
        {"id": "promo", "title": "Promo / Modelling Gig",
         "blurb": "A brand wants a presentable face at the mall this week.",
         "req": {"stat_app": 45}, "window": (10, 18), "days": 3,
         "hours": 3, "pay": 110, "energy": 14, "stat": [("app", 8), ("chr", 6)], "bg": "mallday",
         "line": "Smile, hand out samples, look the part. Easiest money you'll make all week."},
        {"id": "moving", "title": "Moving-Day Help",
         "blurb": "Cash job hauling boxes — no experience needed, just muscle.",
         "req": {"stat_str": 20}, "window": (9, 18), "days": 2,
         "hours": 3, "pay": 55, "energy": 25, "stat": [("str", 9)], "bg": "warehouse",
         "line": "Stairs, boxes, more stairs. Your back files a complaint, your wallet doesn't care."},
    ]
    GIG_BY_ID = {g["id"]: g for g in GIG_POOL}

    def roll_gigs():
        """Drop expired gigs, then (40%) post one new gig that isn't already up."""
        store.gigs_board = {gid: exp for gid, exp in store.gigs_board.items()
                            if exp >= store.day and gid in GIG_BY_ID}
        if renpy.random.random() < GIG_POST_CHANCE:
            candidates = [g["id"] for g in GIG_POOL if g["id"] not in store.gigs_board]
            if candidates:
                gid = renpy.random.choice(candidates)
                # stays visible today through today+days-1
                store.gigs_board[gid] = store.day + GIG_BY_ID[gid].get("days", 1) - 1

    def gig_open(g):
        """Is it currently within this gig's hours window?"""
        o, c = g["window"]
        return o <= store.hour < c

    def gig_window_text(g):
        o, c = g["window"]
        return "%02d:00-%02d:00" % (o % 24, c % 24)

    def gig_days_left_text(gid):
        left = store.gigs_board.get(gid, store.day) - store.day + 1
        return "Last day" if left <= 1 else ("%d days left" % left)

    def gig_req_text(req):
        """Readable requirement, e.g. 'Programming Lv3' / 'STR 30'."""
        parts = []
        for k, v in req.items():
            if k.startswith("stat_"):
                parts.append("%s %d" % (k[5:].upper(), v))
            elif k.startswith("skill_"):
                nm = PRO_SKILLS.get(k[6:], (k[6:].title(),))[0]
                parts.append("%s Lv%d" % (nm, v))
            elif k == "degree":
                parts.append(v.replace("_", " ").title())
        return ", ".join(parts)


# ── Phone "Jobs" app: the gig board ───────────────────────────────────────
screen phone_jobs_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 8
            null height 8
            text "Gig Work" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
            null height 2
            $ _gigs = [GIG_BY_ID[g] for g in gigs_board if g in GIG_BY_ID]
            viewport:
                xfill True
                ysize 560
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 10
                    xfill True
                    if not _gigs:
                        null height 8
                        text "Nothing posted right now. New gigs turn up now and then — check back." font ACT_FONT size 13 color "#7a8aa0"
                    for _g in _gigs:
                        $ _ok   = meets_req(_g["req"])
                        $ _open = gig_open(_g)
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 24, 24, 24, 24)
                            padding (14, 10, 14, 10)
                            vbox:
                                spacing 4
                                text _g["title"] font PROFILE_FONT size 15 color "#cfe0f5"
                                text _g["blurb"] font ACT_FONT size 12 color "#8fa4bc"
                                hbox:
                                    spacing 12
                                    text ("%s" % gig_window_text(_g)) font ACT_FONT size 13 color ("#8fb0d0" if _open else "#e8a24d")
                                    text ("%dh work" % _g["hours"]) font ACT_FONT size 13 color "#8fb0d0"
                                    text ("+$%d" % _g["pay"]) font ACT_FONT size 13 color "#ffd66a"
                                hbox:
                                    spacing 12
                                    text ("Needs: " + gig_req_text(_g["req"])) font ACT_FONT size 12 color ("#7fd06a" if _ok else "#e8a24d")
                                    text gig_days_left_text(_g["id"]) font ACT_FONT size 12 color "#6a8098"
                                textbutton ("Apply" if (_ok and _open) else ("Not now" if not _open else "Apply (long shot)")):
                                    xalign 1.0
                                    text_font ACT_FONT text_size 15 text_color "#cfe0f5" text_hover_color "#ffffff"
                                    action ([SetVariable("_pending_gig", _g["id"]), Hide("phone_jobs_scr"), Hide("phone_home"), Function(renpy.jump, "do_gig")]
                                            if (_ok and _open) else
                                            Function(renpy.notify,
                                                     ("This one only runs %s — come back then." % gig_window_text(_g)) if not _open
                                                     else ("You apply — they pass. They want: %s." % gig_req_text(_g["req"]))))
            null height 4
            textbutton "Back" action [Hide("phone_jobs_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Working a gig ─────────────────────────────────────────────────────────
label do_gig:
    if _pending_gig not in GIG_BY_ID:
        jump map
    $ _g      = GIG_BY_ID[_pending_gig]
    $ _pending_gig = None
    $ _gt     = _g["title"]
    $ _g_line = _g["line"]
    scene expression _g["bg"]
    show screen hud
    "You take the gig — [_gt]."
    $ spend_time(_g["hours"])
    python:
        gain_money(_g["pay"])
        for _sk, _amt in _g.get("exp", []):
            gain_skill(_sk, _amt)
        for _st, _amt in _g.get("stat", []):
            gain_stat(_st, _amt)
        if _g.get("energy"):
            store.need_energy = max(0, store.need_energy - _g["energy"])
        # consume it so it can't be re-worked
        store.gigs_board = {gid: exp for gid, exp in store.gigs_board.items() if gid != _g["id"]}
    "[_g_line]"
    jump map
