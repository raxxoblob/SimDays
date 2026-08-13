"""Downtown Summer Festival runtime self-check.

Same approach as phase66-69: EXTRACTS the real `init python` blocks out of the
shipping .rpy files and execs them against a stub `store`, so every assertion
below runs the SHIPPING code. Change the state dict, the scheduling window, the
blackout difficulty or the follow-up mail tag and this fails.

    python summer_festival_selfcheck.py
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
    """`default name = <literal>` lines. Multi-line dict/list literals included."""
    out = {}
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read()
    for m in re.finditer(r"^default\s+(\w+)\s*=\s*(.+?)$", src, re.M):
        name, first = m.group(1), m.group(2)
        chunk = first
        if first.count("{") > first.count("}") or first.count("[") > first.count("]"):
            tail = src[m.end():]
            depth = first.count("{") - first.count("}") + first.count("[") - first.count("]")
            buf = []
            for ln in tail.split("\n"):
                buf.append(ln)
                depth += ln.count("{") + ln.count("[") - ln.count("}") - ln.count("]")
                if depth <= 0:
                    break
            chunk = first + "\n" + "\n".join(buf)
        chunk = re.sub(r"#.*$", "", chunk, flags=re.M)
        try:
            out[name] = eval(chunk, {"__builtins__": {}}, {})
        except Exception:
            pass
    return out


DEFAULTS = {}
for _f in ("data.rpy", "mail.rpy", "calendar.rpy", "phone_messages.rpy",
           "possessions.rpy", "world_pulse.rpy", "npc_schedules.rpy",
           "npc_relationships.rpy", "summer_festival.rpy"):
    DEFAULTS.update(rpy_defaults(_f))


class Store(object):
    def __init__(self):
        self.day = 20
        self.hour = 12.0
        self.money = 500
        self.need_energy = 80
        self.npc_messages = []
        self.unlocked_locations = []
        self._check_pity = {}
        self._check_attempts = {}
        for k, v in DEFAULTS.items():
            setattr(self, k,
                    list(v) if isinstance(v, list) else
                    dict(v) if isinstance(v, dict) else v)
        # After the defaults, so the shipping `default X_met = False` lines
        # don't clobber the premise of the test.
        for k in ("cook", "fit", "art", "prog", "mech", "music", "biz"):
            setattr(self, "skill_" + k, 5)
        self.marcus_met = self.eli_met = self.zoe_met = self.nora_met = True


class _Config(object):
    developer = False


class _Renpy(object):
    config = _Config()

    def notify(self, *a, **k):
        return None

    def log(self, *a, **k):
        return None

    def image(self, *a, **k):
        return None

    def loadable(self, path):
        return os.path.exists(os.path.join(GAME, path))


store = Store()
RENPY = _Renpy()
_events = []
G = {}


def boot():
    global G
    G = {
        "store": store,
        "renpy": RENPY,
        "Transform": lambda *a, **k: None,
        "DAY_NAMES": ["Monday", "Tuesday", "Wednesday", "Thursday",
                      "Friday", "Saturday", "Sunday"],
        "record_game_event": lambda eid, cat, title, **k: _events.append((eid, cat, title)),
        "gain_skill": lambda k, a=1: None,
        "gain_skill_practice": lambda k, x, h=1: x,
        "gain_money": lambda *a, **k: None,
        "spend_time": lambda h: None,
        "skill_val": lambda k: getattr(store, "skill_" + k, 0),
        "is_location_unlocked": lambda lid: True,
        "npc_known": lambda nid: True,
        "npc_is_temporarily_unavailable": lambda nid: False,
        "NPC_DATA": {n: {"name": n.capitalize()} for n in
                     ("marcus", "eli", "zoe", "nora")},
        "NPC_INTERESTS": {},
        # Names owned by files this check deliberately does not exec whole.
        "PRO_SKILLS": {"cook": {}, "fit": {}, "art": {}, "prog": {},
                       "mech": {}, "music": {}, "biz": {}, "med": {}},
        "MON_FRI": {0, 1, 2, 3, 4}, "MON_SAT": {0, 1, 2, 3, 4, 5},
        "WKD": {5, 6}, "FRISUN": {4, 5, 6},
        "npc_rel": lambda nid, axis, default=0: 0,
        "npc_interest": lambda nid, domain: 0,
        "npc_relationship_stage": lambda nid: "friend",
        "npc_rel_profile": lambda nid: {"openness": 0.5, "social_selectiveness": 0.5,
                                        "saturation_rate": 0.5},
        "apply_relationship_change": lambda *a, **k: {},
        "has_possession": None,      # replaced by the real one below
    }
    for path, prio in (("resolution_checks.rpy", None),
                       ("mail.rpy", None),
                       ("calendar.rpy", None),
                       ("phone_messages.rpy", None),
                       ("npc_schedules.rpy", None),
                       ("possessions.rpy", None),
                       ("world_pulse.rpy", 1),
                       ("summer_festival.rpy", 2)):
        for blk in rpy_python_blocks(path, prio):
            try:
                exec(compile(blk, path, "exec"), G)
            except Exception as e:                     # noqa: BLE001
                print("  (skipped a block in %s: %s: %s)" % (path, type(e).__name__, e))
    G["store"] = store


FAILS = []


def chk(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    if not cond:
        FAILS.append(label)
    print("  [%s] %s%s" % (status, label, ("  — " + str(detail)) if detail else ""))


def main():
    boot()
    sf_default = DEFAULTS["summer_festival_state"]

    # ── A. state initialises correctly / old-save safe ───────────────────────
    print("\nA. state dict")
    expected_keys = {"scheduled_day", "eligible", "discovered", "attended",
                     "missed", "blackout_choice", "blackout_result",
                     "shelter_focus", "keepsake_awarded",
                     "follow_up_mail_queued", "aftermath_done", "sync_run_day"}
    chk("summer_festival_state parsed from a single `default`",
        isinstance(sf_default, dict), type(sf_default).__name__)
    chk("all 12 keys present", set(sf_default) == expected_keys,
        sorted(expected_keys ^ set(sf_default)) or "exact match")
    chk("unscheduled sentinel is -1", sf_default["scheduled_day"] == -1)
    chk("no boolean starts True",
        not any(v is True for v in sf_default.values()))
    chk("shipping code never subscripts the dict blind",
        "summer_festival_state" in DEFAULTS)

    # ── I. discovery + scheduling are idempotent ─────────────────────────────
    print("\nI. scheduling idempotency")
    store.day = 20
    store.summer_festival_state = dict(sf_default)
    chk("eligible with all four met past day 14", G["summer_festival_eligible"]())
    store.nora_met = False
    chk("not eligible while an NPC is unmet", not G["summer_festival_eligible"]())
    store.nora_met = True
    store.day = 5
    chk("not eligible before SF_MIN_DAY", not G["summer_festival_eligible"]())
    store.day = 20

    d1 = G["schedule_summer_festival"]()
    d2 = G["schedule_summer_festival"]()
    chk("scheduling twice returns the same day", d1 == d2, "day %d" % d1)
    chk("scheduled 4-7 days ahead", 4 <= d1 - 20 <= 7, "+%d" % (d1 - 20))
    chk("prefers Friday or Saturday", d1 % 7 in (4, 5),
        "weekday %d" % (d1 % 7))
    chk("exactly one festival in the pulse for that day",
        len([e for e in store.world_pulse_data[d1]["major_events"]
             if e["template_id"] == "summer_festival"]) == 1)
    chk("exactly one calendar entry",
        len([e for e in store.calendar_events
             if e["title"] == "Downtown Summer Festival"]) == 1)
    chk("the random generator can never pick it",
        G["WORLD_EVENT_TEMPLATES"]["summer_festival"]["day_weights"] == {})
    chk("event registered at location_centrum (downtown)",
        G["SF_LOCATION"] == "location_centrum")

    # ── B. NPC schedule overrides ────────────────────────────────────────────
    print("\nB. NPC schedule overrides")
    ov = [o for o in store.npc_schedule_overrides
          if o.get("source_id") == "summer_festival"]
    chk("one override per festival NPC", len(ov) == 4,
        [o["npc_id"] for o in ov])
    chk("all four NPCs covered",
        {o["npc_id"] for o in ov} == set(G["SF_NPCS"]))
    chk("format matches npc_schedules.rpy",
        all({"npc_id", "day", "hour_start", "hour_end", "location_id",
             "activity_id", "public", "interactable", "expires_day"}
            <= set(o) for o in ov))
    chk("they arrive before the player (17:00) and stay to 23:00",
        all(o["hour_start"] == 17 and o["hour_end"] == 23 for o in ov))
    chk("all overrides expire on the festival day",
        all(o["expires_day"] == d1 for o in ov))
    G["schedule_festival_npcs"](d1)
    chk("re-running schedule_festival_npcs dedupes on source_id",
        len([o for o in store.npc_schedule_overrides
             if o.get("source_id") == "summer_festival"]) == 4)
    store.day = d1 + 1
    G["_expire_schedule_overrides"]()
    chk("overrides self-expire the next day",
        not [o for o in store.npc_schedule_overrides
             if o.get("source_id") == "summer_festival"])
    store.day = 20

    # ── availability window ──────────────────────────────────────────────────
    print("\n   availability window")
    store.day, store.hour = d1, 19.0
    chk("open downtown at 19:00 on the night", G["summer_festival_open_now"]())
    store.hour = 17.0
    chk("closed at 17:00", not G["summer_festival_open_now"]())
    store.hour = 23.5
    chk("closed at 23:30", not G["summer_festival_open_now"]())
    store.hour = 19.0
    store.summer_festival_state["attended"] = True
    chk("closed once attended", not G["summer_festival_open_now"]())
    store.summer_festival_state["attended"] = False

    # ── H. social post format ────────────────────────────────────────────────
    print("\nH. discovery / social post")
    store.day = d1 - 2
    store._pulse_budget_day = -1
    store.social_feed_posts = []
    G["_sf_announce"]()
    posts = [p for p in store.social_feed_posts if str(p["id"]).startswith("sf_")]
    chk("announcement post queued two days out", len(posts) == 1, posts)
    chk("post has the social_feed_posts field set",
        posts and set(posts[0]) >= {"id", "npc_id", "text", "day"}, posts[0] if posts else None)
    chk("post is dated today", posts and posts[0]["day"] == store.day)
    chk("post names the correct weekday",
        posts and G["DAY_NAMES"][d1 % 7] in posts[0]["text"])
    chk("discovery recorded", store.summer_festival_state["discovered"])
    G["_sf_announce"]()
    chk("announcing twice does not duplicate the post",
        len([p for p in store.social_feed_posts
             if str(p["id"]).startswith("sf_announce")]) == 1)
    store.day = d1 - 1
    G["_sf_announce"]()
    G["_sf_announce"]()
    chk("exactly one NPC text the day before",
        len([m for m in store.npc_messages
             if m["tag"] == "summer_festival_marcus_ping"]) == 1)

    # ── D. blackout check ────────────────────────────────────────────────────
    print("\nD. blackout mechanics check")
    dist = G["calculate_check_chance"]("festival_blackout_repair",
                                       skill_val=store.skill_mech, difficulty=52)
    chk("returns a probability dict",
        isinstance(dist, dict) and "distribution" in dist
        and "success_or_better" in dist)
    chk("tiers sum to 100",
        sum(dist["distribution"].values()) == 100, dist["distribution"])
    chk("skill 5 vs difficulty 52 is a real risk, not a formality",
        20 <= dist["success_or_better"] <= 95, dist["success_or_better"])
    chk("higher mechanics improves the odds",
        G["calculate_check_chance"]("festival_blackout_repair", 8, 52)["success_or_better"]
        > G["calculate_check_chance"]("festival_blackout_repair", 1, 52)["success_or_better"])
    r1 = G["roll_check"]("festival_blackout_repair", 5, 52, stable=True)
    store._check_pity = {}
    r2 = G["roll_check"]("festival_blackout_repair", 5, 52, stable=True)
    chk("stable=True: same day + same attempt = same roll (no save-scum)",
        r1["raw_roll"] == r2["raw_roll"], "%s / %s" % (r1["tier"], r2["tier"]))
    chk("tier is one of the Phase 60 five",
        r1["tier"] in ("critical_failure", "weak", "success", "great", "critical"))

    # ── C. keepsake ──────────────────────────────────────────────────────────
    print("\nC. keepsake")
    chk("festival_wristband already exists in POSSESSION_CATALOG "
        "(no duplicate added)", "festival_wristband" in G["POSSESSION_CATALOG"])
    src = "summer_festival_day%d" % d1
    chk("first grant succeeds", G["grant_possession"]("festival_wristband", src))
    chk("second grant from the same source is a no-op",
        not G["grant_possession"]("festival_wristband", src))
    chk("exactly one instance held",
        len([p for p in store.player_possessions
             if p["item_id"] == "festival_wristband"]) == 1)

    # ── F. accomplishment dedupe ─────────────────────────────────────────────
    print("\nF. accomplishment")
    a1 = G["record_accomplishment"]("attended_summer_festival", "A Night at the Festival",
                                    "desc", "social")
    a2 = G["record_accomplishment"]("attended_summer_festival", "A Night at the Festival",
                                    "desc", "social")
    chk("first record returns True", a1)
    chk("second record is a no-op", not a2)
    chk("one accomplishment stored",
        len([a for a in store.player_accomplishments
             if a["id"] == "attended_summer_festival"]) == 1)

    # ── E. follow-up mail ────────────────────────────────────────────────────
    print("\nE. follow-up mail + aftermath")
    store.day = d1 + 1
    store._pulse_budget_day = -1
    store.summer_festival_state["attended"] = True
    store.summer_festival_state["follow_up_mail_queued"] = True
    store.summer_festival_state["shelter_focus"] = "zoe"
    G["_queue_festival_aftermath"](True)
    chk("organiser mail queued",
        G["mail_already_queued"]("summer_festival_organizer_followup"))
    chk("mail lands 3 days later",
        next(m for m in store.player_mail
             if m["tag"] == "summer_festival_organizer_followup")["send_on_day"]
        == store.day + 3)
    chk("exactly ONE personal follow-up, from the shelter NPC",
        [m["npc_id"] for m in store.npc_messages
         if m["tag"].startswith("summer_festival_followup")] == ["zoe"])
    chk("aftermath social post exists",
        any(str(p["id"]).startswith("sf_after") for p in store.social_feed_posts))
    G["_queue_festival_aftermath"](True)
    chk("re-running aftermath duplicates nothing",
        len([m for m in store.player_mail
             if m["tag"] == "summer_festival_organizer_followup"]) == 1
        and len([p for p in store.social_feed_posts
                 if str(p["id"]).startswith("sf_after")]) == 1)

    # ── G. missed festival ───────────────────────────────────────────────────
    print("\nG. missed festival")
    store.summer_festival_state = dict(sf_default)
    store.summer_festival_state["scheduled_day"] = d1
    store.day = d1
    chk("not missed on the day itself", not G["check_festival_expiry"]())
    store.day = d1 + 1
    chk("missed the day after", G["check_festival_expiry"]())
    chk("missed flag set", store.summer_festival_state["missed"])
    store.day = d1 + 2
    chk("does not re-fire on later days", not G["check_festival_expiry"]())
    store.summer_festival_state["attended"] = True
    store.summer_festival_state["missed"] = False
    store.day = d1 + 1
    chk("attending prevents the missed flag entirely",
        not G["check_festival_expiry"]() and not store.summer_festival_state["missed"])

    # ── daily sync idempotency ───────────────────────────────────────────────
    print("\n   daily sync idempotency")
    store.summer_festival_state = dict(sf_default)
    store.world_pulse_data = {}
    store.calendar_events = []
    store.npc_schedule_overrides = []
    store.day = 20
    G["sync_summer_festival"]()
    sched = store.summer_festival_state["scheduled_day"]
    G["sync_summer_festival"]()
    G["sync_summer_festival"]()
    chk("sync runs at most once per day",
        store.summer_festival_state["sync_run_day"] == 20)
    chk("repeated sync does not reschedule",
        store.summer_festival_state["scheduled_day"] == sched)
    chk("repeated sync does not duplicate the calendar entry",
        len(store.calendar_events) == 1)

    # ── J. debug reset ───────────────────────────────────────────────────────
    print("\nJ. debug reset")
    dbg = rpy_python_blocks("debug_summer_festival.rpy", None)
    chk("debug block extracted", len(dbg) == 1)
    for blk in dbg:
        exec(compile(blk, "debug_summer_festival.rpy", "exec"), G)
    G["_debug_festival_reset"]()
    chk("reset restores the shipping defaults exactly",
        store.summer_festival_state == sf_default,
        store.summer_festival_state)
    chk("debug default table matches the `default` statement",
        G["_SF_DEFAULT_STATE"] == sf_default)
    chk("reset clears festival schedule overrides",
        not [o for o in store.npc_schedule_overrides
             if o.get("source_id") == "summer_festival"])

    # ── K. clear_schedule_overrides — all four call signatures ──────────────────
    print("\nK. clear_schedule_overrides filter semantics")
    def _make_overrides():
        return [
            {"npc_id": "marcus", "day": 10, "hour_start": 17, "hour_end": 23,
             "location_id": "location_centrum", "activity_id": "at_festival",
             "public": True, "interactable": False, "expires_day": 10,
             "source_id": "summer_festival"},
            {"npc_id": "eli",    "day": 10, "hour_start": 17, "hour_end": 23,
             "location_id": "location_centrum", "activity_id": "at_festival",
             "public": True, "interactable": False, "expires_day": 10,
             "source_id": "summer_festival"},
            {"npc_id": "marcus", "day": 12, "hour_start": 21, "hour_end": 23,
             "location_id": "location_bar",     "activity_id": "meeting_player",
             "public": True, "interactable": True, "expires_day": 12,
             "source_id": "invitation_01"},
        ]

    # npc_id only — removes all overrides for that NPC across all days
    store.npc_schedule_overrides = _make_overrides()
    G["clear_schedule_overrides"](npc_id="marcus")
    remaining_nids = [o["npc_id"] for o in store.npc_schedule_overrides]
    chk("npc_id only: all marcus overrides removed",
        "marcus" not in remaining_nids, remaining_nids)
    chk("npc_id only: eli override untouched",
        remaining_nids == ["eli"], remaining_nids)

    # day only — removes all overrides for that day across all NPCs
    store.npc_schedule_overrides = _make_overrides()
    G["clear_schedule_overrides"](day=10)
    remaining_days = [o["day"] for o in store.npc_schedule_overrides]
    chk("day only: all day-10 overrides removed",
        10 not in remaining_days, remaining_days)
    chk("day only: day-12 override untouched",
        remaining_days == [12], remaining_days)

    # both — intersection: only entries where npc_id AND day both match
    store.npc_schedule_overrides = _make_overrides()
    G["clear_schedule_overrides"](npc_id="marcus", day=10)
    remaining = [(o["npc_id"], o["day"]) for o in store.npc_schedule_overrides]
    chk("both: only (marcus, 10) removed",
        ("marcus", 10) not in remaining, remaining)
    chk("both: (eli, 10) untouched — not a union",
        ("eli", 10) in remaining, remaining)
    chk("both: (marcus, 12) untouched — different day",
        ("marcus", 12) in remaining, remaining)

    # neither — must raise, never silently wipe
    store.npc_schedule_overrides = _make_overrides()
    _raised = False
    try:
        G["clear_schedule_overrides"]()
    except (ValueError, TypeError):
        _raised = True
    chk("neither: raises rather than wiping everything", _raised)
    chk("neither: list is untouched after the raise",
        len(store.npc_schedule_overrides) == 3)

    print("\n%s  (%d failure%s)" % ("FAILED" if FAILS else "ALL PASS",
                                    len(FAILS), "" if len(FAILS) == 1 else "s"))
    for f in FAILS:
        print("   - " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
