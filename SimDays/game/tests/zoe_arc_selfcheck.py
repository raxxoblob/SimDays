"""Zoe depth-pass (zoe_arc.rpy) — runtime self-check.

Same approach as tests/location_beats_tier_a_selfcheck.py: EXTRACTS the real
`init python` blocks out of the shipping .rpy file and execs them against a
stub `store`, so the assertions below run the SHIPPING dispatcher, knowledge
back-fill, Talk wrapper and initiative registration. Change a gate, a window,
a message tier or a condition lambda and this fails.

    python zoe_arc_selfcheck.py
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = "zoe_arc.rpy"
SRC = io.open(os.path.join(GAME, FILE), encoding="utf-8").read()
# The Scene Tester pack for this arc lives in the debug file (gameplay .rpy
# files must not touch SCENE_TEST_REGISTRY — location_beats_selfcheck section G).
DST = io.open(os.path.join(GAME, "debug_scene_tester.rpy"), encoding="utf-8").read()

FAILS = []


def chk(name, cond, extra=""):
    print("  %s %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  [%s]" % extra) if extra else ""))
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
        for path in ("data.rpy", FILE):
            for k, v in defaults_of(path).items():
                setattr(self, k, list(v) if isinstance(v, list)
                        else dict(v) if isinstance(v, dict) else v)
        self.zoe_met = True
        self.last_tier_a_beat_day = -1
        self.npc_last_seen = {}
        self.npc_contacts = ["zoe"]


store = Store()
HERE = {"loc": "location_hub"}
FAM = {"v": 20}

G = {
    "store": store,
    "renpy": type("R", (), {"notify": staticmethod(lambda *a, **k: None),
                            "random": None})(),
    "npc_here": lambda nid, loc=None: loc == HERE["loc"],
    "npc_rel": lambda nid, axis, default=0: (
        FAM["v"] if axis == "familiarity" else getattr(store, "zoe_" + axis, default)),
    "_beat_global_ok": lambda: store.last_tier_a_beat_day != store.day,
    "_beat_cooldown_ok": lambda bid, cd: True,
    "_apply_aff": lambda nid, d: None,
    "_apply_trust": lambda nid, d: None,
    "apply_relationship_change": lambda *a, **k: {},
    "mark_npc_encountered": lambda nid: None,
    "set_npc_rel": lambda nid, axis, v: FAM.__setitem__("v", v) if axis == "familiarity" else None,
    "set_romance_state": lambda *a, **k: None,
    "_clear_initiative_pending": lambda nid: None,
    # The shipping resolver this file wraps.
    "_check_talk_followup": lambda nid: ("REAL" if nid == "martha" else None),
    # Shipping initiative tables (shape only — registration is what we assert).
    "_INITIATIVE_MSGS": {},
    "_INITIATIVE_VARIANTS": {"zoe": ["zoe_msg_photo"]},
    "_VARIANT_MIN_TIER": {},
    "_VARIANT_WEIGHTS": {},
    "_VARIANT_CONDITIONS": {},
    "SCENE_TEST_REGISTRY": {},
}

exec(init_block(2), G)
exec(init_block(3), G)   # initiative registration
exec(init_block(1, DST), G)   # the debug file has exactly one init-1 block: this pack

beat_for = G["zoe_arc_beat_for"]
sync = G["_zoe_sync_knowledge"]
talk = G["_check_talk_followup"]


def reset(fam=20, **kw):
    for k, v in defaults_of(FILE).items():
        setattr(store, k, v)
    store.zoe_met = True
    store.zoe_affection = 20
    store.zoe_trust = 20
    store.topic_arc_done = {}
    store.zoe_exhibition_invited = False
    store.zoe_grant_discussed = False
    store.last_tier_a_beat_day = -1
    FAM["v"] = fam
    for k, v in kw.items():
        setattr(store, k, v)


print("\nA. Knowledge back-fill from existing arc flags")
reset()
store.topic_arc_done = {"zoe_art_1": True, "zoe_art_3": True, "zoe_music_2": True}
sync()
chk("arc_zoe_art_1 -> knows_zoe_art_interest", store.knows_zoe_art_interest)
# Story-canon consolidation: art_3 and music_2 now only DISCOVER their subject.
# Deriving the strong fact from them would spend the authored payoff (the Coffee
# scene / the Bass Window reveal) before it ever ran. Old saves are migrated
# once, in _sd_backfill (story_direct_pass.rpy), not derived here.
chk("arc_zoe_art_3 does NOT pre-spend the funding rejection",
    not store.knows_zoe_funding_problem)
chk("arc_zoe_music_2 does NOT pre-spend the bass history",
    not store.knows_zoe_bass_history)
chk("gallery goal NOT invented from art_1", not store.knows_zoe_gallery_goal)
reset()
store.zoe_grant_discussed = True
sync()
chk("zoe_grant_discussed -> knows_zoe_funding_problem", store.knows_zoe_funding_problem)
reset()
store.zoe_exhibition_invited = True
sync()
chk("existing exhibition invite -> knows_zoe_gallery_goal", store.knows_zoe_gallery_goal)

print("\nB. Dispatcher hard gates")
reset()
store.zoe_met = False
chk("no beat when Zoe not met", beat_for("location_hub") is None)
reset()
HERE["loc"] = "location_park"
chk("no beat when Zoe is elsewhere", beat_for("location_hub") is None)
HERE["loc"] = "location_hub"
reset()
store.last_tier_a_beat_day = store.day
chk("respects the shared one-beat-per-day budget", beat_for("location_hub") is None)

print("\nC. Beat windows and thresholds")
reset()
store.hour = 10.0
chk("The Print fires at the hub, weekday morning",
    beat_for("location_hub") == "zoe_print_scene")
reset()
store.hour = 20.0
chk("The Print does not fire outside 09-13", beat_for("location_hub") is None)
reset(fam=19, zoe_print_done=True)
store.hour = 10.0
chk("Bass gated at fam>=20 (fam 19 -> nothing)", beat_for("location_hub") is None)
reset(fam=20, zoe_print_done=True)
store.hour = 10.0
chk("Bass fires at fam 20", beat_for("location_hub") == "zoe_bass_window_scene")

HERE["loc"] = "location_cafe"
reset(fam=24, knows_zoe_art_interest=True)
chk("Beige gated at fam>=25 (fam 24 -> nothing)", beat_for("location_cafe") is None)
reset(fam=25, knows_zoe_art_interest=True)
chk("Beige fires at fam 25", beat_for("location_cafe") == "zoe_beige_client_scene")
reset(fam=25)
chk("Beige requires knows_zoe_art_interest", beat_for("location_cafe") is None)

HERE["loc"] = "location_park"
reset(fam=45, zoe_trust=30, knows_zoe_paid_creative_work=True)
chk("Not Ready needs trust>=30 + fam>=45 + paid-work fact",
    beat_for("location_park") == "zoe_not_ready_scene")
reset(fam=45, zoe_trust=30)
chk("Not Ready blocked without the paid-work fact", beat_for("location_park") is None)
reset(fam=60, zoe_trust=55, zoe_not_ready_done=True, zoe_deadline_scene_done=True)
chk("Just Stay needs fam>=60 and trust>=55",
    beat_for("location_park") == "zoe_just_stay_scene")

print("\nD. Priority order")
reset(fam=60, zoe_trust=55, zoe_second_opinion_pending=True, zoe_coffee_pending=True)
chk("phone-promised scene outranks every one-shot",
    beat_for("location_park") == "zoe_second_opinion_scene")
reset(fam=60, zoe_trust=55, zoe_coffee_pending=True, zoe_deadline_submitted=True,
      zoe_deadline_day=store.day - 4)
chk("coffee (promised) outranks the deadline echo (callback)",
    beat_for("location_park") == "zoe_coffee_not_advice_scene")
reset(fam=60, zoe_trust=55, zoe_deadline_submitted=True, zoe_deadline_day=store.day - 4)
chk("deadline echo fires 4+ days after submission",
    beat_for("location_park") == "zoe_after_deadline_scene")
reset(fam=60, zoe_trust=55, zoe_deadline_submitted=True, zoe_deadline_day=store.day - 3)
chk("deadline echo waits until day 4", beat_for("location_park") != "zoe_after_deadline_scene")

print("\nE. Callback prerequisites")
reset(fam=40, zoe_second_opinion_done=True, zoe_second_opinion_choice="structure")
chk("The Thing You Noticed needs the stored choice",
    beat_for("location_park") == "zoe_noticed_callback_scene")
reset(fam=40, zoe_second_opinion_done=True)
chk("...and never fires without it", beat_for("location_park") is None)

print("\nF. Talk wrapper")
chk("shipping resolver keeps absolute priority", talk("martha") == "REAL")
reset()
chk("Zoe routes to the priority menu", talk("zoe") == "zoe_thread_talk")
store.zoe_met = False
chk("no menu before she is met", talk("zoe") is None)
chk("other NPCs unaffected", talk("nora") is None)

print("\nG. Initiative registration")
msgs, variants = G["_INITIATIVE_MSGS"], G["_INITIATIVE_VARIANTS"]["zoe"]
chk("14 new variants registered", len(G["_ZOE_ARC_MSGS"]) == 14, len(G["_ZOE_ARC_MSGS"]))
chk("all appended to the shipping picker pool",
    all(v in variants for v in G["_ZOE_ARC_MSGS"]))
chk("existing zoe variants preserved", "zoe_msg_photo" in variants)
chk("every variant has text + responses",
    all(m.get("text") and m.get("responses") for m in G["_ZOE_ARC_MSGS"].values()))
chk("every variant has a tier and a weight",
    all(v in G["_VARIANT_MIN_TIER"] and v in G["_VARIANT_WEIGHTS"]
        for v in G["_ZOE_ARC_MSGS"]))
chk("response labels are unique",
    len(set(r["label"] for m in G["_ZOE_ARC_MSGS"].values() for r in m["responses"]))
    == sum(len(m["responses"]) for m in G["_ZOE_ARC_MSGS"].values()))
chk("check-in variants require comfortable+ (tier >= 1)",
    G["_VARIANT_MIN_TIER"]["zoe_msg_alive"] >= 1
    and G["_VARIANT_MIN_TIER"]["zoe_msg_taking_personally"] >= 2
    and G["_VARIANT_MIN_TIER"]["zoe_msg_bad_email"] >= 2)

cond = G["_VARIANT_CONDITIONS"]
reset()
store.npc_last_seen = {"zoe": store.day - 4}
chk("'You alive?' blocked at a 4-day gap", not cond["zoe_msg_alive"]())
store.npc_last_seen = {"zoe": store.day - 5}
chk("'You alive?' opens at a 5-day gap", cond["zoe_msg_alive"]())
store.npc_last_seen = {"zoe": store.day - 7}
chk("'taking it personally' opens at a 7-day gap", cond["zoe_msg_taking_personally"]())
reset()
chk("beige callback blocked before the beige scene", not cond["zoe_msg_beige_callback"]())
store.zoe_beige_done = True
chk("beige callback opens after it", cond["zoe_msg_beige_callback"]())
reset()
chk("bass text blocked before the bass history is known",
    not cond["zoe_msg_bass_window"]())
reset(zoe_second_opinion_done=True, zoe_second_opinion_day=store.day - 2)
chk("second-opinion callback waits 3 days", not cond["zoe_msg_secopin_callback"]())
store.zoe_second_opinion_day = store.day - 3
chk("...and opens on day 3", cond["zoe_msg_secopin_callback"]())
store.zoe_second_opinion_callback_done = True
chk("...and never repeats once answered", not cond["zoe_msg_secopin_callback"]())
reset(zoe_second_opinion_pending=True, knows_zoe_art_interest=True)
chk("second-opinion offer suppressed while one is already pending",
    not cond["zoe_msg_second_opinion"]())

print("\nH. Scene Tester registry")
REG = G["SCENE_TEST_REGISTRY"]
labels = set(re.findall(r"^label\s+([a-z_0-9]+)", SRC, re.M))
chk("5 entries registered", len(REG) == 5, len(REG))
chk("every entry has a callable reset (the screen calls Function(reset))",
    all(callable(e["reset"]) for e in REG.values()))
chk("every entry has at least one preset",
    all(e["presets"] for e in REG.values()))
chk("every preset is callable",
    all(callable(p) for e in REG.values() for p in e["presets"].values()))
chk("every entry category is a real tester category",
    all(e["category"] == "Relationship Scenes" for e in REG.values()))
chk("every scene label exists in this file (bar the state-only entry)",
    all(e["label"] in labels or e["label"] == "map" for e in REG.values()))

print("\nI. Script integrity")
dispatch_targets = set(re.findall(r'return\s+"(zoe_[a-z_0-9]+)"', init_block(2)))
chk("every label the dispatcher can return exists",
    all(t in labels for t in dispatch_targets),
    ",".join(sorted(t for t in dispatch_targets if t not in labels)))
reply_labels = set(re.findall(r'"label":\s*"(npc_ini_zoe_[a-z_0-9]+)"', SRC))
chk("every initiative reply label exists",
    all(l in labels for l in reply_labels),
    ",".join(sorted(l for l in reply_labels if l not in labels)))
chk("every beat label restores the HUD",
    SRC.count('$ set_hud("hidden")') == SRC.count('$ story_scene_active = True')
    and 'jump expression _zarc_dest' in SRC)

print("\n%s  (%d failure(s))" % ("ALL PASS" if not FAILS else "FAILURES: " + ", ".join(FAILS),
                                len(FAILS)))
sys.exit(1 if FAILS else 0)
