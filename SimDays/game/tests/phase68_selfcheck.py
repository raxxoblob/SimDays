"""Phase 68 runtime self-check — NPC initiative, personal lives, follow-ups,
word of mouth, player identity.

EXTRACTS the real `init python:` blocks out of npc_initiative.rpy (plus its
Phase 66/67 dependencies) and execs them against a stub `store`.

    python phase68_selfcheck.py

Covers 68.1 budget enforcement + idempotency, 68.3 personal-life states,
68.4 cancellation rate limits, 68.5 follow-up ordering, 68.6 propagation
(Respect only), 68.7 identity conditions, 68.8 failure cooldowns.
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
        self.day = 100
        self.hour = 9.0
        self.current_loc = "location_park"
        self.player_commitments = []
        self.player_artworks = []
        self.npc_messages = []
        self.player_mail = []
        self.social_feed_posts = []
        self.calendar_events = []
        self.npc_schedule_overrides = []
        self.location_visits = {}
        self.unlocked_locations = ["location_home", "location_bar", "location_cafe",
                                   "location_park", "location_gym", "location_hub",
                                   "location_library", "location_hospital",
                                   "location_office", "location_kitchen"]

    def __getattr__(self, k):
        return 0


class _Cfg(object):
    developer = False


class _Rand(object):
    value = 0.5

    @classmethod
    def random(cls):
        return cls.value

    @staticmethod
    def choice(seq):
        return seq[0]

    @staticmethod
    def randint(a, b):
        return a


class _Renpy(object):
    config = _Cfg()
    random = _Rand

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
             "npc_relationships.rpy", "world_pulse.rpy", "ambient_npc.rpy",
             "npc_initiative.rpy"):
    for blk in rpy_python_blocks(path):
        try:
            exec(compile(blk, path, "exec"), G)
        except Exception:
            if path in ("npc_relationships.rpy", "world_pulse.rpy", "npc_initiative.rpy"):
                raise
    for k, v in rpy_defaults(path).items():
        if k not in store.__dict__:
            setattr(store, k, v)

store.campaign_seed = 424242

# Stubs for helpers owned by files we do not exec here.
_sent = []
G["_check_relationship_thresholds"] = lambda npc_id: None
G["add_relationship_memory"] = lambda *a, **k: None
G["record_game_event"] = lambda *a, **k: None
G["npc_interest"] = lambda n, d: 0
G["mail_already_queued"] = lambda tag: any(m["tag"] == tag for m in store.player_mail)
G["queue_mail"] = lambda s_, su, b, c, d_, tag: store.player_mail.append(
    {"sender": s_, "subject": su, "body": b, "tag": tag})
G["message_already_queued"] = lambda tag: any(m["tag"] == tag for m in store.npc_messages)
G["queue_phone_message"] = lambda npc, text, d_, tag, responses=None: (
    store.npc_messages.append({"npc_id": npc, "text": text, "tag": tag}))
G["deliver_message_now"] = lambda tag: _sent.append(tag)
G["add_calendar_event"] = lambda **k: "cal_stub"

failures = []


def check(name, cond, detail=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("  [%s]" % detail) if detail else ""))
    if not cond:
        failures.append(name)


NPC_DATA = G["NPC_DATA"]
WEIGHTS = G["NPC_PERSONAL_LIFE_WEIGHTS"]
STATES = G["NPC_PERSONAL_LIFE_STATES"]


def reset(day=100):
    store.day = day
    store.hour = 9.0
    store.npc_relationships = {}
    store._npc_personal_life = {}
    store._npc_life_history = {}
    store._followup_queue = []
    store._followup_last_day = -1
    store.public_player_facts = {}
    store._player_identity_flags = {}
    store._npc_cancel_last_day = {}
    store._failure_content_last = {}
    store._npc_initiative_cooldowns = {}
    store._initiative_evaluated_day = -1
    store.npc_initiative_last_global_day = -1
    store._p68_contact_day = -1
    store._pulse_budget_day = -1
    store._pulse_mail_today = 0
    store._pulse_social_today = 0
    store.world_pulse_data = {}
    store._event_last_day = {}
    store._incident_last_day = {}
    store._discovered_events = {}
    store.npc_messages = []
    store.player_mail = []
    store.player_commitments = []
    store.social_feed_posts = []
    store.location_visits = {}
    store._nights_active = 0
    del _sent[:]
    for nid, d in NPC_DATA.items():
        setattr(store, d["aff"], 0)
        setattr(store, d["trust"], 0)


# ── 68.3 Personal life states ────────────────────────────────────────────────
print("\n[PERSONAL LIVES]")
check("every weighted NPC is a real NPC", all(n in NPC_DATA for n in WEIGHTS))
check("every weighted state is a real state",
      all(s in STATES for w in WEIGHTS.values() for s in w))
check("every recurring NPC has a personal life",
      all(n in WEIGHTS for n in NPC_DATA), ", ".join(sorted(set(NPC_DATA) - set(WEIGHTS))) or "all covered")
check("Rena's life is work-only (no social/creative states)",
      set(WEIGHTS["rena"]) <= {"busy_work", "recovering"})
check("Sam's dominant state is her training programme",
      max(WEIGHTS["sam"], key=WEIGHTS["sam"].get) == "training_focus")
check("Zoe's dominant state is a creative project",
      max(WEIGHTS["zoe"], key=WEIGHTS["zoe"].get) == "creative_project")
check("every duration range is sane",
      all(1 <= s["duration_range"][0] <= s["duration_range"][1] <= 7 for s in STATES.values()))

reset()
for nid in WEIGHTS:
    setattr(store, nid + "_met", True)
# States are seeded, expire, and never last forever.
seen = {}
for d in range(100, 260):
    store.day = d
    G["_expire_personal_lives"](d)
    for nid in WEIGHTS:
        if not G["npc_personal_life"](nid):
            G["_roll_personal_life"](nid, d)
    for nid in WEIGHTS:
        st = G["npc_life_state"](nid)
        if st:
            seen.setdefault(nid, set()).add(st)
check("NPCs actually enter personal-life states", len(seen) >= 8,
      "%d/%d NPCs had at least one state" % (len(seen), len(WEIGHTS)))
check("an NPC never gets a state it has no weight for",
      all(s in WEIGHTS[n] for n, ss in seen.items() for s in ss))
active_now = sum(1 for n in WEIGHTS if G["npc_life_state"](n))
check("most NPCs are having a normal week at any moment",
      active_now <= len(WEIGHTS) * 0.7, "%d/%d in a state" % (active_now, len(WEIGHTS)))
check("state seeding is deterministic",
      (lambda: (reset(), [setattr(store, n + "_met", True) for n in WEIGHTS],
                G["_roll_personal_life"]("zoe", 137),
                G["npc_life_state"]("zoe"))[-1])() ==
      (lambda: (reset(), [setattr(store, n + "_met", True) for n in WEIGHTS],
                G["_roll_personal_life"]("zoe", 137),
                G["npc_life_state"]("zoe"))[-1])())

# Availability modifier must reach the invitation system.
reset()
store.nora_affection = 60
store.nora_trust = 50
G["set_npc_rel"]("nora", "familiarity", 60)
base = G["invitation_acceptance_chance"]("nora", "casual")
G["_npc_personal_life"] = None  # noqa - ensure we use the store, not a local
store._npc_personal_life = {"nora": {"state": "stressed_week", "expires_day": store.day + 2}}
stressed = G["invitation_acceptance_chance"]("nora", "casual")
store._npc_personal_life = {"nora": {"state": "social_week", "expires_day": store.day + 2}}
social = G["invitation_acceptance_chance"]("nora", "casual")
check("a stressed week makes an NPC harder to reach", stressed < base,
      "%.2f < %.2f" % (stressed, base))
check("a social week makes an NPC easier to reach", social > base,
      "%.2f > %.2f" % (social, base))

# ── 68.1 Budget + idempotency ────────────────────────────────────────────────
print("\n[INITIATIVE BUDGET]")
reset()
for nid in WEIGHTS:
    setattr(store, nid + "_met", True)
G["evaluate_npc_initiatives"](store.day)
check("the pass records the day it ran", store._initiative_evaluated_day == store.day)
n_msgs = len(store.npc_messages)
G["evaluate_npc_initiatives"](store.day)
check("running the pass twice sends nothing twice", len(store.npc_messages) == n_msgs)

reset()
for nid in WEIGHTS:
    setattr(store, nid + "_met", True)
store.npc_initiative_last_global_day = store.day   # legacy system already fired
G["evaluate_npc_initiatives"](store.day)
check("Phase 68 stays silent when the legacy system already contacted you",
      len(store.npc_messages) == 0)

# Over a long run, never more than one Phase 68 contact per day.
reset()
for nid in WEIGHTS:
    setattr(store, nid + "_met", True)
    setattr(store, NPC_DATA[nid]["aff"], 60)
    setattr(store, NPC_DATA[nid]["trust"], 50)
    G["set_npc_rel"](nid, "familiarity", 70)
worst = 0
for d in range(100, 200):
    store.day = d
    store._p68_contact_day = -1
    store.npc_initiative_last_global_day = -1
    before = len(store.npc_messages)
    G["enqueue_followup"](nid, "comment", "stress_%d" % d, "generic_comment",
                          delay_min=0, delay_max=2, priority=5)
    G["process_world_pulse_day"]()
    G["process_npc_lives_day"]()
    worst = max(worst, len(store.npc_messages) - before)
check("never more than one unprompted contact per day", worst <= 1, "max %d" % worst)

# ── 68.5 Follow-up queue ─────────────────────────────────────────────────────
print("\n[FOLLOW-UPS]")
reset()
store.nora_met = store.marcus_met = store.zoe_met = True
G["enqueue_followup"]("nora", "comment", "a", "generic_comment", delay_min=1, delay_max=3, priority=3)
G["enqueue_followup"]("marcus", "thanks", "b", "generic_thanks", delay_min=1, delay_max=3, priority=9)
G["enqueue_followup"]("zoe", "reaction", "c", "challenge_win", delay_min=1, delay_max=3, priority=5)
check("duplicate enqueue for the same trigger is ignored",
      G["enqueue_followup"]("nora", "comment", "a", "generic_comment") is None)
store.day += 1
first = G["process_followup_queue"](store.day)
check("highest priority is delivered first", first and "marcus" in first, str(first))
check("only one follow-up per day", G["process_followup_queue"](store.day) is None)
store.day += 1
second = G["process_followup_queue"](store.day)
check("the next-highest goes the day after", second and "zoe" in second, str(second))
store.day += 1
third = G["process_followup_queue"](store.day)
check("the lowest priority still arrives", third and "nora" in third, str(third))
check("delivered follow-ups are marked completed",
      all(f["completed"] for f in store._followup_queue))
# Expiry.
reset()
store.nora_met = True
G["enqueue_followup"]("nora", "comment", "old", "generic_comment", delay_min=1, delay_max=2)
store.day += 10
check("expired follow-ups are never delivered",
      G["process_followup_queue"](store.day) is None)
check("expired follow-ups are dropped from the queue", not store._followup_queue)
# Unknown NPC.
reset()
G["enqueue_followup"]("caroline", "comment", "x", "generic_comment", delay_min=0, delay_max=3)
store.caroline_met = False
check("a follow-up from someone you have not met waits",
      G["process_followup_queue"](store.day) is None)

# ── 68.6 Public facts / word of mouth ────────────────────────────────────────
print("\n[WORD OF MOUTH]")
reset()
for nid in ("nora", "marcus", "zoe", "eli"):
    setattr(store, nid + "_met", True)
    setattr(store, NPC_DATA[nid]["aff"], 40)
    setattr(store, NPC_DATA[nid]["trust"], 30)
    G["set_npc_rel"](nid, "familiarity", 50)
    G["set_npc_rel"](nid, "respect", 10)
before = {n: (G["npc_rel"](n, "respect"), G["npc_rel"](n, "affection")) for n in
          ("nora", "marcus", "zoe", "eli")}
fid = G["publish_player_fact"]("won_city_challenge", "chal1")
check("publishing returns a fact id", bool(fid))
check("republishing the same fact on the same day is a no-op",
      G["publish_player_fact"]("won_city_challenge", "chal1") == fid
      and len(store.public_player_facts) == 1)
G["propagate_public_facts"](store.day)
check("a fact does not propagate the same day",
      not store.public_player_facts[fid]["propagated_to"])
store.day += 1
G["propagate_public_facts"](store.day)
prop = store.public_player_facts[fid]["propagated_to"]
check("a fact propagates the next day", bool(prop), ", ".join(prop))
check("propagation respects max_npcs",
      len(prop) <= G["PUBLIC_FACT_TEMPLATES"]["won_city_challenge"]["max_npcs"],
      "%d npcs" % len(prop))
check("winning a challenge raises Respect",
      all(G["npc_rel"](n, "respect") > before[n][0] for n in prop))
check("winning a challenge does NOT raise Affection",
      all(G["npc_rel"](n, "affection") == before[n][1] for n in prop),
      "reputation must not buy warmth")
check("a fact only propagates once", (G["propagate_public_facts"](store.day),
                                      store.public_player_facts[fid]["propagated_to"] == prop)[-1])
check("propagation queues a follow-up", any(f["trigger_source"] == "won_city_challenge"
                                            for f in store._followup_queue))
# Strangers never hear about it.
reset()
store.nora_met = True
G["set_npc_rel"]("nora", "familiarity", 5)
fid2 = G["publish_player_fact"]("got_promoted", "it_r2")
store.day += 1
G["propagate_public_facts"](store.day)
check("people who barely know you do not hear about it",
      not store.public_player_facts[fid2]["propagated_to"])
check("every fact template only grants Respect (and at most 1 Affection)",
      all(t["affects"].get("affection", 0) <= 1
          for t in G["PUBLIC_FACT_TEMPLATES"].values()))

# ── 68.4 Cancellations ───────────────────────────────────────────────────────
print("\n[CANCELLATIONS]")
reset()
store.marcus_met = True
G["set_npc_rel"]("marcus", "familiarity", 50)
c = {"id": "c1", "npc_id": "marcus", "title": "t", "day": store.day + 1, "hour": 20,
     "completed": False, "missed": False, "cancelled": False}
store.player_commitments = [c]
_Rand.value = 0.0        # force the roll to succeed
res = G["maybe_npc_cancellation"]("marcus", c)
check("an NPC can cancel a plan", res is not None and res["type"] == "cancel")
res2 = G["maybe_npc_cancellation"]("marcus", c)
check("max one cancellation per NPC per week", res2 is None)
store.day += 8
c["day"] = store.day + 1
check("after a week they can cancel again",
      G["maybe_npc_cancellation"]("marcus", c) is not None)
# Too late to cancel.
store._npc_cancel_last_day = {}
store.hour = 23.5
late = {"id": "c2", "npc_id": "marcus", "title": "t", "day": store.day, "hour": 23.6,
        "completed": False, "missed": False, "cancelled": False}
check("nobody cancels within the hour", G["maybe_npc_cancellation"]("marcus", late) is None)
# Authored story commitments are immune.
store._npc_cancel_last_day = {}
store.hour = 9.0
auth = {"id": "c3", "npc_id": "marcus", "title": "t", "day": store.day + 1, "hour": 20,
        "authored": True, "completed": False, "missed": False, "cancelled": False}
check("authored story commitments are never cancelled",
      G["maybe_npc_cancellation"]("marcus", auth) is None)
# The player is not punished.
reset()
store.marcus_met = True
store.marcus_trust = 40
G["set_npc_rel"]("marcus", "familiarity", 50)
store.player_commitments = [{"id": "c9", "npc_id": "marcus", "title": "t",
                             "day": store.day + 1, "hour": 20, "completed": False,
                             "missed": False, "cancelled": False}]
G["_process_npc_cancellations"](store.day)
check("an NPC cancelling costs the player no Trust", store.marcus_trust == 40)
check("the cancelled commitment is flagged as NPC-initiated",
      store.player_commitments[0].get("cancelled_by_npc") is True)
_Rand.value = 0.5

# ── 68.7 Player identity ─────────────────────────────────────────────────────
print("\n[IDENTITY]")
reset()
RULES = G["PLAYER_IDENTITY_RULES"]
G["update_player_identity"](store.day)
check("a new player has no identity flags", not store._player_identity_flags)
store.location_visits = {"location_gym": 10}
G["update_player_identity"](store.day)
check("10 gym visits makes you a gym regular", G["player_has_identity"]("gym_regular"))
check("12 cafe visits are still needed for cafe regular",
      not G["player_has_identity"]("cafe_regular"))
store.location_visits = {"location_gym": 3}
G["update_player_identity"](store.day)
check("identity lapses if you stop doing the thing",
      not G["player_has_identity"]("gym_regular"))
store.player_commitments = [{"completed": True, "missed": False} for _ in range(5)]
G["update_player_identity"](store.day)
check("5 kept commitments and no misses makes you reliable",
      G["player_has_identity"]("reliable"))
store.player_commitments += [{"completed": False, "missed": True} for _ in range(4)]
G["update_player_identity"](store.day)
check("missing half your plans loses 'reliable'",
      not G["player_has_identity"]("reliable"))
store._nights_active = 15
G["update_player_identity"](store.day)
check("15 late nights makes you a night owl", G["player_has_identity"]("night_owl"))
store.player_artworks = [{"quality": "great"}, {"quality": "critical"},
                         {"quality": "great"}]
G["update_player_identity"](store.day)
check("three strong pieces makes you creative", G["player_has_identity"]("creative"))
check("every identity rule exposes a dialogue tag",
      all("tag" in r for r in RULES.values()))
check("identity tags are readable", bool(G["player_identity_tags"]()))
# Night counter: one per night.
reset()
store.hour = 23.0
G["record_night_activity"]()
G["record_night_activity"]()
check("late-night presence counts once per night", store._nights_active == 1)
store.hour = 14.0
G["record_night_activity"]()
check("daytime visits do not count as nights", store._nights_active == 1)

# ── 68.8 Failure content ─────────────────────────────────────────────────────
print("\n[FAILURE CONTENT]")
reset()
for nid in ("martha", "caroline", "zoe", "marcus", "sam"):
    setattr(store, nid + "_met", True)
    G["set_npc_rel"](nid, "familiarity", 50)
check("a failure produces content", G["trigger_failure_content"]("promotion_failed"))
check("the same failure is on cooldown",
      not G["trigger_failure_content"]("promotion_failed"))
store.day += 15
check("after the cooldown it can fire again",
      G["trigger_failure_content"]("promotion_failed"))
check("an unknown trigger is a safe no-op", not G["trigger_failure_content"]("nope"))
check("failure content queues an encouraging follow-up",
      any(f["template"] == "encourage_setback" for f in store._followup_queue))
check("every failure template has a cooldown",
      all(t["cooldown_days"] >= 5 for t in G["FAILURE_CONTENT"].values()))

# ── Economy ──────────────────────────────────────────────────────────────────
print("\n[ECONOMY]")
print("  Phase 68 adds NO money source at all. Every output is a message, a")
print("  calendar entry, a relationship axis change or a dialogue tag:")
print("    - event invites      -> calendar entry for an existing Phase 67 event")
print("    - follow-ups         -> phone message only")
print("    - word of mouth      -> Respect (+2/+3), Affection at most +1")
print("    - identity flags     -> dialogue flavour only, no stat or cash bonus")
print("    - failure content    -> mail/social/encouragement, no compensation")
check("no identity rule grants a money or stat bonus",
      all("location_benefit" not in r and "money" not in r for r in RULES.values()))
check("no fact template grants money",
      all("money" not in t["affects"] for t in G["PUBLIC_FACT_TEMPLATES"].values()))

print("\n%d failure(s)" % len(failures))
if failures:
    for f in failures:
        print("  - " + f)
sys.exit(1 if failures else 0)
