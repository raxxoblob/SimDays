# Gameplay Expansion Scene Pack — Technical Asset Context Report

> Source files read: `gameplay_expansion_scenes.rpy`, `locations.rpy`, `data.rpy`, `interact.rpy`, `phone_actionable.rpy`, `phone_messages.rpy`, `images.rpy`.
> All claims are directly verifiable in those files. Nothing is invented or assumed.

**Note on scene count:** The file header in `gameplay_expansion_scenes.rpy` reads "17 gameplay expansion scenes" but 19 `label` blocks are present. The discrepancy is not explained in the code.

---

## Section 1 — Scene Table

| Scene ID | Trigger | Pending state | Canonical location | Time window | Outfit | Asset(s) | Fallback | Expiry |
|---|---|---|---|---|---|---|---|---|
| `scene_nora_feels_ignored` | `new_day()` sets `nora_ignored_pending = True` when aff≥30, trust≥20, `nora_closing_done`, contact in list, absent 8+ days | boolean | `location_cafe` | any | `nora_cafe_normal` | `cg_nora_feels_ignored` | none — waits indefinitely at café | none |
| `scene_marcus_missed_commitment` | `mark_commitment_missed()` when NPC is marcus and `marcus_affection >= 30` | dict | `location_bar` or `location_park` (both checked) | any | `marcus_casual_normal` | `cg_marcus_missed`; bg derived from `current_loc` | bg falls back to `parkday` if not at bar | none |
| `scene_wardrobe_martha` | self-staging: `wardrobe_tier >= 2`, `martha_affection >= 25`, `martha_met`, `not martha_wardrobe_done` | self-stage | `location_office` | any (office hours only) | `martha_neutral` | `cg_wardrobe_martha` | none — waits for next office visit | none |
| `scene_guitar_zoe_busking` | player menu option: `own_guitar`, `skill_music >= 3`, `zoe_affection >= 30`, `zoe_met`, `not zoe_park_guitar_done`, Thu/Fri 14–17 | self-stage | `location_park` | Thu/Fri (`day % 7 in [3,4]`), `hour >= 14` and `hour <= 17` | `zoe_street_neutral` | `cg_zoe_guitar` | option hidden if conditions not met | none |
| `scene_lena_hospital_break_room` | player menu option: `lena_affection >= 20`, `lena_trust >= 15`, `lena_met`, `not lena_break_room_done`, 12–14 | self-stage | `location_hospital` | `hour >= 12` and `hour <= 14` | `drlena_normal` | `hospital_break_room` (bg, not CG) | option hidden outside time window | none |
| `scene_martha_office_coffee` | self-staging: `hour < 10`, `martha_affection >= 20`, `martha_met`, `not martha_coffee_machine_done` | self-stage | `location_office` | `hour < 10` | `martha_neutral` | `nexus_coffee_machine` | none — waits for next early morning office visit | none |
| `scene_nora_bad_day` | `new_day()` sets `nora_bad_day_pending = True` when aff≥30, trust≥20, `nora_closing_done`, contact in list, `worn_out()`; player accepts via phone → `nora_bad_day_1` commitment | boolean + commitment | `location_home_actions` | `hour >= 19` (commitment hour) | `nora_casual_normal` (conditional: only if `renpy.loadable(...)`) | `nora_bad_day_cheap` / `nora_bad_day_good` / `nora_bad_day_rich` (selected by `apartment_tier`) | no sprite if `nora_casual_normal.png` not loadable | condition-based: cleared if player declines via `phone_reply_nora_bad_day_decline` |
| `scene_kitchen_lena_extended` | staging hook not found in any listed file — likely in `home_scenes.rpy` | self-stage | not found in `locations.rpy` | not found | `drlena_normal` | `lena_dinner_good` (tier 2) or `lena_dinner_rich` (tier 3); none for tier 1 | tier 1 → `home_bg()` used, no CG | none |
| `scene_martha_corridor_gesture` | `_check_relationship_thresholds("martha")` when `martha_affection >= 40` and `martha_trust >= 35` | boolean | `location_office` | `hour >= 9` and `hour < 18`; also blocked by `major_scene_last_day == day` | `martha_neutral` | `cg_martha_gesture` | none — waits indefinitely | none |
| `scene_nora_hug_school` | `new_day()` when `nora_bad_day_done` and `nora_school_revealed` | boolean | `location_cafe` | any; blocked by `major_scene_last_day == day` | `nora_cafe_normal` | `cg_nora_hug_school` | none — waits indefinitely | none |
| `scene_eli_deploy_hug` | `new_day()` when `programming_kit_eli_done` | boolean | `location_hub` | `hour >= 19`; blocked by `major_scene_last_day == day` | `eli_normal` | `cg_eli_deploy_hug` | none — waits indefinitely | none |
| `scene_lena_shoulder_gesture` | `new_day()` when `lena_break_room_done`, aff≥45, trust≥45, `worn_out()` | boolean | `location_hospital` | any; blocked by `major_scene_last_day == day` | `drlena_normal` | `cg_lena_shoulder` | none — blocked if player never becomes `worn_out()` again | none |
| `scene_nora_kai_crossover` | `new_day()` when `nora_affection >= 30`, `kai_affection >= 20`, both met, not done | boolean | `location_cafe` | any | `nora_cafe_normal` + `kai_normal` | `cg_nora_kai` | none | 14d — `nora_kai_pending` cleared and `nora_kai_pending_day` reset after 14 in-game days |
| `scene_eli_meets_zoe` | player menu option: `own_programming_kit`, `eli_affection >= 35`, `zoe_affection >= 30`, both met, not done | self-stage | `location_hub` | any (hub open hours) | `eli_normal` + `zoe_street_neutral` | `cg_eli_zoe_collab` | none | none |
| `scene_car_marcus_drive` | self-staging: `not car_marcus_drive_done`, `marcus_affection >= 30`, `marcus_trust >= 20`, `car_tier >= 1`, `hour >= 22`, `major_scene_last_day != day` | self-stage | `location_bar` | `hour >= 22` | no sprite (car image IS Marcus) | `car_interior_night`, `car_interior_pov`, `car_marcus_night` | none | none |
| `scene_martha_gift_accusation` | `do_gift("martha", ...)` when `gift_count_for("martha") >= 2`, not done, pending is None | dict | `location_office` | `hour >= 9` and `hour < 18` | `martha_neutral` | `cg_martha_gift` | none — waits indefinitely at office | `4d→delayed variant`: `variant` promoted `"immediate"→"delayed"` by `new_day()` after 4 days; no expiry |
| `scene_programming_kit_eli` | player menu option: `own_programming_kit`, `eli_affection >= 30`, `eli_trust >= 25`, `eli_met`, `not programming_kit_eli_done`, `hour >= 17` | self-stage | `location_hub` | `hour >= 17` | `eli_normal` | `cg_eli_hardware` | none | none |
| `scene_zoe_rain_shelter` | self-staging: `not zoe_rain_done`, `zoe_met`, `zoe_affection >= 15`, Thu/Fri, `14 <= hour <= 18` | self-stage | `location_park` | Thu/Fri (`day % 7 in [3,4]`), `14 <= hour <= 18` | `zoe_street_neutral` | `parkday_rain` | none — waits for next Thu/Fri 14–18 park visit | none |
| `scene_zoe_spontaneous` | `new_day()` when `zoe_affection >= 45`, `zoe_trust >= 35`, `zoe_beach_night_done` | boolean | `location_nightclub` | `hour >= 21`; blocked by `major_scene_last_day == day` | `zoe_street_neutral` (hidden before CG) | `cg_zoe_almost` | none — waits indefinitely at nightclub | none |

