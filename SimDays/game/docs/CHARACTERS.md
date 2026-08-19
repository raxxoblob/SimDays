# Characters

Character bible for LivingTheDream. One entry per NPC.

**Rule:** Do not invent personality information not established here or in current source.
Per-character files in `SimDays/SimDays/game/docs/characters/` are authoritative for implementation details (flags, schedules, events table). This file covers writing/voice/canon only.

---

## Zoe

**NPC key:** `zoe` | **Role:** artist, park regular, eventual recurring personal contact | **Romanceable**

### Personality

Observant, self-contained, measured. Notices details about other people before they notice her noticing. Does not rush toward connection. Low social openness — warms slowly, holds back deliberately.

Not guarded in the defensive sense. More like: she has her own internal world and doesn't assume others are owed entry to it.

Dry, observational humor. Lands through understatement. Not performance, not trying to entertain.

Does not fill silence. Observations arrive after a pause. Does not name feelings explicitly when they are strong. Deflects rather than confronts.

Artistic confidence exists — she knows her eye is good. Personal work is different: she's protective of it. Paid client/commercial work and her real creative work are kept separate; the tension between them is ongoing.

**What she does NOT do:** not bubbly, not clingy, not generic supportive girlfriend, does not apologise for having opinions, does not gush.

### Affection Behavior

Early: shows interest through remembered details — something MC said three conversations ago surfaces naturally. Makes practical excuses to spend time near MC (same park, same café, incidental overlap).

Later: drops the excuses. Direct invitations. Still not effusive about it.

### Voice Rules

- Quiet register
- Short sentences that land after a beat
- Does not explain her feelings; describes what she notices instead
- Does not over-qualify; not a hedger
- Occasional dry irony; never sarcasm used as armor

### Romance Progression (current design)

```
unopened
  ↓
friends
  ↓
interested
  ↓
Beach Dating Breakpoint (M2) — director CG payoff
  possible canonical first kiss
  ↓
dating
  ↓
Beach After Dark (M3) — director CG payoff
  ↓
(ordinary life expands: coffee / walks / home / gym together)
  ↓
Commitment (M6, terrace) — director CG payoff
  ↓
committed
```

After `dating`: shared ordinary life increases. Coffee, walks, home visits, gym together, group outings. This is intentional — the relationship should feel like it exists between authored beats.

### Known Story Threads

- `zoe_rain_done` — rain shelter scene; first major personal moment; Stage 2 marker; jealousy unlock
- `zoe_moment_deflected_done` — nightclub spontaneous moment (M1)
- `zoe_beach_dating_done` — beach dating breakpoint (M2); CURRENT WORK
- `zoe_beach_night_done` — beach after dark (M3)
- `zoe_exhibition_invited` — set in code; exhibition opening scene NOT YET IMPLEMENTED
- `zoe_grant_discussed` — funding application mentioned; result not yet authored
- Bass guitar history — established canon; she played in a band
- Gallery/exhibition thread — ongoing; structural hole flagged (scene not yet implemented)
- Grant/funding tension — ongoing

### Jealousy

High. Unlock: `zoe_rain_done`. Threshold: 6. Cooldown: 5 days.
Conflict style: deflection. Does not confront directly. Does not apologise quickly.

### Continuity Rules

- `zoe_rain_done` is the Stage 2 gate. Do not skip it.
- Do not write Zoe confronting directly — she deflects.
- Do not write immediate MC apology options.
- Do not give her bubbly or clingy dialogue.
- The exhibition hole is known; do not write around it by having her describe having attended her own opening.

---

## Marcus

**NPC key:** `marcus` | **Role:** neighbour; first recurring daily NPC after MC moves in | **Friendship only** (romance planned, not implemented)

### Personality

Direct, warm but not clingy, practical about city life. Mildly competitive about trivial things. Privately observant — more perceptive than his casual demeanor suggests.

Short declaratives. Occasional dry humor. Doesn't deliver speeches. Doesn't overshare unless trust is high.

Proactive — he initiates, assumes friendship quickly, fills social space naturally without being pushy.

