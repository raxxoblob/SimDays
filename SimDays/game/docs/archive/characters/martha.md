# Martha

## Canon Identity

NPC key: `martha`
Role: senior colleague at the corporate work location
Relationship scope: romanceable
Age: Not yet documented.
Pronouns: Not yet documented.

## Core Personality

Martha is professional, precise, and measured. She expects competence and notices its absence quietly.

Not yet fully documented.

## Voice and Dialogue Rules

- formal register,
- does not soften corrections,
- compliments are rare and specific,
- does not engage with excuses.

## Daily Life and Schedule

Present at the corporate office during corporate shifts. Has an independent schedule beyond shifts.

## Locations

- Corporate office (primary shift location)
- Other corporate-adjacent locations: not yet documented.

## Relationship Progression

Romanceable. Romance states: unopened → friends → interested → dating → committed.

Initial state: Liking 0, Trust 0.

`corp_shifts` count is a key progression gate. Specific romance thresholds not yet documented.

## Liking and Trust Behavior

Social profile (Phase 6B):
- `social_openness`: low
- `initiative`: low
- `jealousy`: low
- `jealousy_unlock`: None
- `jealousy_threshold`: 15
- `trust_sensitivity`: high
- `forgiveness`: low
- `status_sensitivity`: high
- `conflict_style`: indirect

Liking/trust specifics: not yet documented.

## Jealousy and Boundaries

Jealousy level: low.

Jealousy unlock: `martha_corridor_done` (corridor scene complete — personal moment beyond professional).

Threshold: 7. Cooldown: 7 days.

**Implemented (Phase 6C):** `martha_jealousy_first_notice` — fires once through existing Martha Talk follow-up path, after credit/revision/settled follow-ups, before generic Talk.

Eligibility: pending + `martha_corridor_done` + `not martha_jealousy_first_notice_done`.

Branches: "Does it bother you?" → no change; "I wasn't trying to make a point." → no change; "You're overthinking it." → -1 trust. All branches clear pending, set cooldown, add memory `martha_first_jealousy_notice`. No exclusivity established.

One ordinary Talk does not trigger jealousy. Professional conversations do not count.

## Important NPC Relationships

- Martha is a possible introduction route to Sloane. Exact relationship not yet approved.

## Event Chronology

| Order | Event ID | Trigger | What Changes | Follow-up |
|---|---|---|---|---|
| 1 | `wev_corp_final_revision` | Corporate shift | `martha_revision_choice` stored | `talk_followup_martha_revision` fires next Talk |
| 2 | `talk_followup_martha_credit` | Talk after `martha_acknowledged_work` memory | One-time follow-up | Done flag set |
| 3 | `talk_followup_martha_revision` | Talk after `wev_corp_final_revision` | One-time follow-up; branches on choice | Done flag set |
| 4 | `talk_followup_martha_settled` | Talk when `corp_shifts >= 3` | One-time follow-up | Done flag set |
| 5 | `martha_jealousy_first_notice` | Talk after story follow-ups when pending + `martha_corridor_done` | ±trust by branch; memory `martha_first_jealousy_notice` | `martha_jealousy_first_notice_done = True` |
| 6 | `crossover_martha_caroline_static` | WED at Static when Martha and Caroline both present | Memory `martha_seen_with_caroline_static` added | Establishes Martha and Caroline interact professionally; their relationship left undefined |
| 7 | `crossover_martha_caroline_repeat` | WED ambient at Static after original crossover resolved | Dialogue only; 3 variants | Repeatable (cooldown 5); both NPCs must be present |

## Facts Known About MC

Knows MC's performance across corporate shifts. Knows which revision approach MC chose during `wev_corp_final_revision`.

## Open Threads

- Romance arc events not yet designed or documented.
- `martha_gift_scene_pending` mechanics and dialogue not yet fully documented here.
- Sloane introduction route not yet approved.
- Repeat jealousy conversation not yet implemented.

## Continuity Rules

- Martha is romanceable but romance arc is not yet implemented in full.
- `martha_revision_choice` write is guarded so it does not overwrite after the follow-up fires.

## Implemented Assets

| Asset ID | Type | Used In |
|---|---|---|
| `martha_neutral` | sprite | corporate events, `npc_interact` |
