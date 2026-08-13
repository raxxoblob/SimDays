"""Phase 62 runtime self-check.

Unlike the Phase 61 check, this does NOT re-implement the formulas: it EXTRACTS
the real `init python:` blocks out of home_items.rpy / equipment.rpy and execs
them against a stub `store`, so the assertions below run the shipping code. If
someone edits a modifier or a cap, this file fails.

    python phase62_selfcheck.py

Covers spec section 20 tests A-I plus the section 18 economy audit.
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Extract init python blocks from a .rpy file ──────────────────────────────
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


class Store(object):
    """Stand-in for renpy's store. Attribute access only, like the real thing."""
    def __init__(self):
        self.day = 10
        self.hour = 9.0
        self.money = 5000
        self.need_energy = 60
        self.owned_equipment = []
        self.equipment_condition = {}
        self.home_slots = {}
        self.wardrobe_equipped = {}
        self.savings_target = None
        self.guitar_strings_last_refreshed = -999
        self._morning_item_used = None
        self._home_ambient_day = -1
        self._home_ambient_tier = -1
        self._p62_home_flavor = ""
        self.own_guitar = False
        self.own_computer = True
        self.own_coffee_machine = False
        self.own_kitchen_set = False
        self.own_bed = False


G = {}          # the shared "global script namespace"
store = Store()


def _try_spend(amount, category="discretionary", toast=True):
    if amount <= 0:
        return True
    if store.money < amount:
        return False
    store.money -= amount
    return True


def _record_game_event(*a, **k):
    return None


def boot():
    """Load equipment.rpy then home_items.rpy python into one namespace."""
    global G
    G = {"store": store, "try_spend": _try_spend, "record_game_event": _record_game_event,
         "skill_val": lambda s: 5, "__builtins__": __builtins__}
    for path in ("equipment.rpy", "home_items.rpy"):
        for blk in rpy_python_blocks(path):
            exec(compile(blk, path, "exec"), G)
    # init 1 block in home_items.rpy sets _FREE_ITEMS; make sure it ran
    assert G["_FREE_ITEMS"], "_FREE_ITEMS never populated"


failures = []


def check(name, cond, extra=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("  -> " + str(extra)) if extra and not cond else ""))
    if not cond:
        failures.append(name)


def reset():
    global store
    store.__init__()
    G["store"] = store


boot()
CAT = G["ITEM_CATALOG"]

# ── Catalog integrity ────────────────────────────────────────────────────────
print("\n[CATALOG]")
check("at least 60 named items (have %d)" % len(CAT), len(CAT) >= 60)
check("every item has a label, description and price",
      all(d["label"] and d["description"] and d["price_new"] >= 0 for d in CAT.values()))
check("no item grants a skill level",
      not any(k.startswith("skill") or k.endswith("_level")
              for d in CAT.values() for k in d["modifiers"]))

by_cat = {}
for i, d in CAT.items():
    by_cat.setdefault(d["category"], []).append(i)
for c in sorted(by_cat):
    print("       %-12s %d" % (c, len(by_cat[c])))
# Phase 65 added the "studio" category (art_station items). 8 -> 9.
check("all 9 categories populated", len(by_cat) == 9, sorted(by_cat))

# every slotted item resolves to a real room+slot
bad = [i for i, d in CAT.items() if d["slot"] and d["category"] != "wardrobe"
       and G["item_room_slot"](i)[0] is None]
check("every slotted item maps to a room", not bad, bad)
bad = [i for i, d in CAT.items() if d["slot"] and d["category"] != "wardrobe"
       and d["slot"] not in G["HOME_ROOM_SLOTS"][G["item_room_slot"](i)[0]]]
check("every item's slot exists in its room", not bad, bad)

# ── Caps (spec 15: nothing exceeds Phase 61's ceilings) ──────────────────────
print("\n[CAPS]")
reset()
for i in CAT:
    G["grant_item"](i, "Excellent")
    G["equip_item"](i)
frac_over = {k: v for k in ("project_energy", "prog_xp", "music_energy", "cook_time")
             for v in [G["equipment_modifier"]({"project_energy": "computer", "prog_xp": "computer",
                                                "music_energy": "guitar", "cook_time": "kitchen"}[k], k)]
             if v > G["_EQUIP_FRAC_CAP"] + 1e-9}
check("fractional modifiers respect the 15%% cap even fully kitted", not frac_over, frac_over)
pts = {c: G["equipment_modifier"](c, e) for c, e in
       (("guitar", "busk_perf"), ("kitchen", "cook_quality"), ("tools", "repair_chance"))}
