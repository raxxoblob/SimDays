# Activity chooser - floating left-side list of rounded 'glass' bars.
# No panel background: just the bars themselves (narrower, lighter, nicer type).
# Used by location action menus via `menu (screen="activity"):`.
# Dialogue menus keep the default centred `choice` screen.

define ACT_FONT = "fonts/Quicksand-SemiBold.ttf"   # swap weight here globally

init python:
    from functools import lru_cache as _lru_cache

    @_lru_cache(maxsize=128)
    def _split_caption(cap):
        # strip trailing [[...]] lock annotation, then split at first (
        if "[[" in cap:
            cap = cap[:cap.index("[[")].rstrip()
        idx = cap.find("(")
        if idx > 0:
            return cap[:idx].rstrip(), cap[idx:]
        return cap, ""

    # ── Activity effects (hover tooltip) ──────────────────────────────────────
    # There is no in-engine effect list — each activity's effects are inline in its
    # menu branch — so this table mirrors them. Keyed by (current_loc, name) where
    # name is the caption before the "(...)". Each effect is (text, category);
    # category picks the colour. Values are the BASE case (event/supplement bonuses
    # still apply in-game but aren't spelled out). Unlisted activities show no panel.
    ACT_FX_COLOR = {
        "gain": "#7fd06a",   # stat/skill/need gains
        "cost": "#e8704d",   # money out
        "need": "#e8a24d",   # need drain (energy/hunger/hygiene down)
        "time": "#8fb0d0",   # time spent
        "info": "#b6c8dc",   # neutral note
        "earn": "#ffd66a",   # money in
    }
    ACTIVITY_EFFECTS = {
        # ── Grounds / café ───────────────────────────────────────────────
        ("location_cafe", "Buy a coffee"):           [("0.5h", "time"), ("-$3", "cost"), ("+10 Energy", "gain")],
        ("location_cafe", "Work a shift - Barista"): [("4h", "time"), ("+$55-65", "earn"), ("-28 Energy", "need"), ("-12 Hunger", "need")],
        # ── Gym ──────────────────────────────────────────────────────────
        # ponytail: energy is -28 in code; the old caption said -15 (fixed in locations.rpy)
        ("location_gym", "Train - weights"):      [("1.5h", "time"), ("-28 Energy", "need"), ("+STR +XP", "gain"), ("+8 APP", "gain")],
        ("location_gym", "Cardio"):               [("1h",   "time"), ("-12 Energy", "need"), ("+STR +XP", "gain"), ("+4 APP", "gain")],
        ("location_gym", "Week pass"):            [("-$40",  "cost"), ("7-day access", "info")],
        ("location_gym", "Month pass"):           [("-$120", "cost"), ("30-day access", "info")],
        ("location_gym", "Day rate"):             [("-$8",   "cost"), ("1-day access", "info")],
        ("location_gym", "Buy Protein Shake"):    [("-$12",  "cost"), ("+50% STR XP next weights", "info")],
        ("location_gym", "Buy Pre-workout"):      [("-$20",  "cost"), ("+100% STR XP next weights", "info")],
        ("location_gym", "Work a shift"):         [("8h",   "time"), ("+pay", "earn"), ("-Energy", "need")],
        # ── Park ─────────────────────────────────────────────────────────
        ("location_park", "Jog"):             [("1h",   "time"), ("-12 Energy", "need"), ("+STR +XP", "gain")],
        ("location_park", "Read a book"):     [("1.5h", "time"), ("-8 Energy",  "need"), ("+INT +XP", "gain")],
        ("location_park", "Play basketball"): [("1.5h", "time"), ("-20 Energy", "need"), ("+STR +XP", "gain")],
        # ── Beach ────────────────────────────────────────────────────────
        ("location_sandbeach", "Swim"):    [("1h",   "time"), ("-20 Energy", "need"), ("-10 Hunger", "need"), ("+STR +XP", "gain")],
        ("location_sandbeach", "Sunbathe"):[("1.5h", "time"), ("-10 Hunger", "need"), ("+8 APP",    "gain")],
        ("location_sandbeach", "Relax"):   [("1h",   "time"), ("-8 Hunger",  "need")],
        # ── Bar ──────────────────────────────────────────────────────────
        ("location_bar", "Have a drink"): [("0.5h", "time"), ("-$ drink",   "cost")],
        ("location_bar", "Socialize"):    [("1h",   "time"), ("-10 Energy", "need"), ("+CHR +XP", "gain"), ("CHR 25 req", "info")],
        # ── Nightclub ────────────────────────────────────────────────────
        ("location_nightclub", "Hit the dance floor"):    [("1h",   "time"), ("-10 Energy", "need")],
        ("location_nightclub", "Work the crowd"):         [("1h",   "time"), ("-12 Energy", "need"), ("+CHR +XP", "gain"), ("CHR 30 req", "info")],
        ("location_nightclub", "Buy a round"):            [("0.5h", "time"), ("-$15",       "cost"), ("+CHR +XP", "gain")],
        ("location_nightclub", "DJ night - dance floor"): [("1h",   "time"), ("-15 Energy", "need"), ("+8 CHR",   "gain"), ("Fri-Sun", "info")],
        ("location_nightclub", "VIP section"):            [("0.5h", "time"), ("-$50",       "cost"), ("+15 CHR",  "gain"), ("Fri-Sun", "info")],
        # ── Flea Market ──────────────────────────────────────────────────
        ("location_flea_market", "Browse stalls"):       [("1h",   "time"), ("-6 Energy", "need"), ("+6 CHR",  "gain")],
        ("location_flea_market", "Buy a vintage piece"): [("0.5h", "time"), ("-$25",      "cost")],
        ("location_flea_market", "Buy a book"):          [("0.5h", "time"), ("-$12",      "cost"), ("+2 INT",  "gain")],
        ("location_flea_market", "Haggle with vendors"): [("1h",   "time"), ("-8 Energy", "need"), ("+6 CHR",  "gain")],
        # ── Riverside Terrace ────────────────────────────────────────────
        ("location_terrace", "Sit and watch the water"): [("1h",   "time"), ("-6 Hunger", "need"), ("+5 Energy",  "gain")],
        ("location_terrace", "Socialize"):                [("1h",   "time"), ("+6 CHR",    "gain")],
        ("location_terrace", "Have a coffee"):            [("0.5h", "time"), ("-$4",       "cost"), ("+12 Energy", "gain")],
        ("location_terrace", "Read"):                     [("1h",   "time"), ("-10 Energy","need"), ("+4 INT",     "gain")],
        # ── Anchor bar ───────────────────────────────────────────────────
        ("location_anchor", "Have a drink"): [("0.5h", "time"), ("-$6",  "cost"), ("+5 CHR",  "gain")],
        ("location_anchor", "Stay a while"): [("1h",   "time"), ("-7 Energy", "need"), ("+8 CHR",  "gain")],
        ("location_anchor", "Buy a round"):  [("0.5h", "time"), ("-$18", "cost"), ("+18 CHR", "gain")],
        # ── Diner ────────────────────────────────────────────────────────
        ("location_diner", "Order coffee"):    [("0.5h", "time"), ("-$3", "cost"), ("+8 Energy",  "gain")],
        ("location_diner", "Order a meal"):    [("1h",   "time"), ("-$8", "cost"), ("+40 Hunger", "gain")],
        ("location_diner", "Sit for a while"): [("1h",   "time"), ("+5 Energy", "gain")],
        # ── Casino ───────────────────────────────────────────────────────
        ("location_casino", "Casino Bar — have a drink"): [("0.5h",       "time"), ("-$8",              "cost")],
        ("location_casino", "Look Around"):                [("0.5h",       "time"), ("Atmosphere",       "info")],
        ("location_casino", "Blackjack Table"):            [("0.25h/hand", "time"), ("Variable winnings","info")],
        ("location_casino", "Roulette Table"):             [("0.25h/spin", "time"), ("Variable winnings","info")],
        # ── Home ─────────────────────────────────────────────────────────
        ("location_home", "Shower"):              [("0.5h",  "time"), ("+40 Hygiene", "gain")],
        ("location_home", "Nap"):                 [("3h",    "time"), ("+45 Energy",  "gain")],
        ("location_home", "Practice guitar"):     [("2h",    "time"), ("-~15 Energy", "need"), ("+Music +XP",  "gain")],
        ("location_home", "Home workout"):        [("1h",    "time"), ("-25 Energy",  "need"), ("+12 STR",     "gain")],
        ("location_home", "Make coffee"):         [("0.5h",  "time"), ("+7-12 Energy","gain")],
        ("location_home", "Put a record on"):     [("0.5h",  "time"), ("Inspired state","gain")],
        ("location_home", "Change guitar strings"):[("-$12", "cost"), ("+4% busking 7d","gain")],
        ("location_home", "Look around your place"):[("Free","info"), ("Room overview",  "info")],
        ("location_home", "Sleep"):               [("→ next morning","time"), ("Energy fully restored","gain")],
        ("location_home", "Until morning"):       [("8h",   "time"), ("New day, full rest","gain")],
        ("location_home", "6 hours"):             [("6h",   "time"), ("+~60 Energy",  "gain")],
        ("location_home", "4 hours"):             [("4h",   "time"), ("+~40 Energy",  "gain")],
        ("location_home", "2 hours"):             [("2h",   "time"), ("+~20 Energy",  "gain")],
        ("location_home", "Cook something"):      [("Meals restore Hunger","info"), ("+Cook XP with recipes","gain")],
        ("location_home", "Toast"):               [("0.25h","time"), ("-$2",  "cost"), ("+15 Hunger","gain")],
        ("location_home", "Instant noodles"):     [("0.25h","time"), ("-$3",  "cost"), ("+22 Hunger","gain")],
        ("location_home", "Scrambled eggs"):      [("0.5h", "time"), ("-$5",  "cost"), ("+32 Hunger","gain")],
        ("location_home", "Pasta bolognese"):     [("0.5h", "time"), ("-$8",  "cost"), ("+55 Hunger","gain"), ("+Cook XP","gain")],
        ("location_home", "Chicken stir-fry"):   [("0.75h","time"), ("-$10", "cost"), ("+65 Hunger","gain"), ("+8 Energy","gain")],
        ("location_home", "Sunday roast"):        [("1h",   "time"), ("-$18", "cost"), ("+80 Hunger","gain"), ("+15 Energy","gain")],
        # ── Library ──────────────────────────────────────────────────────
        ("location_library", "Study — general"):    [("2h", "time"), ("-15 Energy","need"), ("+20 INT","gain")],
        ("location_library", "Self-study a subject"):[("2h","time"), ("-18 Energy","need"), ("+skill +XP","gain")],
        # ── College ──────────────────────────────────────────────────────
        # ponytail: cost shown as "-$varies" because course_cost() is dynamic (tier + sale event)
        ("location_college", "Programming"): [("3h", "time"), ("-22 Energy","need"), ("+Prog +XP","gain"), ("-$varies","cost")],
        ("location_college", "Medicine"):    [("3h", "time"), ("-22 Energy","need"), ("+Med +XP", "gain"), ("-$varies","cost")],
        ("location_college", "Business"):    [("3h", "time"), ("-22 Energy","need"), ("+Biz +XP", "gain"), ("-$varies","cost")],
        ("location_college", "Art"):         [("3h", "time"), ("-22 Energy","need"), ("+Art +XP", "gain"), ("-$varies","cost")],
        # ── Warehouse ────────────────────────────────────────────────────
        ("location_warehouse", "Work a shift"): [("8h","time"), ("+$115-170","earn"), ("-40 Energy","need"), ("+STR +XP","gain")],
        # ── Hospital ─────────────────────────────────────────────────────
        ("location_hospital", "Cosmetic treatment"): [("2h","time"), ("-$350","cost"), ("+2 APP","gain"), ("+10 temp APP 7d","gain")],
    }

    def activity_fx(caption):
        """Effect list for an activity caption at the current location, or None."""
        name = _split_caption(caption)[0]
        return ACTIVITY_EFFECTS.get((store.current_loc, name))

    def activity_fx_inline(caption):
        """(time_text, [(text, category), ...]) for the button face itself.

        The time entry is pulled out so it can be left-anchored; the next two
        effects in table order are the headline ones. ponytail: "most important"
        is just source order in ACTIVITY_EFFECTS — the tables are already written
        headline-first. Upgrade path is a per-entry priority key if that stops
        holding. Falls back to the caption's own "(...)" when untabled."""
        fx = activity_fx(caption)
        if not fx:
            return (_split_caption(caption)[1], [])
        t = next((x for x, c in fx if c == "time"), "")
        rest = [(x, c) for x, c in fx if c != "time"]
        return (t, rest[:2])

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
        xsize 442
        ymaximum 660
        mousewheel True
        scrollbars ("vertical" if len(items) > 7 else None)
        vbox:
            spacing 12
            for i in items:
                if i.action is not None:
                    $ _nm, _cs = _split_caption(i.caption)
                    $ _t, _fx2 = activity_fx_inline(i.caption)
                    $ _tw = 78 if _fx2 else 386   # untabled: _t is the raw "(...)" caption tail
                    button:
                        action i.action
                        # Debt no longer disables the whole bar — try_spend gates per
                        # category (essentials like food/study/gym stay affordable;
                        # luxuries block themselves). See gains.rpy _DEBT_OK_CATEGORIES.
                        sensitive getattr(i, 'sensitive', True)
                        xysize (420, 84)
                        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                        insensitive_background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                        tooltip i.caption
                        at act_item
                        vbox:
                            yalign 0.5
                            xpos 22
                            xsize 386
                            spacing 3
                            text _nm:
                                font ACT_FONT size 20 color "#cfe0f5" hover_color "#ffffff" insensitive_color "#4e606e" xsize 386 yalign 0.5 line_leading 0
                            # Headline effects on the face of the bar — no hover needed.
                            hbox:
                                spacing 16
                                if _t:
                                    text _t:
                                        font ACT_FONT size 15 color ACT_FX_COLOR["time"] insensitive_color "#3a4a56" xsize _tw yalign 0.5 line_leading 0
                                for _fx_txt, _fx_cat in _fx2:
                                    text _fx_txt:
                                        font ACT_FONT size 15 bold True yalign 0.5 line_leading 0
                                        color ACT_FX_COLOR.get(_fx_cat, "#cfe0f5")
                                        insensitive_color "#3a4a56"

    # Effects card — floats next to the hovered activity bar (nearrect), listing
    # what the activity gives with colour-coded deltas.
    $ _tt = GetTooltip()
    if _tt:
        $ _fx = activity_fx(_tt)
        # Two headline effects are already on the bar; the card is only worth
        # showing when there is more than that to say.
        if _fx and len(_fx) > 3:
            nearrect:
                focus "tooltip"
                prefer_top False   # show BELOW the bar so the top items clear the people dock
                frame:
                    background "#12161ef2"
                    padding (16, 12, 18, 12)
                    xmaximum 320
                    vbox:
                        spacing 6
                        text _split_caption(_tt)[0] font ACT_FONT size 14 color "#8fa4bc"
                        null height 1
                        for _fx_txt, _fx_cat in _fx:
                            hbox:
                                spacing 8
                                frame:
                                    background ACT_FX_COLOR.get(_fx_cat, "#cfe0f5")
                                    xysize (4, 22)
                                text _fx_txt:
                                    font ACT_FONT size 18 bold True yalign 0.5
                                    color ACT_FX_COLOR.get(_fx_cat, "#cfe0f5")

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -16
        background "#000000aa"
        padding (24, 14, 24, 14)
        vbox:
            xsize 150
            spacing 4
            $ _exit_icon = "apartment_ext" if activity_exit_name == "Hallway" else "hub"  # ponytail: hub is a placeholder; a proper icon_city_map.png is needed
            imagebutton:
                xalign 0.5
                idle  Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(120, 120))
                hover Transform("images/ui/icons/icon_%s.png" % _exit_icon, size=(132, 132))
                action [Hide("people_here_dock"), Jump(activity_exit_jump)]
            text "[activity_exit_name]" xalign 0.5 size 16 color "#ffffff"


