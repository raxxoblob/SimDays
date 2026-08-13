"""Phase 69 runtime self-check — possessions, personal bests, accomplishments.

Same approach as phase62/64/65: EXTRACTS the real `init python:` blocks out of
possessions.rpy / resolution_checks.rpy / city_events.rpy / city_challenges.rpy
and execs them against a stub `store`, so every assertion below runs the
SHIPPING code. Change a catalog entry, a preparation bonus or a reward table and
this fails.

    python phase69_selfcheck.py

The init-20 wrapper block in possessions.rpy is deliberately NOT executed here:
it rebinds functions owned by eight other systems and only makes sense inside a
running game. The debug screen (debug_p69.rpy) asserts those wrappers are live.
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
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)\s*(?:#.*)?$", src, re.M):
        try:
            out[m.group(1)] = eval(m.group(2), {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


DEFAULTS = {}
DEFAULTS.update(rpy_defaults("possessions.rpy"))
DEFAULTS.update(rpy_defaults("city_events.rpy"))
DEFAULTS.update(rpy_defaults("city_challenges.rpy"))
DEFAULTS.update(rpy_defaults("world_challenges.rpy"))


class Store(object):
    """Deliberately does NOT predeclare the Phase 69 variables — they come from
    `default` lines only, so a missing default shows up as an AttributeError
    here instead of a KeyError in someone's save."""

    def __init__(self):
        self.day = 30
        self.hour = 12.0
        self.money = 500
        self.loan = 0
        self.need_energy = 80
        self.art_reputation = 0
        self.freelance_reputation = 0
        self.freelance_history = []
        self.bar_first_wins = []
        self.bar_game_cooldowns = {}
        self.city_event_schedule = []
        self.player_artworks = []
        self.active_careers = {}
        self.job_id = None
        self.job_title = ""
        self._check_pity = {}
        self._check_attempts = {}
        self._challenge_prepped = -1
        for k in ("cook", "fit", "art", "prog", "mech", "music", "biz"):
            setattr(self, "skill_" + k, 5)
        for k, v in DEFAULTS.items():
            setattr(self, k,
                    list(v) if isinstance(v, list) else
                    dict(v) if isinstance(v, dict) else v)


class _Rand(object):
    def randint(self, a, b):
        import random
        return random.randint(a, b)

    def random(self):
        import random
        return random.random()

    def choice(self, seq):
        import random
        return random.choice(seq)


class _Config(object):
    developer = False


class _Renpy(object):
    random = _Rand()
    config = _Config()

    def notify(self, *a, **k):
        return None

    def log(self, *a, **k):
        return None

    def loadable(self, path):
        return os.path.exists(os.path.join(GAME, path))


store = Store()
RENPY = _Renpy()
_events = []
_money_log = []
G = {}


def boot():
    global G
    G = {
        "store": store, "renpy": RENPY,
        "record_game_event": lambda eid, cat, title, **k: _events.append((eid, cat, title)),
        "gain_money": lambda amt, cat="discretionary": _money_log.append((amt, cat)),
        "try_spend": lambda amt, cat="discretionary", toast=True: True,
        "gain_skill": lambda k, a=1: None,
        "gain_skill_practice": lambda k, x, h=1: x,
        "gain_art_rep": lambda n: None,
        "spend_time": lambda h: None,
        "skill_val": lambda k: getattr(store, "skill_" + k, 0),
        "has_player_state": lambda s: False,
        "add_player_state": lambda *a, **k: None,
        "submitted_artwork_for": lambda eid: None,
        "exhibition_submission_bonus": lambda eid: None,
        "update_artwork": lambda *a, **k: None,
        "PRO_SKILLS": {},
        "__builtins__": __builtins__,
    }
    for path in ("resolution_checks.rpy", "city_events.rpy"):
        for blk in rpy_python_blocks(path):
            try:
                exec(compile(blk, path, "exec"), G)
            except Exception as e:
                print("       (skipped a %s block: %s)" % (path, e))
    for blk in rpy_python_blocks("city_challenges.rpy", priority=1):
        exec(compile(blk, "city_challenges.rpy", "exec"), G)
    for blk in rpy_python_blocks("possessions.rpy"):
        exec(compile(blk, "possessions.rpy", "exec"), G)


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
    del _events[:], _money_log[:]


