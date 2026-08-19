# Next Visual Generation Pack

Planning-only. Production briefs, **not** final image prompts. No code/declarations/scenes changed.
The owner generates all assets separately; nothing here is wired into the game.

**Visual structure rule:** only two structures exist in this project — (A) background + layered sprite, or (B) complete cinematic CG with the relevant character(s) fully composed in. Do not generate: empty table plates, prop-only POV images, MC-hands-over-object shots, or any CG without the relevant character present. MC may be absent, shown from behind, or partially visible — never face-forward unless established convention allows it.

---

## Pending code changes (implement before or alongside generation)

These code edits are required to wire the generation plan. **Planning only — not yet implemented.**

| # | File | Change | Status |
|---|---|---|---|
| C1 | `home_scenes.rpy` l.156 (Martha dinner) | `scene cg_home_dinner_table with dissolve` → `scene expression home_bg()` | Pending |
| C2 | `home_scenes.rpy` l.177 (Nora dinner) | same swap | Pending |
| C3 | `home_scenes.rpy` l.199 (Zoe dinner) | same swap | Pending |
| C4 | `home_scenes.rpy` l.220 (Marcus dinner) | same swap | Pending |
| C5 | `home_scenes.rpy` l.240 (Lena dinner) | same swap | Pending |
| C6 | `home_scenes.rpy` l.264 (Kai dinner) | same swap | Pending |
| C7 | `home_scenes.rpy` l.287 (Eli dinner) | `scene cg_home_dinner_table with dissolve` → `scene cg_eli_home_dinner with dissolve` | Pending (requires file from generation #1) |
| C8 | `images.rpy` | Add declaration for `cg_eli_home_dinner` → `"images/scenes/home/cg_eli_home_dinner.png"` | Pending (after file exists) |
| C9 | `images.rpy` | Remove unused `cg_home_dinner_table` declaration | Pending (after C1–C7 are done) |

---

## Compact generation table

Ordered within each tier by dependency: sprite → CG.

### Tier 1 — Runtime blockers (generate or fix first)

| Order | Filename | Type | Priority | Scene/Hook | Existing/Missing | Resolution |
|---|---|---|---|---|---|---|
| — | `scenes/home/home_dinner_guest_table.png` | ~~cinematic CG~~ | ~~P0~~ | `home_dinner_scene_×7` | **Rejected** — character-less prop plate | **Code fix** (planning only): replace `scene cg_home_dinner_table` with `scene expression home_bg()` in 6 dinner labels; Eli's dinner gets `cg_eli_home_dinner` (see #1 below) |
| 1 | `scenes/home/cg_eli_home_dinner.png` | cinematic CG | **P0** | `home_dinner_scene_eli` | Missing | Generate — strongest dinner scene; `eli_dinner_done` milestone flag |
| 2 | `scenes/home/home_nora_coffee_machine.png` | cinematic CG | **P0** | `home_nora_coffee_scene` | **Missing (referenced)** | Generate |
| 3 | `scenes/home/home_zoe_guitar_session.png` | cinematic CG | **P0** | `home_zoe_guitar_scene` | **Missing (referenced)** | Generate |
| 4 | `scenes/home/home_eli_side_project_desk.png` | cinematic CG | **P0** | `home_eli_side_project_scene` | **Missing (referenced)** | Generate |
| 5 | `scenes/elle_portugal_payoff/cg_elle_portugal_turn.png` | branch CG | P1 | `scene_elle_portugal_payoff` | **Missing (referenced)** | Generate |
| 6 | `scenes/sam_marcus_crossover/cg_sam_marcus_court.png` | branch CG | P1 | `scene_sam_marcus_court` | **Missing (referenced)** | Generate |
| — | `locations/gym_reception.png` | background | P0 | `scene gym_reception` (every gym entry) | **Fixed** — renamed `gym_reception_random.png` → `gym_reception.png` | No generation needed |

### Tier 2 — Visual continuity (generate after Tier 1)

Not broken at runtime, but visible continuity gaps.

| Order | Filename | Type | Priority | Scene/Hook | Existing/Missing | Why needed |
|---|---|---|---|---|---|---|
| 7 | `characters/rena/rena_normal.png` | character sprite | P1 | culinary arc (5 labels) | Missing (Rena unillustrated) | Only sprite-less career mentor |
| 8 | `characters/dr_lena/drlena_casual_normal.png` | character sprite (outfit) | P1 | `scene_lena_romance_open`, `home_dinner_scene_lena` | Missing | Lena in scrubs at bar/home — outfit continuity break |

### Optional — Career CGs (blocked on scene specs)

**Do not generate yet.** Each needs a defined scene, player choice, consequence, CG beat, outfits, and character positions before generation. Generating before that produces an image that may not fit the implementation.

| Filename | Career | Blocker |
|---|---|---|
| `locations/kitchen_service_line.png` | Culinary | Scene specs needed; bg only (lower risk) |
| `scenes/career_culinary/cul_npc1_rena_mentor.png` | Culinary | Needs Rena sprite (#7) + scene spec |
| `scenes/career_hospital/hosp_difficult_case.png` | Hospital | Scene spec needed |
| `scenes/career_gym/tr_form_correction.png` | Trainer | Scene spec needed |
| `scenes/caroline_romance_open/cg_caroline_romance_open.png` | — | Scene spec needed |
| `scenes/lena_romance_open/cg_lena_romance_open.png` | — | Needs Lena off-duty sprite (#8) + scene spec |

---

## Production briefs — Tier 1 (runtime blockers)

### 1 — `scenes/home/home_dinner_guest_table.png` (shared home-dinner CG)
- **Type/priority:** cinematic CG · **P0** · broken reference
- **Hook:** shared by `home_dinner_scene_{martha,nora,zoe,marcus,lena,kai,eli}` (7 scenes).
- **Trigger / flags:** `home_dinner_invite_menu` → invite NPC (`home_invite_available` aff≥20/trust≥15), 3h.
**REJECTED** — character-less prop plate shared across 7 different guests violates the two-structure rule. Removed from generation.

**Code fix (planning only):** in `home_scenes.rpy`, change `scene cg_home_dinner_table with dissolve` to `scene expression home_bg()` in dinner labels for Martha (l.156), Nora (l.177), Zoe (l.199), Marcus (l.220), Lena (l.240), Kai (l.264). For Eli (l.287), change to `scene cg_eli_home_dinner with dissolve` (see #1 below); fall back to `home_bg()` until the file exists.

**Dinner scene evaluation:** only one of the seven dinners warrants a CG. Eli's dinner carries a `add_relationship_memory` call, an `eli_dinner_done` milestone flag, and a bookend motif (the jasmine rice). The other six guests' dinners are sufficiently served by `home_bg()` + NPC sprite.

### 1 — `scenes/home/cg_eli_home_dinner.png`
- **Type/priority:** cinematic CG · **P0** · new (replaces the rejected shared plate for Eli's dinner)
- **Hook:** `home_dinner_scene_eli`; `eli_dinner_done` milestone; `add_relationship_memory("eli","eli_home_dinner","The rice")`.
- **Characters / outfit:** **Eli (`eli_normal`) is the subject.** Eli at the dinner table, talking. The jasmine rice packet is visible on the counter in the background — the scene's bookend motif.
- **Location / time:** player apartment dining area; evening.
- **Camera / framing:** Eli across the table, mid-conversation. Normal cinematic camera — not POV, not prop-only. MC absent or barely implied (empty seat/table edge). No MC face.
- **Purpose:** the only dinner that earns a CG — the "I like it here" moment. **If not:** Eli's dinner falls back to `home_bg()` + sprite (acceptable but loses the visual beat).

### 2 — `scenes/home/home_nora_coffee_machine.png`
- **Type/priority:** cinematic CG · **P0** · broken reference
- **Hook:** `home_nora_coffee_scene` (commitment `nora_coffee_1`); sets `home_coffee_calibrated`.
- **Characters / outfit:** **Nora (`nora_casual_normal`) is the subject** — at the espresso machine, mid-demonstration. This is Nora's scene; she owns the frame.
- **Location / time:** player apartment kitchen counter (NOT the office `nexus_coffee_machine`); morning light.
- **Camera / framing:** Nora at the machine explaining, animated, coffee-gear visible. MC may be absent or shown as a listening presence behind her — no MC face. Do not design a prop-only coffee-machine shot.
- **Purpose:** relationship memory + espresso lifestyle. **If not:** scene broken.

### 3 — `scenes/home/home_zoe_guitar_session.png`
- **Type/priority:** cinematic CG · **P0** · broken reference
- **Hook:** `home_zoe_guitar_scene`.
- **Characters / outfit:** **Zoe (`zoe_street_neutral`) is the subject** — seated with a sketchbook, watching, while MC plays guitar. Zoe's expression and posture are the emotional content of the CG (sceptical → quietly engaged).
- **Location / time:** apartment living area, couch/floor; evening.
- **Camera / framing:** Zoe in foreground watching, sketchbook visible; guitar-playing implied from her sightline. Do not make this a prop-only guitar image. No MC face if MC is partially visible.
- **Purpose:** relationship memory — the shift from "prove it isn't furniture" to silence. **If not:** scene broken.

### 4 — `scenes/home/home_eli_side_project_desk.png`
- **Type/priority:** cinematic CG · **P0** · broken reference
- **Hook:** `home_eli_side_project_scene`; the collaborative debugging session.
- **Characters / outfit:** **Eli (`eli_normal`) is the subject** — at a desk with a laptop/screens, focused on the problem. MC present as a second figure beside him; both looking at screens.
- **Location / time:** apartment desk; evening/night; screen glow.
- **Camera / framing:** both figures over the desk, screens lit, code or hardware visible. Eli is the closer/more prominent figure. MC shown from behind or side — no MC face.
- **Purpose:** relationship memory; ties to the Eli IT/hardware thread. **If not:** scene broken.

### 5 — `scenes/elle_portugal_payoff/cg_elle_portugal_turn.png`
- **Type/priority:** branch CG · P1 · broken reference (declared, has "needs generation" note)
- **Hook:** `scene_elle_portugal_payoff`.
- **Trigger / flags:** `elle_decision_pending` + `npc_talkable("elle")` at beach; after pier + `elle_abroad_revealed`.
- **Characters / outfit:** **Elle (`elle_sundress_normal`) is the subject** — the "turn back toward you" moment. Elle turning or mid-turn, golden-hour beach behind her.
- **Location / time:** beach; golden hour / late afternoon light.
- **Camera / framing:** Elle is the full subject of the frame. MC absent or implied only by her eyeline. No MC face. Normal cinematic framing — not POV, not a background-only beach shot.
- **Purpose:** sole payoff of the `elle_abroad_revealed` arc thread. **If not:** the game's only unresolved arc has no visual payoff.

### 6 — `scenes/sam_marcus_crossover/cg_sam_marcus_court.png`
- **Type/priority:** crossover CG · P1 · broken reference (declared, has "needs generation" note)
- **Hook:** `scene_sam_marcus_court`.
- **Trigger / flags:** `sam_marcus_scene_pending` + `npc_here("sam")` + `npc_here("marcus")`.
- **Characters / outfit:** **Both Sam and Marcus must be recognizably present and identifiable in the frame** — Sam in sport outfit, Marcus in park/casual. This is a two-character CG; neither character may be absent, cropped out, or reduced to a silhouette.
- **Location / time:** basketball court; day. The court is context, not the subject.
- **Camera / framing:** Sam and Marcus as the two central figures — passing, talking, or mid-play together. MC absent or as a distant observer silhouette. Do not generate an empty-court or ball-only shot.
- **Purpose:** relationship crossover payoff. **If not:** crossover has no visual payoff.

---

## Production briefs — Tier 2 (visual continuity)

### 7 — `characters/rena/rena_normal.png`
- **Type/priority:** character sprite · P1
- **Hook:** `cul_first_day`, `cul_task_1`, `cul_npc1_rena`, `cul_npc2_rena`, `cul_review_commis` — scenes exist, sprite-less. Owner would set `NPC_DATA["rena"]["sprite"]`.
- **Trigger / flags:** culinary shifts (`job_id=="culinary"`); `rena_met`, `cul_*` progression.
- **Characters / outfit:** Rena; chef whites / apron, hair tied. Mentor archetype, authoritative.
- **Identity refs:** none yet — canonical look established here.
- **Camera / framing:** standing 3/4 full-body portrait, transparent PNG, feet-anchored (~1024×1535). No background.
- **Purpose:** career-mentor identity. **MC visible:** no. **Reuse:** very high. **If not:** culinary is the only sprite-less career; 5 scenes stay text-on-kitchen.

### 8 — `characters/dr_lena/drlena_casual_normal.png`
- **Type/priority:** character sprite (outfit variant) · P1
- **Hook:** `scene_lena_romance_open` (bar), `home_dinner_scene_lena` — exist. Owner adds to `NPC_DATA["lena"]["sprites"]["casual"]`.
- **Trigger / flags:** `lena_shoulder_done`, aff≥55/trust≥55 at bar; home dinner invite.
- **Characters / outfit:** Lena; smart-casual/evening off-duty (NOT scrubs). Same face/hair/skin as `drlena_normal`.
- **Identity refs:** reuse `drlena_normal`.
- **Camera / framing:** standing 3/4 portrait, transparent PNG, sprite framing.
- **Purpose:** fixes scrubs-in-social continuity. **MC visible:** no. **Reuse:** medium-high. **If not:** Lena wears scrubs at bar/home — persistent continuity break.

---

## Production briefs — Optional career CGs (blocked on scene specs)

**Do not generate until each has a written scene, player choice, consequence, exact CG beat, outfit list, and character positions.** Generating without a spec risks an image that doesn't fit the implementation.

- **`locations/kitchen_service_line.png`** — Culinary bg (lower risk; no character positioning). The pass mid-service: heat, steam, tickets. Reusable across 5 labels + 3 work events.
- **`scenes/career_culinary/cul_npc1_rena_mentor.png`** — Needs Rena sprite (#7) first. `cul_npc1_rena` scene; Rena + MC at the pass, a correction beat.
- **`scenes/career_hospital/hosp_difficult_case.png`** — Hospital hard-case beat (scene TBD). Lena + MC over chart/bedside; no patient face.
- **`scenes/career_gym/tr_form_correction.png`** — Trainer coaching beat (scene TBD). MC-as-trainer correcting form; POV hands.
- **`scenes/caroline_romance_open/cg_caroline_romance_open.png`** — `scene_caroline_romance_open`; the "opens by a degree" bar moment. Caroline in work clothes.
- **`scenes/lena_romance_open/cg_lena_romance_open.png`** — Needs Lena off-duty sprite (#8) first. The held-breath bar beat.

---

## Assets intentionally rejected as unnecessary
- **`home_dinner_guest_table.png`** — character-less shared prop plate; violates project visual structure. Code fix replaces it (see §1 above).
- **Martha dinner CG** — the weakest dinner scene; no milestone flag, no memorable beat. bg+sprite.
- **Any other per-guest dinner CG beyond Eli** — all five remaining dinners (Nora, Zoe, Marcus, Lena, Kai) are short warmth beats adequately served by bg+sprite. Nora and Zoe already have home CGs from separate scenes.
- **Elle romance-open CG** — Elle is already visually rich (pier 1–7 + portugal CG); correct sundress sprite is enough.
- **More expression sprites** (`*_talk/_laugh/_angry/_sad`) for any NPC — ~40 already exist unused.
- **Kiss CGs for non-romanceable NPCs** — `sam_kiss.png`/`eli_kiss.png` exist physically but there is no first-kiss path for them; do not wire or generate more.
- **Interaction/base art for template characters** (adeyemi, anna, vera, theo, bradley, dr_grant, ray, mila) — not in `NPC_DATA`, no gameplay use.
- **Additional corporate CGs** — career is saturated (18 CGs).
- **Prop-only POV images, empty interaction plates, MC-hands-over-object shots** — not valid visual structures in this project.

## Scenes that should remain background + sprites (no CG)
- All home dinner scenes except Eli's.
- Romance **reopen** scenes (`scene_nora/zoe/martha_romance_reopen`) — dialogue-driven.
- `scene_elle_romance_open` — correct outfit + rich existing beach art.
- `scene_caroline_romance_open` — sprite-adequate (CG only if distinctiveness is wanted → optional).
- Everyday greet / talk / gift / number / hug-text interactions.

## Unclear references requiring owner confirmation
1. Confirm `home_dinner_scene_eli` is reachable (the `eli_dinner_done` flag and `eli_home_dinner` memory suggest it is production-ready, but the scene is not otherwise gated differently from the other 6).
2. `elle_pier_7.png` exists but only frames 1–6 are declared/shown — wire frame 7 or spare?
3. Undeclared interaction images (`adeyemi/anna/vera` `_kiss`/`_hug`, `sam_kiss`, `eli_kiss`) — planned characters or leftovers?
4. `grounds_backrooms.png`, `map_marked.png`, `drlena.png` — keep, wire, or discard?

---

### Planning-pass confirmation
- No gameplay code modified · No new scenes written · No image declarations added · No invented asset referenced in gameplay · Planning-only.