---

## Section 2 — Pending Dict Schemas

### Dict pending flags

#### `marcus_missed_pending`

Exact Python structure (set in `mark_commitment_missed()`, `phone_messages.rpy`):

```python
store.marcus_missed_pending = {
    "trigger_day":    store.day,          # int — day the commitment was missed
    "commitment_id":  c["id"],            # str — e.g. "marcus_park_1"
    "title":          c["title"],         # str — commitment display name
    "location":       c.get("location", ""), # str — scheduled location of the missed commitment
    "hour":           c["hour"],          # int — scheduled hour
    "variant":        _variant,           # str: "first_miss" or "repeat_miss"
}
```

- **Created:** `phone_messages.rpy` / `mark_commitment_missed()` / when `c["npc_id"] == "marcus"` and `marcus_affection >= 30` and `marcus_missed_pending is None`.
- **Modified:** not modified after creation.
- **Cleared:** `marcus_missed_pending = None` at the end of `scene_marcus_missed_commitment` (both the leave-without-speaking branch and the normal branch).
- **Stale behaviour:** if the player avoids both park and bar indefinitely, the dict persists in save data. The scene fires on the next park or bar visit regardless of how many days have passed; the `_mc_days` calculation in the scene (`day - marcus_missed_pending["trigger_day"]`) will show the real elapsed time and branch dialogue accordingly.

> **Note:** `mark_commitment_missed()` also sets `store.marcus_missed_done = False` when creating the dict, allowing a second scene fire after a second miss.

---

#### `martha_gift_scene_pending`

Exact Python structure (set in `do_gift()`, `interact.rpy`):

```python
store.martha_gift_scene_pending = {
    "trigger_day":      store.day,              # int — day the 2nd+ gift was given
    "gift_id":          gift_type,              # str — gift key, e.g. "flowers"
    "gift_name":        GIFT_TYPES[gift_type][0], # str — display name, e.g. "Flowers"
    "gift_count":       _gc,                    # int — total gifts given to Martha so far
    "trigger_location": store.current_loc,      # str — location label where gift was given
    "variant":          "immediate",            # str: "immediate" or "delayed"
}
```

- **Created:** `interact.rpy` / `do_gift()` / when `npc_id == "martha"` and `gift_count_for("martha") >= 2` and `not martha_gift_accusation_done` and `martha_gift_scene_pending is None`.
- **Modified:** `data.rpy` / `new_day()` / when `variant == "immediate"` and `day >= trigger_day + 4` → a copy is made with `variant = "delayed"` and assigned back to `store.martha_gift_scene_pending`.
- **Cleared:** `martha_gift_scene_pending = None` at the end of `scene_martha_gift_accusation`.
- **Stale behaviour:** if the player avoids the office, the dict persists indefinitely. After 4 in-game days the `variant` field is silently promoted to `"delayed"`, which changes Martha's opening line from "I want to ask you something directly." to "I've been meaning to bring something up."

---

### Boolean pending flags

