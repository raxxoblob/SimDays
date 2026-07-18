# Gameplay Polish — Verification & Cleanup Report

## Post-audit fixes applied — 2026-07-17

Nine targeted fixes applied to gameplay expansion scenes. All edits are minimal; no new features added.

| Fix | Scene / system | Change | Status |
|-----|---------------|--------|--------|
| FIX 1 | kitchen_lena_extended staging hook | Already present in `home_scenes.rpy` — no change needed | Verified ✓ |
| FIX 2 | lena_shoulder_gesture trigger | Replaced worn_out() (already removed) with `hospital_hard_case_pending` gate; added setter in hospital shift (`locations.rpy`: `job_performance < 70`); added `default hospital_hard_case_pending = False` | Implemented |
| FIX 3 | nora_hug_school trigger | Removed `nora_bad_day_done` gate; now requires `nora_school_revealed + aff >= 40 + trust >= 35` | Implemented |
| FIX 4 | martha_corridor context | Added `martha_corridor_context` dict on pending set (`interact.rpy`); `_corridor_src` read at scene start (`gameplay_expansion_scenes.rpy`); added `default martha_corridor_context = None` | Implemented |
| FIX 5 | marcus_missed location in dialogue | Added `_missed_loc`/`_missed_title` from pending dict; changed "You blew me off." to `"I was at [_missed_loc]. [_missed_title]. You didn't show."` | Implemented |
| FIX 6 | martha_gift gift_name in dialogue | Added `_gift_name`/`_gift_count` at scene start; changed confrontation line to `"[_gift_name]. And the ones before it."` | Implemented |
| FIX 7 | martha_gift trigger count | Changed `>= 2` to `== 3` (AFTER gift_log append); fires exactly on the 3rd gift, not re-triggers on 4th+ | Implemented |
| FIX 8 | marcus_missed CG neutrality | CG name `cg_marcus_missed` is generic (no location suffix) — confirmed neutral; added comment in scene | Verified ✓ |
| FIX 9a | nora_ignored_response cleared | Added `$ nora_ignored_response = ""` before return in `scene_nora_feels_ignored` | Implemented |
| FIX 9b | nora_kai cooldown | Added `nora_kai_retry_after_day` default; expiry block sets 21-day cooldown; trigger setter checks `day >= nora_kai_retry_after_day` | Implemented |
| FIX 9c | hospital_break_room_day bg | Already wired in `scene_lena_hospital_break_room` — no change needed | Verified ✓ |

---

## Discrepancy Table

| Fix | Pre-cleanup code state | Current state |
|-----|----------------------|---------------|
| FIX 1 — Coding EXP | `gain_skill("prog", 3)` flat — no kit bonus | `gain_skill("prog", 7 if own_programming_kit else 5)` |
| FIX 2 — Stock trading time cost | No time charge anywhere; `stock_buy`/`stock_sell` purely mutated money | `_stock_session_charged` flag; first buy or sell in a session calls `spend_time(0.5)`; flag cleared when market opens, not on every trade |
| FIX 3 — Overlap warnings | Only guitar, library study, and café shift had warnings; all 8h career shifts, college courses, sleep options, nap, dates, and metal detector were unguarded | `_overlap_warning_text(N)` confirm/cancel blocks now cover all 17 time-significant activities (see System Summary below) |
| FIX 4 — HUD notified filter | `if _nc and not _nc.get("notified") and ...` — HUD silently suppressed the reminder after the one-time toast fired | Removed `not _nc.get("notified")` from `hud.rpy`; `notified` still gates the toast in `notify_available_commitments` only |
| FIX 5 — Career perf threshold keys | String keys `"it_0_50"` | 3-tuple `(job_id, job_rank, threshold)` |
| FIX 6 — Relationship threshold keys | String keys `"nora_aff_25"` | 3-tuple `(npc_id, stat_type, threshold)` |
| FIX 7 — Hug failure outcomes | Single `hp["low_trust"]` returned for both aff-block and trust-block | `"low_affection"` key added to every HUG_PROFILE; `do_hug()` returns `hp["low_affection"]` when `aff < min_aff` and `hp["low_trust"]` when `aff >= min_aff` but `trust < min_trust` |
| FIX 8 — Activity tracking | Two parallel mechanisms: `activity_last_used[id] = day` for recency + compound key `id_dDAY` for daily count — grew unboundedly | Single `activity_daily_uses[id] = {"day": N, "count": K}`; count auto-resets when `entry["day"] != store.day`; public interface unchanged |
| FIX 9 — Quest conditions | "Keep Your Word" done lambda used `any(c["completed"] …)` satisfiable by test stubs; "Time for a Promotion" body said "performance is at 100" but quest shows at 80 | done lambda filters `c["npc_id"] in NPC_DATA`; body text corrected to "Push to 100 and request a review." |
| FIX 10 — Tests | Tests covered systems 1–10 but used old `activity_last_used` key, old string threshold keys, and had no coverage for FIX 4/5/6/7/8 specifics | Snapshot/restore uses `activity_daily_uses`; groups 11 (career perf 3-tuple key) and 12 (HUD ignores notified) added; tests 7/8/9 updated |

