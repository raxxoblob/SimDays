# Relationship Scene Pacing Audit
_Generated from code inspection — not from memory_
_Source files read: data.rpy, interact.rpy, gameplay_expansion_scenes.rpy, home_scenes.rpy, locations.rpy, phone_messages.rpy, phone_actionable.rpy, careers.rpy, arcs.rpy, corporate_work.rpy, group_scenes.rpy_

---

## Fixes Applied (post-audit)
- FIX 1: Marcus basketball commitment added — `scene_marcus_missed_commitment` now reachable. Invite fires in `location_bar` once `marcus_sports_1` arc is done and aff≥25; acceptance creates commitment with `npc_id="marcus"`.
- FIX 2: Metal detector added to `location_shop_electronics` at $120 — `eli_find_scene` now reachable.
- FIX 3: `hospital_hard_case_pending` reworked — no longer gated on `job_performance < 70`. Now a 25% random chance per shift once `lena_break_room_done`, `hosp_shifts≥10`, `job_rank≥1`. Performance branches debrief dialogue only.
- FIX 4: Zoe sandbeach schedule extended to `(WKD, 19–24)` in `interact.rpy`; Sam gym scene trigger changed from `hour≥18` to `10≤hour<14` to match Sam's actual schedule.
- FIX 5: Major scene mutex verified — pending flags are only cleared inside scene labels, never on the mutex check. Test group 14 added to `test_gameplay_polish.rpy`.
- FIX 6: `nora_last_seen_day` now updated in `nora_greet` (fires on actual Talk-to-Nora interaction at any location) rather than on unconditional `location_cafe` entry.
- Content Pack 2 (Groups 15–20): Caroline off-work, Natalie humanisation, Kai breakthrough, Elle Portugal payoff, Sam×Marcus crossover, and Eli home dinner implemented. Test count raised from 14 groups to 20 groups (Groups 15–20 added to `test_gameplay_polish.rpy`).

---

## Summary

- **`scene_marcus_missed_commitment` is dead code.** No code path ever schedules a commitment with `npc_id == "marcus"`, so `marcus_missed_pending` can never be set. The scene exists, has art, but is unreachable in the current build.
- **`eli_find_scene` is permanently inaccessible.** `own_metal_detector` has no shop or acquisition path — it is declared in `data.rpy` but never set `True` by any purchasable item. The entire beach-detector arc with Eli cannot fire.
- **`lena_shoulder_gesture` (MAJOR) is unreliable for all players.** `hospital_hard_case_pending` IS set in the code (locations.rpy:1635-1638) — a 25% random roll per qualifying shift. Prerequisites: `lena_break_room_done`, `hosp_shifts >= 10`, `job_rank >= 1` (promotion required — low performers cannot reach this at all). `job_performance >= 70` only changes flavor dialogue, not scene availability. The scene is reachable, but with no pity trigger, a player meeting all prerequisites may work many qualifying shifts without the 25% roll succeeding.
- **Two scene triggers fire outside their NPC's schedule.** `zoe_beach_night_scene` fires at `location_sandbeach` past hour 20, but Zoe's schedule ends at 18 on weekends. `sam_gym_scene` fires at the gym floor past hour 18, but Sam's gym schedule ends at 14 on all days. NPCs appear in scenes with no schedule justification.
- **Six MAJOR scenes share one `major_scene_last_day` mutex with no retry guarantee.** `nora_hug_school`, `martha_corridor_gesture`, `eli_deploy_hug`, `lena_shoulder_gesture`, `car_marcus_drive`, and `zoe_spontaneous` all set this day-lock. Four of them cluster in the same day 15–30 window for any focused playthrough. The blocked scene silently skips with no queuing — it simply fails the check on that visit and must wait for the next visit on a different day.

---

## Stat Gain Rate Assumptions (for day estimates)

All day estimates assume:
- **Visit frequency:** 1 NPC visit per day for the target NPC; player divides attention across 4–5 NPCs.
- **Talk (liked topic):** +2 aff per session (do_talk delta for liked = 2).
- **Talk (neutral):** +0 aff.
- **Date:** +6 aff, +3 trust (immediate, 3h, available at aff ≥ 30).
- **Hug (first time):** +3 aff, +1 trust. Cooldown 2–7 days depending on NPC.
- **Gift (first of week, liked type):** +5 aff; second gift same week: +2 aff; third: +0.
- **Topic arcs:** +1–4 aff or trust per arc stage completion.
- **Money pace:** starting $500; café shifts ($60/shift, 4h); rough net savings $80–90/day if working two shifts.
- **"Likely natural" definition:** player visits this NPC every 2–3 days while also seeing 3–4 others.
- **Career NPCs** (Lena, Martha, Caroline, Natalie, Kai): first met through the relevant job; assume player starts that career in week 1–2.

---

## Per-NPC Scene Chronology

### NORA

Schedule: Café Mon–Fri 07–16, Bar Tue/Fri 17–22, Café Sat–Sun 10–14.
World NPC (no gate).

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| `cafe_first_visit` | everyday (first meet) | first visit to café | 1 | 1 | location_cafe | café | No | No |
| `arc_nora_ambition_1` | everyday (arc) | Nora met | 2 | 3 | location_cafe (talk) | café | No | No |
| `arc_nora_food_1` | everyday (arc) | Nora met | 2 | 3 | location_cafe (talk) | café | No | No |
| `arc_nora_food_2` | everyday (arc) | aff≥12 + food_1 done | 5 | 8 | location_cafe (talk) | café | No | No |
| `arc_nora_ambition_2` | everyday (arc) | trust≥20 + ambition_1 done | 8 | 12 | location_cafe (talk) | café | No | No |
| `nora_closing_scene` | breakthrough | aff≥40 + hour≥19 + not done | 12 | 18 | location_cafe | café night | Yes (7 CG) | No |
| `phone_nora_closing_scene` | commitment | trust≥20 + ≥5 café shifts + closing invite queued + accepted | 14 | 22 | location_cafe | café night | No | No |
| `nora_rent_scene` | everyday | trust≥30 + aff≥30 + nora_closing_done | 16 | 24 | location_cafe | café night | No | No |
| `home_nora_coffee_scene` | item-enabled | own_coffee_machine + aff≥30 + trust≥20 + nora_met + accepted invite | 15 | 25 | location_home | home | Yes | No |
| `scene_nora_bad_day` | breakthrough | aff≥30 + trust≥20 + closing_done + nora in contacts + worn_out() | 18 | 30 | location_home | home | Yes (tier CG) | No |
| `scene_nora_feels_ignored` | conflict | aff≥30 + trust≥20 + closing_done + contacts + 8 days since café visit | 22 | variable | location_cafe | café | Yes | No |
| `scene_nora_hug_school` | breakthrough | nora_school_revealed + aff≥40 + trust≥35 | 18 | 28 | location_cafe | café | Planned (noted "not yet generated") | **YES** |
| `home_dinner_scene_nora` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 12 | 20 | location_home | home | Yes (shared CG) | No |
| `scene_nora_kai_crossover` | crossover | nora_aff≥30 + kai_aff≥20 + both met + pending set by new_day() | 20 | 35 | location_cafe | café | Yes | No |

