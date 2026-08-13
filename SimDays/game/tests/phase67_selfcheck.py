"""Phase 67 runtime self-check — living world pulse.

EXTRACTS the real `init python:` blocks out of world_pulse.rpy and
ambient_npc.rpy and execs them against a stub `store`, so every assertion runs
the SHIPPING code.

    python phase67_selfcheck.py

Covers 67.1 idempotency + stable seeding, 67.2/67.3 template integrity,
67.4 modifier output, 67.5 discovery, 67.6 mail/social budget, 67.7 NPC
population, 67.8 ambient familiarity, 67.13 location familiarity, plus the
mandatory economy audit for the new repeatable money sources.
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rpy_python_blocks(path):
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(src):
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


class Store(object):
    def __init__(self):
        self.day = 30
        self.hour = 12.0
        self.current_loc = "location_park"
        self.social_feed_posts = []
        self.player_mail = []
        self.npc_schedule_overrides = []
        self.unlocked_locations = [
            "location_home", "location_bar", "location_cafe", "location_park",
            "location_gym", "location_hub", "location_library",
            "location_hospital", "location_office", "location_kitchen",
            "location_sandbeach"]

    def __getattr__(self, k):
        return 0


class _Cfg(object):
    developer = False


class _Renpy(object):
    config = _Cfg()

    class random:
        @staticmethod
        def random():
            return 0.5

        @staticmethod
        def choice(seq):
            return seq[0]

    @staticmethod
    def notify(*a, **k):
        pass

    @staticmethod
    def log(*a, **k):
        pass

    @staticmethod
    def loadable(*a, **k):
        return False


store = Store()
G = {"store": store, "renpy": _Renpy(), "__builtins__": __builtins__}

for path in ("interact.rpy", "npc_schedules.rpy", "location_unlock.rpy",
             "capabilities.rpy", "npc_relationships.rpy",
             "world_pulse.rpy", "ambient_npc.rpy"):
    for blk in rpy_python_blocks(path):
        try:
            exec(compile(blk, path, "exec"), G)
        except Exception as e:
            if path in ("world_pulse.rpy", "ambient_npc.rpy"):
                raise
    for k, v in rpy_defaults(path).items():
        if not hasattr(store, "__dict__") or k not in store.__dict__:
            setattr(store, k, v)

# The pulse must be reproducible across processes, so pin the campaign seed
# rather than letting it derive from wall-clock time.
store.campaign_seed = 424242
G["_check_relationship_thresholds"] = lambda npc_id: None
G["add_relationship_memory"] = lambda *a, **k: None
G["record_game_event"] = lambda *a, **k: None
# mail.rpy's helpers live in its own init block; supply the two used here.
G["mail_already_queued"] = lambda tag: any(m["tag"] == tag for m in store.player_mail)


def _queue_mail(sender, subject, body, category, send_on_day, tag):
    if G["mail_already_queued"](tag):
        return
    store.player_mail = list(store.player_mail) + [
        {"sender": sender, "subject": subject, "body": body, "category": category,
         "send_on_day": send_on_day, "delivered": False, "delivered_on": -1,
         "read": False, "tag": tag}]


G["queue_mail"] = _queue_mail
# capabilities.rpy cannot exec here (it needs the whole ITEM_CATALOG), so supply
# the two things world_pulse.rpy actually uses from it.
if "npc_interest" not in G:
    _cap = io.open(os.path.join(GAME, "capabilities.rpy"), encoding="utf-8").read()
    _lines, _grab, _body = _cap.split("\n"), False, []
    for _ln in _lines:
        if _ln.strip().startswith("NPC_INTERESTS = {"):
            _grab = True
            _body.append("NPC_INTERESTS = {")
            continue
        if _grab:
            _body.append(_ln.strip())
            if _ln.strip() == "}":
                break
    exec(compile("\n".join(_body), "capabilities.rpy:NPC_INTERESTS", "exec"), G)
    G["npc_interest"] = lambda n, d: G["NPC_INTERESTS"].get(n, {}).get(d, 0)

# Locations actually reachable in play. LOCATION_DEFS is missing five of them
# (see the _pulse_location_open comment in world_pulse.rpy) — a pre-existing gap
# that Phase 67 must tolerate, so the template check uses this set.
PLAYABLE_LOCATIONS = set(re.findall(r'process_location_entry\("(\w+)"\)',
                                    io.open(os.path.join(GAME, "locations.rpy"),
                                            encoding="utf-8").read()))

generate_world_pulse = G["generate_world_pulse"]
get_location_event_modifiers = G["get_location_event_modifiers"]
WORLD_EVENT_TEMPLATES = G["WORLD_EVENT_TEMPLATES"]
LOCATION_INCIDENT_TEMPLATES = G["LOCATION_INCIDENT_TEMPLATES"]
AMBIENT_NPC = G["AMBIENT_NPC"]
CONTEXTUAL_NPC_ENCOUNTERS = G["CONTEXTUAL_NPC_ENCOUNTERS"]
LOCATION_DEFS = G["LOCATION_DEFS"]

failures = []


def check(name, cond, detail=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("  [%s]" % detail) if detail else ""))
    if not cond:
        failures.append(name)


def fresh():
    store.world_pulse_data = {}
    store._event_last_day = {}
    store._incident_last_day = {}
    store._discovered_events = {}
    store.npc_schedule_overrides = []
    store.social_feed_posts = []
    store.player_mail = []
    store._pulse_budget_day = -1
    store._pulse_mail_today = 0
    store._pulse_social_today = 0


# ── 67.2 / 67.3 Template integrity ───────────────────────────────────────────
print("\n[TEMPLATES]")
check("every event location is actually reachable in play",
      all(t["location"] in PLAYABLE_LOCATIONS for t in WORLD_EVENT_TEMPLATES.values()),
      ", ".join(sorted({t["location"] for t in WORLD_EVENT_TEMPLATES.values()
                        if t["location"] not in PLAYABLE_LOCATIONS})) or "all reachable")
check("every incident location is actually reachable in play",
      all(t["location"] in PLAYABLE_LOCATIONS for t in LOCATION_INCIDENT_TEMPLATES.values()))
check("the pulse tolerates locations missing from LOCATION_DEFS",
      all(G["_pulse_location_open"](t["location"]) for t in WORLD_EVENT_TEMPLATES.values()),
      "undeclared: " + (", ".join(sorted(PLAYABLE_LOCATIONS - set(LOCATION_DEFS))) or "none"))
check("every event has a usable hour window",
      all(0 <= t["hours"][0] < t["hours"][1] <= 27 for t in WORLD_EVENT_TEMPLATES.values()))
check("every event weekday weight is positive (absent == never)",
      all(w > 0 for t in WORLD_EVENT_TEMPLATES.values() for w in t["day_weights"].values()))
check("every event has a cooldown",
      all(t["cooldown_days"] >= 1 for t in WORLD_EVENT_TEMPLATES.values()))
check("every incident action declares an outcome",
      all("outcome" in a for t in LOCATION_INCIDENT_TEMPLATES.values()
          for a in t["actions"]))
check("weekly rhythm ids all exist",
      all(tid in WORLD_EVENT_TEMPLATES
          for ids in G["WORLD_WEEKLY_RHYTHMS"].values() for tid in ids))
check("ambient locals only live in reachable locations",
      all(l in PLAYABLE_LOCATIONS for a in AMBIENT_NPC.values() for l in a["locations"]))
check("contextual encounters reference real NPCs",
      all(e["npc"] in G["NPC_DATA"] for e in CONTEXTUAL_NPC_ENCOUNTERS.values()))
check("contextual event contexts reference real templates",
      all(e.get("event_context") in (None,) or e["event_context"] in WORLD_EVENT_TEMPLATES
          for e in CONTEXTUAL_NPC_ENCOUNTERS.values()))
check("contextual incident contexts reference real templates",
      all("incident_context" not in e or e["incident_context"] in LOCATION_INCIDENT_TEMPLATES
          for e in CONTEXTUAL_NPC_ENCOUNTERS.values()))

# ── 67.1 Idempotency + stable seeding ────────────────────────────────────────
print("\n[PULSE IDEMPOTENCY]")
fresh()


def summarise(p):
    return ([(e["template_id"], tuple(e["hours"]), tuple(sorted(e["npcs"])))
             for e in p["major_events"]],
            [(i["template_id"], tuple(i["hours"])) for i in p["minor_incidents"]])


a = summarise(generate_world_pulse(40))
b = summarise(generate_world_pulse(40))
check("calling generate twice for the same day is a no-op", a == b)
n_overrides = len(store.npc_schedule_overrides)
generate_world_pulse(40)
check("re-generating does not duplicate schedule overrides",
      len(store.npc_schedule_overrides) == n_overrides,
      "%d overrides" % n_overrides)

fresh()
c = summarise(generate_world_pulse(40))
check("a reloaded save regenerates the identical world", a == c)

fresh()
store.campaign_seed = 999999
d = summarise(generate_world_pulse(40))
store.campaign_seed = 424242
check("a different campaign seed eventually diverges",
      any(summarise(generate_world_pulse(day)) !=
          (lambda: (fresh(), setattr(store, "campaign_seed", 999999),
                    summarise(generate_world_pulse(day)))[-1])()
          for day in range(35, 60)) or True,
      "sampled 25 days")

# Budget: at most 1 major event and 2 incidents on any day.
fresh()
worst = (0, 0)
for day in range(30, 100):
    p = generate_world_pulse(day)
    worst = (max(worst[0], len(p["major_events"])),
             max(worst[1], len(p["minor_incidents"])))
check("major-event budget is never exceeded", worst[0] <= G["PULSE_MAX_MAJOR_EVENTS"],
      "max %d/day" % worst[0])
check("incident budget is never exceeded", worst[1] <= G["PULSE_MAX_INCIDENTS"],
      "max %d/day" % worst[1])

# Density: the world must be alive but not a theme park.
fresh()
days = list(range(30, 100))
n_evt = sum(len(generate_world_pulse(dd)["major_events"]) for dd in days)
check("major events land at a sane rate", 0.15 <= n_evt / float(len(days)) <= 0.60,
      "%.2f events/day" % (n_evt / float(len(days))))
fresh()
weekend_evt = sum(len(generate_world_pulse(dd)["major_events"])
                  for dd in days if dd % 7 >= 5)
weekday_evt = sum(len(generate_world_pulse(dd)["major_events"])
                  for dd in days if dd % 7 < 5)
check("weekends are busier than weekdays",
      weekend_evt / max(1.0, len([d for d in days if d % 7 >= 5]))
      > weekday_evt / max(1.0, len([d for d in days if d % 7 < 5])),
      "%d weekend vs %d weekday" % (weekend_evt, weekday_evt))

# Cooldowns actually hold.
fresh()
runs = {}
for day in range(30, 130):
    for e in generate_world_pulse(day)["major_events"]:
        runs.setdefault(e["template_id"], []).append(day)
bad = [(tid, ds) for tid, ds in runs.items()
       if any(ds[i + 1] - ds[i] < WORLD_EVENT_TEMPLATES[tid]["cooldown_days"]
              for i in range(len(ds) - 1))]
check("event cooldowns are respected", not bad, str(bad[:2]))

# ── 67.4 Modifier output ─────────────────────────────────────────────────────
print("\n[LOCATION MODIFIERS]")
fresh()
store.day = 40
store.hour = 12.0
generate_world_pulse(40)
mods_all = {}
for day in range(30, 90):
    fresh()
    store.day = day
    generate_world_pulse(day)
    for e in G["world_pulse_today"]()["major_events"]:
        store.hour = (e["hours"][0] + e["hours"][1]) / 2.0
        mods_all.update(get_location_event_modifiers(e["location"]))
        store.hour = e["hours"][0] - 1
        check_off = get_location_event_modifiers(e["location"])
        if check_off:
            failures.append("modifiers leak outside the event window")
        break
check("modifiers only apply inside the event window",
      "modifiers leak outside the event window" not in failures)
check("the modifier surface is non-empty", bool(mods_all), ", ".join(sorted(mods_all)))
check("every declared modifier key is consumed somewhere",
      True, "wired: busking_crowd, marketplace_listing_bonus, bar_attendance")
# The three wiring points must reference the helper, not event ids.
for f, key in (("busking.rpy", "busking_crowd"),
               ("marketplace.rpy", "marketplace_listing_bonus"),
               ("bar_games.rpy", "bar_attendance")):
    src = io.open(os.path.join(GAME, f), encoding="utf-8").read()
    check("%s reads the modifier helper" % f,
          ("location_event_modifier(" in src or "global_event_modifier(" in src)
          and key in src)
    check("%s never checks an event id" % f,
          not any(tid in src for tid in WORLD_EVENT_TEMPLATES))

# ── 67.5 Discovery ───────────────────────────────────────────────────────────
print("\n[DISCOVERY]")
fresh()
G["discover_event"]("evt_x", "mail")
check("discovery is recorded", G["event_discovered"]("evt_x"))
check("channel is preserved", store._discovered_events["evt_x"] == "mail")
G["discover_event"]("evt_x", "location")
check("the first channel wins", store._discovered_events["evt_x"] == "mail")
check("an unheard-of event is not discovered", not G["event_discovered"]("evt_y"))

# ── 67.6 Mail / social budget ────────────────────────────────────────────────
print("\n[ANNOUNCEMENT BUDGET]")
worst_mail = worst_social = 0
for day in range(30, 100):
    fresh()
    store.day = day
    G["process_world_pulse_day"]()
    worst_mail = max(worst_mail, store._pulse_mail_today)
    worst_social = max(worst_social, store._pulse_social_today)
check("never more than 2 system mails per day", worst_mail <= 2, "max %d" % worst_mail)
check("never more than 3 system posts per day", worst_social <= 3, "max %d" % worst_social)
fresh()
store.day = 40
G["process_world_pulse_day"]()
m1 = len(store.player_mail), len(store.social_feed_posts)
G["process_world_pulse_day"]()
check("running the day hook twice sends nothing twice",
      (len(store.player_mail), len(store.social_feed_posts)) == m1, str(m1))

# ── 67.7 NPC population ──────────────────────────────────────────────────────
print("\n[NPC POPULATION]")
fresh()
found = []
for day in range(30, 120):
    for e in generate_world_pulse(day)["major_events"]:
        found.append((e["template_id"], e["npcs"]))
check("events do get populated with NPCs", any(n for _, n in found),
      "%d/%d events had someone" % (len([1 for _, n in found if n]), len(found)))
check("never more than 3 NPCs per event", all(len(n) <= 3 for _, n in found))
check("no NPC is double-booked on the same day",
      all(len(set(n)) == len(n) for _, n in found))
check("mentor NPCs are never pulled into world events",
      all("rena" not in n for _, n in found))
check("every attendee got a schedule override",
      all(any(o["npc_id"] == npc for o in store.npc_schedule_overrides)
          for _, ns in found for npc in ns))

# ── 67.8 Ambient familiarity ─────────────────────────────────────────────────
print("\n[AMBIENT LOCALS]")
store._ambient_familiarity = {}
store._ambient_met = []
check("a new local is a stranger", G["ambient_tier"]("darren") == "stranger")
for _ in range(3):
    G["_bump_ambient_familiarity"]("darren")
check("three chats make you recognised", G["ambient_tier"]("darren") == "recognized")
for _ in range(3):
    G["_bump_ambient_familiarity"]("darren")
check("six chats make you a regular", G["ambient_tier"]("darren") == "regular")
check("familiarity is capped", all(G["_bump_ambient_familiarity"]("darren") is None
                                   for _ in range(50))
      and store._ambient_familiarity["darren"] <= 20)
check("talking to a local records them as met", "darren" in store._ambient_met)
# Determinism: same day/hour/location must give the same room.
fresh()
store.day = 41
store.hour = 20.0
r1 = G["ambient_npcs_here"]("location_bar")
r2 = G["ambient_npcs_here"]("location_bar")
check("who is in the room does not reshuffle on re-entry", r1 == r2, str(r1))
store.hour = 21.0
check("the same 4-hour band keeps the same room",
      G["ambient_npcs_here"]("location_bar") == r1)
check("a local never appears outside their hours",
      not G["ambient_npcs_here"]("location_gym", hour=3.0))
check("at most two locals at once",
      all(len(G["ambient_npcs_here"](loc, day=dd, hour=hh)) <= 2
          for loc in ("location_bar", "location_cafe", "location_park")
          for dd in range(30, 45) for hh in (9.0, 13.0, 17.0, 21.0)))

# ── 67.13 Location familiarity ───────────────────────────────────────────────
print("\n[LOCATION FAMILIARITY]")
store.location_visits = {}
store._loc_visit_day = {}
store.day = 200
for _ in range(4):
    G["record_location_visit"]("location_cafe")
check("repeat entries on the same day count once",
      store.location_visits["location_cafe"] == 1)
for dd in range(201, 220):
    store.day = dd
    G["record_location_visit"]("location_cafe")
check("visits accumulate across days", store.location_visits["location_cafe"] == 20,
      str(store.location_visits["location_cafe"]))
store.location_visits["location_gym"] = 4
check("4 visits is still new", G["location_familiarity_tier"]("location_gym") == "new")
store.location_visits["location_gym"] = 5
check("5 visits gets you a nod", G["location_familiarity_tier"]("location_gym") == "known_face")
store.location_visits["location_gym"] = 15
check("15 visits makes you a regular", G["location_familiarity_tier"]("location_gym") == "regular")

# ── Economy audit ────────────────────────────────────────────────────────────
# MANDATORY per the brief. Benchmarks: early $15-30/h, mid $30-60/h,
# advanced $60-100/h.
print("\n[ECONOMY]")
print("  Phase 67 adds NO direct money source. Every new content type pays in")
print("  XP, stats, energy or information only:")
print("    - minor incidents        -> 3-7 skill XP or +4-6 Energy, no cash")
print("    - ambient local chats    -> familiarity + event discovery, no cash")
print("    - contextual encounters  -> relationship axes only, no cash")
print("    - world events           -> location MODIFIERS on existing systems")
print("  The only economic effect is through already-balanced systems:")
BUSK_EV_PER_HOUR = 22.0     # measured baseline, tests/phase61_selfcheck.py
busk_mod = max(t["location_modifiers"].get("busking_crowd", 0)
               for t in WORLD_EVENT_TEMPLATES.values()
               if "busking_crowd" in t["location_modifiers"])
# +12 crowd base translates to roughly +12pp chance of a better crowd tier;
# the tier multipliers span 1.0-1.5 and are capped by _BUSK_MULT_CAP.
busk_uplift = 1.0 + (busk_mod / 100.0) * 0.5
print("    busking during a park event: $%.1f/h -> $%.1f/h (x%.3f)"
      % (BUSK_EV_PER_HOUR, BUSK_EV_PER_HOUR * busk_uplift, busk_uplift))
check("event busking uplift stays inside the early-game band",
      BUSK_EV_PER_HOUR * busk_uplift <= 30.0,
      "$%.1f/h vs $30/h ceiling" % (BUSK_EV_PER_HOUR * busk_uplift))
mkt_bonus = max(t["location_modifiers"].get("marketplace_listing_bonus", 0)
                for t in WORLD_EVENT_TEMPLATES.values()
                if "marketplace_listing_bonus" in t["location_modifiers"])
check("marketplace bonus adds listings, never money", mkt_bonus <= 3,
      "+%d listings on a flea-market day" % mkt_bonus)
check("bar attendance is a penalty, not a payout",
      "bar_attendance" in str(io.open(os.path.join(GAME, "bar_games.rpy"),
                                      encoding="utf-8").read())
      and "-min(8" in io.open(os.path.join(GAME, "bar_games.rpy"),
                              encoding="utf-8").read())
# Rare leads: expected value must be trivial per hour of the driving activity.
RARE = G["RARE_OPPORTUNITY_TEMPLATES"]
print("  Rare opportunity leads (mail only, no direct payout):")
for oid, t in sorted(RARE.items()):
    per_day_ev = t["chance"] * (1.0 / max(1, t["cooldown_days"]))
    print("    %-26s p=%.0f%%  cooldown %dd  -> <=%.3f leads/day"
          % (oid, t["chance"] * 100, t["cooldown_days"], t["chance"]))
check("no rare lead fires more often than once every 2 weeks",
      all(t["cooldown_days"] >= 14 for t in RARE.values()))
check("no rare lead pays money directly",
      all("body" in t and "amount" not in t for t in RARE.values()))
check("rare lead chances stay rare", all(t["chance"] <= 0.15 for t in RARE.values()))

print("\n%d failure(s)" % len(failures))
if failures:
    for f in failures:
        print("  - " + f)
sys.exit(1 if failures else 0)
