# Cinematic Scene Backlog
## LivingTheDream — Narratively Justified CG and Scene Proposals

Each scene here exists because the story needs it, not to pad the CG count.
No CG is commissioned on the strength of this document alone — all proposals
require confirmed scene design before any asset is requested.

Classification:
- **A — Full CG** (single authored illustration, specific characters in specific action)
- **B — Sequence CG** (2–4 frames with expression/pose variation)
- **C — Background variation** (existing sprites on a new BG, or an existing BG with lighting variant)
- **D — Narration beat** (no CG, visual impact through prose + ambient change)

---

## ACTIVE CG SEQUENCES (already in codebase)

| ID | Characters | CG | Status | Replayable | Gate |
|---|---|---|---|---|---|
| eli_side_project | Eli, MC | 1 CG | Implemented | No | `message_already_queued` permanent |
| eli_deploy_hug | Eli, MC | 1 CG | Implemented | No | `eli_deploy_done` permanent |
| zoe_guitar | Zoe, MC | 1 CG | Implemented | No | `message_already_queued` permanent |
| martha_rooftop | Martha, MC | Declared | Implemented | No | `martha_rooftop_done` permanent |
| lena_rooftop | Lena, MC | Declared | Implemented | No | `lena_rooftop_done` permanent |
| eli_meets_zoe | Eli, Zoe, MC | Declared | Implemented | No | `eli_meets_zoe_done` permanent |
| nora_closing | Nora, MC | Declared | Implemented | No | `nora_closing_done` permanent |
| nora_hug_school | Nora, MC | Declared | Implemented | No | `nora_hug_school_done` permanent |
| lena_shoulder_gesture | Lena, MC | Declared | Reachable (25% roll) | No | Set by 25% roll in qualifying shifts; no authored scene |
| nora_cheap_home_cooking | Nora, MC | Declared | Implemented | No | `nora_cooking_state == "done"` |
| scene_zoe_spontaneous | Zoe, MC | Declared | Implemented | No | `zoe_spontaneous_done` permanent |
| wardrobe_martha | Martha, MC | Declared | Implemented | No | `wardrobe_martha_done` permanent |
| car_marcus_drive | Marcus, MC | Declared | Implemented | No | `car_marcus_done` permanent |
| sam_marcus_park | Sam, Marcus, MC | Declared | Implemented | No | `sam_marcus_scene_done` permanent |

---

## PROPOSED CG SEQUENCES (this document)

---

### PROP-CG-1: Hospital Hard Case — `scene_hospital_hard_case`

**Classification: D — Narration beat (no illustration required)**

**Characters:** MC, Lena (background, not present in room)
**Location:** Hospital ward (existing `hospital_ward` background)
**Trigger:** After `lena_break_room_done`, within hospital shift
**CG count:** 0 (no new CG; visual interest through sprite positioning and narration)

**Shot list:**
1. `scene hospital_ward` — empty corridor, night lighting. Narrator line: internal monologue while standing outside a room with a chart.
2. Show MC sprite (neutral/worried). No NPC present. The choice plays in narration, not conversation.
3. One sound cue — footsteps of the patient's family in the corridor, not shown.
4. Narrator line confirming what MC wrote in the chart.
5. `scene_lena_shoulder_gesture` fires 2–4 days later per existing code.

**Asset requirements:** None new. Uses `hospital_ward` BG at an existing lighting state.

**Why no CG:** The scene's emotional weight is in MC's internal decision. A CG of MC at a desk is inert. The shoulder gesture (already written) is the payoff — it needs no illustration companion.

**Justification:** `hospital_hard_case_pending` IS set in the current code (25% random roll during qualifying hospital shifts). This scene replaces that roll with a guaranteed authored moment — making the shoulder gesture reliably reachable and narratively earned rather than random.

---

### PROP-CG-2: Zoe Exhibition Opening — `scene_zoe_exhibition_opening`

**Classification: A — Full CG**

**Characters:** Zoe, MC, gallery background
**Location:** Small gallery (new background: `gallery_evening`)
**Trigger:** `zoe_exhibition_invited = True`, 4–7 days elapsed, player visits on Friday evening
**CG count:** 1 (Zoe standing before a wall of work, half-turned toward MC)

**Shot list:**
1. `scene gallery_evening` — warm light, white walls, Zoe's work partially visible. (New BG required.)
2. Zoe sprite (showing at right): `zoe_smart_normal` or `zoe_smart_smile`. Work visible behind her.
3. **CG beat** — Zoe is standing at an angle to the nearest work. Not posing. Caught mid-conversation with someone who is leaving. She looks toward MC.
4. Player choice lines (three options, narrated perspective).
5. Zoe moves to stand near MC. Sprite only from this point.

