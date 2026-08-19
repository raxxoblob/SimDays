# QWEN WORKMAP — Zoe Romance & Gym Implementation

**This file covers current implementation work only.**
For general canon and architecture, use:
- `game/PROJECT_INDEX.md` — entry point
- `game/docs/CHARACTERS.md` — NPC voice/personality/canon
- `game/docs/GAMEPLAY_SYSTEMS.md` — mechanics design
- `game/docs/STORY_AND_EVENTS.md` — narrative map
- `game/docs/TECHNICAL_ARCHITECTURE.md` — file map, helpers, call flows
- `game/docs/DEVELOPMENT_RULES.md` — coding/directing constraints

All game files are under: `SimDays/SimDays/game/`

---

## Section 1 — Current File Map

### Files to EDIT

`game/zoe_romance_milestones.rpy`
→ Zoe romance spine (M2–M7): eligibility helpers, initiative wiring, phone reply labels, scene labels
→ **EDIT** — primary Zoe content file

`game/locations.rpy`
→ All location entry labels including `location_sandbeach` (line ~466), `location_gym` (line 466), `gym_floor` (line 515)
→ **EDIT** — add commitment triggers, gym shared activity logic

`game/debug_scene_tester.rpy`
→ Scene Tester: preset eligibility functions + SCENE_TEST_REGISTRY
→ **EDIT** — add new scene test entries for each new scene

### Files to INSPECT ONLY

`game/interact.rpy`
→ Romance state machine (`get_romance_state`, `set_romance_state`), `_commit_first_kiss`, `npc_aff`, `npc_trust`, `relationship_memory_exists`
→ **INSPECT ONLY** — do not edit; reuse exported helpers

`game/npc_relationships.rpy`
→ Relationship axes: `npc_rel(npc_id, axis)`, `apply_relationship_change(npc_id, event_key, source, **axes)`
→ **INSPECT ONLY**

`game/phone_messages.rpy`
→ `add_commitment(cid, npc_id, title, day, hour, location, label, grace=2.0)`, `queue_phone_message()`
→ **INSPECT ONLY** — call these, do not rewrite

`game/phone_actionable.rpy`
→ Initiative system: `_INITIATIVE_VARIANTS`, `_DATE_VARIANTS`, `_VARIANT_WEIGHTS`, `_VARIANT_MIN_TIER`, `_VARIANT_CONDITIONS`, `_clear_initiative_pending()`
→ **INSPECT ONLY** — wire new messages by adding entries to these dicts

`game/data.rpy`
→ Player stat defaults (`default stat_str = 10`), `spend_time(hours)` (line 730)
→ **INSPECT ONLY**

`game/npc_schedules.rpy`
→ `add_relationship_memory(npc, key, text)`
→ **INSPECT ONLY**

`game/gameplay_expansion_scenes.rpy`
→ Zoe M1 spontaneous nightclub moment
→ **INSPECT ONLY** — reference only

### Director-Owned (do not create or edit)

`game/director_romance/romantic_subscene_zoe_beach_dating.rpy` — PLANNED, does not exist yet
`game/director_romance/romantic_subscene_zoe_gym_training.rpy` — PLANNED, does not exist yet

---

## Section 2 — Scenes to Implement

### A. Zoe Beach Dating Breakpoint

**PURPOSE:** Canonical `interested → dating` milestone. Beach night buildup leads to director CG subscene for the romantic payoff and possible first kiss.

**QWEN IMPLEMENTS:** eligibility helper, phone invitation + scheduling, beach arrival, full dialogue buildup, safe call into director subscene, post-return handling, old-save migration, Scene Tester entry.

**DIRECTOR/USER IMPLEMENTS:** final CG-driven romantic payoff inside the subscene.

**PLANNED DIRECTOR FILE:** `game/director_romance/romantic_subscene_zoe_beach_dating.rpy`
**PLANNED LABEL:** `romantic_subscene_zoe_beach_dating`

**HANDOFF POSITION:** immediately after
```
z "But apparently that's not stopping me."
```
Guard with `renpy.has_label("romantic_subscene_zoe_beach_dating")` before calling.

---

**FILES QWEN SHOULD EDIT:**
- `game/zoe_romance_milestones.rpy` — eligibility, phone invite, reply labels, scene label
- `game/locations.rpy` — add `commitment_available("zoe_beach_dating_1")` check at `location_sandbeach`
- `game/debug_scene_tester.rpy` — add `zoe_m2_beach_dating` test entry

