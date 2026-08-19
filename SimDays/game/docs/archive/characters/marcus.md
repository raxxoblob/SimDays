# Marcus

## Canon Identity

NPC key: `marcus`
Role: neighbour; first recurring daily NPC the MC meets after moving in
Relationship scope: friendship only; romance planned but not implemented

## Core Personality

Marcus is:

- direct,
- warm but not clingy,
- practical about city life,
- mildly competitive about trivial things,
- privately observant.

## Voice and Dialogue Rules

- conversational and informal,
- uses short declaratives,
- occasional dry humour,
- never delivers speeches,
- does not overshare unless trust is high.

## Daily Life and Schedule

Present in the home corridor and shared areas. Schedule-based appearances tied to `move_in_complete`.

## Locations

- Corridor / shared building (default daily location)
- Player home (when `marcus_home_state` is "invited_once" or "welcome")

## Relationship Progression

Initial state: Liking 0, Trust 0.

Requires `move_in_complete` for most interactions.

`marcus_home_state` progresses through "locked" → "invited_once" → "welcome".

Romance not yet unlocked.

## Liking and Trust Behavior

Social profile (Phase 6B):
- `social_openness`: high
- `initiative`: medium
- `trust_sensitivity`: medium
- `forgiveness`: medium
- `status_sensitivity`: low

Liking increases from: ordinary conversation, showing interest in his life, practical competence.

Liking decreases from: status boasting, dismissiveness, avoiding him.

## Jealousy and Boundaries

Jealousy level: none.

Marcus does not react to MC's other relationships.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `marcus_first_shift_checkin` | After first work shift | `marcus_first_shift_choice` stored | `talk_followup_marcus_first_shift` fires next Talk |
| 2 | `talk_followup_marcus_first_shift` | Talk after `marcus_first_shift_checkin` | One-time follow-up dialogue | Done flag set |
| 3 | `marcus_new_car_comment` | WED at home with `car_tier > 0` | No stat change | — |
| 4 | `crossover_marcus_nora_coffee` | WED at Grounds when Marcus and Nora both present | Memory `marcus_met_nora_at_grounds` added | Establishes Marcus visits Grounds; does not confirm friendship with Nora |
| 5 | `crossover_marcus_nora_repeat` | WED ambient at Grounds after original crossover resolved | Dialogue only; 3 variants | Repeatable (cooldown 5); both NPCs must be present |

## Facts Known About MC

Knows MC moved in recently. Knows MC has a car once `car_tier > 0`.

## Open Threads

- Romance unlock threshold and arc not yet designed.
- `marcus_home_state` deeper content not yet implemented.

## Continuity Rules

- Marcus is not romanceable in the current build.
- Do not write romance dialogue before the unlock is approved.
- `marcus_first_shift_choice` write is guarded by `not talk_followup_marcus_first_shift_done`.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `marcus_casual_normal` | sprite | `npc_interact`, work events |
| `marcus_casual_talk` | sprite | work events |
