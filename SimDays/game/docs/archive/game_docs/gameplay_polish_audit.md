# Gameplay Polish Audit

## Files Read

- `data.rpy` — defaults, spend_time, new_day, DECAY, stats, DAY_END/DAY_START
- `locations.rpy` — all location labels and activity menus
- `activity_menu.rpy` — _split_caption, activity screen, ACT_FONT/PROFILE_FONT defs
- `phone.rpy` — phone UI screens (phone_home, phone_messages_scr, phone_bank_scr, etc.)
- `phone_messages.rpy` — commitment system, inbox, delivered_messages, add_commitment
- `profile.rpy` — profile screen, stats display, WORK section
- `quests.rpy` — QUESTS list, active_quests, completed_quests, _q() helper
- `interact.rpy` — NPC_DATA, npc_aff, npc_trust, simple hug action, topic system
- `work_events.rpy` — work event pool
- `careers.rpy` — CAREERS dict, can_promote, do_shift, PRO_SKILLS
- `hud.rpy` — screen hud (date/time/money/needs)
- `gains.rpy` — gain_stat, gain_money, gain_skill, _push_gain
- `phone_actionable.rpy` — commitment scene labels (martha coffee, eli debug, lena case, nora closing)

---

## Found Problems

### 1. No daily agenda view
- `phone_messages_scr` has a "Upcoming" panel (via `commitments_list`) but only shows future commitments, no "today vs tomorrow" grouping, no live status text.
- No HUD reminder when a commitment is approaching.

### 2. No commitment overlap warning before starting activities
- A player can start a 4-hour activity 30 minutes before a commitment with no warning.

### 3. No career arc progress visibility
- Profile WORK section shows performance bar and `job_next` hint, but not how far through the arc story the player is.
- Next-rank requirements are shown as a single string (`job_next`) rather than colour-coded individual checks.

### 4. No relationship memory system
- Shared scenes (Martha coffee, Nora closing, rooftop scenes, etc.) leave no permanent record in UI.

### 5. No relationship threshold feedback
- Crossing affection/trust milestones (25, 40, 60, 75) is invisible — the bars climb with no celebration.

### 6. Hug is a single generic action
- All NPCs get `"[_nm] smiles and leans in. A brief, warm hug."` + +3 aff, with no cooldown, no per-NPC personality, no memory.

### 7. Activities have no diminishing returns per day
- Player can spam park jog, guitar practice, library study all day for unlimited stat gains.

### 8. Missing quests for key milestones
- No quest for: attending a commitment, buying a home item, paying off debt, building a skill to 3, earning mentor trust, completing a career arc.

### 9. No career performance threshold notifications
- Performance hitting 50/80/100 is invisible unless you open the profile.

---

## Planned Fixes (Systems 1-9)

| System | Description | Files Changed |
|--------|-------------|---------------|
| 1 | Daily Planner helpers + Agenda tab + HUD reminder + overlap warning | phone_messages.rpy, phone.rpy, hud.rpy, data.rpy, locations.rpy |
| 2 | Career arc progress helper + profile panel | careers.rpy, profile.rpy |
| 3 | Relationship memory helpers + hooks + UI | data.rpy, interact.rpy, phone_actionable.rpy, locations.rpy, phone.rpy |
| 4 | Threshold notifications for aff/trust + career perf | interact.rpy, careers.rpy, data.rpy |
| 5 | HUG_PROFILES + do_hug + cooldown + memory | data.rpy, interact.rpy |
| 6 | Anti-repetition: activity_last_used + helpers + location edits | data.rpy, locations.rpy |
| 7 | New QUESTS entries | quests.rpy |
| 8 | Economy/time audit doc | docs/economy_and_time_audit.md |
| 9 | Test file | test_gameplay_polish.rpy |

---

## Files To Be Changed

- `data.rpy` — new defaults + helper functions
- `phone_messages.rpy` — new commitment helpers
- `phone.rpy` — Agenda section, memory display in contacts
- `hud.rpy` — next-commitment HUD reminder
- `interact.rpy` — memory helpers, threshold check, modified _apply_aff/_apply_trust, HUG_PROFILES, do_hug, updated npc_interact/npc_actions
- `careers.rpy` — career_arc_progress, career perf threshold check, call in do_shift
- `profile.rpy` — career arc progress + next-rank requirement display
- `locations.rpy` — add_relationship_memory calls, anti-repetition for park/library/guitar/bar
- `phone_actionable.rpy` — add_relationship_memory calls to scene labels
- `quests.rpy` — new quest entries

---

## Regression Risks

| Risk | Notes |
|------|-------|
| `_apply_aff`/`_apply_trust` modification | All arc files (corporate_arc.rpy, it_arc.rpy, hospital_arc.rpy, etc.) call these — adding threshold check must not break for any npc_id. Guard: `if npc_id not in NPC_DATA: return` in `_check_relationship_thresholds`. |
| Hug system changes | `npc_actions` screen condition changes from `>= 15` to profile-based — NPCs not in HUG_PROFILES default to min_aff=999 (inaccessible). All main NPCs have profiles so this is intentional. |
| New `default` vars | Ren'Py `default` vars are save-safe: old saves get the default value. No risk. |
| `career_arc_progress` in quests.rpy | Function must be defined in init python at priority 0 in careers.rpy before quests.rpy accesses it. Since careers < quests alphabetically, this is safe. |
| Anti-repetition in locations.rpy | Inline menu edits — must preserve exact indentation. |
| `relationship_memories` dict mutation | Uses copy-on-write pattern (same as existing npc_gift_week, npc_last_seen). |

---

## Things Intentionally Left Unchanged

- `work_events.rpy` — work event pool is fine as-is; not part of this pass
- `map.rpy` — no changes needed; HUD reminder goes in hud.rpy not map.rpy
- `casino.rpy`, `stocks.rpy` — out of scope
- `group_scenes.rpy` — out of scope
- `corporate_arc.rpy`, `it_arc.rpy`, `hospital_arc.rpy`, `trainer_arc.rpy`, `culinary_arc.rpy` — arc scenes will pick up add_relationship_memory only for the key scenes listed in the spec; rest untouched
- `C:\Users\oskar.bazydlo\Documents\LivingTheDream\to_generate\scenes\gameplay_expansion\` — not touched per constraint
