# Narrative World Audit
## LivingTheDream — Whole-Game Diagnosis

---

## 1. Overall Assessment

The game has a solid structural foundation and several genuinely strong story moments. However it currently reads as a collection of well-designed individual scenes rather than one coherent world. Careers are largely parallel minigames. NPCs rarely affect one another except in the three existing crossover scenes. Money, home tier, and relationship depth exist in separate compartments with minimal overlap. The game's best work — the Atlas project, the nora_closing_scene, the lena_rooftop — succeeds because it combines character revelation with a real decision that has consequence. Most of the game does not yet reach that standard.

---

## 2. Stories That Currently Feel Complete

**Nora** is the most fully realised NPC. She has a meeting (`location_cafe` / first encounter), a closing-time breakthrough (`nora_closing_scene`), a rent crisis that reveals her trap (`nora_rent_scene`), a culinary school announcement (`arc_nora_ambition_2` / `scene_nora_hug_school`), reactive scenes when MC disappears (`scene_nora_feels_ignored`), and a home relationship arc (coffee machine → cheap-home cooking). Multiple `add_relationship_memory` calls mean the phone screen builds a genuine history. The arc has a beginning, a middle, and a peak. What it lacks is an ending — she says yes to the programme but the game never shows what that meant.

**Corporate / Martha / Atlas** is the game's most consequential professional story. The Atlas project (`atlas_score`, `atlas_risk`, `atlas_martha_involved`, `atlas_credit_choice`) produces genuinely different outcomes that ripple forward into `corp_net_credit_hallway_done`. Martha's rooftop scene is emotionally honest. The credit-in-the-hallway callback (`corp_net_credit_hallway_done`) is an example of how delayed consequence should work throughout the game.

**IT / Eli** has clear professional structure and strong emotional payoff at the deploy hug (`scene_eli_deploy_hug`). The variant phone messages from task choices (`it_task1_followup`, `it_npc1_followup`) are well-implemented. The home relationship (side project, debug session, dinner, metal detector) gives Eli the most personal scenes outside her career of any work-NPC.

**Lena** has a rooftop scene that sets emotional stakes clearly and uses the hospital context as more than set dressing. The extended kitchen scene (`scene_kitchen_lena_extended`) after dinner is a good example of a small scene doing real character work.

---

## 3. Stories That Feel Shallow or Abruptly End

### Culinary Career
**Problem type: B (missing content) + C (weak characterisation) + D (insufficient consequence)**

The arc contains exactly five labels: `cul_first_day`, `cul_task_1`, `cul_npc1_rena`, `cul_npc2_rena`, `cul_review_commis`. All choices converge to promotion. No choice changes the relationship with Rena in a meaningful way. The three work events (`wev_cul_service_rush`, `wev_cul_ingredient_shortage`, `wev_cul_dish_criticism`) are mechanical events with no narrative frame — the player survives or doesn't, then continues. Rena has `no_decay=True`, no world schedule, no relationships with other NPCs, and no scene outside the kitchen at any point. The question Rena asks in `cul_npc2_rena` ("Why the kitchen?") is the most interesting beat in the career, but it leads nowhere — the answer changes nothing.

The culinary arc currently has no: failure state, central professional conflict, climax, consequence after promotion, or later callback in any other scene or location. It is the weakest story in the game by a significant margin.

### Zoe Exhibition
**Problem type: B (missing content)**

`arc_zoe_art_2` introduces a small gallery exhibition submission. `arc_zoe_art_3` addresses gallery funding rejection. `arc_zoe_art_4` (opening on Friday) sets `zoe_exhibition_invited = True`. But no exhibition scene exists anywhere in the codebase. The player is invited, the flag is set, and the event never fires. This is an incomplete arc with a structural hole — the invitation exists but the destination does not.

### Elle Post-Decision
**Problem type: B (missing content) + E (structural pacing)**

