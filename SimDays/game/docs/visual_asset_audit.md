# Visual Asset Audit — LivingTheDream

Planning-only pass. No code, declarations, scenes, or files were changed.

Method: parsed every declaration in `images.rpy` (static `image` + dynamic
`renpy.image`/loop templates), expanded loop-generated paths, and tested each
against the physical asset tree (`images/` → junction to
`LivingTheDream/images/`). Usage confirmed by grepping `scene`/`show`/name
references across all `.rpy` files.

Status legend per reference: **DECLARED** (in images.rpy), **USED** (referenced
by a scene/label), **FILE OK** (physical file confirmed), **FILE MISSING**
(declared/used but no file), **CONFIRM** (ambiguous — owner decision needed).

---

## 1. Files & folders reviewed

- `game/images.rpy` — 104 static `image` decls + ~140 dynamic/loop-generated (≈247 concrete paths expanded & checked)
- `images/locations/` (89 files), `images/characters/*/` (20 folders), `images/scenes/*/` (31 folders), `images/ui/` (zone icons)
- Scene/usage sources: `locations.rpy`, `gameplay_expansion_scenes.rpy`, `home_scenes.rpy`, `culinary_arc.rpy`, `it_arc.rpy`, `hospital_arc.rpy`, `trainer_arc.rpy`, `corporate_work.rpy`, `careers.rpy`, `arcs.rpy`, `group_scenes.rpy`, `work_events.rpy`

Cross-check result: **247 expected paths, 7 concrete FILE MISSING** (rest OK).

---

## 2. Missing referenced assets (declared + USED, FILE MISSING)

These are **active references that resolve to no file** — the scene shows a
broken/placeholder image at runtime.

| Ref (image name) | File path (missing) | Used by | Severity | Resolution |
|---|---|---|---|---|
| `cg_home_dinner_table` | `scenes/home/home_dinner_guest_table.png` | `home_dinner_scene_{martha,nora,zoe,marcus,lena,kai,eli}` | **P0** | **Code fix** — replace `scene cg_home_dinner_table` with `scene expression home_bg()` in all 7 dinner labels (planning only; see §2a) |
| `cg_home_nora_coffee` | `scenes/home/home_nora_coffee_machine.png` | `home_nora_coffee_scene` | **P0** | Generate CG (character + activity; see generation pack) |
| `cg_home_zoe_guitar` | `scenes/home/home_zoe_guitar_session.png` | `home_zoe_guitar_scene` | **P0** | Generate CG (character + activity; see generation pack) |
| `cg_home_eli_desk` | `scenes/home/home_eli_side_project_desk.png` | `home_eli_side_project_scene` | **P0** | Generate CG (character + activity; see generation pack) |
| `cg_elle_portugal_turn` | `scenes/elle_portugal_payoff/cg_elle_portugal_turn.png` | `scene_elle_portugal_payoff` | **P1** | Generate CG (has "needs generation" note) |
| `cg_sam_marcus_court` | `scenes/sam_marcus_crossover/cg_sam_marcus_court.png` | `scene_sam_marcus_court` | **P1** | Generate CG (has "needs generation" note) |
| `gym_reception` | `locations/gym_reception.png` | `scene gym_reception` (every gym entry) | — | **Fixed** — renamed `gym_reception_random.png` → `gym_reception.png` |

### §2a — Home dinner scenes: code fix + CG evaluation

`cg_home_dinner_table` is a character-less prop plate shared across 7 different guests. That concept violates the project's two visual structures (bg+sprite or complete character CG). **Resolution: replace with `scene expression home_bg()` + NPC sprite.** No generation needed for the shared plate.

**Per-scene evaluation** (read against `home_scenes.rpy`):