| Flag | Default | Set True (file / function / condition) | Set False |
|---|---|---|---|
| `nora_ignored_pending` | `False` | `data.rpy` / `new_day()` / aff≥30, trust≥20, `nora_closing_done`, contact in list, absent 8+ days | `scene_nora_feels_ignored` on completion |
| `nora_bad_day_pending` | `False` | `data.rpy` / `new_day()` / aff≥30, trust≥20, `nora_closing_done`, contact in list, `worn_out()` | `scene_nora_bad_day` on completion; or `phone_actionable.rpy` / `phone_reply_nora_bad_day_decline` |
| `martha_corridor_pending` | `False` | `interact.rpy` / `_check_relationship_thresholds("martha")` / aff≥40, trust≥35, not done, not pending | `scene_martha_corridor_gesture` on completion |
| `nora_hug_school_pending` | `False` | `data.rpy` / `new_day()` / `nora_bad_day_done` and `nora_school_revealed` | `scene_nora_hug_school` on completion |
| `eli_deploy_pending` | `False` | `data.rpy` / `new_day()` / `programming_kit_eli_done` | `scene_eli_deploy_hug` on completion |
| `lena_shoulder_pending` | `False` | `data.rpy` / `new_day()` / `lena_break_room_done`, aff≥45, trust≥45, `worn_out()` | `scene_lena_shoulder_gesture` on completion |
| `nora_kai_pending` | `False` | `data.rpy` / `new_day()` / aff(nora)≥30, aff(kai)≥20, both met, not done | `new_day()` on 14d expiry; or `scene_nora_kai_crossover` on completion |
| `zoe_moment_deflected_pending` | `False` | `data.rpy` / `new_day()` / aff≥45, trust≥35, `zoe_beach_night_done` | `scene_zoe_spontaneous` on completion |

---

## Section 3 — Hook Map

### scene_nora_feels_ignored
1. **Trigger hook:** `data.rpy` / `new_day()` / `not nora_ignored_done and not nora_ignored_pending and nora_affection >= 30 and nora_trust >= 20 and nora_closing_done and "nora" in npc_contacts and (day - nora_last_seen_day) >= 8`
2. **Staging hook:** `locations.rpy` / `location_cafe` (Priority 2, line 207) / `nora_ignored_pending and nora_met`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_nora_feels_ignored`
4. **Completion:** `nora_ignored_done = True`, `nora_ignored_pending = False`

### scene_marcus_missed_commitment
1. **Trigger hook:** `phone_messages.rpy` / `mark_commitment_missed()` / `c["npc_id"] == "marcus" and marcus_affection >= 30 and marcus_missed_pending is None`
2. **Staging hook:** `locations.rpy` / `location_bar` (Priority 2, line 585) and `location_park` (Priority 2, line 1088) / `marcus_missed_pending and marcus_affection >= 30`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_marcus_missed_commitment`
4. **Completion:** `marcus_missed_done = True`, `marcus_missed_pending = None`

### scene_wardrobe_martha
1. **Trigger hook:** N/A (self-staging)
2. **Staging hook:** `locations.rpy` / `location_office` (Priority 4/5, line 652) / `wardrobe_tier >= 2 and martha_affection >= 25 and martha_met and not martha_wardrobe_done`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_wardrobe_martha`
4. **Completion:** `martha_wardrobe_done = True`

### scene_guitar_zoe_busking
1. **Trigger hook:** N/A (player menu option)
2. **Staging hook:** `locations.rpy` / `location_park` menu (line 1156) / `own_guitar and skill_music >= 3 and zoe_affection >= 30 and zoe_met and not zoe_park_guitar_done and (day % 7 in [3, 4]) and hour >= 14 and hour <= 17`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_guitar_zoe_busking`
4. **Completion:** `zoe_park_guitar_done = True`

### scene_lena_hospital_break_room
1. **Trigger hook:** N/A (player menu option)
2. **Staging hook:** `locations.rpy` / `location_hospital` menu (line 1548) / `lena_affection >= 20 and lena_trust >= 15 and lena_met and not lena_break_room_done and hour >= 12 and hour <= 14`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_lena_hospital_break_room`
4. **Completion:** `lena_break_room_done = True`

### scene_martha_office_coffee
1. **Trigger hook:** N/A (self-staging)
2. **Staging hook:** `locations.rpy` / `location_office` (Priority 4/5, line 654) / `hour < 10 and martha_affection >= 20 and martha_met and not martha_coffee_machine_done`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_martha_office_coffee`
4. **Completion:** `martha_coffee_machine_done = True`

### scene_nora_bad_day
1. **Trigger hook:** `data.rpy` / `new_day()` / `not nora_bad_day_done and not nora_bad_day_pending and nora_affection >= 30 and nora_trust >= 20 and nora_closing_done and "nora" in npc_contacts and worn_out()` → queues phone message with `_NORA_BAD_DAY_RESP`. Player reply `phone_reply_nora_bad_day_accept` (`phone_actionable.rpy`) adds commitment `nora_bad_day_1` with `hour=19`.
2. **Staging hook:** `locations.rpy` / `location_home_actions` (line 34) / `commitment_available("nora_bad_day_1")`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_nora_bad_day`
4. **Completion:** `nora_bad_day_done = True`, `nora_bad_day_pending = False`, `nora_touched_arm = True`

### scene_kitchen_lena_extended
1. **Trigger hook:** not found in any listed file
2. **Staging hook:** not found in `locations.rpy` — **needs implementation or is in `home_scenes.rpy` (not a listed file)**
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_kitchen_lena_extended`
4. **Completion:** `kitchen_lena_extended_done = True`

### scene_martha_corridor_gesture
1. **Trigger hook:** `interact.rpy` / `_check_relationship_thresholds("martha")` / `npc_id == "martha" and martha_affection >= 40 and martha_trust >= 35 and not martha_corridor_done and not martha_corridor_pending`
2. **Staging hook:** `locations.rpy` / `location_office` (Priority 3, line 649) / `martha_corridor_pending and hour >= 9 and hour < 18` (outer guard: `major_scene_last_day != day`)
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_martha_corridor_gesture`
4. **Completion:** `martha_corridor_done = True`, `martha_corridor_pending = False`, `major_scene_last_day = day`

### scene_nora_hug_school
1. **Trigger hook:** `data.rpy` / `new_day()` / `not nora_hug_school_done and not nora_hug_school_pending and nora_bad_day_done and nora_school_revealed`
2. **Staging hook:** `locations.rpy` / `location_cafe` (Priority 3, line 211) / `nora_hug_school_pending and nora_met` (outer guard: `major_scene_last_day != day`)
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_nora_hug_school`
4. **Completion:** `nora_hug_school_done = True`, `nora_hug_school_pending = False`, `major_scene_last_day = day`

