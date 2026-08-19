# Gameplay Systems

Player-facing systems and design philosophy for LivingTheDream.

---

## Time and Day Flow

The game runs in simulated days. Each day has hours. Activities consume time via `spend_time(hours)` (`data.rpy` line ~730). The clock advances; needs (energy, hunger, hygiene, social) decay accordingly.

The player cannot do everything in one day. Quiet days are valid — no punishment for not filling every hour.

---

## Player Needs

- **Energy** — depleted by activities; restored by sleep
- **Hunger** — depleted over time; restored by eating
- **Hygiene** — slow decay; restored by showering
- **Social** — depleted by isolation; restored by NPC interactions

Needs affect mood/performance but do not instantly disable activities. They create pressure, not hard walls.

---

## Skills

Skills represent actual ability — what the MC can actually do.

**Implemented skills include:**
- `stat_str` — Strength (default 10, stored in `data.rpy`)
- Programming, cooking, fitness/trainer skills, and others per career path

Skills are trained gradually through repeated activity. No shortcut purchases.

**Philosophy:**
- Skill = actual ability
- Reputation = opportunity quality / external standing
- Portfolio = accomplishments
- Money = convenience / acceleration, not a substitute for mastery

---

## Careers

Four career path types (A–D). Each has a performance bar and career ladder. Work shifts consume time and energy. Promotion requires sustained good performance.

Casual/gig jobs available for immediate income. Career jobs build reputation over time.

---

## Money and Economy

Money buys convenience and acceleration — better apartment, car, clothes, gifts. It does not buy skill or relationship depth.

Items must unlock behavior, not just add +stat. See `docs/DEVELOPMENT_RULES.md` for item design rules.

---

## Reputation

Separate from raw relationship points. Affects:
- Opportunity quality available
- NPC first impressions
- Access to certain locations/events

No global Luck stat.

---

## Portfolio and Accomplishments

Portfolio tracks what the MC has actually done — career milestones, completed projects, notable events. Affects long-term reputation.

---

## Relationship System

### Axes

Relationships tracked on multiple axes (verified from `npc_relationships.rpy`):
- **Affection** — warmth, emotional closeness
- **Trust** — reliability, honesty
- **Respect** — competence, standing
- **Familiarity** — shared time, comfort
- **Attraction** — romantic/physical interest (where applicable)

Affection and Trust have legacy NPC-specific store vars (`zoe_affection`, `zoe_trust`). Respect/Familiarity/Attraction are in the `npc_relationships` dict via `npc_rel(npc_id, axis)`.

### Romance States

States (verified from `interact.rpy`):
```
unopened → friends → interested → dating → committed
                                         ↘ paused
                                         ↘ closed
```

**Raw points enable believable progression. Authored scenes make it emotionally meaningful.**

Points alone do not advance romance state. A romance-state change requires an authored scene or scripted trigger. This is intentional.

### Canonical Helpers

- `get_romance_state(npc_id)` / `set_romance_state(npc_id, state, source=...)`
- `npc_rel(npc_id, axis)` — read relationship axis
- `apply_relationship_change(npc_id, event_key, source, **axes)` — canonical mutation
- `npc_aff(npc_id)`, `npc_trust(npc_id)` — legacy affection/trust shortcuts

Do not set relationship variables directly. Always use helpers.

---

## NPC Schedules and Living World

NPCs have schedule-based location appearances. The WED (World Events Daily) system fires ambient and personal events at location visits.

**WED rules:**
- Max 1 personal/major event per day
- Max 1 ambient event per location per visit
- No WED event fires during or immediately after a major authored scene day

WED store vars: `wed_personal_fired_day`, `wed_ambient_fired`, `wed_event_last_day`, `wed_resolved`, `wed_callbacks`.

---

## Phone

NPC-initiated texting system. NPCs send messages via `queue_phone_message()`. Player selects replies. Some messages schedule commitments (dates, activities). Photo messages are handled by the generic photo engine (`photo_message_engine.rpy`).

Initiative system in `phone_actionable.rpy`: `_INITIATIVE_VARIANTS`, `_DATE_VARIANTS`, `_VARIANT_WEIGHTS`, `_VARIANT_MIN_TIER`, `_VARIANT_CONDITIONS`.

---

## Invitations and Commitments

Two-stage system:
1. **Invitation** — NPC sends phone message; player accepts/declines
2. **Commitment** — scheduled event checked at location entry via `commitment_available(cid)`

`add_commitment(cid, npc_id, title, day, hour, location, label, grace=2.0)` — schedules
`commitment_available(cid)` — checked at location entry
`complete_commitment(cid)` / `cancel_commitment(cid)` — close out

---

## Activities

Activities consume time via `spend_time(hours)`. Energy and other needs decay by the amount specified in each activity. Costs are generally hardcoded inline at the activity or location label — there is no central activity cost table.

---

## Gym and Strength

**Strength variable:** `stat_str` (default 10, `data.rpy` line 24)

**Gym location:** `label location_gym` in `locations.rpy` line ~466
Sub-labels: `gym_reception` (~481), `gym_floor` (~515)

**Workout mechanics:** All workout activity logic is inline within `gym_floor`. There is no separate workout module. Workouts call `spend_time(hours)` and apply Strength XP via the gains system (`gain_stat("str", ...)`).

Supplements tracked via `supplements` dict (`"protein"`, `"preworkout"`).

**PLANNED extension:**
Shared replayable Zoe gym activity after `dating`/`committed`. Must reuse `spend_time()` and the existing strength gain flow — not create a parallel workout system.

---

## RNG Philosophy

Pattern: **Guaranteed progress + variable result + rare outcome**

- Randomness should excite, not erase large amounts of player effort
- No purely-random gatekeeping of major story content
- Quiet days (no exciting RNG) are valid gameplay

---

## Items

Every item must unlock behavior, not just add +stat. See `docs/DEVELOPMENT_RULES.md` item rules.

---

## Computer / Home

Computer has an OS shell with registered apps. Apps interact with the phone/computer shared data layer. Do not create a second data store — reuse the shared registry.
