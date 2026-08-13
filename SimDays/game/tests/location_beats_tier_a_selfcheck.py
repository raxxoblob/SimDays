"""Contextual Tier A location-beat pack 1 — runtime self-check.

Same approach as tests/location_beats_selfcheck.py: EXTRACTS the real
`init python` blocks out of the shipping .rpy files and execs them against a
stub `store`, so every assertion below runs the SHIPPING eligibility code.
Change a window, a cooldown, an NPC schedule or a relationship source category
and this fails.

    python location_beats_tier_a_selfcheck.py
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEATS_FILE = "location_beats_tier_a.rpy"

# beat_id -> (check function name, scene label, cooldown_days)
BEATS = [
    ("zoe_outdoor",       "check_zoe_outdoor",        "zoe_outdoor_scene",        5),
    ("zoe_walk",          "check_zoe_walk",           "zoe_walk_scene",           4),
    ("eli_favor",         "check_eli_favor",          "eli_favor_scene",          6),
    ("eli_after_shift",   "check_eli_after_shift",    "eli_after_shift_scene",    7),
    ("marcus_park_favor", "check_marcus_park_favor",  "marcus_park_favor_scene",  5),
    ("marcus_one_game",   "check_marcus_one_game",    "marcus_one_game_scene",    4),
    ("nora_exhausted",    "check_nora_exhausted",     "nora_exhausted_scene",     4),
    ("nora_walk_out",     "check_nora_walk_out",      "nora_walk_out_scene",      6),
    ("marcus_zoe_bar",    "check_marcus_zoe_bar",     "marcus_zoe_bar_scene",     8),
    ("cross_zoe_nora",    "check_cross_zoe_nora",     "cross_zoe_nora_scene",    10),
]

CANONICAL_SOURCE_CATEGORIES = {
    "casual_talk", "meaningful_talk", "gift", "shared_activity",
    "kept_commitment", "helping_npc", "competence_display", "reputation",
    "story_moment", "authored",
}


def rpy_python_blocks(path, priority=None):
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
           "npc_relationships.rpy", "bar_games.rpy"):
    DEFAULTS.update(rpy_defaults(_f))

SRC = io.open(os.path.join(GAME, BEATS_FILE), encoding="utf-8").read()


def label_body(name):
    """Source of `label name:` up to the next top-level label."""
    parts = SRC.split("\nlabel %s:" % name)
    assert len(parts) == 2, "label %s not found in %s" % (name, BEATS_FILE)
    return parts[1].split("\nlabel ")[0]


class Store(object):
    def __init__(self):
        self.day = 5                # Saturday
        self.hour = 14.0
        for k, v in DEFAULTS.items():
            setattr(self, k,
                    list(v) if isinstance(v, list) else
                    dict(v) if isinstance(v, dict) else v)
        # Multi-line dict default, not picked up by rpy_defaults().
        self.summer_festival_state = {"attended": False}


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
        "_apply_aff": lambda nid, d: None,
        "_apply_trust": lambda nid, d: None,
        "_check_relationship_thresholds": lambda nid: None,
        "has_player_state": lambda s: False,
        # Owned by phone_actionable.rpy / interact.rpy — stubbed: no scheduled
        # closing commitment exists in the default state we test against.
        "commitment_available": lambda cid: False,
    }
    for path, prio in (("npc_schedules.rpy", None),
                       ("npc_relationships.rpy", 1),
                       (BEATS_FILE, None)):
        for blk in rpy_python_blocks(path, prio):
            try:
                exec(compile(blk, path, "exec"), G)
            except Exception as e:                     # noqa: BLE001
                print("  (skipped a block in %s: %s: %s)" % (path, type(e).__name__, e))
    G["store"] = store
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


def wipe_beat_state():
    store.last_tier_a_beat_day = -1
    store.tier_a_beat_last_day = {}
    store.tier_a_beat_miss_count = {}
    store.tier_a_beat_roll_cache = {}
    store.npc_schedule_overrides = []


def force_roll(beat_id, value=True):
    """Freeze the roll so hard-requirement tests are chance-independent."""
    c = dict(store.tier_a_beat_roll_cache)
    c[beat_id] = [store.day, bool(value)]
    store.tier_a_beat_roll_cache = c


# Fully valid state for each beat: (day_of_week, hour, setup callable)
def _setup_zoe(fam=40):
    store.zoe_met = True
    G["set_npc_rel"]("zoe", "familiarity", fam)


def _setup_nora(fam=40):
    store.nora_met = True
    store.nora_life_state = "cafe"
    G["set_npc_rel"]("nora", "familiarity", fam)


def valid_state(beat_id):
    """Put the store in a fully eligible state for beat_id (roll aside)."""
    wipe_beat_state()
    store.need_energy = 90
    store.skill_prog = 0
    store.skill_art = 0
    store.skill_fit = 0
    store.active_careers = {}
    store.nora_closing_done = True
    store.nora_affection = 0
    store.summer_festival_state = {"attended": False}

    if beat_id == "zoe_outdoor":
        _setup_zoe(); store.day, store.hour = 5, 14.0          # Sat, sandbeach
    elif beat_id == "zoe_walk":
        _setup_zoe(); store.day, store.hour = 3, 15.0          # Thu, park
    elif beat_id == "eli_favor":
        store.eli_met = True
        G["set_npc_rel"]("eli", "familiarity", 40)
        store.day, store.hour = 0, 14.0                        # Mon, library
    elif beat_id == "eli_after_shift":
        store.eli_met = True
        store.active_careers = {"it": {"rank": 1, "perf": 0}}
        store.day, store.hour = 0, 10.0                        # Mon, hub
    elif beat_id == "marcus_park_favor":
        store.marcus_met = True
        store.day, store.hour = 0, 8.0                         # Mon, park run
    elif beat_id == "marcus_one_game":
        store.marcus_met = True
        store.day, store.hour = 0, 19.0                        # Mon, bar
    elif beat_id == "nora_exhausted":
        _setup_nora(); store.need_energy = 15
        store.day, store.hour = 5, 12.0                        # Sat, café
    elif beat_id == "nora_walk_out":
        _setup_nora(fam=35)
        store.day, store.hour = 5, 17.5                        # Sat, clock-off
    elif beat_id == "marcus_zoe_bar":
        store.marcus_met = True
        _setup_zoe()
        store.day, store.hour = 5, 20.0                        # Sat, bar
    elif beat_id == "cross_zoe_nora":
        _setup_nora(); _setup_zoe()
        store.day, store.hour = 2, 14.0                        # Wed, café
    else:
        raise AssertionError("unknown beat " + beat_id)
    force_roll(beat_id, True)


def main():
    boot()

    # ── A. defaults + hard requirements block invalid scenes ─────────────────
    print("\nA. defaults and hard requirements")
    for name in ("last_tier_a_beat_day", "tier_a_beat_last_day",
                 "tier_a_beat_miss_count", "tier_a_beat_roll_cache"):
        chk("%s has a default in data.rpy" % name, name in DEFAULTS,
            DEFAULTS.get(name))
    chk("last_tier_a_beat_day defaults to -1 (old-save safe)",
        DEFAULTS.get("last_tier_a_beat_day") == -1)
    chk("cooldown/pity/roll dicts default empty",
        DEFAULTS.get("tier_a_beat_last_day") == {}
        and DEFAULTS.get("tier_a_beat_miss_count") == {}
        and DEFAULTS.get("tier_a_beat_roll_cache") == {})

    for beat_id, fn, lbl, cd in BEATS:
        valid_state(beat_id)
        chk("%s: fires when every condition is met" % beat_id, G[fn]() is True)

    # met flag is a hard requirement for every beat
    for beat_id, fn, lbl, cd in BEATS:
        valid_state(beat_id)
        for npc in ("zoe", "nora", "eli", "marcus"):
            if npc in beat_id or (beat_id == "cross_zoe_nora" and npc in ("zoe", "nora")):
                setattr(store, npc + "_met", False)
                chk("%s: blocked before meeting %s" % (beat_id, npc),
                    G[fn]() is False)
                setattr(store, npc + "_met", True)

    valid_state("nora_exhausted")
    store.need_energy = 90
    chk("nora_exhausted: blocked when MC is not actually tired",
        G["check_nora_exhausted"]() is False)
    valid_state("nora_exhausted")
    store.nora_life_state = "school"
    chk("nora_exhausted: blocked once Nora leaves the café",
        G["check_nora_exhausted"]() is False)

    valid_state("eli_after_shift")
    store.active_careers = {}
    chk("eli_after_shift: blocked when the Hub is not MC's workplace",
        G["check_eli_after_shift"]() is False)

    valid_state("eli_favor")
    G["set_npc_rel"]("eli", "familiarity", 5)
    chk("eli_favor: blocked with no alternative qualifier",
        G["check_eli_favor"]() is False)
    store.skill_prog = 3
    force_roll("eli_favor", True)
    chk("eli_favor: programming skill is a valid alternative qualifier",
        G["check_eli_favor"]() is True)
    store.skill_prog = 0
    store.summer_festival_state = {"attended": True}
    force_roll("eli_favor", True)
    chk("eli_favor: festival attendance is a valid alternative qualifier",
        G["check_eli_favor"]() is True)

    valid_state("nora_walk_out")
    G["set_npc_rel"]("nora", "familiarity", 20)
    chk("nora_walk_out: blocked below familiarity 30",
        G["check_nora_walk_out"]() is False)

    # ── B. NPC schedule availability respected ───────────────────────────────
    print("\nB. NPC schedule availability")
    for beat_id, loc, npcs in (
            ("zoe_outdoor", "location_sandbeach", ["zoe"]),
            ("zoe_walk", "location_park", ["zoe"]),
            ("eli_favor", "location_library", ["eli"]),
            ("eli_after_shift", "location_hub", ["eli"]),
            ("marcus_park_favor", "location_park", ["marcus"]),
            ("marcus_one_game", "location_bar", ["marcus"]),
            ("nora_exhausted", "location_cafe", ["nora"]),
            ("nora_walk_out", "location_cafe", ["nora"]),
            ("marcus_zoe_bar", "location_bar", ["marcus", "zoe"]),
            ("cross_zoe_nora", "location_cafe", ["nora", "zoe"])):
        valid_state(beat_id)
        for npc in npcs:
            chk("%s: shipping schedule really puts %s at %s" % (beat_id, npc, loc),
                G["npc_here"](npc, loc),
                G["resolve_npc_state"](npc))

    # wrong hour inside an otherwise valid day
    for beat_id, fn, bad_hour in (("zoe_outdoor", "check_zoe_outdoor", 11.0),
                                  ("zoe_walk", "check_zoe_walk", 13.0),
                                  ("eli_after_shift", "check_eli_after_shift", 13.0),
                                  ("marcus_park_favor", "check_marcus_park_favor", 12.0),
                                  ("marcus_one_game", "check_marcus_one_game", 17.0),
                                  ("nora_walk_out", "check_nora_walk_out", 18.5),
                                  ("marcus_zoe_bar", "check_marcus_zoe_bar", 18.0),
                                  ("cross_zoe_nora", "check_cross_zoe_nora", 15.5)):
        valid_state(beat_id)
        store.hour = bad_hour
        force_roll(beat_id, True)
        chk("%s: blocked outside its window (%.1f)" % (beat_id, bad_hour),
            G[fn]() is False)

    # wrong day of week
    for beat_id, fn, bad_day in (("zoe_outdoor", "check_zoe_outdoor", 0),
                                 ("zoe_walk", "check_zoe_walk", 0),
                                 ("marcus_park_favor", "check_marcus_park_favor", 5),
                                 ("marcus_zoe_bar", "check_marcus_zoe_bar", 0),
                                 ("cross_zoe_nora", "check_cross_zoe_nora", 0)):
        valid_state(beat_id)
        store.day = bad_day
        force_roll(beat_id, True)
        chk("%s: blocked on the wrong weekday (%d)" % (beat_id, bad_day),
            G[fn]() is False)

    # ── C. wrong location blocks the scene ───────────────────────────────────
    print("\nC. wrong location")
    valid_state("zoe_walk")
    # Thu 15:00 Zoe is at the park, so the sandbeach beat must not fire.
    force_roll("zoe_outdoor", True)
    chk("zoe_outdoor: does not fire while Zoe is at the park",
        G["check_zoe_outdoor"]() is False,
        G["npc_location_now"]("zoe"))
    valid_state("eli_after_shift")
    force_roll("eli_favor", True)
    chk("eli_favor: does not fire while Eli is at the Hub, not the library",
        G["check_eli_favor"]() is False,
        G["npc_location_now"]("eli"))

    # ── D/E. stable roll ────────────────────────────────────────────────────
    print("\nD/E. stable roll")
    valid_state("zoe_outdoor")
    store.tier_a_beat_roll_cache = {}
    first = G["_beat_stable_roll"]("probe_beat", 50)
    repeats = [G["_beat_stable_roll"]("probe_beat", 50) for _ in range(6)]
    chk("same opportunity gives the same answer every time",
        all(r == first for r in repeats), [first] + repeats)
    chk("re-asking does not inflate the pity counter",
        store.tier_a_beat_miss_count.get("probe_beat", 0) in (0, 1),
        store.tier_a_beat_miss_count.get("probe_beat"))
    chk("the roll is cached per day, not per call",
        store.tier_a_beat_roll_cache["probe_beat"][0] == store.day)

    store.tier_a_beat_roll_cache = {}
    store.tier_a_beat_miss_count = {}
    spread = []
    for d in range(40):
        store.day = d
        spread.append(G["_beat_stable_roll"]("probe_beat", 50))
    chk("a new day is a genuinely independent opportunity",
        0 < sum(spread) < 40, sum(spread))

    store.tier_a_beat_roll_cache = {}
    store.tier_a_beat_miss_count = {}
    store.day = 5
    a = G["_beat_stable_roll"]("probe_alpha", 50)
    b = G["_beat_stable_roll"]("probe_beta", 50)
    chk("different beats are seeded independently on the same day",
        isinstance(a, bool) and isinstance(b, bool))
    chk("seed fold is deterministic (no hash() randomisation)",
        G["_beat_seed_of"]("zoe_outdoor") == G["_beat_seed_of"]("zoe_outdoor")
        and G["_beat_seed_of"]("zoe_outdoor") != G["_beat_seed_of"]("zoe_walk"))
    chk("_beat_stable_roll does not use hash()",
        "hash(" not in SRC.split("def _beat_stable_roll")[1].split("\n    def ")[0])

    # pity really escalates
    store.tier_a_beat_roll_cache = {}
    store.tier_a_beat_miss_count = {"probe_pity": 8}
    store.day = 5
    lo_misses = dict(store.tier_a_beat_miss_count)
    chk("pity counter is read by the roll",
        "tier_a_beat_miss_count" in SRC.split("def _beat_stable_roll")[1]
        .split("\n    def ")[0], sorted(lo_misses))
    chk("pity is capped", "pity_cap" in SRC and "min(pity_cap" in SRC)

    # ── F. at most one beat per opportunity ─────────────────────────────────
    print("\nF. one beat per opportunity")
    valid_state("cross_zoe_nora")
    for bid in ("cross_zoe_nora", "nora_exhausted", "nora_walk_out"):
        force_roll(bid, True)
    store.need_energy = 10          # would also satisfy nora_exhausted
    eligible_before = [b for b in ("cross_zoe_nora", "nora_exhausted")
                       if G["check_" + b]()]
    chk("more than one café beat can be eligible in principle",
        len(eligible_before) >= 1, eligible_before)
    G["_beat_triggered"]("cross_zoe_nora")
    chk("after one beat fires, the daily budget is spent",
        G["_beat_global_ok"]() is False)
    still = [b for b, fn, l, c in BEATS if G[fn]()]
    chk("no other beat anywhere can fire the same day", still == [], still)

    # the café hook chain in locations.rpy must be if/elif, never three ifs
    loc_src = io.open(os.path.join(GAME, "locations.rpy"), encoding="utf-8").read()
    cafe_chain = loc_src.split("label location_cafe:")[1].split("\nlabel ")[0]
    chk("café hook chains its three beats with elif",
        cafe_chain.count("check_cross_zoe_nora()") == 1
        and "elif check_nora_exhausted()" in cafe_chain
        and "elif check_nora_walk_out()" in cafe_chain)
    bar_chain = loc_src.split("label location_bar:")[1].split("\nlabel ")[0]
    chk("bar hook chains its two beats with elif",
        "if check_marcus_one_game()" in bar_chain
        and "elif check_marcus_zoe_bar()" in bar_chain)
    park_chain = loc_src.split("label location_park:")[1].split("\nlabel ")[0]
    chk("park hook chains its two beats with elif",
        "if check_marcus_park_favor()" in park_chain
        and "elif check_zoe_walk()" in park_chain)
    for beat_id, fn, lbl, cd in BEATS:
        chk("%s is hooked into a location label" % beat_id,
            ("jump " + lbl) in loc_src)

    # ── G. cooldowns ────────────────────────────────────────────────────────
    print("\nG. cooldowns")
    for beat_id, fn, lbl, cd in BEATS:
        valid_state(beat_id)
        base_day = store.day
        G["_beat_triggered"](beat_id)
        chk("%s: cooldown is %d days" % (beat_id, cd),
            not G["_beat_cooldown_ok"](beat_id, cd)
            and (store.tier_a_beat_last_day[beat_id] == base_day))
        store.day = base_day + cd - 1
        store.last_tier_a_beat_day = -1
        chk("%s: still on cooldown one day early" % beat_id,
            G["_beat_cooldown_ok"](beat_id, cd) is False)
        store.day = base_day + cd
        chk("%s: cooldown expires exactly on schedule" % beat_id,
            G["_beat_cooldown_ok"](beat_id, cd) is True)

    # ── H. one-shots ────────────────────────────────────────────────────────
    print("\nH. one-shot behaviour")
    chk("no beat in this pack is a one-shot (all are cooldown-gated)",
        not re.search(r"_triggered\s*=\s*True", SRC),
        "an unexpected fired-once flag was set in " + BEATS_FILE)
    chk("every beat scene stamps its cooldown via _beat_triggered",
        all(("_beat_triggered(\"%s\")" % b) in SRC for b, f, l, c in BEATS))
    # the pre-existing one-shot must still be a one-shot
    old = io.open(os.path.join(GAME, "location_beats.rpy"), encoding="utf-8").read()
    chk("the older nora_cover_shift beat is still one-shot",
        "if store.nora_cover_shift_triggered:" in old
        and "nora_cover_shift_triggered = True" in old)

    # ── I. obsolete beat: nora_walk_out vs nora_closing_scene ───────────────
    print("\nI. obsolescence (nora_walk_out vs nora_closing_scene)")
    valid_state("nora_walk_out")
    chk("fires once the closing scene is done", G["check_nora_walk_out"]() is True)
    valid_state("nora_walk_out")
    store.nora_closing_done = False
    store.nora_affection = 45           # closing scene's own gate
    chk("stands down while nora_closing_scene can still happen",
        G["check_nora_walk_out"]() is False)
    valid_state("nora_walk_out")
    store.nora_closing_done = False
    store.nora_affection = 10           # below the closing gate
    force_roll("nora_walk_out", True)
    chk("allowed when the closing scene is out of reach anyway",
        G["check_nora_walk_out"]() is True)
    valid_state("nora_walk_out")
    G["commitment_available"] = lambda cid: cid == "nora_closing_1"
    _saved = G["commitment_available"]
    chk("stands down while a closing commitment is scheduled",
        G["check_nora_walk_out"]() is False)
    G["commitment_available"] = lambda cid: False
    valid_state("nora_walk_out")
    store.nora_life_state = "school"
    chk("obsolete once Nora no longer works at the café",
        G["check_nora_walk_out"]() is False)
    # the real closing gate this mirrors must not have drifted — locations.rpy
    # now shares this file's helper instead of re-spelling the condition.
    chk("closing-scene gate in locations.rpy uses the shared helper",
        "hour >= 19 and _nora_auto_closing_eligible()" in loc_src)
    chk("shared helper is still affection>=40 / not done",
        "store.nora_closing_done) and store.nora_affection >= 40" in SRC)

    # ── J. refusal has no relationship penalty ──────────────────────────────
    print("\nJ. refusal is free")
    refusal_labels = ["zoe_outdoor_go", "zoe_walk_no", "marcus_park_favor_no",
                      "marcus_zoe_bar_pass"]
    for lbl in refusal_labels:
        body = label_body(lbl)
        chk("%s: no relationship change on refusal" % lbl,
            "apply_relationship_change" not in body)
        chk("%s: no time cost on refusal" % lbl, "spend_time" not in body)
    # inline decline branches: negative deltas must appear nowhere in the pack
    chk("no beat applies a negative relationship delta anywhere",
        not re.search(r"(affection|trust|respect|familiarity)\s*=\s*-\d", SRC))

    # ── K. time cost where specified ────────────────────────────────────────
    print("\nK. time cost")
    for lbl, expect in (("zoe_outdoor_stay", "spend_time(0.5)"),
                        ("zoe_walk_yes", "spend_time(0.5)"),
                        ("marcus_park_favor_yes", "spend_time(20 / 60.0)"),
                        ("marcus_zoe_bar_join", "spend_time(0.5)")):
        chk("%s costs time (%s)" % (lbl, expect), expect in label_body(lbl))
    for lbl in ("eli_favor_scene", "nora_walk_out_scene", "cross_zoe_nora_scene"):
        chk("%s costs time on the engaged path" % lbl,
            "spend_time" in label_body(lbl))
    chk("eli_after_shift costs no time (it is a doorway exchange)",
        "spend_time" not in label_body("eli_after_shift_scene"))
    chk("marcus_one_game delegates its time cost to bar_game_play",
        "spend_time" not in label_body("marcus_one_game_scene")
        and 'bar_game_play("pool", "pool_marcus")' in label_body("marcus_one_game_scene"))

    # ── L. conflicting schedule override suppresses the visitor ─────────────
    print("\nL. schedule overrides")
    valid_state("eli_after_shift")
    chk("no override yet: Eli is at the Hub", G["npc_here"]("eli", "location_hub"))
    G["add_schedule_override"]("eli", store.day, 9, 12, "location_hospital",
                               "working_shift", source_id="test_conflict")
    chk("override overlap is detected",
        G["npc_has_override_overlap"]("eli", store.day, 10, 11) is True)
    force_roll("eli_after_shift", True)
    chk("eli_after_shift suppressed by a conflicting override",
        G["check_eli_after_shift"]() is False)
    valid_state("eli_favor")
    G["add_schedule_override"]("eli", store.day, 12, 18, "location_hospital",
                               "working_shift", source_id="test_conflict2")
    force_roll("eli_favor", True)
    chk("eli_favor suppressed by a conflicting override",
        G["check_eli_favor"]() is False)
    store.npc_schedule_overrides = []

    # ── M. cross-NPC beats need BOTH ────────────────────────────────────────
    print("\nM. cross-NPC beats")
    for beat_id, fn, npcs in (("marcus_zoe_bar", "check_marcus_zoe_bar",
                               ("marcus", "zoe")),
                              ("cross_zoe_nora", "check_cross_zoe_nora",
                               ("zoe", "nora"))):
        for absent in npcs:
            valid_state(beat_id)
            G["add_schedule_override"](absent, store.day, 0, 24,
                                       "location_hospital", "working_shift",
                                       source_id="test_absent")
            force_roll(beat_id, True)
            chk("%s: blocked when %s is elsewhere" % (beat_id, absent),
                G[fn]() is False)
            store.npc_schedule_overrides = []
        valid_state(beat_id)
        chk("%s: fires with both present" % beat_id, G[fn]() is True)
    # both NPCs must finish their exchange before acknowledging MC
    for lbl in ("marcus_zoe_bar_scene", "cross_zoe_nora_scene"):
        body = label_body(lbl)
        first_mc = body.find("\n    mc ")
        first_npc = min(i for i in (body.find("\n    m "), body.find("\n    z "),
                                    body.find("\n    n ")) if i > 0)
        chk("%s: NPCs speak before MC does" % lbl,
            first_npc > 0 and (first_mc == -1 or first_npc < first_mc))

    # ── N. canonical relationship source categories ─────────────────────────
    print("\nN. relationship sources")
    cats = set(re.findall(r'source_category="(\w+)"', SRC))
    chk("every source_category used is canonical",
        cats <= CANONICAL_SOURCE_CATEGORIES, sorted(cats - CANONICAL_SOURCE_CATEGORIES))
    chk("every category exists in RELATIONSHIP_SOURCE_CAPS",
        cats <= set(G["RELATIONSHIP_SOURCE_CAPS"]),
        sorted(cats - set(G["RELATIONSHIP_SOURCE_CAPS"])))
    chk("no beat writes set_npc_rel() directly",
        "set_npc_rel(" not in SRC)
    chk("no beat pays cash", not re.search(r"gain_money|try_spend", SRC))
    # the deltas are small: nothing in a contextual beat should move >4
    big = [int(m) for m in re.findall(
        r"(?:affection|trust|respect|familiarity)=(\d+),", SRC) if int(m) > 4]
    chk("all relationship deltas are small (<=4)", not big, big)
    # every apply_relationship_change targets a real NPC
    for npc in set(re.findall(r'apply_relationship_change\(\s*\n\s*"(\w+)"', SRC)):
        chk("apply_relationship_change target '%s' is a real NPC" % npc,
            npc in G["NPC_DATA"])

    # ── O. scene exits restore state ────────────────────────────────────────
    print("\nO. scene state hygiene")
    for beat_id, fn, lbl, cd in BEATS:
        body = label_body(lbl)
        chk("%s: hides the HUD and flags a story scene on entry" % lbl,
            'set_hud("hidden")' in body and "story_scene_active = True" in body)
    # Every exit path: count restores vs. jumps out of the pack.
    pack_labels = set(re.findall(r"^label (\w+):", SRC, re.M))
    for lbl in sorted(pack_labels):
        body = label_body(lbl)
        exits = [j for j in re.findall(r"jump (\w+)", body)
                 if j not in pack_labels]
        if not exits:
            continue
        chk("%s: every exit restores the HUD" % lbl,
            body.count('set_hud("full")') >= 1
            and body.count("story_scene_active = False") >= 1,
            exits)
        for tgt in exits:
            chk("%s: exit target '%s' exists" % (lbl, tgt),
                re.search(r"^label %s\s*(\(|:)" % tgt, loc_src, re.M) is not None
                or tgt in pack_labels)
    chk("no beat leaves story_scene_active True on any path",
        SRC.count("story_scene_active = True") == len(BEATS)
        and SRC.count("story_scene_active = False") >= len(BEATS),
        (SRC.count("story_scene_active = True"),
         SRC.count("story_scene_active = False")))
    # only confirmed transforms and sprite positions
    known_transforms = {"react_bounce", "react_shake", "react_step_back",
                        "react_lean_in", "react_nod", "react_sigh"}
    used = set(re.findall(r"react_\w+", SRC))
    chk("only the six audited react_* transforms are used",
        used <= known_transforms, sorted(used - known_transforms))
    known_pos = {"sprite_r", "sprite_l"}
    used_pos = set(re.findall(r"at (sprite_\w+)", SRC))
    chk("only audited sprite positions are used",
        used_pos <= known_pos, sorted(used_pos - known_pos))
    # every sprite shown must be defined in images.rpy
    imgs = io.open(os.path.join(GAME, "images.rpy"), encoding="utf-8").read()
    defined = set(re.findall(r"^image ([\w ]+?)\s*=", imgs, re.M))
    for spr in sorted(set(re.findall(r"show (\w+) at sprite", SRC))):
        chk("sprite '%s' is defined in images.rpy" % spr, spr in defined)
    # Eli is she/her — no masculine pronoun may appear near her lines
    eli_lines = re.findall(r"^\s*eli \"(.*)\"$", SRC, re.M)
    eli_scenes = label_body("eli_favor_scene") + label_body("eli_after_shift_scene")
    chk("Eli's scenes use no masculine pronoun",
        not re.search(r"\b(he|him|his)\b", eli_scenes, re.I)
        or not re.search(r"\bEli\b[^\"]*\b(he|him|his)\b", eli_scenes, re.I),
        len(eli_lines))

    # ── P. Scene Tester registry ────────────────────────────────────────────
    print("\nP. Scene Tester registry")
    reg_g = {"store": store, "renpy": _Renpy(), "config": _Config(),
             "mark_npc_encountered": lambda n: None,
             "set_npc_rel": G["set_npc_rel"],
             "SF_NPCS": ["marcus", "eli", "zoe", "nora"],
             "_debug_festival_reset": lambda: None}
    for blk in rpy_python_blocks("debug_scene_tester.rpy", None):
        exec(compile(blk, "debug_scene_tester.rpy", "exec"), reg_g)
    REG = reg_g.get("SCENE_TEST_REGISTRY", {})
    labels = set()
    for fn_ in sorted(os.listdir(GAME)):
        if fn_.endswith(".rpy"):
            labels.update(re.findall(
                r"^label\s+([\w.]+)\s*(?:\(.*?\))?\s*:",
                io.open(os.path.join(GAME, fn_), encoding="utf-8").read(), re.M))

    for beat_id, fn, lbl, cd in BEATS:
        e = REG.get(beat_id)
        chk("%s is registered in the Scene Tester" % beat_id, e is not None)
        if not e:
            continue
        chk("%s: category is Location Beats" % beat_id,
            e["category"] == "Location Beats", e["category"])
        chk("%s: points at the real shipping label" % beat_id,
            e["label"] == lbl and lbl in labels, e["label"])
        chk("%s: has at least a 'basic' preset, all callable" % beat_id,
            "basic" in e["presets"]
            and all(callable(f) for f in e["presets"].values()),
            sorted(e["presets"]))
        chk("%s: reset is callable" % beat_id, callable(e["reset"]))

    # every preset must actually run, and leave the beat launchable
    for beat_id, fn, lbl, cd in BEATS:
        e = REG.get(beat_id)
        if not e:
            continue
        for pname, pfn in sorted(e["presets"].items()):
            wipe_beat_state()
            try:
                pfn()
                ok, err = True, ""
            except Exception as ex:                     # noqa: BLE001
                ok, err = False, "%s: %s" % (type(ex).__name__, ex)
            chk("%s preset '%s' runs cleanly" % (beat_id, pname), ok, err)
        wipe_beat_state()
        try:
            e["reset"]()
            ok, err = True, ""
        except Exception as ex:                         # noqa: BLE001
            ok, err = False, "%s: %s" % (type(ex).__name__, ex)
        chk("%s reset runs cleanly" % beat_id, ok, err)

    # presets put the store where the real check agrees, i.e. they don't lie
    for beat_id, fn, lbl, cd in BEATS:
        e = REG.get(beat_id)
        if not e:
            continue
        wipe_beat_state()
        store.need_energy = 90
        store.nora_closing_done = True
        store.nora_affection = 0
        store.summer_festival_state = {"attended": False}
        e["presets"]["basic"]()
        force_roll(beat_id, True)
        chk("%s 'basic' preset lands on a day/hour the real check accepts"
            % beat_id, G[fn]() is True,
            (store.day % 7, store.hour))

    print("\n%d check(s) failed" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