---

## System Summaries

### FIX 1 — Home Coding Practice EXP
- File: `locations.rpy` — `use_computer` label, "Practice coding (3h)" option
- Code: `gain_skill("prog", 7 if own_programming_kit else 5)`
- Base: +5 Programming EXP; with `own_programming_kit`: +7 Programming EXP
- Deliberately weaker than a paid college course (+10 EXP via `take_course`)

### FIX 2 — Stock Trading Time Cost
- Files: `data.rpy` (default `_stock_session_charged = False`), `locations.rpy` (resets flag with `store._stock_session_charged = False` before `call screen stock_market`), `stocks.rpy` (`stock_buy` and `stock_sell`)
- `spend_time(0.5)` fires on the first buy or sell in a visit; subsequent trades in the same session are free
- Browsing portfolio or closing without trading costs nothing

### FIX 3 — Overlap Warnings — Complete Protected Activity List
- Mechanism: `_overlap_warning_text(N)` (defined in `data.rpy`) returns a warning string when any active same-day commitment falls within `[now, now+N)` hours; an empty string when clear. Each protected activity shows a confirm/cancel menu on non-empty result.
- A separate function `activity_would_overlap_commitment(duration_hours)` (defined in `phone_messages.rpy`) returns the conflicting commitment object or `None`; used in tests and the phone UI.
- All 17 currently overlap-guarded activities:

| Activity | Duration | Location |
|----------|----------|----------|
| Guitar practice | 2h | `location_home` |
| Library study (general) | 2h | `location_library` |
| Café barista shift | 4h | `cafe_work_shift` |
| Home nap | 3h | `location_home` (requires `own_bed`) |
| NPC date | 3h | `npc_date` in `interact.rpy` |
| College course | 3h | `college_course` label |
| Sleep 2h | 2h | `action_sleep_menu` |
| Sleep 4h | 4h | `action_sleep_menu` |
| Sleep 6h | 6h | `action_sleep_menu` |
| Sleep 8h (new day) | 8h | `action_sleep_menu` |
| IT shift | 6h (prog ≥ 5) or 8h | `location_hub` |
| Hospital shift | 8h | `location_hospital` |
| Corporate shift | 8h | `location_office` |
| Trainer shift | 8h | `location_gym` |
| Culinary shift | 8h | `location_kitchen` |
| Warehouse shift | 8h | `location_warehouse` |
| Sandbeach metal detector | 2h | `location_sandbeach` |

### FIX 4 — HUD Reminder
- File: `hud.rpy`
- Current condition: `if _nc and hours_until_commitment(_nc) <= 3 and hours_until_commitment(_nc) > 0:`
- No `notified` check; HUD shows the nearest active commitment within 3 hours regardless of its `notified` state
- `notified = True` still gates the one-time push notification in `phone_messages.notify_available_commitments`

### FIX 5 — Career Perf Threshold Keys
- File: `careers.rpy` — `_check_career_perf_threshold(perf)`
- Key: `(job_id, job_rank, threshold)` tuple; hitting 80 in IT does not consume the 80-slot for corporate; rank promotion restores all thresholds for the new rank
- Thresholds and messages: 50 → "Your work is being noticed.", 80 → "You're close to a review.", 100 → "You're ready for a promotion."

### FIX 6 — Relationship Threshold Keys
- File: `interact.rpy` — `_check_relationship_thresholds(npc_id)`
- Key: `(npc_id, stat_type, threshold)` tuple; `("nora", "aff", 25)` and `("nora", "trust", 25)` are distinct
- Stored in `relationship_thresholds_seen`; default in `data.rpy`

### FIX 7 — Hug Failure Outcomes
- File: `interact.rpy` — `HUG_PROFILES` (11 profiles: martha, nora, zoe, eli, lena, marcus, kai, natalie, caroline, elle, sam) and `do_hug(npc_id)`
- `do_hug()` return paths in order of evaluation:
  1. `hp.get("low_affection", hp["low_trust"])` — when `aff < hp["min_aff"]` (all 11 profiles have a distinct `"low_affection"` key, so the fallback is never reached in practice)
  2. `hp["low_trust"]` — when `aff >= min_aff` but `trust < hp["min_trust"]`
  3. `hp["too_soon"]` — when `day - last_hug_day < hp["cooldown_days"]` (cooldown active); also applies `repeat_gain` to affection
  4. `hp["first"]` — first accepted hug; applies `aff_gain` + `trust_gain`; records "first_hug_{npc_id}" memory
  5. `hp["warm"]` — subsequent accepted hugs; applies `repeat_gain` to affection
  - Note: `hp["repeat"]` key exists in profiles (holds a flavour line) but `do_hug()` does not return it — it returns `hp["warm"]` for all non-first accepted hugs.