### scene_eli_deploy_hug
1. **Trigger hook:** `data.rpy` / `new_day()` / `not eli_deploy_hug_done and not eli_deploy_pending and programming_kit_eli_done`
2. **Staging hook:** `locations.rpy` / `location_hub` (Priority 3, line 1572) / `eli_deploy_pending and eli_met and hour >= 19` (outer guard: `major_scene_last_day != day`)
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_eli_deploy_hug`
4. **Completion:** `eli_deploy_hug_done = True`, `eli_deploy_pending = False`, `major_scene_last_day = day`

### scene_lena_shoulder_gesture
1. **Trigger hook:** `data.rpy` / `new_day()` / `not lena_shoulder_done and not lena_shoulder_pending and lena_break_room_done and lena_affection >= 45 and lena_trust >= 45 and worn_out()`
2. **Staging hook:** `locations.rpy` / `location_hospital` (Priority 3, line 1461) / `lena_shoulder_pending and lena_met` (outer guard: `major_scene_last_day != day`)
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_lena_shoulder_gesture`
4. **Completion:** `lena_shoulder_done = True`, `lena_shoulder_pending = False`, `major_scene_last_day = day`

### scene_nora_kai_crossover
1. **Trigger hook:** `data.rpy` / `new_day()` / `not nora_kai_crossover_done and not nora_kai_pending and nora_affection >= 30 and kai_affection >= 20 and nora_met and kai_met`
2. **Staging hook:** `locations.rpy` / `location_cafe` (Priority 4, line 214) / `nora_kai_pending and nora_met and kai_met`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_nora_kai_crossover`
4. **Completion:** `nora_kai_crossover_done = True`, `nora_kai_pending = False`, `nora_kai_pending_day = -1`

### scene_eli_meets_zoe
1. **Trigger hook:** N/A (player menu option)
2. **Staging hook:** `locations.rpy` / `location_hub` menu (line 1643) / `own_programming_kit and eli_affection >= 35 and zoe_affection >= 30 and eli_met and zoe_met and not eli_meets_zoe_done`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_eli_meets_zoe`
4. **Completion:** `eli_meets_zoe_done = True`

### scene_car_marcus_drive
1. **Trigger hook:** N/A (self-staging)
2. **Staging hook:** `locations.rpy` / `location_bar` (Priority 3, line 589) / `not car_marcus_drive_done and marcus_affection >= 30 and marcus_trust >= 20 and car_tier >= 1 and hour >= 22` (outer guard: `major_scene_last_day != day`)
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_car_marcus_drive`
4. **Completion:** `car_marcus_drive_done = True`, `major_scene_last_day = day`

### scene_martha_gift_accusation
1. **Trigger hook:** `interact.rpy` / `do_gift()` / `npc_id == "martha" and gift_count_for("martha") >= 2 and not martha_gift_accusation_done and martha_gift_scene_pending is None`
2. **Staging hook:** `locations.rpy` / `location_office` (Priority 2, line 645) / `martha_gift_scene_pending and martha_met and hour >= 9 and hour < 18`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_martha_gift_accusation`
4. **Completion:** `martha_gift_accusation_done = True`, `martha_gift_scene_pending = None`

### scene_programming_kit_eli
1. **Trigger hook:** N/A (player menu option)
2. **Staging hook:** `locations.rpy` / `location_hub` menu (line 1647) / `own_programming_kit and eli_affection >= 30 and eli_trust >= 25 and eli_met and not programming_kit_eli_done and hour >= 17`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_programming_kit_eli`
4. **Completion:** `programming_kit_eli_done = True`

### scene_zoe_rain_shelter
1. **Trigger hook:** N/A (self-staging)
2. **Staging hook:** `locations.rpy` / `location_park` (Priority 5, line 1091) / `not zoe_rain_done and zoe_met and zoe_affection >= 15 and day % 7 in [3, 4] and 14 <= hour <= 18`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_zoe_rain_shelter`
4. **Completion:** `zoe_rain_done = True`

### scene_zoe_spontaneous
1. **Trigger hook:** `data.rpy` / `new_day()` / `not zoe_moment_deflected_done and not zoe_moment_deflected_pending and zoe_affection >= 45 and zoe_trust >= 35 and zoe_beach_night_done`
2. **Staging hook:** `locations.rpy` / `location_nightclub` (Priority 3, line 977) / `zoe_moment_deflected_pending and major_scene_last_day != day and hour >= 21 and zoe_met`
3. **Scene label:** `gameplay_expansion_scenes.rpy` / `scene_zoe_spontaneous`
4. **Completion:** `zoe_moment_deflected_done = True`, `zoe_moment_deflected_pending = False`, `major_scene_last_day = day`

---

## Section 4 — Asset Registry

All entries are from the `# ── Gameplay expansion scenes ──` section of `images.rpy` (lines 319–344), plus the `hospital_break_room` entry (line 73) used by `scene_lena_hospital_break_room`.

