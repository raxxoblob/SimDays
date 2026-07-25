# World Event Pilot — State Reference
## LivingTheDream — Pilot Implementation Documentation

---

## Marcus Loan Event

**Event ID:** `marcus_loan`  
**Event label:** `wevent_marcus_loan`  
**Type:** Personal  
**Locations:** `location_bar`, `location_park`  
**Min day:** 10  
**Gate (structural):** `marcus_trust >= 20`, `marcus_met`, no active Marcus commitment today, no major scene today  
**Gate (narrative):** `wed_marcus_loan_state == "none"` (checked inside label)  
**Once:** Yes — fires once per save

### State Machine

```
none
 ├─ [player sees event] → offered (wed_fire sets resolved)
 │    ├─ Full loan ($120) → pending_repay
 │    │    └─ [day passes] → callback_ready
 │    │         └─ [fires at marcus_home or any location] → resolved_repaid
 │    ├─ Partial ($40) → pending_practical
 │    │    └─ [day passes] → callback_ready
 │    │         └─ [fires at marcus_home or any location] → resolved_repaid
 │    ├─ Low-money mutual recognition → resolved_low_money (terminal)
 │    ├─ Respectful refusal → resolved_refused
 │    │    └─ [day passes] → pending_solved
 │    │         └─ [fires at any location] → resolved_solved (terminal)
 │    └─ Dismissive refusal → resolved_dismissed (terminal; npc_anger +2)
```

### Store Variables

| Variable | Default | Purpose |
|---|---|---|
| `wed_marcus_loan_state` | `"none"` | Current state of the loan lifecycle |
| `wed_marcus_loan_callback_day` | `-1` | Day when callback should be promoted to ready |
| `wed_marcus_loan_callback_ready` | `False` | True when callback is ready to fire |

### Callback Labels

| Label | Fires when | Outcome |
|---|---|---|
| `wevcb_marcus_loan_repay` | `pending_repay` + day >= callback_day | Marcus returns $120, +2 trust |
| `wevcb_marcus_loan_partial` | `pending_practical` + day >= callback_day | Marcus offers practical help (Saturday court), +2 trust/aff |
| `wevcb_marcus_loan_solved` | `resolved_refused` → `pending_solved` + day | Marcus mentions he sorted it, +1 trust |

### Trust/Affection Impact

| Choice | Trust | Affection | Anger | Memory |
|---|---|---|---|---|
| Full loan | +3 | +2 | — | `marcus_loan_given` |
| Partial help | +2 | +1 | — | `marcus_loan_partial` |
| Low-money response | +2 | — | — | `marcus_loan_broke` |
| Respectful refusal | 0 | 0 | — | `marcus_loan_refused` |
| Dismissive refusal | — | — | +2 | `marcus_loan_dismissed` |

### Priority-order callback firing location

Marcus loan callbacks fire in `location_marcus_home` when `wed_marcus_loan_callback_ready == True`. They will also fire at the bar or park via `wed_pop_callback()` if added to those hooks — currently the home location is the primary callback point.

---

## Sam Off-Routine Event

**Event ID:** `sam_off_routine`  
**Event label:** `wevent_sam_off_routine`  
**Type:** Personal  
**Locations:** `location_cafe`, `location_gym`  
**Min day:** 7  
**Gate (structural):** `sam_trust >= 15`, `sam_met`, no major scene today  
**Gate (narrative):** `sam_off_routine_done == False` (checked inside label)  
**Once:** Yes — fires once per save

**Additional eligibility:** At `location_gym`, blocked during Sam's normal schedule hours (Mon-Fri 10am-2pm) since encountering her then is routine, not "off-routine."

### State Variables

| Variable | Default | Purpose |
|---|---|---|
| `sam_off_routine_done` | `False` | True after scene fires |
| `sam_off_routine_greet_done` | `False` | True after park greet callback fires |

### Callback

No scheduled callback. The greet callback fires in `location_park` via a simple conditional check:
```renpy
if sam_off_routine_done and not sam_off_routine_greet_done and npc_talkable("sam"):
    # One greet line variant acknowledging the off-routine encounter
```
This check should be added to the `location_park` Talk to Sam option or as a greet variant in `npc_interact("sam")`.

### Relationship Impact

