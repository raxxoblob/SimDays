# Floating "gain" feedback - top-left, under the HUD. When you skill up, earn,
# or spend, a small card slides in (skill = mini bar filling + "+2", cash =
# green "+$120"), lingers, then fades. Non-blocking overlay.

init python:
    import time as _time

    # str/int/chr/app -> (label, colour, hud-icon file or None, bar-fill key)
    STAT_META = {
        "str": ("STR", "#f2765f", "stat_str",    "str"),
        "int": ("INT", "#5f9cf2", "stat_int",    "int"),
        "chr": ("CHR", "#f2c65f", "stat_social", "chr"),
        "app": ("APP", "#c07ee6", None,          "app"),
    }

    def _push_gain(**g):
        g["t"] = _time.time()
        g.setdefault("life", 2.6)
        store._gains.append(g)
        renpy.restart_interaction()

    def _prune_gains():
        now = _time.time()
        kept = [g for g in store._gains if now - g["t"] < g["life"]]
        if len(kept) != len(store._gains):
            store._gains = kept
            renpy.restart_interaction()

    def gain_stat(name, amt):
        """Raise a skill and flash a filling-bar card."""
        cur = getattr(store, "stat_" + name)
        new = min(100, cur + amt)
        setattr(store, "stat_" + name, new)
        label, colour, icon, fillkey = STAT_META[name]
        _push_gain(kind="stat", text="+%d %s" % (amt, label), color=colour,
                   icon=("images/ui/icons/%s.png" % icon) if icon else None,
                   value=new, fill="images/ui/bar_fill_%s.png" % fillkey)

    def gain_money(amt):
        """Change money and flash a green (+) or red (-) cash card."""
        store.money += amt
        if amt >= 0:
            _push_gain(kind="money", text="+$%d" % amt, color="#39c07a",
                       icon="images/ui/icons/stat_money.png")
        else:
            _push_gain(kind="money", text="-$%d" % (-amt), color="#e86a55",
                       icon="images/ui/icons/stat_money.png")

    def gain_aff(npc_name, delta):
        """Flash an affection toast (called from do_talk / do_gift)."""
        if delta > 0:
            _push_gain(kind="aff", text="+%d  %s" % (delta, npc_name), color="#f07888",
                       icon="images/ui/icons/stat_social.png")
        elif delta < 0:
            _push_gain(kind="aff", text="%d  %s" % (delta, npc_name), color="#e86a55",
                       icon="images/ui/icons/stat_social.png")

default _gains = []   # underscore -> excluded from rollback (transient UI)


# Slide in from the left, hold, fade out. `life` matches the prune lifetime.
transform gain_toast(life=2.6):
    xoffset -50 alpha 0.0
    parallel:
        easein 0.28 xoffset 0
    parallel:
        linear 0.28 alpha 1.0
    pause life - 0.9
    linear 0.55 alpha 0.0 xoffset -24


screen gain_card(g):
    frame:
        at gain_toast(g["life"])
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (16, 10, 20, 10)
        hbox:
            spacing 12
            if g["icon"]:
                add g["icon"] xysize (38, 38) yalign 0.5
            vbox:
                spacing 5
                text g["text"] font PROFILE_FONT size 26 color g["color"] yalign 0.5
                if g["kind"] == "stat":
                    bar:
                        value AnimatedValue(g["value"], 100, delay=0.9, old_value=0)
                        xysize (156, 14) yalign 0.5
                        left_bar Frame(g["fill"], 16, 0) right_bar Frame("images/ui/bar_track.png", 16, 0) thumb Null()


# Always-on overlay. ponytail: cards are matched by list index, so pruning the
# oldest can nudge a still-animating card; fine for the 1-2 toasts we show.
screen gains_overlay():
    zorder 40
    timer 0.4 repeat True action Function(_prune_gains)
    vbox:
        xpos 24
        ypos 150
        spacing 10
        for g in _gains:
            use gain_card(g)

init python:
    config.overlay_screens.append("gains_overlay")