| Guest | Scene content | Meaningful choice / emotional payoff | bg+sprite sufficient? | CG candidate? |
|---|---|---|---|---|
| Martha | Compliment on organisation; "don't tell Caroline" | Weak; small warmth beat only | Yes | No |
| Nora | Kitchen takeover, wine for deglazing | Moderate; personality-revealing | Yes — she has the coffee CG | No |
| Zoe | Mystery bottle; staying longer vs. project chat | Moderate | Yes — she has the guitar CG | No |
| Marcus | Two portions; funny construction story | Low; slice-of-life only | Yes | No |
| Lena | Post-shift in scrubs; `kitchen_lena_extended` branch | Moderate; "just pour her a drink" | Yes | No — hospital arc is already CG-rich |
| Kai | Protein math; "same time next week" | Low-moderate | Yes | No |
| **Eli** | Jasmine rice bookend; "I like it here" · 3-way choice · `add_relationship_memory("eli","eli_home_dinner","The rice")` · `eli_dinner_done` flag | **High** — memory tag, milestone flag, bookend motif | bg+sprite is the fallback | **Yes — one CG warranted** |

**Recommendation:** one CG for Eli's dinner — `scenes/home/cg_eli_home_dinner.png`. Eli at the dinner table, jasmine rice packet visible on the counter. The scene's visual identity is the rice; bake it into the composition. All other 6 dinner guests: `scene expression home_bg()` + sprite.

**Code change required (planning only):** in `home_scenes.rpy` lines 156, 177, 199, 220, 240, 264 — change `scene cg_home_dinner_table with dissolve` to `scene expression home_bg()`. For Eli's dinner (line 287), change to `scene cg_eli_home_dinner with dissolve` (once the file exists) or fall back to `home_bg()` until then.

---

## 3. Placeholder / incorrect visual reuse

- **`gym_reception` name mismatch — resolved.** Declaration expected `locations/gym_reception.png`; physical file was `gym_reception_random.png`. Renamed the file. No generation needed.
- **Lena in scrubs in private/social contexts.** `home_dinner_scene_lena` and the new `scene_lena_romance_open` (bar, dialogue says "off shift") both show `drlena_normal` (hospital scrubs). Reads as an asset limit, not intent. → needs a Lena off-duty sprite (§6).
- **Nora/Kai home-outfit issue — already fixed** this session (home scenes now use `nora_casual_*` / `kai_normal`). No action.
- No scenes were found using an *unrelated* placeholder background (e.g. a café bg standing in for a bar). Generic-but-acceptable reuse (`scene kitchen`, `scene bar`) is covered under §7 career parity.

---

## 4. Declared-but-unused images (headroom, NOT gaps)

Expression variants declared + FILE OK but never `show`n: `*_talk / *_laugh /
*_angry / *_sad / *_surprised / *_determined / *_nervous` for nora, caroline,
drlena, natalie, elle, marcus, sam, eli, martha, kai (~40 sprites), plus Zoe
alt-outfit stills (`zoe_hoodie_smile`, `zoe_coat_smile`, `zoe_street_full`,
`zoe_street_surprised`). **No generation needed** — these are available emotion
beats for future dialogue. Not a problem to solve; do not regenerate.

## 4b. Physical-but-undeclared files (exist, no decl/use)

`characters/{adeyemi,anna,vera}/*_kiss.png` & `*_hug.png`, `sam_kiss.png`,
`eli_kiss.png`, `elle_pier_7.png` (frame 7 on disk; decl registers only 1–6),
`grounds_backrooms.png`, `map_marked.png`, `dr_lena/drlena.png`, and various
`*_template.*`. → owner CONFIRM (§9); none block current content.

---

## 5. Important scenes relying on generic background + dialogue only