boot()
CAT = G["POSSESSION_CATALOG"]
grant = G["grant_possession"]
has = G["has_possession"]

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[A] CATALOG")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
check("A1 catalog has 12+ entries", len(CAT) >= 12, len(CAT))
check("A2 every entry has name/category/hint",
      all(d.get("name") and d.get("category") and d.get("hint") for d in CAT.values()))
check("A3 every icon_key exists in POSSESSION_ICONS",
      all(d["icon_key"] in G["POSSESSION_ICONS"] for d in CAT.values()))
check("A4 keepsakes are never sellable",
      all(not d.get("sellable") for d in CAT.values() if d["category"] == "keepsake"))
check("A5 sellable items carry a positive value",
      all(d.get("sell_value", 0) > 0 for d in CAT.values() if d.get("sellable")))
_wired = set(G["CITY_CHALLENGE_KEEPSAKES"].values()) | \
         set(G["WORLD_CHALLENGE_KEEPSAKES"].values()) | \
         set(G["BAR_FIRST_WIN_KEEPSAKES"].values()) | \
         {"promotion_certificate", "first_paid_gig_stub", "freelance_client_card",
          "mechanics_restoration_badge", "festival_wristband",
          "art_market_vendor_card", "rare_vintage_coin",
          # granted by the rare-outcome layer (rare_outcomes.rpy, init 25)
          "musician_contact_card"}
check("A6 every catalog item has a grant path",
      not [i for i in CAT if i not in _wired], [i for i in CAT if i not in _wired])
check("A7 every keepsake target exists in the catalog",
      all(k in CAT for k in _wired), [k for k in _wired if k not in CAT])

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[B] GRANTING")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
check("B1 unknown item_id is refused, not raised", grant("nope_not_real", "test") is False)
check("B2 first grant succeeds", grant("pool_trophy", "test") is True)
check("B3 has_possession sees it", has("pool_trophy"))
check("B4 second grant of a unique item is refused",
      grant("pool_trophy", "other_source") is False)
check("B5 still exactly one instance", len(store.player_possessions) == 1)
check("B6 force=True bypasses uniqueness (debug only)",
      grant("pool_trophy", "debug", force=True) is True)

reset()
check("B7 non-unique item grants once per source",
      grant("freelance_client_card", "client_a") is True)
check("B8 same source is deduplicated",
      grant("freelance_client_card", "client_a") is False)
check("B9 a different source grants again",
      grant("freelance_client_card", "client_b") is True)
check("B10 two instances now exist", len(store.player_possessions) == 2)
check("B11 instance ids are unique",
      len({p["id"] for p in store.player_possessions}) == 2)

reset()
grant("pool_trophy", "t")
grant("rare_vintage_coin", "t")
check("B12 get_possessions_by_category('keepsake')",
      [p["item_id"] for p in G["get_possessions_by_category"]("keepsake")] == ["pool_trophy"])
check("B13 get_possessions_by_category('collectible')",
      [p["item_id"] for p in G["get_possessions_by_category"]("collectible")] == ["rare_vintage_coin"])
check("B14 unearned list excludes what you own",
      "pool_trophy" not in [i for i, _d in G["unearned_possessions"]()])

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[C] FEATURING AND SELLING")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
grant("rare_vintage_coin", "t")
_iid = store.player_possessions[0]["id"]
check("C1 feature returns True", G["feature_possession"](_iid, True))
check("C2 featured flag is persisted", store.player_possessions[0]["featured"] is True)
check("C3 get_featured_possessions", len(G["get_featured_possessions"]()) == 1)
check("C4 a featured item cannot be sold", G["sell_possession"](_iid) == 0)
check("C5 it is still owned", has("rare_vintage_coin"))
G["feature_possession"](_iid, False)
check("C6 unfeatured item sells for its catalog value",
      G["sell_possession"](_iid) == CAT["rare_vintage_coin"]["sell_value"])
check("C7 it is gone from the store", not has("rare_vintage_coin"))
check("C8 the cash actually landed",
      _money_log and _money_log[-1][0] == CAT["rare_vintage_coin"]["sell_value"])
reset()
grant("pool_trophy", "t")
check("C9 an unsellable keepsake yields nothing",
      G["sell_possession"](store.player_possessions[0]["id"]) == 0)