| Variable name | File path (as registered) | Type | Sprite overlay allowed | Location context | Time of day | NPC outfit shown | Used by scene(s) |
|---|---|---|---|---|---|---|---|
| `cg_nora_feels_ignored` | `images/scenes/nora_feels_ignored/cg_nora_feels_ignored.png` | CG | yes (`nora_cafe_normal` shown before CG) | café | any | Nora — café work outfit | `scene_nora_feels_ignored` |
| `cg_marcus_missed` | `images/scenes/marcus_missed_commitment/cg_marcus_missed.png` | CG | yes (`marcus_casual_normal` shown before and during) | bar or park | any | Marcus — casual | `scene_marcus_missed_commitment` |
| `cg_wardrobe_martha` | `images/scenes/wardrobe_martha/cg_wardrobe_martha.png` | CG | yes (`martha_neutral` shown before CG) | office | any | Martha — work outfit | `scene_wardrobe_martha` |
| `cg_zoe_guitar` | `images/scenes/guitar_zoe_busking/cg_zoe_guitar.png` | CG | yes (`zoe_street_neutral` shown before CG) | park | day (Thu/Fri 14–17) | Zoe — street outfit | `scene_guitar_zoe_busking` |
| `nexus_coffee_machine` | `images/locations/nexus_coffee_machine.png` | bg | yes (`martha_neutral` shown on top) | Nexus Tower coffee area | any | Martha — work outfit | `scene_martha_office_coffee` |
| `nora_bad_day_cheap` | `images/scenes/nora_bad_day/nora_bad_day_cheap.png` | CG | no (establishing shot; scene transitions to `home_bg()` afterward) | player apartment tier 1 | evening | Nora — arriving | `scene_nora_bad_day` |
| `nora_bad_day_good` | `images/scenes/nora_bad_day/nora_bad_day_good.png` | CG | no (establishing shot) | player apartment tier 2 | evening | Nora — arriving | `scene_nora_bad_day` |
| `nora_bad_day_rich` | `images/scenes/nora_bad_day/nora_bad_day_rich.png` | CG | no (establishing shot) | player apartment tier 3 | evening | Nora — arriving | `scene_nora_bad_day` |
| `cg_martha_gesture` | `images/scenes/martha_corridor_gesture/cg_martha_gesture.png` | CG | yes (`martha_neutral` shown before CG) | Nexus hallway | day (9–18) | Martha — work outfit | `scene_martha_corridor_gesture` |
| `cg_nora_hug_school` | `images/scenes/nora_hug_school/cg_nora_hug.png` | CG | no (`nora_cafe_normal` hidden before CG via `hide`) | café | any | Nora — café work outfit | `scene_nora_hug_school` |
| `cg_eli_deploy_hug` | `images/scenes/eli_deploy_hug/cg_eli_hug.png` | CG | yes (`eli_normal` shown before CG; `hide eli_normal` after) | The Hub | evening (hour ≥ 19) | Eli — normal | `scene_eli_deploy_hug` |
| `cg_eli_hardware` | `images/scenes/programming_kit_eli/cg_eli_hardware.png` | CG | yes (`eli_normal` shown before CG) | The Hub | evening (hour ≥ 17) | Eli — normal | `scene_programming_kit_eli` |
| `cg_eli_zoe_collab` | `images/scenes/eli_meets_zoe/cg_eli_zoe.png` | CG | yes (`eli_normal` + `zoe_street_neutral` shown before CG) | The Hub | any | Eli + Zoe | `scene_eli_meets_zoe` |
| `cg_lena_shoulder` | `images/scenes/lena_shoulder_gesture/cg_lena_shoulder.png` | CG | yes (`drlena_normal` shown before CG; `hide drlena_normal` after) | hospital | any | Lena — scrubs | `scene_lena_shoulder_gesture` |
| `cg_nora_kai` | `images/scenes/nora_kai_crossover/cg_nora_kai.png` | CG | no (both sprites remain from before; `scene` command replaces bg+sprites) | café | any | Nora (café) + Kai (normal) | `scene_nora_kai_crossover` |
| `lena_dinner_good` | `images/scenes/kitchen_lena_extended/lena_dinner_good.png` | CG | yes (`drlena_normal` shown on top) | player apartment tier 2 | evening | Lena — scrubs | `scene_kitchen_lena_extended` |
| `lena_dinner_rich` | `images/scenes/kitchen_lena_extended/lena_dinner_rich.png` | CG | yes (`drlena_normal` shown on top) | player apartment tier 3 | evening | Lena — scrubs | `scene_kitchen_lena_extended` |
| `cg_martha_gift` | `images/scenes/martha_gift_accusation/cg_martha_gift.png` | CG | yes (`martha_neutral` shown before CG) | office | 9–18 | Martha — work outfit | `scene_martha_gift_accusation` |
| `car_interior_night` | `images/locations/car_interior_night.png` | bg | no (establishing/neutral shot) | car interior | night | none visible | `scene_car_marcus_drive` |
| `car_marcus_night` | `images/scenes/car_marcus_drive/car_marcus_night.png` | CG | **FORBIDDEN** — code comment: "do not add sprite_r on top of car_marcus_night" | car passenger seat | night | Marcus — in car | `scene_car_marcus_drive` |
| `car_interior_pov` | `images/scenes/car_marcus_drive/car_interior_pov.png` | bg-pov | no — code comment: "pov IS the camera" | car interior — player POV | night | none | `scene_car_marcus_drive` |
| `cg_zoe_almost` | `images/scenes/zoe_spontaneous/cg_zoe_almost.png` | CG | no (`zoe_street_neutral` hidden before CG is shown) | nightclub | night (hour ≥ 21) | Zoe — street outfit | `scene_zoe_spontaneous` |
| `hospital_break_room_day` | `images/locations/hospital_break_room_day.png` | bg | yes | hospital break room | day | none directly | **no expansion scene uses this asset** — likely registered in error or reserved |
| `parkday_rain` | `images/locations/parkday_rain.png` | bg | yes (`zoe_street_neutral` shown on top) | park (rain shelter) | day | Zoe — street outfit | `scene_zoe_rain_shelter` |
| `hospital_break_room` | `images/locations/hospital_break_room.png` | bg | yes (`drlena_normal` shown on top) | hospital break room | any | Lena — scrubs | `scene_lena_hospital_break_room` |

