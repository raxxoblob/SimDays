# Zoe

## Canon Identity

NPC key: `zoe`
Role: artist; park regular and eventual recurring personal contact
Relationship scope: romanceable
Age: Not yet documented.
Pronouns: Not yet documented.

## Core Personality

Zoe is observant, self-contained, and measured in how much she reveals. She notices details about other people before they notice her noticing. Her social openness is low; she does not rush toward connection.

Not yet fully documented.

## Voice and Dialogue Rules

- quiet register,
- does not fill silence,
- observations arrive after a pause,
- does not name her feelings explicitly when they are strong,
- deflects rather than confronts directly.

## Daily Life and Schedule

Primary public location: `location_park`. Schedule-based appearances tied to `zoe_met`.

## Locations

- Park (`location_park`) — primary
- Nightclub (`location_nightclub`) — confirmed by nightclub moment
- Beach — confirmed by beach night scene

## Relationship Progression

Romanceable. Romance states: unopened → friends → interested → dating → committed.

Key flags:
- `zoe_met` — initial meeting
- `zoe_rain_done` — rain shelter scene; first major personal moment (Stage 2 marker)
- `zoe_moment_deflected_done` — nightclub moment
- `zoe_beach_night_done` — beach night scene
- `zoe_romance_unlocked` — romance fully available
- `zoe_reopen_done` — romance reopen scene

## Liking and Trust Behavior

Social profile (Phase 6B):
- `social_openness`: low
- `initiative`: low
- `jealousy`: high
- `jealousy_unlock`: `zoe_rain_done` (Stage 2 — rain shelter scene complete)
- `jealousy_threshold`: 6
- `trust_sensitivity`: high
- `forgiveness`: medium
- `status_sensitivity`: low
- `conflict_style`: deflection

Liking/trust specifics: not yet documented in full.

## Jealousy and Boundaries

Jealousy level: high.

Jealousy unlock: `zoe_rain_done` must be True.

Threshold: 6 accumulated tension points before pending conversation fires.

**Implemented (Phase 6B):** `zoe_jealousy_first_notice` — fires once through normal Talk path when pending and unlock satisfied and `not zoe_jealousy_first_notice_done`.

Cooldown: 5 days after `zoe_jealousy_last_day` is set.

Branches:
- "It doesn't mean anything." → -1 trust
- "I didn't realise it bothered you." → no stat change
- "Are you jealous?" → -1 liking

All branches: clear pending, set cooldown day, add memory `zoe_first_jealousy_notice`.

## Important NPC Relationships

Not yet documented.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `zoe_hears_guitar` (busking) | Park / busking scene | Memory `zoe_hears_guitar` | Earliest Zoe progression |
| 2 | `scene_zoe_rain_shelter` | Park or early encounter | `zoe_rain_done = True`; memory `zoe_rain_shelter` | Stage 2 unlocked |
| 3 | Nightclub moment | Nightclub scene | `zoe_moment_deflected_done`; memories `zoe_spontaneous_direction_*`, `zoe_almost_moment` | — |
| 4 | Beach night scene | Late-game trigger | `zoe_beach_night_done`; memory `zoe_beach_night` | — |
| 5 | Romance reopen | Post-deflection trigger | `zoe_reopen_done`; memories `zoe_reopen_romance` / `zoe_reopen_platonic` | — |
| 6 | `wevent_zoe_sketching_stranger` | WED at park when `zoe_met` and Zoe present | Dialogue only | — |
| 7 | `wevent_zoe_wrong_colour` | WED at park when `zoe_met` and Zoe present | Dialogue only | — |
| 8 | `wevent_zoe_lost_pencil` | WED at park when `zoe_met` and Zoe present | +1 trust; memory `zoe_pencil_attention` | — |
| 9 | `crossover_sam_zoe_park` | WED at park when Sam and Zoe both present | Memory `zoe_met_sam_in_park` added | Establishes Zoe has observed Sam's movement; no relationship change |
| 10 | `crossover_sam_zoe_repeat` | WED ambient at park after original crossover resolved | Dialogue only; 3 variants | Repeatable (cooldown 5); both NPCs must be present |
| 9 | `zoe_jealousy_first_notice` | Talk when pending jealousy + `zoe_rain_done` | ±stat by branch; memory `zoe_first_jealousy_notice` | `zoe_jealousy_first_notice_done = True` |

## Facts Known About MC

After `zoe_rain_done`: Knows MC by name and has spent personal time with them.

After nightclub moment: Knows something almost happened and was deflected.

After `zoe_jealousy_first_notice`: Knows MC has been spending time with at least one other person.

## Open Threads

- Full romance arc beyond current flags not yet documented.
- `zoe_exhibition_invited` path not yet documented here.
- `zoe_grant_discussed` event not yet documented here.
- Future jealousy conversations beyond first notice not yet designed.

## Continuity Rules

- `zoe_rain_done` is the Stage 2 gate for jealousy unlock.
- Jealousy pending is cleared on conversation fire; `zoe_jealousy_first_notice_done` permanently prevents the first-notice label from re-firing.
- Cooldown of 5 days is enforced via `npc_jealousy_last_day["zoe"]`.
- Do not make Zoe confront directly; she deflects.
- Do not write immediate apology options for MC.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `zoe_street_neutral` | sprite | WED park events |
| `zoe_street_talk` | sprite | `npc_interact`, Talk path |
| `zoe_street_smile` | sprite | specific positive moments |