check("C10 selling an unknown instance is a no-op", G["sell_possession"]("nope") == 0)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[D] PERSONAL BESTS")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
pb = G["record_personal_best"]
check("D1 first value is always a best", pb("highest_busking_tips", 40, "higher"))
check("D2 a lower value is not", pb("highest_busking_tips", 20, "higher") is False)
check("D3 a higher value is", pb("highest_busking_tips", 84, "higher"))
check("D4 stored value is the best", store.player_personal_bests["highest_busking_tips"] == 84)
check("D5 'lower' comparison works", pb("fastest", 30, "lower") and
      pb("fastest", 10, "lower") and pb("fastest", 20, "lower") is False)
check("D6 tier comparison ranks upward",
      pb("best_open_mic_tier", "success", "tier") and
      pb("best_open_mic_tier", "great", "tier") and
      pb("best_open_mic_tier", "weak", "tier") is False)
check("D7 rating comparison ranks D..S",
      pb("best_freelance_rating", "B", "rating") and
      pb("best_freelance_rating", "S", "rating") and
      pb("best_freelance_rating", "A", "rating") is False)
check("D8 None is ignored", pb("whatever", None) is False)
check("D9 an unknown tier string is ignored, not ranked",
      pb("best_open_mic_tier", "banana", "tier") is False)
check("D10 an unknown tier as the FIRST value is also ignored",
      pb("brand_new_key", "banana", "tier") is False)
check("D11 personal_best_display renders a tier as its label",
      G["personal_best_display"]("best_open_mic_tier")[1] == "Great Success")
check("D12 personal_best_display returns None for an unset key",
      G["personal_best_display"]("never_set") is None)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[E] ACCOMPLISHMENTS")
# ═══════════════════════════════════════════════════════════════════════════════
reset()
acc = G["record_accomplishment"]
check("E1 first record succeeds", acc("first_promo", "First Promotion", "d", "career"))
check("E2 duplicate id is refused", acc("first_promo", "x", "y", "career") is False)
check("E3 exactly one entry", len(store.player_accomplishments) == 1)
check("E4 the day is stamped", store.player_accomplishments[0]["day"] == store.day)
acc("won_cookoff", "Cook-Off", "d", "culinary")
check("E5 filter by category",
      [a["id"] for a in G["accomplishments_by_category"]("career")] == ["first_promo"])
check("E6 unfiltered is newest-first",
      [a["id"] for a in G["accomplishments_by_category"]()] == ["won_cookoff", "first_promo"])

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[F] PREPARATION AND ODDS")
# ═══════════════════════════════════════════════════════════════════════════════
reset(need_energy=80)
check("F1 rested contributes the rest bonus",
      ("Rested", G["PREPARATION_BONUSES"]["rest_well"]) in G["preparation_mods"]("cook"))
reset(need_energy=40)
check("F2 tired contributes nothing", G["preparation_mods"]("cook") == [])
check("F3 the hint tells you what you are missing",
      any("rested" in h for h in G["preparation_hints"]("cook")))
reset(need_energy=80)
store._p69_last_practice = {"cook": store.day - 1}
check("F4 recent practice counts", G["prep_practiced_recently"]("cook"))
store._p69_last_practice = {"cook": store.day - 9}
check("F5 stale practice does not", not G["prep_practiced_recently"]("cook"))
check("F6 no skill key -> no practice bonus", not G["prep_practiced_recently"](None))
check("F7 total preparation is bounded at +8",
      sum(G["PREPARATION_BONUSES"].values()) == 8, sum(G["PREPARATION_BONUSES"].values()))

# The preview and the roll must read the SAME numbers. Both call
# calculate_check_chance / roll_check with identical arguments, so it is enough
# to prove the distribution the app would show is a real probability mass.
reset(need_energy=80)
_spec = [t for t in G["CITY_CHALLENGE_TEMPLATES"] if t["id"] == "cook_off"][0]["challenge"]
_dist = G["calculate_check_chance"]("prev_cook_off", 5, _spec["difficulty"],
                                    G["preparation_mods"]("cook"))
check("F8 odds preview returns a full tier distribution",
      set(_dist["distribution"]) == {"critical_failure", "weak", "success", "great", "critical"})
check("F9 the distribution sums to 100",
      sum(_dist["distribution"].values()) == 100, sum(_dist["distribution"].values()))
