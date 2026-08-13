"""Phase 65 runtime self-check — capability system + painting vertical slice.

Same approach as phase62/phase64: EXTRACTS the real `init python:` blocks out of
equipment.rpy / home_items.rpy / capabilities.rpy / resolution_checks.rpy /
painting.rpy and execs them against a stub `store`, so every assertion below
runs the SHIPPING code. Change a modifier, a price or a cap and this fails.

    python phase65_selfcheck.py

Covers spec section 17 tests A-H and the section 15 mandatory economy audit.
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    """Every `default name = value` in a file, as a dict. Keeps the stub store
    honest: if a new persistent variable is added it appears here for free."""
    out = {}
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read()
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)\s*(?:#.*)?$", src, re.M):
        try:
            out[m.group(1)] = eval(m.group(2), {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


# ── Stub store ───────────────────────────────────────────────────────────────
class Store(object):
    def __init__(self):
        self.day = 30
        self.hour = 9.0
        self.money = 5000
        self.loan = 0
        self.need_energy = 70
        self.need_hunger = 70
        self.need_hygiene = 70
        self.owned_equipment = []
        self.equipment_condition = {}
        self.home_slots = {}
        self.wardrobe_equipped = {}
        self.savings_target = None
        self.guitar_strings_last_refreshed = -999
        self._morning_item_used = None
        self._home_ambient_day = -1
        self._home_ambient_tier = -1
        self._check_pity = {}
        self._check_attempts = {}
        self.city_event_schedule = []
        self.skill_art = 0
        self.own_guitar = False
        self.own_computer = False
        self.own_sketchbook = False
        self.own_coffee_machine = False
        self.own_kitchen_set = False
        self.own_bed = False
        self.zoe_affection = 40
        self.marcus_affection = 40
        self.sam_affection = 40
        self.elle_affection = 40
        self.art_reputation = 0
        for k, v in DEFAULTS.items():
            setattr(self, k, v() if callable(v) else (list(v) if isinstance(v, list)
                    else dict(v) if isinstance(v, dict) else v))


DEFAULTS = {}
DEFAULTS.update(rpy_defaults("painting.rpy"))
DEFAULTS.update(rpy_defaults("home_items.rpy"))

store = Store()
G = {}

_events = []
_xp_log = []
_money_log = []
_aff_log = []


class _Rand(object):
    """renpy.random stand-in. `fixed` makes randint return the band midpoint so
    expected-value maths is deterministic."""
    fixed = False

    def randint(self, a, b):
        import random
        return (a + b) // 2 if self.fixed else random.randint(a, b)

    def choice(self, seq):
        import random
        return seq[0] if self.fixed else random.choice(seq)

    def random(self):
        import random
        return 0.5 if self.fixed else random.random()


class _Renpy(object):
    random = _Rand()

    def notify(self, *a, **k):
        return None

    def loadable(self, *a, **k):
        return False


RENPY = _Renpy()

NPC_DATA_STUB = {
    "nora":   {"name": "Nora",   "aff": "nora_affection",   "trust": "nora_trust"},
    "marcus": {"name": "Marcus", "aff": "marcus_affection", "trust": "marcus_trust"},
    "zoe":    {"name": "Zoe",    "aff": "zoe_affection",    "trust": "zoe_trust"},
    "eli":    {"name": "Eli",    "aff": "eli_affection",    "trust": "eli_trust"},
    "sam":    {"name": "Sam",    "aff": "sam_affection",    "trust": "sam_trust"},
    "elle":   {"name": "Elle",   "aff": "elle_affection",   "trust": "elle_trust"},
    "lena":   {"name": "Dr. Lena", "aff": "lena_affection", "trust": "lena_trust"},
    "rena":   {"name": "Chef Rena", "aff": "rena_affection", "trust": "rena_trust"},
    "martha": {"name": "Martha", "aff": "martha_affection", "trust": "martha_trust"},
}
for _n in NPC_DATA_STUB:
    setattr(Store, _n + "_affection", 40)
    setattr(Store, _n + "_trust", 20)
    setattr(Store, _n + "_met", True)


def _try_spend(amount, category="discretionary", toast=True):
    amount = int(amount)
    if amount <= 0:
        return True
    if store.money < amount:
        return False
    store.money -= amount
    return True


def _gain_money(amt, category="discretionary"):
    if amt < 0:
        return _try_spend(-amt, category)
    store.money += amt
    _money_log.append((amt, category))
    return True


def _spend_time(hours):
    store.hour += hours


def _gain_skill_practice(key, base_xp, hours=1):
    eff = max(1, int(base_xp * 0.8))          # stands in for the DR curve
    _xp_log.append((key, eff))
    return eff


def _record_game_event(event_id, category, title, **k):
    _events.append({"id": event_id, "category": category, "title": title, "meta": k})


def _apply_aff(npc_id, delta):
    av = NPC_DATA_STUB[npc_id]["aff"]
    setattr(store, av, max(-100, min(100, getattr(store, av, 0) + delta)))
    _aff_log.append((npc_id, delta))


def boot():
    global G
    G = {
        "store": store, "renpy": RENPY,
        "try_spend": _try_spend, "gain_money": _gain_money, "spend_time": _spend_time,
        "gain_skill_practice": _gain_skill_practice, "record_game_event": _record_game_event,
        "gain_skill": lambda k, a=1: None,
        "skill_val": lambda k: getattr(store, "skill_" + k, 0),
        "has_player_state": lambda s: False,
        "add_player_state": lambda *a, **k: None,
        "home_upgrade_effect": lambda k: 0,
        "owns_home_upgrade": lambda k: False,
        "NPC_DATA": NPC_DATA_STUB, "_apply_aff": _apply_aff,
        "show_npc_expr": lambda *a, **k: None,
        "npc_aff": lambda n: getattr(store, NPC_DATA_STUB[n]["aff"], 0),
        "__builtins__": __builtins__,
    }
    for path in ("equipment.rpy", "home_items.rpy", "resolution_checks.rpy",
                 "capabilities.rpy", "painting.rpy"):
        for blk in rpy_python_blocks(path):
            try:
                exec(compile(blk, path, "exec"), G)
            except Exception as e:
                # resolution_checks.rpy has blocks that touch systems we do not
                # load (careers, states). Only painting's own blocks must run.
                if path in ("painting.rpy", "capabilities.rpy", "home_items.rpy"):
                    raise
                print("       (skipped a %s block: %s)" % (path, e))


failures = []


def check(name, cond, extra=""):
    print(("  OK   " if cond else "  FAIL ") + name +
          (("  -> " + str(extra)) if extra and not cond else ""))
    if not cond:
        failures.append(name)


def note(s):
    print("       " + s)


def reset(**kw):
    global store
    store = Store()
    for k, v in kw.items():
        setattr(store, k, v)
    G["store"] = store
    del _events[:], _xp_log[:], _money_log[:], _aff_log[:]


def own_and_equip(item_id, condition="Excellent"):
    store.owned_equipment = list(store.owned_equipment) + [item_id]
    store.equipment_condition[item_id] = condition
    G["equip_item"](item_id)


def own(item_id, condition="Excellent"):
    store.owned_equipment = list(store.owned_equipment) + [item_id]
    store.equipment_condition[item_id] = condition


boot()
CAT = G["ITEM_CATALOG"]
has_cap = G["has_home_capability"]

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[A] CAPABILITY SYSTEM")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
check("A1 no art gear -> no painting capability", not has_cap("painting"))
check("A1 no art gear -> no sketching capability", not has_cap("sketching"))
check("A1 no art sessions offered", G["available_art_sessions"]() == [],
      G["available_art_sessions"]())

reset()
own("sketchbook")
check("sketchbook (lifestyle, no slot) grants sketching by ownership alone",
      has_cap("sketching"))
check("sketchbook does NOT grant painting", not has_cap("painting"))
check("sketch practice is offered at art 0",
      "sketch_practice" in G["available_art_sessions"]())

reset()
own_and_equip("basic_easel")
check("A2 basic_easel equipped -> painting capability", has_cap("painting"))
check("A2 practice painting available", "paint_practice" in G["available_art_sessions"]())
check("A2 basic easel does NOT grant professional_painting",
      not has_cap("professional_painting"))
check("sketch practice hides once a real easel is present",
      "sketch_practice" not in G["available_art_sessions"]())

reset()
own_and_equip("studio_easel")
check("A3 studio_easel grants the SAME painting capability", has_cap("painting"))
check("A3 studio_easel additionally grants professional_painting",
      has_cap("professional_painting"))

reset()
own("basic_easel")          # owned but NOT slotted
check("A4 owning without equipping does not grant a slotted capability",
      not has_cap("painting"))
reset()
own_and_equip("basic_easel")
store.home_slots = {}
check("A4 removing from the slot removes the capability", not has_cap("painting"))

# Acceptance criterion 2: nothing outside the catalog names an easel.
src_all = {f: io.open(os.path.join(GAME, f), encoding="utf-8").read()
           for f in ("locations.rpy", "painting.rpy", "painting_ui.rpy",
                     "capabilities.rpy", "home_visits.rpy", "portfolio.rpy")}
def _code_only(text):
    """Strip comments and docstring prose — a doc mention of an item id is not
    a gate. Only executable lines count."""
    text = re.sub(r'"""[\s\S]*?"""', "", text)      # docstrings
    out = []
    for ln in text.splitlines():
        if ln.strip().startswith("#"):
            continue
        out.append(ln.split("#")[0])                 # trailing comments
    return "\n".join(out)


namers = [f for f, s in src_all.items()
          if "basic_easel" in _code_only(s) or "studio_easel" in _code_only(s)]
check("no gameplay file gates on a specific easel item id", not namers, namers)
check("home menu gates on has_home_capability",
      'has_home_capability("painting")' in src_all["locations.rpy"])

# The feature is unreachable if the gear cannot be bought. SHOP_CATEGORIES is a
# hardcoded list, so a new item category MUST be added to it — this assertion
# exists because the first cut of Phase 65 missed exactly that.
shop_cats = [c for c, _ in G["SHOP_CATEGORIES"]]
missing_cats = sorted(set(d["category"] for d in CAT.values()) - set(shop_cats))
check("every item category is reachable in the shop", not missing_cats, missing_cats)
for _need in ("basic_easel", "studio_easel", "sketchbook", "art_supply_kit"):
    check("%s is purchasable" % _need,
          _need in G["shop_items"](CAT[_need]["category"]), CAT[_need]["category"])

# Gear maths — the Phase 64 truncation bug must not recur.
reset(); own_and_equip("basic_easel")
b = G["art_gear_bonus"]()
reset(); own_and_equip("basic_easel"); own("art_supply_kit")
bk = G["art_gear_bonus"]()
reset(); own_and_equip("studio_easel")
s_ = G["art_gear_bonus"]()
reset(); own_and_equip("studio_easel"); own("art_supply_kit")
sk = G["art_gear_bonus"]()
note("gear bonus: basic %d | basic+kit %d | studio %d | studio+kit %d" % (b, bk, s_, sk))
check("basic easel gives a NON-ZERO roll bonus (no int() truncation)", b > 0, b)
check("studio easel is +5 over basic (spec)", s_ - b == 5, s_ - b)
check("supply kit is +4 (spec)", bk - b == 4, bk - b)
check("gear total stays below the +25 skill ceiling", sk < 25, sk)
# Condition wear must actually cost you — it does for every other item class.
reset(); own_and_equip("studio_easel", "Poor")
worn = G["art_gear_bonus"]()
note("studio easel at Poor condition: +%d (vs +%d at Excellent)" % (worn, s_))
check("a worn easel is worth less than a maintained one", worn < s_, (worn, s_))

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[B] PAINTING FLOW")
# ═══════════════════════════════════════════════════════════════════════════════
reset(skill_art=0)
own("sketchbook")
h0, e0 = store.hour, store.need_energy
res = G["do_painting"]("sketch_practice")
check("B1 practice always grants XP", res["xp"] >= 1, res["xp"])
check("B1 practice consumes time", store.hour > h0)
check("B1 practice consumes energy", store.need_energy < e0)
check("B1 practice normally produces no artwork object",
      res["artwork"] is None or res["tier"] == "critical")

reset(skill_art=3)
own_and_equip("basic_easel")
h0, e0, n0 = store.hour, store.need_energy, len(store.player_artworks)
res = G["do_painting"]("still_life", "still_life")
check("B3 still life consumes time", store.hour - h0 == 2.0, store.hour - h0)
check("B3 still life consumes energy", e0 - store.need_energy == 12)
check("B4 artwork saved to player_artworks", len(store.player_artworks) == n0 + 1)
art = store.player_artworks[-1]
check("B4 artwork has every spec field",
      set(["id", "type", "subject", "quality", "art_skill", "day", "estimated_value",
           "displayed", "in_portfolio", "gifted_to", "sold", "submitted_to"])
      <= set(art.keys()), sorted(art.keys()))
check("B4 artwork quality is a real engine tier",
      art["quality"] in G["CHECK_TIER_DATA"], art["quality"])
check("B4 mastery accrued for the subject",
      G["painting_mastery_points"]("still_life") > 0)

# B2: the distribution preview must exist and be a real probability distribution.
d = G["painting_chance"]("still_life", "still_life")["distribution"]
check("B2 preview distribution sums to 100", abs(sum(d.values()) - 100) <= 1, sum(d.values()))
check("B2 preview is available before committing", d["success"] >= 0)

# B5: save/load. Ren'Py persists `default` variables; the shape must be picklable.
import pickle
check("B5 player_artworks survives a pickle round-trip",
      pickle.loads(pickle.dumps(store.player_artworks)) == store.player_artworks)
check("B5 painting_mastery survives a pickle round-trip",
      pickle.loads(pickle.dumps(store.painting_mastery)) == store.painting_mastery)
check("B5 active commissions survive a pickle round-trip",
      pickle.loads(pickle.dumps(store.active_painting_commissions))
      == store.active_painting_commissions)
store._art_gift_week = {"zoe": (4, 1)}
check("B5 gift-week tuples survive a pickle round-trip",
      pickle.loads(pickle.dumps(store._art_gift_week)) == store._art_gift_week)
check("B5 sale log survives a pickle round-trip",
      pickle.loads(pickle.dumps(store._art_sale_log)) == store._art_sale_log)

# roll engine reuse — acceptance criterion 5
psrc = src_all["painting.rpy"]
check("painting uses roll_check(), no parallel RNG", "roll_check(" in psrc)
check("painting uses calculate_check_chance()", "calculate_check_chance(" in psrc)
check("painting never calls random.randint for outcome tiers",
      "randint(1, 100)" not in psrc)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[C] ARTWORK ACTIONS")
# ═══════════════════════════════════════════════════════════════════════════════
reset(skill_art=5)
own_and_equip("studio_easel")
G["do_painting"]("still_life", "still_life")
aid = store.player_artworks[-1]["id"]

before = G["home_visual_score"]()
G["update_artwork"](aid, displayed=True)
after = G["home_visual_score"]()
check("C1 displaying an artwork raises the home visual score", after > before,
      "%.2f -> %.2f" % (before, after))
check("C1 displayed_artwork_count tracks it", G["displayed_artwork_count"]() == 1)

G["update_artwork"](aid, in_portfolio=True)
check("C2 artwork marked in_portfolio", G["artwork_by_id"](aid)["in_portfolio"])

# C4 sell
reset(skill_art=5, art_reputation=20)
own_and_equip("studio_easel")
G["do_painting"]("still_life", "still_life")
a = store.player_artworks[-1]
m0 = store.money
price = G["sell_artwork"](a, "street")
check("C4 selling pays money", store.money == m0 + price and price > 0, price)
check("C4 sold artwork is marked sold", G["artwork_by_id"](a["id"])["sold"])
check("C4 sold artwork is no longer free", not G["artwork_is_free"](G["artwork_by_id"](a["id"])))
check("C4 sale is logged for the weekly cap", len(store._art_sale_log) == 1)
# Spec section 7: portfolio work is not for sale (checked in the action menu).
uisrc = src_all["painting_ui.rpy"]
check("C portfolio pieces are excluded from selling",
      '_p65_sellable = _p65_free and not _p65_art["in_portfolio"]' in uisrc)
check("C gifting stays available for any artwork, including weak ones",
      '"Give it to someone" if _p65_can_gift' in uisrc)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[E] NPC INTEREST REACTIONS")
# ═══════════════════════════════════════════════════════════════════════════════
NI = G["NPC_INTERESTS"]
check("all 9 audited NPCs present", len(NI) == 9, sorted(NI))
check("every NPC has all six domains",
      all(set(v) == set(["art", "music", "fitness", "programming", "cooking", "mechanics"])
          for v in NI.values()))
check("Zoe is the art passion (4-stage gallery arc)", NI["zoe"]["art"] == 3)
check("Marcus's stated dislike of art is encoded", NI["marcus"]["art"] < 0)
check("Eli is the programming passion", NI["eli"]["programming"] == 3)
check("Sam and Marcus are the fitness pair",
      NI["sam"]["fitness"] == 3 and NI["marcus"]["fitness"] == 3)
check("Nora and Rena are the cooking pair",
      NI["nora"]["cooking"] == 3 and NI["rena"]["cooking"] == 3)
check("Elle's art is casual (listed like, zero dialogue) not passion",
      NI["elle"]["art"] == 1)
check("Martha is domain-empty, as the audit found",
      all(v == 0 for v in NI["martha"].values()))
check("nobody has an unaudited passion",
      all(-1 <= v <= 3 for d in NI.values() for v in d.values()))

reset(skill_art=6)
own_and_equip("studio_easel")
G["do_painting"]("still_life", "still_life")
a = dict(store.player_artworks[-1]); a["quality"] = "great"
G["update_artwork"](a["id"], quality="great")
a = G["artwork_by_id"](a["id"])

hi = G["artwork_gift_value"](a, "zoe")     # interest 3
lo = G["artwork_gift_value"](a, "sam")     # interest 0
neg = G["artwork_gift_value"](a, "marcus") # interest -1
note("gift value for a Striking piece: zoe %d | sam %d | marcus %d" % (hi, lo, neg))
check("E1 high-interest NPC values the gift most", hi > lo > neg or (hi > lo and lo >= neg))
check("E1/E2 gift dialogue varies by interest level",
      len(set([G["art_gift_line"](3)[:20], G["art_gift_line"](0)[:20],
               G["art_gift_line"](-1)[:20]])) == 3)
rep0 = store.art_reputation
G["gift_artwork"](a, "zoe")
check("E1 gifting to an art-interested NPC earns reputation",
      store.art_reputation > rep0)
check("E1 gift is recorded on the artwork",
      G["artwork_by_id"](a["id"])["gifted_to"] == "zoe")
check("E1 gifting raised affection", any(n == "zoe" for n, _ in _aff_log))

# E3 home-visit comment
reset(skill_art=6)
own_and_equip("studio_easel")
G["do_painting"]("still_life", "still_life")
G["update_artwork"](store.player_artworks[-1]["id"], displayed=True)
check("E3 art-interested visitor comments on displayed work",
      G["displayed_artwork_comment"]("zoe") is not None)
check("E3 uninterested visitor says nothing",
      G["displayed_artwork_comment"]("sam") is None)
reset()
check("E3 no comment when nothing is on the wall",
      G["displayed_artwork_comment"]("zoe") is None)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[D] COMMISSIONS")
# ═══════════════════════════════════════════════════════════════════════════════
reset(skill_art=5, art_reputation=0)
own_and_equip("studio_easel")
check("commission board is closed below art_rep 5", G["painting_commission_offer"]() is None)

reset(skill_art=5, art_reputation=8)
own_and_equip("studio_easel")
o1 = G["painting_commission_offer"]()
o2 = G["painting_commission_offer"]()
check("D board opens at art_rep 5", o1 is not None)
check("D offer is stable within a refresh cycle (not rerollable)",
      o1 == o2, (o1 or {}).get("id"))
store.day += G["COMMISSION_REFRESH_DAYS"]
o3 = G["painting_commission_offer"]()
check("D offer refreshes on a new cycle", o3 is not None)
store.day -= G["COMMISSION_REFRESH_DAYS"]

check("D senior commissions are gated at art_rep 20+",
      all(t["art_rep_min"] >= 20 for t in G["PAINTING_COMMISSIONS"] if t["pay"] >= 120),
      [(t["id"], t["pay"], t["art_rep_min"]) for t in G["PAINTING_COMMISSIONS"]])

c = G["accept_painting_commission"](o1)
check("D1 accepting adds an active commission",
      G["active_painting_commission"]() is not None)
check("D1 accepting alone pays nothing", not _money_log)
check("D1 deadline is in the future", c["deadline_day"] > store.day)
check("D commission board closes while one is active",
      G["painting_commission_offer"]() is None)

check("D4 commission survives a pickle round-trip",
      pickle.loads(pickle.dumps(store.active_painting_commissions))
      == store.active_painting_commissions)

h0, m0 = store.hour, store.money
r = G["do_commission_work"](c)
check("D2 working consumes time", store.hour > h0)
check("D3 commission pays out", store.money > m0, store.money - m0)
check("D3 failure still pays something (forward progress)",
      min(G["_COMMISSION_PAY_MULT"].values()) > 0)
check("D3 meeting the brief earns +3 art reputation",
      (r["rep"] == 3) if r["met"] else True, (r["tier"], r["rep"]))
check("D critical failure costs reputation",
      G["_COMMISSION_PAY_MULT"]["critical_failure"] < 1.0)
check("D commission clears from the active list",
      G["active_painting_commission"]() is None)
check("D commission produces a delivered artwork record",
      store.player_artworks[-1]["type"] == "commission")

# deadline expiry
reset(skill_art=5, art_reputation=10)
own_and_equip("studio_easel")
G["accept_painting_commission"](G["painting_commission_offer"]())
store.day += 99
rep0 = store.art_reputation
dead = G["expire_painting_commissions"]()
check("D missed deadline expires the commission", len(dead) == 1)
check("D missed deadline costs reputation", store.art_reputation < rep0)
check("D expiry never drives reputation below 0", store.art_reputation >= 0)

# commissions must NOT be freelance templates (acceptance criterion 9)
# Code only: the ECONOMY NOTE mentions freelance as a comparison benchmark,
# which is documentation, not a dependency.
check("commissions use their own templates, not freelance",
      "freelance" not in _code_only(psrc).lower())
check("commissions have their own template table",
      "PAINTING_COMMISSIONS" in psrc)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[G/H] REPUTATION GATES, EXHIBITION, LONG-TERM CHALLENGE")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
check("art_reputation starts at 0", store.art_reputation == 0)
G["gain_art_rep"](-50)
check("art_reputation cannot go below 0", store.art_reputation == 0)
G["gain_art_rep"](500)
check("art_reputation caps at 100", store.art_reputation == 100)

gates = G["ART_REP_GATES"]
note("gates: " + ", ".join("%s %d" % (k, v) for k, v in sorted(gates.items(), key=lambda x: x[1])))
check("street sale is always available", gates["street_sale"] == 0)
check("commission board at art_rep 5", gates["commission_board"] == 5)
check("gallery consignment at art_rep 10", gates["gallery_sale"] == 10)
check("exhibition entry at art_rep 8", gates["exhibition_entry"] == 8)
check("senior commission tier at art_rep 25", gates["senior_commission"] == 25)

# exhibition wiring lives in the EXISTING challenge system
cc = io.open(os.path.join(GAME, "city_challenges.rpy"), encoding="utf-8").read()
check("G art_exhibition added to CITY_CHALLENGE_TEMPLATES", '"art_exhibition"' in cc)
check("G exhibition requires art_reputation 8 and an entered piece",
      '"art_reputation": 8' in cc and '"submitted_artwork"' in cc)
check("G exhibition awards art_rep, not freelance rep", '"art_rep":' in cc)
check("G exhibition placements award a portfolio entry", '"portfolio": "art"' in cc)
check("G no new event system was created",
      "CITY_EVENT_TEMPLATES.append" in cc and "def generate_" not in cc)

# submitted piece quality drives placement
reset(skill_art=6, art_reputation=10)
own_and_equip("studio_easel")
G["do_painting"]("still_life", "still_life")
a = store.player_artworks[-1]
store.city_event_schedule = [{"id": "ev1", "template_id": "art_exhibition",
                              "title": "Local Art Exhibition", "attended": False}]
check("G nothing submitted -> no submission bonus",
      G["exhibition_submission_bonus"]("ev1") is None)
G["update_artwork"](a["id"], quality="success", submitted_to="ev1")
lowb = G["exhibition_submission_bonus"]("ev1")[1]
G["update_artwork"](a["id"], quality="critical")
highb = G["exhibition_submission_bonus"]("ev1")[1]
check("G a better entered piece places better", highb > lowb, (lowb, highb))
check("G only success+ pieces can be entered",
      all(G["quality_at_least"](x["quality"], "success")
          for x in G["exhibition_submittable_artworks"]()))

wc = io.open(os.path.join(GAME, "world_challenges.rpy"), encoding="utf-8").read()
check("H first_exhibition_win added to WORLD_CHALLENGES", '"first_exhibition_win"' in wc)
check("H challenge is gated on art 4 AND art_rep 8",
      '"unlock_req":  {"art": 4, "art_rep": 8}' in wc)
check("H difficulty 72 as specified", '"difficulty":  72' in wc)
check("H 14-day cooldown", 'first_exhibition_win' in wc and '"cooldown_days": 14' in wc)
check("H non-skill unlock requirements are table-driven, not an if-chain",
      "_WC_NON_SKILL_REQ" in wc)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[F] ECONOMY — MANDATORY EV AUDIT (spec section 15)")
# ═══════════════════════════════════════════════════════════════════════════════
BENCHMARK = 40.0        # $/hour flag threshold at mid skill (spec section 15)
RENPY.random.fixed = True

TIERS = ["critical_failure", "weak", "success", "great", "critical"]


def ev_sale(skill, subject, session, channel, rep, gear):
    """Expected $/hour for painting a piece and selling it."""
    reset(skill_art=skill, art_reputation=rep)
    for it in gear:
        if CAT[it]["slot"]:
            own_and_equip(it)
        else:
            own(it)
    dist = G["painting_chance"](session, subject)["distribution"]
    hours = G["ART_SESSIONS"][session]["hours"]
    if channel == "street":
        hours += 1.0                       # an hour on the pavement to sell it
    total = 0.0
    for t in TIERS:
        val = G["artwork_estimated_value"](t, subject, skill)
        fake = {"estimated_value": val}
        total += (dist[t] / 100.0) * G["art_sale_price"](fake, channel, preview=True)
    total -= G["art_material_cost"](session)
    return total, total / hours, dist


def ev_commission(skill, template_id, rep, gear):
    reset(skill_art=skill, art_reputation=rep)
    for it in gear:
        if CAT[it]["slot"]:
            own_and_equip(it)
        else:
            own(it)
    t = next(x for x in G["PAINTING_COMMISSIONS"] if x["id"] == template_id)
    c = G["accept_painting_commission"](t)
    dist = G["commission_chance"](c)["distribution"]
    ev = sum((dist[k] / 100.0) * t["pay"] * G["_COMMISSION_PAY_MULT"][k] for k in TIERS)
    ev -= G["art_material_cost"]("canvas")
    return ev, ev / t["hours"]


BASIC = ["basic_easel", "art_supply_kit"]
STUDIO = ["studio_easel", "art_supply_kit"]

print("\n       PAINTING INCOME PATHS — expected value per session and per hour")
print("       %-46s %9s %9s" % ("path", "EV/sess", "EV/hour"))
print("       " + "-" * 66)

rows = []
for label, fn in [
    ("1. Street sale, still life (art 2, basic easel)",
     lambda: ev_sale(2, "still_life", "still_life", "street", 0, BASIC)[:2]),
    ("2. Street sale, portrait (art 6, studio easel)",
     lambda: ev_sale(6, "portrait", "canvas", "street", 15, STUDIO)[:2]),
    ("3. Gallery consign, portrait (art 6, rep 15)",
     lambda: ev_sale(6, "portrait", "canvas", "gallery", 15, STUDIO)[:2]),
    ("4. Gallery consign, portrait (art 8, rep 40)",
     lambda: ev_sale(8, "portrait", "canvas", "gallery", 40, STUDIO)[:2]),
    ("5. Gallery consign, portfolio piece (art 8, rep 60)",
     lambda: ev_sale(8, "portrait", "portfolio_piece", "gallery", 60, STUDIO)[:2]),
    ("6. Basic commission, family portrait (art 4)",
     lambda: ev_commission(4, "family_portrait", 8, BASIC)),
    ("7. Basic commission, family portrait (art 6)",
     lambda: ev_commission(6, "family_portrait", 15, STUDIO)),
    ("8. Senior commission, gallery portrait (art 8)",
     lambda: ev_commission(8, "gallery_commission", 30, STUDIO)),
]:
    sess, hourly = fn()
    rows.append((label, sess, hourly))
    print("       %-46s %8.1f %8.1f" % (label, sess, hourly))

print("       " + "-" * 66)
worst = max(rows, key=lambda r: r[2])
print("       highest $/hour path: %s at $%.1f/h" % (worst[0].strip(), worst[2]))

for label, sess, hourly in rows:
    check("EV/h under $%d: %s" % (BENCHMARK, label.split(".")[1].strip()),
          hourly < BENCHMARK, "$%.1f/h" % hourly)

# Exhibition prize EV over its 14-day cooldown.
exh = {"critical_failure": 0, "weak": 0, "success": 60, "great": 120, "critical": 200}
reset(skill_art=6, art_reputation=15)
for it in STUDIO:
    own_and_equip(it) if CAT[it]["slot"] else own(it)
d = G["painting_chance"]("canvas", "portrait")["distribution"]
exh_ev = sum((d[t] / 100.0) * exh[t] for t in TIERS)
print("\n       exhibition prize EV (art 6): $%.0f per 14-day cooldown = $%.1f/week"
      % (exh_ev, exh_ev / 2.0))
check("exhibition prize stays supplemental (<$80/week)", exh_ev / 2.0 < 80, exh_ev / 2.0)

# Weekly ceilings against the corrected Phase 64 baseline.
# Gallery sales AND commission deliveries share the same weekly absorption, so
# the ceiling is 2 full-price pieces a week however the player mixes them.
best_piece = max(rows[3][1], rows[7][1])
painting_week = best_piece * G["ART_MARKET_WEEKLY_SLOTS"]
print("\n       WEEKLY CEILINGS vs corrected Phase 64 baseline")
print("       painting, best 2 pieces/wk (shared throttle)   : $%.0f/week" % painting_week)
print("       repair bench (Phase 61, for comparison)        : $103/week")
print("       catering (Phase 64, for comparison)            : $73/week")
print("       gym class (Phase 64, for comparison)           : $60/week")
print("       freelance prog skill 5 (Phase 63)              : $300-400/week")
check("painting's best weekly total stays below freelance",
      painting_week < 300, "$%.0f/week" % painting_week)
check("painting lands in supplemental territory, not career territory",
      100 < painting_week < 300, "$%.0f/week" % painting_week)

# The shared throttle must be real, not merely documented.
reset(skill_art=8, art_reputation=40)
for _it in STUDIO:
    own_and_equip(_it) if CAT[_it]["slot"] else own(_it)
_c = G["accept_painting_commission"](G["PAINTING_COMMISSIONS"][0])
G["do_commission_work"](_c)
check("a delivered commission consumes a market slot",
      G["art_sales_this_week"]("gallery") == 1)
check("the market is throttled, not just priced",
      G["ART_MARKET_WEEKLY_SLOTS"] <= 2)
check("saturating the market really costs you", G["_ART_SATURATED_MULT"] < 0.5)
check("sale ceiling scales with reputation, not skill",
      G["art_sale_cap"]("gallery") > 0)

reset(art_reputation=0)
cap0 = G["art_sale_cap"]("gallery")
reset(art_reputation=60)
cap60 = G["art_sale_cap"]("gallery")
check("reputation is the lever on sale price", cap60 > cap0 * 2, (cap0, cap60))

# Painting must not out-earn its own purpose.
reset(skill_art=6, art_reputation=15)
for it in STUDIO:
    own_and_equip(it) if CAT[it]["slot"] else own(it)
r = G["do_painting"]("canvas", "portrait")
check("a painting session always yields XP", r["xp"] >= 1)
check("painting sessions never pay money directly", not _money_log)

RENPY.random.fixed = False

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[X] INTEGRATION AND STATE")
# ═══════════════════════════════════════════════════════════════════════════════
loc = src_all["locations.rpy"]
check("home menu has exactly ONE painting entry",
      loc.count("call painting_menu") == 1, loc.count("call painting_menu"))
check("portfolio has an Art section",
      'text "Art"' in io.open(os.path.join(GAME, "portfolio.rpy"), encoding="utf-8").read())
check("home visits surface the displayed-artwork comment",
      "displayed_artwork_comment" in src_all["home_visits.rpy"])

dbg = io.open(os.path.join(GAME, "debug.rpy"), encoding="utf-8").read()
check("debug screen is registered", "debug_p65_scr" in dbg)

# Every Function() wrapper must return None or Ren'Py treats it as a label result.
p65src = psrc + src_all["painting_ui.rpy"]
wrappers = re.findall(r"def (_\w*wrapper)\(", p65src)
bad = []
for w in wrappers:
    body = p65src.split("def " + w + "(")[1].split("\n    def ")[0]
    if re.search(r"^\s+return \S", body, re.M):
        bad.append(w)
check("all Function() wrappers return None", not bad, bad)

# Persistent state must all be declared with `default`.
declared = set(rpy_defaults("painting.rpy"))
for v in ("player_artworks", "painting_mastery", "art_reputation",
          "active_painting_commissions", "_art_sale_log"):
    check("`%s` is a declared default (saves/loads)" % v, v in declared)

print("\n" + "=" * 62)
if failures:
    print("FAILED (%d):" % len(failures))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("Phase 65 self-check: all checks passed.")
