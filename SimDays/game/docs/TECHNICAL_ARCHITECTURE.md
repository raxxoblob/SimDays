# Technical Architecture

File map and helper reference for LivingTheDream.

**Game root:** `SimDays/SimDays/game/`

All paths below are relative to that root.

---

## Core Files

| System | File | Main Helpers / Notes |
|---|---|---|
| Player stats, needs, time | `data.rpy` | `default stat_str = 10`; `spend_time(hours)` (line ~730) |
| Romance state, first kiss, NPC affection | `interact.rpy` | `get_romance_state(npc_id)`, `set_romance_state(npc_id, state, source=...)`, `_commit_first_kiss(npc_id)` (line ~1580), `npc_aff(npc_id)`, `npc_trust(npc_id)`, `relationship_memory_exists(npc, key)` (line ~316) |
| Relationship axes, mutation | `npc_relationships.rpy` | `npc_rel(npc_id, axis)` (line ~96), `apply_relationship_change(npc_id, event_key, source, **axes)` (line ~395) |
| Relationship memories | `npc_schedules.rpy` | `add_relationship_memory(npc, key, text)` (line ~368) |
| Commitments, phone messages | `phone_messages.rpy` | `add_commitment(cid, npc_id, title, day, hour, location, label, grace=2.0)` (line ~99), `queue_phone_message(npc_id, text, send_on_day, tag, responses=None, attachment=None)` (line ~29) |
| Initiative / phone actionable | `phone_actionable.rpy` | `_INITIATIVE_VARIANTS`, `_DATE_VARIANTS`, `_VARIANT_WEIGHTS`, `_VARIANT_MIN_TIER`, `_VARIANT_CONDITIONS`, `_clear_initiative_pending(npc_id)` (line ~601) |
| Photo messages (generic engine) | `photo_message_engine.rpy` | `register_npc_photo_message(...)` at `init 1 python:` |
| NPC schedules, locations | `npc_schedules.rpy` | NPC location availability, schedule overrides |
| All location entry labels | `locations.rpy` | `label location_gym` (~466), `label gym_floor` (~515), `label location_sandbeach`, `label location_terrace`, etc. |
| Zoe romance content | `zoe_romance_milestones.rpy` | Milestones M2–M7, `_zoe_m2_beach_eligible()`, `can_trigger_zoe_beach_after_dark()` (~144), `zoe_beach_dating_scene` (~921) |
| Expansion scenes (M1, ambient) | `gameplay_expansion_scenes.rpy` | Zoe M1 nightclub moment; various ambient events |
| NPC interaction / talk | `interact.rpy` | `npc_interact` label, talk path, jealousy wiring |
| NPC sprites | `images.rpy` | Sprite declarations; `npc_sprite()`, `show_npc_expr()` |
| Scene Tester | `debug_scene_tester.rpy` | `SCENE_TEST_REGISTRY`, preset eligibility functions |
| WED (living world events) | `locations.rpy` + WED registry | `WED_REGISTRY`; `wed_personal_fired_day`, `wed_ambient_fired` |
| Gains / XP | `gains.rpy` | `gain_stat("str", ...)` maps to `stat_str` |
| Skills | Various | Inline per career/activity label |
| Save migration | `zoe_romance_milestones.rpy` (and others) | `config.after_load_callbacks`; `_zoe_romance_milestone_backfill()` |

---

## Key Helper Contracts

### FIRST KISS
`_commit_first_kiss(npc_id)` in `interact.rpy`
→ Records `first_kiss_{npc_id}` relationship memory, grants `attraction=6` via `apply_relationship_change`.
→ **Always use this. Do not recreate first-kiss state changes independently.**

### ROMANCE STATE
`get_romance_state(npc_id)` / `set_romance_state(npc_id, state, source=...)`
States: `unopened / friends / interested / dating / committed / paused / closed`

### RELATIONSHIP MUTATION
`apply_relationship_change(npc_id, event_key, source, **axes)`
→ Canonical. Source categories: `"authored"`, `"ambient"`, `"player"`.
→ Do not set relationship axis variables directly.

### RELATIONSHIP MEMORY
`add_relationship_memory(npc, key, text)` — `npc_schedules.rpy`
`relationship_memory_exists(npc, key)` — `interact.rpy`
→ Key must be globally unique per NPC. Use descriptive snake_case strings.

