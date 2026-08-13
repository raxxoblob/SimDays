# Mail — institutional and transactional emails (rent, freelance, bank).
# Distinct from phone messages (personal NPC conversations in phone.rpy).

define RENT_BY_TIER = {1: 220, 2: 550, 3: 1300}

default player_mail = []
default _active_mail_tag = None

init python:

    def queue_mail(sender, subject, body, category, send_on_day, tag):
        """Enqueue a mail. No-op if tag already exists."""
        if mail_already_queued(tag):
            return
        store.player_mail = list(store.player_mail) + [{
            "sender": sender,
            "subject": subject,
            "body": body,
            "category": category,
            "send_on_day": send_on_day,
            "delivered": False,
            "delivered_on": -1,
            "read": False,
            "tag": tag,
        }]

    def deliver_due_mail():
        """Mark mail whose send_on_day <= day as delivered. Called from new_day()."""
        updated = []
        for m in store.player_mail:
            if not m["delivered"] and m["send_on_day"] <= store.day:
                m = dict(m)
                m["delivered"] = True
                m["delivered_on"] = store.day
            updated.append(m)
        store.player_mail = updated

    def unread_mail_count():
        return sum(1 for m in store.player_mail if m.get("delivered") and not m.get("read"))

    def mark_mail_read(tag):
        store.player_mail = [
            dict(m, read=True) if m["tag"] == tag else m
            for m in store.player_mail
        ]

    def mail_already_queued(tag):
        return any(m["tag"] == tag for m in store.player_mail)


# ── Phone: inbox list ──────────────────────────────────────────────────────────
screen phone_mail_scr():
    modal True
    $ _delivered = [m for m in player_mail if m.get("delivered")]
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Mail" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 600
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    xfill True
                    if not _delivered:
                        null height 12
                        text "No mail yet." font ACT_FONT size 14 color "#4a6080" xalign 0.5
                    for _m in reversed(_delivered):
                        button:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 24, 24, 24, 24)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 24, 24, 24, 24)
                            padding (12, 8, 12, 8)
                            action [Function(mark_mail_read, _m["tag"]), SetVariable("_active_mail_tag", _m["tag"]), Hide("phone_mail_scr"), Show("phone_mail_detail_scr")]
                            vbox:
                                spacing 2
                                hbox:
                                    xfill True
                                    text _m["sender"] font PROFILE_FONT size 13 color ("#ffffff" if not _m["read"] else "#7a90a8")
                                    if not _m["read"]:
                                        text " ●" font PROFILE_FONT size 10 color "#5bcafa" yalign 0.5
                                text _m["subject"] font ACT_FONT size 13 color ("#cfe0f5" if not _m["read"] else "#5a7090")
                                $ _snip = (_m["body"][:50] + "…") if len(_m["body"]) > 50 else _m["body"]
                                text _snip font ACT_FONT size 11 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("phone_mail_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Phone: mail detail ─────────────────────────────────────────────────────────
screen phone_mail_detail_scr():
    modal True
    $ _dm = next((m for m in player_mail if m.get("tag") == _active_mail_tag), None)
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            hbox:
                spacing 8
                button:
                    xysize (28, 28)
                    background None
                    hover_background Frame("images/ui/act_bar_idle.png", 10, 10, 10, 10)
                    action [Hide("phone_mail_detail_scr"), Show("phone_mail_scr")]
                    text "‹" font PROFILE_FONT size 22 color "#7fb0d6" hover_color "#ffffff" align (0.5, 0.5)
                text "Mail" font PROFILE_FONT size 18 color "#ffffff" yalign 0.5
            null height 6
            if _dm:
                viewport:
                    xfill True
                    ysize 580
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        xfill True
                        text _dm["subject"] font PROFILE_FONT size 15 color "#ffffff"
                        text ("From: " + _dm["sender"]) font ACT_FONT size 12 color "#5bcafa"
                        null height 4
                        text _dm["body"] font ACT_FONT size 14 color "#cfe0f5"
            else:
                text "Mail not found." font ACT_FONT size 14 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("phone_mail_detail_scr"), Show("phone_mail_scr")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"


# ── Computer: full-width inbox (list + inline detail via _active_mail_tag) ──────
screen computer_mail_scr():
    modal True
    $ _delivered = [m for m in player_mail if m.get("delivered")]
    add "#000000aa"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 600
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (20, 16, 20, 16)
        vbox:
            spacing 8
            if _active_mail_tag is None:
                text "Mail" font PROFILE_FONT size 24 color "#ffffff" xalign 0.5
                null height 4
                viewport:
                    xfill True
                    ysize 460
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        xfill True
                        if not _delivered:
                            text "No mail yet." font ACT_FONT size 15 color "#4a6080" xalign 0.5
                        for _m in reversed(_delivered):
                            button:
                                xfill True
                                background Frame("images/ui/act_bar_idle.png", 20, 20, 20, 20)
                                hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20, 20, 20)
                                padding (12, 8, 12, 8)
                                action [Function(mark_mail_read, _m["tag"]), SetVariable("_active_mail_tag", _m["tag"])]
                                vbox:
                                    spacing 2
                                    hbox:
                                        xfill True
                                        text _m["sender"] font PROFILE_FONT size 14 color ("#ffffff" if not _m["read"] else "#7a90a8")
                                        if not _m["read"]:
                                            text " ●" font PROFILE_FONT size 11 color "#5bcafa" yalign 0.5
                                    text _m["subject"] font ACT_FONT size 14 color ("#cfe0f5" if not _m["read"] else "#5a7090")
                                    $ _snip = (_m["body"][:80] + "…") if len(_m["body"]) > 80 else _m["body"]
                                    text _snip font ACT_FONT size 12 color "#4a6080"
                textbutton "Close" action Return() xalign 0.5 text_font ACT_FONT text_size 19 text_color "#9fb6d6" text_hover_color "#ffffff"
            else:
                $ _dm = next((m for m in player_mail if m.get("tag") == _active_mail_tag), None)
                if _dm:
                    text _dm["subject"] font PROFILE_FONT size 18 color "#ffffff" xalign 0.5
                    text ("From: " + _dm["sender"]) font ACT_FONT size 13 color "#5bcafa" xalign 0.5
                    null height 4
                    viewport:
                        xfill True
                        ysize 400
                        mousewheel True
                        scrollbars "vertical"
                        vbox:
                            spacing 8
                            xfill True
                            text _dm["body"] font ACT_FONT size 15 color "#cfe0f5"
                hbox:
                    spacing 16
                    xalign 0.5
                    textbutton "Back to inbox" action SetVariable("_active_mail_tag", None) text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"
                    textbutton "Close" action [SetVariable("_active_mail_tag", None), Return()] text_font ACT_FONT text_size 17 text_color "#9fb6d6" text_hover_color "#ffffff"