**Dependency tree:**
```
cafe_first_visit (day ~1)
  └─ arc_nora_ambition_1 (day ~2, first talk on ambition)
       └─ arc_nora_ambition_2 (day ~8, trust≥20)
            └─ nora_school_revealed flag set
                 └─ scene_nora_hug_school (day ~18, aff≥40 + trust≥35) [MAJOR]
  └─ arc_nora_food_1 (day ~2)
       └─ arc_nora_food_2 (day ~5, aff≥12)
  └─ nora_closing_scene (day ~12, aff≥40 + hour≥19)
       └─ nora_rent_scene (day ~16, trust≥30 + aff≥30)
       └─ scene_nora_feels_ignored (day ~22+, 8-day café gap needed)
       └─ scene_nora_bad_day (day ~18+, worn_out() via hunger<25)
  └─ home_nora_coffee_scene (day ~15, own_coffee_machine + invite)
       └─ home_coffee_calibrated = True (enables +energy bonus at home)
  └─ scene_nora_kai_crossover (day ~20+, kai relationship also required)
```

**Flags:**
- `nora_school_revealed` is the single gate before `scene_nora_hug_school`. It is only set in `arc_nora_ambition_2`. If the player never picks "ambition" as a topic with Nora, the entire hug_school chain is permanently blocked.
- `nora_last_seen_day` is only updated at `location_cafe` entry — bar visits to Nora (her Tue/Fri 17–22 schedule) do **not** reset the 8-day timer for `scene_nora_feels_ignored`. This is an inconsistency: `npc_last_seen["nora"]` is updated by every npc_interact call, but the ignore scene uses the café-specific `nora_last_seen_day` variable.
- `worn_out()` in new_day() — the check runs AFTER energy is restored to 95–100. So `worn_out()` via energy (< 30) can never trigger for `nora_bad_day`. The scene can only arm via `need_hunger < 25`, which requires the player to end the previous day with hunger < 25 + lose another 5–15 on wakeup. Narrow but possible; not impossible.
- `nora_hug_school` uses `do_hug("nora")` which has its own cooldown (2 days) and aff/trust minimums (20/15). Since the scene itself calls `do_hug`, the hug will always succeed at the scene's trigger thresholds (aff≥40 far exceeds min_aff=20).

**Issues:**
- `scene_nora_hug_school` (MAJOR) competes with all other major scenes on the same day.
- The CG for `scene_nora_hug_school` is explicitly noted as "not yet generated" in a code comment — if triggered, it falls back to café background only.

---

### MARCUS

Schedule: Park any day 06–10, Bar any day 17–24, Nightclub Sat–Sun 23–27.
World NPC (no gate).

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Marcus greet / first meet | everyday | world NPC, cold approach | 1 | 1 | location_park / location_bar | park/bar | No | No |
| `arc_marcus_sports_1` | everyday (arc) | Marcus met | 2 | 3 | any (talk) | — | No | No |
| `arc_marcus_sports_2` | everyday (arc) | aff≥15 + sports_1 done | 7 | 12 | any (talk) | — | No | No |
| `arc_marcus_food_1` | everyday (arc) | Marcus met | 2 | 4 | any (talk) | — | No | No |
| `arc_marcus_food_2` | everyday (arc) | trust≥15 + food_1 done | 8 | 14 | any (talk) | — | No | No |
| `scene_marcus_missed_commitment` | conflict | **DEAD CODE — marcus_missed_pending never set** | — | — | location_bar / location_park | bar/park | Yes | No |
| `scene_car_marcus_drive` | breakthrough | car_tier≥1 + aff≥30 + trust≥20 + bar + hour≥22 | 18 | 35 | location_bar | car interior | Yes (3 CG) | **YES** |
| `home_dinner_scene_marcus` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 12 | 22 | location_home | home | Yes (shared CG) | No |

**Dependency tree:**
```
Marcus met (day ~1)
  └─ arc_marcus_sports_1 (day ~2, no req)
       └─ arc_marcus_sports_2 (day ~7, aff≥15) — reveals basketball miss
  └─ arc_marcus_food_1 (day ~2, no req)
       └─ arc_marcus_food_2 (day ~8, trust≥15) — reveals mother's recipe
  └─ scene_car_marcus_drive (day ~18 earliest, requires car + stats + late bar)  [MAJOR]
  └─ scene_marcus_missed_commitment (DEAD — no Marcus commitment creation path)
```

**Critical issues:**
- **`scene_marcus_missed_commitment` is dead code.** `mark_commitment_missed()` sets `marcus_missed_pending` when a commitment with `npc_id == "marcus"` is missed. However, `add_commitment()` is never called with `"marcus"` in `phone_actionable.rpy` or anywhere else. The `npc_date()` flow is immediate (not a future commitment). The scene, its CG asset (`cg_marcus_missed`), and all its pending-dict infrastructure exist but cannot be reached.
- Marcus has no conflict scene that can actually fire. The car drive is his only major moment, locked behind significant financial investment ($1,500 car).
- `marcus_chili` flag is set in `script.rpy` line 49 (introductory context) but is never read by any subsequent scene or condition.

---

### ZOE

