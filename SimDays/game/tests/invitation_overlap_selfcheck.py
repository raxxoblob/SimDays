"""Invitation vs. schedule-override overlap self-check.

Same approach as summer_festival_selfcheck.py: extracts the real `init python`
blocks from npc_schedules.rpy + npc_invitations.rpy and execs them against a
stub store, so every assertion runs the SHIPPING code.

    python invitation_overlap_selfcheck.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from summer_festival_selfcheck import (  # reuse the extractor + stubs
    rpy_python_blocks, rpy_defaults, Store, _Renpy, GAME)

store = Store()
G = {
    "store": store,
    "renpy": _Renpy(),
    "MON_FRI": {0, 1, 2, 3, 4}, "MON_SAT": {0, 1, 2, 3, 4, 5},
    "WKD": {5, 6}, "FRISUN": {4, 5, 6},
    "NPC_DATA": {n: {"name": n.capitalize(), "aff": n + "_aff", "sched": []}
                 for n in ("marcus", "eli", "zoe", "nora")},
    "LOCATION_DEFS": {},
    "npc_is_temporarily_unavailable": lambda nid: False,
    "npc_schedule_entries": lambda nid: [],
    "cafe_bg": lambda: "cafeday",
    "DAY_NAMES": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                  "Saturday", "Sunday"],
    "LOCATION_NAMES": {"location_bar": "the bar", "location_cafe": "Grounds Café"},
    "apply_relationship_change": lambda *a, **k: {},
    "add_relationship_memory": lambda *a, **k: None,
    "record_game_event": lambda *a, **k: None,
    "invitation_acceptance_chance": lambda nid, at: 1.0,
    "spend_time": lambda h: None,
    "npc_sprite": lambda *a, **k: "",
}
for _f in ("npc_schedules.rpy", "phone_messages.rpy", "calendar.rpy",
           "npc_invitations.rpy"):
    for k, v in rpy_defaults(_f).items():
        setattr(store, k, list(v) if isinstance(v, list)
                else dict(v) if isinstance(v, dict) else v)
    for blk in rpy_python_blocks(_f, None):
        exec(compile(blk, _f, "exec"), G)

overlap = G["npc_has_override_overlap"]
can_gen = G["can_generate_invitation_for_npc"]
accept = G["accept_npc_invitation"]
# The phone UI calls the wrappers, not the raw functions — test what ships.
ui_accept = G["_accept_npc_invitation_wrapper"]
ui_decline = G["_decline_npc_invitation_wrapper"]
cal_events = G["get_calendar_events"]
card = G["invitation_card_lines"]
expire_pass = G["process_missed_invitations"]

FAILS = []


def chk(label, cond, detail=""):
    if not cond:
        FAILS.append(label)
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", label,
                           ("  — " + str(detail)) if detail else ""))


def fest(npc, day, h0=17, h1=23):
    return {"npc_id": npc, "day": day, "hour_start": h0, "hour_end": h1,
            "location_id": "location_centrum", "activity_id": "at_festival",
            "public": True, "interactable": False, "expires_day": day,
            "source_id": "summer_festival"}


# ── A. overlap formula ───────────────────────────────────────────────────────
print("\nA. overlap formula (marcus, day 5, 17-23)")
store.npc_schedule_overrides = [fest("marcus", 5)]
for label, args, want in (
        ("21-23 fully inside",        (5, 21, 23), True),
        ("16-18 straddles the start", (5, 16, 18), True),
        ("20-22 fully inside",        (5, 20, 22), True),
        ("15-24 spans entirely",      (5, 15, 24), True),
        ("14-17 ends on boundary",    (5, 14, 17), False),
        ("23-24 starts on boundary",  (5, 23, 24), False),
        ("10-16 entirely before",     (5, 10, 16), False),
        ("24-25 entirely after",      (5, 24, 25), False)):
    chk(label, overlap("marcus", *args) is want)
chk("different NPC same window is free", not overlap("eli", 5, 21, 23))
chk("different day same NPC is free", not overlap("marcus", 6, 21, 23))
chk("pure read — override list untouched", len(store.npc_schedule_overrides) == 1)
store.npc_schedule_overrides = [{"npc_id": "marcus", "day": 5}]
chk("old-save override missing hour fields treated as all-day",
    overlap("marcus", 5, 9, 10))

# ── B. generation-time block ─────────────────────────────────────────────────
print("\nB. generation-time block")
store.active_npc_invitations = []
store.npc_invitation_history = []
store.npc_invitation_week_counts = {}
store.day = 7
store.npc_schedule_overrides = [fest("marcus", 7)]
chk("21-23 overlapping is not offered",
    not can_gen("marcus", proposed_day=7, start_hour=21, end_hour=23))
chk("14-18 overlapping is not offered",
    not can_gen("marcus", proposed_day=7, start_hour=14, end_hour=18))
chk("14-17 up to the boundary is offered",
    can_gen("marcus", proposed_day=7, start_hour=14, end_hour=17))
chk("23-24 from the boundary is offered",
    can_gen("marcus", proposed_day=7, start_hour=23, end_hour=24))
chk("other NPC unaffected", can_gen("eli", proposed_day=7, start_hour=21, end_hour=23))
try:
    _old = can_gen("marcus")
    chk("old call site (npc_id only) still works", _old is True, _old)
except TypeError as e:
    chk("old call site (npc_id only) still works", False, e)
# real generator honours it: marcus template is 21-23 tomorrow
store.day = 6
store.npc_schedule_overrides = [fest("marcus", 7)]
for n in ("marcus", "eli", "zoe", "nora"):
    setattr(store, n + "_met", True)
    setattr(store, n + "_aff", 99)
_elig = [t["id"] for t in G["NPC_INVITATION_TEMPLATES"]
         if can_gen(t["npc"], store.day + t["advance_days"],
                    t["start_hour"], t["end_hour"])]
chk("generate_npc_invitations eligibility drops marcus_static_01",
    "marcus_static_01" not in _elig and "nora_coffee_01" in _elig, _elig)

# ── C. acceptance-time block ─────────────────────────────────────────────────
print("\nC. acceptance-time block")
store.day = 8
store.npc_schedule_overrides = []
store.npc_invitation_history = []
store.npc_messages = []
inv = {"id": "inv_marcus_static_01_day8", "template_id": "marcus_static_01",
       "npc": "marcus", "activity": "bar_visit", "location": "location_bar",
       "proposed_day": 8, "start_hour": 19, "end_hour": 21, "status": "pending",
       "calendar_event_id": None, "consequence_processed": False,
       "rel_gain": 5, "rel_stat": "affection"}
store.active_npc_invitations = [dict(inv)]
chk("slot free at generation time", not overlap("marcus", 8, 19, 21))
store.npc_schedule_overrides = [fest("marcus", 8)]
chk("slot taken before acceptance", overlap("marcus", 8, 19, 21))
_before = len(store.npc_schedule_overrides)
chk("accept returns False", accept(inv["id"]) is False)
chk("no override created", len(store.npc_schedule_overrides) == _before)
chk("no invitation override present",
    not [o for o in store.npc_schedule_overrides
         if str(o.get("source_id", "")).startswith("invitation_")])
chk("invitation dropped from the active list", store.active_npc_invitations == [])
chk("history records cancelled, not accepted/missed",
    [h["status"] for h in store.npc_invitation_history] == ["cancelled"],
    store.npc_invitation_history)
chk("player told by phone message",
    [m["tag"] for m in store.npc_messages] == ["inv_cancel_" + inv["id"]],
    store.npc_messages)

print("\n   happy path still works")
store.npc_schedule_overrides = []
store.active_npc_invitations = [dict(inv)]
store.npc_invitation_history = []
chk("accept returns True when the slot is free", accept(inv["id"]) is True)
_ovs = [o for o in store.npc_schedule_overrides
        if o.get("source_id") == "invitation_" + inv["id"]]
chk("exactly one invitation override created", len(_ovs) == 1, _ovs)
chk("override window matches the invitation",
    _ovs and (_ovs[0]["hour_start"], _ovs[0]["hour_end"], _ovs[0]["day"]) == (19, 21, 8))
chk("status is accepted",
    store.active_npc_invitations[0]["status"] == "accepted")
# NOTE: this is a logic-level check, not a full integration test — the phone UI
# path that calls accept_npc_invitation is not exercised here.

# ── D. summer festival regression ────────────────────────────────────────────
print("\nD. summer festival regression (marcus, day 12, 17-23)")
store.npc_schedule_overrides = [fest("marcus", 12)]
chk("21-23 blocked", overlap("marcus", 12, 21, 23))
chk("14-17 allowed", not overlap("marcus", 12, 14, 17))
chk("23-24 allowed", not overlap("marcus", 12, 23, 24))
chk("16-18 blocked", overlap("marcus", 12, 16, 18))


def pending(inv_id, day, h0=19, h1=21, status="pending", npc="marcus"):
    return {"id": inv_id, "template_id": "marcus_static_01", "npc": npc,
            "activity": "bar_visit", "location": "location_bar",
            "proposed_day": day, "start_hour": h0, "end_hour": h1,
            "status": status, "calendar_event_id": None,
            "consequence_processed": False, "rel_gain": 5,
            "rel_stat": "affection"}


def reset(invs):
    store.day = 8
    store.active_npc_invitations = list(invs)
    store.npc_schedule_overrides = []
    store.npc_invitation_history = []
    store.npc_messages = []
    store.calendar_events = []
    store._inv_effects_applied = []


def find(inv_id):
    return next((i for i in store.active_npc_invitations if i["id"] == inv_id), None)


# ── E. full acceptance flow through the UI wrapper ───────────────────────────
print("\nE. full acceptance flow (phone Accept button path)")
reset([pending("test_inv_001", 10)])
ui_accept("test_inv_001")
chk("status is accepted", find("test_inv_001")["status"] == "accepted")
_ce = cal_events(day=10)
chk("calendar commitment created for the NPC",
    any(e.get("npc_id") == "marcus" and e.get("commitment") for e in _ce), _ce)
chk("calendar event links back to the invitation",
    any(e.get("invitation_id") == "test_inv_001" for e in _ce))
chk("schedule override created", overlap("marcus", 10, 19, 21))
chk("second Accept click is a no-op",
    accept("test_inv_001") is False
    and len([o for o in store.npc_schedule_overrides
             if o.get("source_id") == "invitation_test_inv_001"]) == 1
    and len(store.calendar_events) == 1)
chk("card shows the accepted status, not buttons",
    card(find("test_inv_001"))[3] == "Accepted", card(find("test_inv_001")))

# ── F. conflict blocks acceptance through the UI path ────────────────────────
print("\nF. conflict blocks acceptance (UI path)")
reset([pending("test_inv_002", 12, 20, 22)])
store.npc_schedule_overrides = [fest("marcus", 12)]      # 17-23, inserted first
ui_accept("test_inv_002")
chk("invitation is gone from the actionable list", find("test_inv_002") is None)
chk("history says cancelled",
    [h["status"] for h in store.npc_invitation_history] == ["cancelled"],
    store.npc_invitation_history)
chk("no invitation override created",
    not [o for o in store.npc_schedule_overrides
         if str(o.get("source_id", "")).startswith("invitation_")])
chk("no calendar event created", store.calendar_events == [])
chk("rain-check message delivered to the player",
    [(m["tag"], m["delivered"]) for m in store.npc_messages]
    == [("inv_cancel_test_inv_002", True)], store.npc_messages)

# ── G. already-resolved invitations are inert ────────────────────────────────
print("\nG. already-resolved invitations are inert")
reset([pending("test_inv_003", 15, status="declined")])
chk("declined cannot be accepted", accept("test_inv_003") is False)
chk("status stays declined", find("test_inv_003")["status"] == "declined")
chk("no override, no calendar event",
    store.npc_schedule_overrides == [] and store.calendar_events == [])
chk("declined cannot be declined twice", G["decline_npc_invitation"]("test_inv_003") is False)
chk("no duplicate history row", store.npc_invitation_history == [])
reset([pending("test_inv_004", 15)])
ui_decline("test_inv_004")
chk("one decline drops it from the actionable list", find("test_inv_004") is None)
chk("one decline writes exactly one history row",
    [h["status"] for h in store.npc_invitation_history] == ["declined"])
chk("decline creates no override and no calendar event",
    store.npc_schedule_overrides == [] and store.calendar_events == [])

# ── H. ignored invitations expire (else they block all future ones) ──────────
print("\nH. ignored pending invitations expire")
reset([pending("test_inv_005", 8)])
store.day = 9
expire_pass()
chk("pending invitation past its day is dropped", store.active_npc_invitations == [])
chk("no relationship-penalty message for a never-accepted invite",
    store.npc_messages == [], store.npc_messages)
chk("a new invitation can be generated again", can_gen("eli"))

# ── I. commitment cancellation (the phone Messages "Cancel" button) ──────────
# The button's action is exactly Function(cancel_commitment, id, late) — no
# extra logic in the screen — so calling the function here tests what ships.
print("\nI. commitment cancellation")
TRUST = []
G["_apply_trust"] = lambda nid, d: TRUST.append((nid, d))
add_commitment = G["add_commitment"]
cancel = G["cancel_commitment"]
upcoming = G["upcoming_commitments"]


def commit(cid):
    return next((c for c in store.player_commitments if c["id"] == cid), None)


store.day = 5
store.hour = 12.0
store.player_commitments = []
store.npc_messages = []
store.npc_schedule_overrides = []
del TRUST[:]
add_commitment("test_commit_001", "lena", "Case observation", 10, 19,
               "Hospital", "nop")
chk("commitment is listed as upcoming",
    [c["id"] for c in upcoming()] == ["test_commit_001"])
cancel("test_commit_001", False)
chk("cancelled flag set", commit("test_commit_001").get("cancelled") is True)
chk("not marked missed — no-shows stay distinguishable",
    commit("test_commit_001").get("missed") is False)
chk("gone from the actionable list", upcoming() == [])
chk("early-cancel trust penalty applied once", TRUST == [("lena", -2)], TRUST)
chk("NPC reply queued", [m["tag"] for m in store.npc_messages]
    == ["cancel_test_commit_001"], store.npc_messages)
# double-cancel must not double-penalise (guarded by _c_active)
cancel("test_commit_001", True)
chk("second cancel does not re-penalise", TRUST == [("lena", -2)], TRUST)
chk("second cancel queues no second message",
    len(store.npc_messages) == 1, store.npc_messages)
# late cancel (< 4h out) costs more
store.player_commitments = []
store.npc_messages = []
del TRUST[:]
add_commitment("test_commit_00b", "lena", "Case observation", 5, 14,
               "Hospital", "nop")
cancel("test_commit_00b", True)
chk("late-cancel uses the higher penalty", TRUST == [("lena", -4)], TRUST)
# unknown NPC falls back to the default penalty pair, unknown id is inert
del TRUST[:]
cancel("no_such_commitment", False)
chk("cancelling an unknown id is a no-op", TRUST == [])

# ── J. terminal-state commitments cannot be cancelled ────────────────────────
print("\nJ. terminal-state commitments are not cancellable")
store.day = 15
store.npc_messages = []
del TRUST[:]
store.player_commitments = []
add_commitment("test_commit_002", "nora", "Past thing", 10, 19, "Café", "nop")
commit("test_commit_002")["completed"] = True
cancel("test_commit_002", False)
chk("completed commitment keeps its status",
    commit("test_commit_002")["completed"] is True
    and commit("test_commit_002").get("cancelled") is False)
chk("no penalty for a completed commitment", TRUST == [], TRUST)
add_commitment("test_commit_003", "nora", "Missed thing", 10, 19, "Café", "nop")
commit("test_commit_003")["missed"] = True
cancel("test_commit_003", False)
chk("missed commitment keeps its status",
    commit("test_commit_003").get("cancelled") is False)
chk("past commitments are not offered in the UI list", upcoming() == [], upcoming())

# ── K. accepted invitations are a SEPARATE store from player_commitments ─────
# accept_npc_invitation() creates a calendar event + schedule override, NOT a
# player_commitments row, so cancel_commitment() cannot reach it. This check
# pins that boundary: if a future change makes invitations write commitments,
# the cancel button starts covering them and this test must be revisited.
print("\nK. invitation acceptance vs. the commitment store")
reset([pending("test_inv_006", 10)])
store.player_commitments = []
del TRUST[:]
ui_accept("test_inv_006")
chk("accept creates a calendar commitment + override",
    len(store.calendar_events) == 1 and overlap("marcus", 10, 19, 21))
chk("accept creates NO player_commitments row",
    store.player_commitments == [], store.player_commitments)
chk("nothing cancellable appears in the Upcoming panel",
    upcoming() == [], upcoming())
cancel("test_inv_006", False)
chk("cancel_commitment on an invitation id is inert",
    TRUST == [] and len(store.calendar_events) == 1
    and overlap("marcus", 10, 19, 21))
chk("cancel_accepted_invitation still writes no player_commitments row",
    G["cancel_accepted_invitation"]("test_inv_006") is True
    and store.player_commitments == [], store.player_commitments)

# ── L–Q. player cancellation of an ACCEPTED invitation ───────────────────────
cancel_inv = G["cancel_accepted_invitation"]
ui_cancel = G["_cancel_accepted_invitation_wrapper"]
REL = []
G["apply_relationship_change"] = (
    lambda npc, sid, cat, **kw: REL.append((npc, sid, cat, kw)) or {})


def inv_overrides(inv_id):
    return [o for o in store.npc_schedule_overrides
            if o.get("source_id") == "invitation_" + inv_id]


def cal(event_id):
    return next((e for e in store.calendar_events if e["id"] == event_id), None)


def setup_accepted(inv_id, day, h0=19, h1=21, now_day=8, now_hour=12.0):
    reset([pending(inv_id, day, h0, h1)])
    store.day = now_day
    store.hour = now_hour
    store.player_commitments = []
    del REL[:]
    ui_accept(inv_id)
    store.npc_messages = []          # drop the invitation text itself
    return find(inv_id)


# ── L. early cancellation ────────────────────────────────────────────────────
print("\nL. early cancellation (two days out)")
_iv = setup_accepted("test_inv_L", 10)
_cal_id = _iv["calendar_event_id"]
chk("precondition: override + calendar commitment exist",
    len(inv_overrides("test_inv_L")) == 1 and cal(_cal_id)["status"] == "upcoming")
chk("cancel returns True", cancel_inv("test_inv_L") is True)
chk("status is cancelled", find("test_inv_L")["status"] == "cancelled")
chk("invitation override removed", inv_overrides("test_inv_L") == [])
chk("NPC is free again in that window", not overlap("marcus", 10, 19, 21))
chk("calendar event marked cancelled", cal(_cal_id)["status"] == "cancelled")
chk("player_commitments untouched", store.player_commitments == [],
    store.player_commitments)
chk("no relationship change for an early cancel", REL == [], REL)
chk("early reply queued exactly once",
    [m["tag"] for m in store.npc_messages] == ["inv_player_cancel_test_inv_L"],
    store.npc_messages)
chk("early reply uses the forgiving text",
    store.npc_messages[0]["text"] == "Sure, no worries. Another time.")
chk("history records the player cancellation",
    "player_cancelled" in [h["status"] for h in store.npc_invitation_history],
    store.npc_invitation_history)
chk("card shows Cancelled", card(find("test_inv_L"))[3] == "Cancelled")
store.day = 11
expire_pass()
chk("cancelled invitation is swept so future ones can generate",
    store.active_npc_invitations == [], store.active_npc_invitations)

# ── M. late cancellation (< 4h out) ──────────────────────────────────────────
print("\nM. late cancellation (same day, 2h out)")
setup_accepted("test_inv_M", 8, 14, 16, now_day=8, now_hour=12.0)
chk("cancel returns True", cancel_inv("test_inv_M") is True)
chk("one relationship change applied", len(REL) == 1, REL)
chk("it is a small trust hit",
    REL and REL[0][3].get("trust") == -2
    and not REL[0][3].get("affection") and not REL[0][3].get("respect"), REL)
chk("penalty is smaller than the no-show penalty (aff -4 / trust -3 / resp -2)",
    REL and abs(REL[0][3].get("trust", 0)) < 3 + 4 + 2)
chk("late reply queued once",
    [m["tag"] for m in store.npc_messages] == ["inv_player_cancel_test_inv_M"])
chk("late reply uses the pointed text",
    store.npc_messages[0]["text"]
    == "Okay. Wish you'd said something a little sooner.")
chk("hours_until_invitation reports 2h for this case",
    G["hours_until_invitation"](find("test_inv_M")) == 2.0)

# ── N. double cancellation ───────────────────────────────────────────────────
print("\nN. double cancellation")
setup_accepted("test_inv_N", 8, 14, 16, now_day=8, now_hour=12.0)
cancel_inv("test_inv_N")
_rel_after_first = list(REL)
_msgs_after_first = len(store.npc_messages)
chk("second cancel returns False", cancel_inv("test_inv_N") is False)
chk("no second relationship change", REL == _rel_after_first, REL)
chk("no second message", len(store.npc_messages) == _msgs_after_first)
chk("status stays cancelled", find("test_inv_N")["status"] == "cancelled")

# ── O. started / past invitations cannot be cancelled ────────────────────────
print("\nO. started or past invitations cannot be cancelled")
setup_accepted("test_inv_O1", 8, 14, 16, now_day=8, now_hour=12.0)
store.hour = 14.0
chk("start_hour == now returns False", cancel_inv("test_inv_O1") is False)
store.hour = 15.0
chk("mid-meeting returns False", cancel_inv("test_inv_O1") is False)
chk("status still accepted", find("test_inv_O1")["status"] == "accepted")
chk("override survives", len(inv_overrides("test_inv_O1")) == 1)
chk("no message, no relationship change",
    store.npc_messages == [] and REL == [])
setup_accepted("test_inv_O2", 8, 14, 16, now_day=8, now_hour=12.0)
store.day = 9
chk("past day returns False", cancel_inv("test_inv_O2") is False)
chk("status still accepted", find("test_inv_O2")["status"] == "accepted")

# ── P. override removal is invitation-specific ───────────────────────────────
print("\nP. override removal only touches this invitation")
setup_accepted("test_inv_P", 10)
store.npc_schedule_overrides = [fest("marcus", 12)] + store.npc_schedule_overrides
chk("precondition: festival + invitation overrides both present",
    len(store.npc_schedule_overrides) == 2)
chk("cancel returns True", cancel_inv("test_inv_P") is True)
chk("invitation override removed", inv_overrides("test_inv_P") == [])
chk("festival override survives",
    [o["source_id"] for o in store.npc_schedule_overrides] == ["summer_festival"],
    store.npc_schedule_overrides)
chk("festival window still blocks", overlap("marcus", 12, 21, 23))

# ── Q. non-accepted statuses are inert ───────────────────────────────────────
print("\nQ. non-accepted statuses are inert")
for _st in ("completed", "missed", "declined", "pending", "left_early", "expired"):
    reset([pending("test_inv_Q_" + _st, 10, status=_st)])
    store.hour = 12.0
    del REL[:]
    _r = cancel_inv("test_inv_Q_" + _st)
    chk("%s cannot be cancelled" % _st,
        _r is False and find("test_inv_Q_" + _st)["status"] == _st
        and REL == [] and store.npc_messages == [])
chk("unknown invitation id is inert", cancel_inv("no_such_invitation") is False)

print("\n%s  (%d failure%s)" % ("FAILED" if FAILS else "ALL PASS",
                               len(FAILS), "" if len(FAILS) == 1 else "s"))
for f in FAILS:
    print("   - " + f)
sys.exit(1 if FAILS else 0)