check("point modifiers respect the 15-point cap", all(v <= G["_EQUIP_POINT_CAP"] for v in pts.values()), pts)
print("       fully-kitted totals: %s" % pts)
check("sleep_recovery capped at +25%%", G["sleep_recovery_modifier"]() <= 0.25 + 1e-9,
      G["sleep_recovery_modifier"]())
check("home_social_quality capped at 30", G["home_social_quality"]() <= 30, G["home_social_quality"]())
check("home_visual_tier never exceeds 4", G["home_visual_tier"]() == 4, G["home_visual_tier"]())

# ── A. Purchase / equip / persistence ───────────────────────────────────────
print("\n[A: purchase flow]")
reset()
store.money = 600
check("cannot equip an unowned item", G["equip_item"]("quality_mattress") is False)
before = store.money
check("buy_item succeeds", G["buy_item"]("quality_mattress") is True)
check("try_spend charged the retail price", store.money == before - CAT["quality_mattress"]["price_new"],
      store.money)
check("item is in the (single, shared) inventory", "quality_mattress" in store.owned_equipment)
check("owns_item agrees", G["owns_item"]("quality_mattress"))
check("not equipped until asked", not G["is_equipped"]("quality_mattress"))
check("equip_item works", G["equip_item"]("quality_mattress") is True)
check("is_equipped now True", G["is_equipped"]("quality_mattress"))
check("modifier is live", G["sleep_recovery_modifier"]() > 0, G["sleep_recovery_modifier"]())
check("cannot buy the same item twice", G["buy_item"]("quality_mattress") is False)
check("cannot buy what you cannot afford", G["can_buy_item"]("desktop_workstation") is False)

# save/load: everything Phase 62 needs lives in plain `default` vars
saved = dict(home_slots={k: dict(v) for k, v in store.home_slots.items()},
             owned_equipment=list(store.owned_equipment),
             equipment_condition=dict(store.equipment_condition),
             wardrobe_equipped=dict(store.wardrobe_equipped))
reset()
for k, v in saved.items():
    setattr(store, k, v)
check("equipped item survives a save/load round trip", G["is_equipped"]("quality_mattress"))
check("modifier survives a save/load round trip", G["sleep_recovery_modifier"]() > 0)

defaults = re.findall(r"^default\s+(\w+)", io.open(os.path.join(GAME, "home_items.rpy"),
                                                   encoding="utf-8").read(), re.M)
check("all new persistent state has a `default`",
      set(["home_slots", "wardrobe_equipped", "savings_target",
           "guitar_strings_last_refreshed"]) <= set(defaults), defaults)

# ── B. Modifier preview matches the live value ──────────────────────────────
print("\n[B: modifier preview]")
reset()
store.money = 9999
G["buy_item"]("quality_mattress"); G["equip_item"]("quality_mattress")
live_before = G["sleep_recovery_modifier"]()
G["buy_item"]("premium_bed")
preview = dict((lbl, val) for lbl, val in G["equip_delta"]("premium_bed"))
check("preview shows a delta for the better bed", "Sleep recovery" in preview, preview)
predicted = live_before + float(preview["Sleep recovery"].strip("+%")) / 100.0
G["equip_item"]("premium_bed")
live_after = G["sleep_recovery_modifier"]()
check("previewed delta == actual change (%.3f vs %.3f)" % (predicted, live_after),
      abs(predicted - live_after) < 0.011)
check("swapping back down shows a negative delta",
      any(v.startswith("-") for _, v in G["equip_delta"]("quality_mattress")),
      G["equip_delta"]("quality_mattress"))
check("current occupant is reported", G["current_slot_occupant_label"]("quality_mattress") == "Platform Bed + Mattress",
      G["current_slot_occupant_label"]("quality_mattress"))

# ── C. Home visual state ────────────────────────────────────────────────────
print("\n[C: visual tier]")
reset()
check("bare flat is tier 0", G["home_visual_tier"]() == 0, G["home_visual_tier"]())
check("tier 0 flavour text", G["home_visual_text"]().startswith("The apartment is almost empty"))
check("ambient fires once per day", G["check_home_ambient"]() is True)
check("ambient does not repeat the same day at the same tier", G["check_home_ambient"]() is False)
tiers = [0]
for group in (["double_bed", "desk_lamp", "basic_sofa", "small_tv", "basic_decor"],
              ["quality_mattress", "blackout_curtains", "good_sofa", "mid_tv", "nice_decor"],
              ["premium_bed", "smart_lighting", "ac_unit", "sectional_sofa", "large_tv",
               "curated_decor", "plants_set", "record_player", "bookshelf"]):
    for i in group:
        G["grant_item"](i, "Excellent"); G["equip_item"](i)
    tiers.append(G["home_visual_tier"]())
