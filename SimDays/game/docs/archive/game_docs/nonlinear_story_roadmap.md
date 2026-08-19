# Nonlinear Story Roadmap
## LivingTheDream — Arcs, Connective Scenes, Crossovers, Priority Order

All proposals are design-only. No gameplay code is modified here.
Prerequisites are current code unless marked [NEW PREREQUISITE].

---

## SECTION 1 — Five Major Arc Additions

---

### ARC-1: Hospital Hard Case (replaces random roll with authored scene)

**Scene ID:** `scene_hospital_hard_case`
**Characters:** Lena, MC, unnamed patient
**Location:** Hospital ward
**Current prerequisite:** `lena_break_room_done`, `hosp_npc2_done` (Lena has already lost someone in Room 7)
**New prerequisite:** None — this scene should set `hospital_hard_case_pending = True`

**What this improves:** `scene_lena_shoulder_gesture` requires `hospital_hard_case_pending = True`. The flag IS set in the existing code — a 25% random roll during qualifying hospital shifts (`lena_break_room_done`, `hosp_shifts >= 10`, `job_rank >= 1`). The shoulder gesture scene is reachable, but the trigger is a silent probability roll with no player-facing moment and no pity mechanism. This scene replaces that roll with an authored dramatic choice, making the shoulder gesture feel earned rather than random.

**Conflict:** A case arrives where MC's documentation call, made in `hosp_task_1`, has a downstream consequence. Not necessarily a mistake — it could be that the conservative documentation created a diagnostic gap. Or a new case where MC sees the same ambiguity and has to decide alone. Lena is not in the room to ask.

**Player choice:** Document what you know and flag the gap / Push through with the available data / Wait for Lena.

**Immediate result:** All options resolve the case, but differently. The "flag the gap" choice produces the cleanest outcome and earns a specific line from Lena when she reviews the file. The "wait" choice delays treatment and creates a mild performance note.

**Delayed consequence:** `hospital_hard_case_pending = True` fires. Two to four days later, Lena notices MC in the hospital corridor and touches her shoulder briefly — `scene_lena_shoulder_gesture`. The touch acknowledges what happened without naming it. No speech. No debrief. The gesture is the consequence.

**State changed:** `hospital_hard_case_pending = True`, optional: `_hosp_hardcase_mc_choice` (string) affecting Lena's gesture line.

**Later callback:** `scene_lena_shoulder_gesture` fires. After that scene, the Lena trust track reaches the threshold that makes `scene_lena_romance_open` possible.

**Failure possible:** Yes — waiting for Lena produces a performance hit. But not a game-ending failure; it is a documented mistake.

**Recovery possible:** Yes — the mistake is in the record but Lena's arc continues. The shoulder gesture fires regardless of which choice was made.

**Supports:** Both platonic and romantic routes.

**Why this scene is necessary:** The shoulder gesture can currently fire — but only by surviving a 25% random roll per qualifying shift with no guaranteed pity trigger. For most players it will feel like it never fires. An authored scene makes it guaranteed and meaningful. This is the most urgent narrative improvement in the hospital arc.

**If not added:** `lena_shoulder_gesture` remains accessible only via RNG, with no authored moment creating the context that makes the gesture land.

---

### ARC-2: Culinary Service Failure

**Scene ID:** `scene_cul_service_crisis`
**Characters:** Rena, MC, implied customers
**Location:** Kitchen
**Current prerequisite:** `cul_task_1_done`, `cul_npc1_done`
**New prerequisite:** None — fires at a scheduled shift after npc1 (knife correction) is done

**What this fixes:** The culinary arc has no climax, no failure state, and no moment where MC's understanding of what Rena was teaching is tested.

**Conflict:** Saturday service. A key component for the signature dish isn't there — or arrives wrong. Rena is managing a different station. MC has to decide without her and the result is visible to the dining room. This is not a solvable problem that leads to the same outcome; the choices produce genuinely different results.

