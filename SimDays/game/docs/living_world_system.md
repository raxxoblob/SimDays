# Living World System
## LivingTheDream — World Event Director Reference

---

## Overview

The World Event Director (WED) is a central data-driven system that fires ambient and personal events at location labels. It replaces scattered, location-specific random checks with one registry, one poll function per event type, and a callback queue.

**Design principles:**
- Maximum one personal/major event per day across all locations
- Maximum one ambient event per location per visit
- No event fires during or after a major scene (same day as `major_scene_last_day`)
- No personal event fires if a conflicting NPC commitment exists today
- Random rolls happen in `new_day()` (ambient pre-roll) or at visit time (personal), both via `renpy.random` — rollback-safe
- All state is stored in simple Ren'Py store dicts/lists — save-compatible

---

## Store Variables

| Variable | Type | Purpose |
|---|---|---|
| `wed_personal_fired_day` | int | Day when last personal event fired. `-1` = none today. Check `!= day` for "one per day." |
| `wed_ambient_fired` | dict | `{location_id: True}` — marks locations where ambient already fired this visit |
| `wed_ambient_today` | dict | Pre-rolled: `{location_id: event_id_or_None}` for today |
| `wed_event_last_day` | dict | `{event_id: day}` — for cooldown calculations |
| `wed_resolved` | list | `[event_id]` — once-only events that have fired (permanent) |
| `wed_callbacks` | list | `[{label, fires_day}]` — pending callbacks |
| `wed_ready_callbacks` | list | Callbacks whose `fires_day` has passed; fire at next location visit |

All variables have safe defaults in `data.rpy`. Old saves receive empty dicts/lists — all functions guard against missing keys.

---

## Event Registry (`WED_REGISTRY`)

Defined in `world_events.rpy` `init python:` block.

```python
WED_REGISTRY = {
    "event_id": {
        "type":         "ambient" | "personal",
        "label":        "wevent_label_name",
        "locations":    ["location_bar", ...],   # eligible location IDs
        "min_day":      int,                      # earliest day (inclusive)
        "once":         True | False,             # once=True: never repeats after first fire
        "priority":     int,                      # higher = preferred when multiple eligible
        "cooldown":     int,                      # days between fires (0 = use once flag only)
        "weight":       float,                    # ambient only: 0.0–1.0 probability per day
        "conflict_npc": "npc_id" | None,          # personal only: blocked if active commitment today
    }
}
```

---

## Event Types

### Ambient Events

- Pre-rolled once per day in `new_day()` via `wed_preroll_day()`
- One per location per visit (second visit to the same location does not re-roll)
- `weight` is the probability the event fires on any eligible day
- No NPC required to be present

**Pattern in location labels:**
```renpy
$ _wed_amb = wed_poll_ambient("location_bar")
if _wed_amb:
    call expression _wed_amb
```

**Pattern in event label:**
```renpy
label wevent_bar_quiz_night:
    $ wed_fire("bar_quiz_night")   # FIRST line — marks fired, marks ambient location
    ...
```

### Personal Events

- Checked at visit time (not pre-rolled)
- One per day across all locations (`wed_personal_fired_day == day` → skip)
- Structural eligibility checked by `wed_poll_personal()` (location, day, cooldown, major scene, commitment conflict)
- Narrative eligibility (trust/affection thresholds) checked inside the event label
- If the label returns without calling `wed_fire()`, the day slot is not consumed — another event could fire later that day if the player visits a different eligible location

**Pattern in location labels:**
```renpy
$ _wed_per = wed_poll_personal("location_bar")
if _wed_per:
    call expression _wed_per
```

**Pattern in event label:**
```renpy
label wevent_marcus_loan:
    # Narrative check FIRST — return without wed_fire() if not ready
    if not marcus_met or marcus_trust < 20 or wed_marcus_loan_state != "none":
        return
    $ wed_fire("marcus_loan")   # only called when scene actually runs
    ...
```

---

## Callback System

Callbacks are labels scheduled to fire on or after a specific day. They fire at the next location visit after their day.

**Scheduling a callback:**
```python
wed_schedule_callback("wevcb_label_name", fires_day)
```

