# Trainer Career — Scene Asset Plan

> Covers all scenes in `trainer_arc.rpy`. NPC: Kai (she/her), head trainer. Location: Iron Gate Gym.
> Kai has an existing NPC interact system (`npc_talkable("kai")`) — check if a sprite already exists before generating new art.

---

## Scene Overview

| Scene | Label | Category | Existing BG | New BG | CG Count | Priority |
|---|---|---|---|---|---|---|
| First Day | `tr_first_day` | Story | `gymdaypeople` | No | 1 | **High** |
| First Solo Session | `tr_task_1` | Story | `pov_gym_weights` or new | Maybe | 1 | **High** |
| Programming Lesson | `tr_npc1_kai` | NPC | `gymdaypeople` | No | 1 | Medium |
| After Last Session | `tr_npc2_kai` | NPC | `gymdaypeople` | No | 1 | Medium |
| Promotion | `tr_review_asst` | Story | `gymdaypeople` | No | 0 (sprite only) | Low |
| Challenging Client | `wev_tr_challenging_client` | Work Event | `pov_gym_weights` | No | 0 | Low |
| Equipment Issue | `wev_tr_equipment_issue` | Work Event | `gymdaypeople` | No | 0 | Low |
| Group Class | `wev_tr_group_class` | Work Event | `gymdaypeople` | No | 0 | Low |

**Possible new background: `gym_training_floor.png`** — A trainer-perspective view of the floor (not the client POV). See notes below.

---

## Existing Backgrounds

| File | Used in | Notes |
|---|---|---|
| `gymdaypeople` | Most Kai scenes | Main gym floor with visible members |
| `gym_cardio` | Cardio sessions | Cardio area |
| `pov_gym_weights` | Client weights POV | MC's POV as a client doing weights — may not be appropriate for trainer-mode scenes |
| `gym_reception` | Pass purchase | Not applicable to trainer arc |

**Note on `pov_gym_weights`:** This background is designed for when the player is the CLIENT doing weights. For the trainer arc, the perspective is different — Kai (and MC as trainer) are observing clients, not being the client. Consider a new background for trainer-perspective scenes, or adapt `gymdaypeople` which already shows the floor from an observer's angle.

**Recommended new background: `gym_training_floor.png`**
The gym floor from a trainer's standing perspective — seeing the space as a trainer does. Visible: a training bay (rack, bench, open space), the wider floor behind, other members training in the background. Not client POV (looking up at equipment) — standing-level observational view. This is the primary background for trainer-mode scene CGs.

---

## CG Plans

### CG 1: `tr_first_day_shadow.png`
**Scene:** `tr_first_day`
**Purpose:** MC shadowing Kai during the 7am session. The shot that establishes the trainer's observational register — Kai coaching, MC watching, the client as the subject.

**Camera:** From behind MC — MC in foreground, Kai and client in the mid-ground.

**Framing:** Client at a station (a squat rack or similar) in the centre. Kai beside them, mid-cue (hand gesture or physical adjustment, non-contact or light contact). MC visible from behind in the foreground, watching.

**Characters:**
- Kai: mid-30s, athletic build, trainer-appropriate clothing (technical wear, nothing flashy). Beside the client, demonstrating or adjusting. Her body language is attentive and precise — she's simultaneously watching the client and communicating.
- Client: mid-40s, gym clothing, at a training station. Their form is the subject Kai is addressing.
- MC: back to camera, foreground. Watching.

**Expressions:**
- Kai: focused on the client. Her attention is complete — she's not performing for MC's benefit.

**Environment:** Gym training floor — the new `gym_training_floor.png` background or `gymdaypeople`. Training bay with rack/bench visible, other gym members in the background.

**Lighting:** Gym lighting — bright, functional, some daylight from windows. Not dramatic.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Modern gym interior, morning. A training bay — squat rack and bench press visible. In the centre: a gym client (mid-40s, athletic wear) performing or about to perform an exercise. Beside them: Kai (a female trainer in her mid-30s, athletic build, technical training wear) — positioned for coaching, her hand gesturing to cue form or slightly adjusting the client's position. Her attention is entirely on the client — focused, precise, not performing. In the foreground: MC (back to camera, no face), standing and observing. The gym floor visible in the background — other members, equipment, morning light from windows. The composition: MC watches Kai coach, Kai watches the client. Observer — coach — athlete.
```

---

### CG 2: `tr_task_1_solo_session.png`
**Scene:** `tr_task_1`
**Purpose:** MC's first solo session. MC in the trainer role facing the new client — the dynamic is now reversed from the shadow scene.

**Camera:** From slightly behind Kai — Kai in background observing, MC and client in the foreground.

**Framing:** MC (in trainer role now) faces the new client — a younger person, slightly nervous. The framing shows the reversal: now MC is the coach and Kai is the observer.

**Characters:**
- MC: facing the client, visible from the back or three-quarter side. No face. Trainer posture — present, attentive.
- Client: the new client (early 20s, gym-anxious energy — their body language is slightly tense, compensating). Facing MC.
- Kai: small in the background, watching from a distance. Deliberately giving space.

**Expressions:**
- Client: slightly tense, but willing.
- Kai: watching without interfering. Evaluating.

**Environment:** Training bay or open floor area. Similar to CG 1 but with a different spatial dynamic — Kai at a distance now.

**Lighting:** Standard gym lighting.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Modern gym interior. In the foreground: MC (back or three-quarter back to camera, in trainer role) faces a new client — an early-20s gym-goer, slightly nervous energy in their posture, willing but not comfortable yet. They're mid-conversation or MC is about to begin an assessment. The space between them is professional. In the far background: Kai (mid-30s female trainer, technical wear) stands watching from a distance — arms loosely crossed or at her sides, deliberately not intervening, evaluating. The gym floor stretches between them. The reversal from CG 1 is the point: now MC is the coach, Kai is the observer.
```

