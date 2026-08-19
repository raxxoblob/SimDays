# Sam

## Canon Identity

NPC key: `sam`
Role: gym regular; met at `location_gym`
Relationship scope: friendship only (romance planned but not implemented)
Age: Not yet documented.
Pronouns: Not yet documented.

## Core Personality

Not yet documented.

## Voice and Dialogue Rules

Not yet documented.

## Daily Life and Schedule

Appears at the gym (`location_gym`) according to schedule when `sam_met` is True.

## Locations

- Gym (`location_gym`) — primary

## Relationship Progression

Not romanceable in the current build. Romance planned (`ROMANCE_AVAILABILITY["sam"] = "planned"`).

Initial state: Liking 0, Trust 0.

Requires `sam_met` for WED events.

## Liking and Trust Behavior

Social profile (Phase 6B):
- `social_openness`: high
- `initiative`: high
- `jealousy`: none
- `trust_sensitivity`: low
- `forgiveness`: high
- `status_sensitivity`: low
- `conflict_style`: direct

Liking/trust specifics: not yet documented.

## Jealousy and Boundaries

Jealousy level: none.

Sam does not react to MC's other relationships.

## Important NPC Relationships

Not yet documented.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `wevent_gym_sam_last_rep` | WED at gym when `sam_met` and Sam present | Dialogue only | — |
| 2 | `wevent_gym_sam_bad_advice` | WED at gym when `sam_met` and Sam present | Dialogue only | — |
| 3 | `wevent_gym_sam_water_break` | WED at gym when `sam_met`, Sam present, `need_energy <= 40` | +1 trust | — |
| 4 | `crossover_sam_zoe_park` | WED at park when Sam and Zoe both present | Memory `sam_met_zoe_in_park` added | Establishes Sam has been observed by Zoe; no relationship change |
| 5 | `crossover_sam_zoe_repeat` | WED ambient at park after original crossover resolved | Dialogue only; 3 variants | Repeatable (cooldown 5); both NPCs must be present |

## Facts Known About MC

Knows MC from the gym.

## Open Threads

- Romance arc not yet designed.
- Sam personality and voice not yet approved.

## Continuity Rules

- Not romanceable in the current build.
- WED events require Sam to actually be present (`npc_here("sam")`), not just `sam_met`.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `sam_normal` | sprite | WED gym events |