**Player choice:**
- Substitute the component confidently — if `skill_cook >= 3`: the substitute works. If not: the dish is wrong.
- Stop the dish and tell the table it's unavailable — the table is disappointed but nothing fails visibly.
- Ask Rena mid-service — she handles it but there is a cost. Her trust goes up (you asked at the right moment) or down (you asked at the wrong moment, based on a second sub-choice).

**Immediate result:** Varies. The confident substitute with low skill produces a returned dish (`wev_cul_dish_criticism` is already in the work-event pool — this would be a story version). The stop-the-dish option costs aff but gains trust. Asking Rena correctly costs pride but gains relationship.

**Delayed consequence:** Rena's reaction in `cul_npc2_rena` ("Why the kitchen?") hits differently depending on this outcome. If MC substituted successfully: she acknowledges it without praise. If the dish was returned: the "why the kitchen?" question is harder to answer and the answer matters more. If MC asked correctly: Rena gives the question with a different register — less testing, more genuine.

**State changed:** `cul_service_crisis_done = True`, `_cul_crisis_outcome` (string: "substitute_success", "substitute_fail", "stopped", "asked_right", "asked_wrong")

**Later callback:** `cul_review_commis` — Rena's promotion speech varies by `_cul_crisis_outcome`. "You know what not to do" is different from "You made the call."

**Failure possible:** Yes — substitute with low skill produces a real failure. Performance is hit. But not a career-ending event.

**Recovery possible:** Yes — the promotion path continues. The outcome affects dialogue, not the gate.

**Supports:** Culinary career only, but Rena relationship affects friendship path.

**Why this scene is necessary:** Without a failure state, the culinary career has no stakes. Every choice leads to the same promotion. The crisis makes the kitchen mean something.

**If not added:** Culinary continues as the game's only career with no dramatic identity, no consequence, and no reason to prefer one choice over another.

---

### ARC-3: Zoe Exhibition Opening

**Scene ID:** `scene_zoe_exhibition_opening`
**Characters:** Zoe, MC, implied gallery visitors
**Location:** Small gallery (new location or existing `nadbrzeze` area)
**Current prerequisite:** `zoe_exhibition_invited = True`, `arc_zoe_art_4` completed
**New prerequisite:** MC must have been present for at least one of: `scene_guitar_zoe_busking`, `zoe_beach_night_scene`, or `scene_eli_meets_zoe` — i.e., MC has seen Zoe's creative side, not just her social side.

**What this fixes:** `zoe_exhibition_invited = True` is set in the code. The opening is announced in `arc_zoe_art_4`. No scene exists. This is the only arc in the game where an explicit invitation leads nowhere.

**Conflict:** Zoe has work on the walls. People are looking at it. She is performing calm. The work is personal — the sketchbook series, probably including drawings of people whose faces are partly absent. The player is one of the people in the room. Whether MC recognizes themselves in a drawing is a choice: ask or not ask.

**Player choice:**
- "Is one of these mine?" — Zoe answers honestly. The answer is "yes" or "eventually" depending on relationship state.
- Say something about the work itself — she takes it seriously, responds specifically.
- Stay close without analyzing — she notices, appreciates it later.

**Immediate result:** +3–5 aff/trust depending on choice and relationship state. Memory: `("zoe", "zoe_exhibition_opening", "The gallery opening")`.

**Secondary result (branching on arc context):** If the grant was rejected (`arc_zoe_art_3`) and this show is a subsequent attempt: the outcome of this show — two pieces sold / one sold / none sold — should be determined by a simple roll weighted by relationship depth. This is not a skill check. It reflects whether Zoe took the risk with or without support.

**Delayed consequence:** One follow-up phone message from Zoe the next day, varying by outcome. Not long — one line about something specific she noticed at the opening. Sets `zoe_gallery_followup_sent = True`.

**State changed:** `zoe_exhibition_done = True`, `_zoe_exhibition_outcome` (string), relationship memory set.

