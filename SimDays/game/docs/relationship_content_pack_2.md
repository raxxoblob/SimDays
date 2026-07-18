# Relationship Content Pack 2 — Design Doc
_Based on relationship_scene_pacing_audit.md gaps_

---

## Overview

This pack addresses the six NPCs with the most critical arc gaps identified in the pacing audit: Caroline (zero scenes outside the corporate career mechanism), Natalie (one scene total, no breakthrough), Kai (no standalone breakthrough from any career path), Elle (arc_elle_travel_2 sets `elle_abroad_revealed` and then nothing happens), Sam (one scene, no crossover payoff despite NPC_RELATIONS marking her as gym_friends with Marcus), and Eli (explicitly absent from home_dinner_invite_menu). Every scene here uses only existing backgrounds and sprites except where a CG is justified by a standout emotional moment; the total new-art ceiling is two CGs and one background.

---

## Caroline — Off the Clock

**Scene label:** `scene_caroline_thursday_bar`
**Type:** everyday-elevated
**Narrative gap it fills:** Caroline is purely a career mechanism — she gates Martha, processes promotions, and has no scene that treats her as a person. This is the first moment the player sees her outside the office context.

### Canonical staging

- **Location:** `location_bar` (bg: `bar`) — Thursday evening
- **Time window:** 19:00–22:00 (day % 7 == 3)
- **Day restriction:** Thursday only
- **NPC outfit:** `caroline_normal` — only sprite set that exists. The formal blazer reads as slightly incongruous at the bar, which is intentional. No casual sprite exists; note this for future asset work.
- **Player requirement:** `caroline_met = True`, `caroline_affection >= 30`, `caroline_trust >= 25`

### Trigger

- **Sets** `caroline_bar_pending = True` **(new flag)** in `new_day()` when: `caroline_met and caroline_affection >= 30 and caroline_trust >= 25 and not caroline_bar_done and not caroline_bar_pending`
- **Fires** at `location_bar` when: `caroline_bar_pending and day % 7 == 3 and 19 <= hour < 22`
- **Important:** Caroline has no bar schedule entry in `NPC_DATA`. The scene fires via the pending flag directly — `npc_here("caroline")` returns False and is intentionally bypassed. She is there as a coincidence, not a schedule fact.
- **Pending pattern:** boolean (`caroline_bar_pending`, new)
- **Expiry:** 14 days. If the player does not visit the bar on a Thursday within 14 days of `caroline_bar_pending` being set, reset to False and re-evaluate next time conditions are met.

### Dependency chain

- **Requires:** `caroline_met` (set on first corporate shift) + relationship thresholds above
- **Unlocks:** nothing mechanically, but signals that Caroline is accessible as a person; sets `caroline_bar_done = True` **(new flag)** to prevent repeating

### Scene structure

1. **Opening beat.** The bar is mid-evening loud. The player spots Caroline at a corner table — a glass of something pale in front of her, a phone face-down. She sees them immediately. She doesn't pretend she didn't. "Well. If you need a seat, there's one." She does not wave them over. She simply states the fact.

2. **Core moment.** She says something small about the day ending that isn't a complaint and isn't office-speak. Not performance. Just tiredness, stated plainly. Then she asks the player a question — not HR, not corporate, not what-are-you-working-toward. Something specific and personal, which surprises the player because she has evidently been paying attention to something they mentioned in passing weeks ago.
   ```
   menu:
       "Answer honestly.":
           $ _apply_trust("caroline", 3)
           caro "That's what I thought."
           "She picks up her drink. Doesn't explain what she thought."
       "Deflect with something light.":
           $ _apply_aff("caroline", 2)
           caro "Sensible."
           "She seems to find this genuinely acceptable."
       "[Say nothing for a moment.]":
           $ _apply_trust("caroline", 2)
           $ _apply_aff("caroline", 1)
           "She nods once. Moves on."
   ```

3. **Resolution.** She finishes her drink. Stands. "I'm not in the habit of running into colleagues after hours." A pause. "But this was fine." She leaves without looking back. The player is left with the faint unsettling sense that Caroline noticed more than she ever said.

**CG:** No. The dissonance of seeing her in this location is the point; a sprite-only scene preserves it better than a produced CG would.
**New background needed:** No. Uses existing `bar`.

### Rewards