check("visual tier rises monotonically %s" % tiers, tiers == sorted(tiers) and tiers[-1] > tiers[0])
check("fully furnished reaches tier 3+", tiers[-1] >= 3, tiers)
check("flavour text tracks the tier", G["home_visual_text"]() == G["HOME_VISUAL_FLAVOR"][tiers[-1]])
check("ambient re-fires when the tier changes", G["check_home_ambient"]() is True)

# ── D. Sleep recovery ───────────────────────────────────────────────────────
print("\n[D: sleep recovery]")
reset()
check("bare bedroom = no bonus", G["sleep_recovery_modifier"]() == 0)


def morning_energy():
    """Mirrors the new_day() block in data.rpy (the only duplicated formula)."""
    base = 100 if store.own_bed else 95
    m = G["sleep_recovery_modifier"]()
    return min(100, int(base * (1.0 + m))), int(round(15 * (1.0 - m)))


base_e, base_hunger = morning_energy()
for i in ("quality_mattress", "blackout_curtains", "ac_unit"):
    G["grant_item"](i, "Excellent"); G["equip_item"](i)
up_e, up_hunger = morning_energy()
check("sleep_recovery_modifier increases (%.2f)" % G["sleep_recovery_modifier"](),
      G["sleep_recovery_modifier"]() > 0.2)
check("morning energy is higher (%d -> %d)" % (base_e, up_e), up_e > base_e)
check("overnight hunger loss is lower (%d -> %d)" % (base_hunger, up_hunger), up_hunger < base_hunger)
check("6h partial sleep scales up (60 -> %d)" %
      int(round(60 * (1 + G["sleep_recovery_modifier"]()))),
      int(round(60 * (1 + G["sleep_recovery_modifier"]()))) > 60)
store.hour = 27.0   # up past 2am
check("blackout curtains add a late-night bonus",
      G["sleep_recovery_modifier"]() >= 0.25 - 1e-9)
store.hour = 9.0

# ── E. Home social quality ──────────────────────────────────────────────────
print("\n[E: home social]")
reset()
check("bare living room scores 0", G["home_social_quality"]() == 0)
check("bare living room gives no visit bonus", G["home_social_bonus"]() == 0)
for i in ("good_sofa", "mid_tv"):
    G["grant_item"](i, "Excellent"); G["equip_item"](i)
q1 = G["home_social_quality"]()
check("good sofa + mid TV raises the score (%d)" % q1, q1 >= 9)
check("that is a real visit bonus", G["home_social_bonus"]() >= 1, G["home_social_bonus"]())
for i in ("sectional_sofa", "large_tv", "curated_decor", "record_player"):
    G["grant_item"](i, "Excellent"); G["equip_item"](i)
q2 = G["home_social_quality"]()
check("upgrading raises it further (%d -> %d)" % (q1, q2), q2 > q1)
check("best tier reached", G["home_social_tier"]() == 3, G["home_social_tier"]())
check("visit bonus stays small (<=3)", G["home_social_bonus"]() <= 3)
check("dinner threshold (>=12) is reachable", q2 >= 12)

# ── F. Second-hand condition scaling ────────────────────────────────────────
print("\n[F: marketplace / condition]")
reset()
G["grant_item"]("pro_cookware", "Excellent"); G["equip_item"]("pro_cookware")
exc = G["equipment_modifier"]("kitchen", "cook_quality")
store.equipment_condition["pro_cookware"] = "Poor"
poor = G["equipment_modifier"]("kitchen", "cook_quality")
check("Poor condition scales the bonus down (%d -> %d)" % (exc, poor), poor < exc)
check("Poor is roughly half of Excellent", abs(poor - exc * 0.5) <= 1, (poor, exc))
store.equipment_condition["pro_cookware"] = "Good"
check("restoring the condition restores the bonus",
      G["equipment_modifier"]("kitchen", "cook_quality") > poor)
used_ok = [i for i, d in CAT.items() if d["available_used"]]
check("enough catalog items can appear used (%d)" % len(used_ok), len(used_ok) >= 40)
check("free default items never appear used",
      not any(CAT[i]["price_new"] == 0 for i in used_ok))
