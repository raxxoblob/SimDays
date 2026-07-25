# Character Depth Bible
## LivingTheDream — NPC Design Reference

Key: **[CANON]** = supported by current code. **[INFERENCE]** = reasonable reading of existing scenes. **[PROPOSAL]** = requires owner approval before implementation.

---

## NORA

**Established personality [CANON]:** Direct, food-obsessed, self-aware, not sentimental. Stays in control of social situations — her greet line upgrade ("Hey, you. I was hoping you'd come in today") is more honest than she usually allows.

**Current role [CANON]:** Café barista, culinary programme candidate, first-contact NPC.

**External goal [CANON]:** Enter and complete the culinary programme (`nora_school_revealed`, `scene_nora_hug_school`).

**Internal need [INFERENCE]:** Permission to leave what she's already good at. She is competent at the café — that competence is keeping her there.

**Central contradiction [CANON + INFERENCE]:** The café feels safe because she's good at it. The culinary school is the thing she actually wants. Her landlord raising rent (`nora_rent_scene`) is pressure to earn more, which means staying in the job that traps her, not training for the career she wants.

**Flaw [INFERENCE]:** Stays in comfortable expertise rather than risking genuine change. Uses competence as insulation. Henry's raise-offers are easier to accept than the programme's demands.

**Fear [INFERENCE]:** That the culinary school is harder than the café, and she fails there too — but this time at the thing she chose on purpose.

**What she wants from MC [INFERENCE]:** To be treated as a person rather than a coffee-delivery mechanism. Someone who notices her when she's not performing the job.

**What she wants that has nothing to do with MC [CANON]:** The culinary programme spot. A kitchen where the hob is straight.

**Existing NPC relationships [CANON]:** Kai (regulars, flat white argument — `scene_nora_kai_crossover`). Henry (employer, implied throughout `nora_closing_scene` and `nora_rent_scene`). Elle (both at the café Tue/Thu; no scene yet).

**Strongest scene [CANON]:** `nora_closing_scene` — emotionally specific, has real stakes, the memory system records the outcome.

**Weakest scene [CANON]:** `arc_nora_food_2` (pastry course) — an interesting detail with no follow-through.

**Arc beginning [CANON]:** Exists — café meet, closing scene, rent reveal.

**Arc middle [CANON]:** Exists — school announcement, hug scene, home scenes.

**Arc ending [MISSING]:** She says yes to the programme. Nothing follows. **[PROPOSAL]:** One callback scene, 3–6 weeks after `nora_hug_school_done`, where she references the programme having started and shows one specific thing that is harder or better than the café.

**Platonic path [CANON]:** Fully supported — closing scene has platonic branch, reopen scene exists.

**Romantic path [CANON]:** Supported — full romance state system, first kiss scene, momentum tracking.

**Failure/distancing path [CANON]:** `scene_nora_feels_ignored` handles absence consequence. `nora_ignored_pending` fires from daily check.

**Recovery path [CANON]:** `scene_nora_romance_reopen` handles post-withdrawal reconnection.

**Recurring motif [CANON]:** Coffee — the machine, the calibration, the memory of closing. Coffee is the language of the relationship.

**What the player should remember:** The person who made the best espresso you ever had in that apartment, and the conversation where she told you she'd stopped trying to convince herself the café was enough.

---

## ZOE

**Established personality [CANON]:** Dry wit, independent, avoidant through humor, strong aesthetic judgment. Dislike: ambition. Sketchbook always present.

**Current role [CANON]:** Artist, beach regular, nightlife regular, world NPC.

**External goal [CANON]:** Exhibition success — submits work, gets rejected, tries again (`arc_zoe_art_2`, `arc_zoe_art_3`, `arc_zoe_art_4`).

**Internal need [INFERENCE]:** To be taken seriously as an artist without needing to perform confidence she doesn't always feel.

**Central contradiction [INFERENCE]:** Values independence so strongly she's suspicious of caring what anyone thinks — but the rejection in `arc_zoe_art_3` clearly matters. The wit is protection.