- `caroline_affection += 2–3` (depending on choice)
- `caroline_trust += 2–3` (depending on choice)
- `caroline_bar_done = True` **(new flag)**

### Fallback

If the player never triggers this scene: Caroline's relationship stalls as a professional mechanism. The hug profile (min_aff 50, min_trust 45) becomes unreachable in practice without this humanisation scene raising the affection ceiling's emotional justification. Relationship feels transactional indefinitely.

---

## Natalie — After the Whistle

**Scene label:** `scene_natalie_bar_offduty`
**Type:** breakthrough
**Narrative gap it fills:** Natalie's entire arc is a warehouse role and an optional overtime shift. This is the first scene that shows who she is when she's not managing anything.

### Canonical staging

- **Location:** `location_bar` (bg: `bar`) — weekend evening
- **Time window:** 17:00–21:00 (day % 7 in [5, 6])
- **Day restriction:** Saturday or Sunday
- **NPC outfit:** `natalie_normal` — only existing sprite; all Natalie sprites are presumably work presentation. The scene notes she's off shift without relying on a visual outfit change.
- **Player requirement:** `natalie_met = True`, `natalie_affection >= 25`, `natalie_trust >= 20`

### Trigger

- **Sets** `natalie_bar_scene_pending = True` **(new flag)** in `new_day()` when: `natalie_met and natalie_affection >= 25 and natalie_trust >= 20 and not natalie_bar_scene_done and not natalie_bar_scene_pending`
- **Fires** at `location_bar` when: `natalie_bar_scene_pending and day % 7 in [5, 6] and 17 <= hour < 21`
- Natalie IS scheduled at the bar on weekends (17–21, per `NPC_DATA`), so `npc_here("natalie")` returns True. No schedule bypass needed.
- **Pending pattern:** boolean (`natalie_bar_scene_pending`, new)
- **Expiry:** 14 days. Reset and re-evaluate if no bar visit in that window within 14 days.

### Dependency chain

- **Requires:** warehouse work to meet Natalie + relationship thresholds
- **Unlocks:** nothing mechanically. Sets `natalie_bar_scene_done = True` **(new flag)**; marks the first time trust is built outside a work context.

### Scene structure

1. **Opening beat.** Natalie is at the bar not doing anything. Drink in front of her, not talking to anyone, watching the room with the same flat attention she uses on the warehouse floor. The player sits down. She makes room without ceremony, without greeting.

2. **Core moment.** After a silence that she clearly doesn't find uncomfortable: "I coach three nights a week. Muay Thai. The gym two streets from the warehouse." She says it the same way she'd say she takes the metro — a fact, not an offer. The player is the first person from the warehouse who has ever seen this version of her. She asks the player one direct question — something she has been thinking about for a while, not an ice-breaker.
   ```
   menu:
       "Ask who she trains.":
           $ _apply_aff("natalie", 2)
           nat "Kids, mostly. Some adults who think they're tougher than they are."
           "She almost smiles."
           nat "The kids figure it out faster."
       "Ask why she coaches when she already works the longest hours on the floor.":
           $ _apply_trust("natalie", 3)
           nat "Because hauling freight pays the rent. This is the part that's actually mine."
           "A pause. She doesn't add anything to that."
       "[Don't ask. Just listen to whatever she says next.]":
           $ _apply_trust("natalie", 2)
           $ _apply_aff("natalie", 1)
           "She takes a slow drink. Then: 'The warehouse pays the bills. This is the part that stays.'"
   ```

3. **Resolution.** She finishes her drink before the player does. Stands. "Same time next weekend, if you end up here." Not an invitation. An observation about what will probably happen. She goes.

**CG:** No. The task specifies no new CG required. The existing `natalie_normal` sprite at the bar background carries the scene.
**New background needed:** No. Uses existing `bar`.

### Rewards

- `natalie_affection += 2` (baseline) + choice-dependent
- `natalie_trust += 2–3` (choice-dependent)
- `natalie_bar_scene_done = True` **(new flag)**
- `add_relationship_memory("natalie", "natalie_bar_offduty", "Off the clock")`

### Fallback

If never triggered: Natalie remains a single-dimensioned authority figure whose only scene is overtime. The hug profile (min_aff 35, min_trust 40, the highest trust threshold in the game) stays permanently unreachable for all but the most warehouse-invested players. The scene is the only humanising content in Natalie's arc.

---

