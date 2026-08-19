# Gameplay Polish — Final Report

## Changed Files

| File | Nature of change |
|------|-----------------|
| `game/data.rpy` | New defaults + anti-repetition helpers + `_overlap_warning_text` |
| `game/phone_messages.rpy` | New agenda/planner helpers |
| `game/phone.rpy` | Agenda section in messages screen, memory display in contacts |
| `game/hud.rpy` | Next-commitment HUD reminder |
| `game/interact.rpy` | Memory helpers, threshold notifications, modified `_apply_aff`/`_apply_trust`, `HUG_PROFILES`, `do_hug`, updated hug action in `npc_interact` + `npc_actions` screen |
| `game/careers.rpy` | `career_arc_progress`, `_check_career_perf_threshold`, call in `do_shift` |
| `game/profile.rpy` | Career arc progress + colour-coded next-rank requirements in WORK section |
| `game/locations.rpy` | `add_relationship_memory` calls in 4 scenes, anti-repetition for 5 activities, overlap warnings for 3 activities |
| `game/phone_actionable.rpy` | `add_relationship_memory` calls in 4 commitment scenes |
| `game/quests.rpy` | 7 new quest entries |
| `game/test_gameplay_polish.rpy` | New file — 10-test suite |
| `docs/gameplay_polish_audit.md` | Audit document |
| `docs/economy_and_time_audit.md` | Economy/time table + imbalance analysis |

---

## New Helper Functions

### data.rpy
- `activity_recently_used(activity_id, days=1)` — was this activity used in the last N days?
- `mark_activity_used(activity_id)` — record day-level use
- `activity_use_count_today(activity_id)` — how many times today?
- `mark_activity_used_today(activity_id)` — increment today's count
- `_overlap_warning_text(duration)` — returns warning string if a commitment would be skipped

### phone_messages.rpy
- `today_commitments()` — active commitments for today
- `tomorrow_commitments()` — active commitments for tomorrow
- `next_commitment()` — soonest not-yet-started active commitment
- `hours_until_commitment(c)` — float hours until commitment fires
- `commitment_status_text(c)` — human-readable status: "Available now", "In 3h", "Tomorrow", etc.
- `activity_would_overlap_commitment(duration_hours)` — returns first overlapping commitment or None

### interact.rpy
- `add_relationship_memory(npc_id, memory_id, title)` — add a deduplicated memory entry
- `relationship_memory_exists(npc_id, memory_id)` — membership check
- `relationship_memories_for(npc_id)` — list of all memories for an NPC
- `_check_relationship_thresholds(npc_id)` — fire `renpy.notify()` once for each new milestone
- `do_hug(npc_id)` — full hug logic: profile check, cooldown, gains, memory

### careers.rpy
- `career_arc_progress(cid)` — returns `(done_steps, total_steps)` for a career's arc
- `_check_career_perf_threshold(perf)` — notify once when performance crosses 50/80/100

---

## New `default` Variables

| Variable | Default | File |
|----------|---------|------|
| `relationship_memories` | `{}` | data.rpy |
| `relationship_thresholds_seen` | `{}` | data.rpy |
| `npc_last_hug_day` | `{}` | data.rpy |
| `activity_last_used` | `{}` | data.rpy |
| `career_perf_thresholds_seen` | `{}` | data.rpy |

All are save-safe: old saves receive the default value automatically.

---

## UI Changes

### phone_messages_scr (phone.rpy)
- Added **Agenda** section above City News: shows today + tomorrow active commitments with live status text (colour-coded: blue = available, dim = done/missed, grey = upcoming).
- Added **relationship memories** under each contact's last message (last 2 memories).

### HUD (hud.rpy)
- Added **next-commitment reminder**: if a commitment is within 3h and not yet notified, a small blue text appears below the tooltip bar.

### Profile — WORK section (profile.rpy)
- Added **Career story: X/Y** progress line showing arc flag completion.
- Added **colour-coded next-rank requirements**: each stat/skill/degree requirement shown individually with ✓ (blue) or current progress (red).