**Processing:** Called automatically by `wed_preroll_day()` in `new_day()`. Callbacks whose `fires_day <= today` are moved from `wed_callbacks` to `wed_ready_callbacks`.

**Consuming at a location:**
```renpy
$ _wed_cb = wed_pop_callback()
if _wed_cb:
    call expression _wed_cb
```

`wed_pop_callback()` returns the label of one ready callback and removes it from the queue. Returns `None` if no callbacks are ready.

**Note:** For NPC-specific callbacks (like Marcus loan repay) that should fire at a specific location, check the relevant state variable directly in that location rather than using the generic callback queue. See `location_marcus_home` for an example.

---

## Priority Rules

When multiple personal events are eligible at the same location on the same day, the WED picks the one with the highest `priority` value. If two events share the same priority, one is chosen at random from the tied group.

Current priority assignments:
- `priority: 2` — pilot personal events (marcus_loan, sam_off_routine)
- `priority: 1` — ambient events (no priority comparison needed between locations)

Higher-priority events from other systems (e.g. `major_scene_last_day` checks, commitment triggers, pending arc scenes) all fire before the WED hook in every location label. WED hooks are always placed **last** before the activity menu.

---

## Conflict Rules

| Conflict type | Mechanism |
|---|---|
| Active major scene today | `major_scene_last_day == day` — all personal events blocked |
| Active NPC commitment today | `conflict_npc` field — blocks personal event for that NPC |
| Event already fired today | `wed_personal_fired_day == day` — all personal events blocked |
| Ambient already fired at this location entry | `wed_ambient_fired[location]` — ambient blocked |

The WED does not block ambient events during major scenes (an ambient quiz night can still be in the background). Only personal events are blocked.

---

## Adding a New Event

1. Add an entry to `WED_REGISTRY` in `world_events.rpy`
2. Write a label named `wevent_<event_id>`
3. Call `wed_fire("event_id")` at the start of the label (after any narrative eligibility checks)
4. Add the location to the location label's WED hook (or add a WED hook if the location doesn't have one yet):
   - After `show screen hud` and sprite setup, before the `menu (screen="activity"):`
   - For ambient: `$ _wed_amb = wed_poll_ambient("location_id")`
   - For personal: `$ _wed_per = wed_poll_personal("location_id")`
5. If the event needs a callback, write a label named `wevcb_<callback_id>` and call `wed_schedule_callback("wevcb_<callback_id>", fires_day)` inside the event label

**Locations with WED hooks already active:**

| Location | Ambient | Personal |
|---|---|---|
| `location_bar` | `bar_quiz_night` | `marcus_loan` |
| `location_park` | `rain_in_park` | `sam_off_routine` |
| `location_cafe` (cafe_actions) | — | `sam_off_routine` |
| `location_gym` (gym_floor) | — | `sam_off_routine` |
| `location_hub` | `metro_delay` | — |
| `location_hospital` | `metro_delay` | — |

---

## Old Save Compatibility

All WED store variables have `default` declarations in `data.rpy`. Old saves that pre-date the WED load empty collections:
- `wed_event_last_day = {}` — all events treated as never fired
- `wed_resolved = []` — once events not marked resolved
- `wed_callbacks = []` — no pending callbacks
- `wed_personal_fired_day = -1` — no personal event fired yet

Once events that have effectively already "happened" in narrative terms may need guard clauses inside their event labels. For the pilot events (marcus_loan, sam_off_routine), narrative state variables (`wed_marcus_loan_state`, `sam_off_routine_done`) are checked first and will correctly block the event from re-firing in old saves where the scene was never implemented.

---

## Appendix A — WED Hook Flow Audit

Verified control flow for each hooked location. "Before" = everything that runs before the WED poll; "After" = everything that runs after it returns.

| Location label | Hook type | Before the hook | After the hook |
|---|---|---|---|
| `cafe_actions` | personal | group scene check, sprite display | activity menu |
| `gym_floor` | personal | sprite display | activity menu |
| `location_bar` | ambient + personal | priority scenes, `scene bar`, HUD, basketball invite block | `location_sprites()`, sprite display, activity menu |
| `location_park` | ambient + personal | sprite display, group scene check | activity menu |
| `location_hospital` | ambient | lena_shoulder check, `scene hospital`, HUD | `location_sprites()`, sprite display, activity menu |
| `location_hub` | ambient | eli_deploy check, `scene hub`, HUD | activity menu |
| `new_day()` | pre-roll | day advance, stat decay, `roll_daily_events()` | Marcus invite trigger, callback promotion |
| `marcus_talk` (Door 14) | home routing | BG set, HUD | routes to `location_marcus_home` or `npc_interact` |

