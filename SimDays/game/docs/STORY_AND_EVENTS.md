# Story and Events

Narrative map for LivingTheDream. What exists, what connects, what's next.

**IMPLEMENTED** = authored scenes exist in current `.rpy` source.
**PLANNED** = design exists; scene not yet in source.
**HOLE** = flag set in source but scene not written (runtime bug risk).

---

## Opening

MC moves to a new city. First days establish home, neighbour (Marcus), and the neighbourhood. The player has arrived; the rest is built through play.

---

## Zoe Arc

### Contact and Early Moments

| Scene | Status | Key Flag |
|---|---|---|
| First meeting at park / busking | IMPLEMENTED | `zoe_met` |
| WED ambient park events (sketching, pencil, wrong colour) | IMPLEMENTED | `zoe_met` |
| Rain shelter scene — first major personal moment | IMPLEMENTED | `zoe_rain_done` |
| Sam × Zoe park crossover | IMPLEMENTED | `crossover_sam_zoe_park` |

### Romance Spine

| Milestone | Status | Key Flag / Label |
|---|---|---|
| M1 — Nightclub spontaneous moment | IMPLEMENTED | `zoe_moment_deflected_done` |
| M2 — Beach Dating Breakpoint (interested → dating) | ENGINE IMPLEMENTED; director CG pending | `zoe_beach_dating_done` |
| M3 — Beach After Dark (post-first-kiss) | IMPLEMENTED | `zoe_beach_night_done` |
| M4 — Home Evening (no reason) | IMPLEMENTED | `zoe_home_no_reason_done` |
| M5 — Group Public Recognition | IMPLEMENTED | (requires M3 + M4) |
| M6 — Commitment (terrace) | IMPLEMENTED | `zoe_commitment_done` |
| M7 — Love Spoken | IMPLEMENTED | `zoe_love_spoken_done` |
| Romance reopen | IMPLEMENTED | `zoe_reopen_done` |

### Current Next Work: Beach Dating Breakpoint

Full parent scene implemented in `zoe_romance_milestones.rpy` (label `zoe_beach_dating_scene`, line 921).

Director takes over after: `z "But apparently that's not stopping me."`

**DIRECTOR/USER OWNS:**

```
game/director_romance/romantic_subscene_zoe_beach_dating.rpy
label: romantic_subscene_zoe_beach_dating
```

Entry state: `get_romance_state("zoe") == "interested"`, no `first_kiss_zoe` memory.
Intended outcome: possible canonical first kiss → `interested → dating`.
Return: plain `return`.

Directory `game/director_romance/` does not yet exist — PLANNED.

### Other Zoe Threads

| Thread | Status | Notes |
|---|---|---|
| Gallery/Exhibition opening | HOLE | `zoe_exhibition_invited` set in source; opening scene NOT implemented |
| Grant / funding application | PARTIAL | Event mentioned; result not yet authored |
| Bass guitar history | BACKGROUND CANON | Established; no dedicated scene |
| Client vs personal work tension | BACKGROUND CANON | Woven into conversation |
| Jealousy conversations beyond first notice | PLANNED | First-notice implemented; follow-ups not designed |

### Planned: Zoe Gym Training

After `dating`/`committed`. Repeatable shared activity.

Parent scene: AI implemented (in `zoe_romance_milestones.rpy`).
CG workout sequence: DIRECTOR/USER OWNED.

```
game/director_romance/romantic_subscene_zoe_gym_training.rpy
label: romantic_subscene_zoe_gym_training
```

Entry state: `dating` or `committed`, inside gym, `stat_str >= 3`.
Design: Strength 5 unlocks extra coaching variant. No permanent Zoe gym schedule. Replayable with cooldown. Later Zoe may initiate.

---

## Marcus Arc

### Contact and Friendship