**Flaw [INFERENCE]:** Avoidance via irony. When something gets real she redirects. `scene_zoe_spontaneous` is the moment where this breaks briefly.

**Fear [INFERENCE]:** Making something she cares about and having it definitively rejected. The grant failure is manageable; a well-attended show where nobody buys anything would be worse.

**What she wants from MC [INFERENCE]:** Someone who doesn't treat her art as a personality accessory.

**What she wants that has nothing to do with MC [CANON]:** The gallery, the show, the sketchbook full of work that holds.

**Existing NPC relationships [CANON]:** Elle (friends — `NPC_RELATIONS` entry). Eli (met in `scene_eli_meets_zoe`). Nora (no scene yet but both in café circle).

**Strongest scene [CANON]:** `scene_zoe_spontaneous` — an authentic almost-moment that requires the player to read it correctly.

**Weakest scene [CANON]:** The exhibition arc — invitation is set (`zoe_exhibition_invited`), opening is announced (`arc_zoe_art_4`), but no exhibition scene fires. The arc has a structural hole.

**Arc ending [MISSING]:** The exhibition opening. `zoe_exhibition_invited = True` is set but no scene exists. **[PROPOSAL]:** `scene_zoe_exhibition_opening` — player attends the gallery. Outcomes branch: success (one piece sold), partial (appreciated but unsold), quiet (no sales, Zoe handling it). Scene reveals something about how she processes public judgment of private work.

**Platonic path [CANON]:** Fully supported.

**Romantic path [CANON]:** Supported — romance state system, spontaneous moment, reopen scene, first kiss.

**Recurring motif [CANON]:** The sketchbook — she draws people without showing their faces. The guitar session (she draws MC while they play) is the motif's clearest expression.

**What the player should remember:** She drew you without your face. You didn't ask to see it before she said you could.

---

## ELI

**Established personality [CANON]:** Precise, dry, technically honest. Arrives on time. Functions lie. `no_decay=True` through employment. She/her pronouns.

**Current role [CANON]:** Senior developer at The Hub. Part-time MSc candidate. IT career mentor.

**External goal [CANON]:** Finish the environmental systems thesis. Deploy the pipeline (`eli_deploy_pending`).

**Internal need [INFERENCE]:** Proof that the thesis work matters even when the evidence of impact is nonexistent.

**Central contradiction [INFERENCE]:** Analytical precision is her skill — but the big problem she's studying (climate systems, policy modelling) cannot be solved with precision or even with a good thesis. She knows this. `arc_eli_work_2`: "What if the thesis is good and it still doesn't matter?"

**Flaw [INFERENCE]:** Prefers problems with solutions. Humans are harder to debug than code. Home scenes (side project, dinner) show her more comfortable when the interaction has a defined purpose.

**Fear [CANON]:** That the work is right and still doesn't matter (`arc_eli_work_2`).

**What she wants from MC [INFERENCE]:** Someone who treats her like a peer without needing her to be warm about it.

**What she wants that has nothing to do with MC [CANON]:** The thesis to be sound. The deploy to hold.

**Existing NPC relationships [CANON]:** Zoe (`scene_eli_meets_zoe` — generative art argument, clearly a genuine intellectual match). Hub colleagues (implied but unspecified).

**Strongest scene [CANON]:** `scene_eli_deploy_hug` — she initiates physical contact, which costs her something, and the narrative marks it as such.

**Weakest scene [CANON]:** `arc_eli_work_1` (part-time MSc introduction) — setup without payload; the thesis topic never appears in any later scene with stakes attached.

**Arc beginning [CANON]:** IT first day, thesis arcs.

**Arc middle [CANON]:** Debug session, hardware prototype, deploy pending.

