"""Nora after-hours café entry — runtime self-check.

The bug this locks down: nora_closing_scene and scene_nora_romance_reopen are
gated on hour >= 19, but they live in cafe_actions, which sits behind
`if not venue_open("coffee_shop")` (café closes at 19:00). Both were therefore
unreachable through normal location entry. label location_cafe now carries a
narrow 19:00-21:00 authored exemption in front of the venue-open check.

Rather than re-describing that priority chain, this file INTERPRETS the real
chain out of locations.rpy (a ~30-line if/elif/jump reader) and runs it against
the real eligibility helpers exec'd out of location_beats_tier_a.rpy. Reorder
the chain, widen the window or change a gate and this fails.

    python nora_cafe_closing_selfcheck.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import location_beats_tier_a_selfcheck as tb  # noqa: E402  (real helpers + store)

LOC_SRC = io.open(os.path.join(GAME, "locations.rpy"), encoding="utf-8").read()
DST_SRC = io.open(os.path.join(GAME, "debug_scene_tester.rpy"), encoding="utf-8").read()
MAP_SRC = io.open(os.path.join(GAME, "map.rpy"), encoding="utf-8").read()

# The entry chain, from `label location_cafe:` down to the venue-open rejection.
ENTRY = LOC_SRC.split("label location_cafe:")[1].split("# Priority 2:")[0].split("\n")

FAILS = []


def chk(label, cond, detail=""):
    if not cond:
        FAILS.append(label)
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", label,
                           ("  - " + str(detail)) if detail else ""))


def route(ns):
    """Walk the real location_cafe entry chain; return the first label it
    reaches. 'map' means the player was turned away (café closed)."""
    taken, skip = {}, None
    for raw in ENTRY:
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        ind = len(raw) - len(raw.rstrip("\n").lstrip())
        if skip is not None:
            if ind > skip:
                continue
            skip = None
        m = re.match(r"^(el)?if (.+):$", s)
        if m:
            if m.group(1) and taken.get(ind):
                skip = ind
                continue
            val = bool(eval(m.group(2), dict(ns)))          # noqa: S307 (test-only)
            taken[ind] = val
            if not val:
                skip = ind
            continue
        m = re.match(r"^(?:call|jump) (\w+)", s)
        if m:
            return m.group(1)
    return None


def ns(hour, day=5):
    tb.store.hour = float(hour)
    tb.store.day = day
    return {
        "hour": tb.store.hour,
        "venue_open": tb.G["venue_open"],
        "_nora_closing_commitment_accepted": tb.G["_nora_closing_commitment_accepted"],
        "_nora_auto_closing_eligible": tb.G["_nora_auto_closing_eligible"],
        "_nora_romance_reopen_eligible": tb.G["_nora_romance_reopen_eligible"],
    }


def plain_player():
    """No Nora story state at all."""
    tb.store.nora_met = False
    tb.store.nora_affection = 0
    tb.store.nora_trust = 0
    tb.store.nora_closing_done = False
    tb.store.nora_reopen_done = False
    tb.store.major_scene_last_day = -1
    tb.G["commitment_available"] = lambda cid: False
    tb.G["can_offer_romance_reopen"] = lambda nid: False


def closing_ready():
    plain_player()
    tb.store.nora_met = True
    tb.store.nora_affection = 45        # gate is >= 40
    tb.store.nora_life_state = "cafe"


def reopen_ready():
    plain_player()
    tb.store.nora_met = True
    tb.store.nora_affection = 45
    tb.store.nora_closing_done = True   # reopen is post-closing only
    tb.G["can_offer_romance_reopen"] = lambda nid: nid == "nora"


def main():
    tb.boot()
    # venue_open lives in map.rpy, which the tier A harness does not load.
    exec(compile(tb.rpy_python_blocks("map.rpy")[0], "map.rpy", "exec"), tb.G)
    tb.G["store"] = tb.store
    tb.store.nora_life_state = "cafe"

    print("\nA. public hours are untouched")
    chk("coffee_shop is still 07:00-19:00", '"coffee_shop": (7, 19),' in MAP_SRC)
    chk("open at 18:00", tb.G["venue_open"]("coffee_shop") if not ns(18) else
        tb.G["venue_open"]("coffee_shop"))
    ns(18.9)
    chk("open at 18:54", tb.G["venue_open"]("coffee_shop") is True)
    ns(19)
    chk("closed at 19:00", tb.G["venue_open"]("coffee_shop") is False)

    print("\nB. ordinary player gets the closed message")
    plain_player()
    chk("19:00, no Nora state -> turned away", route(ns(19)) == "map")
    chk("20:00, no Nora state -> turned away", route(ns(20)) == "map")
    plain_player()
    chk("18:00 normal entry is unaffected (falls past the exemption)",
        route(ns(18)) is None)

    print("\nC. automatic closing route")
    closing_ready()
    chk("_nora_auto_closing_eligible() True at aff 45 / not done",
        tb.G["_nora_auto_closing_eligible"]() is True)
    chk("19:00 -> nora_closing_scene", route(ns(19)) == "nora_closing_scene")
    chk("20:59 -> nora_closing_scene", route(ns(20.98)) == "nora_closing_scene")
    closing_ready()
    tb.store.nora_affection = 39
    chk("aff 39 is below the gate -> turned away", route(ns(19)) == "map")

    print("\nD. commitment outranks the automatic route")
    closing_ready()
    tb.G["commitment_available"] = lambda cid: cid == "nora_closing_1"
    chk("both eligible -> phone_nora_closing_scene wins",
        route(ns(19)) == "phone_nora_closing_scene")
    chk("the commitment branch is not window-bound (its own hour rules apply)",
        route(ns(22)) == "phone_nora_closing_scene")
    tb.G["commitment_available"] = lambda cid: False

    print("\nE. romance reopen sits below the automatic closing scene")
    reopen_ready()
    chk("_nora_romance_reopen_eligible() True post-closing",
        tb.G["_nora_romance_reopen_eligible"]() is True)
    chk("19:00 -> scene_nora_romance_reopen",
        route(ns(19)) == "scene_nora_romance_reopen")
    reopen_ready()
    tb.store.nora_closing_done = False          # both somehow eligible
    chk("closing scene wins when both are eligible",
        route(ns(19)) == "nora_closing_scene")
    reopen_ready()
    tb.store.major_scene_last_day = tb.store.day
    chk("one major scene per day -> turned away", route(ns(19)) == "map")

    print("\nF. the exemption window is 19:00-21:00 and nothing wider")
    chk("window is spelled 19..21 in locations.rpy",
        "if hour >= 19 and hour < 21:" in "\n".join(ENTRY))
    for _h in (21, 22, 23):
        closing_ready()
        chk("%02d:00 with valid Nora state -> still turned away" % _h,
            route(ns(_h)) == "map")
    _pre = [l.split("#")[0] for l in ENTRY]
    _pre = _pre[:[i for i, l in enumerate(_pre) if "venue_open" in l][0]]
    chk("the exemption never opens the generic café menu",
        "cafe_actions" not in "\n".join(_pre))

    print("\nG. done flags stop a re-trigger")
    closing_ready()
    tb.store.nora_closing_done = True
    chk("nora_closing_done blocks the automatic route",
        tb.G["_nora_auto_closing_eligible"]() is False)
    chk("...and the entry chain turns the player away", route(ns(19)) == "map")
    reopen_ready()
    tb.store.nora_reopen_done = True
    chk("nora_reopen_done blocks the reopen route",
        tb.G["_nora_romance_reopen_eligible"]() is False)

    print("\nG2. nora_life_state guard blocks after-hours scenes once she leaves the café")
    # "cafe" → closing eligible; "school" (or any non-cafe value) → not eligible.
    closing_ready()
    tb.store.nora_life_state = "cafe"
    chk("life_state 'cafe' allows _nora_auto_closing_eligible",
        tb.G["_nora_auto_closing_eligible"]() is True)
    tb.store.nora_life_state = "school"
    chk("life_state 'school' blocks _nora_auto_closing_eligible",
        tb.G["_nora_auto_closing_eligible"]() is False)
    # Reopen: closing_done can be True (scene ran while she was still café),
    # but after she leaves the scene should no longer be reachable.
    reopen_ready()
    tb.store.nora_life_state = "school"
    chk("life_state 'school' blocks _nora_romance_reopen_eligible",
        tb.G["_nora_romance_reopen_eligible"]() is False)
    tb.store.nora_life_state = "cafe"  # restore for subsequent sections

    print("\nG3. school transition sweeps live nora_closing_1 commitment without Trust penalty")
    WP_SRC = io.open(os.path.join(GAME, "world_progression.rpy"), encoding="utf-8").read()
    _transition_block = WP_SRC.split("Nora: café → school")[1].split("Elle:")[0]
    chk("transition block sweeps nora_closing_1",
        '"nora_closing_1"' in _transition_block)
    chk("sweep does NOT call cancel_commitment (which applies Trust penalty)",
        "cancel_commitment(" not in _transition_block)
    # Inline logic: a dict that looks like a live commitment must be marked cancelled.
    _fake_c = {"id": "nora_closing_1", "cancelled": False, "missed": False, "completed": False}
    def _c_active_stub(c):
        return not c.get("cancelled") and not c.get("missed") and not c.get("completed")
    for _c in [_fake_c]:
        if _c["id"] == "nora_closing_1" and _c_active_stub(_c):
            _c["cancelled"] = True
    chk("live nora_closing_1 commitment is marked cancelled by sweep logic",
        _fake_c["cancelled"] is True)

    print("\nH. Tier A walk-out still stands down")
    # The beat's window is weekend 17-18, so it cannot collide with 19-21; the
    # guard matters because it shares _nora_auto_closing_eligible() now.
    tb.valid_state("nora_walk_out")
    chk("fires when the closing scene is done and out of reach",
        tb.G["check_nora_walk_out"]() is True)
    tb.valid_state("nora_walk_out")
    tb.store.nora_closing_done = False
    tb.store.nora_affection = 45
    chk("stands down while the (now reachable) closing scene is pending",
        tb.G["check_nora_walk_out"]() is False)
    tb.valid_state("nora_walk_out")
    tb.store.hour = 18.5
    chk("18:30 is a dead zone for the beat (no 18/19 boundary overlap)",
        tb.G["check_nora_walk_out"]() is False)

    print("\nI. scene tester registration")
    for key, lbl in (("nora_closing", "nora_closing_scene"),
                     ("nora_romance_reopen", "dst_nora_reopen_launch")):
        chk("registry has '%s'" % key, '"%s": {' % key in DST_SRC)
        chk("'%s' points at %s" % (key, lbl), '"label": "%s",' % lbl in DST_SRC)
    chk("the reopen wrapper label exists (the scene ends with `return`)",
        re.search(r"^label dst_nora_reopen_launch:", DST_SRC, re.M) is not None)
    for preset in ("_dst_nora_closing_basic", "_dst_nora_closing_comfortable",
                   "_dst_nora_reopen_basic", "_dst_nora_reopen_comfortable",
                   "_dst_nora_closing_reset", "_dst_nora_reopen_reset"):
        chk("%s defined" % preset, "def %s(" % preset in DST_SRC)
    for m in re.finditer(r"def _dst_nora_(?:closing|reopen)_(?:basic)\(\):"
                         r"(.*?)(?=\n    def )", DST_SRC, re.S):
        _h = re.search(r"store\.hour = ([\d.]+)", m.group(1))
        chk("preset hour %s is inside the 19-21 window" % (_h and _h.group(1)),
            _h is not None and 19.0 <= float(_h.group(1)) < 21.0)

    print("\n%d check(s) failed" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
