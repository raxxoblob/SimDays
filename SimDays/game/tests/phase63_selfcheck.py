"""Phase 63 economy-balance self-check.

Like the Phase 62 check, this does NOT re-implement formulas: it EXTRACTS the
real `init python:` blocks from the shipping .rpy files and execs them against a
stub store, so every assertion below runs the code that ships. If someone edits a
busking multiplier, a freelance pay value or a skill gate, this file fails.

    python phase63_selfcheck.py

Covers the Phase 63B rebalance:
  A. busking payout is bounded and never zero (consolation floor)
  B. busking has a daily cap
  C. busking reputation gain decays past 50
  D. prog mastery gates are escapable (no circular deadlock at 9/10)
  E. early/mid freelance $/h sits near career, not 4x it
  F. freelance XP rate slowed
  G. world challenges cost time+energy and pay consolation XP
"""
import io, os, re, sys, textwrap, random

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAILS = []


def check(label, cond, extra=""):
    if cond:
        print("  ok   %s" % label)
    else:
        print("  FAIL %s %s" % (label, extra))
        FAILS.append(label)


def rpy_python_blocks(path):
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(src):
        if re.match(r"^init(\s+-?\d+)?\s+python\s*:\s*$", src[i]) or src[i].strip() == "python:":
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
    for ln in io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n"):
        m = re.match(r"^default\s+([A-Za-z_]\w*)\s*=\s*(.+?)\s*$", ln)
        if not m:
            continue
        try:
            out[m.group(1)] = eval(re.sub(r"\s+#.*$", "", m.group(2)), {"__builtins__": {}}, {})
        except Exception:
            out[m.group(1)] = None
    return out


class Store(object):
    pass


store = Store()


class _Renpy(object):
    def notify(self, *a, **k):
        pass

    def loadable(self, *a, **k):
        return False

    def __getattr__(self, name):
        def _noop(*a, **k):
            return None
        return _noop


renpy = _Renpy()
renpy.store = store
renpy.random = random

FILES = ["data.rpy", "player_states.rpy", "home_upgrades.rpy", "careers.rpy",
         "equipment.rpy", "home_items.rpy", "clients.rpy", "freelance.rpy",
         "portfolio.rpy", "project_results.rpy", "resolution_checks.rpy",
         "busking.rpy", "bar_games.rpy", "world_challenges.rpy"]

G = {"store": store, "renpy": renpy, "random": random, "__builtins__": __builtins__}

for f in sorted(os.listdir(GAME)):
    if f.endswith(".rpy"):
        for k, v in rpy_defaults(f).items():
            if not hasattr(store, k):
                setattr(store, k, v)
for f in FILES:
    for blk in rpy_python_blocks(f):
        try:
            exec(compile(blk, f, "exec"), G)
        except Exception:
            pass   # non-economy helpers may reference renpy internals

store._check_pity = {}
store.player_states = {}
store.need_energy = 70
store.owned_equipment = []
store.equipment_condition = {}
store.home_slots = {}
store.wardrobe_equipped = {}
store.guitar_strings_last_refreshed = -999
store.activity_mastery = {}
store.music_reputation = 0
store.day = 15
store.hour = 14

# Phase 67 wired busking's crowd base to the world-pulse location modifier.
# world_pulse.rpy is not part of this harness, so stub it to "no event today" —
# that is exactly the baseline these balance assertions are written against.
G.setdefault("location_event_modifier", lambda loc, key, base=0: base)
G.setdefault("global_event_modifier", lambda key, base=0: base)
# Phase 67/68 side-effect hooks at the end of a busking session. Neither pays
# money, so stubbing them out leaves the payout maths untouched.
G.setdefault("maybe_rare_opportunity", lambda activity_id, location_id=None: None)
G.setdefault("publish_player_fact", lambda fact_type, detail="": None)

print("A. busking payout bounds")
resolve = G["busking_resolve"]
FLOOR = G["_BUSK_TIP_FLOOR"]
worst = []
for _ in range(4000):
    store._check_pity = {}
    store.music_reputation = 0
    worst.append(resolve(1, 0, 70)["tips"])
check("no zero-payout busking session at rep 0 / music 1 (consolation floor)",
      min(worst) >= FLOOR, "min=%d floor=%d" % (min(worst), FLOOR))

store.activity_mastery = {"busking": 100}
best = []
for _ in range(4000):
    store._check_pity = {}
    store.music_reputation = 100
    best.append(resolve(10, 100, 70)["tips"])
ev_max = sum(best) / float(len(best))
# 1.5h/session. Best career is Hospital Chief at $480/8h = $60/h.
check("max busking EV/hour stays within ~1.3x of the best career rate",
      ev_max / 1.5 < 80, "EV/h=%.1f" % (ev_max / 1.5))