**Arc ending [PARTIAL]:** Deploy hug fires, `eli_dinner_done` closes the home arc. But the thesis never resolves — no scene marks whether she finishes it, whether it's published, whether it matters. **[PROPOSAL]:** One callback — after `eli_dinner_done`, a later library or bar encounter where Eli says the thesis was submitted. The player's arc arc response (`arc_eli_work_2` choice) should affect whether she sounds resolved or still uncertain.

**Platonic path [CANON]:** Strong — side project, debug session, dinner, metal detector. The relationship is complete without romance.

**Romantic path [CANON]:** Disabled (`do_kiss` disabled in interact system). Eli is not romanceable. This is correct and should not change.

**Recurring motif [CANON]:** Functions that lie, the naming of things, precise language as care. Also jasmine rice — she brought a packet she hadn't thought through and said so exactly.

**What the player should remember:** She said functions lie when they outlive their original scope. Then she said the same thing about the café and the thesis and the rice, only using different words.

---

## MARTHA

**Established personality [CANON]:** Sharp observer, stayed 9 years past her plan at Nexus, sees through most things, uses irony as distance. "I noticed. I didn't always act on it."

**Current role [CANON]:** Analytics senior, MC's professional mentor in corporate arc.

**External goal [INFERENCE]:** To eventually stop staying past her plan — but this is never stated directly. Her goal is implied by what she confesses on the rooftop.

**Internal need [INFERENCE]:** Acknowledgment that staying had a reason, not just inertia.

**Central contradiction [CANON]:** She coaches MC to be honest and ambitious while having remained at a job she outgrew years ago. She gives the advice she didn't take.

**Flaw [INFERENCE]:** Observes clearly and acts slowly. She noticed MC was being handled badly and didn't always act on it.

**Fear [INFERENCE]:** That she stayed for inertia dressed as loyalty and that this is now just who she is.

**What she wants from MC [CANON]:** Initially: a project that holds up. Later: someone who doesn't already have a fixed idea of who she is.

**What she wants that has nothing to do with MC [INFERENCE]:** To do something next. The rooftop conversation is about whether she has the answer yet.

**Existing NPC relationships [CANON]:** Caroline (colleagues — present in corporate arc throughout). Atlas project stakeholders (Meridian Group, implied). No crossover with non-corporate NPCs currently.

**Strongest scene [CANON]:** `corporate_atlas_problem` — the ethical choice about the 30% workforce cut is the game's clearest example of a decision that matters because someone else bears the cost.

**Weakest scene [CANON]:** `scene_wardrobe_martha` — reactive to a player item, pleasant, no consequence.

**Arc ending [PARTIAL]:** `corp_net_credit_hallway_done` is a good callback. But after Atlas completes, Martha's story has no further movement. She helped MC, she watched the presentation result, she gave feedback on credit. Then she stops. **[PROPOSAL]:** One scene — post-Atlas, after sufficient time — where Martha tells MC she's leaving Nexus. Not a crisis. Just a fact. The player's response should matter to whether it feels like an ending or a beginning.

**Recurring motif [CANON]:** Coffee — she always orders before the other person arrives. It is presumptuous, she says, and faster.

**What the player should remember:** She told you she noticed you were being handled badly and didn't always act on it. That sentence was the most honest thing anyone at the company said to you.

---

## CAROLINE

**Established personality [CANON]:** HR, wry, boundary-setter. "If you're not on fire, make it quick." Off-duty Thursday at the bar — a different register.

**Current role [CANON]:** HR recruiter/contact at Nexus. Sets `corporate_style` at hire.

**External goal [MISSING]:** None established in current code.

**Internal need [MISSING]:** None established.

**Central contradiction [MISSING]:** None currently scripted.

**Current depth:** The weakest of the recurring work NPCs. The ethics scenario she presents in `corporate_recruit` reveals she asks important questions — but what she thinks the answers should be is never revealed. She is the person who enforces systems she may partially disagree with.