check("price_used is below price_new for every item",
      all(d["price_used"] < d["price_new"] for d in CAT.values() if d["price_new"] > 0))

# ── G. Guitar strings ───────────────────────────────────────────────────────
print("\n[G: guitar strings]")
reset()
store.money = 500
G["grant_item"]("cedar_acoustic", "Excellent"); G["equip_item"]("cedar_acoustic")
check("untouched strings are neutral", G["strings_modifier"]() == 0)
check("can afford a set", G["can_refresh_strings"]() is True)
m0 = store.money
check("refresh succeeds", G["refresh_strings"]() is True)
check("refresh cost $%d" % G["GUITAR_STRINGS_COST"], store.money == m0 - G["GUITAR_STRINGS_COST"])
check("fresh strings give +4", G["strings_modifier"] () == 4, G["strings_modifier"]())
check("state text mentions fresh", "fresh" in G["strings_state_text"]())
store.day += 8
check("8 days later strings are stale: -3", G["strings_modifier"]() == -3, G["strings_modifier"]())
check("state text mentions worn", "worn" in G["strings_state_text"]())
store.day -= 1
check("day 7 is still fresh", G["strings_modifier"]() == 4)

# ── Morning routine ─────────────────────────────────────────────────────────
print("\n[morning routine]")
reset()
check("no appliance = nothing to use", G["morning_item"]() is None)
G["grant_item"]("coffee_maker", "Excellent"); G["equip_item"]("coffee_maker")
check("coffee maker is the morning item", G["morning_item"]() == "coffee_maker")
store.hour = 9.0
store.need_energy = 50
check("available in the morning", G["morning_item_available"]() is True)
res = G["use_morning_item"]()
check("gives +5 energy", res == ("Drip Coffee Maker", 5), res)
check("energy actually applied", store.need_energy == 55, store.need_energy)
check("only once per day", G["morning_item_available"]() is False)
check("second use returns None", G["use_morning_item"]() is None)
store.day += 1
check("available again the next day", G["morning_item_available"]() is True)
store.hour = 15.0
check("not available in the afternoon", G["morning_item_available"]() is False)
store.hour = 9.0
G["grant_item"]("espresso_machine", "Excellent"); G["equip_item"]("espresso_machine")
store.need_energy = 50
check("espresso machine replaces it and gives +8",
      G["use_morning_item"]() == ("Espresso Machine", 8), G["morning_item"]())

# ── H. Completionist / cosmetic items ───────────────────────────────────────
print("\n[H: cosmetic items]")
reset()
store.money = 500
t0 = G["home_visual_tier"]()
for i in ("plants_set", "art_print"):
    check("buying %s works" % i, G["buy_item"](i) is True)
    check("%s has no stat return" % i, not CAT[i]["modifiers"])
    check("%s is owned" % i, G["owns_item"](i))
    check("%s has no slot, equipping is a no-op" % i, G["equip_item"](i) is False)
    check("%s shows no modifier lines" % i, G["item_modifier_lines"](i) == [])
    check("%s produces no delta and does not crash" % i, G["equip_delta"](i) == [])
check("owned_home_items lists them", set(["plants_set", "art_print"]) <= set(G["owned_home_items"]()))
# In a part-furnished flat, cosmetics with zero stats still move the visual tier.
reset()
store.money = 9999
for i in ("double_bed", "desk_lamp", "basic_sofa", "small_tv", "basic_decor"):
    G["grant_item"](i, "Excellent"); G["equip_item"](i)
t_bare = G["home_visual_score"]()
for i in ("plants_set", "art_print", "bookshelf", "smart_speaker", "coffee_grinder"):
    G["buy_item"](i)
t_deco = G["home_visual_score"]()
check("stat-free cosmetics raise the visual score (%.2f -> %.2f)" % (t_bare, t_deco),
      t_deco - t_bare >= 0.7)
check("enough cosmetics eventually flip the tier",
      G["home_visual_tier"]() > 0 and t_deco + 0.35 >= 1.0)

# ── Wardrobe ────────────────────────────────────────────────────────────────
print("\n[wardrobe]")
reset()
store.money = 2000
check("everyone starts with a default casual outfit",
      G["wardrobe_equipped_in"]("casual") == "basic_casual")
check("underdressed for a formal event is a penalty, not a block",
      G["dressed_for"]("formal") == -3, G["dressed_for"]("formal"))