| Scene | Current visual | Assessment |
|---|---|---|
| Culinary arc (`cul_first_day`, `cul_task_1`, `cul_npc1_rena`, `cul_npc2_rena`, `cul_review_commis`) + 3 work events | `scene kitchen` / `scene pov_chef` only, **no sprite, no CG** | **Weakest in game** (§7) |
| `scene_caroline_romance_open` | `scene bar` + `caroline_normal` | Sprites acceptable; not visually distinct from `caroline_thursday_bar` (§8) |
| `scene_lena_romance_open` | `scene bar` + `drlena_normal` (scrubs) | Outfit wrong for "off shift" (§8) |
| `scene_elle_romance_open` | beach bg + `elle_sundress_normal` | Acceptable; Elle already visually rich (§8) |
| Romance reopen scenes (nora/zoe/martha) | existing bg + sprites | Dialogue-driven; correctly sprite-only, no CG needed |

---

## 6. Outfit variants needed

| NPC | Have | Missing | Impact if not generated |
|---|---|---|---|
| **Dr. Lena** | scrubs only (`drlena_*`) | **off-duty (casual/evening)** | `lena_romance_open` (bar) & `home_dinner_scene_lena` keep showing scrubs in social settings — reads as asset limit |
| Rena (culinary mentor) | **none** | full base sprite (chef whites) | all 4 culinary NPC scenes stay sprite-less (§7) |
| Nora | cafe + casual | — | (fixed) |
| Kai | gym + casual | — | (fixed) |
| Martha | work + evening dress | — | covered |
| Caroline | corporate blazer | — (blazer-at-bar is narratively justified) | none |
| Elle | sundress + base | — | none |

Only **Lena off-duty** and **Rena base** are worth generating now.

---

## 7. Career visual parity

Ranking: **Corporate (reference) > Hospital ≈ Trainer ≈ IT (4 arc CGs each + extras) >> Culinary (0 CGs, no mentor sprite).**

### Corporate (reference — richest)
- **Backgrounds:** goodoffice1, mediumoffice1, pooroffice1, officelobby1, nexus_meeting_room, nexus_office_night, nexus_cafeteria_day, nexus_coffee_machine
- **Sprites:** Caroline (4 expr), Martha (work 5 + evening dress 4)
- **CGs:** 18 corporate arc CGs + martha corridor/gift/wardrobe
- **Covered:** first day, archive task, review, client call, credit lobby, lunch, overtime — saturated
- **Uncovered:** none critical · **Missing outfits:** none
- **Next high-value CG:** promotion/rank-up milestone CG (optional, saturated) · **Reusable:** already has nexus_cafeteria

### IT
- **Backgrounds:** hub_day, hub_night, hub_pov · **Sprites:** Eli (normal/talk/laugh/nervous)
- **CGs:** 4 arc (first day / bug terminal / PR comments / late deploy) + cg_eli_deploy_hug + cg_eli_hardware + cg_eli_zoe_collab
- **Covered:** intro, debugging, PR review, deployment pressure — good
- **Uncovered:** no "team crunch war-room" wide shot (minor) · **Missing outfits:** none material (Eli reads consistent)
- **Next high-value CG:** deploy-night war-room / multi-screen crunch (optional) · **Reusable:** hub_night already covers late-night

### Hospital
- **Backgrounds:** hospital1, hospital_exam, hospital_night, hospital_break_room(+_day), hospital_rooftop_night, doctor_pov · **Sprites:** Dr. Lena (4, scrubs only)
- **CGs:** 4 arc (ward walk / intake / rounds / break room) + lena_rooftop (5) + lena_shoulder + kitchen_lena_extended (2)
- **Covered:** movement through ward, intake, rounds, break, rooftop — good
- **Uncovered:** a **difficult-case / patient-recovery** dramatic beat (the "responsibility/recovery" theme has no CG) · **Missing outfits:** Lena off-duty
- **Next high-value CG:** difficult-case-then-recovery CG · **Reusable:** recovery-ward corridor bg (extends hospital1)