**FILES QWEN SHOULD INSPECT:**
- `game/interact.rpy` — `get_romance_state`, `set_romance_state`, `_commit_first_kiss`, `relationship_memory_exists`
- `game/phone_messages.rpy` — `add_commitment`, `queue_phone_message`
- `game/phone_actionable.rpy` — initiative dicts for wiring the invite message
- `game/npc_schedules.rpy` — `add_relationship_memory`

**CANONICAL HELPERS TO REUSE:**
- `_commit_first_kiss("zoe")` — grants attraction=6, records `first_kiss_zoe` memory
- `get_romance_state("zoe")` / `set_romance_state("zoe", "dating", source=...)`
- `relationship_memory_exists("zoe", "first_kiss_zoe")` — check before allowing scene
- `apply_relationship_change("zoe", event_key, "authored", affection=N, trust=N, ...)`
- `add_commitment(cid, "zoe", title, day, hour, location, label, grace=N)`
- `add_relationship_memory("zoe", key, text)`
- `_clear_initiative_pending("zoe")`
- `npc_aff("zoe")`, `npc_trust("zoe")`, `npc_rel("zoe", "familiarity")`

**MAIN CONFLICT TO AVOID:** The existing spontaneous nightclub moment (M1, in `gameplay_expansion_scenes.rpy`) and the Summer Festival can both produce a first kiss. If `first_kiss_zoe` memory already exists when the beach scene is reached, `_zoe_m2_beach_eligible()` must return False — the beach breakpoint must not replay the first kiss.

---

### B. Zoe Replayable Gym Training

**PURPOSE:** Shared gym activity unlocked after Zoe is `dating` or `committed`. Requires `stat_str >= 3` (Strength). Repeatable relationship activity — not a new romance-state milestone. Zoe does NOT gain a permanent gym schedule.

**QWEN IMPLEMENTS:** first invitation, scheduling, gym arrival gate, pre-workout dialogue, reuse of `gym_floor` workout mechanics and `spend_time()`, cooldown, Zoe initiative integration, safe call into director workout subscene, post-workout closure dialogue, Scene Tester entry.

**DIRECTOR/USER IMPLEMENTS:** workout CG sequence, CG dialogue, flirt during exercises, exercise choices inside the visual sequence.

**PLANNED DIRECTOR FILE:** `game/director_romance/romantic_subscene_zoe_gym_training.rpy`
**PLANNED LABEL:** `romantic_subscene_zoe_gym_training`

---

**FILES QWEN SHOULD EDIT:**
- `game/zoe_romance_milestones.rpy` — eligibility helper, phone invite, reply labels, scene label, cooldown flag
- `game/locations.rpy` — add commitment trigger inside `location_gym` or `gym_floor`
- `game/debug_scene_tester.rpy` — add `zoe_gym_training` test entry

**FILES QWEN SHOULD INSPECT:**
- `game/locations.rpy` — `gym_floor` label (line 515): understand existing workout flow and `spend_time` calls before inserting
- `game/data.rpy` — `default stat_str = 10`; `spend_time(hours)` (line 730)
- `game/phone_messages.rpy` — `add_commitment`, `queue_phone_message`
- `game/phone_actionable.rpy` — initiative dicts

**CANONICAL HELPERS TO REUSE:**
- `spend_time(hours)` — advance clock and decay needs, same as normal workout
- `stat_str` — check `store.stat_str >= 3` for eligibility; `>= 5` for coaching variant
- `apply_relationship_change("zoe", event_key, "authored", affection=N, familiarity=N)`
- `add_commitment(cid, "zoe", ...)`, `commitment_available(cid)`
- `add_relationship_memory("zoe", key, text)`
- `_clear_initiative_pending("zoe")`
- Initiative dicts in `phone_actionable.rpy` for eventual Zoe-initiated invite

Do NOT copy gym workout logic — call `spend_time()` for cost and let Strength gain happen via the same flow. Do not invent a separate energy system.

---

## Section 3 — Director Handoff Rule