screen people_here_dock(return_location):
    zorder 11
    if (current_loc in ("location_cafe", "location_park", "location_bar", "location_sandbeach",
                        "location_library", "location_hospital", "location_gym", "location_nightclub",
                        "location_office", "location_warehouse", "location_diner", "location_college",
                        "location_casino")
            and not renpy.get_screen("profile")
            and not renpy.get_screen("phone_home")
            and not renpy.get_screen("npc_relbar")
            and _hud2_expanded is None):   # HUD V2 left panel occupies this spot
        $ _dock_npcs = [n for n in public_talkable_npcs_here() if NPC_DATA[n].get("portrait")]
        $ _dock_vis  = _dock_npcs[:4]
        $ _dock_extra = len(_dock_npcs) - 4
        if _dock_vis:
            frame:
                xpos 44
                ypos 164
                background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                padding (10, 8, 10, 8)
                hbox:
                    spacing 8
                    for npc_id in _dock_vis:
                        $ _enc = npc_has_been_encountered(npc_id)
                        $ _disp = NPC_DATA[npc_id]["name"] if _enc else "Stranger"
                        button:
                            xysize (108, 128)
                            background None
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 30, 30, 30, 30)
                            action [SetVariable("_dock_npc", npc_id), SetVariable("_dock_return", return_location), Jump("npc_interact_from_dock")]
                            vbox:
                                spacing 4
                                xalign 0.5
                                # portrait always visible — strangers are named "Stranger"
                                # below but still show their face icon
                                add portrait_circle(npc_id, 100) xalign 0.5
                                text _disp:
                                    size 10 font ACT_FONT color "#b0c4d8" hover_color "#e0ecff"
                                    xalign 0.5
                    if _dock_extra > 0:
                        vbox:
                            yalign 0.5
                            text ("+%d" % _dock_extra):
                                size 13 font ACT_FONT color "#6a8098"
                                align (0.5, 0.5)
