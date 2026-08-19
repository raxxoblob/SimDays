"""Zoe early-onboarding (zoe_onboarding.rpy) — runtime self-check.

Same approach as tests/zoe_arc_selfcheck.py: EXTRACTS the real `init 4 python`
block out of the shipping .rpy and execs it against a stub `store`, so the
assertions below run the SHIPPING daily tick, bootstrap window, beat-boost
wrapper, alternate-intro gate and Marcus Talk wrapper. Change a gate, a day
count or a message key and this fails.

    python zoe_onboarding_selfcheck.py
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = io.open(os.path.join(GAME, "zoe_onboarding.rpy"), encoding="utf-8").read()
LOC = io.open(os.path.join(GAME, "locations.rpy"), encoding="utf-8").read()
SCRIPT = io.open(os.path.join(GAME, "script.rpy"), encoding="utf-8").read()
DATA = io.open(os.path.join(GAME, "data.rpy"), encoding="utf-8").read()
DST = io.open(os.path.join(GAME, "debug_scene_tester.rpy"), encoding="utf-8").read()

FAILS = []


def chk(name, cond, extra=""):
    print("  %s %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  [%s]" % extra) if extra else ""))
    if not cond:
        FAILS.append(name)


def init_block(priority, text):
    src, out, i = text.split("\n"), [], 0
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
    return "\n".join(out)


class Store(object):
    pass


store = Store()

# Defaults declared by the shipping file, read straight out of it.
for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)$", SRC, re.M):
    setattr(store, m.group(1), eval(re.sub(r"#.*$", "", m.group(2)),
                                    {"__builtins__": {}}, {}))
store.day = 1
store.zoe_met = False
store.npc_contacts = []
store.npc_messages = []
store.tier_a_beat_last_day = {}

QUEUED = []
DELIVERED = []
HERE = {"zoe": None}          # location Zoe is currently at, or None
FAM = {"zoe": 0}
BEAT_GLOBAL_OK = [True]
BASE_BEAT = [None]            # what zoe_arc.rpy's dispatcher returns
BASE_TALK = [None]


def queue_phone_message(npc, text, day, tag, responses=None):
    if any(q[3] == tag for q in QUEUED):
        return
    QUEUED.append((npc, text, day, tag))


def zoe_arc_beat_for(loc):
    return BASE_BEAT[0]


def _check_talk_followup(npc_id):
    return BASE_TALK[0]


G = {
    "store": store,
    "queue_phone_message": queue_phone_message,
    "zoe_arc_beat_for": zoe_arc_beat_for,
    "_check_talk_followup": _check_talk_followup,
    "npc_here": lambda nid, loc=None: HERE.get(nid) == loc,
    "npc_rel": lambda nid, axis: FAM.get(nid, 0),
    "_beat_global_ok": lambda: BEAT_GLOBAL_OK[0],
    "_beat_cooldown_ok": lambda bid, cd: (store.day - store.tier_a_beat_last_day.get(bid, -999)) >= cd,
    "mark_npc_encountered": lambda nid: None,
    "deliver_message_now": lambda tag: DELIVERED.append(tag),
}
exec(init_block(4, SRC), G)

tick = G["_zoe_bootstrap_tick"]
beat_for = G["zoe_arc_beat_for"]
alt_ok = G["check_zoe_alt_intro"]
talk = G["_check_talk_followup"]
mark = G["_zoe_mark_introduced"]
backfill = G["_zoe_bootstrap_backfill"]
CB = G["_ZOE_FIRST_CALLBACK"]


def reset(**kw):
    del QUEUED[:]
    del DELIVERED[:]
    store.day = 1
    store.zoe_met = False
    store.npc_contacts = []
    store.npc_messages = []
    store.tier_a_beat_last_day = {}
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)$", SRC, re.M):
        setattr(store, m.group(1), eval(re.sub(r"#.*$", "", m.group(2)),
                                        {"__builtins__": {}}, {}))
    HERE["zoe"] = None
    FAM["zoe"] = 0
    BEAT_GLOBAL_OK[0] = True
    BASE_BEAT[0] = None
    BASE_TALK[0] = None
    for k, v in kw.items():
        setattr(store, k, v)


print("A. Intro write point")
reset()
store.day = 3
mark("beach")
chk("zoe_met set", store.zoe_met)
chk("zoe_properly_introduced set", store.zoe_properly_introduced)
chk("start day stamped", store.zoe_bootstrap_start_day == 3)
chk("beach route flag set, alt flag untouched",
    store.zoe_intro_beach_done and not store.zoe_intro_alt_done)
chk("contact exchanged — without this _texting_tier('zoe') is None and every "
    "Zoe text is unreachable", "zoe" in store.npc_contacts)
mark("beach")
chk("contact not duplicated", store.npc_contacts.count("zoe") == 1)
reset()
mark("alt")
chk("alt route sets the alt flag only",
    store.zoe_intro_alt_done and not store.zoe_intro_beach_done)

print("\nB. First callback")
for imp in ("observant", "honest", "banter", ""):
    reset()
    store.day = 5
    mark("beach")
    store.zoe_first_impression = imp
    store.day = 6
    tick()
    chk("%-9s silent on day+1" % ("'" + imp + "'"), not QUEUED)
    store.day = 7
    tick()
    chk("%-9s fires on day+2" % ("'" + imp + "'"),
        len(QUEUED) == 1 and QUEUED[0][1] == CB[imp], QUEUED[0][1] if QUEUED else "-")
    chk("%-9s needs no reply" % ("'" + imp + "'"), len(QUEUED[0]) == 4)
    chk("%-9s delivered same day (tick runs after deliver_due_messages)"
        % ("'" + imp + "'"), DELIVERED == ["zoe_first_callback"])
    store.day = 8
    tick()
    chk("%-9s never repeats" % ("'" + imp + "'"), len(QUEUED) == 1)

reset()
store.day = 5
mark("beach")
store.zoe_first_impression = "nonsense_from_an_old_save"
store.day = 7
tick()
chk("unknown impression falls back rather than KeyError",
    QUEUED and QUEUED[0][1] == CB[""])

print("\nC. Marcus beach reminder")
reset(marcus_mentioned_zoe=True)
store.day = 2
tick()
chk("silent before day 3", not any(q[3] == "marcus_beach_reminder" for q in QUEUED))
store.day = 3
tick()
chk("fires on day 3", any(q[3] == "marcus_beach_reminder" for q in QUEUED))
store.day = 4
tick()
chk("fires once only",
    len([q for q in QUEUED if q[3] == "marcus_beach_reminder"]) == 1)
reset(marcus_mentioned_zoe=True)
store.day = 5
mark("beach")
tick()
chk("never nags a player who already met her",
    not any(q[3] == "marcus_beach_reminder" for q in QUEUED))
reset(marcus_mentioned_zoe=False)
store.day = 9
tick()
chk("no reminder if Marcus never named her", not QUEUED)

print("\nD. Bootstrap completion")
reset()
store.day = 1
mark("beach")
for d in range(2, 12):
    store.day = d
    tick()
    if d == 3:
        chk("not complete at day+2 (callback only just sent)",
            not store.zoe_bootstrap_complete)
    if d == 4:
        chk("not complete at day+3 without a beat", not store.zoe_bootstrap_complete)
    if d == 8:
        chk("completes at day+7 even with no beat", store.zoe_bootstrap_complete)

reset()
store.day = 1
mark("beach")
store.day = 3
tick()
store.tier_a_beat_last_day["zoe_print"] = 3
store.day = 4
tick()
chk("a fired beat completes it early (day+3)", store.zoe_bootstrap_complete)

reset()
store.day = 1
mark("beach")
store.tier_a_beat_last_day["zoe_print"] = 0     # BEFORE the intro
store.day = 4
tick()
chk("a beat that fired before the intro does not count",
    not store.zoe_bootstrap_complete)

print("\nE. Bootstrap window / beat boost")
reset()
store.day = 1
mark("beach")
FAM["zoe"] = 15
HERE["zoe"] = "location_cafe"
chk("relaxed Grounds gate opens at fam 15 (ships at 30)",
    beat_for("location_cafe") == "zoe_wednesday_grounds_scene")
chk("boost is café-only", beat_for("location_park") is None)
FAM["zoe"] = 11
chk("still has a floor (fam 12)", beat_for("location_cafe") is None)
FAM["zoe"] = 15
HERE["zoe"] = "location_park"
chk("respects her schedule via npc_here", beat_for("location_cafe") is None)
HERE["zoe"] = "location_cafe"
BEAT_GLOBAL_OK[0] = False
chk("respects the one-beat-per-day global budget", beat_for("location_cafe") is None)
BEAT_GLOBAL_OK[0] = True
store.tier_a_beat_last_day["zoe_wednesday"] = store.day - 2
chk("respects the relaxed 3-day cooldown", beat_for("location_cafe") is None)
store.tier_a_beat_last_day["zoe_wednesday"] = store.day - 3
chk("...and reopens on day 3", beat_for("location_cafe") == "zoe_wednesday_grounds_scene")

BASE_BEAT[0] = "zoe_not_ready_scene"
chk("the shipping dispatcher always wins",
    beat_for("location_cafe") == "zoe_not_ready_scene")
BASE_BEAT[0] = None
store.day = store.zoe_bootstrap_start_day + 11
chk("boost expires after 10 days", beat_for("location_cafe") is None)
store.day = store.zoe_bootstrap_start_day + 1
store.zoe_bootstrap_complete = True
chk("boost stops the moment bootstrap completes", beat_for("location_cafe") is None)
reset()
FAM["zoe"] = 60
HERE["zoe"] = "location_cafe"
chk("boost never fires before the intro", beat_for("location_cafe") is None)

print("\nF. Alternate intro gate")
reset()
HERE["zoe"] = "location_cafe"
store.day = 3
chk("closed before day 4", not alt_ok("location_cafe"))
store.day = 4
chk("open on day 4 at Grounds", alt_ok("location_cafe"))
chk("not offered where she isn't", not alt_ok("location_hub"))
chk("not offered at unhooked locations", not alt_ok("location_park"))
HERE["zoe"] = "location_hub"
chk("open at the Hub too", alt_ok("location_hub"))
mark("beach")
chk("closed once she's been introduced", not alt_ok("location_hub"))
reset(zoe_met=True)
HERE["zoe"] = "location_hub"
store.day = 9
chk("closed for an old save that already met her", not alt_ok("location_hub"))

print("\nG. Marcus Talk callback")
reset()
chk("silent before the intro", talk("marcus") is None)
mark("beach")
chk("offered after the intro", talk("marcus") == "marcus_met_zoe_callback")
chk("not offered for other NPCs", talk("nora") is None)
store.marcus_met_zoe_callback_done = True
chk("fires once", talk("marcus") is None)
store.marcus_met_zoe_callback_done = False
BASE_TALK[0] = "talk_followup_marcus_first_shift"
chk("never pre-empts the shipping followup chain",
    talk("marcus") == "talk_followup_marcus_first_shift")

print("\nH. Old-save backfill")
reset(zoe_met=True)
store.day = 40
backfill()
chk("derives properly_introduced", store.zoe_properly_introduced)
chk("derives bootstrap_complete", store.zoe_bootstrap_complete)
chk("suppresses the callback", store.zoe_first_callback_sent)
chk("suppresses the Marcus callback", store.marcus_met_zoe_callback_done)
tick()
chk("old save gets no onboarding texts at all", not QUEUED)
chk("alt intro impossible", not alt_ok("location_cafe"))
reset()
store.day = 5
backfill()
chk("no-op for a save that never met her",
    not store.zoe_properly_introduced and not store.zoe_bootstrap_complete)

print("\nI. Wiring into the shipping files")
labels = set(re.findall(r"^label\s+([a-z_0-9]+)", SRC, re.M))
chk("zoe_beach_intro routes to the AUTHORED meeting instead of duplicating it",
    "zoe_beach_intro" in labels and "jump beach_meet_zoe" in SRC
    and "label beach_meet_zoe" in LOC)
chk("the beach scene calls the onboarding tail",
    "call zoe_beach_intro_tail" in LOC and "zoe_beach_intro_tail" in labels)
chk("the tail is the only gameplay writer of zoe_met",
    len(re.findall(r"^\s*(?:\$\s*)?(?:store\.)?zoe_met\s*=\s*True", LOC, re.M)) == 0)
chk("beach intro is still the FIRST branch of location_beach",
    re.search(r"label location_beach:(?:.|\n)*?if not zoe_met and hour < 19:\s*\n\s*jump beach_meet_zoe", LOC))
chk("alt intro hooked at Grounds and the Hub",
    LOC.count("check_zoe_alt_intro(") == 2)
chk("alt intro outranks the Tier A chain at Grounds",
    LOC.index('check_zoe_alt_intro("location_cafe")') < LOC.index("check_nora_cover_scene()"))
chk("alt intro outranks the Tier A chain at the Hub",
    LOC.index('check_zoe_alt_intro("location_hub")') < LOC.index("check_eli_after_shift()"))
chk("Marcus names Zoe in the move-in intro",
    "marcus_mentioned_zoe = True" in SCRIPT and "Zoe's usually down there" in SCRIPT)
chk("the daily tick is wired into new_day, before the initiative picker",
    "_zoe_bootstrap_tick()" in DATA
    and DATA.index("_zoe_bootstrap_tick()") < DATA.index("_check_npc_initiative()"))
chk("every impression the intros can record has callback copy",
    set(re.findall(r'zoe_first_impression = "(\w*)"', SRC + LOC)) <= set(CB))
chk("no debug symbol leaks into the gameplay file",
    "SCENE_TEST_REGISTRY" not in SRC)

print("\nJ. Scene Tester pack")
G2 = dict(G)
G2["SCENE_TEST_REGISTRY"] = {}
G2.update({"_dst_zoe_arc_base": lambda: None, "_dst_zoe_arc_reset": lambda: None,
           "_dst_beat_set_weekday": lambda d: None, "_dst_beat_clear": lambda b: None,
           "set_npc_rel": lambda *a: None, "deliver_due_messages": lambda: None,
           "renpy": type("R", (), {"notify": staticmethod(lambda *a: None)})})
exec(init_block(2, DST), G2)
REG = G2["SCENE_TEST_REGISTRY"]
ARC = io.open(os.path.join(GAME, "zoe_arc.rpy"), encoding="utf-8").read()
all_labels = labels | set(re.findall(r"^label\s+([a-z_0-9]+)", LOC + DST + ARC, re.M))
chk("5 onboarding entries registered (init 2, so zoe_arc_selfcheck's init-1 "
    "count of 5 is untouched)", len(REG) == 5, len(REG))
chk("every entry has a callable reset", all(callable(e["reset"]) for e in REG.values()))
chk("every preset is callable",
    all(callable(p) for e in REG.values() for p in e["presets"].values()))
chk("every scene label exists",
    all(e["label"] in all_labels or e["label"] == "map" for e in REG.values()),
    ",".join(sorted(e["label"] for e in REG.values()
                    if e["label"] not in all_labels and e["label"] != "map")))
chk("every checkpoint label exists",
    all(v in all_labels for e in REG.values() for v in (e["checkpoints"] or {}).values()))

print("\n%s  (%d failure(s))" % ("ALL PASS" if not FAILS else "FAILURES: " + ", ".join(FAILS),
                                len(FAILS)))
sys.exit(1 if FAILS else 0)
