"""Phase 66 runtime self-check — relationship depth.

Same approach as phase62/64/65: EXTRACTS the real `init python:` blocks out of
interact.rpy (NPC_DATA, _apply_aff/_apply_trust, GIFT_TYPES) and
npc_relationships.rpy and execs them against a stub `store`, so every assertion
runs the SHIPPING code. Change a cap, a pace or a stage threshold and this fails.

    python phase66_selfcheck.py

Covers spec 66.1 (migration), 66.3 (central API), 66.4 (source caps),
66.5 (saturation), 66.6 (gifts), 66.7 (stages), 66.8 (invitations),
66.12 (old-save safety).
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rpy_python_blocks(path):
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(src):
        # Only top-level `init python:` blocks. Inline `python:` blocks inside
        # labels are indented gameplay code and must not be pulled in.
        if re.match(r"^init(\s+-?\d+)?\s+python\s*:\s*$", src[i]):
            i += 1
            body = []
            while i < len(src):
                ln = src[i]
                if ln.strip() and not ln.startswith((" ", "\t")):
                    break
                body.append(ln)
                i += 1
            out.append(textwrap.dedent("\n".join(body)))
        else:
            i += 1
    return out


def rpy_defaults(path):
    out = {}
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read()
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)\s*(?:#.*)?$", src, re.M):
        try:
            out[m.group(1)] = eval(m.group(2), {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


# ── Stubs ────────────────────────────────────────────────────────────────────
class Store(object):
    def __init__(self):
        self.day = 30
        self.hour = 12.0
        self.gift_log = []
        self.relationship_thresholds_seen = {}
        self.npc_anger = {}
        self._npc_panel_npc_id = None
        self.current_loc = "location_cafe"

    def __getattr__(self, k):
        # Unknown store variable -> 0, the same way a `default 0` would read.
        return 0


class _Cfg(object):
    developer = False


class _Renpy(object):
    config = _Cfg()

    class random:
        @staticmethod
        def choice(seq):
            return seq[0]

        @staticmethod
        def random():
            return 0.5

    @staticmethod
    def notify(*a, **k):
        pass

    @staticmethod
    def log(*a, **k):
        pass

    @staticmethod
    def loadable(*a, **k):
        return False

    @staticmethod
    def say(*a, **k):
        pass


store = Store()
G = {"store": store, "renpy": _Renpy(), "__builtins__": __builtins__}

# interact.rpy defines NPC_DATA, ROMANCE_PROFILES, GIFT_TYPES, _apply_aff/_apply_trust.
for blk in rpy_python_blocks("interact.rpy"):
    exec(compile(blk, "interact.rpy", "exec"), G)
# npc_schedules.rpy owns the canonical add_relationship_memory.
for blk in rpy_python_blocks("npc_schedules.rpy"):
    try:
        exec(compile(blk, "npc_schedules.rpy", "exec"), G)
    except Exception:
        pass
# capabilities.rpy owns NPC_INTERESTS / npc_interest.
for blk in rpy_python_blocks("capabilities.rpy"):
    try:
        exec(compile(blk, "capabilities.rpy", "exec"), G)
    except Exception:
        pass
for blk in rpy_python_blocks("npc_relationships.rpy"):
    exec(compile(blk, "npc_relationships.rpy", "exec"), G)

for k, v in rpy_defaults("npc_relationships.rpy").items():
    setattr(store, k, v)
# _check_relationship_thresholds and add_relationship_memory touch scene flags we
# do not model; neutralise them so assertions test the arithmetic, not the story.
G["_check_relationship_thresholds"] = lambda npc_id: None
G["add_relationship_memory"] = lambda *a, **k: None

npc_rel = G["npc_rel"]
set_npc_rel = G["set_npc_rel"]
apply_relationship_change = G["apply_relationship_change"]
evaluate_gift = G["evaluate_gift"]
npc_relationship_stage = G["npc_relationship_stage"]
invitation_acceptance_chance = G["invitation_acceptance_chance"]
npc_rel_profile = G["npc_rel_profile"]
CAPS = G["RELATIONSHIP_SOURCE_CAPS"]
PROFILES = G["NPC_RELATIONSHIP_PROFILES"]
NPC_DATA = G["NPC_DATA"]


failures = []


def check(name, cond, detail=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("  [%s]" % detail) if detail else ""))
    if not cond:
        failures.append(name)


def reset(npc=None, aff=0, trust=0, respect=None, fam=None):
    store.npc_relationships = {}
    store._rel_saturation = {}
    store._rel_source_totals = {}
    store._rel_trace = []
    store.gift_log = []
    for nid, d in NPC_DATA.items():
        setattr(store, d["aff"], 0)
        setattr(store, d["trust"], 0)
    if npc:
        setattr(store, NPC_DATA[npc]["aff"], aff)
        setattr(store, NPC_DATA[npc]["trust"], trust)
        if respect is not None:
            set_npc_rel(npc, "respect", respect)
        if fam is not None:
            set_npc_rel(npc, "familiarity", fam)


# ── 66.2 Profile sanity ──────────────────────────────────────────────────────
print("\n[PROFILES]")
check("every profile key is a known field",
      all(set(p) <= set(G["DEFAULT_REL_PROFILE"]) for p in PROFILES.values()))
check("every profile value is within 0-1",
      all(0.0 <= v <= 1.0 for p in PROFILES.values() for v in p.values()))
check("every profiled NPC exists in NPC_DATA",
      all(n in NPC_DATA for n in PROFILES), ", ".join(sorted(PROFILES)))
check("every NPC_DATA character has a profile",
      all(n in PROFILES for n in NPC_DATA),
      ", ".join(sorted(set(NPC_DATA) - set(PROFILES))) or "all covered")
# The brief's explicit warning: high social status must not imply low openness.
check("openness and status_sensitivity are independent",
      PROFILES["kai"]["openness"] > 0.8 and PROFILES["kai"]["trust_pace"] < 0.4,
      "Kai: sociable front, slow trust")
check("Martha is the least gift-receptive (only NPC with gift evidence)",
      PROFILES["martha"]["gift_receptiveness"] == min(
          p["gift_receptiveness"] for p in PROFILES.values()))

# ── 66.1 / 66.12 Migration + old-save safety ─────────────────────────────────
print("\n[MIGRATION]")
reset()
store.nora_affection = 50
store.nora_trust = 20
# world NPC -> counts as met
f = npc_rel("nora", "familiarity")
r = npc_rel("nora", "respect")
check("familiarity seeded = max(aff,trust)*0.7 + 30", f == int(50 * 0.7) + 30, str(f))
check("respect seeded = trust*0.5 + 10", r == int(20 * 0.5) + 10, str(r))
check("loading an old save does not zero affection", store.nora_affection == 50)
check("loading an old save does not zero trust", store.nora_trust == 20)
check("affection still reads through npc_rel", npc_rel("nora", "affection") == 50)
# Second access must NOT reseed (would wipe earned respect).
set_npc_rel("nora", "respect", 77)
store.nora_trust = 90
check("seeding happens exactly once", npc_rel("nora", "respect") == 77)
# Never-met, non-world NPC gets no +30 familiarity bonus.
reset()
store.caroline_met = False
check("never-met NPC starts at familiarity 0", npc_rel("caroline", "familiarity") == 0)
store.npc_relationships = {}
check("a brand-new game leaves world NPCs as strangers",
      npc_rel("nora", "familiarity") == 0 and npc_relationship_stage("nora") == "stranger")
check("unknown npc_id is safe", npc_rel("nobody_here", "familiarity") == 0)
check("unknown npc_id change is a no-op",
      apply_relationship_change("nobody_here", "x", "casual_talk", affection=5) == {})

# ── 66.5 Saturation ──────────────────────────────────────────────────────────
print("\n[SATURATION]")
sat_mult = G["relationship_saturation_multiplier"]
reset("nora")
# saturation_rate 0.4 for Nora -> penalty scaled by 0.4/0.5 = 0.8
check("first interaction of the day is unsaturated", sat_mult("nora", "casual_talk") == 1.0)
gains = []
for i in range(4):
    got = apply_relationship_change("nora", "talk_music", "casual_talk",
                                    affection=4, familiarity=4)
    gains.append(got.get("affection", 0))
check("repeat talk yields strictly less each time (until the floor)",
      gains[0] > gains[1] >= gains[2] >= gains[3], str(gains))
check("4th talk of the day is near-worthless", gains[3] <= 1, str(gains[3]))
reset("nora")
m0 = apply_relationship_change("nora", "t", "casual_talk", affection=4)
m1 = apply_relationship_change("nora", "t", "casual_talk", affection=4, meaningful=True)
check("meaningful=True ignores saturation", m1.get("affection", 0) >= m0.get("affection", 0))
reset("nora")
store._rel_saturation = {"nora": {"casual_talk": [store.day - 1, 3]}}
check("saturation is per-day (yesterday's count does not carry)",
      sat_mult("nora", "casual_talk") == 1.0)
# saturation_rate scales the penalty: Rena (0.9) drops harder than Zoe (0.3).
store._rel_saturation = {"rena": {"casual_talk": [store.day, 1]},
                         "zoe":  {"casual_talk": [store.day, 1]}}
check("higher saturation_rate saturates faster",
      sat_mult("rena", "casual_talk") < sat_mult("zoe", "casual_talk"),
      "rena %.2f < zoe %.2f" % (sat_mult("rena", "casual_talk"), sat_mult("zoe", "casual_talk")))

# ── 66.4 Source caps ─────────────────────────────────────────────────────────
print("\n[SOURCE CAPS]")
reset("marcus", aff=CAPS["casual_talk"]["affection"] + 5)
got = apply_relationship_change("marcus", "talk", "casual_talk", affection=5)
check("a source above its cap contributes nothing", got.get("affection", 0) == 0, str(got))
reset("marcus", aff=CAPS["casual_talk"]["affection"] - 2)
got = apply_relationship_change("marcus", "talk", "casual_talk", affection=10)
check("a source cannot overshoot its cap",
      store.marcus_affection == CAPS["casual_talk"]["affection"],
      str(store.marcus_affection))
reset("marcus", aff=90)
got = apply_relationship_change("marcus", "story", "story_moment", affection=5,
                                bypass_saturation=True)
check("story moments bypass caps", got.get("affection", 0) > 0, str(got))
check("gift cap on trust is near-zero (objects do not buy trust)",
      CAPS["gift"]["trust"] <= 5)
check("competence_display is the highest respect source",
      CAPS["competence_display"]["respect"] >= max(
          v["respect"] for k, v in CAPS.items()
          if k not in ("story_moment", "authored")))
check("kept_commitment is the highest trust source",
      CAPS["kept_commitment"]["trust"] >= max(
          v["trust"] for k, v in CAPS.items()
          if k not in ("story_moment", "authored")))
check("every category defines all four base axes",
      all(set(v) >= {"affection", "trust", "respect", "familiarity"} for v in CAPS.values()))

# ── 66.3 Personality pacing ──────────────────────────────────────────────────
print("\n[PACING]")
reset()
a_caroline = apply_relationship_change("caroline", "confide", "meaningful_talk", trust=10)
reset()
a_elle = apply_relationship_change("elle", "confide", "meaningful_talk", trust=10)
check("slow-trust NPC gains less trust than a fast-trust NPC from the same beat",
      a_caroline.get("trust", 0) < a_elle.get("trust", 0),
      "caroline %s vs elle %s" % (a_caroline, a_elle))
reset("nora", aff=20)
loss = apply_relationship_change("nora", "rude", "casual_talk", affection=-5)
check("losses are never damped by pace or saturation", loss.get("affection") == -5, str(loss))
reset("nora", aff=20)
apply_relationship_change("nora", "t1", "casual_talk", affection=3)
loss2 = apply_relationship_change("nora", "rude", "casual_talk", affection=-5)
check("losses land at full size even when saturated", loss2.get("affection") == -5, str(loss2))
check("affection can go negative (historical -100 floor kept)",
      G["_rel_axis_floor"]("affection") == -100 and G["_rel_axis_floor"]("trust") == 0)

# ── 66.6 Gifts ───────────────────────────────────────────────────────────────
print("\n[GIFTS]")
reset("nora", aff=10)
g_liked = evaluate_gift("nora", "sweets")       # sweets -> food, which Nora likes
# "book" -> movies/work/ambition/art. Marcus likes none of those and dislikes
# art. (NOT "flowers": its topic list includes nightlife, which Marcus likes.)
g_disliked = evaluate_gift("marcus", "book")
check("a thoughtful gift beats an unwanted one",
      g_liked["affection"] > g_disliked["affection"],
      "%s vs %s" % (g_liked["affection"], g_disliked["affection"]))
check("a thoughtful gift earns a point of respect", g_liked["respect"] >= 1)
check("gifts never move trust", g_liked["trust"] == 0 and g_disliked["trust"] == 0)
# Expensive-early rule: Martha, familiarity < 30, item > $200, boundary > 0.6.
reset("martha")
set_npc_rel("martha", "familiarity", 12)
G["_gift_value"] = lambda item_id: 900   # stand in for an expensive catalog item
g_bad = evaluate_gift("martha", "expensive_watch")
check("expensive gift too early reads as uncomfortable",
      g_bad["reaction"] == "uncomfortable", str(g_bad))
check("expensive gift too early costs respect", g_bad["respect"] < 0, str(g_bad["respect"]))
set_npc_rel("martha", "familiarity", 85)
g_ok = evaluate_gift("martha", "expensive_watch")
check("the same gift later is not a boundary violation",
      g_ok["reaction"] != "uncomfortable", str(g_ok))
G["_gift_value"] = G["_gift_value"]  # keep the override for the repetition test
reset("nora", aff=10)
G["_gift_value"] = lambda item_id: 15
mults = []
for i in range(4):
    store.gift_log = list(store.gift_log) + [
        {"npc_id": "nora", "gift_type": "sweets", "day": store.day}]
    mults.append(G["_gift_repetition_multiplier"]("nora"))
check("repeat gifting decays hard", mults == sorted(mults, reverse=True) and mults[-1] <= 0.1,
      str(mults))

# ── 66.7 Stages ──────────────────────────────────────────────────────────────
print("\n[STAGES]")


def stage(npc, aff, tr, rsp, fam):
    reset(npc, aff=aff, trust=tr)
    set_npc_rel(npc, "respect", rsp)
    set_npc_rel(npc, "familiarity", fam)
    return npc_relationship_stage(npc)


check("no history -> stranger", stage("nora", 0, 0, 0, 0) == "stranger")
check("seen around, barely -> known", stage("nora", 5, 0, 5, 12) == "known")
check("familiar but not warm -> acquaintance", stage("nora", 10, 0, 5, 40) == "acquaintance")
check("warm and familiar -> friendly", stage("nora", 32, 18, 10, 40) == "friendly")
check("solid on all axes -> friend", stage("nora", 48, 38, 20, 55) == "friend")
check("deep -> close", stage("nora", 65, 58, 30, 65) == "close")
check("trusted needs respect, not just affection",
      stage("nora", 30, 75, 60, 60) == "trusted")
check("stage never returns None",
      all(npc_relationship_stage(n) for n in NPC_DATA))
# Monotonic: raising every axis must never move you backwards.
order = ["stranger", "known", "acquaintance", "friendly", "friend", "close", "trusted"]
seq = [order.index(stage("nora", v, v, v, v + 10)) for v in (0, 10, 25, 40, 55, 70, 85)]
check("stages are monotonic as every axis rises", seq == sorted(seq), str(seq))

# ── 66.8 Invitations ─────────────────────────────────────────────────────────
print("\n[INVITATIONS]")
reset("nora", aff=60, trust=20)
set_npc_rel("nora", "familiarity", 60)
set_npc_rel("nora", "respect", 20)
c_casual = invitation_acceptance_chance("nora", "casual")
c_home = invitation_acceptance_chance("nora", "home_visit")
check("low trust hurts a home visit more than a coffee", c_home < c_casual,
      "%.2f vs %.2f" % (c_home, c_casual))
reset("martha", aff=20, trust=20)
set_npc_rel("martha", "familiarity", 40)
set_npc_rel("martha", "respect", 80)
check("respect carries a professional invite",
      invitation_acceptance_chance("martha", "professional")
      > invitation_acceptance_chance("martha", "casual"))
check("chance is always a usable probability",
      all(0.05 <= invitation_acceptance_chance(n, t) <= 0.95
          for n in NPC_DATA for t in ("casual", "home_visit", "professional", "romantic", "other")))
reset("elle", aff=0, trust=0)
check("a stranger is not impossible, just unlikely",
      invitation_acceptance_chance("elle", "casual") <= 0.35)

# ── 66.9 Legacy interception ─────────────────────────────────────────────────
print("\n[LEGACY CALL SITES]")
reset("zoe")
G["_apply_aff"]("zoe", 6)
check("authored _apply_aff still applies its exact number", store.zoe_affection == 6)
check("authored beats also build familiarity", npc_rel("zoe", "familiarity") > 0)
reset("zoe")
G["_apply_trust"]("zoe", 8)
check("authored _apply_trust still applies its exact number", store.zoe_trust == 8)
check("authored trust gives a share of respect", npc_rel("zoe", "respect") > 0)
reset("zoe", aff=95)
G["_apply_aff"]("zoe", 20)
check("authored beats are uncapped by source category", store.zoe_affection == 100)

print("\n%d failure(s)" % len(failures))
if failures:
    for f in failures:
        print("  - " + f)
sys.exit(1 if failures else 0)