Schedule: Beach Sat–Sun 12–18, Park Thu–Fri 14–18, Nightclub Fri–Sun 21–27.
World NPC (no gate).

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| `beach_meet_zoe` | everyday (first meet) | first beach visit daytime | 1 (Sat/Sun) or day 6 | 6 | location_beach | beach | Yes (7 CG) | No |
| `arc_zoe_art_1` | everyday (arc) | Zoe met | 7 | 9 | any (talk) | — | No | No |
| `arc_zoe_art_2` | everyday (arc) | aff≥10 + art_1 done | 9 | 13 | any (talk) | — | No | No |
| `arc_zoe_art_3` | everyday (arc) | trust≥15 + art_2 done | 12 | 18 | any (talk) | — | No | No |
| `arc_zoe_art_4` | everyday (arc) | aff≥30 + art_3 done | 16 | 25 | any (talk) | — | No | No |
| `arc_zoe_music_1` | everyday (arc) | Zoe met | 7 | 9 | any (talk) | — | No | No |
| `arc_zoe_music_2` | everyday (arc) | aff≥15 + music_1 done | 10 | 16 | any (talk) | — | No | No |
| `scene_zoe_rain_shelter` | everyday | aff≥15 + park Thu/Fri 14–18 + zoe_met | 11 | 16 | location_park | park (rain) | No explicit CG | No |
| `home_zoe_guitar_scene` | item-enabled | own_guitar + skill_music≥1 + aff≥25 + zoe_met + invite accepted | 16 | 25 | location_home | home | Yes | No |
| `scene_guitar_zoe_busking` | item-enabled | own_guitar + skill_music≥3 + aff≥30 + park Thu/Fri 14–17 | 25 | 35 | location_park | park | Yes | No |
| `zoe_beach_night_scene` | breakthrough | aff≥40 + location_sandbeach + hour≥20 | 20 | 30 | location_sandbeach | beach night | Yes (3 CG) | No |
| `scene_zoe_spontaneous` | breakthrough | aff≥45 + trust≥35 + zoe_beach_night_done + nightclub + hour≥21 | 25 | 38 | location_nightclub | nightclub | Yes (cg_zoe_almost) | **YES** |
| `scene_eli_meets_zoe` | crossover | own_programming_kit + eli_aff≥35 + zoe_aff≥30 + both met | 22 | 35 | location_hub | hub | Yes | No |
| `home_dinner_scene_zoe` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 12 | 20 | location_home | home | Yes (shared CG) | No |

**Dependency tree:**
```
beach_meet_zoe (day ~6, first weekend)
  └─ arc_zoe_art_1 (day ~7, no req)
       └─ arc_zoe_art_2 (day ~9, aff≥10)
            └─ arc_zoe_art_3 (day ~12, trust≥15) — grant rejection
                 └─ arc_zoe_art_4 (day ~16, aff≥30) — exhibition invite; sets zoe_exhibition_invited
  └─ arc_zoe_music_1 → arc_zoe_music_2 (day ~10–16)
  └─ scene_zoe_rain_shelter (day ~11, aff≥15 + Thu/Fri park)
  └─ home_zoe_guitar_scene (day ~16, item-enabled)
       └─ scene_guitar_zoe_busking (day ~25, skill_music≥3 required)
  └─ zoe_beach_night_scene (day ~20, aff≥40 + sandbeach at night)  ← schedule mismatch
       └─ scene_zoe_spontaneous (day ~25, aff≥45 + trust≥35 + nightclub) [MAJOR]
  └─ scene_eli_meets_zoe (day ~22, crossover via hub)
```

**Issues:**
- **Schedule mismatch on `zoe_beach_night_scene`.** Zoe's schedule has `(WKD, (12, 18), "location_beach")`. The scene fires at `location_sandbeach` when `hour≥20`. Zoe is not scheduled at that location after hour 18. `npc_here("zoe")` returns False at sandbeach past 18, but the trigger is a direct `jump` (not gated on `npc_talkable`). Zoe therefore appears in the scene without being present per schedule. This can be fixed by either extending Zoe's schedule to cover `location_sandbeach` at evening hours, or by gating the scene on `npc_here("zoe")`.
- `zoe_beach_night_done` is a hard gate for `scene_zoe_spontaneous`. A player who never visits sandbeach at night (e.g., prefers nightclub visits directly) will never reach Zoe's major moment even with aff≥45 and trust≥35.
- `zoe_exhibition_invited` is set by `arc_zoe_art_4` but there is no follow-up scene honouring the invitation — the art arc completes without a gallery CG or payoff scene.
- `own_sketchbook` is declared in `data.rpy` as "sketch at home for +art skill" but is never referenced in any location or scene — it is unimplemented infrastructure.

---

### ELI

Schedule: Library daily 12–20, Bar Tue/Wed/Thu 20–23.
World NPC (no gate). **Note:** Eli is also introduced through the IT career (`it_first_day`), but the world flag `eli_met` is separate from that path.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Eli greet / first meet | everyday | world NPC, cold approach at library | 1 | 3 | location_library | library | No | No |
| `arc_eli_work_1` | everyday (arc) | Eli met | 2 | 4 | any (talk) | — | No | No |
| `arc_eli_work_2` | everyday (arc) | aff≥10 + work_1 done | 6 | 10 | any (talk) | — | No | No |
| `home_eli_side_project_scene` | item-enabled | own_programming_kit + aff≥25 + trust≥20 + invite accepted | 15 | 25 | location_home | home | Yes | No |
| `phone_eli_debug_scene` | commitment | IT career active; invite queued after shifts | 14 | 22 | location_hub | hub | No | No |
| `eli_find_scene` | item-enabled | own_metal_detector + eli_met + sandbeach | **INACCESSIBLE** | — | location_sandbeach | beach | Yes (6 CG + bonus) | No |
| `scene_programming_kit_eli` | item-enabled | own_programming_kit + aff≥30 + trust≥25 + hub + hour≥17 | 18 | 28 | location_hub | hub | Yes | No |
| `scene_eli_deploy_hug` | breakthrough | programming_kit_eli_done → pending + hub + hour≥19 | 20 | 30 | location_hub | hub | Yes | **YES** |
| `scene_eli_meets_zoe` | crossover | own_programming_kit + eli_aff≥35 + zoe_aff≥30 + both met | 22 | 35 | location_hub | hub | Yes | No |

**Dependency tree:**
```
Eli met (day ~1–3)
  └─ arc_eli_work_1 (day ~2)
       └─ arc_eli_work_2 (day ~6, aff≥10)
  └─ home_eli_side_project_scene (day ~15, programming_kit + invite)
  └─ phone_eli_debug_scene (day ~14, IT career gate)
  └─ eli_find_scene (PERMANENTLY INACCESSIBLE — own_metal_detector has no purchase path)
  └─ scene_programming_kit_eli (day ~18, own_programming_kit + thresholds + hub evening)
       └─ scene_eli_deploy_hug (day ~20, pending arms next new_day()) [MAJOR]
  └─ scene_eli_meets_zoe (day ~22, crossover)
```