**Later callback:** The exhibition outcome should surface once in a later conversation — specifically if Zoe returns to the gallery theme in any future arc content. "That show" becomes a reference point.

**Failure possible:** The show can go quietly (no sales) without being a disaster. Zoe handles it. The choice is how she handles it — alone or with MC present.

**Recovery possible:** N/A — the show is not a failure state, only an outcome.

**Supports:** Both platonic and romantic routes.

**Why this scene is necessary:** An invitation has been issued and recorded. Not attending is not a player choice — it is a missing scene. The Zoe arc currently ends at almost-moment (`scene_zoe_spontaneous`), which is a strong emotional peak with no grounded creative payoff. The exhibition is the grounding.

**If not added:** `zoe_exhibition_invited` is set and nothing follows. The arc's invitation arc ends in a dead flag.

---

### ARC-4: Marcus and the Basketball Question

**Scene ID:** `scene_marcus_basketball_question`
**Characters:** Marcus, MC
**Location:** Park or bar (triggers in either)
**Current prerequisite:** `arc_marcus_sports_2_done` (the backstory is established), `marcus_trust >= 30`
**New prerequisite:** None — `marcus_basketball_invite_pending` is already set by `new_day()` once prerequisites are met. `marcus_basketball_invite_done = True` is set when the existing bar invite scene fires.

**What this adds:** The basketball invite mechanics ARE implemented — `new_day()` sets `marcus_basketball_invite_pending`, the bar fires the invite scene, a court commitment is created, `marcus_basketball_invite_done` is set. What does not exist is the deeper authored conversation: a scene where Marcus weighs the decision with MC, where MC's response actually matters to the outcome.

**Conflict:** Marcus mentions someone reached out. A veterans' league, a community coaching slot, a pickup team that reformed. Something low-stakes enough to be real. He's not asking for permission. He's mentioning it. The question MC faces is what to say to someone who is clearly still not sure.

**Player choice:**
- "You should go. You obviously want to." — He pushes back slightly, then considers.
- "What do you actually want from it?" — He doesn't answer immediately. This is the right question and he knows it.
- "It's been a while. Might be different now." — He agrees. This ends the conversation sooner than it should.

**Immediate result:** +2–4 trust depending on choice. The choice that doesn't give a quick answer (+4 trust) leaves the conversation unresolved — which is the honest version.

**Delayed consequence:** One to two weeks later, Marcus mentions in a bar or park encounter what he decided. The decision should differ based on MC's response. MC's trust level with Marcus also affects whether he comes back to MC with the result.

**State changed:** `marcus_basketball_invite_done = True`, `_marcus_basketball_decision` (string: "going", "not_going", "still_thinking").

**Later callback:** If `_marcus_basketball_decision == "going"`: one later park morning where Marcus is tired in a way he's not usually tired, and mentions the first session. Small. Specific. One line.

**Failure possible:** No — this is a conversation, not a performance. All outcomes are valid.

**Recovery possible:** N/A.

**Supports:** Platonic only (Marcus is not currently romanceable).

**Why this scene is necessary:** The basketball invite fires — but as a functional mechanical event, not a character moment. Marcus asks MC to come to court. MC goes. No conversation about why he's doing it, whether he's sure, what it costs him to try again. The backstory from `arc_marcus_sports_2` earns its setup only when there's a real authored scene that tests MC's relationship with him.

**If not added:** Marcus's basketball history remains a detail without weight — the invite fires, the court commitment completes, and nothing is said about what it means.

---

### ARC-5: Sam as a Person

**Scene ID:** `scene_sam_off_routine`
**Characters:** Sam, MC
**Location:** Gym or café (outside the park morning)
**Current prerequisite:** `sam_gym_done`, `sam_trust >= 20`
**New prerequisite:** None

**What this fixes:** Sam has no arc, no external goal, no personal life established beyond her schedule and her enthusiasm. She is the flattest recurring NPC in the game.