> **Note:** `hospital_break_room` is registered at `images.rpy` line 73 (outside the expansion section). `hospital_break_room_day` (line 342, inside the expansion section) is not referenced by any expansion scene.
>
> **Note:** `nora_casual_normal` (registered at line 247, standard sprite section) is used conditionally in `scene_nora_bad_day` via `renpy.loadable("images/characters/nora/nora_casual_normal.png")`. It is not in the expansion asset section but is required by the scene.

---

## Section 5 — Fallback Inventory

### Fallbacks that exist

| Scene ID | What the fallback is | When it triggers |
|---|---|---|
| `scene_nora_bad_day` | No sprite shown at all | When `images/characters/nora/nora_casual_normal.png` fails `renpy.loadable()` check (both the show and hide are gated) |
| `scene_kitchen_lena_extended` | `home_bg()` used as scene background (no CG image) | When `apartment_tier == 1`; `_lena_ext_cg` evaluates to `None` and the `if _lena_ext_cg:` branch is skipped |
| `scene_car_marcus_drive` | Returns to `car_interior_night` after the CG choice | Structural — always happens after each menu branch; not an error fallback |
| `scene_marcus_missed_commitment` | Falls back to `parkday` bg string | `_mc_bg` is `"bar"` only if `current_loc == "location_bar"`, otherwise the string `"parkday"` is used — works at any other location, not just the park |

### Scenes with no fallback (will silently fail or wait)

| Scene ID | What happens if conditions never met | Recommended action |
|---|---|---|
| `scene_nora_feels_ignored` | Waits indefinitely — `nora_ignored_pending` stays True until the player visits the café | None required; expected behaviour |
| `scene_wardrobe_martha` | Waits indefinitely for the next office visit with conditions met | None required |
| `scene_guitar_zoe_busking` | Option never appears in the menu if it's not Thu/Fri 14–17 — player cannot trigger it outside that window | None required; expected window-gating |
| `scene_lena_hospital_break_room` | Option hidden outside 12–14 each day | None required |
| `scene_martha_office_coffee` | Waits indefinitely for next early-morning office visit | None required |
| `scene_martha_corridor_gesture` | Waits indefinitely — `martha_corridor_pending` stays True until office visit during 9–18 | None required |
| `scene_nora_hug_school` | Waits indefinitely — `nora_hug_school_pending` stays True; scene never fires if player avoids café | None required |
| `scene_eli_deploy_hug` | Waits indefinitely at The Hub each evening — fires on next visit with `hour >= 19` | None required |
| `scene_lena_shoulder_gesture` | **Hard prerequisite:** `worn_out()` must be True at the start of any day after conditions are met. If the player always maintains energy ≥ 30 and hunger ≥ 25, `lena_shoulder_pending` is never set. The scene can be permanently blocked. | Consider whether the `worn_out()` gate on the trigger (not the staging) is intentional |
| `scene_nora_kai_crossover` | Expires after 14 days: `nora_kai_pending = False` and `nora_kai_pending_day = -1` in `new_day()`. If thresholds remain met, `new_day()` will set pending again on the next evaluation pass — so expiry resets and retries on the same conditions. | None required; behaviour is documented |
| `scene_eli_meets_zoe` | Waits indefinitely; player must manually choose the hub menu option | None required |
| `scene_car_marcus_drive` | Waits indefinitely until `hour >= 22` at the bar with all conditions met | None required |
| `scene_martha_gift_accusation` | Waits indefinitely for an office visit during 9–18 | None required |
| `scene_programming_kit_eli` | Waits for next hub visit at `hour >= 17` | None required |
| `scene_zoe_rain_shelter` | Waits for next Thu/Fri 14–18 park visit; fires immediately then | None required |
| `scene_zoe_spontaneous` | Waits indefinitely at nightclub with `hour >= 21` | None required |
| `scene_kitchen_lena_extended` | **Staging hook not found in listed files.** If the hook is absent entirely, the scene never fires regardless of `kitchen_lena_extended_done`. | Verify staging hook exists in `home_scenes.rpy`; if not, implement one |

---

## Section 6 — Defaults and Flags Registry

All from `data.rpy` lines 211–251 (`# ── Gameplay expansion defaults ──`).