**[PROPOSAL] — Central human problem:** Caroline is good at identifying what people need and very controlled about what she reveals about herself. The bar scene (`scene_caroline_thursday_bar`) is off-duty, which is where the gap between her professional register and the person underneath it starts to show. Her problem: she is skilled at managing other people's narratives and has almost no practice with her own. She knows exactly what the correct answer to the ethics question is. She doesn't necessarily believe it.

This should create choices rather than exposition: when MC pushes back on something she said in the bar, she either defends the position (trust gain, distance increase), admits it's complicated (trust gain, warmth), or deflects (aff gain, no real progress).

**Platonic path [CANON]:** Possible — no romance is not penalised.

**Romantic path [CANON]:** Supported — romance state system, bar romance open, first kiss.

**Recurring motif [INFERENCE]:** The ethics scenario — the question she asks at hire. If she appears in later content, the scenario she described should return.

**What the player should remember [PROPOSAL]:** The question she asked during your interview. Not the answer she was looking for — the question itself.

---

## DR. LENA

**Established personality [CANON]:** Chose medicine and means it. "I didn't account for what it costs." Disciplined, not cold. Different register with patients than with colleagues.

**Current role [CANON]:** Hospital clinician and MC's medical career mentor.

**External goal [INFERENCE]:** To keep doing the work without losing the ability to care.

**Internal need [INFERENCE]:** Someone who doesn't need her to be capable. All her professional relationships involve her being the one with answers.

**Central contradiction [CANON]:** Chose this knowing what it costs → still didn't fully account for it → won't admit she needs support → which means her support has to come through professional channels (MC as colleague) rather than personal ones.

**Flaw [INFERENCE]:** Applies the same emotional discipline to herself that she applies to cases. Controlled even about her own cost.

**Fear [INFERENCE]:** Losing the ability to care about individual patients — the burnout that turns compassion into processing.

**What she wants from MC [INFERENCE]:** Someone who sees the cost without requiring her to name it every time.

**Shoulder gesture [CANON]:** `scene_lena_shoulder_gesture` requires `hospital_hard_case_pending = True`. This flag IS set — a 25% random roll per qualifying hospital shift when `lena_break_room_done`, `hosp_shifts >= 10`, and `job_rank >= 1` are met (locations.rpy:1635-1638). The scene IS reachable; `job_performance >= 70` only changes flavor dialogue, not scene availability. The problem is the trigger quality: no authored moment, no pity mechanism, and a 25% ceiling per shift means qualifying players may work many shifts without the roll succeeding. ARC-1 replaces the random roll with a guaranteed authored scene. The shoulder gesture is one of the game's stronger physical moments — it must not depend solely on RNG.

**Strongest scene [CANON]:** `lena_rooftop_scene` — specific, measured, honest without being performative.

**Weakest scene [CANON]:** `hosp_npc1_lena` (rounds observation) — introduces how she changes register with patients but the player choice is observation-only with no follow-through.

**Recurring motif [CANON]:** The cost of the work. She returns to this. The rooftop is its fullest expression.

**What the player should remember:** She said she chose this. She wanted to be clear about that. She wasn't there by accident. She just didn't account for what it costs.

---

## ELLE

**Established personality [CANON]:** Traveler, space-seeker. Comes to the pier every Wednesday as her own space. "Nobody comes this far down. Which is exactly the point."

**Current role [CANON]:** Beach regular, café occasional, world NPC.

**External goal [CANON]:** The Portugal marine research position — or the decision about it.

**Internal need [INFERENCE]:** To make a real choice rather than keeping all options open. Elle has been deferring the decision long enough that deferral has become a choice she didn't consciously make.

**Central contradiction [INFERENCE]:** Wants to leave and has a reason to leave — and keeps finding reasons to stay, defer, or reconsider. The deferral is comfortable; action in either direction is not.

**Flaw [INFERENCE]:** Comfort in optionality. She can stay at the pier every Wednesday precisely because she hasn't committed to anything that would take her away from it.

**Existing NPC relationships [CANON]:** Zoe (friends — `NPC_RELATIONS` entry). Nora (both at café Tue/Thu — no scene yet).