| Scene | Status | Key Flag |
|---|---|---|
| Move-in and first corridor meeting | IMPLEMENTED | `move_in_complete` |
| First shift check-in + follow-up talk | IMPLEMENTED | `marcus_first_shift_checkin` |
| New car comment | IMPLEMENTED | `marcus_new_car_comment` |
| Marcus × Nora Grounds crossover | IMPLEMENTED | `crossover_marcus_nora_coffee` |
| Home state progression (locked → invited → welcome) | IMPLEMENTED | `marcus_home_state` |

### Pending Marcus Threads

| Thread | Status | Notes |
|---|---|---|
| Basketball authored scene | HOLE | Invite mechanics work; authored scene missing |
| Loan event (Static/park) | IMPLEMENTED | `wed_marcus_loan_state` state machine; callbacks at bar and park |
| Marcus deeper friendship content | PLANNED | Not yet designed |
| Romance unlock | PLANNED | Not designed; no current threshold |

---

## Eli Arc

| Scene | Status |
|---|---|
| IT shift ambient events (bug report, code comment, deploy window) | IMPLEMENTED |
| Deploy hug scene | IMPLEMENTED (`eli_deploy_hug_done`) |
| Jealousy first notice | IMPLEMENTED |
| Home dinner | IMPLEMENTED (`cg_eli_home_dinner` asset needed — Tier 1) |
| Romance | DISABLED |

---

## Nora Arc

| Scene | Status | Notes |
|---|---|---|
| Café interactions | IMPLEMENTED | |
| Bad day scene | IMPLEMENTED (`nora_bad_day_done`) | Jealousy unlock |
| Jealousy first notice | IMPLEMENTED | |
| Romance arc | PLANNED | Events not yet designed |
| Arc ending | HOLE | Nora has no closing story beat |

---

## Other NPC Threads

**Martha:** Corporate arc implemented. Corridor scene (`martha_corridor_done`), talk chain, rooftop scene. Caroline × Martha Static crossover.

**Rena:** Culinary arc mostly implemented (`cul_npc1_rena`, `cul_npc2_rena`, `scene_cul_service_crisis`, `cul_review_commis`). `scene_rena_bar` NOT YET IMPLEMENTED.

**Elle:** Portugal decision made in-game. Consequence scene NOT YET IMPLEMENTED (structural hole).

**Lena:** Rooftop scene implemented (`lena_rooftop`). Hospital hard case scene: 25% RNG roll with no pity trigger — flagged as a structural problem.

**Sam:** Gym events implemented. Sam × Zoe park crossover implemented. Basketball authored scene with Marcus: PENDING.

**Caroline:** Off-the-clock bar scene implemented (`caroline_bar_done`).

**Natalie:** Humanisation scene implemented.

---

## Major Events

### Summer Festival

IMPLEMENTED. Multi-scene shared sequence. Zoe romance branch exists.

Structure: shared sequence → optional short character/romance branch → reconvergence → shared event continues.

Director CG needed: `game/director_romance/summer_festival_romance.rpy`, label `summer_festival_zoe_romance`.

### Art and Culture Night

Status: verify in source. Not confirmed implemented.

---

## Narrative Architecture Rules

- Major events: mostly shared sequence → optional character branch → reconvergence. Most CGs exposed in one run.
- Do not turn the game into quest chains.
- Large event branches should reconverge to the shared event.
- Relationship progression should be behavioral and authored, not "level up" notification.
- Quiet days are valid. Not every day has a story beat.

### CG Scene Structure

```
A — Setup/approach
B — Obstacle/tension
C — Breakthrough/turning point (CG here if scene earns one)
D — Consequence
E — Exit / scene memory written
```

One CG per breakthrough is the default. Two to three CGs for milestone scenes.

### Scene Trigger Architecture

Split triggers into:
- **Narrative triggers** — story condition, authored moment
- **Availability triggers** — schedule, time-of-day, prior flags

`can_trigger_X()` helpers own the availability check. The scene label owns the narrative.