### COMMITMENT PIPELINE
```
add_commitment(cid, npc_id, title, day, hour, location, label, grace)
    ↓ (at location entry)
commitment_available(cid) → jump scene_label
    ↓
complete_commitment(cid) or cancel_commitment(cid)
```

### SPEND TIME
`spend_time(hours)` in `data.rpy`
→ Advances clock, decays needs. Called by ALL activity types. Do not implement a parallel cost system.

---

## Call Flows

### Location Entry

```
label location_X:
    $ current_loc = "location_X"
    → process WED / commitment checks
    → authored scene triggers (commitment_available / can_trigger_X)
    → regular activity menu
```

### Invitation → Scene

```
eligibility helper (_zoe_m2_beach_eligible)
    → initiative message wired in _INITIATIVE_VARIANTS
    → player response label (npc_ini_zoe_bdating_ok/nine/cant)
    → add_commitment(...)
    ↓
location entry → commitment_available(cid) → jump scene_label
    ↓
parent scene:
    setup → dialogue → buildup
    → director handoff (if renpy.has_label("director_label"))
    → call director_label
    ← return
    → aftermath → complete_commitment / cancel_commitment → jump location
```

### Relationship Progression

```
authored scene
    → apply_relationship_change(...)     ← stat mutation
    → add_relationship_memory(...)       ← memory write
    → set_romance_state(...) if milestone ← state change
    → complete_commitment(...)           ← pipeline close
```

---

## Director Handoff Convention

**AI/Qwen owns:** parent scene setup, backgrounds/sprites, dialogue, buildup, eligibility, scheduling, call, aftermath.

**Director/user owns:** final CG-driven subscene, CG presentation, choices inside visual payoff, physical/romantic climax, `_commit_first_kiss()` placement, romance state transitions where specified.

**Guard pattern:**
```renpy
if renpy.has_label("director_label_name"):
    call director_label_name
else:
    # developer-facing notify; set retry cooldown; cancel commitment; jump back to location
```

**Never invent CG filenames. Never create content inside director-owned files unless explicitly instructed.**

### Planned Director Files

Directory `game/director_romance/` — DOES NOT YET EXIST.

| File | Label | Entry State | Purpose |
|---|---|---|---|
| `romantic_subscene_zoe_beach_dating.rpy` | `romantic_subscene_zoe_beach_dating` | interested, no first kiss | Beach breakpoint M2 payoff |
| `romantic_subscene_zoe_gym_training.rpy` | `romantic_subscene_zoe_gym_training` | dating/committed, gym, str≥3 | Workout CG sequence |
| `zoe_beach_after_dark_romance.rpy` | `zoe_beach_after_dark_payoff` | dating, post-first-kiss | M3 beach night payoff |
| `zoe_commitment_romance.rpy` | `zoe_commitment_payoff` | dating | M6 terrace commitment |
| `zoe_love_spoken_romance.rpy` | `zoe_love_spoken_payoff` | committed | M7 love spoken |
| `summer_festival_romance.rpy` | `summer_festival_zoe_romance` | any romance state | Festival branch |

---

## Save Compatibility

Old saves auto-initialise new `default` flags to False. Use `config.after_load_callbacks` for backfills where a flag needs to be set based on existing state (e.g. advancing a spine without replaying scenes old saves already passed).

Pattern: `_zoe_romance_milestone_backfill()` in `zoe_romance_milestones.rpy` is the reference implementation.

---

## Ren'Py Specifics

- `init python:` — runs at startup; define helpers here
- `init 5 python:` — runs after init; wire initiative dicts here (after NPC data is ready)
- `config.after_load_callbacks` — save migration; runs after a save is loaded
- `renpy.has_label(name)` — guard before `call`; safe if director file absent
- `call` targets labels; `jump` does not return
- Screen language `for` is valid. Raw script Python `for` is different.

---

## Sprite Conventions

Five standard expression keys: `normal`, `talk`, `happy`, `angry`, `sad`.
Pattern: `<character>_<outfit>_<expression>` or `<character>_<expression>`.
Fallback: same-outfit `_normal`. Never fall back across outfit sets.

Stable sprite tags: use `as npcsprite` / `at sprite_r` / `at sprite_l` from the established tag set.