`scene_elle_portugal_payoff` branches on `elle_travel_2_response`: she goes, stays, or defers. The decision is made in front of the player. Memory `elle_portugal_moment` is set. Then nothing. If she goes to Portugal: the game does not acknowledge her absence. If she stays: nothing changes. The arc has setup and decision but no consequence regardless of outcome. `elle_decision_done = True` is a dead-end flag.

### Marcus Basketball
**Problem type: B (missing content — deeper scene, not dead flags)**

`arc_marcus_sports_2` establishes that Marcus had a semi-pro basketball offer at 18 that he didn't take because his father was sick. The invite flow IS wired: `new_day()` sets `marcus_basketball_invite_pending = True` once `arc_marcus_sports_2_done`, `marcus_trust >= 30`, and `day >= 20` are met; `locations.rpy` fires the bar invite scene when pending is True, creates a court commitment, and sets `marcus_basketball_invite_done = True`. The backstory does have present-tense follow-through. What is missing is the deeper authored scene — a real conversation where Marcus weighs the decision with MC — which is the substance of ARC-4. The invite mechanics work; the character depth does not yet match the setup.

### Hospital Hard Case
**Problem type: B (missing authored content — not a broken flag)**

`lena_shoulder_gesture` (`scene_lena_shoulder_gesture`) has the precondition `hospital_hard_case_pending = True`. The flag IS set: `locations.rpy` triggers it on a 25% random roll during hospital shifts when `lena_break_room_done`, `hosp_shifts >= 10`, and `job_rank >= 1` are all true; `data.rpy:560` clears it after arming `lena_shoulder_pending`. The shoulder gesture scene IS reachable. The problem is the quality of the trigger — a silent probability roll with no player-facing moment, no authored choice, and no pity mechanism. A player who works 10+ qualifying shifts may still never see the scene by RNG. ARC-1 proposes replacing that roll with an authored dramatic scene; it is a narrative improvement, not a bug fix.

### Sam
**Problem type: B (missing content) + C (weak characterisation)**

Sam's entire narrative consists of `sam_gym_scene` (reveals she used to hate the gym) and `scene_sam_marcus_park` (the court argument crossover). She has no arc topics, no `add_relationship_memory` calls beyond the court crossover, no external goal mentioned in any dialogue, no personal life outside her schedule. `sam_marcus_scene_done` exists but Sam has no story of her own. She is currently the flattest recurring NPC in the game.

### Caroline
**Problem type: C (weak characterisation) + B (missing content)**

Caroline appears in `corporate_recruit` (as the recruiter who sets `corporate_style`), `scene_caroline_thursday_bar`, and `scene_caroline_romance_open`. She has no arc in any topic conversation. The bar scene is listed as her "major scene" but its content beyond three choices is not substantial. She has no external goal, no internal conflict, no revealed life beyond HR. Her most distinctive trait from the code — the ethics scenario in `corporate_recruit` — is never revisited.

### Natalie
**Problem type: B (missing content)**

One meaningful scene (`scene_natalie_bar_offduty`), one relationship memory (`natalie_muaythai_revealed`), and warehouse work. She has no arc, no follow-through on the Muay Thai reveal, and no relationship to any other NPC. The Muay Thai coaching detail is interesting and unused.

### Kai
**Problem type: E (structural pacing problem)**

`scene_kai_cafe_quiet` is a genuinely good scene — Kai admits exhaustion from always performing the energy people pay for. But it is isolated. No scene precedes it that would make the contrast land harder. No scene follows that shows whether the admission changed anything. It is currently a character moment without a context or consequence.

---

## 4. Characters Who Feel Distinctive

- **Nora**: specific voice, specific trap (competence as prison), recurring coffee motif
- **Martha**: observer who stayed too long and knows it, specific power dynamic with MC
- **Eli**: precision as personality, thesis anxiety as real stakes, technical honesty
- **Lena**: chosen-this-knowingly, which removes complaint but not cost — specific internal position

---

## 5. Characters Who Feel Like Archetypes