**Arc ending [MISSING]:** `scene_elle_portugal_payoff` resolves the decision. Nothing follows. If she goes to Portugal: her schedule still shows at the beach. No NPC acknowledges her absence. If she stays: nothing changes in any dialogue. **[PROPOSAL]:** One callback — a few weeks after `elle_decision_done`. If she went: MC finds a postcard-length phone message from her about something specific she saw. If she stayed: one café or beach line where she acknowledges having decided and what it cost to choose.

**Platonic path [CANON]:** Supported.

**Romantic path [CANON]:** Supported — romance open, first kiss.

**Recurring motif [CANON]:** The pier — specifically the part where nobody comes. The distance from the main beach. She shows MC her actual geography.

**What the player should remember:** She went every Wednesday to a place where nobody came. She showed it to you. That was either a decision or a test.

---

## MARCUS

**Established personality [CANON]:** Early riser (6am park, can't sleep past 5), social ("at the bar every evening"), basketball history, makes one thing in the kitchen (chili, from his mother's notepad). Dislike: art.

**Current role [CANON]:** Park regular, bar regular, first social anchor for MC. Construction worker (implied in dinner scene: "a construction job that went badly — somehow funny").

**External goal [MISSING]:** None currently established. Marcus has no present-tense tension. His basketball history is past. His current life appears content.

**Internal need [INFERENCE]:** Unknown from code. The basketball backstory — father sick, didn't go pro — suggests a person who made a sacrifice and either made peace with it or is still working out what to want now.

**Basketball invite [CANON]:** `marcus_basketball_invite_pending` is set by `new_day()` once `arc_marcus_sports_2_done`, `marcus_trust >= 30`, and `day >= 20` are met. The bar fires the invite scene when pending is True, creates a court commitment, and sets `marcus_basketball_invite_done = True`. The invite flow is wired and functional. What is absent is the deeper authored conversation — ARC-4 — where Marcus weighs the decision with MC and the choice lands with real weight.

**[PROPOSAL] — Central human problem:** Marcus is doing fine by every visible measure. He has a job, a bar, a morning routine. But the basketball backstory suggests a person whose identity was organised around something that didn't happen, and who found a comfortable enough substitute without necessarily resolving the original question. The basketball invite flags suggest a planned scene where an old contact offers him something — a coaching role, a veterans' league, a community team slot — that brings the question back. His problem is not dramatic. It is the ordinary problem of a man in his late twenties who made a reasonable choice and isn't sure if it was the right one.

This creates player choices rather than exposition: encourage him to try, tell him the past is the past, say you don't know. Each response should matter to whether the scene ends with him in motion or at rest.

**Existing NPC relationships [CANON]:** Sam (gym friends — `NPC_RELATIONS`, crossover scene). Nightclub circuit (implied by schedule). Caroline (both at bar Thursday evenings — no scene yet).

**Strongest scene [CANON]:** `scene_car_marcus_drive` — the late-night drive works because it is quiet and unannounced.

**Recurring motif [CANON]:** The chili recipe, the notepad, the fact that he checks it every time. His relationship to his mother's instructions is more specific than anything else said about him.

**What the player should remember:** He checks the recipe every time. Not because he doesn't know it — because it's how he stays connected to the person who wrote it down.

---

## KAI

**Established personality [CANON]:** High-energy trainer, checks portion sizes, "Same time next week?" Dislike: work. The energy is a performance that costs something.

**Current role [CANON]:** Gym trainer, café regular. Trainer career mentor.

**External goal [MISSING]:** None established. The café quiet scene (`scene_kai_cafe_quiet`) hints at burnout but provides no forward goal.

**Internal need [INFERENCE]:** Permission to have a flat day without it meaning she's failing the people who paid for her energy.

**Central contradiction [CANON]:** Works at a job that requires constant performance (trainer — people pay for motivation) while privately exhausted by always being the energy.