**Conflict:** MC encounters Sam somewhere off her routine — at the café on a day she doesn't usually come, or at the gym at a different time. She's had a bad morning. Not dramatic — she missed her run. For Sam, this is disproportionately affecting her. She mentions it in a way that reveals the routine is structural, not just habitual.

**Player choice:**
- "One missed run doesn't mean anything." — She agrees too quickly. This is the wrong answer.
- "What happens when you don't go?" — She describes it specifically. The description reveals more than she intended.
- "You probably needed the sleep." — She laughs. This is kind and also slightly off. She doesn't answer directly.

**Immediate result:** +2–3 trust. Memory: `("sam", "sam_off_routine", "Off schedule at the café")`.

**Delayed consequence:** The next time MC encounters Sam at the park, she's back to the morning routine. But she acknowledges that MC asked the right question. This doesn't need to be long — one greet line variant if `sam_off_routine_done = True`.

**State changed:** `sam_off_routine_done = True`, relationship memory set.

**Later callback:** Greet line variant at park: instead of "You run, or just admiring?" she says something that acknowledges the café conversation.

**Failure possible:** No — a gentle conversation with no performance stakes.

**Recovery possible:** N/A.

**Supports:** Platonic primarily; Sam's romantic path shouldn't open until she has an arc.

**Why this scene is necessary:** Sam currently has no texture beyond enthusiasm and consistency. This scene gives her one specific human problem — the routine as identity — that the player can engage with or not. It requires no CG, no new location, and minimal writing.

**If not added:** Sam remains a presence without a person.

---

## SECTION 2 — Eight Connective Scenes

---

### CONN-1: Nora School Callback

**Scene ID:** `scene_nora_school_first_week`
**Characters:** Nora, MC
**Location:** Café
**Prerequisite:** `nora_hug_school_done`, 14+ days elapsed
**Conflict:** None — this is a quiet moment. Nora mentions one specific thing that is harder than expected, and one that is easier.
**Player choice:** Ask the hard thing or the easy thing.
**State changed:** `nora_school_started_callback = True`; `add_relationship_memory("nora", "nora_school_week_one", "First week of the programme")`
**Purpose:** Closes the arc gap. "She said yes" currently goes nowhere. This costs minimal writing.

---

### CONN-2: hospital_hard_case_pending Authored Moment (prerequisite improvement)

This is ARC-1 above. Listed here for cross-reference: `hospital_hard_case_pending` IS set in the current code (25% random roll during qualifying hospital shifts), but the shoulder gesture is effectively unreliable for most players. ARC-1 replaces the random roll with `scene_hospital_hard_case` — a guaranteed authored scene. This makes the shoulder gesture, and the romance-open path with Lena that follows it, reliably reachable.

---

### CONN-3: Home Upgrade Reaction — One NPC