check("underdressed casually costs nothing", G["dressed_for"]("casual") >= 0)
G["buy_item"]("formal_outfit"); G["equip_item"]("formal_outfit")
check("owning formalwear turns the penalty into a bonus",
      G["dressed_for"]("formal") > 0, G["dressed_for"]("formal"))
G["buy_item"]("performance_jacket"); G["equip_item"]("performance_jacket")
check("stage clothes help a performance", G["dressed_for"]("music_performance") > 0)
c0 = G["wardrobe_confidence"]()
G["buy_item"]("nice_casual"); G["equip_item"]("nice_casual")
G["buy_item"]("premium_watch"); G["equip_item"]("premium_watch")
check("everyday confidence rises (%d -> %d)" % (c0, G["wardrobe_confidence"]()),
      G["wardrobe_confidence"]() > c0)
check("confidence stays capped at 8", G["wardrobe_confidence"]() <= 8)
check("clothes never decay: no durability key in any wardrobe item",
      not any("durab" in k or "wear" in k for i in by_cat["wardrobe"] for k in CAT[i]["modifiers"]))

# ── Savings target ──────────────────────────────────────────────────────────
print("\n[savings target]")
reset()
check("no target by default", G["savings_target_text"]() is None)
G["_set_savings_target"]("large_tv")
txt = G["savings_target_text"]()
check("target text renders", txt and "Large" not in txt and "65" in txt, txt)
check("target text shows both numbers", "$1100" in txt and "$5000" in txt, txt)
G["_set_savings_target"]("large_tv")
check("setting the same target again clears it", G["savings_target_text"]() is None)
G["_set_savings_target"]("large_tv")
store.money = 5000
G["buy_item"]("large_tv")
check("buying the target clears it", store.savings_target is None)
expensive = [i for i, d in CAT.items() if d["price_new"] >= 800 and d["shop_available"]]
check("there are save-goal-worthy items (%d)" % len(expensive), len(expensive) >= 5)

# ── Integration wiring (grep-level: the hooks are actually connected) ───────
print("\n[integration]")


def has(path, needle):
    return needle in io.open(os.path.join(GAME, path), encoding="utf-8").read()


check("new_day() applies sleep_recovery_modifier", has("data.rpy", "sleep_recovery_modifier()"))
check("partial sleep scales too", has("locations.rpy", "1.0 + sleep_recovery_modifier()"))
check("busking reads the strings modifier", has("busking.rpy", "strings_modifier()"))
check("open mic reads stage clothes", has("busking.rpy", 'dressed_for("music_performance")'))
check("cooking respects the cookware ceiling", has("cooking.rpy", "recipe_difficulty_max"))
check("home visits apply the quality bonus", has("home_visits.rpy", "home_visit_quality_bonus"))
check("dinner-at-home threshold is wired", has("home_visits.rpy", "home_social_quality() >= 12"))
check("marketplace seeds from the catalog", has("marketplace.rpy", "_seed_market_pool_from_catalog"))
check("marketplace shows repair eligibility", has("marketplace.rpy", "Mechanics 4+"))
check("phone registers the Home app", has("phone.rpy", 'Show("home_shop_scr")'))
check("phone shows the savings chip", has("phone.rpy", "savings_target_text()"))
check("home menu offers the morning drink", has("locations.rpy", "morning_item_available()"))
check("home menu offers the room overview", has("locations.rpy", "home_rooms_scr"))
check("debug screen is registered", has("debug.rpy", "debug_p62_scr"))
check("event prep is optional and shared with the preview",
      has("city_challenges.rpy", "_city_chal_mods(") and has("city_challenges.rpy", "buy_event_prep"))
# Spec 19: every function used as a Function() screen ACTION must return None,
# otherwise Ren'Py treats the value as a result and can exit the current label.
NEWFILES = ["home_items.rpy", "home_items_ui.rpy", "marketplace.rpy",
            "city_challenges.rpy", "home_upgrades.rpy"]
allsrc = "\n".join(io.open(os.path.join(GAME, f), encoding="utf-8").read() for f in NEWFILES)
action_fns = set(re.findall(r"Function\(\s*(_[A-Za-z]\w*)", allsrc))
offenders = []
for fn in sorted(action_fns):
    m = re.search(r"^(\s*)def %s\(.*?\):\n((?:\1\s+.*\n|\s*\n)*)" % re.escape(fn), allsrc, re.M)
    if m and re.search(r"^\s+return\s+\S", m.group(2), re.M):
        offenders.append(fn)
check("all %d Function() action wrappers return None" % len(action_fns), not offenders, offenders)
check("Function() wrappers were actually found", len(action_fns) >= 5, action_fns)

