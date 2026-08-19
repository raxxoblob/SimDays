# Culinary Career — Scene Asset Plan

> Covers all scenes in `culinary_arc.rpy`. NPC: Rena (she/her), head chef. Location: The Kitchen.
> Rena is a new character — all sprite and CG art must be generated from scratch.

---

## Scene Overview

| Scene | Label | Category | Existing BG | New BG | CG Count | Priority |
|---|---|---|---|---|---|---|
| First Day | `cul_first_day` | Story | `kitchen` | No | 1 | **High** |
| Saturday Service | `cul_task_1` | Story | `pov_chef` | No | 1 | **High** |
| Knife Lesson | `cul_npc1_rena` | NPC | `kitchen` | No | 1 | Medium |
| After Service | `cul_npc2_rena` | NPC | `kitchen` | No | 1 | Medium |
| Promotion | `cul_review_commis` | Story | `kitchen` | No | 0 (sprite only) | Low |
| Service Rush | `wev_cul_service_rush` | Work Event | `pov_chef` | No | 0 | Low |
| Ingredient Shortage | `wev_cul_ingredient_shortage` | Work Event | `kitchen` | No | 0 | Low |
| Dish Criticism | `wev_cul_dish_criticism` | Work Event | `kitchen` | No | 0 | Low |

**No new backgrounds required.** All scenes use `kitchen` and `pov_chef`.

---

## Existing Backgrounds

| File | Used in | Notes |
|---|---|---|
| `kitchen` | Prep and quiet scenes | The kitchen before/between services |
| `pov_chef` | During service scenes | MC's active station POV during service |

---

## CG Plans

### CG 1: `cul_first_day_station.png`
**Scene:** `cul_first_day`
**Purpose:** Establishing shot. MC at station three, the box of onions in front of them, Rena visible at the pass in the background — watching without watching.

**Camera:** MC's station in the mid-foreground. Rena at the pass in the background.

**Framing:** Station three: cutting board, mise en place containers, the onion box. MC's hands in frame (no face — POV-adjacent). In the background, Rena at the pass — turned away, working, but her peripheral awareness is implicit.

**Characters:**
- Rena: at the pass, back mostly to the camera. She's at work, not performing evaluation — but her presence here means something.
- MC: hands visible on the station, no face.

**Environment:** Professional kitchen interior — stainless steel surfaces, pendant lighting, mise en place containers in rows, a hanging rack of pans. Clean before service. Functional, not stylised.

**Lighting:** Kitchen overhead lighting — bright, cool-white, industrial. No romanticism. The kitchen looks like a kitchen.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Professional kitchen interior before service. Stainless steel prep stations, hanging pan racks, industrial overhead lighting — cool, bright, no shadows. In the foreground: a prep station with a wooden cutting board, a box of onions, and mise en place containers. MC's hands visible on the surface (no face). In the middle-to-far background: the pass — a stainless steel service counter. A woman (Rena, late 30s) works at the pass with her back mostly to camera — purposeful, efficient. She is not watching MC directly, but her presence suggests peripheral awareness. The kitchen is clean and set up for service — nothing is out of place.
```

---

### CG 2: `cul_task_1_service_chaos.png`
**Scene:** `cul_task_1`
**Purpose:** The moment the Saturday service breaks — MC's station during a surge, plating in progress, time pressure made visible.

**Camera:** Station-level angle — from the side, slightly low, looking along the line.

**Framing:** MC's station in the foreground — several plates in mid-plate, the expeditor's window in the background with tickets. Sense of density and pressure without becoming illegible.

**Characters:**
- MC: visible from the side, working at the station. No face — body language communicates urgency.

**Environment:** The kitchen in service — hotter register than CG 1. Steam from pans, tickets at the window, activity in the background. The camera angle should show the physical reality of being on the line.

**Lighting:** Kitchen overhead plus stove/range heat light — warmer, more active than the prep scene.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Professional kitchen during dinner service — hotter, more active register than prep. Side-angle view along the line. In the foreground: a prep/plating station — several plates in mid-assembly, sauce ladle, garnish components. A figure (MC) works the station from the side, body language indicating urgency (slightly forward, focused). No face visible. Background: the expeditor's window with paper tickets, activity at other stations, steam from pans. The overhead lighting is the same bright industrial as before, but the environment reads hotter — movement, steam, the density of service pressure.
```

---

### CG 3: `cul_npc1_knife_lesson.png`
**Scene:** `cul_npc1_rena`
**Purpose:** Rena demonstrating knife grip — the one-time show before stepping back. The physical transmission of craft. The most character-specific image in the arc.