### Known Canon

- Bartender, associated with Static
- Early morning runner
- Basketball history (invite mechanics exist; authored scene pending)
- Stayed in city because father was ill (established character background)
- Chili/family recipe/notepad thread — do not discard this
- Does NOT go to the gym (still true per current docs)

### Relationship Mechanics

Home state: `marcus_home_state` → `"locked"` → `"invited_once"` → `"welcome"`
No jealousy. High social openness. Does not punish MC for neglect.

### Continuity Rules

- Not romanceable in current build. No romance dialogue until explicitly approved.
- Do not put Marcus at the gym.
- Basketball authored scene is pending; do not write around it.

---

## Nora

**NPC key:** `nora` | **Role:** barista at Grounds Café (`location_cafe`) | **Romanceable**

Personality not yet fully documented. Works regular café hours.

Social profile: high openness, medium jealousy. Jealousy unlock: `nora_bad_day_done`. Threshold: 10. Cooldown: 7 days. Conflict style: gentle.

Romance arc events not yet designed.

---

## Eli

**NPC key:** `eli` | **Role:** IT colleague | **Friendship only** (romance disabled)

Present at IT office during IT shifts. Romance disabled in source (`ROMANCE_AVAILABILITY["eli"] = "disabled"`).

Medium jealousy. Unlock: `eli_deploy_hug_done`. Threshold: 7. Cooldown: 6 days. Reacts only to romantic actions (kiss/date/flirt); hugs and ordinary talk do not trigger jealousy tension.

Personality and voice not yet approved.

---

## Rena

**NPC key:** `rena` | **Role:** head chef | **Not romanceable** | **DIRECTOR-LOCKED CANON**

Age: 36. She/her. Full physical description and expression sets documented in `game/docs/characters/rena.md`.

**Canonical visual rule:** Blackwork snake tattoo on RIGHT forearm. This is fixed.

Career arc implemented: `cul_npc1_rena`, `cul_npc2_rena`, `scene_cul_service_crisis`, `cul_review_commis`.
`scene_rena_bar` — NOT YET IMPLEMENTED.

Do not invent Rena dialogue or backstory beyond the approved character file.

---

## Elle

**NPC key:** `elle` | **Romanceable**

High social openness. High forgiveness. High status sensitivity. Medium jealousy (not yet implemented).

Portugal consequence thread: decision was made in-game; consequence scene not yet implemented.

---

## Martha

**NPC key:** `martha` | **Role:** corporate senior | **Romanceable**

Low jealousy. Unlock: `martha_corridor_done`. Threshold: 7. Cooldown: 7 days. Phase 6C implemented.

---

## Dr. Lena

**NPC key:** `lena` | **Role:** hospital doctor | **Romanceable**

Sprite: `drlena_normal`. Most character fields not yet documented.

---

## Sam

**NPC key:** `sam` | **Role:** gym regular | **Friendship only** (romance planned, not implemented)

Requires `sam_met` flag. Associated with gym. Three WED gym events + sam_zoe_park crossover.
**Sam ≠ Kai.** They are separate NPCs at the gym.

---

## Kai

**NPC key:** `kai` | **Role:** trainer career NPC | **Friendship only** (romance planned, not implemented)

Trainer career NPC. Separate from Sam. Most fields not yet documented.

---

## Caroline

**NPC key:** `caroline` | **Romanceable**

Medium jealousy (not implemented). Associated with off-the-clock bar scene (`caroline_bar_pending`/`caroline_bar_done`).

---

## Natalie

**NPC key:** `natalie` | **Friendship only**

No jealousy. Humanisation scene implemented.

---

## Planned NPCs

**Camila** — Bartender at Static, 29, she/her. Formal intro after 2 visits or status threshold. Romance possible. Full design in `game/docs/characters/camila.md`.

**Owen** — Bus mechanic, Static regular, 37, he/him. Not romanceable. Patient, practical, dry humor.

**Sloane** — Events manager, 32, she/her. Intro via status, corporate career, or Martha. Romance undecided.