| Variable name | Type | Default value | Role | Reset policy |
|---|---|---|---|---|
| `nora_ignored_done` | bool | `False` | done flag | permanent — never cleared once set |
| `nora_ignored_pending` | bool | `False` | pending flag | cleared on scene fire |
| `nora_ignored_response` | str | `""` | pending data (response branch) | never explicitly cleared — persists after scene fires; harmless since `nora_ignored_done` prevents re-trigger |
| `nora_bad_day_done` | bool | `False` | done flag | permanent |
| `nora_bad_day_pending` | bool | `False` | pending flag | cleared on scene fire or player decline |
| `nora_touched_arm` | bool | `False` | done flag (relationship milestone) | permanent |
| `marcus_missed_done` | bool | `False` | done flag / re-arm gate | reset to `False` by `mark_commitment_missed()` when a new miss creates a new pending dict; effectively allows multiple firings |
| `marcus_missed_pending` | None/dict | `None` | pending data | cleared on scene fire |
| `martha_wardrobe_done` | bool | `False` | done flag | permanent |
| `zoe_park_guitar_done` | bool | `False` | done flag | permanent |
| `zoe_rain_done` | bool | `False` | done flag | permanent |
| `zoe_moment_deflected_done` | bool | `False` | done flag | permanent |
| `zoe_moment_deflected_pending` | bool | `False` | pending flag | cleared on scene fire |
| `zoe_moment_deflected_pending_day` | int | `-1` | day tracker | set when pending created; never used in any expiry check (no expiry for this scene) |
| `martha_corridor_done` | bool | `False` | done flag | permanent |
| `martha_corridor_pending` | bool | `False` | pending flag | cleared on scene fire |
| `martha_corridor_pending_day` | int | `-1` | day tracker | set when pending created; not used in expiry checks |
| `nora_hug_school_done` | bool | `False` | done flag | permanent |
| `nora_hug_school_pending` | bool | `False` | pending flag | cleared on scene fire |
| `nora_hug_school_pending_day` | int | `-1` | day tracker | set when pending created; not used in expiry checks |
| `eli_deploy_hug_done` | bool | `False` | done flag | permanent |
| `eli_deploy_pending` | bool | `False` | pending flag | cleared on scene fire |
| `eli_deploy_pending_day` | int | `-1` | day tracker | set when pending created; not used in expiry checks |
| `lena_shoulder_done` | bool | `False` | done flag | permanent |
| `lena_shoulder_pending` | bool | `False` | pending flag | cleared on scene fire |
| `lena_shoulder_pending_day` | int | `-1` | day tracker | set when pending created; not used in expiry checks |
| `nora_kai_crossover_done` | bool | `False` | done flag | permanent |
| `nora_kai_pending` | bool | `False` | pending flag | reset on 14d expiry or scene fire |
| `eli_meets_zoe_done` | bool | `False` | done flag | permanent |
| `car_marcus_drive_done` | bool | `False` | done flag | permanent |
| `martha_gift_accusation_done` | bool | `False` | done flag | permanent |
| `martha_gift_scene_pending` | None/dict | `None` | pending data | cleared on scene fire; `variant` field mutated in-place (via copy) after 4 days |
| `programming_kit_eli_done` | bool | `False` | done flag | permanent |
| `nora_last_seen_day` | int | `0` | day tracker | updated on every `location_cafe` entry (`nora_last_seen_day = day`) |
| `nora_kai_pending_day` | int | `-1` | expiry tracker | set when `nora_kai_pending = True`; reset to `-1` on expiry or scene fire |
| `kitchen_lena_extended_done` | bool | `False` | done flag | permanent |
| `lena_break_room_done` | bool | `False` | done flag | permanent |
| `martha_coffee_machine_done` | bool | `False` | done flag | permanent |
| `gift_log` | list | `[]` | counter (gift history) | permanent — appended only, never cleared |
| `major_scene_last_day` | int | `-1` | day tracker (anti-double-major) | set to `day` at the start of each major scene; reset naturally by day changing |

> **Note on `_pending_day` variables:** `martha_corridor_pending_day`, `nora_hug_school_pending_day`, `eli_deploy_pending_day`, `lena_shoulder_pending_day`, and `zoe_moment_deflected_pending_day` are set when their respective pending flags are enabled, but none of these are used in any expiry check. They exist for future use or diagnostic purposes only.

---

## Section 7 — Test Checklist