**Critical issues:**
- **`eli_find_scene` is permanently inaccessible.** `own_metal_detector` defaults to `False` and is not available in any shop (not in `location_shop_electronics`, `location_shop_gifts`, or any other purchasable menu). The scene has six CG images, a ring-find bonus branch, and meaningful trust/aff gains — all dead. This is Eli's most unique scene (item gimmick with personal dialogue) and it cannot fire.
- Eli has **no home dinner** — Eli is omitted from `home_dinner_invite_menu` even though all other major world NPCs are included. Eli can visit the player's home (side project scene) but cannot be invited for dinner.
- `scene_eli_deploy_hug` requires `scene_programming_kit_eli` to complete first. That scene gates on `own_programming_kit` ($100) + aff≥30 + trust≥25 + hub location + hour≥17. All conditions achievable by day 18–20, but the hub is open Mon–Fri daytime, and the scene requires hour≥17 (end of IT shift). Players not in the IT career still need to visit the hub in the evening, which has no location entry barrier but is not prompted.

---

### LENA

Schedule: Hospital Mon–Fri 08–16, Bar Wed/Fri 18–22.
Career NPC — met through hospital job (Clinical Assistant requires skill_med≥2, INT≥30, CHR≥15), OR promoted to Resident at which point `lena_met = True` if not already set.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| `hosp_first_day` (lena_met set) | career arc | hospital job + shift 1 | 3 | 5 | location_hospital | hospital | No explicit CG | No |
| `hosp_task_1_done` / `hosp_npc1_lena` / `hosp_npc2_lena` | career arc | shifts 3 / 5 / 7 respectively | 5 / 7 / 9 | 8 / 12 / 16 | location_hospital | hospital | No | No |
| `scene_lena_hospital_break_room` | everyday | lena_aff≥20 + trust≥15 + lena_met + hospital + hour 12–14 | 12 | 20 | location_hospital | break room | No explicit CG | No |
| `phone_lena_case_scene` | commitment | IT/hospital career; invite queued | 14 | 22 | location_hospital (Wed 14:00) | hospital | No | No |
| `lena_rooftop_scene` | breakthrough | job_rank≥1 + lena_trust≥25 + hospital shift + hour≥22 | 18 | 28 | location_hospital | rooftop | Yes (5 CG) | No |
| `home_dinner_scene_lena` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 14 | 24 | location_home | home | Yes (shared CG) | No |
| `scene_kitchen_lena_extended` | item-enabled | auto-trigger from dinner: lena_trust≥30 + own_kitchen_set | 16 | 26 | location_home | home | Yes (tier CG) | No |
| `hospital_trial_resident` | career arc | job_rank 0 + performance≥100 + can_promote() | 15 | 25 | location_hospital | hospital | No | No |
| `scene_lena_shoulder_gesture` | breakthrough | lena_break_room_done + hospital_hard_case_pending + aff≥45 + trust≥45 | 22 | 35 | location_hospital | hospital | Yes | **YES** |

**Dependency tree:**
```
Hospital career (day ~3)
  └─ hosp_first_day → npc1 → npc2 → review (days ~5–15)
       └─ lena_rooftop_scene (day ~18, rank≥1 + trust≥25 + night shift)
  └─ scene_lena_hospital_break_room (day ~12, aff≥20 + trust≥15 + break hour)
       └─ lena_break_room_done flag set
            └─ scene_lena_shoulder_gesture (day ~22+, ALSO needs hospital_hard_case_pending + high thresholds) [MAJOR]
  └─ hospital_trial_resident (day ~15)
       ← adds lena_trust+12 on pass — significant trust injection
  └─ home_dinner_scene_lena (day ~14, own_kitchen_set)
       └─ scene_kitchen_lena_extended (auto-trigger, trust≥30 + own_kitchen_set)
```

**Critical issues:**
- **`scene_lena_shoulder_gesture` gates on bad performance.** `hospital_hard_case_pending` is set only when `job_performance < 70` at the end of a hospital shift. A player performing well (performance ≥ 70 always) can never trigger Lena's MAJOR breakthrough. The scene is Lena's only physical-touch peak and her highest-trust moment — it should not be permanently blocked by competence. Recommended: add an alternate trigger (e.g., after a sufficiently hard case regardless of performance, or after a certain number of shifts at rank 1+).
- `lena_rooftop_scene` requires `hour≥22` after a hospital shift. Hospital shifts are 8h. If started at 8:00, the shift ends at 16:00 — not 22:00. This scene can only fire if the player does a second hospital visit that same evening, which is impossible because only one shift per career per day is modelled. The trigger is checked `if not lena_rooftop_done and job_rank >= 1 and lena_trust >= 25 and hour >= 22: jump lena_rooftop_scene` inside the hospital shift block. Since `spend_time(8)` from an 8:00 start brings hour to 16:00, `hour >= 22` is never met immediately post-shift. **This scene may be unreachable without unusual time manipulation.** However, if the player starts a shift very late (17:00 + 8h = 25:00 = next day trigger), that would push past midnight — but `DAY_END = 27` and `spend_time` calls `new_day()` when `hour >= 27`. So the rooftop check fires only if the shift ends between 22:00 and 27:00, meaning it must start after 14:00. Check: hospital shift can start any time `hour + 8 <= DAY_END (27)`. Starting at 14:00 ends at 22:00 — exactly the minimum. So the scene is reachable but only for players who arrive at the hospital at 14:00 or later.

---

### MARTHA

Schedule: Office Mon–Fri 09–18, Bar Thu 19–23.
Career NPC. Gate: `caroline_met` (story_gate) — player must join the corporate career and meet Caroline first. Martha becomes talkable only after `caroline_met = True`.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Martha met (via `corp_task_1`) | career arc | corporate job + shifts≥2 | 4 | 7 | location_office | office | No | No |
| `phone_martha_coffee_scene` | commitment | martha_met + invite from Caroline's area; accepted | 8 | 14 | location_cafe | café | No | No |
| `scene_martha_office_coffee` | everyday | office + hour<10 + aff≥20 + martha_met + not done | 8 | 14 | location_office | office | No | No |
| `scene_wardrobe_martha` | everyday | office + wardrobe_tier≥2 + aff≥25 + martha_met + not done | 10 | 18 | location_office | office | Yes | No |
| `scene_martha_gift_accusation` | conflict | office 09–18 + exactly 3rd gift to martha | 14 | 22 | location_office | office | Yes | No |
| `scene_martha_corridor_gesture` | breakthrough | office 09–18 + martha_corridor_pending (aff≥40 + trust≥35) | 18 | 28 | location_office | office hall | Yes | **YES** |
| `martha_rooftop_scene` | breakthrough | corp_work_martha + aff≥40 + trust≥35 + hour≥19 | 20 | 30 | location_office → rooftop | rooftop bar | Yes (6 CG) | No |
| `home_dinner_scene_martha` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 12 | 22 | location_home | home | Yes (shared CG) | No |
| Corporate arc scenes (`corp_martha_1/2`, atlas, review) | career arc | various corp_shifts gates | 6–25 | 10–40 | location_office | office | No | No |