**Scene ID:** `scene_home_upgrade_nora` (or Eli)
**Characters:** Nora or Eli, MC
**Location:** Home (player's new tier-2 or tier-3 apartment)
**Prerequisite:** `apartment_tier >= 2`, NPC visits via existing commitment (dinner, coffee, side project)
**How it works:** Add a `if apartment_tier >= 2 and not home_upgrade_nora_reacted:` check at the start of any home scene with Nora or Eli. One added line of dialogue acknowledging the different space. No extra scene label needed.
**State changed:** `home_upgrade_nora_reacted = True` (or per-NPC flag)
**Purpose:** Currently no NPC reacts to apartment tier in any home scene. This is the minimum to make the home feel like it exists in the world rather than just as a background.

---

### CONN-4: Career Acknowledgment Outside Work

**Scene ID:** No new label — modify existing greet logic
**Characters:** Eli (bar or library), Martha (bar)
**How it works:** Add a conditional greet-line variant that fires once when MC has been promoted (`job_rank >= 1`) and the NPC hasn't yet acknowledged it. Eli's variant: "I heard you moved off the junior track." Martha's: "So. Senior. I expected that." Both fire once, set a flag, and return to normal greet logic.
**State changed:** `eli_acknowledged_promo = True`, `martha_acknowledged_promo = True`
**Purpose:** Currently work and social exist in completely separate compartments. These NPCs know MC professionally. One acknowledgment line per NPC costs four lines of dialogue.

---

### CONN-5: Zoe Exhibition Rejection Callback

**Scene ID:** Modify `arc_zoe_art_3` or add one follow-up message
**Characters:** Zoe, MC
**Prerequisite:** `zoe_grant_discussed = True`, 7+ days elapsed
**How it works:** Queue a phone message from Zoe that references the rejection — not to dwell on it, but to announce the next step. "Submitted to the Hartfield. Different selectors." This sets context for `arc_zoe_art_4` and makes the rejection feel like a chapter rather than a dead end.
**State changed:** `zoe_rejection_followup_sent = True`
**Purpose:** `arc_zoe_art_3` (rejection) and `arc_zoe_art_4` (next submission) are arc arc labels with no bridge between them. The callback provides the bridge without requiring a new scene.

---

### CONN-6: Elle Post-Decision Callback

**Scene ID:** Add a follow-up phone message or one short beach line
**Characters:** Elle, MC
**Prerequisite:** `elle_decision_done = True`, 10+ days elapsed
**How it works:**
- If `elle_travel_2_response == "take_it"` (going to Portugal): phone message mentioning one specific thing she saw in the first week — brief, personal, not dramatic.
- If `elle_travel_2_response == "what_miss"` (staying): one café or beach line where she acknowledges she's still here and it was a choice.
- If `else` (deferring): phone message noting the deadline passed and she's still thinking.
**State changed:** `elle_decision_callback_done = True`
**Purpose:** `elle_decision_done` is currently a terminal flag. The decision the player influenced has no echo.

---

### CONN-7: Nora Cooking / Culinary Career Crossover

**When:** If `nora_cooking_state == "done"` and MC is in culinary career (`job_id == "culinary"`)
**How it works:** Add a single conditional line to the culinary work event `wev_cul_service_rush` (table of 6, scale pasta immediately). If `nora_cooking_state == "done"`: an additional narrator line — "You remember what Nora said about the uneven hob. You've been compensating for something for weeks without noticing." +1 to the relevant outcome.
**State changed:** None new — flag already exists.
**Purpose:** The Nora cooking lesson currently has no later consequence anywhere. This uses an already-written work event to provide one small callback without building a new scene.

---

### CONN-8: Rena Outside the Kitchen

**Scene ID:** `scene_rena_bar`
**Characters:** Rena, MC
**Location:** Bar (weekend)
**Prerequisite:** `cul_npc2_done`, Rena trust >= 20
**Conflict:** Rena is off duty. She doesn't want to talk about the kitchen. She asks MC one question about something unrelated to cooking. The player responds.
**Player choice:** Answer the question / redirect to the kitchen / ask her the same question back.
**State changed:** `rena_bar_scene_done = True`, `add_relationship_memory("rena", "rena_off_duty", "Off the clock")`
**Purpose:** Rena currently has no world schedule and no scene outside the kitchen. This one scene makes her a person. Without it she remains a function: the chef mentor who appears when you work, disappears when you don't.

---

## SECTION 3 — Six NPC Crossover Callbacks

---

### CROSS-1: Eli + Zoe Follow-up

**Prerequisite:** `eli_meets_zoe_done = True`, 14+ days elapsed
**How it works:** In a subsequent bar or Hub conversation, Eli mentions Zoe once. "Your friend. The artist. She sent me something." Nothing elaborate — Eli read an article Zoe referenced. Or: in a Zoe arc arc conversation, Zoe mentions Eli. "Turns out she's thought about generative art more than most artists have. Which is annoying."
**State changed:** `eli_zoe_followup_done = True`
**Purpose:** `scene_eli_meets_zoe` currently fires and ends. The friendship implied by the exchange ("they exchanged contacts without you suggesting it") has no subsequent existence. One callback proves the world continued.

---

### CROSS-2: Nora + Kai Aftermath

**Prerequisite:** `nora_kai_crossover_done = True`
**How it works:** Next time MC encounters Nora at the café after the crossover, one optional topic — "Kai comes in here?" — lets Nora mention that Kai has been asking about something. Or: Kai's next café encounter (`scene_kai_cafe_quiet`) has one additional line if the crossover is done: "Nora makes a decent latte. Don't tell her I said that."
**State changed:** None new — add conditional branch to existing scenes.
**Purpose:** The flat white argument is one of the game's best small moments. Currently it fires and both NPCs forget it happened.

---

### CROSS-3: Sam + Marcus After the Court

**Prerequisite:** `sam_marcus_scene_done = True`, 7+ days elapsed
**How it works:** In a park morning encounter with Marcus after the court scene, Marcus mentions Sam once: "Sam came back Wednesday. We had a rematch. She's right about the reps." One line. No new label.
**State changed:** None — conditional within existing greet or talk logic.
**Purpose:** The court argument has memories set for both NPCs but no subsequent acknowledgment that the relationship between them continued.

---

### CROSS-4: Marcus + Caroline (Bar, Thursday)

**Prerequisite:** `marcus_met`, `caroline_bar_done`, both in bar location Thursday 19–22
**How it works:** One background observation line when MC encounters Marcus at the Thursday bar on a night Caroline is also scheduled there. "Is that— do you know her? She's in here every Thursday." Marcus doesn't know her by name. This is not a crossover scene — it is a one-line acknowledgment that both NPCs share a location.
**State changed:** None — purely observational.
**Purpose:** The world currently has no overlap between the work NPCs and the social NPCs. Both Marcus and Caroline are at the Thursday bar. One line confirms the world is one space.

---

### CROSS-5: Nora + Elle (Café)

**Prerequisite:** `elle_pier_done`, `nora_closing_done` (both relationships established)
**How it works:** MC encounters Elle at the café on a Tuesday or Thursday when Nora is working. Nora's service line to Elle is one sentence: "The usual?" Elle has a usual. This is the smallest possible crossover — it exists to confirm that Nora and Elle occupy the same space. If MC asks Elle later about the café, she mentions Nora by name.
**State changed:** `nora_elle_acknowledged = True` (simple flag)
**Purpose:** Elle and Nora have overlapping schedules (Elle: Tue/Thu 9–13 at café; Nora: Mon–Fri 7–16 at café). They share a space every week and the game currently acts as if they have never met.

---

### CROSS-6: Martha + Lena (Workplace Proximity)

**Prerequisite:** `martha_rooftop_done`, `lena_rooftop_done`
**How it works:** Not a scene — a piece of dialogue. In a bar or terrace encounter with Martha after both rooftop scenes are done, Martha mentions a doctor she knows who works brutal hours. She doesn't use a name. MC can choose whether to make the connection or let it pass. This confirms that Martha and Lena exist in the same world without requiring them to meet on screen.
**State changed:** `martha_lena_reference_done = True`
**Purpose:** Martha and Lena are the two NPCs whose rooftop confessions are the game's strongest character moments. Both are professional women in demanding roles who stayed past a version of themselves. Acknowledging that they share a world — even obliquely — deepens both.

---

## SECTION 4 — Priority Roadmap

### P0 — Structural Problems That Undermine Current Content

| # | Problem | Characters/Systems | Dependency | Scope |
|---|---|---|---|---|
| P0-1 | `hospital_hard_case_pending` set by 25% roll only → shoulder gesture unreliable | Lena, hospital career | ARC-1 | Small |
| P0-2 | Basketball invite fires but has no authored character conversation | Marcus | ARC-4 | Small |
| P0-3 | `zoe_exhibition_invited` set but no exhibition scene | Zoe | ARC-3 | Medium |
| P0-4 | Culinary arc has no climax, failure state, or consequence | Rena, culinary career | ARC-2 | Medium |

All P0 items involve existing flags or code that points to missing content. P0-1 is the most urgent because it gates an already-written scene.

### P1 — Missing Arc Middles, Endings, and Cross-System Connections

| # | Problem | Characters/Systems | Dependency | Scope |
|---|---|---|---|---|
| P1-1 | Nora says yes to culinary school; nothing follows | Nora | CONN-1 | Small |
| P1-2 | Elle's Portugal decision has no aftermath | Elle | CONN-6 | Small |
| P1-3 | Sam has no personal arc or external goal | Sam | ARC-5 | Small |
| P1-4 | Marcus basketball invite fires mechanically but without authored character conversation | Marcus | ARC-4 | Small |
| P1-5 | Home tier is a visual reskin; NPCs never react | Home system, all NPCs | CONN-3 | Small |
| P1-6 | Career and social exist in completely separate compartments | Eli, Martha, career system | CONN-4 | Small |
| P1-7 | Rena has no existence outside the kitchen | Rena, culinary career | CONN-8 | Small |

### P2 — Depth, Variation, and Cinematic Enrichment

| # | Problem | Characters/Systems | Dependency | Scope |
|---|---|---|---|---|
| P2-1 | Crossover friendships fire once and are never referenced again | Eli+Zoe, Nora+Kai, Sam+Marcus | CROSS-1/2/3 | Small |
| P2-2 | World NPCs don't share space with work NPCs | Marcus+Caroline, Nora+Elle | CROSS-4/5 | Small |
| P2-3 | Nora cooking lesson has no callback in any later scene | Nora, culinary career | CONN-7 | Small |
| P2-4 | Zoe exhibition rejection acknowledged but not bridged | Zoe | CONN-5 | Small |
| P2-5 | Caroline has no personal arc or human problem | Caroline | Character bible proposal | Medium |

### Top 10 by Value (cross-cutting)

1. **P0-1** — Replace random `hospital_hard_case_pending` roll with authored scene (ARC-1). Makes the shoulder gesture reliable and meaningful.
2. **P0-4** — Culinary climax scene (ARC-2). Fixes the only career with no dramatic stakes.
3. **P0-3** — Zoe exhibition opening (ARC-3). Closes the only arc with a literal dead invitation.
4. **P1-1** — Nora school callback (CONN-1). Two scenes of writing; closes a narrative gap the player notices.
5. **P0-2 / P1-4** — Marcus basketball question (ARC-4). Gives the existing mechanical invite real authored weight.
6. **P1-3** — Sam scene (ARC-5). Minimum to make Sam a character rather than a presence.
7. **P1-6** — Career acknowledgment in social (CONN-4). Two greet-line variants; fixes the career-social wall at minimal cost.
8. **P1-5** — Home upgrade NPC reaction (CONN-3). One conditional per home scene with Nora or Eli; minimal cost.
9. **P1-7** — Rena bar scene (CONN-8). Makes the culinary mentor a person in the world.
10. **CROSS-1** — Eli + Zoe follow-up (CROSS-1). Two-line callback that confirms the world continued after the crossover.

### Implementation Order Recommendation

Write ARC-1 first (it makes the shoulder gesture reliable and gives the hospital arc a real authored climax moment). Write CONN-1, CONN-3, CONN-4 concurrently (all small, no asset dependencies). Write ARC-2 before generating any new culinary CGs — the scene is necessary to know what the CG should show. Write ARC-3 (Zoe exhibition) after confirming the scene design, then commission the gallery CG. Write ARC-4 and ARC-5 last — they require the least infrastructure but are medium-complexity character work.

Do not generate CGs for culinary, Zoe exhibition, or Marcus basketball until the scene design is confirmed and the owner has approved the story direction. Visual assets generated before the story is settled will constrain the writing.