### Culinary — WEAKEST
- **Backgrounds:** `kitchen`, `pov_chef` only · **Sprites:** **none (Rena unillustrated)** · **CGs:** **zero**
- **Covered visually:** nothing beyond a generic kitchen still
- **Uncovered:** first day, mentor moments (cul_npc1/2_rena), service rush, plating/criticism — all text-on-kitchen
- **Missing outfits:** Rena base sprite (chef whites) · a **service-line/pass** background (heat, movement, service pressure) and a "quiet kitchen after service" beat
- **Next high-value CG:** `cul_npc1_rena` mentor moment (requires Rena sprite first) · **Reusable:** **service-line/pass background** — unlocks all 5 cul labels + 3 work events

### Trainer
- **Backgrounds:** pov_trainer, pov_gym_weights, gym_cardio, gymdaypeople/nopeople, (gym_reception → see §3) · **Sprites:** Kai (casual 4 + gym 1)
- **CGs:** 4 arc (shadow / solo session / planning / after-last-session) + sam_gym (7)
- **Covered:** shadowing, solo coaching, planning, client progress — good
- **Uncovered:** a **hands-on physical-correction** coaching beat (the "physical correction" theme has no CG) · **Missing outfits:** none
- **Next high-value CG:** form-correction coaching CG (needs scene spec first) · **Reusable:** `gym_reception` fixed (renamed)

---

## 8. Recommended CGs for Caroline / Lena / Elle (romance-opening scenes)

| Scene | Deserves a CG? | Strongest visual moment | Sprites enough? | Outfit correct? | Extra prerequisite? | Visually distinct? |
|---|---|---|---|---|---|---|
| `scene_caroline_romance_open` | **Later / optional** | She sets the glass down; posture "opens by a degree" as she confirms | Yes, for now | Yes (work clothes, narratively justified) | No — pacing fine (needs `caroline_bar_done` + 65/60) | **No** — another bar shot with `caroline_normal`, not distinct from `caroline_thursday_bar`; a CG would help distinguish |
| `scene_lena_romance_open` | **Optional, after the sprite** | The held breath she lets out when you say it back | **No** — needs off-duty sprite (§6) | **No** (scrubs at a bar, "off shift") | No | Low — bar + scrubs; the off-duty sprite fixes this more cheaply than a CG |
| `scene_elle_romance_open` | **No (defer)** | Grin, then she looks back at the water | Yes | Yes (sundress, beach) | Consider raising 40/35 threshold or a 2nd prerequisite (flagged prior round) — Elle opens early | Low — Elle is already beach-heavy (pier 1–7 + portugal CG) |

Verdict: **none is required this pack.** Lena's real fix is the **off-duty
sprite** (already required, §6). Caroline's CG is the strongest optional
(distinctiveness). Elle needs nothing visual.

---

## 9. Unclear references requiring owner confirmation

1. **`home_dinner_scene_eli` reachability** — all 7 dinner scenes use the same `home_invite_available` gate (aff≥20/trust≥15); confirm Eli's is reachable and the `eli_dinner_done` flag is wired correctly.
2. **The 3 remaining `scenes/home/` CGs** — confirm the home coffee/guitar/eli-desk/dinner scenes are reachable in the current build and were intended to ship (no "pending" comment exists). If reachable, they are broken now.
3. **`elle_pier_7.png`** — a 7th pier frame exists on disk but only 1–6 are declared/shown. Should frame 7 be wired, or is it a spare?
4. **Undeclared interaction images** for `adeyemi`, `anna`, `vera` (`*_kiss/_hug`), and `sam_kiss` / `eli_kiss` — are these characters/interactions planned, or leftovers? Currently unused.
5. **`grounds_backrooms.png`, `map_marked.png`, `drlena.png`** — undeclared physical files; keep, wire, or discard?

---

## 10. Documentation paths

- `game/docs/visual_asset_audit.md` (this file)
- `game/docs/next_visual_generation_pack.md` (the prioritized generation pack + table)

---

### Planning-pass confirmation
- No gameplay code modified · No new scenes written · No image declarations added · No invented asset referenced in gameplay · Planning-only.