**Notes:**
- At `location_bar`: WED hooks fire after `scene bar` + HUD (line 640) but before `location_sprites()` (line 668). Events manage their own sprites; the standard sprite setup follows after return.
- At `location_hospital` and `location_hub`: WED hook fires after BG/HUD. The `metro_delay` event narration ("The board reads DELAYED") is framed neutrally enough to work at both — the Hub has a departure board, the hospital has nearby transit signage.
- `cafe_actions` and `gym_floor` have personal hooks only; no ambient events are registered for those locations.
- The WED poll at `new_day()` (`wed_preroll_day()`) runs AFTER `roll_daily_events()` — no ordering conflict.

---

## Appendix B — Marcus Home Access Route Table

Route taken when the player visits Door 14 (`marcus_talk`).

| `marcus_home_state` | `marcus_is_home()` | Route taken |
|---|---|---|
| `"locked"` | True | "You don't have Marcus's address yet." → `jump map` |
| `"locked"` | False | "You don't have Marcus's address yet." → `jump map` |
| `"invited_once"` | True | BG shown, callback checks run, activity menu (Talk / Chili / Watch game / Head out). "Head out" promotes state to `"welcome"`. |
| `"invited_once"` | False | "You knock. No answer." → `jump map` |
| `"welcome"` | True | BG shown, callback checks run, activity menu (same as above). |
| `"welcome"` | False | "You knock. No answer." → `jump map` |

`marcus_is_home()` returns True when `10 <= hour < 17` AND `day % 3 != 0` (~67% of afternoons).

**Callback check order** (runs before the activity menu when state is not locked and Marcus is home):
1. If `wed_marcus_loan_callback_ready` and state is `pending_repay` → call `wevcb_marcus_loan_repay`, loop
2. If `wed_marcus_loan_callback_ready` and state is `pending_practical` → call `wevcb_marcus_loan_partial`, loop
3. If `wed_marcus_loan_callback_ready` and state is `pending_solved` → call `wevcb_marcus_loan_solved`, loop
4. Else: proceed to activity menu

---

## Appendix C — Event State-Machine Summary

### Marcus Loan (`wed_marcus_loan_state`)

```
none
 └─ [event fires: wed_fire called] → offered
      ├─ Full loan ($120, try_spend succeeds)  → pending_repay
      │    └─ [day >= callback_day]            → callback_ready
      │         └─ [visit marcus_home]         → resolved_repaid  (terminal)
      ├─ Partial help ($40, try_spend succeeds)→ pending_practical
      │    └─ [day >= callback_day]            → callback_ready
      │         └─ [visit marcus_home]         → resolved_repaid  (terminal)
      ├─ Low-money mutual recognition          → resolved_low_money  (terminal)
      ├─ Respectful refusal                    → resolved_refused
      │    └─ [day >= callback_day]            → pending_solved
      │         └─ [visit marcus_home]         → resolved_solved  (terminal)
      └─ Dismissive refusal (npc_anger +2)     → resolved_dismissed  (terminal)
```

Note: `resolved_repaid` is the terminal state for both repay and partial-help paths. Marcus considers the debt settled in both cases.

### Sam Off-Routine (`sam_off_routine_done`)

```
False
 └─ [event fires at cafe or gym, off-schedule at gym]
      └─ True  (terminal — once-only event)
           └─ [park greet, npc_talkable("sam")] → sam_off_routine_greet_done = True
```

### Ambient Events (no named state — cooldown only)

| Event | State tracked | Cooldown |
|---|---|---|
| `metro_delay` | `wed_event_last_day["metro_delay"]` | 5 days |
| `rain_in_park` | `wed_event_last_day["rain_in_park"]` | 4 days |
| `bar_quiz_night` | `wed_event_last_day["bar_quiz_night"]` | 6 days |

Ambient events are not `once=True`; they repeat after the cooldown window.