### FIX 8 — Activity Tracking Consolidation
- File: `data.rpy`
- Default: `activity_daily_uses = {}` (replaces old dual-mechanism `activity_last_used` + compound-key pattern)
- Schema: `{activity_id: {"day": N, "count": K}}`
- Count auto-resets to 0 when `entry["day"] != store.day`; the entry itself persists (bounded key space)
- Public helpers: `activity_recently_used(id, days=1)`, `activity_use_count_today(id)`, `mark_activity_used(id)`, `mark_activity_used_today(id)`
- Old compound key pattern (`"park_jog_d5"`) is gone

### FIX 9 — Quest Conditions
- File: `quests.rpy`
- "Keep Your Word": done condition filters `c["npc_id"] in NPC_DATA` to exclude test stubs
- "Time for a Promotion": body text corrected; show condition (perf ≥ 80) documented via comment
- Other 5 quests verified correct: variable references exist, completion stamps via `quests_completed` list

### FIX 10 — Tests
- File: `test_gameplay_polish.rpy`
- 13 test groups, 35 individual assertions
- Snapshot/restore uses `activity_daily_uses` (not old `activity_last_used`)
- Group 11: career perf threshold 3-tuple key (`(job_id, job_rank, threshold)`)
- Group 12: HUD next_commitment found even after `notified = True`
- Group 13: hug outcome routing — `too_soon` (days_since < cooldown), `repeat` (days_since == cooldown, below warm threshold), `warm` (days_since >= warm_after_days)
- Group 7: asserts both `low_affection` and `low_trust` paths independently
- Group 8: asserts 3-tuple relationship threshold key after crossing aff 25
- Group 9: verifies auto-reset semantics — count returns 0 on a new day; underlying entry day is yesterday

---

## Verified against current code

Inspected files and key symbols confirmed present:

- `data.rpy`: `activity_daily_uses` (default `{}`), `gift_log` (default `[]`), `major_scene_last_day` (default `-1`), `nora_kai_retry_after_day` (default `0`), `hospital_hard_case_pending` (default `False`), `martha_corridor_context` (default `None`), `_stock_session_charged` (default `False`), `career_perf_thresholds_seen` (default `{}`); activity helpers `activity_recently_used`, `activity_use_count_today`, `mark_activity_used`, `mark_activity_used_today`; overlap helper `_overlap_warning_text(duration)`
- `interact.rpy`: `do_hug()` with 5 return paths; `HUG_PROFILES` with 11 profiles each containing `low_affection` and `low_trust` keys; `gift_count_for(npc_id)`; `_check_relationship_thresholds()` using `(npc_id, stat_type, threshold)` 3-tuple keys; `do_gift()` with martha gift trigger at `gift_count_for("martha") == 3`; `npc_date` label with `_overlap_warning_text(3)` guard
- `locations.rpy`: `use_computer` label — `gain_skill("prog", 7 if own_programming_kit else 5)` confirmed; `store._stock_session_charged = False` reset before `call screen stock_market`; `_overlap_warning_text(N)` guards on all 17 activities listed in FIX 3 table; `college_course` label has 3h overlap guard; `action_sleep_menu` has guards on all 4 timed sleep options (2h/4h/6h/8h); IT shift uses `_it_h = 6 if skill_prog >= 5 else 8`
- `stocks.rpy`: `stock_buy` and `stock_sell` both check `not store._stock_session_charged` before calling `spend_time(0.5)` and setting flag
- `careers.rpy`: `_check_career_perf_threshold(perf)` — key is `(store.job_id, store.job_rank, thresh)` 3-tuple; thresholds 50/80/100
- `hud.rpy`: commitment reminder condition is `if _nc and hours_until_commitment(_nc) <= 3 and hours_until_commitment(_nc) > 0:` — no `notified` filter present
- `phone_messages.rpy`: `activity_would_overlap_commitment(duration_hours)` — returns conflicting commitment dict or `None`; distinct from `_overlap_warning_text` which returns a display string
- `test_gameplay_polish.rpy`: 13 test groups (groups 1–13), 35 total `check()` assertions; snapshot/restore covers `activity_daily_uses`, `relationship_thresholds_seen`, `npc_last_hug_day`, `career_perf_thresholds_seen`