# workspace quality drives the study-together modifier
reset()
check("bare workspace gives no study bonus", G["study_focus_modifier"]() == 0)
for i in ("large_desk", "desktop_workstation"):
    G["grant_item"](i, "Excellent"); G["equip_item"](i)
check("a real workspace gives a small study bonus (%d)" % G["study_focus_modifier"](),
      1 <= G["study_focus_modifier"]() <= 4)

# ── I. Economy audit (spec 13 + 18) ─────────────────────────────────────────
print("\n[I: economy audit]")
reset()
BANDS = [(1, 40), (40, 150), (150, 400), (400, 900), (900, 2000), (2000, 5000)]
for lo, hi in BANDS:
    n = [i for i, d in CAT.items() if d["shop_available"] and lo <= d["price_new"] < hi]
    print("       $%-4d-%-4d  %2d items   e.g. %s" %
          (lo, hi, len(n), ", ".join(CAT[i]["label"] for i in sorted(n, key=lambda x: CAT[x]["price_new"])[:3])))
    check("band $%d-%d has 3+ options" % (lo, hi), len(n) >= 3, len(n))

# minimum "meaningfully equipped": cheapest non-default item per gameplay slot
GAMEPLAY_SLOTS = [("bedroom", "bed"), ("bedroom", "lighting"),
                  ("workspace", "desk"), ("workspace", "computer"), ("workspace", "chair"),
                  ("kitchen", "cookware"), ("kitchen", "appliance_small"),
                  ("music_corner", "instrument"), ("workshop", "tools"),
                  ("living_room", "seating"), ("living_room", "display"),
                  ("living_room", "decor_level")]


def slot_items(room, slot):
    return [i for i, d in CAT.items() if d["slot"] == slot and G["_room_for_item"](i) == room
            and d["price_new"] > 0 and d["shop_available"]]


minimum = sum(min(CAT[i]["price_new"] for i in slot_items(r, s)) for r, s in GAMEPLAY_SLOTS)
best_per_slot = sum(max(CAT[i]["price_new"] for i in slot_items(r, s)) for r, s in GAMEPLAY_SLOTS)
everything = sum(d["price_new"] for d in CAT.values() if d["shop_available"])
lifestyle = sum(CAT[i]["price_new"] for i in by_cat["lifestyle"])
wardrobe_all = sum(CAT[i]["price_new"] for i in by_cat["wardrobe"])
print("       minimum meaningfully equipped : $%d" % minimum)
print("       best item in every slot       : $%d" % best_per_slot)
print("       every lifestyle item          : $%d" % lifestyle)
print("       every wardrobe item           : $%d" % wardrobe_all)
print("       buy the entire catalogue      : $%d" % everything)

# Weekly income reference points taken from the shipping economy.
WEEKLY = [("early (busking + odd jobs)", 180), ("mid (junior freelance)", 520),
          ("late (senior/corporate)", 1250)]
for lbl, wk in WEEKLY:
    print("       %-28s minimum kit = %.1f weeks | full slots = %.1f weeks | everything = %.1f weeks"
          % (lbl, minimum / float(wk), best_per_slot / float(wk), everything / float(wk)))
check("minimum kit is reachable inside ~2 months of early income", minimum / 180.0 <= 9,
      minimum / 180.0)
check("fully kitted stays aspirational for a mid-game player", best_per_slot / 520.0 >= 8,
      best_per_slot / 520.0)
check("the catalogue outlasts late-game income", everything / 1250.0 >= 10, everything / 1250.0)

# meaningful choice at every wealth level
print("\n       affordable options at each wealth level:")
for wealth in (60, 200, 500, 1200, 3000, 8000):
    reset()
    store.money = wealth
    n = G["affordable_item_count"]()
    print("         $%-5d -> %2d buyable items" % (wealth, n))
    check("player with $%d has 3-5+ meaningful choices" % wealth, n >= 3, n)

# ── Phase 62 adds no income ─────────────────────────────────────────────────
print("\n[no income]")
src = io.open(os.path.join(GAME, "home_items.rpy"), encoding="utf-8").read()
check("home_items.rpy never calls gain_money with a positive amount",
      not re.search(r"gain_money\(\s*(?!-)", src))
check("no resale path was added", "sell" not in src.lower().replace("sells", ""))

# ── Result ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 62)
if failures:
    print("FAILED (%d):" % len(failures))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("Phase 62 self-check: all checks passed.")