**Dependency tree:**
```
Corporate career started (day ~3)
  └─ caroline_met → martha_met (via corp_task_1, day ~5–7)
       └─ phone_martha_coffee_scene (day ~8, invite)
       └─ scene_martha_office_coffee (day ~8, hour<10 + aff≥20)
       └─ scene_wardrobe_martha (day ~10, wardrobe_tier≥2 + aff≥25)
       └─ scene_martha_gift_accusation (day ~14, 3rd gift → pending) [conflict]
       └─ scene_martha_corridor_gesture (day ~18, aff≥40 + trust≥35) [MAJOR]
       └─ martha_rooftop_scene (day ~20, via corp_work_martha + aff≥40 + trust≥35 + evening)
  └─ home_dinner_scene_martha (day ~12, own_kitchen_set)
```

**Issues:**
- `martha_rooftop_scene` is triggered exclusively from `corp_work_martha`, which is gated on `job_id == "corporate"` and the "Work alongside Martha" menu option (also requires `martha_collab_available()` cooldown). A player who leaves the corporate career before reaching aff≥40 + trust≥35 can **never** see the rooftop scene.
- `scene_martha_corridor_gesture` (MAJOR) and `martha_rooftop_scene` may both become available in the same day-18–25 window. The corridor gesture fires automatically at the office; the rooftop requires active corporate work. If both are pending at once, the corridor gesture fires first (on any office visit), but the rooftop requires the player to use `corp_work_martha` on the same day at hour≥19 — which is unusual because the 8h shift starting at 9:00 ends at 17:00. The rooftop check fires right after the shift return. This means both scenes can occur on the same day: corridor in the morning, then rooftop after an evening collab shift started after 11:00.
- The gift accusation fires at exactly the 3rd gift. Since `gift_count_for("martha") == 3` is the trigger, the 4th+ gift never re-triggers. However, the scene clears `martha_gift_scene_pending` after completion, so the conflict only fires once regardless of future gifting.

---

### CAROLINE

Schedule: Office Mon–Fri 09–18.
Career NPC. Gate: joining corporate career — `caroline_met` set on first corporate shift.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Caroline met (via `corporate_recruit`) | career arc | first corporate shift | 3 | 5 | location_office | office | No | No |
| General conversation (greet) | everyday | caroline_met | 3 | 5 | location_office | office | No | No |
| `corporate_review_intern` | career arc | corp_review_intern conditions | 12 | 20 | location_office | office | No | No |
| Corporate arc dialogue (via collab pool) | career arc | various | 6–30 | 10–45 | location_office | office | No | No |

Caroline has **no standalone relationship scenes** outside the corporate career arc. No conflict scene, no breakthrough CG, no home visit, no crossover with other NPCs. The `caroline_met` flag gates Martha's entire relationship tree but Caroline herself has no independent scene arc.

---

### SAM

Schedule: Park Mon–Fri 06–10, Gym Mon–Fri 10–14, Gym Sat–Sun 09–13.
World NPC (no gate).

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Sam greet / first meet | everyday | world NPC, cold approach | 1 | 3 | location_park / location_gym | park/gym | No | No |
| `sam_gym_scene` | breakthrough | aff≥35 + trust≥25 + gym_floor + hour≥18 | 20 | 30 | location_gym | gym | Yes (6 CG) | No |

**Dependency tree:**
```
Sam met (day ~1–3)
  └─ sam_gym_scene (day ~20, aff≥35 + trust≥25 + gym + hour≥18)
```

**Critical issues:**
- **Schedule mismatch on `sam_gym_scene`.** Sam's schedule places her at the gym Mon–Fri 10–14 and Sat–Sun 09–13. The scene trigger in `gym_floor` fires when `hour≥18`. Sam is not at the gym after 14:00 on any day. The trigger fires via direct `jump` (not gated on `npc_here("sam")`), so Sam appears in the scene without being at that location per her schedule. Either Sam's schedule needs an evening gym slot, or the trigger needs to use Sam's bar presence (she has no bar schedule listed — she's entirely absent from evening locations).
- Sam has **no phone invites, no home dinner, no conflict scene, no crossover scene**. Her entire relationship arc is one gym breakthrough. This is the thinnest NPC arc in the game — Sam has fewer scenes than any other NPC.

---

### KAI

Schedule: Café Tue/Thu 10–14, Gym Sat–Sun 10–14, Beach Sat–Sun 14–18, Bar Sat–Sun 18–22, Nightclub Fri–Sun 22–27.
World NPC (no gate). Also career NPC for trainer arc — `kai_met` set on first trainer shift.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Kai greet / first meet | everyday | world NPC or trainer day 1 | 1–5 | 3–7 | location_cafe / location_gym | — | No | No |
| `tr_first_day` (kai_met via career) | career arc | first trainer shift | 5 | 8 | location_gym | gym | No | No |
| `tr_npc1_kai` / `tr_npc2_kai` | career arc | shifts≥5 / shifts≥7 | 9 / 12 | 14 / 18 | location_gym | gym | No | No |
| `home_dinner_scene_kai` | everyday | own_kitchen_set + aff≥20 + trust≥15 | 14 | 22 | location_home | home | Yes (shared CG) | No |

**Issues:**
- No standalone conflict scene. No breakthrough CG outside the trainer career. No phone invite. No crossover scene (Kai appears in the nora_kai_crossover as a co-participant but it's Nora's scene).
- Kai's weekend schedule is very dense (café → gym → beach → bar → nightclub), making her the most schedule-accessible NPC, but this richness has no scene payoff beyond dinner and career arcs.

---

### NATALIE

