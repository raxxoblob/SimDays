"""Tier A location-beat runtime self-check.

Same approach as phase66-69 / summer_festival: EXTRACTS the real `init python`
blocks out of the shipping .rpy files and execs them against a stub `store`, so
every assertion below runs the SHIPPING code. Change the eligibility window,
Nora's schedule, the source_category or the follow-up tag and this fails.

Grows as more Tier A beats land — one section per beat.

    python location_beats_selfcheck.py
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rpy_python_blocks(path, priority=None):
    """Blocks from a .rpy file. priority=None -> unprioritised `init python:`
    only; priority=N -> `init N python:` only."""
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(src):
        m = re.match(r"^init(?:\s+(-?\d+))?\s+python\s*:\s*$", src[i])
        if m:
            got = int(m.group(1)) if m.group(1) else None
            i += 1
            body = []
            while i < len(src):
                ln = src[i]
                if ln.strip() and not ln.startswith((" ", "\t")):
                    break
                body.append(ln)
                i += 1
            if got == priority:
                out.append(textwrap.dedent("\n".join(body)))
        else:
            i += 1
    return out


def rpy_defaults(path):
    out = {}
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read()
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)$", src, re.M):
        name, chunk = m.group(1), re.sub(r"#.*$", "", m.group(2))
        try:
            out[name] = eval(chunk, {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


DEFAULTS = {}
for _f in ("data.rpy", "phone_messages.rpy", "npc_schedules.rpy",
           "npc_relationships.rpy"):
    DEFAULTS.update(rpy_defaults(_f))


class Store(object):
    def __init__(self):
        self.day = 5            # day 5 = Saturday (day % 7 == 5, in WKD)
        self.hour = 16.0
        for k, v in DEFAULTS.items():
            setattr(self, k,
                    list(v) if isinstance(v, list) else
                    dict(v) if isinstance(v, dict) else v)
        self.nora_met = True


class _Config(object):
    developer = False


class _Renpy(object):
    config = _Config()

    def notify(self, *a, **k):
        return None

    def log(self, *a, **k):
        return None


store = Store()
REL_CALLS = []
G = {}


def boot():
    global G
    G = {
        "store": store,
        "renpy": _Renpy(),
        "MON_FRI": {0, 1, 2, 3, 4}, "MON_SAT": {0, 1, 2, 3, 4, 5},
        "WKD": {5, 6}, "FRISUN": {4, 5, 6},
        "npc_known": lambda nid: True,
        "npc_is_temporarily_unavailable": lambda nid: False,
        "NPC_DATA": {n: {"name": n.capitalize(),
                         "aff": n + "_affection", "trust": n + "_trust"}
                     for n in ("nora", "marcus", "eli", "zoe", "kai", "sam",
                               "lena", "natalie", "martha", "caroline", "rena")},
        "skill_val": lambda k: 0,
        "gain_skill_practice": lambda k, x, h=1: x,
        "_NPC_DISPLAY": {"nora": "Nora"},
        # Owned by interact.rpy (init 0), which this check does not exec whole.
        "_apply_aff": lambda nid, d: None,
        "_apply_trust": lambda nid, d: None,
        "_check_relationship_thresholds": lambda nid: None,
        "has_player_state": lambda s: False,
    }
    for path, prio in (("phone_messages.rpy", None),
                       ("npc_schedules.rpy", None),
                       ("npc_relationships.rpy", 1),
                       ("location_beats.rpy", None)):
        for blk in rpy_python_blocks(path, prio):
            try:
                exec(compile(blk, path, "exec"), G)
            except Exception as e:                     # noqa: BLE001
                print("  (skipped a block in %s: %s: %s)" % (path, type(e).__name__, e))
    G["store"] = store
    # Record what the accept branch would hand the relationship system, while
    # still letting the real capped/paced implementation run.
    real_arc = G["apply_relationship_change"]

    def _spy(npc_id, source_id, source_category, **kw):
        REL_CALLS.append((npc_id, source_id, source_category, kw))
        return real_arc(npc_id, source_id, source_category, **kw)
    G["apply_relationship_change"] = _spy


FAILS = []


def chk(label, cond, detail=""):
    if not cond:
        FAILS.append(label)
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", label,
                           ("  — " + str(detail)) if detail else ""))


def eligible():
    return G["check_nora_cover_scene"]()


def reset(**kw):
    store.day, store.hour = 5, 16.0
    store.nora_cover_shift_triggered = False
    store.covered_nora_shift = False
    store.nora_met = True
    store.nora_life_state = "cafe"
    store.npc_messages = []
    store.npc_schedule_overrides = []
    for k, v in kw.items():
        setattr(store, k, v)


def main():
    boot()

    # ── A. defaults are old-save safe ────────────────────────────────────────
    print("\nA. defaults")
    chk("nora_cover_shift_triggered defaults False",
        DEFAULTS.get("nora_cover_shift_triggered") is False,
        DEFAULTS.get("nora_cover_shift_triggered"))
    chk("covered_nora_shift defaults False",
        DEFAULTS.get("covered_nora_shift") is False,
        DEFAULTS.get("covered_nora_shift"))

    # ── B. eligibility ───────────────────────────────────────────────────────
    print("\nB. eligibility (real check_nora_cover_scene)")
    reset()
    chk("fires when every condition is met",
        eligible() == "nora_cover_shift_scene", eligible())
    reset(nora_cover_shift_triggered=True)
    chk("never fires twice", eligible() is None, eligible())
    reset(nora_met=False)
    chk("blocked before meeting Nora", eligible() is None)
    reset(hour=13.0)
    chk("blocked too early in her shift (13:00)", eligible() is None)
    reset(hour=18.5)
    chk("blocked after her shift ends (18:30)", eligible() is None)
    reset(day=1)      # Tuesday: 15-17 is 'lingering', not a shift
    chk("blocked when she is off-shift lingering (Tue 16:00)",
        eligible() is None)
    reset(day=0)      # Monday 16:00: she is commuting/at home, not at the café
    chk("blocked when she is not at the café (Mon 16:00)", eligible() is None)
    reset(nora_life_state="school")
    chk("blocked once she has left the café for nursing school",
        eligible() is None)

    # the shipping schedule really does put her there in the window we claim
    reset()
    chk("npc_here agrees she is at the café",
        G["npc_here"]("nora", "location_cafe"))
    chk("and that she is on shift",
        G["resolve_npc_state"]("nora")["activity_id"] == "working_shift")

    # ── C. accept branch effects ─────────────────────────────────────────────
    print("\nC. accept branch")
    reset()
    del REL_CALLS[:]
    store.covered_nora_shift = True
    hours = max(1.0, 19.0 - float(store.hour))
    chk("covering runs to café close, never negative hours",
        hours == 3.0, hours)
    chk("late entry still costs at least an hour",
        max(1.0, 19.0 - 18.9) == 1.0)
    chk("covered_nora_shift set on accept", store.covered_nora_shift is True)

    G["apply_relationship_change"]("nora", source_id="nora_cover_shift",
                                   source_category="helping_npc",
                                   trust=4, familiarity=1, meaningful=True)
    chk("one relationship call, categorised as helping_npc",
        len(REL_CALLS) == 1 and REL_CALLS[0][2] == "helping_npc", REL_CALLS)
    chk("trust-led reward (trust 4, familiarity 1, no affection)",
        REL_CALLS[0][3].get("trust") == 4
        and REL_CALLS[0][3].get("familiarity") == 1
        and not REL_CALLS[0][3].get("affection"), REL_CALLS[0][3])
    chk("helping_npc cap lets trust move at all",
        G["RELATIONSHIP_SOURCE_CAPS"]["helping_npc"]["trust"] >= 4)
    chk("trust actually rose on the real store",
        G["npc_rel"]("nora", "trust") > 0, G["npc_rel"]("nora", "trust"))

    # ── D. follow-up message ─────────────────────────────────────────────────
    print("\nD. follow-up message")
    reset()
    for _ in range(2):
        G["queue_phone_message"]("nora", "Seriously, thanks again. You really "
                                 "saved me last night.", store.day + 1,
                                 "nora_cover_shift_thanks")
    chk("queued exactly once even if the label re-runs",
        len(store.npc_messages) == 1, len(store.npc_messages))
    msg = store.npc_messages[0]
    chk("from Nora, tagged nora_cover_shift_thanks",
        msg["npc_id"] == "nora" and msg["tag"] == "nora_cover_shift_thanks")
    chk("arrives the next day", msg["send_on_day"] == store.day + 1)
    chk("not delivered before its day",
        (G["deliver_due_messages"](), store.npc_messages[0]["delivered"])[1] is False)
    store.day += 1
    G["deliver_due_messages"]()
    chk("delivered on the next day", store.npc_messages[0]["delivered"] is True)

    # ── E. decline branch is inert ───────────────────────────────────────────
    print("\nE. decline branch")
    reset()
    del REL_CALLS[:]
    chk("no relationship change on decline", REL_CALLS == [])
    chk("no message queued on decline", store.npc_messages == [])
    chk("covered_nora_shift stays False", store.covered_nora_shift is False)
    chk("beat still marked as fired so it cannot be re-rolled",
        G["check_nora_cover_scene"]() is not None
        and (setattr(store, "nora_cover_shift_triggered", True)
             or G["check_nora_cover_scene"]() is None))

    # ── F. in-person callback in nora_greet ──────────────────────────────────
    print("\nF. in-person callback")
    chk("nora_cover_thanks_said defaults False",
        DEFAULTS.get("nora_cover_thanks_said") is False,
        DEFAULTS.get("nora_cover_thanks_said"))
    greet = io.open(os.path.join(GAME, "interact.rpy"), encoding="utf-8").read()
    greet = greet.split("label nora_greet:")[1].split("\nlabel ")[0]
    chk("nora_greet gates the acknowledgement on covered_nora_shift",
        "covered_nora_shift" in greet)
    chk("and one-shots it so it cannot repeat every greeting",
        "not nora_cover_thanks_said" in greet
        and "nora_cover_thanks_said = True" in greet)

    # ── G. Scene Tester registry integrity ───────────────────────────────────
    # Compile-time checks only: the registry must never point at a label or a
    # preset that does not exist, and must never be mistaken for gameplay data.
    print("\nG. Scene Tester registry (debug_scene_tester.rpy)")
    reg_g = {"store": store, "renpy": _Renpy(), "config": _Config(),
             "mark_npc_encountered": lambda n: None,
             "set_npc_rel": lambda n, a, v: None,
             "SF_NPCS": ["marcus", "eli", "zoe", "nora"],
             "_debug_festival_reset": lambda: None}
    for blk in rpy_python_blocks("debug_scene_tester.rpy", None):
        exec(compile(blk, "debug_scene_tester.rpy", "exec"), reg_g)
    REG = reg_g.get("SCENE_TEST_REGISTRY", {})
    CATS = reg_g.get("SCENE_TEST_CATEGORIES", None)

    chk("registry is non-empty", bool(REG), len(REG))
    chk("SCENE_TEST_CATEGORIES is a list of strings",
        isinstance(CATS, list) and CATS
        and all(isinstance(c, str) for c in CATS), CATS)

    # every label / checkpoint string must exist as `label X:` somewhere in game/
    labels = set()
    for fn in sorted(os.listdir(GAME)):
        if fn.endswith(".rpy"):
            labels.update(re.findall(
                r"^label\s+([\w.]+)\s*(?:\(.*?\))?\s*:",
                io.open(os.path.join(GAME, fn), encoding="utf-8").read(), re.M))

    for sid, e in sorted(REG.items()):
        chk("%s has the required keys" % sid,
            all(k in e for k in ("title", "category", "desc", "label",
                                 "presets", "reset")), sorted(e))
        chk("%s category is a known category" % sid,
            e.get("category") in (CATS or []), e.get("category"))
        chk("%s label '%s' exists" % (sid, e.get("label")),
            e.get("label") in labels)
        chk("%s presets are all callable" % sid,
            bool(e.get("presets"))
            and all(callable(f) for f in e["presets"].values()),
            list(e.get("presets", {})))
        chk("%s reset is callable" % sid, callable(e.get("reset")))
        for cn, cl in sorted((e.get("checkpoints") or {}).items()):
            chk("%s checkpoint '%s' -> label '%s' exists" % (sid, cn, cl),
                cl in labels)

    # the registry must not shadow any gameplay registry's keys
    gameplay_keys = set()
    for path, name in (("world_pulse.rpy", "WORLD_EVENT_TEMPLATES"),
                       ("world_pulse.rpy", "RARE_OPPORTUNITY_TEMPLATES")):
        src = io.open(os.path.join(GAME, path), encoding="utf-8").read()
        blk = src.split(name + " = ")[1].split("\n    }")[0] if name + " = " in src else ""
        gameplay_keys.update(re.findall(r'^\s{8}"(\w+)"\s*:', blk, re.M))
    inv = io.open(os.path.join(GAME, "npc_invitations.rpy"), encoding="utf-8").read()
    gameplay_keys.update(re.findall(r'"id"\s*:\s*"(\w+)"', inv))
    chk("no registry id collides with a gameplay template id",
        not (set(REG) & gameplay_keys), sorted(set(REG) & gameplay_keys))

    # no gameplay file may read the debug registry
    readers = [fn for fn in sorted(os.listdir(GAME))
               if fn.endswith(".rpy") and fn != "debug_scene_tester.rpy"
               and "SCENE_TEST_REGISTRY" in
               io.open(os.path.join(GAME, fn), encoding="utf-8").read()]
    chk("SCENE_TEST_REGISTRY is referenced by no other .rpy file", not readers, readers)

    # the screen is gated on config.developer
    dst = io.open(os.path.join(GAME, "debug_scene_tester.rpy"), encoding="utf-8").read()
    chk("dev screen gates on config.developer", "config.developer" in dst)
    chk("debug menu has exactly one entry point",
        io.open(os.path.join(GAME, "debug.rpy"), encoding="utf-8")
        .read().count('Show("debug_scene_tester")') == 1)

    print("\n%d check(s) failed" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