**Flaw [INFERENCE]:** Can't distinguish between the professional persona and the person. The flat days feel like failure because clients hired the persona.

**[PROPOSAL] — Arc consequence:** `scene_kai_cafe_quiet` is isolated. One follow-up scene is needed — either at the gym (Kai asks MC to cover a client) or at the bar (she mentions she took a day off without telling anyone why). This should require no new CG and minimal writing. Its purpose: show that the quiet café moment had some effect, even a small one.

**Existing NPC relationships [CANON]:** Nora (`scene_nora_kai_crossover`). Bar circuit (scheduled Fri–Sun nightclub).

**Recurring motif [INFERENCE]:** Energy as currency — she spends it, people take it, she refills alone.

**What the player should remember:** She asked whether you wanted the energy all the time. She was asking because she was tired of giving it.

---

## SAM

**Established personality [CANON]:** Morning runner, consistent, hated the gym before making it productive. "You're consistent. That's rarer than people think."

**Current role [CANON]:** Park regular, gym regular, world NPC.

**External goal [MISSING]:** None established.

**Internal need [MISSING]:** None established.

**Existing scenes [CANON]:** `sam_gym_scene`, `scene_sam_marcus_park`. Two relationship memories: `sam_marcus_court`. One greet upgrade at aff >= 50.

**Assessment:** Sam currently has no story. She is the most underdeveloped of the twelve major NPCs. Her one character-revealing detail — she used to hate the gym and made herself like it — is the kind of specific that deserves a problem attached to it.

**[PROPOSAL] — Central human problem:** Sam is consistent because she decided to be. That decision has a cost: consistency as identity means any deviation feels like failure. She runs every morning because she made a rule. The rule helps and also traps. Her problem is ordinary: she holds herself to standards she set when she was a different person, and she doesn't easily revise them. When a run gets missed (injury, weather, obligation), the morning feels broken in a way that's disproportionate to the event. The gym is the same — she made it productive by making it compulsory.

This creates a player choice: validate the discipline (she appreciates it but nothing changes) or question it gently (she pushes back, then thinks). The scene should happen at the gym or park, not over a special commitment.

**[PROPOSAL] — Sam's external life:** She works somewhere. The game doesn't say where. Her schedule (park 6–10, gym 10–14) suggests either part-time work or shift work in the afternoon. One mention of what she does for money would make her feel like a person with a life.

**Platonic path:** Strong potential — she has a warmth and directness that makes her a natural consistent presence. She doesn't need romance to be complete.

**Romantic path:** Planned but no profile exists. Should remain planned, not implemented, until Sam has an arc.

**Recurring motif [INFERENCE]:** Showing up. The park at 6am, the gym at 10, the commitment to the routine. The question is whether showing up is a virtue or a substitute for deciding where to go.

**What the player should remember [PROPOSAL]:** She was always there at 6am. Eventually you realised that wasn't because the run was easy.

---

## NATALIE

**Established personality [CANON]:** Warehouse, no-nonsense, Muay Thai coach. "Not bad." Missed commit text: "Shift got covered."

**Current role [CANON]:** Warehouse work contact, bar regular (weekends).

**External goal [MISSING]:** None established.

**Internal need [MISSING]:** None established.

**Existing scenes [CANON]:** `scene_natalie_bar_offduty` (Muay Thai reveal), `phone_natalie_extra_scene` (shift).

**Assessment:** The Muay Thai coaching detail is the most interesting fact about Natalie and it is currently a disclosure with no consequence. She teaches people to hit correctly. That is a specific relationship to physical force and precision that could generate scenes.

**[PROPOSAL] — Central human problem:** Natalie's minimum viable arc: one scene where she offers to teach MC something specific (not a full training montage — one technique, one principle). Her coaching philosophy is probably the same as her warehouse philosophy: do the thing correctly or don't do it. This reveals that her directness is a methodology, not a personality quirk. If MC follows the instruction correctly, she respects it without announcing she does. If MC doesn't, she says why and stops.

