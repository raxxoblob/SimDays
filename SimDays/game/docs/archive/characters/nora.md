# Nora

## Canon Identity

NPC key: `nora`
Role: barista at Grounds Café
Relationship scope: romanceable
Age: Not yet documented.
Pronouns: Not yet documented.

## Core Personality

Not yet documented.

## Voice and Dialogue Rules

Not yet documented.

## Daily Life and Schedule

Present at Grounds Café (`location_cafe`) during regular hours.

## Locations

- Grounds Café (primary)

## Relationship Progression

Romanceable. Romance states: unopened → friends → interested → dating → committed.

Initial state: Liking 0, Trust 0.

Specific unlock thresholds: not yet documented.

## Liking and Trust Behavior

Social profile (Phase 6B):
- `social_openness`: high
- `initiative`: medium
- `jealousy`: medium
- `jealousy_unlock`: None (not yet tied to a specific flag)
- `jealousy_threshold`: 10
- `trust_sensitivity`: medium
- `forgiveness`: medium
- `status_sensitivity`: low
- `conflict_style`: gentle

Liking/trust specifics: not yet documented.

## Jealousy and Boundaries

Jealousy level: medium.

Jealousy unlock: `nora_bad_day_done` (bad-day visit scene complete — first personal moment beyond café interaction).

Threshold: 10. Cooldown: 7 days.

**Implemented (Phase 6C):** `nora_jealousy_first_notice` — fires once through normal Talk path when pending + `nora_bad_day_done` + `not nora_jealousy_first_notice_done`.

Branches: "Are you jealous?" → no change; "You could have just asked." → no change; "It's none of your business." → -1 liking. All branches clear pending, set cooldown, add memory `nora_first_jealousy_notice`. No exclusivity established.

One ordinary Talk does not trigger jealousy. Professional conversations do not count.

## Important NPC Relationships

Not yet documented.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `nora_jealousy_first_notice` | Talk when pending + `nora_bad_day_done` | ±aff by branch; memory `nora_first_jealousy_notice` | `nora_jealousy_first_notice_done = True` |
| 2 | `crossover_marcus_nora_coffee` | WED at Grounds when Marcus and Nora both present | No stat change | Nora shown aware of Marcus; their relationship left ambiguous |
| 3 | `crossover_marcus_nora_repeat` | WED ambient at Grounds after original crossover resolved | Dialogue only; 3 variants | Repeatable (cooldown 5); both NPCs must be present |

## Facts Known About MC

Not yet documented.

## Open Threads

- Romance arc events not yet designed or documented.
- Schedule and availability details not yet confirmed in code.
- Repeat jealousy conversation not yet implemented.

## Continuity Rules

Not yet documented.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `nora_cafe_normal` | sprite | `npc_interact`, café scenes |
| `nora_cafe_talk` | sprite | café scenes |
