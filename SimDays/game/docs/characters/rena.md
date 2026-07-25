# Rena — Character Reference
## Status: APPROVED CANON (director-locked)

---

## Identity

| Field | Value |
|---|---|
| Age | 36 |
| Pronouns | she/her |
| Title | Head Chef, Eleven |
| Romanceable | No |
| Routes | Friendship / professional mentorship (both complete) |
| NPC ID | `rena` |
| Phone display | Chef Rena |
| Decay | `no_decay=True` — relationship does not decay from absence |

---

## Voice and Presence

Calm, highly precise, rarely raises her voice. Becomes **quieter under pressure**, not louder — this is the tell that something serious is happening.

Values early honest communication. Prefers a specific, honest admission of a mistake to a general reassurance that things are fine.

Gives specific praise ("You compensated for the hob correctly") rather than generic encouragement. She does not compliment effort; she acknowledges execution.

Does not explain herself unless asked directly. Will answer a direct question honestly.

---

## Physical Description

- Compact, strong build
- Warm olive skin
- Dark chestnut hair in a low braided knot
- One naturally lighter streak at the left temple
- Amber-brown eyes
- Small old burn mark on left forearm — never referenced by Rena
- Charcoal chef jacket with rolled sleeves (on duty)
- Dark apron
- Analog watch worn on the inner wrist, face inward
- Black marker and thermometer in the same pocket, always

---

## Mannerisms

- Taps the pass twice before service begins
- Straightens tickets while thinking — an unconscious tell
- Asks "what exactly happened?" not "is everything fine?"
- Remembers honest admissions of mistakes and does not hold the admission against the person
- Smiles with one corner of her mouth when genuinely amused — not a full smile

---

## Character Core

**External conflict:** Eleven's owners pressure her to cut costs, simplify the menu, and reduce staffing. She is managing the gap between what the kitchen could be and what the business needs it to be. She has not resolved this tension.

**Internal need:** Learn to distribute responsibility. She cannot run a kitchen by being the only person in it who meets her own standard. Her current approach makes her indispensable; her flaw is that she believes this is the same as being good.

**Central flaw:** Confuses leadership with being indispensable. Holds standards by being present everywhere rather than by raising the floor. This makes the kitchen dependent on her presence rather than her principles.

**What she wants from MC:** Someone who asks the right question, not just executes the instruction. A commis who understands the reason behind the correction — why the grip matters before the dish matters — is worth more than one who complies.

**What she wants without MC:** Eleven survives. The owners back down or she finds another way to hold the standard while cutting where it won't show. She either solves the staffing problem through distribution (her internal arc resolution) or continues managing it personally (her failure state, narratively).

---

## Off-Duty Life

**Recurring location:** A late-night diner near the waterfront (not yet named in code). She reads used crime novels there. She orders from someone else's menu and lets someone else cook.

This is the only space where she is not performing the role. The diner scene is where the player can learn something real about her that the kitchen never reveals.

---

## Arc Status

| Scene | Status | Notes |
|---|---|---|
| `cul_npc1_rena` (knife correction) | Implemented | First establishment of character |
| `cul_npc2_rena` ("why the kitchen?") | Implemented | Best current scene |
| `scene_cul_service_crisis` | Implemented | 4-branch crisis; CG pre-choice; aftermath callback on next shift |
| `scene_rena_bar` | Not implemented | Required for off-duty humanity |
| `cul_review_commis` (promotion) | Implemented | Payoff scene post-crisis |

---

## Writing Guidelines

**Do write:**
- Corrections that are specific: "the blade angle, not the force"
- Questions that assume the person can handle the honest answer
- Silence as acknowledgment (she does not confirm every small correct action out loud)
- Her asking about what happened, not about how you feel about what happened

**Do not write:**
- Unprompted backstory disclosures — she does not volunteer personal information
- Warmth expressed through words rather than through expectation — she shows it by expecting more
- Her shouting or expressing frustration loudly — the quiet is the signal
- Generic mentor lines ("you're doing great") — she is specific or silent

**Dialogue register:** Precise, short, declarative. She does not soften instructions. She does not apologise for standards. She uses concrete nouns: the hob, the timing, the pass.

---

## Relationship Network

No NPC relationships currently established in code. Future connections:
- The late-night diner owner/staff: one off-duty scene
- Crossover potential with any NPC who frequents the nadbrzeze area at night

---

## Sprites

Expression keys are standardized. Rena's personality controls how the emotion is performed — the key names are not descriptions of her acting direction.

All sprites are in `images/characters/rena/`. Kitchen and casual sets share the same folder — distinguished by prefix only.

### Kitchen set

| Image name | File | Acting direction |
|---|---|---|
| `rena_normal` | `rena_normal.png` | At rest; on service |
| `rena_talk` | `rena_talk.png` | Giving instruction or correction |
| `rena_happy` | `rena_happy.png` | Restrained approval — one corner of the mouth, not a full smile |
| `rena_angry` | `rena_angry.png` | Controlled displeasure — quieter, not louder; this is her tell |
| `rena_sad` | `rena_sad.png` | Rare; defeat without display |

### Casual set

| Image name | File | Acting direction |
|---|---|---|
| `rena_casual_normal` | `rena_casual_normal.png` | Off-duty, at rest; outside her context |
| `rena_casual_talk` | `rena_casual_talk.png` | Speaking; looser register than kitchen |
| `rena_casual_happy` | `rena_casual_happy.png` | Genuine, slightly warmer than kitchen-happy |
| `rena_casual_angry` | `rena_casual_angry.png` | Controlled — same tell as kitchen; harder to read off-duty |
| `rena_casual_sad` | `rena_casual_sad.png` | Quieter than kitchen-sad; this is private |

Fallback rule: if a required expression is missing, fall back to the same outfit's `_normal` sprite. Never fall back across outfit sets (do not use a kitchen sprite when the scene context is casual, or vice versa).

### Visual continuity rules (director-locked)

- **Blackwork snake tattoo on the RIGHT forearm.** `rena_normal.png` is the authoritative reference. Never mirror any sprite.
- No wristwatch unless `rena_normal.png` shows one. The character description notes a watch worn face-inward on the inner wrist; do not add it in post if it is absent in the source image.
- If a new sprite shows the left forearm, the small old burn mark should be visible.

---

## Implementation Notes

- `no_decay=True`: correct — professional mentors don't decay from absence
- `rena_affection` and `rena_trust` track the relationship; currently only written via `_apply_trust` in culinary shifts and arc completion
- No phone messages from Rena outside the culinary arc; this is intentional — she is not a social contact, she is a professional one
- Off-duty diner scene should NOT use kitchen background — the whole point is that she is outside her context