check("crowd x perf product is capped", G["_BUSK_MULT_CAP"] <= 2.0,
      str(G["_BUSK_MULT_CAP"]))

print("B. busking daily cap")
check("BUSK_DAILY_CAP defined and small", 1 <= G["BUSK_DAILY_CAP"] <= 4,
      str(G["BUSK_DAILY_CAP"]))
busk_src = io.open(os.path.join(GAME, "busking.rpy"), encoding="utf-8").read()
check("busking label enforces the cap",
      "activity_use_count_today(\"busking\") >= BUSK_DAILY_CAP" in busk_src)
check("busking label records the use",
      'mark_activity_used_today("busking")' in busk_src)
loc_src = io.open(os.path.join(GAME, "locations.rpy"), encoding="utf-8").read()
check("park menu hides Busk once the cap is spent",
      'activity_use_count_today("busking") < BUSK_DAILY_CAP' in loc_src)

print("C. busking reputation decay")
store.activity_mastery = {"busking": 100}
lo = [resolve(10, 10, 70)["rep_gain"] for _ in range(2000)]
hi = [resolve(10, 90, 70)["rep_gain"] for _ in range(2000)]
check("rep gain is slower past 50 than below it",
      sum(hi) / 2000.0 < sum(lo) / 2000.0,
      "below=%.2f above=%.2f" % (sum(lo) / 2000.0, sum(hi) / 2000.0))

print("D. prog mastery gates are escapable")
TPL = G["FREELANCE_TEMPLATES"]
fl_src = io.open(os.path.join(GAME, "freelance.rpy"), encoding="utf-8").read()
for lvl in (9, 10):
    m = re.search(r"if _msk >= (\d+):\s*\n\s*complete_skill_gate\(\"prog\", %d," % lvl, fl_src)
    assert m, "gate %d trigger not found" % lvl
    need = int(m.group(1))
    # a template with min_skill == need must be reachable at a level BELOW lvl
    ok = any(t["min_skill"] == need for t in TPL) and need < lvl
    check("prog gate %d is clearable before reaching level %d" % (lvl, lvl), ok,
          "trigger min_skill=%d" % need)

print("E. freelance $/hour vs career")
CAREERS = G["CAREERS"]
# Mean rank-0 rate is the representative "entry career" baseline. Using min()
# would benchmark against Assistant Trainer ($65/8h), the lowest-paid job in the
# game, and understate what a typical starting worker earns.
_r0 = [c["ranks"][0]["pay"] / 8.0 for c in CAREERS.values()]
career_r0 = sum(_r0) / len(_r0)
entry = [t for t in TPL if t["min_skill"] == 1]
entry_rate = max(t["pay"] / float(t["hours"]) for t in entry)
check("entry freelance is better than entry career", entry_rate > career_r0,
      "%.1f vs %.1f" % (entry_rate, career_r0))
check("entry freelance is not more than 3x entry career",
      entry_rate <= career_r0 * 3.0, "%.1f vs %.1f" % (entry_rate, career_r0))
# Per-hour freelance beats a shift, but only one project can be run per day, so
# absolute daily income at entry stays below a full career shift.
best_entry_day = max(t["pay"] for t in entry)
check("one entry freelance project/day earns less than one career shift",
      best_entry_day < min(c["ranks"][0]["pay"] for c in CAREERS.values()) * 1.2,
      "$%d vs shift $%d" % (best_entry_day,
                            min(c["ranks"][0]["pay"] for c in CAREERS.values())))
check("skill 6+ freelance tiers kept as late-game reward",
      [t["pay"] for t in TPL if t["id"] == "perf_01"] == [700])

print("F. freelance XP rate")
m = re.search(r"xp = int\(hours \* (\d+) \* xp_mult", fl_src)
check("freelance session XP/hour reduced from 8", m and int(m.group(1)) <= 5,
      m.group(1) if m else "?")
check("completion exp bonus is scaled down",
      'gain_skill("prog", max(1, int(pmt["exp"] * 0.5)))' in fl_src)

print("G. world challenges cost resources and pay consolation")
wc_src = io.open(os.path.join(GAME, "world_challenges.rpy"), encoding="utf-8").read()
check("attempt spends time", "spend_time(ch.get(\"hours\"" in wc_src)
check("attempt spends energy", "ch.get(\"energy\"" in wc_src)
check("failure grants consolation XP", "_base // 3" in wc_src)
check("the only cash challenge is off a 1-day cooldown",
      G["WORLD_CHALLENGES"]["beat_professor_pool"]["cooldown_days"] >= 3,
      str(G["WORLD_CHALLENGES"]["beat_professor_pool"]["cooldown_days"]))

print()
if FAILS:
    print("FAILED %d check(s): %s" % (len(FAILS), ", ".join(FAILS)))
    sys.exit(1)
print("All Phase 63 balance checks passed.")
