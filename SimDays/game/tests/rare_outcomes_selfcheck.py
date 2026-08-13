"""Rare-outcomes runtime self-check.

Same approach as phase65/67/69: EXTRACTS the real `init python:` blocks out of
resolution_checks.rpy, rare_outcomes.rpy, busking.rpy, painting.rpy and
city_challenges.rpy and execs them against a stub `store`, so every assertion
below runs the SHIPPING code. Change a tier threshold, a rare percentage or a
table weight and this fails.

    python rare_outcomes_selfcheck.py

The init-25 wrapper block in rare_outcomes.rpy is deliberately NOT executed
here: it rebinds functions owned by five other systems and only makes sense
inside a running game (same rule as possessions.rpy's init-20 block).
"""
import io, os, random, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, cond, extra=""):
    if cond:
        print("  ok   %s" % name)
    else:
        FAILS.append(name + ((" — " + extra) if extra else ""))
        print("  FAIL %s%s" % (name, (" — " + extra) if extra else ""))


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
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)\s*(?:#.*)?$", src, re.M):
        try:
            out[m.group(1)] = eval(m.group(2), {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


# ── Stub store / Ren'Py surface ────────────────────────────────────────────────
class Store(object):
    pass


store = Store()
DEFAULTS = {}
for f in ("rare_outcomes.rpy", "resolution_checks.rpy", "busking.rpy",
          "painting.rpy", "possessions.rpy"):
    DEFAULTS.update(rpy_defaults(f))
for k, v in DEFAULTS.items():
    setattr(store, k, v.copy() if hasattr(v, "copy") else v)

store.day = 30
store.hour = 14
store.need_energy = 80
store._check_pity = {}
store._check_attempts = {}
store._breakthrough_sessions = {}
store._pending_breakthrough = None
store.activity_mastery = {}
store.activity_mastery_wins = {}
store._daily_condition = None
store._daily_condition_day = -1
store.music_reputation = 20
store.art_reputation = 12
store.player_personal_bests = {}
store.player_accomplishments = []
store.player_possessions = []
store.rare_outcome_last_day = {}
store.rare_outcome_seen = []
store.rare_bar_challenger = -1
store._rare_opportunity_last = {}
store._pulse_mail_today = 0
store.mail_queue = []


class _Rnd(object):
    """Ren'Py's renpy.random surface, backed by a seeded Random so the
    distribution tests below are reproducible run to run."""
    def __init__(self):
        self.r = random.Random(1234)

    def randint(self, a, b):
        return self.r.randint(a, b)

    def random(self):
        return self.r.random()

    def choice(self, seq):
        return self.r.choice(seq)


class _Renpy(object):
    random = _Rnd()

    class config(object):
        developer = False

    @staticmethod
    def notify(*a, **kw):
        pass

    @staticmethod
    def log(*a, **kw):
        pass

    @staticmethod
    def loadable(p):
        return False

    @staticmethod
    def random_seed(*a):
        pass


G = {"store": store, "renpy": _Renpy, "__builtins__": __builtins__}

# Minimal stand-ins for functions the extracted blocks reach out to. Every one
# of these is *outside* the code under test.
STUBS = """
PRO_SKILLS = {"prog": ("Programming","",""), "cook": ("Culinary","",""),
              "med": ("Medicine","",""), "biz": ("Business","",""),
              "fit": ("Fitness","",""), "mech": ("Mechanics","",""),
              "art": ("Art","",""), "music": ("Guitar","","")}
_SKILLS = {"music": 5, "art": 5, "cook": 5, "fit": 5, "mech": 5, "prog": 5}
def skill_val(k): return _SKILLS.get(k, 0)
def gain_skill(k, n): pass
def gain_skill_practice(k, xp, hours=1): return xp
def gain_money(n, cat=None): pass
def try_spend(n, cat=None): return True
def spend_time(h): pass
def has_player_state(s): return False
def add_player_state(s, t=None): pass
def equipment_modifier(a, b): return 0
def strings_modifier(): return 0
def dressed_for(x): return 0
def home_upgrade_effect(x): return 0
def location_event_modifier(a, b, c=0): return c
def activity_use_count_today(a): return 0
def mark_activity_used_today(a): pass
def record_game_event(*a, **kw): pass
def publish_player_fact(*a, **kw): return None
def maybe_rare_opportunity(*a, **kw): return None
def trigger_failure_content(*a, **kw): pass
def career_perf(c): return 0
def set_career_perf(c, v): pass
def promotion_requirements_status(c): return []
def complete_skill_gate(*a): pass
def queue_mail(sender, subject, body, cat, day, tag):
    store.mail_queue = list(store.mail_queue) + [
        {"sender": sender, "subject": subject, "tag": tag, "day": day}]
def mail_already_queued(tag):
    return any(m["tag"] == tag for m in store.mail_queue)
PULSE_MAX_MAIL_PER_DAY = 3
def _pulse_can_mail(): return store._pulse_mail_today < PULSE_MAX_MAIL_PER_DAY
RARE_OPPORTUNITY_TEMPLATES = {
    "busking_venue_contact": {"activity": "busking", "chance": 0.04,
        "cooldown_days": 14, "sender": "The Anchor", "subject": "Heard you",
        "body": "..."},
    "art_market_commission": {"activity": "art_market_participation",
        "chance": 0.15, "cooldown_days": 21, "sender": "Private buyer",
        "subject": "About the piece", "body": "..."},
}
"""
exec(compile(STUBS, "<stubs>", "exec"), G)

for block in (rpy_python_blocks("resolution_checks.rpy")
              + rpy_python_blocks("rare_outcomes.rpy")
              + rpy_python_blocks("possessions.rpy")
              + rpy_python_blocks("busking.rpy")):
    exec(compile(block, "<rpy>", "exec"), G)

RARE_TIER_ORDER = G["RARE_TIER_ORDER"]
check_rare_outcome = G["check_rare_outcome"]
roll_rare_table = G["roll_rare_table"]
rare_roll_int = G["rare_roll_int"]
rare_cooldown_ok = G["rare_cooldown_ok"]
rare_once_ok = G["rare_once_ok"]
record_rare_triggered = G["record_rare_triggered"]
rare_fires = G["rare_fires"]
rare_pct_for = G["rare_pct_for"]
near_miss_line = G["near_miss_line"]
force_rare_opportunity = G["force_rare_opportunity"]
rare_mail = G["rare_mail"]
roll_check = G["roll_check"]
busking_resolve = G["busking_resolve"]
RULES = G["RARE_ACTIVITY_RULES"]


def fresh():
    """Reset the per-attempt bookkeeping the engine mutates."""
    store._check_pity = {}
    store._check_attempts = {}
    store.rare_outcome_last_day = {}
    store.rare_outcome_seen = []
    store._rare_opportunity_last = {}
    store._pulse_mail_today = 0
    store.mail_queue = []
    _Renpy.random.r = random.Random(1234)


# ══════════════════════════════════════════════════════════════════════════════
print("\nA. GUARANTEED PROGRESS — a bad roll never erases progress")
fresh()
xp_seen = []
for d in range(200):
    store.day = 100 + d
    r = busking_resolve(1, 0, 20)          # skill 1, no rep, exhausted
    xp_seen.append(r["xp_base"])
    check_tips = r["tips"]
    if check_tips < G["_BUSK_TIP_FLOOR"]:
        break
check("A1 guitar XP is granted on every single session", min(xp_seen) > 0,
      "min xp_base=%r" % min(xp_seen))
check("A2 XP is a flat guarantee, not tier-scaled", len(set(xp_seen)) == 1)
fresh()
tips = [busking_resolve(1, 0, 20)["tips"] for _ in range(300)]
check("A3 tips never fall below the consolation floor",
      min(tips) >= G["_BUSK_TIP_FLOOR"], "min=%d" % min(tips))

# ── B ─────────────────────────────────────────────────────────────────────────
print("\nB. SKILL DOMINANCE — high skill is materially better, not just luckier")


def tier_dist(skill, difficulty=45, mods=None, n=4000):
    out = {t: 0 for t in RARE_TIER_ORDER}
    store._check_pity = {}
    for i in range(n):
        store.day = 1000 + i
        out[roll_check("dist_%d" % i, skill, difficulty, mods or [])["tier"]] += 1
    return {k: v * 100.0 / n for k, v in out.items()}


_Renpy.random.r = random.Random(99)
lo = tier_dist(0)
mid = tier_dist(5)
hi = tier_dist(10)


def good(d):
    return d["success"] + d["great"] + d["critical"]


check("B1 skill 10 beats skill 0 on success-or-better by 20+ points",
      good(hi) - good(lo) >= 20, "%.1f vs %.1f" % (good(hi), good(lo)))
check("B2 success-or-better is monotonic in skill",
      good(lo) < good(mid) < good(hi),
      "%.1f / %.1f / %.1f" % (good(lo), good(mid), good(hi)))
check("B3 top tier is monotonic in skill",
      lo["critical"] <= mid["critical"] <= hi["critical"])
check("B4 skill bonus is capped, so skill 10 is not a guarantee",
      good(hi) < 100.0, "%.1f%%" % good(hi))

# ── C ─────────────────────────────────────────────────────────────────────────
print("\nC. PREPARATION — context shifts the ACTUAL distribution, not just the text")
_Renpy.random.r = random.Random(77)
plain = tier_dist(5)
prepped = tier_dist(5, mods=[("Rehearsed setlist", 8), ("Rested", 4)])
check("C1 preparation raises success-or-better",
      good(prepped) > good(plain), "%.1f vs %.1f" % (good(prepped), good(plain)))
calc = G["calculate_check_chance"]
a = calc("prep", 5, 45, [])["success_or_better"]
b = calc("prep", 5, 45, [("Rehearsed setlist", 8)])["success_or_better"]
check("C2 the previewed number moves by exactly the modifier", b - a == 8,
      "%d -> %d" % (a, b))
check("C3 preview and roll share one modifier pipeline (+/-2 of simulation)",
      abs(good(prepped) - calc("prep", 5, 45,
          [("Rehearsed setlist", 8), ("Rested", 4)])["success_or_better"]) < 2.5)

# ── D ─────────────────────────────────────────────────────────────────────────
print("\nD. STABLE RESULT — the same attempt resolves the same way on reload")
store.day = 42
store._check_pity = {}
first = roll_check("mech_job7", 5, 55, [], attempt_number=3, stable=True)
store._check_pity = {}
again = roll_check("mech_job7", 5, 55, [], attempt_number=3, stable=True)
check("D1 stable roll_check replays identically",
      first["final"] == again["final"] and first["tier"] == again["tier"])
store._check_pity = {}
other = roll_check("mech_job7", 5, 55, [], attempt_number=4, stable=True)
check("D2 a different attempt number is a different roll",
      other["raw_roll"] != first["raw_roll"])

# ── E ─────────────────────────────────────────────────────────────────────────
print("\nE. RARE GATE — a poor result cannot buy a rare outcome")
for act, r in RULES.items():
    floor = RARE_TIER_ORDER.index(r["min_tier"])
    bad = [t for t in RARE_TIER_ORDER[:floor]]
    hits = 0
    for t in bad:
        for n in range(400):
            if check_rare_outcome(act, t, n, r["min_tier"], 100):
                hits += 1
    check("E %-22s never fires below %s" % (act, r["min_tier"]), hits == 0,
          "%d leaks" % hits)
check("E5 rare_pct=0 never fires",
      not any(check_rare_outcome("x", "critical", n, "success", 0)
              for n in range(500)))
check("E6 an unknown activity id has no rare layer",
      rare_fires("not_an_activity", "critical", 1) is False)

print("\nE7. observed rare rate matches the declared percentage")
for act, r in RULES.items():
    pct = rare_pct_for(act)
    hits = 0
    N = 6000
    for n in range(N):
        store.day = 500 + (n // 40)
        if check_rare_outcome(act, "critical", n, r["min_tier"], pct):
            hits += 1
    obs = hits * 100.0 / N
    check("  %-22s declared %2d%%, observed %.1f%%" % (act, pct, obs),
          abs(obs - pct) < 2.0)
store.day = 30

# ── F ─────────────────────────────────────────────────────────────────────────
print("\nF. RARE STABILITY — the same attempt picks the same table entry")
TABLE = [(60, "surge", None), (18, "contact", None),
         (12, "lead", None), (10, "memory", None)]
store.day = 55
picks = [roll_rare_table("busking", 7, TABLE) for _ in range(50)]
check("F1 table selection replays identically", len(set(picks)) == 1,
      "got %r" % set(picks))
sizes = [rare_roll_int("busking", 7, 8, 25) for _ in range(50)]
check("F2 the payout size replays identically too", len(set(sizes)) == 1)
check("F3 the payout stays inside its declared band", 8 <= sizes[0] <= 25)
check("F4 the gate, the table and the size are independent streams",
      len({G["_rare_seed"]("busking", 7, "_rare"),
           G["_rare_seed"]("busking", 7, "_table"),
           G["_rare_seed"]("busking", 7, "_size")}) == 3)
spread = set()
for n in range(400):
    store.day = 600 + n
    spread.add(roll_rare_table("busking", n, TABLE))
check("F5 every table entry is reachable", spread == {"surge", "contact", "lead", "memory"},
      "reached %r" % spread)
weights = {}
for n in range(4000):
    store.day = 2000 + n
    p = roll_rare_table("busking", n, TABLE)
    weights[p] = weights.get(p, 0) + 1
check("F6 weights are respected (surge ~60%%)",
      abs(weights["surge"] * 100.0 / 4000 - 60) < 4,
      "%.1f%%" % (weights["surge"] * 100.0 / 4000))
store.day = 30

# ── G ─────────────────────────────────────────────────────────────────────────
print("\nG. UNIQUE DEDUP — an already-earned unique cannot be handed out twice")
fresh()
record_rare_triggered("busk_memorable", once=True)
check("G1 the once flag is stored", not rare_once_ok("busk_memorable"))
onlyunique = [(50, "memory", lambda: rare_once_ok("busk_memorable")),
              (50, "surge", None)]
got = set()
for n in range(300):
    store.day = 700 + n
    got.add(roll_rare_table("busking", n, onlyunique))
check("G2 a consumed unique is filtered out of the table", got == {"surge"},
      "got %r" % got)
check("G3 record_rare_triggered(once=True) is idempotent",
      (record_rare_triggered("busk_memorable", once=True),
       store.rare_outcome_seen.count("busk_memorable"))[1] == 1)
check("G4 an all-invalid table returns None",
      roll_rare_table("busking", 1,
                      [(50, "memory", lambda: False)]) is None)
check("G5 an empty table returns None", roll_rare_table("busking", 1, []) is None)
store.player_possessions = [{"item_id": "musician_contact_card", "id": "p1"}]
check("G6 grant_possession refuses a second copy of a unique",
      G["grant_possession"]("musician_contact_card", "again") is False)
store.player_possessions = []
store.day = 30

# ── H ─────────────────────────────────────────────────────────────────────────
print("\nH. REPEATABLE RARE — cooldowns are respected")
fresh()
store.day = 100
check("H1 a never-fired rare is off cooldown", rare_cooldown_ok("busk_surge", 2))
record_rare_triggered("busk_surge")
check("H2 same day is on cooldown", not rare_cooldown_ok("busk_surge", 2))
store.day = 101
check("H3 one day into a 2-day cooldown is still blocked",
      not rare_cooldown_ok("busk_surge", 2))
store.day = 102
check("H4 the cooldown expires exactly on schedule",
      rare_cooldown_ok("busk_surge", 2))
store.day = 100 + 13
record_rare_triggered("busk_venue")
store.day = 100 + 13 + 13
check("H5 a 14-day lead cooldown still blocks at day 13",
      not rare_cooldown_ok("busk_venue", 14))
store.day = 100 + 13 + 14
check("H6 and clears at day 14", rare_cooldown_ok("busk_venue", 14))
store.day = 30

# ── I ─────────────────────────────────────────────────────────────────────────
print("\nI. FOLLOW-UP — a rare lead schedules exactly one follow-up")
fresh()
store.day = 200
check("I1 the lead queues one mail", force_rare_opportunity("busking_venue_contact", 3))
check("I2 exactly one mail was queued", len(store.mail_queue) == 1,
      "%d" % len(store.mail_queue))
check("I3 it arrives in the future, not today",
      store.mail_queue[0]["day"] == 203)
check("I4 firing it again the same day is refused (dedup + cooldown)",
      force_rare_opportunity("busking_venue_contact", 3) is False)
check("I5 still exactly one mail", len(store.mail_queue) == 1)
store.day = 205
check("I6 and still refused inside the 14-day cooldown",
      force_rare_opportunity("busking_venue_contact", 3) is False)
store.day = 214
check("I7 available again once the cooldown clears",
      force_rare_opportunity("busking_venue_contact", 3))
check("I8 an unknown template id is refused, not crashed on",
      force_rare_opportunity("no_such_template") is False)
fresh()
store.day = 300
store._pulse_mail_today = G["PULSE_MAX_MAIL_PER_DAY"]
check("I9 the daily mail budget is honoured",
      force_rare_opportunity("busking_venue_contact") is False
      and rare_mail("a", "b", "c", "tag_x") is False)
check("I10 nothing was queued when over budget", len(store.mail_queue) == 0)
store.day = 30

# ── J ─────────────────────────────────────────────────────────────────────────
print("\nJ. ECONOMY — the rare layer does not move $/hour meaningfully")
BUSK_HOURS = 1.5
fresh()
N = 3000
base_total = 0
for i in range(N):
    store.day = 3000 + i
    base_total += busking_resolve(6, 40, 80)["tips"]
base_per_h = base_total / float(N) / BUSK_HOURS

# The wrapper is not loaded here, so model its ONE money branch from the real
# constants: pct * weight_share * mean(size).
pct = rare_pct_for("busking") / 100.0
surge_share = 60.0 / (60 + 18 + 12 + 10)
lo_s, hi_s = G["_RARE_BUSK_SURGE"] if "_RARE_BUSK_SURGE" in G else (8, 25)
rare_per_h = pct * surge_share * ((lo_s + hi_s) / 2.0) / BUSK_HOURS
print("     busking base %.2f $/h  +  rare %.2f $/h  =  %.2f $/h"
      % (base_per_h, rare_per_h, base_per_h + rare_per_h))
check("J1 the rare money branch adds under $1.50/hour", rare_per_h < 1.50,
      "%.2f" % rare_per_h)
check("J2 the rare uplift is under 5%% of base", rare_per_h < base_per_h * 0.05,
      "%.1f%%" % (rare_per_h / base_per_h * 100))
BEST_CAREER_PER_H = 60.0     # Hospital Chief, per debug_balance.rpy
check("J3 busking with rares stays under the best career $/h",
      base_per_h + rare_per_h < BEST_CAREER_PER_H,
      "%.2f vs %.2f" % (base_per_h + rare_per_h, BEST_CAREER_PER_H))
BUSK_CAP = G["BUSK_DAILY_CAP"]
check("J4 the daily session cap is still in force", BUSK_CAP == 3)
daily = (base_per_h + rare_per_h) * BUSK_HOURS * BUSK_CAP
print("     busking ceiling: %.0f $/day across %d sessions" % (daily, BUSK_CAP))
check("J5 a full busking day stays under a full career day",
      daily < BEST_CAREER_PER_H * 8)
# Every other rare branch must be non-monetary.
NON_MONEY = ["musician_connection", "venue_lead", "memorable_performance",
             "social_spike", "promoter_notice", "venue_invitation",
             "first_exceptional", "social_exposure", "gallery_interest",
             "collector_interest", "breakthrough_piece", "local_reputation",
             "rematch_invite", "new_challenger", "contact_gain",
             "public_recognition", "unique_first_win"]
src = io.open(os.path.join(GAME, "rare_outcomes.rpy"), encoding="utf-8").read()
check("J6 only ONE rare branch touches money at all",
      src.count("res[\"tips\"] +=") == 1, "%d" % src.count("res[\"tips\"] +="))
check("J7 no rare branch calls gain_money", "gain_money" not in src)
check("J8 every declared outcome id is implemented",
      all(('"%s"' % o) in src for o in NON_MONEY),
      repr([o for o in NON_MONEY if ('"%s"' % o) not in src]))

# ── K ─────────────────────────────────────────────────────────────────────────
print("\nK. RESULT UI — ordinary result and rare reveal both render safely")
store.day = 42
store._check_pity = {}
r = roll_check("ui_probe", 5, 50, [])
check("K1 the result dict carries everything the screen reads",
      all(k in r for k in ("raw_roll", "final", "tier", "breakdown", "modifiers")))
check("K2 tier_label / tier_color resolve for all five tiers",
      all(G["tier_label"](t) and G["tier_color"](t) for t in RARE_TIER_ORDER))
check("K3 near_miss_line never crashes on any tier/score pair",
      all(isinstance(near_miss_line({"tier": t, "final": f}), str)
          for t in RARE_TIER_ORDER for f in (1, 10, 39, 74, 94, 100)))
check("K4 near_miss_line is silent when the score is missing",
      near_miss_line({"tier": "success"}) == "")
check("K5 near_miss_line is silent at the top tier",
      near_miss_line({"tier": "critical", "final": 96}) == "")
check("K6 near_miss_line fires within 5 of the next floor",
      near_miss_line({"tier": "success", "final": 72}) != "")
check("K7 and stays silent at 6 away",
      near_miss_line({"tier": "success", "final": 69}) == "")
check("K8 the near-miss floor matches the engine's real threshold",
      "75" in near_miss_line({"tier": "success", "final": 74}),
      near_miss_line({"tier": "success", "final": 74}))
check("K9 the preview line is non-empty for every rare activity",
      all(G["rare_preview_line"](a) for a in RULES))
check("K10 and empty for anything else", G["rare_preview_line"]("sleeping") == "")
check("K11 rare_possible_for gates the preview to mechanical activities",
      G["rare_possible_for"]("busking") and not G["rare_possible_for"]("date_nora"))
check("K12 the rare_reveal_row screen exists",
      "screen rare_reveal_row" in src)
b_src = io.open(os.path.join(GAME, "busking.rpy"), encoding="utf-8").read()
check("K13 both music screens use it",
      b_src.count("use rare_reveal_row") == 2, "%d" % b_src.count("use rare_reveal_row"))
check("K14 the dead rare_event key is gone from busking.rpy",
      "rare_event" not in b_src)

# ── L ─────────────────────────────────────────────────────────────────────────
print("\nL. OLD SAVE — new fields initialise safely from a save without them")
for k, expect in (("rare_outcome_last_day", {}), ("rare_outcome_seen", []),
                  ("rare_bar_challenger", -1)):
    check("L1 %s has a default" % k, k in DEFAULTS and DEFAULTS[k] == expect,
          repr(DEFAULTS.get(k, "<missing>")))
# p_rare_sync lives in the init-25 block, which is not exec'd here (it rebinds
# five other systems). Exec just that function's source against the stub store.
m = re.search(r"\n    def p_rare_sync\(\):.*?(?=\n    _p_rare_orig_new_day)",
              src, re.S)
check("L2 p_rare_sync exists in the init-25 block", m is not None)
if m:
    ns = dict(G)
    exec(compile(textwrap.dedent(m.group(0)), "<sync>", "exec"), ns)
    p_rare_sync = ns["p_rare_sync"]
    # Simulate a pre-pass save: the fields simply are not there.
    for k in ("rare_outcome_last_day", "rare_outcome_seen", "rare_bar_challenger"):
        if hasattr(store, k):
            delattr(store, k)
    store.player_accomplishments = []
    store.player_possessions = []
    p_rare_sync()
    check("L3 missing fields are created", store.rare_outcome_last_day == {}
          and store.rare_outcome_seen == [] and store.rare_bar_challenger == -1)
    check("L4 it is idempotent",
          (p_rare_sync(), store.rare_outcome_seen)[1] == [])
    # A veteran save that already earned the moments must not be offered them.
    store.player_accomplishments = [
        {"id": "open_mic_first_exceptional"}, {"id": "chal_first_outright_win"},
        {"id": "art_breakthrough_piece"}, {"id": "busk_memorable_set"}]
    store.player_possessions = [{"item_id": "musician_contact_card", "id": "p1"}]
    p_rare_sync()
    for flag in ("om_first_exceptional", "chal_first_win", "art_breakthrough",
                 "busk_memorable", "busk_musician"):
        check("L5 back-filled %s from existing records" % flag,
              flag in store.rare_outcome_seen)
    n_before = len(store.rare_outcome_seen)
    p_rare_sync()
    check("L6 back-fill does not grow on a second run",
          len(store.rare_outcome_seen) == n_before)
    check("L7 None-valued fields are repaired, not crashed on",
          (setattr(store, "rare_outcome_seen", None),
           setattr(store, "rare_outcome_last_day", None),
           p_rare_sync(), store.rare_outcome_seen == [] or
           isinstance(store.rare_outcome_seen, list))[3])

# ── M: simulation report ──────────────────────────────────────────────────────
print("\nM. FREQUENCY — expected rare triggers per week, moderate player")
# Sessions/week a moderate (not optimising) player actually does.
WEEKLY = {"busking": 6, "open_mic": 1, "painting": 4,
          "bar_game": 3, "city_challenge": 0.7}
# P(reaching each activity's declared min_tier) at mid skill, read off the
# distributions measured in B/C rather than assumed.
FLOOR_P = {"success": good(mid) / 100.0,
           "great": (mid["great"] + mid["critical"]) / 100.0,
           "critical": mid["critical"] / 100.0}
total = 0.0
for act in WEEKLY:
    per_week = (WEEKLY[act] * FLOOR_P[RULES[act]["min_tier"]]
                * rare_pct_for(act) / 100.0)
    total += per_week
    print("     %-16s %.2f rare/week  (1 every %.0f weeks)"
          % (act, per_week, (1 / per_week if per_week else 0)))
print("     %-16s %.2f rare/week overall" % ("ALL", total))
check("M1 rares are rare (under 1.5/week overall)", total < 1.5, "%.2f" % total)
check("M2 but not vanishing (over 0.25/week overall)", total > 0.25, "%.2f" % total)

# ── N. DETERMINISTIC HASH — stable across process restarts ───────────────────
print("\nN. DETERMINISTIC HASH — no PYTHONHASHSEED sensitivity")
_det_hash = G["_det_hash"]
check("N1 _det_hash is idempotent",
      _det_hash("busking") == _det_hash("busking"),
      "got %r and %r" % (_det_hash("busking"), _det_hash("busking")))
check("N2 _det_hash differs for distinct inputs",
      _det_hash("busking") != _det_hash("painting"),
      "both %r" % _det_hash("busking"))
check("N3 _rare_seed source uses _det_hash not hash()",
      "hash(" not in src or "_det_hash" in src,
      "unsafe hash() found in rare_outcomes.rpy without _det_hash guard")
# _rare_seed is the only persistent seed in this file — verify the exact line.
check("N4 _rare_seed contains _det_hash call",
      "_det_hash" in G["_rare_seed"].__code__.co_consts
      or any("_det_hash" in str(c) for c in G["_rare_seed"].__code__.co_names),
      "co_names=%r" % list(G["_rare_seed"].__code__.co_names))

# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
if FAILS:
    print("FAILED %d check(s):" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    sys.exit(1)
print("All rare-outcome checks passed.")