---

### CG 3: `tr_npc1_planning_session.png`
**Scene:** `tr_npc1_kai`
**Purpose:** Kai and MC reviewing a training plan — the intellectual side of the work. Not on the floor, at a desk or bench with a tablet or clipboard.

**Camera:** Medium shot — Kai and MC side by side at a surface, both looking at a training plan document.

**Framing:** A tablet or printed plan on the surface between them. Kai and MC visible from the torso up, side by side.

**Characters:**
- Kai: next to MC, slightly turned toward the plan. Pointing at something on it, explaining. Her expression is the explaining-something-with-care register.
- MC: beside Kai, looking at the plan. Three-quarter angle, no face.

**Expressions:**
- Kai: engaged, teaching. Not condescending — genuinely invested in the explanation.

**Environment:** A trainer's desk area or a quiet corner of the gym — a high bench or small table. The training plan visible on the surface (no legible text). Gym floor visible in background.

**Lighting:** Slightly different from the main floor — desk area or side area. Still bright, functional.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Trainer's office area or quiet gym corner. A tablet or printed document (training programme) sits on a surface between two figures. Kai (mid-30s female, athletic build, technical wear) stands or sits beside MC, pointing at a section of the plan — her expression is focused and genuinely engaged in explaining it, not performing instruction. MC is beside her in three-quarter profile (no face), looking at the plan. Gym floor visible in the background through glass or around a partition. The document shows structured grid-like content (no legible text — just the visual format of a training programme). Bright functional lighting.
```

---

### CG 4: `tr_npc2_after_last_session.png`
**Scene:** `tr_npc2_kai`
**Purpose:** After the last session of the day. Kai and MC on the empty gym floor — the quiet honest moment.

**Camera:** Medium wide. Both figures visible in the quieter gym, late in the day.

**Framing:** The gym floor is noticeably less populated than the morning — maybe one or two other people in the background. MC and Kai standing, not training. The conversation is happening at rest, in the space where they work.

**Characters:**
- Kai: standing, slightly looser posture than during sessions. Not fully off-duty — still in the space — but the coaching register is down. Honest.
- MC: beside or slightly turned toward Kai. Three-quarter angle.

**Expressions:**
- Kai: the quiet, honest version of herself. She's saying something real, not coaching or instructing.

**Environment:** Gym floor, end of day. Quieter. Lighting might be slightly different — afternoon/evening rather than morning.

**Lighting:** Later-day gym lighting — still functional but different from morning (different sun angle through windows if applicable, or slightly warmer artificial).

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Modern gym floor, late afternoon or evening. The space is noticeably quieter than during busy hours — one or two members visible in the background, not near the two main figures. Kai (mid-30s, athletic build, technical wear) stands in the mid-foreground, posture slightly looser than during training — present but not in coaching mode. Her expression is honest and quiet, the after-the-work register. Beside or slightly turned toward her: MC (three-quarter angle, no face). They are not training, not coaching — just standing in the space where they work, having a real conversation. Later-day lighting — slightly warmer or differently angled than the morning scene.
```

---

## Character Visual Consistency — Kai

Check existing Kai sprite from the gym NPC interact system before generating new art. If a sprite exists, all CGs must match it.

- **Age:** Mid-30s
- **Build:** Athletic, practical. Visibly works in a physical profession.
- **Clothing:** Technical training wear — fitted, functional. Consistent colour scheme across scenes (suggest dark or muted tones — navy, charcoal, forest green).
- **Hair:** Athletic practicality — pulled back for sessions. Consistent across CGs.
- **Expression range:** Observational (default), explaining/engaged (planning session CG), honest/quiet (after-session CG)
- **Posture tells:** During coaching — attentive and precise. During planning — engaged and forward. After hours — looser, the work register down. Her coaching posture and her human posture are noticeably different.

## Sprite Requirements

- `kai_normal` — default gym presence, observational
- `kai_focused` — coaching/explaining mode
- Verify against existing sprite (if `npc_talkable("kai")` system uses a sprite, check the filename before generating new art).

## New Background: `gym_training_floor.png`

**Priority:** Medium — blocks CGs 1 and 2 if `gymdaypeople` doesn't serve the trainer-perspective framing.

**Description:** Modern gym floor from a standing/trainer perspective (not client POV looking up at equipment). Visible elements: a training bay (squat rack, adjustable bench, open mat space), the wider floor with other members training in the background (not in focus), natural light from windows, functional overhead lighting. The space should read as professional but accessible. Not luxury gym — working gym. Iron Gate's visual register: practical equipment, no excessive decoration, space to work in.

**Generation prompt for background:**
```
Visual novel background, 16:9 landscape, digital illustration. Modern gym interior, training floor. Standing-height observational perspective — not client POV looking up. A training bay in the centre-foreground: adjustable squat rack, flat/adjustable bench, open rubber-mat space. The wider gym floor extends behind it — other members training at other stations, out of focus. Windows along one wall with natural light (morning or afternoon). Overhead functional lighting. Equipment is practical, well-maintained but not luxury — this is a working gym. No excessive branding or decoration. The space is clean, spacious enough to work in, and has the specific energy of a place people come to consistently.
```

## Generation Priority

1. Kai sprite verification — check existing system before generating new art
2. `gym_training_floor.png` — new background blocking CGs 1 and 2
3. `tr_first_day_shadow.png` — establishes the three-figure coaching composition
4. `tr_npc2_after_last_session.png` — most emotionally significant; uses existing BG
5. `tr_task_1_solo_session.png` — role-reversal composition; depends on CG 1 visual register
6. `tr_npc1_planning_session.png` — desk/planning scene; different spatial register