| Choice | Trust | Affection | Memory |
|---|---|---|---|
| "Thought you were a park person" | +2 | — | `sam_off_routine` |
| "You alright?" | +3 | +1 | `sam_off_routine` |
| "Coffee's decent here" | — | +1 | `sam_off_routine` |

**Romance:** This event does not open Sam's romance route. The romance flag check is not touched.

---

## Ambient Events

### Metro Delay

**Event ID:** `metro_delay`  
**Locations:** `location_hub`, `location_hospital`  
**Cooldown:** 5 days  
**Weight:** 0.30 (fires ~30% of eligible days)

**Choices:**
1. Wait it out — costs 0.5–1.0h (random)
2. Find another way ($6) — if can't afford: wait anyway

**No NPC interaction required.** Safe to fire whether or not any NPC is present.

---

### Rain in Park

**Event ID:** `rain_in_park`  
**Locations:** `location_park`  
**Cooldown:** 4 days  
**Weight:** 0.28 (fires ~28% of eligible park visits)

**Choices:**
1. Find cover (stay) — costs 0.5h, BG unchanged
2. Head out — jumps to `take_metro`

If NPCs are present: choice set acknowledges the social context.  
If no NPCs: solo choices.

**NPC presence:** Uses `location_sprites()` result, already available in park context.

---

### Bar Quiz Night

**Event ID:** `bar_quiz_night`  
**Locations:** `location_bar`  
**Cooldown:** 6 days  
**Weight:** 0.35 (fires ~35% of eligible bar visits)

**Choices:**
1. Join a team ($5, 2h) — reward varies by `stat_int >= 30` or `stat_chr >= 30`
2. Skip it — no cost or gain

**Skill interaction:**
- `stat_int >= 30`: +8 CHR (you're useful)
- `stat_chr >= 30` (and not int): +10 CHR (confident even without answers)
- Neither: +4 INT (you listen, things stick)

---

## Marcus Home Access

**State variable:** `marcus_home_state`  
**Default:** `"locked"`  
**States:** `locked` → `invited_once` → `welcome`

### State transitions

| From | To | Trigger |
|---|---|---|
| `locked` | `invited_once` | `marcus_trust >= 35`, `marcus_affection >= 30`, `day >= 15`, phone message queued |
| `invited_once` | `welcome` | Player visits home and leaves (via "Head out" or any activity completion) |

### Access conditions (at `marcus_talk` / `location_marcus_home`)

- `marcus_home_state != "locked"` — must have been invited
- `marcus_is_home()` — Marcus is in his afternoon window (10am-5pm), not an errand day (`day % 3 != 0`)

### Available activities

| Activity | Gate | Effect |
|---|---|---|
| Talk | Always | `npc_interact("marcus")` |
| Eat chili | `marcus_chili_last_day != day` (once daily) | +45 hunger, +1 aff, `marcus_chili_last_day = day` |
| Watch the game | `hour >= 17` (evening) | 1.5h, +8 energy, +1 aff on ask |
| Loan callback | `wed_marcus_loan_callback_ready` | Fires `wevcb_marcus_loan_repay` or `wevcb_marcus_loan_partial` |

### Schedule

Marcus is home 10am-5pm, ~67% of days (not home on days where `day % 3 == 0`). He is always at the park 6am-10am and the bar 5pm-midnight. The hallway Door 14 (`marcus_talk`) routes to `location_marcus_home` when state is not locked and he is home.

---

## Extension Instructions

### Adding a new NPC home location

1. Create `location_<npc>_home` label in `world_events.rpy` or a new file
2. Add a `<npc>_home_state` default variable in `data.rpy`
3. Add an invite trigger in `new_day()` (same pattern as Marcus home invite)
4. Update the hallway or map to include the new location entry
5. Add a `<npc>_is_home()` function based on the NPC's schedule from `NPC_DATA`

### Adding a new loan/financial event for another NPC

1. Add a new state variable: `wed_<npc>_loan_state`
2. Register the event in `WED_REGISTRY`
3. Write `wevent_<npc>_loan` following the marcus_loan pattern
4. Add `conflict_npc` to block it when a commitment with that NPC exists
5. Write callback labels for each outcome (repay, partial, solved)
6. Add callback day promotion in `new_day()`