## Kai — Between Sets

**Scene label:** `scene_kai_cafe_quiet`
**Type:** breakthrough
**Narrative gap it fills:** Kai has a dense weekend schedule and career arc depth, but no standalone breakthrough that works independent of the trainer career. This scene catches her in a context where physical competence is irrelevant and she has to be something else.

### Canonical staging

- **Location:** `location_cafe` (bg: `cafeday`) — Tuesday or Thursday morning
- **Time window:** 10:00–14:00 (day % 7 in [1, 3] — Kai's café schedule: Tue/Thu 10–14)
- **Day restriction:** Tuesday or Thursday
- **NPC outfit:** `kai_normal` (non-gym sprite, appropriate for café). Nora is also present (`nora_cafe_normal`).
- **Player requirement:** `kai_affection >= 35`, `kai_trust >= 25`, `kai_met = True` (met via world flag or trainer career)

### Trigger

- **Sets** `kai_cafe_quiet_pending = True` **(new flag)** in `new_day()` when: `kai_met and kai_affection >= 35 and kai_trust >= 25 and not kai_cafe_quiet_done and not kai_cafe_quiet_pending`
- **Fires** at `location_cafe` when: `kai_cafe_quiet_pending and npc_here("kai") and not nora_kai_pending`
- The `not nora_kai_pending` guard prevents this from competing with `scene_nora_kai_crossover` (both fire at the café when Kai is present). nora_kai gets priority; kai_cafe fires on a visit where nora_kai is not pending.
- **Pending pattern:** boolean (`kai_cafe_quiet_pending`, new)
- **Expiry:** 21 days (Kai's café schedule is only 2 days/week; 21 days gives ~6 windows before reset).

### Dependency chain

- **Requires:** `kai_met` + relationship thresholds. Does NOT require trainer career (`tr_*` flags), athletic cert, or `job_id == "trainer"`. Works from any career path.
- **Unlocks:** nothing mechanically. Sets `kai_cafe_quiet_done = True` **(new flag)**. Signals Kai's arc has a personal beat independent of performance.

### Scene structure

1. **Opening beat.** Kai is at the counter, coffee in hand, not in gym clothes. She's looking at her phone but not really. Nora serves her without asking what she wants — regulars tab. When the player sits down, Kai puts the phone away instead of looking up: she was waiting for the distraction.

2. **Core moment.** Something has been weighing on her — not a crisis, but a specific kind of pressure that doesn't have a training solution. She always knows what the body needs. She is less certain about what people expect her to be. "Everyone wants the energy all the time. Like if I have a flat day, I'm failing them." She's not asking for advice. She's saying it aloud, maybe for the first time.
   ```
   menu:
       "\"That sounds exhausting.\"":
           $ _apply_trust("kai", 3)
           kai "It's just part of it."
           "A pause."
           kai "But yeah. Sometimes."
       "\"You don't have to be the energy.\"":
           $ _apply_aff("kai", 3)
           kai "People pay for a session and they want..."
           "She stops. Considers."
           kai "I know. I know that. I just forget it sometimes."
       "[Say nothing. Let her sit with it for a second.]":
           $ _apply_trust("kai", 2)
           $ _apply_aff("kai", 2)
           "She drinks her coffee. The silence doesn't bother her."
           kai "See, this is the part nobody tells you about."
   ```

3. **Resolution.** She finishes the coffee. Back to herself — or close enough to the version she usually shows. "Same time Thursday?" It's her slot anyway. The offer to share it is new.

**CG:** No. This is a sprite-and-background scene. The intimacy is in the café context, not in a composed image.
**New background needed:** No. Uses existing `cafeday`.

### Rewards

- `kai_affection += 2–3` (choice-dependent)
- `kai_trust += 2–3` (choice-dependent)
- `kai_cafe_quiet_done = True` **(new flag)**
- `add_relationship_memory("kai", "kai_cafe_quiet", "Between sets — the quiet version")`
- `spend_time(0.5)`

### Fallback

If never triggered: Kai remains bounded by the trainer career and the home dinner. Her relationship is pleasant and superficial — a good gym friend who never reveals anything. The hug profile (min_aff 25, min_trust 20) is reachable without this scene, but the scene is the only content that makes that hug feel earned.

---

## Elle — The Atlantic Option

**Scene label:** `scene_elle_portugal_payoff`
**Type:** breakthrough
**Narrative gap it fills:** `arc_elle_travel_2` sets `elle_abroad_revealed` (Elle has been offered an 18-month marine research position in Portugal) and then nothing happens. The flag is declared, set, and never read. This scene is the payoff: the player finds out what she decided.

### Canonical staging

- **Location:** `location_beach` or `location_sandbeach` (bg: `beachday`) — Elle's beach schedule: Wednesday 16–19, Saturday–Sunday 13–18
- **Time window:** 13:00–19:00, Wednesday or weekend
- **Day restriction:** Wednesday (day % 7 == 2) or weekend (day % 7 in [5, 6])
- **NPC outfit:** `elle_sundress_normal`
- **Player requirement:** `elle_abroad_revealed = True` (existing flag, set in arc_elle_travel_2), `elle_pier_done = True` (existing flag), `elle_affection >= 40`, `elle_trust >= 25`

### Trigger

- A phone message from Elle fires in `new_day()` 7+ days after `elle_abroad_revealed` is set, when `elle_pier_done` is True: `"I made up my mind about Portugal. Come find me at the beach when you have time."` Message tag: `elle_decision_msg`. No response options required — it's a statement, not an invitation that can be declined.
- **Sets** `elle_decision_pending = True` **(new flag)** when message is delivered
- **Fires** at `location_beach` (or `location_sandbeach`) when: `elle_decision_pending and npc_talkable("elle")`
- **Pending pattern:** boolean (`elle_decision_pending`, new)
- **Expiry:** None. The scene stays pending until the player visits the beach when Elle is there. This is too important to expire.

### Dependency chain

- **Requires:** `arc_elle_travel_2` complete (sets `elle_abroad_revealed`) + `elle_pier_scene` complete (sets `elle_pier_done`) + thresholds. The pier scene must come first narratively — Elle needs to have had the moment of real openness at the pier before this payoff lands. Typical unlock: day 22–35.
- **Unlocks:** nothing mechanically. Sets `elle_decision_done = True` **(new flag)**. Closes the only open arc thread in Elle's relationship.

### Scene structure

1. **Opening beat.** Elle is at the waterline, shoes off. The same posture as always — like the sea owes her something and she's waiting patiently to collect. When the player approaches, she turns without surprise. "I was starting to think you weren't going to come."

2. **Core moment.** She tells them what she decided. The scene does not force a specific outcome — Elle's answer is shaped by the player's response in `arc_elle_travel_2`:
   - If the player told her "Take it" in the arc: she's going. "You made it sound obvious. I think you were right."
   - If the player asked "What would you miss?" in the arc: she's staying, for now. "I kept making that list. It got long."
   - If the player asked "What's changed?" in the arc: she's undecided and leaves it ambiguous. "I'm going to defer it. One year. See what the year says."
   
   Regardless of her decision, the player responds:
   ```
   menu:
       "\"That's the right call.\"" if elle_trust >= 35:
           $ _apply_trust("elle", 3)
           el "You don't know that."
           "Beat."
           el "But thanks."
       "\"Are you sure?\"":
           $ _apply_trust("elle", 2)
           el "No. But I'm done being unsure about being unsure."
       "\"What happens next?\"":
           $ _apply_aff("elle", 3)
           el "I go to the beach, or I go to Portugal. Either way, I figure it out."
           "She almost laughs."
       "[Don't say anything. Sit down next to her.]":
           $ _apply_trust("elle", 3)
           $ _apply_aff("elle", 2)
           "She sits too. For a while, neither of you says anything."
           el "You're good at this part."
   ```

3. **Resolution.** The light goes gold. Elle says: "I'll let you know how it ends up." Then something shifts in her face — not sadness, just the weight of a thing decided. "It means something that you came." She goes.

**CG:** Yes. The standout moment is Elle at the water's edge in the moment before she tells the player — her expression is the emotional anchor of the entire arc payoff. Proposed: a medium-distance shot of Elle from slightly behind and to the side, facing the sea, player POV implied. She's turned her head slightly toward the player. Late-afternoon light, warm. Image name: `cg_elle_portugal_turn`. Orientation: landscape 1920×1080.

This CG is justified: the existing elle_pier sequence (6 frames) establishes the beach visual grammar; this is the resolution moment in the same location. Without it, the scene has no visual peak.

**New background needed:** No. Uses existing `beachday`.

### Rewards

- `elle_affection += 2–3` (choice-dependent)
- `elle_trust += 2–3` (choice-dependent)
- `elle_decision_done = True` **(new flag)**
- `add_relationship_memory("elle", "elle_portugal_decision", "She told me what she decided")`
- `spend_time(1.0)`

### Fallback

If never triggered: `elle_abroad_revealed` dangles permanently. The arc ends mid-sentence — Elle revealed a life-changing decision and the player never learned the outcome. The relationship can still advance via pier_scene and generic topics, but it carries a specific feeling of incompleteness that the player will notice on a second playthrough.

---

## Sam × Marcus — Early Court

**Scene label:** `scene_sam_marcus_park`
**Type:** crossover
**Narrative gap it fills:** NPC_RELATIONS marks Sam and Marcus as `gym_friends` and produces only generic group conversation when they're at the same location. They share the park Mon–Fri 06–10 every day. This converts a systemic coincidence into a scripted scene that uses their pre-existing dynamic and makes the player's relationship with each of them matter.

### Canonical staging

- **Location:** `location_park` (bg: `basketball_court_day` for the main beats, `parkday` for setup) — weekday morning
- **Time window:** 06:00–10:00 (Mon–Fri, day % 7 in [0, 1, 2, 3, 4])
- **Day restriction:** Weekday only (both Sam and Marcus scheduled at park 06–10 Mon–Fri)
- **NPC outfit:** `marcus_park_neutral` (Marcus) + `sam_normal` (Sam)
- **Player requirement:** `sam_affection >= 30`, `marcus_affection >= 25`, or `marcus_affection >= 30`, `sam_affection >= 25` — combined threshold: total of both >= 55

### Trigger

- **Sets** `sam_marcus_scene_pending = True` **(new flag)** in `new_day()` when: `sam_affection + marcus_affection >= 55 and not sam_marcus_scene_done and not sam_marcus_scene_pending`
- **Fires** at `location_park` when: `sam_marcus_scene_pending and npc_here("sam") and npc_here("marcus") and 6 <= hour < 10 and major_scene_last_day != day`
- Sets `major_scene_last_day = day` (MAJOR scene)
- **Pending pattern:** boolean (`sam_marcus_scene_pending`, new)
- **Expiry:** None. The park is available every weekday morning; no need to expire.

### Dependency chain

- **Requires:** Both relationships developed to the threshold above. No career gates.
- **Unlocks:** nothing mechanically. Sets `sam_marcus_scene_done = True` **(new flag)**. Adds relationship memories to both NPCs.

### Scene structure

The two-outcome branch is gated on which relationship is stronger:
```python
$ _sam_leads = sam_affection >= marcus_affection
```

1. **Opening beat.** The player arrives at the park early. Sam and Marcus are already at the court — mid-argument, low-stakes, the kind they've clearly had before. Marcus: "You count every rep. That's why you plateau." Sam: "You stop counting and you get sloppy." They're both half-right and they know it.

2. **Core moment.** They pull the player in as tiebreaker. The player's response shapes the scene based on which relationship is stronger:

   **If sam_affection >= marcus_affection:**
   ```
   menu:
       "Side with Sam. \"Counting keeps you honest.\"":
           $ _apply_aff("sam", 3)
           $ _apply_trust("sam", 2)
           $ _apply_aff("marcus", -1)
           sam "Finally."
           m "Two against one. Fine. Next week I'll destroy both of you."
       "Side with Marcus. \"At some point you have to trust your body.\"":
           $ _apply_aff("marcus", 3)
           $ _apply_aff("sam", -1)
           sam "You're wrong. But okay."
       "[Split it.] \"Count to build the habit, then drop the count.\"":
           $ _apply_aff("sam", 2)
           $ _apply_aff("marcus", 2)
           sam "That's... actually fine."
           m "You're going to be unbearable about this."
   ```

   **If marcus_affection > sam_affection:**
   ```
   menu:
       "Side with Marcus. \"Listening to your body beats counting reps.\"":
           $ _apply_aff("marcus", 3)
           $ _apply_trust("marcus", 2)
           $ _apply_aff("sam", -1)
           m "See."
           sam "Still wrong. But noted."
       "Side with Sam. \"Structure first.\"":
           $ _apply_aff("sam", 3)
           $ _apply_aff("marcus", -1)
           m "I'm surrounded by people who love spreadsheets."
       "[Split it.] \"Both. At different stages.\"":
           $ _apply_aff("sam", 2)
           $ _apply_aff("marcus", 2)
           m "You're not picking a side."
           sam "They're right."
   ```

3. **Resolution.** They play. It's nothing serious — three-person casual shooting, the kind where score doesn't matter. By the end both of them are more interested in the next coffee than the argument. Sam: "Same time tomorrow?" Marcus doesn't say yes but he'll be there. He always is.

**CG:** Yes. One new CG: the three of them at the basketball court, mid-motion — the moment right after the player takes a shot, Marcus watching the ball, Sam watching the player. Not a confrontation shot. A moment of the three of them in the same space, unremarkable, familiar. Image name: `cg_sam_marcus_court`. Uses `images/scenes/sam_marcus_park/` folder. 1920×1080 landscape.

Justification: The nora_kai_crossover has `cg_nora_kai` for a comparable low-stakes group moment. Consistency of production level warrants a CG here. The marcus_court folder already has court images but they're player-solo or Marcus-solo; a three-person frame is new.

**New background needed:** No. `basketball_court_day` already exists.

### Rewards

- `sam_affection += 2–3` (choice-dependent)
- `marcus_affection += 2–3` (choice-dependent)
- `sam_trust += 1` (baseline)
- `marcus_trust += 1` (baseline)
- `sam_marcus_scene_done = True` **(new flag)**
- `add_relationship_memory("sam", "sam_marcus_court", "Early court — the three of us")`
- `add_relationship_memory("marcus", "marcus_sam_court", "Early morning court")`
- `spend_time(1.5)`

### Fallback

If never triggered: Sam and Marcus continue producing generic group chat. The NPC_RELATIONS link never pays off in scripted content. Sam's arc remains the thinnest in the game (one gym scene). The player who builds both relationships deeply never sees them interact as specific people.

---

## Eli — Home Dinner

**Scene label:** `home_dinner_scene_eli`
**Type:** everyday (home dinner, repeatable)
**Narrative gap it fills:** Eli is absent from `home_dinner_invite_menu` despite being present in every other home-visit system (`home_eli_side_project_scene`, dinner invite list check loop covers nid in ["martha", "nora", "zoe", "marcus", "lena", "kai"] — Eli is not in this list). The audit confirms this as a code gap, not a design choice.

### Canonical staging

- **Location:** `location_home` (bg: `home_bg()`, CG: `cg_home_dinner_table` — the shared dinner CG already used by all other dinner scenes)
- **Time window:** Any (player-initiated from "Invite someone for dinner" menu)
- **Day restriction:** Any day `home_invite_available("eli", min_aff=20, min_trust=15)` returns True
- **NPC outfit:** `eli_normal`
- **Player requirement:** `own_kitchen_set = True` (existing), `eli_affection >= 20`, `eli_trust >= 15`

### Trigger

- No pending flag needed. Follow the existing repeatable dinner pattern: add `"Invite Eli (3h)" if home_invite_available("eli", min_aff=20, min_trust=15):` to `home_dinner_invite_menu`, then `$ spend_time(3)` + `call home_dinner_scene_eli`.
- **Also required:** Add `"eli"` to the `_dinner_ok` check list in `home_dinner_invite_menu`:
  ```python
  for nid in ["martha", "nora", "zoe", "marcus", "lena", "kai", "eli"]
  ```
- **Pending pattern:** None (repeatable, player-initiated)
- **Expiry:** None

### Dependency chain

- **Requires:** `own_kitchen_set` + thresholds. Does not require IT career or `eli_met` via career; Eli is world=True so `npc_known("eli")` is always True.
- **Unlocks:** Nothing mechanically. The scene is the container for a meaningful beat in Eli's relationship; it doesn't gate any further content.

### Scene structure

Eli's dinner is deliberately different from the other six: he doesn't arrive with wine (Zoe), take over the kitchen (Nora), eat two portions cheerfully (Marcus), or arrive from a shift (Lena). He arrives with exactly the right amount of rice to eat and nothing else, because he assumed the player had the rest sorted. He did not check.

1. **Opening beat.** Eli arrives on time to the minute. He has brought a packet of jasmine rice because "it seemed like something that might be missing." He looks at the table, looks at the rice, looks at the player. "I didn't think that through." He says it calmly, like a bug he's just spotted.

2. **Core moment.** The meal itself — whatever the player made — is fine. Eli eats with attention, the way he does everything. At some point he says something about the apartment, or the setup, or the way the player arranged something in the kitchen. Something specific and true. Then:
   ```
   menu:
       "\"You notice a lot.\"":
           eli "I notice most things. It's not always useful."
           $ _apply_trust("eli", 3)
           eli "Here it is. The rice was a mistake."
           "He seems genuinely pleased with this conclusion."
       "Ask what he's been working on.":
           eli "The thesis chapter I've been avoiding for six weeks. I finally opened it this morning."
           $ _apply_aff("eli", 2)
           eli "Coming here felt easier. Which is probably the point."
           $ _apply_trust("eli", 2)
       "[Wait and see if he says something unprompted.]":
           "He does. Eventually."
           eli "I don't come to people's homes very often. This is — it's good. Thank you."
           "He says it to the table. Means it to you."
           $ _apply_aff("eli", 3)
           $ _apply_trust("eli", 2)
   ```

3. **Resolution — the small meaningful beat.** Near the end, the intellectual scaffolding drops for one sentence. Not a revelation. Just Eli, without the framing: "I like it here." He doesn't follow it up. The jasmine rice is still on the counter.

**CG:** No. Reuses `cg_home_dinner_table` (shared bg). The scene's value is in Eli's voice, not in a composed image.
**New background needed:** No.

### Rewards

- `eli_affection += 3` (baseline) + choice-dependent
- `eli_trust += 2–3` (choice-dependent)
- `add_relationship_memory("eli", "eli_home_dinner", "Home dinner — the rice")`

### Fallback

If never implemented (current state): Eli is the only named NPC with a home-visit precedent who cannot be invited to dinner. The player who has built a close relationship with Eli has access to a side-project visit but not the informal intimacy of a shared meal. The gap is visible if the player has already hosted all six other NPCs.

---

## Implementation Order

Ranked by (1) narrative urgency, (2) implementation ease, (3) asset requirements.

| Rank | Scene | Reasoning |
|------|-------|-----------|
| 1 | **Eli — Home Dinner** | Zero new art. Two-line fix to `home_dinner_invite_menu` + one new label following an established pattern. Closes an explicit audit finding (code gap, not design). Highest ROI. |
| 2 | **Natalie — After the Whistle** | No new CG. Bar background + existing sprite. Fills the most starved arc in the game (Natalie currently has one scene). Trigger pattern is simple boolean pending in new_day. |
| 3 | **Elle — The Atlantic Option** | One new CG. Fills the only unresolved arc thread in the game — `elle_abroad_revealed` is set and never read. Highest narrative urgency. Phone-message trigger is clean and tested (follows the nora_bad_day pattern). |
| 4 | **Kai — Between Sets** | No new CG. Café background + existing kai_normal sprite. Simple pending trigger with one guard (`not nora_kai_pending`). Delivers Kai's breakthrough independently of career path. |
| 5 | **Sam × Marcus — Early Court** | One new CG. Existing backgrounds. Both sprites exist. Dual-outcome branch is the most code-complex of this pack (~30 lines), but the pattern is identical to `scene_nora_kai_crossover`. Converts NPC_RELATIONS from documentation to content. |
| 6 | **Caroline — Off the Clock** | No new CG, but the most technically novel: Caroline appears at a location she has no schedule entry for, requiring a pending-flag bypass of the normal `npc_here` check. Write last to avoid contaminating the simpler implementations. |

---

## Asset Generation List

| Image name | Type | Description | Priority |
|------------|------|-------------|----------|
| `cg_elle_portugal_turn` | CG | Elle at the water's edge, late-afternoon light, turning her head slightly toward the player's POV. Medium distance. Emotionally restrained — this is a decision made, not a breakdown. 1920×1080 landscape. Folder: `images/scenes/elle_portugal_payoff/` | HIGH |
| `cg_sam_marcus_court` | CG | Sam, Marcus, and implied player at the basketball court. Mid-motion frame — ball in the air, both NPCs in natural body language that shows they're comfortable with each other and with the player. 1920×1080 landscape. Folder: `images/scenes/sam_marcus_park/` | MEDIUM |

**Total new art: 2 CGs, 0 new backgrounds.** All scenes reuse existing location backgrounds. No new character sprites required.

---

## Scenes Requiring No New Art

All six scenes can be staged with existing assets. The two CGs listed above are recommended but not blocking:

- **Eli home dinner** — `cg_home_dinner_table` (shared), `eli_normal`, `home_bg()`
- **Natalie bar** — `bar`, `natalie_normal`
- **Kai café** — `cafeday`, `kai_normal`, `nora_cafe_normal`
- **Caroline bar** — `bar`, `caroline_normal`
- **Sam × Marcus** — `basketball_court_day`, `parkday`, `marcus_park_neutral`, `sam_normal` (CG is recommended but scene functions without it; can fall back to sprite-over-parkday)
- **Elle beach** — `beachday`, `elle_sundress_normal` (CG is strongly recommended; without it the arc's emotional peak has no visual anchor — but scene text carries it)

---

## Trigger Overlap Risks

| Scene pair | Collision scenario | Likelihood | Resolution |
|------------|-------------------|------------|------------|
| `scene_kai_cafe_quiet` + `scene_nora_kai_crossover` | Both fire at `location_cafe` when Kai is present (Tue/Thu 10–14). Both pending flags can be True simultaneously once relationship thresholds are met. | HIGH — the café is the primary location for both; once both pending, any Tue/Thu café visit triggers the first check. | Explicit guard in `scene_kai_cafe_quiet` trigger: `if nora_kai_pending: skip`. nora_kai takes priority (it is a conflict/repair scene with a pending-day expiry; kai_cafe has no expiry pressure). kai_cafe fires on a subsequent Tue/Thu visit. |
| `scene_sam_marcus_park` + `scene_marcus_missed_commitment` | Both can fire at `location_park` on a weekday morning (06–10). `marcus_missed_pending` is also checked at `location_park`. | MEDIUM — if player misses a Marcus basketball commitment and has also met the sam+marcus threshold, both flags are True simultaneously. | `scene_marcus_missed_commitment` has higher priority (it is a conflict with emotional stakes and a time-decay element). Place its park check before `sam_marcus_scene_pending` in `location_park` entry. sam_marcus defers to next park visit. |
| `scene_caroline_thursday_bar` + `scene_natalie_bar_offduty` | Both fire at `location_bar`. Different day patterns (Caroline: Thu only; Natalie: Sat–Sun only). | NONE — Thursday and Saturday/Sunday do not overlap. These scenes cannot fire on the same calendar day by construction. |
| `scene_elle_portugal_payoff` + `elle_pier_scene` | Elle's pier scene (`elle_pier_done` check in `location_beach`) fires at aff≥40 + npc_talkable("elle"). The portugal payoff requires `elle_pier_done = True`. | NONE — the portugal payoff hard-gates on `elle_pier_done`, so pier_scene always completes first. The two scenes are strictly sequential. |
| `scene_sam_marcus_park` + `scene_car_marcus_drive` (MAJOR) | Both set `major_scene_last_day = day`. sam_marcus fires at park 06–10; car_marcus fires at bar hour≥22. Same calendar day is physically possible (morning park, late bar). | LOW — Marcus's bar schedule starts at 17:00; the player would need to visit both park and bar in one day. The major-scene mutex blocks the second one. sam_marcus fires first (earlier in the day). car_marcus defers to next bar visit at hour≥22 on a separate day. No silent loss — car_marcus_pending survives. |
| `scene_caroline_thursday_bar` + `scene_marcus_missed_commitment` | Both can fire at `location_bar` on a Thursday. marcus_missed_pending checks `marcus_affection >= 30` and fires at bar (or park). | LOW — marcus_missed_pending has higher narrative urgency (conflict resolution). Give it priority in location_bar entry checks. caroline_bar defers to the next Thursday. |

---

## New Flags Summary

All new flags, to be added to `data.rpy`:

```renpy
default caroline_bar_done             = False
default caroline_bar_pending          = False
default natalie_bar_scene_done        = False
default natalie_bar_scene_pending     = False
default kai_cafe_quiet_done           = False
default kai_cafe_quiet_pending        = False
default elle_decision_done            = False
default elle_decision_pending         = False
default sam_marcus_scene_done         = False
default sam_marcus_scene_pending      = False
```

`home_dinner_scene_eli` requires no new flags (repeatable dinner pattern, same as existing six dinner scenes).