**Recurring motif [INFERENCE]:** Doing things correctly. Not quickly. Not impressively. Correctly.

**What the player should remember [PROPOSAL]:** She showed you exactly one thing and said nothing complimentary. The nothing was the compliment.

---

## RENA [APPROVED CANON — DIRECTOR-LOCKED]

**Age:** 36. **Pronouns:** she/her. **Title:** Head Chef, Eleven.

**Romanceable:** No. Friendship and professional mentorship are complete valid routes.

**Established personality [CANON]:** Chef mentor. Corrects knife technique (`cul_npc1_rena`). Asks "why the kitchen?" (`cul_npc2_rena`). Phone display: "Chef Rena." `no_decay=True`.

**Current role [CANON]:** Culinary career mentor and head chef.

**Voice [CANON]:** Calm, highly precise, rarely raises her voice. Becomes quieter under pressure — not louder. Values early honest communication. Gives specific praise rather than generic encouragement. Does not explain herself unless asked.

**Central flaw [CANON]:** Confuses leadership with being indispensable. Distributes responsibility poorly because she does not fully trust that others will execute at her standard. This creates the conditions for the crisis she is trying to prevent.

**External conflict [CANON]:** Eleven's owners pressure her to cut costs, simplify the menu, and reduce staffing. She has been managing the gap between what the kitchen could be and what the business needs it to be.

**Internal need [CANON]:** Learn to distribute responsibility. She cannot run a kitchen by being the only person in it who meets her own standard.

**Physical description [CANON]:**
- Compact strong build
- Warm olive skin
- Dark chestnut hair in a low braided knot
- One naturally lighter streak at the left temple
- Amber-brown eyes
- Small old burn mark on left forearm
- Charcoal chef jacket with rolled sleeves
- Dark apron
- Analog watch worn on the inner wrist
- Black marker and thermometer in the same pocket

**Mannerisms [CANON]:**
- Taps the pass twice before service
- Straightens tickets while thinking
- Asks "what exactly happened?" rather than "is everything fine?"
- Remembers honest admissions of mistakes — does not hold the admission against you
- Smiles with one corner of her mouth when genuinely amused

**Off-duty recurring location [CANON]:** A late-night diner near the waterfront. She reads used crime novels and lets someone else cook.

**What she wants from MC [CANON+INFERENCE]:** Someone who asks the right question, not just executes the instruction. A commis who understands the reason behind the correction is more valuable than one who complies.

**What she wants without MC [CANON]:** Eleven survives. The owners back down, or she finds another way to hold the standard while cutting where it won't show. She solves the staffing problem differently.

**NPC relationships [MISSING]:** None yet established. The diner she visits should eventually be cross-referenced with another NPC who uses the same space.

**Strongest scene [CANON]:** `cul_npc2_rena` — "Why the kitchen?" No other scene currently rivals it.

**Weakest scene [MISSING]:** No failure state. The arc has no moment where Rena is under visible pressure and MC sees the gap between how she presents and what she's managing.

**Arc status [PARTIAL]:** Mentor introduction and NPC scenes done. Climax (`scene_cul_service_crisis`) not yet implemented. Off-duty scene (`scene_rena_bar`) not yet implemented.

**Path — Friendship:** Rena acknowledges competence and honesty. The bar scene makes her a person rather than a function. Post-crisis, she treats MC differently — not warmly, but as someone who met her standard.

**Path — Professional only:** MC can complete the culinary arc and be promoted without any personal revelation. Rena remains a mentor figure whose inner life is never seen.

**Recurring motif [CANON+INFERENCE]:** The correction as care. The question "why the kitchen?" — she still revisits it herself, on balance. The burn mark is old; she does not explain it.

**What the player should remember [CANON]:** She corrected your grip before she corrected the dish. She was teaching you that everything starts with how you hold the thing. When she went quiet during service, that was not calm — that was pressure absorbed.