```
QWEN/AI PARENT SCENE
    backgrounds, sprites, arrival
    normal buildup dialogue
    player choices pre-climax
        |
        v
DIRECTOR HANDOFF
    if renpy.has_label("director_label"):
        call director_label
    else:
        [developer warning, cooldown, jump back to location]
        |
        v
DIRECTOR/USER SUBSCENE
    CG sequence
    romantic or physical payoff
    internal CG choices
    state transitions (if applicable)
    return
        |
        v
QWEN/AI PARENT SCENE
    short aftermath
    memory write
    complete_commitment / cancel_commitment
    jump back to location
```

**Qwen may edit everything BEFORE the handoff and AFTER the return.**
**Qwen must NOT create or rewrite director-owned subscene files unless explicitly asked.**
**Qwen must NOT invent CG image filenames.**

---

## Section 4 — Director-Owned Files

`game/director_romance/` — **directory does not yet exist, PLANNED**

### `romantic_subscene_zoe_beach_dating`
ENTRY: `get_romance_state("zoe") == "interested"`, no `first_kiss_zoe` memory
PURPOSE: romantic beach payoff, possible first kiss, `interested → dating` transition
RETURN: plain `return`

### `romantic_subscene_zoe_gym_training`
ENTRY: `get_romance_state("zoe")` is `dating` or `committed`, inside gym, `stat_str >= 3`
PURPOSE: workout CG sequence, light flirt, exercise choices
RETURN: plain `return`

---

## Section 5 — Canon / Do Not Break

- Romance states use `get_romance_state` / `set_romance_state` in `interact.rpy`. Do not add another state machine.
- First-kiss is `_commit_first_kiss("zoe")` in `interact.rpy`. Always use this — do not write affection/memory manually for the kiss.
- Relationship axes mutate via `apply_relationship_change()`. Do not set relationship vars directly.
- Commitment pipeline: `add_commitment` → `commitment_available(cid)` check at location → scene label → `complete_commitment(cid)` or `cancel_commitment(cid)`.
- `add_relationship_memory` is in `npc_schedules.rpy`. Second-arg key must be unique per event.
- Strength stat is `store.stat_str`. Do not rename or alias it.
- Gym activity time/energy costs call `spend_time(hours)` — do not invent a parallel system.
- Zoe must NOT get a permanent gym NPC schedule entry just for the shared training activity.
- Old saves: every new `default` flag auto-initialises to False on old saves; migrations via `config.after_load_callbacks` only when a flag needs to be backfilled from existing state.
- Director CG files remain user-owned. No invented image filenames anywhere.
- Keep file count minimal — add to existing files before creating new ones.

---

## Section 6 — Quick Start for Qwen

### When implementing Zoe Beach Dating Breakpoint

Open first:
1. `game/zoe_romance_milestones.rpy` — existing spine, add eligibility + scene here
2. `game/locations.rpy` — add commitment trigger at `location_sandbeach`
3. `game/phone_actionable.rpy` — wire initiative message
4. `game/debug_scene_tester.rpy` — add test preset

Search for:
- `_zoe_m2_beach_eligible` — existing eligibility helper to extend or replace
- `zoe_beach_dating_scene` — existing scene label (line 921)
- `_commit_first_kiss` — canonical first-kiss mutator
- `first_kiss_zoe` — relationship memory key for first kiss
- `commitment_available` — how location trigger checks scheduling
- `_INITIATIVE_VARIANTS` — where to wire the phone invite

Do NOT initially load: `gameplay_expansion_scenes.rpy`, `cooking.rpy`, `npc_schedules.rpy` (unless you need `add_relationship_memory` signature).

### When implementing Zoe Gym Training

Open first:
1. `game/locations.rpy` — read `gym_floor` label (line 515) to understand existing workout flow before writing anything
2. `game/zoe_romance_milestones.rpy` — add eligibility, invite, scene label here
3. `game/data.rpy` — confirm `stat_str` default and `spend_time` signature
4. `game/debug_scene_tester.rpy` — add test preset

Search for:
- `stat_str` — Strength variable
- `spend_time` — activity cost function
- `gym_floor` — existing workout label to reuse structure from
- `add_commitment` — scheduling helper
- `_INITIATIVE_VARIANTS` — Zoe initiative wiring
- `apply_relationship_change` — canonical relationship mutation

Do NOT initially load: `cooking.rpy`, `freelance.rpy`, `photo_message_engine.rpy`, unrelated NPC files.
