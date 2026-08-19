"""Relationship continuity pass (relationship_continuity.rpy) — self-check.

Same approach as tests/zoe_arc_selfcheck.py: EXTRACTS the real `init python`
blocks out of the shipping .rpy file and execs them against a stub `store`, so
everything below runs the SHIPPING micro dispatcher, busy gates, pre-Talk
wrapper, routine conditions and old-save backfill. Change a cooldown, a stage
band, a schedule window or a threshold and this fails.

    python relationship_continuity_selfcheck.py
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = "relationship_continuity.rpy"
SRC = io.open(os.path.join(GAME, FILE), encoding="utf-8").read()

FAILS = []


def chk(name, cond, extra=""):
    print("  %s %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  [%s]" % (extra,)) if extra else ""))
    if not cond:
        FAILS.append(name)


def init_block(priority, text=None):
    src = (text if text is not None else SRC).split("\n")
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
    return "\n".join(out)


def defaults_of(path):
    out = {}
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)$",
                         io.open(os.path.join(GAME, path), encoding="utf-8").read(), re.M):
        name, chunk = m.group(1), re.sub(r"#.*$", "", m.group(2))
        try:
            out[name] = eval(chunk, {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


class Store(object):
    def __init__(self):
        self.day = 30
        self.hour = 10.0
        for path in ("data.rpy", "marcus_onboarding.rpy", "zoe_arc.rpy",
                     "zoe_onboarding.rpy", FILE):
            for k, v in defaults_of(path).items():
                setattr(self, k, list(v) if isinstance(v, list)
                        else dict(v) if isinstance(v, dict) else v)
        self.story_scene_active = False
        self.current_loc = "location_bar"
        self.marcus_met = True
        self.zoe_met = True
        self.npc_last_seen = {}
        self.npc_contacts = ["marcus", "zoe"]
        self.tier_a_beat_last_day = {}
        self.bar_game_cooldowns = {}
        self.apartment_tier = 1


store = Store()
STAGE = {"marcus": "friend", "zoe": "friend"}
LIFE = {"marcus": None, "zoe": None}
INTERVIEW = {"open": False}

G = {
    "store": store,
    "config": type("C", (), {"after_load_callbacks": []})(),
    "renpy": type("R", (), {"notify": staticmethod(lambda *a, **k: None)})(),
    "npc_relationship_stage": lambda nid: STAGE[nid],
    "npc_life_state": lambda nid: LIFE[nid],
    "mf_interview_unresolved": lambda: INTERVIEW["open"],
    "_apply_aff": lambda nid, d: None,
    "queue_phone_message": lambda *a, **k: None,
    "_clear_initiative_pending": lambda nid: None,
    "_INITIATIVE_MSGS": {},
    "_INITIATIVE_VARIANTS": {"marcus": ["marcus_msg_x"], "zoe": ["zoe_msg_x"]},
    "_VARIANT_MIN_TIER": {},
    "_VARIANT_WEIGHTS": {},
    "_VARIANT_CONDITIONS": {},
    # The shipping resolver this file wraps. Anything it answers must win.
    "_check_talk_followup": lambda nid: ("REAL" if nid == "nora" else None),
}

exec(init_block(7), G)
exec(init_block(8), G)

pick = G["rc_pick_micro"]
fired = G["rc_micro_fired"]
m_busy = G["rc_marcus_busy"]
z_busy = G["rc_zoe_busy"]
talk = G["_check_talk_followup"]
backfill = G["_rc_backfill"]
COND = G["_VARIANT_CONDITIONS"]


def reset(**kw):
    for k, v in defaults_of(FILE).items():
        setattr(store, k, dict(v) if isinstance(v, dict) else v)
    store.day = 30
    store.hour = 10.0
    store.story_scene_active = False
    store.current_loc = "location_bar"
    store.marcus_met = True
    store.zoe_met = True
    store.zoe_properly_introduced = True
    store.knows_zoe_art_interest = True
    store.mc_knows_marcus_bball_offer = True
    store.marcus_lock_joke_active = False
    store.apartment_tier = 1
    store.tier_a_beat_last_day = {}
    store.bar_game_cooldowns = {}
    store.npc_last_seen = {}
    STAGE["marcus"] = STAGE["zoe"] = "friend"
    LIFE["marcus"] = LIFE["zoe"] = None
    INTERVIEW["open"] = False
    for k, v in kw.items():
        setattr(store, k, v)


print("A. Micro beats cannot be farmed")
reset()
first = pick("marcus")
chk("a micro is available at all", first is not None, first)
fired("marcus", "rc_m_micro_customer")
chk("no second micro the same day", pick("marcus") is None)
store.day += 4
chk("still nothing after 4 days (gap is 5)", pick("marcus") is None)
store.day += 1
chk("a DIFFERENT micro after 5 days", pick("marcus") is not None)
chk("the one that fired is not the one picked",
    pick("marcus") != "rc_marcus_micro_customer", pick("marcus"))
store.day += 40
chk("the same micro comes back after its 14-day cooldown",
    "rc_marcus_micro_customer" in [l for _i, l, _c in G["RC_MARCUS_MICRO"]]
    and G["_rc_micro_avail"]("rc_m_micro_customer"))

print("\nB. Micro beats never land on an authored scene")
reset(story_scene_active=True)
chk("no micro while story_scene_active", pick("marcus") is None)
chk("and none for Zoe either", pick("zoe") is None)

print("\nC. Micro eligibility is real, not decorative")
reset(current_loc="location_park")
chk("the bar-customer micro is bar-only",
    "rc_marcus_micro_customer" not in
    [l for i, l, c in G["RC_MARCUS_MICRO"] if c()])
reset(zoe_properly_introduced=False)
chk("Marcus never mentions a Zoe MC has not met",
    "rc_marcus_micro_zoe" not in
    [l for i, l, c in G["RC_MARCUS_MICRO"] if c()])
reset(mc_knows_marcus_bball_offer=False)
chk("Zoe never references a score MC has not heard about",
    "rc_zoe_micro_marcus" not in
    [l for i, l, c in G["RC_ZOE_MICRO"] if c()])
reset(marcus_lock_joke_active=True, apartment_tier=1)
chk("lock v3 stays locked until the apartment is upgraded",
    "rc_marcus_micro_lock" not in
    [l for i, l, c in G["RC_MARCUS_MICRO"] if c()])
reset(marcus_lock_joke_active=True, apartment_tier=2)
chk("lock v3 opens on apartment_tier 2",
    "rc_marcus_micro_lock" in
    [l for i, l, c in G["RC_MARCUS_MICRO"] if c()])
reset(marcus_lock_joke_active=False, apartment_tier=3)
chk("...but never if MC never took the lock branch",
    "rc_marcus_micro_lock" not in
    [l for i, l, c in G["RC_MARCUS_MICRO"] if c()])

print("\nD. Busy uses real schedule / life-state data")
reset(current_loc="location_bar", hour=19.0, day=30)   # 30 % 7 == 2, a weekday
STAGE["marcus"] = "acquaintance"
chk("Marcus is busy in his own bar on shift", m_busy())
store.hour = 12.0
chk("...but not before 16:00 on a weekday", not m_busy())
store.hour = 19.0
store.current_loc = "location_park"
chk("...and never outside the bar", not m_busy())
store.current_loc = "location_bar"
STAGE["marcus"] = "friend"
chk("...and never once you are a friend", not m_busy())
STAGE["marcus"] = "acquaintance"
chk("busy fires once, then not again that day", m_busy())
store.rc_marcus_busy_day = store.day
chk("second approach the same day is not blocked", not m_busy())

reset()
STAGE["zoe"] = "friendly"
chk("Zoe is not busy with no life state", not z_busy())
LIFE["zoe"] = "busy_work"
chk("Zoe is busy during client work", z_busy())
LIFE["zoe"] = "creative_project"
chk("...but not during an ordinary creative stretch", not z_busy())
LIFE["zoe"] = "stressed_week"
STAGE["zoe"] = "close"
chk("...and never once she is close", not z_busy())
STAGE["zoe"] = "known"
chk("...and never before she knows you", not z_busy())

print("\nE. Pre-Talk initiation")
reset()
chk("the shipping resolver still wins for everyone else",
    talk("nora") == "REAL")
chk("Marcus with nothing pending falls through", talk("marcus") is None)
INTERVIEW["open"] = True
store.marcus_interview_told_day = store.day - 2
chk("Marcus opens an unresolved interview himself",
    talk("marcus") == "marcus_ctx_interview", talk("marcus"))
store.marcus_interview_told_day = store.day
chk("...but not on the same day he was told", talk("marcus") is None)
INTERVIEW["open"] = False
store.marcus_interview_told_day = store.day - 2
chk("...and never once the state answered it", talk("marcus") is None)

reset()
chk("Zoe with nothing pending falls through", talk("zoe") is None)
store.zoe_deadline_submitted = True
store.zoe_deadline_day = store.day - 4
chk("Zoe opens the submission result herself",
    talk("zoe") == "zoe_talk_deadline_followup", talk("zoe"))
store.zoe_deadline_followup_done = True
chk("...once, and then not again", talk("zoe") is None)
store.zoe_second_opinion_done = True
store.zoe_second_opinion_choice = "structure"
store.zoe_second_opinion_day = store.day - 4
chk("Zoe opens the second-opinion result herself",
    talk("zoe") == "zoe_talk_second_opinion_callback", talk("zoe"))
store.zoe_second_opinion_day = store.day - 1
chk("...but not within 3 days of giving it", talk("zoe") is None)

print("\nF. Routine shorthand requires a real routine")
reset()
chk("\"Grounds?\" is locked at 0", not COND["zoe_msg_grounds_short"]())
store.zoe_grounds_count = 1
chk("...still locked at 1", not COND["zoe_msg_grounds_short"]())
store.zoe_grounds_count = 2
chk("...unlocked at 2", COND["zoe_msg_grounds_short"]())
chk("\"Static tonight?\" is locked at 0", not COND["marcus_msg_static_short"]())
store.marcus_bar_count = 2
chk("...unlocked at 2", COND["marcus_msg_static_short"]())
chk("both are registered into the shipping picker",
    "zoe_msg_grounds_short" in G["_INITIATIVE_VARIANTS"]["zoe"]
    and "marcus_msg_static_short" in G["_INITIATIVE_VARIANTS"]["marcus"])
chk("neither displaced an existing variant",
    "zoe_msg_x" in G["_INITIATIVE_VARIANTS"]["zoe"]
    and "marcus_msg_x" in G["_INITIATIVE_VARIANTS"]["marcus"])

print("\nG. Old-save backfill")
reset()
store.npc_last_seen = {"zoe": 25, "marcus": 27}
store.rc_zoe_last_seen_day = -999
store.marcus_last_seen_day = -999
store.rc_backfilled = False
backfill()
chk("a loaded save is not read as a five-day absence",
    store.rc_zoe_last_seen_day == 25 and store.marcus_last_seen_day == 27,
    (store.rc_zoe_last_seen_day, store.marcus_last_seen_day))
chk("routine counters stay at 0 with no evidence",
    store.zoe_grounds_count == 0 and store.marcus_bar_count == 0)
reset()
store.rc_backfilled = False
store.tier_a_beat_last_day = {"zoe_wednesday": 20}
store.bar_game_cooldowns = {"pool_marcus": 22}
backfill()
chk("...and get exactly ONE credit where there is evidence",
    store.zoe_grounds_count == 1 and store.marcus_bar_count == 1,
    (store.zoe_grounds_count, store.marcus_bar_count))
chk("credit is not enough to unlock the shorthand by itself",
    not COND["zoe_msg_grounds_short"]() and not COND["marcus_msg_static_short"]())
store.zoe_grounds_count = 99
backfill()
chk("backfill is idempotent and never lowers a counter",
    store.zoe_grounds_count == 99)
chk("the backfill is on after_load_callbacks, not a second after_load label",
    G["_rc_backfill"] in G["config"].after_load_callbacks
    and not re.search(r"^label\s+after_load\s*:", SRC, re.M))

print("\nH. Script integrity")
LABELS = set()
for fn in sorted(os.listdir(GAME)):
    if fn.endswith(".rpy"):
        LABELS.update(re.findall(
            r"^label\s+([\w.]+)\s*(?:\(.*?\))?\s*:",
            io.open(os.path.join(GAME, fn), encoding="utf-8").read(), re.M))
missing = [l for _i, l, _c in (G["RC_MARCUS_MICRO"] + G["RC_ZOE_MICRO"])
           if l not in LABELS]
chk("every micro label exists", not missing, missing)
missing = [l for l in ("rc_marcus_greet_pre", "rc_marcus_greet_post",
                       "rc_zoe_greet_pre", "rc_zoe_greet_post",
                       "rc_zoe_stage_greet", "zoe_farewell",
                       "rc_marcus_friction_push", "rc_marcus_friction_competitive",
                       "rc_marcus_repair", "rc_zoe_friction_reads_harsh",
                       "rc_zoe_friction_curt", "rc_zoe_repair",
                       "rc_continuity_test")
           if l not in LABELS]
chk("every hook and friction label exists", not missing, missing)
missing = [d["label"] for r in (G["_ZOE_GROUNDS_SHORT_RESP"],
                                G["_MARCUS_STATIC_SHORT_RESP"])
           for d in r if d["label"] not in LABELS]
chk("every shorthand reply label exists", not missing, missing)

IA = io.open(os.path.join(GAME, "interact.rpy"), encoding="utf-8").read()
chk("marcus_greet is bracketed, not rewritten",
    "call rc_marcus_greet_pre" in IA and "call rc_marcus_greet_post" in IA
    and 'm "Hey, neighbor."' in IA)
chk("zoe_greet routes to the stage ladder",
    "call rc_zoe_stage_greet" in IA)
chk("Zoe has a farewell hook in npc_interact",
    "call zoe_farewell" in IA)
chk("both farewells are once per day",
    "rc_marcus_farewell_day" in IA and "rc_zoe_farewell_day" in SRC)
chk("no new image or CG path is introduced",
    not re.search(r"^\s*(scene|show)\s+(?!screen|expression mf_sprite|zoe_street_neutral)",
                  SRC, re.M))
chk("nothing in the micro/friction pack writes relationship points",
    "apply_relationship_change" not in SRC and "_apply_trust" not in SRC)

print("\nI. Scene Tester pack")
# location_beats_selfcheck section G only execs the UNPRIORITISED `init python:`
# block of the debug file, so each pack validates its own init block here — the
# same split zoe_arc_selfcheck (init 1) and zoe_onboarding_selfcheck (init 2)
# already use. This pack is init 4.
DST = io.open(os.path.join(GAME, "debug_scene_tester.rpy"), encoding="utf-8").read()
D = dict(G)
D["SCENE_TEST_REGISTRY"] = {}
D["mark_npc_encountered"] = lambda n: None
D["set_npc_rel"] = lambda n, a, v: None
exec(init_block(4, DST), D)
REG = D["SCENE_TEST_REGISTRY"]
chk("the pack registers entries", bool(REG), len(REG))
bad = [k for k, e in REG.items()
       if not all(f in e for f in ("title", "category", "desc", "label",
                                   "presets", "reset"))]
chk("every entry has the required keys", not bad, bad)
bad = [k for k, e in REG.items() if e["category"] != "Relationship Scenes"]
chk("every entry is filed under Relationship Scenes", not bad, bad)
bad = [(k, e["label"]) for k, e in REG.items() if e["label"] not in LABELS]
chk("every entry label exists", not bad, bad)
bad = [k for k, e in REG.items()
       if not e["presets"] or not all(callable(f) for f in e["presets"].values())]
chk("every preset is callable", not bad, bad)
bad = [k for k, e in REG.items() if not callable(e["reset"])]
chk("every reset is callable", not bad, bad)
chk("gameplay files still do not name the debug registry",
    "SCENE_TEST_REGISTRY" not in SRC)

print("\n%d failure(s)" % len(FAILS))
for f in FAILS:
    print("  - " + f)
sys.exit(1 if FAILS else 0)