- **Sam**: "enthusiastic sporty person" without individual texture
- **Rena**: "strict chef mentor" without a person underneath
- **Natalie**: "tough warehouse worker" — one unexpected detail (Muay Thai) but no depth around it
- **Caroline**: "HR person" who occasionally appears at a bar — no distinctive worldview or problem
- **Kai**: "high-energy trainer" with one exception scene that doesn't connect to a larger story

---

## 6. Relationships That Progress Only Through Statistics

- Sam: aff/trust climb via `sam_gym_scene` and greet lines, but no arc scene tracks the progress
- Rena: all progress through culinary shifts only (`_apply_trust` in career labels)
- Natalie: bar scene + warehouse work, no relationship texture beyond stats
- Every dinner guest except Lena: 3 stat points per visit, no later callback, no memory set

---

## 7. Choices That Are Currently Cosmetic

| Scene | Choices | What Actually Differs |
|---|---|---|
| `cul_task_1` | call help / push through / simplify | Different dialogue, same promotion path |
| `cul_npc2_rena` | "Why the kitchen?" answers | Stat variations only |
| `home_dinner_scene_marcus` | two choices | +4 aff vs +3 aff + trust split |
| `home_dinner_scene_zoe` | stay longer / talk about project | Stat split only |
| `home_dinner_scene_martha` | two choices | +2 trust vs +3 aff |
| `home_dinner_scene_kai` | two choices | Stat split only |
| `arc_nora_food_*`, `arc_marcus_sports_*` | topic choices | +1/+2 aff/trust, no follow-through |
| `tr_npc1_kai`, `tr_npc2_kai` | three choices | Stat split only |
| `hosp_npc1_lena` | observation choices | Stat split only |

---

## 8. Systems That Rarely Interact

**Career ↔ Home**: Career progress does not affect home dialogue. Moving to a better apartment while employed does not generate any acknowledgment from work NPCs. Nora's cheap-home cooking scene is the one exception — it is the only case where home tier gates a scene with a work-adjacent NPC.

**Career ↔ Romance**: No NPC has a line that references MC's job. No work choice affects relationship dialogue in any other location. Martha and Eli know MC professionally and romantically (potentially) but their bar/home conversations never reference the professional relationship.

**Money ↔ Story**: Stock system and casino are financially isolated. No NPC reacts to MC going broke or becoming wealthy. No scene acknowledges the bank loan. `check_collapse` fires if hunger hits zero but nothing story-meaningful triggers from financial stress.

**Car ↔ NPCs**: `car_tier` unlocks `scene_car_marcus_drive` and speeds up travel. No other NPC comments on whether MC has a car. No home-visit dialogue varies with car presence.

**Wardrobe ↔ NPCs**: `wardrobe_tier >= 2` triggers `scene_wardrobe_martha` (one scene). No other NPC reacts to wardrobe. No café or bar scene acknowledges appearance upgrades.

**Skills ↔ Non-career scenes**: `skill_music >= 5` affects `home_zoe_guitar_scene` outcome and `scene_guitar_zoe_busking`. `skill_prog` affects one IT trial branch. Otherwise skills acquired through college or work rarely affect scene availability outside the career that trained them.

**Degrees ↔ World**: College degrees are earnable but no NPC or scene acknowledges having one. `degrees` list is displayed on profile but triggers nothing.

---

## 9. Important Events Currently Forgotten Immediately

| Event | Flag Set | Later Callback |
|---|---|---|
| Atlas workforce cuts decision (`atlas_problem_done`) | `atlas_credit_choice` | Only `corp_net_credit_hallway_done` |
| Nora says yes to culinary school (`nora_hug_school_done`) | `nora_hug_school_done` | None |
| Elle decides about Portugal (`elle_decision_done`) | `elle_decision_done` | None |
| Zoe's exhibition rejection (`arc_zoe_art_3`) | `zoe_grant_discussed` | Never mentioned again |
| Lena's break room confession (`lena_break_room_done`) | `lena_break_room_done` | Only gates shoulder gesture |
| Marcus's dad being sick (`arc_marcus_sports_2`) | stored in memory implicitly | Never revisited |
| MC earns a degree | `degrees` list | No scene, no NPC line |
| Player gets a loan from the bank | `loan > 0` | No NPC or scene reacts |
| `home_coffee_calibrated` | set in coffee scene | Gates cooking scene only |