Schedule: Warehouse Mon–Sat 07–15, Bar Sat–Sun 17–21.
Career NPC. Met automatically on first warehouse shift once STR≥25.

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Natalie met (warehouse shift 1) | career intro | STR≥25 + first warehouse shift | 10 | 18 | location_warehouse | warehouse | No | No |
| `phone_natalie_extra_scene` | commitment | natalie_met + random invite (15% chance per shift) + accepted | 14 | 25 | location_warehouse (Sat 08:00) | warehouse | No | No |

**Issues:**
- **No breakthrough scene, no conflict scene, no crossover, no home dinner.** Natalie's only interaction beyond conversation is a Saturday overtime shift.
- Natalie requires STR≥25 to access (starting STR=10; ~8 gym sessions of +8 STR = 12.5 days minimum training to reach 25). She is the last world NPC the player can reasonably meet.
- `phone_natalie_extra_scene` fires at ~15% chance per regular warehouse shift, capped at one per week. Expected delay: 6–7 shifts = 6–7 days of warehouse work to get an invite. Since each shift is 8h and deducting rental, meeting Natalie meaningfully requires significant logistical investment for very little payoff.
- No topic arcs defined for Natalie in `NPC_DATA` — she can only receive generic topic talk with no story depth.

---

### ELLE

Schedule: Café Tue/Thu 09–13, Beach Wed 16–19, Beach Sat–Sun 13–18, Nightclub Sat–Sun 21–25.
World NPC (no gate).

| Scene label | Type | Unlock conditions | Earliest day | Likely day | Trigger location | Staging | CG? | Major? |
|---|---|---|---|---|---|---|---|---|
| Elle greet / first meet | everyday | world NPC, cold approach | 1 (café) | 3 | location_cafe / location_beach | — | No | No |
| `arc_elle_travel_1` | everyday (arc) | Elle met | 2 | 4 | any (talk) | — | No | No |
| `arc_elle_travel_2` | everyday (arc) | aff≥15 + travel_1 done | 8 | 14 | any (talk) | — | No | No |
| `elle_pier_scene` | breakthrough | aff≥40 + npc_talkable("elle") + not done | 18 | 28 | location_beach | beach pier | Yes (6 CG) | No |

**Dependency tree:**
```
Elle met (day ~1–3)
  └─ arc_elle_travel_1 (day ~2, no req)
       └─ arc_elle_travel_2 (day ~8, aff≥15) — sets elle_abroad_revealed
  └─ elle_pier_scene (day ~18, aff≥40 + elle at beach)
```

**Issues:**
- `elle_abroad_revealed` is set in `arc_elle_travel_2` but there is **no follow-up scene**. The flag is declared in `data.rpy` and set in `arcs.rpy`, but no scene reads it as a gate or references it. The arc's emotional payload (Elle considering an 18-month research position in Portugal) has no payoff scene.
- `elle_pier_scene` is gated on `npc_talkable("elle")` which includes Elle's schedule. Her beach availability: Wed 16–19 and Sat–Sun 13–18. The player must visit the beach during these windows specifically. If the player tends to go to the beach on other days, this scene is easy to miss.
- No conflict scene, no phone invite, no home dinner, no crossover beyond the zoe+elle NPC_RELATIONS group (which only fires generic group conversation, not a scripted crossover scene).

---

## Cross-NPC Collision Risk

The `major_scene_last_day` flag blocks all other major scenes that day once one fires. Six scenes set this flag:

| Scene | NPC | Typical unlock window | Location required | Likely active simultaneously with |
|---|---|---|---|---|
| `scene_nora_hug_school` | Nora | day 18–28 | location_cafe (any hour) | martha_corridor, eli_deploy |
| `scene_martha_corridor_gesture` | Martha | day 18–28 | location_office 09–18 | nora_hug_school, eli_deploy |
| `scene_eli_deploy_hug` | Eli | day 20–30 | location_hub + hour≥19 | nora_hug_school, martha_corridor |
| `scene_lena_shoulder_gesture` | Lena | day 22–35 (if performance<70) | location_hospital | car_marcus |
| `scene_car_marcus_drive` | Marcus | day 18–35 | location_bar + hour≥22 | lena_shoulder, zoe_spontaneous |
| `scene_zoe_spontaneous` | Zoe | day 25–38 | location_nightclub + hour≥21 | car_marcus |

**High-risk collision pairs:**