check("F10 preparation raises the odds",
      G["calculate_check_chance"]("prev_cook_off", 5, _spec["difficulty"],
                                  G["preparation_mods"]("cook"))["success_or_better"]
      > G["calculate_check_chance"]("prev_cook_off", 5, _spec["difficulty"], [])["success_or_better"])

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[G] ECONOMY — EV/hour of every city challenge, fully prepared")
# ═══════════════════════════════════════════════════════════════════════════════
reset(need_energy=80)
TIERS = ["critical_failure", "weak", "success", "great", "critical"]
BENCH = 40.0
for t in G["CITY_CHALLENGE_TEMPLATES"]:
    ch = t["challenge"]
    mods = [("Prepared", 5), ("Preparation", sum(G["PREPARATION_BONUSES"].values()))]
    if t["id"] == "art_exhibition":
        mods.append(("Submitted piece", 10))   # best case: a critical-quality entry
    dist = G["calculate_check_chance"]("ev_" + t["id"], ch["recommended"],
                                       ch["difficulty"], mods,
                                       include_pity=False)["distribution"]
    ev = sum((dist[k] / 100.0) * ch["outcomes"][k].get("money", 0) for k in TIERS)
    ev -= ch.get("entry", 0)
    evh = ev / float(t["duration"])
    check("G %-28s $%6.1f / %dh" % (t["title"], ev, t["duration"]), evh < BENCH,
          "$%.1f/h" % evh)
    note("%-28s EV $%6.1f over %dh  =  $%5.1f/h" % (t["title"], ev, t["duration"], evh))

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[H] OLD SAVES")
# ═══════════════════════════════════════════════════════════════════════════════
check("H1 player_possessions defaults to []", DEFAULTS["player_possessions"] == [])
check("H2 player_personal_bests defaults to {}", DEFAULTS["player_personal_bests"] == {})
check("H3 player_accomplishments defaults to []", DEFAULTS["player_accomplishments"] == [])
check("H4 _possession_seq defaults to 0", DEFAULTS["_possession_seq"] == 0)
check("H5 _p69_last_practice defaults to {}", DEFAULTS["_p69_last_practice"] == {})
check("H6 _possessions_tab defaults to a real tab", DEFAULTS["_possessions_tab"] == "keepsakes")
check("H7 _selected_possession defaults to None", DEFAULTS["_selected_possession"] is None)
reset()
check("H8 a save with no possessions reads cleanly",
      G["get_possessions_by_category"]("keepsake") == []
      and G["get_featured_possessions"]() == []
      and G["possession_by_id"]("anything") is None)
# A dict written by an older build has no "featured" and no "meta". Every
# accessor must read it through .get() rather than [].
store.player_possessions.append({"id": "legacy", "item_id": "pool_trophy",
                                 "acquired_day": 1, "category": "keepsake",
                                 "acquired_source": "old"})
check("H9 a legacy possession dict (no featured/meta) reads without KeyError",
      has("pool_trophy")
      and G["get_featured_possessions"]() == []
      and [p["id"] for p in G["get_possessions_by_category"]("keepsake")] == ["legacy"]
      and G["possession_by_id"]("legacy") is not None)
check("H10 featuring a legacy dict backfills the missing key",
      G["feature_possession"]("legacy", True)
      and G["get_featured_possessions"]()[0]["id"] == "legacy")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[I] ICONS")
# ═══════════════════════════════════════════════════════════════════════════════
check("I1 possession_icon returns None when no asset is loadable",
      G["possession_icon"]("keepsake_trophy") is None
      or os.path.exists(os.path.join(GAME, G["possession_icon"]("keepsake_trophy"))))
check("I2 an unknown icon_key does not raise",
      G["possession_icon"]("not_a_real_key") in
      (None, G["POSSESSION_ICONS"]["_fallback"]))
check("I3 every category has a swatch colour",
      all(d["category"] in G["POSSESSION_CATEGORY_COLOR"] for d in CAT.values()))

# ═══════════════════════════════════════════════════════════════════════════════
print("\n[J] LOSS CONTENT")
# ═══════════════════════════════════════════════════════════════════════════════
_cats = {t["category"] for t in G["CITY_CHALLENGE_TEMPLATES"]}
check("J1 every challenge category has a takeaway line",
      all(c in G["P69_LOSS_TAKEAWAYS"] for c in _cats),
      [c for c in _cats if c not in G["P69_LOSS_TAKEAWAYS"]])
check("J2 an unknown category still returns a line",
      bool(G["p69_loss_takeaway"]("nonsense")))

print("\n" + "=" * 70)
if failures:
    print("FAILURES (%d):" % len(failures))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("ALL PHASE 69 CHECKS PASSED")