---

## Balance Changes

| Activity | Before | After |
|----------|--------|-------|
| Park jog, 2nd use/day | +4–8 STR EXP | +2–4 STR EXP |
| Park jog, 3rd+ use/day | +4–8 STR EXP | 0 (flavour only) |
| Park read, 2nd use/day | +3 INT EXP | +1 INT EXP |
| Park read, 3rd+ use/day | +3 INT EXP | 0 (flavour only) |
| Home guitar, 2nd use/day | +5 Music EXP | +2 Music EXP |
| Home guitar, 3rd+ use/day | +5 Music EXP | 0 (flavour only) |
| Bar socialize, 2nd use/day | +15–30 CHR EXP | +7–15 CHR EXP |
| Bar socialize, 3rd+ use/day | +15–30 CHR EXP | 0 (flavour only) |
| Library study, 2nd use/day | +10 INT EXP | +5 INT EXP |
| Library study, 3rd+ use/day | +10 INT EXP | 0 (flavour only) |
| Hug (all NPCs) | +3 aff, 0.1h, generic text | Profile-specific text, cooldown, gains per profile, first-hug memory |

---

## Test Coverage

`test_gameplay_polish.rpy` covers 10 test cases via `label test_gameplay_polish_run`:

1. Commitment overlap detection (3h overlaps, 1h doesn't)
2. Commitment status text ("In 3h", "Available now")
3. Today/tomorrow commitment helpers + `next_commitment()`
4. Memory deduplication (same id added twice = one entry)
5. Hug cooldown (same-day = too_soon)
6. First hug adds memory
7. Hug low-aff block returns low_trust text
8. Relationship threshold deduplication (crossing 25 twice = one notify)
9. Activity diminishing returns counter (0→1→2, resets on new day)
10. Career arc progress (tuple type, flag counting, unknown career = (0,0))

---

## Manual Regression Checklist

The following scenarios require in-game verification:

- [ ] Accept a commitment, let the grace window expire → NPC sends missed text; shows "Missed" in agenda
- [ ] Start a 4h café shift 2h before a commitment → overlap warning shown, player can choose to continue
- [ ] Cancel a commitment → shows "Cancelled" in agenda; trust penalty applied
- [ ] Miss a commitment → shows "Missed"; NPC message arrives next day
- [ ] First hug Martha (needs aff ≥ 35, trust ≥ 30) → first text, +2 aff, +1 trust, memory logged
- [ ] Second hug Martha same day → too_soon text
- [ ] Hug Martha after 4+ days → warm text
- [ ] Affection crosses 25 for first time → renpy.notify fires once
- [ ] Affection crosses 25 again (via rollback/load) → no second notify
- [ ] Career performance crosses 80 → notification fires once; stays silent after load/rollback
- [ ] Career promotion → new rank; old thresholds don't re-fire
- [ ] Save/load with new default vars → game starts cleanly, no AttributeError
- [ ] Rollback after hug → state restored; memory check works correctly
- [ ] Rollback after phone action → npc_messages restored
- [ ] Profile screen while employed → shows arc progress, colour-coded requirements
- [ ] Profile screen while unemployed → shows "Unemployed" cleanly, no arc panel errors

---

## Known Ceiling / Upgrade Path Notes

- **Anti-repetition system** uses a per-day key (`activity_id_dN`). If the player time-travels or saves are manipulated, counts could be wrong. Ceiling: global count key, not per-day. Upgrade: use `(activity_id, day)` tuple key when dict is persisted.
- **Hug cooldown** uses `store.day` integer. If `day` is rolled back via Ren'Py's rollback, `npc_last_hug_day` is also rolled back (it's a store variable). This is correct behaviour.
- **Threshold notifications** are fire-and-forget via `renpy.notify()`. They don't appear in the inbox. If the player misses the toast, there's no other record. Upgrade: add to inbox as a system message.