---

## 10. Where the World Waits Passively for MC

- **Nora's school decision**: `nora_school_revealed` is set when she tells MC. But nothing happens unless MC reaches the affection and trust thresholds. Nora neither enrolls nor withdraws without MC.
- **Elle's Portugal offer**: `elle_abroad_day` records when she told MC. `elle_decision_pending` is set from `new_day()` after a delay — but the decision only resolves when MC visits the beach. Elle does not decide without MC.
- **Zoe's exhibition**: She has an opening on Friday that MC is invited to. The event never fires regardless of time passing.
- **Marcus**: The basketball invite scene fires at the bar after trust and arc prerequisites are met (`arc_marcus_sports_2_done`, `marcus_trust >= 30`, `day >= 20`). The backstory does have a present-tense follow-through. The deeper authored scene — where Marcus weighs the decision with MC — is the scope of ARC-4, which is not yet implemented.
- All NPC relationships: aff/trust only change when MC initiates interaction. No NPC improves or worsens on their own except via the `nora_ignored_pending` / `last_day_worn_out` daily check, which is a reactive penalty for MC absence, not independent NPC action.

---

## 11. Career Structural Comparison

| Career | Distinct Dramatic Identity | Beginning | Central Conflict | Climax | Failure State | Post-Climax Consequence |
|---|---|---|---|---|---|---|
| Corporate | Ambition, compromise, credit | ✓ | ✓ (Atlas ethics) | ✓ (presentation) | Partial (conditional review) | ✓ (hallway credit) |
| IT | Competence + collaboration | ✓ | Partial (trial) | ✓ (deploy/promotion) | Partial (trial failure) | ✓ (deploy hug, dinner) |
| Hospital | Responsibility + cost | ✓ | Hard-case: 25% roll, no authored moment | ✓ (rooftop) | Partial (trial wrong answer) | Partial (shoulder scene: 25% roll, no pity) |
| Culinary | Unknown — hierarchy? ego? | ✓ | ✗ | ✗ | ✗ | ✗ |
| Trainer | Trust + responsibility | ✓ | ✗ | ✗ | ✗ | ✗ |

Culinary is the only career with no climax, no failure state, no post-career consequence, and no central professional conflict.

---

## 12. Home Tier Evaluation

| Tier | Distinct Experience | NPC Reactions | Activity Changes | Dialogue Variation |
|---|---|---|---|---|
| Cheap (1) | `scene_nora_cheap_home_cooking` | None from any NPC | One gated scene | None |
| Good (2) | Visual upgrade | None | None added | None |
| Rich (3) | Visual upgrade | None | None added | None |

Home tier is currently a visual reskin and a rent cost. The one exception — Nora's cheap-home cooking scene — demonstrates what tier-specific content can do: it reveals Nora's personality (she improvises on bad equipment), says something specific about the cheap home (the uneven hob, the cramped worktop), and has a prerequisite chain that makes it feel earned. That model is not replicated for tier 2 or 3 at all.

The cheap home has no embarrassment scenes. The rich home has no "pressure to maintain the lifestyle" content. No guest makes a comment about the apartment.

---

## 13. Nora Cheap-Home Cooking Evaluation

The scene (`scene_nora_cheap_home_cooking`) does three things well:
1. It reveals Nora's competence — she improvises on limited equipment without complaint
2. It says something true about the cheap home — "the hob's uneven, you've been compensating"
3. It requires a prerequisite chain (`home_coffee_calibrated`) that makes the relationship feel like it took time

What it currently lacks:
- A later callback: Nora never references the cooking lesson in any later scene
- An effect on the culinary career: if MC is doing culinary, there is no acknowledgment that Nora taught them something about working with bad equipment

One small callback would close the loop without adding a new scene: when MC next encounters Nora at the café and skill_cook >= 2, a greet-line variant or topic exchange could reference "the hob lesson."