| Pair | Collision likelihood | What happens to blocked scene | Natural resolution |
|---|---|---|---|
| nora_hug_school + martha_corridor_gesture | HIGH — both require thresholds reached in same day-18–28 window; both pending flags can be True simultaneously | Whichever location is visited second that day fails the `major_scene_last_day != day` check and silently skips | None automatic. Player must visit office/café on separate days. No queue or retry notification. |
| nora_hug_school + eli_deploy_hug | MEDIUM — eli_deploy requires hub hour≥19; nora_hug_school fires at café any hour. Both plausible same day | Hub visit at evening blocked by earlier café visit | Player visits café in morning, hub blocked in evening — or vice versa. One scene simply doesn't fire that day. |
| martha_corridor_gesture + eli_deploy_hug | MEDIUM — office requires daytime (09–18), hub requires hour≥19. Same-day sequencing is physically impossible (can't do office + hub both in bounds). | Not truly same-day collisions since time windows don't overlap | Office in morning, hub in evening → no actual collision! This pair is safe. |
| car_marcus_drive + zoe_spontaneous | MEDIUM — both require hour≥21–22 at bar/nightclub on Fri–Sun; weekend late night is when both are active | Whichever is checked second fails | First location visited wins. No retry guarantee. |
| lena_shoulder_gesture + any other major | LOW — lena_shoulder requires poor hospital performance, which means player is likely in hospital working, not visiting café/bar | Hospital-exclusive location means it doesn't collide with bar/café majors | Location isolation provides natural separation |

**Location-time collisions (same NPC, same window):**

| NPC pair | Shared location/time | Likelihood |
|---|---|---|
| Nora + Kai (nora_kai_crossover) | Café, Kai must be present (Tue/Thu 10–14) during Nora's Mon–Fri 07–16 window. Overlap only Tue/Thu 10–14. | MEDIUM — requires player to visit café on Tue or Thu morning specifically |
| Marcus + Sam | Both at park Mon–Fri 06–10 (group_scene_check via NPC_RELATIONS). Generic group chat only — no scripted collision. | LOW impact |
| Zoe + Elle | Both in nightclub Sat–Sun (Zoe 21–27, Elle 21–25). NPC_RELATIONS marks them as friends — generic group chat. | LOW impact — no scripted scene |

---

## Coverage Gap Matrix

| NPC | Everyday | Item-enabled | Breakthrough | Conflict | Crossover |
|---|---|---|---|---|---|
| Nora | ✅ (greet, closing, rent, dinner, café arcs) | ✅ (coffee machine) | ✅ (closing night, hug_school) | ✅ (feels_ignored) | ✅ (nora_kai) |
| Marcus | ✅ (greet, dinner, park/bar arcs) | ❌ | ✅ (car drive) | ❌ (dead code) | ⚠️ (sam group only, no scripted scene) |
| Zoe | ✅ (meet, rain shelter, dinner, art arcs) | ✅ (guitar) | ✅ (beach night, spontaneous) | ❌ | ✅ (eli_meets_zoe) |
| Eli | ✅ (greet, debug session, work arcs) | ✅ (side project, programming_kit) | ✅ (deploy hug) | ❌ | ✅ (eli_meets_zoe) |
| Lena | ✅ (break room, dinner, career arcs) | ✅ (kitchen extended via own_kitchen_set) | ✅ (rooftop, shoulder gesture) | ❌ | ❌ |
| Martha | ✅ (coffee machine, wardrobe, dinner, collab arcs) | ⚠️ (wardrobe scene exists but wardrobe is a status item, not truly interactive) | ✅ (corridor gesture, rooftop) | ✅ (gift accusation) | ❌ |
| Caroline | ⚠️ (greet only; career arc dialogue) | ❌ | ❌ | ❌ | ❌ |
| Sam | ✅ (greet) | ❌ | ✅ (gym scene) | ❌ | ❌ |
| Kai | ✅ (greet, dinner, career arcs) | ❌ | ❌ | ❌ | ❌ |
| Natalie | ✅ (greet) | ❌ | ❌ | ❌ | ❌ |
| Elle | ✅ (greet, pier scene, travel arcs) | ❌ | ✅ (pier scene) | ❌ | ❌ |

**Narrative gaps by NPC:**

- **Marcus (conflict):** Needs a genuine conflict scene that can actually fire. The missed-commitment mechanic is dead. The most natural fit: a falling-out over something he reveals in `arc_marcus_sports_2` (the basketball decision) — Marcus pushing back if player gives unsolicited advice, or tension around the player spending nights at the bar with other people (jealousy with aff≥60 already exists mechanically).
- **Zoe (conflict):** No consequence for the player consistently deflecting her emotional moments. A scene where she directly confronts avoidance ("You keep doing this thing where you almost stay and then you don't") would fit her character and create stakes before `scene_zoe_spontaneous`.
- **Eli (conflict, home dinner):** Eli can be invited for side projects but not for dinner. The home dinner exclusion is a coding gap (not a design choice — all other friends are in the dinner list). A conflict scene: Eli's thesis receives a difficult committee response and the player's advice lands wrong.
- **Lena (crossover):** Lena has no scene with any other NPC. Given she works at the hospital with the player and is occasionally at the bar, a crossover with Marcus (who is also a bar regular) or with Martha (who is a corporate character the player knows) would fit naturally.
- **Caroline (everything):** The only NPC with no standalone arc at all. She is used entirely as a mechanism (gating Martha, processing promotions). A "Caroline outside work" scene — even one short moment where the player sees her off-guard — would humanise the corporate arc.
- **Sam (conflict, item, crossover):** Sam's arc is a single gym scene. A conflict where Sam calls out the player for inconsistency in training (or for a missed morning run commitment) would fit. A crossover with Marcus (gym_friends via NPC_RELATIONS) should produce a scripted scene, not just generic group chat.
- **Kai (breakthrough):** Kai has no standalone CG breakthrough. Her career arc is the only depth she has. A non-career breakthrough — perhaps related to her relationship with physical performance and pressure — would balance her arc.
- **Natalie (everything):** The thinnest NPC. A breakthrough scene at the warehouse (end-of-day, quiet moment with Natalie after a hard shift) would add texture. She could also have a conflict scene if the player consistently underperforms on shifts.
- **Elle (conflict, crossover, follow-up):** `elle_abroad_revealed` has no payoff. Elle's arc is left unresolved — she reveals a life-changing decision and nothing happens next. A follow-up scene (does she go? does she stay?) is the most urgent missing piece.

---

## Critical Pacing Issues

1. **[FIXED] `scene_marcus_missed_commitment` is unreachable (severity: HIGH).** The conflict is scripted, has art, has pending-dict infrastructure, and CG — but `mark_commitment_missed` only arms it for Marcus commitments, and no such commitment is ever created. Marcus's conflict arc is entirely absent. Fix: Marcus basketball invite now fires in `location_bar` once sports arc 1 is complete and aff≥25, creating a commitment with `npc_id="marcus"`.

2. **[FIXED] `eli_find_scene` is unreachable (severity: HIGH).** `own_metal_detector` has no purchase path. The scene contains six CG images and meaningful trust gains. Fix: metal detector added to `location_shop_electronics` at $120.

3. **[FIXED] `lena_shoulder_gesture` locked for competent players (severity: HIGH).** The MAJOR breakthrough for Lena's most emotionally significant scene requires `job_performance < 70`. A player maintaining good performance never triggers it. Fix: `hospital_hard_case_pending` now set by a 25% random chance per shift once `lena_break_room_done`, `hosp_shifts≥10`, `job_rank≥1`. Performance affects debrief text only.

4. **[FIXED] Six MAJOR scenes compete with one mutex, no retry queue (severity: HIGH).** When two major scenes are both pending, the one not visited on a given day silently fails. Verified: pending flags are never cleared on mutex block — they survive to the next visit. Test group 14 added to confirm this behaviour.

5. **[FIXED] `zoe_beach_night_scene` requires Zoe to appear off-schedule (severity: MEDIUM).** The scene fires at sandbeach past hour 20, but Zoe's schedule ends at 18 on weekends and she has no evening beach entry. Fix: added `(WKD, (19, 24), "location_sandbeach")` to Zoe's schedule in `interact.rpy`.

6. **[FIXED] `sam_gym_scene` requires Sam to appear off-schedule (severity: MEDIUM).** The scene triggers at gym_floor past hour 18, but Sam's gym schedule ends at 14. Sam has no evening location at all. Fix: trigger changed to `10 <= hour < 14` to match Sam's actual gym schedule.

7. **`lena_rooftop_scene` is only reachable if a hospital shift starts at 14:00 or later (severity: MEDIUM).** The trigger fires at `hour≥22` after a shift. Since shifts are 8h, a standard 8:00 start ends at 16:00. Only shifts starting at 14:00+ cross 22:00. Most players start work in the morning. Fix: decouple the rooftop from the shift completion check — make it a standalone evening option ("Go to rooftop (requires rank 1 + late night)") added to the hospital location menu.

8. **`elle_abroad_revealed` flag is set but never read (severity: MEDIUM).** Arc stage 2 of Elle's travel topic reveals a major life decision. No scene uses this flag as a trigger or gate. The arc's emotional weight has no payoff. Fix: write and implement a follow-up scene — at minimum a phone message from Elle ("I said yes.") that triggers a location scene, or an Elle-at-the-café scene where she says goodbye.

9. **`nora_last_seen_day` is only updated at the café, not by bar visits (severity: LOW).** Nora's bar visits (Tue/Fri 17–22) do not reset the 8-day ignore timer. A player who faithfully visits Nora at the bar twice a week but doesn't go to the café will trigger `scene_nora_feels_ignored`. Fix: update `nora_last_seen_day = day` in any `npc_interact("nora")` call, not just at location_cafe entry.

10. **Eli omitted from home dinner invite menu (severity: LOW).** All other close world NPCs (Martha, Nora, Zoe, Marcus, Lena, Kai) appear in `home_dinner_invite_menu`. Eli is absent despite having a home-visit scene (`home_eli_side_project_scene`). Fix: add `home_dinner_scene_eli` and include it in the dinner menu alongside the existing six.

---

## Recommended Threshold / Dependency Changes

| Change | From | To | Reason |
|---|---|---|---|
| `lena_shoulder_gesture` trigger | `hospital_hard_case_pending` set by 25% random roll (requires `job_rank >= 1` + `hosp_shifts >= 10` + `lena_break_room_done`; no pity trigger) | Replace random roll with `scene_hospital_hard_case` (ARC-1) — authored dramatic scene that guarantees `hospital_hard_case_pending = True` | Ensures all qualifying hospital players reliably reach Lena's MAJOR breakthrough |
| `sam_gym_scene` trigger hour | `hour >= 18` (gym, off-schedule) | `hour >= 10 and hour < 14` on weekends (matches Sam's schedule), OR add Sam evening gym slot Fri/Sat 18–21 | Eliminates schedule mismatch |
| `zoe_beach_night_scene` | Auto-trigger at sandbeach hour≥20 (Zoe off-schedule) | Add `(WKD, (18, 24), "location_sandbeach")` to Zoe's schedule; keep auto-trigger | Justifies Zoe's presence narratively |
| `lena_rooftop_scene` | Inside hospital shift code at `hour>=22` | Standalone menu item "Meet Lena on the rooftop (late night)" at location_hospital when `hour>=21 + rank>=1 + trust>=25` | Makes scene reachable for morning-shift players |
| Marcus missed commitment | `marcus_missed_pending` never set (no setter anywhere in the codebase) | Add a miss handler in the basketball commitment that sets `marcus_missed_pending = True` when the grace period expires; or replace the "nop" label with a dedicated miss scene | Unblocks the existing `scene_marcus_missed_commitment` scene (basketball invite commitment now exists but uses "nop" on miss) |
| `own_metal_detector` | No acquisition path | Add to `location_shop_electronics` at $80, or flea_market at $40–60 | Unblocks `eli_find_scene` |
| Eli home dinner | Not in `home_dinner_invite_menu` | Add `home_dinner_scene_eli` scene and menu entry (aff≥20, trust≥15, own_kitchen_set) | Fixes the Eli exclusion |
| `nora_last_seen_day` update | Only at `location_cafe` entry | Also update in `npc_interact("nora")` (in `npc_interact` driver or nora_greet) | Fixes bar-visit not counting for ignore trigger |
| `elle_abroad_revealed` follow-up | No scene exists | Add a delayed phone message (day+3 after arc completion): Elle texts her decision → triggers a café or beach scene | Gives the arc emotional closure |
| major_scene_last_day conflict | Single shared mutex, no retry | Add `_pending_day` re-check: if `major_scene_last_day == day` and scene is pending, defer to tomorrow (set an internal retry_after_day = day+1) | Prevents silent scene loss |

---

## Proposed Next Content Pack

Priority order (by gap severity and player-hours impacted):

1. **Marcus conflict scene** — the missed-commitment scene is built but unreachable. Write the commit invitation system (basketball or morning run, phone invite pattern matching Eli/Nora), then the confrontation when missed. Est: 1 phone response label + 1 commitment label already done + verify existing scene triggers.

2. **Metal detector shop entry** — one line in `location_shop_electronics`. Immediately unblocks `eli_find_scene` and all its CG content with zero new writing.

3. **Elle resolution scene** — `elle_abroad_revealed` needs a payoff. A phone message + a café or beach goodbye/stay scene. Medium content: 1 phone message + 1 scene with 2–3 CG frames.

4. **Lena shoulder gesture rebalance** — change the `hospital_hard_case_pending` setter to fire at perf<85 or shift count≥10. Zero new writing — code change only.

5. **Sam evening gym slot + backup scene** — add Sam to gym Fri/Sat 18–21 (schedule entry only). Fix the trigger hour to match. Consider a second Sam scene (a conflict around inconsistent training attendance, or a crossover with Marcus at the park).

6. **Eli home dinner** — write one home_dinner_scene_eli label (follows the pattern of the other six dinner labels exactly) + add to menu. Low effort, high coverage gain.

7. **Kai breakthrough scene** — Kai's weekend schedule is rich but payoff-free outside the trainer career. A standalone CG moment (e.g., Kai at the beach after a race, or a late-night gym session) would give her a personal arc independent of the career.

8. **Caroline humanisation scene** — one off-work scene (e.g., player spots Caroline at the bar on Thursday, her one evening slot). Short — 4–5 beats, no major flags — but essential for making her a character rather than a function.

9. **Natalie breakthrough scene** — end-of-shift quiet moment at the warehouse. One CG, minimal dialogue. Brings Natalie up to even a minimal arc (she currently has exactly one scene: the extra shift).

10. **Major scene retry queue** — implement a simple `_major_retry_after[scene_id] = day + 1` dict inside the major scene pending checks so blocked scenes defer rather than silently skip. Pure code change, no content required.