**Camera:** Close-medium shot. Rena's hands in the foreground with the knife and vegetable, MC watching from slightly behind.

**Framing:** Rena's hands dominant in frame — the knife hold is the content. Rena partially visible above her hands. MC visible behind her, watching closely.

**Characters:**
- Rena: visible from the mid-torso up. Chef's whites or kitchen clothing. Her hands are the focus — the grip is precise, the demonstration economical.
- MC: behind Rena, watching. Only partially visible.

**Expressions:**
- Rena: focused on the demonstration, not on MC. She's not performing — she's doing it right so it can be seen.

**Environment:** Kitchen pre-service. The station she was working at — one vegetable on the board, knife in hand.

**Lighting:** Kitchen overhead, standard. The hands are clearly lit — no shadow obscuring the grip detail.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Professional kitchen, pre-service. Close-medium shot — in the foreground, a woman's hands (Rena, late 30s) hold a chef's knife in a precise grip, mid-demonstration over a cutting board with a vegetable. The grip is the visual content: correct, deliberate, not showy. Rena's face and upper body are partially visible above the hands — focused on what she's demonstrating, not on the viewer. Behind her, slightly out of focus: MC watching closely (back or three-quarter angle). Kitchen background: stainless steel, overhead lighting, mise en place. The image is a tutorial made visual — skilled hands transmitting knowledge.
```

---

### CG 4: `cul_npc2_after_service.png`
**Scene:** `cul_npc2_rena`
**Purpose:** After service, late. Rena breaking down her station, MC doing the same. The quiet after the rush — the most human Rena gets.

**Camera:** Medium wide. Both figures visible at adjacent stations, working in parallel. No eye contact — they're talking while working.

**Framing:** Two figures at the pass or side-by-side stations, working — wiping down steel, storing containers. The kitchen is clean and dim compared to service. The conversation is happening in the gap between tasks.

**Characters:**
- Rena: at her station, side-on. Still in chef's clothing, slightly undone from service (apron down, sleeves possibly rolled). Not performing rest, just de-escalating.
- MC: at the adjacent station, parallel. Back or three-quarter.

**Expressions:**
- Rena: less managed than during service. The posture of someone at the end of a long, successful day — not relaxed exactly, but down from the service register.

**Environment:** The kitchen after service. Lights dimmed slightly (some overhead off). Surfaces clean. The specific quiet of a kitchen after everyone's gone.

**Lighting:** Fewer overheads than service. Quieter, slightly warmer — the practical lights stay on, the task lights go off.

**Generation prompt:**
```
Visual novel CG, 16:9 landscape, digital illustration. Professional kitchen after evening service — lights partially dimmed, most activity done. Two figures working at adjacent stations, side by side. On the left: Rena (late 30s, chef's clothing, apron partially off or down from service) wipes down a stainless steel surface — her posture is the post-service register, de-escalated from the kitchen intensity but not yet relaxed. On the right: MC (three-quarter angle, back mostly to camera) doing the same at their station. They are talking but not making eye contact — both looking at their work. The kitchen is clean, quiet, after-midnight in character even if it's not that late. Fewer overheads on. The specific stillness of a professional kitchen after the last plate went out.
```

---

## Character Visual Consistency — Rena

New character. Establish in CG 1 or CG 3 (knife lesson) and maintain across all assets.

- **Age:** Late 30s
- **Build:** Physically capable, kitchen-practical. Not described beyond that.
- **Clothing:** Chef's whites or kitchen chef clothing. No ornamentation — functional. Apron in service scenes; partially removed in post-service scenes.
- **Hair:** Practical — tied back, chef hat optional. Consistent across all scenes.
- **Expression range:** Evaluating (default in early scenes), demonstrating/focused (knife lesson), post-service/de-escalated (after service CG). Her approval is rare and will show as the absence of correction rather than visible warmth.
- **Hands:** Visible in multiple CGs — consistent nail style (short, unpolished — kitchen standard).

## Sprite Requirements

- `rena_normal` — default evaluating expression, arms at sides or crossed
- `rena_focused` — looking at food/station, used during cooking direction
- Establish look in CG 3 (knife lesson, clearest hands + face shot) to use as reference for sprite.

## Generation Priority

1. `cul_npc1_knife_lesson.png` — best face/hand reference for establishing Rena's look; no new BG needed
2. `cul_npc2_after_service.png` — most emotionally significant; uses `kitchen` BG
3. `cul_first_day_station.png` — establishing shot; Rena in background so lower face detail required
4. `cul_task_1_service_chaos.png` — no Rena; MC-only; lower priority, atmospheric value
5. Sprite art (`rena_normal`, `rena_focused`) — after CG 1 face lock
