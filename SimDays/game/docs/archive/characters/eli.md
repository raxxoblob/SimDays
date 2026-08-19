# Eli

## Canon Identity

NPC key: `eli`
Role: IT colleague at the IT work location
Relationship scope: friendship only (romance disabled)
Age: Not yet documented.
Pronouns: Not yet documented.

## Core Personality

Not yet documented.

## Voice and Dialogue Rules

Not yet documented.

## Daily Life and Schedule

Present at the IT office during IT shifts.

## Locations

- IT office (primary shift location)

## Relationship Progression

Not romanceable. Romance disabled (`ROMANCE_AVAILABILITY["eli"] = "disabled"`).

Initial state: Liking 0, Trust 0.

## Liking and Trust Behavior

Social profile (Phase 6C update):
- `social_openness`: medium
- `initiative`: medium
- `jealousy`: medium
- `jealousy_unlock`: `eli_deploy_hug_done` (deploy hug scene complete)
- `jealousy_threshold`: 7
- `jealousy_cooldown`: 6 days
- `trust_sensitivity`: medium
- `forgiveness`: medium
- `status_sensitivity`: low
- `conflict_style`: professional

Liking/trust specifics: not yet documented.

## Jealousy and Boundaries

Jealousy level: medium (updated Phase 6C).

Jealousy unlock: `eli_deploy_hug_done` (deploy hug scene complete — personal moment beyond IT work).

Threshold: 7. Cooldown: 6 days.

**Implemented (Phase 6C):** `eli_jealousy_first_notice` — fires once through normal Talk path when pending + `eli_deploy_hug_done` + `not eli_jealousy_first_notice_done`.

Eli reacts only to romantic actions (kiss/date/flirt); hug and ordinary Talk do not create jealousy tension for Eli.

Branches: "It matters what you think." → no change; "There's nothing to explain." → -1 trust; "Are you upset?" → -1 liking. All branches clear pending, set cooldown, add memory `eli_first_jealousy_notice`. Eli is not aggressive or accusatory.

## Important NPC Relationships

Not yet documented.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `wev_it_eli_bug_report` | IT shift | Dialogue; Eli shown at sprite_r | — |
| 2 | `wev_it_eli_code_comment` | IT shift | Dialogue; Eli shown at sprite_r | — |
| 3 | `wev_it_eli_deploy_window` | IT shift | Dialogue; Eli shown at sprite_r | — |
| 4 | `eli_jealousy_first_notice` | Talk when pending + `eli_deploy_hug_done` | ±trust/aff by branch; memory `eli_first_jealousy_notice` | `eli_jealousy_first_notice_done = True` |

## Facts Known About MC

Knows MC as an IT colleague.

## Open Threads

- Romance disabled — reason and canon not yet documented.
- Eli personality and voice not yet approved.

## Continuity Rules

- Not romanceable.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `eli_normal` | sprite | IT work events, `npc_interact` |