**CG specifications:**
- Format: full-width wide shot (not a close-up)
- Composition: Zoe left-centre; abstract or mostly-abstract canvases on the right half of the frame; warm gallery lighting; MC implied by the direction of Zoe's look
- Pose: Zoe relaxed but self-conscious, holding something (a glass or a catalogue — artist at own opening, not performing confidence)
- Art style: same style as existing CGs

**New asset required:** `gallery_evening` background (white walls, warm track lighting, abstract canvases). Could be derived from `nadbrzeze_day` architecture if they share an aesthetic; confirm with art director.

**Why this CG:** The exhibition is Zoe's creative identity made visible and public. The moment is about MC witnessing her work as a completed thing, not a process. That shift — from sketchbook to gallery wall — justifies a single authored illustration.

**Justification:** `zoe_exhibition_invited = True` is set in the existing codebase. An invitation exists with no destination. This closes the gap.

---

### PROP-CG-3: Culinary Crisis Outcome — `scene_cul_service_crisis`

**Classification: B — Sequence CG (2 frames)**

**Characters:** MC (implied, POV), Rena
**Location:** Kitchen (existing `restaurant_kitchen` BG)
**Trigger:** After `cul_npc1_done`, scheduled kitchen shift
**CG count:** 2 frames (one per major outcome branch: recovery / returned dish)

**Shot list — Frame 1 (recovery outcome):**
- `scene restaurant_kitchen` at full service lighting (warm, busy)
- MC POV: plated dish in foreground, Rena at the pass in background
- Rena is facing the pass, not looking at MC; she is not acknowledging the recovery directly
- CG shows the gap between them as spatial: the dish is between MC and Rena, and that's all that's said

**Shot list — Frame 2 (returned dish outcome):**
- Same BG at the same lighting
- Rena has turned. She is looking at MC. Not angry — she is the kind of person who assesses, not accuses.
- The expression is flat. This is the "I saw what happened" moment.

**Both frames are the same commission — different expression/pose for Rena.**

**CG specifications:**
- Wide enough to show both MC position and pass/service window
- Rena in chef whites; expression differs per frame (neutral-approving vs. neutral-assessing)
- No additional characters required — the customers are implied, not shown

**New asset required:** None — `restaurant_kitchen` background already exists (confirm name with art director). If it does not exist, use a warm commercial kitchen reference similar to the existing cheap_home_cooking CG.

**Why this CG:** The culinary career has no visual climax. Every other career has at least one authored illustration at its peak moment. This scene is the first time MC's choices in the kitchen produce a visible consequence.

**Justification:** This fixes the culinary arc's dramatic deficit. The crisis scene is the career's first failure state. A 2-frame CG is the minimum visual acknowledgment this moment needs.

---

### PROP-CG-4: Hospital — Lena Shoulder Gesture — `scene_lena_shoulder_gesture`

**Classification: A — Full CG**
**Status: ALREADY DECLARED in the codebase — this entry is a reminder that the CG is planned, not a new proposal.**

**Characters:** Lena, MC
**Location:** Hospital corridor
**Prerequisite:** `hospital_hard_case_pending = True` (currently set by a 25% random roll; ARC-1 / PROP-CG-1 replaces the roll with a guaranteed authored scene)

This scene and its CG are part of the existing design. It is reachable in the current code via the random roll, but ARC-1 makes it reliably accessible. Once ARC-1 is implemented, this sequence fires without any additional asset work.

**Shot list (from existing code description):**
- Hospital corridor (existing BG)
- Lena approaches; MC does not initiate the contact
- Lena touches MC's shoulder briefly — the gesture acknowledges the hard-case decision without naming it
- No dialogue

**Asset status:** CG declared. Do not recommission — confirm with art director that the asset exists and is in the image directory.

---

### PROP-CG-5: Marcus Basketball Question — `scene_marcus_basketball_question`

**Classification: D — Narration beat (no illustration required)**

**Characters:** Marcus, MC
**Location:** Park (existing `park_day` or `park_evening` BG) or bar
**CG count:** 0

**Shot list:**
1. Park bench or bar booth. Marcus is not looking at MC when he brings it up.
2. Sprites only: `marcus_sport_normal` → `marcus_sport_thinking` (or equivalent expressions).
3. The three player choice options in a standard menu with three dialogue lines.
4. Sprite reaction per choice; then Marcus exits or the conversation moves to another topic.
5. No CG beat required — the scene's weight is in the conversation, not the image.

**Why no CG:** The basketball question is about something not yet decided. A CG implies a moment of action or revelation that would be premature here. If Marcus decides to go back (ARC-4 delayed consequence), that first practice scene — exhausted Marcus in the park — could justify one small CG. That is a future proposal, after the arc is written.