```markdown
### Staging and location gating

- [ ] Trigger in wrong location sets pending flag but does NOT fire scene
      (e.g. marcus_missed_pending set → visit nightclub → confirm scene does not play)
- [ ] Entering canonical location with correct time window fires scene immediately on entry
- [ ] Wrong time window blocks staging even with pending=True
      (e.g. eli_deploy_pending=True → visit hub at hour 10 → scene does NOT fire)
- [ ] Active commitment takes priority over pending conflict scene at location entry
      (nora_bad_day commitment available at home overrides any other home logic)
- [ ] scene_car_marcus_drive does NOT fire at bar when hour = 21 (needs hour >= 22)
- [ ] scene_zoe_spontaneous does NOT fire at nightclub when hour = 20 (needs hour >= 21)
- [ ] scene_martha_corridor_gesture does NOT fire at office when hour = 18 (needs hour < 18)
- [ ] scene_martha_gift_accusation does NOT fire at office when hour = 8 (needs hour >= 9)

### Major scene gate (major_scene_last_day)

- [ ] major_scene_last_day prevents two major scenes on the same day
      (fire one major scene → visit second major scene location same day → confirm NOT fired)
- [ ] major_scene_last_day resets correctly the next day (second major scene fires day+1)

### Pending flag lifecycle

- [ ] Scene does NOT fire a second time after done flag is set
      (nora_hug_school_done = True → visit café → no scene)
- [ ] nora_kai_pending clears after 14 in-game days without firing
      (set pending, advance 15 days without visiting café, confirm nora_kai_pending = False)
- [ ] nora_kai_pending is reset by new_day() on the same evaluation pass that created it only when conditions still met
- [ ] save/load cycle preserves pending dict content
      (marcus_missed_pending dict survives a save+reload — all fields intact)
- [ ] rollback after choice does not re-fire the scene (done flag already set before rollback window)
- [ ] phone_reply_nora_bad_day_decline sets nora_bad_day_pending = False without setting nora_bad_day_done

### Dict field interpolation in dialogue

- [ ] marcus_missed_pending["trigger_day"] produces correct day-elapsed calculation in scene
      (days shown as "0-3" triggers "You blew me off." branch)
- [ ] marcus_missed_pending["title"] appears correctly in dialogue (delayed variant: "We still haven't talked about [title]")
- [ ] marcus_missed_pending["location"] field is stored but confirm it is not used in current dialogue (field present, no interpolation in code — flag if dialogue references it)
- [ ] martha_gift_scene_pending["gift_name"] appears in context of martha_gift_accusation dialogue
      (confirm "The gifts. Why?" line — note: gift_name is stored but the scene dialogue does not actually interpolate it; flag if expected)

### Variant and expiry promotion

- [ ] martha_gift_scene_pending["variant"] promotes to "delayed" after 4 in-game days
      (give 2+ gifts → wait 4 days → verify dict["variant"] == "delayed")
- [ ] martha_gift_scene_pending["variant"] == "immediate" at day 3 (not yet promoted)
- [ ] martha_gift_scene_pending is None after scene_martha_gift_accusation fires

### Asset and sprite correctness

- [ ] nora_bad_day selects nora_bad_day_cheap when apartment_tier == 1
- [ ] nora_bad_day selects nora_bad_day_good when apartment_tier == 2
- [ ] nora_bad_day selects nora_bad_day_rich when apartment_tier == 3
- [ ] nora_bad_day does NOT show nora_cafe_normal at any point (she is off-duty)
- [ ] nora_bad_day: nora_casual_normal shows when loadable; no sprite when not loadable
- [ ] car_marcus_night CG has no sprite overlay (marcus_casual_normal or marcus_bar_normal must NOT appear on top)
- [ ] car_interior_pov has no sprite overlay (POV image — no NPC portrait shown)
- [ ] cg_zoe_almost is shown without zoe_street_neutral on top (sprite is hidden before the CG)
- [ ] cg_nora_hug_school is shown without nora_cafe_normal on top (sprite hidden via hide before scene command)

### Self-staging scenes (no pending flag)

- [ ] scene_wardrobe_martha fires on the first office visit after wardrobe_tier reaches 2 with martha_affection >= 25
- [ ] scene_wardrobe_martha does NOT fire a second time (martha_wardrobe_done = True blocks it)
- [ ] scene_martha_office_coffee only fires before hour 10; does NOT fire at 10:00 or later
- [ ] scene_guitar_zoe_busking menu option appears Thu/Fri at hour 15 with conditions met
- [ ] scene_guitar_zoe_busking menu option does NOT appear on Wednesday at hour 15
- [ ] scene_guitar_zoe_busking menu option does NOT appear on Thu at hour 18 (needs hour <= 17)
- [ ] scene_zoe_rain_shelter fires Thu at hour 16 with zoe_affection >= 15 and zoe_met
- [ ] scene_zoe_rain_shelter does NOT fire at hour 19 even on Thu/Fri (needs hour <= 18)
- [ ] scene_lena_hospital_break_room option appears at hour 12 but NOT at hour 15
- [ ] scene_eli_meets_zoe is only available when own_programming_kit is True

### Prerequisite chain correctness

- [ ] scene_nora_hug_school: confirm nora_school_revealed is True before testing (topic arc must be complete)
- [ ] scene_eli_deploy_hug: confirm scene_programming_kit_eli must fire first (programming_kit_eli_done gate)
- [ ] scene_lena_shoulder_gesture: confirm scene_lena_hospital_break_room must fire first (lena_break_room_done gate)
- [ ] scene_lena_shoulder_gesture: confirm worn_out() == True at new_day() time (energy < 30 or hunger < 25)
- [ ] scene_zoe_spontaneous: confirm zoe_beach_night_done is True (beach night scene prerequisite)
- [ ] scene_nora_feels_ignored: confirm nora_closing_done is True (closing scene prerequisite)

### kitchen_lena_extended (staging unknown)

- [ ] Manually locate staging hook for scene_kitchen_lena_extended in home_scenes.rpy and verify it calls the label
- [ ] Confirm kitchen_lena_extended_done is set to True after scene fires and blocks re-trigger
- [ ] Confirm lena_dinner_good is shown at apartment_tier 2; lena_dinner_rich at tier 3; home_bg() at tier 1
```

---

## End of Report

### Scene Status Summary

| Scene | Status |
|---|---|
| `scene_nora_feels_ignored` | Implemented |
| `scene_marcus_missed_commitment` | Implemented |
| `scene_wardrobe_martha` | Implemented |
| `scene_guitar_zoe_busking` | Implemented |
| `scene_lena_hospital_break_room` | Implemented |
| `scene_martha_office_coffee` | Implemented |
| `scene_nora_bad_day` | Implemented |
| `scene_kitchen_lena_extended` | Partially implemented — scene label and assets exist; staging hook not found in any listed file |
| `scene_martha_corridor_gesture` | Implemented |
| `scene_nora_hug_school` | Implemented |
| `scene_eli_deploy_hug` | Implemented |
| `scene_lena_shoulder_gesture` | Needs manual verification — `worn_out()` gate on trigger can permanently block scene if player never becomes worn out after `lena_break_room_done` |
| `scene_nora_kai_crossover` | Implemented |
| `scene_eli_meets_zoe` | Implemented |
| `scene_car_marcus_drive` | Implemented |
| `scene_martha_gift_accusation` | Implemented |
| `scene_programming_kit_eli` | Implemented |
| `scene_zoe_rain_shelter` | Implemented |
| `scene_zoe_spontaneous` | Implemented |

**Additional findings:**

- `hospital_break_room_day` (registered in the expansion images section) is not referenced by any expansion scene. `scene_lena_hospital_break_room` uses `hospital_break_room` (a separate registration). The `_day` asset is either unused or reserved.
- The file header in `gameplay_expansion_scenes.rpy` claims 17 scenes; 19 label blocks exist. The count is wrong by 2.
- `nora_ignored_response` is never explicitly cleared after `scene_nora_feels_ignored` fires. This is safe because `nora_ignored_done` prevents re-triggering, but the stale string persists in save data.
- The `_pending_day` companion variables for `martha_corridor_pending`, `nora_hug_school_pending`, `eli_deploy_pending`, `lena_shoulder_pending`, and `zoe_moment_deflected_pending` are written but never read in any expiry or validation check. They are informational only.
