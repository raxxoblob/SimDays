# Computer OS shell — a desktop presentation layer over EXISTING systems.
# Zero new game state: mail, freelance, marketplace, calendar, portfolio and
# CityNet all read/write the same stores the phone uses.
# Single-window manager: computer_active_app names the one open app, or None.

init python:
    from collections import OrderedDict

    # ── App registry ─────────────────────────────────────────────────────────
    # "unlock"  : store variable name, or None = always visible
    # "icon"    : path to 64×64 PNG in images/ui/pc_ui/
    # "pinned"  : True = show as quick-launch button in taskbar
    # "stub"    : if set, app shows placeholder text instead of a full screen
    _PC = "images/ui/pc_ui/"

    # ── Shared desktop typography ────────────────────────────────────────────
    # One place for every app's text size/colour. Ren'Py text properties can't
    # be inherited through `use`/transclude, so apps reference these constants
    # instead of each defining its own sizes.
    # ponytail: constants, not a style family — screens here use inline `text`
    # statements everywhere; converting them all to styled text is a bigger
    # refactor than this pass needs. Upgrade path: define `style pc_body_text`
    # et al. and drop the explicit font/size/color properties.
    PC_TITLE_SIZE = 21   # window + section titles
    PC_TEXT_SIZE  = 17   # normal content
    PC_SMALL_SIZE = 15   # secondary content
    PC_FG         = "#e8eef4"   # primary (near-white)
    PC_FG_DIM     = "#8ea4bc"   # secondary floor — do not go darker
    COMPUTER_APPS = OrderedDict([
        ("mail",        {"name": "Mail",        "icon": _PC+"01_mail.png",             "screen": "capp_mail",        "unlock": None,            "pinned": True}),
        ("freelance",   {"name": "Freelance",   "icon": _PC+"02_freelance_projects.png","screen": "capp_freelance",  "unlock": "own_computer",  "pinned": True}),
        ("calendar",    {"name": "Calendar",    "icon": _PC+"03_calendar.png",          "screen": "capp_calendar",   "unlock": None,            "pinned": True}),
        ("marketplace", {"name": "Marketplace", "icon": _PC+"04_marketplace.png",       "screen": "capp_marketplace","unlock": None,            "pinned": True}),
        ("portfolio",   {"name": "Portfolio",   "icon": _PC+"05_portfolio.png",         "screen": "capp_portfolio",  "unlock": None,            "pinned": True}),
        ("social",      {"name": "Social",      "icon": _PC+"06_social.png",            "screen": "capp_browser",    "unlock": None,            "pinned": True}),
        ("music",       {"name": "Music",       "icon": _PC+"07_music.png",             "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "Music library and streaming — coming soon."}),
        # Phase 69: the "Files" slot was a stub. It now hosts the Possessions
        # app — same screen body as the phone version, no duplicated logic.
        ("files",       {"name": "Collection",  "icon": _PC+"08_files.png",             "screen": "capp_possessions","unlock": None,            "pinned": False}),
        ("browser",     {"name": "Browser",     "icon": _PC+"09_browser.png",           "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "No internet connection detected."}),
        ("programming", {"name": "Programming", "icon": _PC+"10_programming.png",       "screen": "capp_programming","unlock": None,            "pinned": True}),
        ("finances",    {"name": "Finances",    "icon": _PC+"11_finances.png",          "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "Budget tracker — coming soon."}),
        ("contacts",    {"name": "Contacts",    "icon": _PC+"12_contacts.png",          "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "Contact list — coming soon."}),
        # The dead "Settings" stub now hosts Home Upgrades — reuses the gear icon
        # rather than adding a 17th asset.
        ("upgrades",    {"name": "Home Upgrades","icon": _PC+"13_settings.png",         "screen": "capp_upgrades",   "unlock": None,            "pinned": True}),
        ("photos",      {"name": "Photos",      "icon": _PC+"14_photos.png",            "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "No photos saved yet."}),
        ("notes",       {"name": "Notes",       "icon": _PC+"15_notes.png",             "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "Notepad — coming soon."}),
        ("trash",       {"name": "Trash",       "icon": _PC+"16_trash.png",             "screen": "capp_stub",       "unlock": None,            "pinned": False,
                         "stub": "Trash is empty."}),
    ])

    def computer_app_visible(app_id):
        unlock = COMPUTER_APPS[app_id]["unlock"]
        return True if unlock is None else bool(getattr(store, unlock, False))

    def computer_visible_apps():
        return [(k, v) for k, v in COMPUTER_APPS.items() if computer_app_visible(k)]

    def computer_pinned_apps():
        return [(k, v) for k, v in COMPUTER_APPS.items()
                if computer_app_visible(k) and v.get("pinned")]

    # ── Badges (all derived live from existing state) ─────────────────────────
    def computer_badge_count(app_id):
        if app_id == "mail":
            return unread_mail_count()
        if app_id == "freelance":
            # No per-offer "seen" flag exists; the board rotates as a batch, so
            # the batch refresh day is the unread signal.
            if store.freelance_active_project is None and \
               store.freelance_last_refresh_day != store._capp_freelance_seen_day:
                return len(store.freelance_offers)
            return 0
        if app_id == "marketplace":
            return 1 if store.market_listings_period != store._capp_market_seen_period else 0
        if app_id == "calendar":
            return _calendar_badge_count()
        return 0

    # ── Window management ────────────────────────────────────────────────────
    def computer_open_app(app_id):
        store.computer_active_app = app_id
        # Opening an app clears its "new since last visit" badge.
        if app_id == "marketplace":
            store._capp_market_seen_period = store.market_listings_period
        elif app_id == "freelance":
            store._capp_freelance_seen_day = store.freelance_last_refresh_day
        elif app_id == "mail":
            store._active_mail_tag = None
        renpy.restart_interaction()
        return None

    def computer_close_app():
        store.computer_active_app = None
        store._active_mail_tag = None
        renpy.restart_interaction()
        return None

    # ── Equipment visual tier (0-3) ──────────────────────────────────────────
    def computer_visual_tier():
        """Thin wrapper over the Phase 62 slot system + legacy EQUIPMENT_DEFS."""
        iid = p62_primary_item_for("computer")
        if iid and iid in ITEM_CATALOG:
            return max(0, min(3, ITEM_CATALOG[iid]["visual_tier"] - 1))
        legacy = equipped_item("computer")
        if legacy and legacy in EQUIPMENT_DEFS:
            return max(0, min(3, EQUIPMENT_DEFS[legacy]["tier"] - 1))
        return 0

    # tier -> (desktop bg, window bg, titlebar, taskbar, accent)
    COMPUTER_THEMES = {
        0: ("#1b1d20", "#24272b", "#2e3237", "#16181a", "#8a9298"),
        1: ("#1d1a15", "#282420", "#332e27", "#171410", "#c9a06a"),
        2: ("#0e1218", "#171d26", "#1f2833", "#0a0e13", "#5bcafa"),
        3: ("#0a1420", "#111f2c", "#17303f", "#060d14", "#7fe0c0"),
    }

    def computer_theme(idx):
        return COMPUTER_THEMES[computer_visual_tier()][idx]

    def computer_boot_flavor():
        """One-shot per computer session. Returns a string or ''."""
        t = computer_visual_tier()
        if t == 0:
            return "The fan starts whirring."
        if t == 3:
            return "Dual monitor setup. Everything fits on screen at once."
        return ""

    def _capp_loc_name(loc_id):
        return (loc_id or "").replace("location_", "").replace("_", " ").title()


# ══════════════════════════════════════════════════════════════════════════════
# DESKTOP
# ══════════════════════════════════════════════════════════════════════════════

screen computer_desktop():
    modal True
    zorder 150

    add Transform("images/ui/pc_ui/pc_wallpaper.png", size=(config.screen_width, config.screen_height))
    # Tint overlay so window chrome stays readable on any wallpaper
    add Solid("#00000055")

    if computer_active_app is None:
        use computer_icon_grid
    else:
        use expression COMPUTER_APPS[computer_active_app]["screen"] pass ()

    use computer_taskbar


screen computer_icon_grid():
    $ _apps = computer_visible_apps()
    vpgrid:
        cols 4
        xpos 80
        ypos 80
        xysize (1760, 900)
        xspacing 20
        yspacing 16
        draggable False
        mousewheel True
        scrollbars None

        for _aid, _app in _apps:
            $ _badge = computer_badge_count(_aid)
            $ _is_stub = _app.get("stub") is not None
            button:
                xysize (200, 150)
                action Function(computer_open_app, _aid)
                background None
                hover_background Frame("images/ui/act_bar_hover_clean.png", 18, 18, 18, 18)
                vbox:
                    align (0.5, 0.5)
                    spacing 10
                    frame:
                        xysize (72, 72)
                        xalign 0.5
                        background None
                        padding (0, 0, 0, 0)
                        add _app["icon"] fit "contain" xysize (72, 72) xalign 0.5 yalign 0.5
                    text _app["name"] xalign 0.5 font ACT_FONT size PC_TEXT_SIZE color (PC_FG if not _is_stub else PC_FG_DIM)
                    if _badge > 0:
                        text ("● %d" % _badge) xalign 0.5 font ACT_FONT size PC_SMALL_SIZE color "#ff5555"
                    else:
                        null height 20


screen computer_taskbar():
    frame:
        yalign 1.0
        xfill True
        ysize 56
        background Solid(computer_theme(3))
        padding (10, 0, 10, 0)

        # Left: current context
        text (COMPUTER_APPS[computer_active_app]["name"] if computer_active_app else "Desktop"):
            xalign 0.0
            yalign 0.5
            xsize 150
            font PROFILE_FONT
            size PC_TEXT_SIZE
            color computer_theme(4)

        # Centre: pinned app launcher buttons (only the real apps, not every icon)
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 4
            for _aid, _app in computer_pinned_apps():
                $ _b = computer_badge_count(_aid)
                button:
                    xysize (52, 52)
                    action Function(computer_open_app, _aid)
                    background (Solid(computer_theme(2)) if computer_active_app == _aid else None)
                    hover_background Frame("images/ui/act_bar_hover_clean.png", 12, 12, 12, 12)
                    vbox:
                        align (0.5, 0.5)
                        spacing 2
                        add _app["icon"] fit "contain" xysize (28, 28) xalign 0.5
                        if _b > 0:
                            text "●" font ACT_FONT size PC_SMALL_SIZE color "#ff5555" xalign 0.5
                        else:
                            null height 19

        # Right: clock, money, exit
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 18
            text ("%s  ·  Day %d" % (time_label(hour), day + 1)) font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM yalign 0.5
            text ("$%d" % money) font ACT_FONT size PC_TEXT_SIZE color "#ffd66a" yalign 0.5
            textbutton "Leave":
                action Return("leave")
                text_font ACT_FONT
                text_size PC_TEXT_SIZE
                text_color "#9fb6d6"
                text_hover_color "#ffffff"
                background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                xpadding 14
                ypadding 6


# ══════════════════════════════════════════════════════════════════════════════
# APP WINDOW SHELL
# ══════════════════════════════════════════════════════════════════════════════

screen computer_app_shell(title):
    $ _shell_icon = COMPUTER_APPS.get(computer_active_app, {}).get("icon", None)
    frame:
        xysize (1560, 850)
        xalign 0.5
        ypos 40
        background Solid(computer_theme(1))
        padding (0, 0, 0, 0)
        vbox:
            spacing 0
            # Title bar
            frame:
                xfill True
                ysize 50
                background Solid(computer_theme(2))
                padding (14, 0, 10, 0)
                hbox:
                    yalign 0.5
                    spacing 10
                    if _shell_icon:
                        add _shell_icon fit "contain" xysize (22, 22) yalign 0.5
                    text title yalign 0.5 font PROFILE_FONT size PC_TITLE_SIZE color "#ffffff"
                # Window controls (right-aligned)
                hbox:
                    xalign 1.0
                    yalign 0.5
                    spacing 2
                    # — Minimise (visual only in V1: just closes back to desktop)
                    textbutton "—":
                        action Function(computer_close_app)
                        text_font PROFILE_FONT
                        text_size PC_TEXT_SIZE
                        text_color "#9fb6d6"
                        text_hover_color "#ffdd88"
                        background None
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 10, 10, 10, 10)
                        xpadding 12
                        ypadding 8
                    textbutton "✕":
                        action Function(computer_close_app)
                        text_font PROFILE_FONT
                        text_size PC_TEXT_SIZE
                        text_color "#9fb6d6"
                        text_hover_color "#ff8888"
                        background None
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 10, 10, 10, 10)
                        xpadding 12
                        ypadding 8
            frame:
                xfill True
                ysize 800
                background None
                padding (24, 18, 24, 18)
                transclude


# ══════════════════════════════════════════════════════════════════════════════
# STUB — placeholder for apps not yet implemented
# ══════════════════════════════════════════════════════════════════════════════

screen capp_stub():
    $ _app_data = COMPUTER_APPS.get(computer_active_app, {})
    $ _stub_msg = _app_data.get("stub", "This app is not available yet.")
    use computer_app_shell(_app_data.get("name", "App")):
        vbox:
            align (0.5, 0.5)
            spacing 16
            if _app_data.get("icon"):
                add _app_data["icon"] fit "contain" xysize (72, 72) xalign 0.5
            text _stub_msg xalign 0.5 font ACT_FONT size PC_TITLE_SIZE color PC_FG_DIM


# ══════════════════════════════════════════════════════════════════════════════
# PROGRAMMING PRACTICE + HOME UPGRADES
# Both used to hang off the legacy `use_computer` menu; they are desktop apps now.
# ══════════════════════════════════════════════════════════════════════════════

label capp_programming_practice_ctx:
    # Runs in its own context so the desktop stays up underneath.
    # ponytail: the XP/energy numbers mirror the legacy use_computer menu entry
    # rather than sharing a helper. Upgrade path: move this block into one
    # do_programming_practice label if a third caller ever appears.
    $ spend_time(3)
    $ _prog_xp_base = 35 if own_programming_kit else 25
    $ _prog_xp_base = int(round(_prog_xp_base * (1.0 + float(equipment_modifier("computer", "prog_xp")))))
    $ gain_skill_practice("prog", _prog_xp_base, 3)
    $ _prog_e = max(1, int(15 * apply_skill_prog_energy_modifier() * (1.0 - home_upgrade_effect("desk_efficiency")) * (1.0 - float(equipment_modifier("computer", "project_energy")))))
    if active_player_state_effect("prog_energy_up") > 0:
        $ _prog_e = int(_prog_e * (1.0 + active_player_state_effect("prog_energy_up")))
    $ need_energy = max(0, need_energy - _prog_e)
    "You work through a few exercises. Good for keeping the fundamentals sharp."
    return


screen capp_programming():
    $ _prog_eff = current_practice_efficiency("prog")
    use computer_app_shell("Programming"):
        vbox:
            spacing 14
            xfill True
            text ("Programming level %d  ·  practice efficiency today %s" % (skill_val("prog"), _prog_eff)):
                font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
            text "Drill exercises in the editor. Three hours, costs energy, keeps the fundamentals sharp.":
                font ACT_FONT size PC_TEXT_SIZE color PC_FG
            if not own_programming_kit:
                text "No dedicated programming kit — you learn a little slower without one.":
                    font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
            null height 6
            textbutton "Practice Programming  ·  3h":
                xalign 0.5
                action Function(renpy.call_in_new_context, "capp_programming_practice_ctx")
                text_font ACT_FONT
                text_size PC_TITLE_SIZE
                text_color computer_theme(4)
                text_hover_color "#ffffff"
                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                xpadding 20
                ypadding 10


label capp_home_upgrades_ctx:
    call screen home_upgrades_scr
    return


screen capp_upgrades():
    use computer_app_shell("Home Upgrades"):
        vbox:
            spacing 14
            xfill True
            $ _hu_owned = [d for u, d in HOME_UPGRADE_DEFS.items() if owns_home_upgrade(u)]
            text ("%d of %d upgrades installed  ·  balance $%d"
                  % (len(_hu_owned), len(HOME_UPGRADE_DEFS), money)):
                font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
            viewport:
                xfill True
                ysize 620
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    if not _hu_owned:
                        text "Nothing installed yet." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                    for _hd in _hu_owned:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (16, 12, 16, 12)
                            vbox:
                                spacing 3
                                text _hd["title"] font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                                text _hd["desc"] font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
            textbutton "Open Upgrade Catalogue  →":
                xalign 0.5
                action Function(renpy.call_in_new_context, "capp_home_upgrades_ctx")
                text_font ACT_FONT
                text_size PC_TITLE_SIZE
                text_color computer_theme(4)
                text_hover_color "#ffffff"
                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                xpadding 20
                ypadding 10


# ══════════════════════════════════════════════════════════════════════════════
# MAIL — reads player_mail / mark_mail_read directly (same state as the phone)
# ══════════════════════════════════════════════════════════════════════════════

screen capp_mail():
    use computer_app_shell("Mail"):
        $ _delivered = [m for m in player_mail if m.get("delivered")]
        hbox:
            spacing 18
            # Inbox list
            vbox:
                xsize 560
                spacing 6
                text ("Inbox  ·  %d unread" % unread_mail_count()) font PROFILE_FONT size PC_TEXT_SIZE color computer_theme(4)
                viewport:
                    xfill True
                    ysize 730
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 6
                        xfill True
                        if not _delivered:
                            text "No mail yet." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        for _m in reversed(_delivered):
                            button:
                                xfill True
                                background (Solid(computer_theme(2)) if _m["tag"] == _active_mail_tag else Frame("images/ui/act_bar_idle.png", 18, 18, 18, 18))
                                hover_background Frame("images/ui/act_bar_hover_clean.png", 18, 18, 18, 18)
                                padding (14, 12, 14, 12)
                                action [Function(mark_mail_read, _m["tag"]), SetVariable("_active_mail_tag", _m["tag"])]
                                vbox:
                                    spacing 2
                                    hbox:
                                        xfill True
                                        text _m["sender"] font PROFILE_FONT size PC_TEXT_SIZE color ("#ffffff" if not _m["read"] else PC_FG_DIM)
                                        if not _m["read"]:
                                            text " ●" font PROFILE_FONT size PC_SMALL_SIZE color "#5bcafa" yalign 0.5
                                    text _m["subject"] font ACT_FONT size PC_TEXT_SIZE color (PC_FG if not _m["read"] else PC_FG_DIM)
            # Reading pane
            vbox:
                xsize 900
                spacing 8
                $ _dm = next((m for m in player_mail if m.get("tag") == _active_mail_tag), None)
                if _dm:
                    text _dm["subject"] font PROFILE_FONT size PC_TITLE_SIZE color "#ffffff"
                    text ("From: %s   ·   Day %d" % (_dm["sender"], _dm.get("delivered_on", 0) + 1)) font ACT_FONT size PC_SMALL_SIZE color computer_theme(4)
                    null height 6
                    viewport:
                        xfill True
                        ysize 700
                        mousewheel True
                        scrollbars "vertical"
                        text _dm["body"] font ACT_FONT size PC_TEXT_SIZE color PC_FG
                else:
                    null height 40
                    text "Select a message to read it." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM


# ══════════════════════════════════════════════════════════════════════════════
# FREELANCE — summary + hand-off to the existing full workspace screen
# ══════════════════════════════════════════════════════════════════════════════

label capp_freelance_ctx:
    # Runs in its own context so the desktop stays up underneath.
    $ _capp_fl_loop = True
    while _capp_fl_loop:
        call screen computer_freelance_scr
        if _return == "close":
            $ _capp_fl_loop = False
        if store._pending_project_result is not None:
            call show_project_result
    return


screen capp_freelance():
    use computer_app_shell("Freelance"):
        vbox:
            spacing 12
            xfill True
            text ("Reputation %d   ·   Completed %d   ·   Failed %d"
                  % (freelance_reputation, freelance_completed, freelance_failed)):
                font ACT_FONT size PC_TEXT_SIZE color computer_theme(4)

            if freelance_active_project is not None:
                $ _p = freelance_active_project
                text "Active Project" font PROFILE_FONT size PC_TITLE_SIZE color "#ffffff"
                frame:
                    xfill True
                    background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                    padding (16, 14, 16, 14)
                    vbox:
                        spacing 6
                        text _p["title"] font PROFILE_FONT size PC_TITLE_SIZE color PC_FG
                        text ("%s  ·  %s  ·  $%d" % (_p["client"], _p["difficulty"].title(), _p["pay"])) font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        $ _frac = min(1.0, float(_p["worked_hours"]) / max(1, _p["required_hours"]))
                        bar value _frac range 1.0 xsize 700 ysize 14
                        text ("%d / %d hours  ·  due Day %d (%d left)"
                              % (_p["worked_hours"], _p["required_hours"], _p["deadline_day"] + 1,
                                 _p["deadline_day"] - day)):
                            font ACT_FONT size PC_SMALL_SIZE color ("#ff8866" if _p["deadline_day"] - day <= 1 else PC_FG_DIM)
            else:
                $ _offers = [t for t in _all_freelance_templates() if t["id"] in freelance_offers]
                text ("Available Projects  (%d)" % len(_offers)) font PROFILE_FONT size PC_TITLE_SIZE color "#ffffff"
                viewport:
                    xfill True
                    ysize 560
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 6
                        xfill True
                        if not _offers:
                            text "No offers on the board right now. Check back after a day or two." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        for _t in _offers:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 18, 18, 18, 18)
                                padding (16, 12, 16, 12)
                                vbox:
                                    spacing 3
                                    text ("%s — %s" % (_t["title"], _t["client"])) font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                                    text ("$%d  ·  %s  ·  %dh over %d days  ·  needs prog %d"
                                          % (_t["pay"], _t["difficulty"].title(), _t["hours"], _t["days"], _t["min_skill"])):
                                        font ACT_FONT size PC_SMALL_SIZE color (PC_FG if freelance_eligible(_t) else PC_FG_DIM)

            null height 4
            textbutton "Open Freelance Workspace  →":
                xalign 0.5
                action Function(renpy.call_in_new_context, "capp_freelance_ctx")
                text_font ACT_FONT
                text_size PC_TITLE_SIZE
                text_color computer_theme(4)
                text_hover_color "#ffffff"
                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16, 16, 16)
                xpadding 20
                ypadding 10
            text "Accept, work and submit projects there. Working costs time and energy.":
                xalign 0.5
                font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM


# ══════════════════════════════════════════════════════════════════════════════
# MARKETPLACE — same listings the phone shows; buying here removes it there
# ══════════════════════════════════════════════════════════════════════════════

screen capp_marketplace():
    use computer_app_shell("Marketplace"):
        $ _all = market_active_listings()
        $ _cats = ["all"] + sorted(set(l["cat"] for l in _all))
        $ _shown = _all if _capp_market_cat == "all" else [l for l in _all if l["cat"] == _capp_market_cat]
        vbox:
            spacing 10
            xfill True
            hbox:
                spacing 6
                for _c in _cats:
                    textbutton (("All" if _c == "all" else MARKET_CATEGORY_LABELS.get(_c, _c.title()))):
                        action SetVariable("_capp_market_cat", _c)
                        text_font ACT_FONT
                        text_size PC_TEXT_SIZE
                        text_color ("#ffffff" if _capp_market_cat == _c else PC_FG_DIM)
                        text_hover_color "#ffffff"
                        background (Solid(computer_theme(2)) if _capp_market_cat == _c else Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14))
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                        xpadding 14
                        ypadding 6
            viewport:
                xfill True
                ysize 700
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    if not _shown:
                        text "Nothing listed in this category." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                    for _l in _shown:
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 18, 18, 18, 18)
                            padding (16, 12, 16, 12)
                            hbox:
                                xfill True
                                spacing 16
                                vbox:
                                    yalign 0.5
                                    spacing 3
                                    hbox:
                                        spacing 10
                                        text _l["name"] font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                                        text MARKET_CATEGORY_LABELS.get(_l["cat"], _l["cat"]) font ACT_FONT size PC_SMALL_SIZE color computer_theme(4) yalign 0.5
                                    text ("%s  ·  seller: %s  ·  listed until Day %d"
                                          % (listing_condition_text(_l), _l["seller"], _l["expire_day"] + 1)):
                                        font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
                                    # ponytail: no equip-delta preview here — market_listing_delta()
                                    # temporarily mutates equipment_condition, which is unsafe to call
                                    # every frame from a screen. Use the phone/shop view for that.
                                    text ("fair range $%d–$%d" % (_l["fair_low"], _l["fair_high"])) font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    spacing 10
                                    text ("$%d" % _l["asking"]) font PROFILE_FONT size PC_TITLE_SIZE color "#ffd66a" yalign 0.5
                                    textbutton "Buy":
                                        action Function(market_buy, _l, _l["asking"])
                                        sensitive (money >= _l["asking"])
                                        text_font ACT_FONT
                                        text_size PC_TEXT_SIZE
                                        text_color "#8fe0a0"
                                        text_hover_color "#ffffff"
                                        background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                                        xpadding 14
                                        ypadding 6
                                    textbutton "Offer…":
                                        action Function(renpy.call_in_new_context, "market_negotiate_ctx", _l["id"])
                                        text_font ACT_FONT
                                        text_size PC_TEXT_SIZE
                                        text_color "#cc9040"
                                        text_hover_color "#ffffff"
                                        background Frame("images/ui/act_bar_idle.png", 14, 14, 14, 14)
                                        hover_background Frame("images/ui/act_bar_hover_clean.png", 14, 14, 14, 14)
                                        xpadding 14
                                        ypadding 6


# ══════════════════════════════════════════════════════════════════════════════
# CALENDAR — get_calendar_events(), same list the phone renders
# ══════════════════════════════════════════════════════════════════════════════

screen capp_calendar():
    use computer_app_shell("Calendar"):
        $ _evts = get_calendar_events()
        vbox:
            spacing 8
            xfill True
            text ("Upcoming  ·  today is Day %d (%s)" % (day + 1, day_name(day))):
                font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
            viewport:
                xfill True
                ysize 730
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    if not _evts:
                        text "No upcoming events." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                    else:
                        $ _last = -1
                        for _ce in _evts:
                            if _ce["day"] != _last:
                                $ _last = _ce["day"]
                                null height 6
                                text ("Day %d  ·  %s%s" % (_ce["day"] + 1, day_name(_ce["day"]),
                                                          "  (today)" if _ce["day"] == day else "")):
                                    font PROFILE_FONT size PC_TEXT_SIZE color computer_theme(4)
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (16, 12, 16, 12)
                                hbox:
                                    spacing 12
                                    yalign 0.5
                                    text time_label(_ce.get("hour", 0)) font ACT_FONT size PC_TEXT_SIZE color "#ffd66a" xsize 110 yalign 0.5
                                    if _ce.get("commitment"):
                                        text "●" font PROFILE_FONT size PC_SMALL_SIZE color "#ffd66a" yalign 0.5
                                    text _ce["title"] font ACT_FONT size PC_TEXT_SIZE color (PC_FG if _ce["status"] == "upcoming" else PC_FG_DIM) yalign 0.5
                                    if _ce.get("npc_id") and _ce["npc_id"] in NPC_DATA:
                                        text NPC_DATA[_ce["npc_id"]]["name"] font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM yalign 0.5
                                    if _ce["status"] != "upcoming":
                                        text _ce["status"].title() font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM yalign 0.5


# ══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO — player_portfolio + player_journal, read-only
# ══════════════════════════════════════════════════════════════════════════════

screen capp_portfolio():
    use computer_app_shell("Portfolio"):
        $ _entries = list(player_portfolio.values())
        $ _g_prog = ("Programming", "#4db1ff", [e for e in _entries if e["domain"] == "programming"])
        $ _g_music = ("Music", "#ff7fb0", [e for e in _entries if e["domain"] == "music"])
        $ _g_craft = ("Craft & Skill", "#ff9f4d", [e for e in _entries if e["domain"] not in ("programming", "music")])
        $ _groups = [_g_prog, _g_music, _g_craft]
        $ _career = [e for e in player_journal if e["category"] == "career"]
        vbox:
            spacing 8
            xfill True
            text ("%d portfolio entries  ·  %d career milestones" % (len(_entries), len(_career))):
                font PROFILE_FONT size PC_TEXT_SIZE color computer_theme(4)
            viewport:
                xfill True
                ysize 740
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 6
                    xfill True
                    if not _entries and not _career:
                        text "Nothing here yet. Complete projects and reach career milestones." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                    for _gname, _gcol, _glist in _groups:
                        if _glist:
                            null height 6
                            $ _paid = sum(e["metadata"].get("pay", 0) for e in _glist)
                            text ("%s  ·  %d entries%s" % (_gname, len(_glist), ("  ·  $%d earned" % _paid) if _paid else "")):
                                font PROFILE_FONT size PC_TEXT_SIZE color _gcol
                            for _pe in sorted(_glist, key=lambda x: -x["day"]):
                                frame:
                                    xfill True
                                    background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                    padding (16, 12, 16, 12)
                                    hbox:
                                        spacing 14
                                        yalign 0.5
                                        text ("Day %d" % (_pe["day"] + 1)) font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM xsize 90 yalign 0.5
                                        text _pe["title"] font ACT_FONT size PC_TEXT_SIZE color PC_FG yalign 0.5
                                        if _pe["metadata"].get("client"):
                                            text _pe["metadata"]["client"] font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM yalign 0.5
                                        if _pe["metadata"].get("pay", 0) > 0:
                                            text ("$%d" % _pe["metadata"]["pay"]) font ACT_FONT size PC_SMALL_SIZE color "#ffd66a" yalign 0.5
                    if _career:
                        null height 6
                        text "Career Milestones" font PROFILE_FONT size PC_TEXT_SIZE color "#ffd66a"
                        for _ce in sorted(_career, key=lambda x: -x["day"]):
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (16, 12, 16, 12)
                                hbox:
                                    spacing 14
                                    yalign 0.5
                                    text ("Day %d" % (_ce["day"] + 1)) font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM xsize 90 yalign 0.5
                                    text "★" font PROFILE_FONT size PC_SMALL_SIZE color "#ffd66a" yalign 0.5
                                    text _ce["title"] font ACT_FONT size PC_TEXT_SIZE color "#ffd66a" yalign 0.5


# ══════════════════════════════════════════════════════════════════════════════
# CITYNET — read-only aggregator over existing city / career / social data
# ══════════════════════════════════════════════════════════════════════════════

screen capp_browser():
    use computer_app_shell("CityNet"):
        hbox:
            spacing 20
            # ── Left column: news + community ────────────────────────────────
            vbox:
                xsize 700
                spacing 10
                text "CityNet  ·  Local" font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
                frame:
                    xfill True
                    background Frame("images/ui/act_bar_idle.png", 18, 18, 18, 18)
                    padding (16, 12, 16, 12)
                    vbox:
                        spacing 5
                        $ _prof = city_day_profile()
                        text ("%s in the city" % _prof["name"]) font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                        text _prof["vibe"] font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        $ _flav = city_flavor_text()
                        if _flav:
                            text _flav font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                text "Community Board" font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
                viewport:
                    xfill True
                    ysize 560
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 6
                        xfill True
                        $ _posts = [p for p in social_feed_posts if p.get("day", 0) <= day][:8]
                        if not _posts:
                            text "The board is quiet today." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        for _p in _posts:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (16, 12, 16, 12)
                                vbox:
                                    spacing 3
                                    $ _pn = "You" if _p["npc_id"] == "you" else NPC_DATA.get(_p["npc_id"], {}).get("name", _p["npc_id"].title())
                                    text ("%s  ·  Day %d" % (_pn, _p.get("day", 0) + 1)) font PROFILE_FONT size PC_SMALL_SIZE color computer_theme(4)
                                    text _p["text"] font ACT_FONT size PC_TEXT_SIZE color PC_FG

            # ── Right column: events + jobs ──────────────────────────────────
            vbox:
                xsize 760
                spacing 10
                text "Upcoming Events" font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
                viewport:
                    xfill True
                    ysize 340
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 6
                        xfill True
                        $ _cevts = sorted([e for e in city_event_schedule if e["status"] == "announced" and e["day"] >= day], key=lambda x: x["day"])
                        if not _cevts:
                            text "No events announced." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        for _e in _cevts:
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (16, 12, 16, 12)
                                vbox:
                                    spacing 3
                                    text _e["title"] font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                                    text ("Day %d  ·  %s  ·  %s" % (_e["day"] + 1, time_label(_e["hour"]), _capp_loc_name(_e["location"]))):
                                        font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
                                    if _e.get("req"):
                                        text ("Recommended: %s" % next_rank_hint(_e["req"])) font ACT_FONT size PC_SMALL_SIZE color "#cc9040"
                                    if _e.get("saved_to_calendar"):
                                        text "✓ In your calendar" font ACT_FONT size PC_SMALL_SIZE color "#6fbf8f"
                                    else:
                                        textbutton "Add to Calendar":
                                            action Function(_save_city_event_to_calendar_wrapper, _e["id"])
                                            text_font ACT_FONT
                                            text_size PC_SMALL_SIZE
                                            text_color computer_theme(4)
                                            text_hover_color "#ffffff"
                                            background Frame("images/ui/act_bar_idle.png", 12, 12, 12, 12)
                                            hover_background Frame("images/ui/act_bar_hover_clean.png", 12, 12, 12, 12)
                                            xpadding 12
                                            ypadding 5

                text "Job Listings" font PROFILE_FONT size PC_TITLE_SIZE color computer_theme(4)
                viewport:
                    xfill True
                    ysize 330
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 6
                        xfill True
                        $ _jobs = [(c, d) for c, d in CAREERS.items() if c not in active_careers]
                        if not _jobs:
                            text "You already hold every posting on the board." font ACT_FONT size PC_TEXT_SIZE color PC_FG_DIM
                        for _cid, _cd in _jobs:
                            $ _r0 = _cd["ranks"][0]
                            frame:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                                padding (16, 12, 16, 12)
                                vbox:
                                    spacing 3
                                    text ("%s — %s" % (_r0["title"], _cd["name"])) font PROFILE_FONT size PC_TEXT_SIZE color PC_FG
                                    text ("$%d  ·  %s  ·  %s" % (_r0["pay"], _r0["hours"], _capp_loc_name(_cd["location"]))):
                                        font ACT_FONT size PC_SMALL_SIZE color PC_FG_DIM
                                    $ _hint = next_rank_hint(_r0["req"])
                                    if can_apply(_cid):
                                        text ("Qualified — apply in person at %s" % _capp_loc_name(_cd["location"])):
                                            font ACT_FONT size PC_SMALL_SIZE color "#6fbf8f"
                                    else:
                                        text ("Requires: %s" % (_hint or "—")) font ACT_FONT size PC_SMALL_SIZE color "#cc9040"


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

label computer_desktop_session:
    $ computer_active_app = None
    $ _active_mail_tag = None
    $ _boot = computer_boot_flavor()
    if _boot:
        $ renpy.notify(_boot)
    call screen computer_desktop
    $ computer_active_app = None
    $ _active_mail_tag = None
    return


init python:
    def debug_print_badges():
        for app_id in COMPUTER_APPS:
            renpy.notify("%s: %d" % (app_id, computer_badge_count(app_id)))
        return None