**Justification:** The scene costs no art assets. The basketball invite mechanics are already wired (`new_day()` sets the pending flag; the bar fires the invite; a commitment is created). What is missing is the authored conversation — Marcus weighing the decision with MC. This scene provides that. It should be written and implemented before a CG is considered.

---

### PROP-CG-6: Sam Off Routine — `scene_sam_off_routine`

**Classification: D — Narration beat (no illustration required)**

**Characters:** Sam, MC
**Location:** Café or gym at off-schedule time
**CG count:** 0

**Why no CG:** This scene's purpose is to establish Sam as a person, not to mark a milestone relationship moment. A CG would signal this as a major arc beat, which overstates its role. The scene should be natural and low-register — a CG would make it feel like an event when it should feel like an encounter.

**Future CG possible:** If Sam receives a full arc and a breakthrough scene (equivalent to `nora_closing` or `lena_rooftop` for her), that breakthrough would justify a CG. This scene is the setup, not the payoff.

---

## DEFERRED CG PROPOSALS (dependent on confirmed design)

These are identified as potential CG moments but should not be commissioned until the scene design is confirmed and agreed.

| Proposed ID | Characters | Type | Condition |
|---|---|---|---|
| `scene_rena_bar` | Rena, MC | D (no CG) | After CONN-8 scene design is confirmed |
| Marcus first practice callback | Marcus | C (lighting variant) | After ARC-4 delayed consequence is written |
| `scene_sam_arc_breakthrough` | Sam | A (full CG) | Only if a Sam arc is designed and confirmed |
| Caroline bar ethics revisit | Caroline, MC | D (no CG) | After Caroline arc design is confirmed |
| `scene_nora_school_first_week` | Nora, MC | D (no CG) | After CONN-1 is written |
| `nora_elle_crossover` | Nora, Elle | D (no CG) | After CROSS-5 conditional check is confirmed |

---

## ASSET CHECKLIST

| Asset | Status | Required for |
|---|---|---|
| `gallery_evening` BG | **NEW — needs commission** | PROP-CG-2 |
| `restaurant_kitchen` BG (confirm name) | Likely exists | PROP-CG-3 |
| Rena CG frame 1 (neutral-approving at pass) | **NEW** | PROP-CG-3 |
| Rena CG frame 2 (neutral-assessing) | **NEW** | PROP-CG-3 |
| Zoe exhibition CG (wide shot, gallery) | **NEW** | PROP-CG-2 |
| `lena_shoulder_gesture` CG | Declared (confirm exists) | Already written scene |
| `hospital_ward` BG at night lighting | Likely exists — check lighting state | PROP-CG-1 |

**Minimum new assets to unlock all P0 scenes:**
- 1 new background (`gallery_evening`)
- 3 new CG frames (Zoe exhibition × 1, Rena crisis × 2)
- 0 new sprites

All other blocked or missing scenes in the P0 list require only prose and state changes.

---

## Scene Purpose Classification

This section classifies all proposed scenes by their narrative purpose, to guard against adding scenes that change nothing.

| Scene | Type | What it changes |
|---|---|---|
| `scene_hospital_hard_case` | Quality improvement | Replaces 25% random roll with authored moment; makes shoulder gesture reliable |
| `scene_zoe_exhibition_opening` | Closes structural hole | Closes `zoe_exhibition_invited` dead flag |
| `scene_cul_service_crisis` | Adds stakes | First failure state in culinary career |
| `scene_marcus_basketball_question` | Authored character scene | Gives existing mechanical invite real weight and player-facing consequence |
| `scene_sam_off_routine` | Character foundation | Sam becomes a person with one specific trait |
| `scene_nora_school_first_week` | Closes arc | Nora's "yes" has a week-one echo |
| `scene_rena_bar` | World presence | Rena exists outside the kitchen |
| Eli career acknowledgment | System crossover | Removes career-social wall for IT |
| Home upgrade NPC reaction | System crossover | Home tier acknowledged in the world |
| Zoe exhibition rejection callback | Arc bridge | Gap between `arc_zoe_art_3` and `art_4` |
| Elle post-decision callback | Arc closure | `elle_decision_done` has an echo |
| Eli+Zoe follow-up | Crossover continuity | World proves itself between scenes |
| Nora+Kai aftermath | Crossover continuity | The flat white argument has a consequence |
| Marcus+Caroline in bar | World coherence | Work NPCs and social NPCs share a space |
| Nora+Elle at café | World coherence | NPCs who share space are shown to know it |
| Martha+Lena reference | World coherence | Two strongest character arcs share a world |

All scenes either fix a structural hole, close an open flag, add a consequence to a choice, or confirm the world continues when MC is not watching. None are purely decorative.
